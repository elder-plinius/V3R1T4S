# PREREG.v3 (frozen 2026-11-11T10:48:43Z; execution order only, before any score of any audit case exists)

PREREG.md and PREREG.v2.md stay in force except for one change of execution ORDER. Measured pace: group
v2023-10-09 C took 178 s for 43 cases (about 4 s per case), slower than the development estimate, so the E1 cap
(11:25:00Z, unchanged) may cut the tail of the sequence. PREREG.v2 put the rerun of group v2022-10-05 PRE (the
largest group, 76 cases, whose first PRE run failed) after everything else, where the cap would most likely drop it.
Change: that rerun now runs immediately after the group in progress (v2023-10-09 PRE); the remaining groups then follow
in the unchanged seeded order of work/group_order.txt, C then PRE for each. Nothing has been scored; no output has been
opened except LIRICAL's logs for errors. Implementation: the old driver (bash PID 669) and the waiting rerun script
(bash PID 1705), both started by this run, are stopped by PID between JVMs; work/run_audit_v3.sh continues.
