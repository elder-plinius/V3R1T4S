# CRITERION verdict

context: fresh Claude Code subagent started by the run's lead agent with only this brief (no workspace notes were auto-inserted that I used).

## Clause by clause
- .sol format: object/set5.sol has 1018 lines "period, room", equal to the 1018 exams in references/set5.exam; all periods in 0..41, rooms in 0..2. Met.
- Independent checker: I wrote my own evaluator (panel/work-criterion/chk.py) from the archived evaluation page, before opening provenance/. Weights are read from [InstitutionalWeightings] (TWOINAROW 40, TWOINADAY 15, PERIODSPREAD 5, NONMIXED 0, FRONTLOAD 250,30,10); same-day only for two-in-row / two-in-day; spread counts shared students for exam pairs at distance 1..5 periods; front load = exams among the 250 largest in the last 30 periods; room/period penalties per use.
- Reproduce-first: my checker gives 2327 for references/opthub_posted_best_set5.sol (spread 957, front 1370, all others 0), hard-feasible. Met.
- Is it the posted best file: I downloaded set5.sol live from the OptHub storage URL (HTTP 200); sha256 b83fcb6a83b95961b08e58fac2a1c9cd547d2024ad3d3553469615869062ee00, byte-identical to references/opthub_posted_best_set5.sol and equal to the sha OptHub's set5 instance page records (Yuri Bykov, 2327.0). Met.
- Hard-feasible: my checker finds 0 violations of conflicts, room capacity, period duration, coincidence, exclusion, after (strict), room-exclusive for object/set5.sol. Met.
- Total soft penalty: object/set5.sol = 2305 (spread 945, front 1360, rest 0).
- Live re-fetch: I fetched https://opthub.uniud.it/problems/timetabling/edutt/ett/itc-2007-ett at 2026-11-15T03:15:04Z, HTTP 200; the set5 row best_solution = "2,327"; the set5 instance page (HTTP 200) lists 2327.0 as best. 2305 < 2327 strictly. Met (and consistent with the run's own fetch 03:03:36Z).
- Nothing uploaded: nothing indicates any upload; the claim lists none. Met as far as observable.

## Ambiguity hunt
- Front-load tie handling: the 250th largest size (47) is shared by 4 exams, one of which must be selected; which one is not specified. Over every possible selection, the posted file scores 1370..1380 and the object 1360..1370. Reproduction of 2327 pins the rule; under the reversed tie rule (not reproducing) the object is 2315 vs posted 2337. Worst-case for the object under any rule is 2315 < 2327, so the verdict cannot flip. 
- Spread boundary (<= 5 vs < 5): fixed by the reproduce-first match (2327 exact, with component split matching the authors').
- Margin is small (22, ~0.9%) but is exact integer arithmetic, not a stretched definition. Null model: an improving-only local search control reached only 2326 in 30 s; the claimed object came from annealing, which is legitimate; provenance does not affect the criterion.
- Partial wins: the full criterion is met for set5 (one of set1-set12). p2 (strictly better for set1-set10 other than set11/12) is also met by set5 and is subsumed by the full criterion; p1/p3 not claimed.

confirmed_scope: For ITC-2007 exam instance set5, claim/object/set5.sol is hard-feasible and scores 2305 under an independently written evaluator that gives 2327 for OptHub's posted set5.sol (sha256 b83fcb6a...ee00), strictly below OptHub's live best of 2,327 (fetched 2026-11-15T03:15:04Z, HTTP 200), robust to front-load tie-breaking; nothing about other instances or optimality.
pass: true
