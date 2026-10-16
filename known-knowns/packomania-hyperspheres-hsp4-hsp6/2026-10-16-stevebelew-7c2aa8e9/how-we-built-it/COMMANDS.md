# How the object was built (commands)

Layout used by run_polish.py: a run folder containing `data/hsp4_radius.txt` (Packomania's radius.txt) and
`data/coords/hsp4-<N>.txt` (the tarball's files), and `attempts/warm-polish/code/` holding these two scripts, with
`attempts/warm-polish/output/` for results.

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python -I attempts/warm-polish/code/run_polish.py 1680 5 66

Output: `attempts/warm-polish/output/polish_66.txt` (the object; first line a comment with r and gain) and `log.txt`.
Seed: `numpy.random.default_rng(1000 + N)`; per-row budget 30-240 s of basin hopping; nice 10.
Pre-registration frozen before the attack: PREREG.md (this folder).
