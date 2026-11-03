# Live re-fetch of the comparison values, 2026-10-18 (novelty skeptic of this panel)

These requests were made by this panel's NOVELTY skeptic, once each, with the honest-client User-Agent, and are recorded in its report (out/novelty.md). The orchestrator copied the values here before the criterion re-check; nothing was re-fetched for this file.

| Source | Request | UTC time | HTTP | sha256 of saved response | Value for (57,14,3) |
|---|---|---|---|---|---|
| coveringrepository.com, plain (v,k,t) table | POST of the site's own search form on https://coveringrepository.com/systems.aspx with V=0, K=14, T=3, M=3 (the table is only served through that form; one GET of the page first for its hidden fields) | 2026-10-18T14:24:06Z | 200 | a2e903b063e78366c55ad98ff5ed7ed93b2186845b76829bafa6fa092e81fd8d | 57 14 03 03 109 90 (v, k, t, m, blocks, lower bound); creator and date: Known design, view notes -> / Creator: Franco Atzeni Method: Local Search Source: Dan Gordon Covering Repository Repository: https://dmgordo.github.io/ / 14/02/ |
| coveringrepository.com latest improvements | GET https://coveringrepository.com/systems.aspx?li=1, li=2, li=3 | 2026-10-18T14:24:11Z to 14:24:12Z | 200 | f0539af8..., 451a83cb..., 9272ec61... | no (57,14,3) row |
| LJCR (dmgordo/LJCR GitHub data) | GET https://raw.githubusercontent.com/dmgordo/LJCR/master/coverings/coverdata.json | 2026-10-18T14:24:23Z | 200 | 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef | 110 (per the novelty report) |
| Zenodo v1.2 (newest version linked from record 19472830) | GET https://zenodo.org/api/records/19735294/files/coverdata.json/content | 2026-10-18T14:24:38Z | 200 | 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 | 109 (per the novelty report) |
| dmgordon.org/covering-designs/ (live LJCR page) | GET https://dmgordon.org/covering-designs/ (orchestrator, 13:46:58Z) | 2026-10-18T13:46:58Z | 200 | a5cc2312afc8dedd... | prose only; the page lists no per-cell values and points to coveringrepository.com |
| WynandVStaden/covering-design-records RECORDS.md | GET raw RECORDS.md | 2026-10-18T14:24:16Z | 200 | 41ffe04b8e3ce9e4e7db7c5fb5ab6864325b8ef2d5e5c5d7c65dbcf7c2ea70a3 | no (57,14,3) row |
| thebrockchain/covering-designs README | GET raw README.md | 2026-10-18T14:24:25Z | 200 | 171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5 | claims only (28,13,4) and (32,13,4) |
| arXiv | export API, query for covering design records/upper bounds, newest first | 2026-10-18T14:26:13Z | 200 | d3e3e66cc64dfe8bac5f5939f1c807c299db83f15328ee3bcf7270c0eebf56d8 | see out/novelty.md |
