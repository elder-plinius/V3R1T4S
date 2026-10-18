(Publication copy of the frozen runs/2026-10-18-0839/PREREG.md, sha256 b738411f40b41b03f302a90d7758ee1f8d58e41c7f96af95bc62c8ff22b1beff, made by the main session at packaging: the angle-bracket path patterns in angle brackets (same lens, lens, ROLE, fam) are written SAME-LENS, LENS, ROLE, FAM so that the kit's placeholder check accepts the file; no other character differs. The original stays unchanged in the run folder.)

# PREREG: private-quarry-B (charter Q15), run 2026-10-18-0839, cell N50 (proportion 0.50, mean NED)

Frozen at 2026-10-18T08:49:14Z (from date -u). THIS FOLDER'S CELL: N50, proportion 0.50, metric mean NED. This folder claims only this cell,
under rule 12. The lenses of this session run in runs/2026-10-18-0839/attempts/; every folder's claim uses their frozen
entries and the carried entries of rule 8.

Written by the main session (Opus 5.5, claude-opus-5-5[1m]) of the session started 2026-10-18T08:39:09Z, before any
lens of this session started and before any surprise-test output of this session has been scored. The same text, apart
from its header, is the PREREG of three run folders, one per claim cell (runs/2026-10-18-0839, -0847, -0848). Never
edited after results exist; a changed plan goes in PREREG.v2.md with its own time.

## Why this run, and why this protocol
Charter v4.5 HANDOFF (the human, 2026-10-17 21:40 and 23:43 PDT): proportions 0.40 and 0.50 go to whichever lane is
free first once this lane's 0.10, 0.20 and 0.30 cells are claimed or closed (they are: runs 2026-10-18-0202/0203/0204);
ONE proportion per run, all lenses on it, 0.50 first. This run took the lock locks/q15-050 at 2026-10-18T08:40:18Z
(neither workspace had a q15-050 lock). The human also asked for all three metrics (NED, BCFS, BLEU); by the lesson of
run 2026-10-18-0202 all three are pre-registered here for the same object before any test scoring.
Clean protocol for 0.50: the splits are nested, so training-P for every P < 0.50 holds the gold of test-0.50. A choice
is clean for 0.50 only if it was made on data disjoint from test-0.50: training-0.50, validation splits cut from
training-0.50, and the development families. Run 2026-10-17-1806's systems were tuned on validation splits cut from
training-0.10 (which overlap test-0.50), so neither their code nor their tuned settings are used here; their methods
reach this run only through run 2026-10-18-0202's lenses, which rebuilt them under a val-0.50-only rule. The 11 frozen
entries of run 2026-10-18-0202 were developed on val-0.50 only and never scored at 0.50 on test: they are eligible
here ("carried entries"), byte-copied with their freeze hashes verified (carry/carry_entries.json,
out/carry_setup.out).

## Criterion (verbatim from data/quarry_definitions/Q15.json, "success_criterion")
A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score.

## Statistic (fixed now)
1. Scorer: the pinned repository's own evaluation code (sigtyp/ST2022 at 03094435cba4293ce0eea383036cab78499ad50d;
   sigtypst2022.compare_words per family, family mean = statistics.mean over the 10 surprise families, as
   compare_systems computes "total"), in the calibrator venv of run 2026-10-16-2026 (bit-identical to the official
   results JSON with left-to-right summation; PROVED-HERE in runs 2026-10-16-2026, 2026-10-17-1806 and 2026-10-18-0202).
   Every value is computed in both summation modes (left-to-right as in 2022; Python 3.13 builtin sum).
2. Declared proportion: 0.50 only. Three cells, one claim per run folder (kit: one cell per claim):

| cell | folder | metric | Bar (best published value on the official scale at 0.50) | Mockingbird-I1 (official) |
|---|---|---|---|---|
| N50 | runs/2026-10-18-0839 | mean NED (lower is better) | FeVeT 0.30880111347517586 | 0.35176136367373956 |
| B50 | runs/2026-10-18-0847 | mean BCFS (higher is better) | FeVeT 0.6423935720824072 | 0.6050308536957327 |
| L50 | runs/2026-10-18-0848 | mean BLEU (higher is better) | FeVeT 0.5768215755932388 | 0.5337187296541888 |

   Bar values are those computed by run 2026-10-18-0202's tools/score_test.py (out/score_test.json there; FeVeT =
   Wientzek 2025's published per-item predictions, github.com/TGH-2020/FeVeT at 31898c53, rescored with the pinned
   scorer). This run's test scoring recomputes them (rule 11); the recomputed values bind. A better published value on
   the official scale that a NOVELTY skeptic finds before the gate becomes the bar.
3. Not claimed: proportions 0.10-0.40, the aggregate over five proportions (charter: only after both lanes report;
   0.40 is still open), partial wins p1-p3. For information only (not a bar, not published): run 2026-10-17-1806's
   combiner, tuned on splits that overlap test-0.50, scored 0.50 test NED 0.25280432863134955, BCFS
   0.7073347646123574, BLEU 0.6451264483943195 (run 2026-10-18-0202 out/score_test.json); the report compares with it.

## Data rules (binding for every system and every lens of this run)
4. A system at 0.50 may read only: data/view/surprise/FAM/training-0.50.tsv of the 10 surprise families (the
   harness manifest); the rows of test-0.50.tsv only through tools/q15h.py run, each row predicted from that row's
   visible cells plus the trained model, with no state carried between rows or partitions; data/view/dev/
   (development families); generic sound-symbol feature tables that contain no word lists. Forbidden: every
   solutions-*.tsv, cognates.tsv, wordlist.tsv, cldf-data/, systems/ and results/ of any family; surprise files of
   any other proportion (this run's data/view holds only the 0.50 files of the surprise families); any other
   system's predictions; external lexical data; pretrained model weights.
5. Row isolation: tools/q15h.py run predicts each family's test file in partitions by masked language (no partition
   holds two rows of one cognate set). Every frozen entry runs tools/q15h.py audit in test mode at 0.50 (AUDIT PASS
   required). Before a claim, the main session runs the sealed check at 0.50 (rule 12 iii).
6. Development (clean protocol). A lens develops and makes every choice using only: shared/val/0.50 (train, test,
   solutions; cut from training-0.50 with the organisers' split rule at ratio 0.15; byte-identical to run
   2026-10-18-0202's), the training-0.50 files (including any further validation folds the lens cuts from them), the
   development families, and its own predecessor folders (runs/2026-10-18-0202/attempts/SAME-LENS/ and
   runs/2026-10-18-0104/attempts/SAME-LENS/, built under val-0.50-only rules), never opening anything in them that
   was produced at P < 0.50. Lenses never open, print or analyse test-0.50.tsv themselves (the harness passes its
   partitions to the system), never score or inspect test outputs, and never read any other run folder (in
   particular run 2026-10-17-1806), dossiers/, private/, scratch_q15/, outbox/, or other lenses' folders.
7. Determinism and size: a frozen entry is deterministic (the lens retrains and re-predicts val 0.50 twice and
   compares the result files byte for byte; the result goes in its REPRODUCE.md), trains in at most 10 min at 0.50 and
   predicts test-0.50 in at most 15 min with --workers 2 on this machine (skeptics and the sealed check retrain it).

## Freeze, stage 2, selection
8. Each lens freezes up to two entries (PRIMARY, SECONDARY) with tools/q15h.py freeze, after val and test runs at
   0.50 (10 families each) and the test-mode audit at 0.50, by 2026-10-18T12:40:00Z (later freezes are not eligible).
   Eligible entries: those frozen in time with all 20 result files and AUDIT PASS, plus the 11 carried entries once
   their test-0.50 runs (carry/LENS-ROLE/test/0.50/) and test-mode audits at 0.50 have finished with AUDIT PASS
   (run by the main session; code verified against the 0202 freeze hashes). Entry names: LENS/ROLE for this
   run's lenses, r0202-LENS/ROLE for carried entries.
9. Stage 2, built by the main session after every lens has returned and before any surprise-test gold is read, with
   tools/stage2.py at P 0.50 (run 2026-10-17-1806's combine.py logic unchanged: per-item minimum-Bayes-risk choice
   under the scorer's item NED, integer weights 0..3 searched exhaustively, ties as in that file; every entry in the
   list supplies candidate strings, weight 0 included; val score leave-one-family-out (LOFO), test weights fit on
   all 10 val families):
   - COMB-6: over the 6 eligible entries with the lowest val-0.50 mean NED;
   - COMB-8: over the 8 eligible entries with the lowest val-0.50 mean NED.
   Ranking ties: lower val-0.50 mean ED, then earlier freeze time. The entry order given to tools/stage2.py (its tie
   rule) is that ranking.
10. Selection, written to selection.md in runs/2026-10-18-0839 (with date -u and the sha256 of every freeze record and
    of every entry's val and test result files) before any surprise-test gold is read: candidate = the lowest
    val-0.50 mean NED among every eligible single entry (its frozen val-0.50 files), COMB-6 and COMB-8 (their LOFO val
    files). Ties: lower val ED, then singles before combinations, then earlier freeze, then COMB-6 before COMB-8. The
    one candidate carries all three cells N50, B50 and L50 (no separate selection per metric).
11. Test scoring after selection.md exists (tools/score_test.py): (a) reproduce Mockingbird-I1's official totals at
    all five P bit for bit with left-to-right summation (else nothing is scored: charter kill criterion 1); (b)
    rescore FeVeT's published predictions at 0.50 (and 0.10, 0.30); (c) score every eligible entry, COMB-6 and COMB-8
    at 0.50. All numbers are reported; only the candidate can carry a claim.
12. Claim rule, applied in each folder to its own cell only: the folder claims its cell if the candidate meets all of:
    (i) its mean on the cell's metric beats the cell's bar by more than 1e-9 (lower NED; higher BCFS; higher BLEU) in
    both summation modes; (ii) the cell's null test (rule 13) passes; (iii) every entry the candidate reads (for a
    combination: every entry of its list, weight 0 included) passed the harness test-mode audit at 0.50, and the
    sealed check passes at 0.50 for each of them (run by the main session or a tools subagent it starts, never by a
    lens): each entry retrained from its frozen code with a manifest of training-0.50 only while every test file,
    every gold copy and every earlier output is unreadable, then each test partition predicted alone in its own fresh
    process, byte-identical to the frozen predictions; (iv) the cell's REPRODUCE skeptic's retrain-and-predict run
    reproduces the frozen predictions (or, if training is not bit-deterministic, a value that also meets (i)).
    Otherwise the folder's status is NOTHING and every number is reported.

## Null test
null_test: required
13. Paired permutation null against the bar holder's per-item predictions (FeVeT's published 0.50 files for all three
    cells), 400 controls, as in runs 2026-10-17-1806 and 2026-10-18-0202: in control c, for every cognate set (COGID
    without its "-i" suffix) of every family, the two systems' predictions for all rows of that set are swapped with
    probability 1/2 (random.Random(20261018 + c)); d_c = the cell metric's advantage of the candidate side over the
    bar side (NED: bar side minus candidate side; BCFS and BLEU: candidate side minus bar side), same scorer,
    left-to-right summation; real d = the same difference for the unswapped pair. real_beats_all_controls = yes only
    if d > max_c d_c. N50 uses tools/null_test.py; B50 and L50 use tools/null_test_metric.py (stdlib metric code
    validated bit for bit against compare_words in run 2026-10-18-0202).

## What is not claimed
14. No claim rests on a lens's own judgement; lenses never see test scores. Proportions other than 0.50, the
    aggregate and the partial wins are not claimed. If this session is cut off, a later session resumes these folders
    under this PREREG (deadlines unchanged; an entry frozen after 12:40:00Z stays ineligible).
