# An 8425-vertex graph with maximum degree 14 and diameter 4

## What

Object SHA256 8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7 has N=8425, maximum degree 14 and diameter 4, exceeding the nonbold live general-graph (14,4) cell value 8303 at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html fetched on 2026-10-20T22:38:09.928483+00:00.

The exact object is `object/G_14_4_n8425.edges`. The equivalent explicit adjacency list is `object/adjacency.txt`. Neither optimality nor exhaustive search is claimed.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder with a C++17 compiler installed. Expected last line: `PASS`. The included checker performs every-root BFS; allow roughly one minute on a laptop (estimate, not a portable timing guarantee).

## Compared to

Live nonbold general-graph (14,4) entry: 8303, fetched 2026-10-20T22:38:09.928483+00:00, HTTP 200, page SHA256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`, https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html. Improvement: 122 vertices. The stronger live/pinned V3R1T4S trophy is 8424; improvement over it is one vertex. The independent novelty review examined 285 open PR descriptions and a bounded recent-literature search, with limitations in `panel/novelty.md`.

## Not claimed

No optimality (Moore bound 33321), no impossibility of larger constructions, no exhaustive literature or parameter search, no chance/statistical claim, and no result about another cell or future table state. The successful construction replay in a clean temporary copy is recorded in `how-we-built-it/replay_receipt.txt`; portability beyond the pinned local environment is not claimed.

## Credits

Francesc Comellas and table contributors: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html. Baseline: the 8424-vertex Bhakar-controller affine-frame lift, credited to its original authors in https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/biggest-graphs; original baseline SHA256 is recorded in `how-we-built-it/baseline.sha256`. This work adds one vertex with coverage selection, joint edge cuts and bounded annealing. V3R1T4S kit: https://github.com/elder-plinius/V3R1T4S. Independent skeptics' unedited verdicts are in `panel/`.
