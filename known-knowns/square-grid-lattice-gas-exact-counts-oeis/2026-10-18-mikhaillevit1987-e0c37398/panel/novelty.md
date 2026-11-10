# Novelty skeptic verdict: A054759(16)

context: subagent (Claude Code Agent tool, general-purpose, fresh context)

Claim (claim/CLAIM.md, claim/object/a054759_16.txt):
A054759(16) = 2781781827849835218619790131266486746689884618378, claimed as partial win p1.

## Live fetches (one plain request each, curl, User-Agent "V3R1T4S-novelty-skeptic/1.0", no retries)
Raw files are saved in skeptic_novelty/fetched/ (outside claim/).

| UTC time | HTTP | bytes | URL | value read |
|---|---|---|---|---|
| 2026-10-18T11:45:20Z | 200 | 304 | https://oeis.org/A054759/b054759.txt | last line `14 15844635835975276495290739119895808472`; largest index 14; sha256 26a83711... matches the author's record in claim/table_record/fetch_records.json |
| 2026-10-18T11:45:21Z | 200 | 16131 | https://oeis.org/A054759 | DATA ends at a(14) = 15844635835975276495290739119895808472; EXTENSIONS: "a(14) from Brendan McKay, Apr 18 2024"; no a(15), no a(16) |
| 2026-10-18T11:45:22Z | 200 | 22306 | https://oeis.org/history?seq=A054759 | latest revisions #36-#40 (May 30 2026, Oct 06 2026) edit LINKS/STATUS only; no pending data edit |
| 2026-10-18T11:45:23Z | 200 | 20976 | https://oeis.org/A028420 | target status page read (main target; not affected by this partial) |
| 2026-10-18T11:45:24Z | 200 | 1920720 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 91 open PRs (newest #398). Only competing one: #366 (2026-10-17T23:05:24Z, mizopl) claims A054759(15) = 4310182149988584261406143524214457416387448 and states "No claim about n >= 16". No PR contains the a(16) value. |
| 2026-10-18T11:45:26Z | 200 | 31235 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | no mention of A054759, square ice, Eulerian orientations or this target |
| 2026-10-18T11:46:11Z | 200 | 16980 | https://oeis.org/A298119 | m x n torus Eulerian-orientation table |
| 2026-10-18T11:46:12Z | 200 | 811 | https://oeis.org/A298119/b298119.txt | n = 1..91 (13 antidiagonals, max side 13); no 15x15 or 16x16 entry |

## Literature (last 24 months)
- Web search for the exact 49-digit value: no hit anywhere.
- Web searches for exact torus square-ice / Eulerian-orientation counts in 2025-2026 (arXiv, OEIS): nothing beyond
  OEIS a(14) (McKay, Apr 2024). Search coverage is limited (general web search only, no MathSciNet/zbMATH access);
  absence of evidence there is weaker than the OEIS/PR checks above.

## Comparison with the best known
- Best published: a(14) (OEIS, 2024). Best claimed anywhere found: a(15) in open PR #366.
- The claim's own run (claim/run_output/results.jsonl) gives a(15) = 4310182149988584261406143524214457416387448,
  identical to PR #366, and reproduces a(1..14) of the b-file. Agreement with an independent party at n = 15 is a
  consistency check, not novelty.
- a(16) is one index beyond everything found: this is a strict extension, not a tie.

## Caveats for the panel (not novelty defects, but relevant to eligibility)
1. The target text defines the claimed index as N = 1 + largest DATA/b-file index = 15. Here n = 16 is claimed while
   a(15) is not yet in OEIS and is claimed first by PR #366. p1 says "next unknown term(s)" (plural), so a(16) is
   plausibly in scope, but the n = 15 credit belongs to #366 by priority; this claim's novelty is a(16) only.
2. Growth check: a(16)^(1/256) = 1.546093, a(15)^(1/225) = 1.546987 vs (4/3)^(3/2) = 1.539601: the gap is about
   6.5e-3, larger than the main target's 1e-3 tolerance. It decreases monotonically toward the constant, consistent with a
   finite-size correction, and p1 explicitly carries over only the "two-run and reproduction rules". Correctness is
   for the other skeptics. I did not re-run the computation, because the user limited CPU on this machine.

novelty: CONFIRMED (a(16) not found in OEIS A054759/A298119, their histories, the repository's open PRs or TROPHY_CASE.md, or a web search; strictly beyond the best known a(15) in PR #366)

pass: true
