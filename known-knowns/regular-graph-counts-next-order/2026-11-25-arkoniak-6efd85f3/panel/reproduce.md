# REPRODUCE skeptic verdict

Definition quoted: "U_4(N) = (1/N!) sum_{g in S_N} Fix(g) ... U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!; 1 + sum U(n) x^n = prod (1 - x^n)^(-C(n))".

1. Independent checker (own script, written before reading claim code, in scratch dir). From results/Dd4_NN_lane{0,1}.txt for N=5..50 (last non-ERR/TIMEOUT row per partition):
   - every partition of N (own enumeration) present, no extras, for all N=5..50: no MISSING/EXTRA output.
   - U(N) = sum F_D/z computed with Fractions: always an integer.
   - U(N) equals methodA/A_terms_d4.txt and data/cx_table_U4.txt for N=29..50 (0 mismatches); equals methodA for N=5..50.
   - C(N) by own inverse Euler transform (U<5 from results/dsum_small_d4.txt, else lane files) equals data/cx_table_C4.txt for N=29..50 and methodA C column (0 mismatches); C(N)=b006820.txt for N=1..28 and U(N)=b033301.txt for N=0..28 (0 mismatches).
   - Output: `bad 0 U50 4567863967927930120629311714346947864974124915610296 C50 4567863812490955416720841969219753968607349955976192`
   - Note: A_terms_d4.txt contains two non-data trailer lines (primes:5 nmax:58 ... mismatches:0, PASS), skipped.
2. REPRODUCE.md checks on a copy:
   - Check 1: `N=50 types=204226 ... AGREE` with matching U_D=U_A, as stated.
   - Check 2: four lines "MISMATCH 0" (checked=22 each), as stated.
   - Check 3: `b033301.txt: checked=29 MISMATCH 0`, `b006820.txt: checked=28 (n=1..28) MISMATCH 0`, as stated.
   - Check 4: F_D(2^16 1^18) = 10422622897928329195570205540102481474954032334149688161566546236, equals the saved lane1 row and the stated value.
   - Method-A rerun to N=36 (97 s): output rows N=5..36 identical (diff empty) to methodA/A_terms_d4.txt; trailing FAIL is the documented no-bbfile message.
3. Extra method-D recomputation of types I chose: 3^7 2^3 1^4 (N=31) = 3736913418157743; 5 4 4 3 3 2 2 1 1 1 (N=26) = 267507; 6 6 6 2 2 2 1 1 1 1 1 (N=29) = 4304826526. All equal saved lane rows.

Caveat: the independent check shares the saved data; method D and A agreement plus external CX/OEIS tables are the independent evidence. Not recomputed: all 204k types at N=50 from scratch (infeasible in budget); saved rows were verified by sum, not individually recomputed.

Mismatches: none. No missing objects, no non-determinism seen.

context: subagent (fresh, general-purpose)
pass: true
