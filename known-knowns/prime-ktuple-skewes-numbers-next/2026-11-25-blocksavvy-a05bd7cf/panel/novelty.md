role: NOVELTY
context: fresh subagent (knowledgeWork)
claim: sexy-prime Skewes number p = 349018493647
date_utc: 2026-11-25T01:47:24Z

## Scope and inputs
Read: repo/kit/RULES.md; header + "## NOVELTY" of runs/2026-11-25-0047-sexy/PANEL_BRIEFS.md; the claim copy at
sandbox/panel-0047sexy-novelty/claim/ (CLAIM.md). Nothing else under runs/ was opened (no attempts/, selfcheck/, other panels).
All fetches: plain curl, User-Agent "V3R1T4S-panel/1.0 (read-only research)", one request each, saved under
sandbox/panel-0047sexy-novelty/fetch/ (full log with HTTP status + UTC time per request: sandbox/panel-0047sexy-novelty/fetch/log.txt).
No retries of any blocked/failed request. No outward actions.
Claim under test (cell): first prime p with pi6(p) > 4*C2*Li2(p), pairs (p, p+6) not necessarily consecutive, inclusive count,
Li2 from 2 (Toth Def. 2) = 349018493647 (exclusive-count variant 349018493981 also stated in the claim).

## Primary status page (fetched once)
- URL https://oeis.org/A210439 | HTTP 200 | 2026-11-25T01:41:55Z | sha256 15fb06d93f4f7dcb2c3736e766f2baa48e1c031d7bd64711903a379a6d0567e7
  (sandbox/panel-0047sexy-novelty/fetch/A210439.html). Value: "The minimal Skewes number for prime n-tuplets", offset 2, data
  1369391, 337867, 1172531, 21432401, 251331775687, 7572964186421, 1203255673037261, 3658988336628289781 (a(2..9);
  a(9) from Desfontaines & Pfoertner, Jun 03 2026); page "Last modified November 24 20:31 EST 2026". KNOWN: no sexy-pair
  (p, p+6) term or comment; n=2 cell is the twin pair (1369391, Wolf 2011). The sexy cell is not represented in this sequence.

## Other sources (one request each; status, UTC time, finding)
- https://en.wikipedia.org/w/index.php?title=Skewes%27s_number&action=raw | 200 | 01:42:08Z | table of k-tuple Skewes numbers
  (twin 1369391 Wolf 2011; cousin 5206837 Toth 2019; ... 8-tuplets Pfoertner/Luhn 2021) and verbatim: "The Skewes number (if it
  exists) for [[sexy prime]]s (p, p+6) is still unknown." Revision history API (01:42:09Z, 200): last edits 2026-10-28 (vandalism
  "Go f yourself" added + reverted, See also), 2026-08-23 (citation link), 2026-06-07 (bounds wording); compare API diffs
  (01:42:50Z, 200 x3) show none touched the sexy sentence. Also https://en.wikipedia.org/wiki/Skewes%27s_number (200, 01:42:08Z).
- https://en.wikipedia.org/wiki/Sexy_prime | 200 | 01:42:10Z | no "Skewes"/"Hardy"/"349018" text.
- https://oeis.org/A080841 | 200 | 01:42:08Z | "Number of pairs (p,q) of (not necessarily consecutive) primes with q-p = 6 and
  q < 10^n": ..., a(10)=54818296, a(11)=448725003, a(12)=3741217498, ... a(19); a(13)-a(19) by Benjamin Chaffin Jun 02 2026
  (a(19) corrected Jul 08 2026). No mention of Skewes / Hardy-Littlewood / first crossing. b-file (200, 01:42:08Z) same values.
  History page https://oeis.org/history?seq=A080841 (200, 01:43:45Z): no Skewes/crossing text.
  NUMERICAL (computed here, mpmath 30 digits, C = 4*C2, Li2 from 2): a(n) - C*Li2(10^n) = -4537.06 (n=10), -12726.36 (n=11),
  +97764.36 (n=12). So the published a(12) already implies a sign change below 10^12 (as the brief says) - an existence/upper
  bound only. No source found that states the first crossing.
- https://oeis.org/search?q=349018493647&fmt=data | 200 | 01:42:08Z | "Sorry, but the terms do not match anything in the table."
  Also q=349018493 (200, 01:42:08Z): no match; q=349018493981 (200, 01:43:33Z): "No results."; q=1416008996 [claimed pi6(p)]
  (200, 01:43:33Z): "No results."
- OEIS text searches: "Skewes number" (200, 01:42:22Z): 8 hits A210439, A332493, A333586 (first gap 2), A348053, A007508,
  A052435, A333587 (first gap 4; a(2) = cousin Skewes number), A347278 - none for gap 6 / sexy pairs. sexy skewes (200,
  01:42:08Z): 1 hit A007508 (a counting remark by S. Pavlov, no Skewes value for p+6). sexy "Hardy-Littlewood" (200, 01:42:22Z),
  sexy "sign change" (200, 01:43:33Z), "p+6" "Hardy-Littlewood" "sign change" (200, 01:43:33Z): only A007508/A210439/A333586/
  A347278, none giving a (p, p+6) crossing. https://oeis.org/A031924 (consecutive sexy, 200, 01:47:19Z): no Skewes/sign change.
  https://oeis.org/history?seq=A210439 (200, 01:43:45Z): no sexy entry in history.
- https://arxiv.org/abs/1910.02636 (200, 01:42:09Z) and PDF https://arxiv.org/pdf/1910.02636 (200, 01:43:01Z): Toth, v1 only
  (7 Oct 2019). The conclusion lists as future work "the extension of the search for Skewes numbers to further k-tuples such as
  2-tuples of the type (p, p+2k) ... (the case k = 3 often being referred to as the "sexy primes" ...)" - i.e. open in the source.
- Papers citing Toth: https://api.semanticscholar.org/graph/v1/paper/arXiv:1910.02636/citations (200, 01:45:29Z): 6 citing items
  (2021-2026). Checked the two arXiv ones from the last 24 months: arXiv:2604.02383 "Neural Prime Sieves" (abs 200 01:45:35Z, PDF
  200 01:45:40Z; no Skewes/sign-change result for sexy pairs) and arXiv:2412.19866 (abs 200 01:45:35Z; asymptotic expansions, no
  crossing).
- Pfoertner/Luhn: https://pzktupel.de/ (200, 01:42:09Z; meta-refresh) -> https://pzktupel.de/ktuplets.php (200, 01:43:11Z,
  "Last updated: 8 November 2026") -> https://pzktupel.de/skewes_numbers.php (200, 01:43:20Z, "Last updated: 31 October 2026",
  sha256 df23bbae...): table row "sexy | p, p+6 | unknown" (twin 1 369 391 Wolf; cousin 5 206 837 Toth; ... 9-tuplet
  3 658 988 336 628 289 781 Desfontaines/Pfoertner 03 Jun 2026). History https://pzktupel.de/KTHIST/kthist2026.php (200,
  01:43:21Z): no Skewes/sexy/349018 text. https://pzktupel.de/ktpatt_hl.php (200, 01:47:18Z): no Skewes/sexy text.
  OEIS wiki User:Hugo_Pfoertner and User:Norman_Luhn (200 each, 01:43:45Z): no Skewes/sexy text.
  http://www.randomwalk.de/ (Pfoertner's homepage) | HTTP 500 | 01:43:33Z | server error, not retried; not a status source
  for this cell (the pzktupel table and OEIS pages Pfoertner maintains were read instead).
- MathWorld https://mathworld.wolfram.com/SexyPrimes.html (200, 01:42:09Z): definitions/constellations only; no Skewes, no
  Hardy-Littlewood crossing. https://mathworld.wolfram.com/SkewesNumber.html (200, 01:47:17Z): no sexy/k-tuple Skewes.
- Web search (WebSearch tool, ~01:44Z): "349018493647" -> only barcode-lookup pages, no mathematical hit; "Skewes number sexy
  primes (p, p+6) first sign change Hardy-Littlewood 2026" -> Wikipedia pages, all saying the sexy case is unknown.
- GitHub API (01:44:06Z-01:44:58Z, all 200): repo search skewes / "skewes number" / skewes prime / "sexy primes" pushed>2024-11-01 /
  hardy-littlewood prime k-tuple; issue/PR search 349018493647 (0), skewes sexy (0), skewes prime created>2024-11-01 (17, none a
  sexy-pair crossing). Inspected: domcity2003/skewes-hunt (pi vs li crossover bound, not k-tuples; no releases),
  vibemathing/problem-wikipedia-6ca8b6d3a25c3170 ("sexy primes" draft contract; results.jsonl and attempts.jsonl empty, 0 PRs,
  0 releases), Ruqing1963/prime-race-skewes (pi vs li). No release assets with the value.
- Zenodo API (01:44:11Z-01:44:32Z): q=349018493647 (200) total 0; q=skewes size 25 (200) 59 hits, none on k-tuple Skewes numbers;
  q="sexy primes" size 25 (200) 30 hits, abstracts screened for Skewes/sign change/crossing/349018: none report the crossing
  (record 23935787 "Counting Sexy Primes and Triplets up to 10^10" stops below p). (Two earlier Zenodo calls with size=50 got 400
  "Page size cannot be greater than 25" - a client parameter error, corrected, not a block.)
- arXiv API: http://export.arxiv.org queries returned 500 (01:44:12Z, x3, not retried); https://export.arxiv.org queries (200,
  01:44:34Z-01:45:22Z): all:skewes, abs:"Skewes number" OR ti:Skewes, math.NT "Hardy-Littlewood" prime tuples, abs:"sexy primes" -
  no paper giving a (p, p+6) Skewes number (hits are "skew" stems or unrelated NT papers).

## This repo and upstream PRs
- git -C repo fetch; origin/main = 989ddf5f1c8b3d7a55370c4407956006727b6388 (2026-11-23T10:25:27-08:00).
  TROPHY_CASE.md: no skewes/sexy/tuplet/A210439/349018 text. known-knowns/ (47 topic dirs): git grep for
  skewes|sexy prime|349018493647|A210439 -> no file. The only hits on origin/main are the bank entry
  (bank/targets.json "prime-ktuple-skewes-numbers-next", known-unknowns/number-hunts/prime-ktuple-skewes-numbers-next.md),
  which lists the sexy cell as open.
- elder-plinius/V3R1T4S PRs via GitHub API https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all, pages 1-12
  (200 each, 01:46:06Z-01:46:25Z): 1188 PRs (573 open, 615 closed, created 2026-10-14T01:52:59Z .. 2026-11-25T00:58:28Z). Titles,
  bodies and branch names matched against skewes|sexy|k-tuple|tuplet|hardy-littlewood|A210439|A332493|A080841|349018|1416008996|
  prime-ktuple|(p, p+6): 0 matches. Issue search repo:elder-plinius/V3R1T4S skewes / sexy / tuplet / 349018493647 /
  Hardy-Littlewood (200 each, 01:46:36Z): total_count 0 each.
- Bare partial clone (sandbox/panel-0047sexy-novelty/prs.git) with refs/pull/*/head: 1187 PR heads; changed paths vs merge-base
  (32209 path lines, sandbox/panel-0047sexy-novelty/pr_paths.txt) contain no skewes/sexy/tuple/hardy/A210439/A332493/A080841
  path; commit messages of all 2232 commits: no match.

## Comparison
- Cell: (p, p+6) Skewes number, Toth definition. Published value: none. Wikipedia ("still unknown"), pzktupel.de Skewes table
  ("sexy | p, p+6 | unknown", updated 31 Oct 2026), Toth 2019 (listed as future work) all mark it open; OEIS has no sequence or
  term containing 349018493647 or 349018493981.
- Strongest published neighbour knowledge: A080841(12) = 3741217498 (Earls et al.), which implies (NUMERICAL, computed here)
  that some sign change occurs below 10^12; nobody publishes WHERE the first one is. Neighbouring cells (twin 1369391, cousin
  5206837, triplets, A333586/A333587) are different patterns; no deletion/restriction/relabelling/symmetry/polish of any published
  object yields the sexy first crossing. The claim is not seeded from a published object (it is a from-2 enumeration).
- Convention variants: no published value under the exclusive ("less than n") convention either (349018493981 not found);
  consecutive-sexy (A031924) has no published Skewes value; so no equivalent object exists under another convention.
- Therefore the claimed exact first crossing strictly improves on everything known (an exact value vs. only an implied existence
  below 10^12); not a tie. This panel judges novelty only; correctness of the value is for REPRODUCE, and the exact cell/
  convention reading is for CRITERION.
- injection_suspected: none found in the fetched pages.

pass: true
