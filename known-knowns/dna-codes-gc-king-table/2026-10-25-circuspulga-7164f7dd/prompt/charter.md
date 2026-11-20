# Research charter v2 (2026-10-17, approved by the human)

## Thesis
Two machines, two tempers. A patient CPU box keeps exact combinatorial searches running on biological codes. A single
24 GB consumer GPU, used in short attended sessions, trains small, carefully controlled models on public
disease-research benchmarks whose published numbers come from plain baselines. The edge is discipline, not scale:
frozen protocols, several seeds, honest nulls, and small models where big ones are the default. Exploratory picks.

## Quarries
1. **id: ptbxl-ecg-macro-auc-fold10**. Question: a model trained on PTB-XL folds 1-8 and selected on fold 9 whose
   fold-10 macro-AUC on one benchmark label set (first: form statements, the least saturated) beats the README maximum
   and every literature value by >= 0.003 as a 5-seed mean. Shape: record (frozen predictions, judged by the
   benchmark's own evaluation code). Defined: Wagner et al., Scientific Data 2020; Strodthoff et al., IEEE JBHI 2021
   (arXiv:2004.13701); Mehari and Strodthoff, arXiv:2211.07579; bank entry of this id. Data: PhysioNet, open access,
   no registration; 100 Hz version under 1 GB. Status to confirm first: README table and post-2022 form-statement
   results. Why us: 1D CNN / state-space models train in minutes per seed on one GPU, so 5 seeds per config are cheap.
   Compute: GPU. Weight 5. Wild: no.
2. **id: pcam-patchcamelyon-from-scratch-accuracy**. Question: a randomly initialised model trained on the official
   PCam train split, selected on validation only, whose test accuracy beats 89.8% (and any from-scratch literature
   value) by >= 0.5 points, AUC >= 0.963, 3-seed mean. Shape: record. Defined: Veeling et al., MICCAI 2018
   (arXiv:1806.03962), github.com/basveeling/pcam README; bank entry of this id. Data: Zenodo record 2546921, plain
   download, roughly 7-8 GB of HDF5 (size to confirm). Status to confirm first: README table and recent from-scratch
   papers. Why us: the from-scratch plateau near 90% is a recipe-and-regularisation question that one GPU can probe
   with many controlled seeds. Compute: GPU. Weight 4. Wild: no.
3. **id: nih-thin-smear-malaria-patient-grouped-sensitivity**. Question: under BOTH the published image-level split
   and a patient-grouped split derived from the filename patient codes, report sensitivity at matched specificity;
   beat the published 97.05% under (a) with a bootstrap interval excluding zero, and report the (b) drop. Shape: record
   plus a released grouped split. Defined: Dehbi and Hamou, Frontiers in Medicine 2026 (PMC13553222); NIH/NLM cell
   image release; bank entry of this id. Data: cell_images.zip, 353 MB, plain request. Status to confirm first: the
   published numbers and any patient-grouped evaluation since. Why us: the honest contribution (the grouped split, p1)
   is cheap and the model is small; one GPU covers many seeds. Compute: GPU (CPU possible). Weight 3. Wild: no.
   Note: diagnostic-image classification only; no work on the parasite itself.
4. **id: medmnist-pathmnist-breastmnist-accuracy**. Question: beat the best listed test ACC on PathMNIST (28x28 first)
   or BreastMNIST under the official splits and Evaluator, and the best literature value. Shape: record. Defined:
   Yang et al., MedMNIST v2, Scientific Data 2023; medmnist.com table; bank entry of this id. Data: Zenodo record
   10519652, CC BY, npz; 28x28 subsets are small (hundreds of MB), 224x224 larger (to confirm). Status to confirm
   first: official table plus MedMNIST+ and later papers (novelty is the hard part). Why us: partial wins p1 (tiny model)
   and p3 (5-seed variance audit of the official table) fit light runs. Compute: GPU. Weight 3. Wild: no.
5. **id: nucleotide-transformer-benchmark-mcc**. Question: a model trained only on one chromatin task's training split
   (first: H3K9me3, best ten-fold mean MCC 0.4807 as listed 2026-10-15) whose ten-fold mean MCC beats the leaderboard
   by >= 0.02, with fold-wise values and a paired comparison. Shape: record. Defined: Dalla-Torre et al., Nature Methods
   2024 (PMC11810778); leaderboard benchmark.csv in the InstaDeepAI nucleotide_transformer_benchmark space; bank entry
   of this id. Data: Hugging Face hub, no registration, short sequences (under 1 GB, to confirm). Status to confirm
   first: benchmark.csv rows for the task. Why us: partial win p1 asks for a model under 100M parameters, the size a
   24 GB card trains comfortably across ten folds. Compute: GPU. Weight 3. Wild: no.
6. **id: hest-bench-cancer-expression-from-morphology**. Question: for one HEST-Benchmark task (first: one of the
   weakest, READ, CCRCC or LYMPH_IDC), per-spot predictions of the 50 benchmark genes whose mean Pearson beats the live
   README maximum by >= 0.015 over 5 seeds (> 2x std). Shape: record. Defined: Jaume et al., HEST-1k, NeurIPS 2024;
   github.com/mahmoodlab/HEST README table; bank entry of this id. Data: Hugging Face MahmoodLab/hest-bench, ungated
   per the bank, 0.5-2.5 GB per task; precomputed CTransPath embeddings included. Blocker to check: most listed
   pathology foundation-model encoders are gated behind registration; this quarry uses only ungated inputs (shipped
   embeddings, an ImageNet encoder, or own features) unless the human registers. Status to confirm first: live README
   table. Why us: the bank notes the head and spatial statistics, not the encoder, may hold the remaining signal; partial
   win p2 (non-foundation-model pipeline) fits. Compute: GPU (feature extraction) + CPU heads. Weight 2. Wild: no.
7. **id: dna-codes-gc-king-table**. Question: for an unmarked (n,d) in the Gaborit-King A_4^GC(n,d,w) table, a
   constant-GC code with pairwise Hamming distance >= d larger than the entry (first: tie a 'v' cell, partial win
   tie-unmarked-mid, e.g. (14,11)=17, (15,12)=15, (18,14)=20). Shape: record. Defined: King, Electron. J. Combin. 10
   (2003) R33 and the live table; bank entry of this id. Status to confirm first: post-2010 literature (arXiv:1903.03535,
   arXiv:2108.02033, arXiv:2403.11551). Why us: the box already has a tested checker and a dossier; it keeps running on
   days without a GPU session. Compute: CPU (box). Weight 3. Wild: no.
8. **id: burnt-pancake-even-n-exact-flips**. Question: for an undecided even n in OEIS A078942, a sorting sequence of
   exactly 3n/2 + 1 flips for I_n, or an exhaustive certificate that none exists. Shape: existence or bound. Defined:
   OEIS A078942, A078941, arXiv:2601.09447; bank entry of this id. Status to confirm first: which even n are decided.
   Why us: symmetry-reduced search on the box, day after day; partial win p1 (re-verify n = 24, 26) first. Compute:
   CPU (box), possibly GPU-parallel BFS later. Weight 1. Wild: yes.

## Lenses
- **key: protocol-freeze**. Title: Freeze, then train. Before any training run, write the split files (with sha256),
  the selection split, the metric code, the seed list (at least 3 seeds; 5 where the criterion says so), the
  hyperparameter grid and the stopping rule into PREREG.md. Train only after the freeze. Dead when a result is only
  reachable by touching the test split for anything (early stopping, thresholds, seeds, ensembles). Skeptic: no.
- **key: modern-recipe**. Title: Old baselines, modern recipe. Take the strongest plain architecture from the published
  table and retrain it with a careful current recipe (cosine schedule, label smoothing, mixup/cutmix or signal
  augmentations, EMA weights, test-free calibration). Dead when 3 seeds of the tuned recipe sit inside the published
  value's seed noise. Skeptic: no.
- **key: small-and-fast**. Title: Smallest model that matches. Hunt the compute-efficiency partial wins: under 100k-1M
  parameters, short training, many seeds. A small model that matches a big one with a tight seed spread is a result;
  a large model that wins by one lucky seed is not. Dead when the small model trails by more than 2x seed std after
  the full grid. Skeptic: no.
- **key: far-import**. Title: Borrow from a distant field. Import methods from signal processing (wavelet or
  state-space front ends for ECG), coding theory (structured codes for the DNA quarry), or spatial statistics
  (neighbourhood smoothing that respects patient splits for HEST). Dead when the import does no better than the plain
  baseline on the same frozen protocol. Skeptic: no.
- **key: evaluator-first**. Title: Fast exact evaluator, then search (box quarries). Bit-packed incremental evaluators
  and plain local search at scale for codes and flips. Dead when a full budget stalls below the published value with
  no improving trend. Skeptic: no.
- **key: null-and-leak-auditor**. Title: Is the gain real, and is the benchmark clean? Run the null: at least 400
  label-permutation controls (permute test labels against the frozen predictions; for a training claim, also at least
  one full retrain on permuted training labels) plus a paired bootstrap of the new model against the reproduced
  baseline. Audit leakage: duplicate or near-duplicate images across splits, patient overlap, source-dataset
  pretraining overlap, test-tuned thresholds. Rerun the published baseline in the same environment first. Dead (for
  this lens) when the quarry survives every check; the survival goes into the brief. Skeptic: yes.

## Scout voice
Read each table for its comparison class first: from-scratch vs pretrained, external data vs none, resolution,
label set, split protocol. A number from another class is not a record to beat. Check the newest papers on the same
protocol before the table itself, and record exact dataset versions and sha256.

## Attacker voice
Patient and exact. Reproduce the baseline before improving it. Prefer many cheap, frozen, seeded runs over one large
run. Write down every configuration tried, including the failures.

## Heuristics
1. Reproduce the published baseline in the same environment before claiming any gain.
2. Protocol, splits, seeds and metric code are frozen in PREREG.md before any model selection.
3. Report the seed mean and std; never the best seed.
4. The test split is opened once, at the end, for the frozen model.
5. One task and one cell per claim; ties are logged as ties.
6. Compare only within the published comparison class.
7. Small models and short schedules first; scale only a survivor.
8. Checkpoint every few minutes so the next session can resume.

## Kill criteria
1. The live table or a later paper already reaches the target in the same comparison class.
2. The gain is inside 2x the seed std, or fails the paired bootstrap against the reproduced baseline.
3. The real result does not beat every one of at least 400 label-permutation controls.
4. Any test-split use before the final frozen evaluation, or any leakage found by the auditor.
5. Data that requires registration, credentials or a signed agreement the human has not personally completed.
6. Any drift toward pathogens, toxins, immune evasion, transmissibility, antimicrobial-resistance genotypes or epitope
   prediction, or toward clinical or treatment interpretation of any result: drop it.

## Self-critique
Medical-image and ECG benchmarks are crowded; the official tables are old and the literature has often moved past them,
so novelty checks will kill most apparent wins. Seed noise on small test sets (BreastMNIST, CODE-sized sets) can
masquerade as progress. GPU sessions need the human present, so the GPU quarries will move more slowly than the
weights suggest. Label-permutation nulls show the model beats chance, not that it beats the record; the paired
bootstrap and seed spread carry that burden.

## Method cards used
evaluator-first, far-import, smaller-first (as small-and-fast), drop-assumption (as modern-recipe: drop the assumption
that the published recipe was tuned), object-as-data (as null-and-leak-auditor). Chosen deliberately, not drawn at
random.

## Changelog (v1 -> v2)
- Added GPU quarries: ptbxl-ecg-macro-auc-fold10 (5), pcam-patchcamelyon-from-scratch-accuracy (4),
  nih-thin-smear-malaria-patient-grouped-sensitivity (3), medmnist-pathmnist-breastmnist-accuracy (3),
  nucleotide-transformer-benchmark-mcc (3), hest-bench-cancer-expression-from-morphology (2).
- Kept: dna-codes-gc-king-table (weight 5 -> 3), burnt-pancake-even-n-exact-flips (wild, weight 2 -> 1).
- Dropped to stay within 8 quarries: dna-codes-gc-rc-king-table (same evaluator as quarry 7), hp-lattice-folding,
  minimizer-density, parsimony-benchmark, pycox-metabric (a CPU disease-research benchmark now covered by GPU ones).
- Lenses: added protocol-freeze, modern-recipe, small-and-fast, null-and-leak-auditor; kept evaluator-first and
  far-import; dropped solver, construct-space, small-cases, contrarian (folded into the auditor).
- Kill criteria rewritten for training: seed std, paired bootstrap, >= 400 label-permutation controls, test-split
  discipline, registration blocker, explicit no-clinical-interpretation rule.
- Dual-use exclusions unchanged.
