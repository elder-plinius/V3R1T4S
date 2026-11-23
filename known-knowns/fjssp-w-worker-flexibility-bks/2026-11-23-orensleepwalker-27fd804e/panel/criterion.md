# Criterion verdict
context: fresh subagent started for this claim only

Claim: runs/2026-11-23-2106-fjsspw139/claim (136 FJSSP-W schedules). Target: fjssp-w-worker-flexibility-bks.
Inputs I read: claim/ only, repo/bank/targets.json (this entry), repo/known-unknowns/optimization-benchmarks/fjssp-w-worker-flexibility-bks.md, repo/kit/POLICY.md, repo/kit/RULES.md. Work files: panel/work-criterion/ (check.py, compare.py, neg.py, rows_checked.csv, fetch.txt, dl/).

## Verbatim criterion (repo/bank/targets.json, id fjssp-w-worker-flexibility-bks)

Success criterion:
> For one of the 402 instances in instances/Example_Instances_FJSSP-WF, an assignment of each operation to an eligible (machine, worker) pair with start times such that an independent checker written from the repository's instance format confirms job precedence, machine and worker no-overlap and the pair-specific durations, and computes a makespan strictly below that instance's UB in https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv, re-fetched live immediately before claiming, with the instance-to-row mapping (e.g. Behnke10.fjs <-> behnkegeiger10) confirmed from the repository's data.csv. Nothing is submitted by the agent.

Partial wins:
> p1: A strictly better makespan on any Brandimarte- or Behnke-derived FJSSP-W instance with UB > LB, verified by the checker.
> p2: Strict improvements on at least 10 distinct FJSSP-W instances, each verified by the checker.
> p3: A strictly better makespan on any Hurink-, Dauzere-Peres-Paulli- or Chambers-Barnes-derived FJSSP-W instance with UB > LB, verified by the checker.

claim/criterion.txt: the success criterion and all three partial wins are contained verbatim (exact substring match by script). CLAIM.md does not restate the criterion; it names the target id and its scope sentence matches the criterion.

## Method

1. Live table re-fetched (plain curl, one request): 2026-11-23T19:16:18Z UTC, HTTP 200, sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf. Byte-identical to claim/references/best_known.csv (same sha256; the claim's fetch was 2026-11-23T19:06:35Z). Header is `Instance;UB;LB`; columns read by header name. UB >= LB on all 402 rows. Rounding per the page: round to nearest integer when within 1e-3 (non-integer LBs such as hurinkedata3 LB 387.866 are kept raw; they are not float noise). All 136 claimed UBs are exact integers in the file (max |UB - round(UB)| = 0.0).
2. data.csv fetched at pinned commit eb1d28381c34525b58736965cddbeb89e095f88a and at main: both HTTP 200, sha256 93debe7b...c1d67f, identical to claim/references/data.csv. data.csv rows are NOT in the same order as best_known.csv, so mapping is not positional. Mapping confirmed as follows: the naming rule (behnkegeiger->Behnke, brandimarte->BrandimarteMk, dppaulli->DPpaulli, hurink{e,r,s,v}data->Hurink{e,r,s,v}data, chambersbarnes, fattahi, kacem) is an exact bijection between the 402 table rows and the 402 data.csv `source` names; claim/references/row_to_file.json agrees with it on all 136 rows; and for every one of the 136 instance files, data.csv's n_jobs, n_machines, n_worker, n_operations, d_min, d_max, d_distinct and d_average (to 1e-6) equal the values computed from the parsed file. Local instances.sha256 matches all 136 files. (I did not fetch the instance files from upstream; that was outside my allowed fetches. The data.csv fingerprint match is strong supporting evidence of identity.)
3. Own checker (panel/work-criterion/check.py, stdlib) written from the page's format description: whitespace integer stream; header jobs machines workers; per job #ops; per op #machine choices k; per choice machine id, #workers w, then w (worker, duration) pairs; parse must consume the file exactly (3-token header for all 136). Note: the bank page's wording omits the machine-id token per choice; the files do carry it (verified by exact consumption with id-range checks). Checks: every (job, op) exactly once, integer records, (machine, worker) eligible, duration equals that pair's, start >= 0, job precedence, no overlap per machine and per worker (half-open), makespan = latest end; schedule's "instance" field equals the file name.
4. Negative control: 20 random schedules x 8 corruption kinds (duration +1, dropped op, duplicated op, ineligible pair, broken precedence, machine overlap, worker overlap, negative start): originals 20/20 valid, 157 corruptions generated, 157 rejected, 0 accepted.
5. Row test: pass iff valid and makespan <= round(UB) - 1, with mapping and fingerprint confirmed. UB > LB recorded per row.

## Results (all 136 rows)

- Valid schedules: 136/136. Makespan <= round(UB) - 1: 136/136. Mapping confirmed: 136/136. Object files: exactly the 136 expected, no extras.
- Every number in the CLAIM.md table (file, rounded UB, our makespan, saving) equals my recomputation; 0 mismatches. Total saving 1367 (matches). Minimum saving 1 (56 rows save exactly 1). provenance/rows.csv makespan and UB agree on all 136.
- UB > LB on all 136 rows (smallest UB - LB = 6.0). No makespan is below its row's LB.

Per-family counts (rows / rows passing with UB > LB):

| Family (file prefix) | Rows | Pass, UB > LB |
|---|---:|---:|
| Behnke (behnkegeiger) | 34 | 34 |
| BrandimarteMk (brandimarte) | 7 | 7 |
| DPpaulli (dppaulli) | 16 | 16 |
| Hurinkedata | 13 | 13 |
| Hurinkrdata | 30 | 30 |
| Hurinksdata | 5 | 5 |
| Hurinkvdata | 31 | 31 |
| Chambers-Barnes, Fattahi, Kacem | 0 | 0 |
| Total | 136 | 136 |

Rows failing: none.

## Partial wins

- p1 holds: 41 Brandimarte/Behnke rows, all with UB > LB, all checker-verified strictly below UB.
- p2 holds: 136 distinct instances (>= 10).
- p3 holds: 95 Hurink (79) and Dauzere-Peres-Paulli (16) rows, all with UB > LB; no Chambers-Barnes rows (the claim does not say otherwise).
- Full criterion: holds separately for each of the 136 rows.

## Overstatement and wording check

- Numbers: no mismatch between the CLAIM.md table and my numbers; family counts in criterion.txt equal mine.
- Scope: the one-sentence claim (validity + at least 1 below rounded UB, per row; p1-p3 together) is exactly what I verified. "Not claimed" excludes optimality and the validity of public values; no "solved", "record", "first", "breakthrough" or "optimal" assertion. The public-value columns are explicitly marked as the authors' screen (novelty is not my brief).
- Minor inconsistency, not an overstatement: CLAIM.md says "The table's LB column is not used", yet p1 and p3 require UB > LB. The claim is still true (UB > LB on all 136 rows, min gap 6), but the sentence should read that LB is used only for the UB > LB condition of p1/p3.
- For the gate (policy, not overstatement): kit/RULES.md rule 4 says "One object or table cell per claim"; this claim bundles 136 cells. Each row is stated and verifiable separately, but the bundling departs from the literal rule and needs the gate's explicit decision/disclosure. CLAIM.md also carries no rule-1 status label (PROVED-HERE etc.); the per-row checks are machine-verifiable (PROVED-HERE in kind) but the label is absent.
- Not checked by me: instance bytes against upstream URLs (outside my fetch scope; fingerprinted via data.csv instead); novelty against public results.

pass: true
