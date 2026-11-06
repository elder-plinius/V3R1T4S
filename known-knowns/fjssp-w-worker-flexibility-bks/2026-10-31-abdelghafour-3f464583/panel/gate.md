# Honesty gate (main session), FJSSP-W partial win p2

reproduce: pass: true (own checker written first, plus the claim's checker: all 95 schedules VALID, makespans match)
novelty: pass: true (best_known.csv re-fetched by the panelist at 2026-10-31T12:36:55Z; 91 of 95 strictly below everything
found. Dropped: hurinksdata61 826 and hurinksdata63 373, tied by valid schedules in jrc-rodec/FJSSP-W-Competition issue #11;
hurinkedata6 and hurinkrdata50, lower values reported in issue #14 whose schedules fail worker no-overlap, excluded to be safe)
criterion: pass: true (p2: at least 10 distinct instances; bundling judged appropriate because p2 is defined over a set)
Main-session review: all three files read; none hedges; three fresh subagent contexts that saw only claim/; panel fetch under
6 hours old; no evasion. Main session also checked that the competition repo holds neither BrandimarteMk4 nor ChambersBarnes1.
Downgrade applied: the confirmed set is the 91 survivors only; the package holds those 91 objects and lists the 4 as not claimed.

status: CONFIRMED_PARTIAL
confirmed_scope: For 95 distinct instance files in instances/Example_Instances_FJSSP-WF (sha256-identical to repo commit eb1d283, the current main HEAD), the supplied schedules pass an independently recomputed check of eligibility, pair durations, job precedence and machine/worker no-overlap, with makespans 1 to 171 below the integer UB of the data.csv-confirmed row of best_known.csv as re-fetched live at 2026-10-31T12:37Z (UB > LB in every case), which meets p2's threshold of at least 10 instances; novelty against the literature beyond that table is left to the NOVELTY panelist.
