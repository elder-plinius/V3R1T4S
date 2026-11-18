context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, package 2cf4ffc7

My own checker (written from the definitions, before opening the package code) was run on object/biplanar_9crit_n19_e92.json and object/uncolorable_8.drat. Results:

1. Partition and simplicity: layer 1 has 45 edges, layer 2 has 47, disjoint, union 92 distinct edges on 19 vertices, no loops, no repeats. Degrees 8..12.
2. Euler check on the rotation systems: each rotation lists exactly the neighbours of its layer; face tracing gives F=28 (layer 1) and F=30 (layer 2); V-E+F=2 for both, and both layers are connected, so each embedding is genus 0.
3. Straight-line drawings: integer coordinates, distinct points, exact integer orientation tests; 0 crossings, 0 overlaps and 0 vertex-on-edge incidences in both layers.
4. Second planarity test: networkx 3.2.1 check_planarity is True for both layers (installed in a venv in work-reproduce). The package's own two stdlib planarity checkers also pass.
5. Not 8-colourable: I regenerated the CNF (152 variables, 763 clauses: at-least-one, edge conflicts, and 8 unit clauses fixing the 8-clique [1,2,4,6,7,9,10,16], which I verified is a clique) and ran the supplied drat-trim build against uncolorable_8.drat: "s VERIFIED". Independently, CaDiCaL (python-sat) says UNSAT both with and without the clique symmetry breaking.
6. Given 9-colouring is proper (uses 9 colours).
7. Criticality: all 92 given edge-deletion colourings are proper 8-colourings of G minus that edge (keys match the 92 edges exactly). CaDiCaL independently finds all 92 G-e 8-colourable. So chi=9 and G is edge-critical (9-critical). Also omega=8, alpha=3, node connectivity 5 (networkx).
8. Package command: in a copy of this package in my work folder, sh verify-it-yourself/run_checks.sh gives 7/7 steps and PASS, agreeing with mine.

Non-isomorphism to Boutin-Gethner-Sulanke lists:
- Fetched 2026-11-18T17:32:17Z https://academics.hamilton.edu/mathematics/dboutin/ThicknessTwo.pdf, HTTP 200, sha256 34620ae3e069e5ecd11af64a26c581332132f9e502246b72e079e994b5a76d17 (author-hosted copy of the J. Graph Theory 57(3) paper, 6 pages as served). The journal DOI (https://doi.org/10.1002/jgt.20282, 2026-11-18T17:31:58Z) returned HTTP 403 (Cloudflare), sha256 ba09c77f09cabdcf78e8569586a372e0c7ea3a51ed699b1e6b0fd8610da35e1b; the Sulanke site hep.physics.indiana.edu gave no connection (code 000). A mistaken guessed arXiv id (https://arxiv.org/abs/0707.1004, 200, sha256 59b2410f...) was an unrelated paper; ignore it.
- That paper's lists are: Sulanke's K6+C5 (n=11); 40 new 9-critical thickness-two graphs on 12 through 16 vertices (Section 3.1, figures only); and the Hajós construction (Section 3.2), whose first example is a 21-vertex graph from two Sulanke graphs. Nothing of order 19 is listed, and a Step-One Hajós sum of two 9-critical graphs has at least 21 vertices. My graph has 19 vertices and connectivity 5, so it is non-isomorphic to every graph in that paper by order alone. I did not rebuild the 40 figure graphs or my own canonical hashes of them (they exist only as pictures), so the canonical-labelling comparison in the package was not independently reproduced; the order argument replaces it.
- Caveat: Step Two of the Hajós construction (identifying independent vertices) can reduce order but yields graphs that are not necessarily 9-critical, and the paper lists none. I did not check the Gethner-Sulanke 2009 part two lists, Alalqam or Patil; those belong to novelty review. Also the package's hash file has an entry with n=23 beyond the stated 11..16 range (cosmetic).

confirmed_scope for reproduction: the 19-vertex, 92-edge graph is simple, biplanar (two genus-0 layers with exact straight-line drawings, networkx agreeing), has chromatic number 9 (DRAT proof checked against my own CNF, plus an independent SAT UNSAT), and is edge-critical (all 92 deletions 8-colourable); it is not isomorphic to any graph in the Boutin-Gethner-Sulanke JGT 2008 paper (orders 11-16 and Hajós sums of order 21 or more).

pass: true
