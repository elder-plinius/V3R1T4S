# ITC2021 sports timetabling: lower-bound certificates on 5 instances

## What
For five ITC2021 instances, every feasible timetable has penalty at least Early 14 4, Early 9 40, Middle 6 60, Middle 9 20, Late 9 20, strictly above the posted bounds 1, 0, 24, 0, 3 and every other published bound found (highest 1, 0, 39, 0, 5), each shown by a saved CP-SAT model that replays OPTIMAL at the bound in a fresh session with one worker and the recorded seed, a solver log and a standard-library derivation, which meets partial win itc2021-lower-bound-certificate for each instance; Early 14's bound equals the score of Team Gionar's posted timetable, which is therefore optimal; nothing else is confirmed.

| instance | posted lower bound | proved lower bound | posted Best UB |
|---|---:|---:|---:|
| Early 14 | 1 | **4** | 4 |
| Early 9 | 0 | **40** | 56 |
| Middle 6 | 24 | **60** | 1090 |
| Middle 9 | 0 | **20** | 415 |
| Late 9 | 3 | **20** | 498 |

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (POSIX shell, curl, sha256sum, Python 3 standard library). It downloads each instance from the RobinX repository, checks its sha256, and re-derives each bound with a standard-library script: object/ITC2021_Early_14/certificate.py and object/ITC2021_Early_9/certificate.py (with PROOF.md), and verify-it-yourself/break_floor_stdlib.py for the other three. With OR-Tools installed it also replays every saved model object/<instance>/bound.pbtxt (one worker, the seed in how-we-built-it/rows.csv) to OPTIMAL at the bound; the solver logs are object/<instance>/bound.log.

## Compared to
The board's Best LB, each instance's history page, and the unposted bound files of Team MODAL in the RobinX repository (Middle 6 39, Late 9 5); see the-record-we-beat/. Every proved bound is strictly higher.

## Not claimed
Any new timetable (a separate claim); that the bounds are best possible; optimality of any instance except Early 14, whose bound equals the score 4 of Team Gionar's posted timetable (included and scored (0, 4) by RobinX and verify_timetable.py); that is the partial win's first clause, not its second. The Early 14 solver model covers the case of at most one break per team (penalty below 10); its PROOF.md covers the other case. One batched claim of five cells (kit rule 4 says one per claim), following Boss's explicit decision to file the full wins and the partial wins as two filings. The bounds come from counting breaks (each team's hard venue rules force some; at most two teams can avoid breaks; breaks come in home/away pairs per slot), a standard argument in sports scheduling; the certificates were made before the plan that fixed this claim (how-we-built-it/PREREG.md).

## Credits
Instances, board, history and the RobinX validator: David Van Bulck, Dries Goossens, Jeroen Belien and Morteza Davari (ITC2021 organisers; https://github.com/Robin-X/RobinX). Bounds exceeded: David Van Bulck (posted 0 bounds); George H. G. Fonseca and Tulio A. M. Toffolo (Early 14 1, Late 9 3); Team Udine (Middle 6 24; Rosati, Di Gaspero, Schaerf et al., Journal of Scheduling 2022, whose CPLEX bounds are 1, 0, 23, 0, 2.9); Team MODAL (bound files in the RobinX repository not posted on the board: Middle 6 39, Late 9 5). The break-counting ideas go back to de Werra (1981). Early 14's optimal timetable: Team Gionar. Tools: OR-Tools CP-SAT. Run by the V3R1T4S kit: Codex (Early 14 and Early 9 certificates, each reviewed earlier by three fresh reviewers), Antigravity (venue relaxations for Middle 6, Middle 9, Late 9) and Claude Code (lead agent, independent derivation and claim), with three fresh reviewer subagents.
