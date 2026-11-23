# Reproduce verdict
context: fresh subagent started for this claim only

Claim: runs/2026-11-23-2106-fjsspw139/claim (136 FJSSP-W schedules, each claimed at least 1 below the rounded live UB; total saving 1367).
Reviewer read only claim/ (REPRODUCE.md, CLAIM.md, criterion.txt, references/, status/, object/) before its own results; claim/provenance/ was opened only after step 5's own comparison. Nothing was written inside claim/. Work folder: panel/work-reproduce/.

## Method

1. **Own checker** (panel/work-reproduce/checker.py, sha256 28d66510c6130880b4de091cd4f05dde5da1830b6f366e15b7ae2c62d59eda85; standard library, `python3 -I`, `PYTHONDONTWRITEBYTECODE=1`), written from REPRODUCE.md alone:
   - Instance: one integer stream; 3-header parse, falling back to 4 only if the 3-header parse does not consume the file exactly (all 136 parse with 3 header numbers, no trailing tokens). Rejects machine/worker ids out of range, duplicate machines in an operation, duplicate (machine, worker) pairs, negative durations.
   - Schedule: top-level keys exactly {instance, ops}; instance field equals the file name; each record 6 non-bool integers; known (job, op); no duplicate op; (machine, worker) allowed for that op; duration equals that pair's duration; start >= 0; all ops present; job order (op i starts >= end of op i-1); no machine overlap and no worker overlap on half-open intervals (sweep per resource, then an independent O(n^2) pairwise check); makespan = latest end.
   - Row: UB from the table rounded half-up (Decimal); pass iff schedule valid and makespan <= round(UB) - 1.
2. Ran on all 136 rows twice: identical output (sha256 b0b1fb40... for both runs), 136/136 PASS, run time about 3 s.
3. **Instances**: downloaded all 136 .fjs files from the pinned-commit URLs (raw.githubusercontent.com, commit eb1d28381c34525b58736965cddbeb89e095f88a, all HTTP 200). sha256 of downloads = claim/references/instances.sha256 = the claim's copies in references/instances/ (136/136 identical). The checker re-run on the downloaded instances and the live table gives byte-identical output to the first run.
4. **Tables**: live best_known.csv fetched 2026-11-23T19:16:56Z (HTTP 200), sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf = claim's references/best_known.csv = the copy at the pinned commit = status/table-fetch.txt. Pinned data.csv sha256 93debe7b... = claim's copy.
   - Row mapping (mapcheck.py): the naming rule (Behnke->behnkegeiger, BrandimarteMk->brandimarte, DPpaulli->dppaulli, Hurink?data->hurink?data, lower-cased) maps all 402 data.csv sources onto all 402 table rows; for each of the 136 entries of row_to_file.json the rule gives exactly that row, the source occurs exactly once in data.csv, and data.csv's n_jobs, n_machines, n_worker, n_operations, d_max, d_min equal the values computed from the instance file. 0 mapping problems.
   - All 136 UBs are already integral in the table (no float noise on these rows); every makespan <= round(UB) - 1.
5. **CLAIM.md table** (tablecmp.py): 136 rows, 136 distinct files; for every row the listed UB, our makespan and saving equal mine; total saving 1367 (mine 1367). Every row also has UB > LB in the live table (relevant to p1/p3). Family counts match criterion.txt (Behnke 34, BrandimarteMk 7, DPpaulli 16, Hurinkedata 13, Hurinkrdata 30, Hurinksdata 5, Hurinkvdata 31). Each makespan is also below the claim's "closest public" and "lowest public reported" columns (authors' numbers, not checked by me).
   - Then opened claim/provenance/rows.csv (provcmp.py): 136 rows; row, table_ub, makespan, saving, object_sha256 (vs sha256 of claim/object/<file>.json) and instance_sha256 all agree; 0 problems. provenance/object_list.csv lists 139 cells; the 3 extra (DPpaulli1 2485, Hurinkrdata28 773, Hurinkvdata18 1038) are exactly the rows the claim says it dropped (references/public-results-screen.txt) and are not in the claim.
6. **Negative tests** (negtests.py, negfallback.py; corrupted copies in panel/work-reproduce/neg/), on all 136 rows (not just 20):
   - duration +1: 136/136 rejected (duration mismatch);
   - duration -1: 136/136 rejected;
   - one operation removed: 136/136 rejected (op count);
   - duplicated operation: 136/136 rejected;
   - worker-only clash on two different machines (an op reassigned to another op's worker on an allowed pair with its true duration, overlapping in time, machine and precedence constraints verified still clean): built and rejected 136/136, every reason "worker N overlap";
   - precedence-only violation (op starts before its predecessor ends, machine/worker still clean): built and rejected 128/128; for the 8 rows where no resource-clean variant existed (BrandimarteMk11, Hurinkrdata10/12/17, Hurinkvdata9/10/16/37) a plain precedence violation was built and rejected 8/8 with reason "precedence";
   - last-ending op delayed so makespan = round(UB): 136/136 rejected by the row rule.
   No corrupted copy was accepted.

## Results

- Rows passing: **136 of 136**. Failing rows: none.
- Two runs identical; result also identical with the freshly downloaded instances and live table.
- Instance hashes: 136/136 match (download = list = claim copy). Table and data.csv hashes match.
- CLAIM.md table and provenance/rows.csv: 0 discrepancies.
- 32,297 scheduled operations, none with zero duration (so the half-open convention never relies on zero-length intervals).

## Not checked

- Whether the 136 cells overlap other V3R1T4S pull requests (#868, #1081) or any public result: outside this reproduce role (no GitHub API access was permitted beyond the named raw URLs); the claim's public-values columns are the authors' and were not re-derived.
- The search method and provenance code (provenance is not evidence; only rows.csv / object_list.csv were compared).
- The live table can change after 2026-11-23T19:16:56Z; it was identical to the claim's copy at that time.

pass: true
