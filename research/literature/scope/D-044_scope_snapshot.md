# D-044 screening-scope snapshot (PROPOSED, 2026-10-30)

| Field | Value |
|---|---|
| Status | **Proposed; not committed; not approved as a governance record.** Prepared for the researcher's review before any inventory rebuild |
| Purpose | Freeze the exact membership of the D-044 screening scope (1,470 `paper_id`s) so that it can be compared before and after an inventory rebuild. It does **not** change D-044, screen any record or replace the inventory |
| File | `D-044_scope_paper_ids.csv` — 1,470 rows plus a header; UTF-8, LF line endings; sorted by `paper_id` |
| File SHA-256 | `a5d4851f764ad0843115740d85e8f6e2bed1596883bf11cc22c63fbf631253ea` |
| ID-list SHA-256 | `0498eba45a221245fe5b2268fe10346505ef0b43d5c9fa9a58ad54860fa15fd5` (the 1,470 `paper_id`s, one per line, sorted, each followed by `\n`) |

## 1. Authoritative source
- **Decision:** D-044 (APPROVED — CONDITIONAL, inactive): "every inventory record retrieved by G-1…G-7, Q-PM-02, Q-PM-11/12 and the remaining RQ1 strands Q-PM-01 and Q-PM-03", where G-1…G-7 = `Q-PM-G1` … `Q-PM-G7` (G-8 excluded; `research/reviews/Q-065_decision_package.md`).
- **Data:** `research/literature/paper_inventory.json`, SHA-256 `a509538dc5e1cf41cd7a4e180ed17df86f6d4cd83a7d227abea073f1689af4a3` (the hash recorded in D-044), committed in `ffee9ec` (2026-10-29) and unchanged at `a20c84f`. Its CSV twin `paper_inventory.csv` (same commit) was used as the independent check.
- **Membership rule:** a record is in scope when its `query_ids` (split on `;`, exact token match) contain at least one of `Q-PM-G1` … `Q-PM-G7`, `Q-PM-01`, `Q-PM-02`, `Q-PM-03`, `Q-PM-11`, `Q-PM-12`.

## 2. Extraction and validation (run 2026-10-30)
| Check | Result |
|---|---|
| Method 1: `jq` 1.7 on `paper_inventory.json` (D-044 / Q-065 Appendix 2 filter, extended to Q-PM-01 and Q-PM-03) | 1,470 IDs |
| Method 2: Python `csv` on `paper_inventory.csv`, exact token match | 1,470 IDs; identical set to method 1 |
| Components | priority strand (G-1…G-7 ∪ Q-PM-02 ∪ Q-PM-11/12) 1,044; Q-PM-01 ∪ Q-PM-03 not in it 426; union 1,470, as recorded in D-044 and Q-065 |
| Duplicates | 0 (1,470 unique `paper_id`s) |
| Malformed IDs | 0 (all match `P\d{4}`) |
| Missing from `records/paper_id_registry.csv` | 0 |
| Records without PMID | 0 |
| Inventory | 3,386 rows, 3,386 unique `paper_id`s, in both JSON and CSV |

## 3. Columns
`paper_id`; `pmid`, `doi`, `arxiv_id` (copied from the inventory, so a rebuild that reassigned an ID would be detected); `d044_query_ids` (the D-044 queries that retrieved the record). No titles, abstracts or raw metadata.

## 4. Intended use (before-and-after comparison)
After any rebuild, the same membership rule is applied to the new inventory, and the result is compared with this file:
1. the set of `paper_id`s must be identical (no record added or dropped);
2. for every `paper_id`, `pmid`, `doi` and `arxiv_id` must be unchanged;
3. differences are reported, never silently accepted. The original scope stays defined by this snapshot and the source hash above; a rebuilt inventory is not substituted for it.

## 5. Known caveats `[EVIDENCE]`
- One possible-duplicate pair has both members in scope (P0113/P0153, an erratum and its article), so the publication count can fall to 1,469 if the pair is merged (as D-044 notes). Three further pairs have one member in scope; a merge decision on them could move a record across the scope boundary. No pair decision exists.
- Verification statuses in scope: 1,460 `partially_verified`, 10 `verified`. The 10 `verified` records depend on the second-source rule questioned by Q-068 (open).
