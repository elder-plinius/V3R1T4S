# Novelty verdict: hsp4, N = 67

context: subagent (Claude Code Agent tool, fresh context for this one claim)
role: novelty skeptic
claim read: CLAIM.md (candidate r* = 0.264072205869627..., file hsp4-67-candidate.txt; posted value 0.264026543809, file hsp4-67-posted.txt; snapshot hsp4_radius_as_fetched.txt)

## Fetches (each URL requested exactly once, plain curl, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: Fri Oct 16 17:48:39 UTC 2026, HTTP 200, 5575 bytes
   row 67 quoted verbatim: `67 0.264026543809`
   byte-identical (cmp) to the snapshot hsp4_radius_as_fetched.txt in the claim folder.
   Candidate header line in hsp4-67-candidate.txt: `# N=67 r_float=0.26407220586962721 table=0.264026543809 gain=4.566e-05 moves=10`.
   Margin candidate minus live table = 0.000045662061, i.e. 4.57e-05, far above the 1e-10 floor.
   First line of hsp4-67-posted.txt: `0.264026543809` (matches the live table row).

2. https://packomania.com/hsp4/hsp4.html
   time: Fri Oct 16 17:48:40 UTC 2026, HTTP 200, 88618 bytes
   page title: "The best known packings of equal 4d hyperspheres in a larger 4d hypersphere"
   quoted: `Last update: 06-Jul-2025`
   History of updates (complete): 04-Jul-2025 first presentation N=2-100; 05-Jul-2025 extension to N=200; 06-Jul-2025 extension to N=300 (all E. Specht [31]).
   No entry newer than 06-Jul-2025. No entry mentions N=67. The only "67" occurrences are the table row for N=67 (radius 0.264026543809) and a contact count in the N=70 row.

3. https://packomania.com/pending-requests.html
   time: Fri Oct 16 17:48:41 UTC 2026, HTTP 200, 4954 bytes
   page dated 08-Oct-2026. Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv. No hsp4 (or any hsp) category row at all, so no hsp4 range includes 67.
   Queue caveat (unresolvable): row `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` is category-unspecified. It could in principle contain hsp4 candidates including N=67. Per the bank rule, N=67 must be re-checked against the live table once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: Fri Oct 16 17:48:42 UTC 2026, HTTP 200, 30936 bytes, 100 lines
   grep (case-insensitive) for hsp4, hsp6, hypersphere, packomania: 0 hits. grep for a standalone 67: 0 hits.
   Note: this file still describes "six result families" (graphs, codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and does not yet list the hsp4-hsp6 family that exists on main; so it cannot contain a competing N=67 entry.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: Fri Oct 16 17:48:43 UTC 2026, HTTP 200, 52 open PRs returned (fewer than 100, so complete)
   Scanned title, body and head branch of every PR for hsp4/hsp5/hsp6/hypersphere/4-ball: 1 textual hit, PR #231 (spherical-codes-cohn-table, (6, 526)), a different target. Packomania PRs open: scu spheres-in-cube N=882-886 (#235-#238), cci N=4141 (#234), scu N=83 and N=507 coordinate audits (#206, #207); none is hsp4, none is N=67.
   PRs whose text contains "67" (#229, #225, #203) are matrix-multiplication and VSX claims, unrelated.

   https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
   time: Fri Oct 16 17:48:44 UTC 2026, HTTP 200: 12 hash-named subdirectories dated 2026-10-14.
   https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 (one extra request, to resolve the N values without touching each subfolder)
   time: Fri Oct 16 17:51:34 UTC 2026, HTTP 200, truncated: false, 312 paths under the family.
   Object files present: hsp4-30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75 (candidate and posted). N=67 is not in the merged family. Confirms the stated list.

6. Literature search (web, 2024-2026)
   Query A: packing equal hyperspheres in a 4-dimensional ball, best known, Packomania hsp4, 2025-2026.
   Query B: 67 equal balls in a 4-ball / 67 spheres four dimensions radius record, arXiv 2025-2026.
   Returned: general sphere-packing pages (Wikipedia, codes.se dimension-4 lattices, OEIS A084829), arXiv 2305.10023 (3-D spheres in a sphere heuristic, 2023), arXiv 2505.02394 (antipode construction, infinite packings), arXiv 2506.11682 (hyperbolic 4-space), arXiv 2609.25120 and a June-2026 preprint on the D4 density conjecture (unbounded space, not a container problem). None lists a finite packing of 67 balls in a 4-ball or any radius for N=67.
   Lead followed: the search surfaced https://www.packomania.com/sspn/pdf/d4.pdf dated 18-JUL-2026. Fetched once (Fri Oct 16 17:50:26 UTC 2026, HTTP 200, 10.6 MB). Decompressed text shows "N spheres in a sphere" for N = 38..49 with radii 0.384276654074 (N=38) down to 0.358059536265 (N=49); these do not match the hsp4 table rows (hsp4 N=38 is 0.300651321630) and are the 3-D spheres-in-a-sphere values. It is a different problem, and it does not reach N=67. Dead end, no competing value.
   Nothing found in the last 24 months that matches or beats 0.264072205869627 for 67 balls in a 4-ball.

## Assessment

- Live table value for N=67 is still 0.264026543809 (unchanged since the snapshot); the candidate beats it by 4.57e-05 (above the 1e-10 floor). Not a tie.
- No History-of-updates entry on the live hsp4.html is newer than 06-Jul-2025 and none covers (4, 67).
- No hsp4 range on the pending-requests page includes 67 (no hsp4 row exists).
- TROPHY_CASE.md, the merged hsp4-hsp6 family (N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75) and the 52 open PRs contain nothing for hsp4 N=67.
- Literature search found no competing value.
- Isometry to the posted packing and the 50-digit feasibility check are the other skeptics' remit; this verdict is novelty only.

Caveat that cannot be resolved: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" pending bundle is category-unspecified; if it contains an hsp4 N=67 candidate that Packomania later posts above 0.264072205869627, this novelty verdict is void. Re-check the live table row 67 once that bundle leaves the pending list.

pass: true
