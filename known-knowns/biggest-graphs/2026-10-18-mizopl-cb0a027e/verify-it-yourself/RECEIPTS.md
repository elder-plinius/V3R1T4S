# Verification receipts

Command run from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
sha256 matches INDEX.csv (cb0a027e53b8282181df4754acb15797d7f954ed518967af6ecda9193a2a85c0)
== check_dd.py on object/G_14_3_N1118.edges
N=1118 edges=7809 degree histogram=[(13, 34), (14, 1084)] max degree=14 exact diameter=3 (BFS from all 1118 vertices) Moore bound=2563
PASS (Delta,D)=(14,3) N=1118 max_degree=14 diameter=3
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL an isolated vertex (or a gap in the vertex numbering))
ALL CHECKS PASS
```
