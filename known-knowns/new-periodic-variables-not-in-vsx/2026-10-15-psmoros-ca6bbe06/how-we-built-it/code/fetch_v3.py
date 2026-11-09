"""Honest single GET with logging (copy of run-1643 calibrator-v2 code/fetch.py; ONLY change: pacing 0.6 s -> 1.0 s
after every request, as run 1739 LENS_RULES require >= 1 s per host). usage: fetch_v3.py URL OUTFILE"""
import sys, time, urllib.request, urllib.error, datetime, json, os
UA = "V3R1T4S-run (research; honest client)"
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fetch_log.tsv")
def get(url, out, timeout=60):
    t0 = datetime.datetime.utcnow().isoformat()+"Z"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(); code = r.status
    except urllib.error.HTTPError as e:
        body = e.read(); code = e.code
    except Exception as e:
        body = repr(e).encode(); code = -1
    with open(out, "wb") as f: f.write(body)
    with open(LOG, "a") as f: f.write(f"{t0}\t{code}\t{len(body)}\t{url}\t{out}\n")
    time.sleep(1.0)
    return code, body
if __name__ == "__main__":
    c, b = get(sys.argv[1], sys.argv[2])
    print(c, len(b)); print(b[:800].decode("utf-8", "replace"))
