# Criterion skeptic verdict: iea37-cs1-opt64

Scope of review: only the claim package (claim/). All numbers below are pasted from commands I ran inside claim/evaluator
(and a scratch folder claim/scratch) with Python 3, numpy, pyyaml, scipy.

## 1. What the success criterion literally requires (evaluator/iea37-wflocs-announcement.pdf, iea37-wakemodel.pdf)
- Scenario 3 of Case Study 1: 64 turbines, circular boundary radius 3000 m centred at (0,0), every hub "on or within".
- No two turbines closer than two rotor diameters; rotor diameter 130 m (announcement table; iea37-335mw.yaml radius 65.0) -> 260 m.
- Objective: AEP = sum_i f_i P_i 8760, 16 bins, 9.8 m/s; judged by running the enclosed iea37-aepcalc.py on the submitted YAML.
- Format: the .yaml format of the iea37-ex##.yaml examples, reporting both total AEP and AEP per binned direction, and
  referencing iea37-windrose.yaml and iea37-335mw.yaml internally. File name pattern iea37-yourname-opt64.yaml.
- The wake-model PDF adds no extra constraint (it restates D = 130 m, 16 bins, and the AEP formula).

## 2. Checks on the object
- sha256 object/iea37-v3r1t4s-opt64.yaml = d63ed6df76fcbf03297cdb171acda406f597bfc959b1610711dc0d68dd93c851 (matches CLAIM.md).
- One layout, not a bundle: 64 xc and 64 yc values, 64 unique points; object/layout64.json holds identical coordinates (array_equal True).
- Format: same skeleton as evaluator/iea37-ex64.yaml; references `iea37-335mw.yaml` (turbine) and `iea37-windrose.yaml` (wind rose),
  which the evaluator resolved: "refs iea37-335mw.yaml iea37-windrose.yaml", "D 130.0 ws 9.8 nbins 16 sumf 1.0".
  Per-bin AEP array (16 values) and default total are both present; binned sum 1539447.1174 vs default 1539447.11737.
  File name "v3r1t4s" is lowercase alphanumeric, fits the stated pattern.
- Evaluator sanity: sha256 of evaluator/iea37-aepcalc.py = ec2d16f2...6b535 (as claimed; I could not compare against upstream
  from inside the package, but the code is the standard BYU release and reproduces the example: iea37-ex64.yaml -> 1294974.2977,
  equal to the example's stated default and to the "(Example Layout)" row of Table 4 in table/nrel72935.pdf).
- Official run (`python3 iea37-aepcalc.py ../object/iea37-v3r1t4s-opt64.yaml`), last line: **1539447.11737**.
- Constraints (float64, no tolerance): `turbines 64 max_radius 2999.999999000001 limit 3000.0 min_spacing 567.6913085779892 limit 260.0 / FEASIBLE`.
  Eight turbines sit on the boundary at 3000 - 1e-6 m. Spacing is not binding (closest pair 567.7 m).

## 3. Hidden quantifiers / fragility
- YAML rounding: the file stores full float repr, which yaml.safe_load reads exactly, so the stored object is feasible as judged.
  If someone re-serialised with 4 or 3 decimals, boundary turbines would land 5.34e-05 m / 3.39e-05 m outside (AEP 1539447.11588 /
  1539447.07512). This does not affect the object as submitted, but any republication must keep full precision.
- Margin is not an artefact of the boundary: scaling the whole layout by 0.999 (3 m inside the boundary, spacing 567.1 m) gives
  AEP 1538762.83016, still 12288 MWh above par12. 1 cm random jitter: AEP range 1539446.52 to 1539447.90. The win is not a
  float-edge or discontinuity effect.

## 4. Is "strictly higher AEP than every known value" the right record reading, and is the comparison fair?
- Table 4 of table/nrel72935.pdf (Baker et al. 2019) ranks entries by the official AEP only; there is no other ranking metric,
  so "higher official AEP while feasible" is the natural record notion. The claim's rule is stricter than needed: it also
  counts infeasible entries in the bar.
- Re-scoring of all 12 official-folder layouts (my run): par12 1526474.80248 (max_radius 3000.0041276 -> INFEASIBLE by 4.1 mm),
  par4 1513311.19361 (max_radius 3000.00000000014, min_spacing 260.0000000000015 -> INFEASIBLE by 1.4e-10 m under a no-tolerance
  reading), par2 1506388.41513, par11 1484287.26071, par10 1480850.9759 (the only feasible one), par1 1476689.66268,
  par3 1455075.60842, par8 1445967.37723, par9 1422268.71443, par6 1364943.00774, par5 1336164.5498, par7 1332883.43284.
  These match Table 4 for the published entries. Comparing against par12 despite its 4 mm violation is the conservative (fair)
  choice; projecting par12 4 mm inward would change its AEP negligibly, nowhere near the 12972 MWh (0.85 %) gap.
- Literature in the package: Pérez-Rúa et al. 2023 Table 2 (64-turbine best 1513.31 GWh, their own 0.85 % below it);
  Quaeghebeur et al. 2021 Fig. 13/14 (lowest 64-turbine wake loss about 19.4 %; the object's wake loss is
  1 - 1539447.11737/(64*3.35*8760) = 18.03 %, par12 18.72 %, par4 19.43 %); wes-9-321 uses 360 directions (not comparable);
  arXiv 2212.00742 is 16 turbines only. Nothing in the package exceeds the object.
- Limitation: I judged novelty only against the package's table and papers; I did not search the wider literature or the
  project's trophy case (outside my brief).

## 5. Subsumption: is it just a polish of participant 12?
Nearest-turbine distance from each object turbine to the participant layouts (no relabelling), plus optimal-assignment RMS:
```
par12: nearest RMS    208.8 max   613.6 median    39.5 n<10m  2 n<50m 37 | matched RMS   435.8
par2:  nearest RMS    277.9 max   573.8 median   243.9 n<10m  0 n<50m  1 | matched RMS   400.3
par4:  nearest RMS    345.4 max   621.4 median   294.5 n<10m  0 n<50m  1 | matched RMS   438.0
par10: nearest RMS    324.1 max   594.1 median   278.7 n<10m  0 n<50m  0 | matched RMS   403.5
par12 best over rotations/reflections, matched RMS 349.5 m
close (<50 m) & on boundary: 5; close interior: 32; boundary turbines: object 8, par12 8
```
The object is clearly related to par12 (37 of 64 turbines within 50 m of a par12 turbine; it was very likely seeded from it),
but it is not a polish: only 2 turbines are within 10 m, 27 turbines moved to positions 50 to 614 m from any par12 turbine,
and the AEP gain (12972 MWh, 0.85 %) is larger than the 0.46 % gap between the published 1st and 2nd places. A millimetre-scale
feasibility repair of par12 cannot reach it (see the 0.999-scaled check). I judge the win non-subsumed. Being derived from a
public layout does not violate any rule in the announcement.

## 6. Null model
Agree that none is needed: the claim is an explicit object scored by a deterministic official evaluator, so there is no
statistical inference to calibrate against a null.

## Verdict
The object meets the full success criterion as literally stated (64 turbines, on or within 3000 m, all pairs >= 260 m with
D = 130 m, official unmodified evaluator, official YAML format with total and per-bin AEP and correct references), and its
official AEP is strictly above every value in the package's table, including the infeasible participant-12 entry.

confirmed_scope: The single 64-turbine layout in claim/object/iea37-v3r1t4s-opt64.yaml (sha256 d63ed6df...dd93c851) lies on or within the 3000 m boundary with every pair at least 260 m apart in float64, and the unmodified iea37-aepcalc.py run on it with the official wind-rose and turbine files gives 1539447.11737 MWh, strictly above every 64-turbine value in the package's table and papers (highest 1526474.80248 for participant 12, published winner 1513311.19361).
context: subagent (Claude Code Agent tool, fresh context)
pass: true
