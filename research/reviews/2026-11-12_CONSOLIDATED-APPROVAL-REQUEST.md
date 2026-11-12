# Consolidated researcher approval request (2026-11-12, Day 30; deadline 2026-11-27)

> **Nothing in this document is approved or recorded.** Each item takes effect only when the researcher states it explicitly. The decision texts A1–A6 are the wording of the 2026-11-12 execution report. One factual correction found since then is noted under A1. The custodian is not named here.
>
> Repository state: `claude/eloquent-mccarthy-bqtxr3-part1` at `a0af2ad`, with the EXEC-SCAFFOLD work uncommitted.

## How to approve
Reply with the items you approve, for example "Approve A1, A2 (custodian: <name or role>), A3, A4, A5; A6 with changes: …". Items you do not name stay unapproved. Partial approval is possible; the dependencies below say what then becomes possible.

| Item | Unblocks | Depends on |
|---|---|---|
| A1 | Stage 0, then the pilot draw (with A2) | — |
| A2 | Pilot screening | A1 for the draw; a named custodian |
| A3 | Baseline and framework code with real learners | — |
| A4 | Synthetic verification of the classifiers | A3 |
| A5 | Committing and pushing the EXEC-SCAFFOLD work and follow-up work | — |
| A6 | Planning to the deadline; protocol-freeze content | Final at the D-019 freeze |

---

## A1. Screening prerequisites
**Decision text:**
> "Q-063: PRESERVED with recorded limitation (approval date, wording and approver not available; conditions none reported). I approve D-114 to D-121 as drafted in the 2026-11-12 execution pack, and authorise recording them, one Stage-0 run under D-121, and the related commit and push."

**Correction since the execution pack.** I dry-ran the drafted rows against the real authorisation checker (`pubrecords.verify_run_authorisation`) in a temporary copy of the decision log. The repository was not changed.
- The original D-121 text was **refused**: "binding 'single_use' is malformed", because a full stop followed `yes`.
- The corrected text, `single_use: yes; scope: …` (Appendix A), is **accepted**.
- A wrong inventory hash, a wrong criteria version and the wrong clause are each refused.

Approving A1 approves the Appendix A texts.

**Consequences:**
- Q-063 is marked answered, with the historical details recorded as "not available". This is permanent and honest.
- The fixed inventory is bound to `paper_inventory.json` `b668dbde…d054`. Any later change needs a new entry (D-108).
- All six activation conditions are recorded as met, so screening becomes activatable.
- One Stage-0 run excludes records by PubMed publication type. The approved pilot frame expects 7 exclusions.
- The authorisation is single-use and enforced by the ledger, which must be committed before any further run (D-099).

**Facts to verify before approving:**
1. That the WhatsApp approval details really cannot be supplied. If they can, give them instead of "not available".
2. That the private Google Drive copies still exist and are still private.
3. The D-114 hashes: they were re-observed by the assistant on 2026-11-12, and all 244 raw exports matched the manifest that day.
4. The condition bases (all checked by the assistant on 2026-11-12):
   - Q-039 → D-036, Q-040 → D-055 (flag D-061), R5 → D-060 (amended by D-068);
   - condition 3 → D-111;
   - the freeze → D-110;
   - condition 6 (b): the D-096 rules are in `.gitignore`;
   - the literature tools are unchanged since `a0af2ad`.
5. Condition rows 1, 2 and 4 rely on decisions that are approved conditionally and are "met at decision level". This is the reading D-111 and the protocol (§10) already use. Confirm that you accept it.

## A2. Minimum pilot
**Decision text:**
> "I approve the R1-min revision of D-102 as drafted in the 2026-11-12 execution pack §2; I approve the D-096 extension allowing the custodian to receive the private sheet; I appoint <name or role> as independent custodian; I authorise implementing and testing `pilot_commitment.py` (synthetic tests) with commit and push."

**Consequences:**
- Clause (1) of D-102 is replaced: no salt in any decision file.
- The custodian runs the assistant's pilot screening outside your account, sends the commitment C, and later sends the decision file F and the salt S.
- The private sheet, which contains PubMed abstracts, is shared with the custodian. It is never committed and is deleted after disclosure.
- One small tool is built with synthetic tests.
- The pilot itself still needs the D-077 (6) authorisation after Stage 0.

**Facts to verify before approving:**
1. The custodian is independent of the pilot outcome. They are not you, and they have no stake in the result.
2. The custodian has their own account and environment that **you cannot access**. Separate sessions under your account do not count.
3. The custodian can run an assistant session with the frozen texts and the committed tools.
4. Sharing abstracts with the custodian is compatible with the source terms and with D-010. Your judgement is needed here.
5. The custodian can return C before you start, and F and S afterwards.

## A3. Environment (D-002)
**Decision text:**
> "I approve D-002 with the pins in `environment/requirements-proposed.txt` and authorise installing them in a git-ignored virtual environment, testing, and committing a hashed lock file."

**Consequences:**
- Seven packages are installed: scipy, scikit-learn, xgboost, shap, statsmodels and matplotlib, plus the numpy and pandas already present.
- The six baselines and the framework classifier F2 become runnable.
- The lock file fixes the environment for the reproducibility check.

**Facts to verify:**
1. The versions are the latest on PyPI on 2026-11-12 and are **not yet tested together**. If one fails, I will report it and propose a replacement pin; I will not change pins silently.
2. XGBoost is proposed for BL-3 and F2 (Q-048), and k-NN for BL-6 (Q-049). These are protocol choices for the D-019 freeze.

## A4. Synthetic classifier verification (Rule S)
**Decision text:**
> "Under D-040 I approve the test plan 'harness end-to-end with BL-1 to BL-6 and F2 on `scripts/models/synthetic.py` data: (1) runs complete with exactly 40 configurations per method; (2) seed-identical reruns give identical results; (3) validation labels never change development results; (4) a negative control with labels independent of features gives AUROC within 0.5 ± 0.05.' I authorise the test code and up to three runs before 2026-11-27, logged in `SYNTHETIC_VERIFICATION_LOG.md`."

**Consequences:**
- Classifiers are fitted only on artificial data, logged as software verification and never reported as evidence.
- This checks the real learners in the harness before any real data are touched.

**Facts to verify:**
1. **Scope of Rule S.** D-040 names "F-A software" (clinical-anchor offset boosting). Applying the Rule S procedure to the BL-1–BL-6 and F2 harness tests extends that framework. Confirm that this is the governance route you want, or state another one.
2. **Negative control.** It will use n = 3,000 synthetic cases per run. Under no association, an AUROC within 0.5 ± 0.05 is expected with high probability; the criterion is fixed before any run.

## A5. Git
**Decision text:**
> "I authorise committing and pushing the EXEC-SCAFFOLD files to `claude/eloquent-mccarthy-bqtxr3-part1`."

**Consequences:** the scaffolding and its tests go on the PR #17 branch, which grows from 48 to 49 commits. Nothing is merged.

**Facts to verify:**
1. Which files: everything listed under EXEC-SCAFFOLD in `logs/CHANGELOG.md` and the follow-up work of 2026-11-12, both in `logs/CHANGELOG.md`.
2. The list includes this approval document.
3. The files contain no data, only code, synthetic tests and documents.

## A6. Deadline scope
**Decision text:**
> "To meet 2026-11-27, the frozen protocol will: keep primary questions Q1–Q3 and all six baselines with 5 seeds; limit sensitivity analyses to S-01, S-08 (reference), S-10a and S-13, with S-09b only if Q-046 is decided; read full texts in tier order (Tier 1 and RQ5 first), recording any unread as limitations. For citations, I will personally confirm each cited record against its publisher or DOI page, recorded as the second source."

**Consequences:**
- The analysis plan is reduced before any result exists, which is defensible; dropped analyses are reported as prespecified future work.
- Literature reading follows the frozen tier order.
- A citation route becomes possible while the automated second sources stay blocked.

**Facts to verify:**
1. **Citation route vs D-064.** D-064 (approved) says URL-only web rows are not independent second sources. Whether your personal confirmation against the publisher or DOI page counts as a second source under D-064 and `research_plan.md` §6 must be decided **explicitly**. It may need a D-064 amendment rather than a protocol line. Without some route, the manuscript cannot cite any record, because none is "verified".
2. **Final content.** S-08 as the reference analysis is the draft protocol's revision-3 proposal (FA-5) and is still a researcher decision. All A6 content becomes final only at the D-019 freeze.

---

## Evidence status (second pass, 2026-11-12)
Legend: **[V]** verified by the assistant with a command; **[R]** reported by you, not observed; **[U]** unavailable or unverified.

### A1 — Q-063 and the screening records
| Claim | Status | Evidence |
|---|---|---|
| The LIT-003 and LIT-005 archives have integrity | **[V]** | Container checks on 2026-10-23, 2026-10-28 and 2026-10-30 (`preservation_status.md`). The copies you uploaded on 2026-10-30 still hash to `69e690f0…` and `7b7d4674…` on 2026-11-12 |
| The raw exports in this workspace match the manifest | **[V]** | `pubrecords.py verify`: 244/244 on 2026-11-12 |
| **Copies exist in your Google Drive** | **[R]** | Your statement of 2026-10-30. The assistant cannot access Drive |
| **The Drive folder is private** | **[R]** | Your statement ("a private folder"). Not observable by the assistant |
| **The Drive copies have integrity** | **[R]** | Your reported hash equality. Not observed |
| Which file the 2026-10-30 uploads came from (Drive or the laptop) | **[U]** | Not recorded |
| WhatsApp approval date, wording, approver | **[U]** | "Not provided" |
| Conditions | **[U]** | Recorded only as "None reported" |

**Assessment:** "PRESERVED" would rest on facts that are only reported. The truthful alternative is to settle Q-063 without the word PRESERVED. **Alternative A1 wording (replaces only the Q-063 clause):**
> "Q-063: answered — preservation status **'off-device backup designated; integrity and privacy researcher-reported; not independently verified'** (not PRESERVED). Archive integrity is verified in the container; the WhatsApp approval date, wording and approver are not available; conditions are not recorded. I accept this as sufficient to record the fixed-inventory entry, with the limitation stated. I approve D-114 to D-121 as drafted … [rest of A1 unchanged]"

The PRESERVED wording is available only if you confirm in writing **now** that the Drive copies exist and are private, and recorded as your confirmation of that date. The rest of A1 (D-114 to D-121) is unaffected: the dry run accepted the corrected texts **[V]**.

### A2 — the custodian
**Requirements:**
1. **Independent of the pilot outcome:** not you, and no stake in the result.
2. **Uses an account and environment you cannot access.** Separate sessions under your account do not qualify.
3. **Can run an assistant session** with the frozen texts and the committed tools at a recorded commit.
4. **Receives the private sheet,** which contains PubMed abstracts. Whether sharing it is compatible with the PubMed and publisher terms and D-010 is **your judgement [U]**.
5. **Can send C before your screening and F and S after it.**

**Appointment: pending.** No person or role is assumed.

### A3 — environment pins
- **Resolution [V]:** `pip install --dry-run --only-binary=:all:` with the eight pins resolved **without conflict** for CPython 3.13 on Linux x86_64. No package was installed.
- **Not tested [U]:** imports and runtime behaviour are untested until installation.
- **Findings, reported without changing any pin:**
  1. **A pre-release dependency.** `statsmodels` → `formulaic` requires `wrapt>=1.17.0rc1` on Python 3.13. Because that specifier names a pre-release, pip selects **`wrapt 2.6.0.dev1`** (a development build). The latest final release is 2.5.2. **Proposed:** pin `wrapt==2.5.2` in the lock file.
  2. **An unnecessary GPU library.** `xgboost==3.4.1` pulls in `nvidia-nccl-cu13` (**206.6 MB**), a GPU communication library this CPU-only container does not use. The disk has 30 GB free. **Options:** keep it; use `xgboost-cpu==3.4.1` (available on PyPI, CPU-only build); or choose scikit-learn histogram gradient boosting (the third option already listed in Q-048).

  Choosing between these is part of Q-048 and A3; the pins stay unchanged until you decide.

### A4 — why Rule S for the baseline harness extends D-040
- D-040 (1) limits Rule S to **"F-A software"** and lists F-A-specific properties: clinical-anchor offset handling throughout boosting, validation offsets and early stopping, sample weights, persistence, reproducibility and attribution.
- D-040's related settings fix the test location as `tests/synthetic_fa/`.
- The baseline harness (BL-1 to BL-6, F2) is not F-A software, so applying Rule S to it widens D-040's scope.
- **A competing reading exists.** D-042 (2) permits "code scaffolding without fitting a model to real data", which could be read as allowing synthetic fitting. But `CLAUDE.md` rule 13 names Rule S as the *only* exception to "no model training".

**Smallest decision:** one sentence choosing the route, either:
> (i) "D-040 Rule S also covers synthetic verification of the BL-1–BL-6/F2 harness (scope extension)",

or:
> (ii) "Fitting classifiers to synthetic data inside unit tests is code scaffolding under D-042 (2), not model training under CLAUDE.md rule 13".

Either sentence must be recorded before any classifier is fitted. **No classifier has been fitted [V].**

### A5 — Git
**Not granted.** No staging, commit, push or PR change has been made **[V]**.

### A6 — D-064 citation route and Q-054
**D-064 (approved) defines "verified" as an automated build status:**
- full field agreement with an *eligible* second source;
- recorded independence: "PubMed ↔ Crossref or publisher record → `independent` only with recorded retrieval or checked-transcription provenance";
- `research_plan.md` §6: only `verified` records may be cited.

**The A6 sentence "I will personally confirm each cited record against its publisher or DOI page" conflicts with D-064 unless the confirmation is captured as a source record with provenance.** Routes:
- **(a) Compliant with D-064.** You export the publisher or Crossref record of each record to be cited as a raw file, with retrieval provenance (the hosts are blocked for the assistant). Then an authorised rebuild sets `verified` where every field agrees.
  - **Caveat:** a rebuild changes `paper_inventory.json`, so a new fixed-inventory entry is needed (D-108 refinement). Run it **after** screening and the pilot draw.
- **(b) Amend D-064** to accept a researcher-attested manual check. This is a governance change (a new decision row) and weaker evidence.
- **(c)** Defer citations, which is not compatible with a submission-ready manuscript by 11-27.

**Recommendation:** (a), limited to the records actually cited, run after the pilot draw.

**Q-054 (open; needed before D-019):** neither an AUROC non-inferiority margin nor a net-benefit range is justified by a verified source. The smallest decision is one of:
- **(b)** no formal non-inferiority claim; report the AUROC difference with its CI. **Recommended.**
- **(a)** provide a margin value with its justification.

For M10: descriptive only, or dropped.

---

## Appendix A — decision rows D-114 to D-121 (dry-run accepted)
`<DATE>` and `<researcher prompt quotation>` are filled in when you approve. The IDs are re-checked as unused at recording.

| D-114 | <DATE> (SCREENING-ACTIVATION) | **Fixed inventory for Stage 0 and the pilot.** (i) `research/literature/paper_inventory.json` SHA-256 `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054`: verified (equal to the committed blob at HEAD and at `bf0c579`; five methods on 2026-11-11; re-hashed 2026-11-12). (ii) Observed on <DATE>: `records/publications.jsonl` `0141d5d8734ef9e5fd30c3add62ec468f3b088edc79ec3062f8b3acd9b9dd192`; `records/source_records.jsonl` `78eba1d36cc791a9cb4bc9b9cc07b8512d5e12945630c4f9b7d29bfd2d379460`. (iii) Provenance of (ii): "Consistent with the T2 build; not verified by a committed hash." (D-113). Raw exports 244/244 match `MANIFEST.csv` on <DATE>. A new entry is required if any of these hashes changes (D-108). At the draw the sidecar hashes must equal (ii), otherwise the pilot stops (D-113). Records no condition and authorises no run | **APPROVED** (governance decision) | Implements D-107, D-108, D-113 | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-115 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 1 recorded as met.** Q-039 answered by D-036 (classification status column `dim_classification`). Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-116 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 2 recorded as met.** Q-040 answered by D-055 (non-metabolic 3-of-5 frameworks retained with a flag; flag name D-061). Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-117 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 3 recorded as met.** D-027 and D-024 approved for screening as specified in D-111; D-027 part (b) and D-024's remaining extraction fields are excluded and must be resolved before full-text extraction. Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-118 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 4 recorded as met.** The remaining R5/D-029 items are decided by D-060 (as amended by D-068). Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-119 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 5 recorded as met.** Screening criteria v1.1 and protocol v0.2 frozen as `criteria_v1.1+protocol_v0.2` (freeze entry D-110, effective 2026-11-11); "`screening_criteria.md` v1.1" refers to `screening_criteria_v1.1.md` (D-081). Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-120 | <DATE> (SCREENING-ACTIVATION) | **D-035 §6 condition 6 recorded as met.** Closed list of D-091: (a) Phase 1 and Stage B tools and the D-098 code committed and tested at `a0af2ad` (D-112; literature tests 365 OK); (b) the D-096 ignore rules in `.gitignore`; (c) the D-088 binding checks implemented (D-095) in the D-097 format; (d) the inventory hash fixed by D-114. Authorises no run | **APPROVED** (governance decision) | D-035 record §6; D-092; D-097 (b) | Researcher (owner), <DATE> — <researcher prompt quotation> |
| D-121 | <DATE> (SCREENING-ACTIVATION) | **Run authorisation under D-074 (f).** criteria_version: criteria_v1.1+protocol_v0.2; inventory_sha256: b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054; freeze_entry: D-110; d035_s6_records: D-115, D-116, D-117, D-118, D-119, D-120; single_use: yes; scope: one Stage-0 run by `scripts/literature/stage0.py` (D-085 A1–A5) on the fixed inventory D-114; the ledger and outputs are committed and pushed in one dedicated commit before any further run (D-099 (1)) | **APPROVED** — run authorisation (single use) | D-074 (f); D-088; D-093; D-097 | Researcher (owner), <DATE> — <researcher prompt quotation> |
