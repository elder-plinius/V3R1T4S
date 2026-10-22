# cage-upper-bounds: [2,7;6]-mixed graph on 184 vertices, below the Table 1 bound 196 (partial win p2)

## What

Under the forward-arc cycle convention that the source paper's table uses, the object is a connected [2,7;6]-mixed graph on 184 vertices (every vertex 7 edges, 2 in-arcs, 2 out-arcs, girth exactly 6), which is a partial win p2 against the listed upper bound 196 for [2,7;6] in arXiv 2506.20003 Table 1, and not a cage record.

The object is `object/mixed_z2_r7_g6_N184.json` (sha256 fc561db7e3e7b50619bb4b6e8673994ad0192d582bab9c29a40ba7b2769cd00b). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 3 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| arXiv:2506.20003, Table 1 (New upper bounds on the order of mixed cages of girth 6) | [2,7;6] upper bound | 196 | **184** | https://arxiv.org/html/2506.20003 | 2026-10-19T05:27:04Z |
| arXiv:2506.20003, Table 1, lower bound (starred: conditional on a conjecture) | [2,7;6] lower bound | 123* | 184 is above it | https://arxiv.org/html/2506.20003 | 2026-10-19T05:27:04Z |
| arXiv:2401.14768, On Mixed Cages of Girth 6 (source of the 196 entry for [2,7;6]; checked for newer values) | [2,7;6] | no newer value | **184** | https://arxiv.org/html/2401.14768 | 2026-10-19T05:33:30Z |
| arXiv:2610.14110, New mixed cages, bounds and computational results (newest mixed-cage paper found; girth 3 and 4, no girth 6 entry for these parameters) | [2,7;6] | none | **184** | https://arxiv.org/html/2610.14110 | 2026-10-19T05:32:54Z |
| Contributor's own closed pull request 102 (same graph), closed unmerged 2026-10-14 | [2,7;6] | n/a (own earlier filing) | **184** | https://github.com/elder-plinius/V3R1T4S/pull/102 | 2026-10-19T04:30:31Z |
| V3R1T4S known-knowns listing (no cage-upper-bounds directory, no merged package) | [2,7;6] | none | **184** | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:27:03Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is a partial win p2 only: a graph that beats a live entry of the mixed-cage table. It is not a cage record, and it is not a claim about the cage problem for ordinary regular graphs.
- Girth 6 holds under the forward-arc cycle convention (a cycle may traverse an edge in either direction and an arc only from its tail to its head). Under the direction-blind convention (every arc treated as an undirected adjacency) the girth of the same object is 4, as the checker prints. The panel found that the source table itself uses the forward-arc convention: several of its listed values are impossible under the direction-blind reading (for example 196 is below the Moore bound 222 for an 11-regular girth-6 graph). The paper's Preliminaries do not state the convention outright; the panel inferred it from the table and the proofs.
- The table's lower bound for [2,7;6] (123*) is marked as conditional on a conjecture; 184 lies above it, and nothing is claimed about the lower bound.
- Google Scholar and the Dynamic Cage Survey were not searched; the newest paper found (arXiv:2610.14110) has no girth-6 entry for these parameters.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here.

## Filing history

This is a refile of the contributor's pull request 102 (the same graph: same S, A0, A1, M; the JSON differs only in list order), closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.

## Credits

- **arXiv:2506.20003**, *New upper bounds on the order of mixed cages of girth 6* (https://arxiv.org/html/2506.20003): Table 1, the comparison table and the definitions used; authors are on the arXiv page.
- **arXiv:2401.14768**, *On Mixed Cages of Girth 6* (https://arxiv.org/html/2401.14768): the source of the earlier upper bound for [2,7;6].
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
