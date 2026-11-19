# PREREG.v2 - escape-hatch record (written 2026-11-19T09:57:51Z)

Nothing in PREREG.md changes: models, features, grids, folds, seeds, gates and null designs are as frozen at
2026-11-19T09:55:11Z. This file records one harness fix made under the declared escape hatch.

1. score_p3.py crashed in its leakage self-test on fold 0 (TypeError: the IDN column of DominicaCodas.csv is a
   string column, and the perturbation added integers to it). The crash came after fold 0's model fit and before
   any held-out score was computed or printed. Fix: the harness now alters IDN by appending a suffix to the
   string (every value changes). Only score_p3.py (the harness) changes; dompipe.py (the frozen model) is
   unchanged, sha256 63f94f42fd5e470b9bd11521944d43cd5ad96932314348c81a51860df9d70c53. Rerun once.
2. Disclosure found while fixing it: IDN holds strings ('0' for 5,705 unidentified rows, ids such as '5586', and
   three ambiguous forms such as '6070/6068' and '59871?'). The frozen p3 features same_whale_last and
   echo2_if_switch compare IDN with the integer 0, which is always unequal for strings, so the frozen model treats
   the label '0' as one more whale label rather than as "unidentified" as the code comment intended. This is a
   feature-definition quirk of the frozen model, not leakage (it reads only earlier codas). It is NOT changed,
   because changing it after the freeze would be a model change; the p3 result is reported for the model as
   frozen.
