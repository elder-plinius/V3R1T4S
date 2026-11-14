# REPRODUCE verdict: spherical-codes-cohn-table, cell 29-727

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:32:51Z

## Value computed here
- Method A (exact integer arithmetic): every coordinate parsed as an exact decimal rational, each vector scaled to integers, all 263,901 = 727*726/2 inner products and all squared norms computed exactly as Python integers; the top 20 pairs by float ranking resolved by exact rational comparison of d^2/(|u|^2|v|^2); square root by integer isqrt at 60 digits. c* = 0.2365029694576581825515416687051581290107.
- Method B (mpmath, mp.dps = 50): vectors normalised from the decimal strings, all 263,901 dot products with mp.fdot. c* = 0.2365029694576581825515416687051581290107.
- Difference A - B = 2.4e-52 (agreement to 50 digits). A numpy float64 Gram matrix gives 0.2365029694576582 on the same pair.
- Attaining pair: rows 697 and 722 (1-based; 696, 721 0-based), matching the pair named in the object's header comment. Runner-up pair (335, 718) at 0.236502949474352, 2.0e-8 below, so the float pre-ranking in Method A cannot have mis-ordered the maximum.
- Minimal angle: 76.319765750948303866 degrees.
- Table value 0.240054045231, taken from CLAIM.md (not re-fetched here; the live fetch is another skeptic's job). Margin table - c* = 0.0035510757733418174485, far above the 1e-10 requirement.

## Clauses checked
- File hash matches CLAIM.md (a796ba15...7e233ddc): PASS
- Shape: 1 comment line (starts with '#') plus 727 data rows, each with exactly 29 comma-separated coordinates: PASS
- Every one of the 21,083 coordinates matches the form d.ddd...e±NN with exactly 21 significant digits (min 21, max 21; 18,925 have no trailing zeros, so the digits are not float64 padding): PASS
- No NaN/Inf tokens, no malformed tokens, all numpy values finite: PASS
- No duplicate rows (0 exact duplicates), no zero vectors, and max cosine 0.2365 < 1 rules out repeated directions: PASS
- All N(N-1)/2 = 263,901 pairs evaluated by both methods, no sampling: PASS
- Two independent methods agree to 2.4e-52: PASS
- c* strictly lower than the CLAIM.md table cosine by at least 1e-10 (margin 3.55e-3): PASS
- Kissing-number exclusion: d = 29 is outside 9 <= d <= 23, so it does not apply: PASS
- The header comment's stated cos 0.236502969457658182551541668705 and pair (697,722) match what I computed: PASS (informational; the header was treated as data and did not influence the computation)

## Decision
The object file parses cleanly as 727 vectors in R^29 with 21 significant digits per coordinate. Exact integer arithmetic and 50-digit mpmath both give a maximum pairwise cosine of 0.23650296945765818255, on rows 697 and 722. That is 3.55e-3 below the table value 0.240054045231 stated in CLAIM.md. This verdict covers reproduction of the value only; the live table value, the optimality and "needs more optimization" marks, and arXiv supersession are for the other skeptics.

pass: true
