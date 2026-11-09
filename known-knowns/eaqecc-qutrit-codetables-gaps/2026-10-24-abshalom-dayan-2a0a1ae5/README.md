# Entanglement-assisted qutrit code `[[28, 9, 11; 7]]_3` (table: `10-14`)

## What

The 26 x 56 GF(3) matrix S in object/eaqecc_28_9_11_7.json defines a [[28,9,11;7]]_3 EAQECC: it has 26 independent rows, rank(S J S^T) = 14 (c = 7) and k = 9, and its distance is exactly 11 as the minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp (exhaustive over all 10-position subsets plus an explicit weight-11 non-isotropic witness), which is strictly above the d_lower = 10 and within the d_upper = 14 of the listed cell [[28,9,10-14;7]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-24T17:42:49Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-24T17:49:29Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0`.

Path note: the panel files and how-we-built-it/PREREG*.md refer to the run's claim folder and work folders. There,
claim/object/ is object/, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md and rebuild/ is
how-we-built-it/; claim/table/RECORD.md is summarized in the-record-we-beat/README.md (the saved page
claim/table/qutrit.php is not shipped). Work files and folders named there (panel/claim.sha256, self_break/, mine/,
scripts/, fetched/, closure_result*.txt and runs/) are not shipped, and the numbered runs named there (for example
2026-10-24-0924, 2026-10-24-1033, 2026-10-24-1640, also written as run 1033) are the contributor's runs of the kit. In the panel files checkers/ is verify-it-yourself/, and data/gate_fetch/ (the gate's re-fetch folder) is not shipped either.

The code comes from the extended one-point Hermitian code `E_17` on `y^3 + y = x^4` over GF(9): a `[28, 15, 11]_9`
code whose natural Hermitian hull has dimension 6 (the maximum over all column sign patterns according to the contributor's search; unverified). That gives
`[[28, 15 - 6, 11; 28 - 15 - 6]]_3 = [[28, 9, 11; 7]]_3`. The object holds the GF(9) generator `G9`, its Hermitian
dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 4 seconds with 3 free cores (4.04 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks every one of the 13,123,110 sets of 10 positions by exact GF(3) ranks
(no vector of `span(S)^perp` outside the isotropic part fits inside any of them, so `d >= 11`), and checks an explicit
weight-11 vector of `span(S)^perp` outside `span(S)` (so `d <= 11`). `RUN_IT_YOURSELF.md` has the expected output and a
second, independent exact check (a GF(9) information-set test over all 13,123,110 sets of 18 columns, under a second).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=28, k=9, c=7)` | `[[28,9,10-14;7]]_3` (`d_lower = 10, d_upper = 14`) | `[[28, 9, 11; 7]]_3` (`d = 11`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T17:49:29Z |

Details, HTTP headers, page hash and the listed `(28, 9)` row are in `the-record-we-beat/README.md`.

Published codes that the table does not list: the plain one-point Hermitian EA codes of length 27 (Christensen,
Munuera, Pereira, Ruano) would need a `[27,15,11]_9` code to reach this cell, and codetables.de lists `[27,15]` over
GF(9) at 10-11 with no such code known; the table's source paper lists `[[28,9,12;9]]_3`, which needs more
entanglement (`c = 9`), and the table's rules never lower `c` without lowering `d` or `k`. The table already uses a
`[28,15,11]_9` code with Hermitian hull 4 (inferred from its `[[28,11,11;9]]_3` entry, not read from the source
paper); what is new is the hull of dimension 6.

## Not claimed

- Optimality for `(n=28, k=9, c=7)` is not claimed; the table's upper bound is 14.
- Only cell `(n=28, k=9, c=7)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[29,9,11;7]]_3` and `[[30,9,11;7]]_3` by lengthening, and others that
  also lie above listed values) are not claimed here.
- This is an improvement of the table cell, not a new technique: the Hermitian construction and one-point Hermitian
  EA codes are published. The classical `[28, 15, 11]_9` code is not ours either: `codetables.de` lists `[28,15]`
  over GF(9) at 11-12 with a Hermitian-curve AG code. What is new is the qutrit EA code from its hull of dimension 6.
- The NOVELTY skeptic could not read three journal-only qutrit papers (IEEE TIT 2025, AMC 2025, IJTP 2024); a
  July 2026 arXiv paper that compares against them states no qutrit code longer than 26. Closed pull requests were not
  searched.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The standalone checker is in `verify-it-yourself/`; the run's skeptic reports are in `panel/`.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and
  https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/).
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting
  codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024),
  https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647, titled "How Much
  Entanglement Does a Quantum Code Need?"), whose Hermitian
  construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code, whose
  one-column extension (Proposition 10) raises a hull, and whose propagation rules the table uses.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314,
  436-439 (2006), https://arxiv.org/abs/quant-ph/0610092.
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum
  error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019),
  https://arxiv.org/abs/1812.05312.
- **Christensen, Munuera, Pereira, and Ruano**, "An Algorithmic Approach to Entanglement-Assisted Quantum
  Error-Correcting Codes from the Hermitian Curve", Advances in Mathematics of Communications 17(1) (2023),
  https://doi.org/10.3934/amc.2021072 (preprint https://arxiv.org/abs/2105.02166): the length-27 family
  this code extends, and the comparison above.
- **V. D. Goppa** (algebraic-geometry codes) and **Henning Stichtenoth** (Hermitian codes), whose distance bound
  gives `d >= 28 - m` for the extended code `E_m`.
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm an earlier run's distance check
  (bz9) uses.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
