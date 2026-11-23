# REPRODUCE skeptic verdict — BORDA-12 (2026-11-19)

context: subagent (fresh panel context, claim package only)

Role: REPRODUCE skeptic. Judged only from the claim package
(claim.md, PREREG.md, REPRODUCE.md, score_borda12.csv,
build_borda12.log, diagnostics.log, null_test.md, scout.md, target.md,
code/, data/) and from my own fresh code. I wrote my own checker from
the criterion quoted in claim.md BEFORE reading the author's
checker.py, and ran it before reading the author's build code.

## 1. Own checker (written from the criterion, before reading author code)

Criterion quoted in claim.md: a saved score file with one real-valued
prediction per mutant in the ProteinGym reference CSV, Spearman
recomputed with the official convention (same mutant set, same
direction, same NaN handling) strictly higher than the max over all
model columns for that assay in the live DMS-level Spearman CSV by at
least 0.015 absolute.

Results (all from my own code, scipy + a hand-written average-rank
Pearson cross-check):

- sha256: score_borda12.csv fe21f86c... (matches claim.md exactly);
  reference_Matreyek_2021.csv 1c52aba9... (matches); live CSV
  f432423b... (matches).
- Score file: columns exactly [mutant, score]; 5,083 rows; 0 duplicate
  mutants; 0 NaNs; all values finite and in [0, 1] (min 0.019964, max
  0.983766, as expected for a mean of percentile ranks); mutant set
  exactly equals the reference set (0 only-in-either); row order
  identical to the reference.
- Spearman: scipy rho = 0.5682423873; hand-written rank-Pearson rho =
  0.5682423873 (|diff| = 1.1e-16). Rounds to 0.5682 as claimed.
- Direction: negated scores give rho = -0.5682423873 (exact negative).
- Fixtures: score = DMS_score -> 1.0; negated -> -1.0; constant ->
  NaN. All as required.
- Live bar, recomputed from claim/data/live_Spearman_DMS_level.csv:
  row PTEN_HUMAN_Matreyek_2021 exists exactly once. Model columns =
  97 (all columns except the 6 metadata columns: DMS ID, Number of
  Mutants, Selection Type, UniProt ID, MSA_Neff_L_category, Taxon).
  All 97 are numeric for this row. Row max = 0.516 (VenusREM); bar =
  0.531. Margin: rho - 0.516 = 0.0522 >= 0.015. rho > 0.531 and rho >
  0.5658 (M1) by 0.0024.
  - Note on my own check: my first pass excluded only DMS ID and
    Number of Mutants as metadata and flagged 4 non-numeric columns.
    Those 4 are genuine metadata (Selection Type, UniProt ID,
    MSA_Neff_L_category, Taxon), not model columns; with the correct
    6-column metadata exclusion the check passes and the row max is
    unchanged. The flag was my checker's error, not the claim's.
- G2 gate: claim/data/score_E2.csv reproduces rho = 0.3666264379 ->
  0.3666 as claimed (5,083 rows, exact mutant-set match).
- Independent Borda recompute from the PREREG definition (fresh code,
  no author code): percentile rank rank/(n-1), ties averaged,
  ascending, mean over the 12 member columns (VenusREM, ProSST-128,
  ProSST-512, ProSST-1024, ProSST-2048, ProSST-4096, S3F, S3F_MSA,
  S2F_MSA, ESCOTT, ESM3, RSALOR) read from
  claim/data/assay_scores_Matreyek_2021.csv. All 12 columns present,
  0 NaNs in any member, assay mutant set exactly equals the reference
  set. Max |diff| vs the claimed score file = 3.33e-16. Independent
  rho = 0.5682432089 vs claimed 0.5682423873 (|diff| = 8.2e-07, within
  the 1e-6 tolerance).
- Null test, re-run myself with a DIFFERENT seed (20261120, not the
  claimed 20261119): 400 permutations of the Borda scores, best
  control rho = 0.0372 vs claimed best 0.0398 (different seed, same
  magnitude); real 0.5682 beats all 400 fresh controls.

## 2. Rebuild from the author's build code

- claim/code/build_borda12.py is byte-identical to the run-folder
  original, and the run-folder assay/live/E2 files are byte-identical
  to the claim/data copies (assay d1a3f267..., live f432423b..., E2
  fd6a8e31...).
- DEFECT (packaging, recorded, not numerical): the claim copy of
  build_borda12.py does NOT run verbatim from its packaged location.
  It resolves RUN via parents[3] of its own path, which from
  claim/code/ lands on runs/ instead of the run folder, so WS
  resolves one level too high and it dies with FileNotFoundError on
  the reference CSV. The byte-identical run-folder original (the
  location REPRODUCE.md directs) runs fine. The claim package
  therefore reproduces via its documented route, but its code copy is
  not self-locating; the path resolution should be fixed before any
  submission.
- Rebuild via the byte-identical run-folder original, run twice:
  both rebuilds byte-identical to the claimed score file (sha256
  fe21f86c..., cmp clean) and byte-identical to each other
  (deterministic). The rebuilt build log is byte-identical to the
  author's build_borda12.log, including fresh G1 fixtures (1.0 PASS /
  -1.0 FAIL) and G2 E2 0.3666.
- Build-code inspection (after my own checker ran): it reads ONLY the
  mutant + 12 member columns from the assay file (usecols); DMS_score
  is never read for method construction, only by the checker and the
  G3 diagnostic identity report, which never drives a drop decision.
  G3 dropped nothing (all 12 members kept, 0 NaN, no constant
  column). The frozen formula in the code matches PREREG.md.

## 3. Author's checker, read after my own checker

claim/code/checker.py (v2.0-dupe-reject) implements the same
convention I implemented independently: duplicate-mutant rejection,
exact mutant-set equality, inner join, scipy Spearman, PASS iff rho
> bar. One softness noted: it drops NaN pairs silently instead of
failing on NaN scores — moot here, since my checker verified the
score file contains zero NaNs.

## 4. Caveats (not reproduction failures)

- The margin over M1 is 0.0024, inside noise: the claim itself states
  the bootstrap CI on the BORDA-12-minus-M1 difference is
  [-0.0172, +0.0228], P(BORDA-12 > M1) = 0.592. The bank criterion
  compares point values and the point value reproduces exactly, so
  this is a matter for the criterion/novelty skeptics, not a
  reproduction failure. I flag it because a point-value record this
  thin deserves the panel's eyes on it.
- The claim-copy path-resolution defect in section 2 should be fixed
  before submission, even though the numbers reproduce.

## Verdict

Every property I was asked to verify reproduces: score file shape and
mutant set, rho 0.5682 (two independent implementations agreeing to
1e-16), direction convention, fixtures, bar 0.531 recomputed from the
live CSV in the package, G2 E2 0.3666, independent Borda recompute
matching the file to 3.3e-16 and rho to 8.2e-07, null test replicated
with a fresh seed, and a byte-identical deterministic rebuild. No
mismatch, no missing object, no non-determinism found. The one defect
is the claim copy's path resolution (section 2), which blocks running
that copy verbatim but does not affect any number.

pass: true
