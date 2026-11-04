# PREREG (frozen 2026-11-03T04:23:34Z per date -u, before any attack program for this cell has been run on all of n = 10)
(Speed check: tools/proto/totF.c and totB10 were timed on the single slice geng -cq 10 3/400 (27059 graphs; both gave
max 296 and identical histograms/hash). That slice is not a result for the cell.)

Target: graph-automata-max-period. Cell: A357953(10). One cell per claim.

Definition (OEIS A357953): connected graph on n nodes; rule R subset {0..n-1}; node v is ON at t+1 iff the number of
ON neighbours of v (not counting v) at t is in R. a(n) = max over connected graphs, rules and start states of the
eventual cycle length.

Statistic: M = max over all 11716571 connected graphs on 10 vertices, all rules, all 1024 starts.

Programs:
- A: totF.c (C). Rules restricted to subsets of {0..maxdeg} (complete: a count never exceeds deg(v) <= maxdeg, so
  higher bits of R never act), walked in Gray-code order (toggle count k => XOR mask M_k[s]); epoch-stamp walk.
- B: main.go (Go, written separately): same rule range in plain binary order, successor from sparse per-state
  (count, mask) lists, Kahn in-degree peeling then cycle walk.
- Both: geng -cq 10 in 32 residue classes; per class: histogram of per-graph maxima, graphs with max >= 150, and an
  FNV-1a hash of the per-graph max sequence in geng order.

Decision rule:
- Both reproduce a(1..8) = 1,2,2,6,7,18,38,96 and a(9) = 180 (our earlier result).
- n = 10: graph total 11716571 = A001349(10) in both; per residue class identical histograms, high lists and FNV hash
  (graph-by-graph agreement); M_A == M_B.
- Witness (graph6, rule, start) gives cycle length exactly M under a third, direct Python stepper.
- Claim only if M is not in OEIS A357953 at claim time. Any disagreement => no claim.
- Max reachable status this session: PROMISING (single-context, unpanelled).

null_test: not needed because the claim is a deterministic exhaustive enumeration checked against a table value (explicit witness plus two agreeing exhaustive programs); no search statistic.
