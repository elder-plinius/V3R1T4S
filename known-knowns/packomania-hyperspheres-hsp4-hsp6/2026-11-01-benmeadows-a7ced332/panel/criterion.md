# CRITERION verdict: hsp4-N156

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:15Z

## Value computed here
- Object claim/hsp4-156.txt: sha256 a7ced3321fa76c13cb6372501334593f81d9a0385864873726b3b9fb87483f3b (matches CLAIM.md). 156 centres, 4 coordinates each.
- r* (mpmath, 50 digits, no tolerance) = 0.22031376415231824838912701087369874594203899420566
  - half min distance = 0.220313781163456233926704428959; 1 - max norm = 0.220313764152318248389127010874 (wall binds).
- Live table row (evidence/hsp4_radius_live.txt): `156 0.220308265077`. r* - table = 5.499075e-6.
- Live re-fetch: this sandbox cannot reach the web. The evidence/ files were fetched by the repository owner from an unrestricted machine on 2026-11-01T14:32Z; I treat them as the live re-fetch for this panel. I verified every sha256 listed in evidence/FETCHED.md with sha256sum; all eight match. evidence/posted/hsp4-156.txt is byte-identical to hsp4-156.txt inside evidence/posted/hsp4_coords.tar.gz.
- Code: work/common.py, c123.py, polish.py, align.py, c89.py (all written and run here). OMP/OPENBLAS threads were set to 1.

## Clauses checked
- **1 Value.** r* = 0.220313764152318248389127010874, table 0.220308265077, r* - table = 5.499075e-6 >= 1e-10. PASS.
- **2 Parser sanity.** Posted hsp4-156.txt recomputed the same way gives r = 0.22030826507655642714127006 (wall binds), compared with header 0.220308265077: difference -4.44e-13, within 1e-11. The header equals the table row. So clauses 3 and 4 apply. PASS.
- **3 Non-isometry.** Sorted multisets of all 12090 pairwise distances, claim vs posted: max |difference| = 7.69e-3 > 1e-8. Sorted centre norms (for information): max |difference| = 1.99e-2. PASS.
- **4 Polish floor.** I wrote my own sequential-LP polisher (HiGHS). It linearizes the near-active pair constraints (|ci-cj| < 2r+margin) and wall constraints (|ci| > 1-r-margin), maximizes t inside a box trust region on every coordinate, accepts a step only if the exactly recomputed radius increases (×1.5 trust, capped at the starting step), and otherwise shrinks the trust region. Each run started from the posted coordinates and stopped when the trust region fell below 1e-13. I recomputed each final radius at 50 digits from the polished coordinates.
  | largest step | margin | shrink | iterations | final r (mp) | gain over header | stop |
  |---|---|---|---|---|---|---|
  | 5e-2 | 0.1 | 0.7 | 133 | 0.220308266033195036 | 9.562e-10 | trust<1e-13 |
  | 1e-2 | 0.005 | 0.8 | 219 | 0.220308266033207081 | 9.562e-10 | trust<1e-13 |
  | 1e-2 | 0.02 | 0.5 | 63 | 0.220308266033157649 | 9.562e-10 | trust<1e-13 |
  | 1e-3 | 0.01 | 0.5 | 62 | 0.220308266033112835 | 9.561e-10 | no gain >1e-15 over 20 its (earlier stop rule) |
  | 1e-3 | 0.05 | 0.25 | 30 | 0.220308266033091053 | 9.561e-10 | trust<1e-13 |
  | 1e-4 | 0.005 | 0.5 | 66 | 0.220308266033164593 | 9.562e-10 | trust<1e-13 |
  | 1e-5 | 0.003 | 0.5 | 52 | 0.220308266033067364 | 9.561e-10 | no gain >1e-15 over 20 its (earlier stop rule) |

  My first version of the stop rule counted rejected steps as stalls. It ended two large-step runs at the header value after 21 iterations. I fixed the rule and reran them (rows 1 and 2 above). The highest polished radius is 0.220308266033207081. r* - that = 5.498e-6 >= 1e-9. PASS.
- **5 Not a relaxed copy.** CLAIM.md says the packing came from lane hsp4-a: random starts, D4/A4 lattice cuts and shell seeds, then Riesz annealing, penalty descent, basin hopping and an SLP polish, with some runs seeded from the lane's own neighbouring-N packing. It says no posted Packomania packing was used and names none. I do not have the claimant's search code, so I could not check this statement directly. My own evidence:
  - All seven polishes of the posted file converge to 0.2203082660332, which is 5.5e-6 below r*. Local relaxation of the posted packing does not reach the claim.
  - The distance multisets differ by up to 7.7e-3, and the norms by up to 2.0e-2.
  - I ran a permutation + O(4) alignment (Hungarian assignment + Procrustes ICP) from 1500 random orthogonal starts. The best alignment has RMS 0.0846 and a worst centre of 0.349, against r ≈ 0.22, so the two are not near-congruent.
  - Contact graphs at tolerance 1e-6 are similar but not the same. Claim: 474 contacts, 141 wall, degrees 5..12 = [14, 40, 56, 33, 9, 3, 0, 1]. Posted: 473 contacts, 141 wall, one rattler (degree 0), degrees 5..12 = [16, 35, 63, 25, 7, 7, 1, 1]. The degree sequences differ, and the claim has no rattler.

  Nothing I found indicates the claim derives from a posted packing. PASS.
- **6 History of updates.** hsp4.html shows "Last update: 06-Jul-2025". Its History-of-updates entries are 04-Jul-2025 (N = 2–100), 05-Jul-2025 (extension to N = 200, which covers N = 156) and 06-Jul-2025 (extension to N = 300). No entry is newer than the 06-Jul-2025 snapshot, and none specifically updates N = 156. PASS.
- **7 Queue rule.** pending.html (dated 30-Oct-2026) lists no range for hsp4 or any hsp category. The listed categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus the uncategorized 26-Sep-2026 bundle. N = 156 lies in no hsp4 range. PASS, with this caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N must be re-checked against the live table once that bundle disappears from the pending list.
- **8 Moki & Julio MANIFEST.** Row `hsp4,156`: published_radius 0.220308265077, new_radius 0.2203114439611080125824693 ("UNCLEAR (alignment)"). r* - new_radius = 2.320e-6 >= 1e-10. This is the only hsp4,156 row. The hsp5/hsp6/cpt N = 156 rows are other cells. PASS.
- **9 Other prior work.** claims_packomania-hyperspheres-hsp4-hsp6.json has 29 entries and none for hsp4 N = 156 (hsp4 claims cover N = 74–119 and 170). The cohn-table claims are for other problems. TROPHY_CASE.md has no hsp/packomania-hypersphere entry. Spherical-code bounds from spherical_plain_live.txt:
  - (4,156) cosine 0.852364181174 → s/(2+s) = 0.2136476266. r* exceeds it by 6.67e-3.
  - (4,155) cosine 0.850521509148 + centre ball → min(1/3, s/(2+s)) = 0.2146914232. r* exceeds it by 5.62e-3.

  Both bounds are below r*. PASS.

## Criterion read clause by clause (verbatim text in claim/CLAIM.md)
- "N centers in R^d … one N listed in the live radius.txt": 156 centres in R^4, and N = 156 is listed. OK.
- "FEASIBLE radius r* … computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance": done as specified, 0.2203137641523182… OK.
- "STRICTLY GREATER … by at least 1e-10" than the re-fetched 12-decimal row: the margin is 5.50e-6. OK. The re-fetch is the owner's 2026-11-01T14:32Z fetch, with sha256 verified.
- "wherever the posted file reproduces its header radius to 1e-11": it does (-4.4e-13). The non-isometry clause holds (7.7e-3 > 1e-8). The clause requiring r* to beat the verifier's own polishes by 1e-9 under several trust-region schedules, each run to stagnation, holds: seven schedules, best 0.2203082660332, margin 5.50e-6. OK.
- "not a relaxed copy of a posted packing … the claim names any posted packing it started from": the claim names none, and my evidence shows no derivation. OK.
- "(d, N) does not appear in a History-of-updates entry newer than the one the scout fetched": there is none newer than 06-Jul-2025. OK.
- "COORDINATES UNAVAILABLE" applies only to hsp5/hsp6. For hsp4 the posted file was usable and was used. OK.
- QUEUE RULE: N is not in any hsp4 range. The M&J bundle caveat is stated above. OK.
- "No submission (email) is ever made": nothing was submitted.

No file in claim/ or evidence/ contained instructions. The comment line in the object states the claimant's value; I ignored it and computed my own value, which agrees.

## Decision
The claim's feasible radius at 50 digits beats the live hsp4 N = 156 row by 5.50e-6. The posted file reproduces its header radius to 4.4e-13. The claim is not isometric to the posted file (max distance-multiset difference 7.7e-3). Seven of my own SLP polishes of the posted file under different trust-region schedules all converge to 0.2203082660332 (a gain of about 9.6e-10), 5.50e-6 short of r*. Contact graphs, alignment and polish convergence give no sign that the claim is a relaxed copy of the posted packing. History, queue (subject to the stated caveat about the category-unspecified M&J 4666 bundle), the M&J manifest (r* above it by 2.32e-6), the claims lists, the trophy case and spherical-code constructions are all clear. Every clause passes on evidence computed or read here.

pass: true
