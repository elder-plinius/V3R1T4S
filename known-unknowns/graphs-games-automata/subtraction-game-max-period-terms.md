# Subtraction games: longest eventual period for largest move n (OEIS A389689 at n = 25 and from n = 30, A389690 beyond n = 22)

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours to laptop-days (exhaustive over 2^(n-1) move sets; about 1.7e7 sets at n = 25, 5.4e8 at n = 30) · open as of 2026-10-28

## The problem

In the subtraction game with finite move set S (a player removes s in S tokens from one heap; whoever cannot move loses), the outcome sequence and the Sprague-Grundy sequence are eventually periodic (Golomb, 1966), but the only general bound on the period is exponential; Althöfer and Bültermann (TCS 148, 1995) gave sets with cubic periods, and Flammenkamp (1997) conjectured at most quadratic periods for 3-move sets. OEIS A389689 (Rui Yao, Oct 2025) lists, for each n, the longest eventual period of the win/lose sequence over all S with max S = n: n = 1..23 known (2, 4, 6, 8, 10, 12, 22, 25, 28, 45, 54, 61, 76, 94, 168, 168, 204, 314, 309, 266, 444, 516, 446). A389690 does the same for the Sprague-Grundy sequence, n = 1..22 known (2, 4, 6, 8, 10, 12, 22, 25, 28, 58, 54, 87, 114, 144, 189, 336, 306, 456, 728, 1178, 1180, 4464). Both entries carry the 'more' keyword and have not been extended since October 2025 (as of 2026-10-28); the terms come from exhaustive Python searches over all 2^(n-1) sets. Both entries were re-read on 2026-10-28 and show these terms. Further A389689 terms were published long before, in a source neither entry cites: Achim Flammenkamp's dissertation, Lange Perioden in Subtraktions-Spielen (Universität Bielefeld, 1997; the author's PostScript diss.ps.gz is linked from OEIS A014588; an enlarged book edition, not checked here, appeared in 1997, Hans-Jacobs-Verlag, ISBN 3-932136-10-1). On printed pp. 40-41 he computes the periods of all move sets with max S < 30 and lists the 44 record holders as max S grows. Its last line for each max S is the maximum for that n: A389689(24) = 1107 ({1, 3, 12, 21, 23, 24}) and A389689(26..29) = 1256, 1937, 3624, 4896, and the list agrees with OEIS at every n <= 23 where it has a line. It has no line for max S = 25, but his symmetric 5-move data (dia55.eps, printed p. 55) give period 1036 there, so 1036 <= A389689(25) <= 1107; the exact value is in neither OEIS nor the dissertation. The list's final line, {4, 10, 15, 20, 26, 30} with period 5296, is ambiguous: the text twice puts the exhaustive range at max S < 30 (pp. 40 and 43) yet counts this line among the 44, and the same line opens his search of symmetric sets only (n - s in S for every s < n in S) up to max S = 60 (p. 43), whose periods are lower bounds, not terms. Here 5296 at n = 30 counts as published, although it may be only a lower bound. The dissertation gives no Sprague-Grundy period maxima, so A389690 is unaffected.

## What counts as a win

CONFIRMED: the exact value of the next unpublished term (A389689 at n = 25, or A389690 at n = 23), or of any later unpublished term once those are filled, using the entries' own definitions (S ranges over all subsets of {1, ..., n} that contain n; the period is the minimal eventual period, found as the first repeat of the length-n window of outcomes or Sprague-Grundy values), with all of: (1) an explicit maximising set S whose period an independent program recomputes exactly; (2) two independently written exhaustive searches over all 2^(n-1) sets that agree on the maximum AND on the full histogram of periods (number of sets with each period); (3) the term is not yet in the OEIS entry, its b-file or its history at verification time, and is not a value in Flammenkamp's 1997 record list (A389689 at n = 24 and 26..29, and 5296 at n = 30): those count as published although the OEIS entry lacks them. Submitting to OEIS is an action for the human only.

## Partial wins

- **p1:** A correction of a published term: for some n already listed (n <= 23 in A389689, n <= 22 in A389690, or n = 24 and 26..30 in Flammenkamp's 1997 record list), an explicit set S with max S = n whose eventual period exceeds the listed value, confirmed by the OEIS Python program and one independent program.

## How a win is checked

Recompute the eventual period of each claimed maximising set with the Python program linked from the OEIS entry (a389689_1.txt or a389690_2.txt) and with an independent implementation. For the maximum, rerun an independent exhaustive search (C or Rust; bit-parallel windows for A389689) and compare the period histogram line by line with the claimant's; also confirm that the search reproduces every published term for smaller n, including Flammenkamp's (for example 1107 at n = 24, for {1, 3, 12, 21, 23, 24}).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A389690>

## Sources

- <https://oeis.org/A389689>
- <https://oeis.org/A389690>
- <https://oeis.org/A389689/a389689_1.txt>
- <https://oeis.org/A389690/a389690_2.txt>
- <https://arxiv.org/abs/2601.18715>
- <https://wwwhomes.uni-bielefeld.de/~achim/diss.ps.gz>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Win/lose sequence as bit operations: with the last n outcomes in a machine word w, the next outcome is ((~w) & maskS) != 0; Brent's cycle detection on w needs no hash table, so each set costs a few thousand word operations and 2^(n-1) sets split perfectly across cores.
- For Sprague-Grundy values the window holds small integers (values are at most |S|); pack them ceil(log2(n+1)) bits per entry (five bits are needed once n >= 16) and use the same cycle detection.
- Study the maximising sets for n <= 23 first (small-data) and seed a running maximum with the analogous sets and with Althöfer-Bültermann-type sets at the new n; this gives an early lower bound for the report, but the exhaustive pass must still cover every set.
- Keep and publish the per-set periods for a random 1% sample plus all sets within 10% of the maximum, so that a checker can spot-check cheaply before a full rerun.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The minimal period is the first repeat of the full length-n window, starting only once n values exist; a repeat of a shorter block, or one found inside the padded prefix, is wrong.
- Off-by-one in the convention: position 0 is a loss (no move), moves may not go below 0, and n itself must be in S.
- A389689 is not monotone (for example 314, 309, 266 at n = 18..20), so a search capped by the previous term is invalid.
- OEIS is not the only record: Flammenkamp's 1997 list already gives A389689 at n = 24 and 26..29 and lists 5296 at n = 30, so recomputing those values is a calibration, not a new term. His second list (p. 43) covers symmetric sets only, so its periods for max S = 30..60 are lower bounds, not terms. His enlarged 1997 book edition has not been checked; a value found there is published too. His symmetric 5-move data (dia5.eps, printed p. 52; dia55.eps, printed p. 55) are lower bounds too, for example 1036 at n = 25 (attained by {5, 8, 17, 20, 25}), 1800 at n = 31 and 8530 at n = 32 (attained by {6, 15, 17, 26, 32}): an exhaustive maximum below such a value is wrong, and one equal to it is a new term only with the exhaustive search the criterion asks for.
- Some periods grow fast (A389690 jumps from 1180 to 4464 at n = 22); detection must not assume a period bound below 2^n (win/lose) or (n+1)^n (Sprague-Grundy).
- This is a modest table: the value of a win is a correct, independently reproduced new term, not a theorem about period growth.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/subtraction-game-max-period-terms.md
```

Already set up? Say `run V3R1T4S on subtraction-game-max-period-terms`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `subtraction-game-max-period-terms`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
