# Skeptic Panel — CRITERION

context: fresh research subagent invoked with zero solver history (role: CRITERION)
target_id: mint-linear-ooa-depth-2-to-8
checked_utc: 2026-11-10T18:41:05Z
injection_suspected: none

## Point-by-Point Criterion and Trap Audit

1. **Base `b = 3` and explicit field model (`F_3 = {0, 1, 2}` modulo 3)**:
   - On the live MinT query page `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2`, MinT lists supported bases `b in {2, 3, 4, 5, 7, 8, 9, 16, 25, 27, 32, 49, 64, 81, 128, 256}`; `b = 3` is in MinT's base list.
   - Because `3` is prime, the finite field `F_3` is uniquely `Z/3Z = {0, 1, 2}` under integer addition and multiplication modulo `3`. This field model is stated explicitly in `how-we-built-it/PREREG.md` (`prime field F_3 = {0, 1, 2}`), `verify-it-yourself/check_ooa.py` (`field alphabet F_3 = {0, 1, 2}` with exact arithmetic `% 3`), `README.md` (`over F_3`, `G * H^T = 0 (mod 3)`), and `object/ooa_b3_T2_m8_s8_k7.tsv` (explicit `8 x 16` matrices `G` and `H` with entries in `{0, 1, 2}`, SHA-256 `194ffead9a4b890088a7fd74dcaacdeb200e2b6f22f70081d38b141a6503e025`).
   - **Verdict**: MET.

2. **Matrix dimensions, block structure, and depth `2 <= T <= 8`**:
   - `object/ooa_b3_T2_m8_s8_k7.tsv` gives an explicit `m x (sT) = 8 x 16` generator matrix `G` over `F_3` with columns grouped into `s = 8` ordered blocks of `T = 2` columns (`b0_c0, b0_c1, ..., b7_c0, b7_c1`).
   - Depth `T = 2` satisfies `2 <= T <= 8` (neither `T = 1` orthogonal arrays nor infinite-depth digital nets).
   - **Verdict**: MET.

3. **Non-digital-net guard (`k > T`) and exhaustive left-justified strength `k = 7`**:
   - Claimed strength `k = 7` strictly exceeds depth `T = 2` (`7 > 2`), so the array is in the genuine intermediate-depth OOA regime and not a digital net (`k <= T`, which belongs to `mint-digital-nets-lower-t`).
   - Independent verification written from the definition confirmed `rank_F3(G) = 8`, `rank_F3(H) = 8`, and `G * H^T = 0 (mod 3)`. Enumerating all left-justified prefix column selections `(d_1, ..., d_8) in {0, 1, 2}^8` (taking the first `d_i` columns of each block `i`, never arbitrary column subsets) confirmed `0` rank-deficient submatrices for every total weight `1 <= w <= 7` (`8, 36, 112, 266, 504, 784, 1016` selections respectively; all `1,016` weight-7 selections have exact rank `7` over `F_3`), whereas at weight `w = 8`, `183` of `1,107` selections have rank `< 8`.
   - Dual exhaustive verification across all `3^8 - 1 = 6,560` nonzero codewords of `rowspan_F3(H)` confirmed minimum Rosenbloom-Tsfasman weight `d_RT = 8 = k + 1` (attained by `366 = 2 * 183` nonzero codewords), matching `t = m - k = 8 - 7 = 1`.
   - Running `sh verify-it-yourself/run_checks.sh` from the package root also exited `0` with final line `PASS`, including rejection of a corrupted `8 x 16` copy.
   - **Verdict**: MET.

4. **Live MinT comparison, direction `max` on `k`, and HTTP / index traps**:
   - One plain HTTP GET (`User-Agent: V3R1T4S-criterion-skeptic`, no retries) to the exact depth-2 cell query URL `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2` at `2026-11-10T18:41:05Z` returned `HTTP 200` (`8,336` bytes, SHA-256 `5aed6c5b2410094646d736a48515f8241cf76491caeafc8be5a0719482cb9dcf`, identical to `the-record-we-beat/mint_b3_T2_m8_s8_snapshot.md`; database footer `2024-09-05`).
   - Live MinT `'Constructive and linear'` entry for `(b, T, m, s) = (3, 2, 8, 8)`: `OOA(3^8, 8, F_3, 2, 8-2) over F_3` (`t_constructive = 2`, constructed as the dual of an `[(8, 2), 8, 7]`-NRT code from extended genus-2 algebraic-geometric code `AG_e(2; F, 9P)`), giving live linear strength `m - t_constructive = 8 - 2 = 6`.
   - Live MinT lower bound on `t` for `(b, T, m, s) = (3, 2, 8, 8)`: `OOA(3^8, 8, S_3, 2, 8-1) in Base 3` (`t_lower_bound = 1`, from the generalized Rao / dual Hamming sphere-packing bound `7,457 > 3^8 = 6,561`; no tighter linear-only lower bound is listed), giving `m - t_lower_bound = 8 - 1 = 7`.
   - Under `k = m - t` (direction `max` on `k`), the verified strength `k = 7` is STRICTLY GREATER than `8 - 2 = 6` (`7 > 6`) and at most `8 - 1 = 7` (`7 <= 7`, meeting the Rao/Hamming bound tightly).
   - **Verdict**: MET.

5. **Excluded cells and post-2008 literature / repository non-subsumption**:
   - The claimed cell `(b, T, m, s) = (3, 2, 8, 8)` is not in the excluded binary set `{(2, 2, 6, 6), (2, 2, 8, 7), (2, 2, 8, 8)}`.
   - Post-2008 OOA and NRT-code literature does not subsume this cell: LFSR constructions (Castoldi, Moura, Panario, and Stevens, `arXiv:2208.00333`, 2023) match the Rosenbloom-Tsfasman / Skriganov block bound `s <= b + 1 = 4 < 8` over `F_3`; function-field NRT codes over `F_3` require genus `g >= 2` to reach `s = 8` rational places (`N_3(0) = 4`, `N_3(1) = 7 < 8`, `N_3(2) = 8`), losing `g = 2` in Riemann-Roch (`k = 6`); and Wang, Li, and Heng (*IEEE Trans. Inf. Theory* 71(9), 6844-6856, 2025) do not give an `[8 x 2, 8, 8]_3` RT-metric code. Neither `TROPHY_CASE.md`, `known-knowns/`, nor any pull request in `elder-plinius/V3R1T4S` covers `mint-linear-ooa-depth-2-to-8`.
   - **Verdict**: MET.

6. **Single-cell scope, null model, attribution, zero prohibited wording, and privacy compliance**:
   - Exactly one table cell `(b, T, m, s) = (3, 2, 8, 8)` and one object file `object/ooa_b3_T2_m8_s8_k7.tsv` are claimed (`INDEX.csv` has one data row; `README.md` `## Not Claimed` excludes all other cells, digital nets, and partial wins `p1`/`p2`).
   - Null model: not needed (`how-we-built-it/PREREG.md` frozen at `2026-11-10T18:10:00Z` states deterministic algebraic verification over `F_3`, and `verify-it-yourself/check_ooa.py` includes a negative-control rank-deficiency check).
   - Full-text scan of all package files confirmed: zero Rule 4 prohibited promotional phrases, zero personal names, zero local user or temporary filesystem paths, zero email addresses or tokens, zero unfilled template placeholders, proper credit links in `README.md`, and `HOW_WE_FOUND_IT.md` explicitly marked `contributor text, unverified`.
   - **Verdict**: MET.

confirmed_scope: Explicit linear ordered orthogonal array OOA(3^8, 8, F_3, 2, 7) of depth T = 2, dimension m = 8, s = 8 blocks of 2 columns, and strength k = 7 > T = 2 over F_3 (an 8 x 16 matrix over F_3 verified exhaustively to have rank 7 across all 1,016 left-justified column selections of total weight 7, and dually verified across all 6,560 nonzero codewords of its Euclidean nullspace [(8, 2), 8, 8]-NRT code to have minimum Rosenbloom-Tsfasman weight d_RT = 8), improving on live MinT's constructive linear entry OOA(3^8, 8, F_3, 2, 6) (t = 2, k = 6) for cell (b, T, m, s) = (3, 2, 8, 8) and matching MinT's generalized Rao/Hamming lower bound t >= 1 (k <= 7).
pass: true
