# Frozen 2026-10-20T19:31:31.844088+00:00

{
  "id": "degree-diameter-table",
  "name": "New largest known (Delta,D) graph in the degree-diameter table",
  "category": "graphs-games-automata",
  "kind": "harvest",
  "tractability": 3.5,
  "compute_profile": "laptop-hours",
  "statement": "For maximum degree \u0394 and diameter D, find a graph with more vertices than the current entry in the Comellas degree-diameter table. The table covers degree up to 20 and diameter up to 10.",
  "success_criterion": "(1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.",
  "partial_wins": [
    {
      "id": "p1",
      "statement": "A graph satisfying (1)-(3) with N strictly greater than the (Delta,D) entry in a table snapshot whose fetch time and SHA-256 were recorded BEFORE the search started, but which was overtaken by another group's update logged on the live table after that snapshot (independent collision); the skeptic checks the graph, the snapshot hash and the update-log date."
    },
    {
      "id": "p2",
      "statement": "A graph strictly beating the live entry of a separately maintained special-class degree-diameter table (bipartite, Cayley or circulant), verified with the same exact degree/diameter checker plus the class property (bipartition, or Cayley group and generators reproducing the edge set), compared against that table's live page."
    }
  ],
  "verification_method": "Load the graph with scipy.sparse. Assert it is symmetric with no loops and no multi-edges, and check the degree array. Run BFS from every vertex: multi-source frontier bitsets in numpy work up to about 2e5 vertices. For Cayley graphs, regenerate the edge set from the stated group and generators, check it equals the submitted list, and then run one BFS. Compare N with the live HTML table. Also confirm N is at most the Moore bound.",
  "primary_sources": [
    "https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html",
    "https://en.wikipedia.org/wiki/Table_of_the_largest_known_graphs_of_a_given_diameter_and_maximal_degree",
    "https://arxiv.org/pdf/2608.27253",
    "https://arxiv.org/abs/2608.03965"
  ],
  "status_source": "https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html",
  "status_checked": "2026-10-03",
  "disclosure": "open",
  "angles": [
    "Voltage-graph lifts: choose a small base graph (Petersen, Hoffman-Singleton, or the record graphs for (\u0394, D-1)) and anneal voltage assignments over Z_n, Z_n x Z_m, or metacyclic groups, scoring by the number of vertex pairs at distance greater than D in the lift. Base graph plus group gives a fast BFS on the quotient.",
    "Cayley graphs of semidirect products Z_m \u22ca_r Z_n with generator sets chosen by SA. Many of the 2026 entries are Cayley graphs, marked with an asterisk in the table.",
    "Polarity-quotient and Kronecker-product constructions (arXiv 2608.27253): apply them systematically to every table entry to propagate the recent improvements to neighbouring (\u0394,D).",
    "G\u00f3mez-style compound graphs: replace vertices of a large diameter-(D-2) graph with copies of a small graph and rewire. Use the fresh 2026 records as seeds.",
    "Target the entries updated least recently. Large-D, small-\u0394 entries got fewer 2026 updates than (\u0394,3), (\u0394,4), (\u0394,5).",
    "Seed voltage-lift and Kronecker/polarity searches with the partial-flag graphs H_{k,q} of arXiv 2608.03965, after checking whether they already appear in the table."
  ],
  "pitfalls": [
    "The table is updated almost daily. A claim must beat the value shown at verification time, not the value at search start.",
    "Diameter computed on the quotient or base graph instead of the actual lift.",
    "Multi-edges or loops in voltage lifts silently reduce the true degree count.",
    "Degree-diameter problems for special classes (bipartite, Cayley-only, circulant) have separate tables. Only the general-graph table counts here.",
    "Boldface entries such as (3,2), (3,3), (3,4) and (4,2) are proven optimal. Beating one means there is a bug.",
    "More than 15 independent groups updated the table in August to October 2026. Timestamp claims and re-fetch the table just before claiming.",
    "arXiv 2608.03965 (partial-flag graphs H_{k,q}, asymptotically attaining the Moore bound) is a new seed family. Its graphs may already be in the table."
  ]
}

Checker: exact all-pairs reachability/BFS, simple undirected edges, max degree within the cell, diameter at most the cell diameter, and N within Moore bound. For (13,4), N must exceed 6631 (already submitted), not merely 6630 or 6615. Other cells must exceed both the live table and shipped trophy. No search cap or greedy cover failure proves impossibility.

null_test: not needed because claims concern explicit finite graphs checked deterministically, not statistical superiority or chance.

No confirmation without three fresh-context skeptics and orchestrator reading their verdicts. No outward actions. Search stops starting new work after 80% of three-hour wall budget; final interval reserved for verification/report.
