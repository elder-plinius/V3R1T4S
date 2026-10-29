# Gate Decision: `conway-99-graph` (Track `p2`)

status: CONFIRMED_PARTIAL
target_id: conway-99-graph
track: p2 (Forced-structure reduction re-derivation in two independent SAT encodings with machine-checked Pure-RUP LRAT certificates)
panel_date_utc: 2026-10-26T04:17:19Z
reproduce_skeptic: pass: true
novelty_skeptic: pass: true
criterion_skeptic: pass: true
confirmed_scope: Track p2 on conway-99-graph (srg(99, 14, 1, 2)): Dual-encoded pure-RUP LRAT (0 RAT lemmas) UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) re-deriving all 5 forced-structure reduction propositions (p2_1_inner_matching_k14, p2_2_outer_bijection_k14, p2_3_inner_outer_balance_k14, p2_4_outer_pair_cn_k14, and p2_5_srg9_uniqueness) of Thakkar & Severini (arXiv:2608.11211), together with a positive SAT non-vacuity check on srg(9, 4, 1, 2) = K_3 box K_3 in both encodings (10 LRAT certificates, 38 RUP steps, 0 RAT lemmas, verified alongside the full 27-theorem / 54-certificate suite by verify-it-yourself/verify.py).
