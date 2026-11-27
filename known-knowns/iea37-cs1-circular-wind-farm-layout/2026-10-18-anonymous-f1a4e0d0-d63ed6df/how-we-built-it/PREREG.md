# PREREG (frozen Sun Oct 18 01:14:07 UTC 2026, before any optimisation output exists)

target: clean-energy-records / iea37-cs1-opt64
criterion (verbatim, from the announcement): "The objective of each scenario is to maximize annual energy production"
; "All turbine (x, y) locations must remain on or within this boundary. No turbine can be less than two rotor
diameters from any other turbine." ; "64 turbines, boundary radius of 3,000 m." ; "Results will be compared by running
the enclosed iea37-aepcalc.py".

statistic: AEP (MWh) printed on the last line by the unmodified data/cs1-2/iea37-aepcalc.py run on the claimed YAML
(from inside data/cs1-2 so the referenced windrose and turbine YAMLs resolve).
feasibility: every hub sqrt(x^2+y^2) <= 3000.0 and every pairwise distance >= 260.0, float64, no tolerance, computed
from the exact coordinates the YAML holds (yaml.safe_load).
threshold for a record claim: feasible AND AEP > 1526474.80248 (the best value known, par12, even though par12 is
4.1 mm outside). Anything feasible above 1513311.19361 but not above 1526474.80248 is reported as "best
constraint-satisfying layout found", NOT as a record, and is not a win claim.
novelty disclosure (frozen): the claim states the RMS and max displacement of its turbines from the nearest
par12 turbine (after the best of the 8 dihedral symmetries is not applied: the wind rose is not symmetric, so the raw
coordinates are compared). If the layout is a polish of par12 (max displacement < 50 m), the claim says so in its
one sentence.
null_test: not needed because the claim is an explicit object (a layout) checked by a deterministic official
evaluator against a table value; no search-for-signal or "beats chance" statistic is involved.
