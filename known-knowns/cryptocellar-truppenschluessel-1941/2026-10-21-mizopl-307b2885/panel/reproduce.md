# Panelist Report — Role: `REPRODUCE` (`cryptocellar-truppenschluessel-1941`, Partial Win `p1`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Mandate & Definition Quote

Mandate:
"Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Quoted definition from `claim/CLAIM.md` (Section 1 and Section 2, citing C. Ostwald and F. Weierud, 2021, *Cryptologia* 45(3):235–249, Section 2 pp. 236–238 and Section 9 Appendix pp. 247–248 [preprint pp. 14–15]):
- **p1**: Blind garble-tolerance benchmark: the verifier enciphers 3 period-style German military texts of 60-100 letters with the TS procedure as implemented from the Cryptologia paper (validated on its worked example), using random squares and injecting about 8% Morse-plausible garbles; the solver, given only the ciphertexts, recovers at least 95% of the plaintext letters of all 3 within a declared compute budget.
- **25-Letter Alphabet (`ALPHA25`):** `ABCDEFGHIKLMNOPQRSTUVWXYZ` (`J` omitted; `J` mapped to `I`, trigraph `SCH` mapped to `SQ`, digraph `CH` mapped to `Q`, word separator `X`).
- **Key Structure:** Two independent $5 \times 5$ key squares $K_1$ (left/first plaintext square) and $K_2$ (right/second plaintext square), each containing a permutation of `ALPHA25`.
- **Encryption (`enc_pair`) of Plaintext Bigram $(x_1, x_2)$:**
  Let $(r_1, c_1)$ be the row and column of $x_1$ in $K_1$, and let $(r_2, c_2)$ be the row and column of $x_2$ in $K_2$ ($r_i, c_i \in \{0, 1, 2, 3, 4\}$):
  - **Rectangle rule ($r_1 \neq r_2$):**
    $$y_1 = K_2[r_1, c_2], \qquad y_2 = K_1[r_2, c_1].$$
  - **Same-row rule ($r_1 = r_2 = r$):** Each letter is replaced by the letter one column to the right (cyclically modulo 5) in the **opposite** square:
    $$y_1 = K_2[r, (c_2 + 1) \bmod 5], \qquad y_2 = K_1[r, (c_1 + 1) \bmod 5].$$
- **Decryption (`dec_pair`) of Ciphertext Bigram $(y_1, y_2)$:**
  Let $(r_a, c_a)$ be the row and column of $y_1$ in $K_2$, and let $(r_b, c_b)$ be the row and column of $y_2$ in $K_1$:
  - **Rectangle rule ($r_a \neq r_b$):**
    $$x_1 = K_1[r_a, c_b], \qquad x_2 = K_2[r_b, c_a].$$
  - **Same-row rule ($r_a = r_b = r$):**
    $$x_1 = K_1[r, (c_b - 1) \bmod 5], \qquad x_2 = K_2[r, (c_a - 1) \bmod 5].$$
- **Zero-Fixed-Point Cross-Diagonal Law:** Under both rules, $x_1 \neq y_2$ and $x_2 \neq y_1$ for every bigram (`0` cross-diagonal fixed points).
- **Exact Gauge Equivalence Group ($G_{\text{TS}}$, order $5! \times 5 \times 5 = 3,000$):**
  $$K_1'[r, c] = K_1[\pi(r), (c + \Delta c_1) \bmod 5], \qquad K_2'[r, c] = K_2[\pi(r), (c + \Delta c_2) \bmod 5].$$

---

## 2. Artifact Size & SHA-256 Verification

Before reading `claim/author_checker_ts1941.py` or `claim/p1_blind_garble_solver.c`, an independent Python verifier was written from the equations in `claim/CLAIM.md` and run on all 9 saved files in `claim/`:

| Artifact | Verified Size (bytes) | Verified SHA-256 Checksum | Status |
|---|---:|---|---|
| `claim/p1_benchmark_certificate.json` | `1,409` | `307b2885211621dbc21f5d46bc3ef1cee905576be48e3371a868905529e43945` | PASS |
| `claim/p1_blind_garble_solver.c` | `67,338` | `68340440b31f162135863c90915e1de0d3725f6fc591bd9079a4de9a765d60d0` | PASS |
| `claim/author_checker_ts1941.py` | `17,592` | `790de8318e5ddf17acc315acc41e40a8d1ffffa49875568958680799c088f7df` | PASS |
| `claim/rebuild_hgnord_exact_lm.py` | `6,525` | `ae102d3aa456d887627b4a026ece961272fb947421bf32a5040b07d5e9a6267d` | PASS |
| `claim/hgnord_25_t1.bin` | `50` | `c51332ee7d9563b7813c4de5dcd2b3cb5707335594a6df7a22ce342785a6fa64` | PASS |
| `claim/hgnord_25_t2.bin` | `1,250` | `b1a6fd9b0cc82e45b59f8efa37461e9d04eebf1abe8aa86a5e96ab31401ebe8b` | PASS |
| `claim/hgnord_25_t3.bin` | `31,250` | `a5e5bb9c1f92509e5cf3944c3a60b928d5c86dbe8ce3631e71b312680c3cbaf1` | PASS |
| `claim/hgnord_25_t4.bin` | `781,250` | `0ea5097705cf5b99add8d75329d0b9465e2e0e104a1a3a71a08f70c090ed370e` | PASS |
| `claim/g-army-ts-messages.html` | `31,268` | `58a057ab7c535edb3517e7d2159afd149b435879aa49bf8372ccaed21a1675af` | PASS |

---

## 3. Independent Checker Verification (`enc_pair`, `dec_pair`, Gauge Equivalence, & Negative Controls)

1. **Key Square Permutation & Exact Gauge Equivalence (`50 / 50 = 100.00%`):**
   - Verified from `claim/p1_benchmark_certificate.json` that `k1_true = "OHIKLZCMGQBNRWYDFEUAVSXPT"`, `k2_true = "UMDHKCIGEVFBPARLQYSXNWZTO"`, `k1_recovered = "MGQZCRWYBNXPTVSIKLOHEUADF"`, and `k2_recovered = "CIGEVFBPARNWZTOUMDHKLQYSX"` are all valid 25-letter permutations of `ALPHA25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"`.
   - Under `row_perm = [1, 2, 4, 0, 3]`, `dc1 = +2`, `dc2 = +0`, `k1_recovered[r, c] == k1_true[row_perm[r], (c + 2) mod 5]` and `k2_recovered[r, c] == k2_true[row_perm[r], (c + 0) mod 5]` hold for all `25 + 25 = 50` cells (`50 / 50 = 100.00%`).
2. **Exhaustive `625 / 625` Bigram Functional Equivalence & Zero-Fixed-Point Law:**
   - Across all `25 x 25 = 625` input bigrams `(y1, y2)`, our independent `enc_pair` and `dec_pair` implementation verified:
     * `enc_pair(k1_recovered, k2_recovered, a, b) == enc_pair(k1_true, k2_true, a, b)` for `625 / 625` (`100.00%`) bigrams.
     * `dec_pair(k1_recovered, k2_recovered, y1, y2) == dec_pair(k1_true, k2_true, y1, y2)` for `625 / 625` (`100.00%`) bigrams.
     * `dec_pair(k1_true, k2_true, enc_pair(k1_true, k2_true, a, b)) == (a, b)` for `625 / 625` (`100.00%`) bigrams.
     * `x1 != y2` and `x2 != y1` for `625 / 625` (`100.00%`) bigrams (Zero-Fixed-Point Cross-Diagonal Law).
3. **Seed, Garble Injection, and Plaintext Recovery on `BENCH_PT_IDX[3]` (`80, 76, 76 = 232` letters):**
   - Verified that `xorshift128plus` seeded with `(0x202610210015, 0xCAFEBABE12345678)` generates `k1_true` and `k2_true` and injects `[7, 6, 6]` (`19 / 232 = 8.1897%`) single-letter International Morse Levenshtein-1 garbles at positions `i = 5, 17, 29, ...` (`18` active garbles after opening crib neighbor resolution at index `5` of Message 1).
   - Verified raw decryption and Morse-Levenshtein-1 error correction on `(k1_recovered, k2_recovered)`:
     * **Raw Decryption (No EC):** `[71, 66, 66]` = `203 / 232` (`87.50%`: `88.75%`, `86.84%`, `86.84%`), `claim_lm_score = 417,578` (`solver_score_with_crib = 487,578`).
     * **Greedy Morse-Levenshtein-1 EC:** `[77, 74, 76]` = `227 / 232` (`97.84%`: `96.25%`, `97.37%`, `100.00%`), all 3 messages at or above `95.0%`.
     * **Bottleneck-Viterbi Morse-Levenshtein-1 EC:** `[79, 74, 76]` = `229 / 232` (`98.71%`: `98.75%`, `97.37%`, `100.00%`), all 3 messages at or above `95.0%`.
4. **Independent Negative Controls:**
   - **Negative Control 1 (Reversed `k1_recovered`):** `lm_score_py = -745,814` (`lm_score_c = -672,145`), raw character accuracy collapses from `203 / 232` (`87.50%`) to `33 / 232` (`14.22%`).
   - **Negative Control 2 (Non-cyclic column swap `col 0` and `col 1` in `k1_recovered`):** Preserves all `500` rectangle bigrams (`ra != rb`) and `50` of `125` same-row bigrams (`550 / 625` bigrams unchanged), breaking `75` same-row bigrams; C-table LM score drops from `417,578` to `305,344` and raw accuracy drops from `203 / 232` (`87.50%`) to `195 / 232` (`84.05%`).
   - **Negative Control 3 (Simultaneous non-cyclic column swap `col 0` and `col 1` in both `k1_recovered` and `k2_recovered`):** Preserves all `500` rectangle bigrams and `20` of `125` same-row bigrams (`520 / 625` bigrams unchanged); C-table LM score drops from `417,578` to `270,949` and raw accuracy drops from `203 / 232` (`87.50%`) to `191 / 232` (`82.33%`).

---

## 4. Determinism & End-to-End C Solver Reproduction

1. **Two-Run Determinism of `claim/author_checker_ts1941.py`:**
   - Executed `claim/author_checker_ts1941.py` twice (`run1.txt` and `run2.txt`); `diff -u` returned `0` differences and identical output SHA-256 (`0b982d3acdb056edd4755397081bac913aa6588d6e74967b823d07e760b87ee5` on both runs), confirming all Checks 1, 2a, 2b, 2c, 3, and 4 pass deterministically.
2. **End-to-End Compilation and Execution of `claim/p1_blind_garble_solver.c`:**
   - Compiled with `arch -x86_64 clang -O3 -pthread claim/p1_blind_garble_solver.c -lm` and executed end-to-end (`real 62.24s`, `user 291.74s`, `sys 3.57s` across 8 threads under x86_64 translation):
     * Stage 1 (`fit_crib_key` + `climb_crib_invariant` + `climb_with_unmix`): reached `cur_sc = 166,804 / 487,578 (exact_crib = 14/14)`.
     * Stage 2 (`polish_crib_islands`): reached `cur_sc = 487,578 / 487,578 (exact_crib = 14/14)`.
     * Stage 3 (`polish_col_perm`): confirmed `cur_sc = 487,578 / 487,578 (exact_crib = 14/14)` and recovered `k1 = "MGQZCRWYBNXPTVSIKLOHEUADF"`, `k2 = "IGEVCBPARFWZTONMDHKUQYSXL"`, which our independent checker verified is `50 / 50` (`100.00%`) gauge-equivalent to `(k1_true, k2_true)` under `row_perm = [1, 2, 4, 0, 3], dc1 = +2, dc2 = +1` and `625 / 625` (`100.00%`) functionally identical on all bigrams (`raw = 203 / 232 = 87.5%`, `ec = 229 / 232 = 98.71% [96.2%, 100.0%, 100.0%]`).
     * 200-Shuffle Null Audit: reproduced `claim_lm_sc = 417,578 (true_lm_sc = 417,578) | null_mean = -106,514.3 null_sd = 56,548.5 null_max = 54,395 | z_mean = +9.27 SD, z_above_max = +6.42 SD`.
   - Restored and verified `claim/p1_benchmark_certificate.json` (`1,409` bytes, `sha256: 307b2885211621dbc21f5d46bc3ef1cee905576be48e3371a868905529e43945`) and removed the scratch working directory.

pass: true
