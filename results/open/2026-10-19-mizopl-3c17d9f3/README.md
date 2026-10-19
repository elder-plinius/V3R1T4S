# IMMREP22 TCR-Epitope Specificity (`immrep22-tcr-epitope-microauc`: Task 1 Micro-AUC, `p1` `SPRWYFYYL`, `p2` Task 2 Rank, and `p3` Provenance Audit)

## What

Multi-Chain (alpha/beta/alphabeta) OOB + Analytical LOO + CSLS Hubness-Corrected CLSS Ensemble trained strictly on claim/training_data/ achieves 17-epitope _Average MicroAUC = 0.882173 in claim/clss_tcr_stats.txt (856 bytes, sha256 3c17d9f39dc9b72c93441d4cc5d4b9fae9d986fe09f8abf3b27fe971d0212090) via the official claim/evaluation/evaluate.py vs the best published tcrexab = 0.847347 (+0.034826 >= +0.0200, winning 15/17 epitopes with 1-sided Wilcoxon p = 6.7139e-04 and 9/17 epitopes over all 22 published methods), single-epitope SPRWYFYYL MicroAUC = 0.877874 vs published column max 0.837823 (+0.040050 >= +0.0300, p1), companion Task 2 _Average Rank = 2.859120 vs published best 3.284289 (-0.425169 <= -0.2500, p2), 17-epitope negative-sampling provenance audit across clss_tcr, tcrexab, tcrexb, and tcrexa (p3), zero control-repertoire overlap, and Levenshtein d_Lev >= 2 MicroAUC = 0.868783 (+0.037753 over d_Lev >= 2 tcrexab 0.831030 and +0.021436 over full-set 0.847347), after reproducing tcrexab (0.846619), tcrexb (0.831443), and tcrexa (0.785032) within <= 0.0024.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are in `object/` (`object/clss_tcr_stats.txt`, `object/clss_tcr_scores/SPRWYFYYL.txt`, `object/clss_tcr_scores/testSet_Global.txt`, `object/clss_tcr_scores/*.txt`, `object/immrep22_audit_manifest.json`), `the-record-we-beat/evaluate.py`, and `how-we-built-it/run_clss_immrep22.py`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`, `pandas`, `scikit-learn`, `scipy`.
- **Rough laptop time**: about 3 to 6 seconds (~22 seconds if running end-to-end training from scratch via `how-we-built-it/run_clss_immrep22.py`).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Task / Metric | Published Best | Ours (`clss_tcr` & Margin) | URL | UTC fetch time |
|---|---|---:|---|---|---|
| `MortimerLab/immrep22` (`microaucs.csv`, 22 methods) | Task 1 `_Average` MicroAUC (17 epitopes) | `0.847347` (`tcrexab`) | **`0.882173`** (**`+0.034826`**, `15/17` wins vs `tcrexab`, Wilcoxon $p = 6.7139 \times 10^{-4}$, `100.00%` paired bootstrap, `9/17` all-22-method column maxima) | https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/microaucs.csv | 2026-10-19T18:10:02Z |
| `MortimerLab/immrep22` (`microaucs.csv`, column max `p1`) | Single-epitope `SPRWYFYYL` MicroAUC ($n_{\text{test}}=140$) | `0.837823` (`tcrexb`) | **`0.877874`** (**`+0.040050`** vs all-22-method max, **`+0.066631`** vs `tcrexab = 0.811243`, `p1`) | https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/microaucs.csv | 2026-10-19T18:10:02Z |
| `MortimerLab/immrep22` (`epitoperank.csv`, Task 2 `p2`) | Task 2 `_Average` Rank (`testSet_Global.txt`, lower is better) | `3.284289` (`tcrexab`) | **`2.859120`** (**`-0.425169 <= -0.2500`**, `p2`) | https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/epitoperank.csv | 2026-10-19T18:10:02Z |
| `MortimerLab/immrep22` (`p3` Levenshtein $d_{\text{Lev}} \ge 2$ & Provenance) | Mean MicroAUC excluding test TCRs with $d_{\text{Lev}}(\alpha) + d_{\text{Lev}}(\beta) \le 1$ | `0.831030` (`tcrexab` $d_{\text{Lev}} \ge 2$) | **`0.868783`** (**`+0.037753`** over $d_{\text{Lev}} \ge 2$ `tcrexab`, **`+0.021436`** over full-set `0.847347`; `0.901893` swapped-neg / `0.854062` control-neg, `p3`) | https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/microaucs.csv | 2026-10-19T18:10:02Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Zero external TCR databases (`VDJdb`, `McPAS-TCR`, `IEDB`, `10x`, `MIRA`, `OLGA`, `SONIA`) and zero pre-trained protein language models (`ESM2`, `ProtBERT`, `TCR-BERT`) were used; all models are fit from scratch strictly on each epitope's official `training_data/{epitope}.txt` split.
- On 2 of the 17 epitopes (`HPVTKYIM` and `NQKLIANQF`, both small sample sizes), `tcrexab` scores higher or ties within `0.0085`; across all 17 epitopes `clss_tcr` beats `tcrexab` on `15 / 17` epitopes (`p = 6.7139e-04`) and beats the column maximum of all 22 published methods on `9 / 17` epitopes.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Pieter Meysman,azawa et al. / IMMREP22 Consortium** (*Benchmarking solutions to the T-cell receptor epitope prediction problem: IMMREP22 workshop report*, *ImmunoInformatics* 10, 100024, 2023, https://github.com/MortimerLab/immrep22), creators of the IMMREP22 paired-chain TCR-epitope specificity benchmark and evaluation suite.
- Contributor credit: `mizopl`.
