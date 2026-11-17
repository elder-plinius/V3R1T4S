# CRITERION skeptic — A357953(9) = 180

context: subagent (criterion skeptic, isolated claim copy)

Inputs read: the isolated claim copy only (claim.md, REPRODUCE.md, table_record.md, code/, result/, data/, tools/geng). No attempts, BRIEF, LOG, REPORT, dossiers or other panel files were read. I did not re-run the full n=9 search; that is reproduce's job. Light checks only: witness stepping, the geng -c 9 count, witness membership and connectivity, and sha256s.

## Clause-by-clause (full criterion)

1. **"A new exact term of … A357953(9)"**: The claimed value is a(9) = 180 for A357953. The offset is 1 (`%O 1,2`), and the 8 published terms 1,2,2,6,7,18,38,96 are n = 1..8, so n = 9 is the next unpublished index. The value is the maximum over the whole search, so it is exact if the search is exhaustive. MET (conditional on reproduce).
2. **"exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required)"**: REPRODUCE uses `geng -cq 9 r/8` for r = 0..7, which is a disjoint split that covers everything. The 8 part counts (44686+35236+38391+18939+20847+12060+56096+34825) sum to 261080, which equals A001349(9). I checked the bundled geng myself: `geng -cq 9 | wc -l` = 261080. Both programs report the same per-part counts, and merged files state 261080 match. Graphs are unlabeled isomorphism classes. That is fine because cycle length does not change under isomorphism. The connected restriction matches the A357953 definition. MET.
3. **"all rules of the class"**: The neighbours-only count is 0..n-1, so there are 2^n rule subsets. Program A uses K = n and loops R < 2^K without `self`. Program B loops R < 2^n with k < n. The rules are deterministic synchronous ON-iff-count-in-R rules, the same convention as the OEIS examples. Both programs reproduce the OEIS rule examples' values for n ≤ 8. This is not the self-counting class (A357952), because A runs in default mode, which prints `mode=neighbours`. MET.
4. **"all 2^n states"**: A walks every start s < 2^n with stamp-based cycle detection, so every cycle reachable from any start is measured. B builds the full successor table on 2^n states, peels transients by in-degree, and walks every remaining cyclic state. Neither uses sampling or pruning by symmetry or heuristics. MET.
5. **"Two independent implementations must agree"**: A uses direct per-state stepping and B uses bit-sliced counting plus in-degree peeling, so the algorithms differ. Each has its own graph6 decoder. They agree on every n = 9 part: the same max, witness graph and rule mask in all 8 parts, and 180 overall. B reports witness state 2 and A reports 175. Both lie on the same cycle: I stepped both through tstepper and each gives cycle_length = 180 with preperiod 0. Caveats: the two programs share the geng input stream, which the criterion requires anyway, and the bundle does not show whether separate authors wrote them. Read literally, the clause is met by two different codebases and algorithms. MET (with caveat).
6. **"reproduce every listed term"**: A_n1_8 and B_n1_8 both give 1,2,2,6,7,18,38,96, which equals the published DATA for n = 1..8. MET.
7. **"witness (graph6, rule, start) whose cycle length equals the claimed value under direct simulation"**: The witness is H?`DBbS, rule {0,2}, start 175. I ran the pure-Python tstepper, which gives preperiod 0 and cycle_length 180. The witness is in the `geng -c 9` output exactly once and is connected (9 nodes, 11 edges). MET.
8. **"not already in the live OEIS entry at claim time"**: The snapshot data/A357953.txt (sha256 e217d9de…4754c, matches claim.md) has only %S 1,2,2,6,7,18,38,96, with keywords nonn,more,hard. It has no a(9) and no b-file. The draft page snapshot says "No pending changes". This is judged from the bundled snapshot only; I did not do a live re-fetch, per the isolation instruction. MET (as of snapshot 2026-11-02 04:58 EST).

## Hidden quantifiers / stretched definitions
- Disconnected graphs: excluded by -c, and the count matches A001349(9). OK.
- Wrong rule class: the run is neighbours-only, not self-inclusive. Rule count n is excluded correctly, since it can't occur anyway. OK.
- Sampling: none. It loops over all graphs × 2^9 rules × 2^9 states. OK.
- Wrong n or offset: n = 9 with offset 1, which is the 9th term. OK.
- "Maximum period" versus "max cycle over starts": the same quantity per the OEIS %C. OK.
- Null-model sanity: the n ≤ 8 terms reproduce exactly. The n = 9 histogram is smooth up to 142, then has isolated values 165 and 180. A single graph attains 180, and its rule {0,2} is the same rule family as the n = 6 and n = 7 optima, so the result is plausible and not an artifact.
- Minor: the tstepper.py docstring says `maxsingle` but the code checks `maxall`. This does not affect the witness check.
- Partial wins p1/p2: the brief says they are "also in claim.md", but this copy of claim.md has no p1/p2 text. I can't judge them, and they aren't needed because the full criterion is met.

## Non-subsumption
The live-entry snapshot has no a(9) and the draft has no pending edits. Nothing in the bundle shows A357953(9) claimed elsewhere. A357951 and A357952 are different sequences (A357953 ≤ A357951), so they do not cover this term. The win is genuine and not subsumed, subject to the reproduce stage confirming the full search.

## confirmed_scope
Exhaustive enumeration of all 261080 connected 9-node graphs (nauty geng -c), all 2^9 neighbours-only totalistic rules and all 2^9 start states, by two differently-built programs that agree and reproduce A357953(1..8), gives A357953(9) = 180, with witness H?`DBbS, rule {0,2}, start 175 confirmed by direct simulation; the term is absent from the OEIS entry snapshot fetched 2026-11-02 04:58 EST.

pass: true
