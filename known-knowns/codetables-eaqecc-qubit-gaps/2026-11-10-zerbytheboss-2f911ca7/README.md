# Entanglement-Assisted Qubit Code `[[19, 2, 11; 9]]_2` (`codetables-eaqecc-qubit-gaps`)

## What

Explicit degenerate binary entanglement-assisted quantum error-correcting code [[19, 2, 11; 9]]_2 (non-catalytic setting) represented as a 26 x 38 stabilizer matrix S over GF(2) in symplectic form [X | Z], independently verified to satisfy rank_GF2(S) = 26, symplectic Gram rank rank_GF2(S Omega S^T) = 18 (c = 9 ebits), isotropic radical size |S cap S^{perp_s}| = 2^8 = 256 (minimum nonzero radical weight 4), and exact non-catalytic minimum distance d_EA = 11 across full enumeration of all 2^12 = 4,096 vectors in S^{perp_s}, raising the lower bound for cell (n, k, c) = (19, 2, 9) in Markus Grassl's codetables.de EAQECC qubit table from [[19, 2, 10-17; 9]]_2 (d_lower = 10) to d_EA = 11.

## Check It Yourself

From the package root directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line (`< 1` second on a laptop, Python 3.8+ standard library only):

```text
PASS
```

`verify-it-yourself/check_eaqecc.py` parses `object/eaqecc_n19_k2_d11_c9.tsv`, runs a negative control on a single-bit perturbation, verifies `rank_GF2(S) = 26` and `rank_GF2(S * Omega * S^T) = 18` (`c = 9` ebits), independently computes `S^{perp_s}` from `S` alone by `GF(2)` row reduction, enumerates all `2^12 = 4,096` vectors in `S^{perp_s}` (`256` vectors in `S cap S^{perp_s}` of minimum nonzero weight `4`, and `3,840` coset vectors in `S^{perp_s} \ S` of minimum symplectic weight `d_EA = 11`), and checks the `GF(4)` Griesmer bound ruling out all `l' in {0, 1, 2}` classical (non-degenerate) quaternary hull ancestors (`[11, 2]_4` LCD max `d = 8`, `[13, 3]_4` 1-hull max `d = 9`, `[15, 4]_4` 2-hull max `d = 10`).

## Compared To

- **Table**: Markus Grassl, *Bounds on the minimum distance of entanglement-assisted qubit quantum codes `[[n,k,d;c]]_2`* (`Last change: 10.07.2025`)
- **Cell**: `n = 19`, `k = 2`, `c = 9` (non-catalytic setting, `c >= 1`)
- **Live Table URL**: `http://www.codetables.de/EAQECC/qubit.php` (re-fetched `2026-11-10T19:51:24Z`, HTTP `200`, SHA-256 `c84dea1ab3b3657e268462019569f0bf6b3cb15872ae0675d47ae9ae62536e6a`)
- **Table Entry**: `[[19, 2, 10-17; 9]]_2` (`d_lower = 10`, `d_upper = 17`, obtained by puncturing `[[28, 2, 10; 0]]_2`)
- **This Package (`object/eaqecc_n19_k2_d11_c9.tsv`)**: `d_EA = 11` (`10 < 11 <= 17`), a genuinely degenerate EAQECC (`d_EA = 11 > 4 = d(S^{perp_s})`).

## Not Claimed

- Optimality (`d = 11` vs `d_upper = 17`), upper-bound reductions (`p1`, which covers `n <= 12`), or improvements to cells outside `(19, 2, 9)` (and its immediate lengthening/subcode consequences) are not claimed.

## Credits

- Contributor: `@HindsightWise`
- Compared against and built on definitions from:
  - M. Grassl, *Bounds on the minimum distance of entanglement-assisted quantum codes* (`http://www.codetables.de/EAQECC/qubit.php`).
  - M. Grassl, F. Huber, and A. Winter, "Entanglement in quantum error-correcting codes," *IEEE Trans. Inf. Theory* 68(6), 3920–3950 (2022), `arXiv:2207.05647`.
  - T. A. Brun, I. Devetak, and M.-H. Hsieh, "Correcting quantum errors with entanglement," *Science* 314(5798), 436–439 (2006), `arXiv:quant-ph/0610092`.
