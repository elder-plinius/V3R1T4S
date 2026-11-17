# CRITERION verdict: Hamburg full criterion

Own evaluator written from REPRODUCE.md definitions (work-criterion/ev.py), Dijkstra from all departure events at the origin to any arrival event at the destination over drive/wait/change arcs (change +5), sync/headway checked for feasibility only; every one of the 823 activities checked.

## Clauses
- Instance allowed: Hamburg is in the criterion list. I downloaded https://timpasslib.aalto.fi/data/Hamburg.zip (HTTP 200); Config/Events/Activities/OD sha256 equal claim/references/instance/instance_files.sha256 (efb780..., eae859..., 0a2dfb..., 605a20...). Same files.
- Format: Config.csv gives period_length 10, ean_change_penalty 5. Timetable has 508 events (all and only the Events.csv ids, each once), times all in 0..9.
- Feasibility, output of my check on object/Timetable.csv: `T 10 P 5 events 508 activities 823 violations 0`.
- Reproduce-first: posted best from claim/references/posted_best/: `total 140850920 routed 9694166 unreach 0` (exact).
- Is that the posted best file? Fetched https://timpasslib.aalto.fi/data/Hamburg/140850920_Timetable.zip (HTTP 200, zip sha256 2d8a43e9...), inner Hamburg-140850920-Timetable.csv sha256 aee78b5fc0d1015de2ca2ea31d8f03f699c843740d0e842eeeceee5f5cbd770a = sha256 of claim/references/posted_best/Hamburg-140850920-Timetable.csv. Identical; my evaluator on the downloaded copy gives 140850920.
- Live page: https://timpasslib.aalto.fi/solutions.html fetched `Tue Nov 17 08:33:09 UTC 2026`, HTTP 200, sha256 41aabc04358009c1be505a763c87686593567ad34e901809a37fd1a25f66128c. Hamburg solutions rows, first listed: total 140850920 (14.53 per pass., 31.08.2026, B. Ramos), then 141610697, 141629305. Bound 139892927 (not a win threshold).
- Object total, my evaluator: `total 140833625 routed 9694166 unreach 0`. 140833625 < 140850920 by 17,295 (0.0123%). Passengers routed 9,694,166 equals the page's Hamburg passenger total, so no OD was dropped. Strict inequality, no tie.
- Nothing submitted: CLAIM.md says so; I saw no submission artifacts (I did not audit logs).

## Stretch hunt
- Seeding from the 2023 published timetable: the criterion has no novelty or method clause; only feasibility and strict total. Not a stretch. The claim discloses it.
- Global cyclic shift: object differs from the posted best in ~285 of 508 events after best shift per claim; I did not need this since the total is strictly lower and the criterion does not require non-shift difference (that is p2). Anyway the total differs, so it cannot be a shift of the posted best (shifts leave totals unchanged).
- Hidden quantifiers: instance files are the official ones (hash match); page re-fetched by me minutes after claim's fetch (08:29:10Z) with no change at top; timing of "immediately before" is satisfied up to the claim's own fetch plus mine.
- Null model: pitfall (sync/headway carry no passengers) is respected, and including them would only lower the total, which my evaluator does not do; routing posted best with the same evaluator gives the posted total exactly, so the evaluator is calibrated to the page, and the object is scored by the identical code.
- Partial wins: p1/p2 not relevant, the full criterion is met for Hamburg. Subsumption: none; the claim is for Hamburg only.

## Cannot judge
Whether the site's own validator would accept the file (nothing is submitted); whether the instance's earlier lower totals exist off-page; independence of the claim's own scripts (I did not read provenance/).

confirmed_scope: The timetable in object/Timetable.csv is feasible for all 823 activities of the official Hamburg instance (T=10, times 0..9) and has total passenger travel time 140,833,625 by an evaluator that reproduces the posted best file 140850920 exactly, strictly below the 140,850,920 listed first for Hamburg on solutions.html on 2026-11-17 08:33 UTC.
context: fresh Claude Code subagent started by the run's lead agent with only this brief; read only claim/ (criterion.txt, REPRODUCE.md, CLAIM.md, references/, object/), the bank entry and POLICY.md; ignored auto-inserted workspace notes.
pass: true
