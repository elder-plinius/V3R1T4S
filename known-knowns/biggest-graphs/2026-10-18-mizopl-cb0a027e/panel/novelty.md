# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
problem_id: degree-diameter-table
target_cell: (Delta, D) = (14, 3) (general undirected simple graphs)
claimed_object: claim/G_14_3_N1118.edges (sha256: cb0a027e53b8282181df4754acb15797d7f954ed518967af6ecda9193a2a85c0, 62,588 bytes, 7,809 lines)

## 1. Local Claim Verification

I inspected `claim/CLAIM.md` and `claim/REPRODUCE.md` and verified the SHA-256 digests of the files in `claim/`:
- `cb0a027e53b8282181df4754acb15797d7f954ed518967af6ecda9193a2a85c0  claim/G_14_3_N1118.edges`
- `3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4  claim/G_14_3_N1117.edges`
- `c4f10c84fba76e70289c9c6f5bd10797401c010771a20ee6ac39060acc3964bc  claim/deg14_diam3_n1116_adjlist.txt`
- `331efcebdd0c481de36fc3c94f5322c4d88be76da59063933c783240cc2c2cb6  claim/table_degree_diameter.html`
- `60c903ad4ae5a5c9ae7f9da2b27f40d5b24e08785661815e8d5458bb0073d6ea  claim/author_checker_check_dd.py`

Running `claim/author_checker_check_dd.py` on `claim/G_14_3_N1118.edges` with `--delta 14 --diameter 3 --record 1117` returned:
```text
N=1118 edges=7809 degree histogram=[(13, 34), (14, 1084)] max degree=14 exact diameter=3 (BFS from all 1118 vertices) Moore bound=2563
PASS (Delta,D)=(14,3) N=1118 max_degree=14 diameter=3
```

## 2. Live Primary Table & Description Page (Single Honest GETs, No Retries)

Each primary URL was fetched once using `curl -sS -D ... -A "V3R1T4S-research-agent (honest single fetch)"`:

| Source | URL | UTC Fetch Time | HTTP Status | Last-Modified Header | SHA-256 of Fetched Response | Extracted `(14, 3)` Record |
|---|---|---|---|---|---|---|
| Comellas general-graph table | `https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html` | `2026-10-18T19:01:55Z` | `200 OK` | `Sun, 18 Oct 2026 12:43:23 GMT` | `331efcebdd0c481de36fc3c94f5322c4d88be76da59063933c783240cc2c2cb6` (`47,143` bytes, identical to `claim/table_degree_diameter.html`) | `1 116` (linked to `desc_g/desc_g3.html#143`, prefixed with asterisk `&lowast;`, not boldface, bgColor `#99EF99`) |
| Comellas `D = 3` description page | `https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html` | `2026-10-18T19:01:55Z` | `200 OK` | `Sat, 17 Oct 2026 16:03:48 GMT` | `334eb8d13c8f695c3d0c9b39d3fca685aa90f8cadeb795dcd9b8446834b9f8d5` (`49,521` bytes) | Anchor `#143` (`Dhar_1116`, lines 324–331): `Degree = 14 , Diameter = 3 ; Order = 1116 ; Moore bound= 2563`, obtained by Dharunish Yugeswardeenoo on October 7, 2026 by adding 28 vertices to R. Rajiv's 1,088-vertex `(14, 3)` graph (superseding M. de Messieres's 1,094-vertex graph of October 3, 2026 and R. Rajiv's 1,088-vertex graph of September 30, 2026) |

The live Comellas table value for `(Delta, D) = (14, 3)` is `1,116` (not boldface; Moore bound `2,563`). Our claimed graph `claim/G_14_3_N1118.edges` has order `1,118`, strictly beating the live Comellas table entry `1,116` by `+2` vertices.

## 3. V3R1T4S Repository (`TROPHY_CASE.md`, `biggest-graphs`, and Open Pull Requests)

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 of Fetched Response | Finding for `(14, 3)` |
|---|---|---|---|---|---|
| V3R1T4S `TROPHY_CASE.md` | `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` | `2026-10-18T19:01:55Z` | `200` | `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` | Lists 7 initial `degree-diameter` rows (`(15,4)=13365`, `(15,3)=1620`, `(14,4)=8424`, `(9,4)=1700`, `(13,4)=6630`, `(13,6)=535495`, `(15,6)=1424896`); simultaneously, the merged contributed package from PR #143 in `known-knowns/biggest-graphs/` holds `(14, 3)` at order `1,117` (`sha256: 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4`) |
| V3R1T4S PR #143 metadata & files | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/143` and `.../pulls/143/files` | `2026-10-18T19:03:37Z` and `2026-10-18T19:03:58Z` | `200` | `4e6df32f...` / `60d2e7ab9c6eebf703d120fb2d6e865ccdd8fe3a8f48db38a5cdbd7a91997945` | Merged `2026-10-15T16:33:53Z`: `[claim] degree-diameter-table: (14,3) graph on 1117 vertices beats the table's 1116` (object matches `claim/G_14_3_N1117.edges`, `sha256: 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4`) |
| V3R1T4S `known-knowns/biggest-graphs` directory & `README.md` | `https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/biggest-graphs` and `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/biggest-graphs/README.md` | `2026-10-18T19:04:28Z` and `2026-10-18T19:04:13Z` | `200` | `3e2f1dd8f018c7074de64d3287df9ba120f15f4fdf22a703c7631fd6f5e05725` and `e765a759019f49412122b6a9b85d6785060bfd99b017da0580fcd3d0220eee39` | Only one contributed directory exists in `known-knowns/biggest-graphs/`, namely the PR #143 `(14, 3)` graph of order `1,117` |
| V3R1T4S open pull requests (page 1, 100 PRs) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-18T19:01:56Z` | `200` | `a221d602f6dd26ec61f5fb9d2040b0c5927f7623198634872697edc6ad2e988f` | `0` of `100` open PRs touch `degree-diameter-table` or `(14, 3)` |
| V3R1T4S open pull requests (page 2, 49 PRs) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2` | `2026-10-18T19:02:27Z` | `200` | `4e6df32f7224e5e178335c81cfe1d65ad337d0a56bd31fcd00537e035182876d` | `0` of `49` open PRs touch `degree-diameter-table` or `(14, 3)` (across all `149` open PRs total, zero touch `degree-diameter-table` or `(14, 3)`) |

Our claimed graph `claim/G_14_3_N1118.edges` (`N = 1,118`) strictly beats the V3R1T4S repository's best `(14, 3)` graph (`N = 1,117`, PR #143) by `+1` vertex.

## 4. Literature & External Repository Search (Last 24 Months)

1. **arXiv API (`2026-10-18T19:01:58Z`, HTTP `200`, `sha256: 06fc370a6e43ad2d579859da047e84972d6c6e205a98d1f216b154b24342a963`)**:
   - Query: `https://export.arxiv.org/api/query?search_query=all:%22degree+diameter%22+OR+all:%22degree/diameter%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
   - Inspected all 25 returned preprints (spanning 2022-09 to 2026-08), including `arXiv:2608.12425v1` (*On the Total Regularity of Almost Mixed Moore Graphs*, 2026-08-12), `arXiv:2608.08997v1` (*A proof of the cyclotomic conjecture and the non-existence of almost Moore digraphs*, 2026-08-10), `arXiv:2608.03965v1` (*Asymptotically attaining the Moore bound*, 2026-08-04), `arXiv:2606.15860v1` (Y. Mizuno, *New lower bounds for the degree/diameter problem via interaction with a browser-accessible LLM*, 2026-06-14, covering `(12, 5)` at least `34,992` and `(16, 5)` at least `147,456`), `arXiv:2606.10954v2` (*Non-Isomorphic Optimal Cayley Graphs*, 2026-06-09), and `arXiv:2507.18797v1` (*Largest planar graphs of diameter 3 and fixed maximum degree*, 2025-07-24). None reports a general graph for `(Delta, D) = (14, 3)` of order exceeding `1,116`.
2. **GitHub Repositories Search API (`2026-10-18T19:01:58Z`, HTTP `200`, `sha256: 85be20a98cf80f629043fdb1bff7fb9a9547a882567c094fdcf2f8c476a83960`)**:
   - Query: `https://api.github.com/search/repositories?q=%22degree-diameter%22+OR+%22degree+diameter%22` (`total_count: 15`).
   - Checked the most recently updated repositories (`2026-10-18T05:40:44Z`, `sha256: 4c9f943fe362e1d5a76dea966dae241aae406343225c68666c471775372e2456` for its `README.md` table of 59 graphs, and `2026-10-16T01:15:10Z` for bipartite graphs). For degree `14`, the 59-graph repository lists only `(14, 4)`, `(14, 8)`, `(14, 9)`, and `(14, 10)`—no `(14, 3)` graph is claimed.
   - Unauthenticated GitHub code search (`https://api.github.com/search/code?q=%22G_14_3%22+OR+%22deg14_diam3%22`, `2026-10-18T19:01:59Z`) returned HTTP `401` (`Requires authentication`, `sha256: b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`), and direct inspection of the relevant public repositories above confirmed no `(14, 3)` graph beyond `1,117` (PR #143).
3. **Zenodo & Comellas Lineage**:
   - The `D = 3` description page traces the entire recent `(14, 3)` progression: R. Rajiv (`1,088`, September 30, 2026, `doi:10.5281/zenodo.23052995`), M. de Messieres (`1,094`, October 3, 2026, `doi:10.5281/zenodo.23136968`), and D. Yugeswardeenoo (`Dhar_1116`, `1,116`, October 7, 2026), followed by V3R1T4S PR #143 (`1,117`, merged October 15, 2026).

## 5. Verdict

The claimed graph `claim/G_14_3_N1118.edges` (`N = 1,118`) strictly exceeds the live Comellas general-graph table record (`1,116`, `+2` vertices) and strictly exceeds the V3R1T4S `TROPHY_CASE.md` / PR #143 record (`1,117`, `+1` vertex), with no competing result in open pull requests or the literature. Temporary working files in `panel/novelty_work` have been removed.

pass: true
