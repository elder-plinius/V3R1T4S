# Novelty skeptic: anomaly-free atlas Q_max extension (SMnuR 19; SM 32..35)

context: subagent (fresh context, Claude Code Agent tool)

Read: only claim/ (CLAIM.md, status.md, object/counts.txt, source/atlas/). Working files and every fetched byte are in
panel_work/novelty/; the fetch log is panel_work/novelty/fetch_log.txt. Each URL was requested once with a User-Agent naming
V3R1T4S. Requests that were blocked were not retried. No outward action was taken.

## Status fetch (primary)

| item | value |
|---|---|
| URL | https://export.arxiv.org/abs/1812.04602 |
| time (UTC) | 2026-10-28T10:49:26Z |
| HTTP | 200 |
| sha256 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 (byte-identical to the scout's copy in claim/source/atlas/arxiv_1812.04602_abs.html) |
| versions | v1 (11 Dec 2018), v2 (7 Jan 2019), v3 (7 Feb 2019), v4 (30 Jul 2019), v5 (8 Jan 2020). There is no v6, so no later version extends the range. |
| value (paper, v5 text in claim/source/atlas/) | the atlas is stored "for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR" |

| item | value |
|---|---|
| URL | https://zenodo.org/api/records/3345889 |
| time (UTC) | 2026-10-28T10:49:27Z |
| HTTP | 200 |
| sha256 | 4f9a6125ab7ce4161d6fbc3f5a35eaf4da57eded7fc3d80c43165480f6843eef |
| value | version 1.1.0 is `is_last: true` and the concept record is 1478084. The description says "lists of anomaly-free charge combinations up to a maximum magnitude charge Qmax given by the number at the end of the filename". Its files are SMcharges0..SMcharges10 and SMnuRcharges0..SMnuRcharges10(.bz2), plus searchU1.cpp/.h, runme.sh and filterNeut.cpp. |
| versions list | https://zenodo.org/api/records/3345889/versions?size=25&sort=version, 10:49:59Z, HTTP 200, sha256 193d4d55…eb4fe. There are 2 versions: 1478085 (v1.0.0, Dec 2018: SM 0..10, SMnuR 0..6) and 3345889 (v1.1.0, Jul 2019: SM 0..10, SMnuR 0..10). There is no newer version. |

**Largest published Q_max: 10 for SM and 10 for SMnuR**, in the paper (v5 plus the JHEP erratum) and in its Zenodo data set.

## What was searched and found

| # | source (one request each) | time (UTC) | HTTP | what it gives | larger census or these counts? |
|---|---|---|---|---|---|
| 1 | export.arxiv.org/abs/1812.04602 | 10:49:26 | 200 | v1..v5; atlas Q_max ≤ 10 (SM, SMnuR) | no |
| 2 | zenodo.org/api/records/3345889 | 10:49:27 | 200 | data files up to Q_max 10 (SM, SMnuR) | no |
| 3 | zenodo.org/api/records/3345889/versions?size=50 | 10:49:39 | 400 | rejected by a validation rule ("Page size cannot be greater than 25"). This was a parameter error, not a block. | n/a |
| 4 | zenodo.org/api/records/3345889/versions?size=25&sort=version | 10:49:59 | 200 | 2 versions, latest is 3345889 | no |
| 5 | zenodo.org/api/records/1478084 (concept) | 10:49:49 | 302 | redirects to /api/records/3345889, the same record as row 2 | no |
| 6 | inspirehep.net refersto:arxiv:1812.04602 (URL as instructed) | 10:49:39 | 200 | 25202 unrelated hits: INSPIRE did not parse the query as a citation search, so the result is unusable | n/a |
| 7 | inspirehep.net/api/arxiv/1812.04602 | 10:49:59 | 200 | recid 1708575, citation_count 121 | n/a |
| 8 | inspirehep.net refersto:recid:1708575 (size 150, most recent) | 10:50:09 | 200 | all 121 citing records with titles and abstracts. I read every abstract from the last 24 months (about 35 records, 2024-11 to 2026-09-01) and every older abstract that hits an enumeration keyword. | no. None enumerates SM/SMnuR charges past Q_max 10. The nearest relatives cover other ground: 2107.07926 (MSSM ν atlas, Q_max = 10, different field content); 2206.11271 (semi-simple completions, max charge ±10); 2203.13731 (vector-like subset, charges ≤ 10); 2206.09956 (Ising-machine solver, no census); 2508.11583 (arithmetic-geometry parametrisation, no counts) |
| 9 | arXiv API: all:"anomaly free atlas" | 10:50:33 | 200 | 2 hits: 1812.04602 and 2107.07926 | no |
| 10 | arXiv API: abs:"anomaly free" AND abs:U(1) AND (enumeration OR census OR Qmax OR "maximum charge" OR "integer charges"), newest first, 100 rows (back to 2022-05) | 10:50:33 | 200 | 395 total; the newest 100 were screened | no (keyword hits are 6D supergravity or no counts) |
| 11 | arXiv API: abs:anomaly AND "charge assignments" AND "right-handed neutrinos" | 10:50:35 | 200 | 24 total, all screened | no |
| 12 | arXiv API: all:Qmax AND all:anomaly | 10:52:08 | 200 | 1 hit (cond-mat 2006, unrelated) | no |
| 13 | zenodo.org/api/records?q="anomaly-free" AND charge (most recent 25) | 10:52:06 | 200 | 59 total. The only census data sets are 3345889 (this atlas) and 5062067 (MSSM ν atlas). The rest are unrelated 2026 uploads. | no |
| 14 | raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 10:51:00 | 200 | sha256 83af764f…6113. Covers other result families only. No match for anomaly, atlas, Q_max or U(1). | no |
| 15 | git ls-remote github.com/elder-plinius/V3R1T4S | 10:51:00 | exit 0 | 1121 refs, of which 774 are refs/pull/*/head (open and closed) | n/a |
| 16 | api.github.com search/issues (PRs matching "anomaly") | 10:51:10 | 403 | blocked by the agent proxy (the session is bound to its configured repos). Not retried. | n/a, covered by row 17 |
| 17 | git fetch --depth=1 --filter=blob:none of all 774 PR heads and main | 10:51:21 | exit 0 | 774 PR trees. I checked every path in every PR, every PR head commit subject, and the main tree for anomaly, atlas, U(1), Q_max, census, SMnuR, Davighi and Allanach. | no. There are 12 path hits in PRs 108, 110, 466, 610 and 736, all false positives (packing seeds "scu1…", nanoalloys "Cu15Ag40", a kit fixture "hsp6_anomaly", quake ids "…u1…"). No PR or trophy carries anomaly-free census rows, including this workspace's earlier rows SMnuR 11..18 and SM 11..31. Those were not filed upstream. |

## Call

- **Published range.** The largest Q_max with published exact counts is 10, for both SM and SMnuR (arXiv v5, JHEP erratum, Zenodo
  v1.1.0, which is the last version). No later arXiv version or Zenodo version extends it.
- **Literature.** None of the 121 INSPIRE citing records, and none of the arXiv or Zenodo searches over the last 24 months, gives SM or SMnuR
  census counts beyond Q_max 10. None gives the claimed numbers.
- **V3R1T4S.** Neither TROPHY_CASE.md nor any of the 774 PR heads contains anomaly-free census rows.
- **The workspace's own earlier rows** (SMnuR ≤ 18, SM ≤ 31) are unpublished and were never filed upstream. Even if they counted as
  "known", the claimed rows still lie strictly past them: SMnuR 19 > 18, and SM 32..35 > 31.
- **Strict beat.** The claimed rows (SMnuR Q_max 19: 4247050205; SM Q_max 32..35: 15866882, 19550225, 22847889, 26469950) are
  new exact counts at Q_max strictly larger than every known tabulation. They are not ties.
- **Limits.** This call covers novelty only. It does not check the counts, which is the reproduction skeptic's job. Literature
  coverage is INSPIRE citations of the atlas plus arXiv and Zenodo keyword searches. GitHub-wide code search was not available (row
  16, 403). Google Scholar and full-text search were not used. An unindexed, uncited private computation cannot be excluded. The
  atlas's own program lets users run larger Q_max, but no such run has been published.

Verdict: novel. Nothing published or recorded elsewhere reaches these Q_max values or gives these counts.

pass: true
