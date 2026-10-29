# Novelty verdict: hsp4, N = 111

context: subagent (Claude Code Agent tool, fresh context for this one claim)
skeptic: novelty (one of three)
claim folder files consulted: CLAIM.md, REPRODUCE.md, hsp4-111-candidate.txt, hsp4-111-posted.txt, hsp4_radius_as_fetched.txt
candidate value (from CLAIM.md / hsp4-111-candidate.txt): r* = 0.237359570027502 (float recomputation from the 111 coordinate rows gives 0.23735957002750163; feasibility at 50 digits is the gate skeptic's job, not mine)

## Live fetches (one plain request each, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: 2026-10-16 17:55:18 UTC, HTTP 200, 5575 bytes
   row 111: "111 0.237355353009"
   file is byte-identical to hsp4_radius_as_fetched.txt (cmp). Candidate minus live = 4.217e-06, which exceeds the 1e-10 margin.

2. https://packomania.com/hsp4/hsp4.html
   time: 2026-10-16 17:55:19 UTC, HTTP 200, 88618 bytes
   "Last update: 06-Jul-2025" (also the page footer date).
   History of updates contains exactly three entries: 04-Jul-2025 (first presentation N = 2-100), 05-Jul-2025 (extension to N = 200), 06-Jul-2025 (extension to N = 300). No entry newer than 06-Jul-2025; no entry mentions N = 111. The only "111" occurrences on the page are the table row for N = 111 (radius 0.237355353009, reference [31]) and incidental counts in other rows.

3. https://packomania.com/pending-requests.html
   time: 2026-10-16 17:55:20 UTC, HTTP 200, 4954 bytes; page dated 08-Oct-2026
   Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one "*many*" bundle. No hsp4 (or hsp5/hsp6) entry at all, so no hsp4 range includes 111.
   QUEUE CAVEAT (unresolvable): the 26-Sep-2026 "Moki & Julio, *many*, 4666 candidates total" bundle is category-unspecified. It could in principle contain an hsp4 N = 111 candidate. This cannot be resolved from the page; per the bank entry, N = 111 must be re-checked against the live table once that bundle leaves the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: 2026-10-16 17:55:21 UTC, HTTP 200, 30936 bytes (100 lines)
   grep (case-insensitive) for "hsp4", "hypersphere", "packomania", and word "111": no matches. The file lists six families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer bound, VNN-COMP, RobustBench) plus cipher commitments; no hypersphere-packing entry.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: 2026-10-16 17:55:22 UTC, HTTP 200, 53 open PRs
   No open PR has target packomania-hyperspheres-hsp4-hsp6, and no title contains "111". The only PR whose title/body/branch matched "hsp[456]|hypersphere" is #231 (spherical-codes-cohn-table, (6, 526)), a different target. Packomania PRs present are scu (spheres in cube, N = 83, 507, 882-886) and cci (circles in circle, N = 4141); none is hsp4.

6. https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
   time: 2026-10-16 17:55:23 UTC, HTTP 200, tree not truncated
   known-knowns/packomania-hyperspheres-hsp4-hsp6/ holds twelve entries, object files hsp4-N-candidate.txt for N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75. N = 111 is not among them.

## Literature search (web, 2024-2026)

Queries: "packing 111 equal hyperspheres in a 4-dimensional ball best known radius 0.2373" and "hyperspheres packing in a hypersphere 4 dimensions N=111 2025 2026 arXiv packomania hsp4 improved".
Returned: Packomania ssp111 (3-D spheres in a sphere, not 4-D), Wikipedia "Sphere packing in a sphere" (3-D), arXiv 2305.10023 (3-D spheres in a sphere), Stoyan-Yaskov 2012 "Packing congruent hyperspheres into a hypersphere" (n-D, no N = 111 value), Sloane's 4-D tables (N up to 32), and unrelated density / jamming / hyperbolic-space papers. Nothing reports a best-known radius for 111 equal balls in a 4-ball, and nothing reports a value above the posted 0.237355353009. The only public table for this cell remains Packomania hsp4, whose live value is the one beaten.

## Assessment

- Live table value for N = 111 unchanged from the snapshot (0.237355353009); candidate exceeds it by 4.217e-06, well above the 1e-10 margin. Not a tie.
- No History-of-updates entry on the live hsp4.html newer than 06-Jul-2025, and none covers (4, 111).
- No hsp4 range on the pending-requests page includes 111 (no hsp entry at all). Caveat: the category-unspecified 4666-candidate bundle of 26-Sep-2026 cannot be resolved; recheck required once it clears.
- No match or better value in TROPHY_CASE.md, the merged hsp4 family (12 other N), the 53 open PRs, or the literature found.
- Isometry versus the posted packing is a gate/reproduce matter; not re-evaluated here beyond noting the claim asserts the sorted distance multisets differ.

Verdict: the candidate strictly beats everything known for (hsp4, N = 111) as of the fetch times above, subject to the unresolvable queue caveat stated.

pass: true
