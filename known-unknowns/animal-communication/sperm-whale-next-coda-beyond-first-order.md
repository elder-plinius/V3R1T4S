# MOONSHOT - Sperm whale codas: frozen next-coda predictions on held-out DTag recordings that beat a first-order model and show dependence beyond the previous coda

🐋 **Animal communication** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: laptop-minutes to laptop-hours (two public CSV files of about 0.5 MB and 0.75 MB in one GitHub repository) · open as of 2026-11-13

## The problem

Sperm whales communicate with codas, short patterned trains of clicks. Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas (Nature Communications 15:3617, 2024) released two tables in github.com/pratyushasharma/sw-combinatoriality: DominicaCodas.csv (8,719 codas recorded off Dominica from 2005 to 2016, 7,770 of clan EC1 and 949 of clan EC2 in its Clan column, with inter-click intervals, coda type, social unit and whale ids, 747,518 bytes) and sperm-whale-dialogues.csv (3,840 codas in 219 REC recordings, recorded on animal-borne DTags; the paper describes 3,948, with click count, duration, inter-click intervals, a whale label and a time stamp per coda, 500,380 bytes). WhaleLM (Sharma, Gero, Rus, Torralba, Andreas; bioRxiv 2024.10.31.621071, NeurIPS 2025 workshop) trained sequence models on these DTag codas and reported that removing coda order raised perplexity by up to 22.7 percent and that dependence reached up to eight codas back, but it gave no absolute values and no code. On 1,483 to 1,501 public Dominica codas, Sinha and Chavan found that adding the second preceding coda gained 0.2076 bits per coda over a pooled first-order model but minus 0.0285 bits (p = 0.955) over a stream-local first-order reference (arXiv 2606.16084v4, 22 September 2026), an order-2 minus order-1 gain of 0.081 bits with interval from minus 0.006 to 0.177 and p = 0.136 (arXiv 2609.16612v2), and a 0.188-bit raw gain that falls to minus 0.004 bits against a repetition-aware model (arXiv 2610.33974v1). As of 2026-11-13 no public, reproducible held-out result shows that a sperm whale's next coda depends on more than the previous one. The repository states no licence; the files are public and cited to the paper.

## What counts as a win

Data: sperm-whale-dialogues.csv. Streams: codas grouped by REC, ordered by TsTo, with ties (7 in the file) kept in file order. Token of a coda: (min(nClicks, 10), duration bin), with 5 equal-frequency Duration bins cut on the training folds only. Folds: sort the distinct REC strings and put the i-th in fold i mod 5; each fold is held out once. Scored: every coda with at least 2 earlier codas in its stream. Reference R1: a bigram over tokens with additive smoothing chosen from 0.01, 0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds. The claim is a frozen model, trained on the training folds only, that outputs a full distribution over tokens at each scored position from earlier codas of the same stream (their intervals, durations, whale labels, time stamps), never from any field of the coda being predicted. Pooled over the 5 folds, both must hold: (1) its cross-entropy is at least 0.10 bits per coda BELOW R1 (direction: min); (2) it is at least 0.05 bits below the same model retrained with its input cut to the single previous coda, and the 95 percent interval of a paired bootstrap over REC groups (10,000 resamples) for this gain excludes 0. Deliverables: code, folds, bin edges, and per-position probabilities for the model, its cut twin and R1.

## Partial wins

- **p1:** Condition (1) alone at a smaller margin: cross-entropy at least 0.05 bits per coda below R1, with the paired bootstrap interval over REC groups excluding 0.
- **p2:** Condition (2) alone at a smaller margin: at least 0.03 bits per coda below the model's own single-previous-coda twin, with the paired bootstrap interval over REC groups excluding 0, even if condition (1) fails.
- **p3:** The same test on DominicaCodas.csv, all 8,719 rows of both clans: tokens are CodaType; each Date is first rewritten with every hyphen replaced by a slash (the file writes four days both ways, for example 02-03-2015 and 02/03/2015); streams are rows sharing that rewritten Date and Unit, ordered by codaNUM2018; folds are the distinct rewritten Date strings sorted as text, with the i-th in fold i mod 5; a model using two or more previous codas beats a smoothed bigram over the same tokens by at least 0.05 bits per coda, with a bootstrap interval over Date groups excluding 0.
- **p4:** Turn-taking: on the dialogues folds, predict whether the next coda carries the same whale label as the previous one with held-out log-loss at least 0.05 bits below a smoothed first-order model of that same-or-switch sequence, with a bootstrap interval over REC groups excluding 0.

## How a win is checked

The skeptic downloads the two CSV files, records their checksums, regenerates folds and bin edges with an independent script, fits R1 and the truncated twin themselves, and recomputes all cross-entropies from the per-position probabilities after checking that each vector sums to 1 with no zero entries. They rerun the bootstrap with a fresh seed and test for leakage by altering every field of the predicted coda and confirming that the predictions do not change.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25>

## Sources

- <https://github.com/pratyushasharma/sw-combinatoriality>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC11076547/>
- <https://www.biorxiv.org/content/10.1101/2024.10.31.621071v1.full>
- <https://arxiv.org/abs/2606.16084>
- <https://arxiv.org/abs/2609.16612>
- <https://arxiv.org/abs/2610.33974>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Interpolated Kneser-Ney n-grams with orders chosen on inner folds, as a strong and transparent first model.
- Continuous features of earlier codas (rubato, the slow drift of duration across a sequence that Sharma et al. 2024 describe) fed to a small recurrent network with heavy dropout.
- Cross-domain import (point processes): a marked Hawkes process in which coda timing and token are modelled together, so that gaps between earlier codas inform the next token.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Do not load the .p files in the repository: unpickling runs code. Everything needed is in the two CSV files.
- The 3,840 codas (3,418 scored) fall into 5 folds of 483 to 1,387 codas, which is small; gains of a few hundredths of a bit can come from repeated runs of one token, so a repetition-aware twin is the honest comparison.
- Whale labels in the dialogues file may be per-recording rather than global identities; treat them as speaker turns within a recording.
- WhaleLM and the Sinha and Chavan papers use other tokenizations and corpora; their numbers are context, not baselines for this exact setup.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/animal-communication/sperm-whale-next-coda-beyond-first-order.md
```

Already set up? Say `run V3R1T4S on sperm-whale-next-coda-beyond-first-order`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `sperm-whale-next-coda-beyond-first-order`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
