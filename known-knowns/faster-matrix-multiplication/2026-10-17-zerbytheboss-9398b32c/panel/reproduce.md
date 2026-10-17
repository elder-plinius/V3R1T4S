# Panel Audit — REPRODUCE Skeptic (`fmm-additive-complexity-records` / `4x5x5_m76`)

context: subagent (fresh invocation)

## 1. Mathematical Definition Quoted Before Inspecting Author Code
A reduced-addition ternary straight-line program (SLP) for multiplying an $N_1 \times N_2$ matrix $A$ by an $N_2 \times N_3$ matrix $B$ in multiplicative rank $m$ over $\mathbb{Z}$ consists of three linear-combination directed acyclic graphs (DAGs):
- $(u_{\text{fresh}}, u)$ mapping the $N_1 N_2$ input variables of $A$ to $m$ linear forms $U \in \{-1, 0, 1\}^{m \times (N_1 N_2)}$,
- $(v_{\text{fresh}}, v)$ mapping the $N_2 N_3$ input variables of $B$ to $m$ linear forms $V \in \{-1, 0, 1\}^{m \times (N_2 N_3)}$,
- $(w_{\text{fresh}}, w)$ mapping the $m$ scalar products $P_r = (U_r \cdot \text{vec}(A))(V_r \cdot \text{vec}(B))$ to the $N_3 N_1$ output entries via $W \in \{-1, 0, 1\}^{(N_3 N_1) \times m}$,
where each fresh intermediate variable $s_k$ is a linear combination of strictly earlier states ($0 \le \text{index} \le k - 1$, ensuring acyclicity) with unit signs $\text{value} \in \{-1, +1\}$, each step of length $L$ incurs $L - 1$ additions/subtractions, and the expanded tensors $(U, V, W)$ satisfy all $(N_1 N_2)(N_2 N_3)(N_3 N_1)$ Brent equations over $\mathbb{Z}$:
$$\sum_{r=0}^{m-1} U_{r, i_1 N_2 + i_2} \, V_{r, j_2 N_3 + j_3} \, W_{k_3 N_1 + k_1, r} = \delta_{i_1, k_1} \, \delta_{i_2, j_2} \, \delta_{j_3, k_3}.$$

## 2. Independent Checker Written from the Definition
Before reading `verify-it-yourself/` or `how-we-built-it/`, an independent Python checker was written directly from the SLP and Brent equation definitions above and executed against `object/4x5x5_m76_cr280_ZT_reduced.json`:
1. **File Integrity (`INDEX.csv`)**: Verified `object/4x5x5_m76_cr280_ZT_reduced.json` has SHA-256 `9398b32cebcc25c00421c96dacdd267857fae5e650e955f41cb118d12e9c12e8`, matching `INDEX.csv` (`target_id = fmm-additive-complexity-records`, `cell = 4x5x5_m76`, `value = 280`, `table_value = 299`).
2. **DAG Acyclicity and Unit Signs**: Verified `n = [4, 5, 5]`, `m = 76`, `z2 = false`, and confirmed that every step in `u_fresh`, `u`, `v_fresh`, `v`, `w_fresh`, and `w` references strictly previously defined indices with coefficients in `{-1, +1}`, expanding to matrices `U`, `V`, `W` with entries strictly in `{-1, 0, 1}`.
3. **Exact Addition Count**: Independently summed `len(step) - 1` across fresh and output lists:
   - `u_adds = 75`
   - `v_adds = 84`
   - `w_adds = 121`
   - Total reduced additions `cr = 75 + 84 + 121 = 280`.
4. **Exhaustive Brent Equation Verification**: Evaluated all $20 \times 25 \times 20 = 10,000$ Brent equations over $\mathbb{Z}$ without sampling. Every single equation matched the Kronecker delta target (`100` ones and `9,900` zeros, `brent_errors = 0`).

## 3. Verification of Package Check Script
Executed `sh verify-it-yourself/run_checks.sh` from the package root:
- Output: `VERIFIED: 4x5x5 rank=76 adds_U=75 adds_V=84 adds_W=121 cr=280 brent_equations=10000 brent_errors=0` followed by `PASS` (exit code `0`).
- Determinism confirmed across repeated runs.

pass: true
