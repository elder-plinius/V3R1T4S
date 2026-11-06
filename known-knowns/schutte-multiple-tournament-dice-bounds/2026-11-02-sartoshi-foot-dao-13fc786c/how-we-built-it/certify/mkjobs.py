"""Writes certify/jobs.tsv (job, tier, prior_s) from the ledgers of runs 0844 and 1144 (certlib.tree).
The structural checks (every child CNF extends its parent; R_j regenerated exactly) run when the cover CNFs are built (validate.py). Usage (workspace root): venv-schutte/bin/python -I certify/mkjobs.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certlib
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
certlib.check_encoder()
leaves, covers = certlib.tree(WS)
rows = []
for cell, lv, p in covers:
    rows.append((certlib.cover_id(cell, lv, p), 'cover', 60.0 if lv == 1 else 5.0))
lr = []
for cell, lv, p, s in leaves:
    j = certlib.leaf_id(cell, lv, p)
    lr.append((j, 'hard', 7200.0) if s is None else (j, 'leaf', s))
rows += sorted([r for r in lr if r[1] == 'leaf'], key=lambda r: r[2]) + [r for r in lr if r[1] == 'hard']
assert len({r[0] for r in rows}) == len(rows)
with open(os.path.join(WS, 'certify', 'jobs.tsv'), 'w') as f:
    f.write('job\ttier\tprior_s\n')
    for r in rows: f.write(f'{r[0]}\t{r[1]}\t{r[2]}\n')
print('jobs', len(rows), 'covers', len(covers), 'leaves', len(leaves), 'hard', sum(r[1] == 'hard' for r in rows),
      'prior solver s', round(sum(r[2] for r in rows if r[1] == 'leaf')))
