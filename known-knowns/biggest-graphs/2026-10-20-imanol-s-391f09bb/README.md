# (13,4) degree-diameter graph on 6 631 vertices

## What

The submitted 6 631-vertex edge list is a simple, connected undirected graph with maximum degree 13 and diameter exactly 4, strictly larger than the live Comellas (13,4) cell of 6 615 (re-fetched 2026-10-20) and than the repo's 6 630-vertex trophy, and below the Moore bound of 24 506.

## Check it yourself

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (about 20-30 s on one laptop core). It rebuilds the adjacency from
`object/G_13_4_n6631.edges`, asserts simplicity, checks the maximum degree, and runs an
all-pairs BFS from every one of the 6 631 vertices. `verify-it-yourself/RECEIPTS.md` has the real
output of the same script.

## Compared to

- Comellas, *Table of the largest known (Delta,D)-graphs*,
  https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, fetched
  2026-10-20T19:06:44Z with one plain GET (HTTP 200, sha256 of the page
  `69486132bac2b05e2f911cc290382eb79c282c219b6d1e70176fafd44ed8804f`). Row `13`, column `4`
  (the table's D columns start at 2) reads `6 615`; the cell is not boldface, so the entry is
  not proven optimal.
- This repo's shipped trophy graph for the same cell has 6 630 vertices
  (`known-knowns/biggest-graphs/graphs/G_13_4_n6630.edges`, re-counted in the panel). The
  submitted graph is one vertex larger and its edge set is not the trophy plus a pendant vertex.
- Moore bound for (13,4): 1 + 13 + 156 + 1 872 + 22 464 = 24 506.

## Not claimed

- Nothing about optimality. 6 631 is far below the Moore bound.
- Nothing about any other cell of the table.
- Nothing about literature beyond the checks recorded in `panel/novelty.md` (Comellas table,
  the repo's trophy case and open pull requests, and a search of the last 24 months).

## Credits

- Francesc Comellas, *Table of the largest known (Delta,D)-graphs*, for the table this cell is
  compared against.
- The holders listed around this cell: D. Yugeswardeenoo (current 6 615 entry, Oct 2026) and
  R. Rajiv (Zenodo 10.5281/zenodo.23052995, the seed graph Q9(T4)++ and surgery behind the
  shipped 6 630-vertex graph this work extends; CC BY 4.0).
- N. Bhakar, P. Isufi and the other holders named on the page's colour legend, whose entries
  define the neighbourhood of this cell.
- The V3R1T4S trophy family `known-knowns/biggest-graphs/` for the 6 630-vertex baseline graph,
  which is the input of this construction.
- numpy and scipy (BSD) for the search and the second checker; the shipped checker is pure
  Python standard library.
