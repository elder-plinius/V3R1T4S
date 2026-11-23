# Multi-activity shift scheduling, instance 80: a roster with penalty 0 (best known 6)

## What

For instance 80 (80_14_10_2) of the schedulingbenchmarks.org multi-activity set, the roster object/80_14_10_2.Solution.0.xml satisfies every hard constraint of ProblemDefinition.pdf and has total penalty 0 under two independent checkers that reproduce 889 on 8_7_20_2.Solution.889.xml, strictly below the best known value 6 (TRA26) shown on the table and Changes page as fetched 2026-11-22T08:03:12Z and unchanged at 08:08:03Z.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (POSIX shell, curl, sha256sum, Python 3 standard library; well under a minute, mostly the 21 MB download). It checks the hashes, downloads the instance archive and the site's example solution and checks their sha256, confirms the evaluator reproduces the example's posted penalty 889, then evaluates the claimed roster: every hard constraint of ProblemDefinition.pdf and the penalty. Expected last line: PASS.

## Compared to

| instance | best known (table) | reference | ours |
|---|---|---|---|
| 80 (80_14_10_2) | 6 | TRA26 | **0** |

Table https://www.schedulingbenchmarks.org/matsp/ fetched 2026-11-22T08:03:12Z and re-fetched unchanged at 2026-11-22T08:06Z (the-record-we-beat/). The penalty is a sum of squared over-cover counts, so 0 is optimal.

## Not claimed

No other instance is claimed here. The closed-source official verifier was not run by any agent; the roster follows the site's example format (0-based days) but omits the schema reference, the metadata fields and the WorkLength attribute, which equals Length in every task of the example, and the site's Solution.xsd is not published, so a format rejection by the official tool cannot be ruled out (panel/gate.md). The TRA26 journal article and its supplement could not be read (publisher login); the table, which takes its values from that work, lists 6. The roster was found by an exact CP-SAT model of the whole definition (how-we-built-it/code/cpsat_matsp.py), run for 300 s with 4 workers and seed 1, which proved penalty 0 optimal after 81 s.

## Credits

Instances, definition and table: Tim Curtois and Yi Qu, [Shift Scheduling Benchmark Data Sets](https://www.schedulingbenchmarks.org/matsp/). Current best known values: Laszlo Kalman Trautsch and Bence Kovari, [Journal of Scheduling (2026)](https://doi.org/10.1007/s10951-026-00886-z). Tools: OR-Tools CP-SAT. Run by the V3R1T4S kit: Claude Code (lead agent, solver and claim), with three fresh reviewer subagents.
