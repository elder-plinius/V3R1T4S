# Lean 4 Formal Proof of Simultaneous PRM+ Last-Iterate Non-Convergence (`alternating-prm-plus-ergodic-convergence`, `p2`)

## What

In Lean 4 with only propext, Classical.choice and Quot.sound, the last iterate (x_t, y_t) of simultaneous Predictive RM+ (Algorithm 2) from R = 0 and uniform strategies on A = [[3,0,-3],[0,3,-4],[0,0,1]] has duality gap at least 1/20 for every t >= 13203, so its liminf is positive; this says nothing about alternating PRM+, averaged iterates, or RM+.

## Check it yourself

From this package folder (with a `YaelDillies/LeanAPAP` checkout providing `Lean v4.36.0-rc2` and Mathlib `2d833a68a3d6bad4dfdb7cbbcacaa978580247d2`):

```sh
LEANAPAP_ROOT=./LeanAPAP sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (verifies the 119-file manifest, audits forbidden tokens, cross-checks `Defs.lean` against 1,000 float64/Decimal iterations to width `4.372e-15`, cold-compiles all 119 Lean modules from source with `-Dwarn.sorry=true`, and audits `#check` and `#print axioms`).

## Compared to

- **Paper**: Cai, Farina, Grand-Clement, Kroer, Lee, Luo & Zheng, *Last-Iterate Convergence Properties of Regret-Matching Algorithms in Games*, ICLR 2025 (https://arxiv.org/abs/2311.00676)
- **Prior status**: Empirical `10^5`-iteration simulation only (Figure 1 of `arXiv:2311.00676v2`); analytically and formally unproved as of `arXiv:2611.02521v1` (Nov 2, 2026, Section 8)
- **Fetched**: `2026-11-16T22:02:00Z` (`HTTP 200`, SHA-256 `845807f5c254c06af6070056c2c5c21963b2f38e2182e6a085cabcba88b282fe`)

## Not claimed

- Partial win `p1` (last-iterate non-convergence of Alternating RM+, Algorithm 7 on `A`) is not claimed here.
- The main open question for Alternating PRM+ (Algorithm 8 universal `O(1/sqrt(T))` ergodic convergence vs counterexample) is not claimed.

## Credits

- **Yang Cai, Gabriele Farina, Julien Grand-Clement, Christian Kroer, Chung-Wei Lee, Haipeng Luo, and Weiqiang Zheng**, *Last-Iterate Convergence Properties of Regret-Matching Algorithms in Games*, ICLR 2025 (https://arxiv.org/abs/2311.00676), for introducing the `3x3` counterexample matrix `A` and Algorithms 1, 2, 7, and 8.
- **Hung P. Nguyen, Ioannis Anagnostides, Brian Hu Zhang, and Tuomas Sandholm**, *Predictive Regret Matching+ in Games* (https://arxiv.org/abs/2611.02521), for context on the analytical status of `3x3` PRM+ dynamics.
- **Lean 4, Mathlib4, and LeanAPAP Communities** (https://github.com/leanprover/lean4, https://github.com/leanprover-community/mathlib4, https://github.com/YaelDillies/LeanAPAP).
