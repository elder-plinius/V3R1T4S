(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the NA CRITERION skeptic subagent (Opus 5.5, model opus, agent a0ecacc915c22337c) could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic panel: cell NA (Q15 private-quarry-B, aggregate A_NED over the five proportions 0.10 to 0.50)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics; I saw only the claim package claim/, kit/RULES.md and TROPHY_CASE.md)
started: Sun Oct 18 22:10:23 UTC 2026 (date -u)
ended: Sun Oct 18 22:52:01 UTC 2026 (date -u)

Material: everything I read was in claim/: CLAIM.md, definition/Q15.json, REPRODUCE.md, rules/*, scout/scout.md, attempts/classifier/FROZEN.md, attempts/classifier/frozen/PRIMARY/ (code, logs, results), tools/q15h.py, tools/sealed_check.py (docstring and sandbox rules), tools/null_test_x.py (docstring), tools/mplstub.py and official/src/sigtypst2022.py. TROPHY_CASE.md has no Q15, SIGTYP or Mockingbird entry. I made no network requests, so nothing was added to the stop list. injection_suspected: none. Interpreters: SCO (the pinned-scorer interpreter: lingpy 2.6.9, lingrex 1.2.0) for scoring and the null test; SYS (the entry's interpreter) for retraining; python3.13 for standard-library checks. My scratch scripts are outside claim/, and every number below is copied from their output.

## 1. The criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

The claim is made in the criterion's aggregate form, on NED only. It does not claim a partial win (p1 to p3).

## 2. Clause-by-clause reading

(a) "aggregated over all 5 proportions, stated in PREREG.md". rules/PREREG.md rule 2 gives cell NA, the formula A_m = (S_m(0.10)+S_m(0.20)+S_m(0.30)+S_m(0.40)+S_m(0.50))/5 summed left to right, where S_m(P) is the official family-mean "total", and the bar "Mockingbird-I1 0.2931673956342817".
- Timing. The header of this folder's PREREG copy was written at 2026-10-18T22:07:31Z, after the results. It states that the body is byte-identical to the body frozen at 2026-10-18T18:11:37Z, with sha256 2840e818...a948bf. Check C16 shows that the body (line 5 to the end) has exactly that sha256. The header adds nothing of substance: cell NA, its formula and its bar are all in the body.
- Order of events in the package:
  - PREREG body: 18:11:37Z.
  - classifier/PRIMARY frozen: 19:14:05Z (its 0.40 audit ran 19:09:54Z to 19:10:15Z).
  - Ranking: 21:12:25Z. selection.md: 21:16:09Z.
  - Sealed checks: 21:24:49Z to 21:38:33Z. Null test started: 21:33:36Z.
  - The main session's test-prediction runs (predictions only, no gold read) finished training at 20:49Z (0.50), 21:02Z (0.30), 21:20Z (0.20) and 21:24Z (0.10).
- So the body predates every result. Limitation: the 18:11:37Z time is attested by the session's own records (the hash commitment out/prereg.sha256 is in the run folder, not in this package). I cannot prove it from claim/ alone.
- This does not matter for the truth of the claim. The candidate beats Mockingbird-I1 in all 50 family-by-proportion cells (C14). So any non-negative weighting of family values, the per-P reading and the rank reading all give a win. The choice of aggregate cannot have been tuned to manufacture one.

(b) "mean score over the 10 surprise families ... aggregated over all 5 proportions": score aggregate or rank aggregate?
- The criterion's bar is "Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric". Those files hold per-family scores and totals, not ranks.
- The README's meta-evaluation averages ranks over proportions and metrics. That mixes metrics, which contradicts "SAME metric" and "a win on one metric is a win on that metric only".
- So the faithful reading is the score aggregate the PREREG uses: the mean over P of the official family-mean NED. With equal weights per P, this equals the mean over all 50 family values.
- Under the rank reading restricted to NED the candidate also wins. At every P no official system has a lower NED total (C14), so it would rank 1st in all five NED columns.
- I conclude that the PREREG aggregate is a fair and literal reading.

(c) "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)".
- What the system reads:
  - At each P the harness manifest lists only the 10 surprise families' training-P.tsv plus dev_dir.
  - The code (C10) reads only the manifest files, its own config.json, and for two families dev_dir/FAM/training-0.10.tsv of the development families mannburmish and listsamplesize.
  - These are training-*.tsv files of the task release, so they are within the letter of the criterion.
  - Masked test rows reach the system only as partitions written by the harness.
- No solutions file, cognates file or wordlist file of any family is read. Check C8 shows that data/view holds no gold.
- One system? The frozen code and config (code tree sha256 4880a9cd...b993051) are retrained at each P on training-P alone. That is how the official systems produced their five per-P results, so it is one system in the criterion's sense.
- Nothing crosses proportions:
  - Every development choice was made on val-0.50, cut from training-0.50.
  - training-0.50's rows are contained verbatim in every training-P and are disjoint from every test-P (C9).
  - So at every P the development data lie inside that P's own training data.
- Row isolation. Every masked answer of test-P appears verbatim in a sibling row of the same file: 4029/4029, 7887/7887, 11586/11586, 14992/14992 and 18101/18101 items (C7). The safeguards:
  - The harness partitions each test file by masked language (asserted: no two rows of one cognate set in a partition).
  - The audit passes at every P (C11).
  - The sealed check passes at every P: retraining under sandbox-exec with only training-P and dev readable, then each partition predicted alone in its own process, 10/10 families bytes IDENTICAL (C11).
  - My own retrains at all five P, from views holding only that P's training and test files plus dev, reproduce all 50 result files byte for byte, and my audit at 0.10 passes (C12).
  - Exact-match rates of 0.655 down to 0.563 (C7) are far below what a sibling-row leak would give.

(d) "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric".
- The bar is Mockingbird-I1's A_NED from its official totals: 0.2931673956342817 left to right, 0.29316739563428174 with the builtin sum (C4).
- The candidate's A_NED is 0.23164186694791358 in both summation modes. That is lower by 0.0615255286863681 (left to right) and 0.06152552868636815 (builtin). Both exceed PREREG rule 12's 1e-9.
- Hidden-quantifier note (no effect on the verdict): the official JSONs hold placeholder zeros for Mockingbird-N2 at 0.20 to 0.50, so its BCFS and BLEU are also 0 there (a missing submission, not scores). A naive mean of its totals gives 0.06269171285472723. The criterion names Mockingbird-I1 as the bar, and the PREREG restricts "best official" to systems with all five proportions. CLAIM.md's parenthesis "(the best official system on this aggregate)" is true only in that restricted sense. I recommend saying so explicitly.

(e) "The repo scorer st2022 at a pinned commit computes the score".
- official/src/sigtypst2022.py has the same sha256 as the module installed in SCO: 9cde59bb...0f5b23a.
- scout/scout.md records commit 03094435cba4293ce0eea383036cab78499ad50d.
- With left-to-right summation the module reproduces Mockingbird-I1's official family values and totals bit for bit at all five P (C3). I used compare_words, the function the CLI's comparison calls, with statistics.mean over families, as compare_systems computes "total".

(f) "Report all three". CLAIM.md reports ED, NED, BCFS and BLEU at every P and for the aggregate. It claims A_NED only, and my recomputed candidate values match its table.

(g) Disclosures.
- Development-family rows. These are permitted by the letter: they are training-*.tsv files from the task release, and PREREG rules 4 and 6 allow them. In spirit, they could add same-language word forms for hillburmish and kesslersignificance. Check C14 shows the win does not depend on them: even if both families are given Mockingbird-I1's own values at every P, A_NED = 0.24705603848296187, still well below the bar 0.2931673956342817.
- Selection note (the reranker's per-family gate was written after val numbers were seen). Rule 6 allows development on val. Rule 10 says exactly which files to compare: singles' frozen val-0.50 files, and COMB LOFO val files. classifier/PRIMARY has the lowest value: 0.26631878067630127, which I recomputed (C15), against COMB-6 0.2707859930173011, COMB-8 0.2726853997296398 and COMB-10 0.2735025293592694. So the selection followed rule 10 as written. An optimistic val number can only change which clean object gets tested. It cannot inflate that object's test score, and only one candidate carries the claim.
- Prior test exposure. This is disclosed in the PREREG: the main session had seen test scores of carried entries. The candidate is a new entry; lenses never see test scores; the selection is mechanical on val; and the main session's test runs are reproduced from the frozen code by the sealed check and by my retrains.
- I judge the claim to be within both the letter and the spirit.

(h) One cell, one metric, one object; not subsumed.
- This folder claims only NA (A_NED). The object is object/predictions-P.tsv for the five P, equal item by item to attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv (C6).
- The same object is claimed on BCFS and BLEU in sibling cells BA and LA. Its 0.40 part is the object of N40, B40 and L40. Each of those is a different metric or statistic, and the criterion makes a win on one metric a win on that metric only.
- No other claim implies the aggregate. The 0.40 cells cover one proportion. Earlier single-proportion wins were made by other objects and would not form one system.
- So this is a genuine, non-subsumed claim of the full criterion in its aggregate form.

## 3. Checks run (real output)

C1. Package integrity: `shasum -a 256 -c MANIFEST.sha256` gave no non-OK lines; "lines: 470", "files: 470".

C2. Scorer identity:
"installed 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a" / "9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a  official/src/sigtypst2022.py" / "lingpy 2.6.9 lingrex 1.2.0".

C3. Independent rescoring: my own script with the official compare_words, run on the claim files and the official files.
```
[ltr] P=0.10 MB family values == official: True; MB totals == official: True; MB NED total 0.2431316340782435 (official 0.2431316340782435)
[ltr] P=0.10 CAND S_NED 0.20017478183757248  (ED 0.7741426354973481 BCFS 0.8091752827860231 BLEU 0.7183395130131847)
[ltr] P=0.10 families where cand NED < MB official NED: 10/10
[ltr] P=0.20 MB family values == official: True; MB totals == official: True; MB NED total 0.2648052468982754 (official 0.2648052468982754)
[ltr] P=0.20 CAND S_NED 0.21213687542061813  (ED 0.8518682371657778 BCFS 0.7629197798251665 BLEU 0.6960719420978517)
[ltr] P=0.20 families where cand NED < MB official NED: 10/10
[ltr] P=0.30 MB family values == official: True; MB totals == official: True; MB NED total 0.2898984929868421 (official 0.2898984929868421)
[ltr] P=0.30 CAND S_NED 0.23201071558421696  (ED 0.9552549562700591 BCFS 0.7347693490340722 BLEU 0.6721728449836378)
[ltr] P=0.30 families where cand NED < MB official NED: 10/10
[ltr] P=0.40 MB family values == official: True; MB totals == official: True; MB NED total 0.316240240534308 (official 0.316240240534308)
[ltr] P=0.40 CAND S_NED 0.2455448938803044  (ED 1.0267686117591617 BCFS 0.7136377968288752 BLEU 0.6533966833715619)
[ltr] P=0.40 families where cand NED < MB official NED: 10/10
[ltr] P=0.50 MB family values == official: True; MB totals == official: True; MB NED total 0.35176136367373956 (official 0.35176136367373956)
[ltr] P=0.50 CAND S_NED 0.26834206801685595  (ED 1.1367942567904354 BCFS 0.690510517808069 BLEU 0.624905217712099)
[ltr] P=0.50 families where cand NED < MB official NED: 10/10
[builtin] P=0.40 CAND S_NED 0.24554489388030437  (the other builtin-mode S_NED values equal the ltr ones)
BAR A_NED Mockingbird-I1 from official totals: ltr 0.2931673956342817 builtin 0.29316739563428174
CAND A_NED: ltr 0.23164186694791358 builtin 0.23164186694791358
margin ltr 0.0615255286863681 margin builtin 0.06152552868636815 > 1e-9: True
```
Builtin-mode Mockingbird family values differ from the official ones in the last bits, as expected: the 2022 numbers were computed with left-to-right sums. No "Missing entry" line was printed for the candidate: grep count 0.

C4. Official A_NED of every official system, as the left-to-right mean of its five official totals (same run):
```
official A_NED Mockingbird-N2: 0.06269171285472723   (placeholder zeros at 0.20-0.50; see 2(d))
official A_NED Mockingbird-I1: 0.2931673956342817
official A_NED Mockingbird-N1-B: 0.314248874788133
official A_NED Mockingbird-N1-A: 0.3166522361794327
official A_NED Mockingbird-N1-C: 0.3326146264819196
official A_NED Baseline-Baseline-SVM: 0.34743783782430304
official A_NED CEoT-Extalign-RF: 0.3599634843631829
official A_NED Baseline-Baseline: 0.3698412067899648
official A_NED CrossLingference-Julia: 0.4071544066766225
official A_NED Leipzig-Transformer: 0.4451431775904207
```
Mockingbird-N2's official entries at 0.20, 0.30, 0.40 and 0.50 are "total [0, 0, 0, 0]", with every family "[0, 0, 0, 0]".

C5. Standalone checker: `python3 -I checker/check_q15.py . object`
```
3. Mockingbird-I1 A_NED from the official totals 0.2931673956342817 (PREREG 0.2931673956342817): EQUAL
4. object A_NED 0.23164186694791358 (claimed 0.23164186694791358): EQUAL
   margin vs Mockingbird-I1 0.061525528686 (lower is better)
5. rebuilt official-format files equal to the frozen ones: 50 of 50
PASS
```
Its step 1 printed "EXACT" at all five P.

C6. Object identity and freeze records:
- The 20 FROZEN.md result hashes of ROLE=PRIMARY: "20 OK". Its code files: "config.json: OK", "system.py: OK".
- checker/frozen_result_sha256.txt against the 50 frozen result files: "50 OK".
- object/predictions-P.tsv against the frozen files, item map: "0.10 object rows 4029 frozen non-empty cells 4029 equal maps True", "0.20 ... 7887 ... True", "0.30 ... 11586 ... True", "0.40 ... 14992 ... True", "0.50 ... 18101 ... True".

C7. Coverage and sibling-row exposure:
- Gold items equal the "?" cells of test-P with the same keys at every P: "0.10 gold items 4029 ? cells in test view 4029 same keys True" and likewise 7887, 11586, 14992, 18101.
- Exact-match and sibling-row lines:
  - "0.10 items 4029 exact-match 2640 (0.655) gold verbatim in a sibling test row 4029"
  - "0.20 ... 4964 (0.629) ... 7887"
  - "0.30 ... 7037 (0.607) ... 11586"
  - "0.40 ... 8764 (0.585) ... 14992"
  - "0.50 ... 10187 (0.563) ... 18101"

C8. Data view: "identical 100 differ 0". All data/view/surprise training-P and test-P files are byte-identical to official/data-surprise. No solutions, cognates or wordlist file exists under data/view. dev/ holds only training-0.10.tsv and test-0.10.tsv for each of the 10 development families.

C9. Splits:
- "disjoint train-P/test-P, train-0.50 disjoint from every test-P, train-0.50 subset of every train-P: True"
- "nesting issues: [] 0"
- "val split within training-0.50 and disjoint from every test-P:  True"
- "training-0.50 rows identical (header and content) inside every training-P: True 0"

C10. Code I/O audit (attempts/classifier/frozen/PRIMARY/code/system.py, config.json):
- train reads man["surprise_train"] and, through devx, dev_dir/mannburmish/training-0.10.tsv (for hillburmish) and dev_dir/listsamplesize/training-0.10.tsv (for kesslersignificance). Dev test-0.10 is explicitly not used.
- predict reads only the model dir and the partition files named in --jobs, and predicts each row with predict_row(m, row, langs).
- No reference to solutions, cognates, wordlist, systems/, results/ or any absolute path. CLS_OPTS is unset in frozen runs (and in mine).

C11. Package audits and sealed checks:
- attempts/classifier/frozen/PRIMARY/audit_test_P.txt for P = 0.10, 0.20, 0.30, 0.40, 0.50: 40 "identical" lines each (3 single rows plus 1 whole partition per family), each ending "AUDIT PASS".
- rules/sealed_cand_P.log for all five P: "train ok ... (sandboxed, strict profile)", 10 of 10 families "ok partitions ... bytes IDENTICAL", "predict: 99 sealed processes", final lines "SEALED_CHECK 0.10 PASS", "SEALED_CHECK 0.20 PASS", "SEALED_CHECK 0.30 PASS", "SEALED_CHECK 0.40 PASS", "SEALED_CHECK 0.50 PASS".

C12. My own retrain and predict at every P:
- Setup: SYS -I tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --props P --workers 2. Q15H_VIEW pointed to a fresh view of mine holding only that P's training-P.tsv and test-P.tsv (copied from official/data-surprise) plus dev/. OMP_NUM_THREADS=2, MKL_NUM_THREADS=2, HOME inside my folder, nice 5.
- The 0.10 manifest's surprise_train lists only "training-0.10.tsv".
- Results:
  - "test 0.10 train rc=0 825s" (machine load about 90), then 10/10 families identical (cmp).
  - "test 0.30 train rc=0 388s", 10/10 identical.
  - "test 0.50 train rc=0 258s", 10/10 identical.
  - "test 0.20 train rc=0 245s", 10/10 identical.
  - "test 0.40 train rc=0 159s", 10/10 identical.
- All 50 result files were reproduced byte for byte.
- My audit on my 0.10 retrain (q15h.py audit --props 0.10): 40 "identical", "AUDIT PASS".

C13. Null test (PREREG rule 13). I wrote my own reimplementation from the rule's text, not the package tool:
- per-item NED by the scorer's own rule;
- compare_words and compare_systems aggregation with left-to-right sums;
- in control c, one random.Random(20261018 + c) drawing at 0.10, 0.20, 0.30, 0.40, 0.50 in that order, families in the fixed order, sets in order of first appearance in that P's gold, swap when the draw is below 0.5;
- 400 controls.
```
real d 0.06152552868636814  A_bar - A_cand 0.0615255286863681
controls 400
best_control 0.0060856017913201
real_beats_all_controls yes
controls >= real 0
control d quantiles min -0.007719839332930034 median -5.150416301762939e-05 max 0.0060856017913201
```
This matches rules/null_test.md exactly (real 0.06152552868636814, best_control 0.0060856017913201, real_beats_all_controls: yes).

C14. Robustness and readings:
- The candidate's family NED is below Mockingbird-I1's official family NED in 10/10 families at every P (C3), so 50/50 cells.
- Per-P totals, candidate against Mockingbird-I1: 0.20017 vs 0.24313, 0.21214 vs 0.26481, 0.23201 vs 0.28990, 0.24554 vs 0.31624, 0.26834 vs 0.35176.
- Official systems with a lower NED total than the candidate, at each P: "[]". The best official at each P is Mockingbird-I1.
- Dev-row worst case: "worst-case A_NED with hillburmish+kesslersignificance set to MB values: 0.24705603848296187 bar 0.2931673956342817".
- 8-family check: "8-family A_NED cand 0.17912732618759658 MB 8-family 0.2367665226267463".

C15. Selection input: my recomputation of classifier/PRIMARY's frozen val-0.50 files with the official scorer gave "classifier/PRIMARY val-0.50 mean NED 0.26631878067630127 ED 1.1139670176922158". This equals rules/ranking_040.md rank 1 and the selection.md rule-10 table row 1, the lowest of 32 rows. The other entries' val files are not in the package, so their values are taken from ranking_040.md.

C16. PREREG body hash: `tail -n +5 rules/PREREG.md | shasum -a 256` gives "2840e8180982bdcb7e95afc583aae1bb397f3262833db88496efab3684a948bf", the hash the header states for the body frozen at 18:11:37Z. Starting at lines 2, 3, 4 or 6 gives other hashes.

## 4. Verdict
- The result meets the full success criterion in its aggregate form on NED:
  - The aggregate is stated in PREREG.md (rule 2), with formula and bar, in a body whose hash matches the frozen one.
  - One frozen system, retrained at each P on training-P only (plus development-family training files, which the letter permits), predicts each masked row in isolation. Isolation is verified by audits and sealed checks at all five P, and my retrains reproduce all 50 result files byte for byte.
  - Its A_NED of 0.23164186694791358, computed with the pinned official scorer (which reproduces the official Mockingbird-I1 values bit for bit), is strictly lower than Mockingbird-I1's 0.2931673956342817 in both summation modes.
  - The pre-registered null passes (0.0615 against a best control of 0.0061).
  - The selection followed PREREG rule 10 as written.
  - The win also holds per proportion, per family, under the NED rank reading, and with the two dev-row families given to Mockingbird-I1.
- Caveats, recorded and not disqualifying:
  - The 18:11:37Z freeze time is attested by session records outside this package.
  - CLAIM.md's "best official system on this aggregate" should say "among official systems with all five proportions": Mockingbird-N2's official JSON entries at 0.20 to 0.50 are placeholder zeros.

confirmed_scope: Over the five proportions 0.10, 0.20, 0.30, 0.40 and 0.50, the frozen single system classifier/PRIMARY (code attempts/classifier/frozen/PRIMARY/code, retrained at each proportion P on that P's surprise training files plus the development-family training files; predictions attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv, equal to object/predictions-P.tsv) has the PREREG aggregate A_NED = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 = 0.23164186694791358, where S(P) is the mean NED over the 10 surprise families under the pinned official ST2022 scorer, strictly lower than Mockingbird-I1's A_NED 0.2931673956342817 computed the same way from its official results-surprise-P.json totals, a win on NED only.

pass: true