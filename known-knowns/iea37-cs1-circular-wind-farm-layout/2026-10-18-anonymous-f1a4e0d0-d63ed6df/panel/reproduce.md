# REPRODUCE skeptic verdict: iea37-cs1-opt64 (claim/object/iea37-v3r1t4s-opt64.yaml)

context: subagent (Claude Code Agent tool, fresh context)

## Definition quoted (claim/evaluator/iea37-wflocs-announcement.pdf, via pdftotext)
- "Each wind farm scenario has a fixed circular boundary centered at (0, 0). All turbine (x, y) locations must remain on or within this boundary. No turbine can be less than two rotor diameters from any other turbine."
- "3. 64 turbines, boundary radius of 3,000 m."; table: "Rotor Diameter 130 m" -> minimum spacing 260 m.
- Objective: AEP = sum_{i=1..16} f_i P_i * 8760 hrs/yr.
- "Results will be compared by running the enclosed iea37-aepcalc.py".

Wake model (claim/evaluator/iea37-wakemodel.pdf): Eq.(1) dV/V = (1 - sqrt(1 - CT/(8 sigma_y^2/D^2))) exp(-0.5((yi-yg)/sigma_y)^2) if (xi-xg)>0 else 0; Eq.(2) sigma_y = ky (xi-xg) + D/sqrt(8); CT = 8/9, ky = 0.0324555, D = 130 m; Eq.(3) root-sum-square combination; rotation Psi = -(pi/2 + theta), xw = x cos Psi + y sin Psi, yw = -x sin Psi + y cos Psi; Ve = Vinf(1 - dV_total); Eq.(4) power curve (cut-in 4, rated 9.8, cut-out 25 m/s, 3.35 MW, cubic ramp); Eq.(5)-(6) sum and AEP. Vinf = 9.8 m/s, 16 bins at 22.5 deg with frequencies from claim/evaluator/iea37-windrose.yaml.

## My checker (written before opening claim/evaluator/check_constraints.py; file claim/scratch/mycheck.py)
- Constraints: exhaustive over all 64 hubs and all 2016 pairs; (i) float64 test r^2 <= 9e6 and sqrt <= 3000, d^2 >= 67600 and sqrt >= 260, no tolerance; (ii) exact rational test (Python Fraction of each stored double) of x^2+y^2 <= 3000^2 and dx^2+dy^2 >= 260^2.
- AEP: pure-Python double loops implementing the PDF equations above (no numpy, no code from the author or the official evaluator).
- Validation on the official example claim/evaluator/iea37-ex64.yaml: my AEP 1294974.29770, all 16 bins identical to the bins stored in that file (34909.41061 ... 29213.50027); official evaluator prints 1294974.2977.

## Results for claim/object/iea37-v3r1t4s-opt64.yaml
- My checker: n 64, pairs 2016, rmax 2999.999999000001, rad_ok_float true, rad_ok_exact true (worst hub about 1.0e-6 m inside), min_spacing 567.6913085779893, sp_ok_float true, sp_ok_exact true. 64 distinct points.
- My AEP: 1539447.11737; bins 37719.67961, 35917.62522, 44756.37560, 55672.79472, 98054.40698, 94461.34522, 156074.43970, 189703.73125, 95033.82357, 56851.45827, 60144.72782, 128538.15852, 335406.96844, 67208.82919, 49821.49076, 34081.26253 (identical to the binned values stored in the YAML).
- Official evaluator (unmodified, run from claim/evaluator): last line 1539447.11737, same 16 bins. Run 3 times; stdout sha256 dc80ec6de8ea4b2eac351136ef75e9c492705600b1b9d89dbbeb6ee05a7908eb all three times (deterministic). Python 3.12.4, numpy 2.2.6, PyYAML 6.0.2.
- Author's check_constraints.py (read and run after my checker): "turbines 64 max_radius 2999.999999000001 limit 3000.0 min_spacing 567.6913085779892 limit 260.0 / FEASIBLE" (last-digit difference from mine is hypot vs sqrt rounding, immaterial).
- claim/object/layout64.json: keys x, y, aep; 64+64 coordinates bitwise identical (float.hex) to the YAML; aep 1539447.117368648.

## Table re-score (claim/table/iea37-cs1-results/*opt64.yaml), official evaluator, run twice (output sha256 1ebbb31e...64d4bf both times)
par1 1476689.66268 | par10 1480850.9759 | par11 1484287.26071 | par12 1526474.80248 | par2 1506388.41513 | par3 1455075.60842 | par4 1513311.19361 | par5 1336164.5498 | par6 1364943.00774 | par7 1332883.43284 | par8 1445967.37723 | par9 1422268.71443
All 12 equal the values listed in CLAIM.md. My independent AEP gives the same 12 values to 5 decimals. Max table value 1526474.80248 (par12) < 1539447.11737.
My constraint check on the table: par12 rmax 3000.0041276138 (infeasible, 4.1 mm out, as claimed); par4 rmax 3000.0000000001 (infeasible by ~1e-10 m, as claimed); only par10 is fully feasible (both float and exact).

## Hashes
- claim/object/iea37-v3r1t4s-opt64.yaml d63ed6df76fcbf03297cdb171acda406f597bfc959b1610711dc0d68dd93c851 (matches CLAIM.md)
- claim/evaluator/iea37-aepcalc.py ec2d16f237ed547fff3d44f314126b3889c000954f5a53ec3e14c28e5bc6b535 (matches REPRODUCE.md, and matches the file fetched now from the official GitHub repo cs1-2/iea37-aepcalc.py)
- claim/table/gh_tree.json c3a54a267ffb10a994f309ac609e4e1e572428e554739fa9057b80d92aca7bf3 (matches CLAIM.md's c3a54a26...c7bf3)
- Extra: iea37-windrose.yaml, iea37-335mw.yaml, iea37-ex64.yaml, par4 and par12 table files are byte-identical to the current upstream GitHub copies.

## Mismatches
- Cosmetic only: REPRODUCE.md says check_constraints.py is "20 lines"; it is 11 lines. Does not affect any claimed property or value.
- No mismatch in any claimed number, property, hash or determinism check.
- Scope note: I did not assess novelty beyond the supplied table (literature is for the other skeptics).

pass: true
