# Preregistration — Lens 2 (`c-evaluator-optimizer`)

frozen_utc: 2026-10-14T06:39:55Z
lens: c-evaluator-optimizer
target_id: covering-designs-record
null_test: Corrupt or drop 1 block from any discovered covering or lottery design and verify `verify_covering.py` prints `FAIL` (`exit 1`).

## Plan
Build a multi-threaded C (`clang -O3 -pthread`) 64-bit bitmask dynamic constraint weighting + tabu/LNS optimizer (`covering_sa.c`).
- Represent every $k$-block and every $m$-subset of $\{0, \dots, v-1\}$ ($v \le 63$) as a 64-bit integer `uint64_t`.
- Precompute the list of all $S = \binom{v}{m}$ $m$-subsets `subs[0..S-1]` (or per-vertex inverted index `v_subs[x]` of all $m$-subsets containing vertex $x$).
- Maintain for each block $i \in \{0, \dots, b-1\}$ and each $m$-subset $s \in \{0, \dots, S-1\}$ the intersection count `inter[i][s] = __builtin_popcountll(block[i] & subs[s])` (or update incrementally when swapping point $u_{\text{out}} \to u_{\text{in}}$ in block $i$: only $m$-subsets containing $u_{\text{out}}$ or $u_{\text{in}}$ change their intersection size by $\pm 1$, and only when the intersection size crosses the threshold $t$ between $t-1$ and $t$ does `cov_count[s]` change!).
- Apply Dynamic Constraint Weighting (DCW): whenever a local minimum is reached with uncovered $m$-subsets (`cov_count[s] == 0`), increment `weight[s] += 1`, forcing the search out of the local basin.
