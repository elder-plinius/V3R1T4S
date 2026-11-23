# Run It Yourself

## 1. Verify the Claimed Object (Zero External Dependencies)

From a fresh shell in this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/7] Simple graph & partition verified: n=19, |E1|=45, |E2|=47, |E|=92, deg in [8..12]
[2/7] Biplanarity verified by independent topological + geometric verifiers ...
[3/7] Proper 9-coloring verified (chi <= 9)
[4/7] 8-coloring UNSAT DRAT proof verified on regenerated CNF (763 clauses, 11963 proof lines -> VERIFIED EMPTY CLAUSE; chi == 9)
[5/7] Exact 9-criticality verified: all 92 edge-deleted subgraphs G - e have valid proper 8-colorings
[6/7] Structural indecomposability verified: complement connected (non-join), vertex connectivity kappa=5, n=19 < 21 (cannot be a Hajos sum)
[7/7] Canonical SHA256 verified (efe251d54fa0a540...), non-isomorphic to all 42 Sulanke + Boutin-Gethner-Sulanke published graphs
PASS
```

## 2. Rebuild from Source

See `how-we-built-it/README.md` for compiling `how-we-built-it/wagner_n18_20.c` (`cc -O3`) and peeling the resulting 19-vertex triangulation union with `how-we-built-it/peel_to_9critical.py`.
