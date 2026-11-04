# REPRODUCE skeptic verdict: iea37-cs1-opt16 (object/iea37-v3r1t4s-opt16.yaml)

context: subagent (Claude Code Agent tool, fresh context, given only claim/)

## Definition checked against
I quoted this from the text of evaluator/iea37-wflocs-announcement.pdf, which I extracted with pdftotext and confirmed matches the quote in CLAIM.md:
- "Each wind farm scenario has a fixed circular boundary centered at (0, 0). All turbine (x, y) locations must remain on or within this boundary. No turbine can be less than two rotor diameters from any other turbine."
- "1. 16 turbines, boundary radius of 1,300 m." The announcement's table gives a rotor diameter of 130, so the minimum spacing is 260 m.
- "Results will be compared by running the enclosed iea37-aepcalc.py, which will read the submitted .yaml file from each participant."

## Method
1. I wrote my own feasibility checker from the definition before reading evaluator/check_constraints.py. It uses three tests:
   - the float64 `hypot` test;
   - the float64 squared test;
   - an exact rational test (Python `Fraction`) on the parsed float64 values: x²+y² ≤ 1300² and pairwise d² ≥ 260².
   All three must pass, and the turbine count must be 16.
2. I wrote my own vectorized AEP code, which does not reuse the official code:
   - model: simplified Bastankhah Gaussian, CT = 8/9, k = 0.0324555, D = 130 m, U = 9.8 m/s;
   - power curve: cut-in 4, rated 9.8, cut-out 25, rated power 3.35 MW;
   - wind rose: 16 bins, frequencies from evaluator/iea37-windrose.yaml;
   - combination: root-sum-square of deficits, then 8760 h × frequency × power.
   I took these parameters from the YAML inputs and the model description.
3. I ran the official evaluator/iea37-aepcalc.py unmodified from claim/evaluator. Its sha256 is ec2d16f2…c6b535, which matches REPRODUCE.md.
4. I ran every step twice and compared the outputs byte for byte.

## Results
**Object.** object/iea37-v3r1t4s-opt16.yaml has sha256 4bd4f7cf…98f4c, which matches the claim.
- **Official AEP:** the last printed line is `424131.9503`, and the per-bin array matches the YAML `binned` list.
- **Independent check:** my AEP is 424131.950298, which agrees with the official value.
- **Feasibility (no tolerance):** n = 16, max radius 1299.9999990000172 m (≤ 1300), min spacing 576.2929952098602 m (≥ 260). All three tests pass, including the exact rational test. **FEASIBLE.**
- **JSON copy:** object/layout16.json x and y equal the YAML coordinates exactly, element by element (16 and 16).
- **Author's checker:** evaluator/check_constraints.py, read after I wrote mine, gives the same numbers: FEASIBLE.

**Table** (official AEP; my AEP agrees to within 1e-5 on every file; F = feasible under my exact checker):

| file | official AEP | max r (m) | min d (m) | F |
|---|---|---|---|---|
| par12 | 421561.89715 | 1303.5181552724919 | 563.30 | no (3.518 m outside) |
| par4 | 418924.40636 | 1300.0000000000039 | 357.62 | no |
| par5 | 414141.29376 | 1299.988082638477 | 419.00 | yes |
| par8 | 412251.19453 | 1300.0010203769073 | 260.0009 | no |
| par1 | 411182.21998 | 1300.0009980660088 | 439.12 | no |
| par11 | 409850.32745 | 1300.0052585482108 | 464.05 | no |
| par2 | 409689.44174 | 1300.0000162460076 | 522.05 | no |
| par10 | 408360.78125 | 1299.9999999913548 | 308.28 | yes |
| par3 | 402318.7567 | 1300.0000000064304 | 376.20 | no |
| par7 | 392587.85803 | 1297.7038537818617 | 366.08 | yes |
| par6 | 388758.35729 | 1299.9999933687166 | 387.20 | yes |
| par9 | 388342.70041 | 1300.0000000045827 | 263.25 | no |

- All 12 values match CLAIM.md.
- The highest is par12 at 421561.89715, which is infeasible. The best feasible table entry is par5 at 414141.29376.
- The author's checker gives the same feasible/infeasible verdict on every file.
- Sanity check: evaluator/iea37-ex16.yaml scores 366941.57116 with both the official code and mine.

**DPCRO-SL** (table/arxiv2212.00742.pdf):
- Table 4 lists 419935.7905 as the best value.
- I transcribed the Table 5 layout from the PDF myself. It is feasible (max r 1299.935 m, min d 359.3 m) and my AEP gives 419933.316, which matches the claim.
- The object's turbines are 142.5 to 458.0 m from their nearest DPCRO-SL turbine, so none is within 50 m.
- 424131.9503 > 421561.89715 > 419935.7905.

**Displacement from par12** (per-turbine nearest distance to table/iea37-cs1-results/iea37-par12-opt16.yaml):
- Sorted distances: 3.803, 15.616, 17.211, 18.033, 21.338, 25.267, 30.890, 35.415, 36.732, 37.156, 37.867, 38.074, 39.750, 51.790, 568.588, 569.895 m.
- 14 of 16 are within 52 m. The other 2 are 568.6 and 569.9 m away (claimed: 550-570 m). The maximum is 569.9 m. All of this matches the claim.
- The 14 near turbines match 14 distinct par12 turbines one to one.
- Wording caveat, not a mismatch: the two vacated par12 positions (indices 2 and 7) are 823 to 1157 m from the two relocated turbines. "Relocated by about 550-570 m" therefore holds only in the nearest-turbine sense used in the claim and its novelty disclosure.

**Determinism:** two runs of my checker plus AEP, and two runs of the official script over all 14 files, gave byte-identical outputs.

## Limits
- I did not contact any external source, so I could not confirm two things:
  - that evaluator/iea37-aepcalc.py is byte-identical to upstream; my independent implementation reproduces its value on all 14 layouts;
  - that no value above 421561.89715 exists outside the supplied table and papers.
- Within the supplied evidence, the claimed value is strictly above every value known.

## Verdict
Every checkable property matches the claim with no tolerance:
- the object's official AEP;
- exact feasibility;
- JSON equals YAML;
- all 12 table values and feasibility statuses;
- the DPCRO-SL figures;
- the par12 displacement statements;
- determinism.

pass: true
