(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the BA CRITERION skeptic subagent (Opus 5.5, model opus, agent a67134ca6d7012fbe) could not write a file named like a report. Text verbatim below.)

# Panel: CRITERION skeptic, cell BA (aggregate mean BCFS over the five proportions 0.10-0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 22:10:23 UTC 2026 (date -u)
end: Sun Oct 18 22:25:46 UTC 2026 (date -u)
material: the claim package claim/ only, plus kit/RULES.md and TROPHY_CASE.md (TROPHY_CASE.md has no Q15 entry). No network requests were made, so no stop-list line was needed. Interpreters: SYS (the entry's ML venv), SCO (the venv with the pinned scorer, used only as an interpreter), python3.13. My own scripts are in my scratch folder, outside claim/.

## Criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Claimed form: the full criterion in its aggregate form on BCFS. This is not a partial win (p1-p3 are not claimed).

## Checks run (numbers copied from command output)

1. Package integrity. `shasum -a 256 -c MANIFEST.sha256`: 470 of 470 OK, with no failures (471 files including the manifest). checker/frozen_result_sha256.txt: 50 lines checked, 0 mismatches. FROZEN.md's PRIMARY record: 20 result lines with 0 mismatches; config.json True; system.py True.

2. Scorer identity and the bar.
   - SCO's sigtypst2022.py has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, the same as official/src/sigtypst2022.py (lingpy 2.6.9, lingrex 1.2.0, Python 3.13.2).
   - scout/st2022_repo_page.html embeds oid 03094435cba4293ce0eea383036cab78499ad50d (2 occurrences).
   - My own rescoring script calls compare_words per family and takes statistics.mean over the 10 families, with sum shadowed left to right in sigtypst2022 and lingrex.util. At every P it prints "MB fam identical: True MB total identical to official: True" for P = 0.10, 0.20, 0.30, 0.40 and 0.50. So Mockingbird-I1's 50 family values and 5 totals reproduce bit for bit. Builtin-sum mode differs only in the last bits, as expected.
   - Official I1 BCFS totals: [0.7672735092897016, 0.7119659170836019, 0.6717099225519634, 0.6428278176401176, 0.6050308536957327].
   - Bar A_BCFS: 0.6797616040522236 left to right (0.6797616040522234 builtin). This equals PREREG rule 2.
   - Over all 10 official systems that have all five proportions, I1 has the highest A_BCFS. Next is Mockingbird-N1-A at 0.6685038317882127, then CrossLingference-Julia at 0.664930871621116.

3. Headline A recomputed independently with the official scorer at all five P from attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv.
   - Candidate S_BCFS(P) = [0.8091752827860231, 0.7629197798251665, 0.7347693490340722, 0.7136377968288752, 0.690510517808069].
   - A_BCFS = 0.7422025452564412 in both summation modes (left-to-right and builtin aggregation).
   - Margin A minus bar = 0.062440941204217615. "beats by more than 1e-9: True" in both modes.
   - The other metrics also match the CLAIM table: A_NED 0.23164186694791358 vs 0.2931673956342817; A_BLEU 0.6729772402356671 vs 0.6015772270938825; A_ED 0.9489657394965564 vs 1.1654140850286332.
   - checker/check_q15.py (python3.13) gives "Mockingbird-I1 mean BCFS recomputed ... EXACT" at all five P; "object A_BCFS 0.7422025452564412 (claimed 0.7422025452564412): EQUAL"; "rebuilt official-format files equal to the frozen ones: 50 of 50"; last line PASS.
   - Coverage: 56595 masked rows (4029, 7887, 11586, 14992 and 18101 at the five P), 0 rows without a prediction, 0 "Missing entry" lines.

4. Was the aggregate stated in PREREG.md before any result (rule 2)?
   - The folder's PREREG copy carries a header written at 22:07:31Z. Its body is everything from line 5 ("Written by the main session ..."). That body has sha256 2840e8180982bdcb7e95afc583aae1bb397f3262833db88496efab3684a948bf, exactly the value the header gives for the body frozen at 18:11:37Z.
   - The body defines A_m = (S_m(0.10)+...+S_m(0.50))/5 summed left to right, the BA bar 0.6797616040522236, the single-candidate rule 10 and the aggregate null (rule 13).
   - Stated order of events: body freeze 18:11:37Z; classifier/PRIMARY freeze 19:14:05Z; selection.md 21:16:09Z ("before any surprise-test gold has been read"); null run 21:33:36Z (null_test.md); header copy 22:07:31Z. The header adds only the cell label.
   - Limit: the package cannot independently timestamp the 18:11:37Z freeze. I verified only that the hash is consistent.
   - Why the timing cannot change the verdict: the candidate beats I1 at every single P (item 5). So any aggregate with positive weights over P, and the rank aggregate, gives the same result. The choice of aggregate could not have been tuned to create the win.

5. Is the score aggregate a fair reading?
   - "Mean score over the 10 surprise families ... aggregated over all 5 proportions": the mean over P of the official family-mean "total" is the equal-weight mean of the 50 family-by-P scores. That is the plain reading.
   - The official meta-evaluation (sigtypst2022.py main, --meta-evaluation) instead ranks systems per metric per proportion and averages the ranks.
   - Under that rank reading with the candidate inserted, the mean BCFS rank is CANDIDATE [1, 1, 1, 1, 1] = 1 against Mockingbird-I1 [2, 2, 2, 2, 3] = 2.2. Among official systems only, I1 is [1, 1, 1, 1, 2] = 1.2.
   - The candidate is first on BCFS at every P among all official systems. The win therefore holds under either reading.
   - Conclusion: the score aggregate is a fair reading, not a stretched one, and the verdict does not depend on which reading is used.

6. "Trained ONLY on training-*.tsv and the masked test-*.tsv"; one system; what it reads.
   - Code reading:
     - train reads only the manifest's surprise_train file per family, plus dev_dir/mannburmish/training-0.10.tsv and dev_dir/listsamplesize/training-0.10.tsv (config "devx").
     - predict reads only the model dir and the partition files listed in --jobs. Each row goes through predict_row(m, row, langs), and there are no global caches.
     - No option depends on P. The same code tree (sha 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051) and config run unchanged at every P.
     - This is one system in the criterion's sense: like the official per-proportion entries, including Mockingbird-I1, it is trained on training-P and predicts test-P.
   - Data view: data/view holds no solutions, cognates or wordlist files. All 100 surprise training/test files equal the official copies byte for byte ("view-vs-official diffs: 0"). The dev view holds only training-0.10/test-0.10.
   - Splits, checked on the official files for all 10 families:
     - Every training-0.50 row has an identical id and contents in every training-P.
     - training-0.50 is disjoint from every test-P.
     - The tests are nested, and training-P is disjoint from test-P. Result: "ALL True".
     - So all development data (shared/val/0.50 and the lens's folds) is training data at every P and contains no test row. The step "val rebuilt from training-0.50 with the organisers' split rule (ratio 0.15)" reports "differences 0".
   - Development-family rows (disclosed). Literally, they are training-*.tsv files of the task release, which the criterion's glob covers.
   - To judge the spirit, I ran a counterfactual with the frozen code and devx switched off (CLS_OPTS {"devx": null}; saved model option devx None at all 5 P). It was trained on hillburmish and kesslersignificance only (the models are per family), with each partition predicted in its own process.
     - Faithfulness control: the same driver with devx on, at 0.10, reproduced both families' frozen files with "bytes IDENTICAL to frozen".
     - Result: A_BCFS without devx = 0.741771109671925 against frozen 0.7422025452564412. The margin over the bar is 0.06200950561970142, and the counterfactual "beats Mockingbird-I1 at every P: True".
     - The development rows do not carry the win.

7. Row isolation at every P (every masked answer sits verbatim in a sibling row).
   - Harness: partitions by masked language, and asserts that no two rows of one cognate set share a partition.
   - Audits: audit_test_P.txt for P = 0.10 to 0.50 each show 40 identical, 0 FAIL, last line "AUDIT PASS".
   - Sealed checks: rules/sealed_cand_P.log for every P show train ok (1), 10 of 10 families "bytes IDENTICAL", "predict: 99 sealed processes", and last lines "SEALED_CHECK 0.10 PASS", "SEALED_CHECK 0.20 PASS", "SEALED_CHECK 0.30 PASS", "SEALED_CHECK 0.40 PASS" and "SEALED_CHECK 0.50 PASS".
   - Row counts in the sealed logs (4029, 7887, 11586, 14992, 18101) equal my counts.
   - From reading tools/sealed_check.py: training is sandboxed to training-P plus dev; each predict process can read only code, model and its own partition; solutions are never readable.

8. Selection (PREREG rule 10 as written).
   - Rule 10 names the lowest val-0.50 mean NED among the eligible single entries and COMB-6, -8, -10.
   - I rescored the candidate's frozen val-0.50 files with the official scorer: [ED, NED, BCFS, BLEU] = [1.1139670176922158, 0.26631878067630127, 0.8356251509060453, 0.6194739711457914]. This equals selection.md and ranking_040.md, where it is lowest (COMB-6 0.2707859930173011, COMB-8 0.2726853997296398, COMB-10 0.2735025293592694; no ties).
   - selection.md lists FROZEN.md with sha 1310b14a..., equal to the package copy. Its 20 classifier-PRIMARY result hashes show 0 mismatches.
   - The candidate froze at 19:14:05Z, before the 21:50:00Z deadline, with AUDIT PASS at 0.40.
   - Limits: the other entries' val files are not in the package, so their values are taken from selection.md.
   - The disclosed reranker gate was written after ungated val numbers were visible. That can only inflate the candidate's own val number, and therefore affect which entry was chosen. It uses no test data. PREREG rule 6 permits val-based development, so the rule was applied as written.
   - Informational: run_test_0.50.txt (20:49Z) and run_test_0.30.txt (21:03Z) show that the frozen code's test predictions at those P were produced before selection.md (21:16:09Z). These were predictions only; rule 11 constrains gold-reading scoring, which selection.md says had not happened.
   - Prior test exposure in earlier sessions is disclosed in PREREG.md. It does not touch this mechanical, val-only choice.

9. Null test (rules/null_test.md, PREREG rule 13). I reran the tool from the claim: python3.13 -I tools/null_test_metric_x.py --agg --metric bcfs --gold-dir official/data-surprise --cand-dir attempts/classifier/frozen/PRIMARY/test --bar-dir official/systems/mockingbird-i1/surprise. Output, exit 0:
   - "fast path bit-identical in every check: yes"
   - "controls: 400"
   - "best_control: 0.006862625341390349"
   - "real: 0.062440941204217726"
   - "real_beats_all_controls: yes"
   - "controls at or above real: 0" (the tool prints this count with a comparison sign)
   - Per-P advantages: 0.041901773496321404, 0.05095386274156466, 0.06305942648210872, 0.07080997918875753, 0.08547966411233632.
   - This matches null_test.md exactly.

10. One cell, one metric, one object, and subsumption.
   - The claim is only cell BA (A_BCFS, one statistic) for one object: the 50 files attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv, equal to object/predictions-P.tsv.
   - Sibling cells NA and LA (other metrics) and the 0.40 cells (single-proportion statistics) are separate claims. Per the criterion, "a win on one metric is a win on that metric only".
   - The aggregate is neither implied by the 0.40 cell nor by earlier single-proportion claims of other objects. Nothing in the package shows an earlier aggregate claim (the NOVELTY skeptic owns the external check).
   - All three metrics are reported (CLAIM table).

## Verdict
Within the letter of the criterion:
- A system that reads only training-*.tsv files (surprise training-P, plus two development-family training files) and the masked test-P rows, one row at a time, never solutions.
- Its 10-family mean BCFS, aggregated over all 5 proportions as stated in PREREG.md, strictly beats Mockingbird-I1's aggregate from the official results JSON totals by 0.0624.
- The score comes from the pinned ST2022 scorer, which reproduces the official values bit for bit.

Within the spirit:
- The win holds at every single proportion and under the README's rank aggregate.
- It survives removing the development-family rows (margin 0.0620).
- It passes the null by a wide margin.
- The disclosures (development rows, val-optimistic gate, prior test exposure) do not carry the win.

The only residual limit is that the PREREG freeze time cannot be timestamped from inside the package. Because the verdict does not depend on the aggregation choice, that limit does not affect the result.

confirmed_scope: The frozen single system classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/code, trained at each proportion P on training-P alone), whose predictions attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv (the same as object/predictions-P.tsv) for P = 0.10, 0.20, 0.30, 0.40, 0.50 give the aggregate A_BCFS = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 = 0.7422025452564412 (S(P) = mean B-Cubed F-score over the 10 surprise families under the pinned official ST2022 scorer, sums left to right), strictly beats Mockingbird-I1's aggregate 0.6797616040522236 computed the same way from its official results-surprise-P.json totals, a win on aggregate BCFS only.
pass: true