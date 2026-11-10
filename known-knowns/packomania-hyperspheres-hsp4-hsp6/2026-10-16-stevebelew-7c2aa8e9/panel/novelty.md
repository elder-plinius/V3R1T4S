# Novelty verdict, hsp4 N = 83

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Claim under test (CLAIM.md, object hsp4-83-candidate.txt): feasible radius r* = 0.252010684947089 for 83 equal balls in the unit 4-ball, vs Packomania's posted 0.252008330509 (margin 2.354e-06, which is 23 544 times the 1e-10 threshold).

## Fetches (one plain request each, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: Fri Oct 16 21:25:18 UTC 2026, HTTP 200, 299 rows
   row 83: `83 0.252008330509`
   byte-identical (diff empty) to the claim's snapshot hsp4_radius_as_fetched.txt, md5 deb4cbcd0a0131989fbf6d1adf1e85f9.
2. https://packomania.com/hsp4/hsp4.html
   time: Fri Oct 16 21:25:19 UTC 2026, HTTP 200
   "Last update: 06-Jul-2025"
   History of updates (complete): 04-Jul-2025 first presentation N=2-100; 05-Jul-2025 extension to N=200; 06-Jul-2025 extension to N=300. No entry newer than 06-Jul-2025, none mentioning N=83. The only "83" occurrences in the page text are the table row itself (radius 0.252008330509, ref [31]) and a boundary-count column value in another row.
3. https://packomania.com/pending-requests.html
   time: Fri Oct 16 21:25:20 UTC 2026, HTTP 200, page dated 08-Oct-2026
   Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, plus one "*many*" bundle. No hsp4 (or hsp5/hsp6) entry, so no hsp4 range includes 83.
   Queue caveat: the 26-Sep-2026 01:11 "Moki & Julio *many* 4666 candidates total" bundle has no category and cannot be resolved; it could in principle contain hsp4 candidates, including N=83. The N must be re-checked against the live table once that bundle leaves the pending list.
4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: Fri Oct 16 21:25:21 UTC 2026, HTTP 200, 30 936 bytes
   grep for hsp4, hypersphere, packomania, sphere, ball and the standalone number 83: zero hits. The trophy case lists six families (degree-diameter graphs, Lehmer, matrix multiplication, VNN-COMP, RobustBench, constant-weight codes) and two cipher commitments; no packing family at all.
5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: Fri Oct 16 21:25:21 UTC 2026, HTTP 200, 78 open PRs
   Open PRs for packomania-hyperspheres-hsp4-hsp6 (all drafts): PR 242 N=79, 243 N=67, 244 N=91, 245 N=81, 246 N=88, 247 N=94, 248 N=89, 249 N=74, 250 N=80, 251 N=111. None is N=83. The only other PR whose text contains "83" is PR 231 (spherical-codes-cohn-table, the digits occur inside a hash), unrelated.
6. https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
   time: Fri Oct 16 21:25:23 UTC 2026, HTTP 200
   12 subdirectories, all dated 2026-10-14.
7. https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 (one extra fetch to resolve the N of each subdirectory from file names; not truncated)
   time: Fri Oct 16 21:26:12 UTC 2026, HTTP 200
   (d,N) present in the merged family: (4,30) (4,35) (4,42) (4,48) (4,54) (4,62) (4,63) (4,64) (4,66) (4,69) (4,74) (4,75). No 83. No path anywhere in main mentions hsp4-83.

## Literature search

Two web searches (standard mode): "packing 83 equal hyperspheres in a 4-dimensional ball best known radius 2025 2026" and "hsp4 packomania hyperspheres 4-ball improved packings arXiv". Results: arXiv 2305.10023 (3D spheres in a sphere), Packomania ssp pages (3D), OEIS A084828/A084829, a 2012 Stoyan/Yaskov hypersphere-in-hypersphere paper (n = 2..24, no 4D table for N=83 surfaced), hyperbolic-space packing papers. Nothing from 2024-2026 lists a packing of 83 equal balls in a 4-ball, let alone one with radius at or above 0.252010684947089. The only public table for (4,83) is Packomania's, reference [31] (E. Specht, July 2025), at 0.252008330509.

## Assessment

- Live table value for N=83 is still 0.252008330509 (snapshot unchanged), so the candidate strictly beats it by 2.35e-06, far above the 1e-10 threshold.
- No History-of-updates entry newer than 06-Jul-2025; none covers (4,83).
- No hsp4 range in the pending queue; caveat above on the category-unspecified 4666-candidate bundle stands and is unresolvable today.
- Nothing in TROPHY_CASE.md, the merged known-knowns family, the open PRs, or the literature matches or beats the candidate.
- Isometry to the posted packing is the correctness skeptics' question; novelty-wise the posted radius differs from the candidate by far more than the table's rounding, so the objects cannot be the same packing.

pass: true
