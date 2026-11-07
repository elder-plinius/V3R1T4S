# CRITERION skeptic verdict: iea37-cs1-opt16 (object/iea37-v3r1t4s-opt16.yaml)

context: subagent (Claude Code Agent tool, fresh context, given only claim/)

## What I checked (all re-run myself, inside claim/)

1. **The criterion quotes match the PDF.** I ran `pdftotext` on evaluator/iea37-wflocs-announcement.pdf. Every quoted sentence in CLAIM.md appears verbatim:
   - "expected value of aerodynamic power"
   - "on or within this boundary"
   - "No turbine can be less than two rotor diameters from any other turbine"
   - "16 turbines, boundary radius of 1,300 m"
   - "Results will be compared by running the enclosed iea37-aepcalc.py"

   The announcement table gives Rotor Diameter 130 m.
2. **The rotor diameter is 130 m.** evaluator/iea37-335mw.yaml has rotor `radius: default: 65.0` and `diameter: expr: radius * 2.0`, so 130 m. iea37-aepcalc.py computes `turb_diam = radius*2`. The minimum spacing is therefore 260 m.
3. **The evaluator and object are the claimed files.** sha256 of evaluator/iea37-aepcalc.py is ec2d16f2…b535 and of the object is 4bd4f7cf…8f4c, both as claimed. The evaluator recomputes AEP from the coordinates. It does not read the YAML's self-reported `default` field. I did not compare the evaluator against an upstream copy. However, it reproduces every published Table 2 value in table/nrel72935.pdf to all printed digits, which validates the code and its inputs.
4. **The object's AEP reproduces.** `python3 iea37-aepcalc.py ../object/iea37-v3r1t4s-opt16.yaml` prints `424131.9503`. object/layout16.json has identical coordinates (unrounded 424131.95029791683).
5. **The constraints hold with no tolerance.** float64 gives max radius 1299.9999990000172 ≤ 1300 and min spacing 576.293 ≥ 260. I also checked in exact rational arithmetic on the decimal strings in the YAML:
   - max r² ≤ 1300², with a slack of 0.0026 m²
   - min d² ≥ 260²

   The boundary margin is only about 1e-6 m. It still satisfies "on or within" literally, so no tolerance is being used.
6. **The table folder reproduces as claimed.** I re-scored all 12 files in table/iea37-cs1-results. The highest is par12 at 421561.89715, which is INFEASIBLE (max radius 1303.518 m). par4 at 418924.40636 is INFEASIBLE by 3.9e-12 m. The best strictly feasible entry is par5 at 414141.29376. All match REPRODUCE.md.
7. **The bundled literature is all below the object.**
   - table/arxiv2212.00742.pdf Table 4 maximum: DPCRO-SL 419935.7905. The other rows are the participant values.
   - table/nrel72935.pdf Table 2 maximum: 418924.4064. It does not list par12.
   - table/wes-8-1453-2023.pdf Case I: roughly 418 GW h, below the SNOPT+WEC value of 418.92 GW h.

   No bundled value reaches 424131.95.
8. **Comparing against infeasible par12 is the strict test, not a stretch.** The frozen rule requires beating every known value, including infeasible ones, so threshold = 421561.89715. Including par12 raises the bar rather than lowering it. The object clears it by 2570.05 MWh (+0.61%).
9. **Subsumption / null check against par12.** I built the obvious repairs of par12 and scored them with the official code:
   - uniform scale into the circle: 421224.5041, FEASIBLE
   - radial projection of the outside turbines: 421451.07221, FEASIBLE

   Both stay below 421561.90, so neither trivial repair reaches the full-win threshold. The object exceeds the best repair by about 2681 MWh. Nearest-neighbour distances to par12 turbines are 3.8–51.8 m for 14 turbines and 568.6 m and 569.9 m for the other 2. That matches the disclosure: the layout is a par12-derived topology with two turbines moved to new sites, not a ≤50 m polish.

   Side finding: the repairs exceed 419935.79, so the frozen "enumerated partial win" alone would be trivially implied by par12. It is not the win being claimed, so this does not affect the verdict.
10. **Null model.** I agree that no statistical null is needed: the object is explicit and the evaluator is deterministic. The relevant null is "a trivial repair of the existing best entry already achieves it", which item 9 checked and rejected.

## Hidden quantifiers / stretched definitions

- **"Best known", not "optimal".** The claim asserts only that the value exceeds every known value. It makes no optimality claim, which is correct.
- **"Every value known" covers the bundled sources plus the scout's searches.** I can verify only the bundled table and three PDFs. Unbundled or unpublished results (e.g. 2024–2026 papers beyond the scout's search) cannot be ruled out from claim/. The confirmed scope is restricted accordingly.
- **Scoring is local, not hosted.** It is local execution of the official evaluator, which is exactly what the announcement specifies ("running the enclosed iea37-aepcalc.py"). No hosted leaderboard exists to stretch.
- **"Exactly" in the claim** means the boundary and spacing constraints hold with zero tolerance. I confirmed this in exact arithmetic.

confirmed_scope: The 16-turbine layout in object/iea37-v3r1t4s-opt16.yaml satisfies the IEA37 case study 1 constraints with no tolerance (all hubs within 1300 m of (0,0), all pairs at least 260 m apart). The unmodified official iea37-aepcalc.py scores it at 424131.9503 MWh, strictly above every 16-turbine value in table/iea37-cs1-results (maximum 421561.89715, par12, infeasible), arXiv 2212.00742 Table 4 (maximum 419935.7905), Baker et al. 2019 Table 2 (maximum 418924.4064), and Pérez-Rúa et al. 2023 Case I (about 418 GW h).

pass: true
