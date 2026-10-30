# Claim: Partial Win (p2) on Minimum-Comparison Selection (n=18)

target_id: selection-min-comparisons-n16-n17
claim_type: partial_win_claim

## Claim Statement

We discover, certify, and dual-verify explicit comparison-selection algorithms for four cells of $n = 18$ ($i \in \{6, 7, 8, 9\}$, 1-based rank), formatted as acyclic Rust decision graphs, whose worst-case comparison counts strictly beat both the classical Hadian–Sobel bound $n - i + (i - 1)\lceil\log_2(n + 2 - i)\rceil$ and every value reported in Gasarch, Kelly, and Pugh (1996, Table 3, *SIGACT News* 27(2):88–96):

1. **$(18, 9)$ (9th element of 18)**:
   - Certified worst-case comparisons: **34**
   - Gasarch–Kelly–Pugh (1996) Table 3 bound: **37** (beating by **3 comparisons**)
   - Hadian–Sobel bound: **41** (beating by **7 comparisons**)
   - Decision graph size: 4,053 functions, 8,104 call sites

2. **$(18, 8)$ (8th element of 18)**:
   - Certified worst-case comparisons: **35**
   - Gasarch–Kelly–Pugh (1996) Table 3 bound: **37** (beating by **2 comparisons**)
   - Hadian–Sobel bound: **38** (beating by **3 comparisons**)
   - Decision graph size: 16,271 functions, 32,540 call sites

3. **$(18, 7)$ (7th element of 18)**:
   - Certified worst-case comparisons: **34**
   - Gasarch–Kelly–Pugh (1996) Table 3 bound: **35** (beating by **1 comparison**)
   - Hadian–Sobel bound: **35** (beating by **1 comparison**)
   - Decision graph size: 8,204 functions, 16,406 call sites

4. **$(18, 6)$ (6th element of 18)**:
   - Certified worst-case comparisons: **31**
   - Gasarch–Kelly–Pugh (1996) Table 3 bound: **32** (beating by **1 comparison**)
   - Hadian–Sobel bound: **32** (beating by **1 comparison**)
   - Decision graph size: 1,556 functions, 3,110 call sites

All four certificates are accepted by:
1. Cremer's static checker `verify_rs_algorithm.py` (with 0 doc-comment violations and valid parameter checks across all call sites).
2. The independent second checker `pathcheck.py` written from the definition without Cremer's code, confirming the exact worst-case depth on all acyclic paths.
