# How we found it (contributor text, unverified)

This condenses the agent run's own account. The claim rests only on `object/G_14_3_N1118.edges` and the checker in `verify-it-yourself/`.

1. **Spare degree.** The (14, 3) graph `G_14_3_N1117.edges` (1,117 vertices, 7,785 edges) is not 14-regular: it has 1,049 vertices of degree 14 and 68 of degree 13, plus 8 redundant edges whose removal preserves diameter 3, yielding 84 unused degree slots.
2. **Add one vertex + screen upgrade.** Vertex 1117 was attached to 14 degree-13 vertices, leaving 49 vertex pairs at distance > 3. In `how-we-built-it/sa2_opt.c`, we included the newly inserted vertex in the fast BFS loss screen (`ends[]`) so that moves breaking length-3 paths from vertex 1117 are screened out immediately, and added multi-temperature polish rounds (`T_start in {0.35, 0.18, 0.08}`) whenever the main annealing pass reached `<= 30` bad pairs.
3. **Repair to 0 bad pairs.** Restart 8 (seed 1) reached 13 bad pairs in 6.87s, and polish rounds 0..9 reduced the remaining bad pairs `13 -> 4 -> 2 -> 0`, producing `object/G_14_3_N1118.edges` (7,809 edges, 34 vertices of degree 13, 1,084 of degree 14, exact diameter 3).
