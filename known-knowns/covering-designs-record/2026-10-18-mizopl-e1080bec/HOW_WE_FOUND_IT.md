# How we found it (contributor text, unverified)

*This is a plain narrative by the contributor (contributor text, unverified); the binding evidence is in `object/`, `verify-it-yourself/`, `panel/`, and `the-record-we-beat/`.*

## Brief and Scouting
Scanning the La Jolla Covering Repository (LJCR) and Covering Repository (CR) tables against generalized two-part combining constructions (splitting the $v$-set into $V_1$ of size $v_1$ and $V_2$ of size $v_2 = v - v_1$ and choosing the optimal block-size split $(k_1, k - k_1)$ independently for each $j = |T \cap V_1| \in \{0,\dots,t\}$) revealed several cells where the published DP table value was strictly larger than what could be built from smaller LJCR ingredient designs already on disk.

For `C(94,13,5)`, splitting $94 = 47 + 47$ and combining the on-disk LJCR ingredient designs for $v = 47$ produced an explicit covering design with `125,236` blocks — already `3,967` blocks below the live Covering Repository record (`129,203`) and `4,101` blocks below the LJCR record (`129,337`).

## What Failed and What Worked
- **What failed:**
  - Re-optimizing the split with padded smaller-$k$ or point-deleted larger-$v$ ingredients (`how-we-built-it/splitopt.py`) did not improve on the `125,236`-block combining bound for `(94,13,5)`.
  - Single-block greedy redundant-block removal (`how-we-built-it/prune.c`) removed `0` blocks from the `125,236`-block `(94,13,5)` design because the combining terms for `(94,13,5)` were already 1-minimal.
- **What worked:**
  - **Pair-merge local search (`how-we-built-it/merge.c`):** Even when no single block is redundant, two blocks $B_a, B_b$ can sometimes be replaced by a single $k$-block if the union of all $t$-subsets that are *uniquely* covered by $B_a$ or $B_b$ spans at most $k = 13$ points. Running `merge.c` found `52` such disjoint merges on `(94,13,5)`, reducing the design from `125,236` to `125,184` blocks (`4,019` blocks below CR).
  - Both the frozen C bit-array checker and independent Python checkers confirmed `0` uncovered 5-subsets across all $\binom{94}{5} = 54,891,018$ 5-subsets, and the 3-skeptic panel (`reproduce`, `novelty`, `criterion`) independently verified coverage, 1-minimality (`0` redundant blocks), and novelty.
