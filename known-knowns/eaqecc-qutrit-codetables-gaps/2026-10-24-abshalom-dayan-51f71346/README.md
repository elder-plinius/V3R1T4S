# Entanglement-assisted qutrit code `[[28, 6, 12; 6]]_3` (table: `11-17`)

## What

object/eaqecc_28_6_12_6.json (sha256 51f713462c7db831...) gives a 28 x 56 GF(3) matrix S (rows (x|z), form x.z' - z.x') for which my own code, working from S alone, finds s = rank(S) = 28, c = rank(S J S^T)/2 = 6, k = n - s + c = 6 and d = 12 exactly (no vector of span(S)^perp outside span(S) ∩ span(S)^perp is supported on any of the 21474180 sets of 11 positions, and a symplectic-weight-12 vector orthogonal to every row of S and outside span(S) exists on 0-based positions 15 to 26), so it is an [[28,6,12;6]]_3 EAQECC whose distance is strictly above d_lower = 11 and at most d_upper = 17 of the listed cell [[28,6,11-17;6]]_3, as read both in the author's table copy (fetched 2026-10-24 15:03:31 UTC per RECORD.md and its saved server Date header, footer "Last change: 10.07.2025", sha256 37bbf731030c113e...) and in my single live re-fetch at 2026-10-24 16:07:32 UTC (HTTP 200, 628039 bytes, byte-identical to that copy).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
The gate re-read the page once more at 2026-10-24T16:14:13Z: same page hash, same cell
(`the-record-we-beat/README.md`). The object's full SHA-256 is
`51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573`.

Path note: the panel files and how-we-built-it/PREREG*.md refer to the run's claim folder and work folders. There,
claim/object/ is object/, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md, and claim/table/RECORD.md
(the "RECORD.md" of the sentence above) is summarized in the-record-we-beat/README.md (the saved page is not
shipped). Work files and folders named there (panel/claim.sha256, self_break/, mine/, scripts/, fetched/ and
work-novelty/) are not shipped, and the numbered runs named there (for example 2026-10-24-0924, 2026-10-24-1033 and
2026-10-24-1500, also written as run 1033) are the contributor's runs of the kit. data/gate_fetch/ (the gate's re-fetch folder) is not shipped either.

The code comes from the extended one-point Hermitian code `E_16` on `y^3 + y = x^4` over GF(9): a `[28, 14, 12]_9`
code whose Hermitian hull has dimension 8 (the maximum over all column sign patterns according to the contributor's search; unverified). That gives
`[[28, 14 - 8, 12; 28 - 14 - 8]]_3 = [[28, 6, 12; 6]]_3`. The object holds the GF(9) generator `G9`, its Hermitian
dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 5 seconds with 4 free cores (4.2 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks every one of the 21,474,180 sets of 11 positions by exact GF(3) ranks
(no vector of `span(S)^perp` outside the isotropic part fits inside any of them, so `d >= 12`), and checks an explicit
weight-12 vector of `span(S)^perp` outside `span(S)` (so `d <= 12`). `RUN_IT_YOURSELF.md` has the expected output and a
second, independent exact check (a GF(9) information-set test over all 21,474,180 sets of 17 columns, about 1 second).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=28, k=6, c=6)` | `[[28,6,11-17;6]]_3` (`d_lower = 11, d_upper = 17`) | `[[28, 6, 12; 6]]_3` (`d = 12`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T16:14:13Z |

Details, HTTP headers, page hash and the listed `(28, 6)` row are in `the-record-we-beat/README.md`.

Published codes that the table does not list: the plain one-point Hermitian EA codes of length 27 (Christensen,
Munuera, Pereira, Ruano) have `c >= 9` wherever `d >= 12` (for example `[[27,6,13;9]]_3`), and the table's rules
never lower `c`, so they give at most `d = 11` at `(28, 6, 6)`. The table's source paper lists `[[28,9,12;9]]_3`, from
a `[28,14,12]_9` code with Hermitian hull 5.

## Not claimed

- Optimality for `(n=28, k=6, c=6)` is not claimed; the table's upper bound is 17.
- Only cell `(n=28, k=6, c=6)` is claimed in this package (one cell per package). Cells that follow from it by the
  table's propagation rules (for example `[[28,7,12;7]]_3` and `[[28,8,12;8]]_3` by increasing dimension, which also
  lie above listed values) are not claimed here.
- Teleportation neighbour: the page lists `[[28,5,12-19;5]]_3` "using teleportation". The page's increasing-dimension
  rule would give these parameters if it applied to teleportation entries; the page does not apply it (the cell reads
  11), and the source paper states that rule only for pure codes from the Hermitian construction. This object is a
  stabilizer EAQECC whose `c` and `k` are computed from `S`.
- This is an improvement of the table cell, not a new technique: the Hermitian construction, one-point Hermitian EA
  codes and extending a code to raise its Hermitian hull are all published. The classical `[28, 14, 12]_9` code is
  not ours either: `codetables.de` lists `[28,14]` over GF(9) at 12-13 with a Hermitian-curve AG code. What is new is
  the qutrit EA code obtained from the extended code's hull of dimension 8.
- The NOVELTY skeptic could not read two qutrit stabilizer-code papers in full (one paywalled, one behind a bot
  check). They would matter only if they held a code such as `[[28,0,12]]_3` or `[[29,1,12]]_3`.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The standalone checker is in `verify-it-yourself/`; the run's skeptic reports are in `panel/`.

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
  https://arxiv.org/abs/1812.05312.
- **Christensen, Munuera, Pereira, and Ruano**, entanglement-assisted quantum codes from one-point Hermitian codes,
  https://arxiv.org/abs/2105.02166 (Advances in Mathematics of Communications 17(1), 2023): the length-27 family
  this code extends, and the comparison above.
- **V. D. Goppa** (algebraic-geometry codes) and **Henning Stichtenoth** (Hermitian codes), whose distance bound
  gives `d >= 28 - m` for the extended code `E_m`.
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm an earlier Brouwer-Zimmermann distance check of this code used.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
