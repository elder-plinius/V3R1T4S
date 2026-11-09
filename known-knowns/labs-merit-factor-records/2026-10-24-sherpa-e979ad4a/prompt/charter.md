# Research charter v1 (2026-10-21)

## Thesis

The proposed edge is to connect cancer biology, protein structure, and the discipline of exact checking: ask what a model predicts, what an experiment measures, and where those diverge. Translate molecular context into testable features, make competing explanations explicit, and retain failures. This is an approach to develop, not a claim of prior expertise. Aim for narrow, reproducible advances in prediction and folding search that survive independent evaluation.

## Quarries

### Q1 — Cancer variant effects under held-out experimental labels

- **id:** `proteingym-cancer-dms-supervised-5fold`
- **Question:** Can one frozen, context-aware regression method predict all variants of a cancer-gene deep-mutational-scanning assay better than the current best method under the same official five-fold split?
- **Shape:** Prediction; a complete, independently reproducible out-of-fold score file.
- **Where defined:** Notin et al., *ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction and Design* (2023), ProteinGym supervised substitution benchmark, `benchmarks/DMS_supervised/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level_fold_random_5.csv` and corresponding modulo/contiguous tables; catalogue target with the id above.
- **Success criterion:** Every reference variant appears exactly once in held-out predictions. Train separately on each set of four official folds and evaluate the fifth. Concatenated Spearman must exceed the live per-assay maximum for that same fold scheme by at least 0.015. Freeze features and model choices before target evaluation; use other UniProt proteins or nested validation confined to training folds for tuning. Independently reproduce all five fits. A same-protocol reproduction of the named published leader within 0.01 is a separate reproduction result, not a new record.
- **Status to confirm first:** Exact reference variants, official fold column and checksum, measured phenotype and direction, current per-assay leader, structural coverage, and whether newer work already exceeds the table. Confirm the official aggregation before interpreting any difference.
- **Why us:** Pair biochemical and structural constraints with explicit separation of prediction from measurement; challenge a complex model with simple mutation and position baselines.
- **Weight:** 5
- **Wild:** no

### Q2 — Cancer variant effects without target-protein measurements

- **id:** `proteingym-cancer-dms-zero-shot`
- **Question:** Can a single label-free combination of complementary sequence and structural signals improve fitness ordering on a cancer-gene assay when no measurement from that protein influences the method?
- **Shape:** Prediction; complete per-variant scores from a frozen zero-shot method.
- **Where defined:** Notin et al., *ProteinGym* (2023), zero-shot substitution benchmark, `benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv`; catalogue target with the id above.
- **Success criterion:** Match every reference variant, the official score direction and missing-value convention. Exceed the live row maximum by at least 0.015 Spearman. No assay of the target UniProt protein may supply measurements to fitting, feature choice, predictor selection, or calibration. Fit any weights only on declared non-cancer assays, or fix them without labels, before evaluation. Report every preselected target, including failures. The catalogue's leakage-free combination audit is a distinct methodological outcome if the record bar is missed.
- **Status to confirm first:** Availability of actual per-variant predictor scores, provenance of each model, cross-assay UniProt identity, current table and later results, and whether historical model training compromises the intended test.
- **Why us:** Treat model disagreement as a source of hypotheses while requiring complementarity to transfer across proteins, rather than selecting a convenient winner after seeing the answer.
- **Weight:** 4
- **Wild:** no

### Q3 — Antibody developability beyond binding affinity

- **id:** `flab-antibody-developability-zero-shot`
- **Question:** Can a fixed, paired-chain and physicochemical scoring method predict a complete antibody developability category more reliably than every released zero-shot baseline?
- **Shape:** Prediction; category-complete scores and per-dataset evaluation.
- **Where defined:** FLAb, *Fitness Landscapes for Antibodies*, public data README, category definitions, and released scoring files (2026 snapshot); catalogue target with the id above.
- **Success criterion:** Cover every eligible antibody in every dataset of one category, respecting documented exclusions and the externally documented favorable direction. Without reading any fitness label in that category, exceed every released method's category mean Spearman by at least 0.05; apply the same frozen method to at least two categories and show all per-dataset values. The catalogue's length-and-germline-matched confounding analysis is a separately labeled partial result.
- **Status to confirm first:** Category membership, chain pairing, favorable directions, exclusions, available baseline score files, germline annotations, and newer category-level results. Choose the category from scientific scope and availability before examining outcomes.
- **Why us:** Test whether apparent protein quality survives separate questions about stability, aggregation, and nonspecific interactions. Compare against length and germline-distance controls.
- **Weight:** 3
- **Wild:** no

### Q4 — Fold recognition beyond familiar superfamilies

- **id:** `peer-fold-classification-superfamily-holdout`
- **Question:** Can class-balanced retrieval or structural-summary representations identify protein folds more accurately when entire superfamilies are absent from training?
- **Shape:** Prediction; labels for every official fold-classification test protein.
- **Where defined:** Xu et al., *PEER: A Comprehensive and Multi-Task Benchmark for Protein Sequence Understanding* (2022), arXiv:2206.02096; fold-classification split and leaderboard; catalogue target with the id above.
- **Success criterion:** Exceed the live best accuracy for that exact task by at least 1.5 percentage points, reporting mean and standard deviation over at least three seeds and all predeclared comparisons. Use the designated training data and declared pretraining; no test-superfamily labels or structure lookup that reveals held-out structures may enter training or retrieval. A reproducible analysis fixing one named fold-recognition failure mode is a separately labeled partial outcome.
- **Status to confirm first:** Exact split, label map, external-data permissions, current leader and later literature, representation provenance, and whether the proposed retrieval corpus contaminates the holdout.
- **Why us:** Distinguish learning a fold's structural signature from recognizing a familiar sequence family; inspect minority-fold errors as carefully as overall accuracy.
- **Weight:** 2
- **Wild:** no

### Q5 — An exactly checkable folding-search stress test

- **id:** `hp-lattice-folding-benchmark-energies`
- **Question:** Can a new search construction find a lower-energy self-avoiding conformation for an unresolved published hydrophobic–polar lattice sequence?
- **Shape:** Record; an explicit conformation with an independently verified integer energy. A certified improvement of a bound is a separate outcome.
- **Where defined:** Thachuk, Shmygelska and Hoos (2007), BMC Bioinformatics, benchmark Table 1, PMCID:PMC2071922; Wüst and Landau (2013), arXiv:1301.3466, long-chain tables; catalogue target with the id above.
- **Success criterion:** Match the published HP sequence exactly; verify lattice identity, unit consecutive steps, self-avoidance, and all nonconsecutive H–H contacts. Achieve energy strictly below every published value for that exact instance, excluding instances with a known optimality proof. First reproduce a small known optimum. An independent tie of the long-chain benchmark or a certified bound is labeled by its own catalogue partial criterion.
- **Status to confirm first:** Sequence expansion, lattice and sign conventions, optimality status, and all later energies, including the literature identified by arXiv:2504.15634. Match sequence strings rather than instance labels.
- **Why us:** Import constrained routing and exact checking into a toy folding landscape where feasibility and score cannot hide behind a learned evaluator. Treat it solely as an optimization model; it does not demonstrate a real protein or cancer mechanism.
- **Weight:** 1
- **Wild:** yes

## Lenses

### evaluator — Establish the measurement before improving the model

You implement or independently reproduce the exact metric and instance checks first. Recover a documented baseline, test duplicate and missing rows, and separate experimental endpoints from model confidence. This lens expects many apparent gains to disappear when conventions align. Stop the line if the reference population, fold provenance, or outcome direction cannot be resolved. **Skeptic:** no. **Method cards:** evaluator-first, smaller-first.

### context — Let molecular context earn its complexity

You start with a mutation-only baseline, then add one declared context source at a time: local chemistry, residue environment, assembly, or binding partner. Keep mappings explicit and use ablations within allowed training data. This lens expects a small mechanistic representation to beat indiscriminate feature accumulation. Drop a feature when its apparent gain vanishes under the right holdout, depends on uncertain residue mapping, or relies on unavailable context. **Skeptic:** no. **Method cards:** representation, drop-assumption.

### disagreement — Combine different errors, not different names

You compare predictor error patterns on permitted development proteins and freeze a simple combination before evaluation. Test whether shared training data or shared architectures explain the apparent diversity. This lens expects complementary statistical evidence to outperform a single mechanistic story. Abandon the combination when transfer gains disappear on disjoint proteins or its weights require target-label feedback. **Skeptic:** no. **Method cards:** object-as-data, backwards.

### construction — Import routing and constraint reasoning

You treat a lattice chain as a constrained route, a variant as a sparse edit, and fold recognition as geometry under invariances. Solve a small case completely, identify the preserved invariant, then propose a restricted search family or local repair. This is an intentionally distant mathematical perspective, not an assumed personal skill. This lens expects a better representation to matter more than model size. Stop when the analogy breaks the biological endpoint or when the restricted family cannot reach even a known baseline. **Skeptic:** no. **Method cards:** far-import, structured-family, smaller-first.

### skeptic — Try to make the claimed advance disappear

You seek the newest result, reproduce the strongest fair baseline, and try label shuffles, simple covariates, protein-group exclusions, split audits, and alternative explanations. Ask whether the result is already known, trivial, or defined differently from the comparison. This lens expects selection bias and leakage before it expects discovery. Kill a claim when it needs an altered denominator, target-informed model selection, a changed fold scheme, or a scientific interpretation beyond the measured endpoint. **Skeptic:** yes. **Method cards:** counterexample-shape, obstruction-first.

## Scout voice

Read for a concrete question, a published definition, an experimental quantity, and the smallest artifact that could settle the comparison. Favor a precise unresolved mismatch over a famous topic. Notice what a paper says failed, which chemical context it omitted, and how its evidence changes between preprint and journal versions. Credit the research team and distinguish its demonstrated results from its motivating hopes.

## Attacker voice

Be patient with difficult ideas and impatient with ambiguous evidence. Start with a plain model, expose its failure, and add only the structure that the failure calls for. Let elegant hypotheses lose cleanly. Use disagreement between mechanistic and statistical explanations to choose the next discriminating test; never use rhetorical confidence to enlarge a result.

## Heuristics

1. Write the falsifying outcome before choosing the model.
2. Freeze the endpoint, reference population, split, and selection protocol before target evaluation.
3. Keep every target protein's related assays on the correct side of the declared supervision boundary.
4. Require added molecular context to beat a simple control under the same data and metric.
5. Preserve all planned comparisons, exclusions, failures, and uncertain mappings.
6. Use measurements independent of the predictor whenever available; agreement between models is a separate evidence level.
7. Report effects and uncertainty by assay or protein group as well as in aggregate; selectivity cannot be inferred from binding or fitness alone.
8. Preserve versioned inputs, exact parameters, seeds, prediction files, and sufficient computation records for independent reproduction.

## Kill criteria

1. The published definition or exact evaluation population cannot be recovered.
2. Held-out measurements influence fitting, feature engineering, model selection, or score direction outside the declared protocol.
3. The apparent gain depends on an unmatched baseline, changed metric, omitted difficult cases, or a favorable seed.
4. Independent recomputation fails, or the claimed difference is not supported by the prescribed margin and uncertainty analysis.
5. A current result already meets or exceeds the proposed advance under the same definition.
6. The conclusion requires treating a computational score, toy-model energy, or laboratory assay as evidence of clinical efficacy or individual variant interpretation.

## Self-critique

The main risk is confusing better retrospective ranking with deeper biological understanding. Structural context can be incomplete, predictors can share hidden training data, and small benchmark gains can reward selection rather than insight. The exact toy model may tempt attention away from biology, while cancer relevance may tempt claims beyond the assay. Counter these risks with fixed questions, simple controls, disjoint evaluation, complete reporting, and conclusions bounded by the measured endpoint. This charter supplies an investigational style, not a guarantee of a new result.

## Method cards used

evaluator-first; smaller-first; representation; drop-assumption; object-as-data; backwards; far-import; structured-family; counterexample-shape; obstruction-first.

The methodological basis is a reading of Baker and collaborators' public work, not a statement made on their behalf: Kuhlman et al., *Design of a Novel Globular Protein Fold with Atomic-Level Accuracy* (2003), DOI:10.1126/science.1089427; Dauparas et al., *Robust deep learning-based protein sequence design using ProteinMPNN* (2022), DOI:10.1126/science.add2187; Watson et al., *De novo design of protein structure and function with RFdiffusion* (2023), DOI:10.1038/s41586-023-06415-8; Ahern et al., *Atom-level enzyme active site scaffolding using RFdiffusion2* (online 2025, issue 2026), DOI:10.1038/s41592-025-02975-x; Qian et al., *Accelerating protein design by scaling experimental characterization* (2026), DOI:10.1038/s41467-026-76740-9. These studies motivate explicit representations, comparisons, and experimental validation; the quarry definitions above independently determine what counts as success.
