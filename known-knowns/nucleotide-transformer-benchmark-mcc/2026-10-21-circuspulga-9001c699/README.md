# NT benchmark histone tasks: most top-rank differences are inside fold noise (partial win p3)

## What
On the 10 histone tasks of benchmark.csv (sha256 a93c1e72...), an exact paired sign-flip test over the 10 per-fold MCC values of every pair of entries with exactly 10 folds (3 HyenaDNA rows excluded) reproduces claim/objects/FOLD_AUDIT.json exactly and shows the best entry is not significantly above the second (p >= 0.05) on H2AFZ, H3K36me3, H3K4me1, H3K4me3, H3K9me3 and H4K20me1; the SE_test-based threshold is not confirmed.

Caveats (from panel/gate.md): folds share one test set, so the sign-flip test is anti-conservative (the "not significant" verdicts are conservative);
no multiple-comparison correction; rows without exactly 10 folds excluded; the SE_test threshold is not confirmed; a CNN precision label said fp32
where the GPU used TF32 (CNN lens only, outside the scope); Zeng et al. 2026 (bioRxiv 10.64898/2026.05.17.724301; main text and supplement read, supplement sha256 f60950d0...) does not mention the NT benchmark and does not list its 184 studies; its point (fold-dependent tests are anti-conservative) is the first caveat above.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` -> last line `PASS` (Python 3 standard library, about 2 seconds on a laptop).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| benchmark.csv | per-fold MCC, 10 histone tasks | e.g. H3K9me3 best 0.4807 vs 0.4750, p = 0.4512 | https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv | 2026-10-21T17:38:54Z |

## Not claimed
No new model or record. Nothing about the SE_test threshold, the CNN, or any disease mechanism. No claim that any ranking difference is significant.

## Credits
Dalla-Torre et al., Nucleotide Transformer (Nature Methods 2024; leaderboard space InstaDeepAI/nucleotide_transformer_benchmark); all models listed in benchmark.csv
(NT, NT-v2, DNABERT-2, Enformer, HyenaDNA); GENERator (arXiv:2502.07272) for literature context. Contributor: circusPulga (V3R1T4S run 2026-10-21-1738).
