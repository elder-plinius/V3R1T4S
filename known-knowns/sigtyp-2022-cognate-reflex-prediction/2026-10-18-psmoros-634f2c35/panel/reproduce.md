(Saved by the main session from the subagent's returned text, 2026-10-18T07:15:51Z: round-2 REPRODUCE skeptic for cell C30 (Opus 5.5, Agent tool), on the round-2 claim package. The same skeptic re-issued its text at the main session's request with angle-bracket tokens written without brackets, for the kit's placeholder check; the main session verified mechanically that it is identical to the skeptic's first text apart from those tokens. Verbatim below.)

# Panel file: REPRODUCE skeptic, cell C30 (proportion 0.30, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
lens: REPRODUCE
started: Sun Oct 18 06:12:43 UTC 2026 (date -u)
ended: Sun Oct 18 06:59:15 UTC 2026 (date -u)
material: claim/ only (plus kit RULES.md). I read no other part of the run folder. I made no network requests, so I did not touch the stop list. injection_suspected: none seen.

Interpreters: SYS = the component venv (Python 3.13.2, lingpy 2.6.13, lingrex 1.4.2). SCO = the scorer venv (Python 3.13.2, lingpy 2.6.9, lingrex 1.2.0, sigtypst2022 installed). OWN = Homebrew python3.13 (3.13.2). All scratch work was in my own folder outside claim/. All jobs ran with OMP/MKL threads = 2, at most 3 heavy processes at once, and perl alarm time caps.

## Verdict (one sentence)
At proportion 0.30, I reproduced the claimed object combiner/test/0.30 byte for byte: my own retraining of all 6 stage-2 entries plus my own MBR combiner gives it again, and the pinned official scorer gives mean NED 0.22327922550091464 (left-to-right sum) and 0.22327922550091467 (builtin sum). That is below the cell's bar of 0.2632988364952282 (FeVeT's published predictions, rescored), and I recomputed the bar from the saved files. PROVED-HERE (NUMERICAL, from the commands below).

## 1. My own checker, written from the definition before reading the author's code
Criterion (definition/Q15.json, verbatim excerpt): "... whose mean score over the 10 surprise families at a declared proportion ... strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED ... The repo scorer `st2022` at a pinned commit computes the score."

How the statistic is defined, taken from official/src/sigtypst2022.py:
- `compare_words(solutions, result)[-1][1:]` gives [ED, NED, BCFS, BLEU] for one family.
- The system score is `statistics.mean` over the 10 families, as `compare_systems` does it.

My script (mine/score_mine.py) works as follows:
- It loads the pinned file official/src/sigtypst2022.py itself through importlib, under SCO.
- In left-to-right mode it replaces `sum` with a plain loop in the scorer's namespace and in lingrex.util. Before doing so it asserts that neither namespace already defines `sum`.
- In builtin mode it uses Python 3.13's builtin `sum`.
- It counts "Missing entry" messages from the scorer.

Integrity of the scorer:
- sha256 of official/src/sigtypst2022.py = 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a.
- This equals the MANIFEST line and the source of SCO's installed sigtypst2022 module ("equal True").

Calibration on Mockingbird-I1 (official/systems/mockingbird-i1/surprise/*/result-0.30.tsv against official/results/results-surprise-0.30.json):
```
mode ltr missing_entries 0
MEAN ED 1.1762187506031638 NED 0.2898984929868421 BCFS 0.6717099225519634 BLEU 0.6058548112827981
ltr per-family bit-identical to official: True | total bit-identical: True
builtin per-family bit-identical to official: False | total bit-identical: False   (last-digit differences only, e.g. BLEU total 0.6058548112827982 vs ...81; NED total equal)
```
So left-to-right mode is bit-identical to the official 2022 numbers: all 10 families x 4 metrics, plus the totals.

## 2. The claimed object, scored with my checker
Both runs report `missing_entries 0`.

Per-family values (left-to-right mode):

| family | ED | NED | BCFS | BLEU |
|---|---|---|---|---|
| bantubvd | 0.9192619915069649 | 0.21838009323747656 | 0.7763400780994074 | 0.6741023152543044 |
| beidazihui | 0.3921901528013582 | 0.11157894736842104 | 0.848248425741431 | 0.8335983521710508 |
| birchallchapacuran | 1.722130687872123 | 0.2893021307624273 | 0.6321189531006525 | 0.5580365563208514 |
| bodtkhobwa | 0.24954545454545454 | 0.10678030303030304 | 0.8518630865296456 | 0.8553520003236321 |
| bremerberta | 1.1725409836065575 | 0.22924058352849336 | 0.7128197643118173 | 0.6554213754303575 |
| deepadungpalaung | 0.46313180992736075 | 0.1615431421509282 | 0.8431828472610786 | 0.7695777982097284 |
| hillburmish | 0.9743553143329804 | 0.26194594164493984 | 0.6919044572632691 | 0.642278699475483 |
| kesslersignificance | 2.2474834814308497 | 0.5999320270372902 | 0.4506966792714886 | 0.23639569173802194 |
| luangthongkumkaren | 0.29605263157894735 | 0.08017178362573099 | 0.9022542805025109 | 0.8724170583606426 |
| wangbai | 0.5903416153527186 | 0.173917302623136 | 0.7788362858753557 | 0.7420535332750455 |

Means:
```
ltr     MEAN ED 0.9027034122955315 NED 0.22327922550091464 BCFS 0.7488264857956657 BLEU 0.6839233380559118
builtin MEAN ED 0.9027034122955314 NED 0.22327922550091467 BCFS 0.7488264857956657 BLEU 0.6839233380559119
```
All four left-to-right means equal the CLAIM.md table exactly. The builtin NED equals the claimed compensated value 0.22327922550091467.

Format check (mine/format_check.py):
- Header and COGID order are the same in test, solutions and result for all 10 families.
- Every result row has exactly one non-empty cell, and it is the masked ("?") cell, which is also the gold cell: 0 bad rows.
- 11586 masked rows in total.
- data/view/surprise/*/{training,test}-0.30.tsv are byte-identical (cmp) to official/data-surprise copies for all 10 families.

## 3. The bar, recomputed
FeVeT files:
- The sha256 of all 10 fevet/pred_0.30_*.tsv files matches fevet/FETCH_RECORD.txt.

Conversion (mine/fevet_convert.py, my own code):
- Plain tab split, no csv quoting.
- Each prediction is written into the masked cell, in solutions COGID order and header.
- Per family: missing 0, extra 0, GOLD-column mismatches 0, duplicates 0, bad lines 0, lines containing a quote 0. For example, bantubvd has 582 rows and 582 needed.

Scores:
```
ltr     MEAN ED 1.0946456488227652 NED 0.2632988364952282 BCFS 0.6986581179861967 BLEU 0.6356571184958077
builtin MEAN ED 1.094645648822765  NED 0.2632988364952282 BCFS 0.6986581179861968 BLEU 0.6356571184958079
```
The bar 0.2632988364952282 is reproduced in both modes, and the left-to-right ED/BCFS/BLEU equal CLAIM.md.

Margins:
- bar - candidate (ltr) = 0.04001961099431353, which is > 1e-9 (True).
- bar - candidate (builtin) = 0.040019610994313504, which is > 1e-9 (True).
- The ltr value equals the claim's "real d".
- Mockingbird-I1 - candidate (ltr) = 0.06661926748592747.

## 4. Integrity of the saved files
MANIFEST.sha256:
- `shasum -a 256 -c` reports 332 OK and 0 not OK.
- Files on disk = the manifest's 332 plus MANIFEST.sha256 itself.

FROZEN.md (mine/frozen_check.py) recomputes every listed code and result hash and the tree hashes. The tree hash is sha256 of the joined lines, as q15h.py freeze computes it.

| entry | frozen at | code files | code tree hash | result files present in package | test/0.30 files | results tree hash |
|---|---|---|---|---|---|---|
| analogist PRIMARY | 2026-10-18T02:43:13Z | 2/2 ok, no extra files | match | 20 ok, 0 BAD (50 listed files not shipped) | 10/10 ok | match |
| analogist SECONDARY | 2026-10-18T03:23:18Z | 2/2 ok, no extra files | match | 20 ok, 0 BAD | 10/10 ok | match |
| broker PRIMARY | 2026-10-18T03:14:07Z | 1/1 ok, no extra files | match | 20 ok, 0 BAD | 10/10 ok | match |
| broker SECONDARY | 2026-10-18T04:00:49Z | 1/1 ok, no extra files | match | 20 ok, 0 BAD | 10/10 ok | match |
| classifier PRIMARY | 2026-10-18T04:03:30Z | 2/2 ok, no extra files | match | 20 ok, 0 BAD | 10/10 ok | match |
| phylo PRIMARY | 2026-10-18T03:19:07Z | 1/1 ok, no extra files | match | 20 ok, 0 BAD | 10/10 ok | match |

(classifier SECONDARY also has a record in FROZEN.md, but it is not a stage-2 entry and its code is not shipped.)

Stage-2 entry list and weights:
- combiner/entries.json order equals combiner_fit.json["0.30"]["entries"].
- Weights at 0.30 are [2, 2, 0, 3, 0, 3] in both files.

## 5. Retraining every stage-2 entry (PREREG rule 12 (iv))
I retrained all 6 entries, the weight-0 ones included, because the per-item rule can choose their strings. Each ran with the harness claim/tools/q15h.py, `run --mode test --props 0.30`, in a fresh folder of mine. The harness writes the manifest itself: the 10 surprise training-0.30 files and data/view/dev.

Two sandbox modes (macOS sandbox-exec):
- broad: the whole harness runs under a profile that can read only the SYS venv, claim/tools, the entry's code/ and data/view, and can write only its own fresh folder. It cannot read official/, shared/, fevet/, combiner/, the frozen predictions, or anything else in the workspace. I tested the denials: solutions, frozen predictions and val gold all gave "Operation not permitted", and so did a write into claim/.
- strict: the harness is unsandboxed (I read all of q15h.py; it reads no gold). Each system.py call goes through a `--python` wrapper that sandboxes that call.
  - train may read only the venv, its code/, its own folder, data/view/dev and the 10 literal training-0.30 files. It cannot read test-0.30.
  - predict may read only the venv, code/ and its own folder (model plus partition files). It cannot read anything under data/.
  - Tests: train could not read test-0.30, solutions or frozen predictions; predict could not read training, test or dev files.

Every run's comparison is `cmp` against attempts/LENS/frozen/ROLE/test/0.30/FAM/result-0.30.tsv:
```
retrain/analogist_PRIMARY        | broad                               | train rc=0 52s  | same 10/10 DIFF 0
retrain/analogist_SECONDARY      | strict per-call: train 1 predict 10 | train rc=0 62s  | same 10/10 DIFF 0
retrain/broker_PRIMARY           | broad                               | train rc=0 121s | same 10/10 DIFF 0
retrain/broker_SECONDARY         | strict per-call: train 1 predict 10 | train rc=0 98s  | same 10/10 DIFF 0
retrain/classifier_PRIMARY       | broad                               | train rc=0 367s | same 10/10 DIFF 0
retrain/phylo_PRIMARY            | strict per-call: train 1 predict 10 | train rc=0 8s   | same 10/10 DIFF 0
retrain_strict/analogist_PRIMARY | strict per-call: train 1 predict 10 | train rc=0 65s  | same 10/10 DIFF 0
retrain_strict/broker_PRIMARY    | strict per-call: train 1 predict 10 | train rc=0 118s | same 10/10 DIFF 0
retrain_strict/classifier_PRIMARY| strict per-call: train 1 predict 10 | train rc=0 356s | same 10/10 DIFF 0
```
The 3 entries first retrained broad were retrained again strict: byte-identical both times.

I also reran the val-0.30 predictions (the inputs to the weight fit) strict, in the same way. Train could read only shared/val/0.30/FAM/train.tsv plus dev. All 6 entries: same 10/10, DIFF 0, train rc=0.

Determinism, per component (the rule 12 (iv) case that holds):
- All 6 entries are bit-deterministic in my runs: every retrain in fresh processes reproduced the frozen bytes exactly.
- broker/PRIMARY, analogist/PRIMARY and classifier/PRIMARY did so in two independent test-0.30 trainings.
- So the "non-deterministic, recomputed NED must beat the bar" fallback is not needed for any entry.

Problem with my own setup, now fixed: my first classifier attempt exited with train rc=1 after 0 s. The cause was my wrapper: it started the job from a parent folder that the sandbox could not read, so `os.getcwd()` failed with "Operation not permitted". I fixed the wrapper by cd-ing into the job folder; the rerun is the row above.

## 6. Row isolation: my own sealed check (mine/sealed_mine.py, my code, not tools/sealed_check.py)
Using the models from my retrains, I made two kinds of fresh-process predictions:
- Each test-0.30 partition (the rows of one masked language; asserted to hold no two rows of one cognate set) predicted alone.
- 3 random single rows per family, each predicted alone.

Each process ran in its own sandbox that could read only the venv, code/, the model dir and that partition's own folder.
```
SEALED_MINE analogist/PRIMARY:   129 sealed processes, 84s,   PASS
SEALED_MINE broker/PRIMARY:      129 sealed processes, 335s,  PASS
SEALED_MINE classifier/PRIMARY:  129 sealed processes, 148s,  PASS
SEALED_MINE analogist/SECONDARY: 129 sealed processes, 68s,   PASS
SEALED_MINE phylo/PRIMARY:       129 sealed processes, 1250s, PASS
SEALED_MINE broker/SECONDARY:    129 sealed processes, 412s,  PASS
```
For every entry and every family:
- Partitions predicted alone matched the frozen predictions on every row (for example beidazihui 19 partitions, 2945/2945).
- The merged file was byte-identical to the frozen result file.
- The single rows predicted alone were identical: 3/3.

Saved harness audits (attempts/*/frozen/*/audit_test*.txt): each of the 6 has 40 "identical" lines at 0.30, 0 FAIL/MISMATCH lines, and ends "AUDIT PASS". rules/sealed_check_0.30.log and rules/sealed2_check_0.30.log end "SEALED_CHECK 0.30 PASS".

## 7. Code audit (what the component code reads)
- Every system.py reads only the files it is given:
  - train: `man["surprise_train"][fam]` (analogist/broker/classifier/phylo); no entry uses dev_dir.
  - predict: its own --model-dir and the partition files named in --jobs.
  - its own config.json.
- A grep for open/np.load/pathlib/glob/listdir/walk/subprocess/socket/urllib/exec/eval/importlib, and for the strings solutions/cognates/wordlist, other proportions and absolute paths, finds nothing else.
- Environment overrides exist but were inactive in my runs: broker reads BRK_* only when BRK_DEV=1, and classifier reads CLS_OPTS. I unset both in every run (`env | grep` showed none set).
- phylo sets HOME to code/../home. Under my sandbox it fell back to a temporary folder, and its output was still byte-identical.
- The strict sandbox runs above enforce all of this mechanically: no gold, no test file at train time, no other proportion, and predict cannot reach data/.

## 8. Stage-2 combination (my own MBR implementation, mine/mbr_mine.py)
The rule, taken from the docstring of tools/stage2.py only:
- Output argmin_i of sum_j w_j·NED(c_j→c_i) + 1e-7·(3−w_i) + 1e-9·i.
- NED(a→b) is the scorer's per-item value, using the pinned module's nw_align; an empty b becomes 2·len(a) 'Ø'.

Results:
- From the FROZEN component predictions with weights [2,2,0,3,0,3]: same 10/10 against combiner/test/0.30 (cmp).
- From MY RETRAINED component predictions: same 10/10 against combiner/test/0.30. Scoring this output gives ltr NED 0.22327922550091464 and builtin 0.22327922550091467.
- Chosen entry counts: broker/PRIMARY 295, analogist/SECONDARY 87, broker/SECONDARY 0, phylo/PRIMARY 9916, analogist/PRIMARY 6, classifier/PRIMARY 1282.
- Items whose chosen string comes only from a weight-0 entry: 6, all from analogist/PRIMARY:
  - bantubvd 1418-1 and 2893-8
  - kesslersignificance 560-1, 1155-4 and 421-5
  - wangbai 3536-5

  This is exactly CLAIM.md's list.

Weight refit with tools/stage2.py:
- Run under a sandbox with no read access to official/, combiner/ or fevet/ (SCO, STUB_MPL=1, --props 0.30).
- It printed "0.30 weights(all 10) [2, 2, 0, 3, 0, 3] in-sample 0.229557 LOFO 0.234363".
- Refit outputs: test 10/10 and val 10/10 byte-identical to combiner/test/0.30 and combiner/val/0.30.
- These combiner_fit.json fields are equal to the shipped file: weights_all10, insample_mean_all10, lofo_val_mean, lofo_weights, single_entry_val_mean, entries, lofo_val_scorer_total and lofo_val_scorer_families.

## 9. What was reproduced

| entry | weight 0.30 | retrain (test-0.30) vs frozen | my sealed check | val-0.30 strict rerun | determinism case | test-0.30 mean NED, ltr / builtin |
|---|---|---|---|---|---|---|
| broker/PRIMARY | 2 | bit-identical 10/10 (broad and strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.23059968384985519 / 0.23059968384985519 |
| analogist/SECONDARY | 2 | bit-identical 10/10 (strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.23041045381260247 / 0.23041045381260247 |
| broker/SECONDARY | 0 | bit-identical 10/10 (strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.23762835661232398 / 0.237628356612324 |
| phylo/PRIMARY | 3 | bit-identical 10/10 (strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.24342897922878887 / 0.24342897922878887 |
| analogist/PRIMARY | 0 | bit-identical 10/10 (broad and strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.2429748003186789 / 0.2429748003186789 |
| classifier/PRIMARY | 3 | bit-identical 10/10 (broad and strict) | PASS (129) | bit-identical 10/10 | bit-deterministic | 0.24036717076520903 / 0.24036717076520903 |
| combiner (stage-2 MBR, [2,2,0,3,0,3]) | n/a | bit-identical 10/10 (own MBR from frozen and from retrained parts; stage2.py refit) | n/a (per-item rule only) | val 10/10 bit-identical (refit) | deterministic | 0.22327922550091464 / 0.22327922550091467 |

References:
- Bar (FeVeT, rescored): 0.2632988364952282 in both modes.
- Mockingbird-I1 (official): 0.2898984929868421.

## 10. Housekeeping and caveats
- I caused one change inside claim/ and undid it. My first scorer import (06:14Z) let Python write official/src/__pycache__/sigtypst2022.cpython-313.pyc into claim/. I deleted that file and its folder at once and used -B and sandboxes from then on. Final re-check:
  - MANIFEST 332 OK and 0 not OK.
  - The only file not in the manifest is MANIFEST.sha256 itself.
  - No file newer than my scorer script exists in claim/.
  - No __pycache__ remains.
- Scope: I confirm only the claim's sentence at 0.30, on mean NED. BCFS and BLEU are also better than both references, but the claim reports them and does not claim them.
- Outside my lens: novelty and status of the bar, PREREG timing and selection, and the null test. I did not rerun the null test.
- All my background processes have ended (checked by PID).

pass: true
