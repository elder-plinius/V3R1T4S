# Novelty skeptic: super-edge-magic-trees-beyond-17, claim "every tree on at most 22 vertices is SEM" (p2)

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

## Status fetch (one plain curl, User-Agent "V3R1T4S", no retry)

- URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- time (UTC, `date -u`): 2026-11-04T03:02:53Z
- HTTP status: 200
- sha256 of body (18415 bytes): 75f70e7bb1910743265e6b43b5299553efc5efa371ffae0a5cc92def05c7eb76
- edition/version shown: "This Version: DS6: Oct 30, 2025" (first published 1998-02-11; citation "#DS6: Oct 30, 2025").
  This is the 28th edition cited in claim/record/RECORD_DS6_pdf_2026-11-03.md; no newer edition is listed.
- Value in the cell (from claim/record/, DS6 Section 5.2, p. 168, not re-fetched by me): "Lee and Shan [2075] have
  verified this conjecture for trees with up to 17 vertices with a computer." Value: 17.

## Repo (github.com/elder-plinius/V3R1T4S, via gh)

- TROPHY_CASE.md: no mention of "magic" (0 hits). No super edge-magic entry.
- known-knowns/: 27 directories, none for super edge-magic.
- known-unknowns/graphs-games-automata/super-edge-magic-trees-beyond-17.md: bank entry, "open as of 2026-10-30",
  bound 17, p1 = at most 20, p2 = at most 22.
- Pull requests (open and closed; searches "super edge-magic", "edge-magic", "magic", "SEM trees", target id):
  only #917 (OPEN, same contributor thefullnacho, 2026-11-03), claiming p1: every tree on at most 20 vertices,
  certificates for n = 18, 19, 20; it explicitly claims nothing about 21 or more vertices. No closed PRs. No issues.

## Literature and code search (last 24 months, plus older)

- Zenodo API "super edge-magic": 3 records. 23918679 (2026-11-03, thefullnacho): certificates for all trees on
  18, 19, 20 vertices (the same contributor's p1 package, single version, files only sem-trees-18-20). 22652143
  (2026-09-08, L. Meng): spiders with equal legs only, with GitHub repo lsmeng/super-edge-magic-spiders (release
  v1.0.0 checked; README covers spiders, not all trees). 842842 (2017): cycles/wheels. Nothing on all trees > 17.
- arXiv API (all/abs/ti "super edge-magic", "edge magic"): newest relevant is 2023 (2308.10661, 2306.15986); the
  2022 survey 2211.04029 repeats the 17-vertex bound. No verification beyond 17.
- Crossref (from 2024-11-01, "super edge-magic trees computer verification"): only class-specific labelings and
  deficiency papers; nothing on exhaustive tree verification.
- GitHub repo search ("super edge-magic", "super edge magic", "superedgemagic", "edge-magic trees") and code search:
  only the Meng spiders repo and the V3R1T4S bank entry.
- Web search: Lee-Shan 2002 (17 vertices) remains the cited bound; a Cerioli et al. paper quotes Enomoto et al. at 15
  and Lee-Shan at 17; a 2022 survey and the Lopez open-problems list still state the conjecture as open with no higher
  verification. Sources: https://arxiv.org/pdf/2211.04029 ,
  https://www.sciencedirect.com/science/article/pii/S1571066119300775 ,
  https://mat.upc.edu/en/people/susana.clara.lopez/publications/openprob.pdf
- Neighbouring cells: graceful-tree verification (to 35 vertices) and the Brinkmann et al. alpha-deficit tables
  (to 26 vertices, DMTCS 2012) do not give SEM labelings of all trees: graceful does not imply SEM, and alpha-labelings
  (which do imply SEM) miss the alpha-deficitary trees; no published object labels every tree on 21 or 22 vertices.

## Comparison

- Published cell value: 17 (DS6 28th ed., current). Pending in-repo: 20 (PR #917, same contributor, Zenodo 23918679).
- This claim: 22, i.e. certificates for n = 18..22 (n = 21, 22 new relative to everything found).
- Trivial-edit test: an SEM labeling of every tree on 21 or 22 vertices cannot be got by deletion, restriction,
  relabelling or symmetry from any published object, since none covers those orders; there is no known valid
  propagation rule that extends all trees on n vertices to all trees on n+1. The n = 18..20 part overlaps the
  contributor's own pending p1 package, which is not a published prior record by someone else and is strictly
  extended here. Not a tie: 22 > 20 > 17.
- Minor (not novelty): claim/record/RECORD_DS6_pdf_2026-11-03.md still says "This package: at most 20"; CLAIM.md
  says 22. Stale text from the p1 package; worth fixing before submission.
- Caveat: Lee and Shan's 2002 talk is cited, not inspectable; orders up to 17 rest on it, as the bank entry allows.
  A private, unpublished extension cannot be ruled out, but none is discoverable.

pass: true
