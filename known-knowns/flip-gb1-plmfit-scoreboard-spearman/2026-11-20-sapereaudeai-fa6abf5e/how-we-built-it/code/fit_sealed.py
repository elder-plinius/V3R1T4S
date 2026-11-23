"""Fit the two SEALED configurations of runs/2026-11-20-0215/claim/UNSCORED-PREDICTION.md and
write prediction files.  No grid, no selection, no tuning: the configuration is an input.

PREREG section 2 fixes both configurations verbatim:
  A  fitset=all        s2=0.5  s3=0.25  alpha=0.03   objective=ls  transform=log0.001
  B  fitset=trainonly  s2=1    s3=1     alpha=0.001  objective=ls  transform=log0.01

THIS SCRIPT NEVER READS THE `score` COLUMN OF A TEST ROW.  It reads `score` exactly once,
through gb1k.scores(), applied to the list of FITTING rows only (see `ytr` below).  Test rows
contribute only their `aa_seq` (for the four site letters and for the output key) - never a score.
Scoring happens afterwards, in code/score.py, from prediction files.

Usage:
  python -I fit_sealed.py <csv> <outdir> --config A|B [--seeds 1,2,3] [--tag T]
"""
import hashlib
import json
import os
import sys
import time

import numpy as np
from sklearn.model_selection import KFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gb1k as G

SPLIT = "three_vs_rest"

# PREREG section 2 - the sealed configurations, as literals.
SEALED = {
    "A": dict(fitset="all", s2=0.5, s3=0.25, alpha=0.03, objective="ls",
              transform="log0.001", extrapolation_rho=0.797099),
    "B": dict(fitset="trainonly", s2=1.0, s3=1.0, alpha=0.001, objective="ls",
              transform="log0.01", extrapolation_rho=0.777742),
}


def main():
    path, outdir = sys.argv[1], sys.argv[2]
    which = sys.argv[sys.argv.index("--config") + 1]
    cfg = SEALED[which]
    seeds = [1, 2, 3]
    if "--seeds" in sys.argv:
        seeds = [int(x) for x in sys.argv[sys.argv.index("--seeds") + 1].split(",")]
    tag_extra = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
    os.makedirs(outdir, exist_ok=True)

    sha, rows = G.load(path)
    print("data sha256:", sha, flush=True)
    print("config %s (SEALED, from PREREG section 2): %s" % (which, json.dumps(cfg)), flush=True)

    want = ("train", "validation") if cfg["fitset"] == "all" else ("train",)
    tr = [r for r in rows if r[SPLIT] in want]
    te = [r for r in rows if r[SPLIT] == "test"]
    counts = {}
    for r in rows:
        counts[r[SPLIT]] = counts.get(r[SPLIT], 0) + 1
    print("rows in file: %d ; %s column counts: %s" % (len(rows), SPLIT, counts), flush=True)
    print("fitset %s -> %d fitting rows ; %d test rows" % (cfg["fitset"], len(tr), len(te)),
          flush=True)

    Ctr, Cte = G.codes(tr), G.codes(te)
    ytr = G.scores(tr)                      # FITTING targets only - the only read of `score`
    m_trtr = G.match_counts(Ctr, Ctr)
    m_tetr = G.match_counts(Cte, Ctr)

    out = {}
    t0 = time.time()
    for seed in seeds:
        # Seed everything that is actually random in the pipeline.  With the configuration
        # given rather than selected, nothing below consumes these streams: the fit is
        # deterministic and the three files are expected to be identical (PREREG section 4).
        rng = np.random.default_rng(seed)
        _ = list(KFold(n_splits=5, shuffle=True, random_state=seed).split(Ctr))
        _ = rng.integers(0, 1000)

        Kfull = G.kernel(m_trtr, cfg["s2"], cfg["s3"])
        Kte = G.kernel(m_tetr, cfg["s2"], cfg["s3"])
        Kc, rm, gm = G.centre(Kfull)
        kte = G.centre_cross(Kte, rm, gm)
        y = G.transform(ytr, cfg["transform"])
        pred = y.mean() + kte @ G.ridge_dual(Kc, y - y.mean(), cfg["alpha"])
        del Kfull, Kte, Kc, kte

        tag = "%sconfig%s_%s_seed%d" % (tag_extra, which, cfg["fitset"], seed)
        pf = os.path.join(outdir, "pred_%s.csv" % tag)
        with open(pf, "w", newline="") as fh:
            fh.write("aa_seq,prediction\n")
            for r, p in zip(te, pred):
                fh.write("%s,%.10g\n" % (r["aa_seq"], p))
        with open(pf, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        out["seed%d" % seed] = dict(pred_file=os.path.basename(pf), sha256=h)
        print("  seed %d -> %s  sha256 %s  (%.1f s)"
              % (seed, os.path.basename(pf), h, time.time() - t0), flush=True)

    hs = sorted(set(v["sha256"] for v in out.values()))
    print("\nDETERMINISM CHECK: %d distinct prediction-file sha256 over %d seeds -> %s"
          % (len(hs), len(seeds), "IDENTICAL as pre-registered" if len(hs) == 1
             else "DIFFERENT - this is a bug, see PREREG section 9"), flush=True)
    with open(os.path.join(outdir, "fit_config%s%s.json" % (which, tag_extra)), "w") as fh:
        json.dump(dict(data_sha256=sha, split=SPLIT, config=which, sealed=cfg,
                       n_fit=len(tr), n_test=len(te), split_counts=counts,
                       seeds=out, identical_across_seeds=(len(hs) == 1)), fh, indent=2)


if __name__ == "__main__":
    main()
