# REPRODUCE skeptic: iea37-cs1-circular-wind-farm-layout, 64 turbines

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Files read: CLAIM.md, criterion.txt, REPRODUCE.md, object/layout.json, references/* (all), status/* (search results and PR #938 live status). I did not open provenance/. Nothing in claim/ was modified, and no `__pycache__` or `.pyc` was created there. The sha256 of object/layout.json is d774540b96ab9d9db5a2b164e8c97e3222dc78ca62c1fbbdcc04ce4993645dc5 and of references/pr938-layout.yaml is d63ed6df76fcbf03297cdb171acda406f597bfc959b1610711dc0d68dd93c851. The PR #938 hash matches the prefix and suffix quoted in the PR body. The sha256 of references/iea37-aepcalc.py is ec2d16f237ed547fff3d44f314126b3889c000954f5a53ec3e14c28e5bc6b535. All three hashes were the same before and after my runs.

My code and captured output are in panel/work-reproduce/: mycheck.py, official_import.py, make_yaml.py, strict_json.py, and the files *_out.txt and *_run{1,2}.txt.

## Definition implemented (quoted from criterion.txt)

> A layout for the 16-, 36- or 64-turbine scenario with every hub at distance at most R from (0,0) and every pair at least 260 m apart, both checked with no tolerance in double precision. Its AEP from the official iea37-aepcalc.py model (16-bin rose, constant 9.8 m/s, iea37-335mw.yaml) must be STRICTLY GREATER (direction: max) by at least 0.01 MWh than the posted record, used as posted even though it lies outside the boundary: ... 1526474.8025 (64), and also strictly greater than every CONFIRMED V3R1T4S known-known for the same scenario at claim time.

> Compute AEP from the wake-model equations (wind-frame rotation by 270 - theta, sigma = k*dx + D/sqrt(8), deficit (1 - sqrt(1 - CT/(8 sigma^2/D^2))) exp(-0.5 (dy/sigma)^2), RSS combination, cubic power curve between 4 and 9.8 m/s, 8760 h).

Constants: k = 0.0324555, CT = 8/9, D = 130 m, U = 9.8 m/s, rated power 3.35 MW, cut-in 4 m/s, rated speed 9.8 m/s, cut-out 25 m/s, R = 3000 m. The rose bins and probabilities are read from references/iea37-windrose.yaml (probabilities sum to 1.0).

mycheck.py was written before I read references/iea37-aepcalc.py. It uses only plain Python floats with math.fsum and does not use numpy. It works from first principles with meteorological 'from' directions: the downwind unit vector for a wind from theta is u = (-sin theta, -cos theta), and dx and dy are projections onto u and its normal. This is equivalent to the 270 - theta rotation.

Feasibility is checked in two ways:
- **Float64:** hypot and sqrt.
- **Exact:** fractions.Fraction applied to the stored doubles, testing x^2+y^2 <= 3000^2 and dx^2+dy^2 >= 260^2 with no rounding at all.

## Evaluator validation (published cases from REPRODUCE.md)

| case | published | mine (mycheck.py) | official (imported) | official CLI |
|---|---|---|---|---|
| par12-opt64 | 1526474.8024800716 | 1526474.8024800713 | 1526474.8024800713 | 1526474.80248 |
| par4-opt64 | 1513311.19361464 | 1513311.1936146398 | 1513311.1936146398 | 1513311.19361 |

The binned values for par12 from my evaluator match the official CLI to all 5 printed decimals in all 16 bins (for example, bin 270 is 331146.82361).

I also ran all 12 posted 64-turbine layouts (par1 to par12). My values agree with the imported official functions with a difference of exactly 0.000e+00 in every case, and they match each file's posted `default` AEP. Examples: par1 1476689.6626809824 vs posted 1476689.662680982; par2 1506388.4151333692 vs 1506388.41513; par7 1332883.4328355915 vs 1332883.43284.

My feasibility check also reproduces the pitfalls stated in the criterion:
- **par12:** rmax = 3000.0041276138268, which is 0.004127613827 m outside R, with 3 hubs outside.
- **par4:** rmax = 3000.0000000001414, which is 1.414e-10 m outside R, with 15 hubs outside under the exact test.

## Object: object/layout.json

- **Structure:** the only top-level key is `coordinates_m`. It has 64 entries, every entry is an [x, y] pair, all values are JSON floats with no NaN or Infinity tokens and no duplicate keys, and there are 64 distinct hubs. All 128 numeric tokens round-trip exactly (repr(float(token)) == token). finite = True.
- **Boundary:**
  - Float64: max hypot = 2999.999900000135 and max sqrt(x^2+y^2) = 2999.999900000135, at hub index 7.
  - Exact: all 64 hubs satisfy x^2+y^2 <= 9,000,000, with n_outside = 0. The exact slack at the worst hub is R^2 - r^2 = 0.5999991808434681 m^2, so that hub is 9.999986514e-05 m inside R.
  - Result: PASS.
- **Spacing:**
  - All 2016 pairs were checked.
  - Float64: min distance = 307.51364081707464 m, for the pair (12, 57).
  - Exact: all pairs satisfy d^2 >= 67600, with n_close = 0. The exact slack is 26964.63928857281 m^2.
  - Result: PASS.
- **AEP:**
  - Mine (mycheck.py): 1543800.4664981717 MWh.
  - Unmodified official functions imported from references/iea37-aepcalc.py and given the full-precision JSON doubles: 1543800.4664981714 MWh. The difference from mine is 2.328e-10.
  - Unmodified official CLI on a YAML of the object (panel/work-reproduce/object-layout.yaml, written with repr floats; I verified that the round-trip to the same doubles is bit-exact): prints 1543800.4665.
  - Binned values (official CLI): 37622.92932, 34854.40959, 44299.27589, 56411.17449, 99616.73069, 97655.05038, 153575.04885, 189692.45533, 95737.38990, 55125.78281, 59380.08308, 129563.36424, 338330.99153, 68793.26970, 49182.30220, 33960.20849. These are identical to mine.
  - Claimed value: 1543800.4665. object minus claimed = -1.83e-06, which is rounding only, so it matches.
- **Determinism:** I ran mycheck.py twice and official_import.py twice. Both pairs of outputs are byte-identical (cmp).

## PR #938 (references/pr938-layout.yaml), recomputed

- **Feasibility:** 64 finite hubs. Max radius = 2999.999999000001, which is 9.99999e-07 m inside R; the exact R^2 slack is 0.0059999937947876805 with n_outside = 0. Min spacing = 567.6913085779892 m with n_close = 0. It is strictly feasible.
- **AEP:**
  - Mine: 1539447.117368648.
  - Official (imported): 1539447.1173686478.
  - Official CLI: 1539447.11737.
  - Reported: 1539447.11737. recomputed minus reported = -1.35e-06.

## Margins (computed from the official imported value 1543800.4664981714)

- object - (1526474.8025 + 0.01) = **17325.653998171445**, which is > 0 and satisfies the 0.01 MWh requirement.
- object - 1526474.8025 = 17325.663998171454. The claim says 17325.66.
- object - 1526474.8024800716 (full-precision record) = 17325.664018099895.
- object - PR #938 recomputed = **4353.349129523616**. The claim says 4353.35.
- object - PR #938 reported 1539447.11737 = 4353.349128171336.

## Known-knowns / open claims (status/pr-search.json, 6 items)

At 64 turbines there is one competing claim, PR #938, which is an open draft and not confirmed. The object beats it, as shown above. The other items do not compete in this cell:
- PR 948 proposes a different, direction-robust target.
- PR 578 is a 16-turbine claim.
- PR 913 is a 36-turbine p1 claim.
- PR 900 is a 16-turbine p2 claim.
- Issue 866 is a data audit.

None of the items is a confirmed known-known for this cell. status/pr938-live.json shows head 9f1145de2f2c98d686f9ca7b74ffca6cab6c467d, OPEN, draft, which matches CLAIM.md.

## Verdict

Every property checks out with no tolerance:
- exactly 64 finite, distinct hubs;
- all hubs within 3000 m, proven exactly in rational arithmetic;
- all 2016 pairs at least 260 m apart, proven exactly;
- AEP 1543800.4664981714 MWh from the unmodified official script, reproduced by my independent evaluator to within 2.3e-10;
- strictly above 1526474.8025 + 0.01;
- strictly above PR #938's recomputed, feasible 1539447.1173686478.

The results are deterministic and I found no mismatches.

pass: true
