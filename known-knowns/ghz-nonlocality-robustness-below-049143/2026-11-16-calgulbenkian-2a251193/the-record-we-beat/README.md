# Status Snapshot: ghz-nonlocality-robustness-below-049143

## Primary Status Source

- **Source**: Sebastien Designolle, Tamas Vertesi, and Sebastian Pokutta, *Symmetric multipartite Bell inequalities via Frank-Wolfe algorithms*, Phys. Rev. A 109, 022205 (2024); `arXiv:2310.20677` (`v3`, revised `5 Oct 2026`)
- **URL**: `https://arxiv.org/abs/2310.20677`
- **Fetched UTC**: `2026-11-15T15:11:51Z`
- **HTTP status**: `200`
- **Headers file**: `data/arxiv_2310.20677.headers.txt` (`sha256: d74d5305be98b20243702b6b5d6d7487d40768a2c568625a85415a0`)
  - `last-modified: Wed, 07 Oct 2026 00:08:05 GMT`
- **Page SHA-256**: `57cf2fd4bbd372dc79c7b809afae763731f5bd72f1406666b64e3d67f6174c35`
- **Full v3 HTML URL**: `https://arxiv.org/html/2310.20677v3` (`HTTP 200`, fetched `2026-11-15T15:12:08Z`, `sha256: dfdc7344fb654255b27c902c792caa7feb2f592b1179b79782c54bc4bba90c62`)
- **Extracted status cell**: In Table III (and Appendix B Table VI bold entries), the best rigorously certified upper bound on the white-noise nonlocality robustness $v_c$ of the three-qubit GHZ state $v |\mathrm{GHZ}_3\rangle\langle\mathrm{GHZ}_3| + (1 - v) I_8 / 8$ is **`0.49143`** (`m = 22` planar settings per party, exact value `0.49142745...`). Larger symmetric planar instances (`m >= 28`) are explicitly marked uncertified in Table VI because exact certification of their local bounds was out of reach.

## Additional Literature and Repository Checks

| Source | URL | UTC fetch time | HTTP status | SHA-256 | Extracted cell / status |
|---|---|---|---|---|---|
| Vertesi and Pal (`arXiv:1108.1998`) | `https://arxiv.org/abs/1108.1998` | `2026-11-15T15:11:51Z` | `200` | `dc5e38eb220f7ceaec6a7fd608133106f043fe7851633043ad5b5ffe9f9287dc` | Prior certified `N = 3` upper bound `0.496057` with `5 x 5 x 5` settings |
| `ZIB-IOL/BellPolytopes.jl` repo metadata | `https://api.github.com/repos/ZIB-IOL/BellPolytopes.jl` | `2026-11-15T15:13:32Z` | `200` | `d6b698617791a2ff5af7bcd6939c0b0a40b5723bc15e463ec7881c83f4ff32a3` | Last push `2026-10-21T07:02:46Z`; no newer `N = 3` certified record |
| Live arXiv API query (`"nonlocality robustness" AND GHZ`) | `https://export.arxiv.org/api/query?search_query=all:%22nonlocality+robustness%22+AND+all:GHZ&sortBy=submittedDate&sortOrder=descending&max_results=10` | `2026-11-15T15:46:50Z` | `200` | `4e926336329e2169e90521b2fc5a082bb786c71dae5344bb46916c65f675490e` | Only `arXiv:2310.20677v3` returned; no newer paper beats `0.49143` |
