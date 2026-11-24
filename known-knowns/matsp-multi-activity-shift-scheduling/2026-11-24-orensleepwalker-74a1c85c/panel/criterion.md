# Criterion verdict
context: fresh subagent started for this claim only

Claim: claim/CLAIM.md, 123 MATSP rosters (object/), each said to be feasible and strictly below the instance's TRA26 best known penalty. Work files: panel/work-criterion/ (scripts/, fetch/, per_row.csv, table.json). Inputs read: claim/ only, the live bank entry, repo/kit/POLICY.md, repo/kit/RULES.md, and one fetch each of the MATSP table and the Changes page. I did not read claim/code/ before writing my checker, and I did not use it afterwards.

## Method

1. Fetched the live bank entry and compared it with claim/target.md (`diff`).
2. Fetched https://www.schedulingbenchmarks.org/matsp/ and https://www.schedulingbenchmarks.org/changes.html once each with `curl -A "V3R1T4S-criterion-skeptic/1.0"`. Recorded the UTC time, HTTP status and sha256, and compared them with claim/data/.
3. Parsed the table myself (scripts/parse_table.py, regex over `<tr>`/`<td>`) to get 225 rows of instance, days, staff, tasks, best known and reference.
4. Wrote my own checker, scripts/check.py, from claim/data/ProblemDefinition.txt, using Python standard library only (`python3 -I`, `PYTHONDONTWRITEBYTECODE=1`). It checks these hard constraints:
   - at most one shift per day;
   - allowed start times (00:00, 06:00-10:00, 14:00-18:00, 20:00-23:45 in 15-minute steps; no 00:00 on day 0; only 00:00 on day h);
   - shift length 360-600 minutes in multiples of 15 (the sum of the task lengths, so tasks fill the shift with no gaps);
   - the shift ends inside the horizon;
   - at least 14 h rest between any two consecutive shifts. This is stricter than the definition, which only checks consecutive days.
   - total minutes within [b_e, c_e] for every employee in the instance, including employees missing from the file;
   - at most 5 shift days in any 6-day window, d = 0..h-5;
   - every maximal run of one activity lasts at least 4 intervals (1 hour). This is again slightly stricter at the horizon start.
   - no overlapping intervals;
   - task IDs in 1..|A|;
   - WorkLength equals Length wherever WorkLength is present;
   - under-cover (count below min) is hard.

   The penalty is Σ max(0, count − max)². The checker also confirms that the instance has a cover line for every (interval, task) pair.
5. Calibration: the checker reports the site's example data/8_7_20_2.Solution.889.xml on data/8_7_20_2.txt as feasible with penalty **889**. It covers all 1344 of 1344 cover cells and finds 20 of 20 employees. Mutation tests (scripts/mutate.py) on two claimed rosters:
   - dropping a shift is rejected;
   - an illegal 11:00 start is rejected;
   - a duplicate day is rejected;
   - lengthening a task changes the penalty (743 → 746, still feasible) or is rejected (shift length 615).
6. Ran all 123 objects (scripts/run_all.py → per_row.csv). For each row it checks:
   - feasibility;
   - computed penalty equals `<Penalty>` and equals the penalty in the filename;
   - the live best known value is positive and greater than ours;
   - days, staff and tasks agree between the filename, the instance file and the table;
   - full cover-line coverage;
   - every employee appears in the file;
   - agreement with the claim/rows.csv record and penalty, and with the CLAIM.md table (instance, best known, ours, below by).

   Also checked: `sha256sum -c SHA256SUMS` (OK, 264 entries), and the object and instance sha256 values in rows.csv (0 mismatches).

## Verbatim criterion (live bank entry)

Live entry fetched 2026-11-24T14:01:04Z, HTTP 200, sha256 a39b0852fced545583927bd08880af7fc3c5be51e2824b48ab05dbed7bc10c75. `diff` against claim/target.md: the only difference is target.md's extra first two lines (`id: matsp-multi-activity-shift-scheduling` and a blank line). The rest is identical, so the frozen criterion is the live one.

"What counts as a win":

> A solution in the site's XML solution format for one instance listed on https://www.schedulingbenchmarks.org/matsp/ with a positive 'Best known' value, such that an independent checker written from the published ProblemDefinition.pdf (which first reproduces penalty 889 on the site's example file 8_7_20_2.Solution.889.xml) reports all hard constraints satisfied and a total penalty strictly below that instance's 'Best known' value, with the table and https://www.schedulingbenchmarks.org/changes.html re-fetched live immediately before claiming. Cross-checking with the site's own RosterViewer or command-line verifier (closed-source binaries) is optional and done by the human, not the agent; nothing is emailed or submitted by the agent.

Partial wins:

> - **matsp-small-instance-improve:** Strict improvement on any instance with at most 20 staff and positive best known value (instances 1-4, 6-10, 76-85, 151-160), checked by the independent evaluator; non-trivial because the current values are fresh 2026 SA results.
> - **matsp-optimality-certificate:** A proof of optimality for any instance with positive best known penalty: an exact MIP/CP model file plus a solver log (and seed) whose matching lower bound a skeptic re-runs to the same value in a fresh session, or a VIPR-style certificate checked by an independent checker; the site lists no lower bounds, so this is new information even without a better solution.
> - **matsp-independent-evaluator:** An open-source evaluator that reproduces the site's posted penalty for the example file and for a TRA26 best known solution if one is published; checkable by running it.

## Table and Changes page

| page | my fetch (UTC) | HTTP | sha256 | claim/data copy (13:34:54Z, 200) |
|---|---|---|---|---|
| matsp/ | 2026-11-24T14:01:04Z | 200 | f14664f5e33d0a99e1bf19d97f6e7eedfad344fbd45b744dbfdb1bbbb17ee984 | byte-identical (also equal to the hash frozen in PREREG.md) |
| changes.html | 2026-11-24T14:01:04Z | 200 | 6eb567e75bfe9a5615fc79a58a6210c980764d2fb1d2a900706bbaff41cfef3b | byte-identical |

- **Table:** 225 rows. Every row has reference TRA26. All best known values are numeric, and only instance 5 has 0.
- **Changes page:** the newest entries (29-Oct, 27-Oct, 21-Oct, 15-Oct-2026) are about the nurse instances. The only multi-activity entries are 07-Oct-2026 (the verifier tool) and 01-Sep-2026 (the TRA26 results). No multi-activity record has changed since then.

## Per-row result counts

- 123 of 123 objects are present. All 123 instances are listed in the live table with a **positive** best known value (TRA26), and none is instance 5.
- **Hard constraints:** 123 of 123 are feasible under my checker, with 0 violations.
- **Penalty:** on 123 of 123 rows, my penalty equals the file's `<Penalty>`, the filename value, rows.csv and CLAIM.md.
- **Strict improvement:** 123 of 123 rows have our penalty strictly below the live best known value. The total margin is **26224**.
  - The smallest margin is 2, on rows 38, 93, 173 and 219.
  - The largest is 1404 (222).
- 40 rows have 7 days, 41 have 14 days and 42 have 28 days, as CLAIM.md says.
- Days, staff and tasks agree among the filename, the instance header and the table on 123 of 123 rows. All employees of each instance appear in each file, and the cover data is complete for every instance.

## Rows failing

None.

## Partial wins

- **matsp-small-instance-improve holds for 6 rows:** 6, 7 (7 d), 81, 82 (14 d), 156, 157 (28 d), each with 20 staff.
  - All six are inside the listed ranges (6-10, 76-85, 151-160), and each is a strict improvement under my independent checker.
  - No other claimed row has 20 staff or fewer.
  - CLAIM.md's "6 rows with at most 20 staff" is correct.
- **matsp-optimality-certificate is not claimed and does not hold from this package.**
  - CLAIM.md lists lower bounds, and rows.csv marks rows 23, 98 and 219 as ending exactly at a bound (1905, 3855, 18988).
  - The package contains no model, log or certificate for those bounds; they come from a screen outside claim/.
  - The claim correctly says "Not claimed: optimality".
- **matsp-independent-evaluator is not claimed.** claim/code/ holds checkers, but no TRA26 solution file is reproduced and the partial win is not asserted.

## Format observations

The object files use the same element hierarchy as the site's example: `Solution` / `ProblemFile` / `Penalty` / `Employee ID=` / `Shift` / `Day`, `Start` / `Task` / `ID`, `Length`. Days are counted from 0, as in the example.

Compared with the example, our files leave out:

- the root attributes `xmlns:xsi` and `xsi:noNamespaceSchemaLocation="Solution.xsd"`;
- the metadata elements `TimeStamp`, `Author`, `Reference`, `Machine` and `SolveTime`;
- the `WorkLength` attribute on every `Task`. In the example, WorkLength equals Length on all 140 tasks.

`ProblemFile` is `<stem>.ros` rather than `../<stem>.ros`.

Judgement: the criterion asks for "the site's XML solution format" and makes the independent checker the deciding test. It names no schema and no required metadata. Every element that carries roster content is present, and the left-out items are either metadata or redundant with Length. So I judge the format requirement met on the literal text. However:

- Solution.xsd is not in the package.
- Whether the official verifier needs WorkLength, or the schema reference, is untested.
- The bank says a disagreement with the official tool, run by the human, withdraws the claim.

## Overstatement check (CLAIM.md)

Every number in CLAIM.md matches my output:

- all 123 rows: instance, best known, ours, below by;
- the total of 26224;
- 40/41/42 rows by horizon;
- the 6 small rows;
- the fetch time, HTTP 200, and "all TRA26".

The text claims feasibility and strict improvement per row and nothing more. It disclaims optimality, acceptance by the official verifier, and any statement about the method. I found no overstatement, no forbidden words ("solved", "record" and the like), and no hedging that contradicts the numbers.

## Points for the gate

1. **Bundling (RULES.md rule 4, "One object or table cell per claim").** This claim bundles 123 rows. Each row is a separate table cell with its own object and meets the criterion on its own. The gate must decide whether a batched filing is acceptable or must be split.
2. **Kit labels (RULES.md rule 1).** CLAIM.md carries none of the required labels (`PROVED-HERE`, `NUMERICAL`, `KNOWN` and so on) on its substantive claims. The feasibility and penalty results would be PROVED-HERE (checker-verified objects), and the lower-bound column would be a NUMERICAL or KNOWN-style screen. This is a policy gap, not an overstatement.
3. **Lower-bound column.** These numbers cannot be checked from the package: their source (scans/...) is outside claim/. For rows 23, 98 and 219 they imply optimality. The claim labels them "information only" and disclaims them, but the gate may want them removed or marked as not verified in this package.
4. **Format.** WorkLength, Solution.xsd and the metadata are left out (see above). The closed-source verifier was not run. Acceptance by the official tool is unknown and is the human's optional cross-check.
5. **Missing file named in PREREG.md.** PREREG.md cites data/object_list.csv (sha256 92ab4244...) as the fixed object list, but that file is not in claim/. The 123 objects are fixed instead by claim/SHA256SUMS and the rows.csv hashes, which all verify. Counting rule (c) also uses bounds from outside claim/.
6. **Live re-check.** The table and Changes page were byte-identical to claim/data at 2026-11-24T14:01:04Z. The criterion requires another live re-fetch immediately before any filing, and any row whose best known value has dropped to or below ours must be withdrawn.
7. **Instance data.** I could not compare claim/data/instances against the archive's sha256 (I was not permitted to download the zip). Each instance's header does agree with the live table's days, staff and tasks.

pass: true
