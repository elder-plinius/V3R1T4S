# How we built it — exact commands

The code in this folder is a verbatim copy of what ran. Layout in the
original run (relative to the workspace folder):

```
code/check_srbench.py                 checker (split, R2, complexity)
code/validate_checker.py            checker validation (not needed to rebuild)
attempts/constructor/code/dict_sr.py  lens 1: dictionary sparse regression
attempts/smuggler/code/distill_sr.py  lens 2: kernel-ridge distillation
data/1028_SWD.tsv.gz                dataset (see the-record-we-beat/record.txt)
data/results.feather                live table (see the-record-we-beat/record.txt)
```

Exact commands (Python with numpy, sympy, scikit-learn, pyarrow, pandas):

```sh
python3 -m venv venv-srbench
venv-srbench/bin/pip install pyarrow pandas numpy sympy pyyaml scikit-learn
venv-srbench/bin/python attempts/constructor/code/dict_sr.py
venv-srbench/bin/python attempts/smuggler/code/distill_sr.py
```

The smuggler lens writes `attempts/smuggler/output/results.json`, which is
the object in this package (`object/expressions.json`, byte-identical).
The frozen rule is `PREREG.v2.md` (which supersedes `PREREG.md` on the
split definition only — see the note at its top). The baseline record
(the bar recomputed from the live table) is in `baseline/leader_table.txt`.

Pinned requirements for the lens code: numpy==2.5.4, sympy==1.14.0,
scikit-learn==1.9.1 (plus pyarrow and pandas for reading the table).
The standalone verifier in `verify-it-yourself/` needs only the three
pinned packages (see its requirements.txt).
