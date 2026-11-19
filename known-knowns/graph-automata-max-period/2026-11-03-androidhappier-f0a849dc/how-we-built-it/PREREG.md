# PREREG (frozen 2026-11-03T03:26:05Z per date -u, before any attack program for this cell has been run at n = 11)
(Speed prototype tools/proto/lifeF.c was timed on one 1/4000 slice of n = 11 in run 2026-11-03-0236 (max 35 on that
slice); that slice is not a result for the cell and no full-n attack output exists.)

Target: graph-automata-max-period. Cell: A384209(11). One cell per claim.

Criterion (bank, verbatim): A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term. It must come from exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required), all rules of the class and all 2^n states. Two independent implementations must agree and reproduce every listed term. The result must include a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation. The term must not already be in the live OEIS entry at claim time.

Definition (OEIS A384209): Life on a simple graph; live vertex survives iff 2 or 3 live neighbours; dead vertex born
iff exactly 3; a(n) = max period over all simple graphs on n vertices (disconnected allowed) and all starts.

Statistic: M = max over all graphs on 11 vertices and all 2048 starts of the eventual cycle length.

Programs:
- A: lifeA11.c (new; from the lifeF prototype: SWAR nibble counts along a Gray-code state walk, epoch-stamp cycle
  finder) on ALL graphs, geng -q 11 in 64 residue classes; outputs per-graph-max histograms (all graphs and the
  connected subset), the graphs whose maximum is >= 40, and a witness.
- B: lifeB2.c (= lifeB.c of run 2026-11-02-0920, bit-sliced successor + in-degree peeling, plus histogram / high-list
  output) on CONNECTED graphs (geng -cq k, k = 1..11) giving the cycle-length set per order, then combine.py (lcm over
  partitions into connected components) for a(n).

Decision rule:
- Both A and B reproduce a(1..9) = 1,1,1,1,2,4,8,14,27 and a(10) = 46 (our earlier result).
- n = 11: A's graph total = 1018997864 = A000088(11); B's connected total = 1006700565 = A001349(11);
  A's connected-subset histogram == B's histogram exactly; the connected graphs with max >= 40 are the same set;
  M_A == M_B (B's M from combine.py).
- Witness (graph6, start) gives cycle length exactly M under a third, direct Python stepper.
- Claim only if M is not in OEIS A384209 at claim time. Any disagreement => no claim.
- Max reachable status this session: PROMISING (single-context, unpanelled).

null_test: not needed because the claim is a deterministic exhaustive enumeration checked against a table value (explicit witness plus two agreeing exhaustive programs); no search statistic.
