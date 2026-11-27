# Status page check

On 2026-11-19 the status source of this target answered an automated request with HTTP 403 (recorded for the same contributor's earlier package on this target; the single refused fetch was not retried). For this package, at the operator's instruction, both pages were therefore read in the operator's own Chrome browser before the reviews. The pages loaded normally, with no challenge page; no cookies, user agents or proxies were altered; nothing was posted. This machine read is disclosed here so that the maintainer can judge it.

Read on 2026-11-27 at 01:16 UTC:

| Page | What it shows | sha256 of the rendered page text | Length of that text |
|---|---|---|---|
| https://www.erdosproblems.com/7 | Problem 7 is listed as open ($25). The text states no numeric lower bound on the least common multiple L. It shows `Comments (23)`, `Proof claims (0)`, `Proof expositions (0)`. | `8c5e4f5b93df9feb76cb41c0d2cdaad97e899c2070953550efa8a5789ad80a85` | 1,740 characters |
| https://www.erdosproblems.com/forum/thread/7 | The newest post is dated 15 Sep 2026 (M. Schroeder, on at least nine prime divisors of L). The largest lower bound on L stated anywhere in the thread is 11,486,475 (post of 18 Aug 2026). | `47f93954e77ee11abbe25c8fa15ff9cdafcbdd5fdde82989588f17ed2aded405` | 15,609 characters |

The hashes are of the text the browser rendered (the page's visible text), not of the HTTP response, so they differ from the hashes of a raw fetch.

Neither page contains the numbers 6,557,114,959,770,375, 168,131,152,814,625, 9,704,539,845 or 1,527,701,174.

Nothing on either page has changed in substance since the check of 2026-11-19: the comment count is the same (23), and the newest post has the same date.

Added after the reviews: the novelty reviewer then made its own single ordinary request for the main page, which was answered this time: https://www.erdosproblems.com/7 at 2026-11-27T02:09:38Z, HTTP 200, 35,524 bytes, sha256 `c354bb8e38af8aae8a48ec63c61030ee25c66277904d51b5a23490b1ad944624`. Its text agrees with the browser read above (open, 23 comments, 0 proof claims, no numeric bound on L). The reviewer's request for the forum thread was not made (it was blocked on the reviewing machine before it ran, and was not retried), so what the thread shows rests on the browser read.
