# Reproduce verdict
context: fresh subagent started for this claim only

## Method

Order followed: I read claim/REPRODUCE.md, claim/CLAIM.md and claim/data/ProblemDefinition.txt, then the example instance and solution files (data only). Then I wrote my own checker, `panel/work-reproduce/mycheck.py` (Python standard library), before I opened claim/code/, claim/rows.csv or claim/provenance/. I never opened claim/provenance/. All scripts and outputs are in panel/work-reproduce/.

- **Time model.** My checker works in plain time, not in the formulation's interval indexes. Absolute minutes are counted from 00:00 of calendar day 0. The horizon runs from minute 360 (06:00 on day 0) to h*1440+360 (06:00 on day h). Horizon interval i = (minute-360)/15, i = 0..h*96-1.
- **Day indexing.** Solution `<Day>` d is calendar day d. An instance cover line with Day c is calendar day c-1.
  - The site's example confirms this. Its solution uses Days 0..7 with h=7, and its day-7 shifts all start at 00:00. Its cover lines run from Day 1 at 06:00 to Day 8 at 05:45 (144 + 6*192 + 48 lines per task).
  - Under this mapping the example scores exactly 889 with 0 violations. Moving the cover by +1 or -1 day gives penalties of 1590 and 1502, with 44 and 47 minimum-cover violations.
- **Instance parsing.** It is strict. Every (task, interval) must have exactly one cover line, every line must be a 15-minute slot, and no line may be duplicated.

## Rule readings (ambiguous ones marked *)

1. **One shift per day.** Each employee has at most one `<Shift>` per calendar day, and Day must be in 0..h. Each shift has one start time. Its length is the sum of its `<Task>` Length values.
2. **Start times.**
   - Allowed starts are 00:00, 06:00-10:00, 14:00-18:00 and 20:00-23:45, all inclusive, in 15-minute steps, with seconds = 0.
   - Day 0 may not start at 00:00. Day h may start only at 00:00.
3. **Shift length.** 360-600 minutes, a multiple of 15. Every task block is greater than 0 and a multiple of 15.
4. **Horizon.*** Every shift must lie inside [06:00 day 0, 06:00 day h].
   - The written formula u ≤ h*96 and the day blocks in constraint 7 use interval indexes that do not quite agree with each other or with the text (00:00 on day h would end past index h*96 under one reading). I applied the text's meaning instead.
   - In practice a shift on day h must be 00:00 and 360 minutes, and a shift on day h-1 must end by 06:00 on day h.
5. **Rest.*** At least 14 h (840 minutes, equality allowed, as in u ≤ t-56) between the end of a shift and the start of the next one.
   - I check every pair of consecutive shifts, not only shifts on consecutive days. This is equivalent given the start-time and length limits, and slightly stricter.
   - The bound is binding: the smallest gap in the 123 rosters is exactly 840 minutes.
6. **Total work time.** b_e ≤ total minutes ≤ c_e, inclusive. An employee missing from the file counts as 0 minutes. 10,647 employees sit exactly on a bound.
7. **Maximum working days.*** At most 5 working days in every window of 6 calendar days d..d+5, for d = 0..h-5. A day counts as worked if a shift starts on it. 14,237 windows hold exactly 5 working days.
8. **Minimum task run.*** Every maximal run of the same task over consecutive intervals (adjacent task blocks with the same ID merge) must be at least 4 intervals (1 h).
   - The literal formula ranges over i = 0..h*96 and needs x_i = 0 before the run, so it does not cover a run that starts at horizon interval 0. I enforce the rule there too and label that case separately (`min_run_at_interval0`).
   - Runs at the end of the horizon treat the intervals past the horizon as 0.
   - No roster has any run shorter than 60 minutes, so the reading does not matter for these 123 files.
9. **Activities.*** Activities only inside a shift, exactly one per interval. The file format implies this: a shift is a gapless sequence of task blocks. I also check task IDs in 1..|A| and flag overlaps.
10. **Cover.** Cover is at least v_ia for every task and interval. I also check that v ≤ w in the instance (true everywhere).
11. **Penalty.** The sum over tasks and intervals of max(0, cover - w_ia)^2. It must equal the file's `<Penalty>` and the penalty in the file name.

## Results

**Example.** My checker gives penalty 889 with 0 violations on data/8_7_20_2.Solution.889.xml with data/8_7_20_2.txt.

**All 123 rosters** (run_all.out, results.json):

| Check | Result |
|---|---|
| Hard-constraint violations | 0 rosters with any violation |
| Computed penalty = `<Penalty>` = file-name penalty | 123 / 123 |
| Penalty strictly below the best known value in data/matsp.html | 123 / 123 |
| Table row for the index has reference TRA26 and Days/Staff/Tasks matching the stem and the instance header | 123 / 123 |
| Total below the best known values | 26,224 (matches CLAIM.md) |

The best known values come from parsing the `<table>` rows of matsp.html myself.

There are no failing rows.

**Live data**, fetched 2026-11-24T14:03Z with one plain request each and User-Agent "V3R1T4S-reproduce-check/1.0", all HTTP 200:

- The sha256 of instances1_225.zip is 202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556, equal to claim/data/instances1_225.zip.sha256.
- All 123 claim/data/instances/<stem>.txt files are byte-identical to the archive's instances1_225/txt/<stem>.txt. claim/data/8_7_20_2.txt is too.
- The live table at https://www.schedulingbenchmarks.org/matsp/ is byte-identical to claim/data/matsp.html (sha256 f14664f5...).
- The live ProblemDefinition.pdf is byte-identical to claim/data/ProblemDefinition.pdf (sha256 6d3f02dc...).
- `sha256sum -c SHA256SUMS` in claim/ passes. The object and instance hashes in rows.csv match.

**Negative tests** (negtests.py, negtests.out, neg/). I used 42 different real rosters and broke one rule in each. The re-serialised unmodified roster passes before every mutation, as a sanity check. My checker rejected all 42, each time flagging the targeted rule:

| Rule broken | Mutation | Rosters |
|---|---|---:|
| Rest | Start moved 15 minutes earlier after an exact 14 h gap | 3 |
| Minimum run | First 15 minutes of a run switched to another task, where the cover stays at or above the minimum | 3 |
| Minimum cover | A task block relabelled where cover equals the minimum | 3 |
| Allowed start time | Start at 10:15 or 19:00 | 6 |
| Allowed start time | A day-1 00:00 shift moved to day 0 at 00:00 | 3 |
| Allowed start time | Last-day start 00:00 moved to 06:00 | 3 |
| Shift length | 600 lengthened to 615, or 360 shortened to 345 | 3 + 3 |
| Maximum working days | A rest-compatible 6 h shift added on the free day of a 5-in-6 window | 3 |
| Total work time | Over the maximum, or under the minimum | 3 + 3 |
| One shift per day | A shift duplicated on the same day | 3 |
| Horizon | Last-day shift 375 minutes, ending at 06:15 | 3 |

Most mutants broke only the targeted rule. Start-time moves also broke cover or rest, as expected.

## Comparison with the claim's checkers (opened only after the results above were final)

**Agreement on the 123 rosters.** On all 123, code/matsp.py `evaluate()` reports 0 violations and the same penalty as mine. code/verify_claim.py prints PASS. rows.csv record, penalty and saving agree with my values (0 disagreements). The 3 rows rows.csv marks as at the lower bound are 23_7_50_4, 98_14_50_4 and 219_28_140_14; that is shown for information only.

**Their verifier on my 42 mutants.** verify_claim.py rejects all 42.

**Differences in reading**, none of which changes any verdict on the 123 rosters:

- **(a) Minimum run at interval 0.** Their checkers use the definition's literal pattern, which does not catch a short run that starts at horizon interval 0. I tested this with a 15-minute run at the start of a day-0 06:00 shift in 12_7_30_2 (neg/run_at_interval0__12_7_30_2.Solution.1339.xml). My checker rejects it; verify_claim.py prints PASS. This is a real gap in their checker under the stricter reading, but no submitted roster has any run under 60 minutes, so it does not matter here.
- **(b) Rest.** They check rest only between shifts on consecutive calendar days; I check all consecutive shifts. This is equivalent under the start and length limits.
- **(c) Cover lines.** Their reader treats a missing cover line as min 0 / max 0 without error. `read_instance` counts the lines, and every instance used has the full |A|*h*96 lines, so there is no effect.
- **(d) Employee set.** They require the employee set to equal the instance's; I allow an absent employee whose minimum is 0. Every roster lists every employee, so there is no effect.
- **(e) Day offset.** Same reading as mine: solution Day + 1 = cover day.
- **(f) Out-of-range shifts.** After a disallowed start or a shift outside the horizon, their verifier skips the rest of that shift's checks. The verdict is still FAIL, so there is no effect.

## Could not check / disclosures

- **Site verifier not run.** I did not run the site's closed-source MATSP_Verifier or RosterViewer, as instructed. Whether the official verifier accepts these files is unknown.
- **Format differences.** All 123 rosters leave out the `WorkLength` attribute on `<Task>` (the site example has it) and the TimeStamp/Author/etc. elements. The definition does not make these hard constraints, but the official verifier's tolerance of them is unknown. Solution.xsd is not available to me.
- **PDF text.** I read the definition from ProblemDefinition.txt. The PDF is byte-identical to the live one, but I did not extract its text myself (no standard-library PDF parser); I assume the .txt is a faithful copy.
- **Bytecode file written inside claim/ (process error, since fixed).** `python3 -I` ignores `PYTHONDONTWRITEBYTECODE` because -I implies -E. When I imported claim/code/matsp.py for the comparison, Python wrote claim/code/__pycache__/matsp.cpython-312.pyc (created 16:04:58 local time). I deleted that file and the empty `__pycache__` folder at once. `sha256sum -c SHA256SUMS` still passes, and claim/ again holds exactly the 264 listed files plus SHA256SUMS. The mtime of the claim/code directory changed. No claim content was altered.

pass: true
