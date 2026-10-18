# SIGTYP 2022 cognate reflex prediction, surprise data, aggregate over the five proportions: A_NED 0.23164186694791358

## What
Over the five proportions 0.10, 0.20, 0.30, 0.40 and 0.50, the frozen single system classifier/PRIMARY (code attempts/classifier/frozen/PRIMARY/code, retrained at each proportion P on that P's surprise training files plus the development-family training files; predictions attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv, equal to object/predictions-P.tsv) has the PREREG aggregate A_NED = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 = 0.23164186694791358, where S(P) is the mean NED over the 10 surprise families under the pinned official ST2022 scorer, strictly lower than Mockingbird-I1's A_NED 0.2931673956342817 computed the same way from its official results-surprise-P.json totals, a win on NED only.

The object is object/predictions-P.tsv for P = 0.10, 0.20, 0.30, 0.40, 0.50: one predicted reflex for each masked test row of the 10
surprise families at each proportion (0.10: 4029, 0.20: 7887, 0.30: 11586, 0.40: 14992, 0.50: 18101 rows; columns family, COGID, language, prediction; segments separated by spaces).
At each P the predictions come from the same frozen system trained on training-P alone.

Data used: at each proportion P the system was trained on the 10 surprise families' training-P.tsv files and the task
release's development families, and predicted each masked test row from that row alone. It also adds rows of two
development families for languages they share with surprise families (mannburmish for hillburmish;
listsamplesize's English, German and French for kesslersignificance); those rows may contain the same concepts
as the surprise gold in another dataset's transcription. Selection note (selection.md): the per-family gate of
its reranker was written after the lens saw per-family validation numbers of the ungated reranker, so its
validation score may be optimistic; the selection rule was applied as written. No solutions file of any family
was read.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS (a few minutes on a laptop; Python 3 standard library only). The script fetches 155 public
files from their pinned commit (the ST2022 repository at 03094435), checks each file's sha256, reproduces
Mockingbird-I1's official values exactly with a scorer written from the task's definition, scores the object and computes both aggregates,
and checks that the object rebuilds the frozen result files. Set V3R1T4S_Q15_DATA to a folder that already holds
those files to skip the download.

## Compared to
| record | cell | value | source | fetched (UTC) |
|---|---|---|---|---|
| Mockingbird-I1, best official system on this aggregate among those with all five proportions (the bar) | A_NED over 0.10-0.50, 10 surprise families | 0.2931673956342817 | https://github.com/sigtyp/ST2022, results/results-surprise-P.json at 03094435 (totals by P in the-record-we-beat/) | 2026-10-18T22:10:57Z |
| this object | same cell | 0.23164186694791358 | object/predictions-P.tsv | |
Corrections found by the panel (recorded here, the claim files are unchanged): (1) the harness command in the claim's REPRODUCE.md needs --python pointing at the systems' interpreter (the default is a placeholder in the packaged harness copy); every REPRODUCE skeptic added it. (2) The development-family disclosure is conservative: at proportions 0.10-0.40 only the listsamplesize rows (English, German, French for kesslersignificance) are read; the mannburmish rows for hillburmish enter only at 0.50 (the targets have at least 30 training reflexes at the smaller proportions). Without any development-family rows the system still beats the bar (CRITERION counterfactuals in panel/). (3) Cognate Transformer (EMNLP 2023) reports proportions 0.10, 0.30 and 0.50, not 0.50 only as the scout note says; it reports no 0.40 value and no aggregate. (4) In copied documentation the original scratch path of the entry's REPRODUCE.md is written SCRATCH_DIR/ (any empty folder).
Details: the-record-we-beat/.

## Not claimed
- Nothing about ED, BCFS or BLEU here (each metric is its own cell), and no single proportion: this cell is the aggregate only (0.40 is claimed separately; 0.10-0.30 and 0.50 were claimed earlier by other objects).
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
