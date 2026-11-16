# How We Found It

_Note: contributor text, unverified._

Auditing `FormalConjectures/WrittenOnTheWallII/` on live `main` (`e028240a6182`), we noticed `GraphConjecture25.conjecture25` was tagged `research solved` (disproved) with `sorry` and zero open PRs. Two subtleties had to be handled cleanly for Lean's kernel without `native_decide`:
1. With `autoImplicit = false`, `{α : Type*}` elaborates as a universe-polymorphic parameter `u_1` outside the negation `¬ ∀ {α : Type u_1} ...`, so a `Type 0` counterexample on `Fin 15` fails to unify; lifting the 15-vertex graph `C_5[K_3]` (the complement of the 3-blowup of `C_5`) to `ULift.{u} (Fin 15)` resolves all universe levels simultaneously.
2. Rather than computing shortest-path matrices with `native_decide`, we proved explicitly via midpoint witnesses `mid15` that every non-adjacent pair has distance `2`, turning `Even (G.dist u v)` into non-adjacency (`distEven = 7` everywhere, so `2 * ceil((1 + 7)/3) = 6`), while a structural-recursion triangle check on `Gᶜ` proved `α(G) <= 2` and hence `b(G) <= 4`.
