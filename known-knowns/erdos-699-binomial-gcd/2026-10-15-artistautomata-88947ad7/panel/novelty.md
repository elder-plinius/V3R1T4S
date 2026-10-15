# Novelty skeptic: Erdős #699, claim "no counterexample for every n <= 10^9, verified exhaustively" (partial win p3)

context: subagent (fresh context, given only claim/)

Question: is an exhaustive check of every n with 4 <= n <= 10^9 strictly beyond everything known?
Scope: this verdict covers novelty only, not whether the computation is correct.

## Primary status fetches (one plain request each, UA "V3R1T4S", no retries)

| URL | UTC time | HTTP | saved as (claim/) | sha256 |
|---|---|---|---|---|
| https://www.erdosproblems.com/699 | 2026-10-15T00:13:42Z | 200 | fetched/status_699.html | 1882f3c2bf2174e76619073f6d5261f3f1508e3fcf2574e3e65ef02a6ae93c80 |
| https://www.erdosproblems.com/forum/thread/699 | 2026-10-15T00:13:42Z | 200 | fetched/forum_699.html | f33bfbe5a9b63148fe2c32e6f1c46d8732be3066a152f223771ef8346bd6e83f |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T00:13:43Z | 200 | fetched/TROPHY_CASE.md | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 |
| https://github.com/conglu1997/erdos_699_rust | 2026-10-15T00:13:43Z | 403 | fetched/cong_repo.html | (sandbox proxy refusal: "GitHub access to this repository is not enabled for this session") |
| https://export.arxiv.org/api/query?search_query=all:%22Erdos%22+AND+all:binomial+AND+all:gcd&max_results=20 | 2026-10-15T00:14:22Z | 200 | fetched/arxiv_search.html | 0 entries |

Text extracts: fetched/status_699.html.txt, fetched/forum_699.html.txt.

## What the sources say

- Status page (Thomas Bloom, "last edited 19 July 2026"): the problem is still open. Quote: "GPT 5.6 (prompted by Price)
  has proved that this is true if $j\leq \frac{3}{2}i$ or $n=2j$." The page reports no computation beyond the forum's.
- Forum thread: the largest exhaustive computation in the thread is Cong's, 01:45 on 06 Jan 2026. Quote: "I ran a Rust
  implementation to test the official statement ... up to n = 10^7; no counterexamples found. Targeted extensions: all
  n = 2^k for k ≤ 27 (n ≈ 1.34×10^8) and all n = 3^m + 1 for m ≤ 17 (n ≈ 1.29×10^8)." Later posts are theory only:
  Del Pin (24 Jul 2026) and MaxDKaos (25 Jul 2026), who writes "#699 remains open." One post is marked "[Post deleted]"
  (30 Apr 2026). Commenting is now suspended. No post reports an exhaustive range larger than n = 10^7.
- Web search (2026-10-15) gave an index snippet of a forum post claiming a resolution by "Parthasarathy" (under review).
  It reports exhaustive verification of "n ≤ 4400, i ≤ 23" and cites Cong's 10^7. That range is far below 10^9, and the
  post is not in the live thread; it is probably the deleted 30 Apr post.
- TROPHY_CASE.md: no match for "699", "binomial" or "Szekeres". The repository lists no earlier #699 result.
- Open PRs: a GitHub search for `repo:elder-plinius/V3R1T4S is:open 699` returned total_count 0.
- arXiv: the API query above returned no entries. Two general web searches found no paper from 2024 to 2026 reporting
  a search beyond 10^7.

## What I could not reach
- Cong's repository (github.com/conglu1997/erdos_699_rust): HTTP 403 from the sandbox proxy, and GitHub API access was
  denied for this session. I did not retry or work around the block. Its README could mention a later, larger run that
  was never posted on the forum. Nothing reachable suggests one: the forum post that announced the repo (10:53,
  06 Jan 2026) describes the 10^7 run.

## Verdict
The best known exhaustive bound is n <= 10^7, with targeted checks of special families up to about 1.34e8. Exhaustive
coverage of all n <= 10^9 is 100 times larger and strictly beyond every result I could reach, so this is not a tie.
novelty: CONFIRMED against the status page, the forum, TROPHY_CASE.md, open PRs and arXiv. Caveat: Cong's repository
could not be reached.
pass: true
