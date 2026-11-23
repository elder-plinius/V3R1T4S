# PREREG (frozen 2026-11-03T02:38:10Z per date -u, before any attack program for this run has been written or run)

Target: graph-automata-max-period. Cell: A357951(8). One cell per claim.

Criterion (bank, verbatim): A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term. It must come from exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required), all rules of the class and all 2^n states. Two independent implementations must agree and reproduce every listed term. The result must include a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation. The term must not already be in the live OEIS entry at claim time.

Definition (OEIS A357951 %C): next state of node v depends only on v's own state and c = number of ON neighbours.
Rule = (B, S), B, S subsets of {0..n-1}: an OFF node turns ON iff c in B; an ON node stays ON iff c in S.
2^(2n) rules (65536 for n = 8).

Statistic: M = max over all connected graphs on 8 nodes (geng -c 8, must total 11117 = A001349(8)), all 65536 rules
(B,S), all 256 starts, of the length of the cycle eventually reached.

Thresholds / decision rule:
- Program A (C, all 2^(2n) rules, no pruning, Gray-code rule walk) and Program B (Go, independently written, rules
  restricted to counts 0..maxdeg with the completeness argument written in its header, different cycle finder) must
  each reproduce a(1..7) = 2,2,4,6,16,26,66 exactly, and agree on M for n = 8, on the graph count 11117, and on the
  per-graph maxima for every graph line (diffed).
- Witness (graph6, B, S, start) must give cycle length exactly M under a third, direct stepper (Python).
- A claim is written only if M is not in OEIS A357951 at claim time (re-fetch before claim). Any disagreement => no claim.
- Status this session can reach: at most PROMISING (single-context, unpanelled); panel requested.

null_test: not needed because the claim is a deterministic exhaustive enumeration checked against a table value (an explicit witness simulated directly plus two agreeing exhaustive programs); there is no search statistic or "beats chance" component.
