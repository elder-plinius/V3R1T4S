# Criterion skeptic: verdict on claim mmlib-multimode-rcpsp-ub (run 2026-11-20-1014)

context: fresh subagent started for this claim only

Read only: CLAIM.md, target.md, PREREG.md, REPRODUCE.md, SHA256SUMS, PREREG.sha256, data/, object/schedules/, evidence/*.output.txt. I did not run code/mm.py or code/verify_claim.py; I wrote my own checker (stdlib, scratch only), described below.

## Integrity
- `sha256sum -c SHA256SUMS`: all OK. PREREG.md matches PREREG.sha256. data/selected_wins.json matches the sha256 frozen in PREREG.md.
- data/MMLIB_v2_1.zip sha256 = 4f6f5318...2fecd, identical to the asset digest in data/release.json (tag v2.1, published 2026-06-23, the release target.md names as latest).
- The 30 instance files in MMLIB_v2_1/MMLIB+.zip inside data/MMLIB_v2_1.zip are byte-identical to the SolutionsUpdate copies in data/MMplus.zip (I compared all 30).

## Clause by clause (target.md, "What counts as a win")
1. **"A mode assignment plus start times"**: each object/schedules/*.json has one mode per job and one start per job (n entries, dummies included). Met.
2. **"one MMLIB50, MMLIB100, MMLIB+ or Boctor100 instance that is open (LB < UB) on its SolutionsUpdate dataset page"**: all 30 are MMLIB+ and have LB < UB in data/MMplus_2.csv (the per-instance file of dataset mmplus); the ID-to-file mapping in that CSV matches each schedule's file name. The CSV has 3,240 rows, no duplicate IDs, and 1,965 open rows, which matches the MMplus row (3240 / 1965 open) of the status page data/mrcpsp.html. Met. Provenance gap (minor): the dataset/mmplus HTML page is not saved, so the evidence that MMplus_2.csv / MMplus_2_BKS.csv are the files linked from that page at fetch time is the claim's assertion plus the consistent 1,965 count, not a saved page.
3. **"an independent checker confirms precedences, renewable capacities in every period and non-renewable totals"**: my own checker (below) confirms all 30. Met.
4. **"makespan strictly below both that instance's value in the best-known-solution CSV ... and its UB-lit in the latest MMLIB release Excel"**: for all 30, makespan < value in data/MMplus_2_BKS.csv and < column O ("UB-lit") of sheet MMLIB+ of 'MMLIB (Parameters and BKS).xlsx' in data/MMLIB_v2_1.zip. Also < UB in data/MMplus_2.csv and >= LB (no contradiction with a listed lower bound). For 2717, 2841, 2843, 3117 the Excel UB-lit is higher than the CSV value; the CSV value is the binding one and is still beaten. Total improvement against min(CSV UB, BKS, UB-lit) = 34 (26 by 1; 2178, 2299, 2842, 2987 by 2), as claimed. Met.
5. **"all re-fetched live immediately before claiming"**: data/status-utc.txt = 2026-11-20T10:14:46Z; PREREG.md frozen 10:20:52Z; claim built within minutes after. For this freeze the clause is met. The status page is still headed "September 2026" (same table as target.md's 2026-10-28 check). A claim is only as fresh as its fetch: PREREG.md correctly requires re-fetching both CSVs and the release before filing and dropping any instance whose UB is now <= our makespan. A filing must carry the new fetch time, and the scope below is bound to 10:14:46Z.

## Hidden quantifiers, stretched definitions
- **Bundling 30 instances**: the criterion is per instance ("one ... instance"). The claim says each instance meets it on its own, and I judged each separately: 30 independent full-criterion wins, not one stretched win. Bundling adds no quantifier as long as a later re-fetch can remove instances one at a time (PREREG.md says it does).
- **Exploratory, not preregistered search**: irrelevant to the criterion. The object is an exact schedule judged against published values; there is no statistic and no selection effect that could make an infeasible or non-improving schedule pass. PREREG.md fixes the object (30 schedules, hash-frozen), which is what matters.
- **8 warm starts from posted schedules** (1767, 1768, 2450, 2717, 2841, 2843, 2854, 3117): the criterion asks for a feasible schedule strictly below the BKS; it does not care where the search started. Each still differs from the posted schedule in 18-46 modes (evidence/warm_start_edits*.output.txt), and for 4 of them (2450, 2717, 2854, 3117) re-timing the posted modes is shown OPTIMAL at the old UB, so changing modes was necessary. For the other 4 that question is undecided, which bears on credit and novelty, not on the criterion. Disclosed in CLAIM.md; acceptable.
- **Partial wins**: the full criterion subsumes mmlibplus-improve-any. The claim is for the full criterion, not a weaker partial win.
- **Lower bounds**: none claimed. No instance is claimed as closed.

## Independent check (code-independent of code/)
A stdlib parser for the .mm format: header counts, precedence table, REQUESTS/DURATIONS with continuation lines, RESOURCE AVAILABILITIES. It checks mode ranges, every successor precedence (start + duration <= successor start), non-renewable totals, and renewable usage in every integer period [0, makespan), then compares with the CSV, BKS and Excel values. It runs on the instance files taken from MMLIB+.zip inside data/MMLIB_v2_1.zip.
- **All 30 schedules (not just 5)**: VALID, recomputed makespan equals the claimed makespan, and the instance is open and beaten on all three references.
- **Null model / checker sanity**: the same checker reproduces the posted BKS schedules in data/MMplus_2_BKS.csv for all 8 warm-start instances, exactly at their posted values (32, 32, 76, 75, 92, 77, 79, 53). It rejects 85 of 85 random single-job mutations of the claimed schedules (start one job 1 unit earlier, or change its mode). So it is not vacuously accepting.

## Residual cautions (not disqualifying)
- Dataset page HTML not saved; the CSV provenance is inferred (see clause 2).
- Freshness holds only as of 2026-11-20T10:14:46Z; any filing must re-fetch and prune per PREREG.md.

confirmed_scope: Each of the 30 MMLIB+ schedules in object/schedules/ is, by an independent checker run on the v2.1 release instance files, a feasible multi-mode schedule whose makespan is strictly below that instance's UB in data/MMplus_2.csv, its value in data/MMplus_2_BKS.csv and its UB-lit in the MMLIB v2.1 release Excel, on instances open (LB < UB) in data/MMplus_2.csv as fetched 2026-11-20T10:14:46Z (34 makespan units in total).

pass: true
