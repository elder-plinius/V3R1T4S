# Run It Yourself — `AME(17, 8)` (`[[17, 0, 9]]_8`)

## 1. Zero-Dependency Exhaustive Verification (`~2.2s`)

From the package root (`known-knowns/ame-states-open-cells-huber-table/2026-10-21-mizopl-d1cb5926/`):

```sh
sh verify-it-yourself/run_checks.sh
```

Or invoke `verify.py` directly with Python 3 (standard library only):

```sh
/opt/homebrew/bin/python3 verify-it-yourself/verify.py
```

### What `verify-it-yourself/verify.py` checks:
1. **Strict Certificate Integrity (`object/ame_17_8_pure_circulant_certificate.json`, `4,176` bytes, `sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`):**
   Checks all scalar fields, `verification` metadata, `prior_status` metadata, `chord_vector_d1_to_d8_int = [1, 2, 5, 1, 5, 2, 2, 2]`, `chord_vector_d1_to_d8_poly = ["1", "w", "w^2+1", "1", "w^2+1", "w", "w", "w"]`, `first_row_int`, `first_row_poly`, hollow diagonal ($\Gamma_{i,i} = 0$), symmetry ($\Gamma_{i,j} = \Gamma_{j,i}$), and circulant law $\Gamma_{i,j} = a_{\min((j-i)\bmod 17, (i-j)\bmod 17)}$. Any corrupted scalar or matrix entry causes immediate exit with status `1`.
2. **Exhaustive $\mathbb{F}_8$ 8-Party Cut Check (`24,310 / 24,310` cuts, `0.40s`):**
   Iterates directly over all $\binom{17}{8} = 24,310$ subsets $S \subset \{0, \dots, 16\}$ (`|S| = 8`) and verifies via exact Gaussian elimination over $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ that every $8 \times 9$ off-diagonal submatrix $\Gamma_{S, S^c}$ has full rank `8` (`bad = 0`).
3. **Exhaustive $51$-Qubit $\mathbb{F}_2$ Trace-Symplectic Graph-State Check (`24,310 / 24,310` cuts, `0.66s`):**
   Expands $\Gamma$ in the self-dual normal trace-orthonormal basis $\{w^3, w^6, w^5\} = \{w+1, w^2+1, w^2+w+1\} = [3, 5, 7]$ of $\mathbb{F}_8 / \mathbb{F}_2$ into a $51 \times 51$ binary symmetric hollow adjacency matrix $B_{51}$ over $\mathbb{F}_2$, and verifies that all $\binom{17}{8} = 24,310$ eight-qudit (`24`-qubit vs `27`-qubit) submatrices $(B_{51})_{Q(S), Q(S^c)}$ have full $\mathbb{F}_2$-rank `24` (`bad = 0`).
4. **`codetables.de` $\mathbb{F}_8 \subset \mathbb{F}_{64}$ Subfield Isomorphism Check:**
   Verifies that in $\mathbb{F}_{64} = \mathbb{F}_2[u]/(u^6 + u^4 + u^3 + u + 1)$, the subfield element $w = u^9$ satisfies $w^3 + w + 1 = 0$ and $w^2 + 1 = u^{54}$, matching the cyclic generator polynomial of `[[17, 0, 9]]_8` on `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (`Construction type: Gajewski`, `last modified: 2026-10-21`).
5. **Positive, Negative, and Mutant Controls:**
   - `AME(5, 2)` 5-cycle $C_5$: `10 / 10` cuts pass;
   - `AME(4, 2)` exhaustive $64$-graph scan: `0 / 64` graphs pass;
   - Single-edge mutant ($\Gamma_{0,1} = \Gamma_{1,0} \leftarrow 0$): `184 / 24,310` bad cuts;
   - Single-chord mutant ($a_1 \leftarrow 0$): `918 / 24,310` bad cuts;
   - Best random 17-circulant from 400-draw `seed=42` null test (`[5, 1, 0, 1, 7, 0, 4, 6]`): `170 / 24,310` bad cuts (`24,140 / 24,310` full rank).

## 2. Reproducing the $D_{17}$ Orbit Filtration & 400-Control Null Test (`~4.6s`)

```sh
/opt/homebrew/bin/python3 how-we-built-it/search_and_verify_ame_17_8_circulant.py
```
