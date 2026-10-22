# RNAGym ncRNA fitness: beat the top signed-Spearman macro score on the live zero-shot leaderboard

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

RNAGym (Rohit Arora, Murphy Angelo, Christian Choe, Courtney Shearer, Aaron Kollasch, Fiona Qu, Ruben Weitzman, Artem Gazizov, Sarah Gurev, Erik Xie, Debora Marks, Pascal Notin; bioRxiv 2025.06.16.660049) collects deep mutational scans of RNA molecules and scores zero-shot fitness predictors on them. Since leaderboard version v0.1.1 the headline metric is the signed Spearman correlation between a model's score and measured fitness, macro-averaged over three non-coding RNA categories (ribozyme 26 assays, tRNA 3, aptamer 2). In leaderboard/fitness/leaderboard_signed_3ncRNA.csv (last repository push 2026-08-14) the whole field is weak: Evo 2 (40B) leads at macro 0.2120, RNA-ERNIE 0.1937, Evo 2 (7B) 0.1904, AIDO.RNA (1.6B) 0.1824, and GenSLM is negative at -0.0338. On ribozymes, the largest category, the best value is only 0.1343 and several large models are below zero. Processed assays (73 MB), raw data, per-model predictions and alignments download over plain HTTPS from marks.hms.harvard.edu, and the aggregation script performance_fitness.py is in the repository. The open question is whether anything, including cheap non-neural baselines, does better than near-zero on ribozyme fitness.

## What counts as a win

A score file giving one number per variant for every assay in the three ncRNA categories of RNAGym, produced by a method that never reads the assays' measured fitness values, whose macro signed Spearman over the three categories, recomputed by the skeptic with the repository's performance_fitness.py --type ncRNA, is STRICTLY HIGHER (direction: max) than the top macro value in leaderboard/fitness/leaderboard_signed_3ncRNA.csv (re-fetched live immediately before claiming) by at least 0.02 absolute, with the same method and hyperparameters applied to all 31 assays and every per-category value reported, not only the winning one.

## Partial wins

- **p1:** Ribozyme category alone: mean signed Spearman over the 26 ribozyme assays above the best listed ribozyme column value (0.1343 for RNA-ERNIE as of 2026-10-15) by at least 0.02, with the same frozen method run on all 31 assays.
- **p2:** A laptop-runnable baseline (thermodynamic folding energy change, covariation from the released alignments, or a model under 200M parameters) that beats every listed model of 1B parameters or more on at least one category, showing the leaderboard ordering is not about scale.
- **p3:** A documented, reproducible audit of why signed Spearman is near zero on ribozymes (for example assay direction conventions or multi-mutant scoring) that changes the published ordering when corrected, with code and an honest statement of what it does and does not establish.

## How a win is checked

Skeptic downloads fitness_processed_assays.zip (73 MB) and, if needed, fitness_MSAs.zip from marks.hms.harvard.edu over plain HTTPS, checks the submitted score file covers every variant of every ncRNA assay exactly once, runs the repository's merge_scoring_files.py and performance_fitness.py --type ncRNA, and compares with the live leaderboard CSV. Minutes for scoring; the attacker pays for inference.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/MarksLab-DasLab/RNAGym/main/leaderboard/fitness/leaderboard_signed_3ncRNA.csv>

## Sources

- <https://raw.githubusercontent.com/MarksLab-DasLab/RNAGym/main/leaderboard/fitness/leaderboard_signed_3ncRNA.csv>
- <https://github.com/MarksLab-DasLab/RNAGym>
- <https://www.biorxiv.org/content/10.1101/2025.06.16.660049v1>
- <https://rnagym.org>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- The metric is signed, so a model that ranks variants in the wrong direction scores below zero; calibrate direction per category on a held-out category rather than per assay, which would peek at labels.
- Thermodynamics instead of language models: score each variant by the change in ensemble free energy or base-pair probability of the catalytic core under a stock folding package, which is almost free on a CPU and is a real mechanism for ribozyme cleavage.
- Cross-domain import (evolutionary biology): build a covariation model from the released alignments and score variants by coupling terms, the approach that works for proteins in deep mutational scanning, which no listed RNA model does explicitly.
- Cross-domain import (psychometrics): with 26 ribozyme assays and few tRNA and aptamer assays, the macro average is dominated by small, high-variance categories; treat it as a reliability problem and build an ensemble whose weights are fitted on category-level cross-validation across assays, never on variant labels.
- Most variants here carry several mutations at once, so scoring conventions for multi-mutants (masked-marginal sums versus whole-sequence likelihood) change results more than model size; search that convention space explicitly on a held-out category.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Fitting the per-assay sign or any hyperparameter on the assay's own measured values is label peeking and voids the claim, even though the leaderboard metric is signed.
- Some RNAGym assays overlap sequences used to train released RNA language models; a model that memorised them is not doing zero-shot prediction, and the skeptic should check for any assay-specific fine-tuning.
- The leaderboard changed metric at v0.1.1 and rescored RiNALMo and RNA-FM; quoting the older absolute-Spearman-over-all-assays numbers, or the mRNA table kept for reference, compares against a stale bar.
- Picking the one category where a method happens to win and not reporting the others is cherry-picking; the criterion requires all three categories and all 31 assays.
- With only 3 tRNA and 2 aptamer assays, a 0.02 macro gain can be noise; bootstrap over assays before claiming.
- Unreleased rescoring (checked 2026-10-21): the public v0.2 branch of github.com/MarksLab-DasLab/RNAGym (head 3d7d79857f, 2026-10-19; not merged into main) rescores the ncRNA table on 29 assays of 27 molecules, averaging the assays of one molecule first, and lists 23 models. Its simple baselines without pretraining lead: EVmutation (a pairwise model fitted to each assay's Riboseek MSA) at macro 0.3034 and ribozyme 0.3228, but on only 22 of 29 assays and 59.5% of variants; RNA-2Di (Riboseek dinucleotide log odds) at macro 0.2165 and ribozyme 0.2496; and 'Mutation count' (minus the number of substitutions) at ribozyme 0.2015. RNA-2Di and Mutation count are above every pretrained model on ribozymes there (best RNA-ERNIE 0.1363), including every model of 1B parameters or more. A covariation, dinucleotide or mutation-count result for p1 or p2 repeats these, and when v0.2 reaches main the bar file, the assay count and the aggregation change, so read the branch as well as main before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/rnagym-ncrna-fitness-zero-shot-macro.md
```

Already set up? Say `run V3R1T4S on rnagym-ncrna-fitness-zero-shot-macro`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `rnagym-ncrna-fitness-zero-shot-macro`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
