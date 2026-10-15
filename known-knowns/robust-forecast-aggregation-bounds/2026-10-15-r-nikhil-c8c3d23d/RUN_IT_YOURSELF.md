# Run it yourself

From this folder, in a fresh shell (needs `sh` and Python 3.9 or newer; every checker uses only the standard library;
nothing is downloaded and nothing is written):

```sh
sh verify-it-yourself/run_checks.sh
```

What it does: runs three standard-library scripts on `object/mixture.json`, then compares their output with the
expected exact fraction.

- `verify-it-yourself/lb_check.py`: computes LB(D) = min over aggregators f of E_D[regret of f], in exact rationals, in
  two ways (the variance form of Lemma 2.1 of arXiv:2604.24517v2, and the literal loss-difference definition with the
  outcome drawn as Bernoulli(theta)); checks the model constraints; exit code 0 only if LB(D) > 31/1326.
- `verify-it-yourself/independent_recheck.py`: a separately written third computation by the normalised-posterior route.
- `verify-it-yourself/check_declared_fields.py`: checks that the object's informational fields (`mu`, `reports`) agree
  with its states, priors and likelihoods.

Expected output ends with:

```
three exact computations agree: LB = 1652448303171916717080006468042849/70681471350112364987160770000000000 > 31/1326; declared fields consistent
PASS
```

About 2 seconds on a laptop. The real output, and a corrupted-object test, are in `verify-it-yourself/RECEIPTS.md`.

To check one script by hand: `python3 -I verify-it-yourself/lb_check.py object/mixture.json` (expected lines include
`LB_variance_form: 1652448303171916717080006468042849/70681471350112364987160770000000000` and
`verdict: LOWER_BOUND_BEATS_BAR`). Control: the paper's own Table 3 mixture evaluates to exactly 31/1326 with the same
script (`verdict: NO_IMPROVEMENT`, exit code 1); build it with the command below and the parameters 5/6 and 5/12.

To rebuild the object byte for byte from its two parameters (Python 3 standard library):

```sh
python3 -I how-we-built-it/code/build_symmetric.py 33307/40000 417121/1000000 rebuilt.json
shasum -a 256 rebuilt.json    # c8c3d23d5e791ec2c2d51a0ce5555fa7af7e9712d0c0ad0acd31f7bdbdc0b971, same as object/mixture.json
```

To redo the search that found the parameters, follow `how-we-built-it/COMMANDS.md` (NumPy; a few seconds per run).
