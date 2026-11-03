# REPRODUCE skeptic verdict: iea37-cs1 36-turbine layout, partial win p1

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Files read: CLAIM.md, criterion.txt, REPRODUCE.md, object/layout.json, references/*.yaml, references/iea37-aepcalc.py.
I did not read provenance/ or status/; they were not needed, because every result below comes from my own code and the official evaluator.
My work is in panel/work-reproduce/: my_checker.py with output my_checker_output.txt, and make_yaml_and_official.py with output official_output.txt (official CLI runs appended).

## Definition implemented (quoted from criterion.txt)

> "Check max sqrt(x^2+y^2) <= R and min pairwise distance >= 260 m exactly. Compute AEP from the wake-model equations (wind-frame rotation by 270 - theta, sigma = k*dx + D/sqrt(8), deficit (1 - sqrt(1 - CT/(8 sigma^2/D^2))) exp(-0.5 (dy/sigma)^2), RSS combination, cubic power curve between 4 and 9.8 m/s, 8760 h). First reproduce par4-opt16 = 418924.406363 and par12-opt36 = 882383.304032."

p1 (quoted): "A feasible 36- or 64-turbine layout with AEP strictly above the best posted non-participant-12 value (SNOPT+WEC: 863676.2993 for 36 ...) by at least 1 MWh, such that under the minimum-total-distance one-to-one matching to the participant-12 layout at least one third of the turbines are more than 50 m from their partner".

My own formulation uses k = 0.0324555, CT = 8/9, D = 130, U = 9.8 and P_rated = 3.35 MW, with cut-in 4, rated 9.8 and cut-out 25. I wrote the wind frame independently. Wind direction theta is the meteorological "from" direction, so the flow vector is d = (-sin theta, -cos theta). The downstream coordinate is p.d and the crosswind coordinate uses the perpendicular vector. A turbine is waked only when dx > 0.

## Checker validation (my code, published cases)
- par4-opt16: 418924.4063629559 (expected 418924.406363, diff -4.4e-08)
- par12-opt36: 882383.3040320877 (expected 882383.304032, diff 8.8e-08)
- par4-opt36: 863676.2993158965 (expected 863676.2993)
- Convention sanity check: flipping to the "to" direction convention gives 881231.3879091194 for par12-opt36, which does not match the published value. This confirms the "from" convention is the right one.

## Object: object/layout.json (sha256 3ea13ecabb80052105d9713b59cdde25b15e888705c009e315e28ae970fadc30)
- Hub count: exactly 36 [x, y] pairs. All values are finite doubles and all 36 points are distinct.
- Radius, exact rational arithmetic on the stored doubles (Fraction): every x^2+y^2 <= 2000^2 is True. The minimum slack in r^2 is 0.3999923823391507 m^2.
- Radius, double precision: the max sqrt(x^2+y^2) is 1999.9999000019018, which is <= 2000. With math.hypot it is 1999.999900001902. 11 hubs have r > 1999.99.
- Spacing, exact rational arithmetic: all 630 pairs have d^2 >= 260^2. The minimum of d^2 - 260^2 is 134.7477812263755 m^2.
- Spacing, double precision: the min pairwise distance is 260.25900134524915, which is >= 260.
- Neither check uses any tolerance.

## AEP
- My own code gives 869713.9496471485 MWh. A rerun in the same process gave a bit-identical result.
- The official references/iea37-aepcalc.py was run unmodified (sha256 ec2d16f237ed547fff3d44f314126b3889c000954f5a53ec3e14c28e5bc6b535):
  - Calling calcAEP directly on a full-precision YAML of the object gives 869713.9496471485. The YAML round-trip was bit-exact.
  - The CLI run gives 869713.94965.
  - The same evaluator also reproduces the validation cases: par4-opt16 418924.40636295587, par12-opt36 882383.3040320876 and par4-opt36 863676.2993158966.
  - Caveat: I could not compare this file with the upstream file byte-for-byte (I had access to claim/ only). It reproduces all three published values.
- Claimed value: 869713.9496471485. My result differs from it by 0.0.
- Threshold: 863676.2993 + 1 = 863677.2993. The AEP is above it, with a margin of 6037.650347148534 MWh over 863676.2993.

## Matching to references/iea37-par12-opt36.yaml
- I used the minimum-total-Euclidean one-to-one assignment (scipy linear_sum_assignment). The total is 12736.71572395246 m.
- An independent LP solve (HiGHS) gives 12736.715723952468. The difference from the assignment total is 7.3e-12, so the matching is optimal.
- Matched distances strictly > 50 m: 36 of 36. p1 needs at least 12.
- Min matched distance: 76.6559137065811 m. Max matched distance: 766.6137271296228 m.
- A stronger bound holds regardless of which matching is used. The nearest participant-12 hub to any object hub is 76.6559137065811 m away, so every one-to-one matching has all 36 distances > 50 m.
- For context only, the object is also distinct from every other posted opt36 layout: matched >50 m counts range from 27 (par4) to 36.

## Notes
- The aep_MWh metadata field in object/layout.json reads 869713.9496471488. That differs in the last digits from the computed 869713.9496471485. The claim says this metadata is not evidence; the value stated in CLAIM.md matches exactly.
- The claim folder was not modified.

All properties of p1 are confirmed: 36 hubs, strict feasibility (both exact and double precision), AEP > 863676.2993 + 1 from both my evaluator and the official one, and 36 of 36 matched distances > 50 m.

pass: true
