# PREREG: private-quarry-B (charter Q15), session 2026-10-18-1758, cell BA (aggregate BCFS over the five proportions (higher is better))

THIS FOLDER'S CELL: BA, A_BCFS = mean over P = 0.10, 0.20, 0.30, 0.40, 0.50 of the family-mean BCFS (rule 2). This folder claims only this cell, under rule 12. The body below (everything after this header) is byte-identical to the PREREG body frozen at 2026-10-18T18:11:37Z in runs/2026-10-18-1758, -1809 and -1811 (runs/2026-10-18-1758/out/PREREG_body.md, sha256 2840e8180982bdcb7e95afc583aae1bb397f3262833db88496efab3684a948bf; out/prereg.sha256). Rule 2 said the aggregate folders are created after the three 0.40 gates: this folder was created at the time below, after those gates were written (runs/2026-10-18-1758, -1809, -1811 panel/gate.md), and this copy was written into it then. Copy written 2026-10-18T22:07:31Z (date -u). The lenses of this session ran in runs/2026-10-18-1758/attempts/; the candidate is the one named by runs/2026-10-18-1758/selection.md.

Written by the main session (Opus 5.5, claude-opus-5-5[1m]) of the session started 2026-10-18T17:58:48Z, before any
lens of this session started and before any surprise-test output of this session has been scored. The same text,
apart from its header, is the PREREG of every claim folder of this session (one per cell, table in rule 2). Never
edited after results exist; a changed plan goes in PREREG.v2.md with its own time.

## Why this run, and why this protocol
Charter v4.5 HANDOFF (the human, 2026-10-17 21:40 and 23:43 PDT): proportions 0.40 and 0.50 go to whichever lane is
free first; one proportion per run, all lenses on it; 0.50 first, then 0.40. 0.50 is claimed (runs 2026-10-18-0839,
-0847, -0848). This run took the lock locks/q15-040 at 2026-10-18T17:59:37Z; neither HOMEDIR/v3r1t4s/locks/q15-040
nor WORKDIR/locks/q15-040 existed (the tables lane has no locks folder; it started its own run
2026-10-18-1759 at 17:59:28Z). The human asked for all three metrics (NED, BCFS, BLEU), and, "if the PREREG allows,
the aggregate over all 5 proportions as a separate claim" (charter v4.5 NEXT item 3). Both are pre-registered here for
ONE object before any test scoring of this session.

Clean protocol for 0.40 and for the aggregate. The splits are nested (checked by the main session on the pinned
clone before this PREREG, all 10 surprise families: test-0.30 within test-0.40 within test-0.50; training-0.50
within training-0.40; training-0.40 and training-0.50 share no cognate set with test-0.40). So the only data
disjoint from EVERY surprise test set (P = 0.10 ... 0.50) is training-0.50, validation splits cut from it, and the
development families. Every choice of this session (lens development, stage-2 weights, selection) is made on that
data only (the "val-0.50 regime" of runs 2026-10-18-0202 and 2026-10-18-0839). Every eligible entry and the selected
object are therefore clean at every proportion, and one object can carry the 0.40 cells and the aggregate cells.

Carried entries: the 11 frozen entries of run 2026-10-18-0202 and the 10 of run 2026-10-18-0839, all developed on
val-0.50 only, byte-copied into carry/ with their code tree hashes and val-0.50 result hashes verified against their
binding FROZEN.md records (out/setup.out, SETUP PASS).

Prior test exposure (disclosed; none of it enters any choice below). Earlier main sessions read surprise-test gold to
score other objects: test-0.10, -0.20, -0.30 (runs 2026-10-17-1806, 2026-10-18-0202/0203/0204), test-0.50 (runs
2026-10-18-0839 and its lead scoring), and run 2026-10-17-1806's combiner (tuned on splits that overlap every test
set except test-0.10; its code is not used here) was scored once at 0.40 (mean NED 0.2395703914618492, information in
the dossier). Because the test sets are nested, those scorings touched rows of test-0.40. Single-entry test scores of
the carried entries exist at 0.10-0.30 (run 0202 entries) and 0.50 (all 21). The selection rule below is mechanical,
reads val-0.50 only, and is the rule of runs 0202 and 0839 (extended by one larger combination, COMB-10, fixed now);
the main session applies it without discretion. No test score of any proportion is shown to any lens.

## Criterion (verbatim from data/quarry_definitions/Q15.json, "success_criterion")
A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score.

## Statistic (fixed now)
1. Scorer: the pinned repository's own evaluation code (sigtyp/ST2022 at 03094435cba4293ce0eea383036cab78499ad50d;
   sigtypst2022.compare_words per family; family mean = statistics.mean over the 10 surprise families, as
   compare_systems computes "total"), in the calibrator venv of run 2026-10-16-2026 (bit-identical to the official
   results JSON with left-to-right summation; PROVED-HERE in runs 2026-10-16-2026, 2026-10-17-1806, 2026-10-18-0202
   and 2026-10-18-0839). Every value is computed in both summation modes (left-to-right as in 2022; Python 3.13
   builtin sum).
2. Six cells, one claim per run folder (kit: one cell per claim):

| cell | folder | statistic | Bar (best published value on the official scale) |
|---|---|---|---|
| N40 | runs/2026-10-18-1758 | mean NED at 0.40 (lower is better) | Mockingbird-I1 0.316240240534308 |
| B40 | runs/2026-10-18-1809 | mean BCFS at 0.40 (higher is better) | Mockingbird-I1 0.6428278176401176 |
| L40 | runs/2026-10-18-1811 | mean BLEU at 0.40 (higher is better) | Mockingbird-I1 0.5723601982335171 |
| NA | a run folder created after the 0.40 gates (named by date -u) | aggregate NED A_NED (lower) | Mockingbird-I1 0.2931673956342817 |
| BA | as NA | aggregate BCFS A_BCFS (higher) | Mockingbird-I1 0.6797616040522236 |
| LA | as NA | aggregate BLEU A_BLEU (higher) | Mockingbird-I1 0.6015772270938825 |

   Aggregate statistic (the criterion's "aggregated over all 5 proportions", stated here): A_m = (S_m(0.10) +
   S_m(0.20) + S_m(0.30) + S_m(0.40) + S_m(0.50)) / 5, summed left to right in that order, where S_m(P) is the family
   mean of metric m at P (the official "total"). The object at P is the candidate system's output on test-P (every
   entry trained by the harness on training-P alone, test-P predicted in partitions; stage-2 weights fixed once, rule
   9). Mockingbird-I1's A_m is computed in the same way from its official results-surprise-P.json totals; it is the
   best official system on all three A_m (every official system with all five proportions, computed by the main
   session from the official JSON files before this PREREG: next best A_NED Mockingbird-N1-B 0.314248874788133, A_BCFS Mockingbird-N1-A
   0.6685038317882127, A_BLEU Mockingbird-N1-B 0.5739708839607733). At 0.40 Mockingbird-I1 is the best official system
   on all three metrics (results-surprise-0.40.json). FeVeT (Wientzek 2025) published predictions at 0.10, 0.30 and 0.50
   only, Cognate Transformer (EMNLP 2023) a table at 0.50 only, so neither has a 0.40 value or an aggregate. A better
   published value on the official scale that a NOVELTY skeptic finds before the gate becomes that cell's bar.
   The official README's meta-evaluation table aggregates RANKS (mean rank over proportions and metrics), not scores;
   this PREREG's aggregate is a score aggregate, as the criterion's words "mean score ... aggregated over all 5
   proportions" read. For information only, the report gives the candidate's rank in each official column.
3. Not claimed: proportions 0.10, 0.20, 0.30, 0.50 as single cells (claimed earlier or by other objects), partial wins
   p1-p3. Order (charter v4.5: "the aggregate over all five proportions is claimed only after both lanes report"): the
   aggregate cells are gated only after the three 0.40 gates. The tables lane holds no Q15 proportion (the HANDOFF gave
   0.40 and 0.50 to whichever lane was free first; this lane took both), so once 0.40 is gated every proportion has been
   reported by the lane that held it; the report names this reading for the human. If the session runs out of time,
   the aggregate cells stay a live lead under this PREREG (their object is fixed by rule 10).

## Data rules (binding for every system and every lens of this session)
4. A system at proportion P may read only: training-P.tsv of the 10 surprise families (the harness manifest); the rows
   of test-P.tsv only through tools/q15h.py run, each row predicted from that row's visible cells plus the trained
   model, with no state carried between rows or partitions; the development families (data/view/dev/); generic
   sound-symbol feature tables that contain no word lists. Forbidden: every solutions-*.tsv, cognates.tsv,
   wordlist.tsv, cldf-data/, systems/ and results/ of any family; any other system's predictions; external lexical
   data; pretrained model weights. The lenses' view (data/view/) holds only training-0.40.tsv, test-0.40.tsv and
   training-0.50.tsv of the surprise families plus dev/. The view with every proportion (main_only/view_allp/, files
   byte-identical to the pinned clone) is used only by the main session and its tools subagent, for the aggregate's
   test runs (tools/q15h.py with Q15H_VIEW set).
5. Row isolation: tools/q15h.py run predicts each family's test file in partitions by masked language (no partition
   holds two rows of one cognate set). Every frozen entry runs tools/q15h.py audit in test mode at 0.40 (AUDIT PASS
   required); for the aggregate the main session runs the same audit at every P. Before a claim, the main session
   runs the sealed check (rule 12 iii).
6. Development (clean protocol). A lens develops and makes every choice using only: shared/val/0.50 (train, test,
   solutions; cut from training-0.50 with the organisers' split rule at ratio 0.15; byte-identical to runs
   2026-10-18-0202's and -0839's), data/view/surprise/FAM/training-0.50.tsv (including further validation folds the
   lens cuts from it), the development families, and its own predecessor folders (runs/2026-10-18-0839/attempts/LENS/,
   runs/2026-10-18-0202/attempts/LENS/ and runs/2026-10-18-0104/attempts/LENS/ for a lens of the same name, built
   under val-0.50-only rules), never opening anything in them produced at P below 0.50 or any test output. Lenses
   never open, print or analyse training-0.40.tsv or test-0.40.tsv themselves (the harness passes them to the system;
   training-0.40 holds rows of test-0.50, which the aggregate predicts), never score or inspect test outputs, and never
   read any other run folder, dossiers/, private/, scratch_q15/, scratch_panel/, outbox/, REPORT.md, LOG.md, or other
   lenses' folders of this session.
7. Determinism and size: a frozen entry is deterministic (the lens retrains and re-predicts val 0.50 twice and compares
   the result files byte for byte; the result goes in its REPRODUCE.md), trains in at most 12 min at 0.40 and predicts
   test-0.40 in at most 15 min with --workers 2 on this machine (skeptics and the sealed check retrain it, at every P
   for the aggregate).

## Freeze, stage 2, selection
8. Each lens freezes up to two entries (PRIMARY, SECONDARY) with tools/q15h.py freeze, after a val run at 0.50 and a
   test run at 0.40 (10 families each) and the test-mode audit at 0.40, by 2026-10-18T21:50:00Z (later freezes are not
   eligible; the binding record of a role is its last record written by then). Eligible entries: those frozen in time
   with all 20 result files and AUDIT PASS, plus the 21 carried entries once their test-0.40 runs and test-mode audits
   at 0.40 have finished with AUDIT PASS (run by the main session from their verified code). Entry names: LENS/ROLE for
   this session's lenses, r0202-LENS/ROLE and r0839-LENS/ROLE for carried entries.
9. Stage 2, built by the main session after every lens has returned and before any surprise-test gold is read in this
   session: run 2026-10-17-1806's combine.py logic unchanged (as in tools/stage2.py: per-item minimum-Bayes-risk choice
   under the scorer's item NED, integer weights 0..3 searched exhaustively over all non-zero tuples, ties as in that
   file; every entry in the list supplies candidate strings, weight 0 included). Weights are fit on val-0.50 only:
   the val score is leave-one-family-out (LOFO); the weights used on test are those fit on all 10 val-0.50 families,
   and the SAME weights are applied to the entries' test outputs at every proportion (tools/stage2.py extended only to
   read val at 0.50 and write test at a list of proportions; the per-item logic is unchanged).
   - COMB-6, COMB-8, COMB-10: over the 6, 8, 10 eligible entries with the lowest val-0.50 mean NED.
   Ranking ties: lower val-0.50 mean ED, then earlier freeze time. The entry order given to the combiner (its tie
   rule) is that ranking.
10. Selection, written to selection.md in runs/2026-10-18-1758 (with date -u and the sha256 of every freeze record and
    of every entry's val-0.50 and test-0.40 result files) before any surprise-test gold is read in this session:
    candidate = the lowest val-0.50 mean NED among every eligible single entry (its frozen val-0.50 files) and COMB-6,
    COMB-8, COMB-10 (their LOFO val files). Ties: lower val ED, then singles before combinations, then earlier freeze,
    then COMB-6, COMB-8, COMB-10 in that order. The one candidate carries all six cells (no separate selection per
    metric or per cell).
11. Test scoring after selection.md exists: (a) reproduce Mockingbird-I1's official totals at all five P bit for bit
    with left-to-right summation (else nothing is scored: charter kill criterion 1); (b) score every eligible entry,
    COMB-6, COMB-8 and COMB-10 at 0.40; (c) score the candidate at all five P and compute A_NED, A_BCFS, A_BLEU. All
    numbers are reported; only the candidate can carry a claim.
12. Claim rule, applied in each folder to its own cell only: the folder claims its cell if the candidate meets all of:
    (i) its value on the cell's statistic beats the cell's bar by more than 1e-9 (lower NED; higher BCFS; higher BLEU)
    in both summation modes; (ii) the cell's null test (rule 13) passes; (iii) every entry the candidate reads (for a
    combination: every entry of its list, weight 0 included) passed the harness test-mode audit at each proportion the
    cell uses (0.40 for N40, B40, L40; all five for NA, BA, LA), and the sealed check passes at each such proportion
    for each of them (run by the main session or a tools subagent it starts, never by a lens): each entry retrained from
    its frozen code with a manifest of training-P only while every test file, every gold copy and every earlier output
    is unreadable, then each test partition predicted alone in its own fresh process, byte-identical to the frozen
    predictions; (iv) the cell's REPRODUCE skeptic's retrain-and-predict run (at 0.40; at every P for NA, BA, LA)
    reproduces the predictions the object is built from (or, if training is not bit-deterministic, a value that also
    meets (i)). Otherwise the folder's status is NOTHING and every number is reported.

## Null test
null_test: required
13. Paired permutation null against the bar holder's per-item predictions (Mockingbird-I1's official files,
    systems/mockingbird-i1/surprise/FAM/result-P.tsv of the pinned clone, for all six cells), 400 controls, as in runs
    2026-10-17-1806, 2026-10-18-0202 and 2026-10-18-0839: in control c, for every cognate set (COGID without its "-i"
    suffix) of every family, the two systems' predictions for all rows of that set are swapped with probability 1/2
    (random.Random(20261018 + c); families in the FAMS order, sets in order of first appearance in the gold solutions
    file; for the aggregate one generator per control draws at P = 0.10, 0.20, 0.30, 0.40, 0.50 in that order, each P
    independently). d_c = the cell statistic's advantage of the candidate side over the bar side (NED: bar side minus
    candidate side; BCFS and BLEU: candidate side minus bar side; aggregate cells: the same on A_m), same scorer,
    left-to-right summation; real d = the same difference for the unswapped pair. real_beats_all_controls = yes only if
    d > max_c d_c. N40 uses tools/null_test.py --prop 0.40 --bar mockingbird; B40 and L40 use tools/null_test_metric.py
    with Mockingbird-I1's files as --bar-dir; NA, BA, LA use the aggregate mode of these tools with Mockingbird-I1 at
    every P (adapted before any scoring; the tools read gold and run only after selection.md).

## What is not claimed
14. No claim rests on a lens's own judgement; lenses never see test scores. Single proportions other than 0.40 and the
    partial wins are not claimed. If this session is cut off, a later session resumes these folders under this PREREG
    (deadlines unchanged; an entry frozen after 21:50:00Z stays ineligible).
