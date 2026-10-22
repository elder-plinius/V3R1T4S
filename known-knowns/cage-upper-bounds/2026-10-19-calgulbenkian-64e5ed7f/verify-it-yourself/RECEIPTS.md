# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 4.5 seconds.

```
sha256 matches INDEX.csv (64e5ed7fd2e7c94e5ac9c7273d7e2abaefaa4d63d4c7816e1ec26a1058b599d4)
== check_mixed.py: regularity, rebuild from generators, girth under both cycle conventions
{"file": "mixed_z2_r8_g6_N234.json", "N": 234, "z": 2, "r": 8, "g": 6, "n_edges": 936, "n_arcs": 468, "order_is_2M": true, "stored_lists_equal_graph_rebuilt_from_generators": true, "no_loops": true, "no_repeated_link_between_a_vertex_pair": true, "regular_z_in_z_out_r_edges": true, "shortest_cycle_up_to_5_forward_arc_convention": null, "girth_at_least_6_forward_arc_convention": true, "girth_direction_blind_convention": 4, "VALID_under_forward_arc_convention": true}
checker verdict: PASS (valid under the forward-arc convention=True, N=234, table upper bound 252; direction-blind girth=4)
== negative control: one arc head changed must NOT be valid
negative control rejected as expected
ALL CHECKS PASS
```
