# Novelty review: C(38,6,3) <= 469 (covering-designs-record)

context: subagent (fresh executor, saw only claim/)
Deviation, disclosed: after the brief was written, the parent said tools/live_cell.py had been changed to follow RULES.md rule 5, and asked that the live check be judged on the changed tool. To check that, I grepped the tool's source for its User-Agent and cookie handling, and nothing else in it. I did not open tools/README.md, the fetches/ folder, or any run, dossier or other skeptic's file.

Claim file: claim/C38_6_3_469blocks.txt, sha256 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b (matches the brief). As a side check, my own scratch script found 469 blocks covering all 8436 of 8436 triples. 469 is at least the Schonheim bound of 425.

novelty: BEATS EVERY VALUE FOUND (469 < 510)

## 1. Live coveringrepository.com value
Each URL was fetched once with curl -A "V3R1T4S-research (honest client)", with no cookies and no retries:
```
== https://coveringrepository.com/
2026-10-20T16:35:02Z
HTTP 200 size 12140
337d7caf92adcd4ef6a9d9f19a2cd610ab0f5ef2f7f6b94ca555fed9e2433652  home.html
== https://coveringrepository.com/download_archive_vkt.aspx
2026-10-20T16:35:04Z
HTTP 200 size 171735
3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7  archive.txt
$ grep -P "^38\t0?6\t0?3\t" archive.txt
38	06	03	03		510
```
The home page has no per-cell values. The archive is the site's public plain-text dump of all plain (v,k,t) cells with M=T. It gives 510 for (38,06,03,03), and its bytes match, by sha256, the archive fetch recorded in claim/data/live_coveringrepository_C38_6_3.txt. I relied on this value, and it came from one plain request by an honest client that names V3R1T4S, which is what rule 5 asks for.

Search-form read with the changed tool, run once (python3 tools/live_cell.py 38 6 3):
```
2026-10-20T16:35:20Z
(38,6,3,3)  blocks=510  lower=425
   author : Known design, view notes ->
   notes  : Creator: Jan de Heer and Steve Muir | Method: Private Tools | Source: Dan Gordon Covering Repository | Repository: https://dmgordo.github.io/
   date   : 05/06/2010
   source : https://coveringrepository.com/systems.aspx (form POST: Search)
   fetched: 2026-10-20 12:35:24 EDT  sha256=3829d7cb815ae511d4bdc23bc9ebfbca797851ec4462f3d7e2f5401fb41742be
   archive: blocks=510  https://coveringrepository.com/download_archive_vkt.aspx  sha256=3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7
```
(12:35:24 EDT is 16:35:24Z. I left out the tool's local save path.)

How the tool makes its requests, from a grep of its source:
```
29:UA = "V3R1T4S-live_cell/1.0 (record-table check; low volume)"
34:# No cookie jar: RULES.md rule 5 forbids cookie replay.
47:    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
```
My judgement: the changed tool is compatible with rule 5. Its User-Agent names V3R1T4S and does not imitate a browser. It replays no cookies, uses no headless browser, makes no retries, and does not request the challenged query-string pages. It does make a GET and then a POST of the site's own search form, which is what a person does by clicking "Search", rather than a single request. That is why I base the verdict on the single-request archive value above, and use the tool only to confirm it. The old method described in claim/data/live_coveringrepository_C38_6_3.txt sent a "Mozilla/5.0 ..." User-Agent and carried a session cookie. I do not rely on that read. Both the old and new reads give the same 510, so the conclusion does not change.

https://www.coveringrepository.com/systems.aspx?li=2 (latest (v,k,t) improvements):
```
2026-10-20T16:35:05Z  HTTP 200 size 180298  sha256 8585c76298cadc2d022dfdb8b691c8fbae66930c84f007b7156aa833e825fa43
parsed rows: 100, dates up to 20/10/2026
rows with V=38: []
rows with T=3: [['28','09','03','03','55','50'], ['30','12','03','03','29','25']]
```
The page includes a Cloudflare script tag, but it was served as a normal page with 100 data rows, not as a challenge. There is no (38,06,03) row.

## 2. La Jolla (LJCR) sources
```
== https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
2026-10-20T16:35:04Z  HTTP 200 size 6517686
0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef
"C(38,6,3)": size 510, low_bd 425, imps: 510 Private Tools, Jan de Heer and Steve Muir, 2010-06-05;
  513 (2009-09-16, same authors); 523 Simulated Annealing, Michael Dambmann, 2008-11-29; 526 Flavio Perona, 2008-11-17
== https://zenodo.org/api/records?q=conceptrecid:10779736&all_versions=true
2026-10-20T16:35:05Z  HTTP 200 size 18140
19472830 1.1 2026-04-08
19735294 1.2 2026-04-24
10779737 v1.0 2024-03-04
== https://dmgordon.org/covering-designs/
2026-10-20T16:35:06Z  HTTP 200 size 9200
a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3   (landing page, no per-cell values)
```
The newest Zenodo version is v1.2 (record 19735294), which is what the claim cites, so I did not fetch the file again. The claim records 510 there. The GitHub coverdata.json fetched now also gives 510.

## 3. Literature, hobbyist and lottery searches (last 24 months)
- Web search for "C(38,6,3) covering design new upper bound 2025 2026" turned up only the LJCR page "425 <= C(38,6,3) <= 510" and the pages above. No improvement.
- I could not connect to the arXiv API (curl: (28) Failed to connect to export.arxiv.org port 80, HTTP 000, not retried). Instead I fetched arxiv.org/search for "covering design", newest first, once (2026-10-20T16:38:26Z, HTTP 200). It returned 54 results, and none mentions C(38,6,3) or (38,6,3). The relevant 2025-2026 papers (single- or double-change coverings, C(12,6,4)=41, lottery papers) concern other objects or other cells.
- The hobbyist repo thebrockchain/covering-designs now redirects to TheEslabonGroup/covering-designs, last pushed 2026-09-20. API tree fetched at 2026-10-20T16:35:54Z, HTTP 200:
  `records/C28_13_4_53blocks.txt, records/C32_13_4_95blocks.txt, reference/...` (no (38,6,3) file)
- Lottery wheels: a web search summary said "38 numbers, 3 if 3 ... 235 tickets". I fetched https://www.lotterypost.com/wheels/pick6 once (2026-10-20T16:36:38Z, HTTP 200), and the row actually says `Key 4 if 6 of 38|38|4 if 6|235`. That is a key-number "4 if 6" wheel, not a full "3 if 3" wheel, so it is a different object. 235 is also below the Schonheim bound of 425, which no full 3-if-3 wheel can be. I found no full 38-number 3-if-3 wheel at or below 510.
- A GitHub code search for "C(38,6,3)" and "38,6,3 covering" returned only unrelated CSV and JS files.

## 4. V3R1T4S repo
```
TROPHY_CASE.md (raw main, 2026-10-20T16:35:35Z, HTTP 200, 89 lines): no match for C(38 / 38,6,3
gh pr list --state all: 583 PRs (#1-#594); title/body match for (38,6,3): none
  only near-hit: #64 CLOSED "[claim] covering-designs-record: C(38, 16, 3) <= 25" (different cell, k=16)
```

## Conclusion
Every value I found for C(38,6,3) is 510:
- the live coveringrepository.com archive, read with one honest request, plus the changed tool's form read
- the LJCR GitHub data
- Zenodo LJCR v1.2 (as recorded in the claim)

I found no claim at or below 510 in the latest-improvements list, the hobbyist repo, lottery-wheel sites, arXiv, GitHub, the V3R1T4S TROPHY_CASE.md, or the repo's pull requests. 469 is strictly below 510, by 41 blocks, so this is not a tie. One limit on coverage: the arXiv API was unreachable, so the arXiv check rests on arxiv.org's own search page.

pass: true
