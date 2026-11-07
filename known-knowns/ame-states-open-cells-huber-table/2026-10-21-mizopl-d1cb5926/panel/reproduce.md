---
panel_role: reproduce
context: independent cold-check skeptic session (fresh process, read-only package audit)
verdict: PASS
date: 2026-11-07
target_id: ame-states-open-cells-huber-table
run_id: 2026-10-21-mizopl-d1cb5926
---

# Reproduce Skeptic Report — `PASS`

## 1. Execution & Zero-Dependency Verification Audit

We executed the standalone verifier from the package root via:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Command exit code:** `0` (`PASS` printed on the final line).
- **Runtime:** `2.24s` on Apple M1 using only the Python 3 standard library (`hashlib`, `itertools`, `json`, `os`, `sys`, `time`).
- **Certificate file verified:** `object/ame_17_8_pure_circulant_certificate.json` (`4,176` bytes, `sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`).

## 2. Exhaustive Cut-Rank & Binary Trace-Symplectic Audit (Zero Sampling)

1. **Direct $\mathbb{F}_8$ cut-rank check across all $\binom{17}{8} = 24,310$ eight-party cuts (`0.40s`):**
   `verify-it-yourself/verify.py` iterates over every 8-element subset $S \subset \{0, \dots, 16\}$ (`itertools.combinations(range(17), 8)`, `24,310` cuts total, with no dihedral orbit reduction or slice sampling) and performs exact Gaussian elimination over $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ on the $8 \times 9$ off-diagonal submatrix $\Gamma_{S, S^c}$ of the symmetric 17-circulant with chord vector $a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w)$. All `24,310 / 24,310` cuts have full $\mathbb{F}_8$-rank `8` (`bad = 0`).
2. **Independent $51$-qubit $\mathbb{F}_2$ trace-symplectic graph-state check across all $\binom{17}{8} = 24,310$ cuts (`0.66s`):**
   Using the self-dual normal trace-orthonormal basis $\{w^3, w^6, w^5\} = \{w+1, w^2+1, w^2+w+1\} = [3, 5, 7]$ of $\mathbb{F}_8 / \mathbb{F}_2$ (where $\operatorname{Tr}(x) = x + x^2 + x^4$ satisfies $\operatorname{Tr}(e_a e_b) = \delta_{a,b}$), `verify.py` expands the $17 \times 17$ $\mathbb{F}_8$ adjacency matrix into a $51 \times 51$ binary symmetric hollow adjacency matrix $B_{51}$ over $\mathbb{F}_2$ and verifies that for all `24,310 / 24,310` eight-qudit (`24`-qubit vs `27`-qubit) partitions, the $24 \times 27$ submatrix $(B_{51})_{Q(S), Q(S^c)}$ has full $\mathbb{F}_2$-rank `24` (`bad = 0`), certifying von Neumann entropy $S(\rho_S) = 24$ bits on every $8$-qudit subsystem.
3. **Corrupted-object and single-entry mutant rejection:**
   - `kit/check_run.py` corrupted-object test (`corrupt_json_value` on `object/ame_17_8_pure_circulant_certificate.json`): properly rejected with non-zero exit code.
   - Single-edge mutant ($\Gamma_{0,1} = \Gamma_{1,0} \leftarrow 0$): `184 / 24,310` rank-deficient cuts (`24,126 / 24,310` full rank).
   - Single-chord mutant ($a_1 \leftarrow 0$): `918 / 24,310` rank-deficient cuts (`23,392 / 24,310` full rank).
   - Best random symmetric 17-circulant from the 400-sample (`seed=42`) null test (`chord = [5, 1, 0, 1, 7, 0, 4, 6]`): `170 / 24,310` rank-deficient cuts (`24,140 / 24,310` full rank; `0 / 400` random controls achieve `AME(17, 8)`).

pass: true
