# Panel Audit — REPRODUCE Skeptic (`fmm-ternary-integer-ring-upgrade` / `6x12x14`)

context: subagent (fresh invocation)

## 1. Mathematical Definition Quoted Before Inspecting Author Code
A bilinear matrix multiplication scheme of rank $m$ for multiplying an $N_1 \times N_2$ matrix $A$ by an $N_2 \times N_3$ matrix $B$ over the ternary coefficient set $ZT = \{-1, 0, 1\} \subset \mathbb{Z}$ consists of three coefficient tensors $U \in \{-1, 0, 1\}^{m \times (N_1 N_2)}$, $V \in \{-1, 0, 1\}^{m \times (N_2 N_3)}$, and $W \in \{-1, 0, 1\}^{m \times (N_3 N_1)}$ satisfying all $(N_1 N_2)(N_2 N_3)(N_3 N_1)$ Brent polynomial identity equations over $\mathbb{Z}$:
$$\sum_{r=0}^{m-1} U_{r, i_1 N_2 + i_2} \, V_{r, j_2 N_3 + j_3} \, W_{r, k_3 N_1 + k_1} = \delta_{i_1, k_1} \, \delta_{i_2, j_2} \, \delta_{j_3, k_3}$$
for all $0 \le i_1, k_1 \le N_1 - 1$, $0 \le i_2, j_2 \le N_2 - 1$, and $0 \le j_3, k_3 \le N_3 - 1$.

## 2. Independent Checker Written from the Definition
Before reading `verify-it-yourself/` or `how-we-built-it/`, an independent Python checker was written directly from the Brent equation definition above and executed against `object/6x12x14_m654_ZT.json`:
1. **File Integrity (`INDEX.csv`)**: Verified `object/6x12x14_m654_ZT.json` has SHA-256 `499ff66185b47cc110a6ea1229311a136f39e1facb28d26dcc85fc748aea5faa`, matching `INDEX.csv` (`target_id = fmm-ternary-integer-ring-upgrade`, `cell = 6x12x14`, `value = 654`, `table_value = 666`).
2. **Dimensions and Rank**: Verified `n = [6, 12, 14]` and `m = 654`, with `len(u) = 654` rows of length `72`, `len(v) = 654` rows of length `168`, and `len(w) = 654` rows of length `84`.
3. **Strict Ternary (`ZT`) Ring Membership**: Verified every scalar entry across all three factor matrices is an exact Python `int` in `{-1, 0, 1}` (maximum absolute entry `1`; zero `+/-2` coefficients).
4. **Exhaustive Brent Equation Verification**: Evaluated all $72 \times 168 \times 84 = 1,016,064$ Brent equations over $\mathbb{Z}$ without sampling. Every single equation matched the Kronecker delta target (`1,008` ones and `1,015,056` zeros, `brent_errors = 0`).

## 3. Verification of Package Check Script
Executed `sh verify-it-yourself/run_checks.sh` from the package root:
- Output: `VERIFIED: 6x12x14 rank=654 ring=ZT max_abs=(1,1,1) brent_equations=1016064 brent_errors=0 random_trials=10/10` followed by `PASS` (exit code `0`).
- Determinism confirmed across repeated runs.

pass: true
