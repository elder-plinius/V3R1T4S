# PREREG (frozen 2026-10-21 17:43:43 UTC)
code: code/nt.py sha256 7503acd1ca82aeccfe2da60b77a3e0d45cbbd6284c154d8f4d86be6702bd9e1c (final; any change => PREREG v2 before measuring).
Disclosure: before this freeze a premature run of fold_audit printed results for H2AFZ, H3K27ac, H3K27me3 (public benchmark.csv only) and was killed;
  outputs deleted; the full audit is rerun after the freeze with this code. Two 1-epoch SMOKE trainings (no test read) checked determinism.
data: HF revised NT tasks rev 851f9946..., sha256 data/nt_sha256.txt; benchmark.csv sha256 a93c1e72...
criterion: verbatim in target.md (not attacked; already met publicly, scout.md). Partial win targeted: p3 (fold-variance audit of histone tasks).
precision/determinism: fp32 training and inference, torch.use_deterministic_algorithms(True), seeds = fold index 0-9; weights saved per model.
lens A (fold_audit): for each of the 18 tasks, every model pair: exact paired sign-flip test over 10 folds (1024 patterns), two-sided.
lens B (small CNN noise floor): 238,722-param CNN, 10 histone tasks x 10 train/val folds (KFold seed 2026), 25 epochs, select best val MCC,
  test read once per model, inference = mean of forward and reverse-complement probabilities, threshold 0.5.
lens C (kmer_audit): chromosome overlap; exact (both strands) duplicates; fraction of each test sequence's canonical 31-mers present in train;
  k-mer vote memorisation baseline MCC (no learning).
significance threshold per task (meaningful difference): a gap between two benchmark entries counts as meaningful only if
  (i) paired sign-flip p < 0.05 over folds AND (ii) |gap| > 2 x SE_test, SE_test = bootstrap sd (1000) of MCC of the CNN fold-0 test predictions.
null (null_test: required): label permutation 1000 controls per CNN model; sign-flip null (1024) for every pair in lens A.
speed: real inference (fp32, forward+RC) on H3K9me3 test, GPU and CPU 1/all threads (speed only reported, not claimed).
decision: PROMISING only for p3 if it is literal and not already published (to check); otherwise audit only.
null_test: required

## PREREG v2 (2026-10-21 17:57:45 UTC, before re-running lens A)
nt.fold_audit crashed on H3K9me3 (benchmark.csv rows with 9/12/13/14 fold values: HyenaDNA-1KB/-32KB). Lens A now uses
code/fold_audit_v2.py sha256 2de549f31a9a05b4fb3d075369e3c9a9f7c58ac407b06f3f6b0171d6613c8772: same test, rows without exactly 10 folds excluded and listed.
The 8 tasks printed before the crash (H2AFZ..H3K9ac) were seen. nt.py is unchanged (7503acd1...), so the GPU lens and kmer audit are unaffected.
