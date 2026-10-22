# CRITERION skeptic — proteingym-cancer-dms-zero-shot / PTEN_HUMAN_Matreyek_2021

Everything below was recomputed from the claim package only, with the project venv Python in my own
scratch folder. Paths are relative to the claim package.

## 1. Score file: one real-valued prediction for every mutant in the reference CSV

- `inputs/reference/PTEN_HUMAN_Matreyek_2021.csv` has 5,083 rows, 0 duplicate `mutant`, 0 NaN in `DMS_score`.
  5,083 matches both `Number of Mutants` in the live DMS-level table row and `DMS_total_number_mutants` in
  `inputs/DMS_substitutions.csv`, so the reference file is the full assay, not a subset.
- `result/PTEN_HUMAN_Matreyek_2021.M1.csv` has 5,083 rows, `mutant` set *and order* identical to the reference,
  0 duplicates, `prediction` float, 0 NaN, 0 tied values. Every mutant is scored. **Met.**
- sha256 of the result file equals the value logged in CLAIM.md (`1aecf9c1...7760db`). The reference file's sha256
  equals the value logged in REPRODUCE.md (`1c52aba9...02e636`). **Logged as required.**

## 2. Skeptic-recomputed Spearman, official convention

- `spearmanr(DMS_score, prediction)` joined on `mutant`, all 5,083 rows, no NaN to handle: **0.5657628916**
  (claim says 0.5658). Direction: positive, higher prediction = higher measured fitness, i.e. the ProteinGym
  convention with no sign flip.
- Convention cross-check: recomputing the *published* single-model columns from the packaged target score file
  with the same call reproduces the live table to three decimals (VenusREM 0.5158 vs table 0.516,
  ProSST-1024 0.5145 vs 0.514, ESCOTT 0.5049 vs 0.505). So my Spearman and the table's are the same statistic.
  This also authenticates the packaged score columns and the reference labels as the genuine ProteinGym ones
  (the forgery-free route would require re-downloading the 1.9 GB zip; the column-by-column agreement with the
  published table is strong indirect evidence and I accept it).

## 3. The bar: max over ALL model columns of the live table, including columns absent from the score zip

- The table copy has 103 columns; exactly 6 are metadata (`DMS ID`, `Number of Mutants`, `Selection Type`,
  `UniProt ID`, `MSA_Neff_L_category`, `Taxon`), leaving **97 model columns**, with 0 NaN on this row.
- Max over all 97 = **0.516** (VenusREM). I checked this includes the columns that are NOT in the packaged
  score zip (SiteRM, Protriever, AIDO Protein-RAG (16B), the xTrimoPGLM family, ESM-C, the Progen3 family);
  the best of those, AIDO Protein-RAG (16B) at 0.496, does not change the max. No hidden higher column.
- **I re-fetched the live CSV myself** from the URL in SCOUT_RECORD.md: HTTP 200, 141,235 bytes,
  sha256 `f432423b...466437` — byte-identical to the author's copy and to `inputs/DMS_substitutions_Spearman_DMS_level.csv`.
  Max recomputed from my own download: 0.516. So the "re-fetched immediately before claiming" condition holds
  and the table has not moved under us.
- Margin = 0.56576 - 0.516 = **+0.0498 >= 0.015. Met**, with 3.3x headroom.
- Information only (not required by the criterion): 1,000-mutant bootstrap of
  (rho_M1 - rho_VenusREM) gives mean 0.0501, 95% interval [0.0395, 0.0607]; 100% of resamples clear 0.015.
  Null model: a random permutation of the same predictions gives rho -0.0066, as expected.

## 4. Zero-shot with respect to the target assay

- `inputs/split.json` (sha256 `bf163ae6...a5a3163`, the value stamped in PREREG.md) excludes **both** PTEN assays:
  `target_assays` contains PTEN_HUMAN_Matreyek_2021 *and* PTEN_HUMAN_Mighell_2018. I verified directly against
  ProteinGym metadata that **no** one of the 187 fitting assays shares the target's UniProt id (PTEN_HUMAN).
  So no measurement from any ProteinGym DMS assay of the same protein enters the method. **Met.**
- `code/m1.py` read literally: `DMS_score` is read only from the 187 fitting assays (for the protein-balanced
  mean used to rank the 95 columns). From the target's score file it takes only `mutant` and the 12 selected
  columns; the z-scoring is per-column over the target's own mutants (mean/sd of the *predictions*, not labels).
  No threshold, weight or model-selection step touches the target's labels. Equal weights, so no fitted weights
  at all. **Met.**
- The 217-assay universe is fully partitioned: 187 fitting + 13 targets + 17 extra-excluded oncology assays,
  with nothing unaccounted for and nothing invented. Exclusion is by UniProt id as PREREG states.
- Allowed-input check: the only external inputs are other groups' published ProteinGym score columns, which the
  criterion explicitly permits ("may use ... other models' published score files"). Those models' own training
  is outside the claim's control and is disclosed in CLAIM.md. I accept this as within the letter of the criterion.

## 5. Fitting set and pre-registration

- The fitting set is declared (187 named non-cancer-gene assays, 16 further oncology proteins also excluded as a
  buffer) and is sha256-stamped inside PREREG.md; PREREG.md's own sha256 matches the value in CLAIM.md. **Met on form.**
- **Residual I cannot close:** the ordering "PREREG frozen 19:11:52Z, prediction written 19:13:23Z" is
  author-reported. Filesystem mtimes inside the package are all ~19:26 (the copy-in time) and carry no
  information about that order, and the exploration logs that chose K=12 live outside the package.
- What I *can* say against post-hoc tuning: the method has only two free knobs (K and equal weighting), neither
  can be fitted to labels it never reads, and a K-sweep I ran on the target shows the win is not knife-edge —
  margin >= 0.015 for every K from 4 to 40 (K=4 +0.026, K=10 +0.053, K=12 +0.050, K=20 +0.037, K=40 +0.016),
  failing only at K<=3 and K>=60. K=12 is not even the best choice for PTEN (K=10 beats it), which is positive
  evidence that K was not picked on this assay. Note the naive "all 95 columns" ensemble gives only 0.5255,
  i.e. below the 0.531 bar, so the fitting-set-based selection is doing real work and it is work done without
  target labels.

## 6. Method code reproduces the claimed object

- I ran `code/m1.py` unchanged. It re-selected exactly the 12 columns listed in EXTERNAL_SCORES.md, in the same
  order, and its output matches `result/...M1.csv` to max absolute difference 3.9e-10; the rebuilt file gives the
  identical Spearman 0.5657628916. **Deterministic and reproducible.**

## 7. External score files with provenance

- EXTERNAL_SCORES.md gives the zip URL, fetch date, byte size, zip sha256, the exact repackaging transform, the
  12 selected columns with their fitting-set scores, and a sha256 for every packaged file. I verified all **188
  listed sha256 values against the files on disk: 188/188 match, 0 missing, 0 unlisted files**. **Met.**
- Provenance is at zip level plus per-repackaged-file hashes; it is adequate and self-consistent, and section 2's
  reproduction of the published table values from these files corroborates it.

## 8. Is PTEN a cancer gene in the criterion's sense?

Yes, and not arguably. PTEN is a canonical tumour suppressor and one of the most frequently somatically mutated
genes in human cancer (Cancer Gene Census tumour-suppressor, Cowden syndrome / PTEN hamartoma tumour syndrome
germline gene). It also sits in the target list the bank itself names (BRCA1, BRCA2, PTEN, MSH2, P53, RASK, RASH,
ERBB2), so it is a cancer gene under both the ordinary meaning and the target's own enumeration. No stretch here.

## 9. Hidden quantifiers and how they limit scope

- **"A chosen cancer-gene DMS assay" vs 13 pre-registered assays.** PREREG scores all 13 with one frozen method
  and the criterion asks only for "a chosen" assay, so a single-assay win satisfies the literal text and the
  pre-registration is honest about the multiplicity. But the honest reading of the evidence is narrow: PREREG's own
  leave-protein-out base rate is 16% of held-out assays clearing +0.015, so ~2 wins among 13 targets is the
  *expected* outcome of this method under its null. One win therefore confirms the criterion on this assay and
  does **not** support a claim that M1 generally beats the ProteinGym per-assay best on cancer genes.
- The other 12 targets' predictions and scores are **not in this package** (only PTEN's result is), so I cannot
  evaluate p1 (>=3 assays) or p2 (MSH2) and I explicitly do not confirm them. The claim does not assert them.
- The win is on PTEN's **expression/abundance** assay (Selection Type "Expression"); it says nothing about the
  function assay PTEN_HUMAN_Mighell_2018, whose live best is already 0.561.
- SCOUT_RECORD.md in this package records only the table fetch; it contains no search of prior claims/PRs for this
  target. Non-subsumption is therefore not demonstrable from my evidence alone and I defer it to the novelty
  panelist. I found nothing in the package that is subsumed by an existing table column: no cross-model ensemble
  column exists in the live table, and the result is not a restatement of any single published number.

## Verdict

Every element of the verbatim full criterion that is checkable from the package checks out, and the two things I
could not close from inside the package (the freeze-before-scoring timestamp order; the zip-level provenance of
the raw score files) are both backed by strong indirect evidence and by the fact that the method reads no target
labels at any point. The margin is 3.3x the required threshold and robust to the only free hyperparameter. I
confirm the full criterion for this one assay, with scope held to exactly that.

confirmed_scope: On the single ProteinGym assay PTEN_HUMAN_Matreyek_2021, the frozen pre-registered equal-weight z-score ensemble of the 12 model columns that M1 selects using only 187 non-cancer-gene, non-PTEN fitting assays assigns a prediction to all 5,083 reference mutants with no target-assay label entering the method and reaches a skeptic-recomputed Spearman of 0.56576, which exceeds by 0.0498 the 0.516 maximum over all 97 model columns of the independently re-fetched live DMS-level table, satisfying the full success criterion on that one assay alone and implying nothing about the other 12 pre-registered cancer-gene assays or about the method's general performance.

context: subagent (Claude Code Agent, fresh context)
pass: true
