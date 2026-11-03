# Novelty report: cover-57-14-3-b108

context: Claude Code subagent, fresh context

Claim: C(57,14,3) <= 108. Compared values: 109 (coveringrepository.com, Zenodo v1.2), 110 (LJCR GitHub data).

## Primary table, coveringrepository.com (the two requests I was allowed)
- Request 1, GET https://coveringrepository.com/systems.aspx, 2026-10-18T14:23:22Z, HTTP 200, sha256 f4640291c3190dc1559eb0e293c6ed1b6e95f8bba334666537658ecc35957f6e. The default page lists only "Recent uploads and derived coverings" (rows dated 18/10/2026) and the search form; it contains no row for v=57, k=14, t=3.
- Request 2, POST to https://coveringrepository.com/systems.aspx with the hidden fields from request 1 (VIEWSTATE, VIEWSTATEGENERATOR, VIEWSTATEENCRYPTED, EVENTVALIDATION) and the form's own fields ddlV=0 (the "--" choice), ddlK=14, ddlT=3, ddlM=3, empty txtA and txtDate, btnSearch=Search; 2026-10-18T14:24:06Z, HTTP 200, sha256 a2e903b063e78366c55ad98ff5ed7ed93b2186845b76829bafa6fa092e81fd8d. No retries, no other trick. Exact row text read: "57 14 03 03 109 90 Known design ... Creator: Franco Atzeni Method: Local Search Source: Dan Gordon Covering Repository ... 14/02/2025". So the live value is 109, lower bound 90.
- Latest improvements, GET https://coveringrepository.com/systems.aspx?li=1, li=2, li=3 at 2026-10-18T14:24:11Z, 14:24:12Z, 14:24:12Z, HTTP 200 each, sha256 f0539af8..., 451a83cb..., 9272ec61.... All listed dates are 18/10/2026; no row for (57,14,3). This window is only the newest entries, so it says nothing about earlier days; the POST result above is the real check.

## Other sources
- LJCR GitHub tree: https://api.github.com/repos/dmgordo/LJCR/git/trees/HEAD?recursive=1, 14:24:13Z, HTTP 200, sha256 30687579.... The cover data file is coverings/coverdata.json (6517686 bytes). The bare raw directory URL returned 404 (a directory, not a file).
- https://raw.githubusercontent.com/dmgordo/LJCR/master/coverings/coverdata.json, 14:24:23Z, HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. Entry C(57,14,3): size 110, low_bd 90, best improvement 110 by Jan de Heer and Steve Muir, 2013-09-05.
- Zenodo record https://zenodo.org/records/19472830, 14:24:13Z, HTTP 200, sha256 69503e6e.... It is version 1.1 (April 8, 2026). Its versions list (https://zenodo.org/api/records/19472830/versions, 14:24:32Z, HTTP 200, sha256 3ce31765...) shows the newer version 1.2 (record 19735294, 2026-04-24). I fetched that version's coverdata.json once (https://zenodo.org/api/records/19735294/files/coverdata.json/content, 14:24:38Z, HTTP 200, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87). Entry C(57,14,3): size 109, low_bd 90, best improvement 109 by Franco Atzeni, Local Search, 2025-02-14 09:31:41.
- thebrockchain/covering-designs: the github.com page returned HTTP 301 (not retried); the README read through the raw URL https://raw.githubusercontent.com/thebrockchain/covering-designs/HEAD/README.md, 14:25:25Z, HTTP 200, sha256 171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5. It claims only C(28,13,4) <= 53 and C(32,13,4) <= 95; no 57 or (14,3) entry.
- WynandVStaden records list, 14:24:16Z, HTTP 200, sha256 41ffe04b8e3ce9e4e7db7c5fb5ab6864325b8ef2d5e5c5d7c65dbcf7c2ea70a3: 233 current records, "checked against the site on 2026-10-18". Rows with v = 57 are (57,9,3), (57,12,3), (57,16,3); no (57,14,3).

## Repository sources (fetched once)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-18T14:23:15Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists no entry for this target family (no covering-design row).
- Pull requests, pages 1 to 5: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 to 5, 2026-10-18T14:23:15Z to 14:23:21Z, HTTP 200 each; page sha256 values cca876cd..., 176c41b2..., 20ec05c4..., f5d26a78..., and page 5 is an empty list (2ba33ca0...). 392 pull requests read by title.
- known-knowns folder listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-18T14:23:22Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty folders; none belongs to this target.

## Pull requests on covering designs
Covering-designs-record pull requests by others: 398 (68,14,5), 397 (94,13,5), 353 (20,6,3), 212 (53,20,3), 211 (41,12,5), 209 (85,24,3), 208 (61,25,3). The author's own closed pull requests 62, 63, 64 are for (55,14,3), (45,14,3), (38,16,3): other cells, not competing. No pull request names (57,14,3). The bank-facts pull request 393 only refreshes statement text.

## Literature (arXiv query: covering designs AND (record OR upper bound), sorted by date)
2026-10-18T14:26:13Z, HTTP 200, sha256 d3e001d6d.... Eleven hits (query sent over https after an http 301); none gives a covering design for (57,14,3) (the recent ones concern Boolean function representations, multi-agent research systems and projective-space blocking sets).

## Verdict
The live repository value is 109, the Zenodo latest value is 109 and the LJCR GitHub value is 110. The claim, 108, is strictly below all three, and no hobbyist or pull-request value for this cell was found.
unresolved: a GitHub-wide search for unlisted hobbyist claims on (57,14,3) was not possible within the named sources; the live table could change after this fetch; the dmgordon.org page was not in this group's list and was not fetched by me.
novelty: strictly beats 109 (coveringrepository.com live row dated 14/02/2025), 109 (Zenodo v1.2) and 110 (LJCR GitHub).

pass: true
