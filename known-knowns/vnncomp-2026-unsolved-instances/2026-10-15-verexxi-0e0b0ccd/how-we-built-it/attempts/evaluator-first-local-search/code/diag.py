"""Diagnostic: at a checkpoint, list the dense units whose flip would raise L_c - L_t and their distance (in u units)."""
import sys, os, json, glob
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'exact-solver', 'code'))
from bnn4864 import Net, parse_box
data, inst, ck = sys.argv[1:4]
tag = inst.split('_')[1]; net = Net(glob.glob(f'{data}/onnx/3_{tag}_*.onnx.gz')[0]); S = net.S
lo, hi, tgt = parse_box(f'{data}/vnnlib/{inst}.00000.vnnlib.gz', (S, S, 3)); net.setup_box(lo, hi, 9)
j = json.load(open(ck)); d = np.array(j['d']).reshape(1, S, S, 3); c = j['cls']
o = net.forward(d); L = o['L'][0]
dw = net.d2[:, c] - net.d2[:, tgt]
want = np.sign(dw); h = o['hd'][0]
wrong = (dw != 0) & (h != want)
# distance: h=+1 iff (u >= Td if posd else u <= Td); u moves by 2 per h3 flip
u = o['u'][0]; dist = np.abs(u - net.Td) / 2
print('G', L[c] - L[tgt], 'n dw!=0', int((dw != 0).sum()), 'wrong', int(wrong.sum()), 'need flips', int(np.ceil((2 - (L[c] - L[tgt])) / 4)))
print('wrong-unit h3-flip distances (sorted):', np.sort(dist[wrong])[:15].round(1))
print('right-unit distances (sorted):', np.sort(dist[(dw != 0) & ~wrong])[:10].round(1))
print('h3 |a3| < 0.5:', int((np.abs(o['a3']) < 0.5).sum()), 'of', o['a3'].size)
print('n changed pixels', int((d != 0).sum()))
