# Self-break summary (before the panel)

Run of 2026-10-25 (a fresh-context session) and run of 2026-10-27 (main session, not a fresh context); the fresh-context
checks of record are panel/.
- Two independent checkers written from the definition (exact integers over all 4,112,784 Brent equations; and the
  full tensor modulo two primes): 0 wrong; 1270 terms, none with a zero factor, no duplicates, no two terms
  proportional. Planted mutants (a dropped term, a duplicated term, coefficients +1 in u and w, a moved v entry, C rows
  flipped) fail every checker by violated Brent equations, not by a parse error.
- Rebuild from LITA's upstream file (sha256 and git blob sha1 match the LITA tree, fetched again 2026-10-27): byte-identical
  u, v, w; an independent re-implementation of the slice also gives a valid 1295-term scheme whose B factors contain
  every final B factor.
- Literal criterion: max dimension 13 <= 16; sorted (12,13,13) not excluded; 1270 < 1274, the minimum of the four live
  sources; exact over Q (needs 1/2, so not a GF(2) scheme); not equal to any listed composition value (listed: 1274,
  1298, 1300).
- Table access: one curl GET per URL with a User-Agent naming V3R1T4S; no cookies or browser imitation. One GitHub
  search request burst met a 403 rate limit on 2026-10-27; those requests were not retried and nothing here rests on
  them.
Verdict: SURVIVES.
