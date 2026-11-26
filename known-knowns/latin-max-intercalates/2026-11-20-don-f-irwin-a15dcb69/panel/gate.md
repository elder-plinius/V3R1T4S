status: CONFIRMED_PARTIAL
confirmed_scope: An explicit order-28 Latin square with 3324 intercalates, strictly exceeding the 2940 bar read from the comments and proving-list headers of A092237 and A307164, and below the proven bound 5292.

# Honesty gate — main session's own reading

## Panel files read
- `panel/reproduce.md` — context: headless hermes CLI — last line `pass: true`
- `panel/novelty.md` — context: headless hermes CLI — last line `pass: true`
- `panel/criterion.md` — context: headless hermes CLI — last line `pass: true`

All three are genuine fresh contexts: each ran as a separate `hermes -z` headless process in its own copy of
`claim/` (`panel_work/<role>/claim/`), each wrote its own code, and none saw the other two or my attempts folders.

## Gate checks I ran myself
1. **No hedging.** All three state an unambiguous pass with a stated reason, not a conditional one.
2. **Reproduction.** My own three counters agree: countA 3324, countB 3324, literal O(n^4) recount 3324. The
   REPRODUCE skeptic's independent checker also gives 3324 and rebuilt the square byte-identically from the two
   source files. No mismatch anywhere.
3. **Strictly better than the live table.** 3324 > 2940 by 384. Both the proving-list headers and (per the
   CRITERION skeptic, who re-fetched them successfully) the OEIS comment blocks give 2940 for n=28, so the bar is
   corroborated on both legs the criterion names. The NOVELTY skeptic found Vatutin's n=28 spectrum file
   (2803 known values) whose maximum is exactly 2940 — our object is not in it.
4. **Not a stretched criterion.** n=28 is in range 10..28 and is neither 15 nor 16. The object is an explicit
   Latin square. The count is deterministic and agrees across independent programs. This is the literal main
   criterion, not a partial win: partial win p1 (a *diagonal* Latin square) is not claimed and not needed.
5. **Scope no wider than reproduced.** The confirmed_scope names one order, one count, one bar and the bound.
   It does not say "record", "solved", "first ever" or "world record" — the criterion does not use those words.
6. **Not a capped search used as an exclusion.** No exclusion is claimed. Nothing here rests on an incomplete
   search.
7. **No bundling.** One object, one cell.
8. **Table access.** All fetches were single honest GETs with a User-Agent naming V3R1T4S. The OEIS HTML pages
   returned 403 (Cloudflare challenge) at 12:20Z; we did not retry, did not evade, and recorded PENDING TABLE
   CHECK. The proving-list .txt files returned 200. The CRITERION skeptic later got the comment pages at 200 with
   the same honest method. No evasion anywhere.
9. **Benchmark baseline.** Not an empirical benchmark; no baseline reproduction required (explicit object against
   a table value).

## The one thing I disagree with in a panel file
The REPRODUCE skeptic passed the claim but asserted a "definitional over-count": it says the counting rule also
counts 3936 three-distinct 2x2 blocks, and that the "standard" intercalate count of our square is 135624.

I checked this myself and the skeptic is **wrong**, in a way that does not change the verdict:

- An intercalate is a 2x2 Latin subsquare, i.e. the pattern [a,b,b,a] — **two** distinct symbols, not four.
- I enumerated every 2x2 block of our square by its number of distinct symbols: 135624 have 4 distinct symbols
  (the generic case, not intercalates), 3936 have 3, and exactly 3324 have 2.
- Every block the rule counts has exactly 2 distinct symbols (distribution {2: 3324}), so the rule counts exactly
  the intercalates, once each. There are zero 3-distinct blocks among the rule-counted ones.
- Cross-check against the published values: on the order-4 group table the rule gives 12 = published a(4)=12,
  while "4 distinct symbols" gives 24 (each intercalate counted twice). On the posted order-5,6,7,9,14,28 squares
  the rule reproduces the headers exactly (4, 27, 42, 72, 391, 2940). The rule is right and the skeptic's
  "standard count" is not the intercalate count.

So the skeptic's caveat is recorded here, its arithmetic corrected, and the pass stands. This is a case where a
wrong SURVIVES would be bad — but the check here is a recount of a saved object against a published bar, and four
independent counters (three of mine, one of the skeptic's) give 3324, so the number itself is solid.

## Also recorded
The CRITERION skeptic noticed the bank's quoted odd-order values are stale relative to the live comments
(a(23) 983 not 985, a(27) 648 not 1372, a(21) 1026 vs 884). None touch n=28, so the bar stands at 2940; but the
bank entry's "2026-10-30 values" paragraph should be refreshed by a human. This goes under "Needs you".

## Status decision
`CONFIRMED_PARTIAL` — not `CONFIRMED_SOLUTION`, because the target's success criterion is per-cell and this run
settles one cell (n=28) of a 19-cell table; it is not the whole target. Three skeptics passed, the object is
deterministic and reproducible, the bar is corroborated on both named legs, and the count is strictly above it.
The gate condition is `CHECK_RUN: PASS`, run at the end of this report.
