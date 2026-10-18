(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the BA REPRODUCE skeptic subagent (Opus 5.5, model opus, agent a375550ea217295d2) could not write a file named like a report. Text verbatim below.)

# Panel: REPRODUCE skeptic, cell BA (aggregate mean BCFS over P = 0.10-0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE
start: Sun Oct 18 22:10:23 UTC 2026 (date -u)
end: Sun Oct 18 22:47:39 UTC 2026 (date -u)
material: the claim package claim/ only (paths below are relative to it), plus kit rules. Interpreters: SYS (the entry's ML venv), SCO (the pinned-scorer venv, used only as an interpreter), and a plain Python 3.13 for my own scripts. My scratch was outside claim/. I made no network requests, so I added nothing to the stop list.

## Summary
- All 50 re-predicted test-P files (10 families x 5 proportions) are byte-identical to the claimed ones.
- Retraining is bit-deterministic. I retrained twice at 0.10, 0.20 and 0.30 and got 100% identical model files and predictions both times. 0.40 and 0.50 were retrained once each.
- My own scorer reproduces Mockingbird-I1's official values bit for bit: 50 family values and 5 totals, left-to-right summation.
- The bar is 0.6797616040522236. The claimed value is A_BCFS = 0.7422025452564412, in both summation modes.
- File tracing at every P shows the entry reads:
  - that proportion's surprise training-P files;
  - one or two development-family files (always dev/listsamplesize/training-0.10.tsv; dev/mannburmish/training-0.10.tsv only at 0.50).
- It reads no solutions, cognates, wordlist, test-P or other-proportion surprise file.
- My own row-isolation test passes at every P: every row was predicted from a file that holds only that row.
- The case under PREREG rule 12 (iv) is: training is bit-deterministic and the predictions are reproduced exactly. The fallback "recomputed A beats the bar" case is not needed.

## 1. Definition and my own checker (written before reading the entry's code)
Criterion (definition/Q15.json, quoted): "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

PREREG rule 2 (quoted): "A_m = (S_m(0.10) + S_m(0.20) + S_m(0.30) + S_m(0.40) + S_m(0.50)) / 5, summed left to right in that order, where S_m(P) is the family mean of metric m at P (the official "total")."

Statistic, as defined by the pinned scorer official/src/sigtypst2022.py:
- compare_systems computes, per family, `compare_words(solutions-P.tsv, result-P.tsv, report=False)[-1][1:]`, which gives [ED, NED, BCFS, BLEU].
- The total is `statistics.mean` over the 10 families.
- Inside compare_words, the TOTAL row divides each sum by `len(languages)` of the gold file.

My scorer (my own script, outside claim/):
- loads official/src/sigtypst2022.py as a module from its file;
- calls compare_words per family and P, then statistics.mean over the families;
- computes A as the left-to-right mean over the five P.
- Mode "ltr" shadows `sum` with a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces. Mode "builtin" uses Python 3.13's builtin sum.

Check that the scorer source is the pinned one:
- `cmp official/src/sigtypst2022.py` against SCO's installed sigtypst2022.py: identical.
- sha256 of official/src/sigtypst2022.py: 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a.

## 2. Bar: Mockingbird-I1 per-item files against the official JSON, all five P
Input: official/systems/mockingbird-i1/surprise/FAM/result-P.tsv. Output of my scorer in ltr mode:
```
S 0.10 0.9200532775139207 0.2431316340782435 0.7672735092897016 0.6633184488563897
S 0.20 1.0413225298738344 0.2648052468982754 0.7119659170836019 0.632633947442519
S 0.30 1.1762187506031638 0.2898984929868421 0.6717099225519634 0.6058548112827981
S 0.40 1.272493550651723 0.316240240534308 0.6428278176401176 0.5723601982335171
S 0.50 1.4169823165005235 0.35176136367373956 0.6050308536957327 0.5337187296541888
A(ltr over P) 1.1654140850286332 0.2931673956342817 0.6797616040522236 0.6015772270938825
```
Comparison with official/results/results-surprise-P.json, "Mockingbird-I1":
```
mode ltr family values compared 50 totals compared 5 mismatches 0
bar A from official totals (ltr): ED NED BCFS BLEU = 1.1654140850286332 0.2931673956342817 0.6797616040522236 0.6015772270938825
bar A from official totals (builtin sum): 1.1654140850286332 0.29316739563428174 0.6797616040522234 0.6015772270938825
```
- In ltr mode all 50 family values and 5 totals match bit for bit.
- Builtin mode differs from the 2022 values in the last bits, as expected (for example 0.50 BLEU total 0.5337187296541887 against the official 0.5337187296541888).
- Bar: A_BCFS(Mockingbird-I1) = 0.6797616040522236 (ltr), the PREREG value. With builtin sum it is 0.6797616040522234.

## 3. The claimed object, scored by my scorer
Input: attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv. Output in ltr mode:
```
S 0.10 0.7741426354973481 0.20017478183757248 0.8091752827860231 0.7183395130131847
S 0.20 0.8518682371657778 0.21213687542061813 0.7629197798251665 0.6960719420978517
S 0.30 0.9552549562700591 0.23201071558421696 0.7347693490340722 0.6721728449836378
S 0.40 1.0267686117591617 0.2455448938803044 0.7136377968288752 0.6533966833715619
S 0.50 1.1367942567904354 0.26834206801685595 0.690510517808069 0.624905217712099
A(ltr over P) 0.9489657394965564 0.23164186694791358 0.7422025452564412 0.6729772402356671
A(builtin over P) 0.9489657394965564 0.23164186694791358 0.7422025452564412 0.6729772402356671
```
Builtin mode, same files:
```
S 0.10 0.7741426354973481 0.20017478183757248 0.8091752827860231 0.7183395130131847
S 0.20 0.8518682371657779 0.21213687542061813 0.7629197798251665 0.6960719420978518
S 0.30 0.955254956270059 0.23201071558421696 0.7347693490340722 0.6721728449836379
S 0.40 1.0267686117591617 0.24554489388030437 0.7136377968288752 0.6533966833715619
S 0.50 1.1367942567904354 0.26834206801685595 0.690510517808069 0.624905217712099
A(ltr over P) 0.9489657394965564 0.23164186694791358 0.7422025452564412 0.6729772402356671
```
- Every number agrees with the CLAIM.md values table: all 4 metrics at all 5 P and A, ltr mode.
- Margin over the bar: 0.7422025452564412 - 0.6797616040522236 = 0.062440941204217615 (ltr). Against the builtin-sum bar 0.6797616040522234 the margin is 0.06244094120421784. Both are greater than 1e-9.
- BCFS per family (candidate). The candidate's family BCFS beats Mockingbird-I1's in 50 of 50 family-P cells.

| family | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|
| bantubvd | 0.830600 | 0.750793 | 0.709210 | 0.701316 | 0.638236 |
| beidazihui | 0.876635 | 0.855994 | 0.846079 | 0.844681 | 0.841845 |
| birchallchapacuran | 0.708853 | 0.654223 | 0.617731 | 0.619945 | 0.588461 |
| bodtkhobwa | 0.875884 | 0.849246 | 0.841540 | 0.817163 | 0.798741 |
| bremerberta | 0.823234 | 0.749583 | 0.714235 | 0.689071 | 0.670300 |
| deepadungpalaung | 0.930296 | 0.884278 | 0.829297 | 0.801258 | 0.785561 |
| hillburmish | 0.728347 | 0.719309 | 0.679780 | 0.645429 | 0.618665 |
| kesslersignificance | 0.535660 | 0.460726 | 0.438261 | 0.381064 | 0.379430 |
| luangthongkumkaren | 0.926291 | 0.903462 | 0.902957 | 0.891111 | 0.862872 |
| wangbai | 0.855953 | 0.801586 | 0.768604 | 0.745340 | 0.720994 |

As a cross-check I also ran the package's own standard-library checker (`python3 checker/check_q15.py . object`). Key lines:
```
3. Mockingbird-I1 A_BCFS from the official totals 0.6797616040522236 (PREREG 0.6797616040522236): EQUAL
4. object A_BCFS 0.7422025452564412 (claimed 0.7422025452564412): EQUAL
5. rebuilt official-format files equal to the frozen ones: 50 of 50
PASS
```

## 4. Integrity of the saved files
**MANIFEST.sha256**
- `shasum -a 256 -c MANIFEST.sha256` gives "OK lines: 470 of 470".
- The package holds exactly 470 files besides the manifest; none is missing and none is unlisted.
- One file was mine and has been removed: when my scorer imported official/src/sigtypst2022.py, Python wrote official/src/__pycache__/sigtypst2022.cpython-313.pyc into the package. I moved it out and re-ran the check, with the result above. After that I ran with bytecode writing off, and nothing else was written into claim/.

**attempts/classifier/FROZEN.md** (the only ROLE=PRIMARY record, frozen 2026-10-18T19:14:05Z)
- The code files hash to 225856a4... (config.json) and 8482ef52... (system.py).
- `shasum -a 256 config.json system.py | shasum -a 256` gives 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051, which equals the record's code_tree_sha256.
- Result files: "FROZEN result hashes: 20 of 20 identical" (test/0.40 and val/0.50). Their tree hash is 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0, which equals the record's results_tree_sha256.

**checker/frozen_result_sha256.txt**: "50 of 50 files match (50 records)".

**object/predictions-P.tsv against the result files.** My own script compares them and checks coverage of the masked cells of data/view test-P:
```
P 0.10 object rows 4029 result cells 4029 object==results True masked cells in test-P 4029 predicted 4029
P 0.20 object rows 7887 result cells 7887 object==results True masked cells in test-P 7887 predicted 7887
P 0.30 object rows 11586 result cells 11586 object==results True masked cells in test-P 11586 predicted 11586
P 0.40 object rows 14992 result cells 14992 object==results True masked cells in test-P 14992 predicted 14992
P 0.50 object rows 18101 result cells 18101 object==results True masked cells in test-P 18101 predicted 18101
```

**Data view**
- data/view/surprise has 100 files (training-P and test-P, 5 P, 10 families). Compared with official/data-surprise, 0 differ.
- data/view/dev holds only training-0.10.tsv and test-0.10.tsv per development family.
- No file named solution, cognate or wordlist exists under data/view.
- I could not check the dev files against the release independently, because the package has no official copy of the dev families. scout/scout.md records them as byte-identical to the pinned clone.

**Run and audit records of the other proportions**
- run_test_0.10/0.20/0.30/0.50.txt show train rc=0 and 10 of 10 families "ok". Row counts sum to 4029, 7887, 11586 and 18101, matching the object.
- audit_test_P.txt for all five P: 40 "identical" lines each (3 single rows plus 1 whole partition per family), 0 FAIL or MISMATCH, last line "AUDIT PASS".

**Sealed-check logs** (rules/sealed_cand_P.log)
- Each P has 10 of 10 families "bytes IDENTICAL" and a final line "SEALED_CHECK P PASS".
- Sandboxed train times: 238 s, 206 s, 176 s, 155 s and 129 s for 0.10 to 0.50.

## 5. Retrain and re-predict (PREREG rule 12 iv), five proportions, fresh scratch folders
Command at each P, run from claim/ with OMP_NUM_THREADS=2, MKL_NUM_THREADS=2 and HOME inside my scratch:
`SYS -I tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --out NEW/rP --props P --workers 1 --python SYS`

Run setup:
- I ran 3 proportions in parallel (0.10, 0.20, 0.30 first, then 0.40 and 0.50).
- I used --workers 1 instead of the REPRODUCE.md value 2 to limit my process count. That flag only sets how many families are predicted at once; each family's prediction is a separate process either way.
- The system's training uses its own internal 2-process pool regardless of the flag.

Manifests:
- The harness wrote manifest.json with surprise_train = the 10 data/view/surprise/FAM/training-P.tsv files, and dev_dir = data/view/dev.
- My check printed, for example: `0.10 manifest train files: ['training-0.10.tsv'] dev_dir data/view/dev`, and the same with 0.20 and 0.30.

Harness training times on a heavily loaded machine (load average up to about 89; slower than the authors' runs):
- first runs: 0.10 729 s, 0.20 652 s, 0.30 542 s, 0.40 438 s, 0.50 394 s;
- second (traced) runs: 0.10 481 s, 0.20 432 s, 0.30 263 s.
- Every run reported 10 of 10 families "ok", with the same row counts as the claimed runs.

`cmp` of each re-predicted test/P/FAM/result-P.tsv against attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv:
```
P 0.10: 10 of 10 result files byte-identical (cmp)
P 0.20: 10 of 10 result files byte-identical (cmp)
P 0.30: 10 of 10 result files byte-identical (cmp)
P 0.40: 10 of 10 result files byte-identical (cmp)
P 0.50: 10 of 10 result files byte-identical (cmp)
```

Determinism: a second, independent retrain (with file tracing) at 0.10, 0.20 and 0.30, in new folders:
```
second (traced) run P 0.10: 10 of 10 byte-identical
  model files identical between my two retrains at 0.10: 11 of 11
second (traced) run P 0.20: 10 of 10 byte-identical
  model files identical between my two retrains at 0.20: 11 of 11
second (traced) run P 0.30: 10 of 10 byte-identical
  model files identical between my two retrains at 0.30: 11 of 11
```

My scorer on my retrained files gives exactly the values of section 3, with A(ltr over P) BCFS = 0.7422025452564412.

| P | retrained test-P files bit-identical to claimed | recomputed mean BCFS S(P) (ltr) | Mockingbird-I1 official S(P) |
|---|---|---|---|
| 0.10 | yes, 10/10 (two independent retrains) | 0.8091752827860231 | 0.7672735092897016 |
| 0.20 | yes, 10/10 (two independent retrains) | 0.7629197798251665 | 0.7119659170836019 |
| 0.30 | yes, 10/10 (two independent retrains) | 0.7347693490340722 | 0.6717099225519634 |
| 0.40 | yes, 10/10 | 0.7136377968288752 | 0.6428278176401176 |
| 0.50 | yes, 10/10 | 0.690510517808069 | 0.6050308536957327 |
| A (left to right) | 50/50 | 0.7422025452564412 (builtin sum also 0.7422025452564412) | 0.6797616040522236 (builtin 0.6797616040522234) |

## 6. What the entry reads at each P
**Code reading** (attempts/classifier/frozen/PRIMARY/code/system.py and config.json):
- The train command reads the manifest, its surprise_train files, and, through config "devx", dev_dir/DEVFAM/training-0.10.tsv. The loop is hard-coded to that one file name; dev test-0.10 files are not used.
- The predict command reads only the model folder (opts.json and model-FAM.pkl) and the partition files named in the jobs file.
- Options come from config.json. The only other source is the CLS_OPTS environment variable, which the harness does not set.
- No solutions, cognates, wordlist, systems or results path appears in the code. I found no network or subprocess use apart from the multiprocessing training pool.

**Runtime trace.** I added a Python audit hook (a sitecustomize on PYTHONPATH, inherited by the harness's system processes and their spawn workers) that logged every open() and directory listing. The harness itself ran unhooked. Files under claim/data opened by the system's processes:
- P 0.10: data/view/dev/listsamplesize/training-0.10.tsv and data/view/surprise/FAM/training-0.10.tsv for the 10 families.
- P 0.20: data/view/dev/listsamplesize/training-0.10.tsv and the 10 surprise training-0.20.tsv.
- P 0.30: data/view/dev/listsamplesize/training-0.10.tsv and the 10 surprise training-0.30.tsv.
- P 0.40: data/view/dev/listsamplesize/training-0.10.tsv and the 10 surprise training-0.40.tsv.
- P 0.50: data/view/dev/listsamplesize/training-0.10.tsv, data/view/dev/mannburmish/training-0.10.tsv and the 10 surprise training-0.50.tsv.

Other files and events in the trace:
- Predict processes opened only RUNOUT model/opts.json, model/model-FAM.pkl, parts/jobs.tsv and parts/part-NN.tsv (read), parts/pred-NN.tsv (write), and the code files.
- Every P reported "FORBIDDEN-NAME OPENS: 0" (no path matching solution, cognates, wordlist, cldf, systems/ or results/).
- No socket, exec or subprocess audit event was recorded.
- The only non-library directory listings were the code folder and the working directory (claim/). These are import-machinery listings; no file in them was opened.

So no solutions, cognates or wordlist file is read, no test-P file is read except through the harness partitions, and no surprise file of another proportion is read. The dev files are named training-0.10.tsv at every P, but they belong to development families; this is disclosed, and PREREG rules 4 and 6 allow it.

Precision note on the CLAIM.md disclosure: mannburmish rows enter only at 0.50. At 0.10 to 0.40 they are not read, because of config "max_nref": 30 for hillburmish and its "pool": 0. listsamplesize rows (for kesslersignificance) are read at every P. The disclosure says more than actually happens, so this is not a concealment.

## 7. Row isolation (each row predicted from its own row only)
My own test, independent of tools/q15h.py audit, used my retrained models and three parts:
- (b) Every masked row of every family written to its own single-row file, all of a family's files predicted in one predict process.
- (a) 5 random rows per family (my seed) each predicted alone in a fresh process.
- (c) One whole partition per family with its rows in reversed order.

Each prediction was compared with the claimed result cell:
```
ROWISO 0.10 single-row files in one process: 4029/4029 identical; single rows in fresh processes: 50/50; reversed partitions: 403/403
ROWISO 0.10 PASS
ROWISO 0.20 single-row files in one process: 7887/7887 identical; single rows in fresh processes: 50/50; reversed partitions: 751/751
ROWISO 0.20 PASS
ROWISO 0.30 single-row files in one process: 11586/11586 identical; single rows in fresh processes: 50/50; reversed partitions: 1080/1080
ROWISO 0.30 PASS
ROWISO 0.40 single-row files in one process: 14992/14992 identical; single rows in fresh processes: 50/50; reversed partitions: 1424/1424
ROWISO 0.40 PASS
ROWISO 0.50 single-row files in one process: 18101/18101 identical; single rows in fresh processes: 50/50; reversed partitions: 1790/1790
ROWISO 0.50 PASS
```
Every one of the 56,595 claimed predictions is reproduced from an input file that contains only its own row. predict_row in the code uses only the row's visible cells and the loaded model; its only module-level cache is a memo of sound classes per segment.

## 8. Notes (none changes the verdict)
- The null test's reported real d is 0.062440941204217726. My A difference is 0.062440941204217615. The two differ only in the last digits, consistent with a different float summation order. The null test is not this skeptic's check, and both values are far above 1e-9.
- The claimed predictions at 0.30 and 0.50 were produced by the main session (20:49Z and 21:03Z) before selection.md (21:16:09Z). They are gold-free predictions from the frozen code, and I reproduced them bit for bit.
- Training uses an internal 2-process pool, so each of my parallel proportion runs used up to 3 processes during its training phase.
- No injection_suspected: no web content was read.

pass: true