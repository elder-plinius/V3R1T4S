# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 27.5 seconds.

```
sha256 matches INDEX.csv (2c7b60282a1cf2cb4de947f8aa0554577cc57874f1d7c547ce6f1a90e05d8fb6)
== check_mixed.py: regularity, rebuild from generators, girth under both cycle conventions
{"file": "mixed_z2_r11_g6_N450.json", "N": 450, "z": 2, "r": 11, "g": 6, "n_edges": 2475, "n_arcs": 900, "order_is_2M": true, "stored_lists_equal_graph_rebuilt_from_generators": true, "no_loops": true, "no_repeated_link_between_a_vertex_pair": true, "regular_z_in_z_out_r_edges": true, "shortest_cycle_up_to_5_forward_arc_convention": null, "girth_at_least_6_forward_arc_convention": true, "girth_direction_blind_convention": 4, "VALID_under_forward_arc_convention": true}
checker verdict: PASS (valid under the forward-arc convention=True, N=450, table upper bound 480; direction-blind girth=4)
== negative control: one arc head changed must NOT be valid
negative control rejected as expected
ALL CHECKS PASS
```
