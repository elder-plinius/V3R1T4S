# How we found it (contributor text, unverified)

The run first tried to beat the community bound 5/9 with real (4,5)-sets. Every 2-point self-similar chain, single
seed or mixed, over the published libraries of extremal 12- and 14-point seeds and a sample of 15-point seeds, and every
single-seed 3-point chain over the same libraries, gave growth ratios of 5/9 or more (exact max-plus transfer
matrices, no cycle below 5/9). That pointed at
the gluing itself: a chain of blocks glued on two vertices has a 4x4 max-plus transfer matrix, and its growth is at most
C/D exactly when an integer potential psi satisfies D*M[s][t] <= C + psi[t] - psi[s].

So the run dropped the integers and searched the paper's abstract class directly. cegar.py asks CP-SAT for an
n0-vertex block (labels as the order, one edge per middle, linear, F7-free by lazy cuts, anchors at the first and last
vertex) together with psi; each independent set that violates the potential inequality comes back as a cut ("this set
contains an edge, or the inequality holds"). Calibration: it finds the known 11-vertex growth-5 block in 4 seconds and
proves an 11-vertex block of growth 9/2 impossible (as the 9/17 theorem requires). At n0 = 13 with growth 6 it found
the block in object/construction.json in 77 seconds. Gluing 9 copies gives H: n = 101, alpha = 56, the first chain
length below 5/9 (8 copies give exactly 5/9). A 2-vertex cut cannot carry an F7 (each F7 vertex has degree 2 or more
inside it) and the merged order keeps every edge's middle, so the chain stays in the class.

What failed: H is not the A.P.-hypergraph of any set of numbers (an 8-vertex piece of each copy forces a coincidence
or an extra progression). A realizability-aware search over 30 anchor classes at n0 = 13 (206 abstract blocks, 1,155
bad-relation cores) and an integer-position model found no realizable growth-6 block within their time caps; those
searches were capped, so they exclude nothing.
