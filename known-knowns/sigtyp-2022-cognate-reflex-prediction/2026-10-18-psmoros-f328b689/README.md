# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.10: mean NED 0.18916240713560675

## What
At proportion 0.10, the frozen stage-2 minimum-Bayes-risk combination combiner/test/0.10 (seven frozen components trained only on the 10 surprise families' training-0.10 files and the development view, each masked test-0.10 row predicted in isolation, integer weights fit on validation splits cut from training-0.10) scores mean NED 0.18916240713560675 over the 10 surprise families under the pinned ST2022 scorer (left-to-right summation; the same value with compensated summation), strictly lower than this workspace's earlier confirmed 0.10 system (0.19710919181751296, bar_holder/), FeVeT's published predictions (0.2296925777970808) and Mockingbird-I1's official results-surprise-0.10.json value (0.2431316340782435), as a win on mean NED only.

The object is object/predictions-0.10.tsv: one predicted reflex for each of the 4029 masked test rows of the 10
surprise families at proportion 0.10 (columns family, COGID, language, prediction; segments separated by spaces).

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (a few minutes on a laptop; Python 3 standard library only). The script fetches 41 public
files from their pinned commits (the ST2022 repository at 03094435 and the FeVeT repository at 31898c53), checks each file's sha256, reproduces
Mockingbird-I1's official values exactly with a scorer written from the task's definition, scores the other bars
and the object, and checks that the object rebuilds the frozen result files. Set V3R1T4S_Q15_DATA to a folder that
already holds those files to skip the download.

## Compared to
| record | cell | value | source | fetched (UTC) |
|---|---|---|---|---|
| Mockingbird-I1, best official system | surprise, proportion 0.10, mean NED over 10 families | 0.2431316340782435 | https://github.com/sigtyp/ST2022, results/results-surprise-0.10.json at 03094435 | 2026-10-18T05:08:54Z |
| FeVeT (Wientzek 2025), published per-item predictions, rescored with the official scorer | same cell | 0.2296925777970808 | https://github.com/TGH-2020/FeVeT, results/predictions/reflex at 31898c53 | files 2026-10-16T20:48Z; repository unchanged at 2026-10-18T02:07:47Z |
| this workspace's earlier confirmed 0.10 system (package 2026-10-18-psmoros-81bf5365, not submitted) | same cell | 0.19710919181751296 | the-record-we-beat/previous-0.10-predictions.tsv | |
| this object | same cell | 0.18916240713560675 | object/predictions-0.10.tsv | |
FeVeT's paper prints 0.205 at proportion 0.1 (language-pooled); on that scale the object scores 0.1645 (panel/novelty.md). The object also beats this workspace's own earlier confirmed object at 0.10 (0.19710919181751296), which the human set as the bar for a new 0.10 claim.
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, BCFS or BLEU (all reported in the panel files; the claim is mean NED only).
- Nothing about other proportions, the development families, or other data; proportions 0.40 and 0.50 and the
  aggregate over all proportions are not part of this package.
- No comparison with published values beyond those listed; several bibliographic services were unreachable
  (rate limits or bot walls, recorded and never retried; panel/novelty.md lists what was searched).
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
- Ideas the component systems import (see their notes): joint-sequence models (Bisani and Ney 2008; Phonetisaurus),
  ROVER (Fiscus 1997), minimum-Bayes-risk decoding (Kumar and Byrne 2004), Felsenstein's pruning algorithm,
  memory-based learning (Daelemans and van den Bosch).
- Software: LingPy (https://github.com/lingpy/lingpy) and LingRex (https://github.com/lingpy/lingrex) in the official
  scorer and some components; scikit-learn in one component.
- Built by V3R1T4S agents (Opus 5.5) for Pavlos Moros (psmoros).
