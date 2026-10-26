"""Candidate hygiene (pitfall 3): raise the minimum layer-1 distance |maxpool(conv1(x)) - T1| (pre-BN units) while
keeping EVERY layer-1 pooled sign unchanged (so all deeper layers and the logits are unchanged). Greedy single-pixel
moves on the 2^-9 grid, strictly inside the box, restricted to the receptive field of the currently worst neuron.
numpy only (vnn venv), single image. Usage: robust_polish.py SIZE IDX X.npy OUT.npy [target_margin]"""
import sys, os, gzip
import numpy as np
import onnx
from onnx import numpy_helper
LENS = os.environ.get('LENS', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(LENS, 'in'))
import vnnspec
NETS = {48: '3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30',
        64: '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30'}
G = 2.0 ** -9
size, idx, xin, xout = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
target = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05
s = vnnspec.load(os.path.join(LENS, 'in/bench/model_%d_idx_%d_eps_1.00000.vnnlib.gz' % (size, idx)))
lo = s['lo'].reshape(size, size, 3).transpose(2, 0, 1); hi = s['hi'].reshape(size, size, 3).transpose(2, 0, 1)
m = onnx.load_from_string(gzip.decompress(open(os.path.join(LENS, 'in/bench/%s.onnx.gz' % NETS[size]), 'rb').read()))
W = {t.name: numpy_helper.to_array(t) for t in m.graph.initializer}
conv = [n for n in m.graph.node if n.op_type == 'Conv'][0]; bn = [n for n in m.graph.node if n.op_type == 'BatchNormalization'][0]
w1 = W[conv.input[1]].astype(np.float64)  # (32,3,5,5)
sc, B, mean, var = [W[i].astype(np.float64) for i in bn.input[1:]]
eps = [a.f for a in bn.attribute if a.name == 'epsilon'][0]
T1 = mean - B * np.sqrt(var + np.float64(np.float32(eps))) / sc
x = np.load(xin).astype(np.float64).reshape(size, size, 3).transpose(2, 0, 1).copy()
Ho = size - 4


def conv1(x):
    a = np.zeros((32, Ho, Ho))
    for c in range(3):
        for i in range(5):
            for j in range(5):
                a += w1[:, c, i, j][:, None, None] * x[c, i:i + Ho, j:j + Ho][None]
    return a


def pooled(x):
    a = conv1(x)
    p = a.reshape(32, Ho // 2, 2, Ho // 2, 2).max(axis=(2, 4))
    return a, p


a, p = pooled(x)
sign0 = p >= T1[:, None, None]
marg = np.abs(p - T1[:, None, None])
print('start min margin', marg.min(), 'n below target', int((marg < target).sum()), flush=True)
Hp = Ho // 2


def try_move(a, marg, cc, R, C, d):
    r_lo, r_hi = max(0, R - 4), min(Ho - 1, R); c_lo, c_hi = max(0, C - 4), min(Ho - 1, C)
    pr0, pr1, pc0, pc1 = r_lo // 2, r_hi // 2, c_lo // 2, c_hi // 2
    reg = a[:, 2 * pr0:2 * pr1 + 2, 2 * pc0:2 * pc1 + 2].copy()
    for r in range(r_lo, r_hi + 1):
        for c in range(c_lo, c_hi + 1):
            reg[:, r - 2 * pr0, c - 2 * pc0] += d * w1[:, cc, R - r, C - c]
    pr = reg.reshape(32, pr1 - pr0 + 1, 2, pc1 - pc0 + 1, 2).max(axis=(2, 4))
    if not np.array_equal(pr >= T1[:, None, None], sign0[:, pr0:pr1 + 1, pc0:pc1 + 1]):
        return None
    loc = np.abs(pr - T1[:, None, None])
    tmp = marg.copy(); tmp[:, pr0:pr1 + 1, pc0:pc1 + 1] = np.inf
    return min(tmp.min(), loc.min())


for it in range(2000):
    a, p = pooled(x)
    marg = np.abs(p - T1[:, None, None])
    k = np.unravel_index(np.argmin(marg), marg.shape)
    if marg[k] >= target:
        break
    ch, pr, pc = k
    active = bool(p[k] >= T1[ch])
    best = (marg.min(), None)
    for (r, c) in [(2 * pr + u, 2 * pc + v) for u in range(2) for v in range(2)]:
        if active and a[ch, r, c] != p[k]:
            continue
        if (not active) and a[ch, r, c] < T1[ch] - target:
            continue
        for cc in range(3):
            for i in range(5):
                for j in range(5):
                    w = w1[ch, cc, i, j]; dirn = w if active else -w
                    R, C = r + i, c + j
                    for st in (16, 64, 256):
                        xn = x[cc, R, C] + dirn * st * G
                        xn = min(max(xn, lo[cc, R, C] + G), hi[cc, R, C] - G)
                        if xn == x[cc, R, C]:
                            continue
                        mm = try_move(a, marg, cc, R, C, xn - x[cc, R, C])
                        if mm is not None and mm > best[0]:
                            best = (mm, (cc, R, C, xn))
    if best[1] is None:
        print('no improving move at iter', it, 'min margin', marg.min(), flush=True)
        break
    cc, rr, cl, xn = best[1]; x[cc, rr, cl] = xn
a, p = pooled(x)
marg = np.abs(p - T1[:, None, None])
assert np.array_equal(p >= T1[:, None, None], sign0)
assert np.all(x > lo) and np.all(x < hi) and np.all(np.round(x / G) * G == x)
print('final min margin', marg.min(), 'iters', it, flush=True)
np.save(xout, x.transpose(1, 2, 0))
