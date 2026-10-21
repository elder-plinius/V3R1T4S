# Entanglement-assisted qutrit code `[[14, 3, 8; 5]]_3` (table: `7-10`)

## What

The artifact `claim/object/qutrit_14_3_8_5.json` (`sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5`) gives an explicit, pure, non-catalytic qutrit entanglement-assisted quantum error-correcting code `[[14, 3, 8; 5]]_3` via a `16 x 28` symplectic generator matrix `S` over `GF(3)` (and its `6 x 14` dual generator matrix `H9` over `GF(9)`) whose exact minimum symplectic distance `d = 8` on `span(S)^perp \ (span(S) ∩ span(S)^perp)` (and on `span(S)^perp \ {0}`) strictly improves the lower bound `d_lower = 7` in `[[14, 3, 7-10; 5]]_3` for `(n=14, k=3, c=5)` on `https://eaqecc.codetables.de/qutrit.php` (`claim/data/qutrit.php`, `sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same object file, with identical bytes (`sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5`), is `object/qutrit_14_3_8_5.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` 3.8 or later (standard library only).
- **Rough laptop time:** ~2 seconds.
- **Expected last line:** `PASS`

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=14, k=3, c=5)` | `[[14,3,7-10;5]]_3` (`d_lower = 7, d_upper = 10`) | `[[14, 3, 8; 5]]_3` (`d = 8`) | https://eaqecc.codetables.de/qutrit.php | 2026-10-17T04:54:03Z (re-fetched by panel 2026-10-17T05:40:20Z) |

Details, HTTP headers, and page hash (`37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`) are in `the-record-we-beat/README.md`.

## Not claimed

- Optimality (`d = 9` or `d = 10`) for `(n=14, k=3, c=5)` is not claimed. The EA-Singleton bound `2d <= n + c - k + 2 = 18` only gives `d <= 9`; the binding `d <= 8` limit is the `codetables.de` upper bound on the minimum distance of the `[14, 6]_9` linear code used as the Hermitian dual in the construction. The general EAQECC table upper bound for this cell is `10`.
- Only cell `(n=14, k=3, c=5)` is claimed in this package (`one cell per package`). Other cells along the `[14, 6, 8]_9` diagonal and propagation consequences (`[[14, 0, 8; 2]]_3`, `[[13, 0, 8; 3]]_3`, `[[12, 0, 8; 4]]_3`, `[[11, 0, 8; 5]]_3`) are not claimed here.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed; verified by a three-skeptic panel (`panel/`) and by the standalone checker in `verify-it-yourself/`.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/), and author of "Entanglement-assisted quantum communication beating the quantum Singleton bound", *Physical Review A* 103, L020601 (2021), https://arxiv.org/abs/2007.01249.
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024), https://doi.org/10.1007/s11128-023-04211-x (preprint "How Much Entanglement Does a Quantum Code Need?", https://arxiv.org/abs/2207.05647), whose Hermitian construction (Proposition 1) and hull-decreasing diagonal monomial scaling theorem (Theorem 4) we build upon directly.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314, 436–439 (2006), https://arxiv.org/abs/quant-ph/0608027.
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019), https://arxiv.org/abs/1804.01754.
- Contributor credit: `anzal1`, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
