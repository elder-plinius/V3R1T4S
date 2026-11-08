"""Export the trained VarBench state (PyTorch checkpoint r10_J0.9_B1.pt) to one self-contained ONNX file.

  python export_onnx.py CKPT NQS_DIR OUT_DIR

CKPT is the checkpoint the panel reviewed (sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485),
NQS_DIR the folder holding the nqs.py it was trained with (how-we-built-it/nqs.py is that file).  Writes to OUT_DIR:
  r10_J0.9_B1.onnx                  the state: input spins [batch, 100] float32, outputs log_abs_psi [batch] and
                                    phase [batch] (radians, in (-pi, pi]), float32, standard ONNX operators, opset 17
  r10_J0.9_B1.reference_values.csv  100 random Sz = 0 configurations (seed 20261108) with log|psi| and phase from the
                                    trained model's own forward pass (nqs.NQS.forward, GPU, float32)
  export_report.json                agreement of the ONNX file (onnxruntime, CPU) with that forward pass and with the
                                    measurement code (estimator2.NQSWave), which sums the 16 images in float64

The exported graph is the model's forward pass as trained: the periodic ResNet on all 16 images g s of the
configuration (C4v about site 0 times global spin flip), the stripe sign rule and the B1 characters added as phases,
and the sum over images, all in float32.  It differs from nqs.NQS.forward only in using -1 in its reshapes, so that the
batch size stays free.  (A float64 image sum, as in estimator2, is not possible with standard operators that
onnxruntime runs on the CPU: it has no float64 Cos.)
"""
import hashlib, json, math, os, sys
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

CKPT, NQS_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, NQS_DIR)
import nqs, estimator2

L, N = 10, 100
SEED = 20261108
OPSET = 17


class Exported(nn.Module):
    def __init__(s, m):
        super().__init__()
        s.net = m.net
        for b in ('perms', 'flips', 'chphase', 'prior_mask'):
            s.register_buffer(b, getattr(m, b).detach().clone())
        s.G = m.perms.shape[0]

    def resnet(s, x):  # x (M, N) -> (M, 2)
        h = s.net.inp(x.reshape(-1, 1, L, L))
        for b in s.net.blocks:
            h = b(h)
        return s.net.head(F.gelu(h)).sum((2, 3))

    def forward(s, x):  # x (B, N) float32, +1 = up, -1 = down
        xs = (x[:, s.perms] * s.flips[None, :, None]).reshape(-1, N)          # (B*G, N), images g s
        out = s.resnet(xs).reshape(-1, s.G, 2)
        a = out[..., 0]
        nup_odd = (((1.0 + xs) * 0.5) @ s.prior_mask).reshape(-1, s.G)        # up spins on odd columns
        ph = out[..., 1] + math.pi * nup_odd + s.chphase[None, :]
        m = a.max(1, keepdim=True).values
        e = torch.exp(a - m)
        re = (e * torch.cos(ph)).sum(1); im = (e * torch.sin(ph)).sum(1)
        return m[:, 0] + 0.5 * torch.log(re * re + im * im), torch.atan2(im, re)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def random_sz0(n, rng):
    x = np.full((n, N), -1.0, np.float32)
    for i in range(n):
        x[i, rng.permutation(N)[:N // 2]] = 1.0
    return x


def angdiff(a, b):
    return np.abs(np.angle(np.exp(1j * (np.asarray(a, np.float64) - np.asarray(b, np.float64)))))


os.makedirs(OUT, exist_ok=True)
rep = dict(checkpoint_sha256=sha(CKPT), nqs_py_sha256=sha(os.path.join(NQS_DIR, 'nqs.py')), opset=OPSET,
           torch=torch.__version__)
model, d = nqs.load_ckpt(CKPT, 'cuda')
model.eval()
rep['config'] = model.cfg; rep['step'] = d['opt_state']['step']; rep['parameters'] = nqs.nparams(model)
gpu = Exported(model).eval()

rng = np.random.default_rng(SEED)
xt = random_sz0(100, rng)
xv = random_sz0(1000, rng)                 # a second, larger set for the agreement figures
wave = estimator2.NQSWave(model)


def measured(x):  # (log|psi|, phase) as the measurements computed them, and how much the 16 image terms cancel
    xx = torch.tensor(x, device='cuda')
    lp = wave.logs(xx)[0].cpu().numpy()
    a, ph = wave.images(xx)
    e = torch.exp(a - a.max(1, keepdim=True).values)
    canc = ((e * torch.exp(1j * ph)).sum(1).abs() / e.sum(1)).cpu().numpy()
    return np.stack([lp.real, lp.imag], 1), canc


with torch.no_grad():
    ref_t = model(torch.tensor(xt, device='cuda')).double().cpu().numpy()
    ref_v = model(torch.tensor(xv, device='cuda')).double().cpu().numpy()
    meas_v, canc_v = measured(xv)
    la, ph = gpu(torch.tensor(xv, device='cuda'))
rep['wrapper_vs_model_gpu'] = dict(max_abs_log_abs=float(np.abs(la.double().cpu().numpy() - ref_v[:, 0]).max()),
                                   max_phase=float(angdiff(ph.double().cpu().numpy(), ref_v[:, 1]).max()))
rep['model_vs_measurement_code_gpu'] = dict(max_abs_log_abs=float(np.abs(ref_v[:, 0] - meas_v[:, 0]).max()),
                                            max_phase=float(angdiff(ref_v[:, 1], meas_v[:, 1]).max()))

cpu = Exported(nqs.load_ckpt(CKPT, 'cpu')[0].eval()).eval().cpu()
onnx_path = os.path.join(OUT, 'r10_J0.9_B1.onnx')
torch.onnx.export(cpu, (torch.tensor(xt[:4]),), onnx_path, dynamo=False, opset_version=OPSET,
                  do_constant_folding=True, input_names=['spins'], output_names=['log_abs_psi', 'phase'],
                  dynamic_axes={'spins': {0: 'batch'}, 'log_abs_psi': {0: 'batch'}, 'phase': {0: 'batch'}})

import onnx, onnxruntime as ort
mo = onnx.load(onnx_path)
mo.doc_string = ''; mo.producer_name = 'pytorch'
for n in mo.graph.node:
    n.doc_string = ''
onnx.save(mo, onnx_path)                   # one file, no external data
onnx.checker.check_model(onnx_path, full_check=True)
mo = onnx.load(onnx_path)
rep['onnx'] = dict(sha256=sha(onnx_path), bytes=os.path.getsize(onnx_path), ir_version=mo.ir_version,
                   opsets={o.domain or 'ai.onnx': o.version for o in mo.opset_import},
                   op_types=sorted({n.op_type for n in mo.graph.node}),
                   node_domains=sorted({n.domain or 'ai.onnx' for n in mo.graph.node}),
                   external_initializers=sum(1 for t in mo.graph.initializer
                                             if t.data_location == onnx.TensorProto.EXTERNAL),
                   inputs=[(i.name, [dd.dim_param or dd.dim_value for dd in i.type.tensor_type.shape.dim])
                           for i in mo.graph.input],
                   outputs=[(o.name, [dd.dim_param or dd.dim_value for dd in o.type.tensor_type.shape.dim])
                            for o in mo.graph.output],
                   onnxruntime=ort.__version__, onnx=onnx.__version__)

so = ort.SessionOptions(); so.intra_op_num_threads = 2; so.inter_op_num_threads = 1
sess = ort.InferenceSession(onnx_path, so, providers=['CPUExecutionProvider'])
agree = {}
for bs in (1, 7, 100, 333):
    la_o, ph_o = sess.run(None, {'spins': xv[:bs]})
    agree[str(bs)] = dict(max_abs_log_abs=float(np.abs(la_o - ref_v[:bs, 0]).max()),
                          max_phase=float(angdiff(ph_o, ref_v[:bs, 1]).max()))
la_o, ph_o = sess.run(None, {'spins': xv})
worst = int(np.argmax(np.abs(la_o - ref_v[:, 0])))
rep['onnx_cpu_vs_measurement_code_gpu'] = dict(max_abs_log_abs=float(np.abs(la_o - meas_v[:, 0]).max()),
                                               max_phase=float(angdiff(ph_o, meas_v[:, 1]).max()))
rep['cancellation'] = dict(
    note='|sum_g e_g exp(i ph_g)| / sum_g e_g over the 16 images, float64; small = strong cancellation',
    median=float(np.median(canc_v)), at_worst_onnx_vs_model_row=float(canc_v[worst]),
    worst_row_abs_diffs=dict(onnx_vs_model=float(abs(la_o[worst] - ref_v[worst, 0])),
                             onnx_vs_measurement_code=float(abs(la_o[worst] - meas_v[worst, 0])),
                             model_vs_measurement_code=float(abs(ref_v[worst, 0] - meas_v[worst, 0]))))
agree['1000'] = dict(max_abs_log_abs=float(np.abs(la_o - ref_v[:, 0]).max()),
                     max_phase=float(angdiff(ph_o, ref_v[:, 1]).max()),
                     log_abs_range=[float(ref_v[:, 0].min()), float(ref_v[:, 0].max())],
                     phase_mod_pi_range=[float(np.mod(ref_v[:, 1], np.pi).min()), float(np.mod(ref_v[:, 1], np.pi).max())])
rep['onnx_cpu_vs_model_gpu'] = agree

with open(os.path.join(OUT, 'r10_J0.9_B1.reference_values.csv'), 'w') as f:
    f.write('index,spins,log_abs_psi,phase\n')
    for i in range(len(xt)):
        f.write('%d,%s,%.12f,%.12f\n' % (i, ''.join('u' if v > 0 else 'd' for v in xt[i]), ref_t[i, 0], ref_t[i, 1]))
la_o, ph_o = sess.run(None, {'spins': xt})
rep['table'] = dict(rows=len(xt), seed=SEED, max_abs_log_abs=float(np.abs(la_o - ref_t[:, 0]).max()),
                    max_phase=float(angdiff(ph_o, ref_t[:, 1]).max()),
                    phase_mod_pi_range=[float(np.mod(ref_t[:, 1], np.pi).min()), float(np.mod(ref_t[:, 1], np.pi).max())])
json.dump(rep, open(os.path.join(OUT, 'export_report.json'), 'w'), indent=1)
print(json.dumps(rep, indent=1))
