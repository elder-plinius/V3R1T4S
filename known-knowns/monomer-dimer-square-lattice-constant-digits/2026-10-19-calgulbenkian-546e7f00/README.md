# Monomer-dimer entropy of the square lattice: 36 decimals of h2 by two methods

## What

The numerical value h2 = 0.662798972833745915155196234397725566 (36 decimals, natural log per site) is reproduced from the shipped data and agrees numerically between the corner-transfer-matrix ladder (four rungs sharing 43 decimals, 30 under the pre-registered stop rule) and the open-strip Wynn extrapolation (four truncations sharing 36 decimals), with no error bound, and exceeds every published value found in arXiv and OEIS searches (Google Scholar not searched).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.9 or later, standard library only.
- **Rough laptop time**: a few seconds, negligible memory.
- **Expected last line**: `PASS`

The check re-derives the decimals shared by the two methods from the shipped data. It does not recompute the eigenvalues or the corner transfer matrix; the commands for that are in `RUN_IT_YOURSELF.md` and `how-we-built-it/README.md`.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Friedland and Peled, Adv. Appl. Math. 34 (2005), arXiv math/0402009 | certified decimals of h2 | 8 ("h2 = .66279897, correct to 8 decimal digits") | https://arxiv.org/abs/math/0402009 | 2026-10-19T04:38:44Z (novelty skeptic; the contributor's team fetched the pdf at 2026-10-19T03:44:36Z) |
| Kong, Phys. Rev. E 74, 061102 (2006), arXiv cond-mat/0610690 | printed value and bracket | 0.662798972834 (12 printed decimals, "11 correct digits"); bracket 0.662798972831 to 0.662798972845 from numerical cylinder values, not a proof | https://arxiv.org/abs/cond-mat/0610690 | 2026-10-19T04:38:06Z (abstract page) and 2026-10-19T04:38:50Z (pdf) |
| Butera, Federbush and Pernici (2013), arXiv 1305.7028 | lower bound and series estimate | lower bound 0.662798966; Pade estimate 0.662798972(1) | https://arxiv.org/abs/1305.7028 | 2026-10-19T03:57:23Z (contributor's team) |
| Finch, arXiv 2001.00578 | abstract page only | 0.66279897 as quoted by the bank, not independently confirmed | https://arxiv.org/abs/2001.00578 | 2026-10-19T03:57:22Z (contributor's team) |
| OEIS digit searches for 6627989728337 and 1940215351483, and A028420 | any entry holding the digits | none found (empty results); A028420 is the matchings count, not the constant | https://oeis.org/A028420 | 2026-10-19T04:38:07Z (novelty skeptic) |

Kong's printed value is 0.662798972834; the value here rounds at 12 decimals to it and lies inside his bracket. Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

Companion package: the same team also submitted a second package for the same target, `md-p1-enclosure-13` (a rigorous enclosure certifying 13 decimals of h2 from exact-integer certificates). It is a separate claim. This package does not depend on it.

## Not claimed

- No rigorous error bound. The 36 decimals are numerical agreement of two methods; the only rigorous statement is the separate 13-decimal enclosure in the other package.
- Post-hoc elements, in plain words: (1) the first periodic-strip method, run exactly as pre-registered, reached only 15 decimals, so it is not one of the two methods; (2) a second periodic variant was chosen after we had seen the corner-transfer-matrix value, so it is not one of the two methods either; (3) the open-strip method's recipe was written before its data were computed, but its shape was borrowed from that second variant after the periodic data had been seen; (4) the corner-transfer-matrix ladder was extended past its pre-registered stop. Under the pre-registered stop rule alone that method gives 30 decimals; the 36 decimals rest on the extension.
- No claim from a general web search or Google Scholar: the literature search covered arXiv and OEIS only.
- Not peer reviewed. The panel skeptics and the builder are the same model family (Claude), disclosed in `panel/gate.md`.

## Credits

- **S. Friedland and U. N. Peled**, Adv. Appl. Math. 34 (2005), https://arxiv.org/abs/math/0402009: the rigorous transfer-matrix bounds (8 certified decimals). Their inequalities underlie the companion package on this target, which proves a 13-decimal enclosure; this package compares its numerical digits with Kong's 12.
- **Yong Kong**, Phys. Rev. E 74, 061102 (2006), https://arxiv.org/abs/cond-mat/0610690: the 2006 value 0.662798972834 and its bracket.
- **D. Butera, P. Federbush and M. Pernici**, arXiv 1305.7028 (2013), https://arxiv.org/abs/1305.7028: the lower bound and the Pade estimate 0.662798972(1).
- **R. J. Baxter**, corner transfer matrices (Baxter 1968 and later work): the method behind the corner transfer matrix computation, and the earlier 8-digit value Kong credits.
- **P. Wynn**, the epsilon algorithm for sequence acceleration.
- **OEIS A028420**, number of monomer-dimer tilings of an n x n chessboard, https://oeis.org/A028420: used by the checker to test the matching counts.
- **S. R. Finch**, arXiv 2001.00578, https://arxiv.org/abs/2001.00578: errata page, abstract only.
- Contributor credit: `calgulbenkian`.
