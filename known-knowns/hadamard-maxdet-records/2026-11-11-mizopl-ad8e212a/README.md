# Hadamard Maximal Determinant (`hadamard-maxdet-records`): 8 New Record Determinants for Orders `n = 81, 89, 93, 97, 101, 105, 109, 117`

## What

Eight explicit n x n {+1,-1} matrices in object/M081.txt through object/M117.txt and object/hadamard_maxdet_8_records.json (sha256 ad8e212ac8397998c64702e7a9837dd048bf833df109520d01d713111b13b190) establish new record normalized determinants D_norm = |det(X)| / 2^(n-1) for orders n = 81 (200 * 20^39 vs 196 * 20^39, +2.0408%), n = 89 (226 * 22^43 vs 220 * 22^43, +2.7273%), n = 93 (243 * 23^45 vs 239 * 23^45, +1.6736%), n = 97 (264 * 24^47 vs 256 * 24^47, +3.1250%), n = 101 (7626 * 25^48 vs 7110 * 25^48, +7.2574%), n = 105 (7413 * 26^50 vs Rokicki's 2005 record, +8.0164%), n = 109 (309 * 27^53, +19.8565% above Rokicki's 2005 record and +6.1856% above merged V3R1T4S PR #155 at 291 * 27^53), and n = 117 (335 * 29^57 vs Rokicki's 2005 record, +5.3179%), each verified from scratch by fraction-free Bareiss elimination, 14-prime Chinese Remainder Theorem modular elimination, and SymPy Bareiss cross-check to lie strictly below Barba's n = 1 (mod 4) upper bound (as verified by our local 3-skeptic review panel), without claiming optimality on any of the eight orders.

## Check it yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Dependencies:** Python 3.8+ standard library only (zero external packages required; if `sympy` is installed, `verify.py` automatically runs a third determinant cross-check via `sympy.Matrix.det(method="bareiss")`).
- **Runtime:** ~0.6s (standard library Bareiss + 14-prime CRT) or ~1.2s (with SymPy Bareiss enabled) on a laptop CPU.
- **Expected final line:** `PASS` (and `python3 verify-it-yourself/verify.py --corrupt` exits `1` with final line `FAIL`).

## Compared to

All normalized values report `D_norm = |det(X)| / 2^(n-1)` (`OEIS A003432` scaling) for `X in {+1, -1}^(n x n)`, compared against Barba's (1933) `n = 1 (mod 4)` upper bound `sqrt(2n - 1) * (n - 1)^((n - 1)/2) / 2^(n - 1)`. Full URL, fetch-timestamp, and `sha256` snapshot metadata are recorded in `the-record-we-beat/README.md`.

| Order `n` | New `D_norm` (`|det(X)| / 2^(n-1)`) | Prior Record & Baseline Holder(s) | Gain vs. Literature | Barba Ratio `R` | Matrix File |
|---:|---|---|---:|---:|---|
| `81` | `200 * 20^39` (`1.0995e+53`) | `196 * 20^39` (N. Farmakis & S. Kounias (1987)) | `+2.0408%` | `0.788110` | `object/M081.txt` |
| `89` | `226 * 22^43` (`1.1975e+60`) | `220 * 22^43` (N. Farmakis & S. Kounias (1987)) | `+2.7273%` | `0.772145` | `object/M089.txt` |
| `93` | `243 * 23^45` (`4.6064e+63`) | `239 * 23^45` (W. P. Orrick & B. Solomon (2003)) | `+1.6736%` | `0.776770` | `object/M093.txt` |
| `97` | `264 * 24^47` (`1.9567e+67`) | `256 * 24^47` (B. Solomon & W. P. Orrick (2003)) | `+3.1250%` | `0.791797` | `object/M097.txt` |
| `101` | `7626 * 25^48` (`9.6254e+70`) | `7110 * 25^48` (W. P. Orrick & B. Solomon (2003)) | `+7.2574%` | `0.860635` | `object/M101.txt` |
| `105` | `7413 * 26^50` (`4.1559e+74`) | `3.8474e+74` (T. Rokicki (2005); open `V3R1T4S PR #539`: `7202 * 26^50` (`+2.9297%`)) | `+8.0164%` | `0.758532` | `object/M105.txt` |
| `109` | `309 * 27^53` (`2.2503e+78`) | `1.8775e+78` (T. Rokicki (2005); merged `V3R1T4S PR #155`: `291 * 27^53` (`+6.1856%`); open `PR #540`: `297 * 27^53` (`+4.0404%`)) | `+19.8565%` | `0.776900` | `object/M109.txt` |
| `117` | `335 * 29^57` (`7.6161e+85`) | `7.2315e+85` (T. Rokicki (2005); open `V3R1T4S PR #541`: `325 * 29^57` (`+3.0769%`)) | `+5.3179%` | `0.756779` | `object/M117.txt` |

Exact full-integer decimal expansions of `D_norm` and `|det(X)|` are stored in `INDEX.csv` and `object/hadamard_maxdet_8_records.json` and checked digit-for-digit by `verify-it-yourself/verify.py`.

## Not claimed

- **No optimality claim:** All eight determinants have Barba ratios in `[0.7568, 0.8606]` (`2n - 1` is non-square for all eight orders), so none is claimed maximal.
- **Other residue classes and orders:** No new strict record above the live table is claimed here for `n = 2 (mod 4)` or `n = 3 (mod 4)` (including the six orders `51, 103, 107, 111, 115, 119` improved in `arXiv:2608.22518v3`).
- **Peer review:** Not peer-reviewed; verified mechanically by `verify-it-yourself/verify.py` and audited by our local three-skeptic panel (`panel/`).

## Credits

- **W. P. Orrick and B. Solomon**, *The Hadamard Maximal Determinant Problem* (archived MaxDet catalog, 2002-2012) and *Large-determinant sign matrices of order 4k+1*, *Discrete Math.* 307 (2007), 226-236 (`arXiv:math/0311292`).
- **N. Farmakis and S. Kounias**, *The excess of Hadamard matrices and optimal designs*, *Discrete Math.* 67 (1987), 165-176 (prior records for `n = 81, 89`).
- **T. Rokicki**, *New determinant records from circulant pairs* (April 2005, archived in Orrick's MaxDet catalog; prior literature records for `n = 105, 109, 117`).
- **G. Butbaia et al.**, *Reinforcement learning for the Hadamard maximal determinant problem*, `arXiv:2608.22518v3` (Oct 2026) and `Math-AI-Caltech/hadamard-maxdet`.
- **Prior `V3R1T4S` contributor `@calgulbenkian`**, merged `PR #155` (`291 * 27^53` on `n = 109`) and open PRs `#539, #540, #541`.
- **Construction & verification:** **we\*** + `@mizopl`.
