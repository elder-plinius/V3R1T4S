"""Kit step 3c: reproduce the published RSV scores of arXiv 2605.16238 v2, Supplementary Table 6 (task set: 52
jurisdictions excluding US, horizons 0-3, reference dates 2026-01-03..2026-05-30, 4,576 tasks per eligible model),
from the CDCgov hub's model-output at commit e947ca8, with attempts/evaluator/code/wis.py, truth = pinned
oracle-output.parquet and, as a second view, the 2026-06-03 time-series vintage.
usage: python reproduce_era_table.py <hub dir>"""
import os, sys
import numpy as np, pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)  # claim copy: score_cdc.py and wis.py sit next to this file
import score_cdc as S  # noqa: E402

hub = sys.argv[1]
PUB = {"Google_SAI-RSVEns": (14.7, 21.2, 0.85), "RSVHub-ensemble": (16.4, 25.3, 0.87),
       "CEPH-Rtrend_rsv": (19.8, 28.4, 0.78), "RSVHub-baseline": (18.3, 27.8, 0.93)}
d = S.load_models(os.path.join(hub, "model-output"), models=list(PUB), window=("2026-01-03", "2026-05-30"))
W, ndrop = S.wide(d)
W = W[(W.location != "US") & (W.horizon.between(0, 3))]
truths = {"oracle e947ca8": S.load_truth(os.path.join(hub, "target-data", "oracle-output.parquet")),
          "time-series as_of 2026-06-03": S.truth_from_vintage(os.path.join(hub, "target-data", "time-series.parquet"), "2026-06-03")}
print("incomplete quantile sets dropped:", ndrop)
for tn, tr in truths.items():
    Sc = S.score_wide(W, tr)
    print("truth:", tn, " max |pinball - interval| = %.3g" % np.abs(Sc.wis - Sc.wis_int).max())
    for m in PUB:
        g = Sc[Sc.model_id == m]
        pw, pm, pc = PUB[m]
        tol = 0.05 + 0.02 * pw
        print("  %-20s tasks %5d dates %2d  mean WIS %7.3f (published %.1f, |diff| %.3f, tol %.3f: %s)  MAE %6.2f (pub %.1f)  cov95 %.3f (pub %.2f)"
              % (m, len(g), g.reference_date.nunique(), g.wis.mean(), pw, abs(g.wis.mean() - pw), tol,
                 "WITHIN" if abs(g.wis.mean() - pw) <= tol else "MISS", g.ae.mean(), pm, g.cov95.mean(), pc))
