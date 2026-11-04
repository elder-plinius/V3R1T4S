# CRITERION skeptic — run 2026-11-03-0324, claim A384209(11) = 71

Context: I started fresh and worked from an isolated copy (`cp -a .../claim [scratch]/panel0324-criterion`) on 2026-11-03 at 02:53–02:56 EST. I read claim.md, table_record.md, REPRODUCE.md, code/*, the A10/A_n1_9/A11_summary/combine/compare_AB/witness result files and data/A384209_claimtime.txt. I wrote my own pure-Python Life stepper with a standard graph6 decoder ([scratch]/mysim.py) and used it for witness checks and small-n checks. I did not re-run n=11.

## Bank criterion, clause by clause

1. **"A new exact term of any of the four sequences: A384209(10), A357951(8), A357952(9) or A357953(9), or a later term."** The claimed term is A384209(11), which counts as a "later term" of A384209. It is not a term of A357951/2/3. I checked the live entries today. Those three use connected graphs and range over all outer-totalistic or totalistic rules: A357951 has 2,2,4,6,16,26,66, A357952 has 2,2,4,6,8,18,42,112, and A357953 has 1,2,2,6,7,18,38,96. A384209 fixes the rule to Life B3/S23 and allows disconnected graphs. Hidden quantifier: does "later term" require a(10) to be established first? The a(11) result does not depend on a(10) being in the OEIS. Program A enumerates every 11-vertex graph directly. Program B's component-lcm step uses the order-10 connected periods only to bound disconnected graphs, and those stay at 46 or below, under 71. So the clause is met. a(10)=46 is the contributor's own earlier claim (open PR #904). This package reproduces it but does not claim it, and it gets no credit for it here. **MET (a(11) only).**
2. **"exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required)".** A384209 covers all simple graphs, disconnected ones included. Program A ran `geng -q 11` in 64 residue classes and got 1,018,997,864 graphs, which equals A000088(11). Of these, 1,006,700,565 are connected, which equals A001349(11). Program B ran `geng -cq k` for k=1..11 and got 1,006,700,565 connected graphs at k=11. It covers disconnected graphs exactly through the lcm over component partitions; a disjoint union evolves componentwise, so this step is sound. Note: B's coverage of disconnected graphs is derived, not enumerated graph by graph. Even so, the class is covered exhaustively, and A's direct all-graph enumeration closes the gap. geng sha256 matches the stated 75d1bf01…. **MET.**
3. **"all rules of the class".** The class has one rule, Life B3/S23. Both programs implement birth on exactly 3 and survival on 2 or 3: A uses nibble SWAR tests, B uses a bit-sliced counter with eq3 | (live & eq2). **MET.**
4. **"all 2^n states".** A walks cycles from every state 0..2^n−1. B builds the full successor map, peels transients and walks every remaining cycle. **MET.**
5. **"Two independent implementations must agree".** A and B use different successor constructions (Gray-code incremental + pext vs. bit-sliced) and different cycle detection (epoch-stamped walks vs. in-degree peeling). They also decode graph6 separately. They share only geng and the author. compare_AB.txt shows several agreements:
   - The connected-graph histograms of per-graph maxima are identical (sum 1,006,700,565).
   - The 1718 high (≥40) connected graphs are identical.
   - A's all-graph max is 71, matching B's connected max of 71 and B's combined a(11)=71.
   
   **MET.**
6. **"and reproduce every listed term".** The listed terms are OEIS DATA a(1..9) = 1,1,1,1,2,4,8,14,27. A reproduces them directly (A_n1_9.txt), and B reproduces them through combine (combine_n1_11.txt). Both also give the unlisted a(10)=46. My own simulator independently gave n=7 → 8 (1044 graphs) and n=8 → 14 (12346 graphs), and it reproduced the OEIS n=9 example HCZJtzm/47 → 27. **MET.**
7. **"a witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct simulation".** My own stepper gave these results:
   - J?qrdjivb}_ (11 vertices, 31 edges), rule B3/S23, start 752: preperiod 0, cycle 71.
   - Over all 2048 starts on that graph, the maximum cycle is 71.
   - The second witness JCpbdo}ttv_ with start 1728 also gives preperiod 0, cycle 71.
   
   **MET.**
8. **"The term must not already be in the live OEIS entry at claim time".** The claim-time fetch (2026-11-03T07:36:52Z = 02:36 EST) shows %S 1,1,1,1,2,4,8,14,27, %I #8 May 22 2025. The draft page says "No pending changes". I re-fetched the live entry at 02:54 EST and it was unchanged, with no a(10) and no a(11). The only repo hit is #904, which is for a(10). **MET.**

## Residual caveats (not failing)
- I accepted the n=11 exhaustive outputs as recorded rather than re-running them, as the brief allows. They pass the completeness checks against A000088 and A001349, and the two programs agree.
- The two programs share an author and the geng binary, so they are not fully independent provenance. Their algorithms are clearly distinct.

## Win type
This is the full success criterion ("a later term" of A384209), not a partial win. It is not subsumed by PR #904, which claims only a(10)=46. Credit goes only to the new value a(11)=71.

confirmed_scope: A384209(11) = 71 (maximum Life B3/S23 cycle length over all 1,018,997,864 simple graphs on 11 vertices and all 2^11 start states), with witness J?qrdjivb}_ from start 752; a(10)=46 is excluded from this package's credit (prior own claim, PR #904), and the claim is unrelated to A357951/2/3.

pass: true
