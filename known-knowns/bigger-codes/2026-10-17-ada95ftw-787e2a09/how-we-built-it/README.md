# How the certificate was built
Python 3.13 with the pinned requirements.txt (numpy, scipy/HiGHS). Floats only locate the LP optimum; the certificate is then rebuilt and checked in exact Fractions.
Layout expected by the scripts (as in the original run folder): `attempts/obstruction/code/` = code/ here, `tools/` = tools/ here, `data/Andw.html` = one plain download of https://aeb.win.tue.nl/codes/Andw.html (not included; sha256 in the-record-we-beat/).
```sh
mkdir -p run/attempts/obstruction/result run/attempts/obstruction/output run/data && cp -R code run/attempts/obstruction/ && cp -R tools run/
curl -sS -o run/data/Andw.html https://aeb.win.tue.nl/codes/Andw.html
cd run/attempts/obstruction
python3 code/lpsweep.py ../../tools ../../data/Andw.html output/sweep.json   # main-table sweep
python3 code/lpsweep2.py                                                     # + secondary tables
python3 code/lpsweep3_conservative.py                                        # refuse single-value inputs
python3 code/make_certs.py 31 10 7                                       # -> result/cert_A31_10_7.json
```
If the table page has changed since the fetch recorded in the-record-we-beat/, the sweep can differ; the certificate in object/ does not depend on it except through the one input value named in table_inputs.
PREREG.md is the run's preregistration (frozen 2026-10-17T08:04:55Z). null_test: not needed (explicit certificate, deterministic exact checker).
