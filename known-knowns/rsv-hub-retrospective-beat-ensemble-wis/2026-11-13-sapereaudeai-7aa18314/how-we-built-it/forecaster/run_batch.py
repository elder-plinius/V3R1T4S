"""Run dev_eval.py for every line (name<TAB>json) of a config file, N in parallel. usage: run_batch.py <tsv> <N>"""
import sys, subprocess, os
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
rows = [l.rstrip("\n").split("\t", 1) for l in open(sys.argv[1]) if l.strip()]
log = os.path.join(RUN, "attempts", "forecaster", "out", "batch.log")
def go(r):
    p = subprocess.run([sys.executable, "-W", "ignore", os.path.join(HERE, "dev_eval.py"), r[0], r[1]], cwd=RUN,
                       capture_output=True, text=True)
    with open(log, "a") as f:
        f.write((p.stdout or "") + (p.stderr[-2000:] if p.returncode else ""))
with ThreadPoolExecutor(int(sys.argv[2])) as ex:
    list(ex.map(go, rows))
with open(log, "a") as f:
    f.write("BATCH_DONE %s\n" % sys.argv[1])
