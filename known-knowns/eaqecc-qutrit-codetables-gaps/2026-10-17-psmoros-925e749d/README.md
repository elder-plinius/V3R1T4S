# Entanglement-assisted qutrit code [[33,1,31;24]]_3 (table: [[33,1,25-32;24]]_3)

## What

The 56-row, 66-column GF(3) symplectic generator matrix object/S_33_1_31_24.txt (sha256 925e749d…629edc) defines a degenerate entanglement-assisted qutrit code with n = 33, s = 56 independent generators, c = 24, k = 1 and exact minimum distance d = 31 under the criterion's definition (exhaustive over all 3^10 vectors of span(S)^perp, excluding span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 25 and at most d_upper = 32 of the cell [[33,1,25-32;24]]_3 of the live table eaqecc.codetables.de/qutrit.php (page "Last change: 10.07.2025", sha256 37bbf731…c936c, re-fetched 2026-10-17T18:55:50Z), and no table entry with c <= 25 has d_lower >= 30.

## Check it yourself

From this package folder, run:

    sh verify-it-yourself/run_checks.sh

- **Requirements:** python3, standard library only.
- **Rough laptop time:** about 15 s of CPU (all 3^10 = 59049 vectors of span(S)^perp are enumerated).
- **Expected last line:** `PASS`

## Compared to

| table | cell (n,k,c) | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes ("Last change: 10.07.2025") | (33,1,24) | [[33,1,25-32;24]]_3 (d_lower 25, d_upper 32) | [[33,1,31;24]]_3 (d = 31) | https://eaqecc.codetables.de/qutrit.php | 2026-10-17T17:24:09Z; panel re-fetches 18:49:50Z and 18:55:50Z; packaging re-fetch 19:14:06Z (all sha256 37bbf731...) |

Details are in the-record-we-beat/.

## Not claimed

- **Optimality.** d = 32 is not ruled out by anything in this package.
- **The margin.** The table lists d_lower = 25. The NOVELTY skeptic noted that an elementary k = 1 extension rule ([[n,1,d;c]] -> [[n+1,1,d+1;c+1]], valid for q >= 3), applied to the table's own teleportation codes such as [[10,1,7;1]]_3, already gives [[33,1,30;24]]_3. So the improvement over what known codes give by easy derivation is +1 (31 vs 30), not +6.
- **Other cells.** Only the cell (33,1,24) is claimed, one cell per package. The run found many other cells that beat the table: the same construction family in other (n,1,c) rows; the [[12,1,10;3]]_3 core inside this object; GF(9)-linear and GF(3)-additive codes elsewhere. None of them is claimed here.
- **Not submitted** to, or listed by, the table maintainer.
- **Not peer reviewed.** It was checked by a three-skeptic panel (panel/) and by the standalone checker in verify-it-yourself/.

## Credits

- **Markus Grassl** maintains the EAQECC bounds tables (https://eaqecc.codetables.de/, qutrit table https://eaqecc.codetables.de/qutrit.php) and codetables.de (https://codetables.de/). Paper: "Entanglement-assisted quantum communication beating the quantum Singleton bound", Physical Review A 103, L020601 (2021), https://arxiv.org/abs/2007.01249.
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl and San Ling**, "Constructing quantum error-correcting codes that require a variable amount of entanglement", Quantum Information Processing 23, 4 (2024), https://arxiv.org/abs/2207.05647. Source of the table entries and propagation rules compared against.
- **Markus Grassl, Felix Huber and Andreas Winter**, "Entropic proofs of Singleton bounds for quantum error-correcting codes", IEEE Trans. Inf. Theory (2022), https://arxiv.org/abs/2010.07902. Bounds consulted by the panel.
- **Todd A. Brun, Igor Devetak and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", Science 314, 436-439 (2006), https://arxiv.org/abs/quant-ph/0608027. The entanglement-assisted stabilizer formalism.
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S.
