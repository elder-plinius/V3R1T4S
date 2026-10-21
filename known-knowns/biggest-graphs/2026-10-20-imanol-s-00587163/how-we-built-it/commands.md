# Commands used

Working directory: this package's `how-we-built-it/`.

The portable replay uses the recorded trajectory, not wall-clock randomness or CPU scheduling:

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python rebuild_general.py trajectory.json --out rebuilt
```

The replay rebuilds from `seed6631.edges`, replays every recorded annealing chunk with its recorded seed and temperatures, asserts every exact cost against the measured trajectory, rebuilds after each zero, and ends by asserting `n=6637`, cost 0 and object SHA-256 `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059`. A fresh from-scratch replay of the final trajectory did not finish inside this run; the earlier 6633-vertex replay and every measured chunk are included, and no unrun replay is claimed.

The original search was run with the same source files in a workspace and its exact per-chunk output is summarised in `trajectory.json`. `PREREG.md` is the frozen preregistration from before any result. The only edit to `search.py` in this package is its hard-coded path to the submitted baseline package, replaced with the neutral name `submitted-baseline-package`; program logic is unchanged.
