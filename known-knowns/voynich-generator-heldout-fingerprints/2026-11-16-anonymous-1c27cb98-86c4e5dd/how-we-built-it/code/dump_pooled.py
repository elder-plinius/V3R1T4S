import sys, os, json, time
ROOT=os.environ.get('RUN_ROOT', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT,'code'))
# default RUN_ROOT = the run folder that contains this how-we-built-it/ (run's data/ + code/). Override via env RUN_ROOT.
from naibbe_run import gen_run, PTEXTS, SEEDS
# Pool per mode as TEMPLATE-WRAPPED LINES (space-joined tokens, one wrapped line per row),
# matching how run_naibbe_batch.py computed the pooled H1 (sg.score_all over concatenated rr['lines']).
for mode in ('A','B'):
    wrapped=[]
    for pname in sorted(PTEXTS):
        if PTEXTS[pname]['dialect']!=mode: continue
        for seed in SEEDS:
            wrapped.extend(gen_run(pname, seed)['lines'])
    OUT=os.environ.get('POOL_OUT', os.path.join(ROOT,'output')); os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f'pooled_{mode}.wrapped.txt'),'w') as f:
        f.write('\n'.join(' '.join(w) for w in wrapped))
    print(mode, len(wrapped), "wrapped lines ->", os.path.join(OUT, f'pooled_{mode}.wrapped.txt'), flush=True)
