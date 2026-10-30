# IEA Wind Task 37 case study 1, 16 turbines: a strictly feasible layout with AEP 424131.9503 MWh

## What
The 16-turbine layout in object/iea37-v3r1t4s-opt16.yaml satisfies the IEA37 case study 1 constraints with no tolerance (all hubs within 1300 m of (0,0), all pairs at least 260 m apart). The unmodified official iea37-aepcalc.py scores it at 424131.9503 MWh, strictly above every 16-turbine value in table/iea37-cs1-results (maximum 421561.89715, par12, infeasible), arXiv 2212.00742 Table 4 (maximum 419935.7905), Baker et al. 2019 Table 2 (maximum 418924.4064), and Pérez-Rúa et al. 2023 Case I (about 418 GW h).

Target: clean-energy-records (charter quarry), instance iea37-cs1-opt16. Status: CONFIRMED_SOLUTION (three
fresh-context skeptics passed; see panel/).

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Python 3 standard library only, about 1 second. It checks the object's sha256, that the
JSON and YAML hold the same coordinates, both constraints with no tolerance, and recomputes the AEP from the wake-model
equations. To use the benchmark's own judge, download the official files (see RUN_IT_YOURSELF.md) and run
`python3 iea37-aepcalc.py iea37-v3r1t4s-opt16.yaml`: last line 424131.9503.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| IEA37 case study 1 official results folder | best 16-turbine AEP (participant 12) | 421561.89715 (layout 3.518 m outside the boundary) | https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results | 2026-10-20T02:24:14Z (NOVELTY skeptic; scout 01:08:33Z, same tree 267f6e5d) |
| arXiv 2212.00742 (DPCRO-SL), Table 4 | best feasible 16-turbine AEP known | 419935.7905 | https://arxiv.org/abs/2212.00742 | 2026-10-18 (scout of runs/2026-10-18-0107) |
| Baker et al. 2019, Table 2 | best 16-turbine AEP (SNOPT+WEC) | 418924.4064 | https://docs.nlr.gov/docs/fy19osti/72935.pdf | 2026-10-18T01:09:42Z |
Details in the-record-we-beat/record.md.

## Not claimed
- No optimality claim; nothing about the 36- or 64-turbine scenarios (the 64-turbine scenario is a separate package).
- Not an independent topology: 14 of the 16 turbines lie within 52 m of a participant-12 turbine; 2 sit about 570 m
  from any participant-12 turbine (nearest-turbine distance). The search that found it started from a random-start
  optimum and never read participant 12's layout, but the result is a variant of participant 12's ring structure.
- Not a physical or site-realistic optimum: like every entry, it exploits the 16-bin wind rose.
- Boundary hubs sit 1e-6 m inside the circle: copies must keep full float precision.
- Not submitted to any organiser (the case study closed in 2019).

## Credits
- Nicholas F. Baker, Andrew P. J. Stanley, Jared J. Thomas, Andrew Ning (BYU FLOW Lab) and Katherine Dykes (NREL):
  the IEA Wind Task 37 case studies, wake model, evaluator and results,
  https://github.com/IEAWindSystems/iea37-wflo-casestudies ; Baker et al., AIAA 2019-0540.
- IEA Wind Task 37 participants, especially participant 12 (whose layout this one closely resembles) and sub4
  (SNOPT + wake expansion continuation, Thomas and Ning).
- Majid Bastankhah and Fernando Porté-Agel: the Gaussian wake model.
- Moreno-Saavedra, Salcedo-Sanz et al., arXiv 2212.00742 (DPCRO-SL); Pérez-Rúa, Stolpe and Cutululis, Wind Energ.
  Sci. 8, 1453 (2023); Valotta Rodrigues et al., Wind Energ. Sci. 9, 321 (2024).
- Method: ruin-and-recreate large-neighbourhood search (Shaw 1998; Ropke and Pisinger 2006) with SciPy SLSQP polishing.
