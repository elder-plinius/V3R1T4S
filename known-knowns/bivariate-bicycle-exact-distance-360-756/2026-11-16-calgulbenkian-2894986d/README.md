# Weight-28 Nontrivial Logical Operator for the `[[504, 12, <= 30]]` Covering Bivariate Bicycle Code (`p1`)

## What

An explicit weight-28 nontrivial logical operator (index-negated labeling of the standard convention, equivalent by relabeling) exists for the [[504,12]] covering BB code with l=42, m=6, A=x^27+y+y^2, B=y^3+x^37+x^38, verified exactly over GF(2), so its minimum distance is at most 28, below the published bound of 30; no lower bound, no exact distance, and no claim on the 360, 432 or 756 codes.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in `< 0.2 s`, Python 3 standard library only; performs exact `GF(2)` syndrome and rank-augmentation checks).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Symons, Rajput, Browne, `arXiv:2511.13560v3` (6 Aug 2026, Table 1) | `[[504, 12]]` (`l=42, m=6, A=x^27+y+y^2, B=y^3+x^37+x^38`) | `d <= 30` | https://arxiv.org/abs/2511.13560 | 2026-11-15T16:29:27Z |
| Rowshan and Devitt, `arXiv:2609.39395v2` | Exact BB code distances | Certified up to `n = 288` (`[[504, 12]]` untouched) | https://raw.githubusercontent.com/mohammad-rowshan/BB-Codes-Distance-Logical-Decomposition/main/README.md | 2026-11-15T16:29:26Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Establishes upper bound `d <= 28` (`p1`) via an explicit weight-28 nontrivial logical operator; does not claim an exhaustive lower-bound certificate proving `d = 28`, nor bounds below published records on `[[360, 12, <= 24]]`, `[[432, 12, <= 24]]`, or `[[756, 16, <= 34]]`.

## Credits

- **Owen R. Symons, Kaustubh Rajput, and Dan E. Browne** (<https://arxiv.org/abs/2511.13560>): introduced the `[[504, 12, <= 30]]` prime-degree (`h = 7`) covering bivariate bicycle code.
- **Sergey Bravyi, Andrew W. Cross, Jay M. Gambetta, Dmitri Maslov, Patrick Rall, and Theodore J. Yoder** (*Nature* 627, 778–782, 2024) and **Mohammad Rowshan and Simon J. Devitt** (<https://arxiv.org/abs/2609.39395>): BB code formulation and colon-ideal logical decomposition.
