# Linear Ordered Orthogonal Array `OOA(3^8, 8, F_3, 2, 7)` for MinT Cell `(b=3, T=2, m=8, s=8)`

## What

Explicit linear ordered orthogonal array OOA(3^8, 8, F_3, 2, 7) of depth T = 2, dimension m = 8, s = 8 blocks of 2 columns, and strength k = 7 > T = 2 over F_3 (an 8 x 16 matrix over F_3 verified exhaustively to have rank 7 across all 1,016 left-justified column selections of total weight 7, and dually verified across all 6,560 nonzero codewords of its Euclidean nullspace [(8, 2), 8, 8]-NRT code to have minimum Rosenbloom-Tsfasman weight d_RT = 8), improving on live MinT's constructive linear entry OOA(3^8, 8, F_3, 2, 6) (t = 2, k = 6) for cell (b, T, m, s) = (3, 2, 8, 8) and matching MinT's generalized Rao/Hamming lower bound t >= 1 (k <= 7).

## Check It Yourself

From the package root directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line (`< 1` second on a laptop, Python 3.8+ standard library only):

```text
PASS
```

`verify-it-yourself/check_ooa.py` parses `object/ooa_b3_T2_m8_s8_k7.tsv`, checks a negative corrupted `8 x 16` copy (confirming rejection), recomputes the generalized Rao/Hamming sphere volume `7457 > 3^8 = 6561` ruling out `k = 8` (`t = 0`), verifies `rank(G) = rank(H) = 8` and `G * H^T = 0 (mod 3)`, checks all `1,016` left-justified prefix column selections `(d_1, ..., d_8)` in `{0, 1, 2}^8` with `d_1 + ... + d_8 = 7` by exact modular Gaussian elimination over `F_3`, and checks all `3^8 - 1 = 6,560` nonzero codewords of the dual `[(8, 2), 8, 8]`-NRT code.

## Compared To

- **Table**: MinT ("Advanced" Ordered Orthogonal Array tables, University of Salzburg; database footer `2024-09-05`)
- **Cell**: `b = 3` (`F_3`), depth `T = 2`, dimension `m = 8`, factors `s = 8` (`k > T`, non-digital-net regime)
- **Live Query URL**: `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2` (fetched `2026-11-10T18:30:43Z`, HTTP `200`, SHA-256 `5aed6c5b2410094646d736a48515f8241cf76491caeafc8be5a0719482cb9dcf`)
- **Live Overview Table URL**: `http://mint.sbg.ac.at/table.php?i=x&b=3&col=1&mode=cd&opt=bd&de=2&p=smt&minx=1&maxx=20&miny=0&maxy=15` (fetched `2026-11-10T18:30:44Z`, HTTP `200`, SHA-256 `f9ed86586695a5a120ca499a43d5bd53e99de174806290b493b3739c05473ef8`)
- **MinT Constructive & Linear Value**: `t = 2` (`k = 8 - 2 = 6`), constructed as the dual of an `[(8, 2), 8, 7]`-NRT code via the extended genus-2 algebraic-geometric NRT code `AG_e(2; F, 9P)` over `F_3`.
- **MinT Lower Bound on `t`**: `t >= 1` (`k <= 8 - 1 = 7`), via the generalized Rao / dual Hamming bound `M >= 7457 > 3^8 = 6561`.
- **This Package (`object/ooa_b3_T2_m8_s8_k7.tsv`)**: `t = 1`, `k = 7` (`d_RT = 8`), strictly exceeding `k = 6` and meeting the Rao/Hamming bound `k <= 7`.

## Not Claimed

- No claim is made for other `(b, T, m, s)` cells in MinT, for digital nets (`k <= T`), or for raising any lower bound (`p1`/`p2`).

## Credits

- Contributor: `zerbytheboss` (`@HindsightWise`)
- Compared against and built on definitions from:
  - R. Schürer and W. Ch. Schmid, *MinT — Digital Net and OOA Tables*, University of Salzburg (`http://mint.sbg.ac.at/`).
  - M. Yu. Rosenbloom and M. A. Tsfasman, "Codes for the m-metric," *Problems of Information Transmission* 33(1), 45–52 (1997).
  - M. M. Skriganov, "Coding theory and uniform distributions," *St. Petersburg Math. J.* 13(2), 301–337 (2002).
  - A. G. Castoldi, L. Moura, D. Panario, and B. Stevens, "Ordered Orthogonal Array Construction Using LFSR Sequences," *IEEE Trans. Inf. Theory* 63(2), 1336–1347 (2017) / `arXiv:2208.00333` (2022).
  - X. Wang, C. Li, and Z. Heng, "New Bounds of Linear Matrix Codes for the Rosenbloom-Tsfasman Metric and Optimal Constructions," *IEEE Trans. Inf. Theory* 71(9), 6844–6856 (2025).
