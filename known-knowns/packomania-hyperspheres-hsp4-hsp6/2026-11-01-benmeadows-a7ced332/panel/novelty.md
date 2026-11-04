# NOVELTY verdict: hsp4-N156

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:13Z

## Value computed here
- Object `claim/hsp4-156.txt`: sha256 a7ced332…483f3b matches CLAIM.md. It has 156 rows of 4 coordinates (17 significant digits), with no duplicates and no NaN.
- r* = 0.220313764152318248389127010874. Two independent computations agree to all printed digits: mpmath at 50 digits, and exact Fractions with 50-digit Decimal square roots.
  - Binding term: 1 - max|c_i| = 0.2203137641523182483891270.
  - Half minimum distance: 0.2203137811634562339267044.
- Live table row 156 = 0.220308265077, so r* - table = 5.499075e-6.
- Live re-fetch: the files in `evidence/` were fetched by the repository owner on 2026-11-01T14:32Z from an unrestricted machine, and they serve as this panel's live re-fetch. All 8 sha256 values in FETCHED.md match the `sha256sum` output computed here.
- `injection_suspected`: none. The `#` header line in the object only states the claimant's values, and they were not used.

## Clauses checked
- **1 Value:** r* - table = 5.499e-6, which is ≥ 1e-10. **pass**
- **2 Parser sanity:** The posted `hsp4-156.txt` is byte-identical to the copy inside `hsp4_coords.tar.gz`. Its radius at 50 digits is 0.220308265076556427141. It differs from both the header and the table row (0.220308265077) by -4.44e-13, so it reproduces them to 1e-11. **pass**, and clauses 3 and 4 apply.
- **3 Non-isometry:** Over the 12090 sorted pairwise distances, the claim and the posted file differ by at most 7.69e-3, which exceeds 1e-8. For information, the sorted centre norms differ by at most 1.99e-2. **pass**
- **4 Polish floor:** I wrote my own sequential-LP polisher (HiGHS). It uses:
  - near-active pairs (distance < 2r + 4Δ + extra) and near-active walls;
  - a box trust region Δ on every coordinate;
  - acceptance only if the exactly recomputed radius increases;
  - shrinking Δ after a rejected step and growing it when the step reaches the box.

  It started from the posted coordinates. Every schedule ran until Δ < 1e-13. Final radii were recomputed at 50 digits from the polished coordinates.

  | schedule | Δmax | shrink | margin extra | iterations | final radius (50 digits) | gain over header |
  |---|---|---|---|---|---|---|
  | S1 | 1e-2 | 0.5 | 1e-3 | 82 | 0.22030826603323311032 | 9.562e-10 |
  | S2 | 1e-3 | 0.5 | 1e-3 | 83 | 0.22030826603323309988 | 9.562e-10 |
  | S3 | 1e-4 | 0.5 | 1e-3 | 73 | 0.22030826603323311120 | 9.562e-10 |
  | S4 | 1e-2 | 0.25 | 1e-2 | 47 | 0.22030826603323316843 | 9.562e-10 |
  | S5 | 1e-3 | 0.7 | 1e-4 | 266 | 0.22030826603323311724 | 9.562e-10 |

  The highest polished radius is 0.2203082660332331684, and r* minus it is 5.498e-6, which is ≥ 1e-9.

  As a sanity check, the same polisher applied to the claim raises it by 1.42e-7, so the polisher does move non-stationary packings. **pass**
- **5 Not a relaxed copy:** The claim says its starts were random configurations, D4/A4 cuts, shell seeds and its own lane's neighbouring-N packings, and it names no posted packing. I do not have the claimant's search code. My own evidence:
  - All five polishes of the posted file stop at 0.22030826603, which is 5.5e-6 below the claim. The claim therefore lies in a different local maximum from the posted packing.
  - The claim's distance multiset differs from the polished posted packing's by 7.72e-3.
  - Contact graphs at tolerance 1e-6 are close but not identical:

    | | contacts | degree histogram (degrees 0–11) |
    |---|---|---|
    | claim | 474 | [0,0,0,0,10,41,54,35,12,3,0,1] |
    | posted | 473 | [1,0,0,0,11,35,66,25,9,7,1,1] |

    The posted packing has 1 rattler and the claim has none.
  - The overall layout is shared: both have 141 wall balls and 15 inner balls. That is the natural shell structure for this N and is not evidence of copying.

  Nothing indicates that the claim derives from a posted packing. **pass**
- **6 History of updates:** `hsp4.html` shows "Last update: 06-Jul-2025". Its History-of-updates entries are 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to N=200) and 06-Jul-2025 (extension to N=300). No entry is newer than the table snapshot, and none names N = 156 individually. **pass**
- **7 Queue rule:** `pending.html` (dated 30-Oct-2026) lists no range for category hsp4. Its categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus one unspecified bundle, so N = 156 lies in no hsp4 range. **pass**

  Caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not say which category it covers, and this cannot be resolved. N = 156 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio manifest:** The row `hsp4,156` has published_radius 0.220308265077 and new_radius 0.2203114439611080125824693 (kind "UNCLEAR (alignment)"). r* - new_radius = 2.32e-6, which is ≥ 1e-10. It is the only hsp4 row with N = 156, and no other row carries a radius near 0.2203. The other N = 156 rows are hsp5, hsp6, cpt and crc_*, which are different cells. **pass**
- **9 Other prior work:**
  - Claims list: there is no open, closed or merged claim PR for hsp4 N = 156 (the hsp4 claims cover N = 30–119, 170 and 301).
  - `TROPHY_CASE.md` has no hsp entry.
  - Spherical-code constructions from `spherical_plain_live.txt`:
    - (4,156), cosine c = 0.852364181174, gives s/(2+s) = 0.213647626609, which is 6.67e-3 below r*.
    - (4,155) with a centre ball, cosine c = 0.850521509148, gives min(1/3, s/(2+s)) = 0.214691423246, which is 5.62e-3 below r*.

  **pass**

## Decision
All nine clauses pass on numbers computed here. The claimed packing beats the live table row 0.220308265077 by 5.50e-6. It also beats the best published competitor, Moki & Julio's manifest radius 0.22031144396, by 2.32e-6.

On the prior-work clauses:
- No History-of-updates entry after 06-Jul-2025 touches N = 156.
- No hsp4 range appears in the 30-Oct-2026 pending list. The unresolved category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle still means N = 156 must be re-checked against the live table once that bundle leaves the pending list.
- There is no prior claim or trophy entry for this cell.
- The spherical-code constructions fall well short of r*.

The posted packing polishes only to 0.2203082660 under five trust-region schedules, so the claim is a distinct local optimum and not a relaxed copy. I could not inspect the claimant's search code.

pass: true
