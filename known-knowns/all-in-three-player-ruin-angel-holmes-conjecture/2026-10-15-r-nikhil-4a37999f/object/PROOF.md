# An exact region certificate for the Angel–Holmes conjecture

For all positive real x,y,z with x<y, we prove f(x,y,z)>f(y,y,z), where f is the probability that player 1 is the first player eliminated in the all-in game. This is Conjecture 9 of Angel Y. He and Mark Holmes, *All In: Give me your money!*, arXiv:2410.15329v1, Section 5.3. The conjecture is attributed there to Omer Angel and Mark Holmes. Their Theorem 1 proves a different, swapping inequality; it is not used here. The partition approach is inspired by their MeshItUp framework. The adaptive enclosure generator and separate exact certificate checker here are new implementations.

The game is the one in the paper's abstract and Section 1. At each live state, choose one of the three unordered pairs uniformly and toss a fair coin. Transfer the smaller stack from loser to winner. Stop as soon as a stack becomes zero. Each pair/coin outcome thus has probability 1/6. Scaling all stacks by a positive constant preserves every transition and elimination outcome.

## Infinite-horizon bound

Let H_n be the probability that player 1 is eliminated first within n rounds, with H_0=0. The paper uses h_n for elimination in exactly round n; the bank uses h_n for our cumulative H_n.

At every live state, at most three of the six outcomes continue, and at most two immediately eliminate player 1. Put U=4/5. If continuing-state values are at most U, their Bellman update is at most (2+3U)/6=11/15<=U. Induction from H_0=0 gives 0<=H_n<=U. The events increase to first elimination of player 1, so 0<=f<=U. Moreover, each round survives with conditional probability at most 1/2. Survival through n rounds is at most 2^(-n), absorption occurs almost surely, and f satisfies the six-outcome Bellman equation. The constant U also appears as Lemma 2 of the source; the elementary argument here is sufficient by itself.

## Enclosures on a region

All live stacks in the computation are affine forms in two normalized coordinates. A polygon or segment denotes its relative interior, and a point denotes itself. If an affine form is weakly nonnegative at every vertex and strictly positive at at least one vertex, it is strictly positive on the relative interior. If all its vertex values vanish, it is identically zero there. Negative signs follow by negation. Otherwise its sign is unresolved on the region.

At recursion depth zero enclose every live-state probability by [0,U]. For a pair with known comparison, compute both coin outcomes exactly. Immediate elimination of player 1 contributes [1,1], elimination of another player contributes [0,0], and a live successor contributes its enclosure at the next smaller depth. Sum all pair/coin contributions and divide by six.

An unresolved comparison is stopped locally for that pair. If player 1 is in the pair, at most one outcome can immediately eliminate player 1 and at most one can continue. Their combined contribution before division by six is in [0,1+U]. If player 1 is outside the pair, neither outcome immediately eliminates player 1 and at most one continues, giving [0,U]. A tie only removes continuing outcomes. These bounds hold throughout the region, regardless of the unresolved comparison's sign. Induction on depth proves every resulting enclosure sound for the infinite-horizon f.

Every stored leaf has four integer numerators (L_A,U_A,L_B,U_B) over 5*6^d, for its two initial states A,B and its own depth d. The certificate's global depth is the default; a leaf's explicit depth field overrides it. The strict inequality L_A>U_B is checked at every leaf. The leaf need not resolve every possible subsequent comparison: its conservative enclosures suffice.

## Domains, including equality cases

The three disjoint alternatives z>=y, x<z<y, and z<=x exhaust all positive x<y.

* Leader: normalize by y+z, put a=x/(y+z), b=y/(y+z). Compare A=(a,b,1-b), B=(b,b,1-b). The domain 0<a<b<=1/2 is the relative interior of the triangle (0,0),(0,1/2),(1/2,1/2), together with the open edge (0,1/2)--(1/2,1/2). That edge is z=y. The other edges and all vertices violate a strict hypothesis.
* Middle: normalize by y, put a=x/y, c=z/y. Compare A=(a,1,c), B=(1,1,c). The domain 0<a<c<1 is the relative interior of the triangle (0,0),(0,1),(1,1). No outer edge is included.
* Shortest: use the same normalization and states as the middle case. The domain 0<c<=a<1 is the relative interior of the triangle (0,0),(1,0),(1,1), together with the open diagonal edge (0,0)--(1,1). That edge is z=x. The other edges and all vertices violate a strict hypothesis.

The checker hard-codes these domains and initial affine forms from the definition. It does not read them from the generator.

Each internal node records an affine line crossing its parent's relative interior. Its three children, in order, are the negative part, the equality section, and the positive part. Their relative interiors partition the parent's relative interior. Original excluded boundary points stay excluded. Intersections inside the parent appear in the equality child. A split of a segment has two open-segment children and the intervening point.

For each split the checker independently intersects the line with every vertex-pair segment and takes rational convex hulls. This reconstructs the three exact closures; including diagonals changes no hull. It checks all three children, every root, all reachable nodes exactly once, absence of unreachable nodes, and absence of unfinished or unresolved leaves. These checks establish complete continuous coverage, including every admissible internal equality face. No grid or sampling argument contributes to coverage.

## Certificate values

| Ordering | File | Nodes | Leaves | Leaf depths | Minimum enclosure separation |
|---|---|---:|---:|---|---|
| z>=y | certificates/leader.json | 128 | 86 | 7 | 181/1399680 |
| x<z<y | certificates/middle.json | 7 | 5 | 3 | 1/135 |
| z<=x | certificates/shortest.json | 9704 | 6470 | 2260 at 12; 4210 at 13 | 379/1813985280 |

All three minima are strictly positive. Their common minimum is 379/1813985280. Thus the certificates actually imply the uniform inequality f(x,y,z)-f(y,y,z)>=379/1813985280>0 for every admissible triple, proving the stated conjecture. The lower bound is conservative; no assertion of optimality is made.

## Independent implementation and exactness

The prover uses backward recursion with memoized affine states, homogeneous integer polygon clipping, and a heuristic choice of split. None of its choices are assumptions of the verifier. The verifier imports no prover code: it uses rational convex hull intersections and forward propagation of exact multiplicities over the six explicit pair/coin outcomes. It recomputes all four leaf bounds and compares them with the stored integers.

The standard-library Python verifier uses unbounded integers and fractions.Fraction. The optional C++17 kernel accelerates only forward enclosure evaluation; Python still checks the complete partition exactly. The kernel guards depth<=18, absolute homogeneous vertex coordinates<=2^60, positive homogeneous denominators, and absolute initial affine coefficients<=2^30. After at most 18 transitions, affine coefficients have magnitude at most 2^48 and comparison differences at most 2^49. Sign dot products therefore fit comfortably in signed 128-bit integers. At most 6^18 outcome paths exist; multiplicities fit unsigned 64-bit integers. The total bound numerators are at most 5*6^18 and fit signed 64-bit integers, while their intermediate sums use signed 128-bit integers. There is no floating-point arithmetic in any proof check.

The optional kernel is a separate forward implementation, not the prover's backward kernel. A Python forward implementation and a Fraction-based recursive reference are also supplied for inspection. This is a computer-assisted exact region proof, not a Lean, Coq or Isabelle formalization. Its analytic enclosure and partition lemmas are the elementary arguments above.
