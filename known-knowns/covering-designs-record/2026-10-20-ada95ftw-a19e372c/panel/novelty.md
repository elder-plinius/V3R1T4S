# Novelty skeptic: C(35,5,3) <= 713 (covering-designs-record)

context: subagent (fresh executor, saw only claim/ plus the permitted live-table tool and its README describing the 12:34 PM ET rule-5 fix)

Claimed: claim/C35_5_3_713blocks.txt, 713 blocks, sha256 a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149.

## Sanity (own code, not claim/checker.py)
```
a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149  C35_5_3_713blocks.txt
713 713 True 0      # blocks, distinct blocks, all blocks 5 distinct points in 1..35, uncovered triples of 6545
```
Schonheim L(35,5,3) = 658 <= 713, so no "below the bound" bug signal.

## 1. Live coveringrepository.com value

### 1a. Home page (status_source), one plain curl, UA "V3R1T4S-research (honest client)", no cookies
```
== https://coveringrepository.com/
2026-10-20T16:37:42Z
HTTP 200 bytes 12140
cea0cea94f7e517ffa8c3288d782dc925198afb8ee8f3a10116ef0543b811fae  home.html
```
Home page only; no per-cell values (they load by JavaScript). No challenge page ("Just a moment" count 0).

### 1b. Public plain-text archive, one plain curl, same UA, no cookies, no retries
```
== https://coveringrepository.com/download_archive_vkt.aspx
2026-10-20T16:37:43Z
HTTP 200 bytes 171735
3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7  archive.txt
35^I05^I03^I03^I^I732^M$
```
Line for (35,05,03,03): 732 blocks. Same bytes (same sha256) as recorded in claim/data/live_coveringrepository_C35_5_3.txt.

### 1c. Live search-form read with the fixed tool (run once)
Tool request method as now written in the tool (checked in its source):
```
29:UA = "V3R1T4S-live_cell/1.0 (record-table check; low volume)"
34:# No cookie jar: RULES.md rule 5 forbids cookie replay.
35:_opener = urllib.request.build_opener()
47:    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
```
Output:
```
2026-10-20T16:37:25Z
(35,5,3,3)  blocks=732  lower=658
   author : Known design, view notes ->
   notes  : Creator: Moshe Milshtein | Method: Tabu Search started from a 733-block covering previously created by Kleszek | Source: Dan Gordon Covering Repository | Repository: https://dmgordo.github.io/
   date   : 13/07/2024
   source : https://coveringrepository.com/systems.aspx (form POST: Search)
   fetched: 2026-10-20 12:37:28 EDT  sha256=c0ba5ccaaec10663743bad8f8a38369e9c639ce1ab50aaac736073142e155cd1
   archive: blocks=732  https://coveringrepository.com/download_archive_vkt.aspx  sha256=3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7
2026-10-20T16:37:32Z
```
Honest-access judgment: the fixed tool uses a User-Agent that names V3R1T4S with no browser prefix, carries no cookies, does not touch the Cloudflare-challenged query-string/per-cell URLs, and makes no retries. The GET-then-POST of the site's own unchallenged search form is what a plain client submitting the form does; it bypasses nothing. I judge this read compatible with rule 5. The earlier 16:26:12Z read recorded in claim/data/live_coveringrepository_C35_5_3.txt used a "Mozilla/5.0 ..." User-Agent and carried the session cookie; I do NOT rely on that earlier read. My comparison rests on 1b (plain curl) and 1c (fixed tool), which agree.

Live value relied on: 732 (Moshe Milshtein, Tabu Search, 13/07/2024), fetched 2026-10-20T16:37:28Z (tool) and 2026-10-20T16:37:43Z (archive).

## 2. Latest improvements page (one plain curl)
```
== https://www.coveringrepository.com/systems.aspx?li=2
2026-10-20T16:37:46Z
HTTP 200 bytes 180298
c5587a51ed1a47bff01c47c8d3dd2933af626417896f3e2818223700089e1522  li2.html
li2 title: Covering Repository - Coverings nochallenge
rows 100
35/05/03 rows: []
t=3 rows: [['28', '09', '03', '03', '55', '50'], ['30', '12', '03', '03', '29', '25']]
```
Newest row dated 20/10/2026; no (35,05,03) row.

## 3. LJCR GitHub and Zenodo
```
== https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
2026-10-20T16:37:44Z
HTTP 200 bytes 6517686
0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef  gh_coverdata.json
github C(35,5,3): {'size': 733, 'low_bd': 658, 'imps': [['733', 'Wheel Generator', 'kleszek', '2017-03-25 12:48:15'], ['734', 'Wheel Generator', 'Anastasios Tampakis', '2011-03-30 13:17:01'], ['735', 'Private tools', 'Jan de Heer and Steve Muir', '2011-03-29 10:03:25'], ['752', '', 'Anastasios Tampakis', '2009-01-01 14:45:31'], ['784', 'Simulated Annealing', 'Michael Dambmann', '2008-12-12 06:49:32'], ['815', 'Simple construction: combined (34,5,3) and  (34,4,2)', 'LJCR', '2008-12-05 10:08:05']]}
== https://zenodo.org/api/records?q=conceptrecid:10779736&all_versions=true
2026-10-20T16:37:45Z
HTTP 200 bytes 18140
f64bca01fb2aa45b4654c8ccb046cba6601d82017f0310af7d82ea06aba395cd  zenodo.json
10779737 v1.0 2024-03-04 2024-03-04T21:48:18.296330+00:00
19735294 1.2 2026-04-24 2026-04-24T15:59:08.905409+00:00
19472830 1.1 2026-04-08 2026-04-08T17:06:16.591689+00:00
```
Newest Zenodo version is still v1.2 (record 19735294), so per the brief I did not refetch its coverdata.json; claim/data/zenodo_v1.2_coverdata_C35_5_3.json records "size": 732 (Moshe Milshtein, 2024-07-13).

## 4. dmgordon.org landing page
```
== https://dmgordon.org/covering-designs/
2026-10-20T16:37:47Z
HTTP 200 bytes 9200
a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3  dmg.html
```
Landing page, no per-cell value. A web search surfaced the legacy LJCR cell page titled "658 <= C(35,5,3) <= 732" (ljcr.dmgordon.org/cover/show_cover.php?k=5&t=3&v=35, Milshtein); not fetched, consistent with 732.

## 5. V3R1T4S repo (elder-plinius/V3R1T4S), plain unauthenticated requests
```
== https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
2026-10-20T16:38:00Z
HTTP 200 bytes 31235
(grep for "35,5,3" / "C(35" / "covering": no matches; 100 lines)
pulls pages 1-4 (state=all, sorted by updated): 400 PRs, numbers 205..594 plus older
covering-designs PRs seen: #353 C(20,6,3), #572 C(29,5,3), #435 C(40,16,7), #407 C(57,14,3), #398 C(68,14,5), #397 C(94,13,5), #211 C(41,12,5)
regex (35,5,3)|C(35 over all titles+bodies: no hits
search/issues q=repo:elder-plinius/V3R1T4S "35,5,3": total_count 0
```

## 6. Hobbyist repo thebrockchain/covering-designs
```
api.github.com/repos/thebrockchain/covering-designs/git/trees/HEAD -> HTTP 301 (renamed), followed once to repositories/1326363899
2026-10-20T16:38:17Z HTTP 200
brockchain files 12
['CLAUDE.md', 'LICENSE', 'README.md', 'linkborn.tokens.css', 'records', 'records/C28_13_4_53blocks.txt', 'records/C32_13_4_95blocks.txt', 'reference', 'reference/C28_13_4_54blocks_Fadlaoui2008.txt', 'reference/C32_13_4_96blocks_Fadlaoui2009.txt', 'src', 'src/verify.py']
```
No (35,5,3) file. (GitHub code search requires auth: HTTP 401, not retried.)

## 7. Literature / web (last 24 months)
Web searches for "C(35,5,3)" covering 732, arXiv 2025-2026 t=3 k=5 covering upper bounds, Kramer-Mesner/orbit covering records, GitHub "35,5,3", and 35-number 5-per-ticket "3 if 3" lottery wheels found: only the LJCR/coveringrepository value 732; 2026 papers on C(12,6,4)=41, C(16,5,3)>=62, a fifteen-cell audit (cells v<=20), and Numaro's derived-cell records (C(92,7,4) etc.), none touching (35,5,3). One search-engine summary asserted a "35-number 3 if 3 wheel with 174 tickets"; the cited page's table has no 35-number entry and 174 < Schonheim 658, so it cannot be the same object (it is a different guarantee or a summarizer error). No claim at or below 732 was found anywhere.

## Verdict
novelty: 713 is strictly below every value found: live coveringrepository.com 732 (honest reads at 16:37Z), Zenodo LJCR v1.2 732, dmgordo/LJCR GitHub 733; no lower claim in the repo, its PRs, the hobbyist repo, or the literature. Margin 19 blocks.
pass: true
