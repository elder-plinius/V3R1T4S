# PREREG: private-quarry-B (charter Q15), run 2026-10-18-0202, cell C20

Frozen at 2026-10-18T02:09:41Z (from date -u), before any lens of this session started and before any system of this session has
produced output. Written by the main session (Opus 5.5, claude-opus-5-5[1m]) of the session started
2026-10-18T02:02:48Z. The same text, apart from this header, is the PREREG of three run folders, one per claim cell
(runs/2026-10-18-0202, -0203, -0204). Never edited after results exist; a changed plan goes in PREREG.v2.md with its
own time.

THIS FOLDER'S CELL: C20, proportion 0.20. This folder claims only this cell, under rule 12.
The lenses of this session run in runs/2026-10-18-0202/attempts/; every folder's claim uses their frozen entries.

## Why this protocol (measured before this PREREG; out/val_overlap.txt, copied from run 2026-10-18-0104)
Run 2026-10-17-1806 confirmed one cell (P 0.10, mean NED 0.19710919181751296). Its other cells cannot be claimed
cleanly: its lenses chose their systems on validation splits cut from training-P at every P, and the splits are nested.
The val split cut from training-P lies inside the surprise test set at P + 0.20 (val-0.10: 411 of 556 sets are test
sets at 0.20, all 556 at 0.30). No val split overlaps test-0.10, so the 0.10 claim is unaffected. A cell P is clean
only if every choice was made on data disjoint from test-P: val splits cut from training-P' with P' >= P,
training-P' with P' >= P, and the development families. Run 2026-10-18-0104 pre-registered the same protocol at
01:18Z and was stopped by the setup session after about one hour (no entry frozen, no test file scored, LOG.md);
this run starts it again with its own times and with the cells of charter v4.5's lane split.

## Criterion (verbatim from data/quarry_definitions/Q15.json, "success_criterion")
A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score.

## Statistic (fixed now)
1. Scorer: the pinned repository's own evaluation code (sigtyp/ST2022 at 03094435cba4293ce0eea383036cab78499ad50d;
   sigtypst2022.compare_words per family, family mean = statistics.mean over the 10 surprise families, as
   compare_systems computes "total"), in the calibrator venv of run 2026-10-16-2026 (bit-identical to the official
   results JSON with left-to-right summation; PROVED-HERE in that run and again in run 2026-10-17-1806). Every value
   is computed in both summation modes (left-to-right as in 2022; Python 3.13 builtin sum).
2. Claim metric: mean NED at the cell's proportion. ED, BCFS and BLEU are reported for every cell; no claim is made
   on them.

## Cells, one claim per run folder (charter v4.5: one cell per run folder; lane split of 2026-10-17 18:14 PDT)
| cell | folder | Bar (mean NED; lowest published value on the official scale) |
|---|---|---|
| C20 | runs/2026-10-18-0202 | Mockingbird-I1 0.2648052468982754 (FeVeT published nothing at 0.20) |
| C30 | runs/2026-10-18-0203 | FeVeT 0.2632988364952282 (Mockingbird-I1 0.2898984929868421) |
| C10 | runs/2026-10-18-0204 | our own confirmed 0.19710919181751296 (run 2026-10-17-1806; FeVeT 0.2296925777970808, Mockingbird-I1 0.2431316340782435) |
3. Not claimed in this run: proportions 0.40 and 0.50 (the tables lane's cells under charter v4.5) and the aggregate
   over all five proportions (charter v4.5: only after both lanes report).
4. Bar values are those computed by tools/score_test.py of run 2026-10-17-1806 (resume/out/score_test.out). The test
   scoring of this run recomputes them (rule 11); the recomputed values bind. A lower value on the official scale
   that the NOVELTY skeptic finds before the gate becomes the bar.

## Data rules (binding for every system and every lens of this run)
5. A system at proportion P may read only: data/view/surprise/<fam>/training-P.tsv (this P only) of the 10 surprise
   families; the rows of test-P.tsv only through tools/q15h.py run, each row predicted from that row's visible cells
   plus the trained model, with no state carried between rows; data/view/dev/ (development families); generic
   sound-symbol feature tables that contain no word lists. Forbidden: every solutions-*.tsv, cognates.tsv,
   wordlist.tsv, cldf-data/, systems/ and results/ of any family; surprise files of any other proportion; any other
   system's predictions; external lexical data; pretrained model weights.
6. Row isolation: tools/q15h.py run predicts each family's test file in partitions by masked language (no partition
   holds two rows of one cognate set). Each lens runs tools/q15h.py audit in test mode at P 0.10, 0.20 and 0.30 for
   every frozen entry. Before a claim, the main session runs a sealed check at the claimed P (rule 12 iii).
7. Development (the clean protocol). A lens develops and makes every choice using only: shared/val/0.50 (train, test
   and solutions, cut from training-0.50 with the organisers' split rule at ratio 0.15), the training-0.50 files, the
   development families (data/view/dev), and its own predecessor's folder in run 2026-10-18-0104
   (runs/2026-10-18-0104/attempts/<same lens>/, built under the same rule 7 of that run: development on val-0.50
   only). training-0.50 is disjoint from the surprise test set at every proportion (nested splits;
   out/val_overlap.txt), so these choices touch no test gold at any P. A lens never reads training-P files or val
   splits for P < 0.50 itself; the harness passes them to the lens's system in `run` at that P (training and
   predicting), and the lens never scores or inspects those outputs. Val gold for P < 0.50 is not in the lens-visible
   tree (main_only/, unreadable to lenses). Lenses never read any other folder of any run (the code of run
   2026-10-17-1806 was tuned on splits that overlap test-P for P >= 0.20), dossiers/, private/, scratch_q15/ or any
   copy of the official repository.

## Freeze, stage 2, selection
8. Each lens freezes up to two entries (PRIMARY, SECONDARY) with tools/q15h.py freeze, after val runs at P 0.10, 0.20,
   0.30 and 0.50 and test runs at P 0.10, 0.20 and 0.30 (10 families each) and the test-mode audit at P 0.10, 0.20
   and 0.30, by 2026-10-18T05:45:00Z (later freezes are not eligible).
9. Stage 2, built by the main session after every lens has returned and before any surprise-test gold is read, with
   tools/stage2.py (run 2026-10-17-1806's combine.py logic unchanged, regression-tested byte-identical by run
   2026-10-18-0104: per-item minimum-Bayes-risk choice under the scorer's item NED, integer weights 0..3 searched
   exhaustively, ties as in that file; val score leave-one-family-out, test weights fit on all 10 val families):
   - COMB-NEW: over the K = min(6, number of new entries) new entries with the lowest val-0.50 mean NED (ties: lower
     val-0.50 ED, then earlier freeze); weights fit at each P in {0.10, 0.20, 0.30} on val-P. Eligible at every cell.
   - COMB-ALL10: at P 0.10 only, over the 7 entries with the lowest val-0.10 mean NED among the new entries and run
     2026-10-17-1806's six frozen component entries (its combiner excluded); weights fit on val-0.10. Eligible at C10
     only (the old components are clean for 0.10 only).
10. Selection, written to selection.md in runs/2026-10-18-0202 (with date -u and the sha256 of every freeze record)
    before any surprise-test gold is read (the main session scores val at P < 0.50 with --gold-root
    main_only/val_gold):
    - C20, C30: candidate(P) = the entry with the lowest val-P mean NED among the new entries and COMB-NEW (val-P is
      cut from training-P and is disjoint from test-P). Ties: lower val ED, then earlier freeze.
    - C10: candidate = the lowest val-0.10 mean NED among the new entries, COMB-NEW, COMB-ALL10, run 1806's six
      components and run 1806's combiner (its leave-one-family-out val value 0.21358978758026678). If the candidate
      is run 1806's combiner or one of its components, C10 makes no claim.
11. Test scoring after selection.md exists (tools/score_test.py): (a) reproduce Mockingbird-I1's official totals at
    all five P bit for bit with left-to-right summation (else nothing is scored: charter kill criterion 1); (b)
    rescore FeVeT's published predictions at 0.10, 0.30 and 0.50; (c) score every eligible entry at P 0.10, 0.20,
    0.30. All numbers are reported; only a cell's candidate can carry that cell's claim.
12. Claim rule, applied in each folder to its own cell only: the folder claims its cell if the cell's candidate meets
    all of: (i) mean NED lower than the cell's bar by more than 1e-9 in both summation modes; (ii) the null test of
    rule 13 passes; (iii) every entry with non-zero influence on the candidate passed the harness test-mode audit at
    the cell's P, and the sealed check passes at that P (run by the main session, or by a tools subagent it starts,
    never by a lens): each component retrained from its frozen code with a manifest of training-P only while every
    test file, every other-proportion file, every gold copy and every earlier output is unreadable, then each test
    partition predicted alone in its own fresh process, byte-identical to the frozen predictions (for run 1806's
    components at 0.10 the sealed check of that run, resume/out/sealed_check.log, counts for the components it
    covered); (iv) the REPRODUCE skeptic's retrain-and-predict run reproduces the frozen predictions (or, if training
    is not bit-deterministic, a NED that also meets (i)). Otherwise the folder's status is NOTHING and every number
    is reported. At 0.20 the report also states that FeVeT published no value there.

## Null test
null_test: required
13. Paired permutation null against the bar holder's per-item predictions, 400 controls, as in run 2026-10-17-1806
    rule 13: in control c, for every cognate set (COGID without its "-i" suffix) of every family, the two systems'
    predictions for all rows of that set are swapped with probability 1/2 (random.Random(20261018 + c)); d_c =
    NED(bar side) - NED(candidate side) with the same scorer and left-to-right summation; real d = bar - candidate.
    Bar holder: Mockingbird-I1's official per-item files at 0.20; FeVeT's published files at 0.30; run
    2026-10-17-1806's combiner (its frozen test-0.10 predictions) for C10. real_beats_all_controls = yes only if
    d > max_c d_c.

## What is not claimed
14. Partial wins p1-p3 are not claimed (published systems already meet each at some proportion). BCFS, BLEU and ED
    are reported, not claimed. No claim rests on a lens's own judgement; lenses never see test scores. If this session
    is cut off, a later session resumes these folders under this PREREG (deadlines unchanged).
