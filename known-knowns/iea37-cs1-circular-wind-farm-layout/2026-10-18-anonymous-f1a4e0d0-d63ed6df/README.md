# IEA Wind Task 37 case study 1, 64 turbines: a strictly feasible layout with AEP 1539447.11737 MWh

## What
The single 64-turbine layout in claim/object/iea37-v3r1t4s-opt64.yaml (sha256 d63ed6df...dd93c851) lies on or within the 3000 m boundary with every pair at least 260 m apart in float64, and the unmodified iea37-aepcalc.py run on it with the official wind-rose and turbine files gives 1539447.11737 MWh, strictly above every 64-turbine value in the package's table and papers (highest 1526474.80248 for participant 12, published winner 1513311.19361).

Target: iea37-cs1-circular-wind-farm-layout (bank target; found and panelled under the charter quarry
clean-energy-records), instance iea37-cs1-opt64. Status: CONFIRMED_SOLUTION (three
fresh-context skeptics passed; see panel/).

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Python 3 standard library only, about 5 seconds. It checks the object's sha256, that the
JSON and YAML hold the same coordinates, both constraints with no tolerance, and recomputes the AEP from the wake-model
equations. To use the benchmark's own judge, download the official files (see RUN_IT_YOURSELF.md) and run
`python3 iea37-aepcalc.py iea37-v3r1t4s-opt64.yaml`: last line 1539447.11737.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| IEA37 case study 1 official results folder | best 64-turbine AEP (participant 12, posted 2019-07-29) | 1526474.80248 (layout 4.1 mm outside the boundary) | https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results | 2026-10-18T03:20:29Z (NOVELTY skeptic; scout 01:07:59Z, same sha256) |
| Baker et al. 2019, Table 4 | best 64-turbine AEP (SNOPT+WEC) | 1513311.19361 (1513.31 GWh) | https://docs.nlr.gov/docs/fy19osti/72935.pdf | 2026-10-18T01:09:42Z |
| V3R1T4S known-knowns and open claims for iea37-cs1-circular-wind-farm-layout | best 64-turbine value | none: no known-known in the family; the open claims #578 (16 turbines), #900 (16) and #913 (36) cover other scenarios | https://github.com/elder-plinius/V3R1T4S/pulls | 2026-11-04T01:04:24Z |
Details in the-record-we-beat/record.md. Against the bank target's 64-turbine record (1526474.8025, participant 12) the
margin is 12972.31489 MWh; there is no CONFIRMED V3R1T4S known-known or open claim at 64 turbines to beat (re-checked
2026-11-04T01:04:24Z; the results folder's last commit is still 1b2062b6 of 2019-07-29).

## Not claimed
- Nothing about the 16- or 36-turbine scenarios (our 36-turbine search did not beat participant 12 with a new design).
- Not a physical or site-realistic optimum: like every entry, the layout exploits the 16-bin wind rose; rotating the
  rose by 1 degree costs about 0.5 % AEP, by 5 degrees 11-14 %.
- The search started from participant 12's layout (repaired into feasibility); the result moved 28 hubs more than
  50 m (RMS 208.8 m to the nearest participant-12 hub), and chains that never saw participant 12 also passed it
  (best 1533259), but this layout is not an independent design from scratch. Under the bank target's
  minimum-total-distance one-to-one matching, 28 of 64 turbines are more than 50 m from their participant-12
  partner (median 39.5 m; computed 2026-11-04, after the panel).
- Boundary hubs sit 1e-6 m inside the circle: copies must keep full float precision.
- Not submitted to any organiser (the case study closed in 2019).

## Credits
- Nicholas F. Baker, Andrew P. J. Stanley, Jared J. Thomas, Andrew Ning (BYU FLOW Lab) and Katherine Dykes (NREL):
  the IEA Wind Task 37 case studies, wake model, evaluator and results,
  https://github.com/IEAWindSystems/iea37-wflo-casestudies ; Baker et al., AIAA 2019-0540.
- IEA Wind Task 37 participants, especially participant 12 (layout this search was warm-started from) and sub4
  (SNOPT + wake expansion continuation, Thomas and Ning).
- Majid Bastankhah and Fernando Porté-Agel: the Gaussian wake model.
- Literature compared against: Pérez-Rúa, Stolpe and Cutululis, Wind Energ. Sci. 8, 1453 (2023); Quaeghebeur, Bos and
  Zaaijer, Wind Energ. Sci. 6, 815 (2021); Valotta Rodrigues et al., Wind Energ. Sci. 9, 321 (2024); arXiv 2212.00742.
- Method: ruin-and-recreate large-neighbourhood search (Shaw 1998; Ropke and Pisinger 2006) with SciPy SLSQP polishing.
