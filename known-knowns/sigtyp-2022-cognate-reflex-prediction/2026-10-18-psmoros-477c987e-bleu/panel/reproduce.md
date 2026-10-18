(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the L40 REPRODUCE skeptic subagent (Opus 5.5, model opus, agent accfd26c785484be9) could not write a file named like a report. Text verbatim below.)

# Panel: REPRODUCE skeptic, cell L40 (proportion 0.40, mean BLEU)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: 2026-10-18T21:39:50Z (date -u)
end: 2026-10-18T21:55:05Z (date -u)
material: claim/ only (plus kit RULES.md). Interpreters: SYS (the entry's ML venv), SCO (used only as an interpreter with lingpy/lingrex; the scorer itself was loaded from claim/official/src/sigtypst2022.py by file path), python3.13 for my own standard-library scripts. All scratch went in my own folder outside claim/. Network requests: none, so nothing was added to the stop list.

## Definition used (quoted, before reading the authors' code)
Success criterion (definition/Q15.json): "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion ... strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: ... or a higher mean BLEU. ... The repo scorer `st2022` at a pinned commit computes the score."
The statistic, from official/src/sigtypst2022.py: compare_words(solutions, result, report=False) returns a TOTAL row `sum([row[-1] for row in all_scores])/len(languages)` (BLEU; ED, NED and BCFS the same way), and compare_systems takes `results[stm][dataset] = compare_words(...)[-1][1:]` and then `results[stm]["total"] += [statistics.mean([row[i] for row in totals])]`.

## Check 1: my own scorer (my_score.py, written from the definition)
It loads claim/official/src/sigtypst2022.py with importlib, calls compare_words per family against official/data-surprise/FAM/solutions-0.40.tsv, and takes statistics.mean over the 10 families. It runs in two modes: "ltr" (builtin sum shadowed in the sigtypst2022 and lingrex.util namespaces by a plain left-to-right loop; lingrex.util.bleu_score does call sum, output `"bleu_score_uses_sum": true`) and "builtin".
Calibration on official/systems/mockingbird-i1/surprise/FAM/result-0.40.tsv, compared with the "Mockingbird-I1" entry of official/results/results-surprise-0.40.json using float ==:
```
ltr: 44 values compared with 'Mockingbird-I1', 0 differ; total [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171] vs official [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171]
builtin: 44 values compared with 'Mockingbird-I1', 17 differ; total [1.272493550651723, 0.316240240534308, 0.6428278176401175, 0.5723601982335171] vs official [...0.6428278176401176, 0.5723601982335171]
```
Left-to-right mode is bit-identical to the official values. In builtin mode the mean BLEU is still identical. The bar is 0.5723601982335171, the highest BLEU total of all 10 entries in that JSON (the next is Mockingbird-N1-B at 0.5466088108887145). PROVED-HERE.

## Check 2: the claimed value, from the frozen files
My scorer on attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (0 "Missing entry" lines):
```
mode ltr
  bantubvd             ED 1.2005905027996897 NED 0.27916294398249597 BCFS 0.7013164444226421 BLEU 0.5832800617998198
  beidazihui           ED 0.3925756420035596 NED 0.10776336977709974 BCFS 0.8446805979042571 BLEU 0.8353130901381886
  birchallchapacuran   ED 1.756988426450673 NED 0.2839230935858309 BCFS 0.6199449054800916 BLEU 0.5614710409078928
  bodtkhobwa           ED 0.3091154909814428 NED 0.132006932235699 BCFS 0.8171628277465056 BLEU 0.822466684196625
  bremerberta          ED 1.2888991834723542 NED 0.24604231412836958 BCFS 0.6890705686574227 BLEU 0.6260984947459621
  deepadungpalaung     ED 0.5775141010502853 NED 0.20351674569684436 BCFS 0.8012583356894782 BLEU 0.715949620314872
  hillburmish          ED 1.0973619920237618 NED 0.2930415045598018 BCFS 0.6454293325998819 BLEU 0.6005714430070029
  kesslersignificance  ED 2.633152655979697 NED 0.6225228428310707 BCFS 0.38106383833251 BLEU 0.22073285723213143
  luangthongkumkaren   ED 0.3241486182584384 NED 0.08643897155559252 BCFS 0.8911113677575528 BLEU 0.8622149525906906
  wangbai              ED 0.687339504571714 NED 0.20103022045023938 BCFS 0.7453397496984093 BLEU 0.7058685887824336
  MEAN                 ED 1.0267686117591617 NED 0.2455448938803044 BCFS 0.7136377968288752 BLEU 0.6533966833715619
mode builtin
  MEAN                 ED 1.0267686117591617 NED 0.24554489388030437 BCFS 0.7136377968288752 BLEU 0.6533966833715619
```
- The mean BLEU is 0.6533966833715619 in both modes, equal to CLAIM.md. ED, NED and BCFS (left-to-right) also equal the CLAIM.md table.
- Margin over the bar: 0.08103648513804473 in both modes, which is more than 1e-9.
- The candidate's BLEU is higher than Mockingbird-I1's in 10 of 10 families.

NUMERICAL.

## Check 3: integrity of the saved files
- `shasum -a 256 -c MANIFEST.sha256`: 167 lines, 0 not OK. The file set equals the manifest. I checked again after all runs: still 0 not OK. My scorer had left one official/src/__pycache__ bytecode file in claim/; I deleted it, and the file set again equals the manifest.
- FROZEN.md, ROLE=PRIMARY block:
  - code files: config.json 225856a4...a9f109 and system.py 8482ef52...6030ca both match.
  - result files: all 20 listed (test/0.40 and val/0.50) equal (`FROZEN.md result hashes: all 20 equal`).
  - Tree hashes recomputed the harness's way (sha256 of the sorted "sha  relpath" lines): code_tree 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051, results_tree 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0. Both equal FROZEN.md and CLAIM.md.
- object/predictions-0.40.tsv against the result files (my check_object.py):
  - per family: header equal, COGID order equal, and the predicted, masked ('?' in test-0.40) and gold cell sets are equal (bantubvd 699, beidazihui 3933, birchallchapacuran 584, bodtkhobwa 2856, bremerberta 306, deepadungpalaung 1218, hillburmish 1405, kesslersignificance 311, luangthongkumkaren 1178, wangbai 2502).
  - `object rows 14992, rows from result files 14992`, `object == result cells (same order): True`, `duplicates in object: 0`, `PROBLEMS 0`.
- data/view/surprise/FAM training-0.40 and test-0.40 are byte-equal to official/data-surprise (10 and 10 "equal"). data/view contains no solutions file (only training/test 0.40 and 0.10 files plus two datasets json files).
- Package checker `python3 checker/check_q15.py . object/predictions-0.40.tsv`: "Mockingbird-I1 mean BLEU recomputed 0.5723601982335171, official 0.5723601982335171: EXACT", "object mean BLEU 0.6533966833715619 over 14992 items (claimed 0.6533966833715619): EQUAL", "rebuilt official-format files equal to the frozen ones: 10 of 10", "PASS".

PROVED-HERE.

## Check 4: retrain and re-predict (PREREG rule 12 iv)
Command: tools/q15h.py run (frozen code, --mode test --props 0.40 --workers 2, OMP/MKL threads 2), output to an empty scratch folder of mine.
- The manifest it wrote lists only data/view/surprise/FAM/training-0.40.tsv for the 10 families and dev_dir = data/view/dev.
- Run 1: "test 0.40 train rc=0 209s", then all 10 families "ok". cmp against the frozen files: all 10 IDENTICAL. The sha256 values of the re-predicted files equal the FROZEN.md lines (for example bantubvd cbf74c9d...eedd0, wangbai b3c23443...f943).
- Run 2 (independent retrain with the access trace of check 5): "train rc=0 248s", all 10 "ok", all 10 IDENTICAL. Tree hash of the run 2 results is c5c4c7030ab1c85850661206f43de751dba7f23cf6e57978acf2b2c3d24b0d4f, the same as for the frozen test/0.40 files.
- Re-scored with my scorer: `ltr retrain == frozen (all family values and totals): True`, `builtin ... True`. BLEU 0.6533966833715619, margin 0.08103648513804473 in both modes.

Which case holds: training and prediction are bit-deterministic (2 of 2 independent retrains are byte-identical to the frozen predictions). The fallback clause of rule 12 (iv) is not needed. NUMERICAL.

## Check 5: what the entry reads
Code reading of attempts/classifier/frozen/PRIMARY/code/system.py:
- train reads only man["surprise_train"] and dev_dir. In load_train it opens only dev_dir/DEVFAM/training-0.10.tsv, for the devx families in config.json: hillburmish from mannburmish (max_nref 30, pool 0) and kesslersignificance from listsamplesize (pool 1).
- predict reads model-FAM.pkl, opts.json and the jobs/partition files, and writes one line per row from predict_row(m, row, langs).
- grep for solutions, cognates, wordlist, official, systems/ and results finds no match. There is no network, subprocess or directory-walking code. The only module-level caches (_bc, _sc) memoise pure symbol functions.

Runtime trace (my own sitecustomize audit hook, logging every Python open, listdir and subprocess event in the train, spawn-worker and predict processes of run 2; Python install and venv paths filtered out). Files opened, summed over processes:
```
data/view/surprise/FAM/training-0.40.tsv  (all 10 families, read)
data/view/dev/listsamplesize/training-0.10.tsv  (8 reads)
attempts/classifier/frozen/PRIMARY/code/{system.py,config.json}
scratch: manifest.json, model/*.pkl and opts.json (write, then read), FAM/parts/jobs.tsv (10), part-NN.tsv (99 read), pred-NN.tsv (99 written)
```
Other events: os.listdir of the code folder, of the claim folder (import path scan of the cwd, no file read from it) and of my hook folder. There are no subprocess or socket events from the entry.

Not read: any solutions, cognates or wordlist file; anything under official/; any surprise file of another proportion; any test-0.40.tsv directly (rows arrive only as harness partitions).

Finding: data/view/dev/mannburmish/training-0.10.tsv is never opened at 0.40. The reason is the max_nref gate: the five mapped hillburmish targets have 95, 51, 122, 42 and 108 reflexes in training-0.40, all at least 30, and pool is 0 for that family. So at 0.40 only listsamplesize rows (English, German, French onto kesslersignificance) are added. The CLAIM.md disclosure about mannburmish rows for hillburmish overstates what happens at this proportion. This errs on the conservative side and is not a failure.

Sensitivity, for the CRITERION skeptic: with kesslersignificance's BLEU replaced by Mockingbird-I1's, the mean would be 0.6459177394059678, margin 0.07355754117245061. NUMERICAL.

## Check 6: row isolation
- My own test (isolation.py, using the run 1 model): every masked row, with partitions in reversed language order and rows shuffled (Random(4040)), in one fresh process per family. Plus 5 random rows per family (Random(4041)), each alone in its own fresh process. All 10 families pass (for example "beidazihui reversed+shuffled one process: 3933/3933 rows identical (rc 0); single rows alone: 5/5 identical ok"). Result: "ISOLATION PASS".
- tools/q15h.py audit on my retrain: 40 identical, 0 FAIL/MISMATCH, "AUDIT PASS". The audited rows are the same as in the frozen audit_test_0.40.txt (also 40 identical, 0 FAIL).
- rules/sealed_cand_0.40.log (read, not rerun): train ok 155s sandboxed, 10 of 10 families "bytes IDENTICAL", final line "SEALED_CHECK 0.40 PASS".

## Reproduction table
| item | result |
|---|---|
| my scorer vs official Mockingbird-I1 0.40 (44 values, left-to-right) | bit-identical (0 differ) |
| claimed object, mean BLEU (left-to-right / builtin) | 0.6533966833715619 / 0.6533966833715619, equal to claim |
| margin over bar 0.5723601982335171 | 0.08103648513804473 (both modes), more than 1e-9 |
| MANIFEST.sha256 (167 files) | all OK |
| FROZEN.md code, result and tree hashes | all equal |
| object/predictions-0.40.tsv vs result files | identical cells, 14992 rows |
| retrain run 1, 10 test-0.40 files | bit-identical; recomputed BLEU 0.6533966833715619 |
| retrain run 2 (traced), 10 test-0.40 files | bit-identical; same results tree hash |
| determinism | bit-deterministic (2 of 2) |
| files read at runtime | training-0.40 (10), dev listsamplesize training-0.10, partitions; no gold or other-proportion surprise file |
| row isolation (my test, harness audit, sealed log) | PASS / PASS / PASS |

## Non-blocking notes for the main session
1. REPRODUCE.md section 3 fails as written. tools/q15h.py defaults --python to the placeholder "WORKDIR/venvs/q15ml/bin/python", and my first attempt failed with FileNotFoundError. With `--python SYS` added, it works. Add `--python SYS` to the documented command.
2. The CLAIM.md and selection.md disclosure says mannburmish rows are added for hillburmish. At 0.40 the trace shows that file is never read (check 5). Only the listsamplesize rows are used.
3. check_q15.py numbers its output lines 1, 3, 4 (there is no line 2). This is cosmetic.

No mismatch, missing object or non-determinism found. Labels: the score reproduction and the retrain are PROVED-HERE / NUMERICAL. The access audit is empirical: a Python-level trace plus code reading.

pass: true