# Risk or Safety (OEIS A387261/A387262): the next 15 exact optimal-play win probabilities, n = 16..30, with Bellman certificates

## What

For each n = 16, ..., 30, the reduced fraction given for n in values.txt and claim.md is P(0,0,0) of object/nK.json with K = n, which lists a value and an action at every one of the n^2(n+1)/2 non-terminal positions and satisfies the criterion's equations exactly in rational arithmetic (P = 1 when a + b >= n, forced toss at a = 0, P = max(continue, stop) for a >= 1 with the listed action attaining the max and no exact ties), so by the proof note's uniqueness argument (checked sound) it is the starting player's win probability from (0, 0, 0) under optimal play in the game of Sections 1-4 of arXiv:2603.01002, and the same solver, re-run, regenerates all 30 certificates byte-for-byte with its n = 1..15 values equal to the A387261/A387262 terms in the package's OEIS snapshot (data/), n = 1..6 also equal to the values printed in the paper.

(Panel status: see `panel/gate.md`. The panel's `claim/values.txt`, `claim/object/n16.json ... n30.json` and `claim/calibration/n1.json ... n15.json`
are this package's `object/values.txt`, `object/n16.json` ... `object/n30.json` (n = 27..30 gzipped, same bytes after `gzip -d`) and
`verify-it-yourself/calibration/n1.json ... n15.json`; the panel's `claim/data/` b-files are `verify-it-yourself/published_terms/`.)

The object is the 15-term table `object/values.txt` (sha256 8e69676d99d3dc6726098a75c1167f2820f2c3e9c2bd0b82ed98e2dbb8446f24), lines
"n num/den" for n = 1..30 (n = 1..15 are the published terms, reproduced; n = 16..30 are new), together with one
certificate per n in `object/`: a JSON table `{"n": n, "P000": "num/den", "table": [[a, b, c, "num/den", "toss"|"stop"], ...]}`
listing the win probability of the player to move and the optimal action at every one of the n^2 (n+1)/2 positions
(a open points, b banked points of the player to move, c banked points of the opponent).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after `15 certificates n=16..30 verified; 15 calibration certificates n=1..15 equal the published
terms; second verifier agrees`). About 30 seconds on a laptop, Python 3 standard library and gzip only. Details:
`RUN_IT_YOURSELF.md`; real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| published terms of A387261/A387262 | n = 1..15 only; last term n = 15: 14364898791782224577113184680141626682/27711032758513212360715995025634765625 | https://oeis.org/A387261 and https://oeis.org/A387262 (b-files; page sha256 ee962761…) | 2026-10-15T03:16:19Z (re-fetched 2026-10-15T09:31:05Z, unchanged) |
| published optimal strategies | A394776 / Table 1 of arXiv:2603.01002: toss counts for points needed up to 20 | https://oeis.org/A394776 | 2026-10-15T03:16:22Z |
| this object | **15 new exact terms, n = 16..30** (152-digit numerator and denominator at n = 30), each proved by its certificate; the derived toss counts agree with all 400 published A394776 terms | `object/` | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches: `panel/novelty.md`.

## Not claimed

- Nothing about n > 30 is claimed here (the run also certified n = 31..40 and larger tables; those are a separate matter).
- No correction of any published value or action: all 15 published terms and all 400 published toss counts are reproduced.
- The exact rules are those of Sections 1-4 of arXiv:2603.01002 as restated in the certificate equations (reaching n with
  open points wins; a player with no open points must toss). Variants in which a player must bank to win, may pass with
  no open points, or chooses x coins at once give the same values (checked for n <= 8); a game in which the second player
  moves first does not.
- The provided checker does not itself test that each fraction is in lowest terms; the second verifier and the panel's
  own checkers do, and every entry is reduced.

## Credits

- Rüdiger Jehn, "Optimal strategy in the game Risk or Safety", arXiv:2603.01002 (2026): the game as posed here, the uniqueness
  argument, the equations of Section 4, Table 1, and OEIS A387260, A387261, A387262 (terms n = 1..15, more terms by Jinyuan
  Wang) and A394776. https://arxiv.org/abs/2603.01002 · https://oeis.org/A387261 · https://oeis.org/A387262 · https://oeis.org/A394776
- Todd W. Neller and Clifton G. M. Presser, "Optimal Play of the Dice Game Pig", The UMAP Journal 25(1) (2004) 25-47: the coin
  game "Piglet" (first to 10 points, same rules) with its exact goal-2 solution (P(0,0,0) = 4/7) and value iteration; they credit
  Fendel et al. for the independently invented "Pig Tails". https://cs.gettysburg.edu/projects/pig/
- Fabián Crocce and Ernesto Mordecki, "A non-iterative algorithm for generalized pig games", arXiv:1808.06707 (2018): exact
  solution of Piglet by the same Bellman equations, with the exact goal-3 table. https://arxiv.org/abs/1808.06707
- The OEIS Foundation and its editors for the sequences compared against.
- J. Glenn, H.-r. Fang, C. P. Kruskal, "A retrograde approximation algorithm for two-player Can't Stop" (2008), whose
  component-by-component argument Jehn's uniqueness proof follows; L. S. Shapley, "Stochastic games", PNAS 39 (1953).
