# XHSTT-2014 high school timetabling: AU-BG-98 solution below the best archived cost

## What
For each of three open XHSTT-2014 instances, separately, the solution in object/ evaluated on the instance's dataset-page file by an evaluator written from the HSEval specification (which reproduces every stored solution value of these files, and agrees with a second evaluator written by a reviewer) has cost AU-BG-98 (0, 91), DK-HG-12 (12, 2326), DK-VG-09 (2, 2322), hierarchically strictly lower than the best on both the XHSTT-2014 overview and the dataset page (AU-BG-98 126 and 128, DK-HG-12 12.2330, DK-VG-09 2.2323; fetched 2026-11-28, unchanged at 09:22Z), so each meets the full criterion separately; not cross-checked with HSEval; nothing is confirmed about optimality.

This package carries the AU-BG-98 row only. The claim was reviewed as one batch of three rows, each meeting the criterion separately; the other two rows (DK-HG-12, DK-VG-09) are filed as separate packages.

Costs are (infeasibility, objective) pairs, compared hierarchically: lower infeasibility first, then lower objective. The overview writes a feasible cost as the objective alone (AU-BG-98: 126) and an infeasible one as infeasibility.objective (DK-HG-12: 12.2330).

| instance | overview best | dataset-page best | ours |
|---|---|---|---|
| AU-BG-98 | (0, 126) | (0, 128) | **(0, 91)** |

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (POSIX shell, curl, sha256sum, Python 3 standard library). It checks each solution's sha256, downloads each instance file (with all its submitted solutions) from its dataset page and checks its sha256, and runs verify-it-yourself/verify.py: the evaluator first reproduces the best stored solution at the dataset-page value, checks our solution's structure, and requires our cost to be strictly lower than both bests. A cross-check with Jeffrey Kingston's HSEval is described in RUN_IT_YOURSELF.md.

## Compared to
The XHSTT-2014 overview and each instance's dataset page, fetched 2026-11-28T08:57:12Z (hashes in the-record-we-beat/snapshot.md). The record is the GOAL team's solution from December 2016.

## Not claimed
Optimality of any solution; anything about DK-HG-12's minimum infeasibility (12 hard violations stay); anything about the search method beyond how-we-built-it/. The Danish improvements are small (4 and 1 objective points at the record's infeasibility). The search started from the record solution stored in the instance file (panel/gate.md, disclosure 1). The searches were exploratory and not preregistered; the plan fixing the objects and checks was frozen after them (how-we-built-it/PREREG.md). The evaluator was written by the claimant's team from the HSEval specification; it reproduces all 57 values on the 8 open XHSTT-2014 dataset pages (how-we-built-it/evaluator-validation/), and a reviewer wrote a second one from the specification (panel/reproduce.md). HSEval itself was not run.

## Credits
XHSTT format and archive: Gerhard Post and colleagues (University of Twente, https://www.utwente.nl/en/eemcs/dmmp/hstt/); HSEval and its specification: Jeffrey Kingston. Instances: the contributors credited on each dataset page. Records compared against: George Fonseca, Haroldo Santos and Eduardo Carrano (GOAL team, 2016). Tools: OR-Tools CP-SAT. Run by the V3R1T4S kit: Charlie (Antigravity; search), Claude Code (lead agent; evaluator, checks and claim), with three fresh reviewer subagents.
