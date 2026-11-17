# Honesty gate: run 2026-11-09-1306, claim erdos-1023-union-free-n8, n = 8 (full success criterion)

Written by the main session at 2026-11-09T13:41:06Z (date -u), after reading all three panel files in full.

- reproduce.md: pass: true. Two own checkers (per-element cover test and every union of other members), calibrated by
  exhaustive search on a(1..5) = 1, 2, 4, 7, 13; all 80 members checked; repeat runs identical. Noted: the shipped
  checker silently drops a repeated number within a line (does not affect the claimed file); fixed in the package.
- novelty.md: pass: true. OEIS A347025 fetched once (HTTP 200, 2026-11-09T13:27:28Z; JSON hash identical to the
  scout's), revision 111; no family of 80 or more in the entry, its 111 revisions, its links (Blair 60, Loo 74),
  erdosproblems.com, Math.SE, arXiv, GitHub or this repository. Not a trivial edit of Schoenfield's 79-family
  (different size profile, at most 64 shared sets under any relabelling, and that family is maximal).
- criterion.md: pass: true, with the confirmed_scope below.
- The table fetches are from 13:04-13:28Z today, under 6 hours old.

status: CONFIRMED_SOLUTION
confirmed_scope: object/union_free_n8_80.txt lists exactly 80 distinct nonempty subsets of {1..8} (2 of size 2, 15 of size 3, 63 of size 4) in which no member equals the union of any nonempty subcollection of the other members (the OEIS A347025 property, equivalently no member equals the union of all other members it contains), confirmed by the contributor's script and by an independent brute force, so its size exceeds by one the bar a(8) >= 79 (Jon E. Schoenfield, Apr 2022), the only n = 8 value in the live OEIS A347025 entry body and comments as fetched 2026-11-09T13:28:00Z.
