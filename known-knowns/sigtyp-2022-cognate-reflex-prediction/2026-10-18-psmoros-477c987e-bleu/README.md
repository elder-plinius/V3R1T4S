# SIGTYP 2022 cognate reflex prediction, surprise data, proportion 0.40: mean BLEU 0.6533966833715619

## What
At proportion 0.40, the predictions of the frozen single system classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv, identical to object/predictions-0.40.tsv), made for the masked rows of the 10 SIGTYP 2022 surprise families from training-0.40 and development-family training files only, have mean BLEU 0.6533966833715619 under the pinned ST2022 scorer (commit 03094435, both summation modes), strictly higher than Mockingbird-I1's official 0.5723601982335171 from results-surprise-0.40.json, by 0.08103648513804473; this is a win on mean BLEU at 0.40 only.

The object is object/predictions-0.40.tsv: one predicted reflex for each of the 14992 masked test rows of the 10
surprise families at proportion 0.40 (columns family, COGID, language, prediction; segments separated by spaces).

Data used: at proportion 0.40 the system was trained on the 10 surprise families' training-0.40.tsv files and the task
release's development families, and predicted each masked test row from that row alone. It also adds rows of two
development families for languages they share with surprise families (mannburmish for hillburmish;
listsamplesize's English, German and French for kesslersignificance); those rows may contain the same concepts
as the surprise gold in another dataset's transcription. Selection note (selection.md): the per-family gate of
its reranker was written after the lens saw per-family validation numbers of the ungated reranker, so its
validation score may be optimistic; the selection rule was applied as written. No solutions file of any family
was read.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (a few minutes on a laptop; Python 3 standard library only). The script fetches 31 public
files from their pinned commit (the ST2022 repository at 03094435), checks each file's sha256, reproduces
Mockingbird-I1's official values exactly with a scorer written from the task's definition, scores the object,
and checks that the object rebuilds the frozen result files. Set V3R1T4S_Q15_DATA to a folder that already holds
those files to skip the download.

## Compared to
| record | cell | value | source | fetched (UTC) |
|---|---|---|---|---|
| Mockingbird-I1, best official system (the bar) | surprise, proportion 0.40, mean BLEU over 10 families | 0.5723601982335171 | https://github.com/sigtyp/ST2022, results/results-surprise-0.40.json at 03094435 | 2026-10-18T21:41:36Z |
| this object | same cell | 0.6533966833715619 | object/predictions-0.40.tsv | |
Corrections found by the panel (recorded here, the claim files are unchanged): (1) the harness command in the claim's REPRODUCE.md needs --python pointing at the systems' interpreter (the default is a placeholder in the packaged harness copy); every REPRODUCE skeptic added it. (2) The development-family disclosure is conservative: at proportions 0.10-0.40 only the listsamplesize rows (English, German, French for kesslersignificance) are read; the mannburmish rows for hillburmish enter only at 0.50 (the targets have at least 30 training reflexes at the smaller proportions). Without any development-family rows the system still beats the bar (CRITERION counterfactuals in panel/). (3) Cognate Transformer (EMNLP 2023) reports proportions 0.10, 0.30 and 0.50, not 0.50 only as the scout note says; it reports no 0.40 value and no aggregate. (4) In copied documentation the original scratch path of the entry's REPRODUCE.md is written SCRATCH_DIR/ (any empty folder).
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, NED or BCFS here (each metric is its own cell; all values are in the panel files).
- Nothing about other proportions or the aggregate over all proportions (separate cells).
- No comparison with published values beyond those listed (panel/novelty.md lists what was searched).
- Not a claim that the method generalises; it is one frozen system and its score on this public test set.

## Credits
- Task, data and scorer: Johann-Mattis List, Ekaterina Vylomova, Robert Forkel, Nathan Hill and Ryan Cotterell,
  "The SIGTYP 2022 Shared Task on the Prediction of Cognate Reflexes", SIGTYP 2022, https://aclanthology.org/2022.sigtyp-1.7/ ;
  repository https://github.com/sigtyp/ST2022 (and the datasets' original compilers credited there).
- Record compared against: Christo Kirov, Richard Sproat and Alexander Gutkin, "Mockingbird at the SIGTYP 2022 Shared
  Task: Two Types of Models for the Prediction of Cognate Reflexes", https://aclanthology.org/2022.sigtyp-1.9/ .
- Also checked: T. Wientzek, FeVeT, Open Research Europe 5:174 (2025), https://github.com/TGH-2020/FeVeT (no 0.40
  value, no aggregate); Akavarapu and Bhattacharya, Cognate Transformer, EMNLP 2023,
  https://aclanthology.org/2023.emnlp-main.423/ (proportions 0.10, 0.30 and 0.50 only; no 0.40 value, no aggregate).
- Software: LingPy (https://github.com/lingpy/lingpy) and LingRex (https://github.com/lingpy/lingrex) in the official
  scorer; scikit-learn and PyTorch where the system's code uses them.
- Built by V3R1T4S agents (Opus 5.5) for Pavlos Moros (psmoros).
