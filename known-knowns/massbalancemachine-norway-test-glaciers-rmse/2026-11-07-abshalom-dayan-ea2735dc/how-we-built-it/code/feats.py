"""Feature sets built only from allowed shipped columns (PREREG.md): FEATURES, month, n_months."""
import numpy as np
import mbdata

F = {c: i for i, c in enumerate(mbdata.FEATURES)}


def build(d, fs):
    X = d["X"]
    cols = [X]
    names = list(mbdata.FEATURES)
    if fs in ("F1", "F2", "F3"):
        # month position in the hydrological year (oct=0..sep=11) and season type
        cols += [d["month"][:, None].astype(float), d["n_months"][:, None].astype(float)]
        names += ["month", "n_months"]
    if fs in ("F2", "F3"):
        t = X[:, F["t2m"]] - 273.15 + 0.0065 * X[:, F["altitude_diff"]]  # fixed standard lapse rate to the stake
        tp = X[:, F["tp"]]
        cols += [t[:, None], np.maximum(t, 0)[:, None], (tp * (t < 1.0))[:, None],
                 (X[:, F["ssrd"]] * (1 - X[:, F["fal"]]))[:, None]]
        names += ["t_stake", "pdd_stake", "solid_tp", "abs_sw"]
    if fs == "F3":
        # aspect as sin/cos (aspect is in radians in the shipped CSV)
        cols += [np.sin(X[:, F["aspect"]])[:, None], np.cos(X[:, F["aspect"]])[:, None]]
        names += ["aspect_sin", "aspect_cos"]
    return np.hstack(cols), names
