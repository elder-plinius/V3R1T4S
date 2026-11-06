# Entanglement-assisted qutrit code `[[33, 7, 15; 12]]_3` (table: `14-23`)

## What

The 38 x 66 GF(3) stabilizer matrix S in object/eaqecc_33_7_15_12.json has 38 independent rows, c = rank(S J S^T)/2 = 12 and k = n - s + c = 7 at n = 33, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 15, strictly above d_lower = 14 and at most d_upper = 23 of the cell [[33,7,14-23;12]]_3 listed on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T21:29:07Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-24T21:38:48Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256`.

Path note: the sentence above, the panel files and `how-we-built-it/PREREG.md` refer to the run's claim folder, whose
root is this package's root. There, `claim/object/eaqecc_33_7_15_12.json` is `object/eaqecc_33_7_15_12.json` (same
sha256), `CLAIM.md` is `README.md`, `REPRODUCE.md` is `RUN_IT_YOURSELF.md`, `checkers/` is `verify-it-yourself/` and
`rebuild/` is `how-we-built-it/`. `claim/table/` (the fetched page) is not shipped; its URL, fetch times, sha256 and
the listed row are in `the-record-we-beat/README.md`. Work files and folders named there (`panel/claim.sha256`,
`panel/main_session_notes.txt`, `self_break/`, `data/gate_fetch/`, `attempts/`, `objects/`, and the skeptics' `mine/`,
`run/`, `author_run/`, `work-criterion/`, `fetched/` and `scripts/`) are not shipped. Dated run and folder names ("run" or
"folder" followed by a date and time, or by a four-digit time alone) name runs of the contributor's workspace, which are not shipped either.

The code is a Construction X code over GF(9) from two algebraic-geometry codes of the Hermitian curve
`y^3 + y = x^4` whose divisors are supported on a place `Q` of degree 3 and the point at infinity:
`C(D_28, 4Q + 4P_inf)` `[28, 14, 12]_9` contains `C(D_28, 3Q + 4P_inf)` `[28, 11, 15]_9`, glued to a `[5, 3, 3]_9`
Reed-Solomon tail, with a column sign pattern chosen so that the Hermitian hull has dimension 7 (the maximum over every
Construction X code of this pair according to how-we-built-it/hullbound.c; this bound is unverified contributor
text, and the claim does not depend on it). The result is a `[33, 14, 15]_9` code with Hermitian hull 7, which gives
`[[33, 14 - 7, 15; 33 - 14 - 7]]_3 = [[33, 7, 15; 12]]_3`. The object holds the GF(9) generator `G9`, its Hermitian
dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 7 seconds with 3 free cores (6.89 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, recovers from `S` the GF(9)-linear `[33, 14]` code `C` with
`phi(C) = span(S)^perp` (so symplectic weight there is Hamming weight on `C`), checks every one of the
818,809,200 sets of 19 coordinates for an information set of `C` (none fails, so every nonzero vector of
`span(S)^perp` has weight at least 15), and checks an explicit weight-15 vector of `span(S)^perp` outside `span(S)`
(so `d <= 15`). It then proves `d >= 15` a second way without any codeword search (`goppa_x.py`: the head and
zero-tail codes are identified exactly as the two AG codes, the Goppa bound gives 12 and 15, and Construction X gives
`min(15, 12 + 3) = 15`). `RUN_IT_YOURSELF.md` has the expected output and two more independent exact checks (a GF(3)
position-subset rank test over all 818,809,200 sets of 14 positions, about 12 minutes, and a Brouwer-Zimmermann
distance computation, about 15 seconds).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=33, k=7, c=12)` | `[[33,7,14-23;12]]_3` (`d_lower = 14, d_upper = 23`) | `[[33, 7, 15; 12]]_3` (`d = 15`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T21:38:48Z |

Details, HTTP headers, page hash and the listed `(33, 7)` row are in `the-record-we-beat/README.md`.

The classical code behind it is listed but not at this hull: `codetables.de` lists `[33,14]` over GF(9) at 15-18
(Construction X on the same kind of AG codes). The qutrit table's `[[33,12,15;17]]_3` has the parameters a
`[33,14,15]_9` code with Hermitian hull 2 would give (the table credits it to arXiv:2207.05647 without naming the code,
so reading it as such a code is an inference); the table lists 14 at every cell that hulls 3 to 7 would
reach (`(33,11,16)`, `(33,10,15)`, `(33,9,14)`, `(33,8,13)`, `(33,7,12)`). The closure of the table under its own
propagation rules, of the codes in this repository's open pull requests (#710's `[[33,8,16;15]]_3` included) and of
the newest qutrit EA codes the NOVELTY skeptic found (arXiv:2607.02170, July 2026, length at most 25) gives at most
14 at this cell.

## Not claimed

- Optimality for `(n=33, k=7, c=12)` is not claimed; the table's upper bound is 23.
- Only cell `(n=33, k=7, c=12)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[34,7,15;12]]_3` to `[[36,7,15;12]]_3` by lengthening, and
  `[[33,8,15;13]]_3`, `[[33,9,15;14]]_3`, `[[33,10,15;15]]_3`, `[[33,11,15;16]]_3` by increasing dimension) are not
  claimed here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction, Construction X and AG
  codes from places of higher degree are published. The classical `[33, 14, 15]_9` code is not ours either:
  `codetables.de` lists it (Construction X on the same kind of AG codes). What is new is a version of it with
  Hermitian hull 7, and the qutrit EA code it gives.
- The NOVELTY skeptic read abstracts for most papers (the full text only for arXiv:2607.02170); four journal-only
  papers were judged from abstracts and from the codes later papers cite from them, journal papers without an arXiv
  version may be missed, and closed or merged pull requests were checked through the repository's search (one,
  #331) and `known-knowns/` folder.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- The leads `[[33,9,14;12]]_3` and `[[33,3,20;18]]_3` named in `panel/gate.md` are not claimed here.
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.

Corrections to the panel text:
- `panel/gate.md` and `panel/novelty.md` say the qutrit table uses the `[33,14,15]_9` code type only at hull 2 (its
  `[[33,12,15;17]]_3`). The table does not name that code; the entry only has the parameters such a code would give.
- "Listed since 2003" (`panel/gate.md`) and "since 2003" (`panel/novelty.md`) refer to the `codetables.de` page's
  "last modified: 2003-10-23".

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
  https://arxiv.org/abs/1812.05312, https://doi.org/10.1007/s11128-019-2234-5.
- **Cunsheng Ding, Harald Niederreiter, and Chaoping Xing**, "Some new codes from algebraic curves", *IEEE
  Transactions on Information Theory* 46(7) (2000) 2638-2642, https://doi.org/10.1109/18.887873, the reference `codetables.de` gives for its `[33, 14, 15]_9` construction (Construction X with
  algebraic-geometry codes from divisors of degree 3 and 4).
- **V. D. Goppa** (algebraic-geometry codes) and **Henning Stichtenoth** (Hermitian codes), whose distance bound
  gives `d >= 28 - deg` for the two AG codes, and **N. J. A. Sloane, S. M. Reddy and C.-L. Chen** (Construction X).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the fourth distance check (bz64)
  uses.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
