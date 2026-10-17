# REPRODUCE skeptic: ssp radius.txt errata

## Sources (fetched fresh 2026-10-16 ~19:00 CEST from packomania.com/ssp/, HTTP 200, not taken from the package)
- radius.txt sha256 9a4d7b62c61ac3aad69c11f238c76707c51ee824f163bee44a2b345a04b39fe3 (matches claim)
- ssp.html sha256 e2d84d0d6cfd66870b940bfc068ba3e0827a51ea407b365473b869db828e77fd (matches claim)
- ssp_coords.tar.gz sha256 c077c79ef6c767e7d14d73942beed2f4be1bd15286073ef1548475f230c3e5f3 (matches claim)
- (hydra.nat.uni-magdeburg.de mirror unreachable; packomania.com used.)

## Independent check (written from the claim before opening package code)
- Geometry: equal spheres in a unit container sphere (ssp.html: radius of spheres in container sphere, ratio = 1/radius).
- r_coord = min( min_ij |ci-cj|/2 , min_i (1-|ci|) ), from exact rational coordinates plus mpmath dps=50. Pair candidates come from a float cell grid, and the minimum is then taken exactly.
- Script: panel-scripts/reproduce/indep_check.py, raw output panel-scripts/reproduce/indep_check.out.txt, TIE-rule summary panel-scripts/reproduce/summarize.py (prints PASS).
- Note: indep_check.py's own last line prints FAIL. That is because it flags gaps above 1e-12, which catches 6 rounding-level rows (N=70000, 90000, 100000, 100281, 180000, 500000; gap ~1.0-1.4e-12). In those rows ssp.html equals radius.txt, and they are TIE under the panel's 1e-9 rule. Applying that rule to the same output without rerunning (summarize.py):
  - 90 rows with radius.txt above r_coord by more than 1e-9, N = 1055..50000, smallest N 1055
  - min gap 6.093e-9 (N=1601), max gap 6.476e-5 (N=20000)
  - |ssp.html - r_coord| <= 2.78e-12 in all 90 rows
  - 0 rows have radius.txt below the coordinates
- 42 N in radius.txt have no coordinate file in the tarball (1369-1374, 1402-1432 except 1409, 1857-1862). They were not checked. They are not part of the 90 rows and do not affect the claim.

## Package rerun (after my own check)
- verify-it-yourself/run_checks.sh (local tarball with the same sha256): `# rows 90 failed 0`, `PASS` (panel-scripts/reproduce/package_run_checks.out.txt).
- object/ssp_radiustxt_errata.csv: same 90 N as mine. coord_rstar agrees with mine to printed precision (max diff 5.6e-17).

## Findings
Every number in the claim reproduces independently: 90 rows, N 1055..50000, gaps 6.09e-9..6.48e-5, ssp.html equal to the coordinates within 2.8e-12, none below.

verdict: PASS
context: executor subagent, fresh context
pass: true
