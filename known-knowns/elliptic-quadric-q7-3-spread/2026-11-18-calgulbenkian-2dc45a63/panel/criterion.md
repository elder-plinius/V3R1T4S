context: Claude Code subagent, fresh context [Sonnet 5.5]

# CRITERION report, elliptic-quadric-q7-3-spread, claimed partial win p1

## Literal reading of p1
p1: "no spread of Q^-(7,3) admits an automorphism of order 2 (or of order 3) ... The skeptic reruns the code."
- "Order 3 alone": the parenthetical "(or of order 3)" reads as an alternative, so a proof for order 3 meets p1. It is the weaker reading, and the package does not hide it. README.md "Not claimed" and how-we-built-it/PROOF.md say the order-2 case is NOT fully excluded: the fixed-point-free similarity involution class Inv_0_sim (Q(Hx)=2Q(x), H^2=2I) remains, giving |Aut(S)| in {1,2}. Anyone reading p1 as "order 2 and order 3" would not be satisfied. Order 2 is covered only inside PO^-(8,3).
- Right group: yes. Automorphisms are taken in the full collineation group of the polar space, PGO^-(8,3) (similarities mod scalars), not only isometries. Field automorphisms are trivial over GF(3). I recomputed |O^-(8,3)| = 2*3^12*(3^4+1)(3^2-1)(3^4-1)(3^6-1) = 40,607,874,478,080 = the stated |PGO^-(8,3)| (the multiplier-2 similarity doubles GO, the scalars +-I halve it back). The package also proves Aut(collinearity graph) = PGO^-(8,3) by frame-stabiliser backtracking (stabiliser 64, 1066*729*112*81*10*9*64 = the same number) and shows planes are exactly the 13-cliques, so there is no hidden bigger group.
- Every order-3 automorphism: yes in argument. (i) An order-3 element of PGO has a unique lift A with A^3=I, and the multiplier must be 1, so A is in O^-. (ii) Cayley map in characteristic 3 (X=-(D+D^2), D=A-I, D^3=0) gives a bijection with skew S with (G^-1 S)^3=0. The count 59,696+537,264+42,981,120+386,830,080 = 430,408,160 is derived by strata (rank 2 or 4 only, forced by 8 <= 3*dim ker), and the classes are 5 with sizes from BFS or centraliser enumeration summing to that total. I re-derived the rank bound and the sum by hand, and the strata arithmetic is consistent (386,830,080 = 2 * 193,415,040). Because the five fixed-point counts (94,121,13,4,22) are distinct and class sizes sum to the full count, no class is missing. (iii) Each class is shown unsatisfiable. C3_121 and C3_94 by dim ker(A-I)=6 (no disjoint plane 3-orbits; fixed planes all meet a 4-point line, at most 4 < 82). C3_22 and C3_4 by tiny exact cover. C3_13 is the only large one: fixed planes force the plane Pi_* into any spread, then normaliser transitivity on 6,561 plane 3-orbits plus staged pair elimination, 143 or 144 tasks, about 8.8M nodes, two engines, 0 solutions. I checked the dichotomy argument for C3_13 myself and it is correct.

## Runs (in a copy of this package, in my own work folder)
- sh verify-it-yourself/run_checks.sh: exit PASS, last line "PASS", 57 s wall (Engine 2 C3_13: 143 tasks, 8,776,899 branches, UNSAT). Matches verify-it-yourself/RECEIPTS.md.
- Engine 1, how-we-built-it/solve_ord3_staged_swar.c (4 threads, nice): "STAGED SWAR COMPLETE: sat=0, total_tasks=144, total_nodes=8796560, wall_time=15.4s", the same count as BUILD_COMMANDS.md. Note run_checks.sh runs only Engine 2; Engine 1 is a separate manual step and was run.
- No fetches made. All compute well under budget. I did not write a separate from-scratch checker (not the CRITERION role); the Python checker and Engine 2 share no code with the builder/solver files, per the package.

## Limits and hidden-quantifier hunt
- The nonexistence rests on the correctness of the code and on the pen-and-paper reductions (unique lift, Cayley bijection, class enumeration, normaliser WLOG). The two engines agree but share the same mathematical reductions (normaliser symmetry breaking), so they are not independent of that reasoning. Engine 2 does verify normaliser transitivity itself.
- Not a certificate-style proof (no DRAT/LRAT); it is rerunnable code, which p1 asks for.
- The extra claims (odd primes 5,7,13,41; involutions in PO^-) are outside p1 and were not fully audited; they do not affect the order-3 conclusion.
- Does not claim existence or nonexistence of a spread, and says so.

confirmed_scope: Rerunning the package (run_checks.sh PASS in 57 s, plus the SWAR engine with 0 solutions) confirms that no spread of Q^-(7,3) is invariant under any element of order 3 of the full collineation group PGO^-(8,3), covering all 430,408,160 such elements in 5 classes; order-2 automorphisms are excluded only inside PO^-(8,3), the similarity involutions (class Inv_0_sim) remain open.

pass: true
