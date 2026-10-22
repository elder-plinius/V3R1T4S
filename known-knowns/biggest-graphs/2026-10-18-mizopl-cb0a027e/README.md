# Degree-diameter graph (14, 3) on 1,118 vertices

## What

An explicit simple undirected graph claim/G_14_3_N1118.edges (62,588 bytes, sha256 cb0a027e53b8282181df4754acb15797d7f954ed518967af6ecda9193a2a85c0) on N = 1,118 vertices with 7,809 edges and maximum degree 14 (34 vertices of degree 13 and 1,084 of degree 14), verified by independent all-pairs BFS to be connected with exact diameter 3 and order at most the Moore bound 2,563, strictly exceeding the live non-boldface (14, 3) record of 1,116 on the Comellas general-graph table by 2 vertices and the previous 1,117-vertex graph claim/G_14_3_N1117.edges by 1 vertex.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/G_14_3_N1118.edges`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1 second.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---:|---:|---|---|
| Comellas, *The degree/diameter problem for general graphs* (table; Last-Modified Sun, 18 Oct 2026 12:43:23 GMT) | (Delta, D) = (14, 3) | 1116, not boldface (not proved optimal) | 1118 | https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html | 2026-10-18T19:01:55Z |
| Comellas, D = 3 description page | Dhar_1116 | order 1116, D. Yugeswardeenoo, 7 October 2026 | 1118 | https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html | 2026-10-18T19:01:55Z |
| V3R1T4S `TROPHY_CASE.md` (PR #143) | (14, 3) | 1117 (`G_14_3_N1117.edges`) | 1118 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-18T19:01:55Z |
| Moore bound 1 + 14 + 14*13 + 14*13^2 | (14, 3) | 2563 | 1118 | | |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed. The Moore bound is 2563.
- No symmetry is claimed. The graph is not claimed to be vertex-transitive or a Cayley graph.
- The margin is two vertices over the live Comellas table (1116) and one vertex over the previous V3R1T4S record (1117). Most of its structure builds on the earlier authors' work.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Dharunish Yugeswardeenoo**, the (14, 3) graph Dhar_1116 (7 October 2026), listed on the Comellas D = 3 page: https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html.
- **R. Rajiv**, the 1088-vertex (14, 3) graph that Dhar_1116 extends.
- **Francesc Comellas**, the degree/diameter table compared against: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html.
- **V3R1T4S PR #143** (`anonymous-c6d1e0ab`), the 1117-vertex (14, 3) graph `G_14_3_N1117.edges` extended here.
- Contributor credit: `mizopl`.
