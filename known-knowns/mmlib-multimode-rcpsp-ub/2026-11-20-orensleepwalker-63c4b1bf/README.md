# MMLIB+: 30 open instances with a shorter makespan than the best known

## What

Each of the 30 MMLIB+ schedules in object/schedules/ is, by an independent checker run on the v2.1 release instance files, a feasible multi-mode schedule whose makespan is strictly below that instance's UB in data/MMplus_2.csv, its value in data/MMplus_2_BKS.csv and its UB-lit in the MMLIB v2.1 release Excel, on instances open (LB < UB) in data/MMplus_2.csv as fetched 2026-11-20T10:14:46Z (34 makespan units in total).

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (POSIX shell, curl, sha256sum, Python 3 standard library; about a minute, mostly the 15.7 MB download). It checks the hashes, downloads the MMLIB v2.1 release from GitHub and checks its sha256, then verifies every schedule against its instance file (one mode per activity, non-renewable budgets, precedences, renewable capacity in every period, makespan) and compares it with the recorded best-known values and the release Excel. Expected last line: PASS.

## Compared to

SolutionsUpdate dataset MMplus (http://solutionsupdate.ugent.be/dataset/mmplus), values fetched 2026-11-20T10:14:46Z and re-fetched unchanged at 2026-11-20T10:41:46Z; release Excel UB-lit read from MMLIB v2.1. Every makespan is strictly below the dataset UB, the best-known CSV value and the Excel UB-lit (the-record-we-beat/).

| instance | LB | best known UB | ours | UB held by | start |
|---|---|---|---|---|---|
| Jall248_3 | 40 | 51 | 50 | mmlib.eu 2018 | from scratch |
| Jall354_2 | 30 | 32 | 31 | Coelho and Vanhoucke 2011 | posted schedule |
| Jall354_3 | 29 | 32 | 31 | Coelho and Vanhoucke 2011 | posted schedule |
| Jall433_1 | 66 | 73 | 72 | mmlib.eu 2018 | from scratch |
| Jall434_5 | 47 | 54 | 53 | mmlib.eu 2018 | from scratch |
| Jall436_2 | 44 | 51 | 50 | mmlib.eu 2018 | from scratch |
| Jall436_3 | 51 | 58 | 56 | mmlib.eu 2018 | from scratch |
| Jall436_5 | 47 | 54 | 53 | mmlib.eu 2018 | from scratch |
| Jall445_3 | 68 | 76 | 75 | mmlib.eu 2018 | from scratch |
| Jall460_4 | 59 | 69 | 67 | mmlib.eu 2018 | from scratch |
| Jall490_1 | 62 | 77 | 76 | mmlib.eu 2018 | from scratch |
| Jall490_5 | 64 | 76 | 75 | Etminaniesfahani et al. 2023 | posted schedule |
| Jall491_2 | 46 | 52 | 51 | mmlib.eu 2018 | from scratch |
| Jall504_4 | 51 | 53 | 52 | mmlib.eu 2018 | from scratch |
| Jall543_4 | 41 | 47 | 46 | mmlib.eu 2018 | from scratch |
| Jall544_2 | 64 | 75 | 74 | Shichen Tian 2026 | posted schedule |
| Jall555_4 | 42 | 51 | 50 | mmlib.eu 2018 | from scratch |
| Jall569_1 | 79 | 92 | 91 | Shichen Tian 2026 | posted schedule |
| Jall569_2 | 60 | 71 | 69 | mmlib.eu 2018 | from scratch |
| Jall569_3 | 63 | 77 | 76 | Shichen Tian 2026 | posted schedule |
| Jall570_1 | 50 | 58 | 57 | mmlib.eu 2018 | from scratch |
| Jall570_5 | 48 | 56 | 55 | mmlib.eu 2018 | from scratch |
| Jall571_4 | 66 | 79 | 78 | Etminaniesfahani et al. 2023 | posted schedule |
| Jall572_2 | 46 | 60 | 59 | mmlib.eu 2018 | from scratch |
| Jall597_3 | 51 | 61 | 60 | mmlib.eu 2018 | from scratch |
| Jall598_2 | 64 | 80 | 78 | mmlib.eu 2018 | from scratch |
| Jall599_3 | 45 | 52 | 51 | mmlib.eu 2018 | from scratch |
| Jall609_2 | 44 | 51 | 50 | mmlib.eu 2018 | from scratch |
| Jall624_2 | 46 | 53 | 52 | Shichen Tian 2026 | posted schedule |
| Jall625_2 | 72 | 84 | 83 | mmlib.eu 2018 | from scratch |

Total: 34 makespan units (26 instances by 1, 4 by 2).

## Not claimed

No instance is claimed optimal, and no lower bound is claimed. Other MMLIB sets (MMLIB50, MMLIB100) and Boctor100 are not part of this claim. The search was exploratory (targets chosen as results came in) and not preregistered; the preregistration froze the selection and the checks. Eight schedules started from the instance's posted best-known schedule and change 18 to 46 of 100 modes; for four of them (Jall354_2, Jall354_3, Jall569_1, Jall569_3) it is not proved that re-timing the posted modes alone cannot reach our makespan (panel/gate.md). One 2025 paper (Ahmeti and Musliu, Journal of Heuristics) could not be read in full. Each row stands alone: any row can be dropped without affecting the others.

## Credits

Instances and best-known values: Van Peteghem and Vanhoucke, [European Journal of Operational Research 235(1) (2014)](https://doi.org/10.1016/j.ejor.2013.10.012), the [MMLIB library](https://github.com/MarioVanhoucke/MMLIB-Multi-Mode-Resource-Constrained-Project-Library) and Vanhoucke and Coelho's [SolutionsUpdate](http://solutionsupdate.ugent.be/mrcpsp) ([Computers & Industrial Engineering 118 (2018)](https://doi.org/10.1016/j.cie.2018.02.001)). Records compared against: Coelho and Vanhoucke ([EJOR 213 (2011)](https://doi.org/10.1016/j.ejor.2011.03.019)); Etminaniesfahani, Gu, Moslemi Naeni and Salehipour ([Annals of Operations Research 338 (2024)](https://doi.org/10.1007/s10479-023-05775-8)); Shichen Tian (SolutionsUpdate, 2026); the mmlib.eu values (2018). Tools: OR-Tools CP-SAT, NumPy, Numba. Run by the V3R1T4S kit: Claude Code (lead agent, phase A, claim) and Antigravity (search phases B and C), with three fresh reviewer subagents.
