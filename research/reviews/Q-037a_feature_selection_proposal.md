# Q-037a: Defining the feature/biomarker-selection component for RQ5 (PROPOSAL)

| Field | Value |
|---|---|
| Task | Q-037a (2026-10-24) |
| Status | Written as a PROPOSAL (D-032). **Owner responses received 2026-10-24: D-032 APPROVED — CONDITIONAL, inactive for screening** (see §10 and `RQ5_component_decisions_D032-D034.md`). Nothing here governs screening until the activation conditions are met |
| Decision it serves | D-031 (APPROVED — CONDITIONAL): RQ5 requires ≥ 4 of 5 components (feature/biomarker selection; classification; explainability; probability calibration; uncertainty estimation). This proposal addresses condition **C2** only |
| Not decided here | Q-037b ("covering" a component), Q-038 (3-of-5 frameworks), D-029/R5 (explainability, calibration and uncertainty definitions), screening schema, criteria v1.1 |

Labels: `[EVIDENCE]` verified source or project file; `[RECOMMENDATION]` assistant proposal; `[OPEN]` owner choice.

## 1. The question

**Q-037a.** For RQ5 counting, when does a study have the *feature/biomarker-selection* component? The current documents name the component but never define it for screening:
- `screening_criteria.md` §3, RQ5 row: "biomarker/feature selection";
- `search_strategy.md` §3, concept block F: "feature/variable/biomarker selection; recursive feature elimination; stability selection" (retrieval terms only).

A second, linked question from Q-037: should the component be recorded as its own screening descriptor (`dim_feature_selection`)?

Why it matters. Under D-031, a framework missing one of the other four components qualifies for RQ5 only if it has selection. How broad or narrow this definition is therefore changes the RQ5 set:
- a broad definition (e.g., any importance ranking or any PCA) makes RQ5 easier to reach;
- a narrow one makes it harder.

The recommendation below is based on what "selection" means as a method and on how reproducibly screeners can apply it. It is **not** chosen to enlarge or shrink the RQ5 set.

## 2. Sources used `[EVIDENCE]`

All three were checked through the PubMed connector on 2026-10-24. Only statements visible in the PubMed record (title and abstract) are attributed to them.

| Ref | Bibliographic details | What the record supports |
|---|---|---|
| [S1] | Saeys Y, Inza I, Larrañaga P. A review of feature selection techniques in bioinformatics. *Bioinformatics* 2007;23(19):2507–2517. doi:10.1093/bioinformatics/btm344. PMID 17720704 | Feature selection is an established, distinct family of techniques in bioinformatics; the review provides "a basic taxonomy of feature selection techniques" |
| [S2] | Tibshirani R. The lasso method for variable selection in the Cox model. *Stat Med* 1997;16(4):385–395. doi:10.1002/(sici)1097-0258(19970228)16:4<385::aid-sim380>3.0.co;2-3. PMID 9044528 | The lasso performs variable selection and shrinkage: it "produces some coefficients that are exactly zero". This is selection embedded in model fitting |
| [S3] | Ambroise C, McLachlan GJ. Selection bias in gene extraction on the basis of microarray gene-expression data. *PNAS* 2002;99(10):6562–6566. doi:10.1073/pnas.102102699. PMID 11983868 | When gene selection is not repeated inside each cross-validation step, the error estimate is biased. *Where* selection is done is therefore a quality issue, separate from *whether* it is done |

**Not verified, so not cited.**
- The filter / wrapper / embedded labels used below are this proposal's working terms. They are commonly associated with [S1]'s taxonomy, but the category names were not checked against the full text.
- The statement that projection methods such as PCA create new variables rather than selecting original ones is offered as a definition, not as a cited finding.
- No verifiable source on PLS-DA VIP-based selection was retrieved (two PubMed searches returned nothing). The VIP rules below are operational proposals.
- **No claim is made that the recommended definition is an established standard.**

## 3. Decision options

| Option | Definition | Effect |
|---|---|---|
| **A. Broad** | Any procedure that identifies, ranks or reduces variables: includes importance rankings for interpretation, PCA/latent-variable reduction, and a-priori panels | High recall, low specificity. Overlaps with explainability, so one analysis could count twice. Hard to apply consistently |
| **B. Data-driven subset selection** (recommended) | A documented, data-driven procedure **in the study** that reduces the candidate input variables to a **subset of the original variables**, where that subset is used as model input or reported as the selected panel | Matches the usual meaning of feature selection (choosing variables, not transforming them). Separates selection from explanation and from dimensionality reduction. Moderate recall |
| **C. Narrow** | Only named, dedicated selection algorithms (e.g., lasso/elastic-net selection, RFE, stability selection, Boruta, genetic algorithms). Univariate filtering and VIP thresholds excluded | High agreement, lower recall. Excludes common metabolomics practice (statistical filtering, VIP thresholds), so it would under-count selection in the very literature RQ5 targets |

Separate sub-choice (all options): **knowledge-based panels.** A panel chosen from prior literature or clinical knowledge, without a data-driven procedure in the study, does not count under B. The owner may decide otherwise.

## 4. Comparison of candidate definitions (under option B)

| Candidate | Selection? | Evidence needed | Ambiguous reporting is labelled … | Likely screener disagreement |
|---|---|---|---|---|
| **Explicit selection method**: lasso/elastic-net with variables retained, RFE, stability selection, Boruta, wrapper/GA search | **Yes** | The method is named **and** a retained subset is stated (number or list), or the subset is said to be used in the model | `unclear` if the method is named but it is not stated whether a subset was retained or used (e.g., "a LASSO model was built") | Whether lasso used purely as a classifier counts. Rule: yes only if a selected subset is stated or reported ([S2] shows zeroing is selection, but the abstract must say it was used as such) |
| **Univariate filtering**: t-test / Wilcoxon / FDR threshold / fold change / correlation filter, then a model on the retained variables | **Yes** | A test or criterion with a threshold **and** the filtered variables are used as model input or reported as the panel | `unclear` if differential analysis is reported but it is not stated whether the classifier used only those variables | Very common in metabolomics, where "biomarker discovery" and "classification" are often reported as separate analyses. Needs the link between them |
| **PLS-DA / OPLS-DA VIP ranking or selection** | **Yes** only with a threshold-based retention used as panel or model input; ranking alone **No** | A VIP threshold (or other cut-off) **and** the retained variables form the panel or model input | `unclear` if VIP values are reported without a stated threshold or use | VIP is both a ranking (interpretation) and a selection tool. Disagreement is likely; the threshold-and-use rule is the tie-breaker |
| **Embedded selection inside a model** (tree-based importance thresholding, L1 models, model-based selection loops) | **Yes** if the model's built-in mechanism is used to retain a subset; **No** if the model simply uses all variables (e.g., ridge, a random forest on all features) | The study states that the model's mechanism selected or retained variables, or reports the selected subset | `unclear` if only "embedded selection" or "regularised model" is mentioned without the outcome | Ridge vs lasso vs elastic net: shrinkage without zeroing is **not** selection |
| **Dimensionality reduction**: PCA, factor analysis, PLS components, autoencoders used as model inputs | **No**: a transformation into new latent variables, not a subset of the original variables | — | `no` when latent components are the model input and no original-variable subset is chosen. `unclear` if loadings are later used to pick original variables but the use is not clear | PCA "for feature reduction" is often described as selection. Rule: only original-variable subsets count. Loadings-based selection of original variables, if documented, is **yes** |
| **Feature importance for interpretation only**: SHAP, permutation importance, built-in importance, VIP plots shown but not used to restrict inputs | **No** for selection. May count for **explainability** under D-029 | — | `no` for selection when the abstract shows importance used only to explain a model built on all variables; `unclear` when the use is not stated | The main overlap risk with explainability. A single analysis counts for selection only if it actually restricted the model inputs or defined the reported panel (see §6, example B3) |
| **Biomarker panel from a documented data-driven procedure** (any of the above, multi-step) | **Yes** | The procedure that produced the panel is named or described | `unclear` if a "panel" is reported without saying how it was derived | — |
| **Panel from prior knowledge / literature only** | **No** (sub-choice §3) | — | `unclear` if the origin of the panel is not stated | Some screeners will count any "panel". The rule requires a data-driven procedure in the study |

**Where** selection was done (inside resampling or on the full dataset; [S3]) does **not** affect whether the component counts. It is recorded at full text in the methodological appraisal (`search_strategy.md` §8.2, leakage safeguards).

## 5. Recommended operational definition (option B) `[RECOMMENDATION]`

> **Feature/biomarker selection is present** when the study describes a data-driven procedure that reduces
> the candidate input variables to a **subset of the original variables**, and that subset is either used
> as the input of the classification model or reported as the selected biomarker panel.
> Qualifying procedures include:
> - filter methods with a stated criterion;
> - wrapper/search methods;
> - embedded methods that retain a subset (e.g., non-zero lasso/elastic-net coefficients, importance thresholds used for retention);
> - PLS-DA/OPLS-DA VIP (or similar) thresholds used to retain variables.
>
> **Not selection:**
> - transformations into new latent variables (PCA, factor analysis, PLS scores, autoencoders) unless original variables are then selected;
> - importance or attribution analyses used only to interpret a model built on all variables;
> - shrinkage without exclusion (e.g., ridge);
> - panels taken from prior knowledge without a data-driven procedure in the study.

**Evidence and uncertainty rules.** These are consistent with the D-029 conventions proposed in R5, which are not yet approved.

| Value | Title/abstract rule |
|---|---|
| `yes` | The procedure is named or described **and** a retained subset is stated (number, list, or "the selected metabolites were used in …") |
| `no` | The abstract states that all variables were used, or describes inputs that clearly involve no subset selection (e.g., "PCA scores were used as inputs"; "all 150 metabolites entered the model") |
| `unclear` | Not mentioned (**silence is not `no`**); a method named without the retained subset or its use; "biomarkers were identified" without saying how they relate to the model; a panel of unstated origin; no abstract |

At full text, the value is confirmed or corrected. Final RQ5 membership uses full-text-confirmed values only (as proposed in R5).

**Human review (`needs_human=yes`)** when:
1. selection is `unclear` and the record has ≥ 3 other components that are `yes` or `unclear` (selection then decides potential RQ5 status);
2. one analysis may serve both selection and explanation (example B3);
3. VIP or importance values are reported without a stated threshold or use;
4. PCA or another projection is followed by loadings-based choices.

**Representation `[RECOMMENDATION]`** (design only; nothing implemented):
- New **optional** column `dim_feature_selection` (`yes` / `no` / `unclear`) in `screening/decisions.csv`.
- It would be added to `SCREENING_OPTIONAL` and `SCREENING_ENUMS` in `scripts/literature/pubrecords.py`, to `schemas/screening_decision.schema.json` (properties and `x-column-order`), and as an inventory column.

Why this is safe:
- Optional columns may be omitted, so files without the column stay valid.
- No screening file exists yet, so there is no data to migrate.
- Paper IDs and the registry are unaffected.
- Existing tests that compare code with schema (`test_screening_schema_matches_code`, `test_inventory_columns_match_schema`) would catch any mismatch.

Whether the column is *required* for include/uncertain follows the D-029/R5 decision.

## 6. Examples (hypothetical abstract wording, for illustration only)

**Positive**
- **P1.** "LASSO logistic regression selected 9 of 214 metabolites, which were used to train an SVM." → `yes` (named method, retained subset, used as input).
- **P2.** "Metabolites differing between groups (FDR < 0.05; n = 23) were entered into a random-forest classifier." → `yes` (filter with a threshold; filtered set used as input).

**Negative**
- **N1.** "PCA reduced 300 lipid features to 10 components, which were used as SVM inputs." → `no` (transformation; no subset of original variables).
- **N2.** "An XGBoost model was trained on all 87 laboratory variables; SHAP values were used to explain predictions." → selection `no`. Explainability is assessed separately under D-029.
- **N3.** "A previously published five-metabolite panel was evaluated with logistic regression." → `no` under the recommended sub-choice (no data-driven selection in this study).

**Borderline**
- **B1.** "Differential analysis identified 31 discriminating metabolites; a PLS-DA model achieved AUC 0.91." → `unclear`. It is not stated whether the model used the 31 metabolites or all variables. Full text decides; `needs_human` if this decides RQ5.
- **B2.** "OPLS-DA VIP scores highlighted the most important metabolites." → `unclear` at title/abstract: a ranking without a threshold or use. Becomes `yes` only if the full text shows a VIP threshold used to define the panel or model input; otherwise `no` for selection.
- **B3.** "Random-forest importance was used to choose the top 20 features; the final model was explained with the same importance ranking." → selection `yes` (the ranking restricted the inputs). Whether the *same* ranking also counts for explainability depends on D-029 ("presented as the explanation") and on how Q-037b treats one step serving two components. **Not resolved here**; `needs_human`.
- **B4.** "An elastic-net classifier was developed." → `unclear`. Elastic net can exclude variables, but the abstract does not say that a subset was retained. `yes` at full text only if the non-zero set is reported or used as such.
- **B5.** "PCA loadings were used to select 12 original metabolites, which formed the diagnostic panel." → `yes` (original variables selected; the projection was only the means).

## 7. Risks and limitations

- **Reporting incompleteness.** Abstracts often omit whether discovered biomarkers were the model's inputs, so many records will be `unclear` at title/abstract. Full-text confirmation is needed for RQ5, which adds work.
- **Overlap with explainability.** Importance analyses can play either role. The "used to restrict inputs" test separates them, but B3-type cases need human judgement.
- **Excluding knowledge-based panels** may under-count frameworks built around clinically chosen markers. This is a deliberate owner sub-choice.
- **No verified methodological source for VIP thresholds.** The VIP rule is operational, not literature-backed in this proposal.
- **Effect on RQ5 size is unknown.** The rule has not been applied to any record, and no estimate is given.
- **Agreement unknown.** Inter-screener agreement on this descriptor would be measured only in the pilot (D-025), if approved.

## 8. Dependencies (not resolved here)

| Dependency | Interaction |
|---|---|
| Q-037b ("covering") | Whether selection must be part of the proposed/evaluated framework or merely reported, and whether one analytic step can satisfy two components (B3) |
| Q-038 (3-of-5 frameworks) | How frameworks that miss the threshold only because selection is absent are reported |
| D-029 / R5 | Shared `yes` / `no` / `unclear` conventions; the explainability definition (for B3 and N2); whether descriptors are required for include/uncertain; the potential-RQ5 rule |
| D-027 / screening schema | Adding `dim_feature_selection` as an optional column (§5); D-027 approval currently covers required columns only |
| D-024 / inventory schema | The matching inventory column |
| `screening_criteria.md` v1.1 | The RQ5 row would carry this definition once D-031's conditions C1–C4 are met |
| D-025 pilot | Measures agreement on the descriptor |

## 9. Owner response (left unanswered)

**R-Q037a-1 — Definition option (§3)**
[ ] APPROVE option B (recommended)  [ ] APPROVE option A  [ ] APPROVE option C  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

**R-Q037a-2 — Knowledge-based panels (§3 sub-choice)**
[ ] Do not count (recommended)  [ ] Count  [ ] DEFER
Comments:

**R-Q037a-3 — Evidence/uncertainty rules and human-review triggers (§5)**
[ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

**R-Q037a-4 — Optional descriptor `dim_feature_selection` (§5; implementation later, with tests)**
[ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

**R-Q037a-5 — Recording**
[ ] Record the answers above in `logs/DECISION_LOG.md` (D-032)  [ ] Do not record yet
Comments:

## 10. Owner responses recorded (2026-10-24)

The owner's prompt of 2026-10-24 gave the answers below. Its option letters do not all match the fields in §9, so the answers are recorded by their content (`RQ5_component_decisions_D032-D034.md` §1). The §9 fields above are left as written; this section is the record.

| Field | Owner choice (prompt) | Recorded content |
|---|---|---|
| R-Q037a-1 | Option B | Option B as in §3 and §5 |
| R-Q037a-2 | Option C | A reused published panel alone does not count. A new qualifying procedure in the same study is assessed independently. The study is not excluded for this reason. Reuse is tracked with `scope_flags` token `published_panel_reused` |
| R-Q037a-3 | Option A | Strict evidence: `yes` only when a qualifying procedure **and** the retained subset of original variables are evidenced; `no` only when evidence establishes absence; otherwise `unclear`. Mentions of importance, panels or reduced predictor sets are not enough |
| R-Q037a-4 | Option A | Add `dim_feature_selection` (`yes/no/unclear`). Implemented as an optional column; inactive |
| R-Q037a-5 | Option A | D-032 APPROVED — CONDITIONAL; inactive for screening until its dependencies are resolved |

