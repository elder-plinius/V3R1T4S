(Saved by the main session at 2026-10-18T12:37:59Z from the reproduce skeptic subagent's returned text (cell B50; Opus 5.5, agent ae26e76bcbd6ef62c); the subagent could not write a file named like a report. Text verbatim below.)

# Panel: REPRODUCE skeptic, cell B50 (proportion 0.50, mean BCFS), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE
start: 2026-10-18T11:44:27Z (date -u)
end: 2026-10-18T12:36:28Z (date -u)
material: the claim package only (paths below are relative to claim/), the kit rules, the interpreters SYS and SCO and my own python3.13. I wrote my scratch scripts and outputs in my own work folder, outside claim/. Network: none used. No request was made, so nothing was appended to the stop list. injection_suspected: none.

## Verdict in one sentence
I reproduced the claim end to end. The pinned scorer, run with left-to-right summation, matches Mockingbird-I1's official 0.50 values exactly. My own scorer gives the claimed mean BCFS 0.7114179305724276 in both summation modes, against the recomputed FeVeT bar 0.6423935720824072. All 8 stage-2 entries, retrained from their frozen code (each once inside a sandbox that denies gold, test files and earlier outputs), give byte-identical test-0.50 predictions. My own implementation of the per-item MBR rule rebuilds combiner/test/0.50 byte for byte. Every partition and a sample of single rows give identical predictions when each runs alone in a sealed process. PROVED-HERE

## Definition used (quoted)
The success criterion in definition/Q15.json, verbatim: "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

The statistic comes from official/src/sigtypst2022.py, compare_systems:
    results[stm][dataset] = compare_words(data_path.joinpath(dataset, "solutions-{0:.2f}.tsv".format(proportion)), system_path.joinpath(system, partition, dataset, "result-{0:.2f}.tsv".format(proportion)), report=False)[-1][1:]
    ...
    results[stm]["total"] += [statistics.mean([row[i] for row in totals])]
That is, [ED, NED, BCFS, BLEU] per family from compare_words, and the system value is statistics.mean over the 10 surprise families.

## Check 1: my own scorer, calibrated on Mockingbird-I1 (PROVED-HERE)
I wrote scripts/myscore.py before reading any author code. It loads official/src/sigtypst2022.py through importlib under the module name sigtypst2022, using the SCO interpreter (lingpy 2.6.9, lingrex 1.2.0). It calls compare_words(solutions-0.50.tsv, result-0.50.tsv, report=False)[-1][1:] for each family and takes statistics.mean over the 10 families. It has two modes:
- ltr: builtin sum is replaced by a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces.
- builtin: Python 3.13 builtin sum.

Mockingbird-I1 (official/systems/mockingbird-i1/surprise/FAM/result-0.50.tsv) compared with the "Mockingbird-I1" entry of official/results/results-surprise-0.50.json, output copied:
    ltr compared 44 values (10 families + total x 4 metrics); differing: 0
    builtin compared 44 values (10 families + total x 4 metrics); differing: 21
    (builtin, e.g.: ('total', 3, 0.5337187296541888, 0.5337187296541887), ('wangbai', 3, 0.6048226940083821, 0.604822694008381))
    SYSTEM mockingbird ltr ED NED BCFS BLEU 1.4169823165005235 0.35176136367373956 0.6050308536957327 0.5337187296541888
So the ltr mode matches the official values bit for bit. The builtin mode differs only in the last digits.

## Check 2: claimed value and bar (PROVED-HERE)
I converted FeVeT's published files (fevet/pred_0.50_FAM.tsv) into the official layout with my own converter (scripts/fevet_to_official.py). For every family: missing 0, unknown 0, dup 0, gold_col_mismatch 0. For example, "beidazihui gold_items 4921 fevet_rows 4921 missing 0 unknown 0 dup 0 gold_col_mismatch 0". Total: 18101 items. The package's tools/fevet_to_harness.py output is byte-identical to my conversion in 10 of 10 families.

    SYSTEM candidate ltr ED NED BCFS BLEU 1.0166617451971307 0.24912258145405175 0.7114179305724276 0.6520222200978466
    SYSTEM candidate builtin ED NED BCFS BLEU 1.0166617451971307 0.24912258145405175 0.7114179305724276 0.6520222200978465
    SYSTEM fevet ltr ED NED BCFS BLEU 1.286021835157271 0.30880111347517586 0.6423935720824072 0.5768215755932388
    SYSTEM fevet builtin ED NED BCFS BLEU 1.286021835157271 0.30880111347517586 0.6423935720824072 0.5768215755932388
    margin ltr 0.06902435849002042 margin builtin 0.06902435849002042 margin > 1e-9 both: True
    vs Mockingbird-I1 (ltr): 0.10638707687669491
The candidate is combiner/test/0.50/FAM/result-0.50.tsv. The claimed BCFS (0.7114179305724276), the bar (0.6423935720824072) and the ED, NED and BLEU values in CLAIM.md all match. Rule 12 (i) holds in both summation modes.

Per-family BCFS (ltr): the candidate beats FeVeT in all 10 families.
| family | candidate | FeVeT | Mockingbird-I1 | candidate minus FeVeT |
|---|---|---|---|---|
| bantubvd | 0.736765 | 0.695978 | 0.605223 | +0.040788 |
| beidazihui | 0.849633 | 0.802986 | 0.803904 | +0.046647 |
| birchallchapacuran | 0.617283 | 0.499038 | 0.439851 | +0.118245 |
| bodtkhobwa | 0.805630 | 0.754436 | 0.702295 | +0.051194 |
| bremerberta | 0.672607 | 0.571330 | 0.620276 | +0.101277 |
| deepadungpalaung | 0.788406 | 0.704891 | 0.602416 | +0.083516 |
| hillburmish | 0.637283 | 0.576844 | 0.513843 | +0.060439 |
| kesslersignificance | 0.402951 | 0.345583 | 0.303937 | +0.057368 |
| luangthongkumkaren | 0.868615 | 0.791823 | 0.800249 | +0.076792 |
| wangbai | 0.735007 | 0.681028 | 0.658315 | +0.053979 |

My own consistency check of object/predictions-0.50.tsv against combiner/test/0.50:
    masked test items: 18101 object rows: 18101 keys equal: True values equal: True empty predictions: 0
The package's checker (python3 checker/check_q15.py . object/predictions-0.50.tsv) ends:
    3. object mean BCFS 0.7114179305724276 over 18101 items (claimed 0.7114179305724276): EQUAL
    4. rebuilt official-format files equal to the frozen ones: 10 of 10
    PASS

## Check 3: integrity of saved files (PROVED-HERE)
- shasum -a 256 -c MANIFEST.sha256: rc=0, 379 OK, 0 not OK. Run at the start and again at the end, after cleanup.
- fevet/expected.sha256: all 10 pred_0.50 files OK. The 0.10 and 0.30 lines in that file name files that are not in the package, and they are not used.
- data/view: 40 of the 42 lines of data/view_manifest.sha256 are OK. The two others, data/view/datasets.json and data/view/datasets-surprise.json, are metadata files absent from the package. No entry's code and not the harness mention "datasets" (grep), and the retrains reproduced byte for byte without them. The surprise training-0.50 and test-0.50 files in data/view are byte-identical (cmp) to official/data-surprise.
- Freeze records: my own scripts/check_freeze.py parses each attempts/LENS/FROZEN.md block. Output: ALL_FREEZE_OK. For each of the 8 entries:
  - every code file's sha256 matches, with no unlisted files;
  - every val/0.50 file matches;
  - for this run's entries, every test/0.50 file matches FROZEN.md;
  - for the carried r0202 entries, the 10 test/0.50 files match CARRIED.md, and CARRIED's code_tree_sha256 equals the 0202 record (True for both).
  - code_tree_sha256 and results_tree_sha256 reproduce as the sha256 of the sorted "sha  path" lines (for example, broker/PRIMARY a8f295186339fbdbafa43d3ed1606281f91e1f40b6619efb53c0c2e29b7a4e5e and 39ded20f82d73b29dbb8fb752877dd2eb8bc02a96c0b4b38f3634b11df0b3da1).
- Validation split: my own scripts/check_val.py output is VAL_SPLIT_OK. For each family:
  - shared/val/0.50 train rows are identical to training-0.50 rows;
  - every val row's visible cells plus its solution rebuild a training-0.50 set (0 mismatches);
  - train sets plus val sets equal the training-0.50 sets;
  - training-0.50 sets are disjoint from the test-0.50 sets.

## Check 4: retraining every entry, PREREG rule 12 (iv) (PROVED-HERE)
The harness was tools/q15h.py run --code attempts/LENS/frozen/ROLE/code --mode test --props 0.50 --workers 2, with OMP/MKL threads set to 2, a fresh HOME and BRK_DEV unset, writing into fresh scratch folders. The training manifest written by the harness lists only data/view/surprise/FAM/training-0.50.tsv (10 files) and dev_dir data/view/dev.

The sandbox (macOS sandbox-exec, network denied) blocks reads of:
- claim/official, shared, combiner, fevet, object, rules, checker, scout;
- every attempts/*/frozen/*/test and val folder;
- every data/view/surprise/*/test-0.50.tsv;
- any path containing "solutions";
- my own output folders (and, in the second batch, my first retrain folder).
A probe confirmed that test-0.50.tsv, sigtypst2022.py and the frozen results are DENIED, while training-0.50.tsv, the dev files and the code are READABLE.

Run 1: the first 5 entries were trained without the sandbox; analogist, r0202-analogist and phylo were trained inside it. Run 2: the 5 entries trained without the sandbox in run 1 were trained again inside it. Every run gave "CMP LENS/ROLE: 10 of 10 families byte-identical".

## Check 5: row isolation and file access
Static audit (HEURISTIC, by reading the code): I grepped every system.py for open, glob, listdir, walk, Path, solution, cognate, wordlist, other-proportion strings, environ, subprocess, network modules and pickle.load, and read the train and predict functions.
- train reads only the manifest's training-0.50 files.
- broker/PRIMARY and broker/SECONDARY also read data/view/dev/FAM/training-0.10.tsv, to learn a universal substitution table. classifier PRIMARY and SECONDARY read data/view/dev/mannburmish and listsamplesize training-0.10.tsv (the devx rows). PREREG rule 4 permits the development view.
- predict reads only the model folder and the partition files named in --jobs. State is rebuilt fresh for every row.
- No entry reads any solutions, cognates or wordlist file, or any surprise file of another proportion.
- No network code.
- phylo/PRIMARY sets HOME to a folder beside its frozen code and writes a lingpy cache there. I deleted it after my runs, together with the __pycache__ folders my runs created in official/src and tools. The claim file list is identical to the start (380 files), and MANIFEST still shows 379 OK.

Dynamic checks with my own scripts (PROVED-HERE):
- scripts/iso_entry.py rebuilds the masked-language partitions from data/view/surprise/FAM/test-0.50.tsv. It predicts each partition alone, in its own fresh process, under a sandbox that denies data/, gold, outputs, every other partition and the harness's partition folders. It then merges the predictions in the harness layout and compares them byte for byte with the frozen result files. All 8 entries: "partitions 99 failed 0 families identical 10 of 10" and "ISO LENS/ROLE PASS".
- scripts/row_entry.py takes 5 random rows per family (my seed 5050), 50 rows per entry, and predicts each row alone in a sandboxed fresh process. All 8 entries: "50 of 50 single rows ... identical to the frozen prediction: PASS".
- Each entry's audit_test_0.50.txt ends "AUDIT PASS" with 40 identical. The rules/sealed_new_0.50.log and rules/sealed_carry_0.50.log files end "SEALED_CHECK 0.50 PASS". These are the package's own records; I did not rerun them.

## Check 6: stage-2 combination (PROVED-HERE)
- My own implementation (scripts/my_mbr.py) follows the rule in the tools/stage2.py docstring. For each item, it outputs argmin over i of sum_j w_j * NED(c_j to c_i), where NED is the scorer's per-item value (nw_align from sigtypst2022; an empty prediction becomes 2*len 'Ø'; an empty pseudo-gold row stays 0). Ties go by adjusted score + 1e-7*(3 - w_i) + 1e-9*i. It uses the weights in combiner/combiner_fit.json "0.50" "weights_all10" = [1, 2, 3, 2, 2, 1, 0, 2] (equal to the weight_at_0.50 values in entries.json) and the entry order of combiner/entries.json. I also ran an exact-fraction version of the same rule.
  - Output: "MY_MBR vs combiner/test/0.50: 10 of 10 byte-identical".
  - The float and exact versions never disagree (float_vs_exact_disagree 0 in every family), and the smallest gap between best and second-best score is 1.0e-9.
  - Items whose chosen string comes only from a weight-0 entry: 4+3+2+0+0+1+7+0+0+3 = 20 (bantubvd 4, beidazihui 3, birchallchapacuran 2, deepadungpalaung 1, hillburmish 7, wangbai 3). This matches the claim's "20 of the 18101".
  - Scored with my scorer: SYSTEM mymbr ltr ED NED BCFS BLEU 1.0166617451971307 0.24912258145405175 0.7114179305724276 0.6520222200978466.
- Since every retrained test file is byte-identical to the frozen one, the combination of the retrained predictions is the same file.
- Refit with the package tool (SCO -I tools/stage2.py --entries over the frozen entries in entries.json order, --val-test-root shared/val, --props 0.50):
    0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507
    stage2 refit test/0.50 vs combiner/test/0.50: 10 of 10 byte-identical
    stage2 refit val/0.50 vs combiner/val/0.50: 10 of 10 byte-identical
  Every field of combiner_fit.json except seconds and entry_dirs is EQUAL: weights_all10, lofo_weights, lofo_val_mean, single_entry_val_mean, lofo_val_scorer_total and the rest.

## Check 7: null test rerun with the package tool (PROVED-HERE that the tool gives these numbers)
python3 -I tools/null_test_metric.py --metric bcfs (candidate combiner/test/0.50, bar = FeVeT converted by tools/fevet_to_harness.py):
    real: candidate bcfs 0.7114179305724277, bar 0.6423935720824072, d = 0.06902435849002053
    controls: 400
    best_control: 0.010059480747746763
    real_beats_all_controls: yes
    controls >= real: 0
These match CLAIM.md. The tool's stdlib metric gives 0.7114179305724277; the official ltr scorer gives 0.7114179305724276. The two differ by one unit in the last place, from summation.

## Table: what I reproduced
| object | weight | retrain runs (train s) | test-0.50 files byte-identical | 99 partitions alone, sandboxed | 50 single rows alone, sandboxed | recomputed mean BCFS (ltr) | rule 12 (iv) case |
|---|---|---|---|---|---|---|---|
| broker/PRIMARY | 1 | plain 261, sandboxed 202 | 10/10 both runs | PASS | 50/50 | 0.7019616687984177 | bit-identical |
| classifier/SECONDARY | 2 | plain 209, sandboxed 137 | 10/10 both runs | PASS | 50/50 | 0.6857705765369353 | bit-identical |
| broker/SECONDARY | 3 | plain 428, sandboxed 290 | 10/10 both runs | PASS | 50/50 | 0.7046937552779176 | bit-identical |
| r0202-broker/PRIMARY | 2 | plain 35, sandboxed 33 | 10/10 both runs | PASS | 50/50 | 0.7014250530890156 | bit-identical |
| classifier/PRIMARY | 2 | plain 457, sandboxed 135 | 10/10 both runs | PASS | 50/50 | 0.6778710220295727 | bit-identical |
| analogist/PRIMARY | 1 | sandboxed 422 | 10/10 | PASS | 50/50 | 0.6986272390353196 | bit-identical |
| phylo/PRIMARY | 0 | sandboxed 8 | 10/10 | PASS | 50/50 | 0.6969010334975051 | bit-identical |
| r0202-analogist/SECONDARY | 2 | sandboxed 43 | 10/10 | PASS | 50/50 | 0.6935686191516645 | bit-identical |
| stage-2 combination (combiner/test/0.50) | weights [1,2,3,2,2,1,0,2] | own MBR + tools/stage2.py refit | 10/10 (own MBR), 10/10 (refit; val also 10/10) | n/a (per-item rule over candidates) | n/a | 0.7114179305724276 (both summation modes) | bit-identical |

The training times are the harness "train rc=0" seconds on a shared machine; load varied a great deal. In this run every entry is bit-deterministic, so rule 12 (iv) holds through byte-identical reproduction, not through the value fallback. Each single entry also beats the bar by more than 1e-9 (True for all 8).

## Notes for the panel and the gate (do not change my verdict)
- Development-family rows: the claim discloses that classifier/PRIMARY and classifier/SECONDARY add renamed rows of the development families mannburmish and listsamplesize (data/view/dev/FAM/training-0.10.tsv) for hillburmish and kesslersignificance. Those rows may contain the same concepts as the surprise gold, in another dataset's transcription. This is within PREREG rule 4, and the file is a training-*.tsv of the task release. Whether it fits the criterion's intent is for the CRITERION skeptic. Size of the effect (NUMERICAL): those two families contribute 0.011780645306750348 of the 0.06902435849002042 margin. Setting both families to FeVeT's values would still leave a margin of 0.057243713183270074.
- Compute: during the first scoring pass (two scorer processes, about one minute, around 11:46Z) and the package checker run, up to five of my processes ran beside the three retrains for short periods. All other phases kept to three heavy processes. I started and stopped only my own processes. None were left running at the end.

pass: true