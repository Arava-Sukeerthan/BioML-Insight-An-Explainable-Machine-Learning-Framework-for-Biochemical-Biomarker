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
| Off-device backup availability (2026-10-23, LIT-004-PREPARATION) | **Not currently available.** The project owner reports having no external drive. This limitation is accepted for now and stays explicit; it is not resolved |
| Remaining step | Put a third copy on separate private media or storage (e.g. an encrypted external drive, institutional storage, or a private, access-restricted cloud folder), verify its SHA-256, and report it (no credentials) |

### Status history (earlier values kept)
| Date | Task | Status |
|---|---|---|
| 2026-10-23 | LIT-003-HOTFIX | PENDING: verified archive created in the container and delivered to the researcher |
| 2026-10-23 | LIT-003-PRESERVATION-CONFIRMATION (1) | **DOWNLOADED AND CHECKSUM-VERIFIED; DURABLE STORAGE NOT YET CONFIRMED.** The researcher downloaded the archive and verified its SHA-256 on Windows on 2026-10-23 (see the 'Researcher-side verification' section). Durable preservation is complete only once the project owner confirms a second private backup or other durable storage location (Q-011) |
| 2026-10-23 | LIT-003-PRESERVATION-CONFIRMATION (2) | Archive integrity verified; local redundancy established (2 copies, same computer); off-device backup outstanding |
| 2026-10-28 | LIT-003-RESTORE | Archive uploaded to the session and verified again; the 205 raw files restored into the workspace's `raw_exports/`; `pubrecords.py verify` OK for all 244 manifest files. Off-device backup still outstanding. Details: section "LIT-003 archive: restoration into the workspace" at the end of this file |

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
- **(2026-10-23, LIT-004-PREPARATION)** No off-device backup is currently available (no external drive). Disaster-recovery risk stays **open**. Alternatives not requiring a drive (institutional storage, a private access-restricted cloud folder) are possible but not chosen.
- **(Updated 2026-10-23, second update)** Two verified copies now exist outside the container, **both on the researcher's Windows computer**. A failure or loss of that computer would affect both. Off-device backup is outstanding.
- **(Earlier update, 2026-10-23)** One verified copy now exists outside the container, on the researcher's Windows machine. Until a second private backup or another durable location is confirmed, loss of that machine or file would leave only the ephemeral container copy.
- Container copy and app attachment: retention not guaranteed.
- If the files are lost, the PubMed searches can be re-run with the same `[edat]`-capped queries. The PMID sets should be reproducible apart from later PubMed deletions or corrections, but the metadata may differ (PubMed updates records). The arXiv and web results are **not** reproducible.
- The harness's own copies of the metadata responses (`tool-results/`) are also in the container and will be lost with it.

---

## LIT-005 raw exports (LIT-005-PRESERVATION, 2026-10-28)
Scope: this section covers only the 39 raw export files registered in `raw_exports/MANIFEST.csv` on 2026-10-28 (task LIT-005). Everything above refers to the LIT-003 archive and is unchanged.

| Field | Value |
|---|---|
| **Preservation status** | **ARCHIVE INTEGRITY VERIFIED (container and researcher side); ONE COPY OUTSIDE THE CONTAINER (researcher's Windows laptop); OFF-DEVICE BACKUP / DISASTER RECOVERY OUTSTANDING** |
| Files preserved in archive | **39** raw export files: 18 PubMed search pages (9 original + 9 `CHECK-` re-fetch), 20 PubMed metadata files (`META_2026-10-28_000…019.json`), 1 alphaXiv structured transcription (`Q-AX-G9_2026-10-28.json`) |
| Archive filename | `LIT-005_raw_exports_2026-10-28.tar.gz` |
| Archive (container copy) | `research/literature/preservation/archive/LIT-005_raw_exports_2026-10-28.tar.gz` (git-ignored; inside the ephemeral container) |
| Archive size | 479,473 bytes |
| Archive SHA-256 | `7b7d4674426c7581839b970cad37e21251ade0bf22d295814ac542bd7ec96ea1` |
| Archive contents | Exactly the 39 files, stored under their repository paths `research/literature/raw_exports/<file>`; file entries only (no directories); no checksum or manifest file inside the archive |
| Companion files (container, git-ignored, delivered with the archive) | `LIT-005_raw_exports_2026-10-28.tar.gz.sha256` (archive checksum); `LIT-005_SHA256SUMS.txt` (SHA-256 of the 39 files, paths relative to the extraction root); `LIT-005_archive_manifest.csv` (the 39 `MANIFEST.csv` rows plus each archive path) |
| Determinism | GNU tar 1.35, `--sort=name`, `--format=gnu`, fixed mtime 2026-10-28T00:00:00Z, owner/group 0 (numeric), fixed mode `u=rw,go=r`, `--no-recursion`; `gzip -n -9`. Built twice; both builds byte-identical |

### Container-side verification (2026-10-28)
| Check | Result |
|---|---|
| File list | 39 rows dated 2026-10-28 in `MANIFEST.csv`, all with LIT-005 notes; no duplicate or unexpected names; no path under `data/` or referring to NHANES |
| Files vs `MANIFEST.csv` before archiving | 39/39 present as regular files (no symlinks); 39/39 SHA-256 match |
| Archive entries | 39 entries, all regular files; entry list identical to the 39 manifest paths; no `.git`, environment, NHANES or `data/` paths |
| Extraction into a fresh temporary directory; `sha256sum -c LIT-005_SHA256SUMS.txt` | 39/39 OK, 0 failed; 39 files extracted. The temporary directory was deleted afterwards |
| Archive checksum file | `sha256sum -c LIT-005_raw_exports_2026-10-28.tar.gz.sha256` → OK (re-checked before the second delivery) |
| Original raw files modified | No (read and archived only) |
| Git | Archive and companion files git-ignored (`.gitignore`: `research/literature/preservation/archive/`); not staged or committed |

### Delivery and researcher-side verification (2026-10-28)
| Item | Recorded value |
|---|---|
| Delivery | Archive and the three companion files delivered as attachments in the Claude app session (twice, the second time on the researcher's request; the original archive was re-sent, not rebuilt) |
| Copy verified | `%USERPROFILE%\Downloads\LIT-005_raw_exports_2026-10-28.tar.gz` on the researcher's Windows laptop |
| Result (as reported by the researcher, 2026-10-28) | SHA-256 `7b7d4674426c7581839b970cad37e21251ade0bf22d295814ac542bd7ec96ea1`, exactly the expected value |
| Evidence type | Researcher's statement in the prompt. The assistant did not observe the command or its output. Whether the optional per-file check (`sha256sum -c LIT-005_SHA256SUMS.txt` after extraction) was run was not reported |
| What it establishes | The downloaded copy is byte-identical to the container archive, whose 39 files were verified against `MANIFEST.csv` and `LIT-005_SHA256SUMS.txt` |
| What it does **not** establish | Durable or off-device backup. There is **one** copy outside the container, in the Downloads folder of one laptop. No second copy (same or other device), external drive, institutional storage or cloud copy has been reported. Loss of that file or laptop would leave only the ephemeral container copy |

### Remaining steps (researcher)
1. Optionally make a second local copy (e.g. a backup folder, as for LIT-003) and verify its SHA-256.
2. For disaster recovery, put a copy on separate private media or storage (encrypted external drive, institutional storage or a private, access-restricted cloud folder), verify its SHA-256, and report the location type and result (no credentials). Do **not** put it in the public repository (D-010, proposed; the files contain PubMed abstracts).
3. Keep the LIT-003 archive (`69e690f…`) and the LIT-005 archive (`7b7d4674…`) together: an inventory rebuild needs both sets of raw files (Q-063).

### Status history (LIT-005)
| Date | Task | Status |
|---|---|---|
| 2026-10-28 | LIT-005-PRESERVATION (archive) | Archive created and verified in the container; delivered to the researcher |
| 2026-10-28 | LIT-005-PRESERVATION (confirmation) | Researcher reports the downloaded copy's SHA-256 matches exactly. Archive integrity verified; one copy outside the container (Windows Downloads); off-device backup outstanding |

### Outstanding risks (LIT-005)
- Only one copy exists outside the container, on one laptop. Disaster-recovery risk stays **open**.
- Container copy and app attachments: retention not guaranteed.
- If lost: the 8 PubMed queries (`Q-PM-G1…G8@2026-10-28`) are `[edat]`-capped and can be re-run, but metadata may differ. The alphaXiv ranking (`Q-AX-G9`) is **not** reproducible.

---

## LIT-003 archive: restoration into the workspace (LIT-003-RESTORE, 2026-10-28)
Scope: the LIT-003 archive described at the top of this file. Earlier entries are unchanged.

| Field | Value |
|---|---|
| Source of the uploaded copy | The researcher's copy reported at `%USERPROFILE%\Documents\BioML-Insight-Backup\LIT-003_raw_exports_2026-10-23.tar.gz` (researcher statement), uploaded to the Claude Code session. A first upload attempt produced a 0-byte, unrelated CSV and was not used |
| Uploaded file (container, outside the repository) | `/root/.claude/uploads/e89f2544-52ab-549f-965c-1d5f571bc462/e9f8022d-LIT-003_raw_exports_2026-10-23.tar.gz` (not copied into the repository) |
| Size / SHA-256 | 3,647,967 bytes / `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e` — **exact match** with the value recorded above (checked twice: verification task and restore task) |

### Verification (tool output, 2026-10-28)
| Check | Result |
|---|---|
| Listing before extraction | 211 entries = 209 regular files + 2 directories (`lit003_raw_exports/`, `lit003_raw_exports/raw_exports/`); no absolute paths, no `..`, no symlinks, hard links or other entry types |
| Extraction | into a new, empty scratch directory outside the repository; 209 files, 0 symlinks |
| `sha256sum -c SHA256SUMS.txt` | **208/208 OK**, 0 failures; every extracted file covered |
| Archive `SHA256SUMS.txt` vs committed `archive_contents_SHA256SUMS.txt` | byte-identical |
| 205 raw JSON files vs current `raw_exports/MANIFEST.csv` (LIT-003 rows) | 205 = 205; none missing or extra; 0 hash mismatches |
| 205 raw JSON files vs committed `raw_exports_inventory.csv` | 0 hash mismatches, 0 size mismatches |
| Archived `MANIFEST.csv` | identical to the committed manifest at `53e419a` (before LIT-005). Not used: the current manifest has 244 rows |
| Archived `raw_exports_inventory.csv` | identical to the committed file. Not used |
| Archived `raw_exports/README.md` | an earlier, shorter version of the committed README (notes were appended after the archive was built); passes its checksum. Not used |

### Restoration (tool output, 2026-10-28; researcher-authorised)
| Item | Result |
|---|---|
| Files copied | **205** LIT-003 raw JSON files only, byte-for-byte, into `research/literature/raw_exports/` |
| Overwrite protection | every destination checked first (0 conflicts); each file written with exclusive create (fails if the file exists); each copy re-hashed against `MANIFEST.csv` |
| Not copied or changed | `MANIFEST.csv`, `README.md`, `raw_exports_inventory.csv`, `SHA256SUMS.txt`, the archive itself; no existing file modified |
| `python3 -I scripts/literature/pubrecords.py verify` | `OK: all raw exports match MANIFEST.csv` (exit code 0); the manifest lists **244** files (205 LIT-003 + 39 LIT-005) |
| Git | restored files are git-ignored (D-010, proposed); working tree clean afterwards |
| Temporary extraction directories | deleted after each task; the uploaded archive was left in place |
| Inventory | **not rebuilt**; no generated artifact or registry change |

### What this establishes, and what it does not
- **Establishes:** the uploaded copy is byte-identical to the archive verified on 2026-10-23; all 244 raw exports in the manifest are now present in this workspace and match their checksums. The precondition for an inventory rebuild (`verify_manifest` passes) is met.
- **Does not establish:** off-device backup or disaster recovery. The researcher's copies of the LIT-003 archive are reported to be on the same computer; the LIT-005 archive has one copy in that computer's Downloads folder. Both remain **outstanding** for off-device storage.
- **Workspace copies are not durable:** the restored files exist only in this ephemeral container and would need restoring again in a new workspace.
- **Q-063:** its first option (restore from the researcher's backup) has been carried out for this workspace. The rebuild it is meant to enable has **not** been done, and Q-063's status in `research/reviews/unresolved_questions.md` is unchanged (**Open**); closing it is the researcher's decision.
