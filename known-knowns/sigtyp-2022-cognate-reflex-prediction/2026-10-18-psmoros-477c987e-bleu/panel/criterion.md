(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the L40 CRITERION skeptic subagent (Opus 5.5, model opus, agent aa18b932c49ce264e) could not write a file named like a report. Text verbatim below.)

# Panel: CRITERION skeptic, cell L40 (proportion 0.40, mean BLEU), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics: REPRODUCE, NOVELTY, CRITERION)
start: Sun Oct 18 21:39:53 UTC 2026 (date -u)
end: Sun Oct 18 22:02:45 UTC 2026 (date -u)

Material read: the claim package (claim/, starting with CLAIM.md and definition/Q15.json), kit/RULES.md and
TROPHY_CASE.md. Nothing else in the workspace was opened. Interpreters: SYS (the entry's ML venv), SCO (the venv with
the official scorer module, used only as an interpreter), PY313 (a plain Python 3.13). All scratch work went to a scratch folder
next to claim/ (written SCRATCH below). One slip, disclosed: one shell command briefly created an empty temporary file in the system temp folder and deleted it in the same command; nothing was read from it.
Network: none. This panel made no web or API requests, so nothing was added to any stop list (kit rule 5 not
triggered).

## The criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Partial wins listed in the definition: p1 (beat the LingRex baseline on all three metrics), p2 (beat Mockingbird-I1 on
1 or more surprise families on NED), p3 (beat Mockingbird-I1 on exactly one of the three means). The claim is for the full
criterion on mean BLEU at 0.40, not a partial win.

## Checks run (real output copied; absolute paths shortened to claim-relative or SCRATCH)

### C1. Package integrity and the frozen object
Command: shasum -a 256 -c MANIFEST.sha256 (every line OK; nothing printed by grep -v OK), and shasum of the frozen files.
- "manifest lines: 167"; files in the package other than MANIFEST.sha256: 167; failed lines: none.
- code/config.json 225856a472703e1e82fbd79bbd2aedd18b19359170fd28a7fecb1f6461a9f109, code/system.py
  8482ef52c4e41beb4a67da8fc5524263f58945fbf8a093644b783b43656030ca, and all 10 test/0.40 and 10 val/0.50 result files
  equal the ROLE=PRIMARY record in attempts/classifier/FROZEN.md (frozen 2026-10-18T19:14:05Z) and the hashes listed in
  rules/selection.md (e.g. test/0.40/hillburmish ea8df80b485f7ec04571209f092bb363bcff9cdab7f2ebb59c1047f515016123).
- checker/frozen_result_sha256.txt equals the FROZEN.md test-0.40 hashes ("checker frozen hashes == FROZEN.md PRIMARY test-0.40 hashes").

### C2. Headline recomputed independently (my own script, SCRATCH/scripts/myscore.py)
It imports official/src/sigtypst2022.py from the claim (SCO's lingpy/lingrex), runs compare_words per family against
official/data-surprise/FAM/solutions-0.40.tsv, takes statistics.mean over the 10 families (as compare_systems computes
"total"), in both summation modes. Output:
- ltr Mockingbird-I1 recomputed total [ED,NED,BCFS,BLEU]: ['1.272493550651723', '0.316240240534308', '0.6428278176401176', '0.5723601982335171'] (equal to results-surprise-0.40.json "Mockingbird-I1" "total": [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171])
- builtin Mockingbird-I1 recomputed total: ['1.272493550651723', '0.316240240534308', '0.6428278176401175', '0.5723601982335171']
- ltr classifier/PRIMARY total [ED,NED,BCFS,BLEU]: ['1.0267686117591617', '0.2455448938803044', '0.7136377968288752', '0.6533966833715619']
- builtin classifier/PRIMARY total: ['1.0267686117591617', '0.24554489388030437', '0.7136377968288752', '0.6533966833715619']
- BLEU margin vs bar 0.5723601982335171: 0.08103648513804473 (ltr), 0.08103648513804473 (builtin)
- per family, ltr (candidate BLEU / Mockingbird-I1 BLEU / difference): bantubvd 0.5832800617998198 / 0.5661977163086089 / +0.0171;
  beidazihui 0.8353130901381886 / 0.814750835504507 / +0.0206; birchallchapacuran 0.5614710409078928 / 0.411928039696805 / +0.1495;
  bodtkhobwa 0.822466684196625 / 0.7365117535911341 / +0.0860; bremerberta 0.6260984947459621 / 0.5826607550447371 / +0.0434;
  deepadungpalaung 0.715949620314872 / 0.4809877707436378 / +0.2350; hillburmish 0.6005714430070029 / 0.518665599693807 / +0.0819;
  kesslersignificance 0.22073285723213143 / 0.1459434175761906 / +0.0748; luangthongkumkaren 0.8622149525906906 / 0.8158542903399361 / +0.0464;
  wangbai 0.7058685887824336 / 0.6501018038358075 / +0.0558. Families where the candidate is higher: 10 of 10.
Mockingbird-I1 is the highest official BLEU total at 0.40 in results-surprise-0.40.json (next: Mockingbird-N1-B 0.5466088108887145).

### C3. The claim's own scoring tool (REPRODUCE.md step 2)
Command: STUB_MPL=1 SCO -I tools/score_test_040.py --entries E.json --calib-props 0.40 --json OUT.json (rc=0). Lines:
- "ltr 0.40 Mockingbird-I1 NED 0.316240240534308 official 0.316240240534308 total EXACT families EXACT"
- "ltr 0.40 classifier/PRIMARY ED 1.026769 NED 0.2455448938803044 BCFS 0.7136377968288752 BLEU 0.6533966833715619"
- "BAR L40 Mockingbird-I1 official 0.40 BLEU 0.5723601982335171 PREREG 0.5723601982335171: EQUAL"
- "L40 classifier/PRIMARY | ltr: 0.6533966833715619 bar 0.5723601982335171 margin 0.081036485138 [arrow] MEETS (i) ... | builtin: 0.6533966833715619 bar 0.5723601982335171 margin 0.081036485138 [arrow] MEETS (i) ... | both modes: MEETS (i)"
- same tool, other metrics (information): N40 margin 0.070695346654, B40 margin 0.070809979189, both modes MEETS (i).

### C4. Standalone checker
Command: PY313 -I checker/check_q15.py . object/predictions-0.40.tsv. Output:
"1. Mockingbird-I1 mean BLEU recomputed 0.5723601982335171, official 0.5723601982335171: EXACT" /
"3. object mean BLEU 0.6533966833715619 over 14992 items (claimed 0.6533966833715619): EQUAL" /
"margin vs Mockingbird-I1 0.081036485138 (higher is better)" / "4. rebuilt official-format files equal to the frozen ones: 10 of 10" / "PASS".

### C5. Null test (rules/null_test.md, PREREG rule 13)
(a) The claim's tool, rerun: SCO -I tools/null_test_metric.py --metric bleu --gold-dir official/data-surprise --cand-dir
attempts/classifier/frozen/PRIMARY/test/0.40 --bar-dir official/systems/mockingbird-i1/surprise --prop 0.40 --out NULL.json:
"controls: 400", "best_control: 0.013304732573755529", "real: 0.08103648513804473", "real_beats_all_controls: yes",
controls at or above real: 0. Identical to the numbers in rules/null_test.md.
(b) My own implementation (SCRATCH/scripts/mynull.py: per-item BLEU from the pinned scorer's own bleu_score and
load_cognate_file, the same swap design: one random.Random(20261018 + c) per control, families in the fixed order, sets
in first-appearance order of the gold file, swap if draw below 0.5): "real d 0.08103648513804473"; "controls 400; max
control d 0.01330473257375564; min -0.014076342458233637; mean 0.0002188822815988678; controls at or above real: 0;
real_beats_all_controls: yes". Real d is about 6 times the largest control.

### C6. Gold isolation: what the data looks like and what the system can read
(a) SCRATCH/scripts/datacheck.py (PY313): for every family, data/view/surprise training-0.40 and test-0.40 are
byte-identical to official/data-surprise; training-0.40 and test-0.40 share no cognate set (overlap 0 in all 10); and
"total gold items 14992 found verbatim in a sibling test row 14992". So every answer IS in the masked test file, and
row isolation is essential.
(b) Code audit of attempts/classifier/frozen/PRIMARY/code/system.py: train reads config.json, the manifest, the
manifest's surprise training files and (devx) dev_dir/mannburmish/training-0.10.tsv and
dev_dir/listsamplesize/training-0.10.tsv; predict reads opts.json, model-FAM.pkl and the partition files of --jobs,
and calls predict_row once per row. No listdir/glob/walk, no network, no solutions path. The only non-ASCII tables are
generic sound classes (vowel set, consonant classes, tone characters); no word lists.
(c) Sealed check rerun by me (tools/sealed_check.py, strict profiles, --jobs 2, my own work root):
"SEALED 0.40 classifier__PRIMARY train ok 273s (sandboxed, strict profile)"; for all 10 families "ok ... items identical
N/N bytes IDENTICAL" (bantubvd 699/699, beidazihui 3933/3933, birchallchapacuran 584/584, bodtkhobwa 2856/2856,
bremerberta 306/306, deepadungpalaung 1218/1218, hillburmish 1405/1405, kesslersignificance 311/311,
luangthongkumkaren 1178/1178, wangbai 2502/2502); "predict: 99 sealed processes, 87s"; "SEALED_CHECK 0.40 PASS".
The training sandbox input held only the 10 surprise training-0.40.tsv files and the dev view (training-0.10 and
test-0.10 of the 10 development families; no solutions file). Each partition was predicted alone in its own process
that could read only code, model and its own partition. This matches the main session's log rules/sealed_cand_0.40.log
("SEALED_CHECK 0.40 PASS", 10 of 10 bytes IDENTICAL).
(d) Probe of the generated training profile (SYS under sandbox-exec -f train.sb): "DENIED
claim/official/data-surprise/hillburmish/solutions-0.40.tsv PermissionError", "DENIED
claim/data/view/surprise/hillburmish/test-0.40.tsv PermissionError", "READABLE .../input/surprise/hillburmish/training-0.40.tsv".
(e) attempts/classifier/frozen/PRIMARY/audit_test_0.40.txt: 40 "identical" lines, last line "AUDIT PASS".

### C7. Development data never touches test-0.40 (val-0.50 regime)
SCRATCH/scripts/valcheck.py: for all 10 families the shared/val/0.50 cognate sets (train, test, solutions) are a
subset of training-0.40 and overlap test-0.40 in 0 sets ("total val/test-0.40 overlap 0"). Candidate val-0.50 mean from
its frozen val files with the pinned scorer: ['1.1139670176922158', '0.26631878067630127', '0.8356251509060453',
'0.6194739711457914'] (ED, NED, BCFS, BLEU), equal to the rule-10 table of rules/selection.md (val NED 0.26631878067630127).

### C8. Disclosure 1 (development-family rows): does the win depend on them?
I retrained the entry with "devx" removed from config.json (everything else unchanged; harness tools/q15h.py, SYS,
test 0.40, all 10 families predicted):
- "test 0.40 train rc=0 254s"; all 10 families "ok".
- compared with the frozen files: 9 families byte-identical (including hillburmish: its devx applies only to targets
  with fewer than max_nref = 30 training reflexes, and at 0.40 none qualifies, so the mannburmish rows are not used at
  0.40); only kesslersignificance differs.
- official scorer: "ltr no-devx variant: kesslersignificance BLEU 0.19020570642542908; mean BLEU 0.6503439682908917;
  margin vs bar 0.07798377005737456"; builtin: mean BLEU 0.6503439682908916, margin 0.07798377005737445.
So without any development-family row the same system still beats the bar by 0.078. The disclosed rows are worth
+0.0030 of the mean (kesslersignificance only) and do not carry the win.

### C9. Disclosure 2 (reranker gate written after validation numbers were seen): does the win depend on it?
I re-predicted with the gate removed (rr.skip set to the empty list; the skip list is read only at predict time, so
only bantubvd, beidazihui and kesslersignificance change; the other 7 families were taken from the frozen files):
"ltr ungated-reranker variant: kesslersignificance BLEU 0.24250698126774192; mean BLEU 0.6617644457641102; margin vs
bar 0.08940424753059306" (builtin 0.6617644457641101). The gate LOWERS the test BLEU (0.6534 gated vs 0.6618
ungated): the gate was not tuned toward test-0.40 BLEU, which fits its stated validation/fold origin, and the win
does not depend on it.

### C10. Robustness bound
With Mockingbird-I1's own official predictions put in place of the candidate's for hillburmish and kesslersignificance
(the two families with disclosed development rows), the mean BLEU is 0.6377271550746482 (margin 0.06536695684113103).

### C11. Timeline (as recorded in the files; not checkable from file times, which are copy times of the package)
PREREG.md frozen 2026-10-18T18:11:37Z (says: before any lens started, before any test scoring of the session) and fixes
cell L40 = mean BLEU at 0.40, bar Mockingbird-I1 0.5723601982335171, the selection rule (rule 10), the claim rule (rule
12) and the null design (rule 13). classifier/PRIMARY frozen 19:14:05Z (before the 21:50:00Z deadline). Lenses
returned by 21:10:30Z; selection.md written 21:16:09Z "before any surprise-test gold has been read in this session";
null test 21:17:52Z-21:18:14Z; sealed check 21:35:35Z-21:38:33Z. The order is consistent with the PREREG.
Note: selection.md hashes "PREREG.md" as 254f8e51a592ea6cf2e59215d7219b1ab47df443308a7bc172f7a1173db2761b, while
claim/rules/PREREG.md (the L40 copy, own header) hashes 34682a4f99b3cf09fc6c6bd9cd0eddba1a0fa7e9958e777932d11b5b2d91a703;
the PREREG says every folder holds the same body under its own header, so a different hash is expected, but the
body identity cannot be checked from this package.

### C12. Status source and pinned commit
scout/st2022_repo_page.html sha256 fec88fad967728c78c42ddd0b95a19a6bb6be63f7e8c9b4fd6ef77d314cc1012 (as in scout.md);
it embeds currentOid "03094435cba4293ce0eea383036cab78499ad50d" (2 hits), the commit PREREG rule 1 pins. The scorer
copy official/src/sigtypst2022.py (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a) reproduces
every Mockingbird-I1 0.40 total bit for bit (C2, C3, C4); official/setup.py maps the CLI "st2022=sigtypst2022:main",
whose compare_systems computes "total" as statistics.mean of compare_words over the families, the procedure used here.

## Judgement

1. "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)". Met, in letter and spirit.
   The sandboxed retrain (C6c, C6d) shows the system can be trained with nothing readable but the 10 surprise
   training-0.40.tsv files and the development view (training-0.10/test-0.10 of the development families; no
   solutions file of any family), and each test partition predicted alone reproduces all 14992 frozen predictions
   byte for byte. Every masked answer sits in a sibling row (C6a), but no partition holds two rows of one cognate set
   and every partition ran in its own sandboxed process, so the sibling rows could not be used. No other proportion's
   test file or gold was read: the development choices used val-0.50, cut from training-0.50, which lies inside
   training-0.40 and shares no set with test-0.40 (C7). The development-family files the entry reads are
   training-0.10.tsv files of the task release: they match the literal glob "training-*.tsv" and are not solutions.
   They are a stretch of the spirit (another dataset's forms for kesslersignificance's English/German/French). The
   ablation (C8) settles it: without them the same system scores 0.6503439682908917 and still beats the bar. At 0.40
   the mannburmish rows are not even used.
2. "mean score over the 10 surprise families at a declared proportion". Met. 0.40 and BLEU are declared in PREREG.md
   (18:11:37Z), before selection.md (21:16:09Z) and null_test.md (21:17:52Z). All 10 families are present with one
   prediction per gold item (14992 items; checker). The mean is statistics.mean over the 10 families, as the official
   compare_systems computes it.
3. "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric". Met. BLEU
   0.6533966833715619 against the official 0.5723601982335171 (read from results-surprise-0.40.json and reproduced bit
   for bit from Mockingbird-I1's own files). The margin is 0.08103648513804473 in both summation modes. That is far
   above the PREREG 1e-9 threshold and about 6 times the largest of 400 paired-permutation controls (C5).
4. "Report all three; a win on one metric is a win on that metric only". Met. CLAIM.md reports ED, NED, BCFS and BLEU
   and claims only BLEU. Hidden quantifier checked: partial win p3 ("exactly one" metric) could suggest a stricter
   full-win reading needing more than one metric. That reading is satisfied too: the same object beats Mockingbird-I1
   at 0.40 on all three means (NED margin 0.070695346654, BCFS margin 0.070809979189, BLEU margin 0.081036485138; C3).
   This cell still claims BLEU only.
5. "The repo scorer st2022 at a pinned commit computes the score". Met (C12). The value comes from the pinned module's
   compare_words plus the compare_systems mean, not the CLI wrapper itself. This is the same computation, and it is
   proved by the bit-exact reproduction of the official values.
6. Selection (PREREG rule 10 as written). Followed. The rule takes the lowest val-0.50 mean NED among eligible singles
   (their frozen val files) and COMB-6, COMB-8 and COMB-10 (LOFO). classifier/PRIMARY has 0.26631878067630127, which I
   recomputed from its frozen val files (C7). The next values listed are broker/PRIMARY 0.2692807965192631 and COMB-6
   0.2707859930173011, so there is no tie. One candidate carries every cell, and selection.md predates every
   gold-reading step. The gate disclosure does not break rule 10. Rule 6 lets a lens make every choice on
   shared/val/0.50, and rule 10 compares the frozen val numbers without asking singles for held-out val. So the
   asymmetry with the LOFO-scored combinations is in the PREREG as written, not a deviation from it. In spirit,
   val optimism can only change WHICH entry is picked; it cannot inflate that entry's test score, because val-0.50 and
   test-0.40 are disjoint (C7). Without the gate, broker/PRIMARY (val 0.2693) would have been picked over the ungated
   0.2722, so the gate did decide the selection. But the gate does not help on test (C9: ungated 0.6618 against gated
   0.6534), and the claimed object is the gated entry exactly as frozen.
7. One cell, one metric, one object. Met. Cell L40 (mean BLEU at 0.40) only. The object is
   attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (object/predictions-0.40.tsv holds the same
   predictions; checker step 4). The sibling cells N40 and B40 claim the same object on NED and BCFS. Under the
   criterion's "a win on one metric is a win on that metric only" these are separate wins, and this file confirms only
   BLEU. TROPHY_CASE.md has no Q15/SIGTYP row, so nothing subsumes this cell there. A better published 0.40 BLEU value
   is the NOVELTY skeptic's question; the criterion's literal bar is Mockingbird-I1's official score.

Residual items, not blocking: (a) the PREREG, freeze and selection times are self-reported (C11). (b) Lens-side
discipline (lenses never seeing test scores; rule 6) cannot be audited from the package. The system-level evidence
(sealed retrain, val/test disjointness, the gate hurting test BLEU) shows no sign of test leakage into the object.
(c) Prior test exposure in earlier sessions is disclosed in the PREREG; the selection rule was mechanical and fixed
before any lens started.

## Verdict
The claimed object meets the full success criterion, literally, on mean BLEU at the declared proportion 0.40. It is a
genuine win, not subsumed and not a partial win. Neither disclosed issue carries the result: development rows give
0.6503 without them, and the reranker gate gives 0.6618 without it, both above the bar 0.5724.

confirmed_scope: At proportion 0.40, the predictions of the frozen single system classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv, identical to object/predictions-0.40.tsv), made for the masked rows of the 10 SIGTYP 2022 surprise families from training-0.40 and development-family training files only, have mean BLEU 0.6533966833715619 under the pinned ST2022 scorer (commit 03094435, both summation modes), strictly higher than Mockingbird-I1's official 0.5723601982335171 from results-surprise-0.40.json, by 0.08103648513804473; this is a win on mean BLEU at 0.40 only.

pass: true