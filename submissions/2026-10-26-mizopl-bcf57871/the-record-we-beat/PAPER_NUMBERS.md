# Exact Literature Numbers vs. Machine-Certified Quantities (`conway-99-graph`)

| Reference | Theorem / Proposition | Prior Status | Present Certificate (`object/certificate.json`) |
|---|---|---|---|
| `arXiv:2608.11211v2` §2.3 | Forced $1$-regular matching on $\Gamma_1(x)$ ($k=14$) | Prose proof | `p2_1_inner_matching_k14`: Dual DRAT + LRAT (`4`/`4` core clauses, `1`/`1` RUP lemma, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 | Bijection $\Gamma_2(x) \leftrightarrow 84$ non-matched pairs | Prose proof | `p2_2_outer_bijection_k14`: Dual DRAT + LRAT (`13`/`12` core clauses, `3`/`3` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 (Constraint 4) | Inner-outer coordinate balance $\mathbf{1}_{m(a)\in P_u} + \deg_{N(a)}(u) = 2$ | Prose proof | `p2_3_inner_outer_balance_k14`: Dual DRAT + LRAT (`2487`/`2483` core clauses, `836`/`780` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 (Constraints 2–3) | Outer pair common-neighbor equation $E(u,v) + \mathrm{cn}_{\Gamma_2}(u,v) = 2 - s$ | Prose proof | `p2_4_outer_pair_cn_k14`: Dual DRAT + LRAT (`345`/`342` core clauses, `142`/`111` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 | Validation on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ | CP-SAT run | `p2_5_srg9_uniqueness`: Positive SAT control + Dual DRAT + LRAT uniqueness (`13`/`7` core clauses, `1`/`1` RUP lemma) |
| `arXiv:2308.02978` §4.1 | Prime order $p=3$ fixing $33$ vertices ($22 \times 3$-cycles) | Custom search (no DRAT/LRAT) | `p3_t1_fix33`: Dual DRAT + LRAT (`166`/`251` core clauses, `23`/`35` RUP lemmas, `0` RAT) |
| `arXiv:2308.02978` §4.2 | Prime order $p=2$ involutions fixing $73, 53, 51, 21, 19, 11$ vertices | Custom search (no DRAT/LRAT) | `p2_a0_b1_c6_fix73` .. `p2_a1_b3_c2_fix11`: 12 DRAT + LRAT proofs (`0` RAT) |
| `arXiv:2308.02978` Prop 4.10 | Frobenius subgroup $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ ($p=7,3$) | Custom search (no DRAT/LRAT) | `frob21_z7_z3`: Dual DRAT + LRAT (`14407`/`8678` core clauses, `3253`/`3016` RUP lemmas, `0` RAT) |
