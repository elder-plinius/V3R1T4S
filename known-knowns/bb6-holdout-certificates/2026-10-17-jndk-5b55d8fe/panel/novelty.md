# Novelty verdict: p1 macro-rule reduction for 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB

context: subagent (fresh context, Claude Code Agent tool)
role: NOVELTY skeptic (panel of three)
claim read: claim/CLAIM.md (target bb6-holdout-certificates, partial win p1)
date of checks: 2026-10-17, 17:13Z to 17:22Z
injection_suspected: none (no fetched page or file contained instructions aimed at an agent)

## Verdict in brief

- The machine is in the NEWEST BB(6) holdout file linked from the status page: BB6_holdouts_663.txt (October 16th, 2026, @mxdys), line 523, sha256 cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9. This is byte-identical to claim/data/BB6_holdouts_663.txt. Of the 240 mirror/state-permutation images, only the machine itself appears in the file.
- The machine is not marked decided anywhere I could check: it has no wiki page (404), and none of the 240 images appears on any of the 560 wiki pages (whole-wiki wikitext dump), on Holdouts_lists, BB(6), Cryptids, or TMBR Sep/Oct 2026. The annotated sheet lists it only as "Quadratic Mess" with empty Status, Notes and Sources. The 4319 sheet has an empty Decided Status. It is absent from the busycoq BB6 branch and from every busycoq PR, open or closed. It is also absent from google-deepmind/cryptids and its PRs, including open PR #6 created today.
- I found no accelerated rule set, reduction or decider certificate for the machine or any image anywhere I could search. Third-party GitHub repos that do list it hold only triage output: an "open / no-period" verdict, an "ops-limit" macro attempt, and simulation statistics.
- There is no equivalent result in the V3R1T4S repo. TROPHY_CASE.md has 0 hits, and none of the 50 open PRs is a bb6 claim.
- One source could not be checked. cosearch.bbchallenge.org answered 502 twice, on two different URLs, with no retry: **PENDING STATUS CHECK for that source**. Search-engine queries surfaced no cosearch contribution for this machine, and no wiki page links one. I judge this residual risk small; it is recorded below.

novelty: NEW (for p1: no published accelerated rule set found), with one secondary source (cosearch) PENDING STATUS CHECK

## Fetch table (one plain request per URL, User-Agent "V3R1T4S-novelty (curl)", no retries)

| # | URL | UTC time | HTTP | sha256 | value read |
|---|---|---|---|---|---|
| 1 | https://wiki.bbchallenge.org/wiki/Holdouts_lists | 2026-10-17T17:13:38Z | 200 | cc7726143a291df936d770382d6df67fd85edb1f4a19f0ee07e66a7a1c570262 | BB(6) table top row: "October 16th, 2026 @mxdys 663 BB6_holdouts_663.txt"; header count 6-state 2-symbol = 663; page revision 9191. This is the same revision as the scout's copy (claim/data/holdouts_lists.html). The hash differs only in per-request IDs and timing. |
| 2 | https://wiki.bbchallenge.org/w/images/6/69/BB6_holdouts_663.txt | 2026-10-17T17:14:01Z | 200 | cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9 | 663 lines; line 523 = 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB; no other image present; identical to claim copy |
| 3 | https://wiki.bbchallenge.org/wiki/BB(6) | 2026-10-17T17:13:39Z | 200 | 2d8627649b485cc1d56900b22963d0012a3a8969fb8322ac6ed719eb634dc690 | 0 of 240 images |
| 4 | https://wiki.bbchallenge.org/wiki/1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB | 2026-10-17T17:13:39Z | 404 | 09256ec64ccc347c864ad0f11b0f20827ff32e215f0a09997a45d095767a2c80 | no page for the machine |
| 5 | https://wiki.bbchallenge.org/wiki/Cryptids | 2026-10-17T17:13:39Z | 200 | 336f9272dbc857a2c4e10c93291df009a51a8d10575f81a211d51b55739c51b9 | 0 of 240 images |
| 6 | https://wiki.bbchallenge.org/wiki/TMBR:_October_2026 | 2026-10-17T17:17:59Z | 200 | 4c604c2c5bbb2eacbeb7c5085e81172416828c183d2220ec52051ea4a9daef0a | 0 images (all notations) |
| 7 | https://wiki.bbchallenge.org/wiki/TMBR:_September_2026 | 2026-10-17T17:17:59Z | 200 | ebbc60586dc9c1e29546fdbadacfe6fba6db930f540b3da8e5951b296306aef2 | 0 images |
| 8 | https://cosearch.bbchallenge.org/ | 2026-10-17T17:18:00Z | 502 | 06eb358ae605e4a5ab7a141a591b6991b89dc6109db492dd9fea9cf5891be95d | nginx "502 Bad Gateway": PENDING STATUS CHECK |
| 9 | https://cosearch.bbchallenge.org/contribution/4r04jv3b/reviews (the only cosearch URL a web search surfaced near this machine's prefix) | 2026-10-17T17:21:58Z | 502 | 06eb358ae605e4a5ab7a141a591b6991b89dc6109db492dd9fea9cf5891be95d | 502: PENDING STATUS CHECK |
| 10 | https://wiki.bbchallenge.org/w/api.php?action=query&list=search&srwhat=text&srlimit=50&format=json&srsearch=%221RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB%22 | 2026-10-17T17:18:14Z | 200 | 688d401ed6447a04b61b8b5aea327e975f2f69ec5596d800d49a0b230236ea4b | totalhits 0 |
| 11 | same API, srsearch = "1LB1RC_1RC0LD_0RE1RA_0LF1LA_1RA0RA_---0LB" (mirror) | 2026-10-17T17:18:14Z | 200 | 688d401ed6447a04b61b8b5aea327e975f2f69ec5596d800d49a0b230236ea4b | totalhits 0 |
| 12 | same API, srsearch = 0RF1RA_1LA0LA | 2026-10-17T17:18:14Z | 200 | 688d401ed6447a04b61b8b5aea327e975f2f69ec5596d800d49a0b230236ea4b | totalhits 0 |
| 13 | same API, control: srsearch = "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE" (a machine that has its own wiki page) | 2026-10-17T17:18:23Z | 200 | 460c71f92834ceee72bd0f8152ac92e892e8603f9ebab294d27a7bd41ebe051a | returns 1 hit, a DIFFERENT page, so the wiki full-text search is unreliable for machine strings (see rows 16 and 17) |
| 14 | same API, control without quotes | 2026-10-17T17:18:23Z | 200 | 011d4fbe30dd2a45da27302ced9217ee0f7e7cf412461289d86faf2a9d266333 | same wrong single hit |
| 15 | https://wiki.bbchallenge.org/w/api.php?action=query&list=allpages&aplimit=max&format=json | 2026-10-17T17:18:35Z | 200 | 799ae58a318a8e61b69821b97b2c5da6e942dd2b3731481451aafc84ea3028bf | 480 main-namespace titles (103 are 6-state machine pages); no title equals any image |
| 16 | https://wiki.bbchallenge.org/w/api.php?action=query&generator=allpages&gapnamespace=0&gaplimit=50&prop=revisions&rvprop=content%7Ctimestamp&rvslots=main&format=json (plus 9 continuation URLs) | 2026-10-17T17:21:05Z to 17:21:07Z | 200 x10 | first page b3c392602ef2644ec91424cbd82b3889cc7827812b54a6edd4c531bd096406f2 (others logged in work/) | full wikitext of all main-namespace pages |
| 17 | same with gapnamespace=2 (User pages), 2 URLs | 2026-10-17T17:21:07Z | 200 x2 | 0d31e29784c0ef5f129db5e077e7190a2e22ac65374d84d5571f7292d16b17d8, 4db5dd02b6678edf36d1cc5e50ae11dbe47d0084a43153d4ca7ea5f9ab865631 | 560 pages in total (1.70M chars): 0 hits for the 240 images in underscore, "---"/HHH/any-undefined, space-separated or compact notation. The control string is found (1), so the dump method works. |
| 18 | https://wiki.bbchallenge.org/w/api.php?action=query&list=allimages&ailimit=max&format=json | 2026-10-17T17:21:18Z | 200 | 43dc5506b4d52c86c03610d6b672971f68232e5dc86b457e2d8f78190a6700a0 | 164 uploaded files; none named after any image |
| 19 | https://docs.google.com/spreadsheets/d/1mMp8bAcTFT91j7azn72liX8NSTwc2E_ozKnOGTfRCfw/export?format=csv&gid=1330361301 (one redirect followed) | 2026-10-17T17:18:54Z | 200 | fc025a7fe96f1e36376c76216439511c621ca871b8f7e9f07d782f75e7577195 | row `1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB,,Quadratic Mess,,,`: Status, Notes, Sources and Done By are empty. Identical to the claim copy. |
| 20 | same sheet, gid=806905077 | 2026-10-17T17:18:55Z | 200 | 25e311c0bba9c2268470620cbf672b08afa5e820c0d59a99afad69d589476704 | 0 images |
| 21 | 4319 sheet (claim/data/notes/sheet_4319.csv, scout fetch 17:10:27Z, sha 7e519e56...; not re-fetched) | - | - | 7e519e56a90a9fd591faa21c9744426e576525704d7956ac53e86c4528b0568a | row 3464: machine, Decided Status / Notes empty |
| 22 | https://discuss.bbchallenge.org/search.json?q=1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA | 2026-10-17T17:21:26Z | 200 | e37fb4e8bf3894fa2cd9fdeb7aeaca637675d0be775fc9699e33307f0875ddb6 | 0 posts |
| 23 | http://export.arxiv.org/api/query?search_query=all:%22busy%20beaver%22&sortBy=submittedDate&sortOrder=descending&max_results=50 | 2026-10-17T17:21:27Z | 301 | e3b0c442... (empty body) | redirect to https; fetched the https URL once (next row) |
| 24 | https://export.arxiv.org/api/query?search_query=all:%22busy%20beaver%22&sortBy=submittedDate&sortOrder=descending&max_results=50 | 2026-10-17T17:21:34Z | 200 | 434173b0de5a3379bac10a4d0472c412056463ae7d2119e684d49f92b6ec892b | 10 papers since 2024-10 (BB(5) determination 2509.12337, deciders part I 2504.20563, Castor Ministerialis 2510.17438, theory papers); none on individual BB(6) holdouts or this machine |

### GitHub (gh CLI, read-only)

| # | Object | UTC time | sha256 of saved output | value read |
|---|---|---|---|---|
| G1 | ccz181078/busycoq branch BB6 head | 2026-10-17T17:14:31Z | - | commit 2733f6108e394f55b29b83f07c1c7aaa1b6139c1, 2026-10-16T07:43:26Z "add 35 proofs from PR"; README: "For BB(6), there're about 663 holdouts" |
| G2 | busycoq BB6 recursive tree (613 paths, not truncated) | 2026-10-17T17:14:31Z | 81fff56882c43630dcb9dceaf065c86e7177cdab608c9e1a76241a5355707fd4 | 0 file names contain any image (checked with "---", "HHH" and any undefined-transition notation) |
| G3 | busycoq BB6 tarball at 2733f61 (contents of all files, 59 MB unpacked) | 2026-10-17T17:14:53Z | 415fd05a1343a23016b5c490d8fd51841d066df249808056ba9136efb2121327 | 0 hits for 240 images in underscore / any-undefined / compact / space notation. The tree holds ~216k other 6-state machine strings, so the encoding is grep-able. |
| G4 | `gh pr list -R ccz181078/busycoq --state all --limit 500` | 2026-10-17T17:15:15Z | 1f0e98d36098482615ef125bd26662d537c1541c711e45f3b6dea87ce195e5a2 | 31 PRs (30 target BB6, created 2026-08-15 to 2026-10-17); 0 title/branch hits |
| G5 | `gh pr view` (files, body, comments) for PRs 2-31 | 2026-10-17T17:15:28Z | logged in work/prs | 0 hits in changed-file names (incl. M_..._HHH naming), bodies, comments |
| G6 | `gh pr diff` for all non-merged PRs (2,3,4,6-13,29,30,31; open: 3, 4, 13, 29) | 2026-10-17T17:15:54Z | logged in work/prs | 0 hits in diff content. PR 13 "original815 row9" is 1RB0LA_0RC1LE_0RD1RE_1LA1RF_1RB0LD_1RC---, a different machine. |
| G7 | google-deepmind/cryptids main @38ae6721 tarball | 2026-10-17T17:16:30Z | ee894e1ab37a5339ba9dafefe7196849ab8ad3cbdfa58d1d42f5cecd7f891656 | 42 machine files; 0 image hits |
| G8 | cryptids PRs (5 total); PR #6 (OPEN, 2026-10-17 "Add 11 novel BB(6) cryptid reductions and accelerations") diff | 2026-10-17T17:16:45Z | diff sha 51d8a947c90b67b5... | 0 hits in diff, files, body, comments. PR #5 (closed) and #4 (merged) diffs exceed the API limit (HTTP 406, recorded). Their file lists (45 files for #5) and bodies give 0 hits, and #4's content is in G7. |
| G9 | `gh search code` for machine prefix / mirror prefix | 2026-10-17T17:19:15Z | - | 8 hits, all lists or triage files, mirror 0. Repos: bbchallenge/bbchallenge static/BB6_holdouts_815.txt; JacobRSchwartz-AI/bb6-holdouts (hunt.tsv "open no-period", triage.tsv "4 ops-limit", open.txt, holdouts-1534.csv); skm12323/bb6-holdout-analysis (BB6_holdouts_815.txt, triage2/scan.txt statistics); icy-001/fiery (machine listed in a "bb6-holdouts" collection) |
| G10 | Those files fetched via contents API | 2026-10-17T17:19:26Z to 17:19:28Z | eafc13f7..., d2e2615e..., 5451c2b0..., acf84835..., b858930b... | none carries rules; a triage verdict or list entry only |
| G11 | skm12323/bb6-holdout-analysis full tarball (main @277f8b2, pushed today) | 2026-10-17T17:19:50Z | 9c4675e0ccf4a7598ddf63b90d49291e5b58417cc8b69a1ce2948f0081a21546 | machine only in the 815 list and scan.txt; its reductions concern 7 other machines |
| G12 | CyclingCycloid/bb6-holdout-research full tarball (main @1338b63) | 2026-10-17T17:20:08Z | 7fd353cd30ec08b7f8624cc36631e904442e858d7bc03cdbe6a168091f7efb29 | machine appears only in lists, ledger and triage: holdouts-815eqv, undec_now, ledger ("Quadratic Mess", rest empty), quad_mess_undec.txt line 41, aug30 triage "DONE ... lastRuns=7". The attack dossier covers only the first 30 of 53 Quadratic Mess machines; this one is #41. |
| G13 | V3R1T4S: repo copy TROPHY_CASE.md (sha 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9) | 2026-10-17T17:17:11Z | - | 0 image hits; no BB / Turing / bb6 entries |
| G14 | `gh pr list -R elder-plinius/V3R1T4S --state open --limit 500` and `--state all --search bb6` | 2026-10-17T17:17:11Z / 17:17:20Z | 231f23365c92b7c31f70b2a2f250925dbdb6c9c77299dd3033b3228e87442142 | 50 open PRs, none on bb6-holdout-certificates; 0 image hits in titles/bodies; bb6 search returns nothing |

### Web search (WebSearch)
- `"1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB"`: no matching page.
- `"1LB1RC_1RC0LD_0RE1RA_0LF1LA_1RA0RA_---0LB"` (the mirror): no matching page.
- `"1RB1LC_1LC0RD_0LE1LA" OR "1RB1LC 1LC0RD 0LE1LA 0RF1RA"` (extended search): no matching page.
- `bbchallenge "1RB1LC 1LC0RD 0LE1LA"`: only other machines, plus one cosearch URL (unreachable, rows 8 and 9).
- `cosearch bbchallenge BB(6) contribution "1RB1LC_1LC0RD"`: the only bb6-tagged cosearch item shown is a different machine (1RB1LA_1RC0RC_...).
- BB(6) macro-rule / holdout literature 2024-2026: wiki TMBR pages and BB(5) papers only; nothing names this machine.

## Image set

I wrote a script for the image set (work/images.py). It applies L<->R mirroring times all 120 permutations of states B..F, with A fixed, which gives 240 distinct tables. I grepped them in four notations:
- underscore form;
- "---" replaced by any 3 characters, covering HHH, 1RZ and so on;
- compact form with no separators;
- space-separated form.

The machine itself is in TNF; the mirror is 1LB1RC_1RC0LD_0RE1RA_0LF1LA_1RA0RA_---0LB.

## Human reports (Discord #bb6, CLAIM.md items 1-5)

These are what they claim to be: manual reports by the workspace's human, not fetched evidence. I could not verify them.

- Items 1 to 3 (exact string, mirror, attachments since 2026-09-30) are the right searches for the main gap I cannot reach. They agree with everything fetched. The only hit is a 2024 list captioned "haven't been decided or classified". Since then the machine appears only in successive @mxdys holdout lists.
- Item 4 (the Oct 1 longitudinal-analysis list) rules out the one recent batch where an informal analysis would most likely have appeared.
- Item 5 (wiki browser full-text search) is weak on its own: my control (row 13) shows the wiki search does not reliably find machine strings. I have replaced it with a complete wikitext dump of all 560 main and user pages (rows 16 and 17), which has 0 hits and a positive control.

Remaining gaps:
- (a) Discord text search would not find a rules post that names the machine only in a non-underscore notation or only inside an attachment posted before 2026-09-30.
- (b) cosearch.bbchallenge.org was unreachable (502).

Neither gap affects the literal p1 condition: "a machine in the newest BB(6) holdout file whose wiki/holdout notes give no accelerated rule set". I verified that condition directly against the newest file, the whole wiki and both sheets. For the broader condition "not published anywhere I can find", the fetched evidence and the human reports together are sufficient in my judgment. A rules post for a named holdout would normally carry its standard string, and the human's string search covers that.

## Conclusion

The machine is in the newest holdout file (BB6_holdouts_663.txt, 2026-10-16, line 523, sha256 cfb2540f...) and is not marked decided. No accelerated rule set, reduction or certificate for it or any of its 240 images is published on the wiki, in the sheets, in busycoq (BB6 tree and all PRs), in google-deepmind/cryptids (tree and all PRs), in third-party GitHub analyses, on the bbchallenge forum, on arXiv or on the web. Nothing equivalent is in V3R1T4S TROPHY_CASE.md or its open PRs. The claim would be the first published macro-rule reduction for this machine, so it strictly improves on what is known for p1; it does not tie an existing result. Residual risks: cosearch is PENDING STATUS CHECK (502), and the Discord coverage rests on human reports.

pass: true
