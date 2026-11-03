# CRITERION skeptic verdict: claim of partial win p1 (36-turbine cell), iea37-cs1-circular-wind-farm-layout

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Files read: CLAIM.md, criterion.txt, REPRODUCE.md, object/layout.json, references/* (provenance/ was not used for any check). My scripts and outputs are in panel/work-criterion/ (check.py -> check_output.txt, extra.py -> extra_output.txt, CLI run -> cli_output.txt).

## Evaluator validation
- references/iea37-aepcalc.py (sha256 ec2d16f2...b6535) was imported as-is and also run as an unmodified CLI. I also wrote a separate vectorised evaluator from the bank's equations.
- par4-opt16: official 418924.40636295587, mine 418924.406362956 (published 418924.406363).
- par12-opt36: official 882383.3040320876, mine 882383.3040320878 (published 882383.304032).
- par4-opt36: official 863676.2993158966, mine 863676.2993158966 (published 863676.2993).
- Inputs read from the files: 16 bins, 9.8 m/s, D 130.0, cut-in 4.0, rated 9.8 m/s, 3350000.0 W.

## p1 parsed word by word
1. "A feasible 36- ... layout": I used the bank's definition from the full criterion (hub radius <= R = 2000, every pair >= 260 m, double precision, no tolerance). The object has 36 rows, all finite, 36 distinct rows. max r = 1999.9999000019018 (margin 9.999809822147654e-05 m), and all hubs are <= 2000. Minimum of 630 pair distances = 260.25900134524915, and all are >= 260. An exact rational check on the stored doubles also passes (r^2 <= 4e6 True, pair^2 >= 67600 True), so the result does not depend on sqrt rounding. A YAML round-trip of the coordinates is bit-exact. The layout is feasible with no tolerance.
2. "AEP strictly above the best posted non-participant-12 value (SNOPT+WEC: 863676.2993 for 36) by at least 1 MWh": object AEP is 869713.9496471485 (import), 869713.94965 (unmodified CLI) and 869713.9496471485 (my evaluator), so the difference is 0.0. The threshold is 863676.2993 + 1 = 863677.2993. Margin over 863676.2993 is 6037.650347148534 MWh (6037.650331251905 over the full-precision posted value). I confirmed that 863676.2993 is the best of the 11 posted non-participant-12 opt36 files. The next best posted value is par10 at 851631.931.
3. "minimum-total-distance one-to-one matching to the participant-12 layout": I used a Hungarian assignment (scipy linear_sum_assignment) on Euclidean costs against references/iea37-par12-opt36.yaml. Total cost is 12736.71572395246 m. Matched distances range from 76.656 to 766.614 m.
4. "at least one third of the turbines are more than 50 m from their partner": count > 50 m = 36 of 36, against a requirement of >= 12. The smallest matched distance (76.656 m) is well clear of 50 m, so no ties or near-ties matter.
5. "(an independent topology)": I read this as a parenthetical gloss that the matching test defines, not as an extra condition. It is met with a large margin either way.

## Hidden quantifiers and stretched definitions
- Matching to participant 12 only, as worded, versus to all layouts: I also matched against every posted opt36 layout. Counts > 50 m: par1 33, par2 36, par3 34, par4 27, par5 34, par6 33, par7 34, par8 33, par9 32, par10 34, par11 33. Every count is >= 12. The closest is SNOPT+WEC (par4) at 27/36 with median 151.4 m. The wider reading would therefore not change the verdict.
- Squared-cost matching gives 36 > 50 m. The minimum over par12 rotated in 0.25-degree steps, with and without reflection, is 31 (informational only, because p1 names the untransformed layout). The independence result does not depend on the choice of matching.
- No tolerance is used anywhere. The two hubs about 1e-4 m inside R are inside R exactly.
- The AEP comes from the unmodified official model, not from the object's own aep_MWh metadata field (869713.9496471488). That field differs only in the last digits and was not used as evidence.

## Subsumption, scope and null model
- p1 is a property of one object: a qualifying layout. I read it literally. If some other non-participant-12 layout, such as a published one, also meets or exceeds the threshold, p1 for this object is not voided. Whether a prior identical or better layout exists is a NOVELTY question that I cannot settle from claim/. The comparators named in CLAIM.md (about 865 GWh in Perez-Rua et al. 2023, about 863.8 GWh in da Silva et al. 2025) are the author's assertions. If they are accurate, both lie below 869713.95 MWh.
- The win is not subsumed by the full criterion and not inflated toward it. The object is 12669.354384938953 MWh below participant 12's posted 882383.3040, and the claim correctly disclaims a full win.
- Only one explicit object is claimed. The check is deterministic, so I agree that no null test is needed.

confirmed_scope: The single 36-turbine layout in object/layout.json is strictly feasible for IEA37 case study 1 (all hubs within 2000 m and all pairs at least 260 m apart in exact double precision), has AEP 869713.9496471485 MWh under the unmodified references/iea37-aepcalc.py model, which is 6037.65 MWh above the SNOPT+WEC 863676.2993 MWh threshold, and has all 36 of its turbines more than 50 m from their partners under the minimum-total-Euclidean one-to-one matching to participant 12's posted layout, so it meets enumerated partial win p1 for the 36-turbine cell (not the full criterion, and with prior-art novelty left to the novelty skeptic).

Note: importing references/iea37-aepcalc.py briefly created claim/references/__pycache__/. I deleted it immediately. No claim file was changed, and the aepcalc sha256 is unchanged.

pass: true
