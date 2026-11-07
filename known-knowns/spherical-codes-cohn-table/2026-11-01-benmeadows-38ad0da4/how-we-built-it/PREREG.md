# PREREG: spherical-codes-cohn-table, (d, N) = (31, 64)

written_utc: 2026-11-01T14:36Z (trimmed to this cell on 2026-11-06; no criterion, threshold or margin changed)

## Timing, stated plainly

This file was written after the search (2026-11-01, about 05:04 to 08:50 UTC) and after a first panel (13:47Z to about
14:00Z) that did not pass the cell. The object is unchanged since then (same file, same sha256). It is not a
pre-registration in the strict sense: it freezes the judging, not the search. The criterion below is quoted from the
public bank, `bank/targets.json` at https://github.com/elder-plinius/V3R1T4S commit
f3b19b475065f35d0a7f93e8a6078c9b2f12566e (committed 2026-10-30T03:12:11-07:00). No threshold or margin was chosen by
us; every number below is the bank's.

## Criterion: spherical-codes-cohn-table

Quoted verbatim from the bank:

> Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Cell: (d, N) = (31, 64).

## Evidence available to the panel

We fetched these pages on 2026-11-01 at 14:32Z; URLs and sha256 values are in `the-record-we-beat/RECORD.md`:
https://spherical-codes.org/plain, the https://spherical-codes.org/ index row for (31, 64), and two arXiv API searches
(newest 15 for "spherical code" and for "Tammes").

## Statistic, thresholds, null design

- c* as defined; pass iff table - c* >= 1e-10, coordinates >= 20 digits, no star, no 'needs more optimization' text,
  no newer arXiv result for (31, 64), not in the kissing range.
- Null test: not applicable. This is a deterministic construction checked against a definition, not a search or
  statistical claim.

## Starting points

The search started from random, cross-polytope and two-simplex seeds; no posted code was used (see
`HOW_WE_FOUND_IT.md`).

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), new subagents; none sees the search code or our checker.
The cell is dropped unless all three write `pass: true`. Their verdicts are in `panel/`.
