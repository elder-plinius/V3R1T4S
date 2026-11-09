# PREREG (frozen 2026-11-02T21:06:19Z per date -u, before any attack program for this run has been written or run)

Target: graph-automata-max-period. Cell: A357952(9). One cell per claim.

Criterion (bank, verbatim): A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term. It must come from exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required), all rules of the class and all 2^n states. Two independent implementations must agree and reproduce every listed term. The result must include a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation. The term must not already be in the live OEIS entry at claim time.

Statistic: M = max over all connected graphs on 9 nodes (geng -c 9, must total 261080 = A001349(9)), all rules
R subset {0..9} (1024 rules, ON iff |N(v) cap ON| + [v ON] in R), all 512 starts, of the length of the cycle reached.

Thresholds / decision rule:
- Program A (totA self, from run 0959) and Program B (new, independently written in Go) must each reproduce
  a(1..8) = 2,2,4,6,8,18,42,112 exactly, and agree on M for n = 9, on the graph count 261080, and on the full
  per-graph-maximum histogram (stronger: per-graph maxima identical for every graph line, diffed).
- Witness (graph6, rule, start) must give cycle length exactly M under a third, direct stepper (Python).
- A claim is written only if M is not in OEIS A357952 at claim time (re-fetch before claim). Any disagreement => no claim.
- Status this session can reach: at most PROMISING (single-context, unpanelled); panel requested.

null_test: not needed because the claim is a deterministic exhaustive enumeration checked against a table value (an explicit witness simulated directly plus two agreeing exhaustive programs); there is no search statistic or "beats chance" component.
