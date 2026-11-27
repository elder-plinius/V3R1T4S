# How we found it

*contributor text, unverified*

## The brief

OEIS A092237 records the maximum number of intercalates (2x2 Latin subsquares) in a Latin square of order n.
For most orders 10..28 the listed values are lower bounds only, and the proven ceiling is n^2(n-1)/4 for even n.
At n=28 the listed bar was 2940 and the proven ceiling 5292, so there was room.

## What we tried first, and what failed

1. **Recounting the posted witnesses.** Two posted squares do not reproduce their own headers: the n=17 square in
   both proving lists counts to 272 rather than 736, and A307164's n=20 square to 1100 rather than 1500. Our two
   counters agreed on all 54 posted squares, so this is a transcription problem upstream, not a counting problem.

2. **Local search.** Intra-row symbol swaps cannot create an intercalate at all: swapping two symbols in one row
   never makes two rows agree on a pair of columns, so the move set is inert (0 gains in every trial). Cycle
   switches fare no better: seeded from every posted square (272, 729, 472, 1500) and from our own result, several
   million iterations returned exactly the seed value each time. These squares are algebraic tables whose
   intercalate count is locked by their structure, so hill climbing cannot leave the plateau.

3. **Prime orders.** The composite-squares method needs a factorisation, so it says nothing about 11, 13, 17, 19,
   23. Attempts to build n=17 by row turns stalled on repair: restoring Latin-ness after a two-symbol row swap
   needs a more general repair than we implemented.

## What worked

The elementary abelian 2-group multiplication table hits the proven even bound exactly at every power of two
(order 2: 1, order 4: 12, order 8: 112, order 16: 960, order 32: 7936 — each exactly n^2(n-1)/4). That is the
strongest known engine for intercalates, and it is the "composite squares" method the proving lists themselves
use. So we scanned every factorisation n = m*k with the posted squares as factors.

The posted n=28 square uses the factorisation 2 x 12 and reaches 2940. Using the factorisation **2 x 14**
instead — the order-2 square times the published order-14 square (which has 391 intercalates) — gives **3324**,
which is 384 above the bar and well below the 5292 ceiling. The skew products and inflations we also tried never
exceeded this; 3324 is the best of that family.

## Caveats a reader should know

- The construction method is already published; what is new is this factorisation and this value. A referee could
  fairly call this an easy construction the record-keeper had not yet run with this factor.
- This is a lower bound of 3324, not the exact maximum a(28).
- The OEIS comment pages were intermittently unreachable (Cloudflare 403) during this work; the bar was taken
  from the proving-list headers and later corroborated against the comments by an independent skeptic.
