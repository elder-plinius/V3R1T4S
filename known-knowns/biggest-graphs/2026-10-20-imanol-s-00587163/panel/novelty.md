# Independent novelty verdict

Context: fresh headless opencode run --standalone (role novelty).

The submitted object `claim/object/G_13_4_n6637.edges` has exact SHA-256 `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059`.

## Actual object checks

Independent code `check_graph.py` parsed the actual edge list, rejected loops and repeated undirected edges, checked every label 0 through 6636, and performed BFS from **all 6637 roots**. Result: 6637 vertices, 43140 edges, minimum degree 12, maximum degree 13, connected, exact diameter 4 (every root has eccentricity 4). Order is below the Moore bound 24506. Runtime was 5.358 seconds, completed 2026-10-20T21:28:13.413610Z. Results: `graph_result.json`, `graph_check.log`.

## Live primary table: fetched exactly once

- URL: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
- UTC fetch start: **2026-10-20T21:27:55.146458Z**.
- HTTP status: **200**; 47382 bytes saved unchanged in `evidence/primary.bytes`.
- SHA-256: `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`.
- Actual live **(13,4) value: 6615; nonbold** (no bold markup in the cell).

`investigate.py` parsed HTML rows/cells, preserving markup; `summarize.py` selected degree row `13` and located diameter `4` through the actual header. Diameter columns start at 2, so the selected cell is index 3, not index 4. Evidence: `evidence/table_rows.json`, `evidence/cell.json`. The candidate strictly exceeds this cell by 22. No second primary-table fetch or access workaround occurred.

## Upstream and literature checks

Read-only live requests fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md (HTTP 200, 2026-10-20T21:27:56.115764Z; SHA-256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`). Its (13,4) trophy is **6630**, seven fewer than the candidate; other cells are not comparators.

Fetched https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 and pages 2 and 3, all HTTP 200, covering **284 open PRs** (100 + 100 + 84). Searched their titles and bodies; the relevant same-cell PR is **598, 6631 vertices**, also fetched directly at https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/598. This is a known baseline, not a new result here. Candidate improves it by **6**, not a tie. PR457 concerns (14,3), not (13,4). Raw JSON and selected text are retained in `evidence/open_prs*.bytes`, `evidence/pr598.bytes`, and `evidence/all_graph_prs.json`.

Independently queried the arXiv export API for `"degree diameter"` and submission dates **2024-10-20 through 2026-10-20**, newest first, limit 100; HTTP 200 returned 16 entries. Actual query URL, fetch times, statuses and hashes are in `evidence/receipts.jsonl`; raw feed and parsed abstracts are `evidence/literature.bytes` and `evidence/literature.txt`. Results included irrelevant astronomy and mixed/directed/planar graph papers; those are not same-cell records. Separately fetched abstract and full HTML pages for all three supplied leads, all HTTP 200:

- https://arxiv.org/abs/2606.15860 and https://arxiv.org/html/2606.15860: highlighted improvements concern **(12,5)** and **(16,5)**, not a 6637-or-larger (13,4) record.
- https://arxiv.org/abs/2608.27253 and https://arxiv.org/html/2608.27253: new families have diameters **2, 3 and 5**, with highlighted finite records at diameter 3; not this diameter-4 cell.
- https://arxiv.org/abs/2608.03965 and https://arxiv.org/html/2608.03965: asymptotic partial-flag construction is not a degree-13 record. Its equation (6) gives order `[2k+1]_q!/(q+1)^k`. At k=4 and the smallest prime power q=2, the order is **125687642325**, already above the (13,4) Moore bound 24506; order increases with q. Thus these H_(4,q) graphs cannot have maximum degree at most 13. Independently executed arithmetic: `literature_check.py`, `evidence/literature_check.json`.

Full fetched paper bytes and extracted text are saved as `evidence/full_*.bytes` and `evidence/full_*.txt`. No checked source establishes a (13,4) result reaching or exceeding 6637.

## Limitations and disposition

This is a time-stamped strict improvement over the checked known results, not a proof of optimality or an exhaustive guarantee about all unpublished work. The literature search is bounded by arXiv indexing and one query; the Kronecker lead was checked separately rather than relying on its appearance in that feed. Google search returned HTTP 200 but only a JavaScript challenge, not usable results; no retry or bypass was attempted, and it supplies no positive evidence. PR searches cover titles/bodies, not every attached artifact or discussion. Baseline PR598 and trophy claims were treated conservatively as known bounds without revalidating their graph objects.

All required primary/upstream sources were accessible. The new graph is independently valid and strictly exceeds 6615, 6630, and 6631. Execution commands and timing receipts: `COMMANDS.md`, `investigation.log`, `followup.log`, `extract.log`, and `evidence/receipts.jsonl`. No claim files were modified; no outward write actions or subagents were used.

pass: true
