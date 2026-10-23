# raw_exports/

Immutable raw responses from literature APIs and tools. **Never edit a file here.**
`MANIFEST.csv` records each file's sha256, query ID, route, and UTC retrieval time.
`python3 -I scripts/literature/pubrecords.py verify` checks every file against it.

Only `MANIFEST.csv` and this README are committed. The repository is public and abstracts may be
copyrighted (see `../collection_workflow.md` §7 and decision D-010).

LIT-003 (2026-10-23): 205 raw files registered (50 PubMed search pages (25 original + 25 `CHECK-` re-fetch pages), 144 PubMed metadata files, 5 arXiv and 6 web-search files; about 14 MB). They exist only in the session container and are **not** in Git. The manifest lets them be verified if they are re-supplied, and the snapshot-capped queries let them be re-fetched (Q-011).

LIT-003-HOTFIX (2026-10-23): a verified, deterministic archive of all 205 files was created and delivered to the researcher. Preservation in researcher-controlled storage is **still pending**. See `../preservation/preservation_status.md`.
