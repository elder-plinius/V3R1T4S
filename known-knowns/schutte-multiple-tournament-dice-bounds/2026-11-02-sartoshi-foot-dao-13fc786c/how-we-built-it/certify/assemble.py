"""Assembles the certificate from certify/ledger.tsv (D-023). Usage (workspace root): venv-schutte/bin/python -I certify/assemble.py
For each cell, rebuilds every CNF of the tree (leaves and cover lemmas) with certlib, recomputes its sha256, and requires a
VERIFIED ledger row with that exact sha256. Prints, per cell, whether the cell is certified and which jobs are missing.
It trusts what README.md lists as trusted; it does not re-run any checker."""
import sys, os, hashlib, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certlib, driver
certlib.check_encoder()
leaves, covers = certlib.tree(driver.WS)
ok = {}
for r in driver.read_ledger():
    if r['verdict'] == 'VERIFIED': ok.setdefault(r['job'], set()).add(r['cnf_sha256'])
tmp = tempfile.mkdtemp(dir=driver.WORK)
miss = {c: [] for c in certlib.CELLS}; n = {c: 0 for c in certlib.CELLS}
def chk(cell, job, nv, cl):
    sha, _, _ = certlib.write_dimacs(os.path.join(tmp, 'x.cnf'), nv, cl); n[cell] += 1
    if sha not in ok.get(job, set()): miss[cell].append(job)
for cell, lv, p in covers:
    nv, cl, _ = certlib.cover_cnf(cell, lv, p); chk(cell, certlib.cover_id(cell, lv, p), nv, cl)
for cell, lv, p, _ in leaves:
    nv, cl, _ = certlib.leaf_cnf(cell, lv, p); chk(cell, certlib.leaf_id(cell, lv, p), nv, cl)
os.remove(os.path.join(tmp, 'x.cnf')); os.rmdir(tmp)
for cell in certlib.CELLS:
    print(f'{cell}: {n[cell]} jobs, {n[cell] - len(miss[cell])} VERIFIED with matching CNF sha256, missing {len(miss[cell])}: {miss[cell][:12]}')
    print(f'{cell}: ' + ('ALL LEAVES AND COVER LEMMAS VERIFIED BY cake_lpr' if not miss[cell] else 'NOT certified (see missing)'))
