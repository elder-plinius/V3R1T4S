# Novelty: the published exhaustive bound is still 12; n = 23 is new

context: subagent (fresh context; adversarial auditor of certificate format, literature and claim framing; did not read the author's generator, checker, run notes, or other skeptics' output)

Published exhaustive bound is still 12 vertices. I did not find a published or arXiv verification of all
trees past order 12, and I did not find any claim of order 23.

Gallian, A Dynamic Survey of Graph Labeling, Electronic Journal of Combinatorics DS6, 29th edition,
6 November 2026, Section 3.6, is the status source. The PDF was downloaded 2026-11-17T16:46:26Z from
https://www.combinatorics.org/files/Surveys/ds6/ds6v29-2026.pdf (HTTP 200; the article page
https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 is also dated 6 November 2026). After
the definition and the conjecture, the survey still says: "She conjectures that all trees are odd-graceful
and proves the conjecture for all trees with order up to 10. Barrientos [515] has extended this to trees
of order up to 12." Also recorded: every tree of diameter at most five is odd-graceful, and so are
caterpillars and caterpillar forests (Barrientos). There is no later "all trees of order n" bound in that
section. (The bank entry still cites the 28th edition, 30 October 2025; the live survey is now the 29th,
but the bound in Section 3.6 is unchanged.)

OEIS A000055, page and b-file fetched 2026-11-17T16:46:26Z, HTTP 200: "Number of trees with n unlabeled
nodes." b-file line "23 14828074". Independently recomputed via the Otter / Heinz recurrence, same value.

arXiv API, 2026-11-17T16:47:20Z, HTTP 200: 9 hits for "odd-graceful" OR "odd graceful", 2 of them also
matching "tree". None is an exhaustive verification past order 12. The only tree-enumeration paper in
that set is Barrientos, arXiv:0807.3738 (2008), diameter at most 5 and the order-12 extension. The most
recent hit, arXiv:2508.17799 (2025, v2), is about the odd-graceful chromatic number, not a census of all
trees.

GitHub, elder-plinius/V3R1T4S, read only, 2026-11-17T16:47:20Z to 2026-11-17T16:48:04Z, HTTP 200. Two
pull requests, both drafts, both by CharanRayudu, both claiming every tree on at most 22 vertices, not 23:
- #880, created 2026-11-01T12:15:38Z, closed unmerged at 2026-11-17T10:22:17Z by elder-plinius as a
  duplicate of #1007. Maintainer comment (6 November 2026): their own checker confirmed the certificates
  for orders 2..20 against A000055; they also read the 29th edition of DS6 and still found the bound 12;
  orders 21 and 22 were left for a later maintainer download. Closing comment: review continues on #1007;
  object files are byte-identical.
- #1007, open draft, created 2026-11-07T20:52:36Z, "resubmission of #880," same <=22 claim.

This repo's TROPHY_CASE.md and READ_BEFORE_CITING.md contain no odd-graceful entry.

So: the published record is still order 12 (Barrientos, as recorded in DS6 29th ed.). There is an
unmerged, still-draft claim of order <= 22 in PRs #880/#1007. Neither that claim nor the published
survey covers n = 23. The present certificate is not a tie with anything I found.

pass: true
