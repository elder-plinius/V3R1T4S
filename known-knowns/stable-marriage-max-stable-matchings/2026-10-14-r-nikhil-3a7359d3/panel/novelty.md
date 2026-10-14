# Novelty skeptic verdict: stable-marriage-max-stable-matchings, cell n = 15, claimed 27510

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Role: NOVELTY skeptic. Read only claim/CLAIM.md. claim/a357271_1.txt was used only for a byte and hash comparison. claim/instance_n15.prefs and claim/ong_n15_published_27059.prefs were used only for a byte comparison. Also read the repo's TROPHY_CASE.md, as instructed.
Client: curl, User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)", `-w '%{http_code}'`, no cookies, no browser imitation. One request per page, no retries. `date -u` was recorded before each fetch. No fetch returned 401, 403, 429, 503 or a challenge page.
Scratch copies are in panel/scratch_novelty/.

## 1. Status source (record instance file)
- URL: https://oeis.org/A357271/a357271_1.txt
- UTC time: 2026-10-14T15:32:16Z. HTTP code: 200 (text/plain, 11018 bytes, Last-Modified: Fri, 16 May 2025 17:50:14 GMT)
- Quoted lb(15) line: `lb(15)=27059 (previously 25011, or 26424 shown in A371810)`
- File header: "Improved Hill Climbing for the Stable Marriage Problem", Ong, Ang, Ho, Eilers, Marks, Buzi, 2024-11-01, IFoRE 2024
- Saved copy: panel/scratch_novelty/f1/a357271_1.txt
- sha256 of the fetched file: 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47
- sha256 stated in CLAIM.md: 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47. EQUAL. The fetched file is also byte-identical to claim/a357271_1.txt.

## 2. OEIS entry A357271
- URL: https://oeis.org/search?q=id:A357271&fmt=text
- UTC time: 2026-10-14T15:32:28Z. HTTP code: 200. Revision line: `%I A357271 #23 May 26 2025 15:56:20`
- a(15) = 25011. This is the 15th term of `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,...`; Thurber 2002 composition bound.
- Quoted comment: "Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file."
- Link text: "Improved lower bounds for n=7, 9, 11, 13, 15", Ong, Ang, Ho, Eilers, Marks, and Buzi, 2025, pointing to a357271_1.txt (section 1, lb(15)=27059).

## 3. Other OEIS cross-checks (one request each)
- https://oeis.org/search?q=id:A371810&fmt=text (2026-10-14T15:33:01Z, HTTP 200): a(15) = 26424. This sequence counts pseudo-Latin matchings in Thurber's matrix. The entry itself says "it is likely this sequence which is incorrect".
- https://oeis.org/search?q=id:A357269&fmt=text (2026-10-14T15:33:01Z, HTTP 200): the exact maximum is known only for n <= 5 (`1,2,3,10,16`). No order-15 value.
- https://oeis.org/search?q=id:A069124&fmt=text (2026-10-14T15:34:15Z, HTTP 200): a(15) = 13536.
- https://oeis.org/search?q=%22stable+matchings%22&fmt=text (2026-10-14T15:34:16Z, HTTP 200): 49 results, of which I read the first page of 10.
  - A069156 has a(15) = 25011.
  - A351413 (Latin variant) goes only to n = 7.
  - The other sequences on that page count preference profiles; none is a lower-bound table above 27059 for n = 15.

## 4. Literature, last 24 months
- arXiv API: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
  - 2026-10-14T15:32:49Z, HTTP 200, totalResults 6.
  - The only item from the last 24 months is arXiv:2601.14195 (almost-stable matchings, minimax blocking pairs). It does not count stable matchings.
  - No order-15 value.
- arXiv API: https://export.arxiv.org/api/query?search_query=all:%22number%20of%20stable%20matchings%22&sortBy=submittedDate&sortOrder=descending&max_results=50
  - 2026-10-14T15:33:02Z, HTTP 200, totalResults 12.
  - arXiv:2607.10306 (2026-07, regular anti-phase group templates) gives a counting lower bound in terms of subgroup indices. The abstract says it is sharp only for groups of order <= 5 and states no order-15 value.
  - arXiv:2507.20013, 2507.14362, 2505.06717 and 2409.04885 are on other topics.
  - No order-15 value.
- Zenodo API: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
  - 2026-10-14T15:32:50Z, HTTP 200, total 1.
  - The one hit is 10.5281/zenodo.23329599 (2026-10-13), "A computer-assisted proof that the maximum number of stable matchings of order seven is 85". It covers order 7 only and states no order-15 value.
- Zenodo API: https://zenodo.org/api/records?q=%22stable%20marriage%22%20OR%20%22stable%20matchings%22&size=25&sort=mostrecent
  - 2026-10-14T15:34:49Z, HTTP 200, total 46. I read the 25 most recent.
  - Recent records found:
    - order-7 f(7)=85 (above)
    - 10.5281/zenodo.22909380 (2026-09-23, order six, f(6)=48)
    - 10.5281/zenodo.23130297 and 10.5281/zenodo.23226065 (2026-10, prime factorisation of instances)
    - 10.5281/zenodo.23308285 (2026-10-12, complexity)
  - The rest are unrelated. None mentions 27059, 27510 or an order-15 count. The "fifteen" hits refer to rotation posets of order 6.
- Two web searches, run between 15:33:02Z and 15:34:15Z UTC:
  - Query 1: `"stable matchings" new lower bound order 15 stable marriage maximum number 2025 2026`
  - Query 2: `maximum number of stable matchings stable marriage instance n=15 27059 OR 27510 OR "hill climbing" record`
  - Results were only older literature: the Karlin, Oveis Gharan and Weber c^n upper bound (2017), the 3.55^n upper bound (2020), Thurber 2002, and surveys. No source mentions 27059, 27510 or any order-15 value.

## 5. TROPHY_CASE.md and open pull requests
- TROPHY_CASE.md (local repo file, 100 lines) has no stable-marriage, stable-matching or A357271 entry. The only hits for "stable" and "matching" are in an unrelated RobustBench row and an unrelated degree-diameter row.
- Open PRs: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
  - 2026-10-14T15:32:59Z, HTTP 200, 11 open PRs, so no pagination was needed.
  - PRs #1, #8, #9, #28, #30, #31, #78, #124, #125, #126 and #127 cover: packomania hyperspheres, Thomson problem (4 PRs), constant-weight codes, an A(34,8,7) review, and verifier/harness fixes.
  - None concerns stable marriage, stable matchings or A357271.

## 6. Decision
- Order-15 values found:
  - 27059: the published best, from Ong et al. 2025, the status source linked from OEIS A357271.
  - 26424: A371810.
  - 25011: A357271 a(15) and A069156.
  - 13536: A069124.
- No source from the last 24 months has an order-15 value at or above 27059. The only newer work on f(n) concerns n = 6 and n = 7.
- The claimed 27510 is above the best known 27059 by +451 (+1.67 %). This is a strict improvement, not a tie, and nothing newer contradicts it.
- Scope: this is a novelty verdict only. I did not recompute the exact count of claim/instance_n15.prefs; correctness belongs to another panel member.
- claim/instance_n15.prefs is not byte-identical to claim/ong_n15_published_27059.prefs. Isomorphic instances have equal counts, so if 27510 is confirmed, the instance cannot be a relabelling of the published 27059 instance.
- The novelty pass therefore depends on the count 27510 being confirmed.

pass: true
