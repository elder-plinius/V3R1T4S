"""Load the shipped ML_MB_Norway monthly CSVs into numpy arrays (standard library csv + numpy only).

Allowed model inputs (PREREG.md): FEATURES below plus month and n_months. balance is the target only.
"""
import csv, hashlib, os
import numpy as np

RAW = os.environ.get("MBM_RAW", os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "mbm_raw"))
TRAIN_CSV = "src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf_monthly.csv"
TEST_CSV = "src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv"
SHA = {TRAIN_CSV: "19e10b018db4e291f4e9e99dcc908ca08a82ef25817b633a3b809b3b30200e94",
       TEST_CSV: "d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c"}
# MBM's feature order (its X columns before the 3 metadata columns)
FEATURES = ["altitude_diff", "aspect", "slope", "skyview_factor", "t2m", "sshf", "slhf", "ssrd", "fal", "str", "tp"]
MONTHS = ["oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
TEST_RGI = ["RGI60-08.00434", "RGI60-08.00449", "RGI60-08.01013", "RGI60-08.01026", "RGI60-08.01258",
            "RGI60-08.01286", "RGI60-08.01484", "RGI60-08.01598", "RGI60-08.02384", "RGI60-08.02650",
            "RGI60-08.02916", "RGI60-08.02918", "RGI60-08.02920", "RGI60-08.02969"]


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(which):
    """which: 'train' or 'test'. Returns dict of arrays, one entry per monthly row."""
    name = TRAIN_CSV if which == "train" else TEST_CSV
    path = os.path.join(RAW, name)
    assert _sha(path) == SHA[name], "input hash mismatch: " + name
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    d = {"X": np.array([[float(r[c]) for c in FEATURES] for r in rows], dtype=np.float64),
         "gid": np.array([int(r["id"]) for r in rows]),
         "n_months": np.array([int(r["n_months"]) for r in rows]),
         "month": np.array([MONTHS.index(r["month"]) for r in rows]),
         "balance": np.array([float(r["balance"]) for r in rows]),
         "rgi": np.array([r["RGIID"] for r in rows])}
    if which == "train":
        assert not set(d["rgi"]) & set(TEST_RGI), "test glacier in training file"
    else:
        assert set(d["rgi"]) == set(TEST_RGI)
    return d


def groups(d):
    """Unique point balances: returns (uid array, inverse index per row, season n_months per uid, obs per uid, rgi per uid)."""
    uid, inv = np.unique(d["gid"], return_inverse=True)
    nm = np.zeros(len(uid), int); obs = np.zeros(len(uid)); rgi = np.empty(len(uid), dtype=object)
    nm[inv] = d["n_months"]; obs[inv] = d["balance"]; rgi[inv] = d["rgi"]
    return uid, inv, nm, obs, rgi


def glacier_folds(d, k=6):
    """Fixed greedy assignment of training glaciers to k folds, balancing point-balance counts (largest first)."""
    uid, inv, nm, obs, rgi = groups(d)
    names, counts = np.unique(rgi.astype(str), return_counts=True)
    order = sorted(zip(names, counts), key=lambda t: (-t[1], t[0]))
    load_ = [0] * k; fold_of = {}
    for n, c in order:
        j = min(range(k), key=lambda i: (load_[i], i)); fold_of[n] = j; load_[j] += c
    return np.array([fold_of[r] for r in d["rgi"]]), fold_of
