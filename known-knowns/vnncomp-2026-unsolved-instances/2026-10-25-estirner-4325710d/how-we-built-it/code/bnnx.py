"""Exact integer model of the traffic_signs_recognition_2023 binarized nets 3_48_48 and 3_64_64 (GPU, torch).

Credit: idea and pixel map from the repo's how-we-built-it/bnn.py and make_witness.py (exact integer model of the
3_30_30 BNN; strict-interior map x = v + off + m*d, m = 1 - 2^-pw, half-step offset for boxes clipped at 0/255).

Graph (both nets): NHWC input -> Conv(+-1, 5x5) -> MaxPool2 -> BN -> [Sign,+0.1,Sign] -> Conv(+-1,5x5) -> MaxPool2 -> BN
-> sign -> Conv3x3 (48: BN fused into weights +-s_o and bias; 64: +-1 then MaxPool2 -> BN) -> sign -> flatten (NHWC)
-> MatMul(+-1) -> Mul,Add (BN) -> sign -> MatMul(+-1) -> Softmax.   sign(z) here = +1 iff z >= 0 (Sign(0)=0, +0.1 -> +1).

Integer form: every layer is h_out = +1 iff (integer pre-activation) >= thr (real threshold, computed in float64 from the
float32 parameters), except layer 1, where a1 = C1 + m*K (C1 = conv1(v+off) exact, K = conv1(d) integer), so
'conv position active' iff K >= kthr := ceil((T1 - C1)/m); pooled neuron active iff max over its 2x2 window of (K-kthr)>=0.
With pw = 8 every input is a multiple of 2^-9 with |x| <= 255, so all conv1 partial sums (|.| < 2^15) are exact in float32
(no rounding in onnxruntime's conv either). BN rounding in onnxruntime float32 is the only inexact step: we report the
minimum distance |pre - thr| per layer and every final candidate is replayed on CPU onnxruntime.
"""
import sys, os, gzip, io, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if not os.environ.get('BNNX_CPU'):
    import cuda_blocking  # noqa: F401  (must precede torch)
DEV = 'cpu' if os.environ.get('BNNX_CPU') else 'cuda'
import numpy as np
import torch
import torch.nn.functional as F
import onnx
from onnx import numpy_helper

torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
try:
    torch.backends.cuda.matmul.fp32_precision = 'ieee'
    torch.backends.cudnn.conv.fp32_precision = 'ieee'
except Exception:
    pass
# cuDNN may pick Winograd/FFT conv algorithms whose fp32 results are not exact integers; every integer-valued conv and
# matmul below is therefore rounded (errors are far below 0.5 at these magnitudes), which restores exactness.

LENS = os.environ.get('LENS', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(LENS, 'in'))
NET = {48: os.path.join(LENS, 'in/bench/3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx.gz'),
       64: os.path.join(LENS, 'in/bench/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz')}
NETNAME = {48: '3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30',
           64: '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30'}


def vnnlib_path(size, idx, eps=1):
    return os.path.join(LENS, 'in/bench/model_%d_idx_%d_eps_%d.00000.vnnlib.gz' % (size, idx, eps))


def load_onnx(size):
    return onnx.load_from_string(gzip.decompress(open(NET[size], 'rb').read()))


def parse_net(size):
    """Returns dict of float64 numpy params in graph order."""
    m = load_onnx(size)
    W = {t.name: numpy_helper.to_array(t) for t in m.graph.initializer}
    convs, bns, mms, muls, adds = [], [], [], [], []
    for n in m.graph.node:
        if n.op_type == 'Conv':
            convs.append([W[i].astype(np.float64) for i in n.input[1:]])
        elif n.op_type == 'BatchNormalization':
            eps = [a.f for a in n.attribute if a.name == 'epsilon'][0]
            sc, B, mean, var = [W[i].astype(np.float64) for i in n.input[1:]]
            bns.append(dict(scale=sc, B=B, mean=mean, var=var, eps=float(np.float32(eps))))
        elif n.op_type == 'MatMul':
            mms.append(W[n.input[1]].astype(np.float64))
        elif n.op_type == 'Mul':
            muls.append(W[n.input[1]].astype(np.float64))
        elif n.op_type == 'Add' and n.input[1] in W and W[n.input[1]].shape != ():
            adds.append(W[n.input[1]].astype(np.float64))
    return dict(convs=convs, bns=bns, mms=mms, muls=muls, adds=adds, model=m)


def bn_thr(bn):
    # y = scale*(x-mean)/sqrt(var+eps) + B >= 0  <=>  x >= mean - B*sqrt(var+eps)/scale   (scale > 0 here)
    assert np.all(bn['scale'] > 0)
    return bn['mean'] - bn['B'] * np.sqrt(bn['var'] + bn['eps']) / bn['scale']


def pixel_map(lo, hi, pw=8):
    """from how-we-built-it/bnn.py (credited): x = v + off + m*d strictly inside, float32-exact."""
    lo = np.asarray(lo, dtype=np.float64); hi = np.asarray(hi, dtype=np.float64)
    assert np.all(lo == np.round(lo)) and np.all(hi == np.round(hi)) and np.all(hi > lo)
    v = np.floor((lo + hi) / 2)
    m = 1.0 - 2.0 ** -pw
    off = np.where(v == lo, 2.0 ** -(pw + 1), np.where(v == hi, -2.0 ** -(pw + 1), 0.0))
    dmin = (lo - v).astype(np.int64); dmax = (hi - v).astype(np.int64)
    xlo = v + off + m * dmin; xhi = v + off + m * dmax
    assert np.all(xlo > lo) and np.all(xhi < hi)
    return v, off, m, dmin, dmax


class Spec:
    def __init__(self, size, idx, eps=1):
        import vnnspec
        self.size, self.idx, self.eps = size, idx, eps
        s = vnnspec.load(vnnlib_path(size, idx, eps))
        self.ishape = s['ishape']
        self.lo = s['lo'].reshape(size, size, 3); self.hi = s['hi'].reshape(size, size, 3)
        # every disjunct is a single atom Y_j - Y_t >= 0
        tset = set(); self.rivals = []
        for A, b in s['disjuncts']:
            assert A.shape[0] == 1 and b[0] == 0
            j = int(np.argmax(A[0])); t = int(np.argmin(A[0]))
            assert A[0, j] == 1 and A[0, t] == -1 and np.abs(A[0]).sum() == 2
            tset.add(t); self.rivals.append(j)
        assert len(tset) == 1
        self.true = tset.pop()


class ExactNet:
    """Integer model on the GPU. Input: d (B,H,W,3) integer-valued tensor (any float/int dtype) in [dmin,dmax]."""

    def __init__(self, size, spec, pw=8, device=None):
        device = device or DEV
        self.size, self.dev, self.pw = size, device, pw
        P = parse_net(size)
        self.P = P
        v, off, m, dmin, dmax = pixel_map(spec.lo, spec.hi, pw)
        self.v, self.off, self.m, self.dmin, self.dmax = v, off, m, dmin, dmax
        w1 = P['convs'][0][0]; assert set(np.unique(w1)) <= {-1.0, 1.0}
        self.w1 = torch.tensor(w1, dtype=torch.float32, device=device)
        x0 = (v + off).transpose(2, 0, 1)[None]  # NCHW float64, exact
        C1 = F.conv2d(torch.tensor(x0, dtype=torch.float64), torch.tensor(w1, dtype=torch.float64))[0]  # (32,Ho,Wo)
        T1 = bn_thr(P['bns'][0])
        self.T1 = T1
        self.C1 = C1.numpy()
        kthr = np.ceil((T1[:, None, None] - self.C1) / m)
        # guard: if (T1-C1)/m is an exact integer, K = that integer gives a1 == T1 exactly -> BN out 0 -> +1 (ok, >=)
        self.kthr = torch.tensor(kthr, dtype=torch.float32, device=device)
        # distance of layer-1 threshold to the reachable grid (diagnostic)
        self.w2 = torch.tensor(P['convs'][1][0], dtype=torch.float32, device=device)
        assert set(np.unique(P['convs'][1][0])) <= {-1.0, 1.0}
        self.T2 = torch.tensor(bn_thr(P['bns'][1]), dtype=torch.float64, device=device)
        self.T2c = torch.ceil(self.T2).float()
        w3 = P['convs'][2][0]
        if size == 48:
            s_o = np.abs(w3).reshape(64, -1).max(1)
            assert np.allclose(np.abs(w3), s_o[:, None, None, None])
            assert np.all(s_o > 0)
            self.w3 = torch.tensor(np.sign(w3), dtype=torch.float32, device=device)
            b3 = P['convs'][2][1]
            self.T3 = torch.tensor(-b3 / s_o, dtype=torch.float64, device=device)
            self.pool3 = False
        else:
            assert set(np.unique(w3)) <= {-1.0, 1.0} and len(P['convs'][2]) == 1
            self.w3 = torch.tensor(w3, dtype=torch.float32, device=device)
            self.T3 = torch.tensor(bn_thr(P['bns'][2]), dtype=torch.float64, device=device)
            self.pool3 = True
        self.T3c = torch.ceil(self.T3).float()
        W4 = P['mms'][0]; assert set(np.unique(W4)) <= {-1.0, 1.0}
        self.W4 = torch.tensor(W4, dtype=torch.float32, device=device)
        r, s = P['muls'][0], P['adds'][0]
        assert np.all(r > 0)
        self.T4 = torch.tensor(-s / r, dtype=torch.float64, device=device)
        self.T4c = torch.ceil(self.T4).float()
        W5 = P['mms'][1]; assert set(np.unique(W5)) <= {-1.0, 1.0}
        self.W5 = torch.tensor(W5, dtype=torch.float32, device=device)
        self.dmin_t = torch.tensor(dmin.transpose(2, 0, 1), dtype=torch.float32, device=device)
        self.dmax_t = torch.tensor(dmax.transpose(2, 0, 1), dtype=torch.float32, device=device)

    # ---- layer functions (all tensors NCHW float32, exact integers)
    def l1_pre(self, d_nchw):
        K = torch.round(F.conv2d(d_nchw, self.w1))  # integer
        return K - self.kthr  # active iff >= 0 ; pooled via max

    def forward_real(self, x_nchw64):
        """real inputs (B,3,H,W) float64 -> logits via the exact threshold model (conv1 in float64)."""
        a1 = F.conv2d(x_nchw64, self.w1.double())
        p1 = F.max_pool2d(a1, 2)
        h1 = torch.where(p1 >= torch.tensor(self.T1, device=self.dev)[None, :, None, None], 1.0, -1.0).float()
        return self.forward_from_h1(h1)

    def forward_from_h1(self, h1, keep=False):
        n2 = torch.round(F.conv2d(h1, self.w2))
        p2 = F.max_pool2d(n2, 2)
        z2 = p2 - self.T2c[None, :, None, None]
        h2 = torch.where(z2 >= 0, 1.0, -1.0)
        n3 = torch.round(F.conv2d(h2, self.w3))
        if self.pool3:
            n3 = F.max_pool2d(n3, 2)
        z3 = n3 - self.T3c[None, :, None, None]
        h3 = torch.where(z3 >= 0, 1.0, -1.0)
        f3 = h3.permute(0, 2, 3, 1).reshape(h3.shape[0], -1)
        n4 = torch.round(f3 @ self.W4)
        z4 = n4 - self.T4c[None]
        h4 = torch.where(z4 >= 0, 1.0, -1.0)
        L = torch.round(h4 @ self.W5)
        if keep:
            return L, dict(n2=n2, p2=p2, z2=z2, h2=h2, n3=n3, z3=z3, h3=h3, f3=f3, n4=n4, z4=z4, h4=h4)
        return L

    def forward(self, d_nchw, keep=False):
        """d_nchw: (B,3,H,W) float32 integer values. Returns logits (B,43) float32 exact integers (+ intermediates)."""
        z1 = self.l1_pre(d_nchw)
        p1 = F.max_pool2d(z1, 2)
        h1 = torch.where(p1 >= 0, 1.0, -1.0)
        n2 = torch.round(F.conv2d(h1, self.w2))
        p2 = F.max_pool2d(n2, 2)
        z2 = p2 - self.T2c[None, :, None, None]
        h2 = torch.where(z2 >= 0, 1.0, -1.0)
        n3 = torch.round(F.conv2d(h2, self.w3))
        if self.pool3:
            n3 = F.max_pool2d(n3, 2)
        z3 = n3 - self.T3c[None, :, None, None]
        h3 = torch.where(z3 >= 0, 1.0, -1.0)
        f3 = h3.permute(0, 2, 3, 1).reshape(h3.shape[0], -1)  # NHWC flatten
        n4 = torch.round(f3 @ self.W4)
        z4 = n4 - self.T4c[None]
        h4 = torch.where(z4 >= 0, 1.0, -1.0)
        L = torch.round(h4 @ self.W5)
        if keep:
            return L, dict(z1=z1, p1=p1, h1=h1, n2=n2, p2=p2, z2=z2, h2=h2, n3=n3, z3=z3, h3=h3, f3=f3, n4=n4, z4=z4, h4=h4)
        return L

    def d_to_x(self, d_hwc):
        """d (H,W,3) int numpy -> x float32 (H,W,3), asserted exact and strictly inside."""
        x64 = self.v + self.off + self.m * d_hwc
        x = x64.astype(np.float32)
        assert np.all(x.astype(np.float64) == x64)
        return x

    def real_margins(self, d_nchw):
        """distance of each layer's pre-activation to its real threshold (float64) for robustness diagnostics."""
        L, I = self.forward(d_nchw, keep=True)
        out = {}
        K = F.conv2d(d_nchw.double(), self.w1.double())
        a1 = torch.tensor(self.C1, device=self.dev)[None] + self.m * K
        pa1 = F.max_pool2d(a1, 2)
        out['l1'] = (pa1 - torch.tensor(self.T1, device=self.dev)[None, :, None, None]).abs().amin(dim=(1, 2, 3))
        out['l2'] = (I['p2'].double() - self.T2[None, :, None, None]).abs().amin(dim=(1, 2, 3))
        out['l3'] = (I['n3'].double() - self.T3[None, :, None, None]).abs().amin(dim=(1, 2, 3))
        out['l4'] = (I['n4'].double() - self.T4[None]).abs().amin(dim=1)
        return L, out


def ort_session(size, extra_outputs=False):
    import onnxruntime as ort
    m = load_onnx(size)
    if extra_outputs:
        names = [n.output[0] for n in m.graph.node if n.op_type == 'MatMul']
        for nm in names:
            m.graph.output.append(onnx.helper.make_tensor_value_info(nm, onnx.TensorProto.FLOAT, None))
    so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
    return ort.InferenceSession(m.SerializeToString(), so, providers=['CPUExecutionProvider'])


def ort_run(sess, x_hwc):
    """x (H,W,3) float32 -> list of outputs (softmax first, then extra)."""
    return sess.run(None, {sess.get_inputs()[0].name: x_hwc[None].astype(np.float32)})


def vnn_margin(Y, true, rivals):
    """margin of the violation: max_j (Y_j - Y_t) over the rivals listed in the vnnlib."""
    Y = np.asarray(Y, dtype=np.float64).ravel()
    return float(max(Y[j] - Y[true] for j in rivals))
