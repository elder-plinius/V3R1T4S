"""Refit the 3-parameter winter model LW1 from the training CSV only (18 glaciers), check the coefficients equal the
frozen object/frozen_LW1.json, then predict every test winter point balance and print its RMSE (n must be 999).
Model: monthly f = b0 + b1*solid + b2*solid*dz/1000, summed over the 7 winter months (oct-apr) of each point, where
dz = altitude_diff (m, climate-cell minus stake altitude), t = t2m - 273.15 + 0.0065*dz (fixed lapse rate, deg C),
tp in mm/day (ERA5-Land tp * 1000), solid = tp if t < 1.0 else 0 (fixed threshold). Fitted by ordinary least squares.
Usage: python3 -I code/fit_and_score_LW1.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, mbdata, score
import cv_linear as L
fz = json.load(open(os.path.join(HERE, "..", "object", "frozen_LW1.json")))
tr = mbdata.load("train")  # asserts no test glacier in the training file
A, y, rgi = L.design(tr, fz["phis"], season=7)
b = L.fit(A, y)
print("training winter points:", len(y), "glaciers:", len(set(rgi)))
print("refit coef:", b.tolist()); print("frozen coef:", fz["coef"]); assert np.array_equal(b, np.array(fz["coef"]))
te = mbdata.load("test"); P = L.phis(te)
monthly = sum(c * P[n] for c, n in zip(fz["coef"], fz["phis"]))
w = te["n_months"] == 7
r = score.rmse_by_season(te["gid"][w], monthly[w], te["balance"][w], te["n_months"][w])
assert r["n_Bw"] == 999
print("TEST Bw RMSE %.4f (n=%d); 2-decimal %.2f; fitted parameters %d" % (r["Bw"], r["n_Bw"], r["Bw"], len(b)))
