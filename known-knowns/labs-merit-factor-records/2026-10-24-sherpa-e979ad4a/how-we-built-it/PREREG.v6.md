# Pre-registration v6 — the other named-table lengths in reach: L = 381 and L = 449

Sealed 2026-10-24T19:02:19Z (from `date -u`), before any search output at L = 381 or L = 449 exists in this session.

## Why these two

The pass-1 CRITERION ruling: only lengths that a named table lists can meet the criterion as written. The Bošković et al.
archive (borkob/git_labs, `results-2018/2018-labs-skew.txt`, one of the bank's named sources) lists, between 351 and 449,
only L = 381 (E = 10238) and L = 449 (E = 15456), plus L = 401, already handled under PREREG.v5. For each, the
comparison is against the strictest value known, not only the archive's.
- L = 381: bar 9878 (F 7.3477), an end-derivation of a published L = 383 sequence (`data/bar_351_449.json`). Dimitrov's
  published L = 381 value is 10078; the archive's is 10238.
- L = 449: bar 13392 (F 7.5269), an end-derivation of arXiv:2607.09688's L = 450 record. Dimitrov's L = 449 value is
  14112; the archive's is 15456.
Before any claim, `code/deep_derivations.py` (end-extensions up to 10 symbols exhaustively, up to 12 by beam, and
truncations, from every public sequence of length L-12..L+12) is run at that length. The bar becomes min(this bar,
that result).

## Method

Exactly the PREREG.v2 method (`search.py --mode saw --walk 4000 --prandom 0.5 --pcross 0.9 --heads auto --exploit 0.7
--top-arms 6`), random starts only, 600 s per length, one at a time on the GPU.
- L = 381: heads r1 24-28, r2 12-14, r3 9-11, seed 6381.
- L = 449: heads r1 26-30, r2 12-15, r3 9-12, seed 6449.
Code unchanged since PREREG.v2 (same sha256).

## Forecast

L = 401 reached F 7.46 in 130 s against a published 7.02. Here the bars are higher in F (7.35 and 7.53), so I expect
L = 381 to be beaten (60%) and L = 449 not (35%).

null_test: not needed because each claim is an explicit sequence whose exact integer energy is checked by a deterministic checker against a fixed numeric bar
