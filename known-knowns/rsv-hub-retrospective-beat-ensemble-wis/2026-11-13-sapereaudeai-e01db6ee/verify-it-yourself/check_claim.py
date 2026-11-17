"""Standalone checker for the p3 package (written from the definition, separately from how-we-built-it/).

Definition used: the weighted interval score of a quantile forecast with the hub's 23 levels (Bracher et al. 2021, as
in scoringutils/hubEvals with the median counted once) equals the mean over the levels tau of 2 x pinball loss,
2 * (1{y < q_tau} - tau) * (q_tau - y). A model's season-average WIS is the mean over its scored tasks, one task =
(target, reference_date, location, horizon) with all 23 quantiles and an oracle value.

Inputs: the hub files listed in verify-it-yourself/pinned_inputs.txt (path, sha256) at commit
e947ca8fe8d50a581a181e6aefacfe922ba95af5 of github.com/CDCgov/rsv-forecast-hub, either from a local copy
(--hub DIR) or fetched one by one from raw.githubusercontent.com (one GET each, 1 s apart, no retries).
It also checks the reconciliation with the published row-level scores of github.com/sarahmart/epi-hub-analysis
(commit 2294a6331e6317059b49b20da893a86b2f0751dd; files in verify-it-yourself/pinned_published.txt, from a local folder
--ext DIR or fetched): every published row's hub forecast, rescored with the published truth_value, must equal the
published wis (|diff| <= 1e-6).
Added in the text-corrected version (run 2026-11-13-0349): the two other third-party score sets found for the season,
from a local folder (--ext2 DIR or EXT2) or fetched from the pinned URLs in verify-it-yourself/pinned_published2.txt:
- ACCIDDA/EpiBenchmark rsv25-26_complete-model-scores.parquet: every row's 5-level WIS (levels 0.025, 0.25, 0.5, 0.75,
  0.975, same pinball definition) of the hub forecast, with truth = the hub's target-data/time-series.parquet value at
  as_of 2026-09-16, must equal the published wis (|diff| <= 1e-6);
- ACCIDDA/tapestry B2-screen leaderboard.csv: each RSVHub-ensemble 2025-2026 cell (target x states+DC / US x horizon
  all/0-3) must equal the 23-level mean WIS with truth = time-series.parquet at as_of 2026-09-02, horizons 0-3, all
  2025-26 ensemble files, and, for the ED target, rows whose target_end_date is not reference_date + 7 x horizon left
  out (same n, relative |diff| <= 1e-9);
- ACCIDDA/tapestry B2-screen manifest.json (hub-evaluation.md): RSVHub-ensemble and UGA_flucast-INFLAenza season WIS on
  their common ensemble-defined units for both RSV targets (horizons 0-3, Puerto Rico out, rows whose target_end_date is
  not reference_date + 7 x horizon out, truth = time-series.parquet as_of 2026-09-02): same n, relative |diff| <= 1e-9;
- ACCIDDA/tapestry google-comparison (06508218): Google_SAI-RSVEns pooled WIS (per-seed.csv, native) and the 51
  per-location WIS sums of Google_SAI-RSVEns and RSVHub-ensemble (native-location-scores.csv, frozen_all, seed 42), on
  the hosp tasks both have (states+DC, horizons 0-3), truth as_of 2026-09-02: relative |diff| <= 1e-9.
Needs Python 3 with pandas and pyarrow (parquet files). Last line printed: PASS or FAIL.
"""
import argparse, csv, hashlib, os, sys, time, urllib.request

REF = "e947ca8fe8d50a581a181e6aefacfe922ba95af5"
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
LEV = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
       0.95, 0.975, 0.99]
PUBLISHED = {"Google_SAI-RSVEns": 14.7, "RSVHub-ensemble": 16.4, "CEPH-Rtrend_rsv": 19.8, "RSVHub-baseline": 18.3}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def get_inputs(hub):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "pinned_inputs.txt")) if l.strip()]
    if hub is None:
        hub = os.path.join(PKG, ".hub_cache")
        for path, _ in rows:
            out = os.path.join(hub, path)
            if os.path.isfile(out):
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            url = "https://raw.githubusercontent.com/CDCgov/rsv-forecast-hub/%s/%s" % (REF, path)
            req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-package-checker/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(out + ".part", "wb") as f:
                f.write(r.read())
            os.replace(out + ".part", out)
            time.sleep(1)
    bad = [p for p, h in rows if not os.path.isfile(os.path.join(hub, p)) or sha(os.path.join(hub, p)) != h]
    return hub, rows, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hub", default=os.environ.get("HUB"))
    ap.add_argument("--ext", default=os.environ.get("EXT"))
    ap.add_argument("--ext2", default=os.environ.get("EXT2"))
    a = ap.parse_args()
    import pandas as pd
    hub, rows, bad = get_inputs(a.hub)
    print("inputs: %d files, sha256 mismatches or missing: %d" % (len(rows), len(bad)))
    ok = not bad
    o = pd.read_parquet(os.path.join(hub, "target-data", "oracle-output.parquet"))
    o = o[o.output_type == "quantile"]
    truth = {}
    for t, l, d, v in zip(o.target, o.location.astype(str), pd.to_datetime(o.target_end_date).dt.strftime("%Y-%m-%d"), o.oracle_value):
        truth[(t, l if l == "US" else l.zfill(2), d)] = float(v)
    # accumulate per (target, model) and on the published subset
    acc, sub = {}, {}
    for path, _ in rows:
        if not path.startswith("model-output/"):
            continue
        model = path.split("/")[1]
        f = os.path.join(hub, path)
        d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype=str)
        d = d[d.output_type.astype(str) == "quantile"]
        q = {}
        for t, rd, l, h, ted, lev, v in zip(d.target.astype(str), pd.to_datetime(d.reference_date).dt.strftime("%Y-%m-%d"),
                                            d.location.astype(str), d.horizon.astype(int),
                                            pd.to_datetime(d.target_end_date).dt.strftime("%Y-%m-%d"),
                                            d.output_type_id.astype(float), d.value.astype(float)):
            l = l if l == "US" else l.zfill(2)
            q.setdefault((t, rd, l, h, ted), {})[round(lev, 4)] = v
        for (t, rd, l, h, ted), qs in q.items():
            if len(qs) != 23 or (t, l, ted) not in truth:
                continue
            y = truth[(t, l, ted)]
            w = sum(2 * ((1.0 if y < qs[round(tau, 4)] else 0.0) - tau) * (qs[round(tau, 4)] - y) for tau in LEV) / 23
            k = (t, model)
            s = acc.setdefault(k, [0, 0.0, 0.0])
            s[0] += 1; s[1] += w; s[2] += abs(y - qs[0.5])
            if t == "wk inc rsv hosp" and l != "US" and 0 <= h <= 3 and "2026-01-03" <= rd <= "2026-05-30":
                u = sub.setdefault(model, [0, 0.0, 0.0, 0.0, set()]); u[0] += 1; u[1] += w
                u[2] += abs(y - qs[0.5]); u[3] += 1.0 if qs[0.025] <= y <= qs[0.975] else 0.0; u[4].add(rd)
    tab = list(csv.DictReader(open(os.path.join(PKG, "object", "p3_table.csv"))))
    keys = set()
    for r in tab:
        k = (r["target"], r["model_id"]); keys.add(k)
        if k not in acc:
            print("FAIL row without recomputation:", k); ok = False; continue
        n, sw, sa = acc[k]
        good = n == int(r["n_tasks"]) and abs(sw / n - float(r["mean_wis"])) <= 1e-8 * max(1.0, abs(sw / n)) \
            and abs(sa / n - float(r["mae"])) <= 1e-8 * max(1.0, sa / n)
        print("%-27s %-28s tasks %5d mean WIS %.10g (table %s) %s" % (k[0], k[1], n, sw / n, r["mean_wis"], "ok" if good else "MISMATCH"))
        ok = ok and good
    missing = set(acc) - keys
    if missing:
        print("FAIL models with scored forecasts missing from the table:", sorted(missing)); ok = False
    for m, pub in PUBLISHED.items():
        n, sw = sub.get(m, [0, 0.0])[:2]
        good = n == 4576 and abs(sw / n - pub) <= 0.05 + 0.02 * pub
        print("published subset %-20s tasks %d mean WIS %.3f published %.1f %s" % (m, n, sw / n if n else float("nan"), pub, "ok" if good else "MISMATCH"))
        ok = ok and good
    # object/p3_era_subset.txt: every model line recomputed (tasks, dates, mean WIS, MAE, cov95 as printed)
    import re
    era = open(os.path.join(PKG, "object", "p3_era_subset.txt"), encoding="utf-8").read()
    lines = re.findall(r"^(\S+)\s+tasks\s+(\d+) dates\s+(\d+) mean WIS\s+([\d.]+) MAE\s+([\d.]+) cov95 ([\d.]+)$", era, re.M)
    bad_era = []
    for m, nt, nd, mw, ma, cv in lines:
        u = sub.get(m)
        mine = (str(u[0]), str(len(u[4])), "%.3f" % (u[1] / u[0]), "%.2f" % (u[2] / u[0]), "%.3f" % (u[3] / u[0])) if u else None
        if mine != (nt, nd, mw, ma, cv):
            bad_era.append((m, (nt, nd, mw, ma, cv), mine))
    good = len(lines) == len(sub) and not bad_era
    print("object/p3_era_subset.txt: %d model lines recomputed, %d mismatches %s" % (len(lines), len(bad_era), "ok" if good else "MISMATCH"))
    for b in bad_era:
        print("  era-subset MISMATCH", b)
    ok = ok and good
    exl = open(os.path.join(PKG, "object", "p3_exclusions.txt"), encoding="utf-8").read()
    cnts = dict(re.findall(r"^(wk inc rsv [a-z ]+?): (\d+) model tasks with quantiles", exl, re.M))
    tot = {}
    for (t, _m), v in acc.items():
        tot[t] = tot.get(t, 0) + v[0]
    good = bool(cnts) and all(int(cnts.get(t, -1)) == n for t, n in tot.items()) and len(cnts) == len(tot)
    print("object/p3_exclusions.txt: task counts %s vs recomputed %s %s" % (cnts, tot, "ok" if good else "MISMATCH"))
    ok = ok and good
    # reconciliation with the published row-level scores
    pubrows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "pinned_published.txt")) if l.strip()]
    ext = a.ext
    if ext is None:
        ext = os.path.join(PKG, ".ext_cache")
        os.makedirs(ext, exist_ok=True)
        for name, path, _ in pubrows:
            out = os.path.join(ext, name)
            if not os.path.isfile(out):
                url = "https://raw.githubusercontent.com/sarahmart/epi-hub-analysis/2294a6331e6317059b49b20da893a86b2f0751dd/" + path
                req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-package-checker/1.0"})
                with urllib.request.urlopen(req, timeout=120) as r, open(out + ".part", "wb") as f:
                    f.write(r.read())
                os.replace(out + ".part", out)
                time.sleep(1)
    badp = [n for n, _, h in pubrows if not os.path.isfile(os.path.join(ext, n)) or sha(os.path.join(ext, n)) != h]
    if badp:
        print("FAIL published files missing or sha256 mismatch:", badp); ok = False
    else:
        K2 = pd.read_parquet(os.path.join(ext, "scores.parquet"))
        fc = {}
        for path, _ in rows:
            m = path.split("/")[1] if path.startswith("model-output/") else None
            if m not in set(K2.model_id):
                continue
            f = os.path.join(hub, path)
            d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype=str)
            d = d[(d.output_type.astype(str) == "quantile") & (d.target.astype(str) == "wk inc rsv hosp")]
            for rd, l, h, ted, lev, v in zip(pd.to_datetime(d.reference_date).dt.strftime("%Y-%m-%d"), d.location.astype(str),
                                             d.horizon.astype(int), pd.to_datetime(d.target_end_date).dt.strftime("%Y-%m-%d"),
                                             d.output_type_id.astype(float), d.value.astype(float)):
                fc.setdefault((m, rd, l if l == "US" else l.zfill(2), h, ted), {})[round(lev, 4)] = v
        worst, n, miss = 0.0, 0, 0
        for m, rd, l, h, ted, y, w0 in zip(K2.model_id, pd.to_datetime(K2.reference_date).dt.strftime("%Y-%m-%d"), K2.location.astype(str),
                                           K2.horizon.astype(int), pd.to_datetime(K2.target_end_date).dt.strftime("%Y-%m-%d"),
                                           K2.truth_value.astype(float), K2.wis.astype(float)):
            qs = fc.get((m, rd, l, h, ted))
            if not qs or len(qs) != 23:
                miss += 1; continue
            w = sum(2 * ((1.0 if y < qs[round(tau, 4)] else 0.0) - tau) * (qs[round(tau, 4)] - y) for tau in LEV) / 23
            worst = max(worst, abs(w - w0)); n += 1
        good = miss == 0 and worst <= 1e-6
        print("published row-level scores: %d rows rescored with the published truth, %d without a hub forecast, max |diff| %.3g %s"
              % (n, miss, worst, "ok" if good else "MISMATCH"))
        ok = ok and good
    ok = check_ext2(a, hub, rows, pd) and ok
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def fetch_list(listfile, cache_name, folder):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, listfile)) if l.strip()]
    if folder is None:
        folder = os.path.join(PKG, cache_name)
        os.makedirs(folder, exist_ok=True)
        for name, url, _ in rows:
            out = os.path.join(folder, name)
            if not os.path.isfile(out):
                req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-package-checker/1.0"})
                with urllib.request.urlopen(req, timeout=120) as r, open(out + ".part", "wb") as f:
                    f.write(r.read())
                os.replace(out + ".part", out)
                time.sleep(1)
    bad = [n for n, _, h in rows if not os.path.isfile(os.path.join(folder, n)) or sha(os.path.join(folder, n)) != h]
    return folder, bad


def check_ext2(a, hub, rows, pd):
    import datetime
    ext2, bad = fetch_list("pinned_published2.txt", ".ext2_cache", a.ext2)
    if bad:
        print("FAIL third-party files (EpiBenchmark, tapestry) missing or sha256 mismatch:", bad)
        return False
    ts = pd.read_parquet(os.path.join(hub, "target-data", "time-series.parquet"))
    vint = {}
    for t, l, d, av, v in zip(ts.target, ts.location.astype(str), pd.to_datetime(ts.target_end_date).dt.strftime("%Y-%m-%d"),
                              pd.to_datetime(ts.as_of).dt.strftime("%Y-%m-%d"), ts.observation):
        if av in ("2026-09-16", "2026-09-02"):
            vint[(av, t, l if l == "US" else l.zfill(2), d)] = float(v)
    fc = {}
    for path, _ in rows:
        if not (path.startswith("model-output/RSVHub-ensemble/") or path.startswith("model-output/RSVHub-baseline/")
                or path.startswith("model-output/UGA_flucast-INFLAenza/") or path.startswith("model-output/Google_SAI-RSVEns/")):
            continue
        m = path.split("/")[1]
        f = os.path.join(hub, path)
        d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype=str)
        d = d[d.output_type.astype(str) == "quantile"]
        for t, rd, l, h, ted, lev, v in zip(d.target.astype(str), pd.to_datetime(d.reference_date).dt.strftime("%Y-%m-%d"),
                                            d.location.astype(str), d.horizon.astype(int),
                                            pd.to_datetime(d.target_end_date).dt.strftime("%Y-%m-%d"),
                                            d.output_type_id.astype(float), d.value.astype(float)):
            fc.setdefault((m, t, rd, l if l == "US" else l.zfill(2), h, ted), {})[round(lev, 4)] = v
    ok = True
    # EpiBenchmark: 5-level WIS, truth = time-series as_of 2026-09-16
    L5 = [0.025, 0.25, 0.5, 0.75, 0.975]
    E = pd.read_parquet(os.path.join(ext2, "rsv25-26_complete-model-scores.parquet"))
    worst, n, miss = 0.0, 0, 0
    for m, rd, ted, l, h, w0 in zip(E.model, E.reference_date.astype(str), E.target_end_date.astype(str),
                                    E.location.astype(str), E.horizon.astype(int), E.wis.astype(float)):
        l = l if l == "US" else l.zfill(2)
        qs = fc.get((m, "wk inc rsv hosp", rd, l, h, ted))
        y = vint.get(("2026-09-16", "wk inc rsv hosp", l, ted))
        if not qs or y is None:
            miss += 1
            continue
        w = sum(2 * ((1.0 if y < qs[tau] else 0.0) - tau) * (qs[tau] - y) for tau in L5) / 5
        worst = max(worst, abs(w - w0))
        n += 1
    good = miss == 0 and n == len(E) and worst <= 1e-6
    print("EpiBenchmark rows: %d rescored (5 levels, truth as_of 2026-09-16), %d unmatched, max |diff| %.3g %s"
          % (n, miss, worst, "ok" if good else "MISMATCH"))
    ok = ok and good
    # tapestry: RSVHub-ensemble cells, 23 levels, truth as_of 2026-09-02, ED date-consistent rows only
    T = list(csv.DictReader(open(os.path.join(ext2, "b2screen_leaderboard.csv"), encoding="utf-8")))
    T = [r for r in T if r["model"] == "RSVHub-ensemble" and r["season"] == "2025-2026" and "rsv" in r["target"]]
    cells = {}
    for (m, t, rd, l, h, ted), qs in fc.items():
        if m != "RSVHub-ensemble" or not (0 <= h <= 3) or l == "72" or len(qs) != 23:
            continue
        if t == "wk inc rsv prop ed visits":
            if (datetime.date.fromisoformat(rd) + datetime.timedelta(days=7 * h)).isoformat() != ted:
                continue
        y = vint.get(("2026-09-02", t, l, ted))
        if y is None:
            continue
        w = sum(2 * ((1.0 if y < qs[round(tau, 4)] else 0.0) - tau) * (qs[round(tau, 4)] - y) for tau in LEV) / 23
        g = "US" if l == "US" else "states_dc"
        for hk in ("all", str(h)):
            c = cells.setdefault((t, g, hk), [0, 0.0])
            c[0] += 1
            c[1] += w
    nt, worst = 0, 0.0
    for r in T:
        n0, s0 = cells.get((r["target"], r["geography"], r["horizon"]), [0, 0.0])
        rel = abs(s0 / n0 / float(r["wis"]) - 1) if n0 else float("inf")
        good = n0 == int(float(r["n"])) and rel <= 1e-9
        worst = max(worst, rel)
        nt += 1
        ok = ok and good
        if not good:
            print("tapestry cell MISMATCH", r["target"], r["geography"], r["horizon"], n0, r["n"], rel)
    good = nt == 20 and worst <= 1e-9
    print("tapestry RSVHub-ensemble cells: %d checked (23 levels, truth as_of 2026-09-02), max relative |diff| %.3g %s"
          % (nt, worst, "ok" if good else "MISMATCH"))
    ok = ok and good
    # tapestry hub-evaluation: ensemble and UGA on their common units
    import json
    man = json.load(open(os.path.join(ext2, "manifest.json"), encoding="utf-8"))
    nchk, worst2, good2 = 0, 0.0, True
    for c in man["cases"]:
        if c.get("hub") != "rsv" or c.get("season") != "2025-2026":
            continue
        t = c["target"]
        per = {}
        for (m, tt, rd, l, h, ted), qs in fc.items():
            if tt != t or m not in ("RSVHub-ensemble", "UGA_flucast-INFLAenza") or not (0 <= h <= 3) or l == "72" or len(qs) != 23:
                continue
            if (datetime.date.fromisoformat(rd) + datetime.timedelta(days=7 * h)).isoformat() != ted:
                continue
            y = vint.get(("2026-09-02", t, l, ted))
            if y is None:
                continue
            w = sum(2 * ((1.0 if y < qs[round(tau, 4)] else 0.0) - tau) * (qs[round(tau, 4)] - y) for tau in LEV) / 23
            per.setdefault(m, {})[(rd, l, h, ted)] = w
        common = set(per.get("RSVHub-ensemble", {})) & set(per.get("UGA_flucast-INFLAenza", {}))
        for srow in c["summary"]:
            m = srow["model"]
            if m not in per:
                continue
            vals = [per[m][k] for k in common]
            rel = abs(sum(vals) / len(vals) / srow["wis"] - 1) if vals else float("inf")
            g = len(vals) == int(srow["n"]) and rel <= 1e-9
            worst2 = max(worst2, rel)
            nchk += 1
            good2 = good2 and g
            if not g:
                print("tapestry hub-evaluation MISMATCH", t, m, len(vals), srow["n"], rel)
    good2 = good2 and nchk == 4
    print("tapestry hub-evaluation (RSVHub-ensemble, UGA_flucast-INFLAenza, both targets): %d values checked, max relative |diff| %.3g %s"
          % (nchk, worst2, "ok" if good2 else "MISMATCH"))
    # tapestry google-comparison
    T = "wk inc rsv hosp"
    per = {}
    for (m, tt, rd, l, h, ted), qs in fc.items():
        if tt != T or m not in ("Google_SAI-RSVEns", "RSVHub-ensemble") or not (0 <= h <= 3) or l in ("US", "72") or len(qs) != 23:
            continue
        y = vint.get(("2026-09-02", T, l, ted))
        if y is None:
            continue
        w = sum(2 * ((1.0 if y < qs[round(tau, 4)] else 0.0) - tau) * (qs[round(tau, 4)] - y) for tau in LEV) / 23
        per.setdefault(m, {})[(rd, l, h, ted)] = w
    common = set(per.get("Google_SAI-RSVEns", {})) & set(per.get("RSVHub-ensemble", {}))
    gvals = [per["Google_SAI-RSVEns"][k] for k in common]
    seeds = list(csv.DictReader(open(os.path.join(ext2, "per-seed.csv"), encoding="utf-8")))
    pooled = {float(r["pooled_google_wis"]) for r in seeds if r["target"] == T and r["scale"] == "native"}
    good3 = len(common) == 4692 and len(pooled) == 1 and abs(sum(gvals) / len(gvals) / pooled.pop() - 1) <= 1e-9
    nl = [r for r in csv.DictReader(open(os.path.join(ext2, "native-location-scores.csv"), encoding="utf-8"))
          if r["target"] == T and r["scope"] == "frozen_all" and r["seed"] == "42"]
    worst3 = 0.0
    for r in nl:
        loc = r["location"] if r["location"] == "US" else r["location"].zfill(2)
        for m, col in (("Google_SAI-RSVEns", "google"), ("RSVHub-ensemble", "ensemble")):
            sm = sum(per[m][k] for k in common if k[1] == loc)
            worst3 = max(worst3, abs(sm / float(r[col]) - 1))
    good3 = good3 and len(nl) == 51 and worst3 <= 1e-9
    print("tapestry google-comparison (pooled Google_SAI-RSVEns WIS on %d tasks, 51 x 2 per-location sums): max relative |diff| %.3g %s"
          % (len(common), worst3, "ok" if good3 else "MISMATCH"))
    return ok and good2 and good3


if __name__ == "__main__":
    sys.exit(main())
