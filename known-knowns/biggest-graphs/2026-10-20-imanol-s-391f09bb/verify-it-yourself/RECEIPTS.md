# Receipts

Real output, run from the package folder on 2026-10-20.

```
$ time sh verify-it-yourself/run_checks.sh
VALID n=6631 maxdeg=13 diameter=4 edges=43099
PASS
sh verify-it-yourself/run_checks.sh  17.88s user 0.14s system 99% cpu 18.168 total
```

The checker rebuilds the adjacency from `object/G_13_4_n6631.edges` only: it rejects loops,
multi-edges, out-of-range labels, an isolated vertex, a maximum degree above 13, a disconnected
graph (every one of the 6 631 sources must reach all vertices), and a diameter above 4.

Object sha256: `391f09bb6f72f16ca5b867694b96d1d1ca31569c8974ba0f0ef00099c6cd5cbe`.
