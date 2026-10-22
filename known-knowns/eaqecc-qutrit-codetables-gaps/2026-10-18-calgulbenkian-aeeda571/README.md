# Entanglement-assisted qutrit code [[33,3,23;24]]_3 with minimum distance 23

## What

The 0/1/2 matrix in object/eaqecc_33_3_23_24.json is a 54 x 66 generator matrix over GF(3) defining an entanglement-assisted qutrit code with n = 33, k = 3, c = 24 and exact minimum distance d = 23 (computed here by full enumeration of the symplectic dual outside the isotropic part), which is strictly above the live qutrit table's d_lower = 22 and not above d_upper = 30 for the cell [[33,3,22-30;24]]_3, as that page read on 2026-10-18.

This is a claim about this one cell. Cells that follow from it by the table's propagation rules are not claimed.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later with numpy (set PY to another interpreter if needed).
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

The object `object/eaqecc_33_3_23_24.json` has sha256 aeeda5718cc3d1662ff3fdba77996671c36d732aea511eb157b4667a3168a8a6.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Grassl, entanglement-assisted qutrit table | [[33,3,22-30;24]]_3 | d_lower = 22, d_upper = 30 | **d = 23** | https://eaqecc.codetables.de/qutrit.php | 2026-10-18T14:23:13Z |

The page footer reads "Last change: 10.07.2025". Metadata, HTTP status and the page sha256: `the-record-we-beat/README.md`. The panel's novelty skeptic also read the newest literature on qutrit entanglement-assisted codes; its report is `panel/novelty.md`.

## Not claimed

- Only the cell named above. Nothing is claimed for other (n, k, c) cells, including cells that follow by propagation rules.
- The distance is not shown to be optimal: the table's upper bound for this cell is 30.
- The construction cannot be rebuilt from this package (the construction script is missing from the contributor's snapshot; see `how-we-built-it/README.md`).
- Not peer reviewed. The code was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Markus Grassl**, the entanglement-assisted quantum code tables at https://eaqecc.codetables.de/ (the live qutrit table is the comparison source) and the general tables at https://codetables.de/. Please credit him when using these codes.
- **T. Brun, I. Devetak and M.-H. Hsieh**, *Correcting quantum errors with entanglement*, Science 314 (2006), the entanglement-assisted stabilizer formalism this code is stated in; and the Hermitian-hull reduction from classical codes over GF(9) that the preregistration cites (see arXiv:2207.05647, Luo, Ezerman, Grassl and Ling, https://arxiv.org/abs/2207.05647).
- The authors of the algebraic-geometry and norm-trace code literature the scripts' construction field names (Goppa-style AG codes on curves over finite fields; Xing and Ling for the quadratic norm-trace code family). The exact papers are not listed in the snapshot; the construction text is the search agent's own description and is unverified.
- The search was done by an AI agent (Gemini, called Argon) for the contributor `calgulbenkian`; the checks in `verify-it-yourself/` and `panel/` were written independently of it.
- Contributor credit: `calgulbenkian`.
