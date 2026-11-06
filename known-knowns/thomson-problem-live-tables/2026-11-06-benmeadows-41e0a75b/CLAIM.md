# Claim: thomson-problem-live-tables, N = 436

Object: `object/thomson-436.txt` (sha256 41e0a75b4b6d5bbb4a7c8f3d951ab712da44e958b69641eb2ac2c2da3967f979), 436 lines,
one point per line as `x,y,z` with 30 significant digits.

Claimed: these 436 points, normalised to the unit sphere, have Coulomb energy E = sum_{i<j} 1/|x_i - x_j| of about
90020.6812680730, lower than the best live table value for N = 436 (Wayne Deeter's table, 90020.71608562) by about
0.0348; the configuration is a strict local minimum, and a different basin from the posted table configurations.

Success criterion (V3R1T4S bank target thomson-problem-live-tables, quoted verbatim):

> Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER (direction: min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/, N = 4..524), CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the Wikipedia table and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6 in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD xyz/<N>.xyz, Riesz dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6. N > 1500 (Riesz rows up to 9913) cannot be Hessian-certified in under an hour and is partial win p3 only.

The bank's verification method: (1) curl all live tables and take the minimum for N. (2) Normalize the claimed points
in mpmath (mp.dps = 30), compute E* exactly. (3) Tangent-space Newton in mpmath until gradient norm < 1e-20; confirm E*
changes by < 1e-12; build the 3N x 3N Hessian in double, project out rotations, assert 2N-3 positive eigenvalues.
(4) Download every table's point file for N and polish identically; assert each E_table_polished - E* >= 1e-6.
(5) Assert E_table_min - E* >= 1e-6. Report all energies to 12 digits.

Live sources (fetch them yourself):
- https://deetour.net/oppp/thomson/ and its point file https://deetour.net/oppp/thomson/e.436.txt
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html, https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html,
  CCD point file https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/436.xyz
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html (Riesz s = 1)
- https://en.wikipedia.org/wiki/Thomson_problem
- Prior claims: open, merged and closed pull requests at https://github.com/elder-plinius/V3R1T4S with
  "thomson" in the title, and TROPHY_CASE.md on its main branch.
