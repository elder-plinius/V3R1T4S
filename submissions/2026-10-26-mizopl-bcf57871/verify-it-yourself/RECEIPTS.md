# Verification Receipts — `conway-99-graph` (`2026-10-26-mizopl-bcf57871`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Exact Terminal Output
```text
[PASS] Positive non-vacuity control on srg(9, 4, 1, 2) = K_3 box K_3 (Encoding A & Encoding B)
[PASS] Track p2 p2_1_inner_matching_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_2_outer_bijection_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_3_inner_outer_balance_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_4_outer_pair_cn_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_5_srg9_uniqueness: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p3_t1_fix33: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b1_c6_fix73: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b2_c5_fix51: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b0_c5_fix53: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b4_c3_fix19: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b2_c3_fix21: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b3_c2_fix11: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 frob21_z7_z3: Enc A & Enc B CNF membership + LRAT RUP verified
All 26 UNSAT proofs (13 theorems x 2 encodings, 19693 RUP lemmas, 0 RAT lemmas) verified.
VERIFY: PASS
```

## Summary of Machine Checks
- **Total Theorems Certified:** `13` (`5` forced-structure reduction propositions in Track `p2` + `8` prime-order and Frobenius automorphism exclusions in Track `p1`)
- **Total Independent SAT Encodings:** `2` (`Sinz_2005_Sequential_Counter` and `Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`)
- **Total UNSAT Proofs Verified:** `26` (`13` theorems $\times$ `2` encodings)
- **Total Core Clauses Verified Against Freshly Generated CNFs:** `44,756` (Encoding A) + `31,292` (Encoding B) = `76,048` clauses
- **Total LRAT Reverse Unit Propagation (RUP) Lemmas Verified:** `9,816` (Encoding A) + `9,877` (Encoding B) = `19,693` RUP steps (`0` RAT lemmas)
