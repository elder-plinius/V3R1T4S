# REPRODUCE verdict — degree-diameter-table, cell (13,4)

context: subagent

## Definition used (quoted from `claim.md`, "Success criterion")

> (1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

Claim: N = 6 631, Delta = 13, D = 4, `object/G_13_4_n6631.edges`, 43 099 edges, 0-based labels 0..6630.

## Method

Before reading `checkers/ddcheck.py` or `checkers/verify_scipy.py`, I wrote two checkers from the definition above:

- `../panel/reproduce_checker.py` — strict parser (one `#` header, every other line exactly two ints), vertex-set check `labels == {0..6630}`, self-loop/multiedge check, max degree, union-find connectivity, and **exact all-pairs BFS by bitset frontier from every one of the 6631 sources, capped at depth 4** (a source fails if any vertex is not in `seen` after 4 layers, so distance > 4 and disconnection are both caught).
- `../panel/reproduce_crosscheck.py` — independent second path: scipy `shortest_path(unweighted=True, directed=False)` for the exact diameter, plus a from-scratch HTML parse of `table/table_claim.html` that locates the row labelled `13`, the column headed `4`, and tests the cell for boldface markup.

## Output — my checker (`../panel/reproduce_checker.py object/G_13_4_n6631.edges 13 4 6631 43099`)

```
header_lines=1 first='# (13,4) N=6631 cost=0; sa2_resume seed 43 from sa_pivot_s34_c57.edges'
n=6631 claim_n=6631 label_min=0 label_max=6630 labels_in_range=True labels_cover_0..n-1=True
edges=43099 claim_edges=43099 self_loops=0 duplicate_undirected_edges=0
maxdeg=13 mindeg=11 claim_delta=13 n_deg_eq_delta=6627 maxdeg_ok=True
components=1
diameter_bound=4 observed_max_within_cap=4 sources_with_distance_eq_4=6631 sources_unreached_within_cap=0
moore_bound(delta=13,D=4)=24506 n<=moore=True
VALID
```

Runtime 6.5 s, all 6631 sources searched (not a sample).

## Output — independent scipy + table parse (`../panel/reproduce_crosscheck.py object/G_13_4_n6631.edges 6631`)

```
scipy_n=6631 edges=43099 max_degree=13
scipy_all_finite=True scipy_diameter=4 n_pairs_at_diameter=32202882
scipy_VALID
table_header=['&Delta; &nbsp; \\ D&nbsp;', '2', '3', '4', '5', '6', '7', '8', '9', '10']
table_row_13_cells=[('162', False), ('873', False), ('6 615', False), ('&lowast;  51 417', False), ('535 302', False), ('&lowast; 3 691 038', False), ('&lowast; 36 275 160', False), ('&lowast; 362 492 640', False), ('&lowast; 3 789 298 110', False)]
table_cell_13_4='6 615' value=6615 bold=False
table_matches_claim(6615)=True
moore=24506
```

Two structurally different algorithms agree: diameter exactly 4, connected, max degree 13.

## Property-by-property re-derivation

| # | Property | Evidence | Result |
|---|---|---|---|
| 1 | Explicit simple undirected graph, N = 6631 | 43 099 unique unordered pairs, 0 self-loops, 0 duplicate (either orientation), labels exactly `{0..6630}`, 1 header line | holds |
| 2 | max degree <= 13 | max degree 13, min 11, histogram `[(11,1),(12,3),(13,6627)]`; `sum(deg) = 86198 = 2*43099` | holds |
| 3 | connected, diameter <= 4 | union-find: 1 component; bitset BFS from all 6631 sources reaches all vertices within 4; scipy diameter = 4 | holds |
| 4 | N > live table (13,4) cell | saved page row `13`, col `4` reads `6 615`, not bold (detector independently fires on 7 other bold cells: 10, 20, 38, 15, …); 6631 > 6615 | holds |
| 5 | N <= Moore bound | 1+13+13·12+13·12²+13·12³ = 24506; 6631 <= 24506 | holds |

`table_claim.html` has exactly one table and exactly one row labelled `13`, so the cell lookup is unambiguous; it references the 2026 Mendeley/arXiv releases and states "Updates: September 2026", consistent with the claimed fetch date.

## Integrity and determinism

- sha256 `object/G_13_4_n6631.edges` = `391f09bb6f72f16ca5b867694b96d1d1ca31569c8974ba0f0ef00099c6cd5cbe` — matches `claim.md`.
- sha256 `table/table_claim.html` = `69486132bac2b05e2f911cc290382eb79c282c219b6d1e70176fafd44ed8804f` — matches `claim.md`.
- Two consecutive runs of my checker produced byte-identical output (`diff` empty): deterministic.
- Edge lines shuffled with seed 7 (a shuffled copy of the edge list): same verdict `VALID`, same degrees and diameter — the result does not depend on file order.
- Author's own checkers, run after mine, agree with my numbers: `ddcheck.py` → `VALID n=6631 maxdeg=13 diameter=4 edges=43099 moore=24506` (17.3 s) and `verify_scipy.py` (under the project venv, which is the interpreter that has scipy) → `VALID n=6631 maxdeg=13 diameter=4 edges=43099`.

## Caveats (none affecting the verdict)

- Criterion (4)'s "re-fetched immediately before claiming" cannot be re-verified offline: only the saved page exists in the package, and no HTTP headers were stored. The saved artifact is consistent with the claim and hashes as stated, but live-table freshness is unproven here.
- The repo-trophy comparison (N > 6 630) points to `repo/known-knowns/...`, which is outside this package and was not read; it is supporting context, not part of the success criterion, and criterion (4) is already met against 6 615.
- `REPRODUCE.md`'s `python3 checkers/verify_scipy.py` fails under system `python3` (no scipy); it runs under the project venv (scipy 1.18.1). Documentation nit only.
- Nothing here speaks to optimality (6 631 << 24 506), which the claim does not assert.

All five success criteria reproduced from the saved files with an independently written exact check.

pass: true
