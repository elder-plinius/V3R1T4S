"""Optional (needs numpy, ase, torch, mace-torch): re-run the saved models on the official test structures and compare with the
predictions file. Test structures come from the public jarvis 'mlearn' dataset (fetched by fetch_sources.py, hash-checked)."""
import csv, io, json, os, sys, zipfile
import numpy as np, torch
from ase import Atoms
from mace.calculators import MACECalculator
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
src = json.load(open(os.path.join(here, 'sources.json')))
bench = json.load(zipfile.ZipFile(os.path.join(here, '_cache', 'benchmark.json.zip')).open(src['benchmark_member']))
allrec = {r['jid']: r for r in json.load(zipfile.ZipFile(os.path.join(here, '_cache', 'mlearn_figshare.zip')).open('mlearn.json'))}
torch.set_num_threads(int(os.environ.get('OMP_NUM_THREADS', '4')))
calcs = [MACECalculator(model_paths=os.path.join(pkg, m), device='cpu', default_dtype='float64') for m in src['models']]
rows = list(csv.reader(io.StringIO(open(os.path.join(pkg, src['predictions']), encoding='utf8').read())))
pred = {r[0]: np.array([float(x) for x in r[1].split(';')]) for r in rows[1:]}
worst = 0.0
for jid in bench['test']:
    at = allrec[jid]['atoms']; lat = np.array(at['lattice_mat'])
    pos = np.array(at['coords']) @ lat if at['cartesian'] is False else np.array(at['coords'])
    a = Atoms(at['elements'], positions=pos, cell=lat, pbc=True)
    f = np.mean([ (a.__setattr__('calc', c), a.get_forces())[1] for c in calcs ], axis=0)
    worst = max(worst, float(np.abs(f.ravel() - pred[jid]).max()))
print('max |re-run - predictions file| = %.3e eV/A over %d test structures' % (worst, len(bench['test'])))
print('PASS' if worst <= 1e-6 else 'FAIL')
sys.exit(0 if worst <= 1e-6 else 1)
