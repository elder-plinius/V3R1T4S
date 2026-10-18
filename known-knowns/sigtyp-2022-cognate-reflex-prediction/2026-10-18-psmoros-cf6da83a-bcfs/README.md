# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.50: mean BCFS 0.7114179305724276

## What
At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (the same predictions as object/predictions-0.50.tsv) of 8 entries, which read only the 10 surprise families' training-0.50.tsv, the masked test-0.50.tsv one masked-language partition at a time, and the task release's development-family training-0.10.tsv and masked test-0.10.tsv files (no solutions file of any family), scores mean B-Cubed F-score 0.7114179305724276 over the 10 SIGTYP 2022 surprise families under the pinned ST2022 scorer (commit 03094435, the same value under left-to-right and builtin summation), strictly above Mockingbird-I1's official 0.6050308536957327 in results-surprise-0.50.json and above the cell's stricter bar, FeVeT's published predictions rescored at 0.6423935720824072; this is a win on mean BCFS at 0.50 only.

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
| FeVeT (Wientzek 2025), published per-item predictions, rescored with the official scorer (the bar) | surprise, proportion 0.50, mean BCFS over 10 families | 0.6423935720824072 | https://github.com/TGH-2020/FeVeT, results/predictions/reflex at 31898c53 | 2026-10-18T11:47:19Z-11:47:22Z (NOVELTY skeptic of B50; sha256 equal to the packaged files) |
| Mockingbird-I1, best official system | same cell | 0.6050308536957327 | https://github.com/sigtyp/ST2022, results/results-surprise-0.50.json at 03094435 | 2026-10-18T11:45:21Z |
| this object | same cell | 0.7114179305724276 | object/predictions-0.50.tsv | |
Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023, Table 5) prints BCFS 0.6477 at proportion 0.5, above FeVeT's rescored value; the object beats it by 0.0637 (panel/novelty.md). FeVeT's paper prints 0.673, a mean over 99 languages; on that scale the object scores 0.742250.
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, NED or BLEU here (each metric is its own cell; all values are in the panel files).
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
