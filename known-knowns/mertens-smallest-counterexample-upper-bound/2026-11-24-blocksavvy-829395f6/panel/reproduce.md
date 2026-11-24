# REPRODUCE skeptic report, claim_v3 (Kim-Nguyen arXiv:2502.21021v1 Tables 1-2, p1)

context: fresh-context knowledgeWork skeptic launched by parent session (relaunch after interrupted first attempt)

Scope seen: a copy of claim_v3/ (in a private sandbox folder), kit/RULES.md, and one fetch of the arXiv v1 PDF. Not read: claim/, claim_v2/, panel/, panel_v2/, other panel_v3 files, attempts/, PANEL_BRIEFS*, other sandbox folders, the earlier reproduce attempt. SHA256SUMS.txt of the copy: all 17 files OK.

## Definitions (quoted from my own pdftotext of arXiv:2502.21021v1)
- Sec. 2.1: "γ := Im ρ, α := |ρζ′(ρ)|^−1, ψ := arg(ρζ′(ρ))"
- (2.6): "hP(y) := 2 Σ_{γ<14000} α exp(−1.5 · 10^−6 γ^2) cos(γy − ψ)"
- (2.7): "hStR(y) := 2 Σ_{γ<74000} α exp(−3 · 10^−9 γ^2) cos(γy − ψ)"
These agree with the definitions in claim_v3/CLAIM.md (sum over zeros with γ > 0).

## Method (all my own code, written before reading the author's code)
1. Zeros (KNOWN library, NUMERICAL-certified): python-flint 0.9.0 in a sandbox venv, `acb.zeta_zeros(n0, 400)` at 256 bits for n = 1..99,200 (248 chunks, 3 workers, nice 10, one file per chunk written atomically, so resumable); ζ′(ρ) from the first-order jet `acb_series.zeta(acb_series([ρ,1]))[1]`; Re ρ asserted to be exactly 1/2. Enclosures written as plain `arb.str(more=False)` strings (Arb guarantees the parsed string ball contains the value). Wall time about 26 min.
2. Completeness (PROVED-HERE, by Arb's rigorous count): index list 1..99,200 has no gaps and γ_n is certified strictly increasing; `arb.zeta_nzeros` returns exact counts N(14000) = 14950 and N(74000) = 98625; γ_14950 = 13999.73323828320175229822 < 14000 < γ_14951 = 14001.22872573036583642327 and γ_98625 = 73999.70302662447060247899 < 74000 < γ_98626 = 74000.65088718601965066604.
3. Evaluation (NUMERICAL, ball arithmetic): for each of the 19 y in claim_v3/inputs/ (y parsed exactly as integer/10^6), α = 1/|ρζ′(ρ)|, ψ = arg(ρζ′(ρ)), h = 2 Σ α exp(−kγ^2) cos(γy − ψ) over n ≤ N(T), at 256 and 320 bits (zeros re-parsed at 320 bits). Resulting radii ≤ 4.3e-30. Takes about 8 s.
4. Shipped values: every row of claim_v3/result/p1_certified_values.json matched by y (all 19 present, N counts 98625/14950 equal to mine); checked file, k, h_256 and h_320 overlap my balls, shipped `overlap` flag true, `abs_minus_1_lower` overlaps my |h|−1, and my 320- and 256-bit balls lie inside the shipped balls. Result: ALL_SHIPPED_VALUES_VERIFIED True.
5. Printed values: one plain curl of https://arxiv.org/pdf/2502.21021v1 (User-Agent naming V3R1T4S) at 2026-11-24T13:05:06Z: HTTP 200, application/pdf, 828676 bytes, sha256 3141e044428b0ec955407ef0ef44682faed61c36cc8b8cfec3b26587b5818f54 (same as the hash in CLAIM.md). `pdftotext -layout`; my own regex parser read all 5 Table 1 rows and 14 Table 2 rows (y, h, y+√y mantissa and exponent); the parsed y equal the inputs/ files row by row. (The table lines in inputs/kn_arxiv_v1_tables_excerpt.txt are identical to my extraction.)
6. Comparison (my own code, exact rationals from ball endpoints): display at the printed number of decimals under rounding (half away from zero) and truncation (toward zero); MATCH = whole ball maps to the printed value, MISMATCH = no point does, else AMBIGUOUS. Also 3-decimal renderings, and y+√y (ball) rendered to the printed 4 significant digits under both conventions.
7. check/spot_check_zeros.py (author's, unmodified) on my own zero files: chunks n0 = 1, 49601, 98401 converted to its jsonl layout (fields copied verbatim from my files).
8. Determinism: recomputed my zero chunks n0 = 1, 49601, 98801 from scratch: byte-identical. Re-ran my evaluator and comparator: output JSON byte-identical (sha256 my values 7ab4346a9e07..., compare 3cbe5e1e436a...). Author's check/compare_printed.py re-run in my copy: its .json and .md byte-identical to the shipped ones; its counts and row classes equal mine.

## Per-row results (my balls, my parse of the PDF)
| table | row | y | printed | my h_320 ball | 7 dp | at printed dp (round / trunc) | rounding | truncation | 3 dp printed (r/t) | 3 dp certified (r/t) | y+√y printed | y+√y (r/t) | y+√y mode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 821801872381554552551865.064536 | 0.991 | [0.991173511338183522489481518265 +/- 8.00e-32] | 0.9911735 | 0.991 / 0.991 | MATCH | MATCH | 0.991 / 0.991 | 0.991 / 0.991 | 8.218 e23 | 8.218 / 8.218 | both |
| 1 | 2 | 1217019235269548564510534.246242 | -0.993 | [-0.993065928074099927752401729153 +/- 3.99e-31] | -0.9930659 | -0.993 / -0.993 | MATCH | MATCH | -0.993 / -0.993 | -0.993 / -0.993 | 1.217 e24 | 1.217 / 1.217 | both |
| 1 | 3 | 2316046459031032843375257.362502 | -1.012 | [-1.01221587682662347221214029774 +/- 8.59e-31] | -1.0122159 | -1.012 / -1.012 | MATCH | MATCH | -1.012 / -1.012 | -1.012 / -1.012 | 2.316 e24 | 2.316 / 2.316 | both |
| 1 | 4 | 13355123870465460300049497.114138 | 1.0019 | [1.00188610592665099701662316778 +/- 1.97e-30] | 1.0018861 | 1.0019 / 1.0018 | MATCH | MISMATCH | 1.002 / 1.001 | 1.002 / 1.001 | 1.336 e25 | 1.336 / 1.335 | rounded |
| 1 | 5 | 15070658556209921536065525.478881 | 1.0004 | [1.00044972982669395581599707160 +/- 3.47e-30] | 1.0004497 | 1.0004 / 1.0004 | MATCH | MATCH | 1.000 / 1.000 | 1.000 / 1.000 | 1.507 e25 | 1.507 / 1.507 | both |
| 2 | 1 | 8895437864289868028.044074 | -0.974798 | [-0.974793333630889913344783775431 +/- 3.04e-31] | -0.9747933 | -0.974793 / -0.974793 | MISMATCH | MISMATCH | -0.975 / -0.974 | -0.975 / -0.974 | 8.895 e18 | 8.895 / 8.895 | both |
| 2 | 2 | 13859539710197847064.062257 | -0.9949 | [-0.994969466373158315674447361146 +/- 6.14e-32] | -0.9949695 | -0.9950 / -0.9949 | MISMATCH | MATCH | -0.995 / -0.994 | -0.995 / -0.994 | 1.386 e19 | 1.386 / 1.385 | rounded |
| 2 | 3 | 19571878850562201959.215107 | -1.007 | [-1.00745157221803272139976673191 +/- 3.34e-30] | -1.0074516 | -1.007 / -1.007 | MATCH | MATCH | -1.007 / -1.007 | -1.007 / -1.007 | 1.957 e19 | 1.957 / 1.957 | both |
| 2 | 4 | 44533695580955902790.827323 | -0.9949 | [-0.995000723738640793845909769044 +/- 1.45e-31] | -0.9950007 | -0.9950 / -0.9950 | MISMATCH | MISMATCH | -0.995 / -0.994 | -0.995 / -0.995 | 4.453 e19 | 4.453 / 4.453 | both |
| 2 | 5 | 64171705557420452732.080835 | -1.02 | [-1.02065148019900842134390022441 +/- 4.28e-30] | -1.0206515 | -1.02 / -1.02 | MATCH | MATCH | -1.02 / -1.02 | -1.021 / -1.020 | 6.417 e19 | 6.417 / 6.417 | both |
| 2 | 6 | 133837185572795505699.262652 | -0.9998977 | [-0.999897661097617449254601724357 +/- 1.83e-31] | -0.9998977 | -0.9998977 / -0.9998976 | MATCH | MISMATCH | -1.000 / -0.999 | -1.000 / -0.999 | 1.338 e20 | 1.338 / 1.338 | both |
| 2 | 7 | 155558488686568113612.224656 | 1.025 | [1.02558429356430827151384458116 +/- 3.16e-32] | 1.0255843 | 1.026 / 1.025 | MISMATCH | MATCH | 1.025 / 1.025 | 1.026 / 1.025 | 1.555 e20 | 1.556 / 1.555 | truncated |
| 2 | 8 | 185415676820850375395.577179 | -0.997 | [-0.997360343678521710198230780347 +/- 1.80e-32] | -0.9973603 | -0.997 / -0.997 | MATCH | MATCH | -0.997 / -0.997 | -0.997 / -0.997 | 1.854 e20 | 1.854 / 1.854 | both |
| 2 | 9 | 189471283149477540226.654238 | 0.997 | [0.997507296794185041458949676447 +/- 3.69e-31] | 0.9975073 | 0.998 / 0.997 | MISMATCH | MATCH | 0.997 / 0.997 | 0.998 / 0.997 | 1.894 e20 | 1.895 / 1.894 | truncated |
| 2 | 10 | 834072772235759174844.571429 | 1.0017 | [1.00179189692629580004416982013 +/- 3.61e-30] | 1.0017919 | 1.0018 / 1.0017 | MISMATCH | MATCH | 1.002 / 1.001 | 1.002 / 1.001 | 8.341 e20 | 8.341 / 8.340 | rounded |
| 2 | 11 | 955426264098867920866.136509 | -1.0002 | [-1.00020809765475070064870954971 +/- 3.90e-30] | -1.0002081 | -1.0002 / -1.0002 | MATCH | MATCH | -1.000 / -1.000 | -1.000 / -1.000 | 9.554 e20 | 9.554 / 9.554 | both |
| 2 | 12 | 875055372917917742274.218133 | 1.00057 | [1.00058814190967899070284390736 +/- 2.30e-30] | 1.0005881 | 1.00059 / 1.00058 | MISMATCH | MISMATCH | 1.001 / 1.000 | 1.001 / 1.000 | 8.751 e20 | 8.751 / 8.750 | rounded |
| 2 | 13 | 1622648223749122520779.415144 | 1.0079 | [1.00794964327416058479267552745 +/- 3.14e-30] | 1.0079496 | 1.0079 / 1.0079 | MATCH | MATCH | 1.008 / 1.007 | 1.008 / 1.007 | 1.623 e21 | 1.623 / 1.622 | rounded |
| 2 | 14 | 1883922422293221654459.096574 | -1.00004 | [-1.00007182999346744510505858101 +/- 3.08e-30] | -1.0000718 | -1.00007 / -1.00007 | MISMATCH | MISMATCH | -1.000 / -1.000 | -1.000 / -1.000 | 1.883 e21 | 1.884 / 1.883 | truncated |

Counts: rounding {'MATCH': 11, 'MISMATCH': 8, 'AMBIGUOUS': 0}; truncation {'MATCH': 13, 'MISMATCH': 6, 'AMBIGUOUS': 0}. Expected 8 and 6 mismatches, 0 ambiguous: met.

## Classification checks
- Wrong under either convention (corrections): Table 2 rows 1, 4, 12, 14, and no others. Matches CLAIM.md.
- Mismatch under rounding only (convention-dependent, not corrections): Table 2 rows 2, 7, 9, 10. Under truncation only: Table 1 row 4 and Table 2 row 6. Matches CLAIM.md; none is labelled a correction there.
- At 3 decimals: Table 2 row 4 printed −0.9949 → −0.995 (round) / −0.994 (trunc); certified −0.995 / −0.995, so it disagrees only under truncation (convention-dependent), as CLAIM.md says. 3-dp disagreements under rounding are only Table 2 rows 7, 9; under truncation only Table 2 row 4. Rows 1, 12, 14 agree at 3 dp under both. Table 2 row 5 is printed with 2 decimals (MATCH at that precision both ways).
- y+√y column: print equals the rounded value only (differs from truncation) at Table 1 row 4, Table 2 rows 2, 10, 12, 13; the truncated value only at Table 2 rows 7, 9, 14; both agree at the other 11 rows; no row matches neither; exponents correct. Exactly the mix CLAIM.md states.
- Record row (Table 2 row 3): |h_StR| > 1 + 6e-8 holds rigorously in my ball.
- CLAIM.md 19-row table, all columns (y, printed, 7 dp, at printed dp both conventions, 3 dp both conventions, |diff|, both classifications), the 3-dp deliverable table and the 4 correction balls: compared field by field with my results, 0 discrepancies.

## spot_check_zeros.py on my zero files
- n0 = 1: 400 zeros, balls not containing the 512-bit reference: 0, max midpoint diff (my file vs the script's no-`more` writer): [5.00e-74 +/- 3e-81], ok True
- n0 = 49601: 400 zeros, balls not containing the 512-bit reference: 0, max midpoint diff (my file vs the script's no-`more` writer): [5.00e-72 +/- 3e-79], ok True
- n0 = 98401: 400 zeros, balls not containing the 512-bit reference: 0, max midpoint diff (my file vs the script's no-`more` writer): 0, ok True
- ALL_OK True

## Notes (not failures)
- My first cross-check also required the shipped 20-digit midpoint string to lie in my 1e-30-radius ball; that is not a valid test (the shipped midpoint is a decimal rounding) and failed for that reason only. I replaced it by the stronger valid test that my ball is contained in the shipped ball, which passes for all 19.
- Same library as the author (Arb/FLINT), so this is an independent computation, not an independent method (caveat already stated in CLAIM.md).
- Only arXiv v1 was checked against print, as the claim scopes itself.

Discrepancies found: none. Missing objects: none. Misclassifications: none. Non-determinism: none.

pass: true
