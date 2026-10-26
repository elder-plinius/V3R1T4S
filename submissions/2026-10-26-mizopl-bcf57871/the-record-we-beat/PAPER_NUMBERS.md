# Exact Literature Numbers vs. Machine-Certified Quantities (`conway-99-graph`)

| Reference | Theorem / Proposition | Prior Status | Present Certificate (`object/certificate.json`) |
|---|---|---|---|
| `arXiv:2608.11211v2` §2.3 | Forced $1$-regular matching on $\Gamma_1(x)$ ($k=14$) | Prose proof | `p2_1_inner_matching_k14`: Dual Pure-RUP LRAT (`4`/`4` core clauses, `1`/`1` RUP lemma, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 | Bijection $\Gamma_2(x) \leftrightarrow 84$ non-matched pairs | Prose proof | `p2_2_outer_bijection_k14`: Dual Pure-RUP LRAT (`13`/`12` core clauses, `3`/`3` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 (Constraint 4) | Inner-outer coordinate balance $\mathbf{1}_{m(a)\in P_u} + \deg_{N(a)}(u) = 2$ | Prose proof | `p2_3_inner_outer_balance_k14`: Dual Pure-RUP LRAT (`2487`/`2483` core clauses, `836`/`780` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 (Constraints 2–3) | Outer pair common-neighbor equation $E(u,v) + \mathrm{cn}_{\Gamma_2}(u,v) = 2 - s$ | Prose proof | `p2_4_outer_pair_cn_k14`: Dual Pure-RUP LRAT (`345`/`342` core clauses, `142`/`111` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.3 | Validation on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ | CP-SAT run | `p2_5_srg9_uniqueness`: Positive SAT control + Dual Pure-RUP LRAT uniqueness (`13`/`7` core clauses, `1`/`1` RUP lemma) |
| `arXiv:2308.02978` (Cesarz & Woldar 2023) & `arXiv:2608.11211v2` §2.4 | Standalone prime order $p=7$ ($1$ fixed vertex, $14 \times 7$-cycles) | **OPEN** (timed out at $> 48\text{h}$ on 14 cores in `arXiv:2608.11211`) | `p7_fix1`: **RESOLVED UNSAT** via Dual Pure-RUP LRAT (`36342`/`17392` core clauses, `10590`/`5209` RUP lemmas, `0` RAT) |
| `arXiv:2608.11211v2` §2.4 | Prime order $p=5$ fixing $9$ vertices ($18 \times 5$-cycles) | CP-SAT run (no DRAT/LRAT) | `p5_t1_fix9`: Dual Pure-RUP LRAT (`31141`/`21073` core clauses, `2461`/`2050` RUP lemmas, `0` RAT) |
| `arXiv:2308.02978` & `arXiv:2608.11211v2` | Prime order $p=3$ fixing $33$ vertices ($22 \times 3$-cycles) | Custom/CP-SAT search (no DRAT/LRAT) | `p3_t1_fix33`: Dual Pure-RUP LRAT (`166`/`251` core clauses, `23`/`35` RUP lemmas, `0` RAT) |
| `arXiv:2308.02978` (Cesarz & Woldar 2023) | Frobenius subgroup $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ ($p=7,3$) | Manual/GAP casework (no DRAT/LRAT) | `frob21_z7_z3`: Dual Pure-RUP LRAT (`13758`/`8104` core clauses, `3253`/`3016` RUP lemmas, `0` RAT) |
| `arXiv:2308.02978` & `arXiv:2608.11211v2` | Prime order $p=2$ involutions across 14 profiles (`(0,1,6)` .. `(2,1,2)`) | Partial searches (no DRAT/LRAT) | `p2_a0_b1_c6_fix73` .. `p2_a2_b1_c2_fix13`: 28 Dual Pure-RUP LRAT proofs (`0` RAT) |
