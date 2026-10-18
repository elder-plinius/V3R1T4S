context: subagent
confirmed_scope: At the recorded live survey, claim/scheme.json is an exact integer ternary SLP for (2,5,5) with 40 active products and 148 binary additions/subtractions, matching Sedoglavic's listed rank 40 and strictly beating Perminov's minimum reduced count 153 and matmulcatalog's listed unshared count 256, while Lille cites no reduced-complexity variant for this format.

The literal binding criterion passes for this one submitted object, SHA-256 `fb2744d037444d6e5f84f56628cf97a01ad2650e374421fbe4961bfafefd7ca2`. This is a finite source-relative comparison, not a proof that 148 is optimal or below every construction anywhere.

I reviewed only the submitted `claim/` material and independently fetched primary sources. I did not consult other panel findings, a root verdict, a charter, or local previous runs or attempts. Public claim-identifier checks below were used only for the single-claim condition; other public submissions' verdicts were not evidence for this decision.

Independent exact check: `criterion-code/check.py` expands every sequential sparse form into an integer coefficient vector, checks legal indices before every fresh definition, and rejects repeated indices and all local coefficients except integer ±1. It forms the full bilinear tensor and checks all 10 × 25 × 10 = 2,500 coefficients against ordinary full matrix multiplication. A and B inputs use row-major order; output index `2*j+i` is C[i,j]. Every coefficient agrees over Z, so this checks every integer input pair, not merely sampled evaluations or arithmetic modulo a prime. Expanded U, V, and W coefficients also remain in {-1,0,1}; there is no hidden change to a non-ternary coefficient class.

The count includes every fresh and final form: U has 31 fresh additions and zero final additions; V has 11 fresh additions and 44 final additions; W has 62 fresh additions and zero final additions. Total: **148**. Each k-term form can be evaluated by k−1 binary additions/subtractions, with unary signs and aliases free. No other scalar multiplication occurs. All fresh definitions are reachable; all 40 multiplication inputs are nonzero and all 40 products affect an output. No two bilinear products are equal or opposite. The declared 40 products therefore cannot be attributed to dead padding. The program does not lower the listed rank and is an addition target.

The fresh public GET survey ran **2026-10-14 11:59:21.600922Z–12:03:38.095043Z**. Every completed primary GET returned 200; raw bodies, headers, times, statuses, and SHA-256 receipts are preserved in `criterion-code/`. The first sandbox Lille request failed at DNS resolution before receiving HTTP; the normal authorized network path then made the successful GET. No genuine HTTP denial, rate limit, service error, or challenge was retried or bypassed.

| Binding source | Current evidence | Consequence |
| --- | --- | --- |
| [Sedoglavic fmm_sota.json](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | Exact format [2,5,5] has rank 40. | Rank equality and max dimension 5 satisfy the format/rank conditions. |
| [Perminov live recursive tree](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1) | Tree is explicitly untruncated; scanning all cr filenames, including dimension permutations, finds exactly one format/rank match: `schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json`. | Minimum cr is 153, not an arbitrarily selected directory entry. |
| [Perminov matching reduced scheme](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json) | The independent checker verifies this source object exactly and counts U34 + V55 + W64 = 153 under the same convention. | 148 < 153, a strict five-addition improvement; no tie. |
| [Perminov reduced_known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json) | `2x5x5-40` lists Z313 and Z2 218. | Z313 is a weaker applicable bound; the binary-field record is not substituted for an integer result. |
| [Perminov README](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md), [CHANGELOG](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md) | README defines the sequential fresh-variable format and lists rank 40 for 2x5x5; neither publishes a lower target addition count. | Neither supplies an omitted lower binding record. |
| [Lille 2x5x5 page](https://fmm.univ-lille.fr/2x5x5.html) and its tensor/LRP/raw encodings | Page gives rank 40, credits Hopcroft–Kerr, and cites no complexity variant. `lille_check.py` verifies its linked ternary tensor exactly and independently counts 56 + 66 + 86 = 208 unshared additions; linked LRP has the same count. | No cited lower reduced-complexity count is omitted. 208 is an encoding count, not a theorem about the minimum reduced cost. |
| [matmulcatalog COVERAGE.md](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md) | Format 2,5,5 lists rank 40 and adds +256; the file defines adds as nz(U)+nz(V)+nz(W)−2r−n·p. | 148 < 256 satisfies this explicit binding column; 256 is unshared counting and must not be described as a reduced record. |

Additional lower-construction check: the live Perminov tree's `schemes/known/fmm_add_reduction/Moosbauer-255-40-mod0.m` and `.exp` were fetched once. They encode 40 products with coefficients from {-3,-2,-1,0,1,2,3}, do not give a reduced SLP or lower reduced cost, and do not supply a ternary 148-or-lower counterexample. Lille's actual linked encoding is ternary, so the non-ternary Lille exception is unnecessary here.

Single-claim check: both pages of live open V3R1T4S PRs (104 entries, the final page has no next link) have no matching exact-format title/body identifier; narrowly scoped closed-PR exact-format search and all-PR exact candidate SHA-256 search each return `total_count: 0`, `incomplete_results: false`. This establishes no observed matching public submission in those checks, not universal uniqueness under arbitrary equivalent representations. This review evaluates one object and performs no outward submission.

No statistical null, seeds, or multiple-testing correction is required for the mathematical verification: it exhaustively proves a deterministic integer coefficient identity. The record comparison is a current public-source survey, not a statistical inference. The integer and ternary domain, counting convention, output order, active-product count, strict direction, full-directory minimum, rank equality, and additional binding source comparisons are all checked.

Reproduce the exact object checks without network:

```sh
python3 panel/criterion-code/check.py
python3 panel/criterion-code/check.py panel/criterion-code/perminov-2x5x5-cr153.json
python3 panel/criterion-code/lille_check.py
```

Supporting results: `criterion-code/check-result.json`, `baseline-check-result.json`, `lille-check-result.json`, and `comparison-result.json`.

pass: true
