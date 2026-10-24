# Definition of the automaton, the state order and the vector file

Everything below is implemented, from this text alone, in verify-it-yourself/check_saw482_k34.py. The state list and the transitions are NOT shipped: the checker rebuilds them. Only the integer test vector is shipped (object/vector_part_NN.bin).

## Lattice
Vertices: integer points (x, y) with (x mod 3, y mod 3) one of (1,0) type E, (2,0) type W, (0,1) type N, (0,2) type S. Neighbours (offsets), in this fixed order:
- E: (-1,+1), (-1,-1), (+1,0)
- N: (+1,-1), (-1,-1), (0,+1)
- W: (+1,+1), (+1,-1), (-1,0)
- S: (+1,+1), (-1,+1), (0,-1)
This is the 4.8^2 lattice (squares and octagons, every vertex of degree 3) drawn in the plane with these coordinates: the squares are the diamonds with corners (1,0), (0,1), (-1,0), (0,-1) and their translates by 3Z^2, joined by the horizontal edges (1,0)-(2,0) and the vertical edges (0,1)-(0,2). dist is graph distance. Every vertex has a neighbour with strictly larger x and one with strictly smaller x, and likewise for y (checked by the checker; used in THEOREM.md).

## Automorphisms used
sigma = translation by (3a, 3b) composed with one of 8 symmetries g_s about the origin: for s = 0..7, first sx = -x if bit 0 of s else x; sy = -y if bit 1 of s else y; then (sy, sx) if bit 2 else (sx, sy).

## Walks, canonical form, states
A walk is a list of distinct vertices, consecutive ones adjacent, oldest first, head last. Canonical form: let (ax, ay) be the head, rx = ax mod 3, ry = ay mod 3, tx = ax - (-1 if rx == 2 else rx), ty likewise. Translate all points by (-tx, -ty), apply each of the 8 symmetries, keep the symmetry whose coordinate sequence (x, then y, of the head, then of the previous point, and so on back to the oldest) is lexicographically smallest. The head of a canonical walk is always (-1, 0). A state is a canonical walk. Its key (used for equality and for the order) is the byte string d_1 d_2 ... d_(L-1), where d_i in {0, 1, 2} is the index, in the neighbour order above, of the next vertex backwards from the current one, starting at the head (-1, 0).

Loop length K = 34. prune(walk, head): drop oldest vertices one at a time (start = 0, 1, ...) while start < len - 2 and (len - 1 - start) + dist(walk[start], head) > K; the result walk[start:] is canonicalised.

## Seeds (state indices 0 and 1)
Index 0: the canonical form of [(1,0), (0,1)] (square edge). Index 1: the canonical form of [(1,0), (2,0)] (octagon edge).

## Transitions (rebuilt by the checker)
For a state with walk P (oldest first), vertex set V, head h, and each neighbour A of h (in the neighbour order of h) with A not in V, let ex = P + [A] (so ex[0] is the oldest vertex of the state and A the new head). The move is kept or pruned by the FINITE-POCKET TESTS (use_bridges = 2 of the author's generator):

- Test 1: A must lie in an infinite connected component of the lattice graph with the vertices of P removed (the removed set is exactly the state P, not the longer ex). If A lies in a finite component, the move is pruned.
- Test 2: ex[0] must lie in an infinite connected component of the lattice graph with the vertices ex[1], ..., ex[L] removed (the removed set is the state without its oldest vertex, plus A). If ex[0] lies in a finite component, the move is pruned.

The author's generator decides "infinite" by a breadth-first search from the tested vertex avoiding the removed set: it answers "infinite" as soon as it pops a vertex outside the bounding box of (removed set + tested vertex) enlarged by 2 in every direction, or when the total number of vertices it has discovered (ever enqueued, not the instantaneous queue length) would exceed 4096; it answers "finite" only when the queue empties, that is, when the whole component has been enumerated and is finite. An answer "infinite" from the box rule is exact: a vertex outside the enlarged box can move in a monotone coordinate direction forever without meeting the removed set (every vertex has a neighbour with strictly larger and one with strictly smaller x, and the same for y). An answer "finite" is exact. Only the cap could make the generator answer "infinite" for a finite component (one with more than 4096 vertices); the checker counts such cases, FAILS if there is one, and reports 0 (line "full searches that hit the 4096 cap"). The cap is also unreachable here by counting: see THEOREM.md section 5. The checker uses a faster exact route first (a monotone path in one of the four coordinate directions that leaves the bounding box of the removed set proves "infinite"), and falls back to the same breadth-first search only when no such path exists. Hence the kept/pruned decisions coincide with the generator's, and with the mathematical definition (infinite component) as long as the cap count is 0.

For a kept move, the candidate targets are:
1. c0 = prune(ex, A).
2. If (len(ex) - 1) + dist(ex[0], A) > K: chord shortcuts. For a from min_a (initially 0) up to len(w) - 4 and, for each b with a + 2 <= b <= len(w) - 2 in increasing order, such that w[a] and w[b] are adjacent (w is the walk being examined at that level, its last vertex is A): the shortcut sx = w[0..a] + w[b..end] gives the candidate prune(sx, A); and if the recursion depth is below 3 and (len(sx) - 1) + dist(sx[0], A) > K, recurse on sx with depth + 1 and min_a = a. A candidate joins the candidate list if it is not already in it and the list has fewer than 64 entries.
3. Second pass: if (len(ex) - 1) + dist(ex[0], A) > K: for start = 0, 1, ... while start < len(ex) - 2 and (len(ex) - 1 - start) + dist(ex[start], A) > K, the canonical form of ex[start:] is a further candidate if it is a state of the final state set. There is NO limit on the number of second-pass candidates here (the author's generator stops adding at 32 candidates; we do not, so this is a slightly different, still valid automaton; the checker finds 0 second-pass candidates present in the final state set in this run, so the difference is numerically inert).
The target is the candidate with the smallest vector entry (ties are immaterial).

## State order (this fixes which vector entry belongs to which state)
States are numbered in order of first appearance by this procedure: put the two seeds at 0 and 1. For i = 0, 1, 2, ... (until i reaches the number of states found so far), process state i: for each kept move in neighbour order, for the plain candidate c0 and then for every chord shortcut in the order the recursion above produces them (ALL of them, including repeats and including those beyond the 64-entry list limit), append the candidate's canonical state to the numbered list if it is not already there. Second-pass candidates are never added.
The final number of states is 16,873,086.

## Vector file (object/vector_part_NN.bin concatenated = vector.xz)
vector.xz is an xz (lzma) stream. Its decompressed content is: 8 bytes big-endian N (the number of states), 1 byte format version (1), then three byte strings of length N each: E (exponent), H (high byte of the mantissa), Lo (low byte of the mantissa). The test vector is x_i = ((H_i * 256 + Lo_i) * 2^(E_i)), i = 0 .. N-1, in the state order above. The mantissa has at most 16 bits. The checker computes with these integers exactly.

## Note on the author's generator
The generator's second pass indexes its candidate lists by the count of all unvisited neighbours, while the first pass stores only the kept moves, so after a pruned move the two indexings can disagree. We compiled a copy of the generator with the second pass fixed to skip pruned moves; it produced the same 16,873,086 states and the same exact ratio as the original (19360805483/10605620094). The checker follows the aligned definition above, so it does not depend on this.
