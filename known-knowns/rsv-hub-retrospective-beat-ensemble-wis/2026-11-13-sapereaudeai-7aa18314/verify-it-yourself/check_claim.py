"""Standalone checker, written from the bank's definition (Python standard library + pyarrow to read the hub's parquet).

Definition checked (bank target rsv-hub-retrospective-beat-ensemble-wis, route (a), season 2024-25):
  season-average WIS of our quantile forecasts < hub-ensemble's season-average WIS, recomputed identically on every
  scored task of the hub-ensemble's own 2024-25 files, by >= 3% relative AND with the 95th percentile of a stationary
  bootstrap (mean block 3, over reference dates) of the relative difference below 0.
  WIS = mean over the 23 quantile levels of 2 x pinball loss (= scoringutils/hubverse WIS, weigh = TRUE, median once).
  Truth = HopkinsIDD/rsv-forecast-hub target-data/2026-06-05_rsvnet_hospitalization.csv, target "inc hosp";
  0-0.99 = 0-0.49 + 0.5-0.99, 1-4 = 1-1.99 + 2-4, 5-64 = 5-17 + 18-49 + 50-64 (missing if any part is missing);
  a task without truth is unscored for both.
Inputs: ../object/forecasts/*.csv (ours) and the hub files listed in pinned_inputs.txt, fetched from the pinned commit
(one GET each, User-Agent naming V3R1T4S) or read from --hub <local copy of the hub>; sha256 must match.
Last line: PASS or FAIL."""
import csv, hashlib, io, os, random, sys, urllib.request, glob, math

HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = "6bf251ac3fc798e55ed95d0b7269f5f5781c0207"
RAW = "https://raw.githubusercontent.com/HopkinsIDD/rsv-forecast-hub/%s/" % COMMIT
UA = "V3R1T4S-verify/1.0 (honest single request)"
LEVELS = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85,
          0.9, 0.95, 0.975, 0.99]
DERIVED = {"0-0.99": ["0-0.49", "0.5-0.99"], "1-4": ["1-1.99", "2-4"], "5-64": ["5-17", "18-49", "50-64"]}


def fail(msg):
    print("problem: " + msg)
    print("FAIL")
    sys.exit(1)


def get_bytes(path, hub):
    if hub:
        return open(os.path.join(hub, path), "rb").read()
    req = urllib.request.Request(RAW + path, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def wis(q, y):
    return sum(2.0 * ((1.0 if y < v else 0.0) - a) * (v - y) for a, v in zip(LEVELS, q)) / len(LEVELS)


def end_date(origin, h):
    import datetime as dt
    return (dt.date.fromisoformat(origin) + dt.timedelta(days=7 * int(h) - 1)).isoformat()


def main():
    hub = None
    if "--hub" in sys.argv:
        hub = sys.argv[sys.argv.index("--hub") + 1]
    pins = [l.split() for l in open(os.path.join(HERE, "pinned_inputs.txt")) if l.strip()]
    blobs = {}
    for h, p in pins:
        try:
            b = get_bytes(p, hub)
        except Exception as e:  # no retries
            fail("could not read %s (%s)" % (p, e))
        if hashlib.sha256(b).hexdigest() != h:
            fail("sha256 mismatch for %s" % p)
        blobs[p] = b
    # truth
    tp = [p for p in blobs if p.startswith("target-data/")][0]
    raw = {}
    for r in csv.DictReader(io.StringIO(blobs[tp].decode("utf-8"))):
        if r["target"] == "inc hosp" and r["value"] not in ("", "NA"):
            raw[(r["location"], r["age_group"], r["date"])] = float(r["value"])
    truth = dict(raw)
    keys = set((l, d) for (l, a, d) in raw)
    for g, comp in DERIVED.items():
        for (l, d) in keys:
            if all((l, c, d) in raw for c in comp):
                truth[(l, g, d)] = sum(raw[(l, c, d)] for c in comp)
    # hub-ensemble 2024-25 (parquet)
    import pyarrow.parquet as pq
    ens = {}
    for p, b in blobs.items():
        if not p.startswith("model-output/hub-ensemble/"):
            continue
        t = pq.read_table(io.BytesIO(b)).to_pylist()
        for r in t:
            if r["output_type"] != "quantile":
                continue
            o = str(r["origin_date"])[:10]
            k = (o, int(r["horizon"]), str(r["location"]), str(r["age_group"]))
            ens.setdefault(k, {})[round(float(r["output_type_id"]), 4)] = float(r["value"])
    # ours: the frozen files, byte-identical to the manifest
    ours = {}
    files = sorted(glob.glob(os.path.join(HERE, "..", "object", "forecasts", "*.csv")))
    if len(files) != 31:
        fail("expected 31 forecast files, found %d" % len(files))
    man = dict((l.split()[1].split("/")[-1], l.split()[0]) for l in open(os.path.join(HERE, "..", "object", "forecasts_sha256.txt")) if l.strip())
    for f in files:
        if man.get(os.path.basename(f)) != hashlib.sha256(open(f, "rb").read()).hexdigest():
            fail("object file differs from the frozen manifest: %s" % os.path.basename(f))
    for f in files:
        for r in csv.DictReader(open(f)):
            k = (r["origin_date"], int(r["horizon"]), r["location"], r["age_group"])
            ours.setdefault(k, {})[round(float(r["output_type_id"]), 4)] = float(r["value"])
    per = {}
    missing = 0
    n = 0
    for k, qd in ens.items():
        if len(qd) != 23:
            fail("ensemble task without 23 levels: %s" % (k,))
        y = truth.get((k[2], k[3], end_date(k[0], k[1])))
        if y is None:
            continue
        if k not in ours or len(ours[k]) != 23:
            missing += 1
            continue
        qe = [qd[round(a, 4)] for a in LEVELS]
        qo = [ours[k][round(a, 4)] for a in LEVELS]
        s = per.setdefault(k[0], [0.0, 0.0, 0])
        s[0] += wis(qo, y); s[1] += wis(qe, y); s[2] += 1
        n += 1
    if missing:
        fail("%d scored ensemble tasks have no forecast of ours" % missing)
    dates = sorted(per)
    A = [per[d][0] for d in dates]; B = [per[d][1] for d in dates]; N = [per[d][2] for d in dates]
    mo, me = sum(A) / sum(N), sum(B) / sum(N)
    rel = mo / me - 1
    rng = random.Random(12345)
    m = len(dates); rels = []
    for _ in range(4000):
        i = rng.randrange(m); sa = sb = 0.0
        for t in range(m):
            if t > 0:
                i = rng.randrange(m) if rng.random() < 1 / 3 else (i + 1) % m
            sa += A[i]; sb += B[i]
        rels.append(sa / sb - 1)
    rels.sort()
    lo, hi = rels[int(0.05 * len(rels))], rels[int(math.ceil(0.95 * len(rels))) - 1]
    print("scored tasks %d over %d reference dates" % (n, m))
    print("season-average WIS ours %.4f hub-ensemble %.4f relative %+.4f" % (mo, me, rel))
    print("stationary bootstrap (mean block 3, 4000 resamples) 90%% interval [%+.4f, %+.4f]" % (lo, hi))
    ok = rel <= -0.03 and hi < 0
    print("criterion: rel <= -0.03 and interval below 0 -> %s" % ok)
    print("PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
