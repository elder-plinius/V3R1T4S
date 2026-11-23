# Preregistration (version 2): optimality certificates for 94 best known values (matsp)

Frozen by the lead agent (Andy) before claim/ is built. Version 1 (runs/2026-11-22-0847-matsp-lb, 99 rows) was not confirmed: its NOVELTY reviewer found that the TRA26 article (Trautsch and Kovari, Journal of Scheduling 2026, doi 10.1007/s10951-026-00886-z, open access) already proves instances 1, 4, 77 and 78 optimal (text) and instance 3 (CP lower bound equal to the upper bound, Table 5). Version 2 removes those five rows; nothing else changes. The bound was found in an exploratory screen of all 225 instances on 2026-11-22 (scans/2026-11-21-matsp-scout/zero/screen.py).

null_test: not needed because each certificate is an exact arithmetic inequality recomputed from the instance file; no statistic or chance enters the decision.

## Object
- data/certificates.csv (sha256 293c822d0facd4cf19347dce74a5b6ba7660f7f2db19936cc36690cf7907d17b): one row per instance whose best known penalty is positive, equals W - M (W = sum over employees of ceil(min minutes / 15), M = sum of all maximum-cover entries), and is not already proven optimal in the TRA26 article. 94 rows.

## Certificate (from ProblemDefinition.pdf)
Each employee works at least ceil(b_e / 15) intervals (constraint 4, 15-minute shift granularity); each on-duty interval carries exactly one activity (constraint 7), so total cover >= W; y_ia >= cover_ia - w_ia and y_ia >= 0 (constraint 8) give sum y >= W - M; the objective sum y^2 >= sum y for non-negative integers. Hence every feasible roster has penalty >= W - M; when W - M equals the best known value, that value is optimal.

## Checks
1. An independent checker (code/check_certificates.py) recomputes W, M and the bound for every row from data/instances1_225.zip and finds bound = best known > 0.
2. Each row's best known value matches the table fetched 2026-11-22T08:26:45Z (data/matsp.html).
3. No row is among the instances the TRA26 article proves optimal (1, 3, 4, 5, 77, 78; 5 has best known 0 and was never a row).
4. The table and the changes page are re-fetched before filing; a row whose best known value changed is dropped.
