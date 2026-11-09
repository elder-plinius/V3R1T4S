"""usage: fetch_lcs_v3.py var|cst|gaia TARGET   (Line A2, run 2026-10-15-1739, calibrator-v3)
Copy of run-1643 calibrator-v2 code/fetch_lcs.py with ONLY these changes: (1) imports fetch_v3.get (1.0 s pacing);
(2) stop codes 401/403/405/429/503 or a 'Human Verification' page (run 1739 LENS_RULES); (3) for kind 'gaia' the
usable count starts at the number of usable CST controls in data/fetch_cst.tsv, so TARGET is the TOTAL number of
usable controls (PREREG Line A2: all CST first, Gaia top-up until >= 400 usable in total).
One honest GET per star (SNAD ZTF DB API v3, circle 1.5", UA "V3R1T4S-run (research; honest client)"), in draw
order, until TARGET stars have a USABLE LC (pipeline.bands rule: >= 50 good epochs in zg or zr for one ZTF object
within the cone). No retries. Other errors (timeouts, code -1, non-JSON) -> 'no usable LC (fetch error)', skipped.
Resumable: a draw whose file exists is not re-requested. Log: data/fetch_<kind>.tsv"""
import sys, os, json
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_v3 import get
import pipeline
kind, target = sys.argv[1], int(sys.argv[2])
df = pd.read_csv(f"data/{kind}_draw_order.csv")
ra, de = ("RA_full", "DE_full") if kind in ("var", "cst") else ("ra", "dec")
os.makedirs(f"data/lc_{kind}", exist_ok=True)
log = f"data/fetch_{kind}.tsv"
nuse = 0
if kind == "gaia" and os.path.exists("data/fetch_cst.tsv"):
    c0 = pd.read_csv("data/fetch_cst.tsv", sep="\t", names=["draw", "code", "bytes", "status", "url"]).drop_duplicates("draw", keep="last")
    nuse = int((c0.status == "usable").sum()); print("usable CST controls counted first:", nuse, flush=True)
done = set()
if os.path.exists(log):
    done = set(pd.read_csv(log, sep="\t", names=["draw", "code", "bytes", "status", "url"]).draw)
with open(log, "a") as L:
    for i in range(len(df)):
        r = df.iloc[i]; out = f"data/lc_{kind}/{i:04d}.json"
        url = f"https://db.ztf.snad.space/api/v3/data/latest/circle/full/json?ra={r[ra]}&dec={r[de]}&radius_arcsec=1.5"
        if os.path.exists(out):
            body = open(out, "rb").read(); c = "cached"
        else:
            c, body = get(url, out)
            if c in (401, 403, 405, 429, 503) or b"Human Verification" in body[:5000]:
                L.write(f"{i}\t{c}\t{len(body)}\tSTOP\t{url}\n"); print("STOP host", c, "PENDING TABLE CHECK", flush=True); break
        try:
            d = json.loads(body); d = d if isinstance(d, dict) else {}
            B = pipeline.bands(d); nmax = max([len(v[1]) for v in B.values()] or [0]); usable = nmax >= pipeline.NUSE
            st = "usable" if usable else ("no ZTF object within 1.5 arcsec" if not d else "no band with >= 50 good epochs")
        except Exception as ex:
            usable, st = False, f"no usable LC (fetch error: code {c})"
        nuse += usable
        if i not in done:
            L.write(f"{i}\t{c}\t{len(body)}\t{st}\t{url}\n"); L.flush()
        print(i, c, st, nuse, flush=True)
        if nuse >= target:
            print("reached", target, "usable at draw", i, flush=True); break
