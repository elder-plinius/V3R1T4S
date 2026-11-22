# Multi-activity shift scheduling: 94 best known penalties proved optimal

## What

For each of the 94 instances listed in object/certificates.csv, the best known penalty on the schedulingbenchmarks.org matsp table fetched 2026-11-22T08:26:45Z is positive and equals W - M computed from the instance's TXT file, which by constraints 2, 3, 4, 7 and 8 and the non-negative-integer quadratic objective of ProblemDefinition.pdf is a lower bound on every feasible roster's penalty, so those best known values are optimal (subject to the filing-time re-fetch dropping any changed row).

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (POSIX shell, curl, sha256sum, Python 3 standard library; well under a minute, mostly the 21 MB download). It downloads the official instance archive and checks its sha256, then recomputes W, M and the bound W - M for every row from the instance files and checks that the bound equals the row's best known penalty. Expected last line: PASS.

## The certificate

For every feasible roster (ProblemDefinition.pdf): each employee works at least ceil(min minutes / 15) intervals (constraint 4, shifts in 15-minute steps); every on-duty interval carries exactly one activity (constraint 7), so total cover is at least W, the sum of those minima; over-cover y_ia >= cover_ia - max_ia and y_ia >= 0 (constraint 8), so the y sum to at least W - M, where M is the sum of all maximum-cover entries; and the penalty, a sum of y^2 over non-negative integers, is at least the sum of the y. So penalty >= W - M. Where W - M equals the best known penalty, that value is optimal.

## Compared to

The table (https://www.schedulingbenchmarks.org/matsp/, fetched 2026-11-22T08:26:45Z) lists best known values (all TRA26) and no lower bounds. The certified rows by size: L (70-100): 24, M (30-60): 25, S (10-20 staff): 16, XL (110-150): 29. The TRA26 article already proves instances 1, 3, 4, 5, 77 and 78 optimal; they are not claimed. Its lower bounds for other instances are much weaker (the-record-we-beat/snapshot.md).

## Not claimed

No new rosters are claimed here, and no instance whose best known value lies above the bound (123 instances, among them our separately filed rosters for instances 80 and 155). The certificate holds under ProblemDefinition.pdf, which makes the minimum workload hard; the site's XML instance files weight it as a soft constraint, under which this bound is not claimed. Optimality of a best known value assumes the TRA26 roster behind it is feasible; the site publishes no rosters. The certificate is a short derivation checked numerically and by reading, not a file in the VIPR format.

## Credits

Instances, definition and table: Tim Curtois and Yi Qu, [Shift Scheduling Benchmark Data Sets](https://www.schedulingbenchmarks.org/matsp/). Best known values and published bounds: Laszlo Kalman Trautsch and Bence Kovari, [Journal of Scheduling (2026)](https://doi.org/10.1007/s10951-026-00886-z). Run by the V3R1T4S kit: Claude Code (lead agent), with three fresh reviewer subagents.
