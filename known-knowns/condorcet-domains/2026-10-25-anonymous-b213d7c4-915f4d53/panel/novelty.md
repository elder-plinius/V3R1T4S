# NOVELTY review

context: fresh subagent

Review scope: one prospective claim only: `claim/assignment.txt`, n = 25, claimed |D(A)| = 180870896, SHA256 `915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b`. Candidate inputs were confined to `claim/`; no local attempts, notes, other local panel reports, or search-author reasoning were inspected. Public comparison PR text was used only for prior-claim count and status metadata, never as independent soundness or novelty authority. This review decides novelty only; the separate soundness review must establish the count.

The coordinator requested the saved verification route gpt-6.1-sol / xhigh. No descendants were launched. Frozen run start: 2026-10-25 17:20:06Z; new-work cutoff: 18:35:06Z; hard deadline: 18:50:06Z. This agent began verification at 18:36:11Z, after the cutoff. All work here was bounded verification and source search; no research search, heavy process, benchmark computation, outward submission, or policy/pinned-repository edit was performed.

## Required fresh status and table check

I made exactly one approved plain HTTPS GET to the status URL and, after finding that v1 was the only version in its submission history, exactly one distinct GET to the latest-v1 HTML resource. Both used `/usr/bin/curl -q` with its normal identity, GET, HTTPS only, 10-second connection/30-second total caps, no cookies, no retries, and no redirect following. No previous failure, challenge, redirect, or block was worked around.

| Resource | UTC request start–end | Actual HTTP / curl exit | Raw bytes | SHA256 |
|---|---|---|---:|---|
| https://arxiv.org/abs/2601.07336 | 18:36:28.608783–18:36:28.761824Z | 200 / 0 | 41568 | `5d57174029ffee102f9ea40ec0c18386c28c76987619a73c2b0a7ef2b620608b` |
| https://arxiv.org/html/2601.07336v1 | 18:36:53.790698–18:36:53.944541Z | 200 / 0 | 330995 | `a018d41785d2594aca2ffb57a28eb3e596acda1469395452e565aa4c268fb93a` |

All times above are 2026-10-25 UTC. The abstract response identifies v1, submitted 2026-01-12 09:03:12 UTC, as its sole version. The HTML is the named paper and contains Table 4, “Maximum size of Condorcet domains.” Its n = 25 entry in **f(n) & h(n)** is **≥160316046 (ks)**. The Fishburn column is 84990640; the formula column is 195312500. Those are different quantities and neither replaces the criterion's f(n) & h(n) comparison. Exact raw bodies, response headers, client stdout/stderr, receipts, extracted text, and the exact n25 row are in `panel/novelty-source/`. HTTP cache-age headers are preserved; these were actual fresh client requests to the origin URL, not substituted local saved extracts.

## Fresh comparison search

The following checks were made independently during 18:36–18:39Z:

- GitHub connector query `repo:elder-plinius/V3R1T4S condorcet`, state all, topn 100, sorted updated: 12 results (PRs 378–389). The matching open-state query also returned all 12. The only n25 package is [PR389](https://github.com/elder-plinius/V3R1T4S/pull/389), by psmoros, currently **open**, unmerged, updated 2026-10-24 16:14:46Z, head `9573bcf8d98bebff42c6d82fe1e7c481dd103c27`. Its claimed n25 size is **178950728**. The smaller-n claim-family counts were checked as comparison metadata; no same-n value equal to or larger than 180870896 was found.
- [Current TROPHY_CASE.md](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md), connector blob SHA `571f24117c6b128ffe751a39f22fcab68c498e66`, contains zero Condorcet matches. The current `known-knowns/` directory listing has no `condorcet-domains/` entry; a direct connector request for that path returned 404 Not Found. The complete connector responses are saved. Connector HTTP status/bytes are unavailable except that explicit 404; no HTTP metadata is invented.
- Fresh arXiv/web queries covered the last 24 months (2024-10-25 through 2026-10-25), explicit 2025–2026 literature, largest/record/25-alternative variants, the exact candidate number with and without commas, and exact existing comparison numbers. The actual returned search responses are saved, with literal email addresses omitted from the derivative literature log. A broader global GitHub query was capped at 100 and returned unrelated uses of Condorcet; it is not used as exhaustive coverage.

The primary recent literature found was:

| Source | Relevant scope / numerical comparison |
|---|---|
| [Karpov, Markström, Riis, Zhou (2026), arXiv:2601.07336](https://arxiv.org/abs/2601.07336) | Required latest Table 4, n25 = 160316046, checked from raw HTML above. |
| [Coherent domains and improved lower bounds (2025), DOI 10.1016/j.dam.2025.03.007](https://doi.org/10.1016/j.dam.2025.03.007) | Set-alternating constructions and asymptotic base 2.1973; the 2026 paper's improved table already incorporates the earlier construction context. The publisher direct open returned 403; no retry or alternative-client request was made to that resource. Publisher search excerpts and author-repository results were available as search data. No larger n25 value was found. |
| [Zhou and Riis (2025), DOI 10.1007/s10288-025-00583-1](https://doi.org/10.1007/s10288-025-00583-1) | Record sizes 1082 for n10 and 2349 for n11, below the later table for those n and no new n25 claim in the inspected material. |
| [An orderly algorithm for generation of Condorcet Domains (2025), arXiv:2509.20865](https://arxiv.org/abs/2509.20865) | Orderly enumeration and subclasses; primary abstract inspected. No competing n25 count found. |
| [Coxeter Condorcet domains (2026), arXiv:2606.01690](https://arxiv.org/abs/2606.01690) | General Coxeter-group structure, root posets, connectivity and tilings; primary abstract inspected. No competing n25 count found. |
| [Outer Diversity of Condorcet Domains (2026), arXiv:2610.00720](https://arxiv.org/abs/2610.00720) | Swap-distance diversity, numerical work on few candidates and asymptotics; primary abstract inspected. No competing n25 count found. |

Author research/data search results also led to the current seven-alternative Condorcet atlas, which enumerates seven-alternative representatives and supplies no n25 improvement. Search discovery used secondary listings only to locate primary work; no secondary numerical claim was substituted for a primary record.

## Decision and limits

The candidate exceeds the live latest Table 4 lower bound by **20554850**, and the largest existing same-n public claim found (PR389) by **1920168**. I found no published, merged, open-PR, current trophy, or current known-knowns n25 value ≥180870896. The candidate assignment identity was independently checked at 18:39:19.400575Z: 27416 bytes, 2300 well-formed conditions, every triple exactly once, matching the claimed SHA256. No mathematical count proof is implied by that format check.

This is a genuine strict numerical improvement over every same-n value found by the required current checks. The conclusion is bounded by the indexed sources and public records searched; it asserts no optimality and cannot exclude an unpublished or unindexed larger domain. The required table check is complete, so PENDING TABLE CHECK does not apply. Numerical soundness remains the separate review's responsibility.

Facts without this verdict are available in `panel/novelty-source/source-facts.json` for the coordinator and fresh CRITERION review. Report completed before 2026-10-25 18:41:30Z.

pass:true

