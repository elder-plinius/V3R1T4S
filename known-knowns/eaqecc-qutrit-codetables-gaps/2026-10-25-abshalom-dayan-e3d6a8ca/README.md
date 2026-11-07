# Entanglement-assisted qutrit code `[[35, 7, 16; 14]]_3` (table: `15-26`)

## What

The 42 x 70 GF(3) stabilizer matrix S in claim/object/eaqecc_35_7_16_14.json (sha256 e3d6a8ca...b73b4) has 42 independent rows and rank(S J S^T) = 28, so it defines a non-catalytic entanglement-assisted qutrit code with n = 35, c = 14, k = 7 whose minimum distance (minimum symplectic weight over span(S)^perp outside span(S) ∩ span(S)^perp) is exactly 16, which is strictly above d_lower = 15 and at most d_upper = 26 of the listed cell [[35,7,15-26;14]]_3 on https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T03:52:24Z (HTTP 200, sha256 37bbf731...936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-25T04:58:16Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4`, and the table page's full SHA-256 is
`37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`.

Path note: claim/object/eaqecc_35_7_16_14.json in the sentence above and in the panel files is
object/eaqecc_35_7_16_14.json here. The other run-folder paths in the panel files and how-we-built-it/PREREG.md
(claim/, fetched/qutrit.php, panel/claim.sha256, self_break/, mine/, panel/cutoff-0334/, and work folders such as
scripts/, data/ and attempts/) are not shipped; in claim/, CLAIM.md is README.md, REPRODUCE.md is
RUN_IT_YOURSELF.md, checkers/ is verify-it-yourself/ and rebuild/ is how-we-built-it/. The numbered runs and run
folders named in the panel files and PREREG.md are the contributor's other runs of the same kit; they are not shipped. data/gate_fetch/ (the gate's re-fetch folder) is not shipped either.

The code is a Construction X code over GF(9) from two algebraic-geometry codes of the Hermitian curve
`y^3 + y = x^4` whose divisors are supported on a place `Q` of degree 4 and the point at infinity:
`C(D_28, 2Q + 8P_inf)` `[28, 14, 12]_9` contains `C(D_28, Q + 8P_inf)` `[28, 10, 16]_9`, glued to a `[7, 4, 4]_9`
Reed-Solomon tail, with a column sign pattern chosen so that the Hermitian hull has dimension 7 (the maximum
over every Construction X code of this pair according to how-we-built-it/hullbound4.c; contributor text, unverified). The result is a `[35, 14, 16]_9` code with Hermitian hull 7, which
gives `[[35, 14 - 7, 16; 35 - 14 - 7]]_3 = [[35, 7, 16; 14]]_3`. The object holds the GF(9) generator `G9`, its
Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 21 seconds (21.40 s measured) on one core (see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, recovers from `S` the GF(9)-linear `[35, 14]` code `C` with
`phi(C) = span(S)^perp` (so symplectic weight there is Hamming weight on `C`), checks every one of the
3,247,943,160 sets of 20 coordinates for an information set of `C` (none fails, so every nonzero vector of
`span(S)^perp` has weight at least 16), and checks an explicit weight-16 vector of `span(S)^perp` outside `span(S)`
(so `d <= 16`). It then proves `d >= 16` a second way without any codeword search (`goppa_x4.py`: the head and
zero-tail codes are identified exactly as the two AG codes on a degree-4 place, the Goppa bound gives 12 and 16, and
Construction X gives `min(16, 12 + 4) = 16`). `RUN_IT_YOURSELF.md` has the expected output and more independent exact
checks (a GF(3) position-subset rank test over all 3,247,943,160 sets of 15 positions and a Brouwer-Zimmermann
distance computation).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=35, k=7, c=14)` | `[[35,7,15-26;14]]_3` (`d_lower = 15, d_upper = 26`) | `[[35, 7, 16; 14]]_3` (`d = 16`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-25T04:58:16Z (gate; the same page at 02:35:12Z, 03:37:49Z and 03:52:24Z) |

Details, HTTP headers, page hash and the listed `(35, 7)` row are in `the-record-we-beat/README.md`.

The classical distance is not new: `codetables.de` lists `[35,14]` over GF(9) at 16-19
(https://codetables.de/BKLC/BKLC.php?q=9&n=35&k=14: a shortened, punctured `[37,15,17]` code of Xing and Ling). What
is new is a `[35,14,16]_9` code with Hermitian hull 7, and the qutrit EA code it gives. The closure of the table
under its own propagation rules, of the codes in this repository's open pull requests (none at n = 35 or 36), of
this workspace's other codes and of the literature the NOVELTY skeptic found gives at most 15 at this cell
(the newest qutrit EA codes it found, arXiv:2607.02170 of July 2026, have length at most 25). The same row lists `[[35,7,16-26;15]]_3`, so d = 16 was known only with one more entangled pair. The code of open pull request #721,
`[[33,7,15;12]]_3`, lengthens to `[[35,7,15;12]]_3`, which does not reach d = 16 at `(35,7,14)`.

## Not claimed

- Optimality for `(n=35, k=7, c=14)` is not claimed; the table's upper bound is 26.
- Only cell `(n=35, k=7, c=14)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[36,7,16;14]]_3` by lengthening, above the listed 15-27) are not claimed
  here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction, Construction X and AG
  codes from places of higher degree are published. The classical parameters `[35, 14, 16]_9` are not ours either.
- The table also has cells marked "using teleportation" (`c = k`). If they were fed into the page's six propagation
  rules this cell would get 27, but the same seeding pushes 2700 listed cells above their own upper bounds, so the
  page does not propagate them; this package follows the page.
- The NOVELTY skeptic searched by web search and single abstract pages (the arXiv API answered HTTP 429 and was
  not retried) and read the full text of arXiv:2607.02170; the journal-only paper of Cao, Li and Zhu (IEEE TIT 2025)
  was judged from the codes arXiv:2607.02170 cites from it, and journal papers without an arXiv version may be missed.
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
- **Chaoping Xing and San Ling**, "A class of linear codes with good parameters", *IEEE Transactions on Information
  Theory* 46 (2000) 2184-2188, https://doi.org/10.1109/18.868488, and "A class of linear codes with good parameters
  from algebraic curves", *IEEE Transactions on Information Theory* 46 (2000) 1527-1532 (listed at
  https://personal.ntu.edu.sg/lingsan/publications.html), the references `codetables.de` gives for its `[35, 14, 16]_9`.
- **Cunsheng Ding, Harald Niederreiter, and Chaoping Xing**, "Some new codes from algebraic curves", *IEEE
  Transactions on Information Theory* 46 (2000) 2638-2642, https://doi.org/10.1109/18.887873 (Construction X with
  algebraic-geometry codes from places of higher degree).
- **V. D. Goppa** (algebraic-geometry codes, https://en.wikipedia.org/wiki/Algebraic_geometry_code) and **Henning
  Stichtenoth**, "A note on Hermitian codes over GF(q^2)", *IEEE Transactions on Information Theory* 34 (1988)
  1345-1348, https://doi.org/10.1109/18.21267, whose distance bound gives `d >= 28 - deg` for the two AG
  codes, and **N. J. A. Sloane, S. M. Reddy and C.-L. Chen**, "New binary codes", *IEEE Transactions on Information
  Theory* 18 (1972) 503-510, https://doi.org/10.1109/TIT.1972.1054833 (Construction X).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the bz64 distance check uses (as
  described by Hernando, Igual and Quintana-Orti, https://arxiv.org/abs/1603.06757).
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
