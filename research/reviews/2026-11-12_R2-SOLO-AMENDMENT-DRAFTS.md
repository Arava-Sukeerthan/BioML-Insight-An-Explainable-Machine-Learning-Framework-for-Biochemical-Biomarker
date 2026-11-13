# R2-solo amendment drafts (2026-11-12, 17:00 UTC) — for researcher approval; nothing recorded

> **Researcher direction (2026-11-12):**
> - adopt researcher-first / assistant-second screening (R2-solo) as a **decision-level amendment** (no re-freeze);
> - appoint no custodian;
> - keep the 60-record pilot, κ ≥ 0.60, the audit and the research question;
> - keep the screening sheet and salt in a private local folder;
> - the deadline of 27 November is fixed.
>
> **Prepared here (uncommitted):**
> - decision texts D-123, D-124 and D-122;
> - `scripts/literature/pilot_commitment.py` and `tests/literature/test_pilot_commitment.py`, synthetic only;
> - `research/literature/pilot_assistant_prompt.md`;
> - Q-084 marked *proposed* in `unresolved_questions.md`.
>
> **Not done:** no decision recorded, no draw, no sheet, no salt, no commitment, no pilot, no Q-102, no commit.

## 1. Amendment decisions (recorded only after explicit approval)
**ID order:**
- D-122 is kept for the draw authorisation, as previously named.
- The amendment entries take **D-123** and **D-124**, and are recorded **before** D-122. The decision log would therefore show D-123 and D-124 above D-122.
- *Alternative [RD]:* renumber (amendment D-122/D-123, draw D-124).

**D-123 — revision of D-102** (Decision cell):
> **Revision of D-102: single-researcher pilot workflow ("R2-solo").**
> - **Reason:** an independent custodian as required by D-102 (3) and by both D-109 designs cannot be arranged. The researcher conducts the study alone. No account, session or folder under the researcher's control is used as a substitute for independent custody.
> - **Clause (3) is withdrawn.**
> - **Clauses (1), (2), (5) and (6) are replaced by:**
>   - **(a)** The researcher screens the 60 pilot records first, on their own computer, outside any assistant session. With `scripts/literature/pilot_commitment.py make` they produce the canonical file F_R and a 256-bit salt S_R, both kept in a private local folder. They commit only `research/literature/screening/pilot_researcher_commitment.json`, with:
>     - C_R = SHA-256("bioml-insight pilot commitment v1\n" ‖ S_R ‖ "\n" ‖ F_R);
>     - the row count, `criteria_version`, the SHA-256 of `research/literature/screening/pilot_sample.csv` and the time;
>     - no decision, code, justification or salt.
>   - **(b)** A new assistant session, started with the fixed prompt `research/literature/pilot_assistant_prompt.md` (bound by SHA-256 in D-122) and without access to F_R, generates the blinded sheet for the researcher. After the researcher's commitment is pushed, it screens the same records in one pass. It immediately commits `research/literature/screening/pilot_assistant_commitment.json` (C_A by the same formula) and keeps its file and salt outside the repository. Only after that push does it send them to the researcher as a backup against loss of the session. The researcher undertakes not to open them before their own file is disclosed, verified and committed. This is **not technically enforced**; it does not affect D-101, because the researcher's decisions are already fixed by the pushed C_R.
>   - **(c)** The researcher discloses F_R and S_R. On successful `pilot_commitment.py verify`, F_R is committed as `research/literature/screening/pilot_decisions_researcher.csv` with `research/literature/screening/pilot_researcher_commitment.salt`. Then the assistant's file is committed as `research/literature/screening/pilot_decisions_assistant.csv` with `research/literature/screening/pilot_assistant_commitment.salt`, and verified against C_A. This satisfies protocol v0.2 §7 ("committed only after the researcher's file").
>   - **(d)** A mismatch, or a missing file or salt, is recorded as an integrity failure; no agreement is computed and the pilot is not passed.
>   - **(e)** The order C_R → C_A → F_R → F_A is checked with `pilot_commitment.py order` and recorded in the session log.
> - **Clause (4) is unchanged.** D-025, D-063, D-077, D-096, D-098, D-099, D-101 and D-008 are unchanged; the κ ≥ 0.60 pass rule is unchanged.
> - **Limitations accepted:**
>   - no independent party holds pilot material;
>   - the researcher controls both screening environments;
>   - the absence of information flow from the researcher to the assistant session is attested by the researcher and supported by the commitments, the Git order and the retained session transcript, not verified by a third party.
> - **Superseded descriptive sentences** in frozen protocol v0.2 §7a step 5 are recorded as superseded by this entry: the R1/R2 designation; "D-102 (3) … requires custody by an independent custodian; no custodian is appointed"; the D-096 extension for R1. §7a step 6 ("After delivery, the file is validated and committed") is read as: after the assistant's commitment. The protocol files are not edited.
>
> Status: **APPROVED** (governance decision). Rationale: preserves the pilot and D-101 without a custodian. Related: D-102; D-109; D-101; D-025.

**D-124 — revision of D-109:**
> **Revision of D-109.** The R1 design (custodian-operated assistant screening) and the R2 design with custodian escrow are withdrawn; the design adopted is D-123. Implementation of `scripts/literature/pilot_commitment.py` (`make`, `verify`, `order`; standard library only) and `tests/literature/test_pilot_commitment.py` (synthetic) is approved, with commit and push. The fixed assistant prompt `research/literature/pilot_assistant_prompt.md` is approved, to be committed before the draw. A test-only update of `tests/literature/test_phase1_screening_tools.py` adds D-122 to the permitted activation states (constant `PILOT_DRAW_ACTIVATION`, two fixture tests).
>
> Status: **APPROVED** (governance and implementation decision).

**Status-history rows (on recording):**
- D-102 revised by D-123;
- D-109 revised by D-124;
- Q-084 answered: after the first two expansion batches, as you directed;
- **[RD]:** activation notes for D-063, D-077, D-098, D-101 and D-102 (§6 recorded by D-115 to D-120).

## 2. D-122 draft (D-088/D-097 form)
**Dry-run result (2026-11-12):**
- The text below, with `<CHANNEL>` and the hash filled, was **accepted** by `pubrecords.verify_run_authorisation` for D-077 (6) in a disposable copy of the decision log.
- A wrong clause and a wrong inventory hash were refused.
- The authorisation is unused for `pilot_sample`.
- The repository was not changed.

**Path convention:** the screening directory is `research/literature/screening/` (the only one in the repository). The frozen protocol, D-102 and the tools write it as `screening/…` relative to `--lit-dir research/literature`. All new texts use the full repository path.

> | D-122 | <DATE> (PILOT-DRAW) | **Run authorisation under D-077 (6).** criteria_version: criteria_v1.1+protocol_v0.2; inventory_sha256: b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054; freeze_entry: D-110; d035_s6_records: D-115, D-116, D-117, D-118, D-119, D-120; single_use: yes; scope: one draw by `scripts/literature/pilot_sample.py` (D-063, D-077; 60 records; seed 4004; frame 1,463; D-113 stop rule) writing `research/literature/screening/pilot_sample.csv` and its sidecar, and one blinded sheet by `scripts/literature/pilot_sheet.py` (`research/literature/screening/pilot_sheet_researcher.csv`, Git-ignored), generated in the assistant pilot session and sent to the researcher only, by <CHANNEL> (D-096); assistant start prompt `research/literature/pilot_assistant_prompt.md` SHA-256 <PROMPT_SHA256>; workflow D-123 (revision of D-102); the ledger `research/literature/screening/run_authorisation_ledger.jsonl` and committable outputs are committed and pushed in a dedicated commit after each run (D-099 (1)) | **APPROVED** — run authorisation (single use) | D-077 (6); D-088; D-097; D-123; D-124 | Researcher (owner), <DATE> — <quotation> |

**Prerequisites before recording:**
- D-123 and D-124 recorded;
- the tool and the prompt committed (the prompt's status line updated, then hashed);
- `<CHANNEL>` named [RD];
- **your confirmation that you can run Python 3 on your own computer (§4).**

## 3. Manuscript limitation statement (draft)
> "Title/abstract screening was conducted by a single researcher with an AI assistant applying pre-specified, frozen criteria (criteria v1.1, protocol v0.2). Before the assistant screened the remaining records, the researcher and AI assistant separately screened a stratified pilot of 60 records (seed 4004). Because no independent custodian was available, the protocol's pilot workflow was amended before the pilot (decision D-123, 2026-11-13): the researcher screened first, outside any assistant session, and published a salted SHA-256 commitment; the assistant then screened the same records in a separate session started from a pre-committed prompt, without access to the researcher's decisions, and committed its own commitment; both files were disclosed and verified afterwards, and the order was checked in the version history. The assistant's file was also delivered to the researcher, after the assistant's commitment was published, as a backup; the researcher undertook not to open it before their own file had been disclosed, verified and committed. The pilot agreement (Cohen's κ with 95% CI; pre-specified pass threshold κ ≥ 0.60) is agreement between one human and an AI screener. It is not an estimate of screening accuracy or of inter-human reliability. No second human reviewer or independent custodian was involved. That the researcher's decisions did not reach the assistant session is attested by the researcher and supported by commitments, version-control order and session records, but was not verified by an independent party. The same researcher performed the blind audit of 50 assistant decisions and all full-text assessments."

## 4. Python 3 check on your own Windows computer (no Claude Code involved)
*Python running inside Claude Code says nothing about your computer. Please run these yourself.*

**Step 1 — is Python 3 installed?** Open **PowerShell** (Start menu → type "PowerShell" → open), then run:
```powershell
py -3 --version
```
If that fails, try:
```powershell
python --version
```
- **Pass:** the output shows `Python 3.x.y` with x ≥ 9 (3.9 or newer).
- **Fail or uncertain:**
  - "not recognized" or "was not found", or the Microsoft Store opens: Python 3 is not available.
  - Install it from https://www.python.org/downloads/windows/ and tick "Add python.exe to PATH" during installation.
  - Your institution may restrict installation; then say so, because the workflow depends on it.

**Step 2 — standard-library check** (no internet, nothing installed):
```powershell
py -3 -c "import hashlib, secrets, csv, json; print('stdlib OK', hashlib.sha256(b'abc').hexdigest())"
```
**Expected:** `stdlib OK ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.

**Step 3 — later, after approval and the draw (not now):**
1. Download the repository as a ZIP from GitHub (green "Code" button → "Download ZIP") at the commit named at the draw, and unzip it, for example to `C:\BioML\repo`.
2. Create a private folder **outside** the repository, for example `C:\BioML\private`.
3. Put the sheet, the template and `pilot_sample.csv` there.
4. Fill the template.
5. Run:
```powershell
cd C:\BioML\repo
py -3 scripts\literature\pilot_commitment.py make --file C:\BioML\private\pilot_decisions_researcher_template_filled.csv --sample C:\BioML\private\pilot_sample.csv --screener researcher --criteria-version criteria_v1.1+protocol_v0.2 --out-dir C:\BioML\private\commit
```
- It prints the commitment and writes three files into `C:\BioML\private\commit`.
- **Send only** `pilot_researcher_commitment.json`.
- **Keep** `pilot_decisions_researcher.csv` and `pilot_researcher_commitment.salt` private until disclosure. Back them up. A lost salt means an integrity failure.
- If you edit the CSV in Excel, save it as **"CSV UTF-8 (Comma delimited)"**. Any other encoding is refused.

**To check a disclosure yourself** (optional; the same check also runs in the repository):
```powershell
py -3 scripts\literature\pilot_commitment.py verify --file C:\BioML\private\commit\pilot_decisions_researcher.csv --salt-file C:\BioML\private\commit\pilot_researcher_commitment.salt --record C:\BioML\private\commit\pilot_researcher_commitment.json --sample C:\BioML\private\pilot_sample.csv
```
Expected: `verified: researcher file reproduces commitment …`.

**What to report back:** the output of steps 1 and 2 (or the error message). No draw happens until you confirm.

## 5. Final exact decision rows (2026-11-13)
**Status (2026-11-13):** D-123 and D-124 were approved by the researcher and recorded in `logs/DECISION_LOG.md` with the approval quotation in place of `<approval quotation>`. **D-122 is not approved, not recorded and not active.** The activation-test update is approved but not applied.
These rows supersede the earlier bullet-form drafts in §1 and §2 above.

**Researcher decisions of 2026-11-13 reflected here:**
- order D-123 → D-124 → D-122;
- channel: Claude app file delivery to the researcher's own account;
- backup retained;
- A2 package kept as a superseded record;
- **every Git push requires the researcher's separate, explicit approval immediately before it (no pre-authorisation)**.

The prompt hash in D-122 is that of the approved-form prompt file (header and status line set to approved).

**D-123**

> | D-123 | 2026-11-13 (R2-SOLO-AMENDMENT) | **Revision of D-102: single-researcher pilot workflow ("R2-solo").** Reason: an independent custodian as required by D-102 (3) and by both D-109 designs cannot be arranged; the researcher conducts the study alone; no account, session or folder under the researcher's control is used as a substitute for independent custody. **Clause (3) is withdrawn.** Clauses (1), (2), (5) and (6) are replaced by: (a) the researcher screens the 60 pilot records first, on their own computer, outside any assistant session, and with `scripts/literature/pilot_commitment.py make` produces the canonical file F_R and a 256-bit salt S_R, both kept in a private local folder; only `research/literature/screening/pilot_researcher_commitment.json` is committed and, after the researcher's push approval, pushed, with C_R = SHA-256("bioml-insight pilot commitment v1\n" ‖ S_R ‖ "\n" ‖ F_R), the row count, `criteria_version`, the SHA-256 of `research/literature/screening/pilot_sample.csv` and the time (no decision, code, justification or salt); (b) a new assistant session, started with the fixed prompt `research/literature/pilot_assistant_prompt.md` (bound by SHA-256 in D-122) and without access to F_R, generates the blinded sheet for the researcher and, only after the push of the researcher's commitment has succeeded, screens the same records in one pass; it immediately commits `research/literature/screening/pilot_assistant_commitment.json` (C_A by the same formula), requests push approval and pushes it, and keeps its file and salt outside the repository; only after that push has succeeded does it send them to the researcher as a backup against loss of the session; the researcher undertakes not to open them before their own file is disclosed, verified and committed (not technically enforced; it does not affect D-101, because the researcher's decisions are already fixed by the pushed C_R); (c) the researcher discloses F_R and S_R; on successful `pilot_commitment.py verify`, F_R is committed as `research/literature/screening/pilot_decisions_researcher.csv` with `research/literature/screening/pilot_researcher_commitment.salt`; then the assistant's file is committed as `research/literature/screening/pilot_decisions_assistant.csv` with `research/literature/screening/pilot_assistant_commitment.salt` and verified against C_A (protocol v0.2 §7: "committed only after the researcher's file"); (d) a mismatch, or a missing file or salt, is recorded as an integrity failure; no agreement is computed and the pilot is not passed; (e) the order C_R → C_A → F_R → F_A is checked with `pilot_commitment.py order` and recorded in the session log; (f) every Git push in this workflow requires the researcher's separate, explicit approval immediately before that push; no push is pre-authorised; in the assistant session a push is made only after the researcher's bare message `push approved` in reply to a specific push request, which authorises that one push only. Clause (4) is unchanged. D-025, D-063, D-077, D-096, D-098, D-099, D-101 and D-008 are unchanged; the κ ≥ 0.60 pass rule is unchanged. **Limitations accepted:** no independent party holds pilot material; the researcher controls both screening environments; the absence of information flow from the researcher to the assistant session is attested by the researcher and supported by the commitments, the Git order and the retained session transcript, not verified by a third party. **Superseded descriptive sentences** in frozen protocol v0.2 §7a step 5 (the R1/R2 designation; "D-102 (3) … requires custody by an independent custodian; no custodian is appointed"; the D-096 extension for R1) are recorded as superseded by this entry; §7a step 6 ("After delivery, the file is validated and committed") is read as "after the assistant's commitment". Paths: `screening/` in the frozen protocol and in D-102 denotes `research/literature/screening/`. The protocol files are not edited | **APPROVED** (governance decision) | Preserves the pilot and D-101 without a custodian | Researcher (owner), 2026-11-13 — <approval quotation> |

**D-124**

> | D-124 | 2026-11-13 (R2-SOLO-AMENDMENT) | **Revision of D-109.** The R1 design (custodian-operated assistant screening) and the R2 design with custodian escrow are withdrawn; the design adopted is D-123. Implementation of `scripts/literature/pilot_commitment.py` (`make`, `verify`, `order`; standard library only) and `tests/literature/test_pilot_commitment.py` (synthetic) is approved, with commit; every Git push in this workflow requires the researcher's separate, explicit approval immediately before that push; no push is pre-authorised. The fixed assistant prompt `research/literature/pilot_assistant_prompt.md` is approved, to be committed before the draw. A test-only update of `tests/literature/test_phase1_screening_tools.py` adds D-122 to the permitted activation states (constant `PILOT_DRAW_ACTIVATION`, two fixture tests) | **APPROVED** (governance and implementation decision) | Single-researcher conduct; no custodian | Researcher (owner), 2026-11-13 — <approval quotation> |

**D-122**

> | D-122 | 2026-11-13 (PILOT-DRAW) | **Run authorisation under D-077 (6).** criteria_version: criteria_v1.1+protocol_v0.2; inventory_sha256: b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054; freeze_entry: D-110; d035_s6_records: D-115, D-116, D-117, D-118, D-119, D-120; single_use: yes; scope: one draw by `scripts/literature/pilot_sample.py` (D-063, D-077; 60 records; seed 4004; frame 1,463; D-113 stop rule) writing `research/literature/screening/pilot_sample.csv` and its sidecar, and one blinded sheet by `scripts/literature/pilot_sheet.py` (`research/literature/screening/pilot_sheet_researcher.csv`, Git-ignored), generated in the assistant pilot session and sent to the researcher only, by Claude app file delivery to the researcher's own account (D-096); assistant start prompt `research/literature/pilot_assistant_prompt.md` SHA-256 df077ac642034493576dd761cdf26be85c6dd0b3ff0812a91deb2cab2149fc76; workflow D-123 (revision of D-102); after each run the ledger `research/literature/screening/run_authorisation_ledger.jsonl` and the committable outputs are committed in a dedicated commit, which is pushed before any further authorised run (D-099 (1)); this entry authorises no push: every Git push in this workflow requires the researcher's separate, explicit approval immediately before that push; no push is pre-authorised | **APPROVED** — run authorisation (single use) | D-077 (6); D-088; D-097; D-123; D-124 | Researcher (owner), 2026-11-13 — <approval quotation> |
