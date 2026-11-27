# The record we beat (metadata only)

No third-party page or PDF is copied into this package. The status source of this target refused an automated request with HTTP 403 on 2026-11-19, so both pages below were read once in a browser on 2026-11-27; how, and what was seen, is in `STATUS_CHECK_RECORD.md`. The hashes are of the text the browser rendered, not of an HTTP response.

| Source | URL | UTC time | HTTP status | sha256 of the rendered page text | Extracted status or value |
|---|---|---|---|---|---|
| T. F. Bloom, *Erdős Problem #7* (the target's status source) | https://www.erdosproblems.com/7 | 2026-11-27T01:16Z | read in a browser (see STATUS_CHECK_RECORD.md) | `8c5e4f5b93df9feb76cb41c0d2cdaad97e899c2070953550efa8a5789ad80a85` | Problem 7 listed as open ($25); no numeric lower bound on L stated; `Comments (23)`, `Proof claims (0)`, `Proof expositions (0)` |
| *Erdős Problem #7* discussion thread | https://www.erdosproblems.com/forum/thread/7 | 2026-11-27T01:16Z | read in a browser (see STATUS_CHECK_RECORD.md) | `47f93954e77ee11abbe25c8fa15ff9cdafcbdd5fdde82989588f17ed2aded405` | newest post dated 15 Sep 2026 (M. Schroeder, on at least nine prime divisors of L); the largest lower bound on L stated in the thread is 11,486,475 (post of 18 Aug 2026) |

Neither page contains the numbers 6,557,114,959,770,375, 168,131,152,814,625, 9,704,539,845 or 1,527,701,174 (`STATUS_CHECK_RECORD.md`).

**Compared baseline:** L >= 11,486,475 (Egeozturk, forum post of 18 Aug 2026), the bar named by the bank's partial win p2. The bound claimed here, 6,557,114,959,770,375, is 570,855,285 times that number.

**Other public bounds** (not re-fetched for this package; taken from the earlier checks made on 2026-11-18 and 2026-11-19 for the same contributor's earlier package on this target, and to be re-fetched by the novelty reviewer):

| Bound | Source | Earlier check |
|---|---|---|
| L >= 9,704,539,845 (Corollary 1.3, unrefereed) | M. Schroeder, *Nine prime divisors in odd distinct covering systems*, Zenodo, https://doi.org/10.5281/zenodo.22759614 (metadata at https://zenodo.org/api/records/22759614) | 2026-11-18T23:59:33Z, HTTP 200, sha256 `99da4ccea3947f333c0ea0214fe46c3d5e819276d373a260abffcac27c14475a` (metadata record) |
| L > 1,527,701,174 (Lean 4, kernel-checked) | https://github.com/rw762-sketch/Open-Math-problem (headline dated 2 Nov 2026) | 2026-11-19T12:03:23Z, HTTP 200, sha256 `dffa98d8f507daa829037db9075b786182bbcb40f115dfbc57e2d6b89c78aa1a` |
| L >= 168,131,152,814,625 | the same contributor's earlier package on this target in this repository (an open, unmerged pull request when this package was written) | not a fetched page |

## Fetches made by the novelty reviewer (added after the reviews)

| Source | URL | UTC fetch time | HTTP status | Size | sha256 of fetched response | Extracted status or value |
|---|---|---|---|---|---|---|
| T. F. Bloom, *Erdos Problem #7* (status source) | https://www.erdosproblems.com/7 | 2026-11-27T02:09:38Z | 200 | 35,524 bytes | `c354bb8e38af8aae8a48ec63c61030ee25c66277904d51b5a23490b1ad944624` | Problem 7 open; Comments (23); Proof claims (0); no numeric lower bound on L |
| M. Schroeder, *Nine Prime Divisors in Odd Distinct Covering Systems* (Zenodo record) | https://zenodo.org/api/records/22759614 | 2026-11-27T02:09:38Z | 200 | not recorded | `26974c80864dba7d4b3ec24adc387aa04daf5206b974525b058d6d579d1a0d49` | v1.0.1 is the only version; L >= 9,704,539,845 (unrefereed), the largest public bound the reviewer found |

