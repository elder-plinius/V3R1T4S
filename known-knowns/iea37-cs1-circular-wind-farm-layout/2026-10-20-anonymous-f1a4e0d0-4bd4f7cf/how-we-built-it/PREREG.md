# PREREG (frozen Tue Oct 20 01:12:57 UTC 2026 , before any optimisation output exists)

target: clean-energy-records / iea37-cs1-opt16
criterion (verbatim, from the announcement): "The objective of each scenario is to maximize annual energy production"
; "All turbine (x, y) locations must remain on or within this boundary. No turbine can be less than two rotor
diameters from any other turbine." ; "1. 16 turbines, boundary radius of 1,300 m." ; "Results will be compared by
running the enclosed iea37-aepcalc.py".

statistic: AEP (MWh) printed on the last line by the unmodified data/cs1-2/iea37-aepcalc.py run on the claimed YAML
(from inside data/cs1-2 so the referenced windrose and turbine YAMLs resolve).
feasibility: every hub sqrt(x^2+y^2) <= 1300.0 and every pairwise distance >= 260.0, float64, no tolerance, computed
from the exact coordinates the YAML holds (yaml.safe_load).
threshold for a record claim: feasible AND AEP > 421561.89715 (par12, the best value known, although 3.518 m outside).
partial win (enumerated): feasible AND AEP > 419935.7905 (DPCRO-SL as printed; the best strictly feasible value known)
but not above 421561.89715. Reported as "best constraint-satisfying layout known", never as a record.
Below 419935.7905: no claim.
novelty disclosure (frozen): the claim states the max displacement of its turbines from the nearest turbine of
par12 and of the DPCRO-SL Table 5 layout (raw coordinates; the wind rose is not symmetric). If the layout is a polish
of either (max displacement < 50 m), the claim says so in its one sentence and that is weighed by the panel.
null_test: not needed because the claim is an explicit object (a layout) checked by a deterministic official
evaluator against a table value; no search-for-signal or "beats chance" statistic is involved.
