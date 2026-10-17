# Criterion skeptic verdict — packomania-cci-equal-circles-in-circle, partial win p2, one cell N = 4141

Judged only from the claim folder (CLAIM.md, REPRODUCE.md, verify_standalone.py, candidate_N4141.txt,
radius.txt, cci4141.txt, table_record.md) plus code I wrote myself and one fetch each of the three
public pages named by the criterion. All numbers below are from my own command output, except where
explicitly attributed to the author's checker, which I read and re-ran.

## Clause-by-clause judgement

**1. "N > 2600 that the table lists" / gap value.** radius.txt (packaged, sha256 matches the sha256
recorded in table_record.md: 6c60da0a...ead) lists row `4141 0.014601755763187308074373236782` at
line 2711; 4141 > 2600. The rows above 2600 are sparse (2611, 2623, ..., 4141, 4483, 4495, 5000) —
the gap-value class p2's examples (4495, 5000) come from. My own live re-fetch of the same table on
2026-10-16 returns the identical row 4141 value, so the beaten baseline is current. SATISFIED.

**2. Numeric bar: r* strictly greater than the 30-decimal live table value by >= 1e-11.** I wrote my
own checker (not the author's): float64 pass locates near-min pairs (relative window 1e-6, far above
double rounding error) and near-max norms, then Decimal at 70 digits and mpmath at dps=50 recompute
exactly those quantities from the coordinate strings. Results:
- candidate_N4141.txt: 4141 two-token lines, all 18-decimal strings, no duplicates; dmin/2 =
  0.01460947144881393457598562453074562973768387172171891875111...; 1 - max|c| =
  0.01460947144881400784693320774118... (max|c| = 0.98539052855118599...); half-distance binds;
  r* = 0.0146094714488139345759856245307456297... — identical to the claimed value to all 32 printed
  digits (difference -4.4e-33); mpmath dps=50 from strings gives the same value to 50 digits, meeting
  the criterion's "computed in mpmath at 50 digits directly from the submitted coordinates (no
  tolerance)" literally.
- margin over table value 0.014601755763187308074373236782 = 7.7156856266265016...e-6 >= 1e-11
  (six orders of magnitude above the threshold; 1e-11-level ambiguity is impossible here since both
  computations are string-exact and the two r* terms are balanced only to 7.3e-17).
- The author's verify_standalone.py, read and re-run from the claim folder, reproduces
  r* = 0.0146094714488139345759856245307456297..., margin 7.7156856266265...e-6, PASS.
SATISFIED.

**3. Baseline honesty (posted config vs its own table value).** My string-exact recomputation of the
posted cci4141.txt gives r* = 0.014601755763187308074373236781170572..., i.e. the table value sits at
the posted configuration's own feasible radius to within 8.3e-31 (table_record.md reports -1.01e-16,
an artifact of its float64 input pass; both are >= 15 orders below the margin). The claim measures its
margin against the table value, the marginally harder baseline, and the candidate also beats the
posted configuration's actual feasible radius by the same 7.7157e-6. No inflated baseline. SATISFIED.

**4. Non-isometry clause.** Independently computed sorted pairwise-distance multisets (8,571,870
distances each): max elementwise difference 1.912e-2; 8,571,866 of 8,571,870 entries differ by > 1e-9;
even the extremes differ (min-distance level 0.029218942898 vs 0.029203511526; max pair distance
1.968107831 vs 1.970796488). Any isometry preserves the full distance multiset, so the configurations
are not isometric. SATISFIED.

**5. History-of-updates clause.** My own fetch of the live cci.html (2026-10-16): "Last update:
25-Dec-2024"; 68 dated history lines; none mentions N = 4141 (as a standalone number) at all, so a
fortiori none newer than the scout's fetch this run. (table_record.md says 67 dated lines — an
off-by-one in its counting; immaterial.) SATISFIED.

**6. Queue rule.** My own fetch of pending-requests.html (page dated 08-Oct-2026) confirms the scout's
parse: pending entries exist only for csc, ccq, crt, csq, chx (55, 89), cpt, crc, cxd, csqv; there are
no cci entries, so N = 4141 lies in no queue range for this category. SATISFIED, with the mandatory
caveat below.

**7. Mandatory caveat (category-unspecified bundle).** The 26-Sep-2026 "Moki & Julio *many* 4666
candidates total" bundle is still on the live pending page and cannot be resolved to a category.
STATED here as required: N = 4141 must be re-checked against the live table once that bundle
disappears from the pending list before this result is treated as final.

**8. Container-centred convention.** All 4141 submitted centres satisfy |c| < 1 strictly
(max |c| = 0.98539052855118599...), container unit circle centred at the origin, and the criterion's
own r* formula (1 - max|c|) enforces the convention; the wall term is positive and nearly balanced
against the half-distance term, as expected for a genuine packing. SATISFIED.

**9. One object / one table cell.** The claim asserts exactly one cell (N = 4141) and one object
(candidate_N4141.txt); no other N is claimed or implied. SATISFIED.

**10. p2 phrasing ("record is a lattice-like seed by Specht rather than an optimized packing").**
Provenance: the live cci.html row for 4141 cites reference [31], whose text is "program cci,
1999–2024" — the construction program of the site's author (page copyright E. Specht), not one of the
optimization-study references the table uses elsewhere (Stoyan/Yaskov [20] is cited by N=5000, Lai et
al. [21], batch-optimization [22], Monte-Carlo [23]; none is cited by row 4141). Geometry: the posted
configuration is lattice-derived — 7521 pair distances sit within 1e-12 relative of its minimum
(an exact-contact core) with a thin 0.1% relaxation continuum above it — consistent with a lightly
relaxed lattice seed rather than a heavily optimized packing. For contrast, the candidate itself fits
a pure triangular lattice with max residual 3.6e-16 (all 12189 near-min pairs at one single distance,
relative spread 1.9e-14): the win is a better construction over an unoptimized record, exactly the
scenario p2 describes. I am satisfied the p2 clause is honestly met, not stretched. SATISFIED.

**11. Prereg / null model.** The frozen prereg line exempts the null test because the claim is an
explicit object checked by a deterministic evaluator against a live table value. I hunted for hidden
statistical quantifiers ("beats chance", search-strength claims): there are none — every clause is a
deterministic comparison, and the win reduces to one file beating one table cell by a margin. The
exemption is appropriate; no null model is needed for this claim type. ACCEPTED.

**12. Subsumption.** The live table row is unchanged today, the construction is new (non-isometric to
the posted one), and no submission was made or claimed (verified-construction-only). Not subsumed by
any prior result in or out of the package. SATISFIED.

## confirmed_scope

confirmed_scope: For the single Packomania cci table cell N = 4141 (live row fetched 2026-10-16,
value 0.014601755763187308074373236782), the 4141 container-centred centres in candidate_N4141.txt —
a non-isometric pure triangular-lattice construction with max|c| = 0.9853905285512 — give feasible
radius r* = 0.0146094714488139345759856245307 computed exactly from the submitted 18-decimal strings
(independently reproduced at Decimal 70 and mpmath dps 50), which exceeds that live table value by
7.7157e-6 (>= 1e-11), thereby satisfying partial win p2 for one listed gap value N > 2600 whose
record (reference "program cci", Specht) is a lattice-like seed rather than an optimized packing —
subject to the mandatory caveat that the category-unspecified 26-Sep-2026 "Moki & Julio *many*"
4666-candidate bundle remains on the pending list and N = 4141 must be re-checked against the live
table once it disappears.

context: zcode Agent-tool subagent, fresh context
pass: true
