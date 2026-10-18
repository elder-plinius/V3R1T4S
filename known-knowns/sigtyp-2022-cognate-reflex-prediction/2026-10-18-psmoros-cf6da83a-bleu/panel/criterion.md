(Saved by the main session at 2026-10-18T12:37:59Z from the criterion skeptic subagent's returned text (cell L50; Opus 5.5, agent a3be10b4e07c36905); the subagent could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic, cell L50 (proportion 0.50, mean BLEU), private-quarry-B (Q15)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics; I saw only the claim package, the kit rules and the trophy case)
start: Sun Oct 18 11:44:28 UTC 2026 (date -u)
end: Sun Oct 18 12:12:05 UTC 2026 (date -u)
material: claim/ only (paths below are relative to claim/), repo/kit/RULES.md, repo/TROPHY_CASE.md (no Q15, SIGTYP or cognate entry). Interpreters: SYS (the entries' ML venv), SCO (the pinned-scorer venv, used only as an interpreter), Homebrew Python 3.13 for my own scripts. My scratch was outside claim/. No web request was made, so nothing was added to the stop list. No injection seen.

## Success criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

What is claimed: the full criterion (not a partial win), at proportion 0.50, on mean BLEU only. The object is combiner/test/0.50 (the same predictions in one file: object/predictions-0.50.tsv). The bar for this cell is stricter than the criterion: FeVeT's published per-item predictions, rescored.

## Checks run (real output copied)

C1. Package integrity.
- `shasum -a 256 -c MANIFEST.sha256`: 379 OK, 0 failures.
- `shasum -a 256 -c data/view_manifest.sha256`: 40 OK. 2 listed files are not in the package (data/view/datasets.json, data/view/datasets-surprise.json). They are metadata, no entry opens them, and they are absent from the sealed inputs. This is a packaging note only.
- data/view/surprise: 10 training-0.50.tsv and 10 test-0.50.tsv files, all byte-identical to official/data-surprise ("10 same training, 10 same test"). It holds no file of any other proportion.
- data/view/dev: only training-0.10.tsv and test-0.10.tsv of the 10 development families. There is no solutions file there.

C2. Scorer identity (SCO).
- sha256 of official/src/sigtypst2022.py: 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. The module SCO imports has the same hash (Python 3.13.2, lingpy 2.6.9, lingrex 1.2.0).
- Pin record: scout/st2022_commits.json, newest sha 03094435cba4293ce0eea383036cab78499ad50d. FeVeT: scout/fevet_commits.json, 31898c53bfffeef87265efa8a780b7be740162d1. I did not re-fetch these (no web).
- The scorer reproduces the official JSON bit for bit (C3). That ties this code to the official results.

C3. Independent rescoring. My own script calls official compare_words per family and takes statistics.mean over the 10 families, in two summation modes. It also has its own converter from fevet/pred_0.50_FAM.tsv to result files; the converter's output is byte-identical to tools/fevet_to_harness.py output ("10 same").
- ltr candidate ED NED BCFS BLEU = [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978466]
- ltr mockingbird ED NED BCFS BLEU = [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888]
- ltr fevet ED NED BCFS BLEU = [1.286021835157271, 0.30880111347517586, 0.6423935720824072, 0.5768215755932388]
- builtin candidate BLEU 0.6520222200978465; builtin mockingbird BLEU 0.5337187296541887; builtin fevet BLEU 0.5768215755932388
- official/results/results-surprise-0.50.json, "Mockingbird-I1" total: [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888].
  - Mockingbird family values equal the official ones (ltr): 10 of 10.
  - The highest BLEU total of any system in that JSON is Mockingbird-I1 0.5337187296541888. Next is Mockingbird-N1-B 0.49889009875615786.
- All 10 fevet/pred_0.50 files match the sha256 values in fevet/expected.sha256 and fevet/FETCH_RECORD.txt.

C4. Package scorer (REPRODUCE step 2): `STUB_MPL=1 SCO -I tools/score_test_050.py --entries E.json --json OUT.json --calib-props 0.50 --fevet-props 0.50 --candidate candidate`
- "ltr 0.50 Mockingbird-I1 NED 0.35176136367373956 official 0.35176136367373956 total EXACT families EXACT"
- "L50 (mean BLEU, higher is better): bar FeVeT recomputed ltr 0.5768215755932388 builtin 0.5768215755932388 (PREREG table 0.5768215755932388: EQUAL); Mockingbird-I1 official 0.5337187296541888 (PREREG table 0.5337187296541888)"
- "CANDIDATE L50 candidate | ltr: BLEU 0.6520222200978466 bar 0.5768215755932388 margin 0.075200644505 to MEETS (i); vs Mockingbird-I1 0.118303490444 | builtin: BLEU 0.6520222200978465 bar 0.5768215755932388 margin 0.075200644505 to MEETS (i); vs Mockingbird-I1 0.118303490444 | both modes: MEETS (i)". The tool prints an arrow here; I wrote it as "to".

C5. Standalone checker: `python3 checker/check_q15.py . object/predictions-0.50.tsv`
- "1. Mockingbird-I1 mean BLEU recomputed 0.5337187296541888, official 0.5337187296541888: EXACT"
- "2. FeVeT published predictions mean BLEU 0.5768215755932388"
- "3. object mean BLEU 0.6520222200978466 over 18101 items (claimed 0.6520222200978466): EQUAL"
- "margin vs Mockingbird-I1 0.118303490444 (higher is better)"
- "margin vs FeVeT 0.075200644505 (higher is better)"
- "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
- last line: "PASS"

C6. Object coherence.
- object/predictions-0.50.tsv has 18101 items; combiner/test/0.50 has 18101 items; "equal True".
- Masked cells in the 10 test-0.50 files: 18101. Masked cells without a prediction: 0.

C7. Per-family BLEU (ltr; candidate / FeVeT / Mockingbird-I1 / candidate minus FeVeT). The candidate beats FeVeT and Mockingbird-I1 on all 10 families.

| family | candidate | FeVeT | Mockingbird-I1 | candidate minus FeVeT |
|---|---|---|---|---|
| bantubvd | 0.614914 | 0.592530 | 0.498688 | +0.022384 |
| beidazihui | 0.845287 | 0.792570 | 0.800194 | +0.052717 |
| birchallchapacuran | 0.545083 | 0.427292 | 0.354493 | +0.117792 |
| bodtkhobwa | 0.816511 | 0.760657 | 0.710130 | +0.055854 |
| bremerberta | 0.621662 | 0.515467 | 0.559716 | +0.106195 |
| deepadungpalaung | 0.704483 | 0.567108 | 0.427551 | +0.137375 |
| hillburmish | 0.587845 | 0.520135 | 0.447745 | +0.067710 |
| kesslersignificance | 0.253208 | 0.187940 | 0.153517 | +0.065268 |
| luangthongkumkaren | 0.842636 | 0.763137 | 0.780330 | +0.079499 |
| wangbai | 0.688592 | 0.641380 | 0.604823 | +0.047212 |

C8. Stage-2 refit from the frozen entries (REPRODUCE step 3b; SCO, tools/stage2.py, entries in combiner/entries.json order, val gold shared/val only).
- "stage2: K=8 entries ['broker/PRIMARY', 'classifier/SECONDARY', 'broker/SECONDARY', 'r0202-broker/PRIMARY', 'classifier/PRIMARY', 'analogist/PRIMARY', 'phylo/PRIMARY', 'r0202-analogist/SECONDARY']; 65535 weight tuples"
- "0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507"
- "0.50 LOFO val mean (combine.py value) 0.26250736260023105"
- cmp against the package: test/0.50 is byte-identical for 10 of 10 families; val/0.50 is byte-identical for 10 of 10.
- So the claimed object is exactly the pre-registered COMB-8, with weights fit on the validation split only.

C9. The validation split comes only from training-0.50. I rebuilt shared/val/0.50 from data/view training-0.50 with the harness's copy of the organisers' split rule (ratio 0.15):
- "30 of 30 byte-identical to shared/val/0.50"
- "cognate sets present both in training-0.50 and test-0.50 (all families): 0"

C10. Freeze records. For each of the 8 entries I recomputed the code tree hash and the sha256 of every val/0.50 and test/0.50 file, and compared them with attempts/LENS/FROZEN.md. For carried entries the test hashes come from CARRIED.md.

| entry | freeze time (UTC) | code tree (first 16 hex) | code | val/0.50 | test/0.50 |
|---|---|---|---|---|---|
| broker/PRIMARY | 2026-10-18T10:09:21Z | a8f295186339fbdb | MATCH | 10/10 | 10/10 |
| classifier/SECONDARY | 2026-10-18T10:39:38Z | 6cc33b903ae1097c | MATCH | 10/10 | 10/10 |
| broker/SECONDARY | 2026-10-18T10:43:41Z | fc4aee016f3e2159 | MATCH | 10/10 | 10/10 |
| r0202-broker/PRIMARY | 2026-10-18T03:14:07Z | e0e12da3febeabfd | MATCH | 10/10 | 10/10 (from CARRIED.md) |
| classifier/PRIMARY | 2026-10-18T10:18:47Z | 014f4baa8694bafe | MATCH | 10/10 | 10/10 |
| analogist/PRIMARY | 2026-10-18T09:58:18Z | 94556b993ae1b190 | MATCH | 10/10 | 10/10 |
| phylo/PRIMARY | 2026-10-18T10:07:31Z | 94b531e1fe882c36 | MATCH | 10/10 | 10/10 |
| r0202-analogist/SECONDARY | 2026-10-18T03:23:18Z | 476c111d7f481d91 | MATCH | 10/10 | 10/10 (from CARRIED.md) |

rules/carry_setup.out ends "CARRY_SETUP PASS".

C11. Declaration order (times as recorded inside the package files; file mtimes are copy times).
1. rules/PREREG.md says "Frozen at 2026-10-18T08:49:14Z". It declares proportion 0.50, cell L50 = mean BLEU, the FeVeT bar 0.5768215755932388, the selection rule and the null design.
2. Carried test-0.50 predictions ran from 08:47:05Z to 08:50:22Z. These were predictions only: no gold was read and nothing was scored.
3. Sealed check of the carried entries: 09:01:46Z to 09:20:18Z.
4. Lens freezes: 09:58:18Z to 10:43:41Z, all before the 12:40:00Z deadline.
5. The last lens returned at 11:20:47Z.
6. rules/selection.md was written at 11:25:56Z.
7. The null test ran at 11:27Z.

So the proportion, the metric, the bar and the null test were all declared before any test-0.50 score existed. One candidate was chosen for all three cells by val-0.50 NED, not by test BLEU.

C12. Row isolation. Every masked answer of test-0.50 is visible in a sibling row, so this check is necessary.
- "test-0.50 items 18101 whose gold is visible verbatim in a sibling row of the same file 18101"
- "cognate sets in test-0.50: 2064 sets with a repeated masked language (would put two rows of one set in a partition): 0 partitions: 99"
- Test-mode audits of all 8 entries: each audit_test_0.50.txt has 40 "identical" lines, 0 FAIL, and ends "AUDIT PASS".
- rules/sealed_new_0.50.log: 100 "ok ... bytes IDENTICAL" family lines, ending "SEALED_CHECK 0.50 PASS". It covers broker PRIMARY/SECONDARY, classifier PRIMARY/SECONDARY, analogist PRIMARY and phylo PRIMARY.
- rules/sealed_carry_0.50.log: 110 such lines, ending "SEALED_CHECK 0.50 PASS". It includes carry broker-PRIMARY and analogist-SECONDARY.
- All 8 COMB-8 entries are sealed-checked, including weight-0 phylo/PRIMARY.
- The per-item stage-2 choice depends only on that item's 8 candidate strings and the val-fit weights (C8).

C13. My own sealed run of the two entries that read development-family rows: `python3 -I tools/sealed_check.py --prop 0.50 --components attempts/classifier/frozen/PRIMARY,attempts/classifier/frozen/SECONDARY --jobs 2`, work root in my scratch.
- "SEALED 0.50 start: 2 components, 18101 test rows in memory (parent), jobs 2, strict profiles, python SYS"
- "classifier__PRIMARY train ok 481s (sandboxed, strict profile)"; "classifier__PRIMARY predict: 99 sealed processes, 121s"
- "classifier__SECONDARY train ok 285s (sandboxed, strict profile)"; "classifier__SECONDARY predict: 99 sealed processes, 68s"
- 20 of 20 family lines "ok", for example:
  - "classifier__PRIMARY hillburmish ok partitions 9 rows 1638 items identical 1638/1638 bytes IDENTICAL"
  - "classifier__SECONDARY kesslersignificance ok partitions 5 rows 353 items identical 353/353 bytes IDENTICAL"
- Last line: "SEALED_CHECK 0.50 PASS".
- The sandbox really blocks reads. Under the generated profiles:
  - train profile reading official/data-surprise/hillburmish/solutions-0.50.tsv: rc=1 "Operation not permitted"
  - train profile reading the masked data/view test-0.50.tsv: rc=1 "Operation not permitted"
  - train profile reading its own copy of training-0.50: 234 lines
  - predict profile reading the training input: rc=1 "Operation not permitted"
  - predict profile reading another partition: rc=1 "Operation not permitted"

C14. Code audit of the 8 entries (code/system.py and config.json).
- File access:
  - Each entry reads its manifest's surprise_train files, its model folder, its job partition files and its own config.json.
  - Only classifier/PRIMARY and classifier/SECONDARY also read development rows, and only dev_dir/mannburmish/training-0.10.tsv and dev_dir/listsamplesize/training-0.10.tsv (load_train, option devx).
  - Broker's development-family substitution table is inactive: "umu": 0.0, and environment overrides only work with BRK_DEV=1. The other entries open no development file.
- No network calls and no subprocess calls in any entry.
- No embedded word lists: the longest lines are 144 to 506 characters, and the non-ASCII lines are sound-class and tone sets plus the classifier's segment notation maps.
- No pretrained weights.

C15. The disclosure about development-family rows: measurements and judgement.
- Overlap measured with my own script (the comparison is mine; the classifier's own normalisation is applied to the dev words):
  - hillburmish (dev mannburmish): 1638 items; 960 with a mapped masked language. For 133 of those, the gold (tones dropped) appears verbatim among the dev words of that language. Candidate exact-match rate: 0.3927 on mapped-language items vs 0.3481 on other items.
  - kesslersignificance (dev listsamplesize): 353 items; 229 mapped. For 28 of those, the gold appears verbatim among the dev words. Candidate exact-match rate: 0.0830 on mapped items vs 0.0161 on other items.
- Sensitivity (post hoc, for judgement only, not a claim). Each variant was refit on val with tools/stage2.py and scored with the official scorer (ltr mean BLEU):
  - without the two classifier entries (6 entries, weights [3, 2, 0, 1, 3, 2]): 0.650847279510414
  - without the two carried r0202 entries (6 entries, weights [2, 2, 1, 2, 1, 0]): 0.6411617028563878
  - without both classifier and r0202 entries (4 entries, weights [3, 1, 2, 3]): 0.6496095852455566
  - broker/PRIMARY alone (this run's entry, no development rows): 0.640778849958583
  - candidate with hillburmish and kesslersignificance set to FeVeT's own family values: 0.6387243733093166
  - candidate with those two families set to min(FeVeT, Mockingbird-I1): 0.6280431071250646
  - Every variant is above the bar 0.5768215755932388.
- Judgement:
  - Within the letter. The development families' training-0.10.tsv files are training-*.tsv files of the task release. No solutions-*.tsv of any family was read, and no surprise file of another proportion was read. PREREG rule 4 named data/view/dev as permitted before any lens started.
  - Within the spirit, by my reading, with a caveat. The organisers released the development families for building models. The criterion's restriction exists to keep the public surprise gold out, and these rows are not the surprise gold. The caveat: for two families, the rows are related-dataset data that share languages and concepts with the scored gold (133 and 28 verbatim gold matches above). Readers should know this.
  - Not decisive. The BLEU win does not depend on these rows: every variant without them, or with both families neutralised, still beats FeVeT by more than 0.05.

C16. Null test (PREREG rule 13; rules/null_test.md).
- Rerun of the package tool (REPRODUCE step 5): `python3 -I tools/fevet_to_harness.py --prop 0.50 ...` gave "TOTAL test rows 18101 filled 18101 missing 0 extra 0 language-mismatch 0". Then `python3 -I tools/null_test_metric.py --metric bleu --gold-dir official/data-surprise --cand-dir combiner/test/0.50 --bar-dir FEVET050 --prop 0.50 ...` printed:
  - "real: candidate bleu 0.6520222200978465, bar 0.5768215755932389, d = 0.07520064450460762"
  - "controls: 400"
  - "best_control: 0.01251243685677561"
  - "real_beats_all_controls: yes"
  - "controls >= real: 0" (tool output; ">=" means "at least")
  - These are identical to rules/null_test.md.
- My own version uses official bleu_score per item, ltr sums and statistics.mean, with the same swap protocol (random.Random(20261018 + c), one draw per cognate set):
  - "candidate BLEU 0.6520222200978466 bar BLEU 0.5768215755932388 real d 0.07520064450460784"
  - "controls 400 best_control 0.0125124368567755 controls_ge_real 0 real_beats_all True"
- The null passes. The real d is about 6 times the largest control.

C17. Scope of the claim.
- CLAIM.md claims one cell (proportion 0.50), one metric (mean BLEU) and one object (combiner/test/0.50, with object/predictions-0.50.tsv as an identical one-file copy, C6). It reports all three metrics, as the criterion requires.
- The same object is claimed in the sibling cells on NED and BCFS. Under the criterion, each win counts on its own metric only, so this BLEU claim is not subsumed by them.
- The trophy case has no earlier Q15 or SIGTYP entry. The earlier 0.50 combiner value in the PREREG (BLEU 0.6451264483943195, run 2026-10-17-1806) is information only, from splits overlapping test-0.50, and was never claimed. So this claim is not subsumed by an earlier claim either.

## Clause-by-clause verdict
- "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)": met.
  - Every entry's predictions depend only on training-0.50, the development families' training-0.10 rows (classifier entries only) and the row-isolated masked test-0.50 partitions. Evidence: 8 of 8 sealed checks in the logs, 2 of 2 rerun by me with reads verified to be blocked.
  - Stage-2 weights were fit only on shared/val/0.50, a pure function of training-0.50 (C8, C9).
  - No file of another proportion and no gold was read by any system.
- "mean score over the 10 surprise families at a declared proportion": met. It is statistics.mean of the 10 family values at 0.50, which was declared in rules/PREREG.md before any result (C11).
- "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric": met. BLEU 0.6520222200978466 vs 0.5337187296541888, margin 0.118303490444, in both summation modes. The cell's stricter bar is also met: FeVeT 0.5768215755932388, margin 0.075200644505 in both modes.
- "The repo scorer st2022 at a pinned commit computes the score": met. The pinned module's compare_words was used, and it reproduces the official totals and family values exactly. The pin's commit id is taken from the package's status record; I did not re-fetch it.
- "Report all three": met (CLAIM.md table).

## Residual notes (none changes the verdict)
- The PREREG, selection and null times are the package's own records. I had no independent clock evidence, but the content order is consistent: the PREREG holds no test-0.50 result of this session.
- The entries descend from earlier runs' methods; run 2026-10-17-1806 was tuned on splits that overlap test-0.50. The carried entries were frozen in run 2026-10-18-0202, whose data view also held lower-proportion training files. Their val-0.50-only development is a recorded rule that I cannot audit from the package.
- Mitigations for that lineage risk:
  - The code holds no lexical data.
  - The outputs at 0.50 are a sealed function of training-0.50 plus development rows only.
  - The margin over FeVeT is about 6 times the largest null control.
  - The entries made in this run alone, without carried or classifier entries, give 0.6496095852455566 (C15).
- Novelty of the FeVeT bar (whether a better published value exists) was not checked by me; that is the NOVELTY skeptic's job.
- Hygiene, outside the criterion: several package text files (scout/scout.md, rules/selection.md, rules/null_test.md, rules/sealed_*.log, the entries' REPRODUCE.md, combiner/combiner_fit.json and some tools) contain absolute home-folder paths with a user name. Kit rule 12 forbids that in anything shared. This quarry is private, so it matters only if the package ever leaves the machine.

confirmed_scope: At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (identical to object/predictions-0.50.tsv) predicts the 18101 masked rows of the 10 SIGTYP 2022 surprise families' test-0.50.tsv with mean BLEU 0.6520222200978466 under the pinned official ST2022 scorer (left-to-right summation; 0.6520222200978465 compensated), strictly above Mockingbird-I1's official 0.5337187296541888 and above this cell's bar, FeVeT's published predictions rescored at 0.5768215755932388, using only training-0.50, row-isolated masked test-0.50 partitions and the task's development families (including the disclosed development-family rows for hillburmish and kesslersignificance).

pass: true