# Honesty gate, run 2026-10-16-0024 (main session, model claude-opus-5-5)

status: CONFIRMED_SOLUTION
confirmed_scope: The 526 vectors in R^6 of object/d6_N526.txt (sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a, 26 significant digits per coordinate) have, after normalisation in mpmath at 50 digits over all 138,075 pairs, maximum inner product c* = 0.78643061854457972538529914, which is 2.0578e-4 below the cosine 0.786636400242 of the unstarred, unlabelled (6,526) row of spherical-codes.org /plain and HTML index as fetched 2026-10-16T03:59Z, and arXiv metadata searches at 2026-10-16T04:10Z found no (6,526) result newer than the row's own source arXiv:2610.19988.

gate_time: 2026-10-16T05:12:54Z
claim: one row of spherical-codes-cohn-table, (d, N) = (6, 526), object claim/object/d6_N526.txt (sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a)

## Panel (three fresh contexts, each saw only claim/)
- REPRODUCE: subagent (Agent tool), model fable; own checker written before the author's; all 138,075 pairs at 50 digits, 100-digit spot check of the maximal pair; pass: true.
- NOVELTY: subagent (Agent tool), model opus; live table fetched 2026-10-16T04:04:38Z and 04:04:40Z (HTTP 200, same sha256 as the claim's copies); Vahteristo's Zenodo archive (all three tables), Ganzhinov-Ostergard shells, numaro.tech, GitHub, Zenodo and arXiv searches over 24 months, this repo's TROPHY_CASE.md and all 218 pull requests; pass: true. Not reachable: SSRN full text of Jay et al. (host stopped after a 403), arXiv full texts, uploads pending at the table.
- CRITERION: subagent (Agent tool), model opus; clause by clause against the verbatim bank criterion; pass: true, with two conditions for the gate (below).

## Gate checks (main session)
- Live re-fetch immediately before claiming (criterion clause; CRITERION condition i): https://spherical-codes.org/plain at 2026-10-16T05:12:04Z, HTTP 200, sha256 5bc9a557e80c83b5dea824323b2b07abdf55a7b28f8e1840b5bbe3471917479f, line "6,526,0.786636400242"; https://spherical-codes.org/ at 2026-10-16T05:12:06Z, HTTP 200, sha256 0693ae85b23218945abacc3a92a8eee805de3c82bfa622148034f1868eeb863f; the (6,526) row has no star and no "needs more optimization" (saved as data/sc/gate2/). code/sc_check.py on the claimed file against these: c* 0.7864306185445797253852991, gain 0.00020578169742, 26 significant digits (out/gate2_check_6_526.json). Unchanged since 00:28Z.
- Optimizer sanity control (PREREG; CRITERION condition ii): the configuration that produced the code (brute-scale lens, neighbour (N+1) start + LSE polish, "h3sweep") was run on 18 starred-row entries (attempts/brute-scale/out/wctrl_results.jsonl); largest apparent gain 3.3e-13 (the table's rounding of 1/6); no starred row beaten by 1e-10.
- Table access audit: no browser User-Agent, cookie replay, challenge bypass or retry after a block in any lens's code; every request went through code/vfetch.py; the two blocks of the session (export.arxiv.org 503, papers.ssrn.com 403) were recorded and never retried.
- Downgrade list: no hedging verdict, no reproduction mismatch, strictly better than the live table by 2.0578e-4, no stretched clause, scope equal to the CRITERION sentence, a deterministic check of every pair (no sample), no capped search used as an exclusion, one object, one row.
- Not claimed: (6,525) (the same code minus one point also lies below that row) and the other unpanelled rows listed in the report and dossier.
