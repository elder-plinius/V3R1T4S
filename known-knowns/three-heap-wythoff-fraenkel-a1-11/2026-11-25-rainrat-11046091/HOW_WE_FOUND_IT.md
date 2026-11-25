# How we found it

*(contributor text, unverified)*

1. **Brief**: Prove both of Fraenkel's three-heap Wythoff conjectures for smallest heap $A_1 = 12$ (and independently re-verify $0 \le m \le 11$, since open PR #1117 covers $A_1 = 11$ only and GONC 6 lists $A_1 \le 10$).
2. **Dual exact solvers**: Two independent C++20 solvers were run sequentially on the closed box $0 \le m \le Y \le Z \le 12000$:
   - `reverse.cpp`: downward-closed predecessor marking (~1.8 GiB RAM).
   - `direct.cpp`: sparse middle-row enumeration using signed-gap indexing and the identity $d_3 - d_2 = d - 2(d_2 \mathbin{\&} d)$ when $d_2 \oplus d_3 = d$.
   Both produced the exact same 59,483 P-positions (SHA-256 `30eed56f613e25ffabb9882c9e0bcd4e36889e48c05fef930e16c5ce5485b41d`).
3. **Resolving the Claim 3.5 midpoint typo & $m = 2$ window**:
   - Sun and Zeilberger (2004) p. 235 prints $\alpha' = \lfloor (\max - \min)/2 \rfloor$, which is nonnegative and impossible in Condition 7 ($\alpha^0 - \alpha' \ge 4m$); Table 1 requires the half-sum $\lfloor (\max + \min)/2 \rfloor$.
   - We therefore built `PROOF.md` with a self-contained Lemma 2.6 direct induction and Beatty-floor separation bound that avoids the misprinted formula, while also selecting $(n_2, n_1) = (101, 182)$ for $m = 2$ (fixing an earlier `n1 = 172` window whose span was $[-11, -10]$ rather than $[-11, -9]$) so every layer $1 \le m \le 12$ passes both Claim 3.5 (half-sum) and the direct induction simultaneously.
4. **Standalone stdlib verifier**: `verify_wythoff.py` shares no code with the C++20 solvers, cross-checks 3D game-tree DP on $p_3 \le 55$, recomputes P-positions through $Y \le 5500$ from the game rules, checks all 11 rows of Table 1, checks all Claim 3.3–3.5 and Lemma 2.6 conditions, and validates every field of `object/wythoff_a1_12_certificate.json` in ~31 seconds.
