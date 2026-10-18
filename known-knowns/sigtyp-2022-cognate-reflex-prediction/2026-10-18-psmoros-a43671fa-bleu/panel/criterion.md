(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the LA CRITERION skeptic subagent (Opus 5.5, model opus, agent a34f63cc495cdae5e) could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic, cell LA (aggregate mean BLEU over the five proportions), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics); material: the claim package only (claim/), kit/RULES.md, TROPHY_CASE.md
start: Sun Oct 18 22:10:23 UTC 2026 (date -u)
end: Sun Oct 18 22:51:13 UTC 2026 (date -u)
web requests: none (no fetch of any kind; nothing added to the stop list)
injection_suspected: none

All paths below are relative to claim/. SCO = the pinned-scorer interpreter named in my instructions; SYS = the
entry systems' interpreter. My own scripts lived outside claim/ (score_all.py, my_null.py, val_ned.py,
retrain_all.sh, inline python3.13 checks).

Notation: in quoted command output, the comparison signs are written LE, LT and GE here (the kit's package check rejects
angle brackets); everything else in the quoted lines is exactly what the commands printed.

## 1. The criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score
over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md)
strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED,
or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The
repo scorer `st2022` at a pinned commit computes the score."

Claimed here: the full criterion in its aggregate form, on BLEU only (no partial win p1-p3 is claimed; PREREG rule 3).

## 2. Package integrity
- shasum -a 256 -c MANIFEST.sha256: 470 lines, 470 ": OK", no failures.
- attempts/classifier/FROZEN.md, record "## frozen 2026-10-18T19:14:05Z" (ROLE=PRIMARY): 22 hash lines; code files
  config.json 225856a472703e1e82fbd79bbd2aedd18b19359170fd28a7fecb1f6461a9f109 and system.py
  8482ef52c4e41beb4a67da8fc5524263f58945fbf8a093644b783b43656030ca match; 20 of 20 result files (val/0.50, test/0.40)
  ": OK". Code tree hash recomputed with q15h.tree: 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051
  (equals the record and selection.md).
- python3 -I checker/check_q15.py . object: Mockingbird-I1 mean BLEU recomputed EXACT at all five P; "3. Mockingbird-I1
  A_BLEU from the official totals 0.6015772270938825 (PREREG 0.6015772270938825): EQUAL"; "4. object A_BLEU
  0.6729772402356671 (claimed 0.6729772402356671): EQUAL"; "margin vs Mockingbird-I1 0.071400013142"; "5. rebuilt
  official-format files equal to the frozen ones: 50 of 50"; last line "PASS".

## 3. Is the aggregate stated in PREREG.md before any result? (rule 2)
- rules/PREREG.md = a 4-line header written 2026-10-18T22:07:31Z (the copy time, stated in the header) over the frozen
  body. tail -n +5 rules/PREREG.md | shasum -a 256 = 2840e8180982bdcb7e95afc583aae1bb397f3262833db88496efab3684a948bf,
  exactly the body hash the header names for the body frozen at 2026-10-18T18:11:37Z. (Cut points 1, 2, 3, 5 give other
  hashes; only the documented header boundary matches.)
- The body's rule 2 states the statistic: "A_m = (S_m(0.10) + S_m(0.20) + S_m(0.30) + S_m(0.40) + S_m(0.50)) / 5,
  summed left to right in that order, where S_m(P) is the family mean of metric m at P (the official "total")", the
  cell LA and its bar "Mockingbird-I1 0.6015772270938825"; rule 10 fixes one candidate for all six cells; rule 13 the
  aggregate null.
- Timeline from the package (all times as written in the files): PREREG body 18:11:37Z; audit at 0.40 19:09:54Z-19:10:15Z;
  freeze of classifier/PRIMARY 19:14:05Z; main-session test runs of the frozen code (predictions only) 0.50 train done
  20:49:18Z, 0.30 21:02:56Z, 0.20 21:20:10Z, 0.10 21:24:30Z with audits 20:50, 21:03, 21:20, 21:24; frozen_entries.md
  21:12:05Z; ranking_040.md 21:12:25Z; selection.md 21:16:09Z ("before any surprise-test gold has been read in this
  session"); sealed checks 21:24:49Z (0.50) to 21:38:33Z (0.40); null test 21:33:36Z; this folder's PREREG copy 22:07:31Z.
  The aggregate was stated before any test result of this object existed.
- Not independently verifiable from the package: the 18:11:37Z freeze time itself and the statement that no gold was read
  before 21:16:09Z (they rest on the main session's records; selection.md lists a sha256 of the run folder's own PREREG
  copy, which has a different header and is not in this package). Nothing in the package contradicts them. The test
  predictions at 0.50 and 0.30 existed before selection.md; they were not scored (run logs hold only harness lines),
  and rule 10 reads val-0.50 only, so this does not touch the selection.

## 4. Is the score aggregate a fair reading of the criterion?
- The criterion's words are "mean score over the 10 surprise families ... (or aggregated over all 5 proportions ...)" on
  "the SAME metric". A mean over P of the family-mean score is the literal score aggregate; because every P has the same
  10 families it equals the mean over the 50 (P, family) cells. Mockingbird-I1's value is formed the same way from its
  own official totals, so the comparison is like for like.
- The official README's meta-evaluation averages RANKS over proportions and metrics. That mixes metrics, which "a win on one
  metric is a win on that metric only" rules out, and it is not a score. I conclude the score aggregate is the fair (and the
  literal) reading. It also makes no difference here: on BLEU the candidate is above every official system at every P (my
  scoring vs the 10 systems in each results-surprise-P.json: "official systems above: []" at 0.10, 0.20, 0.30, 0.40, 0.50).
  So a BLEU-only rank aggregate would also put it first (rank 1 at all five P; Mockingbird-I1 would drop to 2).
- Bar check (official JSON, left to right): A_BLEU of the 10 systems that have all five P: Mockingbird-I1
  0.6015772270938825, Mockingbird-N1-B 0.5739708839607733, Mockingbird-N1-A 0.5724785535357948, Mockingbird-N1-C
  0.5513710848081363, Baseline-Baseline-SVM 0.5406672591377498, CEoT-Extalign-RF 0.5227742615104686, Baseline-Baseline
  0.5061025005292537, CrossLingference-Julia 0.4565210644206756, Leipzig-Transformer 0.4259328183325886, Mockingbird-N2
  0.11487912591146295. Mockingbird-I1 is the right bar, and its value equals the PREREG bar exactly.

## 5. Headline recomputed with the official scorer (my script, SCO interpreter)
Scorer: official/src/sigtypst2022.py is byte-identical to the module the SCO interpreter imports (cmp: identical; sha256
9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a). The pinned commit 03094435cba4293ce0eea383036cab78499ad50d
appears as "currentOid" in scout/st2022_repo_page.html (sha256 fec88fad...1012, matching scout.md). Per family:
compare_words(official/data-surprise/FAM/solutions-P.tsv, attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv,
report=False)[-1][1:]; S(P) = statistics.mean over the 10 families (as compare_systems computes "total"); `sum` shadowed by a
left-to-right loop in sigtypst2022 and lingrex.util for mode ltr, builtin sum for mode builtin.

Output, mode ltr:
  "mode ltr MB family values identical to official: True | MB totals identical: True"
  P 0.10 cand S_BLEU 0.7183395130131847, MB official 0.6633184488563897 (recomputed 0.6633184488563897)
  P 0.20 cand S_BLEU 0.6960719420978517, MB official 0.632633947442519 (recomputed 0.632633947442519)
  P 0.30 cand S_BLEU 0.6721728449836378, MB official 0.6058548112827981 (recomputed 0.6058548112827981)
  P 0.40 cand S_BLEU 0.6533966833715619, MB official 0.5723601982335171 (recomputed 0.5723601982335171)
  P 0.50 cand S_BLEU 0.624905217712099, MB official 0.5337187296541888 (recomputed 0.5337187296541888)
  cand A: ED 0.9489657394965564, NED 0.23164186694791358, BCFS 0.7422025452564412, BLEU 0.6729772402356671
  MB A (from official totals): ED 1.1654140850286332, NED 0.2931673956342817, BCFS 0.6797616040522236, BLEU 0.6015772270938825
  A_BLEU diff (cand - MB): 0.07140001314178457
Mode builtin: cand A_BLEU 0.6729772402356671, MB A_BLEU 0.6015772270938825, diff 0.07140001314178457 (Mockingbird-I1's
family values are not bit-identical to the 2022 JSON in builtin mode, as expected; the 2022 scorer summed left to right).
All three metrics are reported as the criterion asks. My values equal every number in the CLAIM.md table. Only A_BLEU is
claimed here. Margin 0.0714 against the 1e-9 of PREREG rule 12 (i), in both modes.
Per-family BLEU vs Mockingbird-I1: the candidate is higher on 10 of 10 families at 0.10, 0.20, 0.30 and 0.40 and on
9 of 10 at 0.50 (not on bantubvd).

## 6. "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)"
One system: the same frozen code tree (4880a9cd...; config.json + system.py) runs at every P. At each P it is trained from
scratch on that P's manifest. This is how the shared task itself produced each system's per-proportion results, so
Mockingbird-I1's aggregate is formed from per-P runs in the same way. No per-P tuning: config.json is a single file.
What it reads (code audit of system.py, every open()/load() call site): config.json; the harness manifest; the manifest's
surprise_train file of each family (training-P.tsv; tools/q15h.py cmd_run builds it from train_file(test, P, FAM) only);
for two families (config "devx") the development files dev_dir/mannburmish/training-0.10.tsv and
dev_dir/listsamplesize/training-0.10.tsv (the code reads only "training-0.10.tsv": "test-0.10 rows ... not used"); its own
model folder; the partition files named in --jobs. No string "solutions", "cognates" or "wordlist" in the code. No word
list is embedded: 17 of 673 string literals hold non-ASCII text, all of them the generic sound-class tables (lines 102-111),
and no non-docstring literal is longer than 200 characters.
No other proportion and no gold:
- data/view/surprise files vs official/data-surprise: 100 files (training and test, five P, ten families) compared, 0 differ.
  No solutions file anywhere under data/ (find: 0).
- Splits (my check over the view): "training-0.50 disjoint from test-P at every P, all families: True"; "training-P
  disjoint from test-P: True"; "test sets nested 0.10 LE 0.20 LE ... LE 0.50: True"; "val-0.50 sets within training-0.50: True";
  "every test row has exactly one '?' cell: True"; "training-0.50 rows (keys) contained in training-P for every P LT 0.50,
  all families: True"; "those rows byte-identical (and same header): True". So all development data (val-0.50 cut from
  training-0.50) lies inside training-P at every P. Every design choice therefore used only data the system may read at
  that P (plus the development families), and no test set was touched.
- Sealed check logs (rules/sealed_cand_P.log; retrained under sandbox-exec, strict profile, with only training-P and the
  development view readable, then each partition predicted in its own process): 0.10 "train ok 238s", 0.20 206s, 0.30
  176s, 0.40 155s, 0.50 129s; each "predict: 99 sealed processes"; 10 of 10 families "bytes IDENTICAL" at each P (e.g.
  0.50: beidazihui "partitions 19 rows 4921 items identical 4921/4921 bytes IDENTICAL"); final lines "SEALED_CHECK 0.10
  PASS", "SEALED_CHECK 0.20 PASS", "SEALED_CHECK 0.30 PASS", "SEALED_CHECK 0.40 PASS", "SEALED_CHECK 0.50 PASS".
- My own retrain (supplementary to the REPRODUCE skeptic): for each P I built a view holding ONLY
  surprise/FAM/training-P.tsv and test-P.tsv plus dev/ (no other proportion and no solutions present), set Q15H_VIEW to it, and ran
  SYS -I tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --props P --workers 2 --python SYS,
  then cmp against the frozen result files:
  "2026-10-18T22:24:13Z RETRAIN 0.50 identical 10/10" (train rc=0 502s)
  "2026-10-18T22:32:58Z RETRAIN 0.40 identical 10/10" (train rc=0 440s)
  "2026-10-18T22:40:06Z RETRAIN 0.30 identical 10/10" (train rc=0 371s)
  "2026-10-18T22:46:02Z RETRAIN 0.20 identical 10/10" (train rc=0 332s)
  "2026-10-18T22:50:25Z RETRAIN 0.10 identical 10/10" (train rc=0 250s)
  So at every P the claimed predictions follow from training-P alone (plus dev/) and the masked test-P rows.
Row isolation (every masked answer is in a sibling row):
- My check: the answer is visible verbatim in a sibling row for 4029 of 4029 items at 0.10, 7887/7887 at 0.20,
  11586/11586 at 0.30, 14992/14992 at 0.40, 18101/18101 at 0.50 (so isolation is essential). The harness partitions by
  masked language and asserts "two rows of one cognate set in a partition" never happens.
- Audits attempts/classifier/frozen/PRIMARY/audit_test_P.txt: 40 "identical" lines (3 single rows and 1 whole partition per
  family, fresh processes) and "AUDIT PASS" at each of 0.10, 0.20, 0.30, 0.40, 0.50.
- The sealed check (above) predicts every partition alone in a sandboxed process that can read nothing but code, model and
  that partition, and it is byte-identical at every P. So no cross-partition state reached the claimed files.
- Sanity: exact-match rate of the candidate vs Mockingbird-I1: 0.6552 vs 0.5761 (0.10), 0.6294 vs 0.5472 (0.20), 0.6074 vs
  0.5284 (0.30), 0.5846 vs 0.4921 (0.40), 0.5628 vs 0.4570 (0.50), far from the 1.0 a sibling copy would give.

## 7. Disclosures in CLAIM.md: letter and spirit
(a) Development-family rows (mannburmish for hillburmish; listsamplesize English/German/French for kesslersignificance).
Letter: they are training-*.tsv files of the official task release, not solutions files. PREREG rules 4 and 6 allow the
development families. Spirit: they are a different dataset of the same release, not surprise gold, and they may share
concepts. Robustness (mine): with the candidate's hillburmish and kesslersignificance BLEU replaced by Mockingbird-I1's
official values at every P, A_BLEU = 0.6592622617157929, still above the bar by 0.057685034621910436. Dropping both families
from both systems gives 0.7330242227627486 vs 0.6609179294853604. devx changes only those two families' models (per-family
training), so the win does not rest on these rows.
(b) Selection note. Rule 10 as written: the candidate is the lowest val-0.50 mean NED among eligible singles (frozen val
files) and COMB-6/8/10 (LOFO), with ties ED, singles first, earlier freeze. My official-scorer recomputation of the
candidate's frozen val files: "ED 1.1139670176922158 NED 0.26631878067630127 BCFS 0.8356251509060453 BLEU 0.6194739711457914",
equal to rule-10 table row 1. The next entries are broker/PRIMARY 0.2692807965192631 and COMB-6 0.2707859930173011 (taken
from selection.md and ranking_040.md; their files are not in this package). Eligibility: frozen 19:14:05Z, before the
21:50:00Z deadline; 20 result files; AUDIT PASS at 0.40 (frozen_entries.md). The reranker gate (config.json rr.skip =
bantubvd, beidazihui, kesslersignificance) was chosen after the lens saw per-family val numbers. Rule 6 allows every lens
choice on val-0.50, so rule 10 was applied as written. The gate decided the selection: according to the note, ungated 0.2722 would
have ranked fifth, below broker/PRIMARY, classifier/SECONDARY, COMB-6 and r0839-broker/PRIMARY. But val-0.50 is disjoint from every test set and lies inside each
training-P, so this optimism is about which entry was picked and cannot inflate the measured test score. No test number
entered the selection.
(c) Prior test exposure (PREREG): earlier sessions read gold at 0.10-0.30 and 0.50 for other objects. This object was frozen
in this session (19:14:05Z) and selected by a mechanical val-only rule. The statistic does not depend on that history: the
candidate leads at every P and, on BLEU, under rank aggregation too.
Within the letter and the spirit.

## 8. Null model (rules/null_test.md, PREREG rule 13)
- Rerun of the package tool: SCO -I tools/null_test_metric_x.py --agg --metric bleu --gold-dir official/data-surprise
  --cand-dir attempts/classifier/frozen/PRIMARY/test --bar-dir official/systems/mockingbird-i1/surprise: "fast path
  bit-identical in every check: yes", "controls: 400", "best_control: 0.006990622234683363", "real: 0.07140001314178449",
  "real_beats_all_controls: yes", "controls GE real: 0". Equal to null_test.md.
- My independent version (item BLEU from the official scorer's own path: sigtypst2022.load_cognate_file +
  lingrex.util.bleu_score, empty prediction as 2n "Ø" as in compare_words; same draw scheme, one random.Random(20261018 + c)
  per control over P = 0.10 ... 0.50, families in order, sets by first appearance in gold): "controls 400 real
  0.07140001314178449 best_control 0.006990622234683363 controls GE real 0 real_beats_all True"; first controls
  0.0049087234965146335, 0.0013954753413267574, 0.003989243374836882. Passes.
- Note: the tool's own metric (tools/metric_tools.py) differs from compare_words in the last bits of some values (e.g. 0.10
  candidate 0.7183395130131845 vs 0.7183395130131847). This does not matter for a margin of 0.064 between the real d and
  the best control.

## 9. One cell, one metric, one object; not subsumed
- Cell LA only; metric BLEU only; statistic A_BLEU only. CLAIM.md reports the other metrics as the criterion asks and
  claims none of them. Object: one frozen system's 50 test prediction files attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv
  (object/predictions-P.tsv rebuild them: checker "50 of 50").
- The same object is claimed in NA and BA (other metrics) and its 0.40 part in N40, B40, L40. Each of those is a different
  statistic or metric. A win at 0.40 (L40) does not imply the five-proportion aggregate, and earlier single-proportion claims
  were made by other objects. So the LA win is its own pre-registered statistic, not a restatement of another cell.

## 10. Verdict
The result meets the full success criterion in its aggregate form on BLEU:
- the aggregate was stated in PREREG.md (rule 2) before results;
- one frozen system, trained at each P on training-P alone (plus the release's development files) and never reading any
  solutions file, row-isolated and sealed-checked at every P;
- the pinned official scorer reproduces Mockingbird-I1 bit for bit at all five P;
- A_BLEU 0.6729772402356671 strictly beats Mockingbird-I1's 0.6015772270938825 (from its official totals) in both summation
  modes;
- the pre-registered null passes (real 0.0714 vs best control 0.0070).
Caveats (none blocking): the PREREG freeze time and "no gold before selection" are attested, not independently
timestamped; the reranker gate makes the candidate's val number optimistic (disclosed; it cannot touch the test value); the
win does not depend on the development-family rows.

confirmed_scope: The frozen single system classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/code, trained at each proportion P on training-P alone) has test predictions attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv for P = 0.10, 0.20, 0.30, 0.40, 0.50 (rebuilt exactly from object/predictions-P.tsv) that reach an aggregate A_BLEU = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 of the 10-surprise-family mean BLEU of 0.6729772402356671 under the pinned official ST2022 scorer, strictly higher than Mockingbird-I1's A_BLEU of 0.6015772270938825 computed the same way from its official results-surprise-P.json totals (margin 0.0714); this is a win on BLEU only.

pass: true