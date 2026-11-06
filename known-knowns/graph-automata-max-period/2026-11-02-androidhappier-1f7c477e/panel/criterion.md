# Criterion skeptic verdict: A384209(10) = 46

context: subagent (executor, criterion)

Bank entry checked: graph-automata-max-period. Its success_criterion text is identical to the copy in claim/claim.md.
Work was done on a private copy of claim/. tools/geng sha256 = 75d1bf01...f450, which matches claim.md.

## Clause-by-clause (literal)

(a) Exhaustive enumeration of all graphs of the class and all 2^n states
- Class: A384209 ranges over all simple graphs, including disconnected ones. Life (B3/S23) is a single fixed rule, so the clause "all rules of the class" is trivially met.
- Program A (code/lifeA.c) reads `geng -q 10` (all graphs, no -c). For every graph it builds the full successor map on all 1024 states and finds every cycle by rho-walking each unvisited state.
  - I rebuilt it and reran it at n=10 split into 4 residue classes (nice 15). The total is 12005168 = A000088(10).
  - Max period = 46, attained by I?zUvYujw (state 62) and IEhffT{^w (state 842).
  - The full histogram of graphs by max period matches result/A_n10_merged.txt exactly (46 occurs for 2 graphs, 44 for 1).
- Program B (code/lifeB.c) works on connected graphs only (`geng -cq`).
  - I reran it at n=10 in 4 parts. There are 11716571 connected graphs = A001349(10), and the period set {1..35,38,39,44,46} matches result/B_order10.txt.
  - The per-length witness graphs differ only because "first seen" depends on the split, which is expected.
  - Orders 1..9 were byte-identical to result/B_order1..9.txt.
- Is B's connected-plus-lcm route valid? Yes.
  - Life on a disjoint union evolves componentwise, so the state space is the product of the component state spaces. A product state is periodic only if every component state is periodic. The cycle length is then the lcm of the component cycle lengths, and every combination of component cycles can be realized, because components may be any connected graphs of the given orders.
  - code/combine.py's reach(n, maxpart) recursion lists all partitions of n into non-increasing parts. It takes the lcm over every choice of p_i in P(k_i), where P(k) is the union of cycle lengths over all connected order-k graphs. It therefore covers every partition and every graph.
  - My rerun of combine.py on my regenerated B outputs is identical to result/combine_n1_10.txt: n=10, a(n)=46.
  - At n=10 no lcm of a proper partition beats 46. The best is 27 (from 9+1).
- Verdict (a): met.

(b) Two independent implementations that agree and reproduce every listed term
- I read both sources. They share no code. Each has its own graph6 decoder.
  - A: per-vertex popcount, rho/stamp cycle detection, all graphs directly.
  - B: bit-sliced 4-bit neighbour counter, Kahn in-degree peeling of transient states, connected graphs plus an lcm combination step.
- The only shared dependency is the geng binary, which the criterion mandates. The graph counts guard it (A000088 and A001349 at every n).
- Both reproduce a(1..9) = 1,1,1,1,2,4,8,14,27; I reran both for n = 1..9. A also reproduces the OEIS optimal graphs D]{, E]yw, FE~vw, GEnvZ{, HCZJtzm.
- Both give 46 at n=10.
- Caveat: both were written by the same author. They are algorithmically and structurally distinct, so I accept them as independent.
- Verdict (b): met.

(c) Witness
- Witness: graph6 I?zUvYujw (10 vertices, 27 edges), rule = Life B3/S23, start state 62 (bit v = vertex v).
- code/stepper.py gives preperiod 0 and cycle_length 46.
- My own simulator checks this independently. It uses a graph6 decoder I wrote from the spec, set-based Life and Brent cycle detection, so the period it reports is the minimal one.
  - I?zUvYujw from 62 and from 31: period 46. IEhffT{^w from 842 and from 47: period 46.
  - Max over all 1024 states is 46 for both graphs.
- My decoder is validated: it reproduces the published maxima 2, 4, 8, 14, 27 on the OEIS optimal graphs.
- Verdict (c): met.

(d) Not already in the live OEIS entry
- I made one plain GET of https://oeis.org/search?q=id:A384209&fmt=text (User-Agent V3R1T4S-research-agent) at 2026-11-02 04:30:53 EST. It returned HTTP 200.
- %S is 1,1,1,1,2,4,8,14,27 and the revision is #8 (May 22 2025), keyword nonn,more.
- All %-lines are identical to data/A384209.txt. There is no a(10).
- data/A384209_draft.html records "No pending changes". I did not refetch the draft page.
- Verdict (d): met.

(e) Hidden quantifiers and definitions
- "Period" is taken as the length of the eventual cycle, maximized over all start states and all graphs. Under this reading both programs reproduce every published term (n = 1..9), and they reproduce the OEIS optimal graphs for n = 5..9. The definition is not stretched.
- No restriction to connected graphs was smuggled in: Program A covers disconnected graphs directly, and Program B covers them by the lcm argument.
- The null model of lcm combinations of small components (relevant only for the disconnected class) was checked, and it gives at most 27 at n=10.
- Partial win or full win: the claim is a new exact term of A384209, which is exactly the full success criterion ("A new exact term of any of the four sequences"). It is also p1, but it is not merely a partial. It is not p2: there is no a(11).

## Outcome
Full win (the full success criterion is met for A384209(10). It is not p2.)

confirmed_scope: Exhaustive enumeration of all 12005168 simple graphs on 10 vertices and all 1024 states, by two independent programs that both reproduce a(1..9), shows that A384209(10) = 46 (a term absent from the live OEIS entry on 2026-11-02), with witness graph6 I?zUvYujw, Life rule B3/S23, start state 62, whose directly simulated cycle length is 46.

pass: true
