"""Run the random-start search over the lane slice with a process pool; append results to results.jsonl."""
import json, os, sys
from multiprocessing import Pool
os.environ["OMP_NUM_THREADS"] = "1"
from search import run_cell
HERE = os.path.dirname(os.path.abspath(__file__))

def budget(r):
    if r["creator"] == "AUTO":
        return 30.0
    return float(min(40 + 0.7 * r["d"] * r["n"], 200))

def job(r):
    try:
        res = run_cell(r["d"], r["n"], r["best"], budget(r), seed=int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    except Exception as e:
        res = dict(d=r["d"], n=r["n"], table=r["best"], error=repr(e))
    with open(os.path.join(HERE, "results.jsonl"), "a") as f:
        f.write(json.dumps(res) + "\n")
    return res

if __name__ == "__main__":
    cells = json.load(open(os.path.join(HERE, "slice.json")))
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    done = set()
    if os.path.exists(os.path.join(HERE, "results.jsonl")):
        done = {(r["d"], r["n"]) for r in map(json.loads, open(os.path.join(HERE, "results.jsonl")))}
    cells = [r for r in cells if (r["d"], r["n"]) not in done]
    cells.sort(key=lambda r: -budget(r))
    print(sum(budget(r) for r in cells) / nproc / 3600, "h estimated")
    with Pool(nproc) as p:
        for res in p.imap_unordered(job, cells):
            print(json.dumps(res), flush=True)
