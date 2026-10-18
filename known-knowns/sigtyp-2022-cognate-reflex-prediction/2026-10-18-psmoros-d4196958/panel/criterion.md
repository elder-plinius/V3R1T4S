(Saved by the main session at 2026-10-18T13:18:27Z from the criterion skeptic subagent's returned text (cell L30; Opus 5.5, agent aa729bcbb53e51c42); the subagent could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic, cell L30 (proportion 0.30, mean BLEU), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics; fresh context; my only material was the claim package claim/, the kit rules and the trophy case)
start: Sun Oct 18 12:53:12 UTC 2026 (date -u)
end: Sun Oct 18 13:16:44 UTC 2026 (date -u)
network: none. I made no web requests, and I added no line to the session stop list.
TROPHY_CASE.md: grep for sigtyp|st2022|Q15|cognate|reflex|quarry-B|BLEU|mockingbird found no matching entry.
Interpreters (as named in claim/REPRODUCE.md): SYS (the entries' ML venv), SCO (the interpreter with the pinned scorer module) and a stock Python 3.13. My scratch scripts are outside claim/: myscore.py, mynull.py, valcheck.py, frozencheck.py, rowalone.py, robust.py.

## Criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

The claim is for the full criterion: one cell (P 0.30), one metric (mean BLEU), one object (combiner/test/0.30). It does not use a partial win (p1-p3).

## Checks run, with real output

### C1. Package integrity (PROVED-HERE)
- shasum -a 256 -c MANIFEST.sha256 gives "lines: 364 ok: 364", "files present: 364", and no files outside the manifest.
- Hashes in rules/bleu_freeze.md (L30, out/bleu_new/test/0.30/FAM) against combiner/test/0.30/FAM/result-0.30.tsv: all 10 OK.
- sha256 of rules/PREREG.v2.md is b6429d194444dedd7eea3fd5b4a81708306c0b4dea9b57f6b39bbacbe7a1ea20, and sha256 of tools/stage2_bleu.py is 3e08ea61c13ebc4ccee6ddfef52f3205a283a5ac2fb851885896faad31a18f00. Both equal the values recorded in rules/bleu_freeze.md.
- The bar files bar_comb_new/test/0.30 match the hashes in rules/selection.md: 10 of 10 OK.
- frozencheck.py takes the last freeze record of each entry's ROLE in attempts/LENS/FROZEN.md:
  - broker/PRIMARY 2026-10-18T03:14:07Z, analogist/SECONDARY 03:23:18Z, broker/SECONDARY 04:00:49Z, phylo/PRIMARY 03:19:07Z, analogist/PRIMARY 02:43:13Z, classifier/PRIMARY 04:03:30Z.
  - For each entry: all code files and all 20 val/test 0.30 result files match ("mismatches 0"), and there are no unrecorded code files. Result: "FROZEN_CHECK PASS".
- Minor discrepancy: combiner/combiner_fit.json has sha256 6bcc7fc68e4f53e1bd08aea7c48b1ec6b124f9023b5fccb935b42a4dda4e46eb. That is not the value bleu_freeze.md records for out/bleu_new/combiner_fit.json (5261847a...). The package copy holds only the "0.30" key and no "seconds" field, so it is an excerpt. Its weights and top-20 list equal my rebuild (C4) exactly. Not material, but the package should say it is an excerpt.

### C2. Headline recomputed with the official scorer (PROVED-HERE)
- Scorer used: claim/official/src/sigtypst2022.py, imported in SCO. Its sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a equals SCO's installed module. Environment: lingpy 2.6.9, lingrex 1.2.0, Python 3.13.2.
- Method: compare_words(solutions-0.30, result-0.30)[-1][1:] for each family, then statistics.mean over the 10 families. "ltr" means builtin sum replaced by a left-to-right loop in the sigtypst2022 and lingrex.util namespaces; "builtin" is Python 3.13's compensated sum.

| system | mode | ED | NED | BCFS | BLEU |
|---|---|---|---|---|---|
| mock | ltr | 1.1762187506031638 | 0.2898984929868421 | 0.6717099225519634 | 0.6058548112827981 |
| mock | builtin | 1.1762187506031638 | 0.2898984929868421 | 0.6717099225519634 | 0.6058548112827982 |
| cand | ltr | 0.8901395410281422 | 0.22149461586532132 | 0.7502543049557795 | 0.6874377388475998 |
| cand | builtin | 0.8901395410281423 | 0.22149461586532132 | 0.7502543049557795 | 0.6874377388475998 |
| bar | ltr | 0.9027034122955315 | 0.22327922550091464 | 0.7488264857956657 | 0.6839233380559118 |
| bar | builtin | 0.9027034122955314 | 0.22327922550091467 | 0.7488264857956657 | 0.6839233380559119 |
| fevet | ltr | 1.0946456488227652 | 0.2632988364952282 | 0.6986581179861967 | 0.6356571184958077 |
| fevet | builtin | 1.094645648822765 | 0.2632988364952282 | 0.6986581179861968 | 0.6356571184958079 |

- Calibration: official Mockingbird-I1 total in results-surprise-0.30.json is [1.1762187506031638, 0.2898984929868421, 0.6717099225519634, 0.6058548112827981]. The ltr recomputation is equal, and the per-family values are equal for all 10 families.
- Margins:
  - ltr: cand-bar 0.003514400791688077, cand-mock 0.08158292756480179, cand-fevet 0.051780620351792095, margin>1e-9 True.
  - builtin: cand-bar 0.003514400791687966, cand-mock 0.08158292756480168, cand-fevet 0.051780620351791984, margin>1e-9 True.
- Per-family BLEU, candidate vs bar (ltr): the candidate is higher in 9 of 10 families.

| family | diff |
|---|---|
| bantubvd | +0.001106 |
| beidazihui | +0.001215 |
| birchallchapacuran | +0.006393 |
| bodtkhobwa | +0.001272 |
| bremerberta | +0.001517 |
| deepadungpalaung | -0.000395 |
| hillburmish | +0.004895 |
| kesslersignificance | +0.014738 |
| luangthongkumkaren | +0.000216 |
| wangbai | +0.004187 |

- Standalone checker (python3 -I checker/check_q15.py . object/predictions-0.30.tsv):
  - "1. Mockingbird-I1 mean BLEU recomputed 0.6058548112827981, official 0.6058548112827981: EXACT"
  - "object mean BLEU 0.6874377388475998 over 11586 items (claimed 0.6874377388475998): EQUAL"
  - "margin vs bar_comb_new/predictions-0.30.tsv 0.003514400792"
  - "rebuilt official-format files equal to the frozen ones: 10 of 10"
  - last line "PASS", exit 0.

### C3. Other known objects at 0.30 (non-subsumption within the package; NUMERICAL)
- The six entries' frozen test-0.30 predictions, official mean BLEU (ltr):
  - broker/PRIMARY 0.6773572720481368
  - analogist/SECONDARY 0.674666799591828
  - broker/SECONDARY 0.6698786005734902
  - phylo/PRIMARY 0.6596514642479974
  - analogist/PRIMARY 0.6583352796054924
  - classifier/PRIMARY 0.6591573147847148
- All six are below the bar (0.6839233380559118) and below the candidate.
- Highest BLEU in official results-surprise-0.30.json: Mockingbird-I1 0.6058548112827981.
- Limit: the run's other five frozen entries (correspondence x2, transducer x2, classifier/SECONDARY) and other runs' objects are not in the package. Completeness of the bar list rests on PREREG.v2's statement (NOVELTY's area).

### C4. The object is exactly the pre-registered rule applied to the frozen entries, with no test gold (PROVED-HERE)
- Command: STUB_MPL=1 SCO -I tools/stage2_bleu.py --entries combiner/entries.json --props 0.30 --val-test-root shared/val --gold-root shared/val --test-root data/view --out (scratch).
- Output: "0.30 weights [2, 2, 1, 3, 1, 3] val mean BLEU (in-sample) np.float64(0.6601872015990811); runner-up [2, 3, 1, 3, 0, 2] np.float64(0.6601218715690348)".
- Comparison: "test identical: 10 of 10", "val identical: 10 of 10". Weights and top-20 list equal combiner/combiner_fit.json (top20 equal True).
- Code reading of tools/stage2_bleu.py:
  - The test file is read only for its keys and the masked language.
  - Weights are fit only on shared/val/0.30 gold.
  - The per-item rule matches PREREG.v2's text.
- Independent re-implementation of the MBR choice (robust.py, rank-1 weights) gives test 0.6874377388.

### C5. Validation split and data views come from training-0.30 only (PROVED-HERE)
- valcheck.py rebuilds shared/val/0.30 from data/view/surprise/FAM/training-0.30.tsv with the harness's copy of the organisers' split rule (ratio 0.15):
  - "val rebuild identical files: 30 of 30"
  - "training-0.30 sets that are test-0.30 sets: 0; val-0.30 sets that are test-0.30 sets: 0"
- data/view/surprise/FAM training-0.30 and test-0.30 equal official/data-surprise/FAM byte for byte: "identical view vs official: 20 of 20".
- Every test row has exactly one "?" cell: "test rows 11586 rows without exactly one ? cell 0".
- data/view/dev holds only training-0.10.tsv and test-0.10.tsv for the 10 development families. There is no solutions file anywhere in data/.
- Hidden quantifier: "masked answers of test-0.30 visible verbatim in a sibling row: 11586 of 11586". Every answer can be copied from the same file, so row isolation is decisive (C6).

### C6. What each entry reads, and row isolation (PROVED-HERE for my retrains and probes; the sealed logs are package evidence)
- Code reading: each frozen code folder holds only system.py (plus a small config.json for analogist x2 and classifier/PRIMARY).
  - train() reads only man["surprise_train"][fam], which the harness sets to training-0.30. No entry uses dev_dir.
  - predict() reads only the model folder and the partition files in --jobs.
  - No reads of solutions, other proportions, network or absolute paths were found.
- Harness (tools/q15h.py run):
  - The manifest lists only the 10 training-0.30 files and the dev view.
  - The model folder is made read-only after training.
  - Test files are split into partitions by masked language, with an assert that no partition holds two rows of one cognate set. A row's gold appears only in sibling rows, which sit in other partitions.
- My retrain of ALL SIX entries with the harness (test mode, 0.30, fresh output folders in my scratch; phylo and classifier from byte copies of their code):
  - broker/PRIMARY, broker/SECONDARY, analogist/PRIMARY, analogist/SECONDARY, phylo/PRIMARY, classifier/PRIMARY: each "retrained test-0.30 byte-identical: 10 of 10".
  - These are unsandboxed harness runs. The manifest each one wrote lists only data/view/surprise/FAM/training-0.30.tsv and the dev dir.
- My row-alone probe (rowalone.py): every one of the 252 masked rows of kesslersignificance, the family contributing most of the gain, was predicted alone in its own fresh process with my retrained model and compared to the frozen merged prediction.
  - "ROWALONE analogist/PRIMARY kesslersignificance rows 252 identical 252 mismatches 0"
  - The same line, "rows 252 identical 252 mismatches 0", for analogist/SECONDARY, broker/PRIMARY, broker/SECONDARY, classifier/PRIMARY and phylo/PRIMARY.
- Sealed-check logs in the package:
  - rules/sealed_check_0.30.log: 4 components (analogist/SECONDARY, phylo/PRIMARY, broker/PRIMARY, classifier/PRIMARY). Sandboxed strict-profile training. 99 sealed partition processes each, every family "bytes IDENTICAL". Ends "SEALED_CHECK 0.30 PASS".
  - rules/sealed2_check_0.30.log: the two entries with zero weight in COMB-NEW but non-zero weight here (analogist/PRIMARY, broker/SECONDARY). Every family "bytes IDENTICAL". Ends "SEALED_CHECK 0.30 PASS".
  - Together they cover all six non-zero-weight entries.
- Test-mode audits in each frozen ROLE folder (audit_test*.txt): 40 audit lines at 0.30 and 120 "identical" overall in each. All six end "AUDIT PASS".
- Other proportions: the entries' code was developed on val-0.50 cut from training-0.50 (PREREG.md rule 7; self-attested).
  - In the organisers' split, test-P is a prefix of one fixed ranking of cognate sets by reflex count. So test-0.30 is inside test-0.50, and training-0.50 is inside training-0.30. That development data contains no test-0.30 set.
  - Training-0.50 is also a training-*.tsv file, which the literal criterion allows.
  - Nothing at test time uses any other proportion.
- Generic lingpy sound-class tables (phylo) are library models, not lexical training data. The organisers' own baseline uses the same library.

### C7. Declaration and timing (self-attested; internally consistent)
- rules/PREREG.v2.md: "Frozen at 2026-10-18T07:19:21Z ... BEFORE the objects below exist". Cell L30 is declared there: P 0.30, mean BLEU, the six COMB-NEW entries, bar = our own COMB-NEW 0.6839233380559118 (FeVeT 0.6356571184958077, Mockingbird-I1 0.6058548112827981). Rules: (i) beat the bar by more than 1e-9 in both summation modes; (ii) the null passes. Otherwise NOTHING.
- rules/bleu_freeze.md (2026-10-18T07:22:11Z) records PREREG.v2's sha256, stage2_bleu.py's sha256 and the 10 object hashes. All match the package (C1).
- rules/null_test.md: run 2026-10-18T12:47:49Z-12:47:50Z.
- Order: PREREG.v2 07:19:21Z, then object frozen 07:22:11Z, then scored and null-tested 12:47Z.
- PREREG.md (02:09:41Z) declares proportion 0.30 (cell C30) and itself says "a changed plan goes in PREREG.v2.md with its own time". PREREG.v2 is that addendum, so "stated in PREREG.md" is met in the project's versioned form.
- Times come only from the package's own records. File mtimes are copy times, so I cannot verify them independently. Because the object rebuilds byte for byte from PREREG.v2's rule (C4), there was no room to pick a variant after scoring.

### C8. Null model (PROVED-HERE)
- Re-run of the pre-registered tool: python3 -I tools/null_test_metric.py --metric bleu --gold-dir official/data-surprise --cand-dir combiner/test/0.30 --bar-dir bar_comb_new/test/0.30 --prop 0.30 --out (scratch). Output:
  - "real: candidate bleu 0.6874377388475998, bar 0.6839233380559119, d = 0.003514400791687966"
  - "controls: 400"
  - "best_control: 0.0035017194380646544"
  - "real_beats_all_controls: yes" (controls_ge_real 0)
  - This is identical to rules/null_test.md.
- My own implementation (mynull.py):
  - Uses the official bleu_score from the scorer module and the linear set-level decomposition of the official aggregation.
  - "items 11586, items where candidate and bar predictions differ 451 (0.0389), sets with nonzero delta 270 of 1237"
  - "real d (sum of set deltas) 0.0035144007916880324"
  - With the pre-registered seeds: "prereg 400 controls: best_control 0.0035017194380646877, controls >= real 0, real - best 1.2681353623344646e-05"
  - Extra controls with a different RNG: "nonzero set deltas 270, positive 162, negative 108; sign-flip sd 0.0012085409570359372; real/sd 2.9079699543716235" and "extra controls 100000: controls >= real 52, p (with +1) 0.0005299947000529995".
- The pre-registered null passes, narrowly in the max-of-400 sense, as CLAIM.md discloses. The estimated permutation p is about 5.3e-4. Even with a Bonferroni factor of 6 for the six pre-registered BLEU/BCFS objects, it stays near 3e-3.

### C9. Genuine and not subsumed (judgement)
- Not subsumed:
  - The earlier confirmed claim on bar_comb_new/test/0.30 is on mean NED. Under the criterion, "a win on one metric is a win on that metric only".
  - COMB-NEW's BLEU was never claimed, and could not be: it was not pre-registered and its test BLEU was already known.
  - This object beats COMB-NEW's BLEU and every other BLEU value at 0.30 in the package (C3), in both summation modes.
- Disclosures checked:
  - The main session had seen the test BLEU of the entries and of COMB-NEW. The object does not use them: it is a fixed function of frozen entries, val-0.30 and PREREG.v2's text (C4). Its only free choices were the risk function (item BLEU, the natural choice for a BLEU target) and the weight-fit statistic.
  - The sibling BLEU objects at 0.10 and 0.20 (same design) failed their bars, which argues against a design tuned to the test set.
- Post-hoc robustness (robust.py; not binding, not a claim): of the 20 best validation weight tuples in combiner_fit.json, "13 of 20" would also beat the bar on test.
  - Rank 2 [2, 3, 1, 3, 0, 2]: test 0.6869820647.
  - Rank 6 [2, 2, 0, 3, 0, 3]: 0.6838427084.
  - The win does not hinge on a single lucky weight tuple, but it is not universal either.

## Observations (none blocks the verdict; the cosmetic ones should be fixed in the package)
1. combiner/combiner_fit.json is an excerpt (0.30 only), so its sha256 differs from the bleu_freeze.md record (C1).
2. Run-folder naming is inconsistent:
   - CLAIM.md names the run folder runs/2026-10-18-1249.
   - rules/null_test.md says run 2026-10-18-1249 but puts its output in runs/2026-10-18-0839/out/lead.
   - This panel's run is 2026-10-18-0839.
3. rules/PREREG.md's header says "run 2026-10-18-0202, cell C30", while its table assigns C30 to runs/2026-10-18-0203.
4. The candidate also has a lower mean NED (0.22149461586532132) and a higher mean BCFS (0.7502543049557795) than the bar. Neither is pre-registered for this object, so no NED or BCFS claim may rest on this package.
5. "No surprise-test gold read for these objects" and the 07:19Z/07:22Z/12:47Z timeline are self-attested (C7).
6. Housekeeping: importing tools/ and official/src/ wrote 4 bytecode files (tools/__pycache__ x3, official/src/__pycache__ x1). One phylo probe run from the package's own code folder created an empty home/.w folder beside attempts/phylo/frozen/PRIMARY/code. I stopped that probe by PID, removed all of these, and reran the probe from a byte copy. Afterwards: "files: 364 ok: 364" and no __pycache__ or home folders in claim/.

## Verdict
The full criterion is met for cell L30:
- Trained only on training-0.30 plus the masked test-0.30 rows, each row predicted from its own visible cells.
- No solutions file read by the system.
- Declared proportion 0.30 and metric BLEU, pre-registered before the object existed.
- Official pinned scorer, calibrated bit for bit on Mockingbird-I1.
- Strictly above Mockingbird-I1, and above the cell's stricter bar (our own NED-targeted COMB-NEW) in both summation modes.
- Null passes.
- One cell, one metric, one object.

The win is genuine and not subsumed by the earlier NED claim.

confirmed_scope: At proportion 0.30, the frozen BLEU-MBR stage-2 object combiner/test/0.30 (the same predictions as object/predictions-0.30.tsv; six frozen entries trained on training-0.30 only, weights [2, 2, 1, 3, 1, 3] fit on the validation split shared/val/0.30 cut from training-0.30) has mean BLEU 0.6874377388475998 over the 10 surprise families under the pinned official ST2022 scorer (same value with left-to-right and compensated summation), strictly above Mockingbird-I1's official 0.6058548112827981, FeVeT's rescored 0.6356571184958077 and the cell's bar, our own earlier NED-targeted object bar_comb_new/test/0.30 at 0.6839233380559118 (by 0.003514400791688077 left-to-right and 0.003514400791687966 compensated), as a claim on mean BLEU only.

pass: true