# Published Spearman values for the FLIP GB1 splits (the related-work survey)

This survey was run in a separate context during this run, from 2026-11-20T00:00Z, with one honest request per
object, `gh api` for GitHub reads, and no retry after any 401/403/429/503. It was launched **before** any model was
fitted, and `PREREG.md` section 9 records that no claim would be written before it was in hand. Every number below
was read from the URL given during that survey; cells that could not be read are marked unread, not guessed.

**This file exists because the bank's full-win criterion requires the claimed value to be "higher than any
published value for the same split and test set found by the NOVELTY check, from any year from the 2021 FLIP
paper's own baselines onward, including later FLIP releases such as the 2026 FLIPv2 baselines and 2024-2026
papers."** It is also the honest answer to the question that cost an earlier run its claim: a pre-registration must
not assert that no competing published number exists until the survey has been done.

## The answer, in two sentences

- **one_vs_rest:** no published Spearman above 0.4571 was found. The highest comparable published values are
  PLMFit's own 0.4571, then 0.4501 (an active-learning budget point, not a like-for-like full-train result),
  0.40 (Kermut's baseline GP), 0.32 (FLIP's own 2021 best).
- **three_vs_rest: published values above 0.8791 exist**, the highest being **0.8995 +- 0.0058 (ProtEGNN(t6),
  bioRxiv 2026.05.28.728196, 2026)** and **0.893 +- 0.0048 (ESM2-3B + LoRA, Schmirler et al., Nature
  Communications 15:7407, 2024; best single seed 0.8980)**, with 0.888 (Ankh-large LoRA) and 0.880 +- 0.003
  (Bradley-Terry CNN, Brookes et al., NeurIPS 2024) also above the scoreboard value. **0.8791 is therefore not the
  published state of the art for three_vs_rest, only the PLMFit scoreboard entry.**

## FLIP's own 2021 baselines (the paper's Table 4, "GB1 baselines (metric: Spearman correlation)")

Read from the NeurIPS Datasets & Benchmarks proceedings PDF
`https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2b44928ae11fb9384c4cf38708677c48-Paper-round2.pdf`.

| model | one_vs_rest | two_vs_rest | three_vs_rest | low_vs_high |
|---|---|---|---|---|
| ESM-1b (per AA) | 0.28 | 0.55 | 0.79 | **0.59** |
| ESM-1b (mean) | 0.32 | 0.36 | 0.54 | 0.13 |
| ESM-1b (mut mean) | -0.08 | 0.19 | 0.49 | 0.45 |
| ESM-1v (per AA) | 0.28 | 0.28 | 0.82 | 0.51 |
| ESM-1v (mean) | 0.32 | 0.32 | 0.77 | 0.10 |
| ESM-1v (mut mean) | 0.19 | 0.19 | 0.80 | 0.49 |
| ESM-untrained (per AA) | 0.06 | 0.06 | 0.48 | 0.23 |
| ESM-untrained (mean) | 0.05 | 0.05 | 0.46 | 0.10 |
| ESM-untrained (mut mean) | 0.21 | 0.21 | 0.57 | 0.13 |
| Ridge (one-hot) | 0.28 | **0.59** | 0.76 | 0.34 |
| CNN | 0.17 | 0.32 | **0.83** | 0.51 |
| Levenshtein | 0.17 | 0.16 | -0.04 | -0.10 |
| BLOSUM62 | 0.15 | 0.14 | 0.01 | -0.13 |

FLIP 2021 maxima: one_vs_rest 0.32, two_vs_rest 0.59, three_vs_rest 0.83, low_vs_high 0.59. The survey noted an
oddity in the published table itself (several rows repeat their one_vs_rest value in the two_vs_rest column); the
same duplication appears in Kermut's reproduction of the table, so it is in the source and not a transcription
error here.

**FLIP's own one-hot ridge baseline on three_vs_rest is 0.76**, and that is the single most relevant comparison for
this run's model, which is a regularised one-hot interaction expansion.

## Later published values, comparable (same FLIP split names)

| split | Spearman | model | source | year |
|---|---|---|---|---|
| three_vs_rest | **0.8995 +- 0.0058** (their Table 4 rounds it to 0.90) | ProtEGNN(t6), ~400-500K trainable parameters on a frozen ESM2-T6 | bioRxiv 2026.05.28.728196, Tables 1 and 4 | 2026 |
| three_vs_rest | 0.8954 | ESMc-M ProtEGNN | same, Table 1 | 2026 |
| three_vs_rest | **0.893 +- 0.0048**, best single seed **0.8980** | ESM2-3B + LoRA fine-tuning | Schmirler, Heinzinger, Rost, Nature Communications 15:7407 (2024); numbers read from the authors' own source-data CSVs in `RSchmirler/data-repo_plm-finetune-eval` | 2024 |
| three_vs_rest | 0.888 +- 0.0095 | Ankh-large + LoRA | same CSVs | 2024 |
| three_vs_rest | 0.883, 0.879 | ESM2-8M full fine-tune; ProtT5 LoRA / ESM2 35M-650M | same CSVs | 2024 |
| three_vs_rest | **0.880 +- 0.003** | CNN with a Bradley-Terry contrastive loss | Brookes, Park, Kim, Listgarten et al., NeurIPS 2024 (arXiv 2305.03136), Table 1 | 2024 |
| three_vs_rest | 0.87 +- 0.004 | CARP-640M pretrained + full fine-tune | Yang et al., Cell Systems 2024 (bioRxiv 2022.05.19.492714v5), Table S6 | 2022/2024 |
| three_vs_rest | 0.871 / 0.850 | ESM embeddings + Bayesian ridge / one-hot + GP | Greenman, Amini, Yang et al., bioRxiv 2023.04.17.536962, Tables S4 and S15 | 2023 |
| three_vs_rest | 0.850 | ESM2 48-layer embeddings | Mollon et al., arXiv 2501.18223, Table 6 | 2025 |
| three_vs_rest | 0.814 | Ankh3-large frozen-embedding ridge probe | arXiv 2611.12000, Tables 6-7 | 2026 |
| three_vs_rest | 0.77 / 0.73 | Kermut composite-kernel GP / baseline GP | Groth, Kermut, NeurIPS 2024, Table H.1 | 2024 |
| one_vs_rest | 0.4501 (budget B=24); 0.3839 at B=28 | TALK active batch design | arXiv 2611.11141, Tables H.4-H.6 | 2026 |
| one_vs_rest | **0.40** / 0.37 / -0.14 | baseline GP / Kermut constant mean / Kermut | Kermut, NeurIPS 2024, Table H.1 | 2024 |
| one_vs_rest | 0.315 / 0.249 | ESM + GP / one-hot + Bayesian ridge | Greenman et al. 2023, Tables S15 and S4 | 2023 |
| one_vs_rest | 0.29 / 0.19 | ESM-1b frozen / CARP-640M pt-ft | CARP Table S6 | 2022/2024 |
| one_vs_rest | 0.133 / 0.091 | CNN with MSE / Bradley-Terry loss | Brookes et al. 2024, Table 1 | 2024 |
| two_vs_rest | **0.73 +- 0.03** | CARP-640M pt-ft | CARP Table S6 | 2022/2024 |
| two_vs_rest | 0.694 / 0.660 / 0.635 / 0.607 / 0.59 | one-hot+GP / HyPLM E1-600M / ESM2-48L / BT-CNN / FLIP ridge | as cited above | 2021-2026 |
| low_vs_high | **0.59** | FLIP's own ESM-1b (per AA) | FLIP 2021 Table 4 | 2021 |
| low_vs_high | 0.567 / 0.545 / 0.53 / 0.474 / 0.43 / 0.42 | BT-CNN / ESM2-48L / ESM-1b frozen / HyPLM / CARP pt-ft / Kermut baseline GP | as cited above | 2021-2026 |

So **published numbers exist for two_vs_rest and low_vs_high despite there being no PLMFit scoreboard entry for
them.** "No scoreboard entry" is not "no published number", and p3 of this bank entry could not have been claimed
as a novelty on that basis. (p3 is out of scope this run in any case.)

## FLIPv2 / FLIP2 (2026): no GB1 baseline numbers exist

The survey read the FLIP repository README (`gh api repos/J-SNACKKB/FLIP/readme`, pushed 2026-11-11), the full
recursive tree (107 blobs), the releases endpoint, the FLIP2 paper full text (bioRxiv 2026.02.23.707496v2) and
`flip.protein.properties`. FLIP2 adds seven new datasets (Amylase, IRED, NucB, TrpB, Hydro, Rhomax, PDZ3) and
sixteen splits; **GB1 appears only under "Legacy FLIP" and no GB1 rows appear in any FLIP2 table.** The releases
endpoint returned no releases, so there are no release assets, and `baselines/` and `analysis/` contain only code -
no results CSV or JSON anywhere in the tree. The GB1 split files are unchanged, and `splits/gb1/README.md` marks
one_vs_rest, two_vs_rest, three_vs_rest and low_vs_high green and `sampled` orange ("Not for performance
comparisons"), consistent with the bank entry.

## Numbers that are NOT comparable bars

- **The FLIP GB1 `sampled` split** (a random 80/20 partition, orange in FLIP's own README): FLIP 2021 reports
  ESM-1b 0.92, ESM-1v 0.92, CNN 0.91, ridge 0.82; Brookes 0.951; Mollon 0.940. None of these is a bar for any
  mutation-order split.
- **Ankh and Ankh3 "GB1" numbers are on the `sampled` split, not three_vs_rest.** Ankh's Table 12 shows a
  6,291/670/1,772 random partition (1,772 = the `sampled` test size); Ankh3's Table 5 reports up to 0.9044 on a
  split described only as "sourced using the FLIP benchmark". The survey flags that ProtEGNN's Table 4 nonetheless
  places "Ankh3 5.7B 0.90" beside its own three_vs_rest 0.90 and claims parity, which is a cross-split comparison
  and looks wrong. This run makes no comparison against any Ankh number.
- ProteinGym's `SPG1_STRSG_Wu_2016` and any random re-split of the 149,361-variant Wu 2016 landscape. The survey
  read no ProteinGym number and reports none.
- `ProtLingo` (GB1 reported only as a mean over all five GB1 splits) and `PETA` (its own partitions).
- A public repository `saanviiyer/leeway` reports a one-hot ridge **floor** of 0.7528 on three_vs_rest from the
  biotrainer FASTA (2,691 train / 299 validation / 5,743 test), with its own caveat that the published GB1 values
  it lists were transcribed from the ProtEGNN preprint and not checked against sources. It is not a published bar.

## Two different three_vs_rest test sets are in circulation - stated plainly

- The PLMFit paper's Table 1 and Mollon's Table 1 give **2,968 train / 5,765 test**.
- The released files - FLIP's biotrainer FASTA and plmfit's `gb1_data_full.csv`, the file this run used - give
  **2,691 train / 299 validation / 5,743 test**. Schmirler's Table 2 also gives 5,743.

So the PLMFit scoreboard's 0.8791 may have been computed on 5,765 rows, while this run's number is on the 5,743
test rows of the file it names, and ProtEGNN's and Schmirler's numbers appear to be on the same 5,743 rows. The
bank's instruction is to name the file and report its counts rather than reconcile the discrepancy, and that is
what is done. Anyone comparing these numbers should know the test sets differ by 22 rows.

## Sources the survey could not read (recorded, not retried)

- `https://www.biorxiv.org/content/10.1101/2023.11.16.565910v3.full.pdf` (the muFormer paper): **HTTP 429**, not
  retried. Its GB1 per-split numbers appear to live only in a bar chart.
- `https://www.nature.com/articles/s41467-024-51844-2` (Schmirler, Nature Communications): **HTTP 303** redirect to
  an authorisation endpoint, not followed. The bioRxiv v2 preprint and the authors' own published source-data CSVs
  were used instead.
- bioRxiv HTML full texts render tables as placeholders, so PDFs were used; the FLIP 2021 bioRxiv PDF came back as
  an unreadable compressed stream and the NeurIPS proceedings PDF was used instead.
- The FLIP2 and ProtEGNN HTML full texts were truncated at 100,000 characters (the last ~4 KB of each unread).
- CARP's Table S7 extracted with interleaved rows, so nothing is quoted from it; Table S6 extracted cleanly.

## Anything addressed to an AI agent

None on any page opened. The survey asked for it explicitly on each fetch and every answer was negative. One search
result URL looked like an agent skill file and was deliberately not opened. Two incidental repository notes, aimed
at human users rather than agents, were recorded: FLIP's quick-start comment "Validation rows may also have
set=\"train\". Exclude them before fitting." and "Preserve the released assignments when comparing models." This
run preserves the released assignments exactly, and reports both the all-non-test fit and the `train`-label-only
fit precisely because of the first note.

## Credits

Dallago, Mou, Johnston, Wittmann, Bhattacharya, Goldman, Madani and Yang (FLIP, NeurIPS 2021 Datasets &
Benchmarks); Wu, Dai, Olson, Lloyd-Smith and Sun (eLife 2016;5:e16965, the GB1 landscape); Bikias, Stamkopoulos and
Reddy (PLMFit, Briefings in Bioinformatics 26(4):bbaf381, 2025); Schmirler, Heinzinger and Rost (Nature
Communications 15:7407, 2024); Brookes, Park, Kim and Listgarten (NeurIPS 2024); Yang and colleagues (CARP, Cell
Systems 2024); Greenman, Amini and Yang (bioRxiv 2023); Groth and colleagues (Kermut, NeurIPS 2024); Mollon and
colleagues (arXiv 2501.18223); the ProtEGNN authors (bioRxiv 2026.05.28.728196); Henikoff and Henikoff (BLOSUM62,
PNAS 1992); Kyte and Doolittle (J Mol Biol 1982); Zamyatnin (Annu Rev Biophys 1972).
