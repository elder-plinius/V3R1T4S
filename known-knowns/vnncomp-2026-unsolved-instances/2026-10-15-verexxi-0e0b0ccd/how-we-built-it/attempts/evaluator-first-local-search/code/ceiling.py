"""Compare the dense-layer (h4) patterns of all G >= -6 local optima: is G = -2 a structural ceiling?"""
import sys, os, glob, json
import numpy as np
sys.path.insert(0, 'attempts/exact-solver/code'); from bnn4864 import Net, parse_box
net = Net(glob.glob('data/onnx/3_48*')[0]); lo, hi, t = parse_box('data/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib.gz', (48, 48, 3)); net.setup_box(lo, hi, 9)
fs = [f for f in glob.glob('attempts/evaluator-first-local-search/out/**/model_48_idx_6371_eps_3*.json', recursive=True) + ['incumbent/model_48_idx_6371_eps_3_G-2.json']]
seen = {}; 
for f in fs:
    try: j = json.load(open(f))
    except Exception: continue
    if j.get('d') is None or int(j.get('eps', 3)) != 3 or j.get('G', -99) < -6: continue
    d = np.array(j['d']).reshape(48, 48, 3); seen.setdefault(d.tobytes(), (d, f))
D = np.array([v[0] for v in seen.values()]); o = net.forward(D)
dw = net.d2[:, 9] - net.d2[:, t]; idx = np.nonzero(dw)[0]
H = o['hd'][:, idx] * np.sign(dw[idx])          # +1 = unit on the helpful side
G = (o['L'][:, 9] - o['L'][:, t]).astype(int)
print('optima with G >= -6:', len(D), 'G values', sorted(G.tolist()))
right_all = (H == 1).all(0); wrong_all = (H == -1).all(0)
print('units with dw != 0:', len(idx), '| always right:', int(right_all.sum()), '| always wrong:', int(wrong_all.sum()), '| vary:', int((~right_all & ~wrong_all).sum()))
var = np.nonzero(~right_all & ~wrong_all)[0]
print('varying units (index: fraction right):', {int(idx[k]): round(float((H[:, k] == 1).mean()), 2) for k in var})
if len(var) > 1:
    C = np.corrcoef(H[:, var].T); np.fill_diagonal(C, 0)
    print('most anti-correlated pairs among varying units:', sorted([(round(float(C[a, b]), 2), int(idx[var[a]]), int(idx[var[b]])) for a in range(len(var)) for b in range(a + 1, len(var))])[:5])
print('per optimum with G = -2: varying-unit status (R/W) and signed distance to the helpful side (u units)')
V = [26, 74, 101, 109, 116, 147, 150, 209]
for k in np.nonzero(G == -2)[0]:
    u = o['u'][k]; q = np.where(net.posd, u - net.Td, net.Td - u) * np.sign(dw)  # >= 0 means helpful side
    print(' ', ' '.join(f'{j}:{"R" if q[j] >= 0 else "W"}{q[j]:+.0f}' for j in V), '|', os.path.relpath(list(seen.values())[k][1])[-60:])
