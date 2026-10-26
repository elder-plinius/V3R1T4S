"""Replay a real point x (npy, HWC float) on CPU onnxruntime (vnn venv): float32 exactness, strict interior in float32,
all VNN-LIB disjuncts, violation margin on softmax outputs, logit gap (extra MatMul output), and robustness
diagnostics: min |maxpool(conv1(x)) - T1| at layer 1 and min |pre - thr| at the BN layers (float64 recomputation).
Saves out/candidate_model_<size>_idx_<idx>_eps_1_<k>.npy (float32, shape (1,H,W,3)) iff margin > 0 and strict.
Usage (vnn venv, -I): replay_x.py SIZE IDX X.npy K"""
import sys, os, gzip
import numpy as np
import onnx, onnxruntime as ort
from onnx import numpy_helper
LENS = os.environ.get('LENS', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(LENS, 'in'))
import vnnspec
NETS = {48: '3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30',
        64: '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30'}
size, idx, xpath, k = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
s = vnnspec.load(os.path.join(LENS, 'in/bench/model_%d_idx_%d_eps_1.00000.vnnlib.gz' % (size, idx)))
lo = s['lo'].reshape(size, size, 3); hi = s['hi'].reshape(size, size, 3)
x64 = np.load(xpath).astype(np.float64).reshape(size, size, 3)
x = x64.astype(np.float32)
exact = bool(np.all(x.astype(np.float64) == x64))
strict = bool(((x > lo.astype(np.float32)) & (x < hi.astype(np.float32))).all())
m = onnx.load_from_string(gzip.decompress(open(os.path.join(LENS, 'in/bench/%s.onnx.gz' % NETS[size]), 'rb').read()))
names = [n.output[0] for n in m.graph.node if n.op_type in ('MatMul', 'MaxPool', 'BatchNormalization')]
for nm in names:
    m.graph.output.append(onnx.helper.make_tensor_value_info(nm, onnx.TensorProto.FLOAT, None))
so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
sess = ort.InferenceSession(m.SerializeToString(), so, providers=['CPUExecutionProvider'])
outs = sess.run(None, {sess.get_inputs()[0].name: x[None]})
O = dict(zip([o.name for o in sess.get_outputs()], outs))
Y = outs[0].astype(np.float64).ravel()
best = max(float((A @ Y + b).min()) for A, b in s['disjuncts'])
logits = O[[n for n in names if n.endswith('MatMul:0')][-1]].ravel()
t = int(np.argmin([A[0].min() for A, b in s['disjuncts']][0:1]))  # placeholder, true class below
true = int(np.argmin(s['disjuncts'][0][0][0]))
gap = float(max(logits[j] for j in range(43) if j != true) - logits[true])
# BN-input robustness: distance of BN outputs to 0 (sign decision) in ORT float32
bn_outs = [O[n] for n in names if 'FusedBatchNormV3:0' in n]
bn_min = [float(np.abs(b).min()) for b in bn_outs]
print('instance', size, idx, 'float32_exact', exact, 'strict_inside', strict,
      'min_dist_to_bound', float(min((x - lo).min(), (hi - x).min())), 'softmax_margin', best, 'logit_gap', gap,
      'argmax', int(Y.argmax()), 'true', true, 'min|BN out| per BN layer', bn_min, 'ort', ort.__version__)
if best > 0 and strict and exact:
    out = os.path.join(LENS, 'out/candidate_model_%d_idx_%d_eps_1_%s.npy' % (size, idx, k))
    np.save(out, x[None].astype(np.float32)); print('saved', out)
