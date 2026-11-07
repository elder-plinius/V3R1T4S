# Novelty verdict, hsp4 N = 88

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Claim under review (CLAIM.md): 88 equal balls in the unit 4-ball with feasible radius
r* = 0.248514071390400... (hsp4-88-candidate.txt), vs Packomania's posted 0.248505598356.
Margin = 8.473e-06, i.e. about 84,700x the 1e-10 threshold.

## Fetches (each URL requested exactly once, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: Fri Oct 16 17:48:33 UTC 2026, HTTP 200
   row 88 (line 87 of the file): `88 0.248505598356`
   The live file is byte-identical to hsp4_radius_as_fetched.txt in the claim folder
   (cmp reports identical; md5 deb4cbcd0a0131989fbf6d1adf1e85f9 for both).
   So the candidate still strictly beats the live table value, by 8.47e-06 (greater than 1e-10).

2. https://packomania.com/hsp4/hsp4.html
   time: Fri Oct 16 17:48:34 UTC 2026, HTTP 200
   quoted: `Last update: 06-Jul-2025`
   History of updates contains exactly three entries: 04-Jul-2025 (first presentation N = 2-100),
   05-Jul-2025 (extension to N = 200), 06-Jul-2025 (extension to N = 300), all by E. Specht [31].
   No entry newer than 06-Jul-2025; no entry mentions N = 88. The table row for N = 88 on that page
   reads `88 0.248505598356 0.661363804740 4.0240542129 ...`, matching radius.txt.

3. https://packomania.com/pending-requests.html
   time: Fri Oct 16 17:48:36 UTC 2026, HTTP 200
   page dated 08-Oct-2026. Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one
   `*many*`. There is NO entry with category hsp4 (or any hsp category), so no hsp4 range includes 88.
   Queue caveat (unresolvable): the 26-Sep-2026 01:11 "Moki and Julio, *many*, 4666 candidates total"
   bundle names no category and no N range. It could in principle contain an hsp4 N = 88 candidate.
   This cannot be decided from the page; per the bank's queue rule, N = 88 must be re-checked against
   the live table once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: Fri Oct 16 17:48:37 UTC 2026, HTTP 200 (30,936 bytes)
   grep (case-insensitive) for `hsp4`, `hypersphere`, and the standalone number `88`: zero matches.
   The file describes six result families (degree-diameter graphs, constant-weight codes, matrix
   multiplication, Lehmer bound, VNN-COMP, RobustBench) plus cipher commitments; it does not mention
   the Packomania hypersphere family at all.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: Fri Oct 16 17:48:37 UTC 2026, HTTP 200
   52 open PRs. None has `hsp4`, `hypersphere` or `4-ball` in title or body. The Packomania-related
   open PRs are for other targets only: scu (spheres in a cube, N = 882/883/884/886, plus two
   posted-coordinate discrepancy reports for N = 83 and 507), cci (N = 4141), and the Cohn spherical
   codes table (6, 526). No open PR targets packomania-hyperspheres-hsp4-hsp6 or N = 88.

6. https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
   time: Fri Oct 16 17:48:39 UTC 2026, HTTP 200
   The merged family holds exactly 12 dated subdirectories (all dated 2026-10-14). That count matches
   the 12 values the panel brief lists for the family (N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69,
   74, 75). The directory names are hash-suffixed and do not encode N, so I could not independently
   confirm each N from this single fetch; the count is consistent with the brief and 88 is not among
   the listed values. CLAIM.md's own note refers to earlier confirmed improvements for N in
   (68, 69, 74, 75, 76), none of which is 88.

## Literature search (public web, 2024-2026)

Queries run (WebSearch, four queries, one in extended mode):
- "packing 88 equal hyperspheres in a 4-dimensional ball best known radius 2025 2026"
- "hyperspheres" "4-ball" OR "4-dimensional ball" packing N=88 radius 0.2485
- "packomania hsp4 improved packings hyperspheres in hypersphere 2026"
- arXiv 2024-2026 "equal spheres"/"hyperspheres" "in a sphere" dimension 4 N up to 300 Specht table

Results: nothing from 2024-2026 lists best-known packings of 88 equal balls in a 4-ball, and no source
reports a radius for (4, 88) above 0.248505598356. The hits were either the 3-dimensional
spheres-in-a-sphere problem (Zhou et al., arXiv 2305.10023, 2023, which cites Packomania's 3D tables),
unbounded 4-space sphere packing density papers (24-cell conjecture, D4 lattice, AI density bounds),
the 2012 Stoyan/Yaskov hypersphere-in-hypersphere paper (predates the 2025 hsp4 table), or codes.se
4D packings normalised by minimum distance rather than a unit container. The only tabulation of this
exact problem that I could find is Packomania's hsp4 page itself, whose value for 88 is quoted above.

## Assessment

- Live table value for N = 88 is unchanged from the snapshot: 0.248505598356. Candidate 0.2485140713904
  strictly beats it by 8.47e-06, far above the 1e-10 threshold. Not a tie.
- No History-of-updates entry on hsp4.html newer than 06-Jul-2025; none covers (4, 88).
- No hsp4 range on the pending-requests page; the category-unspecified Moki and Julio bundle of
  26-Sep-2026 (4666 candidates) is the one caveat and cannot be resolved from public pages.
- TROPHY_CASE.md, the merged hsp4-hsp6 family (12 entries, 88 not among them per the brief), and the
  52 open PRs contain nothing for (4, 88).
- The literature search found nothing matching or beating the candidate.

Residual uncertainties: (a) the unresolvable queue bundle above; (b) the merged family's N values
were taken from the panel brief and only the directory count (12) was confirmed from the API listing.
Neither identifies any known result at or above the candidate radius, so novelty is confirmed on all
checkable sources.

pass: true
