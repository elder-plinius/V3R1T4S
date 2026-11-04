"""Loader for JARVIS mlearn force tasks. Test labels are only read by evaluate()."""
import json, zipfile, numpy as np
CACHE = 'data_cache'
def bench(el):
    z = zipfile.ZipFile(f'{CACHE}/mlearn_{el}_forces.json.zip')
    return json.load(z.open(f'mlearn_{el}_forces.json'))
_all = None
def allrec():
    global _all
    if _all is None:
        _all = {r['jid']: r for r in json.load(open(f'{CACHE}/mlearn_all.json'))}
    return _all
def parse(s): return np.array(s.split(';'), float)
def structs(el, split):
    """list of (jid, lattice(3,3), frac/cart positions(N,3), species list, forces(N,3) or None)"""
    b = bench(el)[split]; a = allrec(); out = []
    for jid, fs in b.items():
        at = a[jid]['atoms']
        lat = np.array(at['lattice_mat'], float); xyz = np.array(at['coords'], float)
        pos = xyz @ lat if at.get('cartesian') is False else xyz
        f = parse(fs).reshape(-1, 3)
        out.append(dict(jid=jid, cell=lat, pos=pos, z=at['elements'], f=f, e=float(a[jid]['energy'])))
    return out
def mae(pred, truth):
    return float(np.mean(np.abs(np.concatenate([p.ravel() for p in pred]) - np.concatenate([t.ravel() for t in truth]))))
