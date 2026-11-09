#!/usr/bin/env python3
"""Standalone check of the witness in ../object/, written from the VNN-LIB definition (VNN-COMP semantics: the .vnnlib
file encodes the violation; a counterexample makes EVERY assertion true).

Instance: VNN-COMP 2026 traffic_signs_recognition_2023 (version 2.0), network
3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx,
property model_64_idx_6371_eps_1.00000.vnnlib.
The property file and the network file (0.43 MB) are fetched from the benchmarks repository on GitHub (commit 303f2327). Both are
fetched once (one request per file) into --cache (default: $VNN_CACHE or a temporary folder) and must match the
pinned sha256 values. Then, with exact rational arithmetic for the input box and onnxruntime CPU float32 for the
output (onnx.reference as a second runtime when the onnx package is installed), it checks:
  1. 12288 values, each exactly representable in float32;
  2. every value strictly inside its bounds: lo < x < hi (no tolerance);
  3. the output assertion (or (and (>= Y[0,k] Y[0,17])) ...) holds, with Y[0,k] - Y[0,17] >= 1e-6 on a satisfied
     disjunct, in every runtime run.
Last output line: PASS or FAIL.  Requirements: Python 3, numpy, onnxruntime (optional: onnx).
Usage: python3 check.py [--cache DIR] [--witness PATH] [--no-reference]
"""
import argparse, gzip, hashlib, os, re, sys, tempfile, urllib.request
from fractions import Fraction

FILES = {
    '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz': (
        'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz',
        '818d676e69caadeb1c9044b9b6aa7d9896dfd2101842918869f9b291a9539b85'),
    'model_64_idx_6371_eps_1.00000.vnnlib.gz': (
        'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_64_idx_6371_eps_1.00000.vnnlib.gz',
        '16efc2694a75e6595816806ff4cf168214e8a5ec368757dad7dc896033658b84'),
}
UA = 'V3R1T4S-verify (one request per file)'
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL, N, NOUT = 17, 64 * 64 * 3, 43


def fetch(name, cache):
    url, pin = FILES[name]
    p = os.path.join(cache, name)
    if not os.path.isfile(p):
        print('fetching', url, flush=True)
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=1800) as r, open(p + '.part', 'wb') as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        os.replace(p + '.part', p)
    data = open(p, 'rb').read()
    got = hashlib.sha256(data).hexdigest()
    if got != pin:
        print(f'{name}: sha256 {got} does not match the pinned value {pin}'); print('FAIL'); sys.exit(1)
    print(f'{name}: sha256 OK')
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default=os.environ.get('VNN_CACHE'))
    ap.add_argument('--witness', default=os.path.join(HERE, '..', 'object', '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000.counterexample.txt'))
    ap.add_argument('--no-reference', action='store_true')
    a = ap.parse_args()
    cache = a.cache or tempfile.mkdtemp(prefix='vnn-check-')
    os.makedirs(cache, exist_ok=True)
    txt = gzip.decompress(fetch('model_64_idx_6371_eps_1.00000.vnnlib.gz', cache)).decode()
    net = gzip.decompress(fetch('3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz', cache))
    ok = True
    vals = [l.strip() for l in open(a.witness) if l.strip()]
    if len(vals) != N:
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
        k = (int(h) * 64 + int(w)) * 3 + int(c)           # row-major order of X[1,64,64,3]
        (hi if op == '<=' else lo)[k] = Fraction(b)
    if len(lo) != N or len(hi) != N:
        print('could not parse the input box'); print('FAIL'); return 1
    inside = all(lo[k] < xf[k] < hi[k] for k in range(N))
    slack = min(min(xf[k] - lo[k], hi[k] - xf[k]) for k in range(N))
    print('2. strictly inside every bound:', inside, '| smallest slack', float(slack)); ok &= inside
    rivals = [int(r) for r, t in re.findall(r'\(and \(>= Y\[0,(\d+)\] Y\[0,(\d+)\]\)\)', txt) if int(t) == LABEL]
    nasserts = len(re.findall(r'\(assert ', txt))
    if sorted(rivals) != [k for k in range(NOUT) if k != LABEL] or txt.count('(or') != 1 or nasserts != 2 * N + 1:
        print('unexpected output assertion shape'); print('FAIL'); return 1
    import onnxruntime as ort
    so = ort.SessionOptions(); so.intra_op_num_threads = 1
    s = ort.InferenceSession(net, so, providers=['CPUExecutionProvider'])
    X = x32.reshape(1, 64, 64, 3)
    runs = [('onnxruntime CPU', s.run(None, {s.get_inputs()[0].name: X})[0].reshape(-1).astype(np.float64))]
    if not a.no_reference:
        try:
            import onnx
            from onnx.reference import ReferenceEvaluator
            m = onnx.load_from_string(net)
            ref = ReferenceEvaluator(m)
            runs.append(('onnx.reference', np.asarray(ref.run(None, {m.graph.input[0].name: X})[0]).reshape(-1).astype(np.float64)))
        except ImportError:
            print('onnx not installed: second runtime skipped')
    for name, y in runs:
        margins = {k: Fraction(float(np.float32(y[k]))) - Fraction(float(np.float32(y[LABEL]))) for k in rivals}
        best = max(margins, key=margins.get)
        good = margins[best] >= Fraction(1, 10 ** 6)
        print(f'3. {name}: argmax {int(np.argmax(y))}; best disjunct (>= Y[0,{best}] Y[0,{LABEL}]) margin {float(margins[best]):.10g} -> {good}')
        ok &= good
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
