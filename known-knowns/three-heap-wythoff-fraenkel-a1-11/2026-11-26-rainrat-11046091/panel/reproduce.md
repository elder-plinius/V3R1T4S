context: subagent (fresh session)

# Independent Reproduction Report: `three-heap-wythoff-fraenkel-a1-11` ($A_1 = 12$)

## 1. Literal Definition Quoted

From Sun and Zeilberger, *On Fraenkel's $N$-Heap Wythoff's Conjectures*, *Annals of Combinatorics* 8 (2004), pp. 225–226 (`Zeilberger_y2004_p225.pdf`):

> "The $N$-heap Wythoff's game is a two-player impartial game with $N$ piles of tokens of sizes $A^1, \dots, A^N, A^1 \le \dots \le A^N$. Players take turns removing any number of tokens from a single pile, or removing $(a_1, \dots, a_N)$ from all piles — $a_i$ tokens from the $i$-th pile, providing that $0 \le a_i \le A^i$, $\sum_{i=1}^N a_i > 0$ and $a_1 \oplus \dots \oplus a_N = 0$, where $\oplus$ is the nim addition. The first player that cannot make a move loses."

Under sorted three-heap coordinates $(m, Y_j^m, Z_j^m)$ with $m \le Y_j^m \le Z_j^m$ and gap-indexed coordinates $[m, A_j^m, B_j^m] = [m, Y_j^m - m, Z_j^m - Y_j^m]$ ($1$-based $j \ge 1$), a position is a $P$-position iff every legal move leads to an $N$-position (with base case $(0, 0, 0)$ being a $P$-position). Exact golden-section floors use integer arithmetic $\lfloor k\phi \rfloor = \lfloor (k + \lfloor \sqrt{5k^2} \rfloor)/2 \rfloor$.

## 2. Independent Checker Construction & Exhaustive Verification (Before Reading Author Code)

Before opening `verify_wythoff.py` or `run_checks.sh`, an independent two-stage checker (`repro_solver.cpp` in C++20 and `repro_check.py` in Python) was written from the literal game definition, `CLAIM.md`, `PROOF.md`, `REPRODUCE.md`, and `Zeilberger_y2004_p225.pdf`:

1. **Literal 3D game-tree DP cross-check**: Evaluated all sorted states $0 \le p_1 \le 12$, $p_1 \le p_2 \le p_3 \le 60$ directly from single-pile and all-pile nim-sum-0 moves. Matched the direct rules-based solver identically on all **199** $P$-positions in $0 \le p_1 \le 12, p_3 \le 60$.
2. **Direct rules-based P-position recomputation ($m = 0..12$, $Y \le 6000$)**: Computed layers $m = 0, \dots, 12$ sequentially. At each $(m, Y)$, any $Y$ covered by an earlier $(i, m, Y)$ ($i < m$) or $(m, y', Y)$ ($y' < Y$) is universally $N$ for all $Z \ge Y$ via single-heap reduction; otherwise all permutations of all earlier $P$-positions $(i, y', z')$ ($i < m, y' \le Y$ or $i = m, y' < Y$) were tested exhaustively for single-heap and XOR-0 moves to find the minimal unblocked $Z \ge Y$.
3. **Mex completeness and $T^m$**: Verified $T^m = \{Z' - m : (i, m, Z') \in P^i \text{ for some } i < m\}$ (and its complement characterization in $\mathbb{Z}_{\ge 0}$) and $Y_j^m = \operatorname{mex}(\{0, \dots, m-1\} \cup (m + T^m) \cup \{Y_r^m, Z_r^m : 1 \le r < j\})$ with $Z_j^m$ unused across all rows up to $Y \le 6000$ for every $0 \le m \le 12$.
4. **Table 1 ($m = 0..10$), $N_3^i$ / $B_{N_3^i}^i$ ($0 \le i \le 11$), and $m = 12$ constants**: Every field in `wythoff_a1_12_certificate.json` matched the independently recomputed values identically (using the Table 1 `>=` threshold convention):

| $m$ | $T^m$ | $|S^m|$ | $\alpha^m$ | $N_1^m$ | $N_2^m$ | $N_3^m$ | $B_{N_3^m}^m$ | $B_{N_3^m+1}^m$ | $n_2$ | $n_1$ | $A_{n_1}^m$ | $B_{n_1}^m$ | $\min \text{slack}$ |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | $\emptyset$ | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 6 | 10 | 14 | 9 | — |
| 1 | $\{1\}$ | 3 | -4 | 21 | 28 | 75 | 77 | 78 | 52 | 91 | 145 | 93 | 0 |
| 2 | $\emptyset$ | 6 | -10 | 28 | 58 | 157 | 162 | 163 | 101 | 182 | 290 | 187 | 2 |
| 3 | $\{1,2,3\}$ | 11 | -16 | 48 | 73 | 206 | 216 | 217 | 131 | 223 | 358 | 233 | 2 |
| 4 | $\{3,6\}$ | 13 | -20 | 126 | 208 | 561 | 573 | 574 | 347 | 575 | 925 | 587 | 0 |
| 5 | $\{4,7,10\}$ | 17 | -26 | 71 | 123 | 345 | 361 | 362 | 213 | 559 | 899 | 575 | 2 |
| 6 | $\{2,3,4,6\}$ | 21 | -32 | 113 | 232 | 637 | 657 | 658 | 392 | 652 | 1049 | 672 | 2 |
| 7 | $\{1,4,6,7,9\}$ | 26 | -39 | 227 | 343 | 937 | 962 | 963 | 576 | 953 | 1536 | 978 | 3 |
| 8 | $\{3,5,10,13\}$ | 29 | -46 | 388 | 648 | 1739 | 1767 | 1768 | 1070 | 1754 | 2829 | 1782 | 3 |
| 9 | $\{4,6,11,15\}$ | 33 | -52 | 645 | 645 | 1070 | 1102 | 1103 | 1065 | 1748 | 2819 | 1780 | 2 |
| 10 | $\{6,7,8,9,13\}$ | 36 | -56 | 656 | 656 | 1766 | 1801 | 1802 | 1084 | 1781 | 2872 | 1816 | 0 |
| 11 | $\{1,7,11,13,17,21,23\}$ | 40 | -61 | 1214 | 1214 | 1381 | 1420 | 1421 | 1990 | 3249 | 5248 | 3288 | 1 |
| 12 | $\{0,8,9,18,22,24\}$ | 43 | -67 | 64 | 352 | 988 | 1030 | 1031 | 601 | 1762 | 2839 | 1804 | 2 |

All 11 rows ($m = 0..10$) match Sun & Zeilberger Table 1 identically (noting Table 1 prints $T^9$ unsorted as `6, 4, 11, 15`), and `m = 12` matches `CLAIM.md` ($N = N_{\text{claim34}}^{12} = 600$, $(n_2, n_1) = (601, 1762)$, $S^{12}$ of size $43$).

## 3. Re-derivation and Verification of Claims 3.3–3.5 and `PROOF.md`

- **Claim 3.3 (modulo-$p(m)$ ray witnesses)**: For every $1 \le m \le 12$, every $c \in S^m = S_1^m(n_1)$, and every $Y \in [Y_{n_1}^m, Y_{n_1}^m + p(m)]$ (with $p(m) = 2^{\lfloor \log_2 m \rfloor + 1}$, exhaustive over all $p(m) + 1$ offsets), the recorded destination $[a, A_0, B_0]$ in `wythoff_a1_12_certificate.json` was verified to be a recomputed $P$-position with $0 \le a < m$ and to admit a permutation $(u_1, u_2, u_3)$ of $(a, a+A_0, a+A_0+B_0)$ satisfying $0 \le d = m - u_1 < p(m)$, $e = Y - u_2 \ge 0$, $f = Y + c - u_3 \ge 0$, $d + e + f > 0$, and $d \oplus e \oplus f = 0$. Since $d < p(m) = 2^{\lfloor \log_2 m \rfloor + 1}$ and $e \oplus f = d$, $e$ and $f$ agree on all bits $\ge \log_2 p(m)$, so shifting $Y \mapsto Y + k \cdot p(m)$ ($k \ge 0$) preserves nonnegativity, $d + e + f > 0$, and $d \oplus e \oplus f = 0$.
- **Claim 3.4 and Claim 3.5**: For $1 \le m \le 12$, all Claim 3.4 bounds ($A_k^m > \max_{i \le m} T^i$, $B_k^m > m + \max_{i \le m} T^i$ for $k > N_{\text{claim34}}^m$, and lower-layer separation through $n_1 + 1$) and all 8 hypotheses of Claim 3.5 hold under the half-sum $\alpha' = \lfloor (\max \alpha_j^m + \min \alpha_j^m)/2 \rfloor = \alpha^m$. Verified explicitly that the p. 235 typographical print $\lfloor (\max - \min)/2 \rfloor \in \{0, 1\}$ violates Condition 7 ($\alpha^0 - \alpha' \ge 4m$) for every $1 \le m \le 12$.
- **`PROOF.md` Section 1–4 re-derivation**:
  - **Section 1 (Closed box & mex)**: Moves never increase the middle or max coordinate after sorting; every skipped $y \ge m$ reduces via single-heap move to $(i, m, y)$ ($y \in m + T^m$) or $(m, y', y)$ ($y' < y$).
  - **Section 2 (Lemma 2.6)**: Verified `Wythoff_forbidden_max` $= \max Q$, $Z_{\text{start}}^m > \max Q$, all early gaps $< B_{\text{start}}^m$, exact match between the synthetic gap-indexed Wythoff sequence $(Y(g), Z(g))$ and the true game from `start` through $Y \le 6000$, and all finite history/anchor inequalities ($Y_{n_2 - 3}^m > \max Q$, $Y_{n_1 - 3}^m > Z_{\text{first\_above}}^m$, $Y_{n_1 - 3}^m - 1 > Z_{n_2 - 5}^m$, $Y_{n_1}^m > Z_{n_2}^m$, $|\varepsilon_j^m| \le 1$ on $[n_2 - 4, n_1]$, $\varepsilon_{n_1}^m = 0$, $\varepsilon_{j-2}^m \varepsilon_{j-1}^m \varepsilon_j^m = 0$ on $[n_2 - 2, n_1]$). Re-derivation confirms Lemma 2.6 guarantees $|\varepsilon^m(g)| \le 1$ and $\varepsilon^m(g-1)\varepsilon^m(g) = 0$ for all synthetic terms $g > B_{n_1}^m$.
  - **Section 4 (Induction on $m = 1..12$)**: Verified exact `small_two_max` values ($2, 2, 6, 10, 15, 15, 16, 21, 24, 26, 34, 36$ for $m = 1..12$), $Y_{n_1+1}^m > \text{small\_two\_max}(m)$, $B_{n_1}^m + 1 > \text{small\_two\_max}(m) + m$, $B_{n_1}^m > \max_{i < m} (\max_{j \le N_1^i} B_j^i + m - i)$, $B_{n_1}^m > \max_{i < m} B_{N_3^i+1}^i$, and exact `offset_slack` values $\alpha^i - \alpha^m - \lfloor (m-i)\phi \rfloor - 3 \ge 0$ (strictly $> 0$ for $m \in \{11, 12\}$). When $\text{slack}(m, i) = 0$ (observed only at $(m, i) \in \{(1, 0), (4, 3), (10, 9)\}$, where $d = 1$ and $\alpha^{m-1} - \alpha^m = 4$), equality $Y_{m-1}(h) = Y_m(g)$ forces $h = g-1$, $\lfloor g\phi \rfloor - \lfloor (g-1)\phi \rfloor = 2$, $\varepsilon_g^m = +1$, and $\varepsilon_{g-1}^m = 0$ (from $\varepsilon_{n_1}^m = 0$ at $g = B_{n_1}^m + 1$ and Lemma 2.6 on layer $m$ for $g \ge B_{n_1}^m + 2$), forcing $Y_m(g) - Y_m(g-1) = 3$, impossible above $\max Q$. Thus every proposed $(m, Y(g), Y(g)+g)$ is the exact next $P$-position for all $g > B_{n_1}^m$.

## 4. Author Verifier Execution, Determinism, and File Integrity

- `wythoff_a1_12_certificate.json` SHA-256: `1104609158ffe4f753070d369f788ee0ae891427af6c8407cb961a5bd9843e1f`
- `verify_wythoff.py` SHA-256: `168fc305ef073bb472beba4dc5cbc1e45224b43db9199edf1b96c05a6f437c64`
- `run_checks.sh` SHA-256: `38031458f128cf2ce783f0c72f8a69b935bd7a6d24d2081876a74dabe218c40a`
- Executed `sh run_checks.sh` twice independently; both runs exited with status `0`, produced byte-for-byte identical output (`diff -u` empty), and ended with `PASS`.

pass: true
