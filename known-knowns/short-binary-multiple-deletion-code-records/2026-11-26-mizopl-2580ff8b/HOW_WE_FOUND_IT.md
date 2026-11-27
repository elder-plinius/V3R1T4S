# How We Found It

> contributor text, unverified

All codebooks were discovered strictly from scratch on local CPU hardware (plus bounded diagnostic runs) without seeding from any published or leaderboard codebook:

1. **Symmetry-Quotient Orbit Search (`(16, 3) = 44`):** On the `(16, 3)` conflict graph, searching directly in symmetry-quotiented orbit spaces under Klein-4 `<c, r>`, `<rc>`, `<r>`, and `<c>` rapidly produced four non-isomorphic size-44 codes (distinct `|D_3|` invariants `2344, 2304, 2410, 2468`), reaching the Klein-4 `<c, r>` 44-word code in under 1 second.
2. **Dynamic `min d_free` + Hyper-ARW Search (`(15, 3) = 31`):** Combining exact dynamic minimum-free-degree (`min d_free`) refill with penalty-guided adaptive random walk produced the 31-word `(15, 3)` code from scratch.
3. **Run-Count Monotonicity + `<c>` Unfreeze (`(15, 2) = 137`):** Deleting `s` bits never increases a word's run count (`r(d) <= r(x)`), so unweighted conflict-degree heuristics systematically under-select high-run outer-shell words (`r >= 11`) while `<c>`-symmetric orbit seeds trap local search. Pairing run-aware dual-LP weights on a `<c>`-symmetric size-136 seed with an unrestricted unbiased unfreeze lifted `(15, 2)` from `136` to `137` in `29.17 s` on a single laptop (`44` words changed, `<c>`-paired words dropped from `136` to `74`).
4. **Pure-Kernel Lean 4.36.0 Certification:** All codebooks were exported to standalone zero-dependency Lean 4 modules verifying general `D_s <-> LCS` equivalence, pairwise validity, exhaustive `2^n` inclusion-maximality (`196,608` binary words total), Klein-4 invariance of `(16, 3) = 44`, and exact dual-LP optimality on `M_2(7) = 5` and `M_3(9) = 5`.
