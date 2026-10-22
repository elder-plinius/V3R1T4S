# The records this claim is compared against

Each row is one honest GET (curl with a User-Agent naming V3R1T4S) or one git clone made by the orchestrator's triage agent; times are UTC as logged in the triage fetch log. Retries on 429 are in that log. Pages are not copied here, only the cells the checker needs.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| 9a.md (primary table, C7 table and comment on larger odd cycles) | https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/9a.md | 2026-10-20T02:43:09Z | 200 | 92f6e1ee5d7219af29572c37dbb54192f3d12c2b1bc818aaf1c3e4ffe46d9899 | see 9a_excerpt.md |
| Bank entry shannon-capacity-odd-cycles | bank/targets.json of the V3R1T4S repository, origin/main commit 69e90f785b77 (committed 2026-10-19), status_checked 2026-10-03 | read from the local clone | n/a | n/a | criterion copied verbatim into CLAIM.md |
| Lean repository head (BPZ) | https://github.com/spectra-research/shannon-capacity-lean, git clone, head aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65 (2026-08-10) | 2026-10-20T02:44:34Z | clone rc=0 | CertC13.lean sha256 7fe600d088d61ca22d06159c9c3f9003b2119dbc152ff72e47fe0361decfa971 | M and d: see records.json (id bpz_lean) |
| Lean sources for the tables and codes | same clone: ShannonBounds/PortRealisation.lean, Substitutions.lean, TerminalCodes.lean | 2026-10-20T02:44:34Z | clone rc=0 | d9bb3f3bbee597a79ab5406546d2a5786c5103e402429b39085c161eb5c98389 ; fd9f47de04fc3019c483b716d12d4371146b3e9beef5bde151ffeb09f66768ec ; f3b082926f921fd28a2a413aaeeee26d95931e0a3098929c19355c5a21dfda03 | rules.json is a transcription of these as data |
| BPZ abstract page | https://arxiv.org/abs/2607.29681 | 2026-10-20T02:43:11Z | 200 | 5bbf974bdf3595b77b36cadff92888f259e9fd1db33ff2b18da360644f7bacf9 | title, authors, date; only v1 exists |
| Gao abstract page | https://arxiv.org/abs/2607.27869 | 2026-10-20T02:43:12Z | 200 | 059970fdfb196a0702d39eda6197aa59399c0d099b06607ec8787d56e2f717ab | title, author, date |
| Itty et al. abstract page | https://arxiv.org/abs/2607.21517 | 2026-10-20T02:43:12Z | 200 | d23d2e7357bed7ec08b35322eb869564b046b233a45adec3933892a05b43253d | title, authors, dates |
| arXiv search, newer results | https://arxiv.org/search/?query=Shannon+capacity+odd+cycle&searchtype=all&order=-announced_date_first ; and query=Shannon+capacity+C7 | 2026-10-20T02:53:19Z and 02:53:22Z | 200 | 7946c07ed885756437c7b08e5f1c005f80707b6cc9e79bea9eda655b0c456cfb ; cbe0536061c66d38d3e78d279533f6f991356cef0d9b89e17ba7e4d33d4bc282 | nothing newer than Tandon on Shannon capacity of odd cycles seen by the orchestrator's triage |

C13 values compared against: Lean repository CertC13.lean, M with d=522 (decimal 6.30292672931010853494960279947052989703296258437934); 9a.md comment value 6.302455083464.

The exact integers of the comparison records are in records.json. For the Lean values the integer M is the number defined as `def M` in the named CertC file; the checker also recomputes it independently from the Lean schedule (known-answer test) before using it.

Best known for this cycle at the time of fetching: the Lean repository head value above (it is higher than the older BPZ version 1 values that the 9a.md comment still lists).

Time sensitivity: the records for these cycles moved several times in July and August 2026. Re-fetch 9a.md, the Lean repository and the arXiv listing immediately before relying on this comparison.
