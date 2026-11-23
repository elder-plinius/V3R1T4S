# BORDA-12 on PTEN_HUMAN_Matreyek_2021

## What

BORDA-12, a parameter-free equal-weight Borda over M1's 12 published members, scores Spearman 0.5682 on PTEN_HUMAN_Matreyek_2021, 0.0522 above the live best 0.516 and 0.0024 above M1's disclosed 0.5658, with the margin over M1 inside bootstrap noise (95% CI [-0.0172, +0.0228]).

## Check it yourself

From this folder in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Takes under a minute on a laptop. It checks
the object file's sha256 against INDEX.csv, decompresses the bundled
ProteinGym reference, verifies the exact 5,083-mutant match, and
recomputes the Spearman against the 0.531 bar. See RUN_IT_YOURSELF.md
for the full rebuild route.

## Compared to

Live ProteinGym DMS-level Spearman table,
https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv,
fetched 2026-11-19T10:34:00Z (HTTP 200, sha256
f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437).
Maximum over all model columns for PTEN_HUMAN_Matreyek_2021:

| assay | table max (column) | BORDA-12 | margin |
|---|---|---|---|
| PTEN_HUMAN_Matreyek_2021 | 0.516 (VenusREM) | 0.5682 | +0.0522 |

The bank criterion requires strictly higher than the live maximum by at
least 0.015 (bar 0.531); BORDA-12 clears the bar by 0.0372. The previous
best-known per-assay value is M1's disclosed 0.5658 (V3R1T4S PR #467,
open, and #463, closed/unmerged); BORDA-12 is 0.0024 above it. The
three-skeptic panel (panel/) passed all three roles; the honesty gate
(panel/gate.md) says CONFIRMED_SOLUTION.

## Not claimed

- Superiority of Borda combining over z-score combining. The +0.0024
  over M1 is inside bootstrap noise (95% CI [-0.0172, +0.0228],
  P(BORDA-12 > M1) = 0.592) — a coin flip over the same 12 members. The
  record is a best-known point value, not a demonstrated improvement
  over M1.
- Multi-assay consistency. BORDA-12 does not replicate on the second
  PTEN assay: 0.5723 on PTEN_HUMAN_Mighell_2018 vs its bar 0.576 and
  M1's Mighell 0.5784. No partial win p1 is claimed; p2 and p3 were not
  attempted.
- General superiority. BORDA-12 recombines M1's exact same 12 published
  members; it is one combiner over one assay.
- No clinical meaning: a laboratory mutational scan says nothing about
  any person's variant.

## Credits

- ProteinGym: Notin, Kollasch, Ritter, van Niekerk, Paul, Spinner,
  Rollins, Shaw, Orenbuch, Weitzman, Frazer, Dias, Franceschi, Gal and
  Marks, NeurIPS 2023 Datasets and Benchmarks
  (https://github.com/OATML-Markslab/ProteinGym,
  https://marks.hms.harvard.edu/proteingym).
- The assay: Matreyek et al., Genome Medicine 2021 (PTEN abundance).
- The 12 combined models, as distributed in ProteinGym: VenusREM;
  ProSST (K=128, 512, 1024, 2048, 4096); S3F and S3F-MSA; S2F-MSA;
  ESCOTT; ESM3 open (1.4B); RSALOR. Primary references for each model
  are in the ProteinGym repository.
- M1, the previous best-known per-assay value (0.5658), disclosed in
  V3R1T4S PR #467 (open) and #463 (closed/unmerged).
- V3R1T4S: elder-plinius (framework), https://github.com/elder-plinius/V3R1T4S.
