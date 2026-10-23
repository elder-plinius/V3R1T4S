# Criterion Skeptic Report: `fmm-additive-complexity-records` — Format `(2, 4, 7)` Rank 45 in 164 Additions over `Z`

context: subagent

## 1. Clause-by-Clause Verification Against the Target's Success Criterion

We audit the claimed straight-line program artifact `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json` (SHA-256 `c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429`), documented in `README.md` and reproducible via `RUN_IT_YOURSELF.md` and `verify-it-yourself/verify_slp.py`, against every literal requirement of `fmm-additive-complexity-records` in `the target's success criterion`:

1. **Explicit straight-line program for format `(n1, n2, n3)` with `max(n1, n2, n3)` at most 8 and rank `m` equal to the best rank in `fmm_sota.json`**:
   - **PASS.** `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json` is an explicit straight-line program for format `(2, 4, 7)` (`2x4x7`), satisfying `max(2, 4, 7) = 7` (at most 8), with bilinear rank `m = 45` matching the best-known rank in `fmm_sota.json` for `2x4x7`. All `m = 45` rows of expanded `U` (width `8`) and `V` (width `28`) and all `14` rows of expanded `W` (width `45`) are strictly non-zero with ternary expanded entries in `{-1, 0, 1}`.
2. **Verified symbolically to compute the full product `A*B` exactly over `Z` with ternary SLP coefficients in `{-1, 1}`**:
   - **PASS.** `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json` has `z2 = false`. Running `verify-it-yourself/verify_slp.py` confirms that every linear form in `u_fresh` (`18` forms), `u` (`45` forms), `v_fresh` (`21` forms), `v` (`45` forms), `w_fresh` (`11` forms), and `w` (`14` forms) uses only ternary coefficients in `{-1, 1}`, references only strictly preceding variables in an acyclic DAG without duplicate variable indices per form, and shares no variables across `U` (`A`-forms), `V` (`B`-forms), and `W` (product-forms). Symbolic expansion over `Z` confirms zero error across all `(2 * 4 * 7)^2 = 3136` bilinear monomials of `C = A * B`.
3. **Reduced addition count `cr` under Perminov's reduced convention strictly less than all live reference bounds**:
   - **PASS.** Under Perminov's reduced convention (each binary `+/-` in `u_fresh`, `u`, `v_fresh`, `v`, `w_fresh`, `w` counts as `1` addition, i.e., `len(form) - 1`; multiplication by `-1` is free; no other scalar multiplications exist), `verify-it-yourself/verify_slp.py` recounts `cr = 164` additions (`U = 27`, `V = 64`, `W = 73`, matching `complexity.reduced = 164`, with `fv = 50` total fresh variables and `cn = 282` naive additions). Comparing against all live reference sources recorded in `README.md` and `the-record-we-beat/README.md`:
     - Perminov `addition_reduced_ZT` minimum for `2x4x7` at rank `45`: `cr = 174` (`2x4x7_m45_cr174_cn308_ZT_reduced.json`), beaten strictly by `-10` additions (`164` vs `174`).
     - Perminov `reduced_known.json` for `2x4x7-45`: `none` (`164` is strictly lower).
     - Perminov `README.md` and `CHANGELOG.md`: no lower reduced addition count for `2x4x7` at rank `45`.
     - `fmm.univ-lille.fr/2x4x7.html`: no complexity variant listed.
     - `solven-eu/matmulcatalog` `COVERAGE.md` `adds` column for `2x4x7`: `+308` (`164` is strictly lower).
4. **Exclusions & Null-Model / Subsumption Checks**:
   - **Not a GF(2)-only SLP**: Verified symbolically over `Z` (`z2 = false`), not modulo 2.
   - **Not a higher-rank SLP**: Uses the exact catalogue best rank `m = 45`.
   - **Not a rank-lowering claim**: Claims only the additive complexity reduction at fixed rank `m = 45`.
   - **Single format per claim**: This package covers exclusively format `(2, 4, 7)`.

## 2. Confirmed Scope

confirmed_scope: Explicit exact integer (ring Z) ternary straight-line program in claim/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json (sha256 c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429) for format (2, 4, 7) at best-known rank m = 45 with reduced addition count cr = 164 (U = 27, V = 64, W = 73, fv = 50, cn = 282), symbolically verified across all 3136 bilinear monomials over Z and strictly beating Perminov addition_reduced_ZT (174 in 2x4x7_m45_cr174_cn308_ZT_reduced.json, margin -10), reduced_known.json (none), README.md/CHANGELOG.md (no lower count), fmm.univ-lille.fr/2x4x7.html (no complexity variant listed), and matmulcatalog COVERAGE.md adds (+308).

pass: true
