# NOVELTY skeptic: site-percolation-2-uniform-lattices-thresholds, lattice #23 site

context: subagent (fresh Claude Code Agent-tool context, general-purpose)

Claim judged (claim/CLAIM.md, claim/result/threshold_23_site.json): lattice #23, (1/2)(3^3,4^2) + (1/2)(4^4),
site p_c = 0.57176454 +- 0.00000010 (one sigma; JSON: 0.57176453954634, sigma 1.04e-07, transfer matrix n <= 16),
with an independent Monte Carlo value 0.5717667 +- 0.0000014.

## Status source fetch (one plain request, no retries)

- URL: https://en.wikipedia.org/w/index.php?title=Percolation_threshold&action=raw (raw wikitext of
  https://en.wikipedia.org/wiki/Percolation_threshold)
- Request: one curl GET, User-Agent "V3R1T4S-research-agent/1.0 (open-notebook percolation threshold check)"
- UTC time (date -u immediately before the request): 2026-10-18T05:11:54Z
- HTTP status: 200
- Bytes: 267722
- sha256: 588b98d38a819a6712a7b3b497a8df7e5a955285ba0b7bc3bace199f2c742ba3 (identical to the hash recorded in
  claim/table/table_record.md for the scout's 2026-10-17T23:58:23Z fetch, so the table has not changed since)
- Saved in my work folder as fetch/percolation_threshold_raw.wiki (not part of claim/).
- Section "=== 2-uniform lattices ===" (wikitext line 1033); row 23 (lines 1146-1151):

      | 23
      |({{frac|1|2}})(3<sup>3</sup>,4<sup>2</sup>) + ({{frac|1|2}})(4<sup>4</sup>)
      | 5,4
      | 4.5
      | 0.5720(2)<ref name="NeherEtAl08"/>
      | 0.45844622(40){{citation needed|date=June 2019}}

- Row 23 site value: **0.5720(2)**, i.e. sigma 2e-4, cited to Neher, Mecke and Wagner 2008.

## Literature search (last 24 months, and anything after 2008 on two-uniform site thresholds)

- arXiv API, 2026-10-18T05:12:16Z, HTTP 200, 55459 bytes, sha256 fb7ce8c8...e63b561f:
  `abs:"site percolation" AND (abs:"uniform" OR abs:"tiling" OR abs:"tilings" OR abs:"row lattice")`, newest first,
  max 60. 29 entries (2001 to 2026-10). None gives a site threshold for any two-uniform lattice (hits are random
  planar maps / UIPT, hypergraphs, the Lorentz mirror model, cutset theorems, random fractional-dimensional lattices,
  and Scullard-Jacobsen 1209.1451, which is the method paper and treats no two-uniform lattice).
- arXiv API, 2026-10-18T05:12:24Z, HTTP 200, 81369 bytes, sha256 1611b7b4...6438481:
  `(abs:"percolation threshold" OR abs:"percolation thresholds") AND (abs:lattice OR abs:lattices) AND
  submittedDate:[202410180000 TO 202610182359]` (the last 24 months), max 200. 34 entries. Abstracts scanned for
  uniform/tiling/Archimedean: only 2507.12229 (Archimedean lattice representation), 2508.01320 (square-lattice
  diamond neighborhoods), 2605.11310 (fractional-dimensional lattices) and unrelated materials papers. No two-uniform
  site value.
- Web search (3 queries: "2-uniform lattice site percolation threshold (3^3,4^2) (4^4) high precision";
  "site percolation thresholds two-uniform tilings critical polynomial transfer matrix 2024 2025 2026 arXiv";
  "percolation thresholds k-uniform tilings site Monte Carlo Ziff new values 2-uniform"). Found: Neher, Mecke and
  Wagner (arXiv:0708.3250, table in arXiv:0708.3251) giving 0.5720(2) for 1/2(3^3,4^2)+1/2(4^4) by Newman-Ziff with
  L = 64..1024; Lebrecht, Centres and Ramirez-Pastor, Physica A 2021 (empirical site-bond formula over Archimedean and
  2-uniform lattices, no new measurement); Suding and Ziff 1999 (Archimedean); Jacobsen 1401.7847 and Scullard-Jacobsen
  1209.1451 (critical polynomials, not this lattice's site threshold); Xun-Hao-Ziff and Malarz et al. (extended
  neighborhoods on Archimedean lattices). No search found a site value for lattice #23 more precise than 2e-4.
- Consistent with claim/table/literature_record.md (the scout's search), which I re-did independently above.

## This repo: TROPHY_CASE.md and open pull requests (elder-plinius/V3R1T4S)

- TROPHY_CASE.md: fetched once from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md at
  2026-10-18T05:14:29Z, HTTP 200, 31235 bytes, sha256 b946f68e...472171a1; the pinned local copy (sha256 738c07a3...)
  was also checked. Neither contains "percolat", "uniform" or "threshold" in any form (case-insensitive grep): no
  trophy for this target.
- Open PRs: `gh pr list -R elder-plinius/V3R1T4S --state open --limit 200` at 2026-10-18T05:14:30Z returned 67 open
  PRs. The only one on this target is **#239** (psmoros, 2026-10-16, updated 2026-10-17T21:46:52Z): "[claim]
  site-percolation-2-uniform-lattices-thresholds (p2): row #22 bond p_c = 0.445287065(21)". I read its body and full
  diff (gh pr diff 239): it claims only the row #22 BOND value, states "No site threshold", and says its #23 (TSSS)
  roots are "not claimed here"; its data contain #23 bond roots only and no #23 site value (no 0.5717... number
  anywhere in the diff). So it is not a competing #23 site value. The four Kaust-a-laut PRs (#208/209/211/212) are
  covering designs; the other open PRs are on unrelated targets.

## Judgement

- Best known published site value for lattice #23: 0.5720(2), sigma 2e-4 (Neher, Mecke and Wagner 2008), and the
  live table still shows exactly that. No newer or more precise value found in 24 months of literature (or since
  2008), in TROPHY_CASE.md, or in open PRs.
- Claimed: 0.57176454 +- 1.0e-7 (JSON sigma 1.04e-7). That is about 1900 times smaller than 2e-4 and far below the
  bank's 2e-6 bar; even the independent Monte Carlo value alone (sigma 1.4e-6) beats every known value. Not a tie.
- On novelty only (criterion (d) and "strictly beats everything known"), the claim passes. I did not judge whether the
  number or its error bar is correct (that is for the other skeptics). Note that the claimed value is about 1.2 table
  sigma below 0.5720, which fits within the table's error bar.

pass: true
