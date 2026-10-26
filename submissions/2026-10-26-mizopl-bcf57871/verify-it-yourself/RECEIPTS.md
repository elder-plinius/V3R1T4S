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
[PASS] Track p1 p7_fix1: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p5_t1_fix9: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p3_t1_fix33: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 frob21_z7_z3: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b1_c6_fix73: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b2_c5_fix51: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b3_c4_fix33: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b4_c3_fix19: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b5_c2_fix9: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b6_c1_fix3: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b0_c5_fix53: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b1_c4_fix35: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b2_c3_fix21: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b3_c2_fix11: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b4_c1_fix5: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b5_c0_fix3: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a2_b0_c3_fix23: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a2_b1_c2_fix13: Enc A & Enc B CNF membership + LRAT RUP verified
All 46 UNSAT proofs (23 theorems x 2 encodings, 92137 RUP lemmas, 0 RAT lemmas) verified.
VERIFY: PASS
```

## Summary of Machine Checks
- **Total Theorems Certified:** `23` (`5` forced-structure reduction propositions in Track `p2` + `18` prime-order and Frobenius automorphism exclusions in Track `p1`, including the resolution of the open prime order $p = 7$ case `p7_fix1`)
- **Total Independent SAT Encodings:** `2` (`Sinz_2005_Sequential_Counter` and `Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`)
- **Total UNSAT Proofs Verified:** `46` (`23` theorems $\times$ `2` encodings)
- **Total Core Clauses Verified Against Freshly Generated CNFs:** `146,183` (Encoding A) + `89,587` (Encoding B) = `235,770` clauses
- **Total LRAT Reverse Unit Propagation (RUP) Lemmas Verified:** `55,502` (Encoding A) + `36,635` (Encoding B) = `92,137` RUP steps (`0` RAT lemmas)
