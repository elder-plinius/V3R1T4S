# Exact local bound 6104 for the 120 x 120 E8 instance: K_G(8) >= 165/109 proven

## What

For the paper's d=8 E8 instance (120 x 120 matrix 3G-13I, signs and order arbitrary), the local bound max a^T A b is exactly 6104, so Q/L = 9240/6104 = 165/109 is a proven lower bound for K_G(8); this converts the heuristic value to a proven one (partial win p2) and says nothing about K_G(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 10 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Designolle, Vértesi and Pokutta, arXiv:2409.03739v4, table of symmetric instances | d = 8, m = 120 (E8) | lower bound 165/109 (about 1.5138), marked with an asterisk: the solution of the binary problem is heuristic, so the value is only putative | https://arxiv.org/abs/2409.03739 (e-print https://arxiv.org/e-print/2409.03739v4) | 2026-10-19T04:46:13Z (e-print, triage); abstract page also 2026-10-19T05:39:14Z (novelty skeptic) |
| Same paper, table of heuristic bounds | d = 8, 120 x 120 | 1.51376, heuristic (state of the art before the paper: 1.48217) | https://arxiv.org/e-print/2409.03739v4 | 2026-10-19T04:46:13Z |
| Same paper, table of exact bounds | d = 5, 65 x 385 | 1.49339, the largest proven bound for d at least 5, inherited by d = 8 through monotonicity | https://arxiv.org/e-print/2409.03739v4 | 2026-10-19T04:46:13Z |
| Same paper, abstract | d in {4, 7, 8} | the highly symmetric instances can only be solved heuristically | https://arxiv.org/abs/2409.03739 | 2026-10-19T05:39:14Z |
| Supplementary files, Zenodo record 13693164 | d8_n1_120x120.mat | same size (239024 bytes) and md5 (59e20586d208c78d49c73fa9bb99c796) as the object file here, version 0.0.2 of 2024-09-06 | https://zenodo.org/api/records/13693164 | 2026-10-19T05:39:59Z (HTTP 200) |
| arXiv 2609.35399v1 (28 Sep 2026) | d = 8 instance | cites 165/109 = 1.513761 as a candidate ratio; its own bounds are conditional on conjectured binary optima; no proof of 6104 | https://arxiv.org/pdf/2609.35399v1 | 2026-10-19T05:39:14Z (HTTP 200) |

This package: the maximum over sign vectors a, b of a^T A b for A = 3G - 13I (G the Gram matrix of the 120 positive roots of E8) is exactly 6104, and Q = 9240, so K_G(8) >= 9240/6104 = 165/109 = 1.5137614678899083 is proven. Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- Partial win p2 only. What is new is the proof that the local bound is 6104, which turns the paper's heuristic value into a proven one. The number 165/109 is not new: the paper already prints it, as a heuristic value. This is not an improvement of any table and not a new numerical bound; the contributor's gain of 0.0204 over 1.49339 is not what is credited.
- Nothing is claimed about K_G(3) or the main criterion of the target (a K_G(3) lower bound above 1.43670).
- The matrix is the paper authors' own supplementary file (same md5 as the Zenodo record); the contribution is the proof, not the instance. Whether the authors' supplementary data files already contain a certificate that this argument reproduces could not be settled (the panel did not open the Julia data files).
- The upper bound 6104 rests on a symmetry reduction (Weyl-group action, vertices of the root zonotope, vectors in twice the root lattice) written out in `verify-it-yourself/UPPER_BOUND.md`. The shipped checker verifies the 18454 dual certificates in exact integer arithmetic and the lower-bound sign vector directly on the matrix, but it does not re-derive the reduction steps; the panel re-derived them independently (`panel/criterion.md`). The dual vectors were found with floating-point linear programs and are verified exactly. It is one method (a symmetry reduction with dual certificates), not two independent algorithms.
- Newer literature was searched in arXiv only (the 25 newest hits plus one full text); a paper outside those words could already prove this instance.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Sébastien Designolle, Tamás Vértesi and Sebastian Pokutta**, *Better bounds on finite-order Grothendieck constants*, arXiv:2409.03739 (v4, 5 Oct 2026), Phys. Rev. A 113, 022401 (2026), https://arxiv.org/abs/2409.03739: the instance (the 120 x 120 E8 matrix), the heuristic value 165/109 and the table this proof completes. Their supplementary files are on Zenodo, https://doi.org/10.5281/zenodo.13693164; the object file here is theirs, unchanged.
- arXiv:2609.35399 (28 Sep 2026), https://arxiv.org/abs/2609.35399: read to check whether the instance had been proven; it had not.
- Contributor credit: `calgulbenkian`. The proof was found by an AI search agent (Gemini) working for the contributor.
