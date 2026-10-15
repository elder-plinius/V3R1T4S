"""Exact threshold model of the VNN-COMP 2026 traffic_signs_recognition_2023 binarized 48x48 and 64x64 networks.

Graph (48 net): NHWC x -> Conv1 32x3x5x5 (+-1) -> MaxPool2 -> BN -> [Sign, +0.1, Sign] -> Conv2 64x32x5x5 (+-1)
-> MaxPool2 -> BN -> sign -> Conv3 64x64x3x3 (BN folded: real weights + bias) -> sign -> flatten NHWC
-> MatMul (+-1) -> Mul/Add (BN) -> sign -> MatMul (+-1) -> Softmax.   64 net: MaxPool2 after Conv3, Dense 1600x1024.
[Sign, +0.1, Sign] means h = +1 iff the BN output >= 0.

Search space (as in the V3R1T4S 3_30_30 work, bnn.py): x = v + off + m*d, v = floor((lo+hi)/2), integer
d in [lo-v, hi-v], m = 1 - 2^-pw, off = +-2^-(pw+1) only where v sits on a clipped bound.  Then the conv1 output is
a1 = C0 + m*K with C0 = w.(v+off) fixed and K = w.d an integer, so every conv1 BN decision is an integer test on K.
Later layers: integer tests on +-1 sums (conv2, dense1) and a real-weighted sum (conv3) evaluated in float64.
`margins()` reports the distance of every decision to its real threshold so near-ties can be rejected.
"""
from __future__ import annotations
import gzip, io, re
import numpy as np
import onnx
from onnx import numpy_helper


def load_onnx(path):
    data = gzip.open(path).read() if path.endswith('.gz') else open(path, 'rb').read()
    return onnx.load(io.BytesIO(data))


def parse_box(path, shape):
    txt = gzip.open(path).read().decode() if path.endswith('.gz') else open(path).read()
    lo = np.full(shape, np.nan); hi = np.full(shape, np.nan)
    pat = r'\(assert \((<=|>=) X\[0,(\d+),(\d+),(\d+)\] ([-0-9.eE]+)\)\)'
    for mm in re.finditer(pat, txt):
        a = (int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
        (hi if mm.group(1) == '<=' else lo)[a] = float(mm.group(5))
    assert not np.isnan(lo).any() and not np.isnan(hi).any()
    tg = set(int(t) for t in re.findall(r'\(>= Y\[0,\d+\] Y\[0,(\d+)\]\)', txt))
    assert len(tg) == 1
    return lo, hi, tg.pop()


def pixel_map(lo, hi, pw=9):
    lo = np.asarray(lo, np.float64); hi = np.asarray(hi, np.float64)
    assert np.all(lo == np.round(lo)) and np.all(hi == np.round(hi)) and np.all(hi > lo)
    v = np.floor((lo + hi) / 2)
    m = 1.0 - 2.0 ** -pw
    off = np.where(v == lo, 2.0 ** -(pw + 1), np.where(v == hi, -2.0 ** -(pw + 1), 0.0))
    dmin = (lo - v).astype(np.int64); dmax = (hi - v).astype(np.int64)
    assert np.all(v + off + m * dmin > lo) and np.all(v + off + m * dmax < hi)
    return v, off, m, dmin, dmax


def im2col(x, k):
    """x: (B,H,W,C) -> (B,H-k+1,W-k+1,k*k*C) with patch order (i,j,c)."""
    B, H, W, C = x.shape
    Ho, Wo = H - k + 1, W - k + 1
    cols = np.empty((B, Ho, Wo, k, k, C), dtype=x.dtype)
    for i in range(k):
        for j in range(k):
            cols[:, :, :, i, j, :] = x[:, i:i + Ho, j:j + Wo, :]
    return cols.reshape(B, Ho, Wo, k * k * C)


def wmat(w):
    """ONNX conv weight (O,C,kh,kw) -> (kh*kw*C, O) matching im2col order."""
    return w.transpose(2, 3, 1, 0).reshape(-1, w.shape[0])


def pool2(a):
    B, H, W, C = a.shape
    return a[:, :H // 2 * 2, :W // 2 * 2, :].reshape(B, H // 2, 2, W // 2, 2, C).max(axis=(2, 4))


class Net:
    def __init__(self, onnx_path):
        m = load_onnx(onnx_path)
        self.model = m
        I = {t.name: numpy_helper.to_array(t) for t in m.graph.initializer}
        nodes = list(m.graph.node)
        convs = [n for n in nodes if n.op_type == 'Conv']
        bns = [n for n in nodes if n.op_type == 'BatchNormalization']
        mms = [n for n in nodes if n.op_type == 'MatMul']
        self.big = any(n.op_type == 'MaxPool' for n in nodes[nodes.index(convs[2]):])
        self.S = 64 if self.big else 48
        self.w1 = I[convs[0].input[1]].astype(np.float64)
        self.w2 = I[convs[1].input[1]].astype(np.float64)
        self.w3 = I[convs[2].input[1]].astype(np.float64)
        self.b3 = I[convs[2].input[2]].astype(np.float64) if len(convs[2].input) > 2 else None
        self.d1 = I[mms[0].input[1]].astype(np.float64)
        self.d2 = I[mms[1].input[1]].astype(np.float64)
        for w in (self.w1, self.w2, self.d1, self.d2):
            assert set(np.unique(w)) <= {-1.0, 1.0}
        def bnp(n):
            sc, b, mu, var = (I[n.input[i]].astype(np.float64) for i in range(1, 5))
            eps = [a.f for a in n.attribute if a.name == 'epsilon'][0]
            s = np.sqrt(var + np.float64(np.float32(eps)))
            return sc, b, mu, s
        self.bn1 = bnp(bns[0]); self.bn2 = bnp(bns[1])
        mul = [n for n in nodes if n.op_type == 'Mul'][0]; add = [n for n in nodes if n.op_type == 'Add' and n.input[0] == mul.output[0]][0]
        self.dmul = I[mul.input[1]].astype(np.float64); self.dadd = I[add.input[1]].astype(np.float64)
        # thresholds: h=+1 iff BN(x) >= 0  <=>  sc*(x-mu)/s + b >= 0
        sc, b, mu, s = self.bn1
        assert np.all(sc != 0)
        self.T1 = mu - b * s / sc; self.pos1 = sc > 0     # pos: h=+1 iff x >= T ; neg: iff x <= T
        sc, b, mu, s = self.bn2
        self.T2 = mu - b * s / sc; self.pos2 = sc > 0
        if self.big:   # 64 net: conv3 (+-1, no bias) -> MaxPool -> BN
            assert self.b3 is None and set(np.unique(self.w3)) <= {-1.0, 1.0}
            sc, b, mu, s = bnp(bns[2])
            self.T3 = mu - b * s / sc; self.pos3 = sc > 0
        assert np.all(self.dmul != 0)
        self.Td = -self.dadd / self.dmul; self.posd = self.dmul > 0
        self.W1 = wmat(self.w1); self.W2 = wmat(self.w2); self.W3 = wmat(self.w3)

    # ---------------- exact forward ----------------
    def setup_box(self, lo, hi, pw=9):
        self.lo, self.hi = lo, hi
        self.v, self.off, self.m, self.dmin, self.dmax = pixel_map(lo, hi, pw)
        self.pw = pw
        base = (self.v + self.off)[None]
        self.C0 = (im2col(base, 5) @ self.W1)[0]          # (Ho,Wo,32) exact in float64
        # integer threshold on K for each conv1 output: a1 = C0 + m*K
        r = (self.T1[None, None, :] - self.C0) / self.m
        # pos: a1 >= T  <=> K >= ceil(r);  neg: a1 <= T <=> K <= floor(r)
        self.th1 = np.where(self.pos1[None, None, :], np.ceil(r), np.floor(r))
        self.r1 = r
        return self

    def x_of(self, d):
        return self.v + self.off + self.m * d

    def layer1(self, D):
        """D: (B,S,S,3) integer d arrays -> h1 (B,P,P,32) in {-1,+1}, plus K."""
        K = im2col(D.astype(np.float32), 5) @ self.W1.astype(np.float32)   # small ints: exact
        K = K.astype(np.float64)
        if True:
            hit = np.where(self.pos1, K >= self.th1, K <= self.th1)           # per conv1 position: unit passes
            # pos: h=+1 iff any position passes (max >= T); neg: h=+1 iff all pass (max <= T)
            B, H, W, C = hit.shape
            hh = hit[:, :H // 2 * 2, :W // 2 * 2, :].reshape(B, H // 2, 2, W // 2, 2, C)
            h = np.where(self.pos1, hh.any(axis=(2, 4)), hh.all(axis=(2, 4)))
        return np.where(h, 1.0, -1.0), K

    def rest(self, h1):
        a2 = im2col(h1.astype(np.float32), 5) @ self.W2.astype(np.float32)   # ints
        p2 = pool2(a2.astype(np.float64))
        h2 = np.where(np.where(self.pos2, p2 >= self.T2, p2 <= self.T2), 1.0, -1.0)
        if self.big:
            a3 = pool2(im2col(h2.astype(np.float32), 3) @ self.W3.astype(np.float32)).astype(np.float64) - self.T3
            a3 = np.where(self.pos3, a3, -a3)     # h3 = +1 iff a3 >= 0
        else:
            a3 = im2col(h2, 3) @ self.W3 + self.b3
        h3 = np.where(a3 >= 0, 1.0, -1.0)
        f = h3.reshape(h3.shape[0], -1)
        u = f.astype(np.float32) @ self.d1.astype(np.float32)
        u = u.astype(np.float64)
        hd = np.where(np.where(self.posd, u >= self.Td, u <= self.Td), 1.0, -1.0)
        L = hd @ self.d2
        return dict(a2=a2, p2=p2, h2=h2, a3=a3, h3=h3, u=u, hd=hd, L=L)

    def forward(self, D):
        h1, K = self.layer1(D)
        out = self.rest(h1); out['h1'] = h1; out['K'] = K
        return out

    def margins(self, D):
        """Minimum distance of each layer's decisions to the real threshold at integer point(s) D."""
        o = self.forward(D)
        a1 = self.C0 + self.m * o['K']
        g1 = np.abs(a1 - self.T1).min()
        g2 = np.abs(o['p2'] - self.T2).min()
        g3 = np.abs(o['a3']).min()
        gd = np.abs(o['u'] - self.Td).min()
        return dict(conv1=float(g1), conv2=float(g2), conv3=float(g3), dense=float(gd))


def ort_logits(onnx_model, X):
    """Run onnxruntime CPU on X (B,S,S,3) float32, returning the pre-softmax logits and the softmax output."""
    import onnxruntime as ort
    m = onnx.ModelProto(); m.CopyFrom(onnx_model)
    mm = [n for n in m.graph.node if n.op_type == 'MatMul'][-1]
    m.graph.output.append(onnx.helper.make_tensor_value_info(mm.output[0], onnx.TensorProto.FLOAT, None))
    so = ort.SessionOptions(); so.intra_op_num_threads = 1
    s = ort.InferenceSession(m.SerializeToString(), so, providers=['CPUExecutionProvider'])
    inp = s.get_inputs()[0].name
    Ls, Ys = [], []
    for x in X:
        y, L = s.run(None, {inp: x[None].astype(np.float32)})
        Ls.append(L[0]); Ys.append(y[0])
    return np.array(Ls, np.float64), np.array(Ys, np.float64)


def rebox(lo, hi, eps_from, eps_to):
    """Box of the same integer image at another integer radius (VNN-COMP rule: [max(0,c-eps), min(255,c+eps)])."""
    lo = np.asarray(lo, np.float64); hi = np.asarray(hi, np.float64)
    c = np.where((lo > 0) & (hi < 255), (lo + hi) / 2, np.where(lo == 0, hi - eps_from, lo + eps_from))
    assert np.all(c == np.round(c)) and not np.any((lo == 0) & (hi == 255))
    assert np.array_equal(np.maximum(0, c - eps_from), lo) and np.array_equal(np.minimum(255, c + eps_from), hi)
    return np.maximum(0, c - eps_to), np.minimum(255, c + eps_to)


def convert_d(d, box_from, box_to, pw=9):
    """Project an integer step vector from one box's pixel map onto another's (clip, then nearest grid point)."""
    v0, o0, m0, _, _ = pixel_map(*box_from, pw); v1, o1, m1, a1, b1 = pixel_map(*box_to, pw)
    x = v0 + o0 + m0 * d
    return np.clip(np.rint((x - v1 - o1) / m1), a1, b1).astype(np.int64)
