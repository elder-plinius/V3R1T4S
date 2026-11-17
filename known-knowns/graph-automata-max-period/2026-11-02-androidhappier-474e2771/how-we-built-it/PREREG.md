# PREREG (frozen 2026-11-02T09:59:47Z per date -u, before any program for this cell has been written or run)

Target: graph-automata-max-period. Cell: A357953(9).

Criterion (bank, verbatim): A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term. It must come from exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required), all rules of the class and all 2^n states. Two independent implementations must agree and reproduce every listed term. The result must include a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation. The term must not already be in the live OEIS entry at claim time.

Definition used: rule = subset R of {0,...,n-1}; next state of node v is ON iff (number of ON neighbours of v) is in R.
a(n) = max over connected graphs on n nodes (geng -c n), all 2^n rules and all 2^n start states of the eventual
cycle length.

Statistic / checkers:
- Program A: C, per graph precomputes neighbour counts, per rule builds the successor map, longest cycle by stamped
  walks. Must reproduce A357953(1..8) = 1,2,2,6,7,18,38,96 with graph counts = A001349(1..8).
- Program B: independently written C, bit-sliced equality masks per (node, count) over all states, successor by
  OR over counts in R, transient removal by in-degree peeling, cycles walked once. Must reproduce A357953(1..8).
- Witness (graph6, rule, start) simulated by an independent pure-Python stepper.
- Claim only if A(9) == B(9), both reproduce a(1..8), counts match A001349, the witness simulates to the value, and
  the OEIS DATA re-fetched right before claiming lacks a(9). Thresholds: exact integer equality.

null_test: not needed because the claim is an exact integer from deterministic exhaustive enumeration checked against published terms and a simulated witness, not a search score or a "beats chance" statistic.
