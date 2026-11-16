# How We Built It

1. Audited live `google-deepmind/formal-conjectures` `main` (`e028240a61822d970c933f4656f51da025cf200b`) and open PRs across `FormalConjectures/WrittenOnTheWallII/`, selecting `WrittenOnTheWallII.GraphConjecture25.conjecture25`.
2. Verified the 15-vertex complement of the 3-blowup of `C_5` (`g15`, isomorphic to `C_5[K_3]`) in Python (`how-we-built-it/`), confirming connectedness, diameter 2, `distEven = 7` at every vertex, independence number `2`, and largest induced bipartite order `b(g15) = 4 < 6`.
3. Lifted `g15` to `ULift.{u} (Fin 15)` in `object/Solution.lean` to match the full universe polymorphism of upstream `conjecture25.{u_1}` and proved all graph-distance and induced-bipartite bounds in Lean 4 (`leanprover/lean4:v4.33.1`) without `native_decide`.
