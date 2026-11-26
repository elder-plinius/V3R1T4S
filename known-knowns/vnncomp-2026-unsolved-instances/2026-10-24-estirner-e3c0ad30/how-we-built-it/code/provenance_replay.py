"""Provenance check of a model file: replay a witness that the competition validator rated 'correct' (VNN-LIB 1.0
'((X_i v) ...' format, or plain) on our copy with onnxruntime CPU and report the property margin (max over disjuncts
of min over atoms, as vnnspec reads the 2.0 file). A positive margin means our copy behaves like the validated one.
  python provenance_replay.py NET.onnx.gz PROP_2.0.vnnlib.gz WITNESS(.gz)"""
import gzip, re, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netload, vnnspec
net, prop, wit = sys.argv[1:4]
s = vnnspec.load(prop)
txt = (gzip.decompress(open(wit, 'rb').read()) if wit.endswith('.gz') else open(wit, 'rb').read()).decode()
vals = {int(i): float(v) for i, v in re.findall(r"\(X_(\d+)\s+([-0-9.eE+]+)\)", txt)}
n = int(np.prod(s['ishape']))
x = np.array([vals[i] for i in range(n)], dtype=np.float32)
inside = bool(((x.astype(np.float64) >= s['lo']) & (x.astype(np.float64) <= s['hi'])).all())
y = netload.ort_forward(netload.ort_session(netload.read_bytes(net)), x, s['ishape']).astype(np.float64)
ms = [min(float(A[i] @ y + b[i]) for i in range(len(b))) for A, b in s['disjuncts']]
print('witness coords', len(vals), 'inside box (closed)', inside, 'margin %.9g disjunct %d' % (max(ms), int(np.argmax(ms))))
