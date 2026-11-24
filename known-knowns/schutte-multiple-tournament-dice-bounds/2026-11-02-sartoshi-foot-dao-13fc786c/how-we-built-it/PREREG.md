# PREREG.v2 (run 2026-10-27-0844, written 09:38 UTC after seeing that the corner cubes (a+b small) time out; does not change the claim rule or any threshold)
Adds one sound strengthening ("v2 cubes") for m=3 cubes launched from now on; cubes already final (UNSAT) under v1 stay valid because v1 is weaker.
Added constraint: out-degree of vertex 0 in T_3 is <= a+b (= its out-degree in T_2).
Soundness: in the cover argument (PREREG.md) after choosing the maximum-out-degree pair (t,v) and moving t to index 1, the two remaining tournaments may be ordered
(by (ii) tournament-index permutation) so that v's out-degree in T_2 is >= its out-degree in T_3. Then a, b describe T_2 as before and the relabelling of A and B
used for T_2 is unchanged. So every S_6 triple satisfies some v2 cube, and the v2 cubes are a cover; each v2 cube CNF is a subset-of-models of the v1 cube.
Level-2 sub-cubes inherit it. A v1-TIMEOUT cube is first retried once as v2 at the same cap (it is a different, stronger cube), then split at level 2 (v2) if it times out again.
The version is recorded in each cube's output file (field "v2"). Test of the extension: cover_check.py is extended to relabel with this ordering and assert acceptance by the v2 CNF.
