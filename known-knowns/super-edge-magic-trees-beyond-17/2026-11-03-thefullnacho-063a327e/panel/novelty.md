# Panel: NOVELTY

context: fresh-context subagent, saw package only
date: 2026-11-03 (UTC), work between 12:47Z and 12:55Z

## Procedure (written out before starting; kit/RUN.md step 6, NOVELTY)

1. Fetch the status source honestly (plain curl, User-Agent "V3R1T4S") and check that the-record-we-beat/RECORD.md
   quotes it accurately: edition, page, sentence, reference, hash.
2. Search for prior art at or beyond 18 vertices under every equivalent name: super edge-magic, strong(ly) edge-magic
   (Wallis), strongly indexable / strongly 1-indexable (Acharya-Hegde), super (a,0)-edge-antimagic total, consecutive
   edge sums, and sequential labelings (Grace; for trees DS6 4.3 says sequential = strongly k-indexable).
3. Sources: DS6 28th ed. full text; arXiv API; scholarly web search; MathOverflow / Math.SE (StackExchange API); OEIS;
   GitHub repository search; elder-plinius/V3R1T4S issues and PRs in every state, bank entry, TROPHY_CASE.md, known-knowns/.
4. Pass only if nothing at or beyond 18 vertices turns up.

## Status source and the record snapshot

- URL: https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/
- fetched 2026-11-03T12:47:14Z, one curl, HTTP 200, 3945134 bytes,
  sha256 b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e (identical to RECORD.md);
  header check 12:52:26Z: Content-Type application/pdf, Content-Length 3945134,
  Content-Disposition attachment; filename="27-PDF file-8928-26-10-20261021.pdf" (all as RECORD.md states).
- Landing page https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 fetched ~12:53Z: "This Version DS6:
  Oct 30, 2025". No newer edition. (Its abstract text says "55 additional pages and 308 new references" while the
  PDF title page says 94 and 445; a stale abstract, not a content signal.)
- Title page: "Twenty-eighth edition, October 30, 2025". Matches.
- Section 5.2, pdftotext: "Enomoto et al. [975] conjecture that every tree is super edge-magic. Lee and Shan [2075] have
  verified this conjecture for trees with up to 17 vertices with a computer." Matches RECORD.md word for word.
  It falls after the "#DS6 167" footer and before the "#DS6 168" footer, so printed page 168. Matches.
- Reference [2075] as printed: "S. M. Lee, and Q. X. Shan, All trees with at most 17 vertices are super edge-magic, 16th
  MCCCC Conference, Carbondale, University Southern Illinois, Nov. 2002." Matches.
- Record snapshot verdict: ACCURATE.
- Other computer bounds in DS6 for trees are for other labelings: graceful at most 35, harmonious at most 26
  (Aldred-McKay), prime at most 34, alpha-deficit tables to 26 (Brinkmann et al.). DS6 4.3 (k,d)-indexable section
  and 5.2 give no tree census for strongly indexable or SEM beyond Lee-Shan.

## Equivalence-based routes checked (could an older census imply SEM at 18+?)

- Graceful (35), harmonious (26/31): neither is known to imply SEM for trees. Not prior art.
- Alpha-labeling implies SEM (and sequential, Grace 1983). Brinkmann, Crevals, Melot, Rylands, Steffen (DMTCS 14,
  2012) tabulate alpha-deficit of all trees up to 26 vertices, but trees with positive alpha-deficit exist at every
  order in range, and the paper (full text grepped) says nothing about SEM, sequential or harmonious labelings of the
  deficient trees. Covers only a subfamily, so not prior art for "every tree".
- Sequential labelings of trees are exactly SEM. Closest lead: github.com/gexahedron/graceful-labeling (2024,
  unpublished notes) defines a "beta+seq" labeling, a subset of sequential labelings, and says "verified ... for all
  trees upto and including 15 or 16 vertices" (beta_plus_seq/README.md: "all trees on 15 vertices and less").
  That is below 17, so below the claim.

## Literature (searches run 2026-11-03)

- arXiv API, all fields: "super edge-magic" (11 hits, newest 2308.10661), "super edge magic" (same 11),
  "strongly indexable" (1, unrelated), "edge-antimagic" AND tree (0), "sequential labeling" (57, all ML/NLP except
  set-sequential odd trees 2011.13110, unrelated), "edge-magic" AND tree (1: 2211.04029), "magic labeling" AND trees.
  None reports a tree census past 17.
- Ichishima, Lopez, Muntaner-Batle, Takahashi, Theory Appl. Graphs 11(1) 2024 / arXiv:2211.04029: still cites 17.
- Raheem-Javaid, TWMS JAEM 10(3) 2020 (super (a,d)-EAT of trees): cites "at most 17 vertices".
- Enomoto, Llado, Nakamigawa, Ringel, SUT J. Math. 34 (1998): checked up to 15.
- Lopez and Muntaner-Batle, "Open problems involving super edge-magic labelings"; their 2017 Springer book
  (snippet only): no higher bound found.
- Bača, Miller, Ryan, Semaničová-Feňovčíková, "Magic and Antimagic Graphs" (2019): web summaries cite 17 only; the
  full text mirror was not readable (fetch blocked), so this book was not checked line by line.
- Web searches for SEM / strongly edge-magic / strongly indexable / super (a,0)-EAT verification at 18, 19, 20, 21, 22
  vertices, SAT/exhaustive SEM tree searches 2025-2026, and later extensions of Lee-Shan: nothing past 17.
- MathOverflow and Math.SE (StackExchange search API): "super edge-magic", "super edge magic", "edge-magic tree",
  "strongly indexable", "sequential labeling tree", "edge-antimagic": no relevant question or answer.
- OEIS: "super edge-magic" gives A060408 (counts of SEM labelings of (n,k)-graphs) and A177742; nothing
  tabulating SEM trees or a verification bound. "strongly indexable", "sequential labeling", "edge-antimagic
  total": nothing relevant.

## Code

- GitHub repository search: "super edge magic" (3 repos), "super-edge-magic" (2), "edge-magic labeling" (6),
  "edge magic tree", "superedgemagic", "strongly indexable". Relevant hits only lsmeng/super-edge-magic-spiders
  (spiders with equal legs, 2026-09-08, no all-trees census) and small EMTL solvers for paths/multipartite graphs.
  (Code search needs auth and was not used.)
- elder-plinius/V3R1T4S, read-only, HEAD 9a0d19a1 (2026-11-02T13:14:05Z): all 916 issues and PRs in every state
  (numbers 1..916, none missing) pulled at ~12:49Z and grepped titles and bodies for magic / sequential / indexable /
  edge sum / antimagic / Lee and Shan. No super edge-magic claim or discussion; nearest are #880 odd-graceful trees
  and #894 harmonious windmills (different labelings). Search API for "super edge-magic", "edge-magic",
  "super-edge-magic", "SEM trees", "strongly indexable", "Lee Shan": 0 each. TROPHY_CASE.md and known-knowns/ have no
  edge-magic entry. The bank entry known-unknowns/graphs-games-automata/super-edge-magic-trees-beyond-17.md says
  "open as of 2026-10-30" and warns that an unpublished extension past 17 may exist.

## Comparison

Published bound for "every tree on at most n vertices is super edge-magic": n = 17 (Lee and Shan 2002, still the
bound in DS6 28th ed., Oct 30 2025, the latest). Claim: n = 20. No prior art at or beyond 18 vertices found
under any equivalent name. The only all-trees census for an SEM-equivalent or stronger labeling (gexahedron
beta+seq) stops at 15 or 16. Strictly better than the published value.

## Residual risk

- The 17 bound is a 2002 conference talk. An unpublished or unindexed extension can't be ruled out by searching,
  and the bank says so too.
- Not read in full: the Bača et al. 2019 book (mirror blocked) and the Lopez and Muntaner-Batle 2017 book (paywalled).
  Web summaries of both cite 15 or 17 only.

verdict: NOVEL
pass: true
