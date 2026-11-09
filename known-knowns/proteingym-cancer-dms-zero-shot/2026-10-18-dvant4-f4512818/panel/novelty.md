# Novelty check: proteingym-cancer-dms-zero-shot, partial win p1

context: subagent (Claude Code Agent, fresh context)

Scope: claim package only (CLAIM.md, SCOUT_RECORD.md) plus the external sources listed here. One plain request per page,
User-Agent "V3R1T4S-research-agent", no retries. Nothing was blocked; every fetch returned HTTP 200.

## 1. Status source

- URL: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- Fetched 2026-10-18T20:56:17Z, HTTP 200, 141,235 bytes, sha256
  f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437 (identical bytes to the author's 20:50:39Z copy).
- 103 columns: `DMS ID`, the five excluded metadata columns, and 97 numeric model columns.

Per-assay maximum over the 97 model columns, top three quoted:

| assay | live max (top 3 columns) | claimed | margin | bar 0.015 |
|---|---|---|---|---|
| PTEN_HUMAN_Matreyek_2021 | 0.516 VenusREM; 0.514 ProSST (K=1024); 0.505 ESCOTT | 0.5658 | +0.0498 | met |
| P53_HUMAN_Kotler_2018 | 0.722 ProSST (K=1024); 0.719 PoET (200M); 0.705 SaProt (650M) | 0.7686 | +0.0466 | met |
| BRCA1_HUMAN_Findlay_2018 | 0.560 S3F-MSA; 0.558 PoET (200M); 0.551 S2F-MSA | 0.5930 | +0.0330 | met |
| PTEN_HUMAN_Mighell_2018 | 0.561 S3F-MSA; 0.556 PoET (200M); 0.555 S2F-MSA | 0.5784 | +0.0174 | met, 0.0024 of slack |

All four maxima agree with CLAIM.md's table. Each claimed value is strictly above its maximum by >= 0.015; no ties. Four
assays clear the bar where p1 needs three. Whether the claimed Spearman values are themselves correct is the reproduction
skeptic's job, not mine; the Mighell margin has only 0.0024 of slack, so a small recomputation difference there would drop
that assay (three would remain).

## 2. Repo prior art

- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched
  2026-10-18T20:56:18Z, HTTP 200, 31,235 bytes. 100 lines. No match anywhere in the file for proteingym, cancer-dms, PTEN,
  P53/TP53, BRCA1, Matreyek, Kotler, Findlay or Mighell (case-insensitive); the word "protein" does not occur. Listed
  families are degree-diameter graphs, Lehmer's totient problem, matrix multiplication, VNN-COMP, RobustBench CIFAR-100,
  constant-weight codes and cipher commitments. No protein-fitness result is banked.
- Pull requests, all states: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100, pages 1-5
  fetched 2026-10-18T20:56:18Z-20:56:21Z, HTTP 200 on all five (2,175,212 / 1,734,828 / 1,989,359 / 1,797,225 / 1,021,134
  bytes). 453 PRs returned, numbers 1-463, so the full set is covered.
- Exactly one PR matches any of those keywords in title or body: **#463**, open, draft, author dvant4, created
  2026-10-18T20:45:08Z, not merged, titled "[claim] proteingym-cancer-dms-zero-shot: PTEN_HUMAN_Matreyek_2021 Spearman
  0.5658 vs table max 0.516 (+0.0498)". No other PR mentions ProteinGym or any of the four assays, and none claims p1, p2,
  p3 or the full criterion on this target.

Does #463 subsume p1? No. It claims one assay. Its body states: "satisfying the full success criterion on that one assay
alone and implying nothing about the other 12 pre-registered cancer-gene assays", and under "Not claimed": "Partial wins
p1-p3 are not claimed here." p1 requires >= 3 assays simultaneously under one frozen configuration. #463 does mention the
other three margins "for the record" (P53 +0.047, BRCA1 +0.033, Mighell +0.017) and says those numbers "were not panelled",
so the multi-assay result is disclosed but neither claimed nor verified anywhere in the repo. The p1 claim is therefore new
relative to the repo, though it overlaps #463 on one of its four assays and the two should not both be banked as separate
wins for the Matreyek assay.

## 3. Literature, last 24 months

Searched for any published zero-shot Spearman at or above the claimed values on these four assays. Nothing found at or above
them; per-assay numbers for these assays are essentially not published outside ProteinGym's own CSV, which is the status
source already checked.

- VenusRAR / Rank-and-Reason, Tan et al. 2026, https://arxiv.org/abs/2602.00197 (HTML v2 fetched 2026-10-18T20:57:23Z, HTTP
  200). Current claimed zero-shot SOTA: "a new SOTA on ProteinGym with a global Spearman correlation of 0.551, surpassing
  the previous best of 0.518". That is the benchmark-wide average, not per-assay; the paper's text contains no mention of
  PTEN, P53, TP53, BRCA1, Kotler, Findlay, Matreyek or Mighell, so it publishes no competing per-assay value. Its code repo
  tree API returned HTTP 404 (no public tree), so no per-assay file is available there.
- ProteinGym benchmark paper, Notin et al., NeurIPS 2023 Datasets and Benchmarks:
  https://proceedings.neurips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract.html - the source of
  the live table; its per-assay values are the ones re-fetched above.
- ProteinGymR Bioconductor package (version dated February 2026):
  https://bioconductor.statistik.tu-dortmund.de/packages/3.22/data/experiment/manuals/ProteinGymR/man/ProteinGymR.pdf -
  redistributes ProteinGym's own zero-shot scores for 79 models; not an independent higher value.
- ProteinGym topic overview, https://www.emergentmind.com/topics/proteingym - aggregate figures only (ESM-2 650M ~0.414,
  sequence+structure ~0.470, ensembles ~0.518).
- Multi-Scale Representation Learning for Protein Fitness Prediction (S3F/S2F line), https://arxiv.org/pdf/2412.01108 - the
  S3F-MSA family that holds two of the four live maxima; its published per-assay values are in the ProteinGym table.
- PoET, https://openprotein.ai/publications/poet-high-performing-protein-language-model-zero-shot/ - holds second place on
  three of the four assays in the table; no higher per-assay value published.
- Pugh et al., "From Likelihood to Fitness", NeurIPS 2025,
  https://mlanthology.org/neurips/2025/pugh2025neurips-likelihood - method gain reported benchmark-wide, no per-assay value.
- ProGen2, https://arxiv.org/pdf/2206.13517 - the only per-gene PTEN/P53 numbers surfaced (0.641 PTEN, 0.398 P53) are 2022
  indel assays, a different assay set, not these substitution DMS assays, and outside the 24-month window.
- Negative searches: queries on the three dataset identifiers verbatim, and on BRCA1 Findlay / TP53 Kotler / PTEN Mighell
  zero-shot Spearman, returned no paper reporting a value on these assays.

Caveat on what a literature search can show: the assay-level maxima move only when ProteinGym adds a model column, and the
ensemble ingredients here are themselves published columns, so the relevant comparison really is the live table. An unindexed
2026 preprint reporting a per-assay value above these is possible; I found none.

## 4. Verdict

Strictly beats the live per-assay best by >= 0.015 on four assays (p1 needs three), nothing in TROPHY_CASE.md covers
protein fitness, no PR among all 453 claims p1 or these assays beyond the author's own single-assay draft #463, which
explicitly does not claim p1 and cannot subsume it, and no published value in the last 24 months reaches the claimed numbers
on these four assays. On novelty grounds this passes. The one standing caution is overlap with #463 on
PTEN_HUMAN_Matreyek_2021: that assay should not be banked twice.

pass: true
