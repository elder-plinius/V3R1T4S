# Entanglement-assisted qutrit code `[[28, 5, 15; 11]]_3` (table: `13-22`)

## What

claim/object/eaqecc_28_5_15_11.json (sha256 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434) holds a 34 x 56 GF(3) symplectic matrix S with n = 28, s = rank(S) = 34, c = rank(S J S^T)/2 = 11 >= 1 and k = n - s + c = 5 (recomputed by me), whose minimum symplectic weight over span(S)^perp minus span(S) ∩ span(S)^perp is at least 15 (I derived d >= 15 from the Hermitian one-point code structure, verified G9 against it, and tested the zero-count bound exhaustively for top pole order <= 10; d is exactly 15 per the author's checkers, which I read but did not rerun), which is strictly greater than d_lower = 13 and at most d_upper = 22 in the listed cell [[28,5,13-22;11]]_3 of claim/table/qutrit.php (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, server date 2026-10-24T10:36:29Z), with no neighbouring cell or legend rule on that saved page giving d_lower >= 15 for (28,5,11); a fresh live re-fetch at the moment of claiming is still owed by the claimer and was not done by me.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder (which held the saved table page; this package does not include the page). The live re-fetch it says was still owed was done at the gate, 2026-10-24T11:35:08Z, with the same page hash and the same cell (`panel/gate.md`, `the-record-we-beat/README.md`). In this package the same object file, with identical bytes (`sha256: 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434`), is `object/eaqecc_28_5_15_11.json`. The other run-folder names in the panel files and how-we-built-it/PREREG*.md:
in claim/, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md, checkers/ is verify-it-yourself/ (its
checkB_gf9.c is not shipped), rebuild/ is how-we-built-it/, and table/RECORD.md is summarized in
`the-record-we-beat/README.md` (the saved page table/qutrit.php is not shipped). Work files and folders named there
(panel/work-criterion/, panel/work-novelty/, panel/work-reproduce/, runs/, data/gate_fetch/) are not shipped, and the
numbered runs named there (2026-10-24-0924, which found the object, and 2026-10-24-1033, which rebuilt it and wrote
the panel files) are the contributor's runs of the kit. In the panel files claim/object/ is object/, and attempts/ is a work folder that is not shipped.

The code comes from the extended one-point Hermitian code `E_13` on `y^3 + y = x^4` over GF(9): a `[28, 11, 15]_9` code with Hermitian hull dimension 6, which gives `[[28, 11 - 6, 15; 28 - 11 - 6]]_3`. The object holds the GF(9) generator `G9`, its Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 2 CPU-minutes, run as 3 parallel parts (about 1 minute with 3 free cores; 57 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It enumerates all 3^22 = 31,381,059,609 vectors of `span(S)^perp` and takes the minimum symplectic weight over those outside the isotropic part. Expected output is in `RUN_IT_YOURSELF.md`; the real output is in `verify-it-yourself/RECEIPTS.md`.

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=28, k=5, c=11)` | `[[28,5,13-22;11]]_3` (`d_lower = 13, d_upper = 22`) | `[[28, 5, 15; 11]]_3` (`d = 15`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-24T11:35:08Z |

Details, HTTP headers, and page hash (`37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`) are in `the-record-we-beat/README.md`.

Published codes that the table does not list: the plain one-point Hermitian EA codes of length 27 (Christensen, Munuera, Pereira, Ruano) imply, through the table's own propagation rules, at most `d = 14` at `(28, 5, 11)`. `d = 15` beats that as well.

## Not claimed

- Optimality for `(n=28, k=5, c=11)` is not claimed; the table's upper bound is 22.
- Only cell `(n=28, k=5, c=11)` is claimed in this package (one cell per package). Cells that follow from it by the table's propagation rules (for example `[[28, 6, 15; 12]]_3`, `[[29, 5, 15; 11]]_3`) and other members of the same code family (for example `[[28, 7, 14; 11]]_3`, `[[28, 6, 12; 6]]_3`) are not claimed here.
- The classical `[28, 11, 15]_9` code is not ours: `codetables.de` has listed an algebraic-geometry code with these parameters from the Hermitian curve since 2003. What is new is the Hermitian hull dimension (6) of the extended code `E_13` used here and the qutrit EA code it gives; the table's own source lists `[[28,4,17;14]]_3` and `[[28,5,16;13]]_3`, exactly the parameters of the neighbors `E_11` and `E_12` at their natural hulls.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The standalone checker is in `verify-it-yourself/`; the run's skeptic reports are in `panel/`.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/), whose best known GF(9) codes of these lengths pointed to the Hermitian curve.
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024), https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647), whose Hermitian construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314, 436-439 (2006), https://arxiv.org/abs/quant-ph/0610092.
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019), https://arxiv.org/abs/1812.05312.
- **Christensen, Munuera, Pereira, and Ruano**, entanglement-assisted quantum codes from one-point Hermitian codes, https://arxiv.org/abs/2105.02166 (Advances in Mathematics of Communications 17(1), 2023): the length-27 family this code extends, and the comparison above.
- **V. D. Goppa** (algebraic-geometry codes) and **Henning Stichtenoth** (Hermitian codes), whose distance bound gives `d >= 28 - m` for the extended code `E_m`.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
