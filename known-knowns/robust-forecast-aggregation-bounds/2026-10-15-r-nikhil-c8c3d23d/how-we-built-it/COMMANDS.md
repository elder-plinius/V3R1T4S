# How the object was built (commands, paths relative to this package)

The object is verified by `verify-it-yourself/` regardless of how it was found. `C=how-we-built-it/code`.

Setup for the float search only: `python3 -m venv venv && venv/bin/pip install -r how-we-built-it/requirements.txt`
(NumPy 2.0.2, Python 3.9.6). During the run every job ran under `nice -n 15` with one thread and a hard time cap.

## 1. Float search from the paper's construction (`mix_opt.py`, NumPy)

`mix_opt.py` maximises, in floating point, LB(D) over adversary mixtures of K conditionally independent two-state
environments sharing R report values (Nelder–Mead with restarts), then rounds the best point to fractions with
denominator `--den` and writes `<out>_mixture.json` for the exact checker. Runs, as described in the lens report
(the exact shell lines were not logged; `--from_table3 1`, 20,000 iterations and the 1/10^9 rounding are named in the
report, `--restarts 1` is inferred from the logs, which show a single restart each):

    venv/bin/python -I $C/mix_opt.py --from_table3 1 --restarts 1 --out output/t3_local
    venv/bin/python -I $C/mix_opt.py --from_table3 1 --restarts 1 --nm_iters 20000 --den 1000000000 --out output/t3_local_fine

Both start exactly at Theorem 3.4's point (float LB 0.023379) and end at float LB 0.023378805, 2.223e-07 above
31/1326. The finer run's optimum: reports about 0.167325 / 0.832675, prior means about 0.417121 / 0.582879, weights
about 1/2 each. Two further runs in the default setting (K = 2, R = 2, asymmetric experts allowed, 200 random
restarts, seed 1; meant to be K = 3 and K = 4 runs, but a quoting slip dropped their arguments) reached the same
optimum from random starts:

    venv/bin/python -I $C/mix_opt.py --out output/k2r2_default

(an equivalent command: the original runs passed the intended arguments inside the `--out` value, so their files are
named after them). Their rationalised mixtures also pass the exact checker with margin 2.223e-07.

## 2. Exact rational point in the mirror-symmetric family (`build_symmetric.py`, standard library)

The float optimum is mirror-symmetric (environment B is the image of A under x ↦ 1 − x, weights 1/2), so the run
evaluated 11 short-fraction points (x_H, mu_A) of that family exactly with `verify-it-yourself/lb_check.py`, using an
inline script that was not saved. Its log (exact values, margin over 31/1326):

    xH=5/6 muA=5/12  LB=0.023378582202  margin=0.0000e+00  no
    xH=33307/40000 muA=417121/1000000  LB=0.023378804538  margin=2.2234e-07  BEATS
    xH=8327/10000 muA=4171/10000  LB=0.023378804245  margin=2.2204e-07  BEATS
    xH=833/1000 muA=417/1000  LB=0.023378741996  margin=1.5979e-07  BEATS
    xH=8327/10000 muA=2607/6250  LB=0.023378804096  margin=2.2189e-07  BEATS
    xH=20817/25000 muA=2607/6250  LB=0.023378804523  margin=2.2232e-07  BEATS
    xH=83267/100000 muA=2607/6250  LB=0.023378804517  margin=2.2232e-07  BEATS
    xH=41633/50000 muA=2607/6250  LB=0.023378804365  margin=2.2216e-07  BEATS
    xH=83267/100000 muA=4171/10000  LB=0.023378804401  margin=2.2220e-07  BEATS
    xH=83267/100000 muA=8343/20000  LB=0.023378804421  margin=2.2222e-07  BEATS
    xH=83267/100000 muA=1043/2500  LB=0.023378803542  margin=2.2134e-07  BEATS
    best: xH=33307/40000 muA=417121/1000000 LB=1652448303171916717080006468042849/70681471350112364987160770000000000

`build_symmetric.py` was written at packaging time to replace that unsaved step: it builds the family member for any
(x_H, mu_A), and for the best point it reproduces the object byte for byte:

    python3 -I $C/build_symmetric.py 33307/40000 417121/1000000 rebuilt.json
    shasum -a 256 rebuilt.json      # c8c3d23d5e791ec2c2d51a0ce5555fa7af7e9712d0c0ad0acd31f7bdbdc0b971
    python3 -I verify-it-yourself/lb_check.py rebuilt.json

Any line of the log above can be re-derived the same way (build the point, run `lb_check.py`); the point 5/6, 5/12 is
the paper's Table 3 mixture and gives exactly 31/1326.

## 3. Pre-registration

`PREREG.md` (frozen before any attack program produced output) fixes the object type, the statistic (exact LB(D) by
the checker, both internal routes agreeing) and the threshold (LB(D) > 31/1326 strictly) for this cell; it states
`null_test: not needed` (a deterministic exact certificate, no statistical component), so there is no `null_test.md`.
`PREREG.v2.md` adds rules for the other (binary-state) cell, which this package does not claim; it changed nothing
for this cell.
