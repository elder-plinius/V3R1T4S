# Thomson problem, N = 1382: a configuration below every live table

## What

The 1382-point configuration in claim/A_1382/cand_1382.txt has mpmath energy 926576.0968589705 — 6.174e-3 below the lowest live-table value for N = 1382 (CCD Riesz s=1, 926576.1030330), with tangent gradient 5.8e-32, all 2761 non-rotational Hessian eigenvalues numerically positive (float64 with explicit error bound), and a basin distinct from both posted N = 1382 files — and, separately, the live CCD posted energies for Riesz s=1 N = 3552 (1.50e-5 above its polished coordinates) and Thomson2 N = 550 (9.00e-5 below what its coordinates reach) are not reproduced by their own coordinates (p1).

Note: the table-integrity findings for Riesz s=1 N = 3552 and Thomson2 N = 550 (partial win p1) are mentioned in the panel's scope sentence above, but they are NOT part of this package. They will be submitted separately later. This package contains one object only: the N = 1382 configuration.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only, about 10 seconds on a laptop. It checks the object's sha256, recomputes the energy at 40 digits from the normalized coordinates, checks the 6.17e-3 margin under the table and that the tangent gradient is below 1e-15. The full certificate (Newton to < 1e-20, Hessian eigenvalues, re-polishing the posted files) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD Riesz s=1 (lowest live value) | N = 1382 | 926576.1030330 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T07:28:29Z |
| CCD Thomson2 | N = 1382 | 926576.1175606 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T07:28:28Z |
| Deeter | no N = 1382 row (max 524) | n/a | https://deetour.net/oppp/thomson/ | 2026-10-14T07:28:26Z |
| CCD Thomson | no N = 1382 row (max 972) | n/a | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T07:28:26Z |
| Wikipedia | no N = 1382 row (max 470) | n/a | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T07:28:30Z |
| arXiv 2610.08122 (literature) | N = 1382 | 926576.10303295 | https://arxiv.org/html/2610.08122 | 2026-10-14T07:28:30Z |

The panel's novelty skeptic re-fetched the tables at 08:56Z on 2026-10-14 (see panel/novelty.md). Details in the-record-we-beat/.

## Not claimed

- Not a global minimum: only a lower local minimum than any posted one for N = 1382.
- The Hessian positivity is NUMERICAL (a float64 eigen-solver with an explicit Weyl perturbation bound of 4.2e-8 against a smallest eigenvalue of 8.31), not interval arithmetic.
- No claim about any other N, and nothing here about the N = 3552 or N = 550 findings (separate submissions).
- The margin is 6.17e-3 in absolute energy (about 7e-9 relative), well above the 1e-6 threshold but small.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Wales and co-workers, Cambridge Cluster Database Thomson, Thomson2 and Riesz s=1 tables: https://www-wales.ch.cam.ac.uk/CCD.html (Wales and Ulker 2006; Wales, McKay and Altschuler 2009).
- Wayne Deeter, Thomson table: https://deetour.net/oppp/thomson/
- Wikipedia editors, Thomson problem: https://en.wikipedia.org/wiki/Thomson_problem
- Authors of arXiv 2610.08122: https://arxiv.org/abs/2610.08122
- The search started from the posted CCD Riesz s=1 N = 1382 file (points_1382_1.dat).
- Libraries: NumPy, SciPy, Numba, mpmath, gmpy2/MPFR.
