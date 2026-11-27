# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output ends with:

```
ok   frozen model: 3 coefficients (at most 20)
ok   predictions recomputed from the frozen coefficients agree (max diff 1.78e-15)
ok   Bw RMSE 0.5239 over 999 points (claimed 0.5239)
ok   p2: Bw RMSE 0.5239 is at most 0.59 with at most 20 fitted parameters
PASS
```

## Rebuild the object (Python 3 with numpy)

```sh
cd how-we-built-it
sh get_data.sh
python3 -I -B code/fit_and_score_LW1.py
# expected: refit coef equal to the frozen ones; TEST Bw RMSE 0.5239 (n=999); 2-decimal 0.52; fitted parameters 3
```

Two numpy RuntimeWarnings, "Mean of empty slice" and "invalid value encountered in scalar divide", are expected: the
scorer is given winter rows only, so its Ba and Bs slices are empty.

`how-we-built-it/REPRODUCE.md` lists every step (baseline, hash-checked scoring, how the choices were made). Its
commands read `data/` (created by `get_data.sh`) and `object/` inside `how-we-built-it/`.
