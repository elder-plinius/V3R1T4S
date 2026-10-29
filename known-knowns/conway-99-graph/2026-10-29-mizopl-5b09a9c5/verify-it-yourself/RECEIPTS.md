# Verification Receipts (`conway-99-graph`)

## 1. Standalone Checker Execution (`sh verify-it-yourself/run_checks.sh`)

Command executed from a clean copy of the submission directory:

```bash
sh verify-it-yourself/run_checks.sh
```

Exact output:

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
[PASS] Track p1 p2_a2_b2_c1_fix7: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a2_b3_c0_fix5: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a3_b0_c1_fix9: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a3_b1_c0_fix7: Enc A & Enc B CNF membership + LRAT RUP verified
All 54 UNSAT proofs (27 theorems x 2 encodings, 92259 RUP lemmas, 0 RAT lemmas) verified.
VERIFY: PASS
```

Exit status: `0`.

---

## 2. Certificate Inventory Across Both Independent SAT Encodings (27 Theorems x 2 Encodings = 54 Pure-RUP LRAT Proofs)

| Track | ID | Mathematical Statement / Automorphism Case | Enc A Full Vars / Clauses | Enc A Core Clauses | Enc A RUP Lemmas | Enc B Full Vars / Clauses | Enc B Core Clauses | Enc B RUP Lemmas | RAT Lemmas |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `p2` | `p2_1_inner_matching_k14` | Neighborhood $\Gamma_1(0)$ is a union of 7 disjoint edges ($7 K_2$) | 469 / 1,107 | 23 | 1 | 595 / 1,457 | 21 | 1 | 0 |
| `p2` | `p2_2_outer_bijection_k14` | Non-neighbors $\Gamma_2(0)$ indexed bijectively by non-matched pairs $\{u,v\}\subset\Gamma_1(0)$ ($|\Gamma_2(0)|=84$) | 4,005 / 9,532 | 12 | 2 | 5,264 / 13,221 | 12 | 2 | 0 |
| `p2` | `p2_3_inner_outer_balance_k14` | Inner-outer degree balance ($|N(x)\cap(\Gamma_2(0)\setminus\{p\})| \in \{1,2\}$) | 22 / 49 | 16 | 4 | 31 / 66 | 17 | 4 | 0 |
| `p2` | `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation ($e_{pq}+\sum_r e_{pr}e_{qr}=2-|P_p\cap P_q|$) | 674 / 1,622 | 355 | 4 | 839 / 2,348 | 491 | 4 | 0 |
| `p2` | `p2_5_srg9_uniqueness` | Uniqueness of $\mathrm{srg}(9,4,1,2)\cong K_3\square K_3$ (UNSAT with blocking clause; SAT without) | 124 / 298 | 75 | 9 | 168 / 442 | 76 | 7 | 0 |
| `p1` | `p7_fix1` | Prime $p=7$: 1 fixed vertex, $14\times 7$-cycles (`p7_orbit_top6`) | 4,296 / 9,330 | 909 | 56,515 | 6,418 / 26,337 | 2,523 | 23,551 | 0 |
| `p1` | `p5_t1_fix9` | Prime $p=5$: 9 fixed vertices, $18\times 5$-cycles (`p5_orbit_sym`) | 4,946 / 10,803 | 1,636 | 3,667 | 7,090 / 24,599 | 2,906 | 3,130 | 0 |
| `p1` | `p3_t1_fix33` | Prime $p=3$: 33 fixed vertices, $22\times 3$-cycles | 8,402 / 19,213 | 85 | 17 | 11,462 / 29,215 | 67 | 20 | 0 |
| `p1` | `frob21_z7_z3` | Subgroup $\mathrm{Frob}(21)=\mathbb{Z}_7\rtimes\mathbb{Z}_3$: 1 fixed vertex, $4\times 7$-orbits, $3\times 21$-orbits (`frob21_fig10`) | 2,045 / 4,672 | 125 | 25 | 2,860 / 7,610 | 89 | 16 | 0 |
| `p1` | `p2_a0_b1_c6_fix73` | Prime $p=2$, profile $(0,1,6)$: 73 fixed vertices, $13\times 2$-cycles | 21,956 / 54,485 | 78 | 11 | 28,996 / 79,577 | 50 | 12 | 0 |
| `p1` | `p2_a0_b2_c5_fix51` | Prime $p=2$, profile $(0,2,5)$: 51 fixed vertices, $24\times 2$-cycles | 65,642 / 168,269 | 117 | 11 | 83,316 / 237,833 | 75 | 12 | 0 |
| `p1` | `p2_a0_b3_c4_fix33` | Prime $p=2$, profile $(0,3,4)$: 33 fixed vertices, $33\times 2$-cycles | 43,394 / 110,601 | 5,288 | 112 | 55,616 / 157,809 | 2,953 | 109 | 0 |
| `p1` | `p2_a0_b4_c3_fix19` | Prime $p=2$, profile $(0,4,3)$: 19 fixed vertices, $40\times 2$-cycles | 27,258 / 68,487 | 4,581 | 88 | 35,442 / 99,003 | 2,535 | 90 | 0 |
| `p1` | `p2_a0_b5_c2_fix9` | Prime $p=2$, profile $(0,5,2)$: 9 fixed vertices, $45\times 2$-cycles (`spectral_trace`) | 22,571 / 56,574 | 5,187 | 184 | 29,217 / 80,687 | 2,952 | 200 | 0 |
| `p1` | `p2_a0_b6_c1_fix3` | Prime $p=2$, profile $(0,6,1)$: 3 fixed vertices, $48\times 2$-cycles (`spectral_trace`) | 16,659 / 41,286 | 56 | 1 | 21,671 / 59,259 | 45 | 1 | 0 |
| `p1` | `p2_a1_b0_c5_fix53` | Prime $p=2$, profile $(1,0,5)$: 53 fixed vertices, $23\times 2$-cycles | 70,836 / 181,694 | 9,854 | 164 | 89,820 / 256,544 | 5,627 | 165 | 0 |
| `p1` | `p2_a1_b1_c4_fix35` | Prime $p=2$, profile $(1,1,4)$: 35 fixed vertices, $32\times 2$-cycles | 46,964 / 119,868 | 145 | 16 | 60,096 / 170,792 | 92 | 25 | 0 |
| `p1` | `p2_a1_b2_c3_fix21` | Prime $p=2$, profile $(1,2,3)$: 21 fixed vertices, $39\times 2$-cycles | 29,639 / 74,715 | 6,401 | 150 | 38,443 / 107,745 | 3,604 | 150 | 0 |
| `p1` | `p2_a1_b3_c2_fix11` | Prime $p=2$, profile $(1,3,2)$: 11 fixed vertices, $44\times 2$-cycles | 19,216 / 47,472 | 3,345 | 65 | 25,366 / 69,366 | 1,861 | 62 | 0 |
| `p1` | `p2_a1_b4_c1_fix5` | Prime $p=2$, profile $(1,4,1)$: 5 fixed vertices, $47\times 2$-cycles (`spectral_trace`) | 19,179 / 47,803 | 2,869 | 127 | 24,957 / 68,494 | 1,648 | 126 | 0 |
| `p1` | `p2_a1_b5_c0_fix3` | Prime $p=2$, profile $(1,5,0)$: 3 fixed vertices, $48\times 2$-cycles (`spectral_trace`) | 16,659 / 41,286 | 4,053 | 1,073 | 21,671 / 59,259 | 2,422 | 996 | 0 |
| `p1` | `p2_a2_b0_c3_fix23` | Prime $p=2$, profile $(2,0,3)$: 23 fixed vertices, $38\times 2$-cycles | 32,256 / 81,561 | 9,858 | 182 | 41,738 / 117,345 | 5,748 | 216 | 0 |
| `p1` | `p2_a2_b1_c2_fix13` | Prime $p=2$, profile $(2,1,2)$: 13 fixed vertices, $43\times 2$-cycles | 20,762 / 51,519 | 6,683 | 202 | 27,316 / 75,045 | 3,777 | 200 | 0 |
| `p1` | `p2_a2_b2_c1_fix7` | Prime $p=2$, profile $(2,2,1)$: 7 fixed vertices, $46\times 2$-cycles (`global_triangle_bijection`) | 10,126 / 23,365 | 1,250 | 39 | 14,016 / 36,227 | 677 | 39 | 0 |
| `p1` | `p2_a2_b3_c0_fix5` | Prime $p=2$, profile $(2,3,0)$: 5 fixed vertices, $47\times 2$-cycles (`global_triangle_bijection`) | 10,167 / 23,465 | 1,303 | 40 | 14,078 / 36,396 | 679 | 40 | 0 |
| `p1` | `p2_a3_b0_c1_fix9` | Prime $p=2$, profile $(3,0,1)$: 9 fixed vertices, $45\times 2$-cycles (`global_triangle_bijection`) | 10,084 / 23,233 | 1,231 | 1 | 13,937 / 35,986 | 74 | 1 | 0 |
| `p1` | `p2_a3_b1_c0_fix7` | Prime $p=2$, profile $(3,1,0)$: 7 fixed vertices, $46\times 2$-cycles (`global_triangle_bijection`) | 10,151 / 23,425 | 1,297 | 185 | 14,050 / 36,317 | 693 | 185 | 0 |
| **Total** | **27 Theorems** | **54 Dual-Encoded Pure-RUP LRAT Proofs** | — | **67,853** | **62,895** | — | **39,587** | **29,364** | **0** |
