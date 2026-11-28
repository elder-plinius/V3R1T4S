# TimPassLib Hamburg: a timetable with total passenger travel time 140,833,625 (posted best 140,850,920)

## What
The timetable in object/Timetable.csv is feasible for all 823 activities of the official Hamburg instance (T=10, times 0..9) and has total passenger travel time 140,833,625 by an evaluator that reproduces the posted best file 140850920 exactly, strictly below the 140,850,920 listed first for Hamburg on solutions.html on 2026-11-17 08:33 UTC.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. It downloads the Hamburg instance and the posted best timetable from the TimPassLib site (about 70 KB), checks both hashes, reproduces 140,850,920 for the posted best with the evaluator in verify-it-yourself/evaluate.py (written from the benchmark's description, standard library only), then requires object/Timetable.csv to be feasible with total 140,833,625. Seconds on a laptop.

## Compared to
The best total shown for Hamburg on https://timpasslib.aalto.fi/solutions.html, 140,850,920 (B. Ramos, 2026-08-31), page fetched 2026-11-17T08:29:10Z, sha256 41aabc04358009c1be505a763c87686593567ad34e901809a37fd1a25f66128c (the-record-we-beat/record.md). The other listed solutions are 141,610,697 (Loebel and Lindner, 2025) and 141,629,305 (Schiewe, Goerigk and Lindner, 2023); the listed lower bound is 139,892,927.

| quantity | value |
|---|---:|
| posted best (B. Ramos), reproduced | 140,850,920 |
| this timetable | 140,833,625 |
| difference | 17,295 (0.0123%) |

## Not claimed
Optimality (the listed lower bound is 139,892,927); anything about any other instance; that the search is a new method (it is large-neighbourhood search with CP-SAT; how-we-built-it/ is provenance). The search was exploratory and not preregistered; the plan that fixes the object and the rule was frozen afterwards (how-we-built-it/PREREG.md). The timetable was found by a search seeded from the 2023 timetable of Schiewe, Goerigk and Lindner; after removing the best global cyclic time shift it differs from that timetable in 280 of 508 events, from the 2025 timetable in 284 and from the posted best in 285 (how-we-built-it/distance_to_published.txt). Results are against the page as fetched at the time above.

## Credits
- TimPassLib benchmark and site: P. Schiewe, M. Goerigk and N. Lindner, "Introducing TimPassLib - a library for integrated periodic timetabling and passenger routing", Operations Research Forum 4:64 (2023), https://doi.org/10.1007/s43069-023-00244-1; hosted at Aalto University (https://timpasslib.aalto.fi).
- Hamburg instance data: S-Bahn Hamburg network, Open Data Portal of Deutsche Bahn AG (CC-BY 4.0), as processed by the benchmark.
- The published Hamburg solutions we compared with and started from: B. Ramos (2026), F. Loebel and N. Lindner (2025), P. Schiewe, M. Goerigk and N. Lindner (2023).
- OR-Tools CP-SAT (Google) for the optimisation model.
