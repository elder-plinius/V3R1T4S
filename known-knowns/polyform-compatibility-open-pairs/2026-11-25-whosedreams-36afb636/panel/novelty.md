# Panel vote: NOVELTY skeptic, claim 2026-11-25-whosedreams-36afb636 (heptiamonds M-X, bounded UNSAT k = 2..20, p3)

context: subagent
I was started as a fresh executor subagent and judged only from files on the box, my own live fetches and my own
scripts. I did not rely on README claims. Scratch: the confirm workspace panel_scratch/novelty/ folder
(LOG.txt holds every fetch line). All fetches: single read-only GET, user agent "V3R1T4S-kit (whosedreams)".

## 1. Live table cell
| URL | fetched (UTC) | HTTP | bytes | sha256 |
|---|---|---|---|---|
| https://sicherman.net/7mond/7compat.html | 2026-11-25T00:38:00Z (2026-11-24 19:38 ET) | 200 | 36097 | c602d9d24d51bf7e5b3d933b6f77e2092f62a95bb479e9d722683d9bcb02ffd0 |

Parsed both summary tables with my own script (header row A..Z without O/W):
- "Minimal Solutions" (unrestricted, first table): row M, column X = `?`; row X, column M = `?`.
- "Holeless Variants" (second table): M-X = `?`, X-M = `?`.
- Zero `×` characters on the page; footer "Last revised 2012-01-04."
The sha256 equals the one in PKG/the-record-we-beat/RECORD.md (fetched 2026-11-25T00:18:18Z) and in the kit's
2026-11-03 fetch, so the page is unchanged. RECORD.md's row-M reading (… U:? V:? X:? Y:6 Z:2) matches my parse.

## 2. Letter mapping (is this Sicherman's M and X?)
Fetched https://sicherman.net/7mond/labels.png at 2026-11-25T00:38:01Z, HTTP 200, 15473 bytes, sha256
3044870c00d4bee9bf8e55ae21713615c93f14211f7d29448d684210408a7ec8, and viewed it. M: a row of five triangles with two
peaks on one side (mirror-symmetric). X: a 3-armed pinwheel (rotationally symmetric, chiral).
I drew PKG/object/mx_k2_20_bounded_unsat.json "pieces" with that file's own "coordinates" convention
((r+c) even = down-pointing, (r+c) odd = up-pointing) and also checked symmetry from triangle centroids:
- M = row (0,0..4) plus (1,1),(1,3): a five-triangle row with two triangles under positions 1 and 3. It has a mirror
  axis and no rotational symmetry, which matches the image's M (shown flipped).
- X = (0,0),(0,1),(1,0..3),(2,0): 120° rotational symmetry, no mirror symmetry. That is the 3-armed pinwheel. It is
  the only heptiamond with 3-fold symmetry, so it can only be Sicherman's X.
The letters match the page.

## 3. Earlier results on M-X
| URL | fetched (UTC) | HTTP | sha256 (prefix) | finding |
|---|---|---|---|---|
| https://erich-friedman.github.io/mathmagic/0904.html | 2026-11-25T00:38:02Z | 200 | c6d1e1ad… | Polyiamonds only up to order 6; no heptiamond pairs. |
| https://sicherman.net/mincom/ | 2026-11-25T00:38:01Z | 200 | 3020fa35… | Smallest polyiamonds incompatible with each heptiamond, orders below 7 only; no heptiamond-heptiamond result. |
| https://sicherman.net/mixedmond/index.html | 2026-11-25T00:39:01Z | 200 | c8868b6a… | Mixed-order pairs only (penti/hexi with hepti); no equal-order M-X result. (https://sicherman.net/mixed/index.html gave 404.) |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+heptiamond | 2026-11-25T00:38:02Z | 200 | c9938ede… | total_count 0. |
| …+polyiamond | 2026-11-25T00:38:52Z | 200 | c9938ede… | total_count 0. |
| …+polyform / …+sicherman | 00:38:52Z / 00:38:02Z | 200 | da80790f… | Only #901 (Sylver Coinage bank item), unrelated. |
| …+compatibility | 2026-11-25T00:38:02Z | 200 | b02e2d03… | 7 hits (#630, #199, #654, #198, #215, #31, #770), all unrelated ("compatibility" in other senses). |
| https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 2026-11-25T00:38:03Z | 200 | 14116fdc… | 47 entries; none for polyform compatibility or heptiamonds. |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-11-25T00:38:03Z | 200 | ceecec91… | The latest 100 PRs: none mention heptiamond, polyiamond, compatibility figures or Sicherman. |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-11-25T00:38:03Z | 200 | 83af764f… | No hept, iamond, polyform, compatib or Sicherman entries. |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json | 2026-11-25T00:38:53Z | 200 | 7c3942f2… | polyform-compatibility-open-pairs still lists p3 as quoted below. |
- Resta's Polypolyominoes is polyomino-only, per Sicherman's ncomresta addendum (packager's fetch). I did not re-fetch
  iread.it or the recmath mirror because the packager's log shows them unreachable (500/404/000); this is a gap, not
  evidence. A web search returned a recmath.com copy of 7compat whose M row also shows `?` at X.
- Two web searches (heptiamond compatibility M X impossible; heptiamond compatibility SAT/DRAT 2025-2026) found no
  M-X impossibility result, bounded or unbounded. The only SAT/DRAT polyform certificate work found is about Heesch
  numbers (tkmt-lab/heesch-certificates, Zenodo 10.5281/zenodo.23572882), not compatibility. One search summary
  claimed "M and X are compatible ... size 14"; that is contradicted by the live table (`?`) and I ignore it as an
  error in the search summary.
- Local repo (commit 5db3547): "heptiamond" appears only in bank/targets.json and
  known-unknowns/graphs-games-automata/polyform-compatibility-open-pairs.md. No existing claim.

## 4. Does p3 count here?
Bank p3: "A computer-certified impossibility (SAT/DLX exhaustive, with checkable proof) up to a stated figure size for
a '?' pair, clearly labelled as bounded." The cell is `?` in the live unrestricted table (and in the holeless
table). The object's claim says "Bounded result only" and gives a stated board per k with k ≤ 20. Nothing in the repo,
PRs, trophy case or the sources above covers this cell, so no earlier equal-or-better bounded result exists that I
could find. For novelty, p3 counts as new. Whether a per-k board is a valid "stated figure size", and whether the
Zenodo draft counts as a checkable proof before it is published, is for the criterion skeptic. I do not vote on those.
Before submitting, re-fetch 7compat.html live again (bank rule).

pass: true
