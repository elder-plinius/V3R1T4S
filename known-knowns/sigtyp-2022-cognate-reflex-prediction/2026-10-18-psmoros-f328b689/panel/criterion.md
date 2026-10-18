(Saved by the main session from the subagent's returned text, 2026-10-18T07:15:51Z: round-2 CRITERION skeptic for cell C10 (Opus 5.5, Agent tool), on the round-2 claim package. The same skeptic re-issued its text at the main session's request with angle-bracket tokens written without brackets, for the kit's placeholder check; the main session verified mechanically that it is identical to the skeptic's first text apart from those tokens. Verbatim below.)

# CRITERION skeptic, cell C10 (proportion 0.10, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: 2026-10-18T06:12:41Z (date -u)
end: 2026-10-18T06:50:10Z (date -u)
material: only the claim package (claim/), plus kit RULES.md. No web requests were made, so the stop list was not touched. Interpreters: SYS (the component venv), SCO (the calibrator venv, used only as an interpreter) and a plain python3.13. All scratch work stayed outside claim/.

## Criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Cell bar (from the task and rules/PREREG.md): this workspace's own earlier confirmed 0.10 system, 0.19710919181751296 (bar_holder/). Also FeVeT 0.2296925777970808 and Mockingbird-I1 0.2431316340782435. No partial win is claimed.

## Checks run (real output)

1. Package integrity (PROVED-HERE). `shasum -a 256 -c MANIFEST.sha256`: 385 lines, no line other than OK. The package holds 385 files besides the manifest, and the file list diff is empty.

2. Scorer identity and calibration (PROVED-HERE). I imported official/src/sigtypst2022.py (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a). This is byte-identical to the module installed in SCO (same sha256). With left-to-right summation, Mockingbird-I1 from official/systems/mockingbird-i1/surprise/*/result-0.10.tsv gives NED 0.2431316340782435. Its "total bit-identical to official: True" and "every family bit-identical: True". Official NED totals at 0.10 for all 10 systems in results-surprise-0.10.json: the lowest is Mockingbird-I1 at 0.2431316340782435 (next: Mockingbird-N1-A 0.2567723485026337). scout/st2022_commits.json shows HEAD 03094435cba4293ce0eea383036cab78499ad50d, 2022-05-27T07:58:23Z, "update for final release". I could not check the commit offline; the bit-exact calibration is the evidence that this is the scorer behind the official JSON.

3. Headline recomputed with my own script (official compare_words per family, statistics.mean over the 10 families) (PROVED-HERE):
- ltr, CANDIDATE combiner/test/0.10: ED 0.73576143576745, NED 0.18916240713560675, BCFS 0.8204529813230585, BLEU 0.7339216116265356
- builtin (compensated summation), CANDIDATE: NED 0.18916240713560675
- ltr, BAR bar_holder/r1806-combiner: NED 0.19710919181751296 (builtin 0.19710919181751294)
- Margin against our own bar: ltr 0.00794678468190621, builtin 0.007946784681906183 (both > 1e-9).
- Margin against Mockingbird-I1's official total: 0.053969226942636755.
- No "Missing entry" warnings appeared in any family.
- Per-family NED (ltr; candidate / bar / MB-I1):

| family | candidate | bar | MB-I1 |
|---|---|---|---|
| bantubvd | 0.179806 | 0.190126 | 0.215172 |
| beidazihui | 0.103610 | 0.118809 | 0.136387 |
| birchallchapacuran | 0.248240 | 0.241971 | 0.295693 |
| bodtkhobwa | 0.098279 | 0.098505 | 0.160100 |
| bremerberta | 0.161518 | 0.174137 | 0.213929 |
| deepadungpalaung | 0.126042 | 0.131198 | 0.216146 |
| hillburmish | 0.230682 | 0.235669 | 0.289540 |
| kesslersignificance | 0.558056 | 0.587669 | 0.669831 |
| luangthongkumkaren | 0.066502 | 0.067982 | 0.091009 |
| wangbai | 0.118889 | 0.125025 | 0.143510 |

All values agree with the CLAIM.md table. All three metrics are reported there; only NED is claimed.

4. FeVeT rescored from fevet/pred_0.10_*.tsv (ltr): NED 0.2296925777970808; missing items 0, gold-column mismatches 0.

5. Data the systems were given (PROVED-HERE).
- data/view/surprise/*/training-0.10.tsv and test-0.10.tsv are byte-identical to official/data-surprise (10 test files identical, 10 training files identical).
- data/view/dev/ holds only training-0.10.tsv and test-0.10.tsv for the 10 development families: no solutions, cognates or wordlist files.

6. Validation split and the sibling-row trap (PROVED-HERE).
- For every family, the organisers' split_training_test_data applied to training-0.10 at ratio 0.15 reproduces shared/val/0.10/FAM/{train,test,solutions}.tsv byte for byte: [True, True, True] in all 10 families.
- Every val set lies inside training-0.10, and val sets overlap test-0.10 sets in 0 cases in every family.
- Trap: "TOTAL masked rows 4029, gold visible verbatim in a sibling row: 4029". Row isolation is therefore essential; see checks 11 to 13.

7. Other proportions (development used training-0.50 and val-0.50) (PROVED-HERE plus inference). In every family, the minimum coverage of test-0.10 sets is at least the maximum coverage of training-0.10 sets, and training-0.10 is in non-increasing coverage order (True x10). This matches the organisers' stable coverage-sorted split in official/src/sigtypst2022.py. From that code it follows that training-P' for P' > 0.10 is a subset of training-0.10. So development on training-0.50 and val-0.50 used no surprise-family information outside training-0.10. The 0.50 files themselves are not in the package. The literal criterion also allows any training-*.tsv.

8. Freeze records (PROVED-HERE). For every stage-2 entry, all code-file and present result-file hashes in attempts/LENS/FROZEN.md match: code ok, bad 0; result files ok 20, bad 0, including test/0.10 10/10. The package code equals the listed code. Freeze times:
- r1806 smuggler 2026-10-17T21:10:10Z and r1806 correspondence 2026-10-17T21:14:15Z (earlier run)
- analogist/SECONDARY 03:23:18Z, broker/PRIMARY 03:14:07Z, phylo/PRIMARY 03:19:07Z, correspondence/PRIMARY 03:40:38Z, classifier/PRIMARY 04:03:30Z

All new freezes fall after PREREG (02:09:41Z) and before selection (04:46:29Z) and the 05:45Z deadline.

9. Pre-registration order (consistent, but times are self-reported in the files):
- rules/PREREG.md frozen 2026-10-18T02:09:41Z; it declares C10 = proportion 0.10, mean NED, and the bar.
- rules/selection.md written 04:46:29Z.
- Sealed check 04:46:45Z to 05:10:00Z.
- Null test 04:49Z.
- Second sealed check (correspondence/PRIMARY) 06:03:17Z to 06:06:05Z.
- sha256(rules/selection.md) = 2d0d43d4901280c8c26b1ae2d3b02e0c8c770873de4e9ee67cbf3dffedd1063c, which is the hash cited in rules/null_test.md.
- The five new lenses' FROZEN.md sha256 values match those listed in selection.md.
- All 10 combiner/test/0.10/*/result-0.10.tsv sha256 values match the "out/comb_all10" hashes in selection.md.
- combiner/combiner_fit.json sha256 c6c55f4b9701ef79b18784c9dd5a94ccdbb01dd8c770f09a89af7108647bea92 matches selection.md.
- The 7 COMB-ALL10 entries are the 7 lowest val-0.10 values in selection.md's table (next lowest: correspondence/SECONDARY 0.2307884591256007).

10. Stage-2 recomputed (PROVED-HERE). I ran tools/stage2.py under SCO on the package's frozen component predictions (val from shared/val, test from data/view). Output: "weights(all 10) [3, 3, 1, 2, 1, 0, 1] in-sample 0.207294 LOFO 0.211310"; LOFO val NED 0.21131035771832854; "empty candidates val 0 test 0".
- Recomputed test/0.10 files: 10/10 byte-identical to combiner/test/0.10. Val files: 10/10 identical.
- weights_all10, insample_mean_all10, lofo_val_mean, lofo_weights, single_entry_val_mean and lofo_val_scorer_total are all equal to combiner/combiner_fit.json.
- Influence trace: every chosen string comes from one of the 7 entries (0 items produced by no entry). Exactly 4 items come only from the weight-0 entry correspondence/PRIMARY: hillburmish 93-3, hillburmish 477-9, kesslersignificance 560-1, kesslersignificance 1222-4. This matches CLAIM.md. Source counts: old+new 3868, r1806-only 77, new-only 84.

11. What each component reads (code audit, HEURISTIC for code, PROVED-HERE for the literal scan).
- Every system.py `train` reads only the manifest's surprise_train files (r1806 smuggler, r1806 correspondence, analogist, broker, classifier, phylo). correspondence/PRIMARY also reads dev_dir.
- `predict` reads only the model dir and the partition files named in --jobs.
- I found no network, subprocess or solutions/results/systems paths.
- A string-literal and config scan of all 14 code files against the 2628 multi-segment test-0.10 gold reflexes found 0 hits.
- Note: correspondence/PRIMARY (weight 0) merges the visible cells of the development families' masked test-0.10 rows into full development cognate sets (dev_full). That uses development families' masked test files only. The literal criterion ("the masked test-*.tsv") and PREREG rule 5 (data/view/dev/) allow this, and it carries no surprise-family information.
- r1806 correspondence sets HOME to a folder of run 1806, used only for the lingpy sound-class cache.

12. Row-isolation evidence in the package. Each of the 7 entries has a harness test-mode audit at 0.10 with 40 checks (3 single rows plus 1 whole partition per family), all "identical", AUDIT PASS. rules/sealed_check_0.10.log covers analogist/SECONDARY, broker/PRIMARY, classifier/PRIMARY and phylo/PRIMARY; rules/sealed2_check_0.10.log covers correspondence/PRIMARY. Both report every family "items identical N/N bytes IDENTICAL" and end "SEALED_CHECK 0.10 PASS". The two r1806 entries' sealed log (from run 1806) is not in this package, so I ran check 13.

13. My own retrain and isolation runs (PROVED-HERE). For each entry I ran tools/q15h.py run in test mode at 0.10. The manifest listed only data/view/surprise/*/training-0.10.tsv plus data/view/dev. HOME was set inside my scratch folder. r1806 correspondence ran from a copy whose only change is line 16 (HOME); corr.py and config.json were identical.
- r1806:smuggler/PRIMARY: train rc=0 133s; 10/10 families byte-identical to frozen. Each of the 99 partitions predicted alone (copied into its own folder, its own fresh process): "TOTAL rows 4029 identical 4029, fresh processes 99".
- r1806:correspondence/PRIMARY (cache warmed first): train rc=0 44s; 10/10 byte-identical. Partitions alone: "TOTAL rows 4029 identical 4029, fresh processes 99".
- analogist/SECONDARY (train 92s), broker/PRIMARY (140s), correspondence/PRIMARY (309s), classifier/PRIMARY (500s), phylo/PRIMARY (12s): each 10/10 families byte-identical to frozen. These runs were not sandboxed; the main session's sealed logs cover these five.

Retraining reproduces every component, and stage 2 reproduces the object (check 10). So the claimed object follows from training-0.10, the development view and row-isolated test rows alone.

14. Each component alone on test-0.10 (ltr NED):

| entry | weight | NED |
|---|---|---|
| r1806 smuggler | 3 | 0.2065798750856504 |
| r1806 correspondence | 3 | 0.20065194617897522 |
| analogist/SECONDARY | 1 | 0.20460403212077688 |
| classifier/PRIMARY | 2 | 0.2061706513594121 |
| broker/PRIMARY | 1 | 0.19836914089048766 |
| correspondence/PRIMARY | 0 | 0.20546744883430543 |
| phylo/PRIMARY | 1 | 0.20809801282747903 |

No single component beats the bar 0.19710919181751296. The gain belongs to the new stage-2 object.

15. Null test, my own implementation (cognate-set paired swaps against bar_holder/, official per-item NED, linear aggregation weights):
- Real: candidate 0.18916240713560645, bar 0.19710919181751255, d 0.0079467846819061.
- Pre-registered seeds (20261018+c, 400 controls): max 0.005948936672339158, controls >= real: 0. rules/null_test.md reports max 0.005948936672339172, real 0.00794678468190621; the values agree to float rounding.
- Extra 20000 controls (seed 777): max 0.00815518976333519, 1 control >= real, one-sided p ~ 0.00010.
- Items: 4029. Candidate string differs from the bar's on 428; candidate better on 219, worse on 126.
- Share of d by family: kesslersignificance +0.002961, beidazihui +0.001520, bremerberta +0.001262, bantubvd +0.001032, wangbai +0.000614, deepadungpalaung +0.000516, hillburmish +0.000499, luangthongkumkaren +0.000148, bodtkhobwa +0.000023, birchallchapacuran -0.000627. Positive in 9 of 10 families.

16. One cell, one metric, one object. CLAIM.md claims only C10 (proportion 0.10), only mean NED, and only the object combiner/test/0.10. BCFS, BLEU and ED are reported and not claimed. The aggregate over five proportions is not claimed. The candidate is COMB-ALL10, not run 1806's combiner or one of its components (PREREG rule 10).

## Judgement
- Literal criterion:
  - Every component trained only on training-0.10 (plus the development families' training-0.10 and masked test-0.10 files). Each masked test row was predicted alone.
  - No solutions-*.tsv file was read by any component or by stage 2. Stage-2 weights and selection used shared/val/0.10, which I showed is the organisers' split of training-0.10 and is disjoint from test-0.10.
  - The proportion and metric were declared in PREREG.md before selection and scoring.
  - The pinned scorer, calibrated bit for bit on Mockingbird-I1, gives mean NED 0.18916240713560675. This is strictly below Mockingbird-I1's official 0.2431316340782435 on the same metric.
- Cell condition: it is also strictly below this workspace's earlier confirmed 0.10 system, 0.19710919181751296, by 0.00794678468190621 (ltr) and 0.007946784681906183 (builtin). The pre-registered null passes (0 of 400 controls, about 1 in 20000 extra).
- Not subsumed: it is a different object with different predictions on 428 items. It is better in 9 of 10 families, and no component alone (including the two reused run-1806 components) reaches the bar. So this is a genuine improvement over the earlier claim, not a restatement of it.

Residual limits (none change the verdict):
- (a) Run 1806's sealed log for its two entries is not in the package. I replaced it with an unsandboxed retrain, per-partition fresh-process prediction and a code audit (checks 11 and 13).
- (b) The val values of COMB-NEW (0.21766634729481002) and run 1806's combiner (0.21358978758026678) used in the selection cannot be recomputed from this package. The selected candidate's own val value is reproduced exactly.
- (c) PREREG and selection times are self-reported. They agree with the freeze records and the cross-cited hashes.
- (d) HEURISTIC: the PREREG was written knowing run 1806's test-0.10 results. COMB-ALL10 is a mechanical rule (lowest val-0.10, weights fit on val) and the null test passes, so I see no sign that the protocol was tuned on test.

confirmed_scope: At proportion 0.10, the frozen stage-2 minimum-Bayes-risk combination combiner/test/0.10 (seven frozen components trained only on the 10 surprise families' training-0.10 files and the development view, each masked test-0.10 row predicted in isolation, integer weights fit on validation splits cut from training-0.10) scores mean NED 0.18916240713560675 over the 10 surprise families under the pinned ST2022 scorer (left-to-right summation; the same value with compensated summation), strictly lower than this workspace's earlier confirmed 0.10 system (0.19710919181751296, bar_holder/), FeVeT's published predictions (0.2296925777970808) and Mockingbird-I1's official results-surprise-0.10.json value (0.2431316340782435), as a win on mean NED only.

pass: true
