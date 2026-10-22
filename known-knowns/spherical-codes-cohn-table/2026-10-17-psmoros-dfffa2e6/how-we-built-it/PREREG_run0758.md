# PREREG: hunting run 2026-10-16-0758, spherical-codes-cohn-table (frozen 2026-10-16T08:15:57Z, from date -u)

Frozen before any lens has run and before any result exists.

## Criterion
The bank success criterion is copied verbatim in target.md. This run makes no V3R1T4S claim (charter Q3 "next"). It
produces an upload ledger, under the charter's rule: "verify each with the run's checker of record (all pairs, >= 20
digits per coordinate, gain >= 1e-10 against a fresh /plain)". robots.txt disallows /plain for our User-Agent (see
scout.md), so "fresh /plain" is replaced by the fresh HTML index "/", which robots.txt allows. The index's cosines
equal /plain's on every common row (08:02Z snapshot).

## Statistic
c* = the maximum pairwise inner product after normalising each vector in mpmath at 50 digits. It is computed by the
checker of record, code/sc_check.py: a float64 screen (1e-7), then mpmath on every screened pair, with the
finiteness and magnitude guards. Input is the file exactly as written to the ledger. gain = table cosine (12
decimals, from the fresh index fetched by the main session after the last lens finishes) minus c*.

## A row enters uploads/cohn-ledger/ only if ALL of these hold (thresholds frozen here)
1. The file has N lines of d numbers each, and every coordinate has >= 20 significant digits.
2. The row is on the fresh index, unstarred, and also in the 08:02Z /plain snapshot (the human's upload script needs
   a /plain row; index-only rows are listed in the dossier instead).
3. gain >= 1e-9. This is stricter than the charter's 1e-10, so the upload script, which uses a float64 margin of
   1e-9, accepts every ledger row. Rows with 1e-10 <= gain < 1e-9 go to the dossier, not the ledger.
4. The row is not one of the eight taken rows (29,114), (30,74), (29,72), (28,70), (30,117), (29,145), (26,232),
   (27,68), and not in uploads/hold.txt.
5. No kissing territory: not (9 <= d <= 23 and c* <= 0.5).
6. For a row the table already shows with our code: gain >= 1e-6 (charter: "do not re-polish rows we already hold
   unless the gain is at least 1e-6").
7. An independent checker, written in a fresh context by a different model (fable) from the definition alone,
   reproduces c* within 1e-14 and the same pass/fail on 1-6.
8. One file per row: the lowest-c* code over all lenses.

## Count for LOG.md
The LOG line ends with "rows verified for upload: N". N = the number of ledger rows written by this run whose
(d, N, sha256) is not already in uploads/uploaded.tsv (the charter's "new rows only").

## Null design
null_test: not needed because each ledger row is an explicit object (coordinates), checked by a deterministic exact
checker against a table value. Nothing is a search statistic or a "beats chance" claim.

## Sanity controls (frozen)
- Optimizer control: each lens that polishes runs its exact pipeline, at its production cap, on at least 10 of the
  28 cached starred codes (data/seeds/, class star). A starred row "improved" by >= 1e-10 under the checker of
  record means a bug. That lens's results stay out of the ledger until the bug is found and fixed, and the report
  says so.
- Checker control: out/checker_calibration.jsonl. Posted codes reproduce the table within 1e-12; malformed and
  perturbed inputs fail.
