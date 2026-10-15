#!/usr/bin/env python3
"""Run the competition's own validator, unmodified, on ../object/witness_v2.txt.
Downloads SCORING/counterexamples_v2.py, benchmark_instances.py and cex_checks.py from the live VNN-COMP 2026 results
repo and the benchmark files (sha256 pinned), then calls validate_vnnlib2_counterexample at abs_tol 0 and 1e-4.
Requires: numpy, onnx, onnxruntime, vnnlib==1.0.2.  Usage: python3 official_validate.py [--cache DIR]
Expected: ('correct', '... all assertions hold with input_tolerance=0.0, output_tolerance=0.0') twice."""
import argparse, hashlib, os, sys, tempfile, urllib.request
from pathlib import Path
R = 'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING'
B = 'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/main/benchmarks/traffic_signs_recognition_2023/2.0'
N = '3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30'
FILES = {f'{R}/counterexamples_v2.py': ('SCORING/counterexamples_v2.py', '5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab'),
         f'{R}/benchmark_instances.py': ('SCORING/benchmark_instances.py', '5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229'),
         f'{R}/cex_checks.py': ('SCORING/cex_checks.py', '695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5'),
         f'{B}/onnx/{N}.onnx.gz': (f'bench/onnx/{N}.onnx.gz', '6f4969db9cea8c278049dc45933485e0b455fba5e2524b7ac307056e1a0b9e6e'),
         f'{B}/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib.gz': ('bench/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib.gz', 'd5f96951d9259ede11b37cc8622e5b12b6e180078c63f4ec4cfab7bb07e5168c')}
class ResultType:
    CORRECT = 'correct'; CORRECT_UP_TO_TOLERANCE = 'correct_up_to_tolerance'; SPEC_NOT_VIOLATED = 'spec_not_violated'
    NO_CE = 'no_ce'; MALFORMED_CE = 'malformed_ce'; UNSUPPORTED = 'unsupported'
ap = argparse.ArgumentParser(); ap.add_argument('--cache', default=None); a = ap.parse_args()
c = a.cache or tempfile.mkdtemp(prefix='vnn-official-')
for url, (rel, pin) in FILES.items():
    p = os.path.join(c, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.isfile(p):
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'V3R1T4S-verify'}), timeout=120) as r, open(p, 'wb') as f:
            f.write(r.read())
    got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    print(rel, 'sha256', 'OK' if got == pin else 'MISMATCH ' + got)
    if got != pin: sys.exit('stopping: file does not match the pinned sha256')
sys.path.insert(0, os.path.join(c, 'SCORING'))
import counterexamples_v2 as cv2
ce = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'object', 'witness_v2.txt')
for tol in (0.0, 1e-4):
    print(f'abs_tol={tol}:', cv2.validate_vnnlib2_counterexample(Path(c) / 'bench', f'onnx/{N}.onnx', 'vnnlib/model_48_idx_6371_eps_3.00000.vnnlib', ce, tol, 0.0, ResultType))
