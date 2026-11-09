"""usage: run_many.py OUT.jsonl NPROC FILE.json [FILE.json ...]  -> one json line per LC file (resumable: skips done files).
Applies pipeline.analyze() (frozen part) to each SNAD json; select() is applied later by the decision script."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")
import pipeline
from multiprocessing import Pool


def one(fn):
    try:
        d = json.load(open(fn))
        if not isinstance(d, dict): d = {}
    except Exception as ex:
        return {"file": fn, "error": repr(ex), "usable": False}
    r = pipeline.analyze(d); r["file"] = fn
    return r


if __name__ == "__main__":
    out, nproc, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["file"] for l in open(out)}
    todo = [f for f in files if f not in done]
    print("PID", os.getpid(), "todo", len(todo), flush=True); T0 = time.time()
    with Pool(nproc) as p, open(out, "a") as ck:
        for r in p.imap_unordered(one, todo):
            ck.write(json.dumps(r) + "\n"); ck.flush()
    print("done", len(todo), "in", round(time.time() - T0, 1), "s", flush=True)
