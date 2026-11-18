# Closing MinT Non-Digital Gap Cell `(b = 3, m = 11, s = 19)` at `t = 3`: Exact Rational `OOA(M, 19, S_3, 4, 8)` LP Dual Proof (`mint-net-below-digital-bound`, Partial Win `p1`)

## What

An exact rational dual solution of the depth-4, strength-8 OOA linear-programming bound (verified in Python Fractions and C99 128-bit integers) shows M >= 2403828588527406331/13544324988667 > 3^11 for OOA(M,19,S_3,4,8), so no (3,11,19)-net in base 3 exists, which makes MinT's general lower bound on t for that single cell at least 4 (it is 3 on the live page today), equal to the digital bound.

## Check it yourself

From this package folder (requires only Python 3 standard library and a C99 compiler `cc`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (verifies in both Python `fractions.Fraction` and standalone C99 `__int128` integer arithmetic that all `60` rational dual weights in `object/certificate_b3_m11_s19_t3.json` satisfy `u_f <= 0` for `|f| >= 9`, `1 + sum_f u_f K_f(X) >= 0` across all `8,854` non-diagonal agreement shapes of `OOA(M, 19, S_3, 4, 8)`, and `1 + sum_f u_f K_f(0, 0, 0, 0, 19) = 2403828588527406331 / 13544324988667 > 177,147 = 3^11`, proving no `(3, 11, 19)`-net in base `3` exists).

## Compared to

- **Live MinT query page**: http://mint.sbg.ac.at/query.php?b=3&s=19&m=11&p=smt (Rudolf Schurer and Wolfgang Ch. Schmid, University of Salzburg)
- **Fetched**: `2026-11-17T15:18:00Z` (`HTTP 200`, SHA-256 `9c138a9b22271f54ab1818ba33ecff9ed21603cce456cb91414caa924a1da399`)
- **Prior table bounds**: `Lower bound on t: 3` vs. `Lower bound on t (digital): 4` (`Best known t: 5`)

## Not claimed

- Does not construct a non-digital `(t, m, s)`-net beating MinT's digital lower bound (`Full Win`).
- Does not settle whether a `(4, 11, 19)`-net in base `3` exists (`4 <= t <= 5`).

## Credits

- **Rudolf Schurer and Wolfgang Ch. Schmid** (http://mint.sbg.ac.at/ and http://mint.sbg.ac.at/desc_OBoundLP.html), for the MinT database and OOA LP formulation.
- **William J. Martin and Douglas R. Stinson**, *Association schemes for ordered orthogonal arrays and `(t, m, s)`-nets*, Canad. J. Math. 51(2) (1999), 326-346, and **Jurgen Bierbrauer**, *A direct approach to linear programming bounds for codes and tms-nets*, Des. Codes Cryptogr. 42(2) (2007), 127-143.
- **Kenneth M. Lawrence** (1996) and **Gary L. Mullen and Wolfgang Ch. Schmid** (1996), for the equivalence between `(t, m, s)`-nets and ordered orthogonal arrays.
