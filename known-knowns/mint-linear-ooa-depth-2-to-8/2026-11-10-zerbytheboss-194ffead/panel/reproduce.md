# Skeptic Panel — REPRODUCE

- context: fresh research subagent invoked with zero solver history (role: REPRODUCE)
- target_id: mint-linear-ooa-depth-2-to-8
- object_verified: object/ooa_b3_T2_m8_s8_k7.tsv (sha256: 194ffead9a4b890088a7fd74dcaacdeb200e2b6f22f70081d38b141a6503e025)

## 1. Target Definition Quoted from Specification

From the target specification (`mint-linear-ooa-depth-2-to-8`):

> A linear OOA(b^m, s, F_b, T, k) of depth T is an m x (sT) matrix over F_b whose columns form s blocks of T columns, such that for every (d_1..d_s) with 0 <= d_i <= T and d_1+...+d_s = k the first d_i columns of each block are linearly independent.
>
> Success means an explicit m x (sT) matrix over F_b (b in MinT's list; field model stated for prime powers), with columns grouped into s blocks of T, whose strength k (every left-justified selection (d_1..d_s), 0 <= d_i <= T, sum k, has full column rank k, checked exhaustively) is STRICTLY GREATER (direction: max) than m minus the 'Constructive and linear' t on the live MinT query page ... for some depth 2 <= T <= 8 with k > T, and at most m minus that page's linear lower bound on t. With k <= T the array is a digital net; such cells belong to mint-digital-nets-lower-t and do not count here. The cells (b,T,m,s) = (2,2,6,6), (2,2,8,7) and (2,2,8,8), already reached in the 2026-10-30 lane and skeptic checks, do not count.

For cell `(b, T, m, s) = (3, 2, 8, 8)` over the prime field `F_3 = {0, 1, 2}`:
- `2 <= T = 2 <= 8`, and `k = 7 > T = 2` (strictly outside the digital-net regime), and `(3, 2, 8, 8)` is not one of the three excluded base-2 cells (`PROVED-HERE`).
- Live MinT (`the-record-we-beat/mint_b3_T2_m8_s8_snapshot.md`) lists constructive linear `t = 2` (`k = 8 - 2 = 6`) and lower bound `t >= 1` (`k <= 8 - 1 = 7`), so `k = 7` strictly exceeds `6` and meets the upper bound `7` (`KNOWN` / `PROVED-HERE`).

## 2. Independent Combinatorial Derivations from First Principles

### 2.1 Exact Count of Left-Justified Selections (`1,016`, Not `1,024`)

A common pitfall is confusing left-justified depth-`T = 2` prefix selections with choosing 7 of 8 blocks and picking 1 of 2 columns independently (`C(8, 7) * 2^7 = 1,024`). Under the OOA definition, a left-justified selection is a tuple `(d_1, ..., d_8)` in `{0, 1, 2}^8` with `d_1 + ... + d_8 = 7`, taking the **first** `d_i` columns of block `i` (`PROVED-HERE`).

Let `c_2`, `c_1`, `c_0` be the counts of indices `i` with `d_i = 2`, `1`, `0` respectively. Then `c_0 + c_1 + c_2 = 8` and `c_1 + 2*c_2 = 7`, so `c_1 = 7 - 2*c_2` and `c_0 = 1 + c_2` for `c_2 in {0, 1, 2, 3}`:
- `c_2 = 0` (`(c_2, c_1, c_0) = (0, 7, 1)`): `C(8, 0) * C(8, 7) = 1 * 8 = 8`
- `c_2 = 1` (`(c_2, c_1, c_0) = (1, 5, 2)`): `C(8, 1) * C(7, 5) = 8 * 21 = 168`
- `c_2 = 2` (`(c_2, c_1, c_0) = (2, 3, 3)`): `C(8, 2) * C(6, 3) = 28 * 20 = 560`
- `c_2 = 3` (`(c_2, c_1, c_0) = (3, 1, 4)`): `C(8, 3) * C(5, 1) = 56 * 5 = 280`

Summing across all four cases gives `8 + 168 + 560 + 280 = 1,016` (`PROVED-HERE`). Cross-checking by inclusion-exclusion on `[x^7](1 + x + x^2)^8 = [x^7](1 - x^3)^8 * (1 - x)^(-8)`:
`C(14, 7) - 8 * C(11, 7) + 28 * C(8, 7) = 3,432 - 2,640 + 224 = 1,016` (`PROVED-HERE`).

### 2.2 Generalized Rao / Ordered Hamming Sphere-Packing Bound (`7,457 > 6,561`)

In one block `(x_0, x_1)` in `F_3^2`, the Rosenbloom-Tsfasman (RT) weight enumerator is `1 + 2*z + 6*z^2` (`1` zero pair, `2` pairs `(x_0, 0)` with `x_0 != 0`, and `6` pairs `(x_0, x_1)` with `x_1 != 0`). Across `s = 8` blocks, the volume of the RT ball of radius `e = floor(8 / 2) = 4` is `[z^0..z^4](1 + 2*z + 6*z^2)^8`:
- `w_RT = 0`: `1`
- `w_RT = 1`: `8 * 2 = 16`
- `w_RT = 2`: `8 * 6 + C(8, 2) * 4 = 48 + 112 = 160`
- `w_RT = 3`: `8 * 7 * 6 * 2 + C(8, 3) * 8 = 672 + 448 = 1,120`
- `w_RT = 4`: `C(8, 2) * 36 + 8 * C(7, 2) * 6 * 4 + C(8, 4) * 16 = 1,008 + 4,032 + 1,120 = 6,160`

Total ball volume `1 + 16 + 160 + 1,120 + 6,160 = 7,457 > 3^8 = 6,561`, ruling out `k = 8` (`t = 0`) and confirming `k <= 7` (`t >= 1`) (`KNOWN` / `PROVED-HERE`).

## 3. Independent Verification of `object/ooa_b3_T2_m8_s8_k7.tsv`

Before trusting `verify-it-yourself/check_ooa.py`, I wrote an independent verifier from scratch using two distinct methods (`PROVED-HERE`):
1. **Exact `w x w` minor determinants modulo 3** across every left-justified selection of weight `w in {1, ..., 8}`.
2. **Direct combinatorial run-table projection**: generating all `3^8 = 6,561` runs `x * G mod 3` (`x in F_3^8`) and checking directly, for all `1,016` weight-7 left-justified column selections, whether every one of the `3^7 = 2,187` tuples in `F_3^7` occurs with exact multiplicity `3^(8 - 7) = 3`.

Results on `object/ooa_b3_T2_m8_s8_k7.tsv` (`PROVED-HERE`):
- **Dimensions and alphabet**: `G` and `H` are `8 x 16` matrices with all entries in `{0, 1, 2}`.
- **Full ranks**: `rank(G) = 8` over `F_3` (columns `{0, 1, 2, 3, 4, 5, 6, 8}` are upper-triangular with diagonal `(1, 1, 1, 1, 1, 1, 1, 2)`, determinant `2 != 0 mod 3`) and `rank(H) = 8` over `F_3` (columns `{7, 9, 10, 11, 12, 13, 14, 15}` of `H` form the exact `8 x 8` identity matrix `I_8`).
- **Exhaustive left-justified submatrix ranks by minor determinants**:
  - `w = 1`: `8 / 8` full rank (`0` dependent)
  - `w = 2`: `36 / 36` full rank (`0` dependent)
  - `w = 3`: `112 / 112` full rank (`0` dependent)
  - `w = 4`: `266 / 266` full rank (`0` dependent)
  - `w = 5`: `504 / 504` full rank (`0` dependent)
  - `w = 6`: `784 / 784` full rank (`0` dependent)
  - `w = 7`: `1,016 / 1,016` full rank (`0` dependent)
  - `w = 8`: `924 / 1,107` full rank (`183` dependent, e.g. `(0, 0, 0, 0, 2, 2, 2, 2)`), confirming exact strength `k = 7`.
- **Direct combinatorial OOA verification**: Across all `1,016` weight-7 selections and all `6,561` runs (`6,665,976` projected 7-tuples), every one of the `2,187` elements of `F_3^7` appears with exact multiplicity `3` (`0` violations).
- **Dual NRT code verification**: Because `rank(G) = rank(H) = 8` and `G * H^T = 0 (mod 3)`, `rowspan(H) = ker(G)`. The complete RT weight enumerator across all `3^8 = 6,561` codewords in `rowspan(H)` is `[(0, 1), (8, 366), (9, 112), (10, 504), (11, 784), (12, 1624), (13, 1008), (14, 1232), (15, 672), (16, 258)]`, confirming `A_1 = ... = A_7 = 0` and exact minimum RT distance `d_RT = 8 = k + 1`.

## 4. Hand Verification of `G * H^T = 0 (mod 3)` and Non-Trivial 7-Column Submatrices

### 4.1 Exact Orthogonality `G * H^T = 0 (mod 3)` Across All Rows

Columns `0..6` of `G` are `[I_7; 0]^T` (`e_0, ..., e_6` in `F_3^8`), row `7` of `G` has `G[7][0..7] = 0` and `G[7][8..15] = (2, 0, 1, 1, 1, 2, 2, 0)`, and columns `{7, 9, 10, 11, 12, 13, 14, 15}` of `H` equal `I_8`. Thus for each row `h_j` of `H`, `(G * h_j^T)[0..6] = h_j[0..6] + sum_{c=7..15} h_j[c] * G[0..6, c] (mod 3)` and `(G * h_j^T)[7] = sum_{c=8..15} h_j[c] * G[7, c] (mod 3)` (`PROVED-HERE`):
- `h_0` (`c=7` is `1`): row 7 gives `0`; rows `0..6` give `(0,2,1,2,2,2,2) + (0,1,2,1,1,1,1) = (0,3,3,3,3,3,3) = 0 (mod 3)`.
- `h_1` (`c=9` is `1`): row 7 gives `0`; rows `0..6` give `(2,1,1,2,0,1,0) + (1,2,2,1,0,2,0) = (3,3,3,3,0,3,0) = 0 (mod 3)`.
- `h_2` (`c=8,10` are `1,1`): row 7 gives `2 + 1 = 3 = 0`; rows `0..6` give `(1,2,0,2,1,0,2) + (1,0,2,0,0,2,1) + (1,1,1,1,2,1,0) = (3,3,3,3,3,3,3) = 0 (mod 3)`.
- `h_3` (`c=8,11` are `1,1`): row 7 gives `2 + 1 = 3 = 0`; rows `0..6` give `(1,1,2,2,2,1,1) + (1,0,2,0,0,2,1) + (1,2,2,1,1,0,1) = (3,3,6,3,3,3,3) = 0 (mod 3)`.
- `h_4` (`c=8,12` are `1,1`): row 7 gives `2 + 1 = 3 = 0`; rows `0..6` give `(2,0,0,1,2,2,2) + (1,0,2,0,0,2,1) + (0,0,1,2,1,2,0) = (3,0,3,3,3,6,3) = 0 (mod 3)`.
- `h_5` (`c=8,13` are `2,1`): row 7 gives `4 + 2 = 6 = 0`; rows `0..6` give `(1,2,2,0,0,1,0) + (2,0,4,0,0,4,2) + (0,1,0,0,0,1,1) = (3,3,6,0,0,6,3) = 0 (mod 3)`.
- `h_6` (`c=8,14` are `2,1`): row 7 gives `4 + 2 = 6 = 0`; rows `0..6` give `(0,1,2,2,0,2,2) + (2,0,1,0,0,1,2) + (1,2,0,1,0,0,2) = (3,3,3,3,0,3,6) = 0 (mod 3)`.
- `h_7` (`c=15` is `1`): row 7 gives `0`; rows `0..6` give `(2,1,1,1,2,2,0) + (1,2,2,2,1,1,0) = (3,3,3,3,3,3,0) = 0 (mod 3)`.

### 4.2 Manual Row-Reduction over `F_3` on Non-Trivial 7-Column Submatrices

1. **Selection `d = (0, 0, 0, 0, 1, 2, 2, 2)` (blocks `4..7` only; `d_i = 2` on 3 blocks, `d_4 = 1`; columns `[8, 10, 11, 12, 13, 14, 15]`)** (`PROVED-HERE`):
   - Pivot 1 at `(r0, c8) = 1` (`[1,1,1,0,0,1,1]`); eliminating `c8` yields on `[c10..c15]`: `r1=[1,2,0,1,2,2]`, `r2=[2,0,1,0,1,0]`, `r3=[1,1,2,0,1,2]`, `r4=[2,1,1,0,0,1]`, `r5=[2,1,2,1,1,2]`, `r6=[2,0,0,1,1,2]`, `r7=[2,2,1,2,0,1]`.
   - Pivot 2 at `(r1, c10) = 1`; eliminating `c10` yields on `[c11..c15]`: `r2=[2,1,1,0,2]`, `r3=[2,2,2,2,0]`, `r4=[0,1,1,2,0]`, `r5=[0,2,2,0,1]`, `r6=[2,0,2,0,1]`, `r7=[1,1,0,2,0]`.
   - Pivot 3 at `(r7, c11) = 1`; eliminating `c11` leaves on `[c12..c15]`: `r2=[2,1,2,2]`, `r3=[0,2,1,0]`, `r4=[1,1,2,0]`, `r5=[2,2,0,1]`, `r6=[1,2,2,1]`.
   - Pivot 4 at `(r4, c12) = 1`; eliminating `c12` leaves on `[c13..c15]`: `r2=[2,1,2]`, `r3=[2,1,0]`, `r5=[0,2,1]`, `r6=[1,0,1]`.
   - Pivot 5 at `(r6, c13) = 1`; adding `r6` to `r2` and `r3` gives on `[c14, c15]`: `r2=[1,0]` (Pivot 6) and `r3=[1,1]`, with `r3 - r2 = [0,1]` (Pivot 7). Exact rank = `7`.

2. **Selection `d = (0, 0, 0, 2, 2, 2, 0, 1)` (`d_i = 2` on blocks `3, 4, 5` and `d_7 = 1`; columns `[6, 7, 8, 9, 10, 11, 14]`)** (`PROVED-HERE`):
   - `c6 = e_6` gives Pivot 1 in `r6`. On the remaining 7 rows `[r0..r5, r7]` and columns `[7, 8, 9, 10, 11, 14]`:
   - Pivot 2 at `(r1, c7) = 1` (`[1,0,2,1,2,2]`) and Pivot 3 at `(r0, c8) = 1` (`[0,1,1,1,1,1]`) reduce `[c9, c10, c11, c14]` on `[r2, r3, r4, r5, r7]` to `r2=[2,0,2,0]`, `r3=[2,0,2,2]`, `r4=[1,1,2,1]`, `r5=[1,1,2,2]`, `r7=[1,2,2,0]`.
   - Pivot 4 at `(r4, c9) = 1` reduces `[c10, c11, c14]` to `r7 - r4 = [1,0,2]` (Pivot 5), `(r3 + r4) - (r7 - r4) = [0,1,1]` (Pivot 6), and `r5 - r4 = [0,0,1]` (Pivot 7). Exact rank = `7`.

3. **Selection `d = (0, 1, 1, 1, 1, 1, 1, 1)` (`d_i = 1` on 7 blocks `1..7`; columns `[2, 4, 6, 8, 10, 12, 14]`)** (`PROVED-HERE`):
   - Columns `c2 = e_2`, `c4 = e_4`, `c6 = e_6` immediately provide 3 pivots on rows `r2, r4, r6`.
   - Restricting `[c8, c10, c12, c14]` to rows `[r0, r1, r3, r5, r7]` gives `[[1,1,0,1], [0,1,0,2], [0,1,2,1], [2,1,2,0], [2,1,1,2]]`.
   - `r0=[1,1,0,1]` (Pivot 4) and `r1=[0,1,0,2]` (Pivot 5) eliminate `c8` and `c10`, yielding `r3 - r1 = [0,0,2,2]` and `(r5 + r0) + r1 = [0,0,2,0]`, which visibly span `F_3^2` on `[c12, c14]` (Pivots 6 and 7). Exact rank = `7`.

## 5. Audit of `verify-it-yourself/` and `how-we-built-it/`

- **`verify-it-yourself/check_ooa.py`, `run_checks.sh`, `RECEIPTS.md`**:
  - Inspected `check_ooa.py` line by line (`226` lines, Python standard library only). There is no hardcoded pass, tautology, or shortcut: it parses `object/ooa_b3_T2_m8_s8_k7.tsv`, validates headers, dimensions, and `F_3` alphabet, runs a genuine negative calibration check (overwriting column `14` with column `0` and verifying `check_primal_ooa` rejects), recomputes the Rao volume `7,457 > 6,561`, checks `rank(G) = rank(H) = 8` and `G * H^T = 0 (mod 3)`, exhaustively row-reduces all `1,016` weight-7 left-justified submatrices over `F_3`, and exhaustively checks all `6,560` nonzero dual codewords in `rowspan(H)` for `w_RT >= 8` (`PROVED-HERE`).
  - Re-running `sh verify-it-yourself/run_checks.sh` exited `0` and reproduced `verify-it-yourself/RECEIPTS.md` verbatim, ending with `PASS`.
- **`how-we-built-it/PREREG.md`**:
  - Freezes target `mint-linear-ooa-depth-2-to-8`, cell `(3, 2, 8, 8)` over `F_3`, exact criterion (`k = 7 > 6` across all `1,016` left-justified selections), and `null_test: not needed because exact finite-field matrix rank over F_3 across all 1016 left-justified selections is a deterministic algebraic property`.
- **`how-we-built-it/search_ooa_f3.c`**:
  - Audited the C99 solver and verified C99 syntax/types (`cc -std=c99 -Wall -Wextra -Wpedantic -fsyntax-only`, clean aside from one unused inline helper `vec_sub`). Heap allocation `ADD3` is freed cleanly on re-initialization and at `done:` (`0` memory leaks). Note: `main()` lists unreached fallback probes at `m = 10` after `try_cell(8, 8, 7, 0)` despite `MAX_M = 9`, but `try_cell(8, 8, 7, 0)` returns `1` and jumps directly to `done:`, so all executed cells (`m = 6` and `m = 8`, `3^8 = 6,561 <= 19,683`) remain strictly inside every static and dynamic buffer bound.
  - Proved and empirically tested the `F_3^m` DP transition (`apply_block_dp` and `block_valid`): `cur_cost` (`dp_stack[blk_idx]`) and `nxt_cost` (`dp_stack[blk_idx + 1]`) are distinct buffers (preventing intra-block double-counting), and scalar invariance `cur_cost[2*x] == cur_cost[x]` holds inductively over `F_3^* = {1, 2}`, so testing `u`, `v`, `v + u`, and `v + 2u` in `block_valid` covers all 2 cost-1 combinations `{u, 2u}` and all 6 cost-2 combinations `{v, 2v, v+u, 2v+2u, v+2u, 2v+u}` (`PROVED-HERE`).
  - Tested `apply_block_dp` + `block_valid` against brute-force left-justified submatrix rank across `1,800` random/adversarial prefix states (`1,359` valid, `441` invalid), observing `0` mismatches, and fed the 8 blocks of `G` through both `k_lim = 7` and uncapped `k_lim = 16` DP over all `6,561` vectors in `F_3^8`, confirming exact agreement on every vector (`cost 0: 1, cost 1: 16, cost 2: 160, cost 3: 1120, cost 4: 4550, cost 5: 714`, covering radius `5`) (`PROVED-HERE`).

pass: true
