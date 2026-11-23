# Novelty skeptic: A127500(12) <= 25 (result/T12_25moves.txt)

context: subagent (novelty skeptic, isolated claim copy of claim/). Paths are relative to claim/.

## Live status fetches (one GET each, UA "V3R1T4S-research-agent", no retries)
- https://oeis.org/A127500 at 2026-11-02T18:19:57Z, HTTP 200, sha256 50ba5e837df3e594556d8d2e6888b4f9af3c8548681737ab90c7345e140a1a6c.
  Value: DATA "5, 9, 9, 12, 13, 16, 18" (n = 4..10). Comment: "gives the bounds 19<=a(11)<=28, 21<=a(12)<=29". No a(12) term is listed and no tighter bound appears.
  (The hash differs from data/A127500.txt because that file is the fmt=text endpoint and this is the HTML page. The content is the same.)
- https://www.gibell.net/pegsolitaire/LargeTriangular/index.html at 2026-11-02T18:19:57Z, HTTP 200, sha256 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6. That is byte-identical to data/bell_large_triangular.html.
  Value: "21&le;S(12)&le;29", "Last modified March 4th, 2007". The shortest known T12 solution has 29 moves, e11 to a3.
- Live published upper bound for A127500(12): 29. Lower bound: 21.

## Prior-art search
- TROPHY_CASE.md: 0 matches for peg, solitaire or A127500.
- known-knowns/: 0 files match solitaire or A127500. The only "peg"/"a(12)" hits come from unrelated targets.
- elder-plinius/V3R1T4S issues/PRs (GitHub search "peg OR A127500 OR triangular" and "solitaire"): 0 results.
- Web search covering the last 24 months of literature and code ("triangular peg solitaire Triangle 12 shortest A127500 2025 2026"; "peg solitaire triangular 78 holes fewer than 29 moves github"):
  this found only Bell's JIS 2008 paper (bell2), Bell's pages, OEIS and generic solvers (feschber/peg-solitaire, MarkusThill/solitaire-diamond). None of them gives a T12 solution under 29 moves.

## Sanity check of the object (not a full verification)
- python3 code/pegcheck.py 12 result/T12_25moves.txt -> "n=12 start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID".
- sha256 of result/T12_25moves.txt is 7ec9d443efe7b234fb31c6d427820f067f3815e99dea8750a547bc1b53a6c78b, which matches claim.md.
- 25 is at least the lower bound 21, so it is consistent with known lower bounds. 25 is at most 28, so it meets the bank criterion.

## Verdict
The claimed 25 is strictly below the live published bound of 29 on both primary sources. It is 4 below, so this is not a tie. I found no prior or concurrent claim at or below 28 in the repo, the PRs or the web.
Novelty holds, provided the panel's validity skeptic confirms the simulator check independently.
pass: true
