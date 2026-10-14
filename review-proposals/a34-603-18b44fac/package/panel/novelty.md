# Independent NOVELTY review

context: fresh invocation; canonical agent id /root/novelty; fork_turns=none.

Invocation identifier available to this reviewer: /root/novelty. No separate opaque invocation UUID or exportable transcript URL/path was exposed. Transcript reference: unavailable. The JSON evidence files below preserve the substantive retrieval requests, returned results, and UTC timestamps; they are not a complete platform transcript.

Independence: I read only the supplied claim.md and status_source.md, the NOVELTY.md role protocol, and the candidate bytes for a hash check from the permitted handoff. I did not read another reviewer report, an author solution note, the staging archive, or parent reasoning. This was a fresh model context within a shared filesystem, not OS isolation, a different model vendor, an external reviewer, or human peer review. I did not communicate with other reviewers.

## Verdict

PASS for the NOVELTY source-comparison gate as checked on 2026-10-14. The proposed size 603 strictly exceeds the highest relevant explicit bound found, 602, and does not exceed the tabulated upper bound 1175. No tie or stronger competing target-cell claim was found in the searched sources or open repository PRs. This verdict does not independently certify the 603-word object's mathematical validity, which is a separate role.

The claim's success criterion was read: strictly exceed the verification-time table lower bound, its complement mirror, the two named arXiv papers and newer arXiv results; do not exceed the table upper bound. Searches covered 2024-10-14 through 2026-10-14, with additional searches after 2026-08-14.

## Primary status and mirror

Primary URL: https://aeb.win.tue.nl/codes/Andw.html

One direct URL open was issued, at 2026-10-14T02:42:41.645Z, completed 2026-10-14T02:42:44.526Z. It succeeded; no blocked response was retried. The returned reference was turn1view0, reported crawled today and 828 lines. Its initial response excerpt stopped before the target section. I subsequently used find on that already obtained reference, rather than opening the URL again, to inspect the target section and mirror notation. Those cached-reference inspection calls are disclosed in status_cached_inspection.json and mirror_cached.json. The provider's internal HTTP/cache behavior and HTTP headers are not observable; I claim one direct URL-open request, not independently audited counts of underlying HTTP requests.

At lines 433–435, the n=34 column of A(n,8,7) reads “601” with Bo attribution, followed by upper bound “1175”. Thus 603 > 601 and 603 <= 1175.

There is no separately displayed weight-27 target cell in this table's distance-8 layout. Complementation is a bijection on binary vectors, changes weight 7 to 27 in length 34, and preserves every Hamming distance. Therefore A(34,8,27)=A(34,8,7), and the same bounds apply to the mirror. I searched both parameter spellings in the literature and checked the repository table/index for both; no separate stronger mirror claim was found. The search engine can return approximate irrelevant matches, so absence of a search hit alone is not a proof of absence.

## Comparison evidence

| Source | Observed target comparison |
|---|---|
| Brouwer live table | 601–1175 |
| Echols arXiv:2608.13906v1, Table 1 line 87 | prior 594, new 600 for (34,8,7) |
| Lysenstøen arXiv:2607.19550v1, abstract and section 5 | four improved distance-6 cells at lengths 23 and 24; no (34,8,7) or complement entry |
| V3R1T4S TROPHY_CASE.md row 26 | 602 for (34,8,7) |
| V3R1T4S current bigger-codes/INDEX.csv | 602, external comparator 601, upper 1175, Echols 600 |
| Open V3R1T4S PRs | two PRs, neither a competing constant-weight-code claim |

Primary paper URLs:
- https://arxiv.org/html/2608.13906v1
- https://arxiv.org/html/2607.19550v1

Repository URLs:
- https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md (fetched blob SHA 6c7a0eb8e13da49031ea2df7ff6d8070a9374469)
- https://github.com/elder-plinius/V3R1T4S/blob/main/known-knowns/bigger-codes/INDEX.csv (blob SHA a9116526aef533c26eb7bfb5417bcf55a6e4fee1)
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100

The PR collection returned two entries, numbers 1 and 2, below the 100-entry page size: #1 fixes malformed null-control counts; #2 claims a matrix-multiplication scheme. I inspected their titles and bodies. Neither concerns this target. The returned base SHA was 7aca3835635e5323b48cdf3b5b59fcde502cab28.

## Recent literature

I searched both available search engines; exact query strings and the full returned responses are retained in literature_search.json and search_round2.json. Primary sources were used for substantive conclusions.

- Rosin, arXiv:2603.00174, https://arxiv.org/pdf/2603.00174: Table 1 lists its 24 improved cells, with no target or mirror entry. Evidence: yang_abs_rosin.json.
- Yang et al., arXiv:2609.35051v1, https://arxiv.org/html/2609.35051v1: Theorem 5.4 and Table 3 give weight-8 support families, including A(34,8,8)>=1960. This is a different weight. No weight-7 target result was found. Evidence: yang_full.json and yang_cells.json.
- Akhiiarov et al., arXiv:2609.23869v2, https://arxiv.org/abs/2609.23869: abstract concerns upper-bound envelopes, not an explicit lower-bound construction for this cell.
- Chee, arXiv:2610.10973v1, https://arxiv.org/abs/2610.10973: abstract concerns asymptotically optimal invariant packings; it does not supply a finite (34,8,7) value.

Unversioned HTML requests for Yang and Rosin initially returned DisabledError; Yang's unversioned PDF also returned an internal error. I resolved paper content through Yang's successfully linked versioned HTML and Rosin's PDF. These were literature retrievals, not retries of the primary status source. The two newest general/asymptotic papers were screened at abstract level, not subjected to a full theorem-by-theorem derivation audit.

No finite literature search proves universal unpublished priority. This pass means the required public-source search and comparisons found 603 strictly above the known relevant explicit values; it is not a claim of community acceptance or a novel search method.

## Audit files and sign-off

All evidence is under validation/novelty/. Each JSON file contains exact tool request arguments and returned source text. Cached-page find/open commands are included, including failures. trophy.txt and repo_index.txt are extracted verbatim connector file contents for easy local inspection.

Candidate hash independently read: 18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad, matching claim.md. No all-pairs validity computation is claimed by this review.

Signed off by /root/novelty, an AI reviewer in a fresh context, on 2026-10-14. Evidence retrieval interval: 02:42:41.645Z–02:44:24.451Z. Report delivery path overrides the protocol's generic panel/novelty.md path as explicitly directed by the parent.

pass: true
