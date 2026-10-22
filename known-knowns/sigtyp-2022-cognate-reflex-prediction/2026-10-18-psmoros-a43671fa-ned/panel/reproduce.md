(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the NA REPRODUCE skeptic subagent (Opus 5.5, model opus, agent a0d630272ceeed057) could not write a file named like a report. Text verbatim below.)

# Panel: REPRODUCE skeptic, cell NA (aggregate mean NED over P = 0.10 to 0.50)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE (one of three skeptics), session 2026-10-18-1758, cell NA
start: 2026-10-18T22:10:21Z (date -u)
end: 2026-10-18T22:39:05Z (date -u)
material: the claim package claim/ only, plus kit rules. No web requests were made, so no stop-list line was written. Scratch work was kept outside claim/.

## Verdict summary
- I wrote my own scorer from the definition. It matches Mockingbird-I1 bit for bit: 10 of 10 families and the total, at all five P.
- The claimed A_NED is 0.23164186694791358. I recomputed exactly this value from the claimed files and again from my own retrained predictions.
- The bar is 0.2931673956342817 and the margin is 0.0615255286863681, more than 1e-9.
- I retrained the frozen entry at each of the five proportions in fresh folders. All 50 re-predicted test-P files are byte-identical to the claimed ones, so training is bit-deterministic at every P. The bit-identical case of PREREG rule 12 (iv) holds.
- Each training ran sealed with only training-P plus two development files readable, and no test file. Each prediction ran sealed with only test-P and the model readable.
- Integrity checks pass: the package manifest, the FROZEN.md hashes, the object files against the result files, the run and audit records, and my own audit at 0.30.

## Definition used (quoted)
- Criterion (definition/Q15.json "success_criterion"): "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, ... The repo scorer `st2022` at a pinned commit computes the score."
- Aggregate (rules/PREREG.md rule 2): "A_m = (S_m(0.10) + S_m(0.20) + S_m(0.30) + S_m(0.40) + S_m(0.50)) / 5, summed left to right in that order, where S_m(P) is the family mean of metric m at P (the official "total")." For NA the bar is "Mockingbird-I1 0.2931673956342817".
- Statistic: official/src/sigtypst2022.py. compare_words(solutions, result, report=False)[-1][1:] gives [ED, NED, BCFS, BLEU] per family. S(P) is statistics.mean over the 10 families, as compare_systems computes "total".
- Scorer identity: claim/official/src/sigtypst2022.py has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. This equals the sigtypst2022 module installed in the SCO interpreter.

## Check 1: own scorer (written before reading the entry's code or the package's scoring tools)
My script loads official/src/sigtypst2022.py by file path. It scores official/data-surprise/FAM/solutions-P.tsv against each system's result-P.tsv.
- Mode L: the builtin sum is shadowed by a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces, and A is summed left to right.
- Mode B: Python 3.13's builtin sum is used everywhere.
- It ran under the SCO interpreter.

Mockingbird-I1 against official/results/results-surprise-P.json, mode L (real output):
```
MOCK L 0.10 families bit-identical to official JSON: 10/10; total identical: True
MOCK L 0.20 families bit-identical to official JSON: 10/10; total identical: True
MOCK L 0.30 families bit-identical to official JSON: 10/10; total identical: True
MOCK L 0.40 families bit-identical to official JSON: 10/10; total identical: True
MOCK L 0.50 families bit-identical to official JSON: 10/10; total identical: True
A L NED cand=0.23164186694791358 mock(recomputed)=0.2931673956342817 bar(official totals)=0.2931673956342817
NA L A_NED cand=0.23164186694791358 bar=0.2931673956342817 margin=0.0615255286863681 beats_by_more_than_1e-9=True
MOCK_CHECK PASS
```

Bar: Mockingbird-I1's A_NED is 0.2931673956342817, both from its official totals and from my recomputation. This equals the PREREG bar.

Claimed object (attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv), mode L:
```
S L P=0.10 cand ED=0.7741426354973481 NED=0.20017478183757248 BCFS=0.8091752827860231 BLEU=0.7183395130131847
S L P=0.20 cand ED=0.8518682371657778 NED=0.21213687542061813 BCFS=0.7629197798251665 BLEU=0.6960719420978517
S L P=0.30 cand ED=0.9552549562700591 NED=0.23201071558421696 BCFS=0.7347693490340722 BLEU=0.6721728449836378
S L P=0.40 cand ED=1.0267686117591617 NED=0.2455448938803044 BCFS=0.7136377968288752 BLEU=0.6533966833715619
S L P=0.50 cand ED=1.1367942567904354 NED=0.26834206801685595 BCFS=0.690510517808069 BLEU=0.624905217712099
A L ED cand=0.9489657394965564   BCFS cand=0.7422025452564412   BLEU cand=0.6729772402356671
```

I parsed the CLAIM.md values table and compared it with my mode-L recomputation: "CLAIM.md table cells equal to my recomputation (repr): 48/48". The claimed A_NED 0.23164186694791358 is equal.

Mode B (builtin sum), real output:
- Mockingbird-I1 is not bit-identical to the JSON without shadowing (0/10, 2/10, 1/10, 0/10, 1/10 families). This confirms that the left-to-right shadowing is what reproduces the 2022 values.
- "NA B A_NED cand=0.23164186694791358 bar=0.29316739563428174 margin=0.06152552868636815 beats_by_more_than_1e-9=True". This matches the claimed builtin-sum value 0.23164186694791358.

## Check 2: package integrity (from the saved files)
- shasum -a 256 -c MANIFEST.sha256: "manifest lines: 470  OK: 470". No file is missing from the manifest and no manifest entry is missing a file.
- attempts/classifier/FROZEN.md: one ROLE=PRIMARY record, frozen 2026-10-18T19:14:05Z, before the rule-8 deadline of 21:50Z.
  - "code lines match FROZEN: True"
  - "code tree recomputed: 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051 FROZEN: 4880a9cd...3051"
  - "result files matching FROZEN hashes: 20/20" (test/0.40 and val/0.50)
  - "results tree recomputed from listed lines: 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0 FROZEN: 242596c2...c11c0"
- checker/frozen_result_sha256.txt: "50/50 match". "claimed result files present: 50 of 50".
- rules/PREREG.md body (from line 5 on) has sha256 2840e8180982bdcb..., which equals the hash stated in its header.
- object/predictions-P.tsv against the result files and test-P (own stdlib script):
```
P=0.10 object rows=4029 dup=0 result-masked-rows=4029 object==result: yes; extra non-empty cells in result files: 0
P=0.20 object rows=7887 dup=0 result-masked-rows=7887 object==result: yes; extra non-empty cells in result files: 0
P=0.30 object rows=11586 dup=0 result-masked-rows=11586 object==result: yes; extra non-empty cells in result files: 0
P=0.40 object rows=14992 dup=0 result-masked-rows=14992 object==result: yes; extra non-empty cells in result files: 0
P=0.50 object rows=18101 dup=0 result-masked-rows=18101 object==result: yes; extra non-empty cells in result files: 0
OBJECT_CHECK PASS
```
  In the same pass, the data/view test-P files are identical to official/data-surprise test-P, and every test row has exactly one "?". Separately, data/view/surprise training-P equals official/data-surprise training-P for 50/50 files.
- Run records run_test_P.txt (0.10, 0.20, 0.30, 0.50): training rc=0 at every P (230 s, 203 s, 277 s, 146 s), and all 10 families "ok". The row counts sum to the object row counts; for example, at 0.10 they sum to 4029.
- Audit records audit_test_P.txt, all five P: 40 "identical", 0 FAIL, last line "AUDIT PASS".
- Sealed-check logs rules/sealed_cand_P.log, all five P:
  - 10 of 10 families "bytes IDENTICAL".
  - "predict: 99 sealed processes".
  - Final lines "SEALED_CHECK 0.10 PASS" through "SEALED_CHECK 0.50 PASS".
- The package's own checker (python3 -I checker/check_q15.py . object), run after my checks without reading its code:
  - Mockingbird-I1 is EXACT at all five P.
  - "3. Mockingbird-I1 A_NED from the official totals 0.2931673956342817 (PREREG 0.2931673956342817): EQUAL"
  - "4. object A_NED 0.23164186694791358 (claimed 0.23164186694791358): EQUAL"
  - "5. rebuilt official-format files equal to the frozen ones: 50 of 50", then "PASS".

## Check 3: retrain and re-predict at each P (PREREG rule 12 iv), sealed in two stages
- Harness: tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --props P --workers 1 --python SYS.
- Each P ran in a fresh empty scratch folder outside claim/, with OMP_NUM_THREADS=2 and MKL_NUM_THREADS=2, HOME inside my folder, and a perl alarm cap of 2400 s per stage. 0.10, 0.20 and 0.30 ran in parallel; 0.40 and 0.50 were queued as slots freed.
- Each stage ran under macOS sandbox-exec with a profile of my own. It denies file-read-data under the whole workspace except: the SYS venv, claim/tools, the entry's code/ folder, the run's own output folder and my HOME/work folders.

Stage 1 (train):
- Also readable: data/view/surprise/FAM/training-P.tsv for the current P, and only two development files: data/view/dev/mannburmish/training-0.10.tsv and data/view/dev/listsamplesize/training-0.10.tsv.
- Not readable: any test file, solutions, other proportions, official/, the frozen outputs.
- Training succeeded at every P. Real output: "test 0.10 train rc=0 807s", "test 0.20 train rc=0 735s", "test 0.30 train rc=0 640s", "test 0.40 train rc=0 321s", "test 0.50 train rc=0 273s". The machine was heavily loaded by other skeptics, with load average up to 155.
- After training, the stage-1 harness stopped, as designed, at its own partitioning step: "PermissionError ... data/view/surprise/bantubvd/test-P.tsv". The system process never needed a test file to train.

Stage 2 (predict, --skip-train):
- Readable: test-P, read by the harness to build partitions, plus the trained model and partitions in the output folder.
- Not readable: training-P, any development file and everything else.
- stage2 rc=0 at every P.
- The harness logs and all predict logs have 0 PermissionError lines at every P, so no blocked read was attempted and then swallowed during training or prediction.

The manifests written by the harness list only data/view/surprise/FAM/training-P.tsv and dev_dir data/view/dev. For example: "0.10 mode test surprise_train files: ['training-0.10.tsv'] ... dev_dir data/view/dev".

Byte comparison, cmp of each re-predicted file with the claimed attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv:
```
SUMMARY 0.10 identical=10/10
SUMMARY 0.20 identical=10/10
SUMMARY 0.30 identical=10/10
SUMMARY 0.40 identical=10/10
SUMMARY 0.50 identical=10/10
```

My scorer (mode L) on the re-predicted tree gives exactly the claimed values. "NA L A_NED cand=0.23164186694791358 bar=0.2931673956342817 margin=0.0615255286863681 beats_by_more_than_1e-9=True", and MOCK_CHECK PASS.

| P | re-predicted files bit-identical to claimed | recomputed mean NED (from retrained output) | Mockingbird-I1 official NED |
|---|---|---|---|
| 0.10 | 10/10 | 0.20017478183757248 | 0.2431316340782435 |
| 0.20 | 10/10 | 0.21213687542061813 | 0.2648052468982754 |
| 0.30 | 10/10 | 0.23201071558421696 | 0.2898984929868421 |
| 0.40 | 10/10 | 0.2455448938803044 | 0.316240240534308 |
| 0.50 | 10/10 | 0.26834206801685595 | 0.35176136367373956 |
| A (left to right) | 50/50 | 0.23164186694791358 | bar 0.2931673956342817 |

Determinism: training and prediction are bit-deterministic at all five P. These were independent retrains in fresh folders and fresh processes, on a different, heavily loaded schedule. So the bit-identical case of rule 12 (iv) holds, and the recomputed-A fallback is not needed.

## Check 4: what the entry reads, and row isolation
- Code review of code/system.py (after my scorer was written):
  - Training reads config.json, the manifest, the manifest's surprise_train files and, through config "devx", dev_dir/mannburmish/training-0.10.tsv (for hillburmish) and dev_dir/listsamplesize/training-0.10.tsv (for kesslersignificance).
  - Prediction reads opts.json and model-FAM.pkl from --model-dir, the jobs file and the partition files.
  - Nothing in the code builds a path to solutions, cognates, wordlist, systems, results or another proportion. The dev file names are fixed ("training-0.10.tsv" of the development family), so they are the same at every P.
  - The optional CLS_OPTS environment variable was not set in my runs.
- This matches the CLAIM.md disclosure, and the sealed stage 1 confirmed it empirically at each P: training succeeded with exactly those two development files readable, and no other development file and no test file.
- Row isolation:
  - Module-level state in the predict path is limited to a constant sound-class table and a CUR_FAM marker set once per process.
  - The package's audit records show 40/40 identical at each P, and the sealed-check logs show each partition predicted alone in its own process (99 per P), byte-identical.
  - My own audit (tools/q15h.py audit --mode test --props 0.30 on my retrained output folder) re-predicted single rows and one whole partition per family in fresh processes: "audit 0.30: identical=40 FAIL=0 last=AUDIT PASS".

## Disclosures about this panel's process
- Order: to launch the long retrains early, I read the harness tools/q15h.py (its docstring, the run, audit and freeze code, and the argument defaults) before writing my scorer. I did not read code/system.py, tools/score_test_040.py or checker/check_q15.py before my scorer was written and run. The checker's code was never read; it was only run.
- False start: my first retrain launch failed in 0 s because my sandbox profile denied reading the working directory, which multiprocessing spawn needs for os.getcwd. That was a fault in my profile, not the entry.
  - Before relaunching, I tested a spawn pool from a python -c snippet. It hung because of my snippet: spawned children cannot import a function defined in -c. I killed it by PID.
  - I fixed the profile and relaunched all three at 22:16:10Z. All results above come from the relaunched runs.
- Compute: the entry's training uses an internal spawn pool of 2 workers, so 3 proportions in parallel meant more than 3 OS processes of mine. I followed the instruction "Run up to 3 proportions in parallel" and used --workers 1 for prediction.
- Out of scope for REPRODUCE: the null test (rules/null_test.md) and the selection (rules/selection.md) were not re-run here.

pass: true