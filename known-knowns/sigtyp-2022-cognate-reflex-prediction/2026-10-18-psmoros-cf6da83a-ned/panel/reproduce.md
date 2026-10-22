(Saved by the main session at 2026-10-18T12:37:59Z from the reproduce skeptic subagent's returned text (cell N50; Opus 5.5, agent ae0d22ce9258dc80f); the subagent could not write a file named like a report. Text verbatim below.)

# Panel file: REPRODUCE skeptic, cell N50 (run 2026-10-18-0839; proportion 0.50, mean NED, lower is better)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 11:44:25 UTC 2026
end: Sun Oct 18 12:23:45 UTC 2026

Material: only the claim package claim/ (plus the interpreters SYS = the entries' venv, Python 3.13.2 with lingpy 2.6.13, and SCO = the scorer venv, lingpy 2.6.9 and lingrex 1.2.0). No web, no network requests. Nothing was added to the stop list because no request was made. All scratch work happened outside claim/. One side effect: loading official/src/sigtypst2022.py wrote one bytecode file into claim/official/src/__pycache__. I removed it, then reran the manifest check: 380 files, 0 failures.

Order of work. First I wrote my own scorer, FeVeT converter, freeze checker and MBR combiner from the definition alone: official/src/sigtypst2022.py and the module docstring of tools/stage2.py. I did not read the authors' scoring code (tools/score_test_050.py, tools/val_scorer.py, checker/check_q15.py, the body of tools/stage2.py) until my own numbers were in. To launch the retrains early, I read only the path, run and audit sections of the harness tools/q15h.py and the entries' REPRODUCE.md notes.

## 1. Definition (quoted)
definition/Q15.json success_criterion: "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Statistic used here (from official/src/sigtypst2022.py, compare_systems):
- Per family: `compare_words(data_path/FAM/"solutions-0.50.tsv", system/FAM/"result-0.50.tsv", report=False)[-1][1:]`, which gives [ED, NED, BCFS, BLEU].
- System value: `statistics.mean` over the 10 families.
- Per item, compare_words aligns gold and prediction with lingpy nw_align. It adds 1 for every aligned position where the two symbols differ, and divides by the alignment length for NED. An empty prediction becomes 2*len(gold) copies of 'Ø'. The language value is the mean of its items. The family TOTAL is the sum of the language values divided by the number of languages.

## 2. Own checker
score.py runs under SCO. It loads claim/official/src/sigtypst2022.py by file path. Its sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a matches the module installed in SCO. It uses its own matplotlib stub. It scores in two modes:
- ltr: builtin sum shadowed by a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces.
- builtin: Python 3.13's builtin sum.

Calibration, Mockingbird-I1 (official/systems/mockingbird-i1/surprise/FAM/result-0.50.tsv) against the "Mockingbird-I1" entry of official/results/results-surprise-0.50.json, comparing every family value and the total (44 floats):
```
ltr compared 44 values; differing 0
builtin compared 44 values; differing 21   (last-bit differences only, as expected; total NED identical)
official total [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888]
```
Left-to-right mode is bit-identical to the official 2022 values.

## 3. Scores at 0.50 (own scorer; mean over the 10 surprise families)
| system | mode | ED | NED | BCFS | BLEU |
|---|---|---|---|---|---|
| candidate combiner/test/0.50 | ltr | 1.0166617451971307 | 0.24912258145405175 | 0.7114179305724276 | 0.6520222200978466 |
| candidate combiner/test/0.50 | builtin | 1.0166617451971307 | 0.24912258145405175 | 0.7114179305724276 | 0.6520222200978465 |
| FeVeT published predictions (the bar) | ltr | 1.286021835157271 | 0.30880111347517586 | 0.6423935720824072 | 0.5768215755932388 |
| FeVeT published predictions (the bar) | builtin | 1.286021835157271 | 0.30880111347517586 | 0.6423935720824072 | 0.5768215755932388 |
| Mockingbird-I1 | ltr | 1.4169823165005235 | 0.35176136367373956 | 0.6050308536957327 | 0.5337187296541888 |
| Mockingbird-I1 | builtin | 1.4169823165005235 | 0.35176136367373956 | 0.6050308536957327 | 0.5337187296541887 |

Per-family NED, ltr (candidate / FeVeT):
| family | candidate | FeVeT |
|---|---|---|
| bantubvd | 0.2593208306278457 | 0.2738211449086926 |
| beidazihui | 0.10371875635033528 | 0.14054392738603266 |
| birchallchapacuran | 0.29407274099122727 | 0.38983503575546774 |
| bodtkhobwa | 0.13754283165441863 | 0.18032880190752512 |
| bremerberta | 0.25311013538965144 | 0.33095427258419824 |
| deepadungpalaung | 0.21434757267661989 | 0.31953980246418506 |
| hillburmish | 0.3189542507627633 | 0.37126877343226733 |
| kesslersignificance | 0.5954639271891037 | 0.6725904854643949 |
| luangthongkumkaren | 0.09961844307789419 | 0.15645594584295797 |
| wangbai | 0.21507632582065814 | 0.2526729450060371 |

Margins (computed): bar minus candidate = 0.05967853202112411, more than 1e-9 in both modes; Mockingbird-I1 minus candidate = 0.10263878221968781. The claimed values in CLAIM.md all match exactly: ED, NED, BCFS and BLEU of the candidate and of FeVeT, the bar 0.30880111347517586, and the margin 0.059678532021.

## 4. The bar, recomputed from fevet/
- `shasum -a 256 -c fevet/expected.sha256`: all 10 pred_0.50_FAM.tsv files OK.
- My converter (fevet_convert.py) builds official-format result files from the COGID, LANGUAGE and PREDICTION columns. It checks each item against solutions-0.50.tsv and the masked cells of test-0.50.tsv:
```
bantubvd             items   816 fevet   816 missing 0 extra 0 gold_mismatch 0 empty_pred 0
beidazihui           items  4921 fevet  4921 missing 0 extra 0 gold_mismatch 0 empty_pred 0
birchallchapacuran   items   683 fevet   683 missing 0 extra 0 gold_mismatch 0 empty_pred 0
bodtkhobwa           items  3426 fevet  3426 missing 0 extra 0 gold_mismatch 0 empty_pred 0
bremerberta          items   366 fevet   366 missing 0 extra 0 gold_mismatch 0 empty_pred 0
deepadungpalaung     items  1450 fevet  1450 missing 0 extra 0 gold_mismatch 0 empty_pred 2
hillburmish          items  1638 fevet  1638 missing 0 extra 0 gold_mismatch 0 empty_pred 0
kesslersignificance  items   353 fevet   353 missing 0 extra 0 gold_mismatch 0 empty_pred 0
luangthongkumkaren   items  1444 fevet  1444 missing 0 extra 0 gold_mismatch 0 empty_pred 0
wangbai              items  3004 fevet  3004 missing 0 extra 0 gold_mismatch 0 empty_pred 0
FEVET_CONVERT OK
```
- The two empty FeVeT predictions are scored as compare_words does (2*len 'Ø'). The bar is 0.30880111347517586 in both modes, equal to the PREREG and CLAIM value.

## 5. Integrity of the saved objects
- `shasum -a 256 -c MANIFEST.sha256`: 379 lines, all OK, rc=0. The package holds 380 files (379 plus the manifest itself). Rerun at the end: 0 failures.
- data/view (the gold-free view) matches the official files: training-0.50 and test-0.50 are byte-identical (cmp) to official/data-surprise for all 10 families.
- object/predictions-0.50.tsv: 18101 items, identical as a mapping to combiner/test/0.50.
- shared/val/0.50, for every family: val train sets and val sets are subsets of the training-0.50 sets; the val sets are disjoint from val train; every val gold cell equals its training-0.50 cell; training-0.50 sets do not overlap test-0.50 sets (overlap 0 for every family). Result: VAL_SPLIT OK.
- Freeze records, own check_freeze.py. It compares every code file and every val/0.50 and test/0.50 result file with FROZEN.md, recomputes the code tree hash and, for this run's entries, the results tree hash. For carried entries it uses the run-0202 record plus the test/0.50 sha256 in CARRIED.md:
```
broker/PRIMARY               frozen 2026-10-18T10:09:21Z  OK   code files 1 match=True code_tree a8f295186339fbdb =record; result files: expected val 10 test 10, present 20, mismatched 0, unlisted 0; results_tree 39ded20f82d73b29 =record
classifier/SECONDARY         frozen 2026-10-18T10:39:38Z  OK   code files 2 match=True code_tree 6cc33b903ae1097c =record; ... mismatched 0; results_tree ce586c78592a07ba =record
broker/SECONDARY             frozen 2026-10-18T10:43:41Z  OK   code files 1 match=True code_tree fc4aee016f3e2159 =record; ... mismatched 0; results_tree a4e9f02634f2c60a =record
r0202-broker/PRIMARY         frozen 2026-10-18T03:14:07Z  OK   code files 1 match=True code_tree e0e12da3febeabfd =record; val 10 + test 10 (CARRIED.md) mismatched 0; results_tree not recomputable here (record lists 70 files of run 0202)
classifier/PRIMARY           frozen 2026-10-18T10:18:47Z  OK   code files 2 match=True code_tree 014f4baa8694bafe =record; ... mismatched 0; results_tree 06a6cbb6ee5f5f88 =record
analogist/PRIMARY            frozen 2026-10-18T09:58:18Z  OK   code files 2 match=True code_tree 94556b993ae1b190 =record; ... mismatched 0; results_tree e5fdcbc3ec1bdc36 =record
phylo/PRIMARY                frozen 2026-10-18T10:07:31Z  OK   code files 1 match=True code_tree 94b531e1fe882c36 =record; ... mismatched 0; results_tree abd67a1da744f210 =record
r0202-analogist/SECONDARY    frozen 2026-10-18T03:23:18Z  OK   code files 2 match=True code_tree 476c111d7f481d91 =record; val 10 + test 10 (CARRIED.md) mismatched 0; results_tree not recomputable here (record lists 70 files of run 0202)
FREEZE_CHECK PASS
```
The code tree hashes in both CARRIED.md files equal the run-0202 records. All freezes are earlier than the PREREG rule 8 deadline of 12:40:00Z.

## 6. Retrain and re-predict every entry (PREREG rule 12 iv)
Setup:
- A fresh run copy outside claim/ holds only tools/ (14 files), data/view/ (40 files: the surprise training-0.50 and test-0.50 files, and the dev families' training-0.10 and test-0.10 files) and attempts/LENS/frozen/ROLE/code (12 files). All 66 sha256 were checked against claim/MANIFEST.sha256 (0 mismatches) and the copy was made read-only.
- No official/, shared/, fevet/, combiner/ or frozen predictions are in the copy.
- Every harness process ran under macOS sandbox-exec with this profile: allow default; deny file-read-data in the whole home tree, /private/tmp and /Volumes; then allow file-read-data only for the SYS venv and the run copy; then deny again any path matching solutions*.tsv/csv/json, cognates*.tsv/csv, wordlist*.tsv/csv, surprise/FAM/(training|test)-0.10..0.40.tsv, or containing "data-surprise".
- Test of the sandbox: reading claim/official/data-surprise/bantubvd/solutions-0.50.tsv and claim/CLAIM.md gave "Operation not permitted". Reading the run copy's training-0.50 and dev files worked, and numpy, scipy, sklearn and lingpy imported.
- Command per entry, run from the run copy: `OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 HOME=(own) SYS -I tools/q15h.py run --code attempts/LENS/frozen/ROLE/code --mode test --out OUT/LENS/ROLE --props 0.50 --workers 1`, with BRK_DEV unset and capped by perl alarm.
- Three entries ran at a time. I used --workers 1 to respect the cap of 3 heavy processes; workers only sets how many families are predicted in parallel, one process each.
- The harness wrote manifests listing only the copy's data/view/surprise/FAM/training-0.50.tsv and data/view/dev.
- Then `cmp` of each of the 10 test/0.50/FAM/result-0.50.tsv files against claim/attempts/LENS/frozen/ROLE/test/0.50/FAM/result-0.50.tsv.

| entry (weight at 0.50) | retrain wall (UTC) | train s | families ok | cmp vs frozen | test-0.50 NED ltr (builtin) | PREREG 12 (iv) case |
|---|---|---|---|---|---|---|
| broker/PRIMARY (1) | 11:47:08-12:08:17 | 343 | 10 | 10 compared, 0 differ: bit-identical | 0.2590010033507703 (0.2590010033507703) | frozen predictions reproduced |
| classifier/SECONDARY (2) | 12:08:17-12:13:44 | 252 | 10 | 10 compared, 0 differ: bit-identical | 0.2722549876396455 (0.2722549876396455) | frozen predictions reproduced |
| broker/SECONDARY (3) | 11:47:08-12:18:22 | 634 | 10 | 10 compared, 0 differ: bit-identical | 0.25678614621567813 (0.25678614621567813) | frozen predictions reproduced |
| r0202-broker/PRIMARY (2) | 11:47:08-11:55:37 | 55 | 10 | 10 compared, 0 differ: bit-identical | 0.260077119099335 (0.260077119099335) | frozen predictions reproduced |
| classifier/PRIMARY (2) | 11:55:37-12:06:49 | 455 | 10 | 10 compared, 0 differ: bit-identical | 0.2832277234193527 (0.2832277234193527) | frozen predictions reproduced |
| analogist/PRIMARY (1) | 12:06:49-12:14:12 | 226 | 10 | 10 compared, 0 differ: bit-identical | 0.2639458361871252 (0.2639458361871252) | frozen predictions reproduced |
| phylo/PRIMARY (0) | 12:18:22-12:20:14 | 3 | 10 | 10 compared, 0 differ: bit-identical | 0.26711162027436225 (0.26711162027436225) | frozen predictions reproduced |
| r0202-analogist/SECONDARY (2) | 12:13:44-12:14:50 | 25 | 10 | 10 compared, 0 differ: bit-identical | 0.27172328707715904 (0.27172328707715904) | frozen predictions reproduced |
| COMBINATION combiner/test/0.50 (own MBR over the 8 re-predicted entries) | n/a | n/a | 10 | 10 compared, 0 differ: bit-identical | 0.24912258145405175 (0.24912258145405175) | reproduced |

All 8 entries are bit-deterministic across independent processes in this retrain. This retrain differed from the frozen runs in machine load (load average 16 to 108), workers (1 instead of 2), HOME, the sealed file view and the random hash seed. No entry needed the rule's non-determinism fallback.

## 7. Stage-2 combination
- Own mbr.py implements the rule from the stage2.py docstring. For each item it outputs argmin over i of sum_j w_j * NED(c_j to c_i), plus 1e-7*(3 - w_i) plus 1e-9*i. NED(a to b) is the scorer's item NED with a as gold, using sigtypst2022's nw_align, with an empty b becoming 2*len(a) 'Ø'. An empty pseudo-gold contributes 0.
- It uses the weights_all10 [1, 2, 3, 2, 2, 1, 0, 2] of combiner/combiner_fit.json, in the entry order of combiner/entries.json. Its own assert checks that these equal the weight_at_0.50 fields.
- Over the frozen entry predictions: `items 18101 weights [1, 2, 3, 2, 2, 1, 0, 2]`, and cmp against combiner/test/0.50 gives "same" for all 10 families.
- Over my re-predicted entry predictions: "own MBR over retrained entries vs combiner/test/0.50: 10 compared, 0 differ".
- "chosen string produced only by weight-0 entries: 20", all phylo/PRIMARY:
  - bantubvd 1396-1, 3664-1, 3756-1, 4688-3
  - beidazihui 1011-10, 60-15, 707-19
  - birchallchapacuran 133-2, 97-9
  - deepadungpalaung 17-14
  - hillburmish 119-2, 125-4, 541-5, 565-9, 646-9, 635-9, 826-9
  - wangbai 3161-2, 2141-2, 4034-5

  This matches CLAIM.md's count and the order of its listed items.
- Weight refit: tools/stage2.py ran under SCO in an isolated copy (tools, shared/val, data/view, the frozen entry val and test files; no surprise gold present), with `--entries combiner/entries.json --val-test-root shared/val --gold-map {"0.50": "shared/val"} --test-root data/view --props 0.50 --procs 1`. Output:
```
stage2: K=8 entries [...]; 65535 weight tuples
0.50 weight search (vectorised): 5.1s, 0 tuple-family pairs recomputed by the exactness guard
0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507
0.50 LOFO val mean (combine.py value) 0.26250736260023105; official compare_words on the written val files: NED 0.26250736260023105
single val NED: broker/PRIMARY 0.271047, classifier/SECONDARY 0.272510, broker/SECONDARY 0.275865, r0202-broker/PRIMARY 0.278080, classifier/PRIMARY 0.278377, analogist/PRIMARY 0.280294, phylo/PRIMARY 0.282760, r0202-analogist/SECONDARY 0.283735
stage2 refit test/0.50: 10 compared, 0 differ
stage2 refit val/0.50: 10 compared, 0 differ
```
  The refitted combiner_fit.json equals the packaged one in every field (weights_all10, lofo_weights, lofo_val_mean, insample_mean_all10, single_entry_val_mean, lofo_val_scorer_*, verify_reference, guard count). The only differences are entry_dirs (paths) and seconds (timings). The val ranking above is ascending and equals the entry order, which is the tie order of rule 9.

## 8. Data access and row isolation
- Reading the code of all 8 system.py files: train reads only `man["surprise_train"][fam]` (the training-0.50 files). The only other data reads are the manifest's dev_dir files: broker learn_univ reads dev_dir/FAM/training-0.10.tsv; classifier devx reads dev_dir/mannburmish and listsamplesize training-0.10.tsv. Both are DEVELOPMENT families, allowed by PREREG rule 4 and disclosed in CLAIM.md.
- No code builds a path to solutions, cognates, wordlist, data-surprise, test-*.tsv or any surprise file of another proportion. predict reads only the model folder and the --jobs partition files.
- Every predict loop builds each output line from that row alone ("fresh per row" scorers/Sim objects; for classifier and phylo, a pure predict_row).
- The sandboxed retrain (section 6) shows the same at the file level. The systems could not read any solutions, cognates or wordlist file, other-proportion surprise file or anything outside the run copy, and they still reproduced every byte.
- Audits: the packaged attempts/LENS/frozen/ROLE/audit_test_0.50.txt each show "identical 40, FAIL 0, mismatches 0, last: AUDIT PASS" (test 0.50) for all 8 entries. I also ran `tools/q15h.py audit --mode test --props 0.50` myself, under the same sandbox, against my retrained outputs. For every entry: "identical 40 FAIL 0 MISMATCH 0 last: AUDIT PASS".
- The rules/sealed_new_0.50.log and rules/sealed_carry_0.50.log files cover all 8 entries: 10 families "bytes IDENTICAL" each, and both logs end "SEALED_CHECK 0.50 PASS".

## 9. Extra: the packaged standalone checker (run after my own checks)
`python3 checker/check_q15.py . object/predictions-0.50.tsv`:
```
1. Mockingbird-I1 mean NED recomputed 0.35176136367373956, official 0.35176136367373956: EXACT
2. FeVeT published predictions mean NED 0.30880111347517586
3. object mean NED 0.24912258145405175 over 18101 items (claimed 0.24912258145405175): EQUAL
   margin vs Mockingbird-I1 0.102638782220 (lower is better)
   margin vs FeVeT 0.059678532021 (lower is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```

## 10. Observations (none changes the result)
- data/view_manifest.sha256 lists 42 files. Two of them, data/view/datasets.json and data/view/datasets-surprise.json, are not in the package ("FAILED open or read"); the other 40 are OK. No entry code or harness path refers to them, and my sandboxed retrain without them reproduced every byte, so they are not inputs of the claim. The package builder may want to drop those two lines or ship the files.
- combiner/combiner_fit.json field entry_dirs holds absolute paths that contain a user name. The publication check of the package may want them scrubbed.
- FeVeT has 2 empty predictions in deepadungpalaung. They are scored as compare_words scores empty cells, and the bar value includes them.
- Not checked here, because the package does not contain the material: whether COMB-8's 8 entries are the 8 lowest-val eligible entries of the whole run (the selection record), and the null test.

## Verdict
- The claimed mean NED 0.24912258145405175 is reproduced exactly by my own scorer, built on the pinned compare_words, in both summation modes.
- The scorer reproduces Mockingbird-I1's official values bit for bit (44 of 44, left to right).
- The bar is recomputed from FeVeT's published files: 0.30880111347517586.
- The candidate beats the bar by 0.05967853202112411 and Mockingbird-I1 by 0.10263878221968781.
- Every one of the 8 entries, weight 0 included, retrained from its frozen code with training-0.50 and dev data only, under a read sandbox. Each re-predicted test-0.50 bit-identically.
- My own MBR implementation rebuilds combiner/test/0.50 byte for byte, both from the frozen and from the retrained entry predictions. The weight refit gives the stored weights.
- No mismatch, missing claim object or non-determinism was found.

pass: true