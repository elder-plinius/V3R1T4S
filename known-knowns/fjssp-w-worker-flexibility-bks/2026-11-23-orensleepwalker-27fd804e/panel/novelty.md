# Novelty verdict
context: fresh subagent started for this claim only

Reviewer role: NOVELTY skeptic. I looked for any public FJSSP-W value or schedule at or below one of the 136 claimed makespans, and for any row whose schedule nearly copies a public one.
Inputs read: claim/ only (CLAIM.md, criterion.txt, REPRODUCE.md, references/, provenance/README.md and rows.csv). The one allowed exception was the old run's zips/index.txt, used only to compare archive hashes; I re-downloaded and re-extracted every archive myself.
Work folder: panel/work-novelty/. It holds the scripts in scripts/, the downloads in dl/ and the outputs in out/.
Checking method: I wrote my own instance parser, checker and re-timer (scripts/fj.py). Re-timing keeps each operation's (machine, worker) pair and the order given by the start times, then builds a semi-active schedule with the instance's own durations. As a self-test it accepts all 136 claim schedules at exactly the claimed makespans.
Review time: 2026-11-23, about 19:16Z to 19:35Z UTC.

## Sources checked

### 1. Live best_known.csv and its full history
- **Live fetch.** I fetched https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv at 2026-11-23T19:16:14Z.
  - The response was HTTP 200 with sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf.
  - It is byte-identical to claim/references/best_known.csv.
  - Benchmark main HEAD is eb1d28381c34525b58736965cddbeb89e095f88a (2026-05-04), the same commit the claim pins.
- **History.** I took a blobless clone of all branches (main and gh-pages; 50 commits). The FJSSP-W best_known.csv has 8 versions: 035912b, 9462fca, 22e1c02, decf461, c5d3007, e8574fb, c894f27 and fb2d06a (= live).
  - The file names changed over time (0_BehnkeGeiger10, Behnke10, BehnkeGeiger10, behnkegeiger10); I normalised them, and all 136 rows matched in every version.
  - **No version ever listed a UB at or below a claimed makespan.**
  - Smallest UB minus ours is 1 in the old and current versions. In decf461 and c5d3007 the UBs are higher (smallest margin 2, on Behnke49).
  - The only values at or below ours in any version are lower-bound columns, which is expected. c894f27 has its header written as LB;UB, but the values are UB;LB.
  - The FJSSP (no-worker) best_known files describe a different problem and are not comparable.
- **Benchmark issue #1** (leonlan, "Explicit best-known solutions FJSSP-W", closed 2026-04-27) discusses Behnke1 only (UB 87 vs 88, later corrected to 85). Behnke1 is not a claim row. Leon Lan offered to share solutions, but I found no published copy (his repositories list nothing FJSSP-W).
- The benchmark repository has no pull requests.

### 2. jrc-rodec/FJSSP-W-Benchmarking README, papers and the authors' result files
- **README.** It says the UBs come from CP, LP, MILP, Hexaly and GA solvers with 20-minute runs. It gives no per-instance values beyond best_known.csv.
- **Supplementary Material PDF** (sha256 03a03570…, 10 pages, all read). It contains models and encodings only; no per-instance values.
- **arXiv 2501.16159.** I read the abstract page: v1 2025-01-27, v2, and v3 revised 2026-05-05. I downloaded the LaTeX sources of all three versions (sha256 v1 53eb3f61…, v2 e783af4b…, v3 eda5f7d2…) and searched every table and caption.
  - Tables give family-level statistics only. v1 adds per-solver "characteristics" tables, which are averages.
  - No version has a per-instance makespan table.
- **jrc-rodec/FJSSPW-GA** (commit b9cb5d878f, the result set cited by the authors' GECCO'25 paper).
  - Files checked:
    - results_cplex_cp.txt (585ae313…)
    - results_hexaly.txt (75ee4fd5…)
    - results_ortools.txt (d05ee327…)
    - results_cplex_lp.txt (f01a9c50…)
    - condensed_ga_results.json (018673f8…)
  - The CPLEX CP schedules re-time as valid on all 136 claim instances. This confirms the instances are identical, and these schedules are the table UBs.
  - Hexaly gives 136 valid schedules and OR-Tools gives 131.
  - Minimum over all of these files minus ours is at least 1 on every row (CPLEX CP = table UB). The GA's best minus ours is at least 2 (Behnke49 108 vs 106).
- **jrc-rodec/scheduling_model** (HEAD 18221eb298, pushed 2026-11-20; shallow clone).
  - I scanned every text file and notebook output for any FJSSP-W instance label followed by a number in [0.8·ours, ours].
  - Every hit was one of these, none an FJSSP-W result on the benchmark instance:
    - an index number or the next instance's value;
    - an instance characteristic, such as "average_assignments";
    - a classic FJSSP or "no_worker" value (schedules with no worker assignment);
    - a mislabelled older instance set.
  - One hit needs stating explicitly. code/upgrades/wjfssp_comparison/compare.ipynb (commit f6e8faaac1, 2024-05-07) prints a Gurobi worker run in which "Behnke59" is FEASIBLE at 371, below our 392.
    - I do not count it, for four reasons:
      - The same table prints "Behnke55 OPTIMAL 19.999999", which is impossible on the benchmark's Behnke55: that instance has 250 operations and a trivial job-path lower bound of 69. So the file's labels do not refer to the benchmark instances.
      - The worker instance files it used ("benchmarks_with_workers", Behnke folder) were never committed. The repository's only committed worker set has no Behnke files.
      - No schedule is given.
      - Every later authors' table, from March 2025 to May 2026, lists Behnke59 at 429 or more.
    - I list it as a residual limit, not a failure.

### 3. jrc-rodec/FJSSP-W-Competition (GECCO 2026)
- **Repository.** Cloned at main f899d1b2943a1644d65f80038594fa664f52b17b and branch GECCO2026-Results b502608feeb70f03b016a08080ed0550557c9b02.
  - I read the README, index.md and the live site (https://jrc-rodec.github.io/FJSSP-W-Competition/, HTTP 200). None of them has a leaderboard with values.
- **Results poster.** PR #16 "Add Gecco Res" (hellwigm, open, one file GECCO_Poster_FJSSPresults.pdf, sha256 1038afa4…), read in full.
  - It gives rankings (MiniZinc scores) and gap plots only, no per-instance values.
  - It says "three of the prior best known results could be improved by the submitted solutions". This is consistent with the competition values below; every one is above ours.
- **Issue threads.** I read all 15 submission threads (#1–#15) and their comments (hashes in out/issues_sha256.txt).
  - #13 (MarkRogoQC) posts a value table in the thread. Its values are far above ours (for example Behnke60 509, DPpaulli15 15217). Its external repository MarkRogoQC/FJSS now returns 404.
  - #10, #11, #12 and #15 have no inline values.
- **Competition instances.** The competition has 30 instances. Eight of them are claim rows: Behnke46, Behnke60, BrandimarteMk7, DPpaulli9, DPpaulli15, DPpaulli18, Hurinkrdata38 and Hurinkvdata30. Their competition files are identical (whitespace-normalised) to the claim's reference instances; I checked 6 directly, and the rest follow because all schedules re-time on our files.
- **The 15 archives.**
  - I downloaded all 15 attachments myself at 2026-11-23T19:19Z, all HTTP 200, with the sizes listed in the index. Each sha256 equals the old local copy; for example z1 0574f6cd…, z9 e11fc09b… and z12 806c93d4… (full list in the work log).
  - I extracted them myself with a path-safe unzipper.
  - I parsed every CSV/JSON record of all 13 Scenario-1/2 result formats: 9,481 records, plus Qin's 2 × 402 × 10 runs.
  - From each record I took every reported value (makespan, Fitness, best_makespan, objective, DeterministicMakespan) and re-timed every schedule (start times plus machine and worker vectors). The BBFWA (z4) entry has only an operation-sequence encoding, so I used its reported values only.
  - z3, z10 and z14 schedules mostly fail the direct check (overlaps); their re-timed values are all higher than their reported values. Every reported and re-timed value is above ours.
- **Haoxiang Qin S1/S2 (z1/z2).** These ran on all 402 instances. Their bundled copies of the 136 instance files are identical to the claim's. All 2 × 1,360 runs re-time as valid, and none is at or below ours.
- **Closest competition values for the key rows:**

| Row | Ours | Closest competition value |
|---|---:|---|
| Behnke39 | 403 | 426 (Qin S1) |
| Behnke56 | 395 | 408 (Qin S1) |
| Behnke57 | 391 | 425 (Qin S1) |
| Behnke58 | 401 | 416 (Qin S1) |
| Behnke59 | 392 | 414 (Qin S1) |
| Behnke60 | 369 | 370, from z9 CMRTS (Team2) and z12 Yu Sun TS, reported and re-timed valid. Next: 371 (z9), 372 (z13 re-timed), 403 (z7), 437 (Qin) |
| Behnke46 | 106 | 107 (z12 Yu Sun, valid) |
| DPpaulli15 | 2036 | 2050 (z12) |
| DPpaulli18 | 2028 | 2035 (z12) |
| DPpaulli9 | 1959 | 1974 (z12) |
| BrandimarteMk7 | 136 | 137 (table UB). Competition minimum 139 reported (z14), 140 valid (z5/z6/z7/z12) |
| Hurinkrdata38 | 1469 | 1471 (table UB). Competition minimum 1488 (z12) |
| Hurinkvdata30 | 1010 | 1018 (table UB). Competition minimum 1029 (z12) |

### 4. Wider search
- **GitHub repository and code search** for FJSSP-W, fjsspw, FJSSP_W, WFJSSP, FJSP-W, Example_Instances_FJSSP-WF, FJSSP-W-Benchmarking, behnkegeiger, hurinkvdata and jrc-rodec.
  - **xuqqqqq/FJSSP-W** (HEAD f9e8a6fa9f, 2026-05-01): an AWLS solver run on all 402 public instances ("layer2") plus the competition 30. I scanned all 207 result files (14,288 records) and re-timed the schedules in its submission files. Nothing is at or below ours; closest are Behnke46 108, BrandimarteMk7 140 and Behnke60 381. Many large rows timed out with no value.
  - **benbekir/GECCO-2026** (319c2e6d11): LAHC, SPEA-II, ML, GREEDY, COMPETITION and "OtherResearcher" JSON files on the competition 30. Nothing at or below ours; closest Behnke46 110. Its best_known.csv is the old table version c5d3007.
  - **ScheduleOpt/optalcp-benchmarks** flexible-jobshop-w: model code and the 402 instance files only. There is no results or reference folder for FJSSP-W; history checked through 2026-11-06.
  - Other repositories (AnastasijaFed: empty; weinbendera, harshinijayabal, hagegegege, LukaHobor, SRNI-2005) hold no results on these instances.
- **Web search** for 2025–2026 FJSSP-W best-known updates, the Hutter/Steinberger/Hellwig GECCO'25 paper (DOI 10.1145/3712255.3726573; its result set is FJSSPW-GA, checked above) and the competition report. I found no other per-instance table.
- **elder-plinius/V3R1T4S** (at 2026-11-23T19:30Z):
  - I listed all 1,173 PRs (open and closed) and searched PRs and issues for fjssp, FJSSP-W, worker flexibility and job shop.
  - The only FJSSP-W PRs are #868 (open, head 9476a0042c…, 91 cells) and #1081 (open, head 0eb8d707b3…, 65 cells).
  - **Cell overlap with this claim is zero for both**, checked against each PR's INDEX.csv and object/*.json file names (156 objects).
  - No FJSSP-W issue exists.

### 5. Trivial-edit check
- **Coverage.** All 136 rows have at least one public schedule on the same instance, from Qin S1/S2, FJSSPW-GA CPLEX CP, Hexaly or OR-Tools, the competition archives, xuqqqqq or benbekir.
- **Agreement with any public schedule.** Highest share of operations with the same (machine, worker) pair, per row:
  - Overall maximum 0.670 (Hurinksdata3 vs Qin S1 run 7). Next highest: Hurinkedata18 0.640, Hurinkedata3 0.610.
  - **No row is above 80%.**
- **Against the table-UB schedule itself (CPLEX CP):**
  - Maximum 0.640 (Hurinksdata3), mean 0.246.
  - Over the 56 rows that save exactly 1 against the table: maximum 0.640, mean 0.319.
  - Same pair and same start time: at most 4%.
- **Calibration.** Two independent public schedules (CPLEX CP vs the best-matching Qin run) already agree 0.63–0.67 on Hurinksdata3, Hurinkedata18 and Hurinkedata3. These instances have little flexibility (1.0–1.13 machines per operation). So our highest overlaps are at the level two independent solvers reach, not near copies.

## Closest public value per row
- out/closest_all.txt gives, for every row, the minimum over all sources above: table versions, FJSSPW-GA, Qin, the 15 archives, xuqqqqq and benbekir, reported and re-timed.
- My minimum equals the claim's "lowest public reported value" column on all 136 rows; I found no discrepancy.
- Margin to the closest public value:
  - 1 on 58 rows. That is the 56 table-saving-1 rows plus Behnke46 (public 107 from the competition) and Behnke60 (public 370 from the competition).
  - 3 or less on 73 rows.
  - At least 1 on every row.

## Rows that fail
None. No public value or re-timed public schedule is at or below any claimed makespan, and no schedule is a near copy (maximum assignment agreement 67%).

## Residual limits
- **Behnke59: the 2024 notebook label at 371** (jrc-rodec/scheduling_model compare.ipynb, Gurobi). It is below our 392, but it demonstrably refers to a different or mislabelled instance set: the same table's "Behnke55" is OPTIMAL at 20, below the benchmark instance's trivial lower bound of 69. It has no schedule and its instance files are not public. I could not prove which instance it ran on. A stricter reader could treat it as an unresolved label-level value for Behnke59.
- **"no_worker" values in jrc-rodec/scheduling_model notebooks.** These are at or below ours for a few rows, for example Behnke14 237, Behnke36 391, Behnke39 399, Hurinksdata48 683. They are schedules without worker assignments (a relaxation, or classic FJSSP), so they are not FJSSP-W results. I did not count them.
- **Large notebooks in scheduling_model** (20 MB analyze_results, cp_results, etc.). I checked them by pattern scan only. Pickles and xlsx files were not parsed.
- **PDF technical reports inside the archives** (HCP_GVNS.pdf, RATS.pdf, the LAHC and ADGA PDFs, the Yu Sun reports, the Bartels report): I did not read them. Their values should duplicate the result files I parsed.
- **Uncovered entries:** the GECCO'25 Companion paper's full text (behind the ACM paywall; its result set is in FJSSPW-GA, which I checked) and Leon Lan's privately offered solutions (not public). GitHub code search covers default branches only.

pass: true
