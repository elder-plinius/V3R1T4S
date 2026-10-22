(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the N40 REPRODUCE skeptic subagent (Opus 5.5, model opus, agent a9faa8c2a67665499) could not write a file named like a report. Text verbatim below.)

# REPRODUCE skeptic: cell N40 (proportion 0.40, mean NED), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE
start: Sun Oct 18 21:39:54 UTC 2026
end: Sun Oct 18 21:56:06 UTC 2026
material: only the claim package (claim/), the kit RULES.md, and the interpreters SYS (the entry's ML venv) and SCO (the venv with the official scorer module installed; used only as an interpreter). I made no web requests, so nothing was added to the stop list. injection_suspected: none seen (I did not open the scout html pages).

## Verdict in one sentence
I retrained the frozen classifier/PRIMARY entry from its frozen code with the harness twice: once plain, and once with each system process sandboxed so that it could read only the 10 surprise training-0.40 files and 2 development training-0.10 files during training, and no data file during prediction. Both runs reproduced all 10 test-0.40 result files byte for byte. My own scorer, after matching the official Mockingbird-I1 entry bit for bit, gives mean NED 0.2455448938803044 with left-to-right summation and 0.24554489388030437 with Python's builtin sum. Both beat the bar 0.316240240534308 by 0.0706953466540036 and 0.07069534665400362 respectively, so by more than 1e-9 in each mode.

## Definition used (quoted)
definition/Q15.json "success_criterion": "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."
The statistic is official/src/sigtypst2022.py (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a), as compare_systems computes it:
`results[stm][dataset] = compare_words(solutions-P.tsv, result-P.tsv, report=False)[-1][1:]` and `results[stm]["total"] += [statistics.mean([row[i] for row in totals])]`

## Check 1: my own scorer, written before reading any of the authors' code
My scoring script loads the pinned file official/src/sigtypst2022.py by path with SCO (Python 3.13.2, lingpy 2.6.9, lingrex 1.2.0). For each of the 10 families it calls compare_words(official/data-surprise/FAM/solutions-0.40.tsv, predictions/FAM/result-0.40.tsv, report=False)[-1][1:], then takes statistics.mean over the families. In "ltr" mode it replaces `sum` in the sigtypst2022 and lingrex.util namespaces with a plain left-to-right loop. In "builtin" mode it leaves Python's builtin sum in place.

Calibration on official/systems/mockingbird-i1/surprise/FAM/result-0.40.tsv against the "Mockingbird-I1" entry of official/results/results-surprise-0.40.json:
- ltr: all 10 families print "EQUAL" on all 4 metrics.
  - MEAN 1.272493550651723 / 0.316240240534308 / 0.6428278176401176 / 0.5723601982335171
  - "TOTAL_BIT_IDENTICAL max abs diff 0.0"
  - missing-entry messages 0
- builtin: the mean NED is still 0.316240240534308, but the mean BCFS is 0.6428278176401175, one ulp off. Several per-family values differ in the last digits. Output: "TOTAL_DIFFERS max abs diff 1.1102230246251565e-16". This is expected: Python 3.13's builtin sum is compensated. The left-to-right mode is the one that is bit-exact with the 2022 results.

## Check 2: the claimed object scored with my scorer
Files scored: attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (missing-entry messages 0 in both modes).

Per-family values, ltr mode:
| family | ED | NED | BCFS | BLEU |
|---|---|---|---|---|
| bremerberta | 1.2888991834723542 | 0.24604231412836958 | 0.6890705686574227 | 0.6260984947459621 |
| wangbai | 0.687339504571714 | 0.20103022045023938 | 0.7453397496984093 | 0.7058685887824336 |
| beidazihui | 0.3925756420035596 | 0.10776336977709974 | 0.8446805979042571 | 0.8353130901381886 |
| hillburmish | 1.0973619920237618 | 0.2930415045598018 | 0.6454293325998819 | 0.6005714430070029 |
| deepadungpalaung | 0.5775141010502853 | 0.20351674569684436 | 0.8012583356894782 | 0.715949620314872 |
| luangthongkumkaren | 0.3241486182584384 | 0.08643897155559252 | 0.8911113677575528 | 0.8622149525906906 |
| bodtkhobwa | 0.3091154909814428 | 0.132006932235699 | 0.8171628277465056 | 0.822466684196625 |
| birchallchapacuran | 1.756988426450673 | 0.2839230935858309 | 0.6199449054800916 | 0.5614710409078928 |
| kesslersignificance | 2.633152655979697 | 0.6225228428310707 | 0.38106383833251 | 0.22073285723213143 |
| bantubvd | 1.2005905027996897 | 0.27916294398249597 | 0.7013164444226421 | 0.5832800617998198 |

Means:
- ltr MEAN: ED 1.0267686117591617, NED 0.2455448938803044, BCFS 0.7136377968288752, BLEU 0.6533966833715619
- builtin MEAN: ED 1.0267686117591617, NED 0.24554489388030437, BCFS 0.7136377968288752, BLEU 0.6533966833715619

All of these equal the values in CLAIM.md exactly, in both modes.

Margins against the bar 0.316240240534308:
- ltr: 0.0706953466540036 ("beats bar by more than 1e-9: True")
- builtin: 0.07069534665400362 ("True")

Other metrics: BCFS 0.7136377968288752 against the bar's 0.6428278176401176, and BLEU 0.6533966833715619 against 0.5723601982335171, are also better. Only NED is claimed in this cell.

## Check 3: integrity of the saved files
- **MANIFEST.sha256** (`shasum -a 256 -c`): 167 OK out of 167 entries. The folder holds 167 files besides the manifest, and none is missing from either side.
  - Disclosure: my first import of the scorer wrote official/src/__pycache__/sigtypst2022.cpython-313.pyc into my copy (14:41 local, created by my own run). I deleted it and re-verified: 167/167. All later runs used -B or PYTHONDONTWRITEBYTECODE.
- **attempts/classifier/FROZEN.md**, PRIMARY record (frozen 2026-10-18T19:14:05Z):
  - code files listed 2, match 2 (config.json, system.py; the code/ folder holds exactly these 2 files)
  - code_tree recomputed 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051 = recorded
  - result files listed 20, match 20
  - results_tree recomputed 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0 = recorded
- **object/predictions-0.40.tsv**, compared with my own rebuild from the result files:
  - object rows 14992, no duplicates; test rows 14992; result rows 14992
  - empty predictions 0; rows whose filled cell is not the masked cell 0
  - solution cells 14992, all covered by result rows
  - "object == result files (keys and values): True"; differing keys 0
- **data/view/surprise/FAM/{training,test}-0.40.tsv**: byte-identical to official/data-surprise/FAM/{training,test}-0.40.tsv (20 of 20). data/view holds no solutions files: only training-0.40 and test-0.40 for the surprise families, and training-0.10 and test-0.10 for the 10 development families.
- **The authors' standalone checker**, run after my own checks (`python3 checker/check_q15.py . object/predictions-0.40.tsv`):
  - "Mockingbird-I1 mean NED recomputed 0.316240240534308, official 0.316240240534308: EXACT"
  - "object mean NED 0.2455448938803044 over 14992 items (claimed 0.2455448938803044): EQUAL"
  - "margin vs Mockingbird-I1 0.070695346654"
  - "rebuilt official-format files equal to the frozen ones: 10 of 10"
  - "PASS"

## Check 4: retrain and re-predict (PREREG rule 12 (iv))
**Run A (plain)**, in a fresh scratch folder outside claim/:
- Command: `tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --props 0.40 --workers 2 --python SYS`
- Threads: OMP/MKL/OPENBLAS = 2.
- The harness manifest lists only data/view/surprise/FAM/training-0.40.tsv for the 10 families, plus dev_dir data/view/dev.
- Log:
  - "test 0.40 train rc=0 236s"
  - then "ok" for all 10 families: bantubvd 699, beidazihui 3933, birchallchapacuran 584, bodtkhobwa 2856, bremerberta 306, deepadungpalaung 1218, hillburmish 1405, kesslersignificance 311, luangthongkumkaren 1178, wangbai 2502 rows.

**Run B (sandboxed)**, in a second fresh folder. The same harness command, but `--python` points to a wrapper that runs every system.py process under `sandbox-exec`:
- Train profile: everything under the workspace root is unreadable and unwritable except the SYS venv, the entry's code/ folder, the run's own output folder, the 10 files data/view/surprise/FAM/training-0.40.tsv, data/view/dev/mannburmish/training-0.10.tsv and data/view/dev/listsamplesize/training-0.10.tsv. Network is denied.
- Predict profile: the same, but with no data file readable at all, only the model and the partition files in the output folder.
- Probe under the train profile:
  - READABLE: training-0.40, dev mannburmish/listsamplesize training-0.10, code/config.json
  - denied (PermissionError): surprise test-0.40, official solutions-0.40, official training-0.40, dev allenbai training-0.10, dev mannburmish test-0.10, shared/val solutions, the frozen result files
- Probe under the predict profile: training-0.40, test-0.40 and dev files all denied.
- The first attempt failed with "PermissionError ... os.getcwd()" because I had started the harness from inside claim/, which the profile blocks. That was my setup error. I reran from an allowed folder: "test 0.40 train rc=0 260s", then "ok" for all 10 families with the same row counts. The wrapper log shows 10 predict and 2 train sandboxed invocations; one train invocation is the failed first attempt.

**Byte comparison** with attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (`cmp`):

| family | run A plain | run B sandboxed | sha256 (first 16) | recomputed NED (ltr) |
|---|---|---|---|---|
| bantubvd | IDENTICAL | IDENTICAL | cbf74c9d5562246e | 0.27916294398249597 |
| beidazihui | IDENTICAL | IDENTICAL | 096c896ef22e806c | 0.10776336977709974 |
| birchallchapacuran | IDENTICAL | IDENTICAL | d82e290ed3a0a833 | 0.2839230935858309 |
| bodtkhobwa | IDENTICAL | IDENTICAL | 804f2df8637d20c4 | 0.132006932235699 |
| bremerberta | IDENTICAL | IDENTICAL | 7122207b75a26d21 | 0.24604231412836958 |
| deepadungpalaung | IDENTICAL | IDENTICAL | df842a55cd8ce880 | 0.20351674569684436 |
| hillburmish | IDENTICAL | IDENTICAL | ea8df80b485f7ec0 | 0.2930415045598018 |
| kesslersignificance | IDENTICAL | IDENTICAL | b98771950df9a71c | 0.6225228428310707 |
| luangthongkumkaren | IDENTICAL | IDENTICAL | 71c83295ca2e79d4 | 0.08643897155559252 |
| wangbai | IDENTICAL | IDENTICAL | b3c23443788bb3e8 | 0.20103022045023938 |
| MEAN (both runs) | 10/10 | 10/10 | | ltr 0.2455448938803044; builtin 0.24554489388030437 |

- Model files from the two independent trainings (10 pickles plus opts.json): all "same".
- Training and prediction are bit-deterministic. The case that holds is the bit-identical reproduction of rule 12 (iv), not the fallback for a non-deterministic training.
- Scoring the retrained files with my scorer gives the same means as Check 2: ltr NED 0.2455448938803044, builtin 0.24554489388030437, ED 1.0267686117591617, BCFS 0.7136377968288752, BLEU 0.6533966833715619.

## Check 5: what the entry reads
**Code review** of system.py, after my checker was written:
- File opens are limited to: config.json; the manifest; the manifest's surprise_train files; `os.path.join(dev_dir, spec["dev"], "training-0.10.tsv")` for the two devx families; the model dir; the jobs file; and the partition files.
- Grep for solution, cognates.tsv, wordlist, data-surprise, official, shared/val, subprocess, socket, urllib, eval(, exec(: NONE.
- The only proportion literal in the code is "training-0.10.tsv", the development-family file. No surprise file of another proportion is named.
- CLS_OPTS was unset in every run.

**Sandbox (run B):** training saw only the 10 training-0.40 files and the 2 dev training-0.10 files, and prediction saw no data file at all. The output was byte-identical. So no solutions, cognates or wordlist file, no test file during training, and no file of another proportion is needed to produce the claimed object.

**What exactly the development-family rows contribute at 0.40:**
- **kesslersignificance.** It uses data/view/dev/listsamplesize/training-0.10.tsv (english, german and french renamed onto English, German and French). Retraining kesslersignificance alone with an empty dev_dir gives a different model; its training-column counts drop from English 1318, German 1069, French 334 to 228, 208, 248.
- **hillburmish.** The mannburmish rows have NO effect at 0.40. config.json has max_nref 30 and pool 0 for hillburmish, and every mapped target has at least 30 reflexes in training-0.40: AchangLongchuan 95, Bola 122, Lashi 42, Maru 108, Atsi 51. Retraining hillburmish alone with an empty dev_dir gives: "hillburmish model trained WITHOUT any dev file: byte-identical to the full-run model".
- Consequence for the claim text: CLAIM.md's disclosure, and the entry REPRODUCE.md's "mannburmish rows for the sparse targets Atsi and Lashi", overstate how the dev data is used at this proportion. The error is on the conservative side and does not affect the result. It is a wording correction for the main session, not a failure.

## Check 6: each row predicted from its own row only
- **Code review:** predict() calls predict_row(m, row, langs) on each row with only the model. The module-level caches _bc and _sc memoise pure functions of segment symbols. OPTS["eqr"] is set and restored inside each call. Nothing carries information from one row to the next.
- **Harness partitions:** the harness asserts that no partition holds two rows of one cognate set, and both runs passed it.
- **The authors' audit file** (attempts/classifier/frozen/PRIMARY/audit_test_0.40.txt): 40 lines "identical", then "AUDIT PASS".
- **My audit run** on run A (`tools/q15h.py audit --mode test --props 0.40 --rows 12`): 130 "identical" (13 per family: 12 single rows plus 1 whole partition, each alone in a fresh process), then "AUDIT PASS".
- **My cross-row test**, a stronger check of my own. For each family I put ALL rows of test-0.40.tsv in one input file, including the sibling rows whose visible cells hold the masked answers, in reversed order. Each family ran in one fresh process, and I compared the predictions with the frozen files:
  - every family rc=0 and identical: bantubvd 699/699, beidazihui 3933/3933, birchallchapacuran 584/584, bodtkhobwa 2856/2856, bremerberta 306/306, deepadungpalaung 1218/1218, hillburmish 1405/1405, kesslersignificance 311/311, luangthongkumkaren 1178/1178, wangbai 2502/2502
  - result line: "XROW PASS 14992/14992"
  - Having the answer-bearing siblings in the same input, or changing the row order, never changes a prediction.
- **Sealed-check log** (rules/sealed_cand_0.40.log, run by the main session):
  - "train ok 155s (sandboxed, strict profile)"
  - 10 of 10 families "ok ... bytes IDENTICAL" (99 sealed processes)
  - "SEALED_CHECK 0.40 PASS"
  - My runs A and B independently agree with it.

## Notes for the main session (none is a REPRODUCE failure)
1. **Dev-row disclosure.** At 0.40 only the listsamplesize rows, used for kesslersignificance, affect the predictions. The mannburmish rows are not used: the hillburmish model is byte-identical without them (Check 5).
2. **Logs cited but not packaged.** The entry's REPRODUCE.md cites final_runs.sh, final_runs.log, determinism.txt and score_val050.txt, and none of these is in the package. They are supporting logs, not the claimed object, and my two retrains establish determinism on their own.
3. **Home-directory paths (kit rule 12).** Seven package files contain an absolute home-directory path, which matters for publication and the package check: scout/scout.md, rules/frozen_entries.md, rules/selection.md, rules/PREREG.md, rules/sealed_cand_0.40.log, rules/ranking_040.md, attempts/classifier/frozen/PRIMARY/REPRODUCE.md.
4. **Scoring under SYS was not possible.** SYS cannot import the scorer: importing lingpy.evaluate fails with "ImportError: cannot import name 'lazyproperty' from 'clldutils.misc'". All scoring above used SCO, which reproduces the official Mockingbird-I1 entry bit for bit.
5. **Not rerun.** I did not rerun the null test (rule 13); it is outside this lens.

## Summary table
| item | result |
|---|---|
| scorer calibration, Mockingbird-I1 0.40 (ltr) | 40/40 family values and 4/4 totals bit-identical |
| claimed mean NED, ltr / builtin | 0.2455448938803044 / 0.24554489388030437, equal to claim |
| margin against bar 0.316240240534308 | 0.0706953466540036 (ltr), 0.07069534665400362 (builtin), both more than 1e-9 |
| MANIFEST.sha256 | 167/167 OK |
| FROZEN.md PRIMARY hashes | code 2/2, results 20/20, both tree hashes equal |
| object against result files | 14992/14992 equal |
| retrain run A (plain), test-0.40 files | 10/10 byte-identical, recomputed NED 0.2455448938803044 |
| retrain run B (sandboxed), test-0.40 files | 10/10 byte-identical, recomputed NED 0.2455448938803044 |
| determinism | models identical across 2 independent trainings; case: bit-identical |
| files read | 10 surprise training-0.40 files plus 2 dev training-0.10 files (only listsamplesize has an effect at 0.40); no solutions, cognates, wordlist or other-proportion surprise file |
| row isolation | authors' audit 40/40, my audit 130/130, cross-row test 14992/14992, sealed log PASS |

pass: true