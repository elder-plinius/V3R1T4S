# Entanglement-assisted qutrit code `[[28, 7, 13; 9]]_3` (table: `12-18`)

## What

The 30 x 56 GF(3) stabilizer matrix S in claim/object/eaqecc_28_7_13_9.json (sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78) has s = 30 independent rows, rank(S J S^T) = 18 (c = 9) and k = 7, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 13, which is strictly above d_lower = 12 and within d_upper = 18 of the cell [[28,7,12-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-25T00:41:55Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-25T00:49:54Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78`.

Path note: the object the sentence names as `claim/object/eaqecc_28_7_13_9.json` is `object/eaqecc_28_7_13_9.json`
in this package (same sha256). More generally, the panel files, `how-we-built-it/PREREG.md` and `how-we-built-it/PREREG_found_run.md` refer to
the run's claim folder, whose root is this package's root: there, `CLAIM.md` is `README.md`, `REPRODUCE.md` is `RUN_IT_YOURSELF.md`,
`checkers/` is `verify-it-yourself/` and `rebuild/` is `how-we-built-it/`. Work files and folders named there
(`panel/claim.sha256`, `self_break/`, `data/gate_fetch/`, `attempts/`, `objects/`, and the skeptics' `mine/`,
`author_run/`, `fetched/` and `scripts/`) are not shipped. Dated run and folder names ("run" or "folder" followed by a
date and time, or by a four-digit time alone) name runs of the contributor's workspace, which are not shipped either.

The code comes from the extended one-point Hermitian code `E_15` on `y^3 + y = x^4` over GF(9) (the 27 affine
points plus a coordinate for the point at infinity): a `[28, 13, 13]_9` code whose natural Hermitian hull (no column
scaled) has dimension 6. That gives `[[28, 13 - 6, 13; 28 - 13 - 6]]_3 = [[28, 7, 13; 9]]_3`. The object holds the
GF(9) generator `G9`, its Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 9 seconds with 3 free cores (8.77 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks every one of the 30,421,755 sets of 12 positions by exact GF(3) ranks
(no vector of `span(S)^perp` outside the isotropic part fits inside any of them, so `d >= 13`), and checks an explicit
weight-13 vector of `span(S)^perp` outside `span(S)` (so `d <= 13`). It then proves `d >= 13` a second way without any
codeword search (`onepoint_check.py`: `span(S)^perp` is exactly `phi(E_15)`, and a function with at most 15 poles at
infinity has at most 15 zeros, so every nonzero word of `E_15` has weight at least 13). `RUN_IT_YOURSELF.md` has the
expected output and a further independent exact check (a GF(9) information-set test over all 30,421,755 sets of 16
columns).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=28, k=7, c=9)` | `[[28,7,12-18;9]]_3` (`d_lower = 12, d_upper = 18`) | `[[28, 7, 13; 9]]_3` (`d = 13`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-25T00:49:54Z |

Details, HTTP headers, page hash and the listed `(28, 7)` row are in `the-record-we-beat/README.md`.

The classical code behind it is listed but not at this hull: `codetables.de` lists `[28,13]` over GF(9) at 13-14 (an
AG code on the Hermitian curve), and the qutrit table uses a `[28,13,13]_9` code at Hermitian hull 3, as
`[[28,10,13;12]]_3`. The closure of the table under its own propagation rules, of the codes in this repository's open
pull requests (#645's `[[28,7,14;11]]_3` and #646's `[[28,6,12;6]]_3` included), of the length-27 one-point Hermitian
EA codes (Christensen, Munuera, Pereira, Ruano) and of the newest qutrit EA codes the NOVELTY skeptic found
(arXiv:2607.02170, July 2026, length at most 25) gives at most 12 at this cell. The same row lists
`[[28,7,13-19;11]]_3`, so d = 13 was known only with two more entangled pairs.

## Not claimed

- Optimality for `(n=28, k=7, c=9)` is not claimed; the table's upper bound is 18.
- Only cell `(n=28, k=7, c=9)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[29,7,13;9]]_3` and `[[30,7,13;9]]_3` by lengthening) are not claimed here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction and one-point Hermitian
  EA codes are published. The classical `[28, 13, 13]_9` code is not ours either: `codetables.de` lists it (an AG code
  on the Hermitian curve). What is new is the qutrit EA code from its hull of dimension 6. The code is the one-column
  extension of the length-27 one-point Hermitian code `[[27,6,13;9]]_3` of Christensen, Munuera, Pereira and Ruano
  (arXiv:2105.02166): one more qutrit and one more logical qutrit at the same d and c. No rule of the table gives
  `(28,7,9)` at d = 13 from it. arXiv:2607.02170 extends one-point Hermitian codes in the same way, but all its qutrit
  codes have n <= 26.
- The table also has cells marked "using teleportation" (`c = k`). If they were fed into the page's six propagation
  rules this cell would get 24, but the same seeding pushes 2700 listed cells above their own upper bounds, so the
  page does not propagate them; this package follows the page.
- The NOVELTY skeptic could not read the table's source paper (arXiv:2207.05647) as HTML (HTTP 404; its codes are on
  the table) and judged journal-only papers (IEEE TIT 2025, IJTP 2024, Discrete Mathematics 2024, AMC 2025) from the
  codes arXiv:2607.02170 cites from them; journal papers without an arXiv version may be missed.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and
  https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/).
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting
  codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024),
  https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647), whose Hermitian
  construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code, whose
  one-column extension (Proposition 10) raises a hull, and whose propagation rules the table uses.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314,
  436-439 (2006), https://arxiv.org/abs/quant-ph/0610092.
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum
  error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019),
  https://doi.org/10.1007/s11128-019-2234-5 (preprint https://arxiv.org/abs/1812.05312).
- **Christensen, Munuera, Pereira, and Ruano**, entanglement-assisted quantum codes from one-point Hermitian codes,
  https://arxiv.org/abs/2105.02166 (Advances in Mathematics of Communications 17(1), 2023): the length-27 family
  this code extends, and the comparison above.
- **V. D. Goppa** (algebraic-geometry codes, https://en.wikipedia.org/wiki/Algebraic_geometry_code) and **Henning
  Stichtenoth**, "A note on Hermitian codes over GF(q^2)", *IEEE Transactions on Information Theory* 34 (1988)
  1345-1348, https://doi.org/10.1109/18.21267, whose distance bound
  gives `d >= 28 - m` for the extended code `E_m`.
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the panel's bz64 distance check
  (`panel/criterion.md`; bz64.c is not shipped in this package, and the shipped checks establish d = 13 without it) uses (as described by Hernando, Igual and Quintana-Orti, https://arxiv.org/abs/1603.06757).
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
