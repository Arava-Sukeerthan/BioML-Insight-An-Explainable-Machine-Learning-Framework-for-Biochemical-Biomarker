# Q-065 Decision Package — Screening Scope and Schedule

| Field | Value |
|---|---|
| Task | Q-065-DECISION-PACKAGE (2026-10-29, Day 16; assistant label, no researcher task ID) |
| Status | **For the researcher's decision. Nothing is decided, approved, activated or screened by this package.** Q-065 stays Open; every decision status is unchanged |
| Screening status | **INACTIVE** (D-035 record §6 conditions 2–6 unmet; `research/reviews/screening_activation_decision_brief_D035.md`) |
| Repository state | `claude/eloquent-mccarthy-bqtxr3` at `5d92d94286a0a8257222a662241b016c545618d5` |
| Labels | `[EVIDENCE]` = stated in a cited repository record or computed here from committed metadata with the method shown; `[HYPOTHESIS]` = unmeasured estimate; `[RECOMMENDATION]` = assistant proposal, not approval; `[OPEN]` = listed in `unresolved_questions.md` |

---

## A. Scope and provenance

### A.1 The question
Q-065 `[OPEN]` (due **2026-11-01**): "Screening scope under the deadline: accept the LIT-005 priority strand (G-1…G-7 hits, Q-PM-02, Q-PM-11/12; `LIT-005_evidence_review.md` §8) for title/abstract screening first, with the remaining strands screened only if time permits and the reduced scope reported? Requires the D-035 §6 conditions to be met first."

Related records: D-005 (review type, PROPOSED); D-008 (screening procedure, PROPOSED); D-009 / Q-007 (Q-PM-02 handling, PROPOSED / Open); D-025 (pilot, PROPOSED); D-018 (baselines, PENDING); D-042 (stage order, APPROVED); schedule: D-001 (PROPOSED), Q-013, Q-058 (Open), protocol CUP-11.

### A.2 Source inventory `[EVIDENCE]`
| File | SHA-256 | Git blob at HEAD |
|---|---|---|
| `research/literature/paper_inventory.json` (primary input) | `a509538dc5e1cf41cd7a4e180ed17df86f6d4cd83a7d227abea073f1689af4a3` | `9f84275f38f4fb22b62b83ee70e3dab1518e2ae6` |
| `research/literature/paper_inventory.csv` (independent check) | `8fc5bea9c57f486ea1099f4f9f3902f2537144c0f22af36f1b556a44d4891846` (equals `collection_stats.json`) | — |

Both files are identical to the committed versions (`git diff --quiet HEAD`). The inventory was built in LIT-005-REBUILD (commit `ffee9ec`): 3,386 publications, one record per deduplicated publication (`collection_workflow.md` §4.2: merge on same PMID/DOI/PMCID/arXiv ID; identifier conflicts never merged; title rules flag but do not merge across years).

### A.3 Counting procedure `[EVIDENCE]`
- **Fields read:** `paper_id`, `query_ids`, `pmid`, `doi`, `pmcid`, `arxiv_id`, `verification_status`, `screening_status`, `source_publication_types`, `abstract_available` (a boolean). **No title or abstract text was read, displayed or sampled.** No record was labelled.
- **Membership:** `query_ids` is a `;`-separated string of base query IDs (all 3,386 records non-empty; no malformed tokens; no date suffixes). A record belongs to a stratum if any token matches exactly:
  - G-1…G-7 = `Q-PM-G1` … `Q-PM-G7` (G-8 excluded, as in `LIT-005_evidence_review.md` §8);
  - Q-PM-02 = `Q-PM-02`;
  - Q-PM-11/12 = `Q-PM-11` or `Q-PM-12`.
- **Deduplication:** counts are of unique `paper_id`s, i.e. after the inventory's own identifier deduplication. Within the union, PMID, DOI and PMCID values are unique (0 duplicates).
- **Implementation 1:** Python, JSON inventory, set operations (script in Appendix 1).
- **Implementation 2 (independent check):** Python `csv` module on the CSV twin, counting records by membership pattern (Appendix 2), plus a `jq` count of the union on the JSON.

### A.4 Results `[EVIDENCE]`
| Stratum | Unique records |
|---|---|
| G-1…G-7 (per query: G1 44, G2 27, G3 33, G4 68, G5 1, G6 21, G7 2) | **194** |
| Q-PM-02 (routine biochemistry, RQ1) | **743** |
| Q-PM-11/12 (RQ5: Q-PM-11 102, Q-PM-12 19) | **120** |

| Overlap | Records |
|---|---|
| G-1…G-7 ∩ Q-PM-02 | 10 |
| G-1…G-7 ∩ Q-PM-11/12 | 0 |
| Q-PM-02 ∩ Q-PM-11/12 | 3 |
| all three | 0 |
| **Union** | **1,044** (194 + 743 + 120 − 10 − 0 − 3 + 0) |

Membership patterns (implementation 2): G only 184; Q-PM-02 only 730; Q-PM-11/12 only 117; G and Q-PM-02 10; Q-PM-02 and Q-PM-11/12 3; none 2,342.

**Validation:** implementations 1 and 2 and the `jq` count agree on every figure. The G per-query counts equal the hit counts recorded in LIT-005 (44/27/33/68/1/21/2). The figure 194 equals `LIT-005_evidence_review.md` §8 ("194 G-1…G-7 PMIDs"). The union 1,044 is below the brief's upper bound of "about 1,057", which had not removed overlaps.

**Characteristics of the 1,044 records** `[EVIDENCE]`: all have a PMID; 4 have no DOI; 339 have no PMCID; 1,043 `partially_verified`, 1 `verified`; 1,040 `abstract_available = True`, 4 `False`; 2 carry a retraction publication type; all `not_screened`.

### A.5 Limitations and uncertainties
1. **Retrieval, not relevance.** Stratum membership records which query retrieved a record, not whether the record is eligible. Counts are records, not studies (version pairs and companion papers count separately).
2. **Residual duplicates.** One of the 15 pending `dedup_review.csv` pairs has one member in the union (`same_title_year_differs_by_1`; the other member is outside). No union record is in the 3 registry identifier conflicts. The one metadata-conflict record (`needs_review`) is outside the union.
3. **Verification.** 1,043 of the 1,044 records are `partially_verified`. They may be screened but not cited (`research_plan.md` §6). Q-021, Q-064 and Q-068 are Open.
4. **What the strand omits** `[EVIDENCE]`: the other two RQ1 strands (Q-PM-01, metabolomics: 399 records not in the union; Q-PM-03, inborn errors with MS/MS: 44), the RQ2–RQ4 methodological strands (Q-PM-04 to Q-PM-10), RQ6 (Q-PM-13, Q-PM-14), Q-PM-15, G-8-only (235), arXiv (Q-AX) and web (Q-WS, Q-RP) records. In total, 2,342 records are outside the union.
5. **Scope decisions still open:** Q-001 (disorders) and Q-002 (biomarker class) `[OPEN]`. They decide whether Q-PM-01 and Q-PM-03 are needed at all.
6. **No workload measurement exists.** Every rate or duration below is `[HYPOTHESIS]`.

## B. Screening-scope options

**Common facts** `[EVIDENCE]`:
- No option can start before screening is activated (D-035 record §6, conditions 2–6).
- D-008 (PROPOSED): the assistant screens and the researcher blind-audits 25 includes and 25 excludes.
- D-025 (PROPOSED): a 60-record pilot with blinded double screening, κ ≥ 0.60.
- `GOVERNANCE.md` §3: researcher time ≈ 1 h/day.
- D-018 (PENDING) requires "Methods most used in the included **RQ1** studies". `search_strategy.md` defines RQ1 as Q-PM-01, Q-PM-02 and Q-PM-03.
- D-042 (APPROVED): the Stage C and Stage D gates must pass before D-017, D-018 and D-019 are approved.

| | Option 1 — Priority strand (Q-065 as proposed) | Option 2 — Entire inventory | Option 3 — Decision-linked scope: priority strand + remaining RQ1 strands |
|---|---|---|---|
| Records | **1,044** | **3,386** | **1,470** (adds Q-PM-01 and Q-PM-03: +426) |
| Coverage | Gap searches G-1…G-7, routine biochemistry (RQ1), RQ5 closest prior art | Every collected record, including methodological, review and arXiv/web strands | Everything in Option 1 plus the complete RQ1 application landscape (metabolomics, inborn errors) |
| Recall limits | RQ1 is incomplete (no metabolomics or inborn-error strand) unless Q-002 restricts the biomarker scope to routine chemistry; no methodological strands (RQ2–RQ4), no RQ6 reviews, no arXiv | Limited only by the searches themselves (`search_strategy.md` §3.1 recall risks; blocked databases) | RQ2–RQ4 methodological and RQ6 strands not screened; method justification would rely on targeted reading of identified references (AB-7) |
| D-005 (structured review, no completeness claim) | Compatible only if reported as a prioritised subset, with the omitted strands and their sizes stated | Fully compatible | Compatible if reported as RQ1 + RQ5 + gap searches, with the omitted strands stated |
| Stage C gate (method comparison) | Comparison can describe routine-biochemistry methods only. D-018's "included RQ1 studies" would be a partial RQ1 set unless Q-002 narrows RQ1 | Full basis | Full RQ1 basis for D-018; RQ5 basis for D-016 |
| Workload | `[HYPOTHESIS]` lowest. Not measured | `[HYPOTHESIS]` about 3.2 × Option 1 | `[HYPOTHESIS]` about 1.4 × Option 1 |
| Main risk | Under-describing the methods landscape if RQ1 is not narrowed; a closest-prior-art set limited to two queries | Time: Stage C may not pass in time for any 2026-11 deliverable | Methodological strands deferred; must be reported |

**Workload arithmetic** (illustration only, `[HYPOTHESIS]`): the ratios above are record ratios (1,470 / 1,044 ≈ 1.41; 3,386 / 1,044 ≈ 3.24). No per-record screening time has been measured. The D-025 pilot is the first point at which a rate can be measured without breaking the "no screening before activation" rule. Any absolute duration given before the pilot would be unsupported.

**Interaction with Q-007 / D-009**: all three options screen all 743 Q-PM-02 records, which is consistent with D-009 Option A (screen all), PROPOSED.

## C. Schedule options (D-001, Q-013, Q-058, CUP-11, under D-042)

**Facts** `[EVIDENCE]`:
- Today is Day 16 (2026-10-29); 2026-11-24 is 26 calendar days away.
- CUP-11 is a *target* ("a defensible manuscript by 2026-11-24"), not a gate.
- D-001 (the 45-day schedule ending 2026-11-27) is PROPOSED.
- D-042 (APPROVED): no gate passes because its date has arrived.
- Protocol §23 (draft revision 5) lists the dependency order: screening-activation decisions → pilot → screening → Stage C gate → Stage D gate (D-016) → D-017, D-018 (with D-014 approved), D-019 → Stage G (AB-1 to AB-13; not before 2026-11-03).

**Can be completed by 2026-11-24 without weakening a requirement** `[RECOMMENDATION]`, dependent on the researcher's decisions:
- the screening-activation decisions;
- criteria v1.1 and protocol v0.2 drafts;
- the restore and rebuild (Q-063 upload);
- the arXiv spot-check (Q-036);
- the pilot;
- screening of the chosen scope as far as it gets;
- a literature review to date;
- protocol and data-feasibility documentation;
- the verification-route decision (Q-021, Q-064, Q-068);
- a Rule S test plan (execution under D-040 only from 2026-11-03).

Real-data model results are possible by that date only if Stages C and D pass, D-014 and D-017 to D-019 are approved, and Stages G to J run, all within 26 days. `[HYPOTHESIS]`: unlikely at about 1 h/day of researcher time.

| Option | What it means | Dependencies | Consequence |
|---|---|---|---|
| S1 | Keep 2026-11-24 as an **interim deliverable**: literature review to date, protocol draft, data-feasibility section, no model results (protocol §23 fallback). Set the submission date after Stage J | Researcher decision on D-001/CUP-11 | No gate pressure; a manuscript with results comes later |
| S2 | **Revise D-001** to a later end date, set after the pilot measures the screening rate | Pilot (after activation) | Dates rest on measured throughput instead of `[HYPOTHESIS]` |
| S3 | Keep 2026-11-24 for a **full manuscript with results** | Every gate from C to J within 26 days | `[HYPOTHESIS]` high risk. Pressure on gates conflicts with `GOVERNANCE.md` §2 ("No stage is skipped to meet the deadline") and D-042 point (5) |

S1 and S2 can be combined: an interim deliverable on 2026-11-24, and a revised D-001 once the pilot has given a rate.

## D. Recommendation `[RECOMMENDATION]`, not a decision

1. **Scope: Option 3 (1,470 records)**, with one condition: decide Q-002 first.
   - If Q-002 restricts the biomarker scope to routine clinical chemistry, then Q-PM-01 and Q-PM-03 fall outside RQ1, and Option 1 (1,044) gives the same RQ1 basis.
   - Reason: D-018's documented evidence ("methods most used in the included RQ1 studies") and the Stage C gate need the complete RQ1 strand set that the scope decision defines. Option 1 alone would silently narrow RQ1. Option 3 is preferred because it matches the evidence requirement, not because it is smaller than Option 2.
   - The remaining 1,916 records (methodological strands RQ2–RQ4, RQ6, Q-PM-15, G-8-only, arXiv, web) would be screened if time permits, and the scope reported under D-005.
2. **Schedule: S1 + S2.** Keep 2026-11-24 as an interim deliverable without model results, and revise D-001 after the pilot has measured a screening rate. Do not use S3.
3. **Trade-offs:** Option 3 adds about 41 % more records than Option 1 (record ratio; time not measured). Deferring the methodological strands means the method justifications (AB-7) rest on targeted reading of identified references, which must be reported.

**Evidence the researcher needs to accept, amend or reject this:**
- your answers to Q-001 and Q-002 (disorder and biomarker scope);
- confirmation that D-018's RQ1 evidence requirement stands;
- after activation, the pilot's measured rate, which turns the `[HYPOTHESIS]` ratios into durations;
- the screening procedure (D-008, D-025) and who acts as second screener.

## Appendix 1 — Implementation 1 (run 2026-10-29, `python3 -I -B`)
```python
# Q-065 priority-strand counts. Metadata only: reads paper_id, query_ids,
# identifier fields, verification_status, source_publication_types,
# abstract_available. Never reads title or abstract text.
import json, sys, itertools, collections
recs = json.load(open(sys.argv[1], encoding="utf-8"))
G = [f"Q-PM-G{i}" for i in range(1, 8)]
STRATA = {"G1-G7": set(G), "Q-PM-02": {"Q-PM-02"}, "Q-PM-11/12": {"Q-PM-11", "Q-PM-12"}}
def toks(r): return {t.strip() for t in r["query_ids"].split(";") if t.strip()}
ids = [r["paper_id"] for r in recs]
assert len(ids) == len(set(ids)), "duplicate paper_id"
members = {k: {r["paper_id"] for r in recs if toks(r) & v} for k, v in STRATA.items()}
for q in G: print(q, sum(1 for r in recs if q in toks(r)))
for k, v in members.items(): print("stratum", k, len(v))
for a, b in itertools.combinations(members, 2): print("overlap", a, "&", b, len(members[a] & members[b]))
allthree = set.intersection(*members.values()); print("overlap all three", len(allthree))
union = set.union(*members.values()); print("union", len(union))
excl = {k: len(v - set.union(*(members[o] for o in members if o != k))) for k, v in members.items()}
print("exclusive", excl)
byid = {r["paper_id"]: r for r in recs}
u = [byid[p] for p in sorted(union)]
for f in ("pmid", "doi", "pmcid", "arxiv_id"):
    vals = [str(r.get(f) or "").strip().lower() for r in u if r.get(f)]
    print("dup", f, len(vals) - len(set(vals)), "| missing", sum(1 for r in u if not r.get(f)))
print("no persistent identifier", sum(1 for r in u if not any(r.get(f) for f in ("pmid","doi","pmcid","arxiv_id"))))
print("verification", dict(collections.Counter(r["verification_status"] for r in u)))
print("abstract_available", dict(collections.Counter(str(r.get("abstract_available")) for r in u)))
print("retracted (publication type)", sum(1 for r in u if "retract" in str(r.get("source_publication_types","")).lower()))
print("screening_status", dict(collections.Counter(r["screening_status"] for r in u)))
print("inventory total", len(recs), "outside union", len(recs) - len(union))
```
Command: `python3 -I -B q065_count.py research/literature/paper_inventory.json`. Output: as in §A.4.

## Appendix 2 — Implementation 2 (independent check) and `jq`
```python
# Independent check: reads the CSV twin; counts records by membership pattern (bit vector).
import csv, sys, collections
csv.field_size_limit(10**8)
rows = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")))
def bits(q):
    t = set(x.strip() for x in q.split(";"))
    g = any(f"Q-PM-G{i}" in t for i in range(1, 8))
    return (g, "Q-PM-02" in t, bool({"Q-PM-11", "Q-PM-12"} & t))
pat = collections.Counter(bits(r["query_ids"]) for r in rows)
for k in sorted(pat): print(k, pat[k])
s = lambda i: sum(n for k, n in pat.items() if k[i])
print("rows", len(rows), "unique paper_id", len({r["paper_id"] for r in rows}))
print("strata", s(0), s(1), s(2))
print("pairs G&02", sum(n for k,n in pat.items() if k[0] and k[1]), "G&11/12", sum(n for k,n in pat.items() if k[0] and k[2]), "02&11/12", sum(n for k,n in pat.items() if k[1] and k[2]))
print("union", sum(n for k, n in pat.items() if any(k)))
```
Command: `python3 -I -B q065_check.py research/literature/paper_inventory.csv`. Output: 3,386 rows, 3,386 unique `paper_id`; strata 194 / 743 / 120; pairs 10 / 0 / 3; union 1,044.

`jq` (version used: jq-1.7): `jq '[.[] | (.query_ids | split(";")) as $t | select(($t | any(test("^Q-PM-G[1-7]$"))) or ($t | index("Q-PM-02")) or ($t | index("Q-PM-11")) or ($t | index("Q-PM-12")))] | length' research/literature/paper_inventory.json` → `1044`.

Alternative-scope sizes (Option 3 etc.) came from the same exact-token method applied to the scope's query set: priority + Q-PM-01 + Q-PM-03 = 1,470; all PubMed Q-PM-01…15 + G1–G8 = 3,261; entire inventory = 3,386; Q-PM-01 records outside the priority strand = 399; Q-PM-03 = 44; G-8-only = 235. The scripts ran from the session scratchpad and are not committed; their full text for the stratum counts is reproduced above.
