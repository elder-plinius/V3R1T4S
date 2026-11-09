# CRITERION skeptic — A357952(9)
context: subagent (criterion skeptic, isolated claim copy)

Inputs read: the isolated claim copy only (claim.md, table_record.md, REPRODUCE.md, code/, result/, data/). I did not re-run the full search.

## Clause-by-clause
1. **"A new exact term of … A357952(9)"**: this is a cell the criterion names. The claimed value is exact (a maximum over a fully enumerated finite space), not a bound. MET.
2. **"exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required)"**: geng -cq 9 split into r/8 parts. The part counts are 44686+35236+38391+18939+20847+12060+56096+34825 = 261080, which equals A001349(9). Both programs list the same set of 261080 graphs (diff_AB: same graph set True, no duplicates asserted). MET. Caveat: I did not check the geng binary's sha256 independently. The count control covers this.
3. **"all rules of the class"**: for self-counting, R ⊆ {0..n}, which gives 2^(n+1) = 1024 rules at n = 9. totA uses K = n+1 in `self` mode and loops R < 1<<K. totB loops R < 1<<(n+1). MET.
4. **"all 2^n states"**: totA visits every s < 2^n as a start, with stamp-based cycle detection. totB peels off the transient states (indegree), then measures every surviving cycle state. Both cover all 512 states. MET.
5. **Class check (A357952 vs A357953)**: totA's self mode adds `(s>>v)&1` to the count. totB's `closed[v]` starts as `1<<v`, so the closed neighbourhood includes the node itself. My own Python stepper counts popcount(x&adj[v]) plus the node's own bit. This is self-counting, the correct class (A357952). The witness rule includes the value 5, but that only shows the rule range is {0..9}. The class decision rests on the code. MET.
6. **"Two independent implementations must agree"**: the two programs are written in different languages (C and Go) with different cycle algorithms. diff_AB finds 0 per-graph mismatches across all 261080 graphs, identical histograms, max 200 in both, and H?o|]|~ as the only graph reaching 200. MET. Soft caveat: the two programs likely share an author, so "independent" means separately written, not written by separate teams.
7. **"reproduce every listed term"**: A_n1_8 and B_n1_8 both give 2,2,4,6,8,18,42,112. This matches the OEIS DATA for a(1..8). Graph counts for n = 1..8 are 1,1,2,6,21,112,853,11117, which match A001349. The witness graphs differ from the OEIS examples in some cases (e.g. n = 8 G?bevw vs G?Dlvw). That is allowed, because the criterion asks for terms, not witnesses. MET.
8. **"witness … cycle length equals the claimed value under direct simulation"**: I ran an independent inline Python stepper on H?o|]|~, rule {1,3,5}, start 1 (node 0 ON). It first returns to the start at step 200, with degrees [3,3,3,3,6,6,6,7,7]. Start 1 lies on the cycle, so the cycle length is 200, not just the preperiod plus the period. MET.
9. **"not already in the live OEIS entry at claim time"**: the fetch at 2026-11-02 21:35:11Z (4:35 PM EST) shows DATA 2,2,4,6,8,18,42,112 with no a(9). The draft page says "No pending changes". Two fetches gave the same hash. MET, as of that fetch. A re-check immediately before submission is advisable.

## Hidden quantifiers / stretched definitions
- "all totalistic rules": the space is complete under the OEIS convention (R ⊆ {0..n}). Nothing is stretched.
- "all initial states": nothing is restricted to a single starting state. The maximum is taken over all 512 states.
- "connected": geng -c is used. Disconnected graphs are correctly excluded for A357952.
- No overreach: the claim does not say 200 is attained uniquely across all rules. The stepper shows that rules {1,3,5} and {1,3,5,9} both reach it on this graph, and the claim does not contradict that.

## Non-subsumption
A357952(9) is its own cell. It is not A357953(9) (neighbours only), A357951(8) or A384209(10), and it is not implied by any of them. a(n) ≤ A357951(n) is only a bound. I have no visibility into other PRs or cells from this isolated copy, so I could not check whether a parallel claim exists for the same cell. Based on this bundle, the win is not subsumed.

## confirmed_scope
Exhaustive enumeration of all 261080 connected 9-node graphs (geng -cq 9), all 1024 self-counting totalistic rules R ⊆ {0..9} and all 512 states, by two separately written programs that agree graph by graph and reproduce A357952(1..8), gives A357952(9) = 200, uniquely attained on graph H?o|]|~, with witness rule {1,3,5} from start state 1 directly simulated to a 200-cycle, and the term was absent from the live OEIS entry as of 2026-11-02 21:35Z.

pass: true
