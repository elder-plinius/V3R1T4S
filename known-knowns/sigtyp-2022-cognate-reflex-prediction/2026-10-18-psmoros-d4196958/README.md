# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.30: mean BLEU 0.6874377388475998

## What
At proportion 0.30, the frozen BLEU-MBR stage-2 object combiner/test/0.30 (the same predictions as object/predictions-0.30.tsv; six frozen entries trained on training-0.30 only, weights [2, 2, 1, 3, 1, 3] fit on the validation split shared/val/0.30 cut from training-0.30) has mean BLEU 0.6874377388475998 over the 10 surprise families under the pinned official ST2022 scorer (same value with left-to-right and compensated summation), strictly above Mockingbird-I1's official 0.6058548112827981, FeVeT's rescored 0.6356571184958077 and the cell's bar, our own earlier NED-targeted object bar_comb_new/test/0.30 at 0.6839233380559118 (by 0.003514400791688077 left-to-right and 0.003514400791687966 compensated), as a claim on mean BLEU only.

The object is object/predictions-0.30.tsv: one predicted reflex for each of the 11586 masked test rows of the 10
surprise families at proportion 0.30 (columns family, COGID, language, prediction; segments separated by spaces). It is a
BLEU-targeted combination of the same six frozen systems whose NED-targeted combination is the object of package
2026-10-18-psmoros-634f2c35; this package claims mean BLEU only.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (a few minutes on a laptop; Python 3 standard library only). The script fetches 41 public
files from their pinned commits (the ST2022 repository at 03094435 and the FeVeT repository at 31898c53), checks each
file's sha256, reproduces Mockingbird-I1's official values exactly with a scorer written from the task's definition,
scores FeVeT's published predictions, our earlier object and this object, and checks that the object rebuilds the frozen
result files. Set V3R1T4S_Q15_DATA to a folder that already holds those files to skip the download.

## Compared to
| record | cell | value | source | fetched (UTC) |
|---|---|---|---|---|
| our own earlier object (confirmed on mean NED at 0.30), highest mean BLEU known at 0.30 | surprise, proportion 0.30, mean BLEU over 10 families | 0.6839233380559118 | the-record-we-beat/earlier_object_predictions-0.30.tsv (package 2026-10-18-psmoros-634f2c35) | n/a |
| FeVeT (Wientzek 2025), published per-item predictions, rescored with the official scorer | same cell | 0.6356571184958077 | https://github.com/TGH-2020/FeVeT, results/predictions/reflex at 31898c53 | repository unchanged at 2026-10-18T12:59:33Z |
| Mockingbird-I1, best official system | same cell | 0.6058548112827981 | https://github.com/sigtyp/ST2022, results/results-surprise-0.30.json at 03094435 | 2026-10-18T12:56:07Z |
| this object | same cell | 0.6874377388475998 | object/predictions-0.30.tsv | |
FeVeT's paper and Cognate Transformer print no BLEU (panel/novelty.md). The margin over our earlier object is small
(0.0035); the pre-registered null test passes narrowly (how-we-built-it/null_test.md; panel/criterion.md estimates p
about 5e-4 with 100,000 extra controls).
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, NED or BCFS here (this object also scores mean NED 0.22149461586532132 and mean BCFS
  0.7502543049557795, but neither was pre-registered for it; the mean-NED claim at 0.30 is package
  2026-10-18-psmoros-634f2c35).
- Nothing about other proportions, the development families, or other data.
- No comparison with published values beyond those listed; several bibliographic services were unreachable (rate limits or
  bot walls, recorded and never retried; panel/novelty.md lists what was searched).
- Not a claim that the method generalises; it is one frozen system and its score on this public test set.

## Credits
- Task, data and scorer: Johann-Mattis List, Ekaterina Vylomova, Robert Forkel, Nathan Hill and Ryan Cotterell,
  "The SIGTYP 2022 Shared Task on the Prediction of Cognate Reflexes", SIGTYP 2022, https://aclanthology.org/2022.sigtyp-1.7/ ;
  repository https://github.com/sigtyp/ST2022 (and the datasets' original compilers credited there).
- Record compared against: Christo Kirov, Richard Sproat and Alexander Gutkin, "Mockingbird at the SIGTYP 2022 Shared
  Task: Two Types of Models for the Prediction of Cognate Reflexes", https://aclanthology.org/2022.sigtyp-1.9/ .
- Best later system compared against: T. Wientzek, "Using feature vectors for automated phonological
  reconstruction and reflex prediction", Open Research Europe 5:174 (2025); code and predictions https://github.com/TGH-2020/FeVeT .
- Also checked: Akavarapu and Bhattacharya, Cognate Transformer, EMNLP 2023, https://aclanthology.org/2023.emnlp-main.423/ .
- Ideas the component systems import: joint-sequence models (Bisani and Ney 2008; Phonetisaurus), ROVER (Fiscus 1997),
  minimum-Bayes-risk decoding (Kumar and Byrne 2004), Felsenstein's pruning algorithm, memory-based learning (Daelemans and
  van den Bosch); BLEU (Papineni, Roukos, Ward and Zhu 2002) as the per-item risk.
- Software: LingPy (https://github.com/lingpy/lingpy) and LingRex (https://github.com/lingpy/lingrex) in the official
  scorer and some components; scikit-learn in one component.
- Built by V3R1T4S agents (Opus 5.5) for Pavlos Moros (psmoros).
