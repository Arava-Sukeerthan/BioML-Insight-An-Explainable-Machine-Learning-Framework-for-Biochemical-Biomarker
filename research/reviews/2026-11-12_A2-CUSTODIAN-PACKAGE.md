# A2 — independent custodian package and pilot readiness (2026-11-12, 14:30 UTC)

> **SUPERSEDED (2026-11-13).** The custodian route was not taken: decisions D-123 and D-124 replace it with the single-researcher workflow. This file is kept as a historical record only; no custodian was appointed or contacted, and S1/S2 was never chosen.

> **Status:** preparation only.
> - No custodian is named or assumed. Nobody has been contacted.
> - S1/S2 is not chosen. No decision is recorded. The pilot is not run.
> - No production code changed. Nothing is committed.
> - Repository at `18bfa9f`, remote equal, tree clean before this file.
>
> **Labels:**
> - **[DONE]** completed and verified;
> - **[RD]** researcher decision required;
> - **[CC]** custodian confirmation required;
> - **[EXT]** external verification required.

## 1. A2 conditions and evidence (exact existing wording)
**Sources:**
- custodian minimum requirements C1–C6: `2026-11-12_DECISION-SHEET_A1-A6.md` §2;
- the requirement itself: D-102 (3);
- the A2 text: `2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md` §A2.

The wording below is copied, not edited. The sheet states that **all are needed**, and that *"a second session or account under your control **never** qualifies"*.

| # | Exact wording | Evidence required | Status |
|---|---|---|---|
| C1 | "A different natural person: not you, and with no stake in whether the pilot passes" | Name and role; the custodian's written statement of no stake in the outcome (no authorship or credit tied to the pilot result, no supervisory or financial interest in it) | **Unsatisfied [CC]** |
| C2 | "Their own account and computing environment, to which you have no access" | The custodian's written statement; your statement that you have no access to that account or machine | **Unsatisfied [CC] + [RD]** |
| C3 | "Able to run an assistant session and Python 3 at a recorded commit" | The custodian's confirmation; a check that they can check out the commit named at the draw and run the pilot tools | **Unsatisfied [CC]** |
| C4 | "Receives the private sheet by a private channel; never publishes or commits it; deletes it after disclosure" | Named channel; written undertaking; a written deletion confirmation after disclosure | **Unsatisfied [CC] + [RD]** (channel; S1/S2 decides what is received) |
| C5 | "Returns C before you start screening, and F and S after you finish (target 11-14 to 11-16)" | Written availability for the dates | **Unsatisfied [CC]** |
| C6 | "Does not discuss any pilot decision with you before disclosure" | Written undertaking | **Unsatisfied [CC]** |

**Already satisfied:** none of C1–C6.

**Satisfied prerequisites around A2 [DONE]:**
- D-035 §6 conditions recorded (D-115 to D-120);
- Stage 0 done and committed (`6079ced`);
- the pilot frame is 1,463 as D-063 expects;
- the sheet path is Git-ignored (D-096; checked in A5/A1).

**Information to obtain from the custodian:** C1–C6 confirmations (template §2D), identity, role, experience, the channel, the dates, and their environment details (C3).

**Researcher decisions pending within A2** (all **[RD]**; drafted texts in the consolidated request §A2):
1. **The R1-min revision of D-102.** It replaces clause (1): no salt in any decision file. Instead C = SHA-256("bioml-insight pilot commitment v1\n" ‖ S ‖ "\n" ‖ F) (decision sheet §1 row 6).
   - *Gap:* the "execution pack §2" cited for the full R1-min text is **not in the repository**. Only the summary in the consolidated request and the formula in the decision sheet exist.
   - Approve against those texts, or ask for a consolidated R1-min text first.
2. **The D-096 extension** allowing the custodian to receive the private sheet. Needed under S1, and under S2 for the abstract-free sheet.
3. **The appointment:** name or role, plus the date of the custodian's written C1–C6 confirmation.
4. **S1 or S2,** with your stated basis (§3).
5. **Authorisation to implement and test `pilot_commitment.py`** (synthetic tests) with commit and push.
6. **D-122:** the D-077 (6) run authorisation for the draw, recorded after Stage 0, which is now done.
7. **Governance status note (for your decision, not assumed):**
   - D-063, D-077 and D-102 carry "APPROVED — CONDITIONAL (inactive) until D-035 record §6 is met"; §6 is now recorded as met.
   - Whether status-history rows recording their activation are wanted is your call. No status cell has been edited.

## 2. Invitation package (placeholders only; nothing sent)
### A. Invitation email (draft)
> **Subject:** Request to act as independent custodian for a blinded screening pilot (about 3 days, 14–16 Nov 2026)
>
> Dear <Name>,
>
> I am conducting a structured literature review as part of a research project on explainable machine learning for biochemical biomarkers. Its screening protocol requires an **independent custodian** for a short blinded pilot, so that my own screening cannot be influenced by an automated screener's decisions.
>
> The role involves, between <start date> and <end date>:
> 1. running a prepared AI-assistant screening session on 60 records in your own account and computing environment;
> 2. sending me a short cryptographic commitment (a hash) before I begin my own screening;
> 3. after I have finished, sending me the decision file and a random value (salt) that lets the commitment be verified;
> 4. keeping the material confidential and deleting it afterwards.
>
> You would need no subject-matter expertise, but you should have no stake in the pilot's outcome and should not discuss the pilot decisions with me until disclosure. The expected effort is <estimate, e.g. 2–3 hours> spread over those days. Full instructions and a written acceptance form are attached.
>
> Would you be willing and available? I would be grateful for a reply by <date>.
>
> Kind regards,
> <Researcher name, affiliation>

### B. Responsibilities (detailed)
1. **Set-up (before the draw):**
   - Use your **own** account and machine (C2).
   - Clone the public repository at the commit the researcher names and confirm Python 3 runs the pilot tools (C3).
   - Agree a private channel with the researcher (C4).
2. **Receive the sheet:**
   - Receive the private pilot sheet by that channel. Under S1 it includes abstracts; under S2 it contains IDs and metadata only, and you read the abstracts on PubMed.
   - Never publish, commit, upload to shared storage, or forward it (C4).
3. **Assistant screening:** in your environment, run the assistant pilot screening (protocol v0.2 §7a) on the 60 records with the frozen criteria v1.1 / protocol v0.2. This produces the decision file F.
4. **Commit before the researcher screens:**
   - Generate a random salt S.
   - Compute C = SHA-256("bioml-insight pilot commitment v1\n" ‖ S ‖ "\n" ‖ F), using the tool supplied once it is approved and implemented.
   - Send **only C** to the researcher before they start (C5).
5. **Silence:** do not discuss or hint at any pilot decision until disclosure (C6).
6. **Disclosure:** after the researcher confirms that their own decision file is committed, send F and S unchanged (C5). The researcher verifies C.
7. **Deletion:** delete the sheet, F, S and any local copies. Confirm deletion in writing (C4).
8. **If anything goes wrong** (lost file, early exposure, a tool error): report it; do not repair it silently. A mismatch or early exposure is recorded as an integrity failure (D-102 (5)).

### C. Eligibility checklist (all must be "yes")
- [ ] A natural person other than the researcher (C1)
- [ ] No stake in the pilot outcome: not a co-author credited on the pilot result, no supervisory, financial or evaluative interest in it (C1)
- [ ] Own account and computer; the researcher has no access, not even shared login, a shared drive or a remote session (C2)
- [ ] Can run an assistant session and Python 3 at a recorded commit (C3)
- [ ] Has a private channel with the researcher; will not publish or commit the sheet; will delete after disclosure (C4)
- [ ] Available to return C before the researcher screens and F + S afterwards, within the dates (C5)
- [ ] Will not discuss pilot decisions with the researcher before disclosure (C6)
- [ ] Has read the responsibilities (B) and the sharing option chosen (S1 or S2)

### D. Written acceptance template (for the custodian to complete and sign)
> I, <full name>, <role / affiliation>, agree to act as independent custodian for the BioML-Insight screening pilot and confirm that:
> - **C1** I am not the researcher and have no stake in whether the pilot passes.
> - **C2** I will use my own account and computing environment, to which the researcher has no access.
> - **C3** I can run an assistant session and Python 3 at the commit <commit hash, supplied at the draw>.
> - **C4** I will receive the private sheet only by <channel>; I will never publish or commit it; I will delete it and all derived files after disclosure and confirm deletion in writing.
> - **C5** I will send the commitment C before the researcher starts screening, and the decision file F and salt S only after the researcher confirms their own decisions are committed, between <start> and <end>.
> - **C6** I will not discuss any pilot decision with the researcher before disclosure.
>
> Signature: ____________  Date: ____________

### E. Information the researcher must collect
| Item | Collected? |
|---|---|
| Name and institutional affiliation | [CC] |
| Role and relevant experience (running Python/an assistant session; no subject expertise needed) | [CC] |
| Confirmation of independence (C1) | [CC] |
| Confirmation of a separate account and environment (C2) | [CC] + your statement of no access [RD] |
| Confirmation of confidentiality and deletion (C4, C6) | [CC] |
| Availability during the pilot period (C5) | [CC] |
| Private communication channel (C4) | [CC] + [RD] |
| Signed acceptance of C1–C6 (template D) | [CC] |

**Note:** the custodian's name and contact details are personal data. Record in the public repository only what you choose, for example the role and the date of the written confirmation; never an email address.

## 3. S1 versus S2 (no option chosen; neither shown to comply)
**Evidence on source terms:**
- D-010 states: "Abstracts may be under publisher copyright", and keeps them out of the public repository.
- The NLM/NCBI/PubMed policy pages were **not readable from this environment**: the container proxy returns CONNECT 403, and the server-side fetch tool fails DNS for www.nlm.nih.gov, www.ncbi.nlm.nih.gov and pubmed.ncbi.nlm.nih.gov (re-checked 2026-11-12).
- **No source-term text is quoted or assumed.**

| Aspect | S1: sheet with abstracts, deleted after the pilot | S2: sheet without abstracts; the custodian reads each abstract on PubMed |
|---|---|---|
| Privacy | No personal data of participants; the risk is to the copyrighted text and to blinding. One extra private copy exists temporarily | No abstract copy leaves the project; the custodian accesses public pages |
| Copyright and licensing | A private, purpose-limited copy of up to 60 abstracts is made and transferred. Whether the PubMed/NLM and publisher terms permit this is **unknown [EXT]** | Reading public PubMed pages is ordinary use. Whether the terms restrict systematic reading is **unknown [EXT]** (presumably less exposure, but not verified) |
| Data minimisation | Transfers abstract text | Better: only IDs and metadata are transferred |
| Reproducibility | High: the custodian screens exactly the text the inventory holds (the sheet comes from the fixed inventory, D-114) | Lower: the custodian screens whatever PubMed shows on the day |
| Version consistency | Identical to the researcher's sheet (the same build) | **Risk of drift:** PubMed text may differ from the inventory text (revised or added abstracts, errata); the custodian and researcher may see different texts. Detecting this needs a per-record comparison, which is not available here |
| Operational feasibility | Simple; one file; needs the D-096 extension and a private channel | More work for the custodian (60 look-ups); a PubMed access route; missing or different abstracts need a rule; may delay C |
| Effect on blinding | None | None |
| Outstanding uncertainties | The PubMed/NLM terms on copying and sharing abstracts; the publishers' terms for the 60 sampled records (several publishers); institutional policy | The same terms for systematic reading; how to handle a PubMed abstract that differs from the inventory text; whether that difference compromises the agreement measure |

**Evidence still needed before either option can be approved [EXT]** (you or your institution):
1. The text of the NLM/PubMed copyright and use policy (for example "Web Policies" and the PubMed disclaimer), read in your browser.
2. Where it defers to publishers: the relevant publishers' terms, or your institution's guidance (library or research-integrity office) on sharing a small number of abstracts privately for research quality control.
3. **For S2:** a rule for abstracts that differ or are missing on PubMed versus the inventory. This is a procedural decision [RD].
4. Your stated basis, recorded with the choice (decision template A2).

*Optionally, I can propose adding the three NLM hosts to this environment's network so that I can read and quote the policy pages. You would approve that change.*

## 4. Pilot readiness checklist (strict; every line must be satisfied before the draw)
| # | Item | State |
|---|---|---|
| 1 | Stage 0 complete; ledger committed and pushed (D-099) | **[DONE]** `6079ced` |
| 2 | D-035 §6 recorded (D-115 to D-120); freeze D-110; inventory D-114 | **[DONE]** |
| 3 | Optional activation status notes for D-063/D-077/D-102 | [RD] (see §1 item 7) |
| 4 | R1-min revision of D-102 approved (or a consolidated text requested first) | [RD] |
| 5 | D-096 extension approved | [RD] |
| 6 | Custodian appointed (name or role) | [RD] |
| 7 | Written C1–C6 acceptance (template §2D) | [CC] |
| 8 | Separate account and environment confirmed; your statement of no access | [CC] + [RD] |
| 9 | Sharing method S1 or S2 chosen, with a stated basis; for S2 a drift rule | [RD] + [EXT] |
| 10 | Private channel named | [CC] + [RD] |
| 11 | `pilot_commitment.py` (make/verify) implemented, 5 synthetic tests, committed and pushed | Needs [RD] authorisation (A2), then implementation |
| 12 | Correct repository commit: the custodian checks out the commit named at the draw; it contains the frozen texts and pilot tools | Commit named after item 11 [CC] |
| 13 | D-122 recorded (D-077 (6) run authorisation); the authorisation check passes | [RD] |
| 14 | Draw: `pilot_sample.py … --authorization D-122 --write` → 60 records; frame 1,463; strata as D-063; sidecar hashes equal D-114 (D-113 stop rule); sample, sidecar and ledger committed and pushed (D-099) | After 13 |
| 15 | Private sheet generated (`pilot_sheet.py`), Git-ignored, sent by the private channel | After 14 + 9 + 10 |
| 16 | Custodian returns C; C committed and pushed **before** the researcher screens (D-102 (2)) | [CC] |
| 17 | Timing: researcher screening of the 60 between C and disclosure; target 11-14 to 11-16 (C5) | [RD] + [CC] |
| 18 | Researcher's decision file validated, committed and pushed | [RD] |
| 19 | Disclosure: F and S sent; `pilot_commitment.py verify` equals C; F committed; otherwise an integrity failure is recorded and no agreement is computed (D-102 (5)) | [CC] |
| 20 | Agreement report and pass rule (κ ≥ 0.60, etc.) | After 19 |
| 21 | Deletion: written confirmation from the custodian; the researcher deletes the private sheet (§7a step 6) | [CC] + [RD] |
| 22 | Q-083 (failed-pilot retry) stays open; needed only if the pilot fails | [RD] (if needed) |

## 5. Deadline feasibility (2026-11-27 fixed; status 2026-11-12, 14:30 UTC)
| Milestone (approved plan) | Latest | Status |
|---|---|---|
| A1 + Stage 0 | 11-13 / 11-14 | **Done 11-12** (about one day ahead) |
| A2 + custodian | 11-13 | **Open; the critical path.** Depends entirely on finding a custodian and on your decisions above |
| Pilot complete | 11-16 | Feasible only if A2 is approved and the custodian is confirmed by **11-13**, `pilot_commitment.py` is ready on 11-13, and the custodian works 11-14/15 |
| Title/abstract screening of about 1,403 records + audit + missing-abstract review | 11-19 (R-1 if missed); latest 11-20 | **At risk.** A large volume in 3 days after the pilot, and it needs your audit time |
| Full text Tier 1 + RQ5 | 11-21 | **At risk.** Full texts are largely unreachable from the container, so you must supply PDFs; CR-02/CR-03 are still abstract-only |
| Stage C/D gates, D-016, D-019 freeze | 11-22 (R-2 if missed) | Depends on all of the above plus D-017/D-018 |
| Parallel lanes: A3/A4 environment, Part 2 data decisions, download and build, AB-7 references, Q-061 | 11-20 / 11-21 | **Not started; at risk.** They need approvals that do **not** depend on A2 |
| Experiments | 11-25 | Only if the freeze is on 11-22 and the data lane is ready |
| Manuscript | 11-27 | Only if every item above holds |

**Assessment:**
- 11-27 remains **possible but not likely without immediate action on two fronts**:
  - **(1)** A2 and a custodian by 11-13;
  - **(2)** starting the parallel lanes now (A3, A4, Part 2, download), which are independent of A2.
- If the pilot completes after 11-16, the R-1 condition is likely to be met.
- **No contingency is triggered today.**

**Governance-compliant reductions** (already defined; each needs your explicit approval; none activated):
- **R-1:** full-text reading narrowed to Tier 1 + RQ5, and 20 explanation refits. This reduces literature depth, not validation. It applies if title/abstract screening cannot finish by 11-19.
- **R-2:** applies if the freeze slips past 11-22.
- **R-3:** two manuscripts, if the gates slip past 11-24 or the pilot fails.
- **A6-a scope** (already proposed): Q1–Q3; all six baselines with 5 seeds; groups A, B and C; S-01, S-08, S-10a, S-13; ABL-1 and ABL-2.

**Never reduced:** temporal validation, equal tuning budgets, the leakage safeguards, pilot blinding and the custodian requirement, reporting of null results.

**A sequencing suggestion (not a scope change):** decide A3, A4 and Part 2 now, in parallel with finding a custodian.

## 6. Q-102 implementation proposal (separate from A2; not applied)
- **Proposal file:** `research/reviews/2026-11-12_Q-102_proposed.patch` (SHA-256 prefix `917d805d`). It changes `scripts/literature/rq5_review.py` and `tests/literature/test_rq5_review.py` only, and `git apply --check` passes.

**Design:**
- `KNOWN_VERIFICATION_STATUSES` = the schema enum (verified, partially_verified, unverified, needs_review, failed).
- `bibliographic_label(value)` → (label, citable):

| Value | Label | Citable |
|---|---|---|
| record absent from the inventory | "unknown" (existing label) | no |
| key missing or null | "missing" | no |
| non-string, or a string outside the enum (no case folding or trimming: "Verified" and "verified " are rejected) | "unrecognised (<repr>)" | no |
| exact "verified" | "verified" | **yes (the only citable case)** |

- `matrix()` uses it. `to_markdown` therefore never receives None, which fixes the crash.

**Tests (5 new):**
- known statuses;
- missing and null (and absent; and no inventory supplied);
- unrecognised values (`Verified`, `verified `, `VERIFIED`, empty, `yes`, 1, True, a list, a dict) → never citable;
- the constant equals the schema enum (keeps them in sync);
- the CLI with an inventory lacking the field → "missing (not citable)" and is counted in "Not citable".

**Evidence (scratch copy, deleted):**
- On the current code, 4 of the 5 new tests fail or error. `test_known_statuses` passes, as it should.
- With the patch, the full `run_checks.sh` passes: literature 423 (= 418 + 5), data protection 10, NHANES 39, models 71, query table PASS.
- The current inventory (`b668dbde…`: partially_verified 3,348, unverified 37, needs_review 1) is labelled exactly as now; no record is verified.

**Needs:** your approval to apply, commit and push. It is independent of A2.

## 7. Your next decisions (in order)
1. **Find and invite a custodian** (use §2A–E). Obtain the signed C1–C6 acceptance and dates. *(Target: 11-13.)*
2. **S1 or S2,** after reading the NLM/PubMed policy (and, if needed, publisher or institutional guidance). State the basis; for S2 add a drift rule.
3. **Approve the A2 texts:** R1-min revision of D-102 (or ask for a consolidated text first), the D-096 extension, the appointment, `pilot_commitment.py` implementation, and D-122. Optionally, activation status notes for D-063/D-077/D-102.
4. **In parallel, independent of A2:** A3/A4 (environment, Rule S), Part 2 data decisions plus download, A6 (scope, citation route), Q-061 (ADA PDF or Route 2), and the CR-02/CR-03 full texts.
5. **Q-102:** approve or defer the proposed patch.
6. **Later:** D-016 (after RQ5 is complete, per Q-101) and the D-019 items, by 11-22.
