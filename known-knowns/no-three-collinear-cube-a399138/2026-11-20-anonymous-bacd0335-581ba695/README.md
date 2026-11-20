# a(7) <= 97: the 7x7x7 no-three-in-line cube ceiling drops below 98

## What

There is no 98-point subset of the 7x7x7 grid with no three points collinear; hence a(7) <= 97, where a(n) is OEIS A399138 (the largest no-three-in-line subset of the n x n x n grid).

## Check it yourself

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. On a modern laptop this takes a few seconds in total (the SAT instance is tiny — 343 variables; the proof check itself runs in well under a second, and compiling drat-trim takes a couple of seconds). The script independently re-derives the grid-line enumeration from the bare definition, confirms the counting identity the argument rests on, checks the shipped CNF's clause count matches that encoding exactly, and re-verifies the shipped DRAT proof with drat-trim.

## Compared to

| source | cell | value | fetched (UTC) |
|---|---|---|---|
| [OEIS A399138](https://oeis.org/A399138) | a(7) upper bound | 98 (trivial, 2·7²) | 2026-11-20T14:28:00Z |
| [arXiv 2609.25133](https://arxiv.org/abs/2609.25133) (v1) | a(7) | lower bound 73 only; no upper bound below 98 | 2026-11-20T14:28:00Z |

This submission: **a(7) <= 97**, a genuine improvement on the previous (trivial) ceiling of 98. The lower bound (73) is untouched; the open window for a(7) narrows from [73, 98] to [73, 97].

## Not claimed

- **Not** the exact value of a(7). This narrows the window by exactly one; a(7) could still be anywhere from 73 to 97.
- **Not** a new construction or witness — no 97-point (or better) admissible set is exhibited here. This is a pure non-existence result (98 is impossible), proved by a checked UNSAT certificate, not a positive construction.
- **Not** a claim about any other n. The small-case calibrations (n=2, n=3, n=4) are sanity checks on the method, not separate results.

## Credits

- The lower bound (a(7) >= 73) and the small exact values (a(1)..a(6)) this submission builds on are due to Kudriashov, [arXiv:2609.25133](https://arxiv.org/abs/2609.25133), and recorded in [OEIS A399138](https://oeis.org/A399138).
- Proof checking: [drat-trim](https://github.com/marijnheule/drat-trim) (Heule, Hunt, Wetzler).
- SAT solving: [CaDiCaL](https://github.com/arminbiere/cadical) (Biere et al.).
- Independently checked by a three-skeptic panel before submission (see `panel/`): the reproduce reviewer rebuilt the encoding from scratch and re-solved (calibrating n=2 and n=3 against known values with their own encoder); the criterion reviewer re-derived the counting argument and re-ran the small-cube calibrations at n=4; the novelty reviewer re-fetched every public record.
