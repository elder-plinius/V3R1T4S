"""predict.py MODEL.model XYZ OUT.npz : float64 force predictions for each structure in XYZ (labels never read)."""
import sys, numpy as np, torch
torch.set_num_threads(int(__import__('os').environ.get('OMP_NUM_THREADS','4')))
from ase.io import read
from mace.calculators import MACECalculator
def predict(model, xyz):
    calc = MACECalculator(model_paths=model, device='cpu', default_dtype='float64')
    out = {}
    for a in read(xyz, ':'):
        a.calc = calc
        out[a.info['jid']] = a.get_forces()
    return out
def mae_xyz(pred, xyz):
    ts = read(xyz, ':')
    e = np.concatenate([np.abs(pred[a.info['jid']] - a.arrays['REF_forces']).ravel() for a in ts])
    return float(e.mean())
if __name__ == '__main__':
    m, x, o = sys.argv[1:4]
    p = predict(m, x); np.savez(o, **p)
    print('val/xyz MAE', mae_xyz(p, x))
