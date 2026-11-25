context: subagent (fresh session)

# Independent Criterion Assessment: `three-heap-wythoff-fraenkel-a1-11` ($A_1 = 12$)

confirmed_scope: Both of Fraenkel's three-heap Wythoff conjectures are proved and independently verified from the game rules for smallest heap A_1 = 12 (together with the full prerequisite inductive chain m = 0..11, including Sun and Zeilberger's Table 1 for m = 0..10 and N_3^i, B_{N_3^i}^i for all 0 <= i <= 11), with explicit thresholds (n_2, n_1) = (601, 1762) and derived constants satisfying Claims 3.3, 3.4, and 3.5 (under the intended midpoint alpha' = floor((max + min)/2)) as well as a self-contained Lemma 2.6 direct induction proof.

## Clause-by-clause check against the verbatim bank criterion

1. **Target scope (`A1 = 11 (or any larger single value, once 11 is done)`) and novelty/non-subsumption**:
   - `CLAIM.md` targets $A_1 = 12$, a larger single value than $11$.
   - `SCOUT.md` records Nowakowski (*Games of No Chance 6*, MSRI Publ. 71, 2025, Problem `A4(53)`, pp. 61–62; <https://library.slmath.org/books/Book71/files/GONC6-04.pdf>) still listing only $A_1 \le 10$ as proved.
   - `pr-1117.json` records open, unmerged PR `#1117` (<https://github.com/elder-plinius/V3R1T4S/pull/1117>, `state: "OPEN"`, created `2026-11-17T05:36:16Z`) claiming only $A_1 = 11$. Thus $A_1 = 12$ is neither published as proved nor subsumed by PR `#1117`.
   - Crucially, this submission does not rely on PR `#1117` as an unverified oracle: `wythoff_a1_12_certificate.json`, `PROOF.md`, and `verify_wythoff.py` independently recompute, certify, and prove the entire prerequisite chain $m = 0, 1, \dots, 11$ alongside $m = 12$. For $m = 11$, the certificate explicitly provides $(n_2, n_1) = (1990, 3249)$, $N = 1989$, $T^{11} = \{1, 7, 11, 13, 17, 21, 23\}$, $|S^{11}| = 40$, $\alpha^{11} = -61$, $N_1^{11} = 1214$, $N_2^{11} = 1214$, $N_3^{11} = 1381$, $B_{N_3^{11}}^{11} = 1420$, $B_{N_3^{11}+1}^{11} = 1421$, $B_{n_1}^{11} = 3288$, and period-16 XOR ray witnesses for $S_1^{11}(n_1) = S^{11}$.

2. **Explicit `n2 < n1`, derived constants, and Claims 3.3, 3.4, and 3.5 (`Zeilberger_y2004_p225.pdf`)**:
   - For $m = 12$, `CLAIM.md` and `wythoff_a1_12_certificate.json` give $n_2 = 601 < n_1 = 1762$ ($N_{\text{claim34}} = 600$), $T^{12} = \{0, 8, 9, 18, 22, 24\}$, $|S^{12}| = 43$, $\alpha^{12} = -67$, $N_1^{12} = 64$, $N_2^{12} = 352$, $N_3^{12} = 988$ ($B_{988}^{12} = 1030$, $B_{989}^{12} = 1031$), $B_{n_1}^{12} = 1804$, and $S_1^{12}(n_1) = S^{12}$ with explicit lower-layer P-position XOR ray witnesses across $[2851, 2867]$ ($p(12) = 16$).
   - **Indexing convention**: `CLAIM.md` and `wythoff_a1_12_certificate.json` explicitly state the Table 1 `>=` convention for $N_1, N_2, N_3$, and verify Claim 3.5 Condition 6 against **both** $B_{N_3^i}^i$ and $B_{N_3^i + 1}^i$ for all $i < m$, eliminating any `>` vs `>=` off-by-one ambiguity.
   - **Printed typo on p. 235 of `Zeilberger_y2004_p225.pdf`**: On p. 235, Claim 3.5 prints $\alpha' = \lfloor (\max(\alpha_j^m) - \min(\alpha_j^m))/2 \rfloor$ instead of the half-sum $\lfloor (\max(\alpha_j^m) + \min(\alpha_j^m))/2 \rfloor$. Literally evaluating the half-difference yields $\alpha' \in \{0, 1\}$, which makes Condition 7 ($\alpha^0 - \alpha' \ge 4m$, where $\alpha^0 = 0$) impossible for every $m \ge 1$ (including Sun and Zeilberger's own Table 1 cases $m = 1..10$, which list $\alpha^m < 0$ matching the half-sum). Here:
     - All eight conditions of Claim 3.5 (and all hypotheses of Claims 3.3 and 3.4) hold for every $1 \le m \le 12$ under the intended half-sum $\lfloor (\max + \min)/2 \rfloor$ used in Table 1.
     - Moreover, `PROOF.md` (Section 4) supplies a self-contained direct induction proof on $m = 1, \dots, 12$ using Lemma 2.6, Claim 3.1, the Claim 3.3 modulo-$p(m)$ ray witnesses, and explicit Beatty-floor separation bounds (`small_two_max` and `offset_slack`), proving Conjectures 1 and 2 for $0 \le m \le 12$ without relying on Claim 3.5's misprinted p. 235 formula.
   - Checking the induction invariants directly against `wythoff_a1_12_certificate.json`: for every $0 \le i < m \le 12$, $N_1^i \le N_2^i \le N_3^i$ and $B_{n_1}^m + 1 - (m - i) > B_{N_3^i + 1}^i > B_{N_3^i}^i$, so every lower-layer gap $h \ge g - (m - i)$ reached from $g > B_{n_1}^m$ lies strictly past $B_{N_3^i}^i$ (covered by the verified finite table up to $B_{n_1}^i$ and by Lemma 2.6 beyond $B_{n_1}^i$).

3. **Recomputed Table 1 and $N_3^i, B_{N_3^i}^i$ for every $i < 11$ (and $i = 11$)**:
   - `wythoff_a1_12_certificate.json` states $T^i, S^i, \alpha^i, N_1^i, N_2^i, N_3^i, B_{N_3^i}^i$, and $B_{N_3^i+1}^i$ for all $0 \le i \le 12$.
   - `verify_wythoff.py` recomputes all of them from the game rules and confirms an exact match on all 11 rows ($m = 0..10$) of Sun and Zeilberger's Table 1 (subsuming partial win `p1`) as well as $m = 11$ and $m = 12$.

4. **Independent rules-based verification**:
   - `verify_wythoff.py` (Python 3.8+ standard library only) shares no code with the C++20 certificate-generation solvers referenced in `REPRODUCE.md`.
   - It recomputes all P-positions $(m, Y, Z)$ for $0 \le m \le 12, Y \le 5500$ directly from Fraenkel's game rules (accounting for single-heap, equal-two-heap, and three-heap XOR moves), cross-checks against literal 3D game-tree evaluation (`brute_force_3heap(12, 55)`, 178 P-positions), and checks every Claim 3.3–3.5 and Lemma 2.6 condition and every field of `wythoff_a1_12_certificate.json`.
   - Running `sh run_checks.sh` in `claim/` completed with exit code `0` and output `PASS`.

## Hidden-quantifier and null-model check

- No hidden quantifiers or horizon truncations remain: downward closure of $Y \le M$ under all legal moves guarantees exactness of the recomputed P-position table; `mex` completeness holds with no skipped rows; modulo-$p(m)$ ray witnesses on $[Y_{n_1}^m, Y_{n_1}^m + p(m)]$ extend to all $Y \ge Y_{n_1}^m$; and Lemma 2.6 + `PROOF.md` Section 4 establish the infinite tail for $0 \le m \le 12$.
- Claim 3.5's p. 235 minus-sign typo is honestly documented rather than concealed, and the self-contained induction closes any literal objection to it.

pass: true
