# Pre-registration (degree-diameter-table)

- **Target ID**: `degree-diameter-table` (`graphs-games-automata`)
- **Target cell**: $(\Delta, D) = (14, 3)$
- **Live Comellas baseline**: $N = 1,116$ (`Dhar_1116`, not boldface; Moore bound $M(14, 3) = 2,563$)
- **V3R1T4S `TROPHY_CASE.md` baseline**: $N = 1,117$ (`G_14_3_N1117.edges`, PR #143)
- **Hypothesis & Method**: `G_14_3_N1117.edges` has 68 vertices of degree 13 (and 84 free degree slots after pruning 8 redundant edges). Attaching vertex 1117 to 14 free-slot vertices and running bit-parallel BFS simulated annealing with new-vertex screen inclusion and multi-temperature polish rounds will eliminate all vertex pairs at distance $> 3$, yielding a valid $(\Delta, D) = (14, 3)$ graph on $N = 1,118$ vertices.
- **Verification**: Deterministic all-pairs BFS from all $N = 1,118$ vertices (`verify-it-yourself/check_dd.py`) confirming simple undirected graph, maximum degree $\le 14$, connected, exact diameter $3$, and $N = 1,118 > 1,117 > 1,116$.
