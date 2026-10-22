(Saved by the main session at 2026-10-18T13:18:27Z from the reproduce skeptic subagent's returned text (cell L30; Opus 5.5, agent a2c845e83cfe329b5); the subagent could not write a file named like a report. Text verbatim below.)

# Panel file: REPRODUCE skeptic, cell L30 (proportion 0.30, mean BLEU), private-quarry-B (charter Q15)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE skeptic (one of three, fresh context; material = the claim package only, plus kit/RULES.md)
start: Sun Oct 18 12:53:15 UTC 2026 (date -u)
end: Sun Oct 18 13:12:50 UTC 2026 (date -u)
network: none. No HTTP request was made, so nothing was added to the stop list. injection_suspected: none seen.

Verdict in one sentence (PROVED-HERE): I retrained all six frozen entries of combiner/entries.json from their frozen code on training-0.30 alone, twice: once with the harness and once in my own read-sandbox, with every test partition predicted alone. All 60 test-0.30 files came out byte-identical to the frozen ones. My own implementation of the PREREG.v2 BLEU-MBR rule, run on those predictions, rebuilds combiner/test/0.30 byte for byte. Under the pinned official scorer that object scores mean BLEU 0.6874377388475998 in both summation modes, above the bar 0.6839233380559118 by 0.003514400791688077 (left-to-right) and by 0.003514400791687966 (builtin sum).

## 0. Definition used for my checker (quoted before I read any of the authors' code)

definition/Q15.json "success_criterion" (verbatim): "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

How the statistic is defined, quoted from official/src/sigtypst2022.py, compare_systems:
`results[stm][dataset] = compare_words(data_path.joinpath(dataset, "solutions-{0:.2f}.tsv".format(proportion)), system_path.joinpath(system, partition, dataset, "result-{0:.2f}.tsv".format(proportion)), report=False)[-1][1:]` ... `results[stm]["total"] += [statistics.mean([row[i] for row in totals])]`

Inside compare_words, item BLEU is `bleu_score(entryA, entryB, n=4, trim=False)`, with the gold in the first slot and an empty prediction replaced by `(2 * len(entryA)) * ["Ø"]`. Each language's value is `sum(...)/len(scores)`, and TOTAL is `sum(...)/len(languages)`.

My checker is mine/score.py, in my scratch folder outside claim/. It loads official/src/sigtypst2022.py by path, calls compare_words per family, and takes statistics.mean over the 10 families. It runs in two modes:
- ltr: builtin sum shadowed by a left-to-right loop in the sigtypst2022 and lingrex.util namespaces.
- builtin: Python 3.13's builtin sum.

Interpreters:
- SCO: Python 3.13.2 with lingpy 2.6.9 and lingrex 1.2.0. Its installed sigtypst2022.py has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, identical to official/src/sigtypst2022.py.
- SYS: the entries' ML venv.
- A system Python 3.13 for my standard-library scripts.

Order of work: I read CLAIM.md, REPRODUCE.md, the PREREGs and the official scorer, then wrote the checker. I started the harness retrains (running tools/q15h.py without reading it) before writing the checker, to save time. I first read tools/*.py, checker/ and the entries' code after my checker had produced the numbers in section 1.

## 1. Scores with my checker (real output)

```
mock ltr  ED NED BCFS BLEU 1.1762187506031638 0.2898984929868421 0.6717099225519634 0.6058548112827981
mock bltn ED NED BCFS BLEU 1.1762187506031638 0.2898984929868421 0.6717099225519634 0.6058548112827982
cand ltr  ED NED BCFS BLEU 0.8901395410281422 0.22149461586532132 0.7502543049557795 0.6874377388475998
cand bltn ED NED BCFS BLEU 0.8901395410281423 0.22149461586532132 0.7502543049557795 0.6874377388475998
bar ltr  ED NED BCFS BLEU 0.9027034122955315 0.22327922550091464 0.7488264857956657 0.6839233380559118
bar bltn ED NED BCFS BLEU 0.9027034122955314 0.22327922550091467 0.7488264857956657 0.6839233380559119
fevet ltr  ED NED BCFS BLEU 1.0946456488227652 0.2632988364952282 0.6986581179861967 0.6356571184958077
fevet bltn ED NED BCFS BLEU 1.094645648822765 0.2632988364952282 0.6986581179861968 0.6356571184958079
object ltr  ED NED BCFS BLEU 0.8901395410281422 0.22149461586532132 0.7502543049557795 0.6874377388475998
object bltn ED NED BCFS BLEU 0.8901395410281423 0.22149461586532132 0.7502543049557795 0.6874377388475998
```

Key to the rows:
- mock: official/systems/mockingbird-i1, per-item 0.30 files.
- cand: combiner/test/0.30.
- bar: bar_comb_new/test/0.30.
- fevet: fevet/pred_0.30_FAM.tsv, turned into official-format files with the gold header's languages.
- object: object/predictions-0.30.tsv.

Calibration against the official JSON, and margins:
```
mockingbird ltr vs official JSON: 44 values compared, 0 differ
builtin-mode differences: 17
ltr cand-bar BLEU diff 0.003514400791688077 > 1e-9: True
builtin cand-bar BLEU diff 0.003514400791687966 > 1e-9: True
object == cand per family (ltr, all 4 metrics): True
```
The 44 values are 10 families x 4 metrics plus the 4 totals; ltr mode reproduces Mockingbird-I1 bit for bit.

Highest BLEU total in official/results/results-surprise-0.30.json: Mockingbird-I1 0.6058548112827981. Next are Mockingbird-N1-B 0.5791625685444537 and Mockingbird-N1-A 0.5779469689176259.

Candidate per-family BLEU (ltr): bantubvd 0.6752086228888102, beidazihui 0.8348134872318679, birchallchapacuran 0.5644293773200516, bodtkhobwa 0.8566239188773908, bremerberta 0.656937933452346, deepadungpalaung 0.7691830534285703, hillburmish 0.6471735122307204, kesslersignificance 0.25113407821197853, luangthongkumkaren 0.8726328601891832, wangbai 0.7462405446450793.

Every value claimed in CLAIM.md's table matches the ltr output above: candidate, bar, FeVeT and Mockingbird-I1 on ED, NED, BCFS and BLEU, plus both margins.

FeVeT files:
- All ten pred_0.30 files match fevet/FETCH_RECORD.txt sha256 ("OK" for all ten).
- 11586 rows. In 10 of 10 families the (COGID, language) set equals the gold item set, and the GOLD column equals the official gold.

Standalone package checker (`python3 checker/check_q15.py . object/predictions-0.30.tsv`):
```
1. Mockingbird-I1 mean BLEU recomputed 0.6058548112827981, official 0.6058548112827981: EXACT
2. FeVeT published predictions mean BLEU 0.6356571184958077
2. earlier object bar_comb_new/predictions-0.30.tsv mean BLEU 0.6839233380559118 (stated 0.6839233380559118): EQUAL
3. object mean BLEU 0.6874377388475998 over 11586 items (claimed 0.6874377388475998): EQUAL
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```

## 2. Integrity of the saved files

MANIFEST.sha256 (`shasum -a 256 -c`):
- 364 OK, 0 failures.
- Files present but not listed: only MANIFEST.sha256 itself. Files listed but missing: none.
- Final recheck at 13:12Z: 364 OK, 0 failures, no __pycache__.
- Self-caused event, disclosed: my first scoring run wrote official/src/__pycache__/sigtypst2022.cpython-313.pyc into claim/ (mtime 12:56:12Z, my import). I deleted it and ran with -B from then on.

FROZEN.md, my own parser (mine/check_frozen.py). It recomputes each file hash and both tree hashes the way q15h.py freeze does: the sha256 of the sorted "hash  path" lines.

| entry | frozen at (UTC) | code files | code_tree | results_tree | result files listed / in claim and identical / mismatched | test/0.30 identical |
|---|---|---|---|---|---|---|
| broker/PRIMARY | 2026-10-18T03:14:07Z | 1 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |
| analogist/SECONDARY | 2026-10-18T03:23:18Z | 2 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |
| broker/SECONDARY | 2026-10-18T04:00:49Z | 1 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |
| phylo/PRIMARY | 2026-10-18T03:19:07Z | 1 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |
| analogist/PRIMARY | 2026-10-18T02:43:13Z | 2 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |
| classifier/PRIMARY | 2026-10-18T04:03:30Z | 2 OK | OK | OK | 70 / 20 / 0 | 10 of 10 |

Summary line: "FROZEN CHECK PASS". About the table:
- "In claim and identical" counts test/0.30 plus val/0.30; the other 50 listed files are not in the package.
- No code file is unlisted, and no result file is unlisted.
- Every freeze precedes the rule-8 deadline of 05:45Z and PREREG.v2 (07:19:21Z).
- CARRIED.md: none in the package, and none is needed. All six entries are frozen in this run's attempts/LENS/FROZEN.md.

rules/bleu_freeze.md (frozen 07:22:11Z):
- The ten L30 hashes match combiner/test/0.30 (10 of 10 "OK").
- tools/stage2_bleu.py sha256 is 3e08ea61...1f00 and rules/PREREG.v2.md is b6429d19...ea20, both as recorded.
- Observation, not a failure: combiner/combiner_fit.json (sha256 6bcc7fc6...46eb) differs from the hash recorded for out/bleu_new/combiner_fit.json (5261847a...8a96). The package file is a 0.30-only extract without the "seconds" key. My rerun of stage2_bleu.py gave "rerun combiner_fit.json (without seconds) == package combiner/combiner_fit.json: True", and my independent fit (section 5) gives the same top 20.

Data:
- data/view/surprise against official/data-surprise, training-0.30 and test-0.30: 20 files, 0 differ.
- I rebuilt shared/val/0.30 from official training-0.30 with the official split_training_test_data(ratio=0.15): 30 files, 0 differ. So the weight-fit gold comes from training-0.30 only.
- Test-0.30 cognate sets are disjoint from the training-0.30 sets and from the val-0.30 sets: True.
- Sibling-row exposure: all 11586 test rows have their gold verbatim in a sibling row of the same test file. This is why the partition-alone check in section 4 is the decisive isolation test.

## 3. Code audit (no forbidden reads)

I read the train() and predict() paths and every file-open site in each code/system.py. In all six entries the only files read are:
- the manifest JSON, and manifest["surprise_train"][FAM] (the training-0.30 files);
- code/config.json (analogist, classifier);
- the model directory;
- the jobs file and the partition files it lists.

No entry reads dev_dir.

grep found no "solutions", "cognates", "wordlist", "test-", other-proportion paths, hard-coded home paths, subprocess, urllib, socket, exec, eval or importlib.

Environment hooks:
- broker reads BRK_* only when BRK_DEV=1, and classifier reads CLS_OPTS. Neither variable was set in any of my runs; `env` check printed nothing.
- phylo sets HOME to a home/ folder beside its code. phylo uses lingpy (its packaged generic sound-class tables) at train time only.

The only randomness is phylo's fixed RandomState(20261018). Predict loops create fresh per-row state (broker `scorers = {}`, analogist `sim = Sim(...)`), and no global caches were found.

## 4. Retrain and re-predict every entry (PREREG rule 12 (iv))

(a) Harness retrain in a fresh scratch run root. It contains only tools/, data/view and the six code folders: no official/, no shared/, no gold. Command per entry: `SYS -I tools/q15h.py run --python SYS --code attempts/LENS/frozen/ROLE/code --mode test --out NEW/LENS/ROLE --props 0.30 --workers 1`, with OMP_NUM_THREADS=2, MKL_NUM_THREADS=2 and HOME inside my folder; 3 entries at a time. REPRODUCE.md uses --workers 2; workers only changes parallelism. The manifest it wrote lists only the ten training-0.30 files and data/view/dev. Then `cmp` against attempts/LENS/frozen/ROLE/test/0.30:
```
broker/PRIMARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 53s; 2026-10-18T12:54:36Z to 2026-10-18T12:58:00Z
analogist/SECONDARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 29s; 2026-10-18T12:58:20Z to 2026-10-18T12:59:10Z
broker/SECONDARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 56s; 2026-10-18T12:54:36Z to 2026-10-18T12:58:32Z
phylo/PRIMARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 5s; 2026-10-18T12:58:00Z to 2026-10-18T12:59:33Z
analogist/PRIMARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 25s; 2026-10-18T12:58:32Z to 2026-10-18T12:59:17Z
classifier/PRIMARY: 10 files compared, 0 differ; train: test 0.30 train rc=0 178s; 2026-10-18T12:54:36Z to 2026-10-18T12:58:20Z
```

(b) My own sealed check (mine/sealed_mine.py), not the authors' tools/sealed_check.py. It uses a macOS sandbox-exec profile that denies file-read-data under the whole home folder. Allowed reads:
- Training: the ML venv, the entry's code and home, its model directory, and a folder holding only the ten training-0.30 files plus a copy of data/view/dev.
- Prediction: code, home, the read-only model and the folder of one single partition. Every partition (masked language) of every family was predicted alone, in its own fresh process. The results were merged in test-file order and compared byte for byte.

Each run first did a sandbox self-test: reading claim's official wangbai solutions file inside the profile must fail. It printed "rc=1 DENIED-OK" in all 6 runs. Limit: reads outside the home folder were not denied; the code audit shows no such reads.
```
SEALED broker/PRIMARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
SEALED analogist/SECONDARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
SEALED broker/SECONDARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
SEALED phylo/PRIMARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
SEALED analogist/PRIMARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
SEALED classifier/PRIMARY PASS: 99 partitions predicted alone, 0 failed, 0 of 10 families differ
```
Sealed train times: 56s, 27s, 57s, 4s, 24s and 190s, in the order above.

(c) Harness audit on my retrained outputs (`tools/q15h.py audit --mode test --props 0.30`). Per family it predicts 3 random single rows and 1 whole partition, each alone in a fresh process:
```
audit_analogist_PRIMARY.log: 40 identical, 0 FAIL; AUDIT PASS
audit_analogist_SECONDARY.log: 40 identical, 0 FAIL; AUDIT PASS
audit_broker_PRIMARY.log: 40 identical, 0 FAIL; AUDIT PASS
audit_broker_SECONDARY.log: 40 identical, 0 FAIL; AUDIT PASS
audit_classifier_PRIMARY.log: 40 identical, 0 FAIL; AUDIT PASS
audit_phylo_PRIMARY.log: 40 identical, 0 FAIL; AUDIT PASS
```
The frozen audit files in the package also end in "AUDIT PASS", each with 120 identical lines.

Which case of rule 12 (iv) holds: every entry was bit-identical to its frozen predictions in two independent trainings (a) and (b). So rule 12 (iv) holds in its first case (the run reproduces the frozen predictions) for all six entries, and the non-determinism fallback is not used.

## 5. Stage-2 combination: own implementation and refit

My implementation is mine/stage2_mine.py, written from the rule text in PREREG.v2 and the stage2_bleu.py docstring, not from its code. It outputs c_i with i = argmin over i of sum_j w_j*(1 - BLEU(c_j to c_i)) + 1e-7*(3 - w_i) + 1e-9*i:
- BLEU(a to b) = lingrex bleu_score(a, b, n=4, trim=False), with a in the gold slot.
- An empty b becomes 2*len(a) 'Ø'; an empty a contributes no risk.
- The risk is summed left to right, and the first minimum wins.
```
own combination (test, entries from frozen, weights 2,2,1,3,1,3) vs combiner/test/0.30: 10 files compared, 0 differ
own combination (val, entries from frozen, weights 2,2,1,3,1,3) vs combiner/val/0.30: 10 files compared, 0 differ
own combination (test, entries from new, weights 2,2,1,3,1,3) vs combiner/test/0.30: 10 files compared, 0 differ
```
"new" means the retrained entries from section 4(a).

My exhaustive weight fit (mine/fit_np.py) over {0,1,2,3}^6 minus the zero tuple, on shared/val/0.30 gold:
- Aggregation as compare_words does it: per-language left-to-right mean, sum over the languages with items divided by the header languages, then statistics.mean over families.
- PREREG.v2 tie rule.
```
val items: 3569
tuples searched: 4095
best: [2, 2, 1, 3, 1, 3] 0.6601872015990811
   [2, 3, 1, 3, 0, 2] 0.6601218715690348
   [1, 2, 0, 3, 0, 2] 0.6600440677945737
own top-20 == combiner_fit.json top20_exact (values and tuples, exact): True
official compare_words, combiner/val/0.30 vs shared/val/0.30 gold, mean BLEU (ltr): 0.6601872015990811
```

Rerun of the authors' tools/stage2_bleu.py on the frozen entries, in a copy of tools/:
```
0.30 weights [2, 2, 1, 3, 1, 3] val mean BLEU (in-sample) np.float64(0.6601872015990811); runner-up [2, 3, 1, 3, 0, 2] np.float64(0.6601218715690348)
tools/stage2_bleu.py rerun vs combiner/{test,val}/0.30: 20 files, 0 differ
```
I also read stage2_bleu.py. It reads test files only for keys and the masked language, and reads val gold only from the gold root (shared/val).

## 6. Null test (PREREG.v2 rule 1), rerun

Authors' tool (tools/null_test_metric.py, gold = official/data-surprise):
```
real: candidate bleu 0.6874377388475998, bar 0.6839233380559119, d = 0.003514400791687966
controls: 400
best_control: 0.0035017194380646544
real_beats_all_controls: yes
```

My own implementation (mine/null_mine.py), with the official item BLEU, compare_words aggregation and statistics.mean over families:
```
own null: candidate 0.6874377388475998 bar 0.6839233380559118 real d 0.003514400791688077; controls 400; best_control 0.0035017194380646544; controls >= real: 0; real_beats_all_controls: yes
```
Observation, not a failure: the tool averages families with a left-to-right sum divided by 10 rather than statistics.mean. Its bar 0.6839233380559119 therefore equals the builtin-mode official value, although rules/null_test.md calls it "left-to-right". The conclusion is the same both ways, and narrow: the real difference beats the best control by about 1.27e-5.

## 7. What was reproduced

| object | weight at 0.30 | harness retrain test-0.30 vs frozen | own sealed retrain, 99 partitions alone | harness audit 0.30 | FROZEN.md hashes | recomputed mean BLEU, ltr | builtin sum |
|---|---|---|---|---|---|---|---|
| broker/PRIMARY | 2 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.6773572720481368 | 0.6773572720481369 |
| analogist/SECONDARY | 2 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.674666799591828 | 0.6746667995918281 |
| broker/SECONDARY | 1 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.6698786005734902 | 0.6698786005734902 |
| phylo/PRIMARY | 3 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.6596514642479974 | 0.6596514642479975 |
| analogist/PRIMARY | 1 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.6583352796054924 | 0.6583352796054924 |
| classifier/PRIMARY | 3 | bit-identical 10/10 | PASS, 10/10 identical | 40/40 | OK | 0.6591573147847148 | 0.6591573147847148 |
| combination, own rule on frozen entries | 2,2,1,3,1,3 | test 10/10 and val 10/10 bit-identical to combiner/ | n/a | n/a | bleu_freeze 10/10 OK | 0.6874377388475998 | 0.6874377388475998 |
| combination, own rule on retrained entries | 2,2,1,3,1,3 | test 10/10 bit-identical to combiner/test/0.30 | n/a | n/a | n/a | 0.6874377388475998 | 0.6874377388475998 |
| combination, stage2_bleu.py refit | refit [2,2,1,3,1,3] | test and val 20/20 bit-identical | n/a | n/a | n/a | 0.6874377388475998 | 0.6874377388475998 |
| bar holder bar_comb_new/test/0.30 (rescored only) | n/a | n/a | n/a | n/a | n/a | 0.6839233380559118 | 0.6839233380559119 |
| FeVeT published predictions (rescored) | n/a | n/a | n/a | n/a | FETCH_RECORD 10/10 OK | 0.6356571184958077 | 0.6356571184958079 |
| Mockingbird-I1 (official per-item files) | n/a | n/a | n/a | n/a | n/a | 0.6058548112827981 (44/44 values equal the official JSON) | 0.6058548112827982 |

The entry BLEU values are those of the retrained files, which are byte-identical to the frozen files. No single entry beats the bar; only the combination does.

## 8. Scope and limits (REPRODUCE only)

- Without web access I could not check the pinned ST2022 commit, FeVeT's provenance, or whether a higher published BLEU exists at 0.30 (that is the NOVELTY skeptic's job). Within the package, official/src/sigtypst2022.py is byte-identical to the scorer venv's module and reproduces Mockingbird-I1's 44 official 0.30 values bit for bit.
- The disclosures in CLAIM.md were not tested by me: before PREREG.v2 the main session had seen the test BLEU of the entries and of COMB-NEW, and five sibling cells came out NOTHING. Whether those disclosures matter for the claim is the CRITERION skeptic's call.

Result: every check in my task passed, and no mismatch, missing object or non-determinism was found.

pass: true