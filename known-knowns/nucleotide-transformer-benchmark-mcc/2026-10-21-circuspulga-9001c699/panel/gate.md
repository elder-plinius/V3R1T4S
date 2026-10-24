# Honesty gate (kit RUN.md step 7): run 2026-10-21-1738, nucleotide-transformer-benchmark-mcc, partial win p3

status: CONFIRMED_PARTIAL
confirmed_scope: On the 10 histone tasks of benchmark.csv (sha256 a93c1e72...), an exact paired sign-flip test over the 10 per-fold MCC values of every pair of entries with exactly 10 folds (3 HyenaDNA rows excluded) reproduces claim/objects/FOLD_AUDIT.json exactly and shows the best entry is not significantly above the second (p >= 0.05) on H2AFZ, H3K36me3, H3K4me1, H3K4me3, H3K9me3 and H4K20me1; the SE_test-based threshold is not confirmed.

Caveats bound to this scope (from the three panel files; they narrow, never widen):
- The 10 folds share one test set and overlapping training data; the sign-flip test treats fold differences as exchangeable, so p-values are
  anti-conservative. The six "not significant" verdicts are therefore conservative in direction; no "significant" verdict is part of the scope.
- No multiple-comparison correction was applied (none is needed for the confirmed "not significant" statements).
- benchmark.csv rows without exactly 10 folds (3 HyenaDNA rows on histone tasks) are excluded.
- The SE_test threshold (0.030-0.066) is NOT confirmed (it rests on the author's CNN), although REPRODUCE found it robust to bootstrap seeds.
- Precision label: PREREG said fp32, but REPRODUCE found the GPU scores match TF32 (PyTorch default cuDNN TF32). This affects only the CNN lens, not the confirmed scope.
- Zeng et al. 2026, bioRxiv 10.64898/2026.05.17.724301: main text read 2026-10-21T19:22:24Z (HTTP 200) and supplement media-1.docx read 2026-10-21T19:24:22Z (HTTP 200, sha256 f60950d0e909c835751c4e13c77a4be08a114a759f31c99079088d5aa786cf9e). Neither mentions Nucleotide Transformer, Dalla-Torre, DNABERT, Enformer, HyenaDNA, histone marks or any genomic leaderboard. Neither lists the 184 meta-analysed studies, so whether the NT paper is among them is unverified, but no NT comparison is re-tested. The paper classes paired permutation tests over CV folds as invalid (anti-conservative), which is the caveat above: it weakens significance claims, not the confirmed non-significance statements. No change to the scope.

Panel read by the main session:
- reproduce.md: pass: true (FOLD_AUDIT reproduced exactly; CNN retraining bit-identical; TF32 label issue noted).
- novelty.md: pass: true (status source re-read 2026-10-21T18:23:59Z, unchanged; no published per-task paired fold test found; search not exhaustive; one PENDING source).
- criterion.md: pass: true for the scope above only.
Gate: no downgrade trigger applies to the confirmed scope. The table fetch is under 6 h old. Novelty hedges only about a non-exhaustive search plus one PENDING source, recorded above.
