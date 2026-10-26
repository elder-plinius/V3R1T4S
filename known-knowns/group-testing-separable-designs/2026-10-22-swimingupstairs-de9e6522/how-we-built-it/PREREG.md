# PREREG (frozen 2026-10-19T17:47:37Z, from date -u; written before any attack output on the scored cells exists in this run)

run: 2026-10-19-1746   target: group-testing-separable-designs (OEIS A054961)   effort: standard (3 lenses)
budget: start 2026-10-19T17:47:37Z; no new line of work after 80% of budget; budget end 2026-10-19T20:47:37Z (END_EPOCH in tools/END_EPOCH).

## Criterion (verbatim from charter.md quarry 1)
"extend or improve the best known values for non-adaptive pooled-testing designs: max number of binary vectors of length n whose pairwise unions are all distinct (OEIS A054961), the same for 3-unions (OEIS A290492), and the min number of tests T(n,d) to identify exactly d defectives among n items (OEIS A361928)."
Partial win scored here: an explicit family of m distinct binary vectors of length n whose C(m,2) pairwise ORs are all distinct, with m > B(n).

## Cells (fixed now). B(n) = max(OEIS Du 2018, emath poisonall.txt, wolfy-out.txt, own workspace best).
| n | OEIS (Du 2018) | emath / wolfy-out | own best | B(n) | candidate iff m >= |
|---|---|---|---|---|---|
| 16 | 91 | 91 / 91 | 92 (run 1345, unpanelled) | 92 | 93 |
| 17 | 112 | 113 / 113 | 108 | 113 | 114 |
| 18 | 145 | 145 / 145 | - | 145 | 146 |
| 19 | 182 | 182 / 182 | - | 182 | 183 |
If several cells qualify, each is its own claim (one cell per claim); the largest margin over B(n) is reported first.

## Statistic and checker
- Judge: python3 checker/check_union.py <file> n 2 -> VALID, and checker/indep_check.py <file> n -> PASS (both exhaustive over all pairs). Search-tool costs and sizes are never trusted; .best checkpoints are not objects.
- Before any claim: re-read OEIS A054961 once (single GET).

## non_trivial_extension: VOID clause
VOID if the family is only a zero-pad of a smaller-n family (published or own) plus at most one vector per added coordinate, a union/restriction of published objects, or a published family plus at most 2 vectors. A family produced by the designer's augment/swap of the own 92-family scores at n=16 only if m >= 93 and is labelled "own-92 + augment" (low-value if +1 over own unpanelled 92; reported, not claimed, unless the 92 itself is confirmed later).

## Null design
null_test: not needed because every candidate is an explicit family judged by deterministic exhaustive checkers against table values.

## Lenses and jobs (fixed now; all nice 12, 600 s chunks, resumable wrappers tools/ladder.sh / tools/augment_watch.sh stopping at END_EPOCH; PIDs in PIDS.txt; HEARTBEAT every 120 s)
- search-engineer (unbiased random-start mc2, density 1/4): (16,93) x2 seed streams (SA 160000, SB 170000); (17,114) x1 (S 270000).
- constructor (fixed-weight random-start mc2w): (16,93) w=4 (S 360000); (17,114) w=4 (S 370000); (18,146) w in {4,5} alternating (S 380000); (19,183) w in {4,5} alternating (S 390000).
- designer (augment_watch.sh): exhaustive +1 augment, then exhaustive 1-out-2-in swap, of the own 92-family, of the own n=17 108-family, and of every new VALID find.
On a VALID find at m, a ladder tries m+1 (alternating warm-from-find and random starts).
