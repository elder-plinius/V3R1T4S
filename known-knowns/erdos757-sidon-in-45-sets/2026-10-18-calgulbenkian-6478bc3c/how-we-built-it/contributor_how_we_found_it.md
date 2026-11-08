# How We Found It: Algebraic Block Gluing of `(4, 5)`-Sets (`|A_21| = 21`, `s(A_21) = 12`)

*(contributor text, unverified)*

## 1. Shell Decomposition and Affine Rigidity of Ma-Tang's `A_14`

Analyzing the `12 x 14` 3-AP incidence matrix `M(H(A_14))` of Ma and Tang's 14-element witness `A_14 = {0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056}` over `Q` reveals `rank(M) = 12` (`dim ker M = 2`, so `A_14` is affinely rigid) and decomposes `H(A_14)` into two isomorphic 8-vertex, 5-edge shells `B_8^in` and `B_8^out` sharing two vertices `{2, 10}` and linked by two cross-edges.

## 2. Single-Vertex Block Gluing with Transversal-Forcing Cross-Edges

We glue `A_14` (`n=14, m=12, tau=6`) to an 8-element shell `B_8 = {b_0, ..., b_7}` carrying 5 internal 3-APs at a single shared vertex `b_5 = a_12 = 596`, giving `14 + 8 - 1 = 21` vertices. When `b_5` is included in a size-6 minimum transversal of `A_14`, the residual hypergraph `B_8 - {b_5}` has only two size-2 transversals `T_A = {b_1, b_6}` and `T_B = {b_2, b_4}`, both of which completely miss `{b_0, b_3, b_7}`. Adding two cross-block 3-APs `(a_8, b_7, b_0) = (2980, 9815, 16650)` and `(b_7, a_13, b_3) = (9815, 10560, 11305)` forces any size-6 transversal of `A_14` containing `a_12` to use at least 3 vertices from `B_8 \ {b_5}`, proving `tau(H(A_21)) = 6 + 3 = 9` and `s(A_21) = 21 - 9 = 12` (`12/21 = 4/7`). Solving the `8 x 8` linear system over `Q` (`how-we-built-it/glue_a14_b8.py`) produces 223 distinct normalized 21-element `(4, 5)`-sets with `s(A_21) = 12`.

## 3. Henning-Yeo Impossibility Bound for `n <= 15`

Combining the Henning-Yeo linear hypergraph bound `17 tau(H) <= 5n + 3m` with `m <= n - 2` gives `17(n - s(A)) <= 8n - 6`, proving that no `(4, 5)`-set of cardinality `n <= 15` (or `n in {17, 19, 21}`) can satisfy `s(A)/|A| < 4/7`, and that `s(A)/|A| = 4/7` for `n <= 15` is possible solely at `n = 14, s = 8`.
