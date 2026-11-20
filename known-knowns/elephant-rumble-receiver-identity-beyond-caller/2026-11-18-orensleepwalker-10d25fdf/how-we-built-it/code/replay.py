"""Replay saved outputs exactly with the frozen programs (written after the results, for reviewers).
Usage: python3 code/replay.py <real|context|null_pa|null_rf> <index> [<index> ...]
Each index is recomputed into a temporary folder by the frozen program's own function and compared byte for byte
with the saved file in output/<kind>/."""
import sys, os, tempfile, filecmp, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MOD = {'real': ('run_real', 'draw_%03d.json'), 'context': ('context_check', 'draw_%03d.json'),
       'null_pa': ('null_pa', 'rerun_%04d.json'), 'null_rf': ('null_rf', 'rerun_%04d.json')}
kind = sys.argv[1]; name, pat = MOD[kind]; m = importlib.import_module(name)
ok = True
with tempfile.TemporaryDirectory() as t:
    m.OUT = t
    for a in sys.argv[2:]:
        i = int(a); m.one(i)
        same = filecmp.cmp(os.path.join(t, pat % i), os.path.join(HERE, '..', 'output', kind, pat % i), shallow=False)
        ok &= same; print(kind, i, 'IDENTICAL' if same else 'DIFFERENT')
print('ALL IDENTICAL' if ok else 'MISMATCH'); sys.exit(0 if ok else 1)
