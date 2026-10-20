# Novelty verdict - degree-diameter-table, cell (13,4)

context: subagent

## Live status check (one GET, no retries)

- URL: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
- Fetched once with plain `curl` at 2026-10-20T19:07:30Z (finished 19:07:31Z); HTTP 200, 47 382 bytes.
- sha256 `69486132bac2b05e2f911cc290382eb79c282c219b6d1e70176fafd44ed8804f` - byte-identical to `claim/table/table_claim.html`, so the claim's snapshot and the live page agree.
- Cell (row `13`, fourth data column = D 4; columns start at D=2: 162, 873, 6 615, ...): **`6 615`**, not boldface, linked to `desc_g/desc_g4.html#134`.
- Independent mirror, same reading: Wikipedia "Table of the largest known graphs of a given diameter and maximal degree" (as of 14 Oct 2026; last edited 20 Oct 2026 01:11 UTC) gives (13,4) = 6 615. CombinatoricsWiki is stale at 6 560.

## Bars compared

| source | (13,4) order | note |
|---|---|---|
| live Comellas table (fetched above) | 6 615 | current holder D. Yugeswardeenoo, Oct 2026 |
| Wikipedia mirror | 6 615 | as of 14 Oct 2026 |
| `repo/TROPHY_CASE.md` row 5 | 6 630 | `repo/known-knowns/biggest-graphs/graphs/G_13_4_n6630.edges`; re-counted here: 6 630 distinct vertices (0..6629), 43 086 edges, max degree 13 |
| claimed object | 6 631 | `claim/object/G_13_4_n6631.edges` |

Literature, last 24 months: the (13,4) lineage is Rajiv 6 611 (Zenodo 10.5281/zenodo.23052995) -> Yugeswardeenoo 6 615 (table, Oct 2026) -> repo trophy 6 630. No paper, preprint, Zenodo entry, wiki or table found that states 6 631 or more for (13,4). Searches for "degree-diameter (13,4) 6615/6630/6631", the 2026 arXiv/Mizuno/Comellas work and the general degree-diameter tables returned nothing at or above 6 631.

Open pull requests (`gh`, repo `elder-plinius/V3R1T4S`): the only degree-diameter PRs are (14,3) submissions - open draft #457 (N = 1 118), merged #143 and closed #60 (N = 1 117). No (13,4) PR, no PR or issue mentioning "6631", and the live GitHub tree of `known-knowns/biggest-graphs/graphs/` contains `G_13_4_n6630.edges` but no 6 631 file. Nobody else has banked this order.

## Object sanity for N (novelty only)

- 6 631 distinct vertices, labels 0..6630, 43 099 edges, no loops, no duplicate pairs, no isolated vertex; degree histogram {11: 1, 12: 3, 13: 6 627}; single BFS from vertex 0 reaches all 6 631 vertices (connected).
- So N = 6 631 is an actual graph order, not a label artefact. Diameter <= 4 is the correctness panel's lane and is not re-proved here.

## Conclusion

6 631 strictly exceeds both the live table cell (6 615, +16) and the repo's own trophy graph (6 630, +1). It is not a tie with anything known, so it is a record by the stated criterion. The margin over the repo trophy is only one vertex and would be erased by any 6 632+ result, but no such result exists in the sources checked.

pass: true
