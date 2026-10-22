# PREREG v2: dna-codes-gc-king-table, run 2026-10-19-1601
frozen_utc: 2026-10-19T16:19:49Z

## Why a v2 (honest disclosure)
Written AFTER a result was seen. During a sanity check of the block-cyclic program (b=1, i.e. plain cyclic, at (11,8)),
the exact max-weight clique over all self-compatible Z_11 orbits gave a 33-word code, against King's unmarked 32 'l'.
PREREG.md (v1) named only (17,13), (18,14) and (14,11). This v2 extends the scope to every unmarked cell. The criterion
(the bank's, verbatim in PREREG.md) and the checker are unchanged; no threshold is changed after seeing a result.

## Criterion: unchanged (see PREREG.md, verbatim from the bank)
## Statistic and checker: unchanged (checker/check_gc_code.py; size m of a VALID code, w = floor(n/2))
## Thresholds
- record: m > King-page value (data/dnacodes.html, sha256 25d6e9f8...) for an unmarked (n,d). The status is at most PROMISING
  until (a) Montemanni-Smith-Koul 2014 and other post-2010 sources are checked (PENDING TABLE CHECK) and (b) a 3-skeptic
  panel passes it. One cell per claim.
- Sweep plan, fixed now: exact max-weight cyclic-orbit cliques (blockcyc with m = n, b = 1) for every odd n in 5..15 and
  every unmarked d with table value <= 600; block-cyclic (b = 2, m = n/2) for every even n in 6..14 and the same d range.
  Report every cell's result, including those below the table.

null_test: not needed because any claim is an explicit code checked by a deterministic checker against a table value, and negatives are exhaustive enumerations, not statistics
