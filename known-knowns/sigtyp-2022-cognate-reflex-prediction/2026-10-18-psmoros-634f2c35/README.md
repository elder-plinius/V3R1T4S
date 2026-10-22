# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.30: mean NED 0.22327922550091464

## What
At proportion 0.30, the frozen stage-2 combiner predictions combiner/test/0.30, reproducible from the surprise families' training-0.30 files and masked test-0.30 rows alone, score mean NED 0.22327922550091464 over the 10 SIGTYP-2022 surprise families under the pinned official ST2022 scorer (left-to-right summation; 0.22327922550091467 with compensated summation), strictly below FeVeT's published predictions rescored on the official scale (0.2632988364952282) and Mockingbird-I1's official results-surprise-0.30.json value (0.2898984929868421).

The object is object/predictions-0.30.tsv: one predicted reflex for each of the 11586 masked test rows of the 10
surprise families at proportion 0.30 (columns family, COGID, language, prediction; segments separated by spaces).

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
| Mockingbird-I1, best official system | surprise, proportion 0.30, mean NED over 10 families | 0.2898984929868421 | https://github.com/sigtyp/ST2022, results/results-surprise-0.30.json at 03094435 | 2026-10-18T04:59:45Z |
| FeVeT (Wientzek 2025), published per-item predictions, rescored with the official scorer | same cell | 0.2632988364952282 | https://github.com/TGH-2020/FeVeT, results/predictions/reflex at 31898c53 | files 2026-10-16T20:48Z; repository unchanged at 2026-10-18T02:07:47Z |
| this object | same cell | 0.22327922550091464 | object/predictions-0.30.tsv | |
FeVeT's paper prints 0.2397 at proportion 0.3; that number is a language-pooled mean on its own distance measure, not the official family mean. On that scale the object scores 0.1966 (panel/novelty.md).
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
