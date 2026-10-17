# PREREG: minimizer-density-record-tables (w=12, k=3)

Timestamp: 2026-10-16T09:52Z

## Criterion (verbatim from bank)
"An explicit minimizer order for a stated (w, k) pair, given either as a complete rank file
or as deterministic released code that emits one, whose DNA density, computed by the skeptic
with the repositories' own density measurement code, is STRICTLY LOWER (direction: min) than
the smallest value listed for that (w, k) pair across the tables in
github.com/OrensteinLab/10-minimizers and the precomputed minimizers of
github.com/OrensteinLab/GreedyMini (both re-fetched live immediately before claiming) by at
least 0.5% relative, with the comparison made under the same density definition (expected
density for the expected-density tables, particular density on the same sequence otherwise)
and with the order's storage cost stated."

## Exact statistic / checker
The density is the exact expected density, not a sample. It is computed on the
de Bruijn sequence of order w+k over the 4-letter alphabet, which contains each
(w+k)-window exactly once:

    d = (M + 4) / 4^(w+k)

where M is the number of window positions t in [1, 4^(w+k-1)) on that sequence
whose minimizer k-mer index differs from that of window t-1, and the +4 charges
the first window (its k-mer is the minimizer of exactly 4 window positions in
the de Bruijn sequence). This is the same convention the repositories' own
sampling routine implements, taken to the limit.

The order's rank function is the one the notebook uses:
  rank(km) = (order[((km>>4)&1)<<2 | ((km>>2)&1)<<1 | (km&1)] << 2k) + km
with the table's own tiebreak appended by the measurement.

## Threshold
- Published best for the cell: 0.138843
- Threshold: 0.138843 * 0.995 = 0.138148785
- Claim requires: exact_density < 0.138148785

## Null design
null_test: not needed because the claim is an explicit order checked by a
deterministic exact checker (the de Bruijn identity above) against a published
table value. There is no search statistic and no "beats chance" claim: the
checker either reproduces the arithmetic or it does not, and it is cross-checked
against the repositories' own sampling routine at n=1,000,000 on three random
orders before the real cell is scored.

This is the shape kit/RUN.md step 3b names explicitly: "an explicit object
checked by a deterministic checker against a table value".

## Search space
- All 8! = 40320 orders of the 8 binary prefixes, exhaustive, uncapped, each
  scored with the exact density. The order file has 8 entries because the
  projection (A=C=0, G=T=1) has 8 values.
- GreedyMini's own order [8, 2, 8, 8, 0, 4, 1, 3] is the incumbent.
- Sentinel handling: the incumbent's value 8 equals the table size and is
  treated as the largest rank, which is what the notebook does (order_dict
  values are used as-is).
