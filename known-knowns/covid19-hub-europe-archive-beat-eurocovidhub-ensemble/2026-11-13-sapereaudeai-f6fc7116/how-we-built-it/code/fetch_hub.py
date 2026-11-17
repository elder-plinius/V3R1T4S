"""Honest, logged, single-request fetcher for hub DATA files (no retries; stop the route on 401/403/429/503).
Checks Content-Length before reading (skips > 200 MB); streams to a .part file then renames.
Usage: python -I fetch_hub.py <list.tsv> <outdir> <logfile> [sleep_s]
list.tsv lines: <relative_out_path>\t<url>"""
import sys, os, time, urllib.request, urllib.error, hashlib, datetime
UA = "V3R1T4S-research-agent (honest single requests; forecast-scoring reproduction)"
lst, outdir, logf = sys.argv[1], sys.argv[2], sys.argv[3]
slp = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
items = [l.rstrip("\n").split("\t") for l in open(lst, encoding="utf-8") if l.strip()]
log = open(logf, "a", encoding="utf-8")
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for rel, url in items:
    dst = os.path.join(outdir, rel)
    if os.path.exists(dst):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            cl = r.headers.get("Content-Length")
            if cl is not None and int(cl) > 200 * 1024 * 1024:
                log.write(f"{now()}\tSKIP_TOO_BIG\t{cl}\t{url}\n"); log.flush(); continue
            h = hashlib.sha256(); n = 0
            tmp = dst + ".part"
            with open(tmp, "wb") as f:
                while True:
                    b = r.read(1 << 16)
                    if not b: break
                    f.write(b); h.update(b); n += len(b)
            os.replace(tmp, dst)
            log.write(f"{now()}\t{r.status}\t{n}\t{h.hexdigest()}\t{url}\n")
    except urllib.error.HTTPError as e:
        log.write(f"{now()}\tHTTP{e.code}\t{url}\n"); log.flush()
        if e.code in (401, 403, 429, 503):
            log.write(f"{now()}\tSTOP_ROUTE\n"); break
    except Exception as e:
        log.write(f"{now()}\tERR {type(e).__name__}: {e}\t{url}\n")
    log.flush()
    time.sleep(slp)
log.write(f"{now()}\tDONE\n"); log.close()
