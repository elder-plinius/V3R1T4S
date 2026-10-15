"""Turn a search checkpoint (integer d on the pixel map) into VNN-COMP witness files and check it every way the bank
criterion asks: strict interior, float32 exactness, onnxruntime CPU float32, onnx.reference (second runtime), and
the UNMODIFIED official SCORING/counterexamples_v2.py at abs_tol 0 and 1e-4.

Usage: python -I validate_hit.py --data DATA --inst model_48_idx_6371_eps_3 --ckpt ckpt.json --out DIR
(DATA holds onnx/, vnnlib/ and SCORING/ exactly as fetched; the validator is imported from DATA/SCORING.)
"""
import argparse, glob, gzip, io, json, os, sys
from pathlib import Path
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from bnn4864 import Net, parse_box
import onnx, onnxruntime as ort
from onnx.reference import ReferenceEvaluator

class ResultType:
    CORRECT = 'correct'; CORRECT_UP_TO_TOLERANCE = 'correct_up_to_tolerance'; SPEC_NOT_VIOLATED = 'spec_not_violated'
    NO_CE = 'no_ce'; MALFORMED_CE = 'malformed_ce'; UNSUPPORTED = 'unsupported'

ap = argparse.ArgumentParser()
ap.add_argument('--data', required=True); ap.add_argument('--inst', required=True); ap.add_argument('--ckpt', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args()
tag = a.inst.split('_')[1]
onnx_path = glob.glob(f'{a.data}/onnx/3_{tag}_*.onnx.gz')[0]; vn = f'{a.data}/vnnlib/{a.inst}.00000.vnnlib.gz'
net = Net(onnx_path); S = net.S
lo, hi, tgt = parse_box(vn, (S, S, 3)); net.setup_box(lo, hi, int(json.load(open(a.ckpt)).get('pw', 9)))
d = np.array(json.load(open(a.ckpt))['d'], np.int64).reshape(S, S, 3)
assert np.all(d >= net.dmin) and np.all(d <= net.dmax)
x64 = net.x_of(d); x = x64.astype(np.float32)
rep = {}
rep['float32_exact'] = bool(np.all(x.astype(np.float64) == x64))
rep['strictly_inside'] = bool(np.all(lo < x) and np.all(x < hi)); rep['min_slack'] = float(min((x - lo).min(), (hi - x).min()))
Le = net.forward(d[None])['L'][0]; Lo = Le.copy(); Lo[tgt] = -1e9
rep['exact_model_G'] = int(Lo.max() - Le[tgt]); rep['exact_model_cls'] = int(Lo.argmax())
rep['margins'] = net.margins(d[None])
so = ort.SessionOptions(); so.intra_op_num_threads = 1
s = ort.InferenceSession(gzip.open(onnx_path).read(), so, providers=['CPUExecutionProvider'])
y = s.run(None, {s.get_inputs()[0].name: x[None]})[0].reshape(-1).astype(np.float64)
yo = y.copy(); yo[tgt] = -1
c = int(yo.argmax()); rep['ort_cls'] = c; rep['ort_margin'] = float(y[c] - y[tgt])
rep['ort_holds_1e-6'] = bool(y[c] - y[tgt] >= 1e-6)
ref = ReferenceEvaluator(onnx.load(io.BytesIO(gzip.open(onnx_path).read())))
yr = np.asarray(ref.run(None, {s.get_inputs()[0].name: x[None]})[0], np.float64).reshape(-1)
rep['ref_margin'] = float(yr[c] - yr[tgt]); rep['ref_holds_1e-6'] = bool(yr[c] - yr[tgt] >= 1e-6)
os.makedirs(a.out, exist_ok=True)
flat = x.reshape(-1)
with open(os.path.join(a.out, 'witness_plain.txt'), 'w') as f:
    for v in flat: f.write(repr(float(v)) + '\n')
with open(os.path.join(a.out, 'witness_v2.txt'), 'w') as f:
    f.write('sat\n'); f.write(f'X float32 [1, {S}, {S}, 3]\n')
    for v in flat: f.write(repr(float(v)) + '\n')
    f.write(f'Y float32 [1, {y.size}]\n')
    for v in y.astype(np.float32): f.write(repr(float(v)) + '\n')
sys.path.insert(0, os.path.abspath(os.path.join(a.data, 'SCORING')))
import counterexamples_v2 as cv2
nf = os.path.relpath(onnx_path, a.data)[:-3]; pf = os.path.relpath(vn, a.data)[:-3]   # 'onnx/NAME.onnx', resolved to .gz
for tol in (0.0, 1e-4):
    r = cv2.validate_vnnlib2_counterexample(Path(a.data), nf, pf, os.path.join(a.out, 'witness_v2.txt'), tol, 0.0, ResultType)
    rep[f'official_abs_tol_{tol}'] = [str(r[0]), str(r[1])[:200]]
json.dump(rep, open(os.path.join(a.out, 'validation.json'), 'w'), indent=1)
print(json.dumps(rep))
