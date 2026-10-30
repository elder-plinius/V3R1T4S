# CRITERION skeptic — partial win p1

Judged literally against p1's verbatim text plus the clauses it inherits from the success criterion.
All numbers below were recomputed inside the panel work directory from the claim package only
(`inputs/`, `result/`, `code/m1.py`), with the project venv Python.

p1 verbatim: "Beat the live per-assay best by >= 0.015 Spearman on at least three cancer-gene assays
simultaneously with ONE method and ONE frozen configuration (pre-registered, fitted only on non-cancer
assays)."

## 1. Scoring convention and the recomputed margins

Convention check first: for each of the four claimed assays I recomputed the Spearman of several
published single-model columns from the packaged score files against `DMS_score` in the official
reference file, joined on `mutant`. They reproduce the live DMS-level table to within 0.0005, i.e.
to the table's 3-decimal rounding (e.g. VenusREM on PTEN_Matreyek 0.5158 vs 0.516; ProSST (K=1024) on
P53_Kotler 0.7221 vs 0.722). So my recompute is on the same convention the bar is quoted in.
`DMS_score` in the score zip equals `DMS_score` in the reference file (max abs diff 5e-10, a
10-significant-digit rounding artifact of the packaging, not a relabelling).

Bar = max over all 97 non-metadata columns of the live table row (metadata excluded: Number of
Mutants, Selection Type, UniProt ID, MSA_Neff_L_category, Taxon). This is wider than the score zip:
the zip has 95 model columns, and the live table carries two columns with no zip counterpart,
`AIDO Protein-RAG (16B)` and `Protriever`. Both are non-NaN on all 13 targets and are included in my
maxima; neither is the argmax on the four winners (AIDO 0.496/0.680/0.491/0.518; Protriever
0.432/0.644/0.524/0.504). All 97 columns are populated for all 13 assays, so no column was silently
dropped. Recomputed, over all 13 pre-registered assays:

| assay | rho_M1 | live max (argmax) | margin | >= 0.015 |
|---|---|---|---|---|
| PTEN_HUMAN_Matreyek_2021 | 0.5658 | 0.516 (VenusREM) | +0.0498 | yes |
| P53_HUMAN_Kotler_2018 | 0.7686 | 0.722 (ProSST K=1024) | +0.0466 | yes |
| BRCA1_HUMAN_Findlay_2018 | 0.5930 | 0.560 (S3F-MSA) | +0.0330 | yes |
| PTEN_HUMAN_Mighell_2018 | 0.5784 | 0.561 (S3F-MSA) | +0.0174 | yes |
| P53_HUMAN_Giacomelli_2018_Null_Etoposide | 0.5234 | 0.509 | +0.0144 | no |
| MSH2_HUMAN_Jia_2020 | 0.4207 | 0.409 | +0.0117 | no |
| RASK_HUMAN_Weng_2022_binding-DARPin_K55 | 0.7171 | 0.710 | +0.0071 | no |
| P53_HUMAN_Giacomelli_2018_Null_Nutlin | 0.5014 | 0.523 | -0.0216 | no |
| RASH_HUMAN_Bandaru_2017 | 0.5851 | 0.619 | -0.0339 | no |
| P53_HUMAN_Giacomelli_2018_WT_Nutlin | 0.5532 | 0.616 | -0.0628 | no |
| RASK_HUMAN_Weng_2022_abundance | 0.3823 | 0.470 | -0.0877 | no |
| BRCA2_HUMAN_Erwood_2022_HEK293T | 0.4335 | 0.534 | -0.1005 | no |
| ERBB2_HUMAN_Elazar_2016 | 0.5402 | 0.695 | -0.1548 | no |

The four claimed margins reproduce exactly as stated; count clearing 0.015 is 4. Three of the four
margins have >= 0.016 of slack over the threshold; PTEN_Mighell's +0.0174 has only 0.0024 of slack, so
it is the one win a table refresh could plausibly erase. Even so, dropping it leaves 3, which still
satisfies "at least three". "Strictly higher ... by at least 0.015" is satisfied by all four
(margin >= 0.015 implies strictly higher).

Completeness: for all 13 assays the prediction file has one real-valued prediction for every mutant of
the reference file (row counts equal, 0 unmatched on a left join from the reference, no NaN in
`DMS_score`, no NaN in any of the 12 contributing score columns), and the row counts equal the table's
`Number of Mutants` exactly.

## 2. ONE method, ONE frozen configuration

Confirmed by reconstruction, not by assertion. Taking the 12 model columns named in EXTERNAL_SCORES,
z-scoring each over the assay's own mutants and averaging with equal weights reproduces every one of
the 13 shipped prediction files to <= 5.2e-10 (float-printing precision), with mutant order identical.
Same 12 columns, same K, same equal weights, same z-scoring, all 13 assays, including the nine losses.
There is no per-assay switch, no per-assay weight, and nothing label-dependent in the target-side step
(z-scoring uses only the model columns).

## 3. Fitted only on non-cancer assays; pre-registration

- Selection step reproduced independently: I recomputed, over the 187 fitting assays alone, each of the
  95 zip columns' Spearman against `DMS_score`, took the protein-balanced mean (weight 1/number of
  fitting assays of that protein), and ranked. The top 12 are exactly the 12 claimed, with means
  matching EXTERNAL_SCORES to 5 decimals (VenusREM 0.54197 ... S3F 0.48957; rank 13 is PoET 0.48930).
  So "which models" was determined entirely by non-cancer data plus the stamped split, with no
  residual freedom.
- Leakage: the split accounts for all 217 table assays as 13 targets + 187 fitting + 17 extra-excluded.
  The fitting set shares no UniProt id with any target (empty intersection over the 8 target UniProt
  ids), so no measurement from any assay of a target protein enters the method. The exclusion is
  conservative beyond what the rules demand: 16 further oncology-related proteins are also held out of
  the fitting set.
- Stamp: sha256 of PREREG.md is 365981fd71fee2d6d4e236fbdfaa476f05b76d8129de5f0e0722581a061420ad,
  matching the stamp quoted in CLAIM.md; sha256 of the split file matches the value named inside
  PREREG.md (bf163ae6...); sha256 of the packaged table copy matches SCOUT_RECORD.md (f432423b...).
  So the pre-registration is stamped and self-consistent, and the configuration it describes is the one
  that produced the files.
- Written-before-scoring is an attestation I cannot independently verify from inside the package: the
  timestamps (PREREG frozen 19:11:52Z, predictions written 19:13:23Z) rest on the author's clock, and
  every packaged file carries the same copy mtime. What limits the exposure is that the only choices
  left after the stamped split are K and "equal weights" (see 4); the model identities are forced by
  the fitting data.
- Residual free knob K: the win count is 3, 4 or 5 for every K from 5 to 16 (K=4: 1; K=5: 3; K=6: 4;
  K=8: 5; K=10: 3; K=12: 4; K=14-16: 5), so K=12 is not a spike and the ">= 3" outcome is not an
  artifact of tuning K to the targets.

## 4. "At least three cancer-gene assays simultaneously"

p1 quantifies over assays, not proteins, and four pre-registered cancer-gene assays clear the bar, so
the literal reading is met with one to spare. The stricter reading matters because two of the four are
PTEN assays, so I checked it: the four winners span three distinct proteins (PTEN x2, TP53, BRCA1), so
even under a "three distinct cancer genes" reading the count is exactly 3 and p1 still holds — though
with zero slack on that reading. PTEN, TP53 and BRCA1 are canonical cancer genes (tumour suppressors in
the standard cancer-gene censuses), so no stretch is needed to call these cancer-gene assays; the two
PTEN assays are genuinely different experiments (Matreyek 2021 abundance-style, 5,083 mutants;
Mighell 2018, 7,260 mutants), not two scorings of one assay. "Simultaneously" is satisfied in the
strong sense: one configuration, one run, all 13 assays written together.

## 5. Multiplicity and null models

13 assays were pre-registered, all 13 were scored, and all 13 result files are shipped, so there is no
post hoc selection of which assays to report: the denominator is fixed and visible. The hidden
quantifier risk here is not in the claim but in how the result could be read.

Against the author's own declared per-assay rate of 16% (measured for this configuration on held-out
fitting assays), a binomial reference gives P(>= 3 of 13) = 0.35, P(>= 4 of 13) = 0.14; counting
distinct proteins, P(>= 3 of 8) = 0.12. Two readings:

- Read as a *chance* model, 4/13 would be unremarkable, and p1's "at least three" would be a bar a
  16%-per-assay method clears about a third of the time. On that reading p1 is a weak threshold — but
  that is a property of the bank's p1 definition, not a defect in this claim, and p1's text contains
  no significance requirement; PREREG declares no null test is needed, which is consistent with the
  criterion being a deterministic margin against a published table value.
- Read correctly, 16% is not a chance rate at all: it is this method's own pre-measured skill rate
  against the same hard bar (the max over 97 published columns), established on non-cancer assays
  before any target was scored. A no-skill predictor does not beat that max by 0.015 at a 16% rate.
  The observed 4/13 (31%) is simply consistent with, and not better than, what was pre-registered.

Either way the consequence for scope is the same, and it is the main thing a reader could overstate:
this is not "M1 beats the ProteinGym per-assay best on cancer-gene assays". M1 loses on 9 of the 13,
several badly (ERBB2 -0.155, BRCA2 -0.101, RASK abundance -0.088). The confirmed scope must be the four
named assays and must carry the 9 losses with it.

## 6. Subsumption

The disclosed related work is a draft single-assay claim on PTEN_HUMAN_Matreyek_2021 (same method, same
prediction file) that explicitly does not claim p1. A single-assay main-criterion claim cannot subsume
a four-assay one-configuration result: p1's content is exactly the part that claim does not assert, and
the three further wins (P53_Kotler, BRCA1_Findlay, PTEN_Mighell) are not contained in it. The
implication runs the other way — p1 covers that claim's assay — so the panel should expect the two to be
reconciled rather than both credited as separate wins on PTEN_Matreyek.

Limit on my non-subsumption finding: SCOUT_RECORD.md records only the table fetch. The package contains
no record of a search of other open claim PRs for a prior p1 or multi-assay claim on this target, so I
can rule out subsumption only by what the package discloses, not globally. That check belongs to
another panel seat; it does not change the literal verdict, but it is why the scope sentence is
qualified as to disclosure.

## 7. Verdict

Every clause of p1 and every inherited clause I can check from the package holds, on the literal
reading and on the stricter distinct-protein reading, with the margins and the model selection
reproduced independently rather than taken on trust. The two honest reservations are (a) the
write-before-scoring ordering is an attestation, mitigated by the selection being forced by the stamped
split and by K-robustness, and (b) 4/13 is no better than the pre-registered 16% per-assay rate, so the
win must not be read as general superiority on cancer-gene assays. Neither is a failure of p1 as
written.

confirmed_scope: With one pre-registered, frozen, zero-shot configuration (equal-weight mean of the z-scored top-12 of 95 published ProteinGym v1.3 model columns, selected only on 187 non-cancer assays sharing no UniProt id with any target), M1 exceeds the maximum over all 97 model columns of the 2026-10-18 live ProteinGym DMS-level Spearman table by at least 0.015 on four of the 13 pre-registered cancer-gene assays — PTEN_HUMAN_Matreyek_2021 (+0.0498), P53_HUMAN_Kotler_2018 (+0.0466), BRCA1_HUMAN_Findlay_2018 (+0.0330) and PTEN_HUMAN_Mighell_2018 (+0.0174), three distinct cancer genes — while losing on the other nine, a 4/13 rate consistent with the pre-registered 16% per-assay base rate and therefore no evidence of general superiority on cancer-gene assays.

context: subagent (Claude Code Agent, fresh context)

pass: true
