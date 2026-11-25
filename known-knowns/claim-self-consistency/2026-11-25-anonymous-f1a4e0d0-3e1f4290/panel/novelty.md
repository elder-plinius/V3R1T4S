# Novelty skeptic: claim-self-consistency / white2011-warp-field-mechanics-101-interferometer-energy

context: subagent (fresh, Claude Code Agent tool)

## Status source (one plain fetch, no retries)
- URL: https://ntrs.nasa.gov/api/citations/20110015936
- Command: `curl -s -A "V3R1T4S-panel" -w '%{http_code}'`
- UTC time: 2026-11-25T19:22:02Z (request start; `date -u`), 2026-11-25T19:22:03Z (end)
- HTTP status: 200
- sha256 of body: a69b4a77ac967c749a43b7f1f5850d41c69d61acc51346745a1dc86f90cf5847 (identical to the scout's 19:07:34Z fetch)
- What it shows: title "Warp Field Mechanics 101", author "White, Harold", stiType CONFERENCE_PAPER, publicationDate 2011-09-30, status CURATED,
  record modified 2025-08-31, download /api/citations/20110015936/downloads/20110015936.pdf. The source is still served
  unchanged; it is a 2011 proposal with no record table. The "value" being tested is the source's own operating point
  (1 cm diameter, boost ~1.0000001), for which the record carries no energy figure.

## Searches done
1. arXiv API (export.arxiv.org, one request per query):
   - `all:"warp field interferometer"` -> 1 hit: 1407.7772 (Lee & Cleaver 2014).
   - `all:White AND all:Juday` -> 1 hit: 1407.7772.
   - `abs:Alcubierre AND abs:interferometer` -> 1 hit: 2108.05169 (Bohmian photon trajectories; unrelated).
   - `abs:"warp field mechanics"` -> 0 hits.
2. Lee & Cleaver, arXiv 1407.7772 (read in full text). Computes the capacitor's electric-field energy density (4.4 J m^-3 for
   10^6 V/m), its curvature (9.2e-43 m^-2) and microlensing angle (1.81e-6 arcsec), and states qualitatively that an
   Alcubierre bubble "can be formed only by negative energy density and/or negative pressure". It gives NO energy computed
   from the Alcubierre/White Eq. (3) at the 1 cm, boost 1.0000001 operating point. It does anticipate the claim's qualitative
   sign point (a positive-energy capacitor is the wrong kind of source), so that half of the claim is not new.
3. White, "Warp Field Mechanics 102" (NTRS 20130011213, fetched): energy figures only for a spacecraft-scale point design
   (~2000 kg negative mass for a 5000 kg ship); no test-article energy.
4. Pfenning & Ford 1997 (gr-qc/9702026, fetched): publishes the exact total-energy integral E = -(v^2/12) int f'^2 r^2 dr
   for the same tanh shape function (equal to the claim's Step 3) and thin-wall estimates with quantum-inequality wall
   thickness for macroscopic bubbles. No sigma-independent lower bound, no evaluation at R = 5 mm or at White's boost.
5. Lobo & Visser 2004 (gr-qc/0406083, fetched): order-of-magnitude quantifier M_warp ~ -v^2 R^2 sigma (thin wall); no
   all-sigma bound, no laboratory/interferometer evaluation.
6. Recent literature (last 24 months): arXiv 2508.20348 (2025 warp-drive review) mentions White's interferometer and
   Lee & Cleaver only descriptively; arXiv 2602.16495 (2026 critique) criticises White et al.'s later work but gives no
   test-article energy; arXiv 2103.05610, 2408.04495, 2511.18251 and a Sept 2025 Zenodo review (17060193) surfaced in web
   search with no interferometer test-article energy.
7. Web search (4 queries: White-Juday interferometer energy / "1.0000001" energy joules / WFM 101 critique / 2024-2026
   test-article energy): Centauri Dreams 2012, NextBigFuture, PopSci, Wikipedia (IXS Enterprise, Harold G. White),
   Physics Forums threads 639719 and 789238. The Physics Forums thread 639719 was read: no joule/kg figure for the
   test article. No source gives a quantitative energy requirement for the 1 cm, boost 1.0000001 article.
8. GitHub: `gh search code` ("1.0000001 warp", "White Juday interferometer") -> nothing; `gh search repos "warp field
   interferometer"` -> one repo, bradgeigermanager-sketch/White-Juday-Experimental-Design-for-Warp-Field-Interferometer-2.0
   (created 2026-11-13): 15 markdown files on hardware wiring/noise analysis, 0 releases; no energy computation.
9. This repo: TROPHY_CASE.md and known-knowns/ (27 target folders) contain no warp/Alcubierre/White entry (the only
   "white" grep hits are unrelated words). Pull requests of elder-plinius/V3R1T4S: open and closed listings (200 closed
   scanned) plus searches for "warp", "Alcubierre", "warp field", "White Juday", "claim-self-consistency", "NTRS",
   "interferometer": no prior claim on this source (search hits #838/#607 are fuzzy matches about asteroids).

## Judgement
No published object fills this cell: nothing in print (at any age) or in this repo gives an energy requirement for White's
own 1 cm, boost ~1.0000001 test article computed from his Eq. (3), let alone a bound valid for every wall parameter sigma.
The ingredients are published (Pfenning & Ford's energy integral; Lobo & Visser's v^2 R^2 sigma scaling), and the claim's
own Step 3 should cite Pfenning & Ford 1997 for the integral; but the trivial edits of those objects (substituting R and v)
yield only sigma-dependent estimates, not the claim's sigma-uniform Cauchy-Schwarz bound E <= -(c^4/(48G)) u*^2 R =
-1.127e37 J at the source's operating point. The sign argument (positive-energy capacitor cannot supply Eq. (3)) is
already in Lee & Cleaver 2014 qualitatively and is not counted as new. Being a bound on a proposal, there is no prior
number to tie; the quantitative bound is new relative to everything found.
Caveat for the record: novelty is modest (a short inequality applied to a published formula), and the claim should name
Pfenning & Ford 1997 as the source of the energy integral.

pass: true
