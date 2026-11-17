# Novelty skeptic: anomaly-free-atlas-qmax, SM Q_max 39 and 40

Claim under test: exact counts of the SM-only anomaly-free U(1) census in the Allanach-Davighi-Melville (ADM) convention:
Q_max 39 = 51237625 and Q_max 40 = 58626334.
Question: does published or posted work already cover this cell, or can it be derived trivially from published work?

All requests used User-Agent "V3R1T4S-research-bot". Each URL was requested once (no retries). There were 44 requests between
2026-11-08T09:40:39Z and 09:44:01Z. The full log is panel_work/novelty/fetch_log.txt (UTC time, HTTP code, sha256, size, URL,
saved file). The saved bytes are in panel_work/novelty/pages/.

## Status source (fetched once)

| URL | fetched (UTC) | HTTP | sha256 | what it says |
|---|---|---|---|---|
| https://arxiv.org/abs/1812.04602 | 2026-11-08T09:40:39Z | 200 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 | Latest version is v5 (8 Jan 2020). There are versions v1 to v5 and no v6. This page is byte-identical to the scout fetches of 2026-11-03 and 2026-11-08 in the status record. In the v5 text (status record), the atlas covers "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR", and Table 2 stops at SM Q_max 10 (23800). |

## Other key sources

| URL | fetched (UTC) | HTTP | sha256 | what it says |
|---|---|---|---|---|
| https://zenodo.org/api/records/3345889 | 09:42:12Z | 200 | 8601344d49e0747502007917aa9e99d245df522fe61d1c909f8f68715571b643 | The atlas data record (v1.1.0, 2018-12-12; concept 1478084). Its files are SMcharges0..10, SMnuRcharges0..10, searchU1.cpp/.h and runme.sh. Nothing goes past Q_max 10. |
| https://zenodo.org/api/records/3345889/versions?size=25 | 09:42:33Z | 200 | 163b4a7670e31f9a9dcf0a042c2f2631bb93f674c5bffaf7f0c85ef63b266d90 | The record has only two versions, 1.0.0 and 1.1.0, both dated 2018-12-12. No later version extends the lists. |
| https://inspirehep.net/api/arxiv/1812.04602?fields=control_number,titles,citation_count | 09:41:35Z | 200 | 31957779617b71e8d595bfd8102de1b7d30d4a8bb3f70b88c8bf6a90734310b9 | INSPIRE record 1708575, with 121 citations. |
| https://inspirehep.net/api/literature?q=refersto:recid:1708575&size=250&sort=mostrecent&fields=titles,arxiv_eprints,abstracts,earliest_date | 09:41:42Z | 200 | 240f8a09b405b4851e8f76e20676dc5398f2b0c8c02fc9b1a04789e6c34da0bc | All 121 citing records, the newest from 2026-09-01. None of the abstracts extends the SM/SMνR tables past Q_max 10 (details below). |
| https://inspirehep.net/api/literature?q=fulltext:%2251237625%22&size=25&fields=titles,arxiv_eprints | 09:41:58Z | 200 | d4a5a65f0ccbe8befce9162f928cd917319514763027500adef278e8961705d3 | 0 hits for the Q_max 39 count. |
| https://inspirehep.net/api/literature?q=fulltext:%2258626334%22&size=25&fields=titles,arxiv_eprints | 09:41:58Z | 200 | 7dd0fd14500029b753f9cc488862abbde66884d20b25e9aa96bc38ac85ca10c4 | 0 hits for the Q_max 40 count. |
| https://inspirehep.net/api/literature?q=fulltext:%2221546920%22&size=25&fields=titles,arxiv_eprints | 09:41:59Z | 200 | a81457c84199456d44d95021b5fe33d4c5f9a448b822f5d44ccf331c7ae1767b | Positive control (published SMνR Q_max 10 value): 2 hits, the atlas and a thesis, "Topological effects in particle physics phenomenology". The full-text search therefore works. |
| https://inspirehep.net/api/literature?q=fulltext:%2223800%22%20and%20fulltext:%2214354%22&size=25&fields=titles,arxiv_eprints | 09:41:59Z | 200 | e0d713896a70d28103452873c3bd2d7d96515089adc667e49f21b38818046232 | Positive control (published SM Q_max 9 and 10 values): the same 2 hits. |
| https://zenodo.org/api/records?q=%2251237625%22%20OR%20%2258626334%22&size=25 | 09:42:32Z | 200 | 94bee2779c832af2f5af69e4905fe5190c4b465edd87a7cf5fad019357093996 | 0 hits. |
| https://api.github.com/search/code?q=58626334+51237625 | 09:43:09Z | 200 | 4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f | 0 hits for both numbers together. |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pull-request+anomaly&per_page=50 | 09:44:01Z | 200 | f9e3e884da6fee2022cfca623e26ceaeabfd7f46c80b0122f7da462a6c5a0bee | 7 PRs. Five are this workspace's own draft PRs #989 to #993 (2026-11-07), whose highest row is SM Q_max 36-38 (#993). The other two (#610, #311) are unrelated. No PR body contains 51237625 or 58626334. |

## Searches and findings

Every row below is in fetch_log.txt with its sha256.

arXiv API (export.arxiv.org/api/query, sorted by submittedDate descending):
- `all:"anomaly-free atlas"` found 2 papers: 1812.04602 (the atlas) and 2107.07926 (the ν-supersymmetric atlas: MSSM content up to Q_max 10, a different census).
- `abs:anomaly AND free AND U(1) AND charge AND assignments` had 523 total; I scanned the 100 most recent, through 2026-11-04. All are phenomenology or model building, with nothing that tabulates bounded-charge counts. The closest is 2508.11583, "Anomaly cancellation for a U(1) factor" (arithmetic-geometry parameterisation, no bounded counts).
- `abs:"anomaly cancellation" AND abs:"family dependent"` found 5 results and `abs:"anomaly free" AND abs:"flavour dependent"` found 6, newest 2026-07-27. Neither set contains a census extension.
- `abs:anomaly AND abs:"maximum charge"` found 1 paper: 2206.11271 ("Flatland"). It is a semi-simple-completion study that uses atlas-type solutions with maximum charge ratio ±10, so it stays inside the published range.
- `abs:anomaly AND abs:Diophantine` found 10 results. The relevant ones are 1905.13729 (general parameterisation), 2006.03588 (general solution for SMνR), 2111.04148 (method of chords) and 2206.09956 (Ising machines). All give parameterisations or methods. None gives bounded exact counts.
- `abs:"anomaly free" AND "Standard Model" AND enumerat*` found 0. `abs:anomaly AND "charge assignments" AND (number OR count OR counting)` found 17, with no census extension.

INSPIRE:
- The first try, `refersto:arxiv:1812.04602`, was not parsed: it returned 25,247 unrelated records and was discarded. The atlas was then resolved to recid 1708575, and `refersto:recid:1708575` returned all 121 citing papers.
- I read the abstracts of every citing paper that might extend the tables: 2007.08733 (U(1)^m constructions), 2408.15536 (leptophilic "atlas", a different object), 2205.03428 (exotic fermions), 2001.11991, 1912.10022, 2402.02577, 2103.06783, 2206.11271, 2206.09956 and 2107.07926. None of them tabulates SM-only counts past Q_max 10.
- Full-text search finds no record containing either claimed count. The controls show that the full-text search finds the published Q_max ≤ 10 values.

Zenodo:
- The atlas record and its version list show that nothing past Q_max 10 was ever deposited.
- Phrase searches `"anomaly-free" AND "charge assignments"`, `"anomaly free" AND "flavour-dependent"` and `"anomaly-free" AND "Qmax"` return only the atlas record, the ν-SUSY atlas record (5062067) and one unrelated item.
- `SMcharges` and the claimed numbers return 0.
- My first set of Zenodo queries used size=50 and returned HTTP 400 (page-size limit 25). Those queries were reissued as new URLs with size=25. Unquoted keyword queries match loosely and gave only noise.

GitHub:
- `gh` is not authenticated, so I used the public REST API.
- Repository search for "anomaly-free atlas", "anomaly free U(1) charges" and "searchU1" found 0. "anomaly cancellation U(1)" found 1 unrelated repository.
- Code search for 51237625 alone found 4000 digit-substring hits in unrelated data files (noise). Both numbers together and "SMnuRcharges" found 0.
- A positive-control code search (published Q_max 10 values) timed out with HTTP 408 and was not retried, so GitHub code search is weak evidence here.
- PR search for 51237625 found only two unrelated UI PRs in another project.

The workspace's earlier rows and the V3R1T4S checkout:
- TROPHY_CASE.md, known-knowns/ and known-unknowns/ contain no entry for this census at all. A grep for anomaly-free / U(1) / Qmax / atlas / 1812.04602 / both counts matched only unrelated text such as "MU(1)" and a C variable name.
- Nothing in the checkout lists SM 39 or 40.
- The upstream draft PRs #989 to #993 are this contributor's own earlier rows, so they are not prior art. They stop at SM 38 and do not contain either claimed value.

Trivially derivable?
- No closed form or generating function for the bounded, canonicalised count exists in the literature found. The parameterisations (1905.13729, 2006.03588, 2111.04148, 2508.11583) describe the solution set, but they do not count it under |F| ≤ Q_max modulo family permutations and sign.
- The atlas's fit 1 + a·exp(bQ + cQ²) − a for the counts is approximate only.
- The published program (searchU1.cpp) could in principle be run. However, the atlas's own run-time fit for the SM, T = exp(−9.45 + 1.38 Q − 0.014 Q²) s, gives about 1.0e10 s (around 330 years) at Q_max 39 and 1.4e10 s (around 440 years) at Q_max 40. This is an extrapolation and only indicative. Even so, getting these rows means writing new code, which is not a trivial use of a published object.

## Best published object for this cell

The ADM atlas itself (arXiv:1812.04602 v5, JHEP 02 (2019) 082, erratum JHEP 08 (2019) 064, with Zenodo 10.5281/zenodo.3345889 v1.1.0). It gives exact SM counts only for Q_max ≤ 10 (the largest is 23800 at Q_max 10). It gives no published value, bound or list for SM Q_max 39 or 40. No later paper, data deposit, citing work or repository found extends the SM-only census past Q_max 10, apart from this workspace's own unmerged draft PRs (which stop at 38).

## Verdict

The cell is novel. SM Q_max 39 and 40 lie well beyond the largest published Q_max (10). No published or posted source found contains either count or a list for these rows. The counts do not follow from any published formula, and the published code cannot reasonably produce them. Caveats:
- arXiv full text is searchable only through INSPIRE's full-text index.
- GitHub code search is weak evidence, because its positive control timed out.
These caveats lower confidence slightly but do not change the verdict.

context: subagent (fresh context, Claude Code Agent tool)
pass: true
