# PREREG (frozen 2026-11-02T09:22:22Z per date -u, before any attack program has been written or run)

Target: graph-automata-max-period. Cell: A384209(10).

Criterion (bank, verbatim): A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term. It must come from exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required), all rules of the class and all 2^n states. Two independent implementations must agree and reproduce every listed term. The result must include a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation. The term must not already be in the live OEIS entry at claim time.

Definition used: period of a start state = length of the cycle its Life orbit eventually enters (the functional graph
on 2^n states is finite and deterministic). a(n) = max over all simple graphs on n labelled-up-to-isomorphism vertices
(geng n, connected or not) and all 2^n start states.

Statistic / checkers:
- Program A: C program reading every graph from "geng n" (all graphs), building the full successor map on 2^n
  states, and taking the longest cycle in that functional graph. Must reproduce A384209(1..9) exactly and report
  graph counts equal to A000088(1..10) (1,2,4,11,34,156,1044,12346,274668,12005168).
- Program B: independently written, different route: reads only CONNECTED graphs ("geng -c k", k = 1..10, counts
  must equal A001349), records the full SET of cycle lengths each connected order admits, then gets a(n) as the max
  over integer partitions of n and over choices of one achievable period per part of the lcm (components of a
  disjoint union evolve independently, so a product cycle has length lcm). Different successor construction
  (bit-sliced neighbour counting) and different cycle finder. Must reproduce A384209(1..9).
- Witness: graph6 string + start state; an independent small Python stepper simulates it and confirms the minimal
  cycle length equals the claimed value.
- Claim only if A(10) == B(10), both reproduce A384209(1..9), graph counts match A000088/A001349, the witness
  simulates to the value, and the OEIS DATA re-fetched right before claiming still lacks a(10). Otherwise no claim.
Thresholds: exact integer equality; no tolerance.

null_test: not needed because the claim is an exact integer from deterministic exhaustive enumeration checked against published terms and a simulated witness, not a search score or a "beats chance" statistic.
