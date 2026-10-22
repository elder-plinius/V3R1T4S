# Erdos problem 757: a 21-element (4,5)-set with Sidon ratio 4/7 (partial win p1)

## What

The set A in object/witness_n21_s12.json (21 distinct integers, 21 not a multiple of 14) is a (4,5)-set whose exact maximum Sidon subset has size 12 (agreed by two independent exact methods run here), giving s/|A| = 4/7, exactly equal to, not below, the 4/7 shown at erdosproblems.com/757 and on the EinsteinArena leaderboard on 2026-10-18; this meets only the p1 partial win, not the full criterion, and says nothing about the lemma in arXiv:2602.23282.

Plainly: this is the p1 partial win, a tie at 4/7, not a better ratio. The set matches the best known upper bound 4/7 for the constant; it does not lower it. What is new is only that its size, 21, is not a multiple of 14.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library. The ILP (the criterion's second exact method, next to the branch-and-bound) needs pulp (`pip install pulp`). Without pulp the script says so, runs the other methods, and ends in `PASS` only if branch-and-bound and exhaustive enumeration both ran and everything agreed.
- **Rough laptop time**: under a minute.
- **Expected last line**: `ALL CHECKS PASS` (with pulp installed).

The object `object/witness_n21_s12.json` has sha256 6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| erdosproblems.com | Problem 757, upper bound for the constant | 4/7 (9/17 <= c <= 4/7, Ma and Tang) | 12/21 = 4/7 (tie) | https://www.erdosproblems.com/757 | 2026-10-18T14:25:04Z |
| EinsteinArena, Sidon Subsets of (4,5)-Sets | leaderboard best ratio | 0.571428571 (4/7) | 4/7 (tie) | https://einsteinarena.com/problems/sidon-45-set | 2026-10-18T14:25:05Z |
| Ma and Tang, arXiv:2602.23282 | best witness, 14 elements, s = 8 | 4/7, sizes in multiples of 14 | 4/7 at size 21 | https://arxiv.org/html/2602.23282 | 2026-10-18T14:27:27Z |

The arena problem as posted allows at most 18 integers; this set has 21, so it is not an arena entry. Details and hashes: `the-record-we-beat/README.md`.

## Not claimed

- No ratio below 4/7. The full success criterion (a strictly smaller ratio) is not met, and no claim is made against the upper bound for the constant.
- Nothing about the lemma in arXiv:2602.23282 (the blow-up lemma or the infimum formula); the panel's report discusses it.
- Not an EinsteinArena entry (21 elements; the arena allows at most 18).
- The claim in the contributor's text that no (4,5)-set with fewer than 16 elements can beat 4/7 has not been checked by the panel.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and the standalone checker shipped here.

## Filing history

Refile of the contributor's pull request #29 (the same 21-element set), closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect. The ILP was added to the package on 2026-10-18, before the panel ran.

## Credits

- **Y.-N. Ma and Q. Tang**, *Largest Sidon subsets in weak Sidon sets*, arXiv:2602.23282 (https://arxiv.org/abs/2602.23282): the 14-element set and the bounds this set is compared with; the witness here is built on their set.
- **Erdos problems** by Thomas Bloom, https://www.erdosproblems.com/757: the problem and its live status.
- **EinsteinArena**, https://einsteinarena.com/problems/sidon-45-set: the leaderboard compared against.
- **M. A. Henning and A. Yeo** on transversals in linear 3-uniform hypergraphs, as used in the contributor's account (via arXiv:2602.23282).
- The solver for the ILP is CBC through **pulp** (https://github.com/coin-or/pulp).
- Search: an AI agent (Gemini, called Argon) for the contributor `calgulbenkian`.
