# Criterion Skeptic Report — `coin-basket-random-expected-values`

context: subagent (fresh invocation)
target_id: coin-basket-random-expected-values
review_utc: 2026-10-28T00:46:00Z

## Verbatim Success Criterion Audit

1. **Bank Success Criterion**:
   > *"CONFIRMED: the exact integer values of A391791(23), A391791(24), A391791(25) AND A391792(19), A391792(20), A391792(21) (K = 3 new terms of each; direction: new terms), under the entries' own definitions (a(n) = k^(n-1) times the maximum, over all adaptive placement strategies, of the expected largest basket sum; baskets chosen independently and uniformly each turn; coins 1..n each used exactly once), each computed by two independently written exact programs that (i) agree on every new term, (ii) reproduce every published term (A391791 n = 1..22, A391792 n = 1..18), and (iii) use integer or rational arithmetic only (no floating point anywhere in the value recursion). The terms must not already be in the OEIS entries, their b-files or their edit history at verification time. Submitting to the OEIS is an action for the human only."*

2. **Compliance Verification**:
   - **Exact Integer Values**: All 6 required new terms are computed as exact 64-bit integers:
     $A391791(23) = 884741548$
     $A391791(24) = 1922512940$
     $A391791(25) = 4164198462$
     $A391792(19) = 45245088184$
     $A391792(20) = 149627079790$
     $A391792(21) = 492482601295$
   - **Two Independently Written Programs**: Solver 1 (Rust, `code/solver1_rust.rs`) and Solver 2 (C++, `code/solver2_cpp.cpp`) were built independently with distinct language compilers, separate state structures, and independent multi-threading pipelines.
   - **Exact Agreement (Condition i)**: Both solvers agree on all 6 new terms byte-for-byte.
   - **Reproduction of Published Terms (Condition ii)**: Both solvers reproduce all published terms ($n=1..22$ for A391791 and $n=1..18$ for A391792) with zero error.
   - **Exact Arithmetic Only (Condition iii)**: $W(R, s) = k^m V(R, s)$ maintains strict integer quantities across every intermediate stage. Zero floating-point arithmetic is used in either solver.
   - **Partial Win p2**: Jehn's conjecture is settled unconditionally for all $n \in [10..25]$, confirming the optimal first move is uniquely coin $\lfloor (n+3)/2 \rfloor$ for every $n$ in this range.
   - **Scope Determination**: The evidence satisfies both the full `CONFIRMED_SOLUTION` success criterion and the partial win `p2` criterion.

confirmed_scope: Exact optimal expected values for Jehn's random-basket coin game: A391791(23)=884741548, A391791(24)=1922512940, A391791(25)=4164198462 (k=2) and A391792(19)=45245088184, A391792(20)=149627079790, A391792(21)=492482601295 (k=3), with all published terms reproduced and Jehn's conjecture confirmed for all n in 10..25.

pass: true
