# Novelty review: set5, 2,305 vs OptHub 2,327

context: fresh Claude Code subagent started by the run's lead agent with only this brief (workspace notes auto-inserted into my context, if any, were ignored; I read only claim/ and public web/GitHub).

## Fetched once
- URL: https://opthub.uniud.it/problems/timetabling/edutt/ett/itc-2007-ett
- UTC: Sun Nov 15 03:14:53 2026 (date -u); HTTP 200; no retry.
- Value: embedded JSON row "instance_id":"set5" has "best_solution":"2,327" (matches claim/status/table-fetch.txt).
- OptHub storage listing for solutions/set5/: only exam5.sol and set5.sol, both Last-Modified 2026-01-23. No newer file.

## Searched
- V3R1T4S repo (gh, read-only): PR search for itc2007 / timetabling / exam / set5: no PR; scanned the latest 100 PRs by title: none on ITC-2007. One open issue, #1092 (set4's posted best not reproducible), nothing about set5. TROPHY_CASE.md has no ITC-2007/set5 entry; the only mention is the target file known-unknowns/optimization-benchmarks/itc2007-exam-timetabling-bks.md. known-knowns/ has no timetabling item. No releases.
- github.com/davidvanbulck/ITC-2007-CETT: no releases; tree has InitMethods/SolStore initial solutions, easylocal; no set5 result better than 2,327 found by filename scan (I did not open all files).
- OpenAlex: works citing Van Bulck/Goossens/Schaerf 2023 (doi 10.1007/s10951-023-00799-1) since 2024-06 and ITC-2007 exam-timetabling searches since 2024-11 (e.g. "Multi-neighborhood local search with room split balancer", 2025; "Exam Timetabling ... Cooperative Hyper-Heuristics ... ITC2007", 2025-11; robust exam timetables 2024). I read titles only, not full text, so I cannot rule out a table in them reporting set5 below 2,327. Nothing seen suggests a set5 value under 2,327.
- Limit: not exhaustive; no web full-text search of those papers' tables.

## Trivial-edit analysis
- Object is seeded from Bykov's posted set5.sol (named in claim; sha matches OptHub's record). 926 of 1,018 exams differ (774 periods, 674 rooms), so it is not a deletion, restriction, relabelling or a few-move polish.
- Lineage (provenance/rescore.txt): 20 s SA from posted -> 2325; 120 s -> 2318; another 120 s from posted -> 2312; 3,600 s from the 2312 file -> 2305. A 3,600 s run from the posted file at T0 6 stayed at 2,327.
- Authors' control (provenance/hillclimb_control.txt): improving-only 30 s gives 2327 and 2326.
- My own control: compiled claim/provenance/code/sa.cpp, ran improving-only (T0 = 1e-6) from the posted file, 300 s, seeds 11, 12, 13: best 2324, 2324, 2326. Outputs in work-novelty/. So plain polish of the posted file gives about 2324, 19 above the claimed 2,305. (Not as long as the 3,600 s of the claim's path; a much longer polish might reach lower, untested.)
- Judgement: the object beats what polish alone gives by a clear margin and is the product of a stochastic search, not a trivial edit. Caveat: I did not independently rescore 2,305 or hard-feasibility (outside the novelty role); that is for the other skeptics.

## Verdict
No published or posted set5 value below 2,327 found; seed named; beats polish controls. Neighbouring cells irrelevant (single instance). Pass on novelty, conditional on validity being confirmed elsewhere.

pass: true
