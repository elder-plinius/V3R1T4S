context: Claude Code subagent, fresh context [Sonnet 5.5]

novelty: PASS (nothing found that reaches 2.006 with at most 15 columns, or above 2.05956508661)

Status source, read once (2026-11-17T15:05:31Z, https://teorth.github.io/optimizationproblems/constants/24a.html, HTTP 200, sha256 1458e39f...96ac; the raw markdown https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/24a.md at 15:05:32Z, HTTP 200). The lower-bound table lists exactly two rows: "1, Trivial (n=1, A=[1])" and "1+sqrt(2), [Kun2023], Best known lower bound on C_24." There are no small-n entries and nothing for at most 15 columns. The page's status line says verified bounds are 1+sqrt(2) <= C_24 <= 36. So the page does not contradict the claim; it is simply silent on small n.

Kunisky arXiv:2111.02974 (abs fetched 15:05:32Z; PDF https://arxiv.org/pdf/2111.02974 fetched, HTTP 200). Section 1 says: "Daniel Spielman recently communicated that an extensive numerical search yielded an (unpublished) example with n = 15 and Delta(A) in [2.005, 2.006]. To the best of our knowledge this is the state of the art at the time of writing." Theorem 1.1: K(2^k) >= 2^{-k/2} + sum_{a=1..k} 2^{-a/2}, so K >= 1+sqrt(2). For k=4 (16 columns) that gives about 2.0607, the first certified value above 2 from the tree matrices. This agrees with the claim's description. (Kunisky's text is a PDF-to-text extraction; the formula was garbled but readable.)

Pull requests and issues of teorth/optimizationproblems (GitHub API, 15:05-15:07Z, HTTP 200): the newest 100 PRs (#263 to #373, all states) contain none about constant 24 except closed #250 ("C_24: Komlos conjecture proved, upper bound 36") and closed #60 ("Update constant 24a", an older issue/PR hit). Searches "24a", "Komlós" and "Komlos" within the repo returned only #250, #252 (an unrelated Ramsey constant), #43 (an unrelated Littlewood-Offord constant), #352 (unrelated), #60 and #81 (unrelated). No open PR touches 24a or proposes a small-n bound. I did not read PR #250's body for any small-n matrix; the title concerns only the upper bound. Older PRs beyond the newest 100 were reached only through the search queries above.

Literature (arXiv API queries, https://export.arxiv.org/api/query, 15:07Z, HTTP 200 each, sorted by date):
- all:Komlos AND all:conjecture: newest are 2609.27172v2 (Akbas-Sra, upper bound), 2508.03961 (Bansal-Jiang, upper bound), 2404.03534 (Gram-Schmidt walk remarks), 1301.4039 (vector colorings). Nothing on lower bounds for small n.
- all:"vector balancing" AND all:"lower bound": online-discrepancy and polarization-constant papers; none gives a Komlos matrix.
- all:Kunisky AND all:discrepancy: Kunisky's own average-case matrix discrepancy papers (2022 to 2024) and 2609.11836 (free-probabilistic random matrix discrepancy); none reports an explicit 15-column matrix above 2.006.
- The query all:Komlos AND all:discrepancy AND all:lower returned zero entries.
The page's own reference list (read in full for the upper/lower tables) cites no work after Kun2023 on the lower side. I did not open the full text of every hit, and no Google Scholar access was available, so coverage of non-arXiv venues and of citations of Kunisky beyond these queries is limited. I did not check the suvrit/komlos certificates repository.

V3R1T4S repository (elder-plinius/V3R1T4S, GitHub API, 15:07Z): TROPHY_CASE.md fetched (HTTP 200, 31306 bytes, sha256 in a working copy (not shipped)); it contains no mention of Komlos, Komlós or 24a. The known-knowns folder lists 39 entries (bigger-codes through vnncomp-2026-unsolved-instances); none concerns Komlos or discrepancy. Issue/PR search for "komlos" in that repo returned 0 results; the newest 100 PRs include no title with Komlos or 24. Code search returned 401 (requires authentication); I did not retry, so the code-search route is a fail, covered by the other checks.

Assessment: the only previous record for at most 15 columns is Spielman's unpublished [2.005, 2.006]; the claimed 2.05956508661 strictly exceeds its top end of 2.006, and no later source I found reaches either. It is below Kunisky's 16-column 2.0607, which is outside the p2 scope (more than 15 columns). Caveat: Spielman's interval is numerical and unpublished, so the claim beats a reported figure, not a verified object; and absence of a later result is not proof. Whether the matrix itself is correct is for the other skeptics.

All fetches (UTC time, URL, status, sha256) are in a working file (not shipped) in my scratch folder.

pass: true
