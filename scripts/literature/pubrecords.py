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
import contextlib
import csv
import datetime as dt
import difflib
import hashlib
import html
import io
import itertools
import json
import os
import re
import sys
import tempfile
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
          "pubmed_connector_metadata", "structured_transcription", "crossref_works"}
# Crossref verification lookups (WP2): one raw /works/{DOI} response per authorised pilot paper,
# registered under query ID "VERIFY-CR-<paper_id>" with manifest route "crossref_works". They are
# second-source evidence for D-064 only: they never become search provenance, never fill or override
# publication metadata, never create a paper ID and attach only to the one existing publication that
# carries the same normalised DOI and is listed in records/verification_pilot.csv.
VERIFY_PREFIX = "VERIFY-CR-"
CROSSREF_ROUTE = "crossref_works"          # manifest route
CROSSREF_SOURCE_ROUTE = "crossref_api"     # source-record route
# Which Crossref date field supplies the publication year is a PENDING researcher decision (options:
# "published-print"; "issued"; "published-print" then "published-online"). Until it is decided the
# Crossref year stays empty, so a Crossref record is "insufficient" on the year and cannot by itself
# make a publication `verified` (D-064 (5), (7)). Set only by a recorded decision.
CROSSREF_YEAR_FIELDS = None
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
                      "dim_uncertainty", "dim_calibration", "validation_design",
                      "criteria_version", "needs_human", "dim_feature_selection", "dim_classification",
                      "biomarker_class"]
# Screening columns that are no longer accepted (T1-A). dim_independent_validation is replaced by
# validation_design (D-029 as specified in D-060); its values are never converted automatically.
RETIRED_SCREENING_COLUMNS = ("dim_independent_validation",)
SCREENING_DECISIONS = ("include", "exclude", "uncertain", "abstract_only")   # "not_screened" = no row
SCREENING_ENUMS = {
    "stage": ("title_abstract", "full_text"),
    "decision": SCREENING_DECISIONS,
    "tier": ("", "1", "2", "3"),
    # D-028 2d: preprint/notice removed (bibliographic facts now held by publication_type)
    "record_type": ("", "original", "methodological", "software", "guideline", "review_lead", "other"),
    "dim_explainability": ("", "yes", "no", "unclear"),
    "dim_uncertainty": ("", "yes", "no", "unclear"),
    "dim_calibration": ("", "yes", "no", "unclear"),
    # D-060 (1): strongest stated validation design
    "validation_design": ("", "external", "temporal", "internal_only", "none", "not_applicable", "unclear"),
    # D-058 (Q-035)
    "biomarker_class": ("", "metabolomics_lipidomics", "newborn_screening_msms", "routine_chemistry",
                        "mixed_both", "other", "unclear"),
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
# D-060 (6): required for include/uncertain at title/abstract; optional for exclude. Not applied to
# full-text rows. The D-060 (6) Stage-0 exemption covers only Stage-0 rule rows as defined by D-068 (5):
# `exclude` rows with reason code E5 or E7 and screener=rule:stage0 (is_stage0_rule_row). Such rows
# never needed the descriptors anyway, so an include/uncertain row is never exempt, whatever its
# screener (Option A, researcher authorisation 2026-11-01). Other rows carrying screener=rule:stage0
# are not rejected for that reason (Option B was not adopted).
TITLE_ABSTRACT_REQUIRED = ("rq_tags", "record_type", "biomarker_class", "dim_explainability",
                           "dim_uncertainty", "dim_calibration", "validation_design")
STAGE0_SCREENER = "rule:stage0"
STAGE0_RULE_REASON_CODES = ("E5", "E7")
# scope_flags tokens a screener may enter (semicolon-separated): the approved vocabulary of D-069 (E)
# -- scope_pending_disorder (D-056, D-069 (A)), scope_pending_proteomics (D-057),
# non_metabolic_method_exemplar (D-069 (B)), non_metabolic_rq5_candidate (D-061), lr_only (D-069 (C)).
# Any combination is allowed; the two non-metabolic retention tags may co-occur (D-070 (1)). All are
# descriptive and inactive for screening until D-035 record §6 is met; accepting a token activates
# nothing. "prognostic" is deferred and not accepted (D-069 (D), D-071). "retracted" is derived by the
# build, never entered by hand. A token may not be repeated within one value (researcher
# authorisation 2026-11-01, recorded in DECISION_LOG as D-078).
SCOPE_FLAG_TOKENS = ("scope_pending_disorder", "scope_pending_proteomics", "non_metabolic_method_exemplar",
                     "non_metabolic_rq5_candidate", "lr_only")
BUILD_DERIVED_SCOPE_FLAGS = ("retracted",)
# D-028 2a: publication_type is derived only from source metadata, first match wins. Table: ballot
# Item 2 (research/reviews/owner_review_ballot_LIT-004.md), same as decision_reconciliation_LIT-004.md
# section 2.2. Row "preprint" also matches when the publication's source database is arXiv (D-028 2b).
# No URL or DOI-prefix rules (D-028 2c). Extensions only by a logged change.
PUBLICATION_TYPE_MAP = (
    ("retraction_notice", ("Retraction of Publication",)),
    ("expression_of_concern", ("Expression of Concern",)),
    ("erratum_or_correction", ("Published Erratum", "Correction")),
    ("study_protocol", ("Clinical Trial Protocol",)),
    ("dataset", ("Dataset",)),
    ("preprint", ("Preprint",)),
    ("review", ("Review", "Systematic Review", "Scoping Review", "Meta-Analysis", "Evidence Synthesis")),
    ("guideline_or_consensus", ("Guideline", "Practice Guideline", "Consensus Statement")),
    ("editorial_comment_letter", ("Editorial", "Comment", "Letter", "News")),
    ("conference_paper", ("Conference Proceedings", "Congress")),
    ("journal_article", ("Journal Article",)),
)
# Kept verbatim in source_publication_types but not used for the class. "Retracted Publication" only
# sets the retracted flag: a retracted article is not a retraction notice.
PUBLICATION_TYPES_IGNORED = frozenset({
    "Research Support, N.I.H., Extramural", "Research Support, N.I.H., Intramural",
    "Research Support, Non-U.S. Gov't", "Research Support, U.S. Gov't, Non-P.H.S.",
    "Research Support, U.S. Gov't, P.H.S.", "Validation Study", "Multicenter Study", "Comparative Study",
    "Observational Study", "Randomized Controlled Trial", "Clinical Trial", "Clinical Trial, Phase I",
    "Clinical Trial, Phase II", "Clinical Trial, Phase III", "Evaluation Study", "English Abstract",
    "Historical Article", "Video-Audio Media", "Retracted Publication"})
PUBLICATION_TYPES = tuple(v for v, _ in PUBLICATION_TYPE_MAP) + ("unknown", "other")
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


# Inline (character-level) JATS/HTML/MathML tags that Crossref titles may carry, e.g. HbA<sub>1c</sub>.
# They are removed WITHOUT inserting a space, so the text reads as in the plain-text PubMed record
# ("HbA1c"); every other tag is replaced by a space, as in strip_markup. Used for Crossref fields only:
# ordinary-build parsing keeps strip_markup unchanged.
# Evidence status: the tag names below are an implementation assumption (common JATS/HTML inline
# formatting and MathML presentation elements). No project document describes Crossref title markup,
# and no real Crossref response has been inspected. The only project evidence is on the PubMed side:
# the PubMed connector titles in raw_exports carried no markup (0 tags in 3,273 articles, checked
# 2026-10-31). Unknown tags are replaced by a space, the conservative choice: a missed inline tag is
# expected to produce a spurious title conflict (needs_review) rather than a spurious agreement.
INLINE_MARKUP_TAGS = frozenset({"sub", "sup", "i", "b", "u", "em", "strong", "italic", "bold", "underline",
                                "sc", "scp", "small", "tt", "monospace", "span", "font", "inline-formula",
                                "math", "mi", "mn", "mo", "ms", "mtext", "msub", "msup", "msubsup", "mrow",
                                "mfrac", "msqrt", "mstyle", "mspace", "semantics", "annotation"})


def strip_inline_markup(text):
    """Markup removal for Crossref text fields: inline tags (INLINE_MARKUP_TAGS, any namespace prefix
    such as jats: or mml:) are dropped without a space; other tags become a space."""
    if text is None:
        return None

    def repl(m):
        local = m.group(1).split(":")[-1].lower()
        return "" if local in INLINE_MARKUP_TAGS else " "
    t = re.sub(r"<\s*/?\s*([A-Za-z][\w.:-]*)[^>]*>", repl, html.unescape(str(text)))
    t = re.sub(r"<[^>]+>", " ", t)          # anything left that is not a well-formed tag name
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


def crossref_year(message, fields=None):
    """Year from a Crossref message using the date fields in `fields` (first present wins).
    Returns None while the field choice is undecided (CROSSREF_YEAR_FIELDS is None)."""
    fields = CROSSREF_YEAR_FIELDS if fields is None else fields
    for field in fields or ():
        value = message.get(field)
        if value is None:
            continue
        parts = value.get("date-parts") if isinstance(value, dict) else None
        if (not isinstance(parts, list) or not parts or not isinstance(parts[0], list) or not parts[0]
                or not isinstance(parts[0][0], (int, str)) or isinstance(parts[0][0], bool)):
            raise ValueError(f"Crossref field {field!r} has no well-formed 'date-parts'")
        year = parse_year(parts[0][0])
        if year is not None:
            return year
    return None


def _crossref_string_list(message, key):
    """A Crossref list-of-strings field (e.g. title, container-title). Absent or null -> [].
    Any other shape (a bare string, number, object, or a list holding non-strings) is malformed."""
    value = message.get(key)
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ValueError(f"Crossref field {key!r} must be a list of strings, got {type(value).__name__}")
    return [v for v in value if v.strip()]


def _crossref_authors(message):
    value = message.get("author")
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(a, dict) for a in value):
        raise ValueError("Crossref field 'author' must be a list of objects")
    for a in value:
        for k in ("family", "given", "name", "sequence"):
            if a.get(k) is not None and not isinstance(a[k], str):
                raise ValueError(f"Crossref author field {k!r} must be a string")
    return value


def parse_crossref_work(message):
    """The `message` object of one Crossref /works/{DOI} response (verification lookups only).
    Raises ValueError when the message is malformed, including wrongly shaped fields: `title` and
    `container-title` must be lists of strings, `author` a list of objects with string name parts,
    `DOI` a string. Inline markup in titles and venues is removed without a space
    (strip_inline_markup). Abstract, publication types and language are not taken; the whole message
    is kept verbatim in `original`."""
    if not isinstance(message, dict):
        raise ValueError("Crossref response has no 'message' object")
    if not isinstance(message.get("DOI"), str):
        raise ValueError("Crossref message has no DOI string")
    doi = normalize_doi(message["DOI"])
    if not doi:
        raise ValueError("Crossref message has no valid DOI")
    m = _empty_meta()
    titles = _crossref_string_list(message, "title")
    m["title"] = strip_inline_markup(titles[0]) or None if titles else None
    authors = _crossref_authors(message)
    firsts = [a for a in authors if a.get("sequence") == "first"]
    if firsts and authors[0] is not firsts[0]:
        authors = [firsts[0]] + [a for a in authors if a is not firsts[0]]
    m["authors"] = [({"last_name": a.get("family"), "fore_name": a.get("given")} if a.get("family")
                     else {"collective_name": a.get("name")}) for a in authors if a.get("family") or a.get("name")]
    m["year"] = crossref_year(message)
    venues = _crossref_string_list(message, "container-title")
    m["journal"] = strip_inline_markup(venues[0]) or None if venues else None
    m["doi"] = doi
    m["original"] = message
    return m


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
    if str(query_id).startswith(VERIFY_PREFIX) != (route == CROSSREF_ROUTE):
        raise ValueError(f"query ID {query_id!r} and route {route!r}: {VERIFY_PREFIX}* query IDs are "
                         f"reserved for route {CROSSREF_ROUTE}, and that route for those IDs only")
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
    if not new and mp.stat().st_size and not _ends_with_newline(mp):
        raise ValueError(f"{mp}: last line is incomplete (interrupted write?); nothing appended. "
                         "Inspect and repair the manifest by hand before registering more files")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=MANIFEST_COLS)
    if new:
        w.writeheader()
    w.writerow(row)
    # one write call, then flush and fsync, so an interruption leaves at most one incomplete last
    # line, which the check above detects (not a guarantee of atomicity on every filesystem)
    with open(mp, "ab") as f:
        f.write(buf.getvalue().encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())
    return row


def _ends_with_newline(path):
    with open(path, "rb") as f:
        f.seek(-1, os.SEEK_END)
        return f.read(1) == b"\n"


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
        if row["query_id"].startswith(VERIFY_PREFIX) and route != CROSSREF_ROUTE:
            # a verification lookup registered under any other route would otherwise be processed as
            # an ordinary search hit (deduplication, paper IDs, metadata, provenance): stop instead
            raise RuntimeError(f"{row['raw_file']}: query ID {row['query_id']} is a Crossref verification "
                               f"lookup but is registered with route {route!r}; only {CROSSREF_ROUTE} is "
                               "allowed (nothing written)")
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
        elif route == CROSSREF_ROUTE:
            if not row["query_id"].startswith(VERIFY_PREFIX) or row["source"] != "crossref":
                raise RuntimeError(f"{row['raw_file']}: route {CROSSREF_ROUTE} is for Crossref verification "
                                   f"lookups registered as {VERIFY_PREFIX}<paper_id> only")
            try:
                with open(path, encoding="utf-8") as f:
                    doc = json.load(f)
                meta = parse_crossref_work(doc.get("message") if isinstance(doc, dict) else None)
            except ValueError as e:   # includes json.JSONDecodeError, UnicodeDecodeError, shape errors
                raise RuntimeError(f"{row['raw_file']}: malformed Crossref response ({e}); malformed "
                                   "responses must never be registered") from None
            direct.append((row, 1, meta))

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
            "route": (CROSSREF_SOURCE_ROUTE if row["route"] == CROSSREF_ROUTE else
                      "eutils_api" if row["route"].startswith("eutils") else
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


def _preview_ids(clusters, records, registry_path):
    """The paper IDs assign_ids would give, without writing the registry."""
    return assign_ids(clusters, records, registry_path, "preview", write=False)


def assign_ids(clusters, records, registry_path, today, write=True):
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
    if new_rows and write:
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


# --------------------------------------------------------------------------------------------
# Second-source verification (D-064, answers Q-068)
# --------------------------------------------------------------------------------------------
# A publication is `verified` only when an eligible second source -- independent of the
# authoritative record by recorded provenance, and spot-checked if transcribed -- agrees with it
# on title, first author, year, venue and a shared persistent identifier. Missing fields are
# insufficient evidence, never conflicts; a conflict with any eligible source gives needs_review.
# Independence classifications and eligibility reasons are reported at report level only (A6).
ARXIV_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org", "alphaxiv.org", "www.alphaxiv.org"}
ID_TYPES = ("pmid", "doi", "pmcid", "arxiv_id")
REQUIRED_FIELDS = ("title", "first_author", "year", "venue", "identifier")
FIRST_AUTHOR_UNRELIABLE = "first-author comparison not reliable"


def normalize_venue(venue):
    """Unicode, case, punctuation, ampersand and whitespace normalisation only. Abbreviations are
    never expanded: an abbreviated and a full journal title stay different."""
    if not venue:
        return ""
    t = unicodedata.normalize("NFKD", strip_markup(venue))
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).casefold()
    t = t.replace("&", " and ")
    t = re.sub(r"[^\w\s]|_", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _first_author(authors):
    for a in authors or []:
        if a.get("last_name") or a.get("collective_name") or a.get("name"):
            return a
    return None


def compare_first_author(a_authors, b_authors):
    """Returns (outcome, reason); outcome is agree / conflict / review / missing (D-064, D2)."""
    ka, kb = first_author_key(a_authors), first_author_key(b_authors)
    if not ka or not kb:
        return "missing", "first author absent"
    fa, fb = _first_author(a_authors), _first_author(b_authors)
    coll_a = bool(fa.get("collective_name")) and not fa.get("last_name")
    coll_b = bool(fb.get("collective_name")) and not fb.get("last_name")
    if coll_a != coll_b:
        return "review", FIRST_AUTHOR_UNRELIABLE + " (collective vs personal author)"
    if ka == kb:
        return "agree", None
    if ka.endswith(kb) or kb.endswith(ka) or ka.startswith(kb) or kb.startswith(ka):
        return "review", FIRST_AUTHOR_UNRELIABLE + " (compound or particle surname)"
    return "conflict", "first author differs"


def compare_identifiers(a, b):
    """By type: every shared type must match; at least one shared type is required."""
    shared = [t for t in ID_TYPES if a.get(t) and b.get(t)]
    mismatched = [t for t in shared if a[t] != b[t]]
    if mismatched:
        return "conflict", "identifier differs: " + ", ".join(mismatched)
    if not shared:
        return "missing", "no shared identifier type"
    return "agree", None


def compare_required_fields(a, b, venue_map=None):
    """Field-by-field outcome between the authoritative record a and a second source b.
    venue_map: frozenset of (authoritative venue, second-source venue) pairs, both already
    normalised with normalize_venue, from records/venue_mappings.csv (explicit reviewed mapping,
    D-064 (3)); exact pairs only, never fuzzy."""
    out = {}
    ta, tb = normalize_title(a.get("title")), normalize_title(b.get("title"))
    out["title"] = (("missing", "title absent") if not ta or not tb else
                    ("agree", None) if ta == tb else ("conflict", "title differs"))
    out["first_author"] = compare_first_author(a.get("authors"), b.get("authors"))
    ya, yb = a.get("year"), b.get("year")
    out["year"] = (("missing", "year absent") if ya is None or yb is None else
                   ("agree", None) if ya == yb else ("conflict", "year differs"))
    va, vb = normalize_venue(a.get("journal")), normalize_venue(b.get("journal"))
    out["venue"] = (("missing", "venue absent") if not va or not vb else
                    ("agree", None) if va == vb else
                    ("agree", "explicit reviewed venue mapping") if venue_map and (va, vb) in venue_map else
                    ("conflict", "venue differs"))
    out["identifier"] = compare_identifiers(a, b)
    return out


def _url_parts(url):
    if not url:
        return "", ""
    m = re.match(r"(?i)^[a-z][a-z0-9+.-]*://([^/?#:]+)(?::\d+)?([^?#]*)", str(url).strip())
    return (m.group(1).lower(), m.group(2)) if m else ("", "")


def source_provider(m):
    """The repository that holds the underlying record, from recorded source and URL only."""
    s = m["source"]
    if s in ("pubmed", "arxiv", "europepmc", "crossref", "consensus", "semantic_scholar"):
        return s
    host, path = _url_parts(m.get("source_url"))
    if host in ARXIV_HOSTS:
        return "arxiv"
    if host == "pubmed.ncbi.nlm.nih.gov":
        return "pubmed"
    if host == "pmc.ncbi.nlm.nih.gov" or (host == "www.ncbi.nlm.nih.gov" and path.lower().startswith("/pmc")):
        return "pmc"
    if host == "europepmc.org" or host.endswith(".europepmc.org"):
        return "europepmc"
    if s == "publisher_site":
        return "publisher:" + (host or "unknown")
    return f"{s}:{host}" if host else s


# retrieval routes whose output is saved without transcription (collection_workflow.md §2,
# routes A and B; D-023): script retrieval via E-utilities and verbatim PubMed-connector output.
# crossref_api: script retrieval of Crossref /works/{DOI}, raw response saved byte for byte with its
# SHA-256 in the manifest (recorded retrieval, D-064 (1), (10)); used as second-source evidence only.
RETRIEVAL_ROUTES = {"eutils_api", "pubmed_connector", CROSSREF_SOURCE_ROUTE}


def _recorded_provenance(m):
    """Retrieved through a recorded non-transcription route, or transcribed with a passed
    spot-check. A non-transcribed record from any other or a missing route does not qualify."""
    if m["transcribed"]:
        return m["transcription_check"] == "passed"
    return m.get("route") in RETRIEVAL_ROUTES


def _url_only(m):
    orig = m.get("original") or {}
    return (isinstance(orig, dict) and orig.get("identifiers_parsed_from_url") is True
            and not (m.get("authors") and m.get("year") is not None and m.get("journal")))


def source_independence(a, c):
    """(value, basis) with value independent / not_independent / undetermined (D-064 table)."""
    pa, pc = source_provider(a), source_provider(c)
    if _url_only(c):
        return "not_independent", "URL-only corroboration (identifier parsed from URL, no bibliographic metadata)"
    if pa == pc:
        return "not_independent", f"same underlying repository ({pa})"
    pair = {pa, pc}
    if pair == {"pubmed", "europepmc"}:
        epmc = a if pa == "europepmc" else c
        if str((epmc.get("original") or {}).get("source", "")).upper() == "MED":
            return "not_independent", "Europe PMC MED record copies PubMed"
        return "undetermined", "Europe PMC record without a recorded independent origin"
    if pair == {"pubmed", "pmc"}:
        return "undetermined", "PubMed vs PMC is undetermined by default (D-064)"
    other = pc if pa == "pubmed" else pa if pc == "pubmed" else None
    if other is not None and (other == "crossref" or other.startswith("publisher:")):
        if _recorded_provenance(a) and _recorded_provenance(c):
            return "independent", f"PubMed vs {other} with recorded retrieval or checked transcription"
        return "undetermined", f"PubMed vs {other} without recorded retrieval or checked transcription"
    if "consensus" in pair:
        return "undetermined", "Consensus record without a recorded underlying source"
    return "undetermined", f"unclassified source relationship ({pa} vs {pc})"


def evaluate_second_sources(auth, candidates, venue_map=None):
    """Classify, check eligibility and compare every candidate against the authoritative record."""
    rows = []
    for c in sorted(candidates, key=lambda m: m["source_record_id"]):
        value, basis = source_independence(auth, c)
        row = {"source_record_id": c["source_record_id"], "source": c["source"],
               "provider": source_provider(c), "independence": value, "independence_basis": basis}
        if value != "independent":
            row.update(eligible=False, eligibility_reason=f"independence {value}", result="ineligible")
        elif c["transcribed"] and c["transcription_check"] != "passed":
            row.update(eligible=False, eligibility_reason="transcribed, spot-check not passed",
                       result="ineligible")
        else:
            fields = compare_required_fields(auth, c, venue_map)
            outcomes = {f: o for f, (o, _) in fields.items()}
            row.update(eligible=True, eligibility_reason="eligible",
                       fields={f: {"outcome": o, "reason": r} for f, (o, r) in fields.items()})
            if "conflict" in outcomes.values():
                row["result"] = "conflict"
            elif "review" in outcomes.values():
                row["result"] = "review"
            elif "missing" in outcomes.values():
                row["result"] = "insufficient"
            else:
                row["result"] = "agrees"
        rows.append(row)
    return {"authoritative_source_record_id": auth["source_record_id"], "candidates": rows}


def auto_verification(members, conflicts, details=None, venue_map=None):
    """Bibliographic verification status (collection_workflow.md §4.3; D-064). When `details` is a
    dict, the second-source evaluation is written into it for report-level output only.
    Crossref verification records (route crossref_api) are second-source candidates only: they are
    never the authoritative record. While CROSSREF_YEAR_FIELDS is None a Crossref year is always
    missing, so a Crossref record can never make a publication `verified`; a conflict it shows on
    title, first author, venue or identifier still gives `needs_review` (D-064 A4: conflicts are not
    outvoted and do not depend on the year rule)."""
    hard = {c["field"] for c in conflicts} & {"title", "year", "doi", "pmid"}
    if hard:
        return "needs_review", "conflicting " + ", ".join(sorted(hard))
    if all(m["metadata_missing"] for m in members):
        return "unverified", "no metadata retrieved"
    sources = {m["source"] for m in members if not m["metadata_missing"]}
    auth = [m for m in members if m["source"] in AUTHORITATIVE_SOURCES and not m["metadata_missing"]
            and m.get("route") != CROSSREF_SOURCE_ROUTE
            and (m.get("pmid") or m.get("doi") or m.get("arxiv_id"))]
    if not auth:
        return "unverified", "no authoritative index record with a persistent identifier"
    # transcribed connector data counts only if its transcription spot-check passed
    trusted_auth = [m for m in auth if not m["transcribed"] or m["transcription_check"] == "passed"]
    if not trusted_auth:
        return "partially_verified", "authoritative record is transcribed and not yet spot-checked"
    if len(sources) < 2:
        return "partially_verified", "single source: " + ", ".join(sorted(sources))
    primary = sorted(trusted_auth, key=_source_rank)[0]
    evaluation = evaluate_second_sources(
        primary, [m for m in members if m is not primary and not m["metadata_missing"]], venue_map)
    if details is not None:
        details.update(evaluation)
    cands = evaluation["candidates"]
    conflicted = [r for r in cands if r["result"] == "conflict"]
    review = [r for r in cands if r["result"] == "review"]
    if conflicted:
        fields = sorted({f for r in conflicted for f, v in r["fields"].items() if v["outcome"] == "conflict"})
        return "needs_review", ("conflict with independent second source: " + ", ".join(fields)
                                + " (" + ", ".join(r["source_record_id"] for r in conflicted) + ")")
    if review:
        reasons = sorted({v["reason"] for r in review for v in r["fields"].values() if v["outcome"] == "review"})
        return "needs_review", "; ".join(reasons) + " (" + ", ".join(r["source_record_id"] for r in review) + ")"
    agree = [r for r in cands if r["result"] == "agrees"]
    if agree:
        return "verified", ("independent second source agrees on all required fields: "
                            + ", ".join(sorted({r["provider"] for r in agree})))
    why = []
    for r in cands:
        if r["result"] == "insufficient":
            missing = [f for f, v in r["fields"].items() if v["outcome"] == "missing"]
            why.append(f"{r['provider']} lacks {', '.join(missing)}")
        else:
            why.append(f"{r['provider']} {r['eligibility_reason']}")
    return "partially_verified", "no qualifying independent second source: " + "; ".join(sorted(set(why)))


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


VENUE_MAPPING_COLS = ("authoritative_venue", "second_source_venue", "basis", "reviewer", "date")


def load_venue_mappings(rec_dir):
    """records/venue_mappings.csv: explicit, reviewed venue pairs (D-064 (3)). Every row needs all
    columns; pairs are compared after normalize_venue only (no fuzzy matching). Returns a frozenset of
    normalised (authoritative, second-source) pairs. Raises ValueError (nothing is written) on an
    incomplete, duplicated or pointless row."""
    rows = _read_csv(Path(rec_dir) / "venue_mappings.csv")
    pairs, errors = set(), []
    for n, r in enumerate(rows, start=2):
        if any(not (r.get(c) or "").strip() for c in VENUE_MAPPING_COLS):
            errors.append(f"line {n}: every column of {', '.join(VENUE_MAPPING_COLS)} is required")
            continue
        pair = (normalize_venue(r["authoritative_venue"]), normalize_venue(r["second_source_venue"]))
        if pair[0] == pair[1]:
            errors.append(f"line {n}: the two venues are already equal after normalisation")
        elif pair in pairs:
            errors.append(f"line {n}: duplicate mapping")
        pairs.add(pair)
    if errors:
        raise ValueError("records/venue_mappings.csv: " + "; ".join(errors))
    return frozenset(pairs)


def attach_verification_records(ver, records, clusters, ids, rows, rec_dir):
    """Attach Crossref verification records to existing publications. Each record must carry the
    DOI it was requested for, that DOI must belong to exactly one existing publication, that
    publication must be the paper ID named in the request, and the paper ID must be listed in
    records/verification_pilot.csv. Anything else stops the build (nothing written).
    Returns {cluster index: [verification records]}."""
    if not ver:
        return {}
    pilot = {r["paper_id"].strip() for r in _read_csv(Path(rec_dir) / "verification_pilot.csv")
             if (r.get("paper_id") or "").strip()}
    requests = {r["raw_file"]: json.loads(r["request_json"] or "{}") for r in rows if r["route"] == CROSSREF_ROUTE}
    query_ids = {r["raw_file"]: r["query_id"] for r in rows if r["route"] == CROSSREF_ROUTE}
    by_doi = {}
    for c, idx in enumerate(clusters):
        for i in idx:
            if records[i].get("doi"):
                by_doi.setdefault(records[i]["doi"], set()).add(c)
    out, errors = {}, []
    for v in sorted(ver, key=lambda r: r["source_record_id"]):
        req = requests.get(v["raw_file"], {})
        want_pid = req.get("paper_id")
        want_doi = normalize_doi(req.get("doi"))
        where = f"{v['raw_file']} ({want_pid})"
        if query_ids.get(v["raw_file"]) != VERIFY_PREFIX + str(want_pid):
            errors.append(f"{where}: query ID does not name the requested paper ID")
            continue
        if not want_doi or want_doi != v["doi"]:
            errors.append(f"{where}: returned DOI {v['doi']} differs from requested DOI {want_doi}")
            continue
        cs = by_doi.get(v["doi"], set())
        if len(cs) != 1:
            errors.append(f"{where}: DOI {v['doi']} matches {len(cs)} existing publications (exactly one required)")
            continue
        (c,) = cs
        if ids[c] != want_pid:
            errors.append(f"{where}: DOI {v['doi']} belongs to {ids[c]}, not to the requested paper ID")
            continue
        if want_pid not in pilot:
            errors.append(f"{where}: paper ID not listed in records/verification_pilot.csv")
            continue
        out.setdefault(c, []).append(v)
    if errors:
        raise RuntimeError("Crossref verification records cannot be attached (nothing written): " + "; ".join(errors))
    return out


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
    # Crossref verification records take no part in deduplication, paper-ID assignment, metadata
    # merging or search provenance; they are attached afterwards as second-source evidence only.
    verification_records = [r for r in records if r["route"] == CROSSREF_SOURCE_ROUTE]
    records = [r for r in records if r["route"] != CROSSREF_SOURCE_ROUTE]
    venue_map = load_venue_mappings(rec_dir)

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
    # checked before the registry is touched: an unattachable verification record stops the build
    # with nothing written (assign_ids only appends registry rows for new keys of base records)
    ids_preview = {}
    if verification_records:
        ids_preview, _ = _preview_ids(clusters, records, rec_dir / "paper_id_registry.csv")
        attach_verification_records(verification_records, records, clusters, ids_preview, rows, rec_dir)
    ids, reg_conflicts = assign_ids(clusters, records, rec_dir / "paper_id_registry.csv", today)
    attached = attach_verification_records(verification_records, records, clusters, ids, rows, rec_dir)
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
    second_source_rows = []      # D-064 report-level evaluation (A6: not stored in publication records)
    for c, idx in enumerate(clusters):
        members = [records[i] for i in idx]
        primary, pub, prov, conflicts = merge_cluster(members)
        pid = ids[c]
        vdetails = {}
        # attached Crossref records are second-source candidates only; everything else in this
        # publication record (fields, provenance, sources, query IDs, timestamps) comes from `members`
        status, note = auto_verification(members + attached.get(c, []), conflicts, vdetails, venue_map)
        auto_status = status
        if pid in overrides:
            status = overrides[pid]["verification_status"]
            note = f"manual override by {overrides[pid].get('reviewer','?')} on {overrides[pid].get('date','?')}: {overrides[pid].get('note','')}"
        if vdetails.get("candidates"):
            second_source_rows.append({"paper_id": pid, "verification_status": status,
                                       "automatic_status": auto_status, **vdetails})
        sc = screening.get(pid)
        ft = fulltext.get(pid)
        if pid in review_by_pid:
            dup = "possible_duplicate_review"
        elif len(members) > 1:
            dup = "merged_duplicates"
        else:
            dup = "unique"
        source_dbs = sorted({m["source"] for m in members},
                            key=lambda s: SOURCE_PRIORITY.index(s) if s in SOURCE_PRIORITY else 99)
        pubs.append({
            "paper_id": pid,
            **pub,
            "source_databases": source_dbs,
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
            "publication_type": derive_publication_type(pub.get("publication_types"), source_dbs),
        })
    pubs.sort(key=lambda p: int(p["paper_id"][1:]))

    if check_schema:
        validate_outputs(records + verification_records, pubs)

    # status changes against the previous build output, read before it is overwritten
    prev_path = rec_dir / "publications.jsonl"
    prev_status = {}
    if prev_path.exists():
        with open(prev_path) as f:
            for line in f:
                if line.strip():
                    q = json.loads(line)
                    prev_status[q["paper_id"]] = q.get("verification_status")
    status_changes = {
        "previous_build_available": prev_path.exists(),
        "changed": [{"paper_id": p["paper_id"], "previous": prev_status[p["paper_id"]],
                     "current": p["verification_status"], "note": p["verification_note"]}
                    for p in pubs if p["paper_id"] in prev_status
                    and prev_status[p["paper_id"]] != p["verification_status"]],
        "new_publications": sum(1 for p in pubs if p["paper_id"] not in prev_status),
        "removed_publications": sorted(set(prev_status) - {p["paper_id"] for p in pubs}),
    }

    with open(rec_dir / "source_records.jsonl", "w") as f:
        for r in sorted(records + verification_records, key=lambda r: r["source_record_id"]):
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
        # D-028: unrecognised source types (publication_type "other" when nothing else matched);
        # the build does not fail; the mapping table is extended only by a logged change
        "unmapped_publication_types": _count(t for p in pubs
                                             for t in unmapped_publication_types(p["publication_types"])),
        "screening_decision": _count(p["screening_decision"] for p in pubs),
        "publications_without_stable_registry_key": sum(
            1 for c in clusters if not any(record_keys(records[i]) for i in c)),
        "verification_second_sources": {
            "rule": "D-064",
            "independence": _count(r["independence"] for p in second_source_rows for r in p["candidates"]),
            "eligibility": _count(r["eligibility_reason"] for p in second_source_rows for r in p["candidates"]),
            "results": _count(r["result"] for p in second_source_rows for r in p["candidates"]),
            "publications": second_source_rows,
        },
        "verification_status_changes": status_changes,
    }
    if verification_records or venue_map:
        report["crossref_verification"] = {
            "year_fields": list(CROSSREF_YEAR_FIELDS) if CROSSREF_YEAR_FIELDS else None,
            "verification_records": len(verification_records),
            "attached": [{"paper_id": ids[c], "source_record_id": v["source_record_id"], "doi": v["doi"],
                          "raw_file": v["raw_file"], "raw_sha256": v["raw_sha256"]}
                         for c in sorted(attached, key=lambda c: ids[c]) for v in attached[c]],
            "venue_mappings": len(venue_map),
        }
    with open(rec_dir / "build_report.json", "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    return report


def unmapped_publication_types(source_types):
    """Source types that are neither in PUBLICATION_TYPE_MAP nor in PUBLICATION_TYPES_IGNORED."""
    known = {t for _, names in PUBLICATION_TYPE_MAP for t in names} | PUBLICATION_TYPES_IGNORED
    return sorted({t for t in (source_types or []) if t and t not in known})


def derive_publication_type(source_types, source_databases):
    """D-028 publication_type from source metadata only (first match wins).
    source_types: the publication-level source types (as kept in source_publication_types);
    source_databases: the publication's source databases, field-priority source first.
    No class-bearing type: "other" if an unrecognised type is present (it is also reported as
    unmapped), otherwise "unknown" (no type at all, or only types not used for the class).
    Never looks at URLs, DOIs or titles."""
    types = list(source_types or [])
    arxiv = bool(source_databases) and source_databases[0] == "arxiv"
    for value, names in PUBLICATION_TYPE_MAP:
        if any(t in names for t in types) or (value == "preprint" and arxiv):
            return value
    return "other" if unmapped_publication_types(types) else "unknown"


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


def _rq5_group_for(n_yes):
    """D-034 thresholds (unchanged): >= 4 yes qualified, exactly 3 near_rq5, 0-2 below_threshold."""
    return "qualified" if n_yes >= 4 else "near_rq5" if n_yes == 3 else "below_threshold"


def derive_rq5_coverage_group(statuses):
    """D-034 coverage group from the five CONFIRMED (full-text) component statuses (D-035).
    Returns (group, provisional): both None when any component is not assessed (empty/None);
    otherwise group is "qualified" (>= 4 yes), "near_rq5" (exactly 3) or "below_threshold" (0-2),
    and "unclear" never counts as yes.
    provisional (D-037-A1): True only when some resolution of the "unclear" statuses to yes/no,
    with all other statuses held fixed, gives a different group. Every resolution is checked.
    Used by build() for rq5_coverage_group / rq5_coverage_provisional (D-036, D-037); a coverage
    descriptor only, never a quality judgment, and never assigned by a screener."""
    vals = [statuses.get(name) for name in RQ5_COMPONENT_FIELDS]
    if any(v in (None, "") for v in vals):
        return None, None
    bad = [v for v in vals if v not in ("yes", "no", "unclear")]
    if bad:
        raise ValueError(f"invalid component status {bad}")
    n_yes = vals.count("yes")
    group = _rq5_group_for(n_yes)
    n_unclear = vals.count("unclear")
    provisional = any(_rq5_group_for(n_yes + resolved.count("yes")) != group
                      for resolved in itertools.product(("yes", "no"), repeat=n_unclear))
    return group, provisional


def is_stage0_rule_row(r):
    """D-068 (5): a Stage-0 rule row is an `exclude` row with reason code E5 or E7 and
    screener=rule:stage0; the D-060 (6) exemption covers only such rows."""
    return (r.get("screener") == STAGE0_SCREENER and r.get("decision") == "exclude"
            and r.get("reason_code") in STAGE0_RULE_REASON_CODES)


def scope_flag_errors(value):
    """Problems in a manually entered scope_flags value (semicolon-separated tokens; empty = none).
    Values are reported, never corrected."""
    if value == "":
        return []
    errors, seen = [], set()
    for tok in value.split(";"):
        if tok in seen and tok != "":
            errors.append(f"scope_flags={value!r}: token {tok!r} is repeated (D-078)")
            continue
        seen.add(tok)
        if tok == "":
            errors.append(f"scope_flags={value!r}: empty token")
        elif tok != tok.strip():
            errors.append(f"scope_flags={value!r}: token {tok!r} has leading or trailing whitespace")
        elif tok in BUILD_DERIVED_SCOPE_FLAGS:
            errors.append(f"scope_flags={value!r}: {tok!r} is derived by the build and cannot be entered")
        elif tok not in SCOPE_FLAG_TOKENS:
            errors.append(f"scope_flags={value!r}: token {tok!r} not in {SCOPE_FLAG_TOKENS}")
    return errors


# Frozen criteria versions (Phase 1, decisions B2-B4, researcher approval 2026-11-01). The registry
# is a machine-readable copy of the approved freeze entry (criteria v1.1 §11 step 9); it does not
# exist until a freeze is recorded, and until then screening rows are validated as before. Once it
# exists, every screening row must carry a registered frozen criteria_version (criteria v1.1 §6;
# protocol v0.2 §5 item 2). Any missing, malformed or contradictory freeze information stops
# validation (fail closed); a value is never filled in or corrected.
CRITERIA_REGISTRY_FILE = "criteria_registry.json"
CRITERIA_VERSION_FORMAT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*")   # format guard only (B1 open)
_REGISTRY_FIELDS = {
    "criteria_version": CRITERIA_VERSION_FORMAT,
    "decision_id": re.compile(r"D-\d{3}"),
    "criteria_path": re.compile(r"\S+"),
    "protocol_path": re.compile(r"\S+"),
    "freeze_commit": re.compile(r"[0-9a-f]{40}"),
    "criteria_sha256": re.compile(r"[0-9a-f]{64}"),
    "protocol_sha256": re.compile(r"[0-9a-f]{64}"),
    "effective_date": re.compile(r"\d{4}-\d{2}-\d{2}"),
}


class CriteriaRegistryError(ValueError):
    """Freeze information is missing, malformed or contradictory (fail closed)."""


def decision_log_path(lit_dir):
    """`logs/DECISION_LOG.md` of the repository that holds `<repo>/research/literature`."""
    return Path(lit_dir).resolve().parents[1] / "logs" / "DECISION_LOG.md"


# Run authorisations (Phase 1 correction 1; convention D-088, answering Q-090; hardened in the
# Stage B preparation under D-095). A run of the Stage-0 generator or of the pilot sampler and sheet
# needs a separate, explicit researcher authorisation (D-074 (f); D-077 (6)). A reference is accepted
# only if it names exactly one decision row of DECISION_LOG.md such that:
# * its Decision cell BEGINS with the exact bold marker below (only the cell's surrounding whitespace
#   is ignored; a marker anywhere else, e.g. in a decision that describes this convention, is not an
#   authorisation);
# * its Status cell reads exactly RUN_AUTHORISATION_STATUS (D-088 (3)); conditional, in-principle,
#   implementation, proposed or other statuses are refused;
# * its Decision text binds the run (D-088 (4)) with each of these fields exactly once, separated by
#   semicolons (backticks are ignored; format = D-097, APPROVED — PROVISIONAL, final review pending):
#       criteria_version: <id>; inventory_sha256: <64 hex>; freeze_entry: D-nnn;
#       d035_s6_records: D-nnn, D-nnn, D-nnn, D-nnn, D-nnn, D-nnn; single_use: yes
# * the freeze entry is one approved decision row and the registered criteria version names it
#   (criteria_registry.json); the six D-035 record §6 rows (one per condition, D-092) are distinct
#   approved decision rows whose Decision cell begins with "**D-035 §6 condition N recorded as met.**"
#   (wording = D-097, APPROVED — PROVISIONAL, final review pending)
#   and contains that sentence once, covering N = 1 to 6 (a decision that only mentions a condition
#   is not a condition record);
# * when the calling tool passes them, the run's inventory SHA-256 and criteria version equal the
#   bound values.
# Single use (D-088 (4)) is enforced by an append-only ledger: each tool may use an authorisation
# once (D-074 (f): the Stage-0 generator; D-077 (6): one draw and one sheet). No current decision
# begins with a marker, so no run is authorised by this code.
RUN_AUTHORISATION_MARKERS = {
    "D-074 (f)": "**Run authorisation under D-074 (f).**",
    "D-077 (6)": "**Run authorisation under D-077 (6).**",
}
RUN_AUTHORISATION_STATUS = "**APPROVED** — run authorisation (single use)"
RUN_AUTHORISATION_TOOLS = {"D-074 (f)": ("stage0",), "D-077 (6)": ("pilot_sample", "pilot_sheet")}
RUN_LEDGER_FILE = "screening/run_authorisation_ledger.jsonl"
_BINDING_PATTERNS = {
    "criteria_version": r"([A-Za-z0-9][A-Za-z0-9._+-]*)",
    "inventory_sha256": r"([0-9a-f]{64})",
    "freeze_entry": r"(D-\d{3})",
    "d035_s6_records": r"(D-\d{3}(?:\s*,\s*D-\d{3})*)",
    "single_use": r"(yes)",
}
_S6_CONDITION = re.compile(r"\*\*D-035 §6 condition ([1-6]) recorded as met\.\*\*")


class RunAuthorisationError(ValueError):
    """A run-authorisation reference is missing, invented or does not authorise this run."""


def _decision_rows(log_lines, ref):
    return [line for line in log_lines if re.match(rf"\| {re.escape(ref)} \| 20\d\d-", line)]


def _one_decision_row(log_lines, ref, log_name, role="authorisation"):
    """Return (decision cell, status cell) of the single decision row of `ref`."""
    rows = _decision_rows(log_lines, ref)
    if not rows:
        raise RunAuthorisationError(f"refused: {ref} ({role}) is not a decision in {log_name}")
    if len(rows) > 1:
        raise RunAuthorisationError(f"refused: {ref} ({role}) has more than one decision row in {log_name}")
    cells = rows[0].split("|")
    if len(cells) < 5:
        raise RunAuthorisationError(f"refused: {ref} ({role}) decision row is malformed")
    return cells[3], cells[4].strip()


def parse_run_authorisation_bindings(decision_text):
    """Parse the D-088 (4) bindings of a run-authorisation Decision cell; raise on any problem."""
    text = decision_text.replace("`", "")
    out = {}
    for key, pat in _BINDING_PATTERNS.items():
        n = len(re.findall(rf"(?<![\w-]){key}\s*:", text))
        if n != 1:
            raise RunAuthorisationError(f"refused: binding {key!r} must appear exactly once (found {n})")
        m = re.search(rf"(?<![\w-]){key}\s*:\s*{pat}\s*(?:;|$)", text)
        if not m:
            raise RunAuthorisationError(f"refused: binding {key!r} is malformed")
        out[key] = m.group(1)
    records = [x.strip() for x in out["d035_s6_records"].split(",")]
    if len(records) != 6 or len(set(records)) != 6:
        raise RunAuthorisationError("refused: d035_s6_records must name six distinct decision IDs (D-092)")
    out["d035_s6_records"] = records
    return out


def verify_run_authorisation(lit_dir, reference, clause, decision_log=None, *, inventory_sha256=None,
                             criteria_version=None):
    """Return the reference if DECISION_LOG.md records it as a complete, approved run authorisation
    for `clause` (a key of RUN_AUTHORISATION_MARKERS) that matches this run; raise
    RunAuthorisationError otherwise. Single use is checked separately (check_authorisation_unused)."""
    marker = RUN_AUTHORISATION_MARKERS.get(clause)
    if marker is None:
        raise RunAuthorisationError(f"unknown authorisation clause {clause!r}")
    ref = (reference or "").strip()
    if not re.fullmatch(r"D-\d{3}", ref):
        raise RunAuthorisationError(f"refused: {reference!r} is not a decision ID (D-nnn)")
    log_path = Path(decision_log) if decision_log else decision_log_path(lit_dir)
    if not log_path.exists():
        raise RunAuthorisationError(f"refused: decision log {log_path} not found")
    lines = log_path.read_text(encoding="utf-8").splitlines()
    rows = _decision_rows(lines, ref)
    if not rows:
        raise RunAuthorisationError(f"refused: {ref} is not a decision in {log_path.name}")
    if len(rows) > 1:
        raise RunAuthorisationError(f"refused: {ref} has more than one decision row in {log_path.name}")
    decision, status = _one_decision_row(lines, ref, log_path.name)
    if not status.startswith("**APPROVED**"):
        raise RunAuthorisationError(f"refused: {ref} is not an unconditional approval ({status[:60]!r})")
    if not decision.strip().startswith(marker):
        raise RunAuthorisationError(f"refused: {ref} decision does not begin with {marker!r}")
    if status != RUN_AUTHORISATION_STATUS:
        raise RunAuthorisationError(f"refused: {ref} status is not exactly {RUN_AUTHORISATION_STATUS!r} "
                                    f"(found {status[:60]!r})")
    b = parse_run_authorisation_bindings(decision.strip()[len(marker):])
    bound = [b["freeze_entry"], *b["d035_s6_records"]]
    if ref in bound or b["freeze_entry"] in b["d035_s6_records"]:
        raise RunAuthorisationError("refused: the authorisation, the freeze entry and the six §6 records "
                                    "must be distinct decisions")
    _, fz_status = _one_decision_row(lines, b["freeze_entry"], log_path.name, "freeze entry")
    if not fz_status.startswith("**APPROVED**"):
        raise RunAuthorisationError(f"refused: freeze entry {b['freeze_entry']} is not approved")
    conditions = []
    for d in b["d035_s6_records"]:
        text, st = _one_decision_row(lines, d, log_path.name, "D-035 §6 record")
        if not st.startswith("**APPROVED**"):
            raise RunAuthorisationError(f"refused: D-035 §6 record {d} is not approved")
        found = _S6_CONDITION.findall(text)
        if len(found) != 1 or not _S6_CONDITION.match(text.strip()):
            raise RunAuthorisationError(f"refused: D-035 §6 record {d} must begin with exactly one "
                                        f"'**D-035 §6 condition N recorded as met.**' (found {found})")
        conditions.append(found[0])
    if sorted(conditions) != ["1", "2", "3", "4", "5", "6"]:
        raise RunAuthorisationError(f"refused: the six §6 records cover conditions {sorted(conditions)}, "
                                    "not 1 to 6 once each")
    try:
        entries = load_criteria_registry_entries(lit_dir, decision_log=log_path)
    except CriteriaRegistryError as e:
        raise RunAuthorisationError(f"refused: {e}") from None
    entry = (entries or {}).get(b["criteria_version"])
    if entry is None:
        raise RunAuthorisationError(f"refused: bound criteria_version {b['criteria_version']!r} is not a "
                                    "registered frozen version (freeze required)")
    if entry["decision_id"] != b["freeze_entry"]:
        raise RunAuthorisationError(f"refused: freeze entry {b['freeze_entry']} does not match the registry "
                                    f"({entry['decision_id']}) for {b['criteria_version']!r}")
    if inventory_sha256 is not None and inventory_sha256 != b["inventory_sha256"]:
        raise RunAuthorisationError("refused: the run's inventory SHA-256 differs from the bound inventory_sha256")
    if criteria_version is not None and criteria_version != b["criteria_version"]:
        raise RunAuthorisationError("refused: the run's criteria_version differs from the bound criteria_version")
    return ref


LEDGER_EVENTS = ("started", "completed")
RUN_LOCK_FILE = "screening/.run_lock.tmp"   # ignored by Git (D-096 rule for *.tmp)


def _ledger_path(lit_dir):
    return Path(lit_dir) / RUN_LEDGER_FILE


def authorisation_uses(lit_dir):
    """Entries of the append-only run-authorisation ledger. Each authorised write run appends a
    "started" entry before it writes and a "completed" entry after its outputs are in place (L5,
    pre-commit audit corrections). Fails closed on malformed or inconsistent content: unknown event,
    "completed" without an earlier "started", or a repeated event for one authorisation and tool."""
    path = _ledger_path(lit_dir)
    if not path.exists():
        return []
    uses, seen = [], set()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            e = json.loads(line)
        except ValueError:
            raise RunAuthorisationError(f"refused: {path.name} line {n} is not JSON") from None
        if not (isinstance(e, dict) and all(isinstance(e.get(k), str) and e.get(k)
                                            for k in ("authorization", "clause", "tool", "run_time_utc", "event"))):
            raise RunAuthorisationError(f"refused: {path.name} line {n} is malformed")
        key = (e["authorization"], e["tool"])
        if e["event"] not in LEDGER_EVENTS:
            raise RunAuthorisationError(f"refused: {path.name} line {n} has unknown event {e['event']!r}")
        if (key, e["event"]) in seen:
            raise RunAuthorisationError(f"refused: {path.name} line {n} repeats {e['event']} for {key} (inconsistent)")
        if e["event"] == "completed" and (key, "started") not in seen:
            raise RunAuthorisationError(f"refused: {path.name} line {n} completes a run that never started (inconsistent)")
        seen.add((key, e["event"]))
        uses.append(e)
    return uses


def check_authorisation_unused(lit_dir, reference, clause, tool):
    """Single use (D-088 (4)): refuse if `tool` already started a run with this authorisation
    (completed, or interrupted: an interrupted run also consumes it, fail closed), or if the
    authorisation was used under another clause."""
    if tool not in RUN_AUTHORISATION_TOOLS.get(clause, ()):
        raise RunAuthorisationError(f"refused: tool {tool!r} cannot use a {clause} authorisation")
    uses = authorisation_uses(lit_dir)
    for e in uses:
        if e["authorization"] != reference:
            continue
        if e["clause"] != clause:
            raise RunAuthorisationError(f"refused: {reference} was already used under {e['clause']} (single use)")
        if e["tool"] == tool:
            done = any(x["authorization"] == reference and x["tool"] == tool and x["event"] == "completed"
                       for x in uses)
            if done:
                raise RunAuthorisationError(f"refused: {reference} was already used by {tool} on "
                                            f"{e['run_time_utc']} (single use)")
            raise RunAuthorisationError(f"refused: a {tool} run with {reference} started on {e['run_time_utc']} "
                                        "and never completed (interrupted); the authorisation is consumed "
                                        "(single use) and the outputs must be inspected")


def require_completed_use(lit_dir, reference, tool):
    """Refuse unless `tool` completed a run with this authorisation (e.g. the draw before the sheet)."""
    if not any(e["authorization"] == reference and e["tool"] == tool and e["event"] == "completed"
               for e in authorisation_uses(lit_dir)):
        raise RunAuthorisationError(f"refused: no completed {tool} run with {reference} in {Path(RUN_LEDGER_FILE).name}")


def _append_ledger(lit_dir, entry):
    path = _ledger_path(lit_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def record_authorisation_start(lit_dir, reference, clause, tool, run_time_utc, details=None):
    """Append a "started" entry before an authorised write (checks that the authorisation is unused)."""
    check_authorisation_unused(lit_dir, reference, clause, tool)
    _append_ledger(lit_dir, {"authorization": reference, "clause": clause, "tool": tool, "event": "started",
                             "run_time_utc": run_time_utc, **(details or {})})


def record_authorisation_completion(lit_dir, reference, clause, tool, run_time_utc, details=None):
    """Append a "completed" entry once the run's outputs are in place."""
    uses = authorisation_uses(lit_dir)
    started = any(e["authorization"] == reference and e["tool"] == tool and e["event"] == "started" for e in uses)
    done = any(e["authorization"] == reference and e["tool"] == tool and e["event"] == "completed" for e in uses)
    if not started or done:
        raise RunAuthorisationError(f"refused: cannot complete {tool} with {reference} (ledger: started={started}, "
                                    f"completed={done})")
    _append_ledger(lit_dir, {"authorization": reference, "clause": clause, "tool": tool, "event": "completed",
                             "run_time_utc": run_time_utc, **(details or {})})


@contextlib.contextmanager
def run_lock(lit_dir):
    """Exclusive lock for authorised write runs in one literature directory (L5). Created with
    O_EXCL, so a second concurrent run is refused; removed when the run ends normally or by an
    exception. A lock left by a killed process is never removed automatically: the run is treated as
    interrupted and must be inspected by hand."""
    path = Path(lit_dir) / RUN_LOCK_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        raise RunAuthorisationError(f"refused: {path} exists: another authorised run is in progress, or an "
                                    "earlier run was interrupted (inspect the outputs and the ledger, then "
                                    "remove the lock by hand)") from None
    try:
        os.write(fd, json.dumps({"pid": os.getpid(),
                                 "time_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}).encode())
        os.close(fd)
        yield path
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def write_new_file_atomically(path, text, check=None):
    """Create `path` with `text` without ever overwriting an existing file (L5): the content is
    written to a temporary file in the same directory, flushed, optionally checked with `check(tmp)`,
    and then hard-linked to `path`, which fails if `path` already exists. The temporary file is
    always removed. Raises FileExistsError if `path` exists."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.stem}.", suffix=".tmp", dir=path.parent)
    try:
        if check is not None:
            check(Path(tmp))                     # e.g. the temporary path must also be ignored by Git
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            fd = None
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.link(tmp, path)
    finally:
        if fd is not None:
            os.close(fd)
        if os.path.exists(tmp):
            os.unlink(tmp)
    return path


def load_criteria_registry(lit_dir, decision_log=None):
    """Return the frozenset of registered frozen criteria versions, or None when no registry exists
    (see load_criteria_registry_entries)."""
    entries = load_criteria_registry_entries(lit_dir, decision_log)
    return None if entries is None else frozenset(entries)


def load_criteria_registry_entries(lit_dir, decision_log=None):
    """Return {criteria_version: registry entry}, or None when no registry exists.

    The registry is cross-checked against the decision log: each entry's decision ID must have a
    row in DECISION_LOG.md that states the identifier, the freeze commit and both SHA-256 values.
    Raises CriteriaRegistryError on any malformed or contradictory content."""
    path = Path(lit_dir) / CRITERIA_REGISTRY_FILE
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise CriteriaRegistryError(f"{path}: unreadable criteria registry ({e})") from None
    entries = data.get("frozen_versions") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise CriteriaRegistryError(f"{path}: 'frozen_versions' must be a non-empty list")
    log_path = Path(decision_log) if decision_log else decision_log_path(lit_dir)
    if not log_path.exists():
        raise CriteriaRegistryError(f"{path}: decision log {log_path} not found for the cross-check")
    log_rows = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (D-\d{3}) \|", line)
        if m:
            log_rows.setdefault(m.group(1), line)
    versions = {}
    for i, e in enumerate(entries):
        where = f"{path}: frozen_versions[{i}]"
        if not isinstance(e, dict):
            raise CriteriaRegistryError(f"{where}: entry must be an object")
        for k, pat in _REGISTRY_FIELDS.items():
            v = e.get(k)
            if not isinstance(v, str) or not pat.fullmatch(v):
                raise CriteriaRegistryError(f"{where}: missing or malformed {k!r}")
        cv = e["criteria_version"]
        if cv in versions and versions[cv] != e:
            raise CriteriaRegistryError(f"{where}: contradictory entries for criteria_version {cv!r}")
        row = log_rows.get(e["decision_id"])
        if row is None:
            raise CriteriaRegistryError(f"{where}: {e['decision_id']} not found in {log_path.name}")
        absent = [k for k in ("criteria_version", "freeze_commit", "criteria_sha256", "protocol_sha256")
                  if e[k] not in row]
        if absent:
            raise CriteriaRegistryError(f"{where}: {e['decision_id']} in {log_path.name} does not state {absent}")
        versions[cv] = e
    return versions


def load_screening_decisions(lit_dir, path=None):
    """Read and validate screening/decisions.csv (or `path`, a candidate file validated before it
    replaces the real one). Any invalid row stops the build (no row is silently dropped). Returns
    the rows as dicts (all columns as strings)."""
    path = Path(path) if path else Path(lit_dir) / "screening" / "decisions.csv"
    if not path.exists():
        return []
    frozen_versions = load_criteria_registry(lit_dir)   # None until a freeze is registered
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        missing = [c for c in SCREENING_REQUIRED if c not in cols]
        retired = [c for c in cols if c in RETIRED_SCREENING_COLUMNS]
        unknown = [c for c in cols if c not in SCREENING_REQUIRED + SCREENING_OPTIONAL + retired]
        if missing or unknown or retired:
            raise ValueError(f"{path}: missing columns {missing}, unknown columns {unknown}"
                             + (f", retired columns {retired} (dim_independent_validation is replaced by "
                                "validation_design, D-029/D-060; values are not converted: record "
                                "validation_design instead)" if retired else ""))
        raw = list(reader)
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in raw]
    errors = []
    for n, (r, r_raw) in enumerate(zip(rows, raw), start=2):
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
        cv = r["criteria_version"]
        if cv and not CRITERIA_VERSION_FORMAT.fullmatch(cv):
            errors.append(f"{where}: malformed criteria_version {cv!r}")
        if frozen_versions is not None:
            if not cv:
                errors.append(f"{where}: criteria_version required once a frozen version is registered")
            elif cv not in frozen_versions:
                errors.append(f"{where}: criteria_version {cv!r} is not a registered frozen version")
        if r["rq_tags"] and not RQ_TAGS.fullmatch(r["rq_tags"]):
            errors.append(f"{where}: rq_tags must be like RQ1;RQ3")
        # checked on the value as written (before stripping), so padded tokens are reported, not fixed
        errors += [f"{where}: {e}" for e in scope_flag_errors(r_raw.get("scope_flags") or "")]
        if (r["stage"] == "title_abstract" and r["decision"] in ("include", "uncertain")
                and not is_stage0_rule_row(r)):
            absent = [k for k in TITLE_ABSTRACT_REQUIRED if not r[k]]
            if absent:
                errors.append(f"{where}: {r['decision']} at title_abstract requires {absent} (D-060 (6))")
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
