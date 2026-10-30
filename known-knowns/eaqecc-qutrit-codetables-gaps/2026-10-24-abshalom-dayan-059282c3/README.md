# Entanglement-assisted qutrit code `[[33, 9, 14; 12]]_3` (table: `13-21`)

## What

The 36 x 66 GF(3) stabilizer matrix S in claim/object/eaqecc_33_9_14_12.json (sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391) defines a non-catalytic qutrit EAQECC with s = 36, c = 12, k = 9 and exact minimum distance d = 14 (minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 13 and at most d_upper = 21 for the listed cell [[33,9,13-21;12]]_3 of https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T22:29:54Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-24T22:41:24Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391`.

Path note: the sentence above, the panel files and how-we-built-it/PREREG.md refer to the run's claim folder and
work folders. There, claim/object/ is object/, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md,
checkers/ is verify-it-yourself/ and rebuild/ is how-we-built-it/; claim/table/ held the table page, whose fetch
record and sha256 are in the-record-we-beat/README.md. Work files and folders named there (for example
self_break/, mine/, run/, fetched/, scripts/, attempts/, data/ and data/gate_fetch/) are not shipped. The numbered
runs and run folders named there (for example 2026-10-24-1640, 2026-10-24-1727, 2026-10-24-1953 and
2026-10-24-2001, also written as run 1640) are the contributor's other runs of the same kit; they are not shipped. panel/claim.sha256 (the list of the claim folder's files) is not shipped either.

The code is a Construction X code over GF(9) from two algebraic-geometry codes of the Hermitian curve
`y^3 + y = x^4` whose divisors are supported on a place `Q` of degree 3 and the point at infinity:
`C(D_28, 3Q + 8P_inf)` `[28, 15, 11]_9` contains `C(D_28, 2Q + 8P_inf)` `[28, 12, 14]_9`, glued to a `[5, 3, 3]_9`
Reed-Solomon tail, with a column sign pattern chosen so that the Hermitian hull has dimension 6 (the maximum
over every Construction X code of this pair according to how-we-built-it/hullbound.c; contributor text, unverified). The result is a `[33, 15, 14]_9` code with Hermitian hull 6, which gives
`[[33, 15 - 6, 14; 33 - 15 - 6]]_3 = [[33, 9, 14; 12]]_3`. The object holds the GF(9) generator `G9`, its Hermitian
dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 9 seconds with 3 free cores (8.69 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, recovers from `S` the GF(9)-linear `[33, 15]` code `C` with
`phi(C) = span(S)^perp` (so symplectic weight there is Hamming weight on `C`), checks every one of the
573,166,440 sets of 20 coordinates for an information set of `C` (none fails, so every nonzero vector of
`span(S)^perp` has weight at least 14), and checks an explicit weight-14 vector of `span(S)^perp` outside `span(S)`
(so `d <= 14`). It then proves `d >= 14` a second way without any codeword search (`goppa_x.py`: the head and
zero-tail codes are identified exactly as the two AG codes, the Goppa bound gives 11 and 14, and Construction X gives
`min(14, 11 + 3) = 14`). `RUN_IT_YOURSELF.md` has the expected output and two more independent exact checks (a GF(3)
position-subset rank test over all 573,166,440 sets of 13 positions, about 12 minutes, and a Brouwer-Zimmermann
distance computation, a few seconds).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=33, k=9, c=12)` | `[[33,9,13-21;12]]_3` (`d_lower = 13, d_upper = 21`) | `[[33, 9, 14; 12]]_3` (`d = 14`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T22:41:24Z |

Details, HTTP headers, page hash and the listed `(33, 9)` row are in `the-record-we-beat/README.md`.

The classical code behind it is listed but not at this hull: `codetables.de` lists `[33,15]` over GF(9) at 14-17
(Construction X on the same kind of AG codes), and the qutrit table has d_lower 14 for a `[33,15]`-type code only
at the cells of Hermitian hulls 0, 1 and 2 (`(33,15,18)`, `(33,14,17)`, `(33,13,16)`, all 14-19).
The closure of the table under its own propagation rules, of the codes in this repository's open pull requests
(#710's `[[33,8,16;15]]_3` included), of codetables.de's qutrit stabilizer codes for n = 33 to 46 and of the newest
qutrit EA codes the NOVELTY skeptic found (arXiv:2607.02170, July 2026, length at most 25) gives at most 13 at this
cell. The same row lists `[[33,9,14-21;13]]_3`, so d = 14 was known only with one more entangled pair. The code of open
pull request #721, `[[33,7,15;12]]_3`, does not give d = 14 at `(33,9,12)` under the table's rules: its d = 15
reaches `(n,k,c) = (33,9,14)`, a different cell.

## Not claimed

- Optimality for `(n=33, k=9, c=12)` is not claimed; the table's upper bound is 21.
- Only cell `(n=33, k=9, c=12)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules are not claimed here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction, Construction X and AG
  codes from places of higher degree are published. The classical `[33, 15, 14]_9` code is not ours either:
  `codetables.de` lists it (Construction X on the same kind of AG codes). What is new is a version of it with
  Hermitian hull 6, and the qutrit EA code it gives.
- The construction string inside the object says the gluing matrix fills "rows 11..13 of the tail"; for this pair
  the rows are 12..14 (a text slip in the builder, checked; no value depends on it).
- The NOVELTY skeptic read abstracts for most papers (the full text for arXiv:2607.02170, arXiv:2501.04921 and
  arXiv:2608.09886); three paywalled journal papers (IEEE TIT 2025, AMC 2025, IJTP 2024) were judged from the codes
  arXiv:2607.02170 cites from them, and journal papers without an arXiv version may be missed.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The standalone checker is in `verify-it-yourself/`; the run's skeptic reports are in `panel/`.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and
  https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/).
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting
  codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024),
  https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647), whose Hermitian
  construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code, and whose
  propagation rules the table uses.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314,
  436-439 (2006), https://arxiv.org/abs/quant-ph/0610092.
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum
  error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019),
  https://doi.org/10.1007/s11128-019-2234-5 (preprint https://arxiv.org/abs/1812.05312).
- **Cunsheng Ding, Harald Niederreiter, and Chaoping Xing**, "Some new codes from algebraic curves", *IEEE Transactions on Information Theory* 46 (2000)
  2638-2642, https://doi.org/10.1109/18.887873, the reference `codetables.de` gives for its `[33, 15, 14]_9` construction (Construction X with
  algebraic-geometry codes from divisors of degree 3 and 5).
- **V. D. Goppa** (algebraic-geometry codes, https://en.wikipedia.org/wiki/Algebraic_geometry_code) and **Henning
  Stichtenoth**, "A note on Hermitian codes over GF(q^2)", *IEEE Transactions on Information Theory* 34 (1988)
  1345-1348, https://doi.org/10.1109/18.21267, whose distance bound
  gives `d >= 28 - deg` for the two AG codes, and **N. J. A. Sloane, S. M. Reddy and C.-L. Chen**, "New binary codes",
  *IEEE Transactions on Information Theory* 18 (1972) 503-510, https://doi.org/10.1109/TIT.1972.1054833 (Construction X).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the fourth distance check (bz64)
  uses (as described by Hernando, Igual and Quintana-Orti, https://arxiv.org/abs/1603.06757).
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
