#!/usr/bin/env python3
"""Run the competition's own validator, unmodified, on ../object/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000_v2.counterexample.
Fetches SCORING/counterexamples_v2.py, benchmark_instances.py and cex_checks.py from the VNN-COMP 2026 results repo
(commit eea564f5) and the two benchmark files (sha256 pinned; both from GitHub), once each, into --cache (default: $VNN_CACHE or a temporary folder); then calls
validate_vnnlib2_counterexample at abs_tol 0 and 1e-4.
Requires: numpy, onnx, onnxruntime, vnnlib==1.0.2.  Usage: python3 official_validate.py [--cache DIR]
Expected: ('correct', '... all assertions hold with input_tolerance=0.0, output_tolerance=0.0') twice."""
import argparse, hashlib, os, sys, tempfile, urllib.request
from pathlib import Path
R = 'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING'
B = 'https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0'
P = 'model_64_idx_6371_eps_1.00000.vnnlib'
FILES = {f'{R}/counterexamples_v2.py': ('SCORING/counterexamples_v2.py', '5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab'),
         f'{R}/benchmark_instances.py': ('SCORING/benchmark_instances.py', '5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229'),
         f'{R}/cex_checks.py': ('SCORING/cex_checks.py', '695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5'),
         f'{B}/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz': ('bench/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz', '818d676e69caadeb1c9044b9b6aa7d9896dfd2101842918869f9b291a9539b85'),
         f'{B}/vnnlib/{P}.gz': (f'bench/vnnlib/{P}.gz', '16efc2694a75e6595816806ff4cf168214e8a5ec368757dad7dc896033658b84')}
ALIAS = {'bench/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz': '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx.gz',
         f'bench/vnnlib/{P}.gz': 'model_64_idx_6371_eps_1.00000.vnnlib.gz'}   # names used by check.py's cache


class ResultType:
    CORRECT = 'correct'; CORRECT_UP_TO_TOLERANCE = 'correct_up_to_tolerance'; SPEC_NOT_VIOLATED = 'spec_not_violated'
    NO_CE = 'no_ce'; MALFORMED_CE = 'malformed_ce'; UNSUPPORTED = 'unsupported'


ap = argparse.ArgumentParser(); ap.add_argument('--cache', default=os.environ.get('VNN_CACHE')); a = ap.parse_args()
c = a.cache or tempfile.mkdtemp(prefix='vnn-official-')
for url, (rel, pin) in FILES.items():
    p = os.path.join(c, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    flat = os.path.join(c, ALIAS.get(rel, '-'))
    if not os.path.isfile(p) and os.path.isfile(flat):
        open(p, 'wb').write(open(flat, 'rb').read())
    if not os.path.isfile(p):
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'V3R1T4S-verify'}), timeout=1800) as r, open(p, 'wb') as f:
            f.write(r.read())
    got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    print(rel, 'sha256', 'OK' if got == pin else 'MISMATCH ' + got)
    if got != pin: sys.exit('stopping: file does not match the pinned sha256')
sys.path.insert(0, os.path.join(c, 'SCORING'))
import counterexamples_v2 as cv2
ce = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'object', '3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000_v2.counterexample')
for tol in (0.0, 1e-4):
    print(f'abs_tol={tol}:', cv2.validate_vnnlib2_counterexample(Path(c) / 'bench', 'onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx', 'vnnlib/' + P, ce, tol, 0.0, ResultType))
