# Entanglement-assisted qutrit code `[[33, 8, 16; 15]]_3` (table: `15-23`)

## What

The 40 x 66 GF(3) matrix S in claim/object/eaqecc_33_8_16_15.json (sha256 763a503e8ca0560a07e6c650f172b8de932bfd91474eafc5302c6a00013ab459) has rank 40 and rank(S J S^T) = 30, so it defines a non-catalytic EAQECC with (n,k,c) = (33,8,15) whose exact minimum distance (minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp) is 16, strictly above the d_lower = 15 and within the d_upper = 23 of the listed cell [[33,8,15-23;15]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T19:06:27Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-24T19:23:20Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`763a503e8ca0560a07e6c650f172b8de932bfd91474eafc5302c6a00013ab459`.

Path note: the sentence above, the panel files and how-we-built-it/PREREG.md refer to the run's claim folder and
work folders. There, claim/object/ is object/, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md,
checkers/ is verify-it-yourself/ and rebuild/ is how-we-built-it/; claim/table/qutrit.php is the table page itself,
whose fetch record and sha256 are in the-record-we-beat/README.md. Work files and folders named there (for example
panel/claim.sha256, self_break/, mine/, repro/, fetched/, data/gate_fetch/ and attempts/constructor/) are not
shipped. The numbered runs named in PREREG.md (runs 1253, 1500 and 1640, also written 2026-10-24-1640) are the
contributor's earlier runs of the same kit; their folders are not shipped.

The code is a Construction X code over GF(9) from two algebraic-geometry codes of the Hermitian curve
`y^3 + y = x^4` whose divisors are supported on a place `Q` of degree 3 and the point at infinity:
`C(D_28, 4Q + 3P_inf)` `[28, 13, 13]_9` contains `C(D_28, 3Q + 3P_inf)` `[28, 10, 16]_9`, glued to a `[5, 3, 3]_9`
Reed-Solomon tail, with a column sign pattern chosen so that the Hermitian hull has dimension 5. The result is a
`[33, 13, 16]_9` code with Hermitian hull 5, which gives `[[33, 13 - 5, 16; 33 - 13 - 5]]_3 = [[33, 8, 16; 15]]_3`.
The object holds the GF(9) generator `G9`, its Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over
GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 5 seconds with 3 free cores (4.58 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, recovers from `S` the GF(9)-linear `[33, 13]` code `C` with
`phi(C) = span(S)^perp` (so symplectic weight there is Hamming weight on `C`), checks every one of the
1,037,158,320 sets of 18 coordinates for an information set of `C` (none fails, so every nonzero vector of
`span(S)^perp` has weight at least 16), and checks an explicit weight-16 vector of `span(S)^perp` outside `span(S)`
(so `d <= 16`). `RUN_IT_YOURSELF.md` has the expected output and a second, independent exact check (a GF(3)
position-subset rank test over all 1,037,158,320 sets of 15 positions, about 5 to 6 minutes with 3 cores).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=33, k=8, c=15)` | `[[33,8,15-23;15]]_3` (`d_lower = 15, d_upper = 23`) | `[[33, 8, 16; 15]]_3` (`d = 16`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T19:23:20Z |

Details, HTTP headers, page hash and the listed `(33, 8)` row are in `the-record-we-beat/README.md`.

The classical code behind it is listed but not at this hull: the table already uses a `[33,13,16]_9` code at
Hermitian hull 2 (its `[[33,11,16;18]]_3`, from arXiv:2207.05647) and lists only 15 at the cells hulls 4 and 5
would reach (`(33,9,16)`, `(33,8,15)`); `codetables.de` lists `[33,14]` over GF(9) at 15-18, so no listed
code of larger dimension reaches d = 16 there. The newest qutrit EA codes the NOVELTY skeptic found (arXiv:2607.02170,
July 2026) have length at most 25, and none of them, nor any code in this repository's open pull requests, reaches
16 at this cell through the table's rules.

## Not claimed

- Optimality for `(n=33, k=8, c=15)` is not claimed; the table's upper bound is 23.
- Only cell `(n=33, k=8, c=15)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[34,8,16;15]]_3` to `[[36,8,16;15]]_3` by lengthening, and
  `[[33,9,16;16]]_3` by increasing dimension) are not claimed here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction, Construction X and AG
  codes from places of higher degree are published. The classical `[33, 13, 16]_9` code is not ours either:
  `codetables.de` lists it (Construction X on the same kind of AG codes). What is new is a version of it with
  Hermitian hull 5, and the qutrit EA code it gives.
- The NOVELTY skeptic read abstracts for most papers (the full qutrit table only for arXiv:2607.02170);
  journal-only papers may be missed, and closed or merged pull requests were checked only through the repository's
  `known-knowns/` folder.
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
  https://arxiv.org/abs/1812.05312.
- **Cunsheng Ding, Harald Niederreiter, and Chaoping Xing**, "Some new codes from algebraic curves", IEEE Trans.
  Inform. Theory 46(7) (2000) 2638-2642, https://doi.org/10.1109/18.887873, the reference `codetables.de` gives for its `[33, 13, 16]_9` construction (Construction X with
  algebraic-geometry codes from a divisor of degree 3).
- **V. D. Goppa** (algebraic-geometry codes) and **Henning Stichtenoth** (Hermitian codes), whose distance bound
  gives `d >= 28 - deg` for the two AG codes, and **N. J. A. Sloane, S. M. Reddy and C.-L. Chen** (Construction X).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the third distance check (bz64)
  uses.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
