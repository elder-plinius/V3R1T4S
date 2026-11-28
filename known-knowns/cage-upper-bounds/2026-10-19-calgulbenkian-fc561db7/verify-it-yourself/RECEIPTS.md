# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 2.8 seconds.

```
sha256 matches INDEX.csv (fc561db7e3e7b50619bb4b6e8673994ad0192d582bab9c29a40ba7b2769cd00b)
== check_mixed.py: regularity, rebuild from generators, girth under both cycle conventions
{"file": "mixed_z2_r7_g6_N184.json", "N": 184, "z": 2, "r": 7, "g": 6, "n_edges": 644, "n_arcs": 368, "order_is_2M": true, "stored_lists_equal_graph_rebuilt_from_generators": true, "no_loops": true, "no_repeated_link_between_a_vertex_pair": true, "regular_z_in_z_out_r_edges": true, "shortest_cycle_up_to_5_forward_arc_convention": null, "girth_at_least_6_forward_arc_convention": true, "girth_direction_blind_convention": 4, "VALID_under_forward_arc_convention": true}
checker verdict: PASS (valid under the forward-arc convention=True, N=184, table upper bound 196; direction-blind girth=4)
== negative control: one arc head changed must NOT be valid
negative control rejected as expected
ALL CHECKS PASS
```
