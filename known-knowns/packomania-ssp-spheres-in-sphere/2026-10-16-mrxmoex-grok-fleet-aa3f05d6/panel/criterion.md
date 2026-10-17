# Criterion skeptic: ssp radius.txt erratum

Live fetch 2026-10-16T16:57Z (18:57 CEST), all HTTP 200, saved to panel-scripts/criterion/live/:
- https://packomania.com/ssp/txt/radius.txt  sha256 9a4d7b62c61ac3aad69c11f238c76707c51ee824f163bee44a2b345a04b39fe3
- https://packomania.com/ssp/ssp.html  sha256 e2d84d0d6cfd66870b940bfc068ba3e0827a51ea407b365473b869db828e77fd
- https://packomania.com/ssp/txt/ssp_coords.tar.gz  sha256 c077c79ef6c767e7d14d73942beed2f4be1bd15286073ef1548475f230c3e5f3
radius.txt and tarball hashes match the package README.

Script: panel-scripts/criterion/check_criterion.py (Decimal prec 50, own code), output in panel-scripts/criterion/run_output.txt, prints PASS.

## Findings
- radius.txt 1153 rows, ssp.html 111 rows. Of the shared rows, 90 have radius.txt above ssp.html by more than 1e-9: N=1055..50000, smallest N 1055. Zero rows fall in the tie band 0<|d|<=1e-9, so the threshold excludes nothing here. Zero rows have radius.txt below ssp.html.
- Exact r* from coordinates (min of 1-|c_i| and half the minimum pair distance, grid search, Decimal 50) for 14 rows: extremes 1055, 1601, 20000, 50000 plus seeded random 1253, 2000, 2587, 3463, 5017, 5481, 5979, 6000, 6363, 40000. In every one, |ssp.html - r*| <= 1.75e-12 (inside 2.8e-12) and radius.txt - r* > 1e-9.
- Gap range: min 6.093e-9 at N=1601, max 6.476e-5 at N=20000. Both match the claim.
- Limits: coordinates were recomputed for 14 of the 90 rows only. For the other 76, "table equals coordinates" relies on the package plus agreement in the sample. radius.txt rows missing from ssp.html (about 1040) were not checked against coordinates. The claim is limited to the 90 html rows, so this does not affect it.
- The framing holds: a radius.txt erratum where the table and the coordinates agree, with no record and no claim about cause.

confirmed_scope: Live Packomania ssp radius.txt (sha256 9a4d7b62c61ac3aad69c11f238c76707c51ee824f163bee44a2b345a04b39fe3) exceeds ssp.html (sha256 e2d84d0d6cfd66870b940bfc068ba3e0827a51ea407b365473b869db828e77fd) by more than 1e-9 in exactly 90 rows, N=1055..50000, with gaps from 6.09e-9 (N=1601) to 6.48e-5 (N=20000), no ties and no row below; in all 14 rows recomputed at 50 digits from ssp_coords.tar.gz (sha256 c077c79ef6c767e7d14d73942beed2f4be1bd15286073ef1548475f230c3e5f3), ssp.html equals coordinate r* within 1.75e-12.

verdict: PASS
context: executor subagent, fresh context
pass: true
