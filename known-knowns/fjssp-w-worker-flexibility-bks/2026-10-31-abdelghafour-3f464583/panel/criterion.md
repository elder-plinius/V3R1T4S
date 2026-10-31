# CRITERION skeptic verdict: fjssp-w-worker-flexibility-bks, partial win p2 (95 instances)

context: subagent (Claude Code Agent tool, fresh context)
inputs read: claim/ only (CLAIM.md, REPRODUCE.md, SHA256SUMS, best_known.csv, data.csv, name_map.csv, fjsspw_check.py, instances/, schedules/), plus live raw fetches from github.com/jrc-rodec/FJSSP-W-Benchmarking.

## Literal reading
- p2: "Strict improvements on at least 10 distinct FJSSP-W instances, each verified by the checker."
  - "strict improvement" = checker-computed makespan strictly below the instance's UB in the live best_known.csv (that is how the full criterion defines a win; the claim uses the stricter test makespan <= round(UB) - 1).
  - "distinct" = different instance files / different table rows. Checked against file names, table rows and file contents (95 different sha256 values, so no duplicates under another name).
  - "each verified by the checker" = every instance checked on its own, no aggregate or average. Checked per instance.
- Full criterion conditions carried into p2: the instance is from instances/Example_Instances_FJSSP-WF; the UB comes from the live best_known.csv; the file-to-row mapping is confirmed from data.csv; nothing is submitted. All hold (below).

## Checks run (2026-10-31T12:37Z)
1. Live re-fetch: best_known.csv HTTP 200, sha256 74f982d5...30cf; data.csv HTTP 200, sha256 93debe7b...d67f. Both byte-identical to the claim copies and to the hashes the scout recorded. Repo main HEAD = eb1d28381c34525b58736965cddbeb89e095f88a, the commit the claim cites.
2. Instance files: I fetched all 95 raw files from Example_Instances_FJSSP-WF at both main and eb1d283 and compared sha256: 95/95 byte-identical to claim/instances (0 mismatches). claim SHA256SUMS also verifies.
3. Mapping: every file stem appears as `source` in data.csv. The rule (lowercase; Behnke->behnkegeiger; BrandimarteMk->brandimarte) maps all 402 data.csv sources one-to-one onto the 402 best_known.csv rows. For all 95 files, name_map.csv and the CLAIM table both name the rule-derived row. (data.csv rows are not in the same order as best_known.csv, so the mapping is by name, not by position. That is acceptable.)
4. UB/LB: the header is `Instance;UB;LB`, and every UB is an integer-valued float (so rounding is a no-op). round(UB) and round(LB) match the CLAIM table for all 95 rows. UB > LB holds for all 95.
5. Independent recheck: I wrote my own parser and checker, separate from fjsspw_check.py. For each instance it checks: every operation scheduled exactly once, (machine, worker) pair eligible, pair-specific duration used, job precedence, machine no-overlap, worker no-overlap, starts >= 0. All 95 are valid, and every recomputed makespan equals the claimed one.
6. Strictness: makespan <= round(UB) - 1 for all 95. The smallest margin is 1 (Behnke2 85 vs 86, and several others); the largest is 171 (Hurinkrdata53 5410 vs 5581).
7. Null/sanity: no makespan is below its raw LB, which would have pointed to a checker or format bug. Hurinkvdata58 reaches its LB (560 = LB), so it is provably optimal and consistent. The large margins on some Hurink rows (e.g. 171, 156) suggest those table UBs are loose. That does not affect the literal criterion, which compares only against the table.
8. Count: 95 distinct instances >= 10.

## Hidden quantifiers / stretched definitions
- No stretching found. The claim does not average, aggregate, or count near-misses, and it does not depend on rounding. Every one of the 95 meets the test individually.
- Bundling: p2 is defined over a set of at least 10 instances, so a multi-instance bundle is the natural unit. Each instance's evidence (file, row, UB, schedule, recheck) stands alone, so any subset of 10 or more would also meet p2. Bundling 95 is appropriate. It does not mean "95 separate wins"; it is one p2 win.
- Subsumption: p2 (>= 10 instances) is not implied by the full criterion (which needs one instance). The same evidence also literally meets the full criterion and p1/p3. I have no visibility into any earlier claimed or awarded wins outside claim/, so "not subsumed by an earlier award" is unverified from my side.
- Literature/novelty (whether these beat published results beyond best_known.csv) is left to the separate NOVELTY panelist and is not part of this scope.

confirmed_scope: For 95 distinct instance files in instances/Example_Instances_FJSSP-WF (sha256-identical to repo commit eb1d283, the current main HEAD), the supplied schedules pass an independently recomputed check of eligibility, pair durations, job precedence and machine/worker no-overlap, with makespans 1 to 171 below the integer UB of the data.csv-confirmed row of best_known.csv as re-fetched live at 2026-10-31T12:37Z (UB > LB in every case), which meets p2's threshold of at least 10 instances; novelty against the literature beyond that table is left to the NOVELTY panelist.

pass: true
