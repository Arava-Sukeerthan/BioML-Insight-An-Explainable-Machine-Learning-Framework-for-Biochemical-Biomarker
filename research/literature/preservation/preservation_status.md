# Raw-Export Preservation Status (LIT-003-HOTFIX)

| Field | Value |
|---|---|
| Date | 2026-10-23 |
| **Preservation status** | **ARCHIVE INTEGRITY VERIFIED; LOCAL REDUNDANCY ESTABLISHED (2 copies on the same computer); OFF-DEVICE BACKUP / DISASTER RECOVERY OUTSTANDING.** See 'Second local copy' below and the status history |
| Files preserved in archive | 205 raw export files (all of `raw_exports/MANIFEST.csv`) + `MANIFEST.csv`, `README.md`, `raw_exports_inventory.csv` + `SHA256SUMS.txt` |
| Total size of raw files | 14,121,733 bytes (about 14 MB) |
| Archive | `research/literature/preservation/archive/LIT-003_raw_exports_2026-10-23.tar.gz` (git-ignored; inside the ephemeral container) |
| Archive size | 3,647,967 bytes |
| Archive SHA-256 | `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e` |
| Determinism | Built twice (GNU tar `--sort=name`, fixed mtime 2026-10-23T00:00:00Z, owner/group 0, `gzip -n -9`); both builds have the same SHA-256 |
| Inventory (committed) | `raw_exports_inventory.csv` (path, type, size, SHA-256, search ID, source, route, retrieval time, manifest check); `archive_contents_SHA256SUMS.txt` |

## Verification performed
| Check | Result |
|---|---|
| Files located vs `MANIFEST.csv` (205 rows) | 205 found, 0 missing, 0 unexpected |
| SHA-256 of each file vs `MANIFEST.csv` | 205/205 match (also `pubrecords.py verify` → OK) |
| JSON validity | 205/205 valid JSON |
| Archive extracted into a separate temporary directory; `sha256sum -c SHA256SUMS.txt` | 208/208 OK |
| Extracted raw files vs original `MANIFEST.csv` | 205/205 match; no extra files; manifest byte-identical |
| Original raw files modified | No (only read and copied) |

Composition: 144 PubMed metadata files, 50 PubMed search pages (25 original + 25 `CHECK-` re-fetch), 5 arXiv (alphaXiv) files, 6 web-search files.

## Researcher-side verification (LIT-003-PRESERVATION-CONFIRMATION, 2026-10-23)
| Item | Recorded value |
|---|---|
| Copy verified | The downloaded copy of `LIT-003_raw_exports_2026-10-23.tar.gz` on the researcher's Windows machine |
| Command (as reported by the researcher) | `certutil -hashfile ".\LIT-003_raw_exports_2026-10-23.tar.gz" SHA256` |
| Result (as reported by the researcher) | `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e`, exactly the expected hash |
| Evidence type | Researcher's statement in the prompt. The assistant did not observe the Windows command output |
| What it establishes | The downloaded copy is byte-identical to the archive verified in the container. That archive's contents were already checked against `MANIFEST.csv`: 205/205 files, 208/208 hashes after extraction |
| What it does **not** establish | Durable backup or long-term retention. A single downloaded copy on one machine can still be lost (disk failure, deletion, no backup). No second private backup or other durable location has been confirmed |
| Durable private storage | **Not confirmed (pending)** as of this entry. No storage location or credentials were requested or recorded. *(Superseded by the next section for local copies; off-device storage still not confirmed.)* |
| Optional further check (not required) | Extract it and run `sha256sum -c SHA256SUMS.txt` (e.g. in WSL or Git Bash) to re-check all 208 contained files |

## Second local copy (LIT-003-PRESERVATION-CONFIRMATION, second update, 2026-10-23)
| Item | Recorded value (as reported by the researcher; outputs not observed by the assistant) |
|---|---|
| Copy 1 | Windows Downloads folder: SHA-256 verified with `certutil -hashfile`, matches `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e` |
| Copy 2 | `%USERPROFILE%\Documents\BioML-Insight-Backup\LIT-003_raw_exports_2026-10-23.tar.gz`: reported as checksum-verified successfully |
| Location of both copies | **The same computer** (same user profile). No external drive, second device, institutional storage or cloud copy has been reported |
| What this establishes | Archive integrity (both copies match the expected hash) and **local redundancy** against accidental deletion of a single file |
| What this does **not** establish | Off-device backup or disaster recovery. Disk failure, loss or theft of the computer, ransomware or a profile reset would affect both copies |
| Remaining step | Put a third copy on separate private media or storage (e.g. an encrypted external drive, institutional storage, or a private, access-restricted cloud folder), verify its SHA-256, and report it (no credentials) |

### Status history (earlier values kept)
| Date | Task | Status |
|---|---|---|
| 2026-10-23 | LIT-003-HOTFIX | PENDING: verified archive created in the container and delivered to the researcher |
| 2026-10-23 | LIT-003-PRESERVATION-CONFIRMATION (1) | **DOWNLOADED AND CHECKSUM-VERIFIED; DURABLE STORAGE NOT YET CONFIRMED.** The researcher downloaded the archive and verified its SHA-256 on Windows on 2026-10-23 (see the 'Researcher-side verification' section). Durable preservation is complete only once the project owner confirms a second private backup or other durable storage location (Q-011) |
| 2026-10-23 | LIT-003-PRESERVATION-CONFIRMATION (2) | Archive integrity verified; local redundancy established (2 copies, same computer); off-device backup outstanding |

## Storage options investigated
| Option | Result |
|---|---|
| Public GitHub repository | **Not used.** The repository is public and the files contain PubMed abstracts (D-010) |
| Container paths (repo working tree, `/tmp`, scratchpad) | Not durable: the container is reclaimed after inactivity |
| Delivery to the researcher through the Claude app (`SendUserFile`) | **Done**: archive delivered as a file attachment in this session (file ID `ce562513-cd1c-4ed0-b484-d003120b0901`). This is a hand-over to the researcher, not durable storage in itself |
| Researcher's Google Drive (connector available) | Not used. (a) It has not been approved as project storage; (b) the connector needs the whole file inline as base64 in a single call, which is not practical for 3.6 MB from this environment. Can be revisited if the researcher approves a folder |
| Other cloud storage (gsutil/bq configured CLIs, gists, file hosts) | Not used: no researcher-approved destination or credentials; uploading copyrighted abstracts to an unapproved service is not allowed |

## Steps for the researcher to complete preservation
1. In the Claude app, open this session and download the attachment `LIT-003_raw_exports_2026-10-23.tar.gz`. While the container is still alive, the same file is also at the path above in the working directory.
2. Save it to private storage you control (e.g. an institutional drive or a private, access-restricted cloud folder). Do **not** put it in the public repository.
3. Check the checksum: `sha256sum LIT-003_raw_exports_2026-10-23.tar.gz` must print `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e`. On Windows: `certutil -hashfile <file> SHA256`.
4. Optional full check: `tar -xzf LIT-003_raw_exports_2026-10-23.tar.gz && cd lit003_raw_exports && sha256sum -c SHA256SUMS.txt`.
5. Tell the assistant the storage location (no credentials) and the checksum result. The status here is then changed to PRESERVED, with the date.

## Outstanding risks
- **(Updated 2026-10-23, second update)** Two verified copies now exist outside the container, **both on the researcher's Windows computer**. A failure or loss of that computer would affect both. Off-device backup is outstanding.
- **(Earlier update, 2026-10-23)** One verified copy now exists outside the container, on the researcher's Windows machine. Until a second private backup or another durable location is confirmed, loss of that machine or file would leave only the ephemeral container copy.
- Container copy and app attachment: retention not guaranteed.
- If the files are lost, the PubMed searches can be re-run with the same `[edat]`-capped queries. The PMID sets should be reproducible apart from later PubMed deletions or corrections, but the metadata may differ (PubMed updates records). The arXiv and web results are **not** reproducible.
- The harness's own copies of the metadata responses (`tool-results/`) are also in the container and will be lost with it.
