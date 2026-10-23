# REPRODUCE Skeptic Report — Format 2x4x7 Rank 45 SLP in 164 Reduced Additions over Z

role: reproduce
skeptic: astra
context: subagent
context: subagent (astra)

## 1. Quoted Definition and Claimed Object

From the claim record (not shipped; `README.md` states the same values):
> # Claim: Format `(2, 4, 7)` Rank 45 Straight-Line Program in 164 Additions over `Z`
> - **Target**: `fmm-additive-complexity-records`
> - **Format**: `(2, 4, 7)` (`2x4x7`)
> - **Rank**: `m = 45` (matches the best rank in `fmm_sota.json`)
> - **Ring**: `Z` (ternary straight-line program, coefficients in `{-1, 1}`)
> - **Claimed Reduced Additions (`cr`)**: `164` (`fv = 50` fresh variables, `cn = 282` naive additions)
> - **Previous Best (`addition_reduced_ZT`)**: `174` (`2x4x7_m45_cr174_cn308_ZT_reduced.json`, margin `-10`)
> - **Other Sources**: `reduced_known.json` = `none`, `matmulcatalog` `adds` = `+308`, `fmm.univ-lille.fr/2x4x7.html` = no complexity variant listed
> - **Object File**: `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json`
> ## Definition Verified
> Every linear form in `u_fresh`, `u`, `v_fresh`, `v`, `w_fresh`, `w` is an acyclic sum/difference of already-computed quantities with coefficients in `{-1, 1}` (each binary `+/-` counted as 1 addition; negation is free), and the expanded bilinear forms compute the exact matrix product $C = A B$ over $\mathbb{Z}$ across all $n_1 n_2 n_3 n_1 n_2 n_3$ monomials.

From the target's success criterion:
> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format (n,m,p) with max(n,m,p) le 8 and rank r equal to the best rank listed for that format in fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column.

Mathematical definition of the straight-line program (SLP) and Brent equations for format `(n1, n2, n3) = (2, 4, 7)` and rank `m = 45` over `Z`:
- In each section (`U` with `na = 8` inputs, `V` with `nb = 28` inputs, `W` with `m = 45` product inputs), intermediate variables in `u_fresh`, `v_fresh`, `w_fresh` and output linear forms in `u`, `v`, `w` are linear combinations `sum_t c_t * var[idx_t]` with ternary coefficients `c_t in {-1, 1}`, strictly prior indices `idx_t` (acyclic DAG), and distinct `idx_t` within each form.
- Each linear form `f` of length `len(f) ge 1` contributes `len(f) - 1` binary additions/subtractions to the reduced addition count `cr`.
- Upon expanding the DAGs to basis matrices `U in Z^{45 x 8}`, `V in Z^{45 x 28}`, `W in Z^{14 x 45}`, all `8 * 28 * 14 = 3136` Brent equations over `Z` must hold identically:
$$\sum_{k=0}^{44} U_{k, i_1 n_2 + j_1} \, V_{k, j_2 n_3 + l_2} \, W_{l_3 n_1 + i_3, k} = \delta_{i_1, i_3} \, \delta_{j_1, j_2} \, \delta_{l_2, l_3}$$

## 2. File Integrity Verification

- **Path**: `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json`
- **Byte size**: `20225` bytes
- **SHA-256**: `c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429`
- **Dimensions & Rank**: `n = [2, 4, 7]`, `m = 45`, `z2 = false`
- **Declared Complexity**: `reduced = 164`, `naive = 282`

## 3. Independent Verification Before Reading Author Code

Before inspecting `verify-it-yourself/verify_slp.py`, I wrote and ran an independent Python SLP verifier from the mathematical definition:

1. **DAG Acyclicity, Ternary Coefficient, and Disjointness Audit**:
   - Verified that every term in `u_fresh` (`18` forms), `u` (`45` forms), `v_fresh` (`21` forms), `v` (`45` forms), `w_fresh` (`11` forms), and `w` (`14` forms) has integer coefficient strictly in `{-1, 1}`, references only strictly earlier variable indices within its own section (`0 le idx le var_id - 1`), has no duplicate variable indices within any single linear form, and shares no variables across `U`, `V`, `W`.
2. **Independent Addition and Fresh-Variable Count**:
   - Recounted reduced additions `cr = sum(len(form) - 1)`:
     - `cr(U) = 27` (`fv(U) = 18`)
     - `cr(V) = 64` (`fv(V) = 21`)
     - `cr(W) = 73` (`fv(W) = 11`)
     - **Total reduced additions**: `cr = 27 + 64 + 73 = 164` (matches claimed `cr = 164` exactly).
     - **Total fresh variables**: `fv = 18 + 21 + 11 = 50` (matches claimed `fv = 50` exactly).
   - Recounted expanded nonzeros and naive additions `cn = sum(max(0, nnz(row) - 1))`:
     - `nnz(U) = 114` (`cn(U) = 69`), `nnz(V) = 160` (`cn(V) = 115`), `nnz(W) = 112` (`cn(W) = 98`).
     - **Total naive additions**: `cn = 69 + 115 + 98 = 282` (matches claimed `cn = 282` exactly).
3. **Exhaustive Symbolic Brent Equation Verification over Z**:
   - Expanded all linear forms over `Z` and checked all `8 * 28 * 14 = 3136` Brent equations over `Z`.
   - Result: `total_eq = 3136`, `bad_eq = 0` (zero error on every bilinear monomial over `Z`).
4. **Step-by-Step Integer Matrix Multiplication Check**:
   - Evaluated the straight-line program step-by-step on deterministic integer matrices `A in Z^{2 x 4}` (`A_{i,j} = 3^{i n_2 + j} + (i+1)(j+2)`) and `B in Z^{4 x 7}` (`B_{j,l} = 5^{j n_3 + l} + (j+2)(l+3)`).
   - Confirmed that the step-by-step SLP output `C_SLP` equals `A * B` entrywise over `Z` across all `14` output entries (`matmul_ok = True`).
5. **1-Entry Corruption Negative Test**:
   - Flipped a single coefficient sign in `u[0][0]` (`value -> -value`).
   - Independent verifier rejected the corrupted SLP (`bad_eq = 10` mismatched Brent equations, `matmul_ok = False`).
   - Author's `verify-it-yourself/verify_slp.py` also rejected the corrupted SLP (`rc = 1`, `FAIL: object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json (corrupted) | Symbolic bilinear identity failed over Z (10 mismatched monomials)`).

## 4. Reproduction of Author Verification Command

Executed the author's verification command (as in `RUN_IT_YOURSELF.md`, with the shipped paths):
```
python3 verify-it-yourself/verify_slp.py object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json
```
Output (`exit 0`):
```
PASS: claim/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json | format=2x4x7 m=45 cr=164 (U=27, V=64, W=73) fv=50 cn=282
```
All temporary files created during verification were cleaned up.

pass: true
