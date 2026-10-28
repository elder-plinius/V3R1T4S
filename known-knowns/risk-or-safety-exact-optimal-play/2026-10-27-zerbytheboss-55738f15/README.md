# Risk or Safety (OEIS A387261/A387262): the next 15 exact optimal-play win probabilities, n = 31..45, with Bellman certificates

## What

Exact reduced rationals A387261(n)/A387262(n) = P(0,0,0) and complete n^2(n+1)/2-position Bellman value/action certificates P(a,b,c) for every n = 31..45 in the coin game Risk or Safety, reproducing published terms n = 1..15 and repository terms n = 16..30, verified by independent exact policy iteration and pure-turn-plan minimax solvers.

The main object is the 15-term table `object/values.txt` (sha256 `55738f1571783da777bc9739cb143fa3c858c087a28411f79aacf93ea14c8925`), listing lines "n num/den" for n = 1..45 (n = 1..15 are the published OEIS terms, reproduced; n = 16..30 are the repository terms, reproduced; n = 31..45 are the new exact terms), together with one certificate per n in `object/`: `n31.json.gz` and `n32.json.gz.part*` through `n45.json.gz.part*` (reassembled during check), each containing a JSON table listing the win probability of the player to move and the optimal action at every one of the n^2(n+1)/2 non-terminal positions (a open points, b banked points of mover, c banked points of opponent).

## Check It Yourself

Run from this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after `15 certificates n=31..45 verified; 30 calibration certificates n=1..30 verified (n=1..15 equal published terms); second verifier agrees`). About 20 seconds on a modern CPU, Python 3 standard library and gzip only. Details: `RUN_IT_YOURSELF.md`; real output: `verify-it-yourself/RECEIPTS.md`.

## Compared To

| what | value | source | fetched (UTC) |
|---|---|---|---|
| published terms of A387261/A387262 | n = 1..15 only; last term n = 15: 14364898791782224577113184680141626682/27711032758513212360715995025634765625 | https://oeis.org/A387261 and https://oeis.org/A387262 (b-files; page sha256 125834621bd2a3df06eb2406f93ade8ce74bde69569e8daf05501607d445c852) | 2026-10-28T00:36:28Z |
| repository known-knowns (2026-10-15-r-nikhil-8e69676d) | exact terms and certificates for n = 16..30 | `known-knowns/risk-or-safety-exact-optimal-play/2026-10-15-r-nikhil-8e69676d` (sha256 8e69676d99d3dc6726098a75c1167f2820f2c3e9c2bd0b82ed98e2dbb8446f24) | 2026-10-28T00:36:32Z |
| published optimal strategies | A394776 / Table 1 of arXiv:2603.01002: toss counts for points needed up to 20 | https://oeis.org/A394776 | 2026-10-28T00:36:31Z |
| this object | **15 new exact terms, n = 31..45** (322-digit numerator and denominator at n = 45), each proved by a complete Bellman certificate in `object/` | `object/values.txt` | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches: `panel/novelty.md`.

## Not Claimed

- Nothing about n > 45 is claimed here.
- No correction of any published value or action: all 15 published OEIS terms, all 15 repository terms, and all 400 published toss counts are reproduced.
- The exact rules are those of Sections 1-4 of arXiv:2603.01002 as restated in the certificate equations (reaching n with open points wins; a player with no open points must toss).
- The primary checker (`ros_cert_check.py`) uses `fractions.Fraction` directly; the independent second verifier (`my_verify.py`) tests exact integer cross-multiplication and verifies that gcd(p, q) = 1 on every value.

## Credits

- Contributor: anonymous-sovereign.
- Rüdiger Jehn, "Optimal strategy in the game Risk or Safety", arXiv:2603.01002 (2026): the game as posed here, the uniqueness argument, the equations of Section 4, Table 1, and OEIS A387260, A387261, A387262 (terms n = 1..15, more terms by Jinyuan Wang) and A394776. https://arxiv.org/abs/2603.01002 · https://oeis.org/A387261 · https://oeis.org/A387262 · https://oeis.org/A394776
- Todd W. Neller and Clifton G. M. Presser, "Optimal Play of the Dice Game Pig", The UMAP Journal 25(1) (2004) 25-47: the coin game "Piglet" (first to 10 points, same rules) with its exact goal-2 solution (P(0,0,0) = 4/7) and value iteration; they credit Fendel et al. for the independently invented "Pig Tails". https://cs.gettysburg.edu/projects/pig/
- Fabián Crocce and Ernesto Mordecki, "A non-iterative algorithm for generalized pig games", arXiv:1808.06707 (2018): exact solution of Piglet by the same Bellman equations, with the exact goal-3 table. https://arxiv.org/abs/1808.06707
- The OEIS Foundation and its editors for the sequences compared against.
- J. Glenn, H.-r. Fang, C. P. Kruskal, "A retrograde approximation algorithm for two-player Can't Stop" (2008), whose component-by-component argument Jehn's uniqueness proof follows; L. S. Shapley, "Stochastic games", PNAS 39 (1953).
