# Independent novelty verdict: (14,4), order 8425

Context: fresh headless opencode run --standalone (role novelty), as specified by the assignment. Work was confined to this directory and read-only public requests; no other skeptic verdicts, parent research, author checker, subagents, submissions, or claim modifications were used.

## Object and independent verification

Object: `claim/G_14_4_n8425.edges`. Exact SHA256: `8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7`.

My independently written and executed `check_graph.py` rejects loops, negative labels, repeated undirected edges and noncontiguous labels; constructs the symmetric adjacency matrix; and runs complete breadth-first search from every vertex, deriving distances from BFS predecessors. This is not sampling. Results in `graph.log` and `evidence/graph_result.json`: 8425 vertices, 58971 edges, minimum degree 13, maximum degree 14, all 8425 roots checked, zero disconnected ordered pairs, zero ordered pairs at distance greater than four, and exact diameter 4. The general Moore upper bound is 33321. Thus the submitted simple undirected graph satisfies the target cell and does not violate that bound.

Reproduce the graph check with the supplied environment:

```bash
../../../../.venv/bin/python check_graph.py
```

## Primary table: one fetch only

- URL: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
- Request UTC: `2026-10-20T22:37:57.540474+00:00`.
- HTTP status: **200**; no block and no retry.
- Saved response bytes: `evidence/primary.html`; receipt: `evidence/primary.html.meta.json`.
- Response SHA256: `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`.
- Live cell **(14,4) = 8303; bold: false**.

My executed `parse_table.py` parses the saved HTML cells and bold tags rather than relying on a search snippet. The header gives diameters 2 through 10; the row labelled 14 has 8303 in its diameter-4 column. Parsed evidence is in `evidence/table_rows.json`, `evidence/live_cell.json`, and `table_parse.log`. The page explicitly warns that it is being updated, so its value is not treated as a complete novelty certificate. The candidate exceeds this live value by 122.

## Upstream trophy and open pull requests

Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md at `2026-10-20T22:39:18.231491+00:00`, HTTP 200. Saved `evidence/TROPHY_CASE.md`, SHA256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`. Its same-cell entry is **8424**, crediting the Bhakar controller/affine-lift construction. The candidate exceeds that stronger benchmark by **one vertex**; this is not a tie. Other degree/diameter cells are not competitors.

Fetched the live GitHub API open-PR listing, including full body fields, from `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1` and pages 2 and 3. All returned HTTP 200 between `22:39:18` and `22:39:21` UTC; page sizes were 100, 100, and 85. All **285** full title/body records were saved in `evidence/open_prs_full.json`; individual responses and metadata are retained, with receipts in `upstream.log`.

My executed `audit_novelty.py` searched all these full titles and bodies for degree-diameter terminology, the target cell and competing orders. The selected full records are retained in `evidence/selected_pr_full.json`. The graph claims found were PR #598, **(13,4), 6631**, and PR #457, **(14,3), 1118**: neither is this cell. No same-cell result reaching 8425 was found in that search. This was keyword screening of full bodies, not a claim to have inspected every linked artifact or comment.

## Independent recent-literature search

Window: **2024-10-20 through 2026-10-20**. An initial arXiv degree-diameter search and a broader title/abstract search were executed independently. The broader query was `(ti:degree OR abs:degree) AND (ti:diameter OR abs:diameter) AND cat:math.CO`, restricted to that submission-date window. It returned **81 total entries**, all within the requested maximum of 100, with no result-page truncation. Saved source: `evidence/literature_broad.xml`; receipt and exact URL: `literature_fetch.log`; titles/abstracts and screening output: `novelty_audit.log`. No same-cell construction of order at least 8425 was located.

The three supplied leads were fetched directly as paper HTML and examined, not accepted from claim notes:

- https://arxiv.org/html/2606.15860: the relevant improved examples concern **(12,5)** and **(16,5)**, not (14,4).
- https://arxiv.org/html/2608.27253: the examined generalized-polygon construction families give diameters **2, 3, and 5**, and the highlighted finite improvements concern diameter 3. No qualifying (14,4) example was located.
- https://arxiv.org/html/2608.03965: an asymptotic Moore-bound result is not itself a finite degree-14 construction. For its explicit Proposition 3.1 family with diameter parameter 4, the smallest field size gives order **125687642325**, already greater than the degree-14 diameter-4 Moore bound 33321; larger field sizes increase that order. Hence this diameter-4 family cannot have maximum degree at most 14. This comparison is computed in `audit_novelty.py`; it does not mistake an upper bound on degree for a lower bound. No finite qualifying example was found elsewhere in the examined result.

Also followed the search hit https://arxiv.org/html/2606.10954, saved as `evidence/cayley.html` and extracted to `evidence/cayley.txt`. Its listed examples concern degrees 3–13 and alternative non-isomorphic optimal Cayley graphs, not a degree-14 diameter-4 improvement. Saved HTML, extraction code and fetch receipts for all leads are retained locally.

## Scope and decision

This is a bounded, time-stamped novelty search, not a proof that no larger graph exists. The arXiv queries can miss different terminology, categories, older papers updated within the window, non-arXiv publications, and unpublished or unindexed constructions. Full-paper examination concentrated on the supplied leads and relevant search hits rather than all 81 papers. The PR audit excludes comments, attachments, linked repositories and closed PRs; pagination is a live snapshot rather than an atomic archive. Algebraic families were not exhaustively optimized over every parameter. The table's update warning and the already stronger trophy entry demonstrate why table comparison alone would be insufficient.

Within those explicit limits, the complete graph check succeeded, 8425 strictly exceeds both the fetched nonbold 8303 cell and pinned/live trophy 8424, and the independent recent-literature and live-open-PR searches found no known same-cell tie or superior result. This passes the requested bounded novelty check, not an optimality claim.

pass: true
