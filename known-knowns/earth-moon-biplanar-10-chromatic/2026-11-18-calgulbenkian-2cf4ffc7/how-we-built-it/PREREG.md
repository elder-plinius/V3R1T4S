# Preregistration: earth-moon-biplanar-10-chromatic

preregistered_utc: 2026-11-18T09:25:57Z
target_id: earth-moon-biplanar-10-chromatic
null_test: not needed because all claims are deterministic finite mathematical objects (simple biplanar graphs with explicit two-layer planar decompositions, combinatorial rotation systems, exact rational LP primal/dual certificates, and SAT/DRAT proof certificates of chromatic number and edge-criticality) rather than statistical signals.

## 1. Frozen Literature Baselines (from `scout.md` before any solver execution)

1. **Chromatic number (`full`):** Best published lower bound is `chi = 9` (Sulanke 1974/1980, `K_6 + C_5`), confirmed open on `27b.html` and `epoch.ai` at `2026-11-18T09:10:09Z`. By Doria/Patil (Aug 2026) and Szeider (Sep 2026, arXiv:2609.28102), any biplanar graph with `chi >= 10` must satisfy `n >= 17` and `alpha(G) >= 3`.
2. **Fractional chromatic number (`p1`):** Although `targets.json` notes `8.5` for `K_6 + C_5` and requires strictly beating any value found in a literature search on fractional colourings of thickness-two graphs, our live scout found Spogreev (Oct 6, 2026, Zenodo `10.5281/zenodo.23113159`, Theorem B), which proves that `K_5 + C_8^2` (`13` vertices, `66` edges) is biplanar and achieves **`chi_f = 9`**. Therefore, **we freeze the threshold for `p1` at `chi_f(G) > 9` (strictly greater than `9`, certified in exact rational arithmetic)**. Note that since `chi(G) >= ceil(chi_f(G))`, any biplanar graph achieving `chi_f(G) > 9` also satisfies `chi(G) >= 10`.
3. **9-critical biplanar graphs (`p2`):** Published and archived 9-critical biplanar graphs consist of:
   - Sulanke (1980): `K_6 + C_5` (`n = 11`).
   - Boutin, Gethner, and Sulanke Part I (2008, J. Graph Theory 57:198–214): `40` nine-critical biplanar graphs on `n = 12..16` (`data/volkopat_pool/17_bgs*.edges`).
   - Gethner and Sulanke Part II (2009, Graphs Combin. 25:197–217) & Alalqam (2012): nine-critical biplanar graphs on `n <= 17` (including `n = 17, alpha = 2`) plus Hajós sums (`n >= 21`).
   - Patil (Aug 2026, Zenodo `10.5281/zenodo.22103613` & `Volkopat/earth-moon-biplanar`): `8` edge-swap 9-criticals on `n = 13..16` and Hajós sums on `n = 21..31` (`data/volkopat_pool/`).
   - Spogreev (Oct 2026, Zenodo `10.5281/zenodo.23113159`): `K_5 + C_8^2` (`n = 13`) and boundary joins (`K_4 + C_10(1,4,5)` on `n = 14`, `K_1 + C_16(1,2,6,7,8)` on `n = 17`).

## 2. Frozen Success Criteria

### A. Full Win (`solution_claim`)
An explicit simple graph `G = (V, E)` with edge partition `E = E_1 union E_2` (`E_1` and `E_2` disjoint) such that:
1. `(V, E_1)` and `(V, E_2)` are simple and certified planar by **two independent planarity algorithms** (Boyer–Myrvold via `networkx.check_planarity` AND an independent Kuratowski-free / Hopcroft–Tarjan / Fáry straight-line or combinatorial sphere-surface verifier written from scratch in Python stdlib), with explicit combinatorial rotation systems saved and verified via Euler's formula `V - E + F = 2 * C` and face-walk manifold checks.
2. `G` is not 9-colorable, proven by SAT UNSAT on the regenerated standard 9-coloring CNF with a DRAT/LRAT certificate verified by an independent DRAT/LRAT checker (`verify_drat` / `drat-trim`).

### B. Partial Win `p1` (`partial_win_claim`)
An explicit simple biplanar graph `G = (V, E_1 union E_2)` certified planar as in (A.1), together with an exact rational primal fractional coloring (`x_I >= 0` on verified independent sets `I` with `sum_(I ni v) x_I >= 1`) and an exact rational dual weight vector (`y_v >= 0` verified to satisfy `sum_(v in I) y_v <= 1` on **every** independent set `I` of `G` enumerated by two independent algorithms), establishing `chi_f(G) = sum_I x_I = sum_v y_v > 9`.

### C. Partial Win `p2` (`partial_win_claim`)
An explicit simple 9-critical biplanar graph `G = (V, E_1 union E_2)` on `n` vertices such that:
1. **Biplanarity:** `(V, E_1)` and `(V, E_2)` partition `E` and are certified planar by two independent planarity checkers plus explicit combinatorial rotation systems checked by Euler's formula.
2. **Exact 9-Chromaticity:** Explicit verified proper 9-coloring of `G`, AND SAT UNSAT on the regenerated standard 8-coloring CNF accompanied by a verified DRAT proof certificate checked by an independent standalone DRAT verifier.
3. **Exact Criticality:** No isolated vertices, AND for **every** edge `e in E`, an explicit proper 8-coloring of `G - e` saved in the certificate and verified edge-by-edge (proving `chi(G - e) <= 8` for all `e in E` and hence `chi(G - v) <= 8` for all `v in V`).
4. **Strict Novelty & Non-Triviality (`NOVELTY` compliance):**
   - Verified non-isomorphic (by canonical partition-refinement labelling + VF2 exact isomorphism check) to `K_6 + C_5`, all 40 Boutin–Gethner–Sulanke (2008) graphs, all graphs in Patil's 246-file corpus (`Volkopat/earth-moon-biplanar`), and Spogreev's joins.
   - To guarantee non-isomorphism with unarchived drawings in Gethner–Sulanke (2009) and Alalqam (2012) (all of whose non-Hajós examples have `n <= 17`) AND guarantee it cannot arise from any Hajós sum or Ore composition of smaller 9-critical biplanar graphs (since every 9-critical non-`K_9` graph has `n >= 11`, so any Hajós sum has `n >= 21` and any Ore composition has `n >= 20`), **we specifically require `n in {18, 19}`**, **connected complement `overline(G)` (not a join `A + B`)**, **vertex connectivity `kappa(G) >= 3` with no clique cutset**, and **not a subgraph of any graph in Patil's or Spogreev's corpora**.
