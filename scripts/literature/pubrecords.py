"""Publication-metadata workflow for BioML-Insight (LIT-002).

Pipeline (see research/literature/collection_workflow.md):

  raw_exports/  --register-->  MANIFEST.csv (sha256, query_id, timestamp, route)
       |
       +--build--> records/source_records.jsonl   one record per retrieved hit, original kept verbatim
                   records/publications.jsonl     deduplicated publication records
                   records/dedup_review.csv       uncertain matches for manual decision
                   records/paper_id_registry.csv  append-only identifier -> paper_id map
                   records/build_report.json      counts, completeness, conflicts

Manual inputs that survive rebuilds:
  records/dedup_decisions.csv        paper_id_a,paper_id_b,decision(same|different),reviewer,date,note
  screening/decisions.csv            paper_id,stage,decision,reason_code,screener,date,justification
                                     (+ optional descriptor columns; schemas/screening_decision.schema.json)
  records/verification_overrides.csv paper_id,verification_status,note,reviewer,date
  records/fulltext_status.csv        paper_id,full_text_availability,note,date

Standard library only (plus optional jsonschema for schema validation).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import hashlib
import html
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

# --------------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------------
SOURCE_PRIORITY = ["pubmed", "europepmc", "crossref", "arxiv", "semantic_scholar", "consensus",
                   "publisher_site", "repository", "google_scholar", "citation_chasing", "web", "manual"]
AUTHORITATIVE_SOURCES = {"pubmed", "europepmc", "crossref", "arxiv"}
ROUTE_PRIORITY = ["eutils_api", "pubmed_connector", "structured_transcription"]
ROUTES = {"eutils_esearch", "eutils_efetch", "pubmed_connector_search",
          "pubmed_connector_metadata", "structured_transcription"}
MANIFEST_COLS = ["raw_file", "sha256", "query_id", "source", "route", "endpoint_or_tool",
                 "request_json", "retrieved_at", "n_items", "transcribed", "transcription_check",
                 "notes"]
# Search pages registered under "CHECK-<query_id>" are independent re-fetches used only to check
# the transcription of the original pages (check_search); they never become source records (LIT-003).
CHECK_PREFIX = "CHECK-"
ABSTRACT_PLACEHOLDER = re.compile(r"\[\s*abstract not available\s*\]\.?", re.I)
FUZZY_THRESHOLD = 0.90
SCREENING_STAGE_ORDER = {"title_abstract": 1, "full_text": 2}
# Screening decision file (LIT-004-WORKFLOW-FIXES). Kept in step with
# research/literature/schemas/screening_decision.schema.json (checked by a unit test).
SCREENING_REQUIRED = ["paper_id", "stage", "decision", "reason_code", "screener", "date", "justification"]
SCREENING_OPTIONAL = ["rq_tags", "tier", "scope_flags", "record_type", "dim_explainability",
                      "dim_uncertainty", "dim_calibration", "dim_independent_validation",
                      "criteria_version", "needs_human", "dim_feature_selection", "dim_classification"]
SCREENING_DECISIONS = ("include", "exclude", "uncertain", "abstract_only")   # "not_screened" = no row
SCREENING_ENUMS = {
    "stage": ("title_abstract", "full_text"),
    "decision": SCREENING_DECISIONS,
    "tier": ("", "1", "2", "3"),
    "record_type": ("", "original", "methodological", "software", "guideline", "review_lead", "preprint", "notice"),
    "dim_explainability": ("", "yes", "no", "unclear"),
    "dim_uncertainty": ("", "yes", "no", "unclear"),
    "dim_calibration": ("", "yes", "no", "unclear"),
    "dim_independent_validation": ("", "external", "temporal", "internal_only", "unclear"),
    "needs_human": ("", "yes", "no"),
    # D-032 (APPROVED - CONDITIONAL, inactive for screening until its dependencies are met):
    # RQ5 feature/biomarker-selection component
    "dim_feature_selection": ("", "yes", "no", "unclear"),
    # D-036 (Q-039; APPROVED - CONDITIONAL, inactive for screening): RQ5 classification component
    # (evidence definition: D-035 record section 2)
    "dim_classification": ("", "yes", "no", "unclear"),
}
# RQ5 components (D-031 to D-036). One status column each in screening/decisions.csv; the build
# derives the D-034 coverage group from the confirmed (full-text) statuses.
RQ5_COMPONENT_FIELDS = {"feature_selection": "dim_feature_selection", "classification": "dim_classification",
                        "explainability": "dim_explainability", "calibration": "dim_calibration",
                        "uncertainty": "dim_uncertainty"}
RQ5_RECORDED_FIELDS = list(RQ5_COMPONENT_FIELDS.values())
RESEARCHER = "researcher"   # screener value for the researcher (screening_protocol.md section 6)
REASON_CODE = re.compile(r"E(1[0-2]|[1-9])")
RQ_TAGS = re.compile(r"(RQ[1-6])(;RQ[1-6])*")


# --------------------------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------------------------
def normalize_doi(doi):
    if not doi:
        return None
    d = html.unescape(str(doi)).strip()
    d = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", d, flags=re.I)
    d = re.sub(r"^doi:\s*", "", d, flags=re.I)
    d = d.strip().rstrip(".").lower()
    return d if re.match(r"^10\.\d{4,9}/\S+$", d) else None


def normalize_pmid(pmid):
    if pmid is None:
        return None
    s = str(pmid).strip()
    return s if re.fullmatch(r"[1-9]\d{0,9}", s) else None


def normalize_pmcid(pmcid):
    if not pmcid:
        return None
    m = re.fullmatch(r"(?i)\s*(?:pmc)?(\d+)\s*", str(pmcid))
    return f"PMC{m.group(1)}" if m else None


def normalize_arxiv(arxiv_id):
    if not arxiv_id:
        return None
    s = str(arxiv_id).strip()
    s = re.sub(r"^(?:https?://)?(?:www\.)?(?:arxiv|alphaxiv)\.org/(?:abs|pdf)/", "", s, flags=re.I)
    s = re.sub(r"^arxiv:\s*", "", s, flags=re.I)
    s = re.sub(r"\.pdf$", "", s)
    s = re.sub(r"v\d+$", "", s)
    if re.fullmatch(r"\d{4}\.\d{4,5}", s) or re.fullmatch(r"[a-z\-]+(?:\.[A-Z]{2})?/\d{7}", s):
        return s
    return None


def strip_markup(text):
    if text is None:
        return None
    t = re.sub(r"<[^>]+>", " ", html.unescape(str(text)))
    return re.sub(r"\s+", " ", t).strip()


def normalize_title(title):
    """Matching key only; the original title is always kept separately."""
    if not title:
        return ""
    t = unicodedata.normalize("NFKD", strip_markup(title))
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def normalize_name(name):
    if not name:
        return ""
    t = unicodedata.normalize("NFKD", name)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z]", "", t)


def normalize_journal(j):
    return normalize_title(j)


def first_author_key(authors):
    for a in authors or []:
        last = a.get("last_name") or a.get("collective_name") or a.get("name", "").split(",")[0]
        if last:
            return normalize_name(last)
    return ""


def parse_year(value):
    if value is None:
        return None
    m = re.search(r"(1[89]\d{2}|20\d{2})", str(value))
    return int(m.group(1)) if m else None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


# --------------------------------------------------------------------------------------------
# Parsers: each returns metadata dicts with the original source object kept verbatim
# --------------------------------------------------------------------------------------------
def _empty_meta():
    return {"title": None, "authors": [], "year": None, "journal": None, "doi": None,
            "pmid": None, "pmcid": None, "arxiv_id": None, "source_url": None,
            "abstract": None, "publication_types": [], "language": None, "original": None}


def parse_connector_article(article):
    """One article object from the PubMed connector's get_article_metadata response."""
    m = _empty_meta()
    ids = article.get("identifiers") or {}
    m["title"] = strip_markup(article.get("title"))
    m["abstract"] = strip_markup(article.get("abstract")) or None
    if m["abstract"] and ABSTRACT_PLACEHOLDER.fullmatch(m["abstract"]):
        m["abstract"] = None   # PubMed placeholder, not an abstract (the original is kept verbatim)
    m["authors"] = [{"last_name": a.get("last_name"), "fore_name": a.get("fore_name"),
                     "initials": a.get("initials")} for a in article.get("authors") or []]
    pd = article.get("publication_date") or {}
    m["year"] = parse_year(pd.get("year"))
    j = article.get("journal") or {}
    m["journal"] = j.get("title") or j.get("iso_abbreviation")
    m["pmid"] = normalize_pmid(ids.get("pmid"))
    m["doi"] = normalize_doi(ids.get("doi") or article.get("doi"))
    m["pmcid"] = normalize_pmcid(ids.get("pmc"))
    m["publication_types"] = list(article.get("article_types") or [])
    m["language"] = article.get("language")
    if m["pmid"]:
        m["source_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{m['pmid']}/"
    m["original"] = article
    return m


def _text(el):
    return strip_markup("".join(el.itertext())) if el is not None else None


def parse_efetch_xml(xml_bytes):
    """PubmedArticleSet XML from E-utilities efetch (db=pubmed, retmode=xml)."""
    root = ET.fromstring(xml_bytes)
    out = []
    for art in root.iter("PubmedArticle"):
        m = _empty_meta()
        mc = art.find("MedlineCitation")
        a = mc.find("Article")
        m["pmid"] = normalize_pmid(_text(mc.find("PMID")))
        m["title"] = _text(a.find("ArticleTitle"))
        parts = []
        for ab in a.findall("Abstract/AbstractText"):
            label = ab.get("Label")
            txt = _text(ab)
            parts.append(f"{label}: {txt}" if label else txt)
        m["abstract"] = " ".join(p for p in parts if p) or None
        for au in a.findall("AuthorList/Author"):
            if au.find("CollectiveName") is not None:
                m["authors"].append({"collective_name": _text(au.find("CollectiveName"))})
            else:
                m["authors"].append({"last_name": _text(au.find("LastName")),
                                     "fore_name": _text(au.find("ForeName")),
                                     "initials": _text(au.find("Initials"))})
        m["journal"] = _text(a.find("Journal/Title")) or _text(a.find("Journal/ISOAbbreviation"))
        pubdate = a.find("Journal/JournalIssue/PubDate")
        year = None
        if pubdate is not None:
            year = parse_year(_text(pubdate.find("Year")) or _text(pubdate.find("MedlineDate")))
        if year is None:
            year = parse_year(_text(a.find("ArticleDate/Year")))
        m["year"] = year
        for aid in art.findall("PubmedData/ArticleIdList/ArticleId"):
            t = aid.get("IdType")
            if t == "doi" and not m["doi"]:
                m["doi"] = normalize_doi(aid.text)
            elif t == "pmc":
                m["pmcid"] = normalize_pmcid(aid.text)
        if not m["doi"]:
            for eloc in a.findall("ELocationID"):
                if eloc.get("EIdType") == "doi":
                    m["doi"] = normalize_doi(eloc.text)
        m["publication_types"] = [_text(p) for p in a.findall("PublicationTypeList/PublicationType")]
        m["language"] = _text(a.find("Language"))
        if m["pmid"]:
            m["source_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{m['pmid']}/"
        m["original"] = ET.tostring(art, encoding="unicode")
        out.append(m)
    return out


def parse_transcribed_record(rec):
    """Records typed into a structured JSON file from a non-JSON tool (Consensus, alphaXiv, web).
    Expected keys: title, authors (list of 'Last, First' strings or dicts), year, journal, doi,
    pmid, pmcid, arxiv_id, url, abstract."""
    m = _empty_meta()
    m["title"] = strip_markup(rec.get("title"))
    authors = []
    for a in rec.get("authors") or []:
        if isinstance(a, dict):
            authors.append(a)
        else:
            parts = [p.strip() for p in str(a).split(",", 1)]
            if len(parts) == 2:
                authors.append({"last_name": parts[0], "fore_name": parts[1]})
            else:  # "First Middle Last" -> last token is the surname
                toks = parts[0].split()
                authors.append({"last_name": toks[-1] if toks else None,
                                "fore_name": " ".join(toks[:-1]) or None})
    m["authors"] = authors
    m["year"] = parse_year(rec.get("year"))
    m["journal"] = rec.get("journal")
    m["doi"] = normalize_doi(rec.get("doi"))
    m["pmid"] = normalize_pmid(rec.get("pmid"))
    m["pmcid"] = normalize_pmcid(rec.get("pmcid"))
    m["arxiv_id"] = normalize_arxiv(rec.get("arxiv_id") or rec.get("url"))
    m["source_url"] = rec.get("url")
    m["abstract"] = strip_markup(rec.get("abstract")) or None
    m["original"] = rec
    return m


# --------------------------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------------------------
def read_manifest(lit_dir):
    p = Path(lit_dir) / "raw_exports" / "MANIFEST.csv"
    if not p.exists():
        return []
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def register_raw(lit_dir, raw_file, query_id, source, route, endpoint_or_tool, request,
                 retrieved_at, n_items, transcribed, notes=""):
    if route not in ROUTES:
        raise ValueError(f"unknown route {route!r}")
    lit_dir = Path(lit_dir)
    raw_path = lit_dir / "raw_exports" / raw_file
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)
    rows = read_manifest(lit_dir)
    if any(r["raw_file"] == raw_file for r in rows):
        raise ValueError(f"{raw_file} already registered (raw files are immutable)")
    row = {"raw_file": raw_file, "sha256": sha256_file(raw_path), "query_id": query_id,
           "source": source, "route": route, "endpoint_or_tool": endpoint_or_tool,
           "request_json": json.dumps(request, sort_keys=True), "retrieved_at": retrieved_at,
           "n_items": str(n_items), "transcribed": "yes" if transcribed else "no",
           "transcription_check": "not_done" if transcribed else "not_applicable",
           "notes": notes}
    mp = lit_dir / "raw_exports" / "MANIFEST.csv"
    new = not mp.exists()
    with open(mp, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row


def set_transcription_check(lit_dir, raw_file, status, note=""):
    """Record the outcome of a re-fetch spot-check for a transcribed raw file. Only the
    manifest's transcription_check/notes columns change; the raw file itself is never edited."""
    if status not in ("passed", "failed", "not_done"):
        raise ValueError(status)
    mp = Path(lit_dir) / "raw_exports" / "MANIFEST.csv"
    rows = read_manifest(lit_dir)
    hit = [r for r in rows if r["raw_file"] == raw_file]
    if not hit or hit[0]["transcribed"] != "yes":
        raise ValueError(f"{raw_file} is not a registered transcribed file")
    hit[0]["transcription_check"] = status
    if note:
        hit[0]["notes"] = (hit[0]["notes"] + " | " if hit[0]["notes"] else "") + note
    with open(mp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLS)
        w.writeheader()
        w.writerows(rows)


SPOT_CHECK_FIELDS = ("title", "year", "journal", "doi", "pmcid", "abstract", "authors")


def _metadata_by_pmid(lit_dir, row):
    path = Path(lit_dir) / "raw_exports" / row["raw_file"]
    if row["route"] == "pubmed_connector_metadata":
        metas = [parse_connector_article(a) for a in _load_raw_json(lit_dir, row).get("articles", [])]
    elif row["route"] == "eutils_efetch":
        metas = parse_efetch_xml(path.read_bytes())
    else:
        raise ValueError(f"{row['raw_file']}: spot-check needs a metadata file")
    return {m["pmid"]: m for m in metas if m["pmid"]}


def spot_check(lit_dir, original_file, refetch_file, record=True):
    """Compare a transcribed metadata file with an independent re-fetch of (a sample of) the
    same PMIDs. Every PMID in the re-fetch must be present in the original with identical
    normalised fields. Records passed/failed on the original's manifest row."""
    rows = {r["raw_file"]: r for r in read_manifest(lit_dir)}
    orig = _metadata_by_pmid(lit_dir, rows[original_file])
    ref = _metadata_by_pmid(lit_dir, rows[refetch_file])
    norm = {"title": normalize_title, "journal": normalize_journal,
            "abstract": lambda x: normalize_title(x)[:2000],
            "authors": lambda a: [first_author_key([x]) for x in a or []]}
    mismatches = []
    for pmid, m in ref.items():
        o = orig.get(pmid)
        if o is None:
            mismatches.append({"pmid": pmid, "field": "*", "original": None, "refetch": "present"})
            continue
        for f in SPOT_CHECK_FIELDS:
            fn = norm.get(f, lambda x: x)
            if fn(o.get(f)) != fn(m.get(f)):
                mismatches.append({"pmid": pmid, "field": f, "original": o.get(f), "refetch": m.get(f)})
    status = "passed" if ref and not mismatches else "failed"
    if record:
        set_transcription_check(lit_dir, original_file, status,
                                f"spot-check vs {refetch_file}: {len(ref)} PMIDs, {len(mismatches)} mismatches")
    return status, len(ref), mismatches


def _search_pmids(lit_dir, rows):
    pmids, total = set(), 0
    for r in rows:
        resp = _load_raw_json(lit_dir, r)
        if r["route"] == "eutils_esearch":
            res = resp.get("esearchresult", {})
            ids, t = res.get("idlist", []), int(res.get("count", 0))
        else:
            ids, t = resp.get("pmids", []), int(resp.get("total_count", 0))
        pmids |= {normalize_pmid(p) for p in ids if normalize_pmid(p)}
        total = max(total, t)
    return pmids, total


def check_search(lit_dir, query_id, record=True):
    """Compare the PMID set of a query's transcribed search pages with an independent re-fetch
    registered as CHECK-<query_id> (e.g. a different sort order). Passes only if both sets are
    identical and complete (= reported total). Records passed/failed on every original page."""
    rows = read_manifest(lit_dir)
    search_routes = ("pubmed_connector_search", "eutils_esearch")
    orig = [r for r in rows if r["query_id"] == query_id and r["route"] in search_routes]
    check = [r for r in rows if r["query_id"] == CHECK_PREFIX + query_id and r["route"] in search_routes]
    if not orig or not check:
        raise ValueError(f"{query_id}: need original pages and {CHECK_PREFIX}{query_id} pages")
    o, ot = _search_pmids(lit_dir, orig)
    c, ct = _search_pmids(lit_dir, check)
    only_o, only_c = sorted(o - c), sorted(c - o)
    ok = not only_o and not only_c and len(o) == ot == ct
    status = "passed" if ok else "failed"
    if record:
        note = (f"check-search vs {CHECK_PREFIX}{query_id}: {len(o)} vs {len(c)} PMIDs, totals {ot}/{ct}, "
                f"{len(only_o)} only in original, {len(only_c)} only in re-fetch")
        for r in orig:
            if r["transcribed"] == "yes":
                set_transcription_check(lit_dir, r["raw_file"], status, note)
    return status, {"original": len(o), "refetch": len(c), "reported_total": ot,
                    "only_original": only_o, "only_refetch": only_c}


def verify_manifest(lit_dir, rows):
    problems = []
    for r in rows:
        p = Path(lit_dir) / "raw_exports" / r["raw_file"]
        if not p.exists():
            problems.append(f"missing raw file {r['raw_file']}")
        elif sha256_file(p) != r["sha256"]:
            problems.append(f"checksum mismatch {r['raw_file']} (raw files must not be edited)")
    return problems


def load_query_strings(lit_dir):
    p = Path(lit_dir) / "search_queries.csv"
    if not p.exists():
        return {}
    with open(p, newline="") as f:
        return {r["query_id"]: r["query_string"] for r in csv.DictReader(f)}


# --------------------------------------------------------------------------------------------
# Source records
# --------------------------------------------------------------------------------------------
def _load_raw_json(lit_dir, row):
    with open(Path(lit_dir) / "raw_exports" / row["raw_file"]) as f:
        doc = json.load(f)
    return doc.get("response", doc)


def build_source_records(lit_dir, rows):
    """Returns (source_records, completeness). Search hits are joined to metadata by PMID."""
    queries = load_query_strings(lit_dir)
    meta_by_pmid = {}            # pmid -> (meta, manifest row)
    hits = []                    # (row, rank, pmid)
    direct = []                  # (row, rank, meta) for routes that carry full metadata
    totals = {}

    for row in rows:
        route = row["route"]
        path = Path(lit_dir) / "raw_exports" / row["raw_file"]
        if row["query_id"].startswith(CHECK_PREFIX):
            continue
        if route == "pubmed_connector_metadata":
            for art in _load_raw_json(lit_dir, row).get("articles", []):
                m = parse_connector_article(art)
                if m["pmid"]:
                    meta_by_pmid.setdefault(m["pmid"], (m, row))
        elif route == "eutils_efetch":
            for m in parse_efetch_xml(path.read_bytes()):
                if m["pmid"]:
                    meta_by_pmid.setdefault(m["pmid"], (m, row))
        elif route in ("pubmed_connector_search", "eutils_esearch"):
            resp = _load_raw_json(lit_dir, row)
            if route == "eutils_esearch":
                res = resp.get("esearchresult", {})
                pmids, total = res.get("idlist", []), int(res.get("count", 0))
                offset = int(res.get("retstart", 0))
            else:
                pmids, total = resp.get("pmids", []), int(resp.get("total_count", 0))
                offset = int(json.loads(row["request_json"] or "{}").get("retstart", 0))
            totals.setdefault(row["query_id"], {"reported_total": 0, "pmids": set()})
            t = totals[row["query_id"]]
            t["reported_total"] = max(t["reported_total"], total)
            for i, p in enumerate(pmids):
                p = normalize_pmid(p)
                if p:
                    t["pmids"].add(p)
                    hits.append((row, offset + i + 1, p))
        elif route == "structured_transcription":
            for i, rec in enumerate(_load_raw_json(lit_dir, row).get("records", [])):
                direct.append((row, i + 1, parse_transcribed_record(rec)))

    records = []

    def make(row, rank, meta, pmid=None, meta_row=None):
        stem = Path(row["raw_file"]).stem
        rid = f"SR-{stem}-{rank:05d}"
        r = {k: meta[k] for k in meta if k != "original"} if meta else _empty_meta()
        r.pop("original", None)
        if pmid and not r.get("pmid"):
            r["pmid"] = pmid
            r["source_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        r.update({
            "source_record_id": rid,
            "source": row["source"],
            "route": ("eutils_api" if row["route"].startswith("eutils") else
                      "pubmed_connector" if row["route"].startswith("pubmed_connector") else
                      "structured_transcription"),
            "query_id": row["query_id"],
            "query_string": queries.get(row["query_id"]),
            "search_timestamp": row["retrieved_at"],
            "rank": rank,
            "raw_file": row["raw_file"],
            "raw_sha256": row["sha256"],
            "metadata_raw_file": meta_row["raw_file"] if meta_row else None,
            "transcribed": (row["transcribed"] == "yes") or bool(meta_row and meta_row["transcribed"] == "yes"),
            "transcription_check": _combined_check(row, meta_row),
            "metadata_missing": meta is None,
            "original": meta["original"] if meta else None,
        })
        return r

    for row, rank, pmid in hits:
        meta, meta_row = meta_by_pmid.get(pmid, (None, None))
        records.append(make(row, rank, meta, pmid=pmid, meta_row=meta_row))
    for row, rank, meta in direct:
        records.append(make(row, rank, meta))

    completeness = {q: {"reported_total": v["reported_total"], "unique_pmids_retrieved": len(v["pmids"]),
                        "complete": len(v["pmids"]) >= v["reported_total"]}
                    for q, v in sorted(totals.items())}
    return records, completeness


def _combined_check(row, meta_row):
    checks = [r["transcription_check"] for r in (row, meta_row) if r and r["transcribed"] == "yes"]
    if not checks:
        return "not_applicable"
    if "failed" in checks:
        return "failed"
    return "passed" if all(c == "passed" for c in checks) else "not_done"


# --------------------------------------------------------------------------------------------
# Deduplication
# --------------------------------------------------------------------------------------------
class _UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i


def _source_rank(r):
    s = SOURCE_PRIORITY.index(r["source"]) if r["source"] in SOURCE_PRIORITY else 99
    ro = ROUTE_PRIORITY.index(r["route"]) if r["route"] in ROUTE_PRIORITY else 99
    return (s, ro, r["metadata_missing"], r["search_timestamp"] or "", r["source_record_id"])


def deduplicate(records, decisions_same=()):
    """Cluster source records. Returns (clusters as lists of indices, review pairs as
    (i, j, reason, similarity) on record indices).

    Automatic merges: shared PMID / DOI / PMCID / arXiv ID, or identical normalised title with
    the same year and first author, unless the clusters carry different values of the same
    identifier (then flagged, never merged). Everything weaker is flagged for review."""
    n = len(records)
    uf = _UF(n)
    ids = {"pmid": [set() for _ in range(n)], "doi": [set() for _ in range(n)],
           "pmcid": [set() for _ in range(n)], "arxiv_id": [set() for _ in range(n)]}
    for i, r in enumerate(records):
        for k in ids:
            if r.get(k):
                ids[k][i].add(r[k])
    review = []

    def conflict(a, b):
        return [k for k in ids if ids[k][a] and ids[k][b] and not (ids[k][a] & ids[k][b])]

    def union(a, b):
        ra, rb = uf.find(a), uf.find(b)
        if ra == rb:
            return True
        c = conflict(ra, rb)
        if c:
            review.append((a, b, "identifier_conflict:" + "+".join(c), None))
            return False
        uf.p[rb] = ra
        for k in ids:
            ids[k][ra] |= ids[k][rb]
        return True

    # 1. exact identifiers (deterministic order)
    for key in ("pmid", "doi", "pmcid", "arxiv_id"):
        first = {}
        for i, r in enumerate(records):
            v = r.get(key)
            if v:
                if v in first:
                    union(first[v], i)
                else:
                    first[v] = i
    # 2. manual "same" decisions (pairs of record indices)
    for a, b in decisions_same:
        union(a, b)
    # 3. normalised titles
    by_title = {}
    for i, r in enumerate(records):
        t = normalize_title(r.get("title"))
        if len(t) >= 20:
            by_title.setdefault(t, []).append(i)
    for t, idx in by_title.items():
        for a_pos, a in enumerate(idx):
            for b in idx[a_pos + 1:]:
                if uf.find(a) == uf.find(b):
                    continue
                ra, rb = records[a], records[b]
                fa, fb = first_author_key(ra["authors"]), first_author_key(rb["authors"])
                same_author = fa == fb or not fa or not fb
                ya, yb = ra.get("year"), rb.get("year")
                if ya and yb and ya == yb and same_author:
                    union(a, b)
                elif ya and yb and abs(ya - yb) == 1 and same_author:
                    review.append((a, b, "same_title_year_differs_by_1", 1.0))
                else:
                    review.append((a, b, "same_title_other_differences", 1.0))
    # 4. fuzzy titles between clusters (blocked by first-author surname)
    reps = {}
    for i in range(n):
        reps.setdefault(uf.find(i), i)
    blocks = {}
    for root, i in reps.items():
        key = first_author_key(records[i]["authors"]) or normalize_title(records[i].get("title"))[:6]
        blocks.setdefault(key, []).append(i)
    norm_t = {i: normalize_title(records[i].get("title")) for idx in blocks.values() for i in idx}
    toks = {i: set(t.split()) for i, t in norm_t.items()}
    for key, idx in blocks.items():
        for a_pos, a in enumerate(idx):
            ta = norm_t[a]
            for b in idx[a_pos + 1:]:
                tb = norm_t[b]
                if not ta or not tb or ta == tb or uf.find(a) == uf.find(b):
                    continue
                # cheap filters first (common surnames make large blocks): a pair reaching the
                # character-ratio threshold shares most words and has similar length
                if min(len(ta), len(tb)) / max(len(ta), len(tb)) < FUZZY_THRESHOLD - 0.1:
                    continue
                inter = len(toks[a] & toks[b])
                if inter / max(len(toks[a] | toks[b]), 1) < 0.5:
                    continue
                sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
                if sm.quick_ratio() < FUZZY_THRESHOLD:
                    continue
                s = sm.ratio()
                if s >= FUZZY_THRESHOLD:
                    review.append((a, b, "fuzzy_title", round(s, 3)))
    clusters = {}
    for i in range(n):
        clusters.setdefault(uf.find(i), []).append(i)
    # drop review pairs that ended up in the same cluster
    review = [p for p in review if uf.find(p[0]) != uf.find(p[1])]
    return list(clusters.values()), review


# --------------------------------------------------------------------------------------------
# Paper-ID registry
# --------------------------------------------------------------------------------------------
def record_keys(r):
    keys = []
    for k in ("pmid", "doi", "pmcid", "arxiv_id"):
        if r.get(k):
            keys.append(f"{k}:{r[k]}")
    t = normalize_title(r.get("title"))
    if t and r.get("year"):
        keys.append(f"title:{t}|{r['year']}")
    if not keys and r.get("source_record_id"):
        # LIT-004-WORKFLOW-FIXES (B-1): a record with no persistent identifier and no year has
        # no other stable key. Its source-record ID (raw file stem + rank) is deterministic
        # (raw files are immutable and checksummed) and unique to one cluster, so the paper ID
        # can never be re-assigned on a rebuild.
        keys.append(f"source_record:{r['source_record_id']}")
    return keys


def load_registry(path):
    reg = {}
    if Path(path).exists():
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                reg[row["key"]] = row["paper_id"]
    return reg


def assign_ids(clusters, records, registry_path, today):
    reg = load_registry(registry_path)
    used = [int(v[1:]) for v in reg.values() if re.fullmatch(r"P\d+", v)]
    nxt = max(used, default=0) + 1
    new_rows, out, conflicts = [], {}, []
    # deterministic order: clusters ordered by their best record's sort key
    order = sorted(range(len(clusters)), key=lambda c: min(_source_rank(records[i]) for i in clusters[c]))
    taken = set()   # an ID already given to another cluster in this build is never reused
    for c in order:
        keys = sorted({k for i in clusters[c] for k in record_keys(records[i])})
        found = sorted({reg[k] for k in keys if k in reg}, key=lambda x: int(x[1:]))
        free = [f for f in found if f not in taken]
        if free:
            pid = free[0]
            if len(found) > 1:
                conflicts.append((pid, [f for f in found if f != pid]))
        else:
            pid = f"P{nxt:04d}"
            nxt += 1
            if found:   # shares an identifier key with a different, unmerged cluster
                conflicts.append((pid, found))
        taken.add(pid)
        for k in keys:
            if k not in reg:
                reg[k] = pid
                new_rows.append({"key": k, "paper_id": pid, "first_seen": today})
        out[c] = pid
    if new_rows:
        new = not Path(registry_path).exists()
        with open(registry_path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["key", "paper_id", "first_seen"])
            if new:
                w.writeheader()
            w.writerows(new_rows)
    return out, conflicts


# --------------------------------------------------------------------------------------------
# Merge into publication records
# --------------------------------------------------------------------------------------------
CONFLICT_FIELDS = {"title": normalize_title, "year": lambda x: x, "journal": normalize_journal,
                   "doi": lambda x: x, "pmid": lambda x: x, "pmcid": lambda x: x,
                   "arxiv_id": lambda x: x}
FILL_FIELDS = ["title", "authors", "year", "journal", "doi", "pmid", "pmcid", "arxiv_id",
               "source_url", "abstract", "publication_types", "language"]


def merge_cluster(members):
    members = sorted(members, key=_source_rank)
    primary = members[0]
    pub, provenance = {}, {}
    for f in FILL_FIELDS:
        val, src = None, None
        for m in members:
            v = m.get(f)
            if v not in (None, "", []):
                val, src = v, m["source_record_id"]
                break
        pub[f] = val
        provenance[f] = src
    conflicts = []
    for f, norm in CONFLICT_FIELDS.items():
        seen = {}
        for m in members:
            v = m.get(f)
            if v in (None, ""):
                continue
            seen.setdefault(norm(v), []).append({"source_record_id": m["source_record_id"], "value": v})
        if len(seen) > 1:
            conflicts.append({"field": f, "values": [x for vals in seen.values() for x in vals]})
    return primary, pub, provenance, conflicts


def auto_verification(members, conflicts):
    hard = {c["field"] for c in conflicts} & {"title", "year", "doi", "pmid"}
    if hard:
        return "needs_review", "conflicting " + ", ".join(sorted(hard))
    if all(m["metadata_missing"] for m in members):
        return "unverified", "no metadata retrieved"
    sources = {m["source"] for m in members if not m["metadata_missing"]}
    auth = [m for m in members if m["source"] in AUTHORITATIVE_SOURCES and not m["metadata_missing"]
            and (m.get("pmid") or m.get("doi") or m.get("arxiv_id"))]
    if not auth:
        return "unverified", "no authoritative index record with a persistent identifier"
    # transcribed connector data counts only if its transcription spot-check passed
    trusted_auth = [m for m in auth if not m["transcribed"] or m["transcription_check"] == "passed"]
    if not trusted_auth:
        return "partially_verified", "authoritative record is transcribed and not yet spot-checked"
    if len(sources) >= 2:
        return "verified", "consistent in sources: " + ", ".join(sorted(sources))
    return "partially_verified", "single source: " + ", ".join(sorted(sources))


def full_text_hint(pub):
    if pub.get("pmcid"):
        return "pmc_record"
    if pub.get("arxiv_id"):
        return "arxiv_preprint"
    return "not_checked"


def _read_csv(path):
    if not Path(path).exists():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def build(lit_dir, today=None, check_schema=True):
    lit_dir = Path(lit_dir)
    today = today or dt.date.today().isoformat()
    rec_dir = lit_dir / "records"
    rec_dir.mkdir(parents=True, exist_ok=True)
    rows = read_manifest(lit_dir)
    problems = verify_manifest(lit_dir, rows)
    if problems:
        raise RuntimeError("; ".join(problems))
    records, completeness = build_source_records(lit_dir, rows)

    # manual dedup decisions are keyed by paper_id -> map back through the registry
    registry = load_registry(rec_dir / "paper_id_registry.csv")
    rec_pid = {}
    for i, r in enumerate(records):
        for k in record_keys(r):
            if k in registry:
                rec_pid.setdefault(i, registry[k])
    pid_recs = {}
    for i, pid in rec_pid.items():
        pid_recs.setdefault(pid, []).append(i)
    decisions = _read_csv(rec_dir / "dedup_decisions.csv")
    same, different = [], set()
    for d in decisions:
        a, b = d["paper_id_a"], d["paper_id_b"]
        if d["decision"] == "same" and a in pid_recs and b in pid_recs:
            same.append((pid_recs[a][0], pid_recs[b][0]))
        elif d["decision"] == "different":
            different.add(frozenset((a, b)))

    clusters, review = deduplicate(records, same)
    ids, reg_conflicts = assign_ids(clusters, records, rec_dir / "paper_id_registry.csv", today)
    cluster_of = {i: c for c, idx in enumerate(clusters) for i in idx}

    screening_rows = load_screening_decisions(lit_dir)
    rq5_evidence = rq5_component_evidence(screening_rows)   # raises on erasure / incomplete rows
    rq5_groups = {pid: derive_rq5_coverage_group(ev["confirmed"]["statuses"]) if ev["confirmed"] else (None, None)
                  for pid, ev in rq5_evidence.items()}
    screening = {}
    for d in sorted(screening_rows, key=lambda d: (SCREENING_STAGE_ORDER[d["stage"]], d["date"])):
        screening[d["paper_id"]] = d          # latest stage, then latest date, then file order
    overrides = {d["paper_id"]: d for d in _read_csv(rec_dir / "verification_overrides.csv")}
    fulltext = {d["paper_id"]: d for d in _read_csv(rec_dir / "fulltext_status.csv")}
    # manual inputs that point at a paper ID absent from this build would be silently lost:
    # stop instead (LIT-004-WORKFLOW-FIXES)
    built_ids = set(ids.values())
    orphans = sorted({(name, pid) for name, rows_ in (
        ("screening/decisions.csv", screening_rows),
        ("records/verification_overrides.csv", overrides.values()),
        ("records/fulltext_status.csv", fulltext.values()),
        ("records/dedup_decisions.csv", [{"paper_id": x} for d in decisions for x in (d["paper_id_a"], d["paper_id_b"])
                                         if d["decision"] != "same"]))
        for pid in (r["paper_id"] for r in rows_) if pid not in built_ids})
    # a "same" decision absorbs one of its two IDs into the other, so only one has to survive
    orphans += sorted(("records/dedup_decisions.csv", d["paper_id_a"] + "+" + d["paper_id_b"]) for d in decisions
                      if d["decision"] == "same" and not {d["paper_id_a"], d["paper_id_b"]} & built_ids)
    if orphans:
        raise RuntimeError("manual inputs refer to paper IDs not in this build (nothing written): "
                           + "; ".join(f"{n}:{p}" for n, p in orphans))

    review_rows, review_by_pid = [], {}
    for a, b, reason, sim in review:
        pa, pb = ids[cluster_of[a]], ids[cluster_of[b]]
        if pa == pb or frozenset((pa, pb)) in different:
            continue
        review_by_pid.setdefault(pa, set()).add(pb)
        review_by_pid.setdefault(pb, set()).add(pa)
        review_rows.append({"paper_id_a": pa, "paper_id_b": pb, "reason": reason,
                            "similarity": "" if sim is None else sim,
                            "title_a": records[a]["title"], "title_b": records[b]["title"],
                            "year_a": records[a]["year"], "year_b": records[b]["year"]})
    seen_pairs, uniq_review = set(), []
    for r in review_rows:
        k = (min(r["paper_id_a"], r["paper_id_b"]), max(r["paper_id_a"], r["paper_id_b"]), r["reason"])
        if k not in seen_pairs:
            seen_pairs.add(k)
            uniq_review.append(r)

    pubs = []
    for c, idx in enumerate(clusters):
        members = [records[i] for i in idx]
        primary, pub, prov, conflicts = merge_cluster(members)
        pid = ids[c]
        status, note = auto_verification(members, conflicts)
        if pid in overrides:
            status = overrides[pid]["verification_status"]
            note = f"manual override by {overrides[pid].get('reviewer','?')} on {overrides[pid].get('date','?')}: {overrides[pid].get('note','')}"
        sc = screening.get(pid)
        ft = fulltext.get(pid)
        if pid in review_by_pid:
            dup = "possible_duplicate_review"
        elif len(members) > 1:
            dup = "merged_duplicates"
        else:
            dup = "unique"
        pubs.append({
            "paper_id": pid,
            **pub,
            "source_databases": sorted({m["source"] for m in members},
                                       key=lambda s: SOURCE_PRIORITY.index(s) if s in SOURCE_PRIORITY else 99),
            "source_urls": sorted({m["source_url"] for m in members if m.get("source_url")}),
            "primary_source_record_id": primary["source_record_id"],
            "field_provenance": prov,
            "search_provenance": [{"query_id": m["query_id"], "query_string": m["query_string"],
                                   "source": m["source"], "search_timestamp": m["search_timestamp"],
                                   "rank": m["rank"], "source_record_id": m["source_record_id"]}
                                  for m in sorted(members, key=lambda m: m["source_record_id"])],
            "duplicate_status": dup,
            "n_source_records": len(members),
            "possible_duplicates": sorted(review_by_pid.get(pid, [])),
            "metadata_conflicts": conflicts,
            "verification_status": status,
            "verification_note": note,
            "full_text_availability": ft["full_text_availability"] if ft else full_text_hint(pub),
            "screening_decision": sc["decision"] if sc else "not_screened",
            "screening_stage": sc["stage"] if sc else None,
            "exclusion_reason": (sc.get("reason_code") or None) if sc else None,
            "screening_details": ({k: sc.get(k) or None for k in
                                   ["screener", "date", "justification"] + SCREENING_OPTIONAL}
                                  if sc else None),
            "rq5_components": rq5_evidence.get(pid),
            "rq5_coverage_group": rq5_groups.get(pid, (None, None))[0],
            "rq5_coverage_provisional": rq5_groups.get(pid, (None, None))[1],
            "retracted": any("Retracted Publication" in (m.get("publication_types") or []) for m in members),
        })
    pubs.sort(key=lambda p: int(p["paper_id"][1:]))

    if check_schema:
        validate_outputs(records, pubs)

    with open(rec_dir / "source_records.jsonl", "w") as f:
        for r in sorted(records, key=lambda r: r["source_record_id"]):
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(rec_dir / "publications.jsonl", "w") as f:
        for p in pubs:
            f.write(json.dumps(p, ensure_ascii=False, sort_keys=True) + "\n")
    with open(rec_dir / "dedup_review.csv", "w", newline="") as f:
        cols = ["paper_id_a", "paper_id_b", "reason", "similarity", "title_a", "title_b",
                "year_a", "year_b"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(uniq_review)
    index_cols = ["paper_id", "title", "first_author", "n_authors", "year", "journal", "doi", "pmid",
                  "pmcid", "arxiv_id", "source_databases", "source_urls", "query_ids", "first_search_timestamp",
                  "abstract_available", "duplicate_status", "possible_duplicates", "n_metadata_conflicts",
                  "verification_status", "full_text_availability", "screening_decision", "exclusion_reason",
                  "retracted"]
    with open(rec_dir / "publications_index.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=index_cols)
        w.writeheader()
        for p in pubs:
            a0 = (p["authors"] or [{}])[0]
            w.writerow({**{k: p.get(k) for k in index_cols if k in p},
                        "first_author": a0.get("last_name") or a0.get("collective_name") or a0.get("name"),
                        "n_authors": len(p["authors"] or []),
                        "source_databases": ";".join(p["source_databases"]),
                        "source_urls": ";".join(p["source_urls"]),
                        "query_ids": ";".join(sorted({s["query_id"] for s in p["search_provenance"]})),
                        "first_search_timestamp": min(s["search_timestamp"] for s in p["search_provenance"]),
                        "abstract_available": bool(p["abstract"]),
                        "possible_duplicates": ";".join(p["possible_duplicates"]),
                        "n_metadata_conflicts": len(p["metadata_conflicts"])})
    report = {
        "built_at": utc_now(),
        "manifest_files": len(rows),
        "source_records": len(records),
        "source_records_missing_metadata": sum(r["metadata_missing"] for r in records),
        "publications": len(pubs),
        "duplicate_status": _count(p["duplicate_status"] for p in pubs),
        "verification_status": _count(p["verification_status"] for p in pubs),
        "publications_with_metadata_conflicts": sum(bool(p["metadata_conflicts"]) for p in pubs),
        "dedup_review_pairs": len(uniq_review),
        "registry_conflicts": [{"kept": k, "also": v} for k, v in reg_conflicts],
        "search_completeness": completeness,
        "retracted": [p["paper_id"] for p in pubs if p["retracted"]],
        "screening_decision": _count(p["screening_decision"] for p in pubs),
        "publications_without_stable_registry_key": sum(
            1 for c in clusters if not any(record_keys(records[i]) for i in c)),
    }
    with open(rec_dir / "build_report.json", "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    return report


def _component_statuses(row):
    return {name: (row.get(col) or None) if col else None for name, col in RQ5_COMPONENT_FIELDS.items()}


def rq5_component_evidence(rows):
    """Per paper, keep RQ5 component statuses by evidence stage (D-035, Q-041):
    - "preliminary": latest title/abstract row; for triage only, never counted toward D-031/D-034;
    - "confirmed": latest full-text row, unless that row is an abstract_only decision (no full text,
      so nothing can be confirmed) or records no component; earlier full-text rows are kept as history,
      so a researcher verification row (screener=researcher) never hides the evidence it replaced.
    Raises ValueError (nothing is written) when a later row of the same stage would blank a component
    recorded earlier at that stage, or when a full-text row records some but not all component statuses
    (an empty value means "not assessed", never "no"). Completeness covers all five component
    columns (RQ5_RECORDED_FIELDS, D-036)."""
    by_pid, errors = {}, []
    order = sorted(enumerate(rows), key=lambda t: (t[1]["paper_id"], SCREENING_STAGE_ORDER[t[1]["stage"]],
                                                   t[1]["date"], t[0]))
    for _, r in order:
        by_pid.setdefault(r["paper_id"], []).append(r)
    out = {}
    for pid, prow in by_pid.items():
        for stage in SCREENING_STAGE_ORDER:
            seen = {}
            for r in (x for x in prow if x["stage"] == stage):
                for f in RQ5_RECORDED_FIELDS:
                    if r[f]:
                        seen[f] = r[f]
                    elif f in seen:
                        errors.append(f"{pid} ({stage}, {r['date']}): {f} is blank but was recorded as "
                                      f"{seen[f]!r} in an earlier {stage} row; restate it (use 'unclear' if unresolved)")
        ft = [r for r in prow if r["stage"] == "full_text"]
        for r in ft:
            filled = [f for f in RQ5_RECORDED_FIELDS if r[f]]
            if filled and len(filled) < len(RQ5_RECORDED_FIELDS):
                missing = [f for f in RQ5_RECORDED_FIELDS if not r[f]]
                errors.append(f"{pid} (full_text, {r['date']}): component assessment incomplete, missing {missing} "
                              "(record 'unclear' when assessed but unresolved)")
        ta = [r for r in prow if r["stage"] == "title_abstract"]
        prelim = None
        if ta and any(ta[-1][f] for f in RQ5_RECORDED_FIELDS):
            prelim = {"statuses": _component_statuses(ta[-1]), "screener": ta[-1]["screener"], "date": ta[-1]["date"]}
        confirmed, note = None, None
        if ft:
            last = ft[-1]
            if last["decision"] == "abstract_only":
                note = "full text unavailable (abstract_only): component statuses cannot be confirmed"
            elif any(last[f] for f in RQ5_RECORDED_FIELDS):
                history = [{"screener": r["screener"], "date": r["date"], "decision": r["decision"],
                            "statuses": _component_statuses(r)}
                           for r in ft[:-1] if any(r[f] for f in RQ5_RECORDED_FIELDS)]
                verified = last["screener"].lower() == RESEARCHER
                prior = [h for h in history if h["screener"].lower() != RESEARCHER]
                confirmed = {"statuses": _component_statuses(last), "screener": last["screener"],
                             "date": last["date"], "researcher_verified": verified,
                             "changed_by_verification": bool(verified and prior and
                                                             prior[-1]["statuses"] != _component_statuses(last)),
                             "history": history}
            else:
                note = "no component statuses recorded at full text (not assessed)"
        if prelim or confirmed or note:
            out[pid] = {"preliminary": prelim, "confirmed": confirmed, "confirmation_note": note}
    if errors:
        raise ValueError("screening/decisions.csv: RQ5 component evidence problems:\n  " + "\n  ".join(errors))
    return out


def derive_rq5_coverage_group(statuses):
    """D-034 coverage group from the five CONFIRMED (full-text) component statuses (D-035).
    Returns (group, provisional): group is None when any component is not assessed (empty/None);
    otherwise "qualified" (>= 4 yes), "near_rq5" (exactly 3) or "below_threshold" (0-2). "unclear"
    never counts as yes; provisional is True when any component is "unclear".
    Used by build() for rq5_coverage_group / rq5_coverage_provisional (D-036); a coverage
    descriptor only, never a quality judgment, and never assigned by a screener."""
    vals = [statuses.get(name) for name in RQ5_COMPONENT_FIELDS]
    if any(v in (None, "") for v in vals):
        return None, None
    bad = [v for v in vals if v not in ("yes", "no", "unclear")]
    if bad:
        raise ValueError(f"invalid component status {bad}")
    n_yes = vals.count("yes")
    group = "qualified" if n_yes >= 4 else "near_rq5" if n_yes == 3 else "below_threshold"
    return group, "unclear" in vals


def load_screening_decisions(lit_dir):
    """Read and validate screening/decisions.csv. Any invalid row stops the build (no row is
    silently dropped). Returns the rows as dicts (all columns as strings)."""
    path = Path(lit_dir) / "screening" / "decisions.csv"
    if not path.exists():
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        missing = [c for c in SCREENING_REQUIRED if c not in cols]
        unknown = [c for c in cols if c not in SCREENING_REQUIRED + SCREENING_OPTIONAL]
        if missing or unknown:
            raise ValueError(f"{path}: missing columns {missing}, unknown columns {unknown}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    errors = []
    for n, r in enumerate(rows, start=2):
        for k in SCREENING_OPTIONAL:
            r.setdefault(k, "")
        where = f"line {n} ({r['paper_id'] or '?'})"
        if not re.fullmatch(r"P\d{4,}", r["paper_id"]):
            errors.append(f"{where}: bad paper_id")
        for k, allowed in SCREENING_ENUMS.items():
            if r[k] not in allowed:
                errors.append(f"{where}: {k}={r[k]!r} not in {allowed}")
        if r["decision"] == "exclude" and not REASON_CODE.fullmatch(r["reason_code"]):
            errors.append(f"{where}: exclude needs reason_code E1-E12")
        if r["decision"] != "exclude" and r["reason_code"]:
            errors.append(f"{where}: reason_code only allowed with decision=exclude")
        if r["decision"] == "abstract_only" and r["stage"] != "full_text":
            errors.append(f"{where}: abstract_only is a full-text-stage decision")
        if r["decision"] in ("exclude", "uncertain") and not r["justification"]:
            errors.append(f"{where}: justification required for {r['decision']}")
        if not r["screener"]:
            errors.append(f"{where}: screener required")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]):
            errors.append(f"{where}: date must be YYYY-MM-DD")
        if r["rq_tags"] and not RQ_TAGS.fullmatch(r["rq_tags"]):
            errors.append(f"{where}: rq_tags must be like RQ1;RQ3")
    if errors:
        raise ValueError(f"{path}: invalid screening decisions:\n  " + "\n  ".join(errors))
    return rows


def migrate_fallback_keys(lit_dir, today=None):
    """One-off migration for B-1: give publications of the last build that have no registry key
    a fallback key mapped to the paper ID they already carry, so the ID is kept rather than
    re-assigned. Appends to the registry only; refuses on any collision. Returns the mapping."""
    lit_dir = Path(lit_dir)
    rec_dir = lit_dir / "records"
    today = today or dt.date.today().isoformat()
    reg_path = rec_dir / "paper_id_registry.csv"
    reg = load_registry(reg_path)
    src = {}
    with open(rec_dir / "source_records.jsonl") as f:
        for line in f:
            r = json.loads(line)
            src[r["source_record_id"]] = r
    new_rows, mapping = [], []
    with open(rec_dir / "publications.jsonl") as f:
        for line in f:
            p = json.loads(line)
            members = [src[s["source_record_id"]] for s in p["search_provenance"]]
            keys = sorted({k for m in members for k in record_keys(m)})
            if any(k in reg for k in keys if not k.startswith("source_record:")):
                continue                     # already stable through a persistent key
            for k in keys:
                if k in reg and reg[k] != p["paper_id"]:
                    raise ValueError(f"collision: {k} already maps to {reg[k]}, not {p['paper_id']}")
                if k not in reg:
                    new_rows.append({"key": k, "paper_id": p["paper_id"], "first_seen": today})
                    reg[k] = p["paper_id"]
                    mapping.append({"paper_id_before": p["paper_id"], "paper_id_after": p["paper_id"],
                                    "registry_key": k, "title": p["title"],
                                    "source_url": (p["source_urls"] or [None])[0]})
    if new_rows:
        with open(reg_path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=["key", "paper_id", "first_seen"]).writerows(new_rows)
    return mapping


def _count(it):
    out = {}
    for x in it:
        out[x] = out.get(x, 0) + 1
    return dict(sorted(out.items()))


def validate_outputs(records, pubs, schema_dir=None):
    try:
        import jsonschema
    except ImportError:  # pragma: no cover
        print("warning: jsonschema not installed; schema validation skipped", file=sys.stderr)
        return
    schema_dir = Path(schema_dir or Path(__file__).resolve().parents[2] / "research/literature/schemas")
    with open(schema_dir / "source_record.schema.json") as f:
        sr = json.load(f)
    with open(schema_dir / "publication_record.schema.json") as f:
        pr = json.load(f)
    for r in records:
        jsonschema.validate(r, sr)
    for p in pubs:
        jsonschema.validate(p, pr)


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lit-dir", default="research/literature")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register", help="register a raw export file in MANIFEST.csv")
    r.add_argument("raw_file", help="file name inside raw_exports/")
    r.add_argument("--query-id", required=True)
    r.add_argument("--source", required=True, choices=SOURCE_PRIORITY)
    r.add_argument("--route", required=True, choices=sorted(ROUTES))
    r.add_argument("--endpoint-or-tool", required=True)
    r.add_argument("--request-json", default="{}")
    r.add_argument("--retrieved-at", required=True, help="ISO-8601 timestamp of the API/tool call")
    r.add_argument("--n-items", required=True, type=int)
    r.add_argument("--transcribed", action="store_true",
                   help="response was written to disk by the assistant from tool output")
    r.add_argument("--notes", default="")
    b = sub.add_parser("build", help="rebuild records from all registered raw exports")
    b.add_argument("--no-schema", action="store_true")
    v = sub.add_parser("verify", help="check raw-export checksums against MANIFEST.csv")
    c = sub.add_parser("spot-check", help="compare a transcribed metadata file with a re-fetch")
    c.add_argument("original_file")
    c.add_argument("refetch_file")
    s = sub.add_parser("check-search", help="compare a query's search pages with its CHECK- re-fetch")
    s.add_argument("query_id")
    mg = sub.add_parser("migrate-fallback-keys", help="B-1: register fallback keys for the last build's IDs")
    mg.add_argument("--mapping-out", required=True, help="CSV file for the ID mapping report")
    t = sub.add_parser("set-check", help="record a transcription spot-check outcome manually")
    t.add_argument("raw_file")
    t.add_argument("status", choices=["passed", "failed", "not_done"])
    t.add_argument("--note", default="")
    a = ap.parse_args(argv)
    if a.cmd == "register":
        row = register_raw(a.lit_dir, a.raw_file, a.query_id, a.source, a.route, a.endpoint_or_tool,
                           json.loads(a.request_json), a.retrieved_at, a.n_items, a.transcribed, a.notes)
        print(json.dumps(row, indent=2))
    elif a.cmd == "build":
        print(json.dumps(build(a.lit_dir, check_schema=not a.no_schema), indent=2))
    elif a.cmd == "spot-check":
        status, n, mism = spot_check(a.lit_dir, a.original_file, a.refetch_file)
        print(json.dumps({"status": status, "pmids_compared": n, "mismatches": mism}, indent=2, default=str))
        return 0 if status == "passed" else 1
    elif a.cmd == "check-search":
        status, detail = check_search(a.lit_dir, a.query_id)
        print(json.dumps({"status": status, **detail}, indent=2))
        return 0 if status == "passed" else 1
    elif a.cmd == "migrate-fallback-keys":
        mapping = migrate_fallback_keys(a.lit_dir)
        cols = ["paper_id_before", "paper_id_after", "registry_key", "title", "source_url"]
        with open(a.mapping_out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(mapping)
        print(f"{len(mapping)} registry keys added; mapping written to {a.mapping_out}")
    elif a.cmd == "set-check":
        set_transcription_check(a.lit_dir, a.raw_file, a.status, a.note)
        print(f"{a.raw_file}: transcription_check={a.status}")
    elif a.cmd == "verify":
        probs = verify_manifest(a.lit_dir, read_manifest(a.lit_dir))
        print("\n".join(probs) if probs else "OK: all raw exports match MANIFEST.csv")
        return 1 if probs else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
