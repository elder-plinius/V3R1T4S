#!/usr/bin/env python3
"""Standalone check of the witness in ../object/witness_plain.txt, written from the VNN-LIB definition.

Downloads the benchmark ONNX and VNN-LIB 2.0 files of VNN-COMP 2026 traffic_signs_recognition_2023 from GitHub
(raw URLs below) and stops unless their sha256 match the pinned values. Then, with exact rational arithmetic for the
input box and onnxruntime CPU float32 for the output (onnx.reference as a second runtime when the onnx package is
installed), it checks:
  1. 6912 values, each exactly representable in float32;
  2. every value strictly inside its bounds: lo < x < hi (no tolerance);
  3. the output assertion (or (and (>= Y[0,c] Y[0,17])) ...) holds, with Y[0,c] - Y[0,17] >= 1e-6 on a satisfied
     disjunct.
Last output line: PASS or FAIL.  Requirements: Python 3, numpy, onnxruntime (optional: onnx).
Usage: python3 check.py [--cache DIR] [--witness PATH]
"""
import argparse, gzip, hashlib, os, re, sys, tempfile, urllib.request
from fractions import Fraction

BASE = 'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/main/benchmarks/traffic_signs_recognition_2023/2.0'
NET = '3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx.gz'
PROP = 'model_48_idx_6371_eps_3.00000.vnnlib.gz'
PIN = {NET: '6f4969db9cea8c278049dc45933485e0b455fba5e2524b7ac307056e1a0b9e6e',
       PROP: 'd5f96951d9259ede11b37cc8622e5b12b6e180078c63f4ec4cfab7bb07e5168c'}
UA = 'V3R1T4S-verify (one request per file)'
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(sub, name, cache):
    p = os.path.join(cache, name)
    if not os.path.isfile(p):
        req = urllib.request.Request(f'{BASE}/{sub}/{name}', headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120) as r, open(p, 'wb') as f:
            f.write(r.read())
    data = open(p, 'rb').read()
    got = hashlib.sha256(data).hexdigest()
    if got != PIN[name]:
        print(f'{name}: sha256 {got} does not match the pinned value'); print('FAIL'); sys.exit(1)
    print(f'{name}: sha256 OK')
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default=None)
    ap.add_argument('--witness', default=os.path.join(HERE, '..', 'object', 'witness_plain.txt'))
    a = ap.parse_args()
    cache = a.cache or tempfile.mkdtemp(prefix='vnn-check-')
    os.makedirs(cache, exist_ok=True)
    net = fetch('onnx', NET, cache)
    txt = gzip.decompress(fetch('vnnlib', PROP, cache)).decode()
    ok = True
    vals = [l.strip() for l in open(a.witness) if l.strip()]
    if len(vals) != 48 * 48 * 3:
        print('wrong number of values:', len(vals)); print('FAIL'); return 1
    try:
        xf = [Fraction(v) for v in vals]
    except ValueError:
        print('unparseable value'); print('FAIL'); return 1
    import numpy as np
    x32 = np.array([float(v) for v in vals], dtype=np.float32)
    exact = all(Fraction(float(v)) == f for v, f in zip(x32, xf))
    print('1. float32 exact:', exact); ok &= exact
    lo, hi = {}, {}
    for op, h, w, c, b in re.findall(r'\(assert \((<=|>=) X\[0,(\d+),(\d+),(\d+)\] ([-0-9.eE]+)\)\)', txt):
        k = (int(h) * 48 + int(w)) * 3 + int(c)
        (hi if op == '<=' else lo)[k] = Fraction(b)
    if len(lo) != 6912 or len(hi) != 6912:
        print('could not parse the input box'); print('FAIL'); return 1
    inside = all(lo[k] < xf[k] < hi[k] for k in range(6912))
    slack = min(min(xf[k] - lo[k], hi[k] - xf[k]) for k in range(6912))
    print('2. strictly inside every bound:', inside, '| smallest slack', float(slack)); ok &= inside
    pairs = [(int(c), int(t)) for c, t in re.findall(r'\(and \(>= Y\[0,(\d+)\] Y\[0,(\d+)\]\)\)', txt)]
    if len(pairs) != 42 or txt.count('(or') != 1:
        print('unexpected output assertion shape'); print('FAIL'); return 1
    import onnxruntime as ort
    so = ort.SessionOptions(); so.intra_op_num_threads = 1
    s = ort.InferenceSession(gzip.decompress(net), so, providers=['CPUExecutionProvider'])
    X = x32.reshape(1, 48, 48, 3)
    runs = [('onnxruntime CPU', s.run(None, {s.get_inputs()[0].name: X})[0].reshape(-1).astype(np.float64))]
    try:
        import io, onnx
        from onnx.reference import ReferenceEvaluator
        ref = ReferenceEvaluator(onnx.load(io.BytesIO(gzip.decompress(net))))
        runs.append(('onnx.reference', np.asarray(ref.run(None, {s.get_inputs()[0].name: X})[0], np.float64).reshape(-1)))
    except ImportError:
        print('(onnx not installed: second runtime skipped)')
    for name, y in runs:
        sat = [(c, float(y[c] - y[t])) for c, t in pairs if y[c] >= y[t]]
        good = any(m >= 1e-6 for _, m in sat)
        print(f'3. {name}: satisfied disjuncts {sat} | margin >= 1e-6: {good}'); ok &= good
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
