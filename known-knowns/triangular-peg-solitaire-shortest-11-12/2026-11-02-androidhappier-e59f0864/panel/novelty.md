# NOVELTY skeptic — A127500(11) <= 22

context: subagent (novelty skeptic, isolated claim copy)

Object: result/T11_22moves.txt (sha256 e59f0864e5e9fc3034f2ee6815a92a2fa05775d4b1e2f6f3515082553a6ef6f4, re-hashed and matched).
It is a 22-move, 64-jump solution on Triangle(11) from vacancy a2 to survivor j11.
Cell: Triangle(11) upper bound, A127500(11).

## Live status fetches (one GET each, UA "V3R1T4S-research-agent", no retries)
- https://oeis.org/A127500 — fetched 2026-11-02T18:17:50Z, HTTP 200 (live sha256 99639c2b...; it differs from data/A127500.txt only because that copy came from the fmt=text endpoint).
  Quoted value: DATA "5, 9, 9, 12, 13, 16, 18"; comment: "The reference calculates a(n) up to n=10 and gives the bounds 19<=a(11)<=28, 21<=a(12)<=29". STATUS approved. Live upper bound for a(11) = **28**.
- https://oeis.org/draft/A127500 — fetched 2026-11-02T18:18:33Z, HTTP 200. No pending edit mentions a(11).
- https://www.gibell.net/pegsolitaire/LargeTriangular/index.html — fetched 2026-11-02T18:17:51Z, HTTP 200. sha256 96000bb3...fd7a6 matches data/bell_large_triangular.html byte for byte.
  Quoted: "Last modified March 4th, 2007"; table row "11 | 66 | 18 | | 19≤S(11)≤28"; "it is believed that S(11) is 20, 21, or 22". Shortest known T11 solution: "a4 to a1 ... (28)". Live upper bound = **28**.
- https://www.gibell.net/pegsolitaire/tindex.html — fetched 2026-11-02T18:18:05Z, HTTP 200. sha256 0aa57a74... matches data/bell_tindex.html ("Last Modified April 27th, 2025"). It says nothing new about T11.

## Literature and code search (last 24 months, plus the primary literature)
- Web searches covered triangular peg solitaire Triangle(11) shortest solution, A127500, and S(11) beam search on GitHub. The only hits were the primary sources:
  - Bell, JIS 11 (2008) / arXiv math/0703865: "The shortest known solution for n=11 has 28 moves".
  - Bell's pages (28).
  - arXiv 0903.3696 (general solver notes, no T11 bound).
  None reports anything below 28.
- GitHub repository search for "triangular peg solitaire" pushed after 2024-11-01 returned 10 repos. All are 15-hole Cracker Barrel games or solvers, generic backtrackers, or unrelated rotation puzzles. None has a minimum-move Triangle(11) result. I did not check release assets one by one, because none of these repos is relevant to minimum-move T11. GitHub code search for "A127500" returned HTTP 401 (needs auth), so I could not run it. I note that limit here.
- Repo data: TROPHY_CASE.md has no peg/A127500/triangular entry. known-knowns/ (31 folders) has no peg-solitaire or A127500 folder or file (grep found nothing).
- elder-plinius/V3R1T4S PRs, searched through the GitHub issues API at 2026-11-02T18:18:11Z:
  - "A127500": 0 results.
  - "peg solitaire": 0 results.
  - "triangular": 7 results, all unrelated (percolation, auctions, circle packing, SAW, etc.).
  None of the open or closed PRs touch this cell.

## Comparison with published objects (this cell and neighbouring cells)
- Same cell: Bell's T11 28-move solution (fixtures/bell_T11_28.txt, a4 to a1).
  - Relabelling or symmetry keeps 28 moves and maps the corner finish a1 onto corners only. The claim finishes at j11, which is not a corner, and starts at a2, so it solves a different SVSS problem.
  - Deletion or restriction cannot produce a full 66-hole solution.
  - Merging consecutive same-peg moves cannot get below Bell's own reordering optimum of 28. Getting to 22 needs a structurally different solution.
  - The claim says the solution came from a fresh beam search (code/beam3.c), not from a published seed.
- Neighbouring cells:
  - T10 (18 moves, 55 holes) and T12 (29 moves, 78 holes). Restricting the T12 solution to T11 does not give a legal T11 SVSS solution. An 18-move T10 solution plus an 11-hole bottom row would need at least about 4 more moves for 11 extra pegs, and no published construction gives that.
  - Bell's n ≡ 0 (mod 12) construction does not apply at n=11.
  - No published edit chain reaches ≤ 27, let alone 22.
- Sanity re-check (not my main role): code/pegcheck.py 11 gives "moves=22 VALID". The independent code/pegsim2.c also gives VALID. Calibration: fixtures/bell_T11_28.txt gives VALID 28, and fixtures/neg_T11_swapped.txt gives ILLEGAL.
- 22 < 28 is a strict improvement of 6 moves, not a tie. It also meets the bank criterion (≤ 27). It lies inside Bell's conjectured range (20–22) and above the proven lower bound 19, so it does not contradict anything known.

## Verdict
The claim strictly beats every known upper bound for A127500(11): 22 vs. the live 28 on OEIS and on Bell's page, both fetched 2026-11-02T18:17:50–51Z. It is not a trivial edit of any published object.

pass: true
