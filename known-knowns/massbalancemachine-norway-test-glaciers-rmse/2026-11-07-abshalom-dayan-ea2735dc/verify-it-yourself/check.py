"""Standalone checker, written from the target's definition. Python 3 standard library only.

Run from the package folder:  python3 verify-it-yourself/check.py      (last line: PASS or FAIL)

What it checks, against verify-it-yourself/expected.json:
1. The shipped test CSV of github.com/khsjursen/ML_MB_Norway has the pinned sha256. It is taken from $MBM_TEST_CSV if
   set, else verify-it-yourself/cache/, else downloaded once from the repository (about 6 MB) into that cache.
2. Every object/ file has the sha256 listed in expected.json.
3. Point balances: one value per `id`; a point is annual, winter or summer by its n_months (12, 7, 5); the counts are
   1065 / 999 / 1028 as in the MBM paper.
4. The object's point predictions cover exactly the claimed points, and their RMSE against the observed balances
   equals the claimed values (to 5e-5 m w.e.).
5. For a linear winter model, the predictions are recomputed from the frozen coefficients and must agree (1e-9).
6. The named partial win holds at 2-decimal rounding against MBM's published 1.00 / 0.59 / 0.70.
"""
import csv, collections, decimal, hashlib, json, math, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
EXP = json.load(open(os.path.join(HERE, "expected.json")))
TEST_NAME = "Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv"
TEST_URL = "https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/main/src/" + TEST_NAME
TEST_SHA = "d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c"
SEASON = {"12": "Ba", "7": "Bw", "5": "Bs"}
N_EXPECTED = {"Ba": 1065, "Bw": 999, "Bs": 1028}
MBM_PUBLISHED = {"Ba": "1.00", "Bw": "0.59", "Bs": "0.70"}
fails = []


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)
    return ok


def r2(x):
    return decimal.Decimal(repr(x)).quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP)


def test_csv():
    if os.environ.get("MBM_TEST_CSV"):
        return os.environ["MBM_TEST_CSV"]
    cache = os.path.join(HERE, "cache", os.path.basename(TEST_NAME))
    if not os.path.isfile(cache):
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        print("downloading " + TEST_URL)
        try:
            urllib.request.urlretrieve(TEST_URL, cache)
        except Exception as e:  # e.g. a Python without CA certificates: use curl instead
            print("urllib failed (%r); trying curl" % (e,))
            if os.path.exists(cache):
                os.remove(cache)
            subprocess.run(["curl", "-sSfL", "-o", cache, TEST_URL], check=True)
    return cache


def main():
    path = test_csv()
    if not check(sha(path) == TEST_SHA, "test CSV sha256 is the pinned %s..." % TEST_SHA[:12]):
        return
    for rel, h in EXP["object_sha256"].items():
        p = os.path.join(PKG, rel)
        check(os.path.isfile(p) and sha(p) == h, "%s sha256 %s..." % (rel, h[:12]))
    by = collections.OrderedDict()
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            by.setdefault(r["id"], []).append(r)
    obs, season = {}, {}
    bad = 0
    for i, g in by.items():
        if len({x["n_months"] for x in g}) != 1 or len({x["balance"] for x in g}) != 1 or len(g) != int(g[0]["n_months"]):
            bad += 1
        obs[i] = float(g[0]["balance"])
        season[i] = SEASON.get(g[0]["n_months"])
    check(bad == 0, "every id has one n_months, one balance and n_months monthly rows (%d bad)" % bad)
    counts = collections.Counter(season.values())
    check(all(counts[s] == n for s, n in N_EXPECTED.items()),
          "point counts Ba %d, Bw %d, Bs %d (expected 1065 / 999 / 1028)" % (counts["Ba"], counts["Bw"], counts["Bs"]))
    pred = {}
    with open(os.path.join(PKG, EXP["predictions"]), newline="") as f:
        for r in csv.DictReader(f):
            if r["id"] in pred:
                check(False, "duplicate id %s in predictions" % r["id"])
            pred[r["id"]] = float(r["pred"])
    want = {i for i, s in season.items() if s in EXP["seasons"]}
    check(set(pred) == want, "predictions cover exactly the %d points of seasons %s (%d given)"
          % (len(want), "/".join(EXP["seasons"]), len(pred)))
    if EXP.get("linear_winter"):
        fz = json.load(open(os.path.join(PKG, EXP["linear_winter"])))
        a, b, c = fz["coef"]
        check(fz["phis"] == ["one", "solid", "solid_dz"] and len(fz["coef"]) <= 20, "frozen model: 3 coefficients (at most 20)")
        worst = 0.0
        for i in want:
            g = by[i]
            if [x["month"] for x in g] != ["oct", "nov", "dec", "jan", "feb", "mar", "apr"]:
                check(False, "winter point %s does not have the 7 months Oct-Apr" % i)
                continue
            p = 0.0
            for x in g:
                dz = float(x["altitude_diff"])
                t = float(x["t2m"]) - 273.15 + 0.0065 * dz
                tp = float(x["tp"]) * 1000
                s = tp if t < 1.0 else 0.0
                p += a + b * s + c * s * dz / 1000
            worst = max(worst, abs(p - pred.get(i, float("inf"))))
        check(worst < 1e-9, "predictions recomputed from the frozen coefficients agree (max diff %.2e)" % worst)
    got = {}
    for s in EXP["seasons"]:
        ids = [i for i in want if season[i] == s and i in pred]
        got[s] = math.sqrt(sum((pred[i] - obs[i]) ** 2 for i in ids) / len(ids))
        check(abs(got[s] - EXP["claimed_rmse"][s]) < 5e-5,
              "%s RMSE %.4f over %d points (claimed %.4f)" % (s, got[s], len(ids), EXP["claimed_rmse"][s]))
    if EXP["partial_win"] == "p1":
        r = {s: r2(got[s]) for s in got}
        m = {s: decimal.Decimal(v) for s, v in MBM_PUBLISHED.items()}
        check(set(r) == set(m) and any(r[s] < m[s] for s in m) and all(r[s] <= m[s] for s in m),
              "p1: 2-decimal %s vs MBM 1.00 / 0.59 / 0.70: one strictly lower, none higher"
              % " / ".join(str(r[s]) for s in ("Ba", "Bw", "Bs")))
    elif EXP["partial_win"] == "p2":
        check(got["Bw"] <= 0.59, "p2: Bw RMSE %.4f is at most 0.59 with at most 20 fitted parameters" % got["Bw"])
    else:
        check(False, "unknown partial win %s" % EXP["partial_win"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # any crash is a failure, never a pass
        check(False, "checker error: %r" % (e,))
    print("FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
