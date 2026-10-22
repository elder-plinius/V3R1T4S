# Monomer-dimer entropy of the square lattice: rigorous enclosure certifying 13 decimals (partial win p1)

## What

For the monomer-dimer entropy h2 of the square lattice (natural log, per site), the shipped certificate vectors for the cylinder transfer matrices of circumference 22 and 24 give, through exact integer Collatz-Wielandt ratios and the two proved inequalities, the rigorous enclosure 0.6627989728337138109756 <= h2 <= 0.6627989728337490653104, certifying 13 decimals; nothing wider is confirmed (no claim on the main criterion, none on novelty beyond the two quoted comparators).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.9 or later, standard library only.
- **Memory and time**: about 6.5 GB of memory and about 40 seconds on an M3 Ultra Mac Studio. A machine with less than about 8 GB free may fail.
- **Expected last line**: `PASS` (the line before it is `CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338  (13 decimals)`).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Friedland and Peled, Adv. Appl. Math. 34 (2005), arXiv math/0402009 | certified decimals of h2 | 8 ("h2 = .66279897, correct to 8 decimal digits") | https://arxiv.org/abs/math/0402009 | 2026-10-19T04:38:44Z (novelty skeptic; the contributor's team fetched the pdf at 2026-10-19T03:44:36Z) |
| Kong, Phys. Rev. E 74, 061102 (2006), arXiv cond-mat/0610690 | printed value and bracket | 0.662798972834 (12 printed decimals, "11 correct digits"); bracket 0.662798972831 to 0.662798972845 from numerical cylinder values, not a proof | https://arxiv.org/abs/cond-mat/0610690 | 2026-10-19T04:38:06Z (abstract page) and 2026-10-19T04:38:50Z (pdf) |
| Butera, Federbush and Pernici (2013), arXiv 1305.7028 | lower bound and series estimate | lower bound 0.662798966; Pade estimate 0.662798972(1) | https://arxiv.org/abs/1305.7028 | 2026-10-19T03:57:23Z (contributor's team) |
| Finch, arXiv 2001.00578 | abstract page only | 0.66279897 as quoted by the bank, not independently confirmed | https://arxiv.org/abs/2001.00578 | 2026-10-19T03:57:22Z (contributor's team) |
| OEIS digit searches for 6627989728337 and 1940215351483, and A028420 | any entry holding the digits | none found (empty results); A028420 is the matchings count, not the constant | https://oeis.org/A028420 | 2026-10-19T04:38:07Z (novelty skeptic) |

Friedland and Peled certify 8 decimals; Kong's 12 printed decimals are numerical, with a bracket that is not a proof. The enclosure here lies inside Kong's bracket and certifies 13 decimals. Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

Companion package: the same team also submitted a second package for the same target, `md-digits-36` (a numerical value of h2 to 36 decimals by two methods, no error bound). It is a separate claim. This package does not depend on it, and it does not make this enclosure wider than 13 decimals.

## Not claimed

- No claim on the main 20-decimal criterion of the target; that is the other package.
- Nothing beyond 13 decimals. The contributor's wider, unshipped 15-decimal enclosure is context only and is not part of this claim.
- No claim on novelty beyond the quoted comparators. The literature search covered arXiv, OEIS and this repository; Google Scholar and a general web search were not made.
- Not peer reviewed. The panel skeptics and the builder are the same model family (Claude); the proofs and checker were reviewed before the panel by a model of a different family.

## Credits

- **S. Friedland and U. N. Peled**, Adv. Appl. Math. 34 (2005), https://arxiv.org/abs/math/0402009: the rigorous transfer-matrix bounds, and the 8 certified decimals this package is compared against. Our two inequalities are proved from the definitions in `object/PROOF.md` and agree with theirs.
- **Yong Kong**, Phys. Rev. E 74, 061102 (2006), https://arxiv.org/abs/cond-mat/0610690: the 2006 value 0.662798972834 and its bracket.
- **D. Butera, P. Federbush and M. Pernici**, arXiv 1305.7028 (2013), https://arxiv.org/abs/1305.7028: the lower bound and the Pade estimate 0.662798972(1).
- **R. J. Baxter**, corner transfer matrices (Baxter 1968 and later work): the method behind the corner transfer matrix computation, and the earlier 8-digit value Kong credits.
- **P. Wynn**, the epsilon algorithm for sequence acceleration.
- **OEIS A028420**, number of monomer-dimer tilings of an n x n chessboard, https://oeis.org/A028420: used by the checker to test the matching counts.
- **S. R. Finch**, arXiv 2001.00578, https://arxiv.org/abs/2001.00578: errata page, abstract only.
- Contributor credit: `calgulbenkian`.
