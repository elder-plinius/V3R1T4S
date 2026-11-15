# ITC-2007 examination timetabling, set5: total soft penalty 2,305 (OptHub best 2,327)

## What
For ITC-2007 exam instance set5, claim/object/set5.sol is hard-feasible and scores 2305 under an independently written evaluator that gives 2327 for OptHub's posted set5.sol (sha256 b83fcb6a...ee00), strictly below OptHub's live best of 2,327 (fetched 2026-11-15T03:15:04Z, HTTP 200), robust to front-load tie-breaking; nothing about other instances or optimality.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. It downloads the set5 instance and OptHub's posted best (Yuri Bykov's set5.sol) from OptHub
storage, checks both hashes, reproduces 2,327 for the posted best, then requires object/set5.sol to be hard-feasible
with total 2,305. A few seconds on a laptop (Python 3, standard library).

## Compared to
OptHub, ITC-2007 examination track (https://opthub.uniud.it/problems/timetabling/edutt/ett/itc-2007-ett), instance set5,
'Best solution' 2,327 (set5.sol, Yuri Bykov, 2021-12-19), read live at 2026-11-15T03:22:44Z (the-record-we-beat/record.md).
Best published value we found: 2,327 (Van Bulck, Goossens and Schaerf 2023, Table 7.2; their own best 2,341).

| instance | OptHub best | ours | difference |
|---|---|---|---|
| set5 | 2,327 | 2,305 | -22 |

## Not claimed
Optimality; any other instance (our set4 timetable at 10,433 is below OptHub's listed 10,448, but set4's posted file
cannot be reproduced, so it is not claimed here; see issue #1092); anything about the method beyond provenance. The
object was seeded from Bykov's posted file (it differs in 926 of 1,018 exams); an improving-only local search from that
file reaches 2,326 (how-we-built-it/hillclimb_control.txt). The object was found in an exploratory scout before this
claim's plan was frozen (how-we-built-it/PREREG.md says so).

## Credits
- ITC-2007 examination track and data: B. McCollum, P. McMullan, A. J. Parkes, E. K. Burke, R. Qu (Queen's University
  Belfast; https://doi.org/10.1287/ijoc.1090.0320).
- OptHub (University of Udine, https://opthub.uniud.it) for hosting instances, posted solutions and validated values.
- Yuri Bykov for the posted set5 best (2,327) that our search started from.
- D. Van Bulck, D. Goossens and A. Schaerf, "Multi-neighbourhood simulated annealing for the ITC-2007 capacitated
  examination timetabling problem", J. Scheduling (2023), https://doi.org/10.1007/s10951-023-00799-1, for the
  published comparison table and the Kempe-chain neighbourhood ideas.
