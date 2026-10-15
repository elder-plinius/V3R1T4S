# PREREG.v2.md (new, timestamped pre-registration for the DEEP EXTENSION; PREREG.md is unchanged and still governs n = 16..30)

frozen_at: Thu Oct 15 09:11:24 UTC 2026
target: risk-or-safety-exact-optimal-play
run: runs/2026-10-15-0312
reason: the OPERATOR raised the budget to heavy at about 09:05 UTC and asked to go deeper on this target; the live line is
extending the certified terms beyond n = 30. This file freezes the rule for that extension before any extension output
beyond the already-checked reserve (n = 31..40 full certificates, checked at 09:01 UTC) is measured.

## Object of the extension

A "compact certificate" for a bound N: the table P0(i, j) = P(0, i, j) for all 1 <= i, j <= N in points-needed
coordinates (i = points the mover still needs, j = the opponent's), as reduced fractions, one line "i j num/den".
Given P0, every other value is defined by the backward recursion V(a, i, j) = max(continue, stop) for a = i-1..1 with
continue = (1/2)(1 - P0(j, i)) + (1/2) V(a+1, i, j), V(i, i, j) = 1, stop = 1 - P0(j, i - a); the certificate is valid
iff for every ordered pair (i, j): P0(i, j) = (1/2)(1 - P0(j, i)) + (1/2) V(1, i, j) exactly. (Then the full table
satisfies all the bank's equations, and by the uniqueness argument it is the optimal-value table; A387261(n)/A387262(n)
= P0(n, n).) The derived toss counts T(i, j) (smallest a >= 1 at which stop beats continue, or i if none) extend A394776.

## Checker that will judge it

code/ros_compact_check.py (written by the main session from the definition before any extension output is examined;
tested on compact tables derived from the already-verified full certificates for n = 30 and n = 40, and on corrupted
copies which must fail). Decisive outputs: "COMPACT_PASS" or "COMPACT_FAIL"; the count of ordered pairs checked (N^2);
"oeis_match=yes" for n = 1..15; agreement of P0(n, n) for n <= 40 with the full certificates' values; agreement of the
derived T(i, j) with all 400 published A394776 terms (i, j <= 20).

## Thresholds (decision rule, fixed now)

- The confirmed scope may be extended from n = 16..30 to n = 16..N iff ALL of: (a) the compact certificate for N passes
  the compact checker (every ordered pair, exact rationals); (b) a second, independently written solver (the contrarian
  lens's minimax solver) produces an IDENTICAL P0 table for the same N (all N^2 entries); (c) P0(n, n) equals the full
  certificates' P(0,0,0) for every n <= 40 and the OEIS terms for n <= 15; (d) the three-skeptic panel verifies the
  extended claim (the REPRODUCE skeptic must run a checker it writes itself over all N^2 pairs).
- If (b) is unavailable for a given N (second solver too slow), the extension to that N is reported as "verified by one
  solver and the independent checker" and is NOT claimed; the claimed scope stops at the largest N satisfying (a)-(d).
- Values beyond the largest checked N are UNCERTIFIED and are never claimed.
- The A394776 extension (toss counts) is claimed only for the same range and only as derived from a certificate that
  passed; it is reported as a by-product, not as a separate claim.

## Null design

null_test: not needed because the result is an explicit object (an exact value table) checked by a deterministic
exact-rational checker against the Bellman equations and the published terms; no search statistic is involved.
