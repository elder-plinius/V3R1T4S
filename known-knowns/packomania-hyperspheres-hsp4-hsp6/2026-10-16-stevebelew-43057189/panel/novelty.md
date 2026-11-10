# Novelty verdict, hsp4 N = 89

context: subagent (Claude Code Agent tool, fresh context for this one claim)
role: novelty skeptic (one of three). Scope: is the claimed radius strictly better than everything known, and is the cell unclaimed elsewhere. Feasibility and isometry are other skeptics' jobs; I only quote the claimed value.

Claim under test (from CLAIM.md and the header line of hsp4-89-candidate.txt): r* = 0.248005420084407 (header: r_float=0.24800542008440662) vs posted 0.247998099891; margin 7.320e-06, i.e. about 73 000 times the 1e-10 threshold.

## Fetches (one plain request each, User-Agent "V3R1T4S skeptic", no retries, times from date -u)

1. https://packomania.com/hsp4/txt/radius.txt
   time 2026-10-16T17:55:07Z, HTTP 200, 299 rows.
   Row 89 quoted verbatim: `89 0.247998099891`
   cmp against hsp4_radius_as_fetched.txt in the claim folder: byte-identical. The live table value is still the snapshot value, so the candidate strictly beats it by 7.32e-06 (more than 1e-10).

2. https://packomania.com/hsp4/hsp4.html
   time 2026-10-16T17:55:14Z, HTTP 200.
   Quoted: `Last update: 06-Jul-2025`
   History of updates contains exactly three entries: 04-Jul-2025 (first presentation N=2-100), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300). No entry newer than 06-Jul-2025; none mentions N=89. The only lines of the page containing "89" are the table row for N=89 (radius 0.247998099891, ref [31]) and a column value in the N=96 row.

3. https://packomania.com/pending-requests.html
   time 2026-10-16T17:55:21Z, HTTP 200, page dated 08-Oct-2026 (same date the bank entry's queue rule cites).
   No entry in category hsp4 (or any hsp category). Categories present: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one "*many*". So no hsp4 range includes 89.
   Near-miss noted for the record: "23-Sep-2026 17:00 Yuan Gao chx 2 candidates for 55, 89" is circles in a hexagon, a different category, not hsp4.
   Caveat that cannot be resolved: "26-Sep-2026 01:11 Moki & Julio *many* 4666 candidates total" is category-unspecified. It could in principle contain hsp4 N=89. Per the bank criterion the verdict must state this, and N=89 must be re-checked against the live table once that bundle leaves the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time 2026-10-16T17:55:28Z, HTTP 200, 30 936 bytes, 53 rows (families: degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, cipher commitments).
   grep for hsp4 / hsp / hypersphere / standalone 89: zero hits. No packing row at all in that file (it predates the hypersphere family; see item 6).

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time 2026-10-16T17:55:48Z, HTTP 200, 53 open PRs.
   Scanned titles and bodies for hsp / hypersphere / packomania / 89. Packomania-related open PRs: #238, #237, #236, #235 (scu, spheres in a cube, N=886/882/883/884), #234 (cci N=4141), #207 and #206 (scu N=83 and N=507 posted-coordinates discrepancies). None targets hsp4, hsp5, hsp6 or N=89. No other PR mentions hyperspheres in a ball.

6. https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
   time 2026-10-16T17:55:59Z, HTTP 200, 2659 entries, not truncated.
   known-knowns/packomania-hyperspheres-hsp4-hsp6/ holds twelve submission directories dated 2026-10-14 with object/hsp4-N-candidate.txt for N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75. Confirms the list given to me; 89 is not among them. No hsp5/hsp6 objects. Also present: known-unknowns/packings-physics/packomania-hyperspheres-hsp4-hsp6.md (the bank entry). No path anywhere contains hsp4-89.

## Literature search (last 24 months)

Three web searches (standard mode), 2026-10-16: "packing 89 equal hyperspheres in 4-dimensional ball best known radius 0.2479981"; "hyperspheres packing in a 4-ball N=89 / 89 hyperspheres packomania hsp4 2025 2026"; "best known packings equal balls in 4-dimensional unit ball new records 2025 2026 arXiv Packomania hsp4".
Returned: Packomania ssp (3-D) pages; arXiv 2305.10023 (equal spheres in a sphere, 3-D, 2023); Stoyan/Yaskov hypersphere-container papers (2020, outside the window, no N=89 value); Yahya-Szirmai 2025 (hyperbolic hyperball packings, unrelated); arXiv 2505.02394 (infinite lattice/non-lattice packings in dims 19-47); 2026 preprints.org and arXiv 2609.25120 on the infinite D4 / 24-cell problem (unrelated to finite packings in a ball); OEIS A084829 (3-D). No source in 2024-2026 lists a best-known packing of 89 equal balls in a 4-ball at all, let alone one with radius at or above 0.247998099891 other than Packomania's own table (reference [31], E. Specht, July 2025). Packomania hsp4 is, as far as I can find, the only public table for this problem.

## Conclusion

- Live table value for N=89 is unchanged (0.247998099891); candidate 0.248005420084407 strictly beats it by 7.32e-06, far above 1e-10. Not a tie.
- No History-of-updates entry newer than 06-Jul-2025; none covers (4,89).
- No hsp4 range on the pending list includes 89 (the only "89" there is category chx).
- Nothing in the literature, TROPHY_CASE.md, the merged hsp4 family (N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75) or the 53 open PRs matches or beats the candidate.
- Unresolvable caveat, stated as the bank requires: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and might contain hsp4 N=89; re-check the live table row for N=89 once that bundle disappears from the pending list.

pass: true
