(Saved by the main session at 2026-10-18T12:37:59Z from the criterion skeptic subagent's returned text (cell B50; Opus 5.5, agent a82aba82daf2bfcdb); the subagent could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic, cell B50 (proportion 0.50, mean BCFS), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics; I saw only the claim package, the kit rules and the trophy case)
start: Sun Oct 18 11:44:26 UTC 2026 (date -u)
end: Sun Oct 18 12:18:29 UTC 2026 (date -u)
material: claim/ only, plus kit/RULES.md and TROPHY_CASE.md (the trophy case has no entry for this private quarry). I made no network requests, so I added nothing to the stop list. injection_suspected: none.
interpreters: SYS (the entries' ML venv), SCO (the pinned-scorer venv, used only as an interpreter) and PY3 (a stock Python 3.13, standard library only). My own scripts are kept outside the package (myscore.py, valsplit.py, freezecheck.py, selhash.py, mynull.py, devoverlap.py, fixedw.py, scoredir.py). Labels: every number below is NUMERICAL, copied from command output; the conclusions are PROVED-HERE for the checks I ran.

## The criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Cell claimed: B50, proportion 0.50, mean BCFS, higher is better. The criterion's bar is Mockingbird-I1 at 0.6050308536957327. The cell's stricter bar is FeVeT's published predictions rescored, 0.6423935720824072. The object is combiner/test/0.50; object/predictions-0.50.tsv holds the same predictions.

## Clause-by-clause judgement

1. "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)": MET.
   - What each entry can read: the harness manifest (tools/q15h.py run) lists only data/view/surprise/FAM/training-0.50.tsv and dev_dir = data/view/dev. data/view contains only:
     - training-0.50.tsv and test-0.50.tsv of the 10 surprise families, byte-identical to official/data-surprise (C3);
     - training-0.10.tsv and test-0.10.tsv (masked) of the 10 development families.
     No solutions file of any family is in the view. No other proportion of a surprise family is in it.
   - The sealed check (rules/sealed_*.log) retrained every one of the 8 COMB-8 entries under the strict sandbox profile and predicted each test-0.50 partition in its own process. All 8 gave 18101 of 18101 items byte-identical to the frozen predictions; both logs end "SEALED_CHECK 0.50 PASS" (C11). So the frozen predictions are a function of training-0.50, the development view and one partition at a time. All 8 entries' test-mode audits end "AUDIT PASS" (C10).
   - Row isolation matters: all 18101 masked answers appear verbatim in a sibling row of the same test-0.50 file (C13). Partitions by masked language keep that cell masked in every row of a partition. The stage-2 choice uses only one item's 8 candidate strings (tools/stage2.py, reproduced in C7).
   - Stage-2 weights: they are fit on shared/val/0.50. I rebuilt that split from training-0.50 with the official split_training_test_data (ratio 0.15) and got byte-identical train, test and solutions files. Its cognate sets lie inside training-0.50, and training-0.50 is disjoint from the test-0.50 sets (C4). The val "solutions.tsv" is therefore derived only from training-0.50. Rerunning stage 2 reproduced weights [1, 2, 3, 2, 2, 1, 0, 2], LOFO 0.26250736260023105, and all 10 test files byte-identical (C7).
   - Selection and freezes: this run's entries froze between 09:58:18Z and 10:43:41Z. The two carried entries froze in run 0202 (03:14:07Z and 03:23:18Z) under val-0.50-only rules, and their test-0.50 runs were made in this run. All code and result hashes equal the freeze records (C8). selection.md (11:25:56Z, written before any gold was read) records sha256 values for those files and for out/comb8. All 180 file hashes and all 6 freeze-record hashes equal the package files (C9). The candidate was picked mechanically by val-0.50 NED, the same pick for all three cells, so no metric-specific choice was made.
   - Development-family disclosure. The classifier entries add mannburmish rows to hillburmish and listsamplesize rows to kesslersignificance. I judge this within both the letter and the spirit of the criterion:
     - Letter: the criterion restricts file kinds, not families. The development families' training-0.10.tsv and masked test-0.10.tsv are training-*.tsv and masked test-*.tsv files of the same ST2022 release (data/). No solutions-*.tsv of any family was readable.
     - Spirit: the definition's verification_method and pitfalls aim to exclude the public surprise gold ("NED=0 is trivially reachable by copying solutions"). These rows are not that gold. They are independent wordlists, with different sources, transcriptions and COGIDs, and they carry no glosses. The organisers released them as the data "users should use to test and design their models", and say the surprise sets were selected "similar to the data in the training set, with respect to the language families in question" (scout/st2022_repo_page.html). Mockingbird-I1 and every 2022 participant had the same data. Broker uses the development families only for a generic sound-substitution prior.
     - Measured effect: the gold appears verbatim (tones dropped) among the development-derived strings for only 133 of 960 mapped hillburmish items and 28 of 229 mapped kesslersignificance items (C15). I retrained both classifier entries with devx removed and refit stage 2 on val. Mean BCFS was 0.7113312125593774 against the claimed 0.7114179305724276, a difference of 0.0000867 (C16). So the win does not rest on these rows.
     - Caveat: PREREG rule 4 forbids "external lexical data". Same-language rows from another dataset in the release come closest to that, but rule 4 explicitly permits data/view/dev, and the effect is negligible either way.

2. "mean score over the 10 surprise families at a declared proportion ... stated in PREREG.md": MET.
   - rules/PREREG.md states "Declared proportion: 0.50 only" and fixes cell B50 with both bars. Its text records "Frozen at 2026-10-18T08:49:14Z". That is before the first sealed run (09:01:46Z), the freezes (09:58Z onward), selection.md (11:25:56Z) and the null test (11:27Z).
   - The value is the mean over the 10 families of compare_words' family BCFS, as compare_systems computes it. All 10 families were scored with 0 missing entries (C5).
   - Limit: these times come from file text; the file mtimes in the package are copy times.

3. "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric": MET.
   - BCFS 0.7114179305724276 against Mockingbird-I1's 0.6050308536957327 (the JSON value, reproduced exactly): margin 0.10638707687669491.
   - Against the stricter FeVeT bar 0.6423935720824072: margin 0.06902435849002042.
   - The best official 0.50 BCFS of any 2022 system is CrossLingference-Julia's 0.6193241007226449, also beaten.
   - The candidate beats FeVeT and Mockingbird-I1 on BCFS in 10 of 10 families. The smallest margin over FeVeT is 0.040788 (bantubvd).

4. "Report all three": MET. CLAIM.md reports ED, NED, BCFS and BLEU for the candidate, FeVeT and Mockingbird-I1. My recomputation gives the same candidate values (NED 0.24912258145405175, BLEU 0.6520222200978466). This folder claims BCFS only, as "a win on one metric is a win on that metric only" requires.

5. "The repo scorer st2022 at a pinned commit computes the score": MET.
   - The SCO module sigtypst2022.py has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, the same as official/src/sigtypst2022.py.
   - The pin is 03094435cba4293ce0eea383036cab78499ad50d, which scout/st2022_commits.json shows as HEAD.
   - Calibration: with left-to-right summation, Mockingbird-I1's 10 family values and its total equal results-surprise-0.50.json exactly.

6. Null test (rules/null_test.md, PREREG rule 13): PASSES. It was rerun with the package tool and with my own version built on the official primitives, with identical draws. Real d is 0.0690; the best of 400 controls is 0.01006; 0 controls reach real (C14).

7. One cell, one metric, one object: MET. This folder claims B50 only. The same object appears in sibling cells N50 and L50 on other metrics; each of those is a separate one-metric claim. The claim is not subsumed by any of them, nor by the 0.10-0.30 cells, which are different proportions.

Residual notes (not blocking):
- (a) That the development view is byte-identical to the pinned clone rests on the package's record (scout.md, data/view_manifest.sha256). I could not read the clone.
- (b) Earlier main sessions saw test scores at 0.10-0.30, whose gold overlaps test-0.50. This run's candidate was chosen mechanically on val. That lenses never saw test scores is documented but cannot be verified from the package. The margin, 0.069 against a null maximum of 0.010, leaves no room for this to matter.

## Checks run (real output)

C1 package integrity: "shasum -a 256 -c MANIFEST.sha256": 379 of 379 OK; 379 files besides the manifest.

C2 scorer identity (SCO, Python 3.13.2):
"module sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a / official/src sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a / lingpy 2.6.9 lingrex 1.2.0".

C3 data view: for all 10 families, training and test-0.50 in data/view/surprise compare SAME (cmp) with official/data-surprise. Files in the view: 10 test-0.10.tsv, 10 test-0.50.tsv, 10 training-0.10.tsv, 10 training-0.50.tsv (the 0.10 files are development families only). No solutions file is present.

C4 val split rebuilt with the official split function: every family "rebuilt==shared(train,test,solutions) [True, True, True] ... val subset of training-0.50 True  training-0.50 sets disjoint from test-0.50 sets True"; "VALSPLIT PASS".

C5 own official scoring (myscore.py, SCO, both summation modes):
- ltr: "Mockingbird-I1 recomputed total [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888] family values == JSON: True total == JSON: True".
- ltr: "candidate total [ED,NED,BCFS,BLEU] ['1.0166617451971307', '0.24912258145405175', '0.7114179305724276', '0.6520222200978466']".
- ltr: "FeVeT total ['1.286021835157271', '0.30880111347517586', '0.6423935720824072', '0.5768215755932388']".
- ltr: "BCFS cand - FeVeT = 0.06902435849002042 ; cand - Mockingbird(JSON) = 0.10638707687669491".
- builtin mode: candidate BCFS 0.7114179305724276, FeVeT 0.6423935720824072 (same).
- Per-family BCFS (candidate / FeVeT / Mockingbird-I1):

| family | candidate | FeVeT | Mockingbird-I1 |
|---|---|---|---|
| bantubvd | 0.736765 | 0.695978 | 0.605223 |
| beidazihui | 0.849633 | 0.802986 | 0.803904 |
| birchallchapacuran | 0.617283 | 0.499038 | 0.439851 |
| bodtkhobwa | 0.805630 | 0.754436 | 0.702295 |
| bremerberta | 0.672607 | 0.571330 | 0.620276 |
| deepadungpalaung | 0.788406 | 0.704891 | 0.602416 |
| hillburmish | 0.637283 | 0.576844 | 0.513843 |
| kesslersignificance | 0.402951 | 0.345583 | 0.303937 |
| luangthongkumkaren | 0.868615 | 0.791823 | 0.800249 |
| wangbai | 0.735007 | 0.681028 | 0.658315 |

- 0 missing entries in every family.
- FeVeT files: fevet/expected.sha256 gives "OK" for all 10 pred_0.50 files. My own conversion found rows equal to gold items in every family (total 18101), 0 missing, 0 GOLD-column mismatches, 0 duplicates.
- object/predictions-0.50.tsv equals combiner/test/0.50: 0 differences and 0 extra rows in every family.

C6 standalone checker ("python3 checker/check_q15.py . object/predictions-0.50.tsv", PY3):
"1. Mockingbird-I1 mean BCFS recomputed 0.6050308536957327, official 0.6050308536957327: EXACT / 2. FeVeT published predictions mean BCFS 0.6423935720824072 / 3. object mean BCFS 0.7114179305724276 over 18101 items (claimed 0.7114179305724276): EQUAL / margin vs Mockingbird-I1 0.106387076877 / margin vs FeVeT 0.069024358490 / 4. rebuilt official-format files equal to the frozen ones: 10 of 10 / PASS".

C7 stage-2 rerun (tools/stage2.py, SCO, entries from combiner/entries.json in that order):
- "0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507"
- "LOFO val mean (combine.py value) 0.26250736260023105"
- "empty candidates val 0 test 0"
- "0 tuple-family pairs recomputed by the exactness guard"
- cmp: "test FAM identical" for all 10 families; no val differences.

C8 freeze hashes (freezecheck.py, PY3): every entry has 0 mismatches, 0 uncovered result files and "code_tree recomputed==record True"; "FREEZECHECK PASS".

| entry | frozen | result files checked | carried test lines |
|---|---|---|---|
| broker/PRIMARY | 2026-10-18T10:09:21Z | 20 | - |
| classifier/SECONDARY | 10:39:38Z | 20 | - |
| broker/SECONDARY | 10:43:41Z | 20 | - |
| r0202-broker/PRIMARY | 03:14:07Z | 10 | 10 |
| classifier/PRIMARY | 10:18:47Z | 20 | - |
| analogist/PRIMARY | 09:58:18Z | 20 | - |
| phylo/PRIMARY | 10:07:31Z | 20 | - |
| r0202-analogist/SECONDARY | 03:23:18Z | 10 | 10 |

C9 selection.md hashes against the package: "180 equal, 0 mismatched"; "SELHASH PASS". The freeze records broker, classifier, analogist, phylo, r0202-broker and r0202-analogist hash to ee19d511..., fdc52d8b..., a6bb14c4..., e6588445..., d41dd287... and c8b4cf2c...; all equal the selection.md lines.

C10 test-mode audits at 0.50: all 8 entries end "AUDIT PASS", with 40 identical lines and 0 FAIL lines each.

C11 sealed logs: rules/sealed_new_0.50.log starts at 11:22:47Z with strict profiles. The new entries analogist/PRIMARY, broker/PRIMARY, broker/SECONDARY, classifier/PRIMARY, classifier/SECONDARY and phylo/PRIMARY each give "train ok families 10 items identical 18101/18101 all bytes IDENTICAL True". rules/sealed_carry_0.50.log starts at 09:01:46Z; carry broker-PRIMARY and analogist-SECONDARY give the same. Both logs end "SEALED_CHECK 0.50 PASS". There are no FAIL, MISMATCH, error or denied lines.

C12 code audit (grep for open, listdir, glob and file-name patterns in the 8 system.py files):
- Every entry reads only the manifest's surprise_train files, its own model folder and the jobs/partition files.
- broker/PRIMARY and broker/SECONDARY also read dev_dir/FAM/training-0.10.tsv for a universal substitution prior (learn_univ).
- classifier/PRIMARY and classifier/SECONDARY read dev_dir mannburmish and listsamplesize training-0.10.tsv (devx, config.json).
- None mentions solutions, cognates or wordlist files, or any absolute data path. phylo uses lingpy's built-in sound classes.

C13 row-isolation need: "items 18101 gold visible verbatim in a sibling row of the same test file: 18101". Every test row has exactly one masked cell (asserted).

C14 null tests:
- Package tool (fevet_to_harness.py, then null_test_metric.py, PY3): "TOTAL test rows 18101 filled 18101 missing 0 extra 0 language-mismatch 0"; "real: candidate bcfs 0.7114179305724277, bar 0.6423935720824072, d = 0.06902435849002053 / controls: 400 / best_control: 0.010059480747746763 / real_beats_all_controls: yes / controls >= real: 0".
- Own version (mynull.py, SCO, official nw_align and bcubed_score, statistics.mean): "'real_d': 0.06902435849002042, 'controls': 400, 'best_control': 0.010059480747746874, 'controls_ge_real': 0, 'real_beats_all_controls': True".
- Own version against Mockingbird-I1's predictions: "'real_d': 0.10638707687669491, 'best_control': 0.012969135184381697, 'controls_ge_real': 0".

C15 development-row overlap (devoverlap.py, SYS, the classifier's own load_train):
- hillburmish: "472 dev rows used"; items_mapped 960, gold_in_dev_strings 133. Exact matches: candidate 377 against FeVeT 291, of which 68 and 57 have the gold in the development strings. Chosen strings produced only by the classifier entries: 66 in all, 3 exact.
- kesslersignificance: "238 dev rows used"; items_mapped 229, gold_in_dev_strings 28. Exact matches: candidate 19 against FeVeT 11, of which 3 and 1 have the gold in the development strings. Chosen strings produced only by the classifier entries: 6, 0 exact.

C16 counterfactual without development rows (my copies of the two classifier code folders with "devx" removed from config.json; tools/q15h.py run in val and test mode at 0.50 with SYS; then stage 2 refit):
- Outside hillburmish and kesslersignificance, every val and test file of both entries is byte-identical to the frozen file (8 of 10 families "same").
- Refit: "weights(all 10) [1, 1, 3, 2, 3, 1, 0, 2] ... LOFO 0.263500".
- Official mean BCFS: devx_off_refit 0.7113312125593774 and devx_off_fixed_weights 0.711216980006625, against claimed_object 0.7114179305724276.
- Single entries: classifierPRIMARY 0.6778710220295727 frozen against 0.6757023609607108 without devx; classifierSECONDARY 0.6857705765369353 against 0.6829680896011234.

C17 sensitivity bound: setting the candidate's hillburmish and kesslersignificance BCFS to FeVeT's family values gives a mean of 0.6996372852656774; setting them to Mockingbird-I1's gives 0.6891725680013983. Both are still above both bars.

C18 weight-0 entries: "items 18101 chosen string produced only by weight-0 entries: 20", as CLAIM.md states (first items bantubvd 1396-1, 3664-1, 3756-1, 4688-3, beidazihui 1011-10).

## Verdict
The result meets the full success criterion for cell B50 as literally written: declared proportion 0.50, mean BCFS, against Mockingbird-I1's official score, using the pinned scorer. It also clears the cell's stricter FeVeT bar and passes the pre-registered null test. The use of development-family rows is within the criterion's letter and spirit, and contributes about 0.00009 of mean BCFS. I found no hidden quantifier or stretched definition that fails.

confirmed_scope: At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (the same predictions as object/predictions-0.50.tsv) of 8 entries, which read only the 10 surprise families' training-0.50.tsv, the masked test-0.50.tsv one masked-language partition at a time, and the task release's development-family training-0.10.tsv and masked test-0.10.tsv files (no solutions file of any family), scores mean B-Cubed F-score 0.7114179305724276 over the 10 SIGTYP 2022 surprise families under the pinned ST2022 scorer (commit 03094435, the same value under left-to-right and builtin summation), strictly above Mockingbird-I1's official 0.6050308536957327 in results-surprise-0.50.json and above the cell's stricter bar, FeVeT's published predictions rescored at 0.6423935720824072; this is a win on mean BCFS at 0.50 only.

pass: true