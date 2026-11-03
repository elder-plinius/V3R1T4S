# CRITERION skeptic: A357951(8) = 150
context: subagent (criterion skeptic, isolated claim copy)

Worked from [scratch]/panel0236-criterion (cp -a of claim/). Did not read attempts/, REPORT, or other panelists' files.
Checks I ran myself: the witness through ostepper.py, diff_AB.py on the shipped result files, geng -cq 8 | wc -l,
recompiling otA.c and rerunning n=5..7 plus the witness graph alone, a connectivity check of GCQfBg, and a live
OEIS fetch (2026-11-02 ~23:20 EST).

## Clause-by-clause (bank criterion, verbatim clauses)
1. "A new exact term of any of the four sequences: ... A357951(8) ... or a later term." PASS. The claim is about
   A357951(8) exactly, the cell the bank names. It is an exact maximum, not a bound.
2. "exhaustive enumeration of all graphs of the class (nauty geng, connected graphs where required)". PASS.
   geng -cq 8 gives 11117 graphs (I re-checked this). That matches A001349(8) = 11117, and labelg plus sort -u also
   gives 11117 (completeness.txt). The per-part summary counts 924+2268+2141+273+97+2562+1473+1379 add up to 11117
   for both A and B. The connectivity flag -c matches the definition's "connected graphs".
3. "all rules of the class". PASS. Program A walks all 2^(2n) = 65536 (B,S) pairs, with B and S subsets of {0..7}.
   Program B restricts counts to 0..maxdeg. Its header proves this is complete: a count c(v) <= deg(v) <= D, so
   memberships above D are never consulted. This is a sound reduction, not a stretched definition.
4. "all 2^n states". PASS. Both programs iterate over every s < 2^n (Program A: the inner loop over all N states for
   each rule; Program B: the full successor map with Kahn peeling).
5. "Two independent implementations must agree and reproduce every listed term." PASS. A is C with Gray-code rule
   walking and a stamp cycle finder. B is Go with restricted rules and in-degree peeling. These are different
   languages and different algorithms. Both reproduce 2,2,4,6,16,26,66 for n=1..7 (A_n1_7, B_n1_7; I reran A for
   n=5..7). At n=8 they agree graph by graph: 11117 keys, 0 mismatches, both maxima 150, unique argmax GCQfBg.
6. "witness (graph6 string, rule, start state) whose cycle length equals the claimed value under direct
   simulation". PASS. Witness: GCQfBg, B={0,2}, S={1,3,4}, start 1. The pure-Python stepper gives transient=0 and
   cycle_length=150. Program A's raw mask B={0,2,7} gives the same 150, since count 7 can't occur at max degree 4.
   GCQfBg is connected (I checked) and has 8 nodes.
7. "The term must not already be in the live OEIS entry at claim time." PASS. The claim-time fetch
   (2026-11-03T02:50:41Z) shows DATA 2,2,4,6,16,26,66, %I #11, keyword "more", and the draft page says "No pending
   changes". My re-fetch at panel time shows the same: %I #11, %S 2,2,4,6,16,26,66.

## Hidden quantifiers / stretched definitions
- "Outer totalistic": the next state depends on (own state, number of ON neighbours) through separate B and S sets.
  Program A, Program B and ostepper all use exactly this. None of them folds in the node's own state as a summed
  count (that would be A357952) or forces B=S (that would be A357953). The OEIS examples' convention matches
  ("first set: OFF turns ON; second set: ON stays ON").
- "Max of the length of that cycle": the code takes the eventual cycle length, not transient plus cycle. The
  witness has transient 0 anyway.
- "All rules": a possible trap is whether counts range over 0..n-1 or 0..n. Neighbour counts are at most n-1, so
  0..n-1 is complete. Program A covers all of 0..n-1.
- Synchronous update: this is implicit in OEIS (and in the n=7 example FBjng with {0,1,3},{2,4,5}, which the
  stepper reproduces at 66). All three tools update synchronously.
- Unlabeled vs labeled graphs: the maximum is the same under isomorphism, so iterating over isomorphism classes is
  enough.
- Null model / sanity: the n=1..7 controls reproduce exactly. The 150 is a single outlier (next best are 124, 115,
  114, 112, 109), but direct simulation confirms it, so it is not an artifact. It also fits the growth pattern
  (66 -> 150, about 2.3x, compared with 26 -> 66, about 2.5x).
- Status source: the bank's status_source URL is A384209, the sibling entry. The claim checks A357951 directly,
  and that is the entry the criterion actually concerns. No stretch here.

## Non-subsumption vs sibling cells
- A357952 (totalistic, own state counted) and A357953 (totalistic, neighbours only) are subclasses of
  outer-totalistic rules. So A357951(n) >= both, but 150 tells us nothing exact about A357952(9) or A357953(9),
  the bank's targets for those cells. This claim also does not borrow from them.
- A384209 (Game of Life on all graphs) is one fixed rule family with its own n=10 target. It is unrelated and not
  implied.
- A357951(8) is the first missing term of A357951. It is not a re-derivation of a listed term, and the live entry
  and draft do not cover it. This is a genuine full win for the named cell, not a partial win.

## confirmed_scope
A357951(8) = 150: exhaustive enumeration of all 11117 connected 8-node graphs (geng -cq 8), all 65536
outer-totalistic (B,S) rules and all 256 initial states, by two independent programs that agree graph by graph and
reproduce a(1..7) = 2,2,4,6,16,26,66, gives a maximum eventual cycle length of 150, attained uniquely by the graph
GCQfBg (witnessed under direct simulation by rule B={0,2}, S={1,3,4} from start state 1), and the term is absent
from the live OEIS entry and its draft at claim time.

pass: true
