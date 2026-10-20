# Criterion verdict - degree-diameter-table, cell (13,4)

context: subagent

## Criterion, verbatim (`claim/claim.md`, from `repo/bank/targets.json`)

> (1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

Claim under test: Delta = 13, D = 4, N = 6 631, object `claim/object/G_13_4_n6631.edges`.

## Clause by clause

| # | Clause | Evidence (independently run here) | Verdict |
|---|---|---|---|
| 1 | Explicit simple undirected N-vertex graph | 43 099 lines parsed as pairs; labels cover exactly `{0..6630}`, so N = 6631 (not a max-label artefact); 0 self-loops; 0 duplicate unordered pairs; degree sum 86 198 = 2 x 43 099; sha256 `391f09bb...cd5cbe` matches the claim | holds |
| 2 | max degree <= 13 | degree histogram `{11:1, 12:3, 13:6627}`, max 13 | holds |
| 3 | connected, diameter <= 4 | `claim/checkers/ddcheck.py` (all-pairs BFS, asserts each source reaches all 6631): `VALID n=6631 maxdeg=13 diameter=4 edges=43099 moore=24506`, 17.6 s. Independent bitset BFS from all 6 631 sources: diameter 4, eccentricity histogram `{4: 6631}`, no unreached vertex. Third spot check (dict BFS, 200 random sources): every source reaches all 6631 within 4 | holds |
| 4 | N > live table cell | Live page re-fetched 2026-10-20: row `13`, column `4` (columns start at D=2) reads `6 615`, linked to `desc_g/desc_g4.html#134`, no `<b>` and no `&lowast;` in the cell. Cell is 6615, so 6631 > 6615 (+16). The description page independently lists `Q9(T4)++ ... Order= 6615` (Yugeswardeenoo, Oct 7 2026). No 6630/6631 value appears anywhere on either page | holds |
| 5 | N <= Moore bound | 1 + 13 + 13*12 + 13*12^2 + 13*12^3 = 1 + 13 + 156 + 1 872 + 22 464 = 24 506 >= 6 631. Cell is not boldface (not proven optimal), so no contradiction | holds |

Neither enumerated partial win fits: p1 (snapshot overtaken by an independent collision) does not apply because the live cell is unchanged at 6 615 and no competing update is logged; p2 (special-class table) does not apply because this is the general-graph table. The full criterion is met, so this would be a full win, not a partial one.

## Hidden quantifiers and null models

- Vertex-set trap: `ddcheck.py` derives n = 1 + max endpoint, so a missing vertex above the largest used label or an isolated tail would be silently absorbed into n. Checked: all labels 0..6630 are present, min degree 11, and BFS from every source reaches all 6631, so N is real and the graph is connected.
- Simplicity: checked unordered duplicates and both orientations; no loops. The edge list is an explicit representation from which adjacency is immediate; `targets.json` itself expects the graph to be loaded from an edge list, so "adjacency list" is not being stretched.
- Diameter direction: diameter is exactly 4, not "<= 4 by default"; the all-pairs BFS asserts every pair is reached and caps eccentricity at 4.
- Table reading: exactly one table and one row labelled `13`; the header is `D = 2..10`, so the fourth data column is D = 4. The linked description page corroborates 6615. The cell has no bold markup and no Cayley star, so clause (5)'s "beating boldface signals a bug" alarm does not fire.
- Null model on novelty: the repo's own trophy `repo/known-knowns/biggest-graphs/graphs/G_13_4_n6630.edges` re-counts to 6 630 distinct vertices, 43 086 edges, max degree 13, connected, diameter 4. The submitted graph is a genuine order larger (6 631, +1), and its edge set is not the trophy plus a pendant vertex (the induced edges on the trophy's vertex set differ in 594 positions; degree histograms differ), so the win is not subsumed by the internal baseline. The margin is thin, but the criterion is a strict inequality with no minimum margin.
- Prior 6631 artifacts in this run are invalid (costs 268, 190, 162, 141, 129, 116, 95, 57); the shipped object is byte-identical to the only cost-0 artifact, `attempts/constructor/state/sa57_s43_c0.edges`, whose log line records `seed 43: sa2 best 0 ... VALID N=6631`. Not a duplicate of an earlier valid 6 631 graph.

## Package defect (not a criterion failure)

`claim/checkers/verify_scipy.py` does not run under system `python3` (no scipy) and, read literally, never asserts `diameter <= D`; it only prints the computed diameter. So the REPRODUCE.md description of "two independent checkers" overstates the package. Criterion (3) is still satisfied by the all-pairs BFS in `ddcheck.py`, which this panel re-ran, and by the independent bitset BFS above. `REPRODUCE.md` also correctly disclaims optimality and other cells.

## Narrowest true scope

confirmed_scope: The submitted 6 631-vertex edge list is a simple, connected undirected graph with maximum degree 13 and diameter exactly 4, strictly larger than the live Comellas (13,4) cell of 6 615 (re-fetched 2026-10-20) and than the repo's 6 630-vertex trophy, and below the Moore bound of 24 506.

pass: true
