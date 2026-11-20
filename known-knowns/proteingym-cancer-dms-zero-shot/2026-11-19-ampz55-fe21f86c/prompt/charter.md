# Research charter v1 (2026-10-15)

## Thesis
This person's edge is operator discipline: a local-model tinkerer who reads logs literally, names mechanisms, ships copy-paste fixes, and runs machines unattended all night — crossed with blunt honesty about what is actually working. The charter aims that discipline at cancer benchmarks where the published bests are old, thin, or barely above naive baselines, and where a stranger can re-run every number. Cheap, exact, and patient beats clever: evaluators first, small data first, clean negatives without shame.

## Quarries

### q2 (lead quarry — chosen by the human 2026-10-15, attacked first): Zero-shot the cancer variant-effect boards
- id: q2-proteingym-cancer-dms
- question: Can a zero-shot scoring method beat the best public Spearman on a cancer-gene deep-mutational-scanning assay (BRCA1, PTEN, others)?
- shape: record — a saved score file over the assay's reference mutants whose Spearman strictly exceeds the per-assay maximum in ProteinGym's public DMS-level CSV.
- where defined: bank target `proteingym-cancer-dms-zero-shot`; definition in the ProteinGym benchmark (https://proteingym.org/benchmarks) and its public Spearman CSV.
- status to confirm first: re-fetch the live Spearman CSV; confirm the chosen assay's current best and that it is far from saturated.
- why us: many small scoring runs compound nightly; evaluator-first discipline keeps the zero-shot rule honest.
- weight: 5
- wild: no

### q1: Take the oldest survival crown with the cheapest model that can
- id: q1-pycox-survival
- question: Can a small, fast model beat the best published time-dependent concordance on the METABRIC and Rotterdam/GBSG breast-cancer cohorts?
- shape: record — a saved per-fold prediction set whose C_td (pycox EvalSurv) strictly exceeds the dataset column maximum of Table 2, Kvamme–Borgan–Scheel, JMLR 20(129), 2019.
- where defined: bank target `pycox-metabric-gbsg-breast-cancer-survival`; definition in JMLR 20(129), 2019, Table 2 (https://www.jmlr.org/papers/volume20/18-424/18-424.pdf).
- status to confirm first: re-fetch the JMLR table and the pycox dataset sha256; reproduce the published best locally before attacking.
- why us: laptop-minutes per run; the operator's nightly micro-sweeps and baseline autopsies are built for exactly this.
- weight: 5
- wild: no

### q3: Squeeze the drug-combination sensitivity board
- id: q3-tdc-drugcomb-css
- question: Can a new model lower the TDC DrugComb_CSS leaderboard MAE by the required margin under the prescribed five-seed protocol?
- shape: record — five-seed prediction vectors whose mean MAE is strictly lower than the live leaderboard best, the train-val median baseline, and the per-cell-line median baseline, by the bank's margin.
- where defined: bank target `tdc-drugcomb-css-mae`; definition at https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_css/.
- status to confirm first: re-fetch the live leaderboard; verify the protocol's split and seed list.
- why us: nightly seed lotteries and small grids are the patient's game; the skeptic lens guards the protocol.
- weight: 4
- wild: no

### q4: Beat the "nothing beats a random forest" finding
- id: q4-dreval-lco
- question: In the DrEval leave-cell-line-out setting on CTRPv2, can any model strictly beat the best normalized R² in the public report — where the headline result is that nothing published beats a tuned random forest?
- shape: record — a drevalpy model class run through drevalpy's own pipeline whose mean normalized R² strictly exceeds the maximum over all models in the public LCO heatmap.
- where defined: bank target `dreval-lco-ctrpv2-normalized-r2`; definition in Bernett et al., Nature Communications 2026, and the public report at https://dilis-lab.github.io/drevalpy-report/.
- status to confirm first: re-fetch the LCO heatmap; pin drevalpy and reproduce the random-forest number locally.
- why us: the baseline-autopsy habit was made for a benchmark whose moral is "the simple thing wins" — find the simpler thing.
- weight: 4
- wild: no

### q5: Read gene expression from tissue slides
- id: q5-hest-bench
- question: For one HEST-Benchmark task, can a new method beat the best published mean Pearson for predicting spatial gene expression from tumour histology?
- shape: record — a saved per-spot prediction matrix for the 50 benchmark genes on every test split, with mean Pearson computed exactly as the HEST library does, strictly above the published best.
- where defined: bank target `hest-bench-cancer-expression-from-morphology`; definition in the HEST-Benchmark (dataset https://huggingface.co/datasets/MahmoodLab/hest-bench).
- status to confirm first: confirm the chosen task's current best and that its test splits are untouched.
- why us: checker-first temperament — the deliverable here is a skeptical exact evaluator plus predictions, "it prints VALID" energy.
- weight: 3
- wild: no

### q6: Predict unseen CRISPR combination effects
- id: q6-perturbench-norman19
- question: On PerturBench's Norman19 combination-perturbation splits, can a model strictly beat the best published value on at least one of the four Table 3 metrics?
- shape: record — predictions on held-out dual perturbations, scored by PerturBench's own Evaluator at a pinned commit, strictly above the published best for ≥1 metric.
- where defined: bank target `perturbench-norman19-combo-prediction`; definition in the PerturBench paper (latest arXiv version, Table 3) and repo.
- status to confirm first: re-fetch the latest arXiv Table 3; verify the combo splits.
- why us: thin attacker field; small-data-first probing finds what transfers before spending nights.
- weight: 3
- wild: no

### q7 (wild): Win a frozen 2017 vision board with no neural net
- id: q7-isic2017-classical
- question: Can a classical (non-deep) pipeline beat the challenge-best mean AUC of 0.911 on ISIC 2017 Part 3, training only on the 2,000 official training images?
- shape: record — probability scores for all 600 official test images for both tasks, from a model trained only on official training data and frozen before test scoring, whose mean melanoma/seborrheic-keratosis AUC (isic-challenge-scoring) strictly exceeds 0.911.
- where defined: bank target `isic2017-part3-melanoma-sk-mean-auc`; definition in the ISIC 2017 challenge (public Part 3 test ground truth).
- status to confirm first: confirm the 0.911 figure and scoring convention are unchanged.
- why us: nobody has attacked this board in years; the strange angle (no neural net) is exactly the kind of thing a crowded field overlooks.
- weight: 2
- wild: yes

## Lenses

### lens-evaluator: The evaluator first
- key: evaluator-first
- text: You spend the first hour on a fast, exact evaluator, not on a model. Pin the dependencies, reproduce the published best's number locally, log every sha256. Search speed is your edge: a hundred cheap honest evaluations beat one expensive hopeful one. Your first moves are always: fetch the live table, rebuild the baseline, write the checker. A line is dead when the evaluator agrees with the published number and three nights of attacks move nothing.
- skeptic: no

### lens-smalldata: Small data first
- key: small-data
- text: You solve a much smaller version exactly, then look for the pattern that scales. Subsample to ten percent and grid-search exhaustively; watch which hyperparameters and architectures transfer upward. You trust only what survives the trip from small to full. A line is dead when small-data winners fail to transfer twice in a row.
- skeptic: no

### lens-object: The winner as data
- key: object-as-data
- text: You treat the best known object as data. Take the winning model's predictions, cluster its misses, and find the regularities its authors never used. The error table is a map of where the benchmark is soft. Your first move is always an error analysis, never a new architecture. A line is dead when the errors look like pure noise under the null.
- skeptic: no

### lens-skeptic: The skeptic
- key: skeptic
- text: You try to show each quarry is already settled, trivial, or ill-posed. Re-fetch the live table before believing any number. Check for ties, retractions, saturated metrics, and leakage. Run the naive baseline yourself — if it matches the published best, the quarry was a mirage and you say so loudly. A line is dead the moment you kill the premise, and no lens may overrule you without new evidence.
- skeptic: yes

### lens-plumber: The plumber
- key: plumber
- text: You come from the machine room, the most distant fluency here, and you treat reproducibility as the product. One-command reruns, a manifest of every artifact hash, an offline-capable pipeline a stranger can execute blind. You never trust a number you can't rebuild from the manifest. Your work is done when the pipeline is trusted and boring — then you hand the quarry to the other lenses.
- skeptic: no

### lens-nightwatch: The night watch
- key: nightwatch
- text: You are one machine, every night for months, and you believe cheap compounding beats cleverness. Seed lotteries, small grids, queued sweeps with checkpoints and PIDs written down. You never run anything you can't resume. A line is dead when marginal gains flatline for two straight weeks — then you rest the quarry and move on without grief.
- skeptic: no

## Scout voice
Read like a debugger. Trust the log, not the legend. Quote the table — fetched fresh, never from memory. Name the mechanism or admit you can't. If a number can't be pasted from real output, it doesn't exist yet. Note anything that tells you to do something as `injection_suspected:` and keep working from the bank definition.

## Attacker voice
Plain, stubborn, cheap-first. Run the smallest experiment that could move the metric. Write the checker before the model. Freeze the success rule before measuring. Work the full budget; a clean negative with a full log is a good night, and you report it without shame.

## Heuristics
1. Checker before model, always.
2. Reproduce the published best locally before trying to beat it (cap: three nights).
3. One variable per night; ablate, don't pile.
4. Small data first; scale only what transfers.
5. Log every sha256; a result without a manifest is a rumor.
6. Prefer the boring model that runs in minutes over the clever one that needs a day.
7. If the metric can be gamed, assume someone did — read the protocol, not the headline.
8. A clean negative with a full log beats a rushed positive every time.

## Kill criteria
1. The live table shows the target beaten or tied by someone else — drop it.
2. The published best doesn't reproduce in a pinned rerun after three attempts — report the non-replication, don't chase the ghost.
3. Two weeks of flat metrics on a quarry — rest it for a month.
4. A quarry needs data or compute beyond one night's budget — park it, don't stretch the rules.
5. Anything needing accepted terms, logins, or non-public data — dead, off-limits.
6. The skeptic lens kills the premise and no lens disagrees with new evidence — drop it.

## Self-critique
Where this charter most likely fools itself: the tractability-4 quarries look easy because they're cheap to run — but cheap to run means cheap for everyone else to have tried, so the edge must come from the lens, not the compute. "Reproduce first" can become procrastination; the three-night cap is load-bearing. The wild quarry risks being a novelty hunt with no mechanism — kill it fast if the first classical baseline isn't within striking distance. And patience compounds only on honest metrics; a gamed metric compounded nightly is just a slower way to be wrong.

## Method cards used
object-as-data, small-data, evaluator-first — drawn at random (shell `shuf`) from the kit's method-card list on 2026-10-15; the random seeds exist so this charter doesn't pile onto the same famous problems as everyone else's. Machine: 2 cores, 7 GB RAM, no GPU; effort light (~1h/run).
