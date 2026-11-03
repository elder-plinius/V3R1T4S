Frozen UTC: 2026-11-02T23:30:40Z
Object under test: data/ruin-best.json, copied from runs/2026-11-01-1648/attempts/constructor36/ruin/best.json, SHA256 3ea13ecabb80052105d9713b59cdde25b15e888705c009e315e28ae970fadc30. Coordinates used exactly as stored (full double precision, no rounding). The frozen claim object will be these coordinates byte-identical or re-serialised losslessly; its own hash will be recorded.

Criterion targeted (verbatim, p1):
p1: A feasible 36- or 64-turbine layout with AEP strictly above the best posted non-participant-12 value (SNOPT+WEC: 863676.2993 for 36, 1513311.1936 for 64) by at least 1 MWh, such that under the minimum-total-distance one-to-one matching to the participant-12 layout at least one third of the turbines are more than 50 m from their partner (an independent topology).

Statistic and thresholds:
1. Feasibility, double precision, no tolerance: max sqrt(x^2+y^2) <= 2000.0 m; min pairwise distance >= 260.0 m over all 630 pairs; exactly 36 hubs.
2. AEP: own evaluator written from the bank definition (validated first on par12-opt36 = 882383.304032 and par4-opt16 = 418924.406363 to 1e-4 MWh) AND the unmodified official iea37-aepcalc.py (sha256 ec2d16f2...). Pass requires both >= 863677.2993 MWh and agreement within 1e-4 MWh.
3. Topology: exact minimum-total-Euclidean one-to-one assignment to data/iea37-par12-opt36.yaml; pass requires count(distance > 50 m) >= 12.
Diagnostics (pre-declared, used for the stop/continue decision, not for the p1 pass): the same matching against every posted opt36 layout and against rotations (0.05 deg grid) and mirror images of participant 12; the object is flagged as a possible trivial edit if any rigid transform of a posted layout leaves fewer than 12 turbines > 50 m away.
Stop rule: stop before the panel if any of 1-3 fails, or the diagnostic flags a trivial edit, or a public 36-turbine layout >= the object's AEP that is not participant 12 is found.
null_test: not needed because only deterministic properties of one explicit object are claimed (no search-yield or statistical inference)
