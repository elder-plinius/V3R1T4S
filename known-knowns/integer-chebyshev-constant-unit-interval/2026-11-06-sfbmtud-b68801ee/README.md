# Integer Chebyshev upper-bound certificate

## What
The explicit 213-factor integer polynomial in ../claim/object/candidate.json with SHA-256 b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce has degree 2000000000052 and normalized supremum norm on [0,1] strictly below the exact rational 0.422640947, which is strictly below 0.422684697505.

The package-local witness is object/candidate.json; the claim path in the verbatim scope names the isolated review layout. This is the repository's criterion A, a better explicit upper-bound witness. The exact value of the integer Chebyshev constant remains undetermined. The result is AI-assisted and has not undergone external peer review.

## Check it yourself
From this directory on Unix, with Python3.12 and no third-party packages:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. This recomputes every bound, checks exact coverage and rejects a corrupted object. The underlying final proof took about222seconds on the research host; allow several minutes on another computer. A timeout is inconclusive. See RUN_IT_YOURSELF.md and the self-contained verification method.

## Compared to
| Cell | Published upper bound | This witness | Primary source |
|---|---:|---:|---|
| Integer Chebyshev constant on [0,1], upper bound | 0.422684697505 | 0.422640947 | [Giraudin, Theorem1, v3](https://arxiv.org/html/2610.00386v3) |

Primary status page fetched2026-11-05T22:56:49.458826Z, HTTP200; final literature/repository refresh2026-11-06T00:03:29.434Z. Exact improvement0.000043750505. Raw web pages are not included; receipts and extracted values are in the-record-we-beat/. The rigorously checked fixed-library barriers exclude reaching this value by reweighting the two compared published libraries alone.

## Not claimed
No exact constant, optimal polynomial, globally optimal search, unrestricted lower bound, newly invented method, worldwide priority, or previously unknown status of every added factor is claimed. The search was adaptive and bounded. The full factor catalog is not an exhaustive enumeration of integer polynomials. The final object, not the floating-point optimizer, is the certificate.

## Credits
Contributor: sfbmtud, with AI-assisted construction, code and independent-context verification. Seed and comparator: [David Niedbala Giraudin](https://arxiv.org/abs/2610.00386v3). Underlying work and methods include [Valérie Flammang](https://doi.org/10.1016/j.jnt.2014.04.002), [Kevin G. Hare and Philip W. Hodges](https://arxiv.org/abs/1804.05985v2), [Igor E. Pritsker](https://arxiv.org/abs/math/0101166), and the Gorshkov-Wirsing constructions credited in the source paper. FLINT/Arb, Python-FLINT, SymPy, SciPy/HiGHS and NumPy supported search or auxiliary checks; the main checker uses Python's standard library. Repository conventions: code under AGPL-3.0 and contributor data under CC BY4.0; third-party mathematical inputs retain their source attribution and applicable licenses.
