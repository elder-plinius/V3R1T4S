# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.50: mean BLEU 0.6520222200978466

## What
At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (identical to object/predictions-0.50.tsv) predicts the 18101 masked rows of the 10 SIGTYP 2022 surprise families' test-0.50.tsv with mean BLEU 0.6520222200978466 under the pinned official ST2022 scorer (left-to-right summation; 0.6520222200978465 compensated), strictly above Mockingbird-I1's official 0.5337187296541888 and above this cell's bar, FeVeT's published predictions rescored at 0.5768215755932388, using only training-0.50, row-isolated masked test-0.50 partitions and the task's development families (including the disclosed development-family rows for hillburmish and kesslersignificance).

The object is object/predictions-0.50.tsv: one predicted reflex for each of the 18101 masked test rows of the 10
surprise families at proportion 0.50 (columns family, COGID, language, prediction; segments separated by spaces).

Data used: the eight stage-2 entries were trained on the 10 surprise families' training-0.50.tsv files and the task
release's development families (data/), and predicted each masked test row from that row alone. Two entries (the
classifier lens) also add rows of two development families for languages they share with surprise families
(mannburmish for hillburmish; listsamplesize's English, German and French for kesslersignificance); those rows may
contain the same concepts as the surprise gold in another dataset's transcription. Without them the win stands
(panel/criterion.md, counterfactuals). No entry read a solutions file of any family.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (a few minutes on a laptop; Python 3 standard library only). The script fetches 41 public
files from their pinned commits (the ST2022 repository at 03094435 and the FeVeT repository at 31898c53), checks
each file's sha256, reproduces Mockingbird-I1's official values exactly with a scorer written from the task's
definition, scores FeVeT's published predictions and the object, and checks that the object rebuilds the frozen
result files. Set V3R1T4S_Q15_DATA to a folder that already holds those files to skip the download.

## Compared to
| record | cell | value | source | fetched (UTC) |
|---|---|---|---|---|
| FeVeT (Wientzek 2025), published per-item predictions, rescored with the official scorer (the bar) | surprise, proportion 0.50, mean BLEU over 10 families | 0.5768215755932388 | https://github.com/TGH-2020/FeVeT, results/predictions/reflex at 31898c53 | 2026-10-18T11:47:19Z-11:47:22Z (NOVELTY skeptic of B50; sha256 equal to the packaged files) |
| Mockingbird-I1, best official system | same cell | 0.5337187296541888 | https://github.com/sigtyp/ST2022, results/results-surprise-0.50.json at 03094435 | 2026-10-18T11:45:21Z |
| this object | same cell | 0.6520222200978466 | object/predictions-0.50.tsv | |
Neither FeVeT's paper nor Cognate Transformer prints BLEU; among the official results the best BLEU at 0.50 is Mockingbird-I1's (panel/novelty.md).
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, NED or BCFS here (each metric is its own cell; all values are in the panel files).
- Nothing about other proportions, the development families, or other data; proportions 0.10-0.40 and the
  aggregate over all proportions are not part of this package.
- No comparison with published values beyond those listed (panel/novelty.md lists what was searched).
- Not a claim that the method generalises; it is one frozen system and its score on this public test set.

## Credits
- Task, data and scorer: Johann-Mattis List, Ekaterina Vylomova, Robert Forkel, Nathan Hill and Ryan Cotterell,
  "The SIGTYP 2022 Shared Task on the Prediction of Cognate Reflexes", SIGTYP 2022, https://aclanthology.org/2022.sigtyp-1.7/ ;
  repository https://github.com/sigtyp/ST2022 (and the datasets' original compilers credited there).
- Record compared against: Christo Kirov, Richard Sproat and Alexander Gutkin, "Mockingbird at the SIGTYP 2022 Shared
  Task: Two Types of Models for the Prediction of Cognate Reflexes", https://aclanthology.org/2022.sigtyp-1.9/ .
- Bar holder (best later system): T. Wientzek, "Using feature vectors for automated phonological
  reconstruction and reflex prediction", Open Research Europe 5:174 (2025); code and predictions https://github.com/TGH-2020/FeVeT .
- Also checked: Akavarapu and Bhattacharya, Cognate Transformer, EMNLP 2023, https://aclanthology.org/2023.emnlp-main.423/ .
- Ideas the component systems import (see their notes): joint-sequence models (Bisani and Ney 2008; Phonetisaurus),
  ROVER (Fiscus 1997), minimum-Bayes-risk decoding (Kumar and Byrne 2004), Felsenstein's pruning algorithm,
  memory-based learning (Daelemans and van den Bosch).
- Software: LingPy (https://github.com/lingpy/lingpy) and LingRex (https://github.com/lingpy/lingrex) in the official
  scorer and some components; scikit-learn in one component.
- Built by V3R1T4S agents (Opus 5.5) for Pavlos Moros (psmoros).
