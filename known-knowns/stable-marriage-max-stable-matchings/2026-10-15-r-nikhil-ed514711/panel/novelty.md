# Novelty check: order-15 stable marriage instance with 30362 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)
role: NOVELTY skeptic of the V3R1T4S three-skeptic panel (novelty only; the count 30362 itself was NOT recomputed here)
client: curl with User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)" and -w '%{http_code}'; one plain
request per URL, no retries, no redirects followed, no cookies; `date -u` recorded immediately before each request.
No request returned 401/403/429/503 or a challenge page.
Saved responses (paths relative to the claim folder): ../panel/scratch_novelty2/dl_*/

## Fetches, in the order made

1. arXiv API (the only arXiv request of this check; made first)
   - URL: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
   - UTC 2026-10-15T03:19:31Z, HTTP 200 (application/atom+xml)
   - value: `<opensearch:totalResults>6</opensearch:totalResults>`. Only one entry falls in the last 24 months:
     arXiv:2601.14195v2 "A Minimax Perspective on Almost-Stable Matchings" (published 2026-01-20, updated 2026-09-02). It is
     about minimising blocking pairs per agent and gives no order-15 count. The other five (1711.01032, 1804.09156,
     1805.09887, 1905.06626, 1910.07159) date from 2017 to 2019, and none states an order-15 value.
   - sha256 0e2dcfc73980000e29b6bb66e941a2bc44b6d277ce3fc8237e8f9a8390e07a03 (CLAIM.md states none)

2. Status source: instance file of OEIS A357271
   - URL: https://oeis.org/A357271/a357271_1.txt
   - UTC 2026-10-15T03:20:34Z, HTTP 200 (text/plain, 11018 bytes, Last-Modified: Fri, 16 May 2025 17:50:14 GMT)
   - quoted line 15: `lb(15)=27059 (previously 25011, or 26424 shown in A371810)`
   - quoted block header: `/* Order 15 example with 27059 SM`
   - sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47: EQUAL to the sha256 stated in CLAIM.md,
     and byte-identical (cmp) to a357271_1.txt in the claim folder.

3. OEIS A357271 entry (internal text format)
   - URL: https://oeis.org/search?q=id:A357271&fmt=text
   - UTC 2026-10-15T03:20:50Z, HTTP 200
   - 15th term of the data line (offset 1, so a(15)): 25011, from
     `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,`
   - revision line: `%I A357271 #23 May 26 2025 15:56:20`
   - "Improved lower bounds" comment: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`
   - sha256 fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143. CLAIM.md states no sha256 for this file;
     it is byte-identical (cmp, same sha256) to A357271.txt in the claim folder.

4. Related OEIS entries (one request each)
   - https://oeis.org/search?q=id:A371810&fmt=text, UTC 2026-10-15T03:21:09Z, HTTP 200: a(15) = 26424
     (`%I A371810 #15 May 17 2025 19:22:52`; the entry itself notes "it is likely this sequence which is incorrect").
     sha256 fb71c17c72ac94a4b56bc61fde7ff1faecb0c275117da713a8e4b0ea60cefa06 (CLAIM.md states none)
   - https://oeis.org/search?q=id:A069156&fmt=text, UTC 2026-10-15T03:21:16Z, HTTP 200: a(15) = 25011
     (`%I A069156 #6 Aug 09 2019 12:31:00`). sha256 a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61
     (CLAIM.md states none)

5. Zenodo API
   - URL: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
   - UTC 2026-10-15T03:21:22Z, HTTP 200
   - value: total 1, namely 10.5281/zenodo.23329599, M. Jo, "A computer-assisted proof that the maximum number of stable
     matchings of order seven is 85" (created 2026-10-13). It covers order 7 only. The record JSON contains none of
     "15", "27059", "27510" or "30362".
   - sha256 0a667f53edafc3ecb648df249b2bf1498833f95fb7c62420c7aaa36f57244d0d (CLAIM.md states none)

6. Open pull requests of https://github.com/elder-plinius/V3R1T4S
   - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   - UTC 2026-10-15T03:21:48Z, HTTP 200. 30 open PRs on a single page (no Link header). Titles and bodies were searched
     for stable marriage/matching, A357271/A357269, order 15/n = 15, 27059, 27510 and 30362.
   - #144 (draft, created 2026-10-14T17:31:38Z), https://github.com/elder-plinius/V3R1T4S/pull/144:
     "[claim] stable-marriage-max-stable-matchings: order-15 instance with 27510 stable matchings (beats 27059)".
     Its object sha256 is 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8. That differs from this
     claim's instance_n15.prefs, sha256 ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef (recomputed;
     equal to CLAIM.md).
   - #147 (draft, created 2026-10-15T03:18:16Z): order-18 instance with 530528 stable matchings. It gives no
     order-15 value.
   - No other open PR concerns stable matchings.

7. Web searches (agent web search tool, about 2026-10-15T03:22:15Z, 2 queries)
   - "maximum number of stable matchings order 15 new lower bound instance": arXiv 2011.00915 (3.55^n upper bound),
     1711.01032, 2011.13248, a University of Washington thesis "Pairing Things Off: Counting Stable Matchings, ..." (not
     opened), a DIMACS seminar page and a Claremont page. No result states an order-15 value.
   - "\"stable marriage\" 15 men 15 women \"stable matchings\" record 27059": nothing mentions n = 15 or 27059.

TROPHY_CASE.md of the repository (local checkout; path relative to the claim folder: ../../../repo/TROPHY_CASE.md): it
has no stable-marriage family and no order-15 stable-matching row.

## Decision for n = 15

| source | order-15 value | is 30362 strictly greater? |
|---|---|---|
| open draft PR #144 (same research workspace, 2026-10-14) | 27510 | yes, +2852 |
| OEIS A357271 instance file, lb(15) (Ong, Ang, Ho, Eilers, Marks, Buzi 2025) | 27059 | yes, +3303 |
| OEIS A371810 a(15) | 26424 | yes |
| OEIS A357271 data line a(15), OEIS A069156 a(15) | 25011 | yes |
| arXiv (last 24 months), Zenodo, web searches, TROPHY_CASE.md | no order-15 value found | n/a |

30362 strictly beats 27510, the value of open draft PR #144. It is not a tie. It also strictly beats the best
published value, 27059, the bar named in CLAIM.md. Nothing newer than the status source contradicts it: the only
newer order-15 value is PR #144's 27510.

Caveats:
- The OEIS pages are not fully current for every n. For n = 7 the Zenodo preprint (f(7) = 85) is newer than lb(7)=81.
  For n = 15 nothing newer than PR #144 turned up.
- The rules allowed one arXiv query. It matched only abstracts that contain both phrases, so literature coverage
  beyond it rests on the Zenodo query and two web searches.
- This verdict covers novelty only. If the count 30362 is wrong, the verdict does not stand.

novelty: STRICT RECORD for n = 15 (30362 > 27510 [open PR #144] > 27059 [OEIS A357271 file])
pass: true
