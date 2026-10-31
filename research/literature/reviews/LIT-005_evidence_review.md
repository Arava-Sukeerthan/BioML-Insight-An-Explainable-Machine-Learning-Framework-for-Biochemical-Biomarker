# LIT-005 — Focused gap searches, transcript-derived notes and evidence review

| Field | Value |
|---|---|
| Task | LIT-005 (researcher instruction, 2026-10-28) |
| Status | **Working document. Not approved.** No screening decisions, no inclusion/exclusion, no novelty claim. Every recommendation needs researcher approval (`CLAUDE.md` rule 7; D-016 reserved) |
| Branch / base | `claude/eloquent-mccarthy-bqtxr3`; prepared on base `53e419a` |
| Session log | `logs/session_logs/2026-10-28_LIT-005.md` |
| Raw exports | 39 new files in `raw_exports/` (git-ignored), registered in `raw_exports/MANIFEST.csv` |

## 0. Evidence labels used here
`GOVERNANCE.md` §1 reserves `[EVIDENCE]` for verified inventory records. **No source in this document is a verified inventory record**, so the following narrower labels are used:

| Label | Meaning |
|---|---|
| `[ABS-28]` | Read by the assistant in the PubMed abstract, metadata retrieved 2026-10-28 (raw file `META_2026-10-28_*.json`). Abstract level only; full text not read; single index (PubMed) |
| `[FT-24]` | Full text (or relevant pages) read by the assistant on 2026-10-24, documented only in the session transcript (§3). Not re-read today |
| `[ABS-24]` | Abstract read on 2026-10-24 (transcript only) |
| `[LIST]` | Search-listing level only (title and listing snippet); not read |
| `[HYPOTHESIS]`, `[RECOMMENDATION]`, `[OPEN]` | as in `GOVERNANCE.md` §1 |

Abstract-level reading here is **not** title/abstract screening under `screening_protocol.md`; it produces no screening status and, under D-035 G2, would never count towards D-031/D-034 anyway.

---

## 1. Searches executed 2026-10-28 (reproducible part)
All PubMed queries were recorded in `search_queries.csv` before execution (status `pending_run`, 2026-10-28T12:04Z), then run unchanged through the PubMed connector (`search_articles`, 200 per page). Every PubMed query was re-fetched with `sort=pub_date` (`CHECK-…`) and compared with `pubrecords.py check-search` (D-023 route-B control, proposed).

| ID | Intended theme | Exact query (PubMed date clause `AND 2015/01/01:2026/10/28[edat]` appended to every PubMed string) | Run (UTC) | Hits | Transcription check |
|---|---|---|---|---|---|
| Q-PM-G1 | 1, 5, 6 | `("Nutrition Surveys"[Mesh] OR NHANES[tiab]) AND (prediabet*[tiab] OR dysglyc*[tiab] OR "undiagnosed diabetes"[tiab] OR "impaired fasting glucose"[tiab]) AND ("Machine Learning"[Mesh] OR "machine learning"[tiab] OR "prediction model*"[tiab] OR "risk score"[tiab])` | 12:04:41 | 44 | passed (44/44) |
| Q-PM-G2 | 6 | `(prediabet*[tiab] OR dysglyc*[tiab] OR "type 2 diabetes"[tiab]) AND ("non-laboratory"[tiab] OR nonlaboratory[tiab] OR "laboratory-based"[tiab] OR "routine blood"[tiab]) AND ("risk score"[tiab] OR "prediction model*"[tiab] OR "machine learning"[tiab])` | 12:05:19 | 27 | passed (27/27) |
| Q-PM-G3 | 6 (methods) | `("added value"[ti] OR "incremental value"[ti] OR "added predictive value"[ti] OR "additional predictive value"[ti]) AND (biomarker*[tiab] OR laboratory[tiab] OR omics[tiab]) AND ("prediction model*"[tiab] OR "clinical predictors"[tiab] OR "clinical model"[tiab])` | 12:05:44 | 33 | passed (33/33) |
| Q-PM-G4 | 5 | `("temporal validation"[tiab] OR "temporally validated"[tiab]) AND ("machine learning"[tiab] OR "prediction model*"[tiab]) AND (diabet*[tiab] OR prediabet*[tiab] OR glyc*[tiab])` | 12:06:15 | 68 | passed (68/68) |
| Q-PM-G5 | 2–4 (closest prior art) | `(SHAP[tiab] OR Shapley[tiab] OR explainab*[tiab]) AND calibration[tiab] AND (conformal[tiab] OR "uncertainty quantification"[tiab] OR "prediction set*"[tiab]) AND (diabet*[tiab] OR prediabet*[tiab] OR "metabolic syndrome"[tiab] OR NAFLD[tiab] OR MASLD[tiab])` | 12:06:38 | **1** | passed (1/1) |
| Q-PM-G6 | 7 (survey design) | `("sampling weights" OR "survey weights" OR "complex survey") AND ("machine learning" OR "gradient boosting" OR "random forest" OR "prediction model") AND (NHANES OR "national survey")` — the 2026-10-24 S6 string; the date cap was **added** (S6 had none and used `max_results=25`), so results are not directly comparable with S6 | 12:06:58 | 21 | passed (21/21) |
| Q-PM-G7 | 7 (outcome definition) | `(HbA1c[tiab] OR "glycated hemoglobin"[tiab]) AND ("fasting plasma glucose"[tiab] OR "fasting glucose"[tiab]) AND (discordan*[tiab] OR concordan*[tiab] OR agreement[tiab]) AND prediabet*[tiab] AND NHANES[tiab]` | 12:07:20 | 2 | passed (2/2) |
| Q-PM-G8 | 7 (leakage) | `("data leakage"[tiab] OR "information leakage"[tiab]) AND ("machine learning"[tiab]) AND (clinical[tiab] OR medical[tiab] OR health[tiab])` | 12:07:41 | 244 (2 pages) | passed (244/244) |
| Q-AX-G9 | 2, 4 | alphaXiv `discover_papers`: question "SHAP stability and class-conditional conformal prediction for tabular clinical data"; keywords `SHAP`, `class-conditional conformal prediction`, `tabular`; difficulty 5 | 12:08:40 | 15 listings | not applicable (ranked, non-reproducible) |
| Q-CN-G5 | 2–4 | Consensus `search`, G-5 PubMed string verbatim (no date clause) | 12:09:07 | — | **Failed: quota.** Tool message: "You've used all 30 searches this month; resets on November 1st." No result, no export |

**Notes**
- The PubMed connector's tool description says wildcards cannot be used. It nevertheless accepted every wildcard query (as on 2026-10-23); `query_translation` in each raw file shows the wildcards were kept.
- G-3 is a methodological strand. D-007 (proposed) would leave methodological strands without a date limit; the 2015 cap was kept as authorised. Older methods papers (P1–P5, §3) are therefore outside G-3 by design.
- **Metadata:** PubMed `get_article_metadata` for the 395 PMIDs not matched in the inventory by PMID (§1.1), in 20 batches of ≤ 20. Responses were saved verbatim by the Claude Code harness and copied unchanged to `META_2026-10-28_000…019.json`. 394 of 395 returned; **PMID 31314250 was not returned** (batch 19: 15 requested, 14 returned). One call hit the rate limit and was retried once.
- **Second-source route:** `api.crossref.org`, `doi.org` and `www.ebi.ac.uk` (Europe PMC) were tested once (2026-10-28) and refused by the environment's network policy (proxy CONNECT 403).
- **Transcription spot-check not done for `Q-AX-G9`:** the alphaXiv file `Q-AX-G9_2026-10-28.json` was hand-copied by the assistant (`structured_transcription`, `transcription_check = not_done`). The ≥ 10 % re-fetch spot-check required for transcribed connector output (D-012, proposed) was **not performed** (compare Q-036 for the LIT-003 arXiv and web files).

### 1.1 Yield
| | Count |
|---|---|
| Unique PMIDs across G-1…G-8 | 435 |
| Already in the 2,979-record inventory (by PMID) | 40 |
| New PMIDs (not matched in the inventory by PMID) | 395 (394 with metadata) |
| New PMIDs from G-1…G-7 only | 173 |
| arXiv listings (G9) | 15 (not checked against the inventory) |
| 2026-10-24 conversation leads re-found | 7: PMID 41950976 (A2, inventory `P0303`), 31694707 (A3), 39990568 (A4) in G-1/G-2; MacNell 2023 (36638125), Kim 2026 (42639427), Si 2025 (39798678) and Morrison 2024 (39678170) in G-6 |

**These records are not in the inventory.** The build cannot run in this workspace (§7). "New" means not matched **by PMID only**: inventory records without a PMID (arXiv and web records) were not compared by DOI, so some of the 395 may duplicate such records. The rebuild's duplicate check is still needed.

---

## 2. Newly found references read at abstract level (2026-10-28)
Selected by the assistant from the G-1…G-7 titles as most relevant to the seven themes (selection is a reading choice, not a screening decision). Identifiers are from PubMed metadata. **Verification status for all rows: single index (PubMed) — equivalent to `partially_verified`; not citable under `research_plan.md` §6.** Full text: not checked, not read. Claims checked against the source: abstract only.

| PMID | DOI | First author, year, journal (PubMed) | Query | What the abstract reports `[ABS-28]` |
|---|---|---|---|---|
| 39696411 | 10.1186/s12911-024-02803-w | Casacchia 2024, BMC Med Inform Decis Mak | G1 | EHR-derived model for HbA1c ≥ 5.7%; Brier, C-statistic, calibration intercept/slope, ICI; external validation and recalibration in **NHANES 2017–2020 pre-pandemic** (2,348 participants, 30.1% outcome) |
| 42922879 | 10.3389/fendo.2026.1961688 | Li 2026, Front Endocrinol | G1, G7 | HbA1c-defined prediabetes, including the phenotype with FPG < 100; NHANES 2005–2018 fasting subsample (6,930) plus a Chinese cohort; survey-weighted models; repeated CV, then **all models, transformations and thresholds frozen** for external validation; TyG-related indices (contain glucose) |
| 31889178 | 10.1093/jamia/ocz204 | De Silva 2020, J Am Med Inform Assoc | G1 | Prediabetes (ADA); NHANES 2013–2014 (n = 6,346) for training/internal validation, **NHANES 2011–2012 (n = 3,000) as external validation**; 156 preselected variables; CDC screening tool AUROC 64.4% as benchmark. (This is not CR-01, which is De Silva 2021, PLoS One) |
| 27371780 | 10.1016/j.diabres.2016.06.022 | Poltavskiy 2016, Diabetes Res Clin Pract | G1 | ADA and CDC screening scores, NHANES 2009–2012 (N = 9,391); for prediabetes AUC 0.72–0.74 (ADA) and 0.70–0.71 (CDC) |
| 25790106 | 10.1371/journal.pone.0120382 | Zhang 2015, PLoS One | G1 | FINDRISC plus HbA1c, NHANES 2005–2010 (3,886), OGTT-defined outcomes; HbA1c ≥ 5.7% alone: sensitivity 35.2%, specificity 86.4% for OGTT prediabetes |
| 34045491 | 10.1038/s41598-021-90406-0 | Vangeepuram 2021, Sci Rep | G1 | Youth, NHANES; ADA biomarker preDM/DM; paediatric screening guideline sensitivity 43.1%, specificity 67.6%; ML classifiers compared |
| 37195986 | 10.1371/journal.pgph.0001556 | Cronjé 2023, PLOS Glob Public Health | G1 | NHANES 1999–2010 (9,987 with fasting samples); three diabetes risk models **miscalibrated by race**, consistently across survey years |
| 39990568 | 10.1101/2025.02.10.25321897 | Hutchison 2025, medRxiv (**preprint**) | G1 | = A4 / CR-03. NHANES 2005–2016 (13,800); GBM estimating 2-h glucose; prediabetes AUROC 0.66/0.71 (HbA1c/FPG) vs 0.77 (model); calibration and decision curves |
| 37567907 | 10.1038/s41598-023-40170-0 | Choi 2023, Sci Rep | G1 | Undiagnosed diabetes, **KNHANES 2014–2018 development, 2019–2020 validation**; non-laboratory features; ML AUC 0.788 vs 0.740 (one feature set) |
| 25570491 | 10.1109/EMBC.2014.6944123 | Chung 2014, IEEE EMBC (conference) | G1 | Prediabetes, **KNHANES 2010 → 2011** validation; SVM AUC 0.761/0.731 vs LR score 0.734/0.712 |
| 42226262 | 10.1186/s13098-026-02176-2 | Kim 2026, Diabetol Metab Syndr | G4 | Diabetes rule-in, adults ≥ 50, **KNHANES 2020–2022 → 2023 temporal validation**; XGBoost; "simple laboratory markers"; calibration, Brier, decision curves, **SHAP**; prespecified threshold |
| 42362634 | 10.1038/s41598-026-59213-3 | Guo 2026, Sci Rep | G4 | **Complete-blood-count-only** model, single centre (Shenzhen); outcome **HbA1c ≥ 5.7%**; development 2018–2023 (70,725), **temporal validation 2024** (26,650); LightGBM AUROC 0.821 → 0.791; calibration: risk ranking preserved, absolute risk **overestimated** in temporal validation; subgroup heterogeneity |
| 40984034 | 10.1177/19322968251376380 | Holm 2025, J Diabetes Sci Technol | G2 | Non-laboratory decision tree for HbA1c-defined prediabetes, 501 adults; age and waist only; AUC 0.83 (train) / 0.80 (validation) |
| 42639928 | 10.1093/aje/kwag195 | Sezgen 2026, Am J Epidemiol | G3 | **Nested predictor blocks** in NHANES 2007–2018 (34,388): demographic/lifestyle → clinical and laboratory → dietary; LR and histogram gradient boosting, 5-fold out-of-fold; clinical block ΔAUC 0.031/0.032; dietary block 0.002 / none. Outcome: self-reported CVD |
| 42838141 | 10.1016/j.diabres.2026.113592 | Yang 2026, Diabetes Res Clin Pract | G3 | Incremental value of retinal parameters over the ADA Risk Test for incident T2D; ΔC 0.005 (internal), 0.013 (external) |
| 32668564 | 10.3390/jcm9072207 | Tucker 2020, J Clin Med | G7 | NHANES, 7,412 adults: **low agreement** between OGTT, HbA1c and FPG classifications; combining FPG and HbA1c did not help for prediabetes |
| 36638125 | 10.1371/journal.pone.0280387 | MacNell 2023, PLoS One | G6 | = 24-Oct lead. NHANES III gradient boosting: unweighted F1 inflated; mitigated when recomputed with weighted outcomes; weights mattered less with low weight variability or n < 5,000 |
| 42639427 | 10.3389/fdgth.2026.1834715 | Kim 2026, Front Digit Health | G6 | = 24-Oct lead. Replicate-weight CV for ML on NHANES (hypertension, diabetes); weighted vs unweighted AUC differ |
| 39798678 | 10.1016/j.annepidem.2024.12.016 | Si 2025, Ann Epidemiol | G6 | = 24-Oct lead. Unweighted ML similar to design-based LR (osteoarthritis, NHANES) |
| 39678170 | 10.1002/cjs.11815 | Morrison 2024, Can J Stat | G6 | = 24-Oct lead. Robust loss-based performance estimators under covariate shift, extended to the NHANES design |
| 37776368 | 10.1093/gigascience/giad071 | Hamdan 2023, GigaScience | G8 | Confound regression combined with nonlinear ML can leak target information |
| 40868358 | 10.3390/bioengineering12080845 | Starcke 2025, Bioengineering | G8 | Inflated performance when diagnostic features are included (Parkinson's) |
| 42800260 | 10.1016/j.compbiomed.2026.111943 | Rangaiah 2026, Comput Biol Med | G8 | Duplicate-record leakage in a public tabular dataset; group-aware CV lowers performance substantially |
| 42557287 | 10.1038/s41598-026-58690-w | Saleem 2026, Sci Rep | G5 (only hit) | Fundus-image deep learning for diabetic retinopathy with Monte Carlo dropout uncertainty — **imaging, not tabular biochemical classification** |

**arXiv listings (G9, `[LIST]`, not read; authors not shown in the listing):** 2609.11838 (target leakage in survey-based cardiovascular screening, national health surveys); 2607.06605 (marginal conformal under-covers the minority class; class-conditional fix; drug discovery); 2610.11957 (subgroup-reliable conformal prediction, clinical motivation); 2606.30702 (population-representative tabular cardiometabolic benchmark with uncertainty quantification and complex survey sampling); 2610.20868 (NHANES, CatBoost and SHAP, biological age); 2602.10532 (statistical inference for SHAP); 2610.11953 (interval-valued SHAP in tree models). The other 8 listings are off-topic by title.

---

## 3. Historical notes recovered from the 2026-10-24 session transcript
**Source and limitations.** These notes come from the assistant's report of 2026-10-24 ("F-A full-text verification and contribution assessment") and the conversation summary preceding it, as stored in the Claude Code session transcript of this session. They were produced in a read-only task and were **never written to the repository**.
- **No raw exports exist** for the 2026-10-24 searches (S1–S21); they are **not** reproducible under D-012 and are **not** re-executed here, except S6 (re-run as Q-PM-G6, with a date cap added).
- Full texts were read by the assistant through PubMed Central / alphaXiv on 2026-10-24; they have **not** been re-read in LIT-005.
- None of these records meets the two-source standard; PMC is not treated as an independent second source (Q-021 open).
- Statements below are the assistant's 2026-10-24 reading, summarised from that report, not re-verified.

| Item | Identifier (as recorded 2026-10-24) | 24-Oct access | Key note (24-Oct report) |
|---|---|---|---|
| P1 Boulesteix & Hothorn 2010 | PMID 20144191; doi 10.1186/1471-2105-11-78 | `[FT-24]` | Fixed logistic-regression offset, componentwise boosting on the new block, binary outcome; clinical part fitted in-sample; allows a fixed external score as offset |
| P2 Binder & Schumacher 2008 | PMID 18186927; doi 10.1186/1471-2105-9-14 | `[FT-24]` | CoxBoost; clinical (IPI) coefficients updated unpenalised, i.e. jointly estimated |
| P3 Volkmann 2019 | PMID 31340753; doi 10.1186/s12874-019-0802-0 | `[FT-24]` | Fixed Cox offset, boosting/LASSO; added value shrinks or disappears with richer clinical models; authors note in-sample clinical model may bias the comparison |
| P4 Tibshirani & Efron 2002 | PMID 16646777; doi 10.2202/1544-6115.1000 | `[ABS-24]` | Pre-validation |
| P5 Boulesteix et al. 2008 | PMID 18544547; doi 10.1093/bioinformatics/btn262 | `[ABS-24]` | Out-of-fold combination of PLS components with clinical predictors |
| Huang et al. 2021 | arXiv 2105.06559; journal DOI per web listing 10.1214/21-AOAS1482 (**not verified**) | `[FT-24]` relevant pages | Tree gradient boosting initialised from an existing model's predictions; compared with Platt and isotonic recalibration |
| Höfling & Tibshirani 2008 | arXiv 0807.4105; DOI 10.1214/07-AOAS152 (not verified) | `[FT-24]` | Standard test on a pre-validated predictor can be biased |
| De Bin et al. 2014 | PMID 25042390; doi 10.1002/sim.6246 | `[ABS-24]` | Strategies for combining clinical and omics data |
| Klau et al. 2018 | PMID 30208855; doi 10.1186/s12859-018-2344-6 | `[ABS-24]` | Priority-Lasso; block offsets |
| Nieboer et al. 2016 | PMID 27678479; doi 10.1186/s12874-016-0231-2 | `[ABS-24]` | Extending an LR model with a new marker; overfitting appears as calibration slope < 1 |
| A1 Türkoğlu Genç & Yildiz 2026 | PMID 42881653; doi 10.3390/healthcare14193214 | `[FT-24]` | Primary care (Türkiye), N = 2,033; FINDRISC as a feature + labs, CatBoost; ΔAUC 0.005 (−0.012 to 0.022); SHAP feature selection on the whole development set |
| A2 Yoo, Maggiore & Jolliet 2026 | PMID 41950976; doi 10.1016/j.jclinepi.2026.112266; inventory `P0303` | `[ABS-24]` | HbA1c/FPG composite outcome; NHANES 1988–2018 development; 7 non-laboratory predictors; external validation NHANES 2021–2023 (N = 3,043), AUROC 0.773 |
| A3 Dinh et al. 2019 | PMID 31694707; doi 10.1186/s12911-019-0918-5 | `[FT-24]` | NHANES 1999–2014; glucose-only prediabetes outcome; lab features including osmolality; abstract 84.4% vs body 80.2%/83.4% |
| A4 Hutchison et al. 2025 | PMID 39990568 (see §2) | `[ABS-24]` | Preprint |
| Zhao 2026; Peprah Osei 2026; Gwira 2024 | DOIs 10.1186/s13098-026-02100-8; 10.1371/journal.pgph.0005596; 10.15620/cdc/165794 | `[ABS-24]` | Period differences 2017–2020 vs 2021–2023 (association); FA-2-type definition in adolescents; NCHS data brief |
| Calibration/validation methods | Van Calster 2016 (10.1016/j.jclinepi.2015.12.005); Van Calster 2019 (10.1186/s12916-019-1466-7, = CR-06); Austin & Steyerberg 2019 (10.1002/sim.8281); Vickers & Elkin 2006 (10.1177/0272989X06295361); Austin 2016 (10.1016/j.jclinepi.2016.05.007); Davis 2020 (10.1016/j.jbi.2020.103611); Guo 2022 (10.1038/s41598-022-06484-1) | `[ABS-24]` | Calibration hierarchy, ICI, decision curves, temporal validity, calibration drift |
| Conformal under shift | arXiv 1904.06019; arXiv 2202.13415 | `[FT-24]` relevant pages | Coverage under shift only under stated conditions; coverage gap bounded by distributional distance |
| Library documentation | XGBoost `base_margin`, LightGBM `init_score` (GitHub source files, master, 2026-10-24) | read | Offsets documented; gradient-at-offset behaviour not stated |

24-Oct conclusion (quoted): F-A is "not a methods contribution"; it is "a reasonable provisional candidate, but only as an application and evaluation study".

---

## 4. Thematic synthesis
Scope: what the sources above report. **No theme is covered by screened, full-text-reviewed, verified evidence.** Statements are labelled by access level.

### Theme 1 — Biochemical-biomarker classification of dysglycaemia
- **Investigated:** NHANES studies use routine and glucose-related laboratory variables for prediabetes/diabetes: A3 (labs including osmolality) `[FT-24]`; A4 (FPG, insulin) `[ABS-28]`; Li 2026 (TyG indices, which contain glucose) `[ABS-28]`; De Silva 2020 (156 preselected exposure variables; whether labs were included is not stated in the abstract) `[ABS-28]`.
- Outside NHANES, Guo 2026 uses **complete blood count only**, a glucose-free laboratory panel, for HbA1c ≥ 5.7% `[ABS-28]`.
- **Consistent:** glucose-containing features (FPG, TyG, osmolality) are common in these models.
- **Uncertain:** no NHANES study using a glucose-free chemistry panel alone (protocol group A) was identified; title-level reading only.
- **Relation to BioML-Insight:** group A is distinguishable from A3/A4/Li 2026 by excluding glucose-derived features (protocol §7), but Guo 2026 shows glucose-free laboratory classification is not new as a concept.

### Theme 2 — Explainability
- SHAP is used in Kim 2026 `[ABS-28]` and A1 `[FT-24]`; A1 selected features with SHAP on the whole development set.
- **No study evaluating explanation stability** (across refits or periods) in dysglycaemia was found. Methods work on SHAP inference and interval SHAP exists `[LIST]`.
- **Uncertain:** whether the 284 explainability-titled inventory records (unscreened) include stability evaluations.
- **Relation:** F5's stability metric still lacks a verified literature basis (protocol AB-7).

### Theme 3 — Calibration
- Reported in Casacchia 2024 (intercept, slope, ICI), Kim 2026 and Guo 2026 (Brier, calibration) `[ABS-28]`; A1 and Huang 2021 `[FT-24]`.
- Guo 2026 reports **overestimated absolute risk on temporal validation** with preserved ranking `[ABS-28]`. Casacchia 2024 externally validated **and recalibrated** its model in NHANES 2017–2020 (the abstract portion read does not report the recalibration results) `[ABS-28]`. Cronjé 2023 reports race-specific miscalibration across NHANES years `[ABS-28]`.
- **Consistent across these abstracts (two studies):** calibration can degrade across periods (Guo 2026) or population groups (Cronjé 2023) even where risk ranking is preserved (Guo 2026). Not established for NHANES 2017–2020 → 2021–2023.
- **Relation:** supports reporting calibration-in-the-large and slope on 2021–2023 as observed, and the protocol's ban on recalibrating with temporal outcomes.

### Theme 4 — Predictive uncertainty
- PubMed G-5 returned one record (imaging, Monte Carlo dropout) `[ABS-28]`; no tabular metabolic study combining explanation, calibration and conformal or interval uncertainty was found in PubMed.
- Methods literature (`[LIST]`): marginal conformal can under-cover the minority class, with class-conditional variants as a remedy (2607.06605); subgroup-reliable conformal (2610.11957). Theory read on 24 Oct `[FT-24]`: coverage does not transfer automatically under shift.
- **Uncertain:** CS venues are poorly indexed in PubMed; Consensus (G-5) failed; arXiv items not read.
- **Relation:** supports class-conditional (Mondrian) sets (protocol F4) and observed-coverage reporting; provides no basis for a novelty claim.

### Theme 5 — Independent or temporal validation
- **Temporal validation across national-survey cycles is established:** KNHANES 2010 → 2011 (Chung 2014), 2014–2018 → 2019–2020 (Choi 2023), 2020–2022 → 2023 (Kim 2026); NHANES 2013–2014 vs 2011–2012 (De Silva 2020); NHANES 2021–2023 as an external set (A2, `[ABS-24]`); NHANES 2017–2020 as an external set (Casacchia 2024) `[ABS-28]`.
- Li 2026 freezes "all fitted models, transformations and thresholds" before external validation `[ABS-28]`, the same principle as protocol §16.
- **Relation:** temporal validation itself cannot be a contribution. The specific 2017–Mar 2020 → 2021–2023 design with laboratory predictors was not found, but A2 (non-laboratory) and Casacchia 2024 (2017–2020) are close.

### Theme 6 — Predictor-group comparisons (biochemical, clinical, combined)
- Nested-block designs exist in NHANES: Sezgen 2026 (clinical + laboratory block over demographic/lifestyle for CVD; dietary block adds ≈ 0) `[ABS-28]`.
- Increment over an established risk score: A1 (labs over FINDRISC, ΔAUC 0.005) `[FT-24]`; Yang 2026 (retinal over ADA Risk Test, ΔC 0.005–0.013) `[ABS-28]`. HbA1c added to FINDRISC raises sensitivity (Zhang 2015) `[ABS-28]`.
- Method level: P3 shows added value shrinks with richer clinical models `[FT-24]`.
- Non-laboratory models: A2, Choi 2023, Holm 2025, Poltavskiy 2016 (ADA/CDC scores) `[ABS-28]`.
- **Consistent:** increments of new marker blocks over clinical models are often small.
- **Uncertain:** no NHANES study was found that compares glucose-free biochemistry alone, clinical alone and combined for the HbA1c/FPG composite.
- **Relation:** the protocol's Q1 comparison (B vs C, A vs C) is plausible as an estimation question; a small or null increment is a credible result.

### Theme 7 — Leakage, outcome definitions, survey design, generalisation
- **Leakage** is widely recognised: 244 PubMed hits for G-8. Mechanisms read at abstract level: confound regression (Hamdan 2023), diagnostic features (Starcke 2025), duplicates (Rangaiah 2026) `[ABS-28]`. Survey-based screening target leakage (2609.11838) is `[LIST]` only. Examples relevant to this project: A1 (feature selection outside folds) and A3 (osmolality) `[FT-24]`.
- **Outcome definitions:** HbA1c, FPG and OGTT classifications agree poorly in NHANES (Tucker 2020; Zhang 2015; Li 2026, HbA1c-defined prediabetes with FPG < 100) `[ABS-28]`. The FA-2 composite therefore combines heterogeneous phenotypes.
- **Survey design:** mixed evidence on weighting (MacNell 2023; Kim 2026; Si 2025; Morrison 2024) `[ABS-28]`.
- **Generalisation:** calibration drift (Theme 3).
- **Relation:** supports the protocol's glucose-derived-variable exclusion, nested preprocessing, outcome-component sensitivity analyses (S-01, S-03) and weighted sensitivity analyses (FA-7).

---

## 5. Related-work comparison matrix
Access level in the last column. "—" = not reported in what was read.

| Study | Data | Outcome | Predictors | Lab glucose-free? | Increment design | Calibration | Uncertainty | Explanation | Temporal/external | Access |
|---|---|---|---|---|---|---|---|---|---|---|
| A2 Yoo 2026 | NHANES 1988–2018 | HbA1c/FPG composite | 7 non-lab | n/a (no labs) | no | yes | — | — | NHANES 2021–2023, KNHANES | ABS-24 |
| Casacchia 2024 | EHR → NHANES 2017–2020 | HbA1c ≥ 5.7% | EHR model (8 predictors in approximation) | — | no | intercept, slope, ICI | — | — | external + recalibration | ABS-28 |
| Li 2026 | NHANES 2005–2018 fasting + China | HbA1c prediabetes | TyG-related indices | **no** (glucose) | compares indices | — | — | — | frozen external | ABS-28 |
| A3 Dinh 2019 | NHANES 1999–2014 | glucose-only | labs incl. osmolality | uncertain | no | no | — | importance | no | FT-24 |
| A4 Hutchison 2025 (preprint) | NHANES 2005–2016 | OGTT | FPG, insulin and others | **no** | vs HbA1c alone | yes | — | — | no | ABS-28 |
| De Silva 2020 | NHANES 2013–2014 / 2011–2012 | prediabetes (ADA) | 46 of 156 variables | — | vs CDC tool | — | — | importance | cross-cycle | ABS-28 |
| Kim 2026 (KNHANES) | KNHANES 2020–2023 | diabetes rule-in | incl. simple labs | — | — | yes | — | SHAP | 2023 temporal | ABS-28 |
| Guo 2026 | Single centre, China | HbA1c ≥ 5.7% | CBC only | **yes** | no | yes (drift) | — | — | 2024 temporal | ABS-28 |
| A1 Türkoğlu Genç 2026 | Primary care, Türkiye | HbA1c/FPG composite | FINDRISC + labs | — | ΔAUC over FINDRISC | yes | — | SHAP | no | FT-24 |
| Sezgen 2026 | NHANES 2007–2018 | self-reported CVD | nested blocks | — | **nested blocks** | — | — | — | no | ABS-28 |
| P3 Volkmann 2019 | breast cancer | survival | clinical + omics | n/a | fixed offset | IBS | — | — | independent set (one study) | FT-24 |
| Huang 2021 | simulation + clinical | binary | existing model + new | n/a | tree boosting from model | vs Platt/isotonic | — | — | no | FT-24 |
| **BioML-Insight (draft protocol, not approved)** | NHANES 2017–Mar 2020 | HbA1c/FPG composite (FA-2, pending) | A (21), B (27), C (6) | **yes** (§7) | B vs C, A vs C | F3 | F4 Mondrian conformal | F5 SHAP stability | 2021–2023, single frozen run | — |

---

## 6. Research-gap matrix `[HYPOTHESIS]`
"Support" = evidence that the gap exists; "Counterexamples" = closest work against it. Strength scale: none / weak / moderate / strong.

| # | Candidate gap | Support | Counterexamples / close work | Competing explanations for not finding studies | Strength | Remaining uncertainty | Implication | Enough to guide design? |
|---|---|---|---|---|---|---|---|---|
| G-a | No NHANES study estimates what a **glucose-free routine chemistry panel** adds over clinical predictors (and performs alone) for HbA1c/FPG-defined dysglycaemia with **2017–Mar 2020 → 2021–2023** temporal validation | G-1 (44), G-2 (27), G-3 (33): none found at title level; 24 abstracts read (§2) | A2 (same outcome and validation period, no labs); Casacchia 2024 (NHANES 2017–2020, HbA1c ≥ 5.7%, recalibration); Li 2026 (NHANES fasting, frozen external, glucose-containing); Sezgen 2026 (nested blocks, other outcome); A1 (same question, other population) | PubMed only; title-level; vocabulary ("laboratory", "biochemical") may miss studies; Europe PMC/Crossref/Consensus not searched; 2,979 inventory records unscreened; topic may be considered routine rather than missing | **weak–moderate** | Screening not done; A2 full text unread | Frame as **estimation**, not superiority | **Provisionally yes**, for framing the question only |
| G-b | Glucose-free biochemistry alone has not been evaluated for dysglycaemia in NHANES | none found | **Guo 2026** (CBC only, HbA1c ≥ 5.7%, temporal) outside NHANES | as G-a | weak | as G-a | Keep group A as a comparison arm; do not claim novelty for it | Yes, as a design arm |
| G-c | Explanation **stability** across refits/periods is not reported in dysglycaemia ML | none found in G-1/G-4 abstracts read | SHAP methods work `[LIST]`; 284 inventory XAI titles unscreened | PubMed search did not target stability terms | weak | high | Keep F5 stability as a reported outcome | Yes, as an outcome; no claim |
| G-d | Calibration + class-conditional conformal + explanation evaluated together under temporal shift for tabular metabolic classification | G-5: 1 PubMed hit (imaging) | methods papers on class-conditional/subgroup conformal `[LIST]`; RQ5 records (120 unique: Q-PM-11 102 + Q-PM-12 19, one record retrieved by both) unscreened; Consensus blocked | CS venues poorly indexed in PubMed; terminology varies (prediction intervals, selective prediction) | **weak (absence of evidence only)** | high | **No novelty claim** | **No** |
| G-e | Temporal validation across survey cycles is rare | — | **Refuted:** Chung 2014, Choi 2023, Kim 2026 (KNHANES), De Silva 2020, A2, Casacchia 2024 | — | gap not supported | low | Temporal validation is good practice, not a contribution | Yes: rules out the claim |
| G-f | New offset-boosting **method** (F-A) | — | **Refuted (24 Oct):** P1, P3, Huang 2021 | — | gap not supported | blocked statistics/ML databases | No method novelty | Yes: rules out the claim |
| G-g | Leakage-safe evaluation is uncommon in applied studies | A1, A3 examples | 244 G-8 hits show leakage is widely recognised; leakage-controlled benchmarks exist | prevalence not measured | weak | unknown prevalence | Leakage audit = design safeguard | Yes, as a safeguard; no prevalence claim |
| G-h | Survey-design handling in NHANES ML is inconsistent | MacNell, Kim, Si, Morrison | Si 2025: unweighted ML ≈ design-based LR | — | weak–moderate | mixed results | Keep weighted sensitivity analyses (FA-7) | Yes, for sensitivity analyses |
| G-i | Outcome-definition heterogeneity (HbA1c vs FPG) is rarely handled in ML for dysglycaemia | Tucker 2020, Li 2026, Zhang 2015 show discordance | not searched for ML handling | G-7 was NHANES- and concordance-specific | weak | high | Report outcome-component sensitivity (S-01, S-03) | Yes, for sensitivity analyses |

---

## 7. Inventory and generated artifacts
- `paper_inventory.csv`/`.json` remain at **2,979 records** (unchanged, LIT-003 build). The 395 new PMIDs (not matched by PMID; no DOI comparison with PMID-less records, §1.1) and 15 arXiv listings are **not** in the inventory.
- `pubrecords.py build` stops in `verify_manifest` before writing anything because the 205 LIT-003 raw exports are missing in this workspace. The generated artifacts were therefore **not rebuilt and not hand-edited**. The new raw exports are registered, so a rebuild after the LIT-003 exports are restored (from the researcher's backup) will add them.

## 8. Screening remains blocked (D-035 record §6)
| Condition | State |
|---|---|
| 1. Q-039 classification status column | **Met** (D-036) |
| 2. Q-040 retention of non-metabolic 3-of-5 frameworks | **Unmet** (Open) |
| 3. D-027 and D-024 (screening-file and inventory schemas) approved | **Unmet** (both PROPOSED) |
| 4. Remaining R5/D-029 items: validation design, required-descriptor rule (Q-032), triggers | **Unmet** (D-029 PROPOSED) |
| 5. D-031–D-035 written into `screening_criteria.md` v1.1 and protocol v0.2, frozen as `criteria_version` | **Unmet** (criteria v1.0, protocol v0.1 drafts) |
| 6. Other pilot-blocking items | **Unmet.** Authoritative list: `research/reviews/final_confirmation_sheet_LIT-004.md`, "Pilot-blocking items after confirmation": (1) Q-028/D-031 conditions C1–C4 resolved (R5; Q-037a/b; Q-038); (2) R5/D-029 definitions approved; (3) D-024 and D-027 recorded; (6) the arXiv transcription spot-check runs and passes (Q-036), so that D-012/D-023 and Q-022 can be recorded; (7) v1 Items 6–9 and 13–15 recorded (scope, Q-PM-02, audit, pilot design D-025/Q-026, A-1/A-2/A-5/A-6); (8) implementation of D-027, D-028, D-029, `biomarker_class` and the scope flags, with tests and a rebuild that changes no paper ID or existing value; (9) criteria v1.1 and protocol v0.2 frozen as the pilot's `criteria_version`. Also `screening_protocol.md` blocker B-6: scope questions Q-001 and Q-002, D-009/Q-007 (Q-PM-02 strand), D-008/Q-008 (audit), Q-022 (strategy approval). **Not pilot-blocking** per the same sheet: Q-024 pair decisions (deferred until after the pilot), D-030 (for the current data), D-010, Q-034 (before extraction). The pilot design (D-025, blinded double screening) still needs a second screener |

**Proposed screening plan `[RECOMMENDATION]`, not started:**
1. By 2026-10-31: restore the LIT-003 raw exports and rebuild, so the LIT-005 records receive paper IDs.
2. By 11-01: researcher decisions on conditions 2–6; criteria v1.1 and protocol v0.2 frozen.
3. 11-02 → 11-04: pilot on 60 records (D-025), with a second screener or a recorded single-screener decision.
4. 11-04 → 11-10: title/abstract screening of a **priority strand**: the 194 G-1…G-7 PMIDs (173 new + 21 already in the inventory; G-8-only hits excluded), Q-PM-02 (743) and the RQ5 queries Q-PM-11/12 (120 unique records; one retrieved by both). The remaining strands are screened only if time permits, and the reduced scope is reported.
5. 11-08 → 11-15: full-text review of ≤ 30 priority records (D-035 G3), including A2.

## 9. Recommended contribution `[RECOMMENDATION]`, not approved (D-016 reserved)
> A prespecified, leakage-audited **estimate of the incremental predictive value of a glucose-free routine biochemistry panel** over clinical predictors, and of its value alone, for HbA1c/FPG-defined dysglycaemia in US adults (NHANES 2017–March 2020), tested once on frozen models in NHANES 2021–2023, with discrimination, calibration (including calibration-in-the-large drift), class-conditional conformal coverage and explanation stability reported as observed.

- **Distinguishable from:** A2 (no laboratory predictors); Casacchia 2024 (HbA1c-only outcome, EHR model, no biochemistry increment); Li 2026 (glucose-containing indices, external not temporal); A3/A4 (glucose-related features, other outcomes); Guo 2026 (CBC, single centre, not NHANES); Kim 2026 (KNHANES, diabetes); Sezgen 2026 (other outcome, no temporal validation). Each distinction rests on abstract-level reading and PubMed only.
- **Not claimed:** a new algorithm (G-f); novelty of temporal validation (G-e); novelty of combining explanation, calibration and uncertainty (G-d); worldwide novelty; superiority over baselines. A small or null increment is an expected, publishable estimate (A1, P3, Sezgen 2026, Yang 2026).
- **Testable:** protocol §13 Q1 (B vs C, A vs C) and Q3 (temporal change).
- **Limitations:** temporal, not external, validation; one cross-sectional survey; composite outcome with discordant components; structured, not systematic, review (D-005 proposed).

## 10. Citations requiring further verification
All rows in §2 and §3. Priority: A2 (full text; eligibility; development-data overlap); CR-08 ADA (Q-061); Casacchia 2024 and Li 2026 (closest NHANES designs: full text); Guo 2026 (counterexample to G-b: full text); Huang 2021 journal version; P4, P5; CR-01, CR-05, CR-07 (not found in G-1…G-8); CR-09–CR-12 (not located); PMID 31314250 (metadata not returned).

## 11. Limitations of this task
PubMed only for systematic queries; Consensus blocked (quota); Crossref, doi.org and Europe PMC blocked (network policy); alphaXiv ranked listings not read and their transcription not spot-checked (D-012); no forward citation search; 2026-10-24 notes not re-verified; abstract-level reading of 24 PubMed records only; no screening.
