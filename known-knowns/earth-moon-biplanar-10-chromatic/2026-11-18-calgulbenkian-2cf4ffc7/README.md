# 19-Vertex 5-Connected 9-Critical Biplanar Graph (`earth-moon-biplanar-10-chromatic`, `p2`)

## What

An explicit simple 19-vertex, 92-edge graph (object/biplanar_9crit_n19_e92.json) is edge-critical 9-chromatic (confirmed independently for chi <= 9 and for all 92 edge-deleted 8-colourings; chi >= 9 via the package's own DRAT check, run_checks.sh printing PASS), splits into two layers (45 and 47 edges) whose rotation systems each give V-E+F = 2 on a single component, and has an order and a canonical hash different from every one of the 42 reconstructed Sulanke and BGS-pool graphs; the extras 5-connected, non-join and (by my own check) clique-cutset-free also hold, but the BGS list is reconstructed rather than taken from the paper, and these extras are not part of p2.

## Check It Yourself

From this folder, run one command using only the Python 3 standard library:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (takes ~8 seconds on a laptop CPU using pure Python stdlib; also runs `networkx.check_planarity` if `networkx` is installed).

## Compared To

- **Status table:** Tao's Optimization Problems Constant 27b (`https://teorth.github.io/optimizationproblems/constants/27b.html`, fetched `2026-11-18T09:10:09Z`, HTTP `200`, SHA256 `c62b3145e7db5cfc8e3bf9531a029cac3b4ed7f9b30bbf6885a943005ff275ea`) and Epoch AI FrontierMath (`https://epoch.ai/frontiermath/open-problems/earth-moon`, fetched `2026-11-18T09:10:10Z`, HTTP `200`, SHA256 `92a7c769d608ad9b8136b71783e17bb1f44edf2aa0bd7ee536723420d3e51ba2`), both listing `9 <= chi_2 <= 12`.
- **Published 9-critical biplanar lists (`p2`):**
  - Sulanke (1974 / Gardner 1980): `K_6 + C_5` (`n = 11, e = 50`).
  - Boutin, Gethner, and Sulanke (*J. Graph Theory* 57(3):198–214, 2008): `40` nine-critical biplanar graphs, all of order `n in {12, 13, 14, 15, 16}` (canonical partition-refinement SHA256 fingerprints verified distinct in `the-record-we-beat/bgs_published_canonical_hashes.json`).
  - Gethner and Sulanke (*Graphs Combin.* 25(2):197–217, 2009) and Alalqam (2012): non-Hajós nine-critical biplanar graphs on `n <= 17` (`n = 17` with `alpha = 2`) plus Hajós sums (`n >= 21`).
  - Patil (Zenodo `10.5281/zenodo.22103613`, Aug 2026): `8` edge-swap nine-critical biplanar graphs on `n = 13..16` and Hajós sums on `n = 21..31` (screened against all 164 whole graphs in that repository for both isomorphism and subgraph containment: `0` matches).
- **Why this graph cannot arise from trivial propagation rules:** A Hajós sum or an Ore composition of two graphs has a vertex cut of size at most `2`, and our graph has vertex connectivity `kappa = 5`, so it is neither. (A count of vertices alone would not settle this: a Hajós sum of `K_9` with an 11-vertex graph has `9 + 11 - 1 = 19` vertices, although Boutin, Gethner and Sulanke show such sums with `K_9` are not biplanar.) Our graph has `n = 19` vertices, connected complement (`not a join`), vertex connectivity `kappa = 5`, minimum degree `8`, maximum degree `12`, `alpha = 3`, and zero clique cutsets.

## Not Claimed

- We do **not** claim a 10-chromatic biplanar graph (`full` solution remains open at `9 <= chi_2 <= 12`).
- We do **not** claim partial win `p1`: our live literature scout found that Spogreev (Zenodo `10.5281/zenodo.23113159`, Oct 6, 2026, Theorem B) already proved `K_5 + C_8^2` (`13` vertices, `66` edges) is biplanar with `chi_f = 9`, so beating all literature on `chi_f` of thickness-two graphs requires `chi_f > 9` (which would imply `chi >= 10`). Our 19-vertex 9-critical graph has `chi_f = 25/3`.

## Credits

- Gerhard Ringel (1959) and Brad Jackson & Gerhard Ringel (2000) for posing and studying the Earth–Moon problem (`https://en.wikipedia.org/wiki/Earth%E2%80%93Moon_problem`).
- Thom Sulanke (1974) and Martin Gardner (*Scientific American* 242(2):14–23, 1980) for `K_6 + C_5`.
- Debra L. Boutin, Ellen Gethner, and Thom Sulanke (*J. Graph Theory* 57(3):198–214, 2008, `https://doi.org/10.1002/jgt.20282`; *Graphs Combin.* 25(2):197–217, 2009, `https://doi.org/10.1007/s00373-008-0833-5`) for the foundational catalogues of 9-critical thickness-two graphs.
- Stefan Szeider (`https://arxiv.org/abs/2609.28102`), Digvijay Patil (`https://doi.org/10.5281/zenodo.22103613`), and Ivan Spogreev (`https://doi.org/10.5281/zenodo.23113159`) for 2026 structural exclusions and corpus reconstructions.
- Terence Tao (`https://teorth.github.io/optimizationproblems/constants/27b.html`) and Epoch AI (`https://epoch.ai/frontiermath/open-problems/earth-moon`) for maintaining the open-problem tracking pages.
