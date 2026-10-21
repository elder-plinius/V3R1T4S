# Search provenance (copied from the run's attempts/search-engineer/)
code: mc2.c (sha256 6d02bdda5b8a00f0f577e71acb3dab80280042e4538867d2ac32237a1532fcfa, written 2026-10-16 11:33 CDT), ladder.sh (9708174d...b403), batch2.sh (62092e14...60f8). Compile: gcc -O2 -o mc2 mc2.c -lm.
command: ladder.sh 14 60 600 (inside batch2.sh; batch2.sh was launched at about 11:48 CDT but waited for the earlier batch to finish, so this ladder actually began at about 12:02 CDT (17:02Z), right after the earlier batch was stopped; PREREG was frozen at 16:33:32Z = 11:33 CDT). Size 60 started from random vectors; each next size started from the previous family plus one random vector.
seeds: the seed argument for size m is 14*1000+m (e.g. 14065 for m=65), XORed with 0x9E3779B97F4A7C15 inside mc2.c.
logs: lad_14_<m>.log (iterations, conflicts, seconds) for m=60..65; ladder_progress_utc.txt has the UTC time each size was found; the m=65 family file was written 2026-10-16 12:04:44 CDT (17:04:44Z) and is byte-identical to the claim's family file.
caveat: the time limit is wall-clock, so a rerun with the same seed is not guaranteed to retrace the same path; the claim rests on the checker, not on the search.
- lad_14_66.log: the failing next size (m=66, not found in 600 s), where the ladder stopped.
