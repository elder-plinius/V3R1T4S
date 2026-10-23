# Entanglement-assisted qutrit code [[16,4,8;4]]_3 with minimum distance 8

## What

The 0/1/2 matrix in object/eaqecc_16_4_8_4.json is a 16 x 32 generator matrix over GF(3) defining an entanglement-assisted qutrit code with n = 16, k = 4, c = 4 and exact minimum distance d = 8 (computed here by full enumeration of the symplectic dual outside the isotropic part), which is strictly above the live qutrit table's d_lower = 7 and not above d_upper = 9 for the cell [[16,4,7-9;4]]_3, as that page read on 2026-10-18.

This is a claim about this one cell. Cells that follow from it by the table's propagation rules are not claimed.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later with numpy (set PY to another interpreter if needed).
- **Rough laptop time**: under a minute.
- **Expected last line**: `ALL CHECKS PASS`

The object `object/eaqecc_16_4_8_4.json` has sha256 e2f4cb89b2b3c23d00e39c2126d5a3e094a9613fece4ba104dac17084c0e88c7.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Grassl, entanglement-assisted qutrit table | [[16,4,7-9;4]]_3 | d_lower = 7, d_upper = 9 | **d = 8** | https://eaqecc.codetables.de/qutrit.php | 2026-10-18T14:23:13Z |

The page footer reads "Last change: 10.07.2025". Metadata, HTTP status and the page sha256: `the-record-we-beat/README.md`. The panel's novelty skeptic also read the newest literature on qutrit entanglement-assisted codes; its report is `panel/novelty.md`.

## Not claimed

- Only the cell named above. Nothing is claimed for other (n, k, c) cells, including cells that follow by propagation rules.
- The distance is not shown to be optimal: the table's upper bound for this cell is 9.
- The construction description is wrong as written: the curve y^3 + y = x^2 has only 15 affine points over GF(9), so C_L(D, 8 P_inf) on it has length at most 15, not 16 (see `HOW_WE_FOUND_IT.md`). The object file is unchanged; its parameters rest on the checks in `verify-it-yourself/`.
- The construction cannot be rebuilt from this package (the construction script is missing from the contributor's snapshot; see `how-we-built-it/README.md`).
- Not peer reviewed. The code was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Markus Grassl**, the entanglement-assisted quantum code tables at https://eaqecc.codetables.de/ (the live qutrit table is the comparison source) and the general tables at https://codetables.de/. Please credit him when using these codes.
- **T. Brun, I. Devetak and M.-H. Hsieh**, *Correcting quantum errors with entanglement*, Science 314 (2006), the entanglement-assisted stabilizer formalism this code is stated in; and the Hermitian-hull reduction from classical codes over GF(9) that the preregistration cites (see arXiv:2207.05647, Luo, Ezerman, Grassl and Ling, https://arxiv.org/abs/2207.05647).
- The search was done by an AI agent (Gemini, called Argon) for the contributor `calgulbenkian`; the checks in `verify-it-yourself/` and `panel/` were written independently of it.
- Contributor credit: `calgulbenkian`.
