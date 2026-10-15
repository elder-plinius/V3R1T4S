"""Compare the exact threshold model with onnxruntime logits at the box midpoint grid point (d=0) and random grid points."""
import sys, glob, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bnn4864 import Net, parse_box, ort_logits
D = sys.argv[1]
rng = np.random.default_rng(0)
for net_tag in ('48', '64'):
    onnx_path = glob.glob(f'{D}/onnx/3_{net_tag}_*.onnx.gz')[0]
    net = Net(onnx_path); S = net.S
    for vn in sorted(glob.glob(f'{D}/vnnlib/model_{net_tag}_*.vnnlib.gz')):
        lo, hi, tgt = parse_box(vn, (S, S, 3)); net.setup_box(lo, hi, 9)
        Ds = [np.zeros((S, S, 3))] + [rng.integers(net.dmin, net.dmax + 1) for _ in range(10)]
        # also random sparse perturbations near d=0
        for _ in range(10):
            d = np.zeros((S, S, 3)); mask = rng.random((S, S, 3)) < 0.05
            d[mask] = rng.integers(net.dmin, net.dmax + 1)[mask]; Ds.append(d)
        Ds = np.array(Ds)
        t = time.time(); o = net.forward(Ds); te = time.time() - t
        X = net.x_of(Ds).astype(np.float32)
        assert np.all(X.astype(np.float64) == net.x_of(Ds)) and np.all(X > lo) and np.all(X < hi)
        Lo, Yo = ort_logits(net.model, X)
        L = o['L']; diff = np.abs(L - Lo).max()
        g0 = L[0].copy(); g0[tgt] = -1e9
        mg = net.margins(Ds[:1])
        print(os.path.basename(vn), 'tgt', tgt, 'maxdiff', diff, 'centre gap', int(g0.max() - L[0, tgt]), 'cls', int(g0.argmax()),
              'unstable-K-range', 'eval_ms/pt %.1f' % (1000 * te / len(Ds)), 'margins', {k: round(v, 4) for k, v in mg.items()})
