(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the B40 REPRODUCE skeptic subagent (Opus 5.5, model opus, agent ae869b850d6c7bf3b) could not write a file named like a report. Text verbatim below.)

# Panel: REPRODUCE skeptic, cell B40 (proportion 0.40, mean BCFS), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE
start (date -u): Sun Oct 18 21:39:52 UTC 2026
end (date -u): Sun Oct 18 21:57:37 UTC 2026
material: only the claim package (claim/), kit/RULES.md, TROPHY_CASE.md and the named interpreters (SYS: the q15ml venv; SCO: the official-scorer interpreter, used only as an interpreter). No web requests were made, so nothing was added to the stop list. Scratch work stayed outside claim/: work/, runA/, runB/, runC/, iso/ in my panel folder.

## Definition (quoted)
definition/Q15.json "success_criterion": "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Statistic, from official/src/sigtypst2022.py (compare_systems):
    results[stm][dataset] = compare_words(... "solutions-{0:.2f}.tsv" ..., ... "result-{0:.2f}.tsv" ..., report=False)[-1][1:]
    results[stm]["total"] += [statistics.mean([row[i] for row in totals])]
So the system score is statistics.mean over the 10 families of the TOTAL row [ED, NED, BCFS, BLEU].

## 1. My own scorer (written before I read any of the authors' scoring or checker code)
work/myscore.py loads claim's official/src/sigtypst2022.py by file path under SCO. For each FAM it calls compare_words(official/data-surprise/FAM/solutions-0.40.tsv, PRED/FAM/result-0.40.tsv, report=False)[-1][1:] and then takes statistics.mean over the 10 families. It has two modes:
- lr: `sum` is shadowed in the sigtypst2022 and lingrex.util namespaces by a plain loop (total = total + x).
- builtin: Python's own sum.

Scorer identity check (sha256 via the SCO interpreter):
    installed scorer module sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a
    claim official/src/sigtypst2022.py sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a
    identical
(SCO: Python 3.13.2, lingpy 2.6.9, lingrex 1.2.0. I could not check the pinned commit 03094435 offline because no web access was allowed.)

### 1a. Calibration on Mockingbird-I1 (official/systems/mockingbird-i1/surprise/FAM/result-0.40.tsv) against results-surprise-0.40.json
    out/mb_lr.json mode lr family values differing: 0 of 40 | total values differing: 0 of 4 | BCFS total mine 0.6428278176401176 official 0.6428278176401176 equal
    out/mb_builtin.json mode builtin family values differing: 16 of 40 | total values differing: 1 of 4 | BCFS total mine 0.6428278176401175 official 0.6428278176401176 DIFF
- Left-to-right summation reproduces the official entry bit for bit (40 of 40 family values, 4 of 4 totals).
- Builtin sum is 1 ulp lower on BCFS (0.6428278176401175).
- Bar = 0.6428278176401176.

### 1b. Claimed predictions (attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv)
lr mode, per family (ED NED BCFS BLEU):
    bantubvd 1.2005905027996897 0.27916294398249597 0.7013164444226421 0.5832800617998198
    beidazihui 0.3925756420035596 0.10776336977709974 0.8446805979042571 0.8353130901381886
    birchallchapacuran 1.756988426450673 0.2839230935858309 0.6199449054800916 0.5614710409078928
    bodtkhobwa 0.3091154909814428 0.132006932235699 0.8171628277465056 0.822466684196625
    bremerberta 1.2888991834723542 0.24604231412836958 0.6890705686574227 0.6260984947459621
    deepadungpalaung 0.5775141010502853 0.20351674569684436 0.8012583356894782 0.715949620314872
    hillburmish 1.0973619920237618 0.2930415045598018 0.6454293325998819 0.6005714430070029
    kesslersignificance 2.633152655979697 0.6225228428310707 0.38106383833251 0.22073285723213143
    luangthongkumkaren 0.3241486182584384 0.08643897155559252 0.8911113677575528 0.8622149525906906
    wangbai 0.687339504571714 0.20103022045023938 0.7453397496984093 0.7058685887824336
    TOTAL 1.0267686117591617 0.2455448938803044 0.7136377968288752 0.6533966833715619
builtin mode:
    TOTAL 1.0267686117591617 0.24554489388030437 0.7136377968288752 0.6533966833715619
Margin over the bar:
    lr cand BCFS 0.7136377968288752 official bar 0.6428278176401176 margin 0.07080997918875753 > 1e-9: True
    builtin cand BCFS 0.7136377968288752 official bar 0.6428278176401176 margin 0.07080997918875753 > 1e-9: True
- These are exactly the CLAIM.md values: BCFS 0.7136377968288752 in both modes; ED 1.0267686117591617, NED 0.2455448938803044, BLEU 0.6533966833715619 (left-to-right).
- The candidate's BCFS is higher than Mockingbird-I1's in all 10 families (compare the per-family values above with section 1a's official values).
- No "Missing entry" messages were printed by compare_words.

Cross-check with the authors' tools, run after my own scorer:
- checker/check_q15.py printed:
      "1. Mockingbird-I1 mean BCFS recomputed 0.6428278176401176, official 0.6428278176401176: EXACT"
      "3. object mean BCFS 0.7136377968288752 over 14992 items (claimed 0.7136377968288752): EQUAL"
      "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
      "PASS"
- tools/score_test_040.py printed:
      "B40 classifier/PRIMARY | ltr: 0.7136377968288752 bar 0.6428278176401176 margin 0.070809979189 -> MEETS (i) ... | builtin: 0.7136377968288752 ... both modes: MEETS (i)"

## 2. Integrity of the saved files
- MANIFEST.sha256: "OK count: 167" of 167 lines. The only file not listed is MANIFEST.sha256 itself. I re-checked after all runs: still 167 of 167, and no files added.
  (My first scorer import wrote a bytecode cache file at official/src/__pycache__/sigtypst2022.cpython-313.pyc. I deleted it straight away; every later run used -B.)
- attempts/classifier/FROZEN.md, ROLE=PRIMARY record (frozen 2026-10-18T19:14:05Z):
  - code files: "config.json: OK", "system.py: OK"
  - result files: "20 OK" (10 test/0.40 and 10 val/0.50)
  - code_tree_sha256 recomputed as the sha256 of the "sha256  path" lines: 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051, equal to the record.
  - results_tree_sha256 recomputed: 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0, equal to the record.
- object/predictions-0.40.tsv against the result files (work/objcheck.py):
      object rows 14992 unique keys 14992 duplicates 0
      families ok 10 of 10; total masked 14992 total predicted 14992 empty predictions 0 rebuilt identical 10 of 10
  In every family:
  - the "?" cells of test-0.40 match the non-empty cells of solutions-0.40;
  - the result file predicts exactly those cells;
  - object and result files agree;
  - result files rebuilt from the object are byte-identical;
  - each result header equals its test header.
- data/view/surprise/FAM/test-0.40.tsv and training-0.40.tsv are byte-identical to the official/data-surprise copies (10 of 10 each).
- data/view_manifest.sha256: 42 OK. The 10 training-0.50 entries are listed but not shipped in this package; 0.40 does not need them.
- Train/test cognate sets are disjoint: "total overlap 0" over the 10 families.

## 3. PREREG rule 12 (iv): retrain from the frozen code and re-predict
Run A, plain harness. The command from REPRODUCE.md section 3 was run from claim/ into my runA/ folder, adding `--python SYS`. OMP/MKL threads were 2, workers 2.
    2026-10-18T21:47:51Z test 0.40 train rc=0 274s
    2026-10-18T21:47:57Z test 0.40 bantubvd             ok 699 rows 6s
    ... (all 10 families "ok", last: 2026-10-18T21:49:04Z test 0.40 wangbai ok 2502 rows 24s)
cmp against the frozen files: bantubvd, beidazihui, birchallchapacuran, bodtkhobwa, bremerberta, deepadungpalaung, hillburmish, kesslersignificance, luangthongkumkaren, wangbai: all "IDENTICAL".

Run B is an independent retrain, sandboxed and traced. Every system.py process (train, its spawn-pool children, each predict) ran:
- under sandbox-exec, with network denied and file-read-data denied for the whole workspace except the SYS venv, the frozen code folder, data/view/dev, the 10 data/view/surprise/FAM/training-0.40.tsv files and my runB/ folder;
- with a Python audit hook (sitecustomize through PYTHONPATH, which chains to the interpreter's own sitecustomize) logging every open/listdir/scandir/glob/subprocess/socket event.
Output:
    2026-10-18T21:54:25Z test 0.40 train rc=0 260s
    ... all 10 families "ok"
- cmp: all 10 "IDENTICAL".
- The model folders of run A and run B are byte-identical: "model dirs byte-identical (11 files)".
- Training and prediction are bit-deterministic. This is the deterministic case of rule 12 (iv), so no recomputed value is needed.
- Train wall times of 274 s and 260 s are within the 12 min of rule 7.

Documentation defect, non-blocking: REPRODUCE.md section 3 omits --python, and the harness default interpreter is a placeholder. Running it as written (runC/) ends with:
    FileNotFoundError: [Errno 2] No such file or directory: 'WORKDIR/venvs/q15ml/bin/python'
The command works once `--python SYS` is added, which is what I did. REPRODUCE.md should say so.

## 4. What the code reads
Static audit of attempts/classifier/frozen/PRIMARY/code/system.py (1568 lines):
- File opens: config.json next to the code; the manifest; load() of the manifest's surprise_train files; dev_dir/DEVFAM/training-0.10.tsv inside load_train (the devx option); model write/read in --model-dir; the jobs file; partition inputs and outputs.
- No os.walk, listdir, glob, network or subprocess calls.
- Module-level caches (_bc, _sc) are pure memo tables of segment class and similarity, so they carry no row information between rows.
- An env override CLS_OPTS exists. It is unset in the harness and in all my runs.

Dynamic trace, run B: every non-library open, by frequency.
    153 open ('W/claim/data/view/surprise/FAM/training-0.40.tsv', 'r')
     99 open ('W/runB/out/test/0.40/FAM/parts/pred-NN.tsv', 'w')
     99 open ('W/runB/out/test/0.40/FAM/parts/part-NN.tsv', 'r')
     13 open ('W/claim/attempts/classifier/frozen/PRIMARY/code/config.json', 'r')
     10 open ('W/runB/out/test/0.40/model/opts.json', 'r')
     10 open ('W/runB/out/test/0.40/model/model-FAM.pkl', 'w')
     10 open ('W/runB/out/test/0.40/model/model-FAM.pkl', 'r')
     10 open ('W/runB/out/test/0.40/FAM/parts/jobs.tsv', 'r')
      8 open ('W/claim/data/view/dev/listsamplesize/training-0.10.tsv', 'r')
  (plus the manifest, read once by train, and Python/venv library files such as entry_points.txt and sklearn css)
- Directory listings: only the code folder, runB and my hook folder.
- No other events.

Conclusions:
- The entry reads no solutions, cognates or wordlist file.
- It reads no surprise file of another proportion.
- No test file is read by training; predict processes read only the model and their own partition file.
- The only development-family file read is data/view/dev/listsamplesize/training-0.10.tsv, used for kesslersignificance (devx with pool=1).

Disclosure discrepancy, non-blocking: CLAIM.md says mannburmish rows are added for hillburmish. At 0.40, data/view/dev/mannburmish/training-0.10.tsv is never opened. That devx option has max_nref 30 and pool 0, and the mapped targets have more reflexes than that:
    {'AchangLongchuan': 95, 'Bola': 122, 'Lashi': 42, 'Maru': 108, 'Atsi': 51} max_nref 30 -> sparse targets: []
So the disclosure claims more than the entry actually reads.

## 5. Row isolation
- The harness audit (tools/q15h.py audit, test mode, 0.40) on run A's model: 40 "identical", 0 FAIL, "AUDIT PASS". The rows, partitions and verdicts are the same as the frozen attempts/classifier/frozen/PRIMARY/audit_test_0.40.txt.
- My own test (work/isotest.py, run A model):
      ISOTEST (a) 14992 rows 0 differ; (b) 80 sealed single-row processes 0 differ; PASS
  - (a) All test rows of each family went into ONE input file in reversed order, so sibling rows of the same cognate set sat together. They were predicted in one process, and every prediction equals the frozen one.
  - (b) 8 random rows per family (random.Random(1758040)) were each predicted alone, in their own process, under sandbox-exec where only the venv, the code, the model folder and that row's own folder were readable. All 80 equal the frozen ones.
- rules/sealed_cand_0.40.log (main session): train ok 155s (sandboxed); 10 of 10 families "bytes IDENTICAL"; "predict: 99 sealed processes"; final line "SEALED_CHECK 0.40 PASS".

## Reproduced (table)
| item | result | BCFS (left-to-right / builtin) |
|---|---|---|
| Mockingbird-I1, my scorer vs results-surprise-0.40.json | bit-identical, 40/40 family values, 4/4 totals (left-to-right) | 0.6428278176401176 / 0.6428278176401175 |
| frozen classifier/PRIMARY result files, my scorer | equal to claimed value | 0.7136377968288752 / 0.7136377968288752 |
| object/predictions-0.40.tsv vs result files | 14992/14992 equal; rebuilt bytes 10/10 identical | same |
| FROZEN.md code (2) and result (20) hashes, tree hashes | all OK | n/a |
| MANIFEST.sha256 | 167/167 OK | n/a |
| run A retrain + predict (plain harness) | 10/10 result files byte-identical | 0.7136377968288752 / 0.7136377968288752 |
| run B retrain + predict (sandboxed, traced) | 10/10 byte-identical; model dir identical to run A (11 files) | identical bytes, same value |
| harness audit (test, 0.40) | 40 identical, AUDIT PASS | n/a |
| own isolation test | 14992 mixed-file rows + 80 sealed single rows, 0 differ | n/a |
| margin over bar (both modes) | 0.07080997918875753 > 1e-9 | n/a |

Labels:
- PROVED-HERE (machine-checked here): the claimed value reproduces bit for bit under the pinned scorer copy, and two independent retrains reproduce the frozen predictions byte for byte.
- NUMERICAL: the beat itself (0.7136377968288752 vs 0.6428278176401176).

## Notes for the main session (none blocking for REPRODUCE)
1. REPRODUCE.md section 3 needs `--python SYS`. As written, the harness default interpreter is the placeholder 'WORKDIR/venvs/q15ml/bin/python' and the run fails.
2. CLAIM.md overstates the development-family use: at 0.40 only listsamplesize rows are read, and mannburmish is never opened.
3. Several package files contain absolute paths with a user name: attempts/classifier/frozen/PRIMARY/REPRODUCE.md, rules/sealed_cand_0.40.log, rules/PREREG.md, rules/selection.md, rules/frozen_entries.md, rules/ranking_040.md, scout/scout.md. The packaging check should scrub them before anything is published (kit rule 12).
4. I could not check offline that official/src/sigtypst2022.py is the pinned commit's version; it is byte-identical to the module installed in the official-scorer interpreter. The NOVELTY and CRITERION skeptics own the status and pin.

verdict: Every requested check reproduced. The scorer matches the official Mockingbird-I1 entry bit for bit, the claimed BCFS 0.7136377968288752 recomputes in both summation modes, beating the bar 0.6428278176401176 by 0.07080997918875753. All saved-file hashes match, and two independent retrains (one sandboxed and traced) are bit-deterministic and byte-identical to the frozen predictions. The entry reads only the training-0.40 files, one development-family file (listsamplesize/training-0.10.tsv) and its own partitions, and each row is predicted from that row alone.
pass: true