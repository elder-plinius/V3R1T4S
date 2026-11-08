"""Turn an attack point into witness files and judge it (CPU only).
  python finalize.py NET.onnx.gz PROP.vnnlib.gz POINT.npy OUT_PREFIX
1. snaps the point into the strict box in float32 (lo < x < hi exactly, compared as rationals);
2. writes OUT_PREFIX.txt (plain, one exact decimal expansion of each float32 value per line) and OUT_PREFIX_v2.txt
   (VNN-LIB 2.0 assignment; outputs from onnxruntime CPU, ignored by the validator);
3. replays in torch (onnx2torch) on CPU in float32 and float64 and reports the margin per runtime and the smallest
   |pre-activation| over all ReLU inputs (distance to a kink) in float64.
The official validator and vnncheck_own.py are run separately on the files written here."""
import gzip, os, sys
from decimal import Decimal
from fractions import Fraction
import numpy as np, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netload, vnnspec
torch.set_num_threads(1)
net_p, prop_p, pt_p, out = sys.argv[1:5]
spec = vnnspec.load(prop_p)
raw = netload.read_bytes(net_p)
x = np.load(pt_p).astype(np.float32).ravel()
lo, hi = spec['lo'], spec['hi']
fix = 0
for i in range(x.size):
    if not (Fraction(float(x[i])) > Fraction(lo[i])):
        x[i] = np.nextafter(np.float32(lo[i]), np.float32(np.inf)); fix += 1
        while not (Fraction(float(x[i])) > Fraction(lo[i])): x[i] = np.nextafter(x[i], np.float32(np.inf))
    if not (Fraction(float(x[i])) < Fraction(hi[i])):
        x[i] = np.nextafter(np.float32(hi[i]), np.float32(-np.inf)); fix += 1
        while not (Fraction(float(x[i])) < Fraction(hi[i])): x[i] = np.nextafter(x[i], np.float32(-np.inf))
sess = netload.ort_session(raw)
y = netload.ort_forward(sess, x, spec['ishape'])
body = "\n".join(format(Decimal(float(v))) for v in x) + "\n"
open(out + '.txt', 'w').write(body)
ish = ", ".join(map(str, spec['ishape'])); osh = ", ".join(map(str, spec['oshape']))
open(out + '_v2.txt', 'w').write("sat\nX float32 [%s]\n%sY float32 [%s]\n%s" % (ish, body, osh, "\n".join(format(Decimal(float(v))) for v in y) + "\n"))
np.save(out + '.npy', x)


def marg(yv):
    yv = np.asarray(yv, dtype=np.float64)
    ms = [min(float(A[i] @ yv + b[i]) for i in range(len(b))) for A, b in spec['disjuncts']]
    k = int(np.argmax(ms)); return ms[k], k


print('snapped coordinates', fix, 'of', x.size)
print('onnxruntime f32 margin %.10g disjunct %d' % marg(y))
net = netload.torch_model(raw, 'cpu')
shape_b = list(spec['ishape'])
for dt in (torch.float32, torch.float64):
    m = net.to(dt)
    pre = []
    hooks = [mod.register_forward_hook(lambda mm, inp, o: pre.append(inp[0].detach().abs().min().item()))
             for mod in m.modules() if isinstance(mod, torch.nn.ReLU)]
    with torch.no_grad():
        yt = m(torch.from_numpy(x.astype(np.float64)).to(dt).reshape(shape_b)).reshape(-1).numpy()
    for h in hooks: h.remove()
    print('torch %s margin %.10g disjunct %d; min |ReLU input| per layer %s' % ((str(dt),) + marg(yt) + ([float('%.3g' % p) for p in pre],)))
print('max |ort - torch64| %.3g' % np.abs(y.astype(np.float64) - yt).max())
