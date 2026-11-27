# Verification Receipts (`conway-99-graph`, Track `p2`)

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
All 10 Track p2 UNSAT proofs (5 propositions x 2 encodings, 1879 RUP lemmas, 0 RAT lemmas) verified.
VERIFY: PASS
```

Exit status: `0`.

---

## 2. Certificate Inventory Across Both Independent SAT Encodings (5 Propositions x 2 Encodings = 10 Pure-RUP LRAT Proofs)

| Track | Proposition ID | Section 2.3 Statement in `arXiv:2608.11211` | Enc A Full Vars / Clauses | Enc A Core Clauses | Enc A RUP Lemmas | Enc B Full Vars / Clauses | Enc B Core Clauses | Enc B RUP Lemmas | RAT Lemmas |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `p2` | `p2_1_inner_matching_k14` | Neighborhood $\Gamma_1(0)$ ($k=14$) is a 1-regular union of 7 disjoint edges ($7 K_2$) under $\lambda=1$ | 273 / 716 | 4 | 1 | 259 / 688 | 4 | 1 | 0 |
| `p2` | `p2_2_outer_bijection_k14` | Non-neighbors $\Gamma_2(0)$ ($M=84$) indexed bijectively by non-matched pairs $\{a,b\}\subset\Gamma_1(0)$ (Constraint 1) | 1,598 / 1,578 | 13 | 3 | 1,585 / 1,576 | 12 | 3 | 0 |
| `p2` | `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\mathbf{1}_{m(a)\in P_u} + \deg_{\Gamma_2(0)\cap N(a)}(u) = 2$ for $a\notin P_u$, and $\deg_{\Gamma_2(0)\cap N(a)}(u)=1$ for $a\in P_u$ (Constraint 4) | 548 / 2,733 | 2,487 | 836 | 522 / 2,717 | 2,483 | 780 | 0 |
| `p2` | `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $E(u,v)+\mathrm{cn}_{\Gamma_2(0)}(u,v)=2-|P_u\cap P_v|$ (Constraints 2 & 3) | 91 / 407 | 345 | 142 | 87 / 407 | 342 | 111 | 0 |
| `p2` | `p2_5_srg9_uniqueness` | Uniqueness of reduced outer graph on $\mathrm{srg}(9,4,1,2)\cong K_3\square K_3$ (UNSAT with blocking clause; SAT without) | 66 / 201 | 13 | 1 | 42 / 147 | 7 | 1 | 0 |
| **Total** | **5 Propositions** | **10 Dual-Encoded Pure-RUP LRAT Certificates (`5,710` Core Clauses, `1,879` RUP Lemmas)** | — | **2,862** | **983** | — | **2,848** | **896** | **0** |
