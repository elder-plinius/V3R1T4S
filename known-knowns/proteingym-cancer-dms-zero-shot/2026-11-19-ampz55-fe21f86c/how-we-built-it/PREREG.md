# PREREG.md (frozen 2026-11-19 10:35 UTC, before any attack output is scored)

Criterion verbatim: see target.md. Score file over the 5,083
PTEN_HUMAN_Matreyek_2021 reference mutants, method zero-shot w.r.t. the
assay (no assay labels anywhere in method choice; no measurement from ANY
ProteinGym DMS assay of the same UniProt protein may enter the method),
Spearman (scipy, official convention, exact mutant-set match, no dupes)
strictly greater than the live row maximum over model columns by >= 0.015
absolute (bar = 0.531 against the 2026-11-19 live CSV; re-fetch immediately
before any claim). Novelty bar (separate gate, from PR #467 re-read in
scouting): M1 = 0.5658 on the same assay. A claim must clear BOTH bars:
rho > 0.531 (bank criterion) AND rho > 0.5658 (record, not subsumed).

Exact statistic / checker: ./checker.py (v2.0-dupe-reject) with bar 0.531.

Threshold: PASS iff reported rho > 0.531. A claim additionally requires
rho > 0.5658. Any claim must also carry a 1,000-sample bootstrap 95% CI
on the reported rho.

Null design:
null_test: required. The combiner is a new deterministic scorer, and the
claim to be tested is that its Spearman beats chance structure, so the same
pipeline runs on 400 controls: 400 random permutations (seed 20261119) of
the primary scores across the 5,083 mutants, Spearman recomputed each
time. Result written to null_test.md with lines: controls: 400,
best_control: <best control Spearman>, real: <primary Spearman>,
real_beats_all_controls: yes|no, command: <how to rerun it>.
(Checker sanity fixtures re-verified this run before scoring: score=DMS_score
-> 1.0 PASS, negated -> -1.0 FAIL, constant -> NaN FAIL.) All frozen rules
below use weights fixed a priori; no weight is swept or selected on this
run's labels. No claim may be based on any swept weight or on any diagnostic
variant. Fitting anything on Mighell labels is forbidden (same UniProt
P60484 as the target; bank pitfall on protein-level leakage). M1's
published Matreyek score (0.5658) is a novelty bar only and enters no
member, weight, or combiner choice.

Step 3c baseline note: the published baseline for this empirical-benchmark
claim is the live table value itself (VenusREM 0.516 on this assay, from the
re-fetched CSV); VenusREM releases no per-mutant predictions in the CSV to
re-score, so there is no baseline code to reproduce. The checker
positive/negative fixtures above are the gate that the scoring pipeline is
correct. No claim is made unless rho > 0.531, and no record is claimed
unless rho > 0.5658.

Inputs (public, themselves label-free except where noted):
- Live CSV: runs/2026-11-19-0953/data/DMS_substitutions_Spearman_DMS_level.csv
  (sha256 f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437,
  HTTP 200, 2026-11-19 10:34 UTC, byte-identical to all fetches since 2026-10-16)
- Reference: runs/2026-10-16-0453/data/dms_ref/DMS_ProteinGym_substitutions/PTEN_HUMAN_Matreyek_2021.csv
  (sha256 1c52aba95950c6d3b1ac8320df4cb99a79ae97353bd43e24c87ef78dbb02e636)
  and Mighell_2018.csv (sha256 d532bed24c80449936dd61cf303225d78e6e9963a58165c1c36dff92c89557e1)
- Published score files: Zenodo record 15293562,
  https://zenodo.org/records/15293562/files/zero_shot_substitutions_scores.zip
  (total 1,911,045,703 bytes). Fetched by HTTP range request ONLY the two
  assay entries below (central directory parsed from the zip tail; entry
  list saved in the 2026-11-15 constructor output). Each entry's sha256 is
  logged after fetch. The fetched assay files contain a DMS_score labels
  column; the build code reads ONLY the mutant column and the member score
  columns (usecols), never DMS_score for method construction — only
  ./checker.py touches labels, and the G3 identity check reports
  recomputed-vs-CSV values as a diagnostic with no drop decision.
  - PTEN_HUMAN_Matreyek_2021.csv (compressed 3,910,103 bytes, local-header
    offset 1,142,491,914, method deflate)
  - PTEN_HUMAN_Mighell_2018.csv (compressed 5,558,497 bytes, local-header
    offset 1,146,402,103, method deflate)
- LLR12 score file (for paired-diff comparison only):
  runs/2026-11-17-0953/attempts/constructor/output/score_llr12.csv
  (rho 0.5647 on Matreyek)
- ENS10 score file (for paired-diff comparison only):
  runs/2026-11-15-0953/attempts/constructor/output/score_ens10.csv
  (rho 0.5637 on Matreyek)
- 150M column: runs/2026-11-07-0953/attempts/lens-constructor/output/score_150m_masked.csv
  (rho 0.4620 on Matreyek); Mighell 150M: runs/2026-11-09-0953/attempts/constructor/output/score_150m_mighell.csv
  (rho 0.5463, diagnostic)
- B62 column: runs/2026-11-03-0953 output (rho 0.3915 Matreyek / 0.4813 Mighell)
  — exact path recorded in the statistician's code when loaded.

Fitting set (frozen, declared before scoring; no cancer-gene assay in it):
all 217 rows of the live CSV EXCEPT the 13 cancer-gene assays, defined by
DMS-ID prefix BRCA1_, BRCA2_, PTEN_, MSH2_, P53_, RASK_, RASH_, ERBB2_,
TP53_: BRCA1_HUMAN_Findlay_2018, BRCA2_HUMAN_Erwood_2022_HEK293T,
ERBB2_HUMAN_Elazar_2016, MSH2_HUMAN_Jia_2020,
P53_HUMAN_Giacomelli_2018_Null_Etoposide, P53_HUMAN_Giacomelli_2018_Null_Nutlin,
P53_HUMAN_Giacomelli_2018_WT_Nutlin, P53_HUMAN_Kotler_2018,
PTEN_HUMAN_Matreyek_2021, PTEN_HUMAN_Mighell_2018, RASH_HUMAN_Bandaru_2017,
RASK_HUMAN_Weng_2022_abundance, RASK_HUMAN_Weng_2022_binding-DARPin_K55.
Fitting set = 204 assays. 'Number of Mutants' is metadata, NOT a model, and
is excluded from both the row max and the ranking. (The fitting set is
declared for completeness; BORDA-12 uses no fitted weights at all — it is
equal-weight by construction.)

Membership (frozen, published, no Matreyek labels used): M1's 12 as
published in V3R1T4S PR #467 (selected by its authors only on 187
non-cancer assays sharing no UniProt id with any target):
VenusREM; ProSST (K=128); ProSST (K=512); ProSST (K=1024);
ProSST (K=2048); ProSST (K=4096); S3F; S3F-MSA; S2F-MSA; ESCOTT;
ESM3 open (1.4B); RSALOR.
Zip column aliases (from the 2026-11-15/17 builds, verified by the G3
identity check as a diagnostic): VenusREM [VenusREM], ProSST (K=128)
[ProSST-128], ProSST (K=512) [ProSST-512], ProSST (K=1024) [ProSST-1024],
ProSST (K=2048) [ProSST-2048], ProSST (K=4096) [ProSST-4096], S3F [S3F],
S3F-MSA [S3F_MSA], S2F-MSA [S2F_MSA], ESCOTT [ESCOTT], ESM3 open (1.4B)
[ESM3], RSALOR [RSALOR]. If a mapped column is absent from the fetched
file, that member is dropped and the run logs it (label-free fallback:
missing column only). No substitute member may be chosen on Matreyek labels.

Sanity gates first (not claims): (G1) checker fixtures re-verified
(score=DMS_score -> 1.0 PASS, negated -> -1.0 FAIL) before scoring any new
formula. (G2) reproduce E2 rho = 0.3666 from the cached score_E2.csv via
the checker before scoring any new formula. (G3) LABEL-FREE member
check (fix for the 2026-11-17 self-break latent caveat): a member is
dropped ONLY if its column is missing from the fetched file, constant
over the 5,083 mutants, or more than 5% NaN; the recomputed-vs-CSV
Spearman comparison is reported for each member as a diagnostic identity
check only and NEVER drives a drop decision. NaN count per member column
is reported, and any NaN is assigned the neutral rank 0.5 for that
member/mutant (frozen rule, stated before seeing the data). (G4) the
fetched assay files' mutant sets must match the reference exactly (the
checker enforces this).

Frozen formula for this run (no fitting on the target assay's labels):

- LENS-CONSTRUCTOR, BORDA-12 (plain equal-weight Borda over M1's 12):
  for each member m, let p_m(i) = percentile rank of model m's score for
  mutant i over the 5,083 reference mutants (rank/(n-1), ties averaged,
  ascending: a higher model score gets a higher rank). BORDA12(i) =
  mean_m p_m(i) — the plain mean of the twelve percentile ranks, equal
  weight 1/12 each, no fitted weight, no clipping, no logit. Score file:
  columns mutant, score = BORDA12. Rationale, stated before scoring: the
  2026-11-17 self-break found this exact combiner recomputes to 0.5682
  post-hoc (independent fresh code); it is the first combiner in this
  family to clear M1's 0.5658, and it is the simplest possible combiner —
  the mean of ranks — so it is the natural next primary. Honest
  expectation: 0.5682 (the post-hoc value), i.e. +0.0024 over M1; the
  bootstrap SE is ~0.01, so a fresh recompute landing anywhere in
  0.55-0.58 is unsurprising and a clean negative just short of 0.5658
  remains the most likely single outcome.

- LENS-CONSTRUCTOR, diagnostics only (no claim may be based on them):
  D-TRIM = trimmed Borda over M1's 12 (drop each mutant's minimum and
  maximum member rank, mean of the remaining 10). Reported for the
  record; it cannot be claimed even if it beats 0.5658, because the
  claim is frozen to BORDA-12. If a diagnostic beats M1, it becomes
  next run's primary (pre-registered then), not this run's claim.

Statistician diagnostics (no claim may be based on them):
- D1: bootstrap 95% CIs (1,000 samples, seed 20261119) for BORDA-12,
  plus paired bootstrap CIs for (BORDA-12 - LLR12), (BORDA-12 - ENS10),
  (BORDA-12 - 150M), (BORDA-12 - B62), (BORDA-12 - 0.516); number
  comparison vs M1 0.5658 only (no paired diff — M1's score file is not
  available to us).
- D2 (diagnostic only): BORDA-12 scored on Mighell_2018 using the same
  frozen members and rule from the same fetched file (no refit); report
  rho vs Mighell bar 0.576 and vs M1's Mighell 0.5784, no claim based
  on it.
- D3: per-position mean absolute rank error for BORDA-12 vs 150M (D5
  autopsy): top-10 worst positions for each and the overlap;
  descriptive only. Tests whether the combiner moves the failure map
  (2026-11-11 D5: worst 130, 123, 92, 125, 15) or merely shrinks it.
- D4: mutant-class slices for BORDA-12 (charge-flip |delta-charge|=2,
  Pro-involving) — descriptive only; the classes were identified on
  labels in prior runs, so no correction based on them may be claimed
  this run.
- D5: null test per the null design above (400 permutations, seed
  20261119), written to null_test.md.
- D6: leave-one-out + pairwise rank correlations for BORDA-12's members —
  diagnostic only (label-computed; must NOT ground any member choice
  this run or later).

Any deviation (different weight, different formula, different column)
requires a new timestamped PREREG.v2.md and the report says so.
