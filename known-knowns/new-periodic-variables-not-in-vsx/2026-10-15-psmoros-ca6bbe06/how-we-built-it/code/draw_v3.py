"""Line A2 draws, run 2026-10-15-1739 (calibrator-v3). Adapted from run-1643 calibrator-v2 code/draw.py ONLY in the
seeds and pool constraints that run 1739 PREREG.md Line A2 states. usage: draw_v3.py var|cst|gaia|order
var : one VizieR TAP query of B/vsx/vsx: Type IN ('EW','EA','RRAB','DSCT'), DEJ2000 > -25, Period not null,
      13.5 <= max <= 19.0, MOD(OID,1000) = k (k = first call of default_rng(SEED_C).integers(0,1000); if k is run
      1407's slice 798 or run 1643's slice 718, the next call). Then VizieR ASU (OID lists) for F9.5 coordinates.
cst : one VizieR TAP query: Type = 'CST' AND ((13.5 <= max <= 19.0 AND -25 < DEJ2000 <= 0) OR (DEJ2000 > 0 AND
      ((13.0 <= max < 13.5) OR (19.0 < max <= 19.5)))), then ASU F9.5 coordinates.
gaia: one Gaia TAP query: gaia_source G 13.5-19, dec > -25, not in vari_summary, phot_variable_flag != 'VARIABLE',
      random_index >= start (start = first call of default_rng(SEED_C+2).integers(0, 10**9)), ORDER BY random_index;
      bounded to [start, start + W) as run 1643 did after its HTTP 408 (the bounded window is an exact prefix of the
      unbounded order as long as fewer rows than the window holds are processed; checked in 'order').
order: var pool sorted by OID, permuted by the same rng's next call, then OIDs drawn in runs 1407/1643 removed;
      CST pool sorted by OID, permuted by default_rng(SEED_C+1), CST used in runs 1407/1643 removed;
      Gaia pool in random_index order, runs 1407/1643 Gaia controls removed.
"""
import sys, os, io, urllib.parse, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_v3 import get
SEED_C = 20261020
R = "<WORKDIR>/runs"
rng = np.random.default_rng(SEED_C)
k_var = int(rng.integers(0, 1000)); k_first = k_var
while k_var in (798, 718):  # run 1407's slice 798, run 1643's slice 718
    k_var = int(rng.integers(0, 1000))
TAP = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY="
cols = '"OID","Name","RAJ2000","DEJ2000","Type","max","n_max","min","Period"'
qv = (f'SELECT {cols} FROM "B/vsx/vsx" WHERE "Type" IN (\'EW\',\'EA\',\'RRAB\',\'DSCT\') AND "DEJ2000">-25 '
      f'AND "Period" IS NOT NULL AND "max">=13.5 AND "max"<=19.0 AND MOD("OID",1000)={k_var}')
qc = (f'SELECT {cols} FROM "B/vsx/vsx" WHERE "Type"=\'CST\' AND ((("max">=13.5 AND "max"<=19.0) AND "DEJ2000">-25 '
      f'AND "DEJ2000"<=0) OR ("DEJ2000">0 AND (("max">=13.0 AND "max"<13.5) OR ("max">19.0 AND "max"<=19.5))))')
ASU = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=B/vsx/vsx&-out=OID,RAJ2000,DEJ2000&-out.max=unlimited&OID="
W = 8000


def asu_coords(oids, out):
    rows = []
    for j in range(0, len(oids), 300):
        part = oids[j:j + 300]
        c, b = get(ASU + urllib.parse.quote(",".join(str(o) for o in part)), f"{out}.{j // 300}.tsv")
        print("asu", c, len(b), flush=True)
        if c != 200: raise SystemExit(f"ASU code {c}: stop, PENDING TABLE CHECK")
        lines = [l for l in b.decode().splitlines() if l and not l.startswith("#")]
        for l in lines[3:]:
            f = l.split("\t")
            rows.append((int(f[0]), float(f[1]), float(f[2])))
    return pd.DataFrame(rows, columns=["OID", "RA_full", "DE_full"])


mode = sys.argv[1]
os.makedirs("data", exist_ok=True)
print("SEED_C", SEED_C, "k first call", k_first, "k used", k_var, flush=True)
if mode in ("var", "cst"):
    q = qv if mode == "var" else qc
    print(q, flush=True)
    c, b = get(TAP + urllib.parse.quote(q), f"data/vsx_{mode}_pool_tap.csv"); print("tap", c, len(b))
    if c != 200: raise SystemExit("stop")
    p = pd.read_csv(io.BytesIO(b))
    co = asu_coords(sorted(p.OID.tolist()), f"data/vsx_{mode}_asu")
    p = p.merge(co, on="OID", how="left")
    print("pool", len(p), "missing full coords", int(p.RA_full.isna().sum()))
    p.to_csv(f"data/vsx_{mode}_pool.csv", index=False)
elif mode == "gaia":
    start = int(np.random.default_rng(SEED_C + 2).integers(0, 10**9))
    q = ("SELECT g.source_id, g.ra, g.dec, g.phot_g_mean_mag, g.phot_variable_flag, g.random_index "
         "FROM gaiadr3.gaia_source AS g LEFT OUTER JOIN gaiadr3.vari_summary AS v ON g.source_id = v.source_id "
         f"WHERE g.random_index >= {start} AND g.random_index < {start + W} AND g.dec > -25 AND g.phot_g_mean_mag BETWEEN 13.5 AND 19.0 "
         "AND v.source_id IS NULL AND g.phot_variable_flag != 'VARIABLE' ORDER BY g.random_index")
    print("start", start, q, flush=True)
    url = "https://gea.esac.esa.int/tap-server/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=" + urllib.parse.quote(q)
    c, b = get(url, "data/gaia_pool.csv", timeout=600); print("gaia", c, len(b))
elif mode == "order":
    old_var = set(pd.read_csv(f"{R}/2026-10-15-1407/attempts/calibrator/data/var_draw_order.csv").OID) | \
              set(pd.read_csv(f"{R}/2026-10-15-1643/attempts/calibrator-v2/data/var_draw_order.csv").OID) | \
              set(pd.read_csv(f"{R}/2026-10-15-1643/attempts/calibrator-v2/data/vsx_var_pool.csv").OID)
    old_cst = set(pd.read_csv(f"{R}/2026-10-15-1407/attempts/calibrator/data/cst_draw_order.csv").OID) | \
              set(pd.read_csv(f"{R}/2026-10-15-1407/attempts/calibrator-null400/data/cst_draw_order.csv").OID) | \
              set(pd.read_csv(f"{R}/2026-10-15-1643/attempts/calibrator-v2/data/vsx_cst_pool.csv").OID)
    old_gaia = set(pd.read_csv(f"{R}/2026-10-15-1407/attempts/calibrator-null400/data/gaia_controls.csv").source_id) | \
               set(pd.read_csv(f"{R}/2026-10-15-1643/attempts/calibrator-v2/data/gaia_draw_order.csv").source_id)
    v = pd.read_csv("data/vsx_var_pool.csv").sort_values("OID").reset_index(drop=True)
    perm = rng.permutation(len(v))           # next call of the same rng
    v = v.iloc[perm].reset_index(drop=True)
    print("k_var", k_var, "pool", len(v), "excluded (drawn in 1407/1643)", int(v.OID.isin(old_var).sum()))
    v = v[~v.OID.isin(old_var)].reset_index(drop=True)
    v.to_csv("data/var_draw_order.csv", index_label="draw")
    cc = pd.read_csv("data/vsx_cst_pool.csv").sort_values("OID").reset_index(drop=True)
    cc = cc.iloc[np.random.default_rng(SEED_C + 1).permutation(len(cc))].reset_index(drop=True)
    print("cst pool", len(cc), "used in 1407/1643", int(cc.OID.isin(old_cst).sum()))
    cc = cc[~cc.OID.isin(old_cst)].reset_index(drop=True)
    cc.to_csv("data/cst_draw_order.csv", index_label="draw")
    g = pd.read_csv("data/gaia_pool.csv", dtype={"source_id": "int64"}).sort_values("random_index")
    print("gaia pool", len(g), "in 1407/1643", int(g.source_id.isin(old_gaia).sum()))
    g = g[~g.source_id.isin(old_gaia)].reset_index(drop=True)
    g.to_csv("data/gaia_draw_order.csv", index_label="draw")
    print("var types", v.Type.str.strip().value_counts().to_dict(), "cst", len(cc), "gaia", len(g))
