# ITC2021 sports timetabling: 6 timetables below the Best UB

## What
For each of six ITC2021 instances (Early 9, Early 12, Middle 5, Middle 12, Middle 15, Late 11), the timetable in object/ is a valid compact double round robin with 0 hard violations whose penalty (51, 300, 278, 338, 459, 191) is strictly below the board's Best UB (56, 315, 279, 358, 462, 196; board fetched 2026-11-27, unchanged at 15:00:20Z) under RobinX built from source at commit 878bf2db on the original instance files and under an independently written evaluator, 49 below in total, so each meets the full criterion separately; nothing is confirmed about optimality.

| instance | Best UB (board) | ours | below by | Best UB held by |
|---|---:|---:|---:|---|
| Early 9 | 56 | **51** | 5 | David Van Bulck, Dries Goossens |
| Early 12 | 315 | **300** | 15 | David Van Bulck, Dries Goossens |
| Middle 5 | 279 | **278** | 1 | David Van Bulck, Dries Goossens |
| Middle 12 | 358 | **338** | 20 | Clemence Van den Ostende |
| Middle 15 | 462 | **459** | 3 | Andreas Krystallidis, Nysret Musliu, Saturn (board entry) |
| Late 11 | 196 | **191** | 5 | I Gusti Agung Premananda and Ahmad Muklason |

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (POSIX shell, curl, sha256sum, Python 3 standard library). It checks each timetable's sha256, downloads each instance file from the RobinX repository and checks its sha256, and runs verify-it-yourself/verify.py, an evaluator written independently of RobinX: valid compact double round robin, 0 hard violations, penalty strictly below the Best UB. For RobinX itself see RUN_IT_YOURSELF.md.

## Compared to
The board https://robinxval.ugent.be/ITC2021/instances.php fetched 2026-11-27T14:42:43Z and each instance's history page (the-record-we-beat/). 49 below the Best UB values in total.

## Not claimed
Optimality of any timetable; partial win itc2021-middle-late-improve (no row has UB - LB > 500); anything about the search method beyond how-we-built-it/. Five of the six timetables keep the record's home/away pattern and re-assign the games (only Late 11 changes venues). The searches were exploratory and not preregistered; the plan fixing the objects and checks was frozen after them (how-we-built-it/PREREG.md).

## Credits
Instances, board, history and the RobinX validator: David Van Bulck, Dries Goossens and the ITC2021 organisers (https://github.com/Robin-X/RobinX). Records compared against: David Van Bulck and Dries Goossens (Early 9, Early 12, Middle 5), Clemence Van den Ostende (Middle 12), Andreas Krystallidis, Nysret Musliu and co-authors (Middle 15), I Gusti Agung Premananda and Ahmad Muklason (Late 11). Tools: OR-Tools CP-SAT. Run by the V3R1T4S kit: Claude Code (lead agent, search and claim), with three fresh reviewer subagents.
