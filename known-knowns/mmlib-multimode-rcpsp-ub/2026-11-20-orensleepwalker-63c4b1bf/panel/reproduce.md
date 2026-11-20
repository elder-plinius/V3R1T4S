# REPRODUCE review: mmlib-multimode-rcpsp-ub (30 MMLIB+ instances)

context: fresh subagent started for this claim only

Scope: only claim/ was read (CLAIM.md, target.md, PREREG.md, REPRODUCE.md, then data/, object/, and code/ last). All work ran on a scratch copy; claim/ was not modified.

## Criterion (quoted from target.md, "What counts as a win")
> A mode assignment plus start times for one MMLIB50, MMLIB100, MMLIB+ or Boctor100 instance that is open (LB < UB) on its SolutionsUpdate dataset page, that an independent checker confirms satisfies precedences, renewable capacities in every period and non-renewable totals, with makespan strictly below both that instance's value in the best-known-solution CSV linked from http://solutionsupdate.ugent.be/dataset/<mm50|mm100|mmplus|boctor100> and its UB-lit in the latest MMLIB release Excel, all re-fetched live immediately before claiming.

## Independent checker (written before reading claim/code/)
- My own .mm parser: reads job count, renewable/non-renewable/doubly-constrained counts from the header (asserts D = 0), the precedence table (checks job numbering, the successor count, and that the mode count matches the request table), the request table (tells job lines from continuation lines by token count, checks the mode order) and the availabilities.
- Checks: one integer mode per job in 1..M_j; integer starts >= 0; each non-renewable total over all jobs <= availability; every precedence S_i + d_i <= S_j; renewable usage in every period t in [S, S+d) <= capacity for each resource; makespan = latest finish, which must equal the stated makespan and the sink's start.
- Instances come from data/MMLIB_v2_1.zip -> MMLIB_v2_1/MMLIB+.zip. The Excel was parsed with the standard library: the sheet was found through workbook relationships, sheet 'MMLIB+', columns found from the header row (FileName = D, UB-lit = O).

## Checker validation
- Posted best-known schedules in data/MMplus_2_BKS.csv: 2,570 of 3,240 rows carry a schedule. I checked all 2,570 (more than the requested sample). All 2,570 were accepted, each with exactly its listed value.
- Corrupted copies (100 random BKS schedules): precedence violated by moving one tight successor 1 earlier, all starts set to 0, every job switched to its most non-renewable-hungry mode, mode out of range. A further 50 had renewable capacity set 1 below the schedule's peak. All 450 of 450 were rejected with the expected kind of violation. All 50 were accepted again at capacity = peak.

## The 30 schedules (object/schedules/*.json, all 30 checked)
- All 30 are feasible under my checker, and each computed makespan equals the stated one. This holds for 30 of 30.
- All 30 instances are open (LB < UB) in data/MMplus_2.csv.
- The makespan is strictly below the dataset UB, the BKS value and the Excel UB-lit, and >= LB, for 30 of 30. For 26 instances UB, BKS and UB-lit are equal. For 4 the Excel UB-lit is higher than the site's value (2717: 76 vs 75, 2841: 94 vs 92, 2843: 79 vs 77, 3117: 54 vs 53), and the claim beats the lower of the two in every case.
- Improvement against the dataset UB: 34 units in total, 26 instances by 1 and 4 by 2 (2178, 2299, 2842, 2987). This matches CLAIM.md.
- The release copy and the SolutionsUpdate copy (data/MMplus.zip, MMplus/<file>) are byte-identical for all 30 instance files.
- The objects match data/selected_wins.json: modes, starts, makespan and warm-start flag, 30 distinct instances, 8 warm-started. That file's sha256 equals the one frozen in PREREG.md.
- Two runs of my checker gave byte-identical output.

## REPRODUCE.md steps 1-2
- Step 1: `sha256sum -c SHA256SUMS` passed on all 49 entries, including the 30 schedules. `sha256sum -c PREREG.sha256` gave OK for PREREG.md and data/selected_wins.json.
- Step 2: `python3 code/verify_claim.py .` printed "30 of 30 schedules verified, 34 points below the current UBs" and then PASS (rc 0). Each line matches my independent results: the same LB, UB, BKS, Excel UB-lit and makespan for all 30.
- Minor robustness note on code/verify_claim.py: it picks the worksheet as sheet<index+1>.xml instead of following the workbook relationships. That gives the correct sheet here, which my relationship-based reader confirms, so it does not affect this result.

## Limits
- I did not re-fetch the live site. The comparison uses the snapshots in claim/data (status-utc 2026-11-20T10:14:46Z, release v2.1 published 2026-06-23 per data/release.json).
- Lower bounds are not checked, as target.md says. The claim does not depend on them beyond LB <= makespan.
- REPRODUCE.md step 4 (the warm-start evidence) was not rerun. It discloses how the schedules were found, and it does not affect whether they are feasible or beat the bounds.

pass: true
