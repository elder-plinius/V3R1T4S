#!/usr/bin/env python3
"""Scale every box of a spec by a factor and evaluate.  usage: scale.py spec K SIGMA factor [NT] [prec] [vecout]"""
import json, sys, os, subprocess
import opt
spec = json.load(open(sys.argv[1])); K = int(sys.argv[2]); sigma = sys.argv[3]; fac = float(sys.argv[4])
nt = int(sys.argv[5]) if len(sys.argv) > 5 else 6
if len(sys.argv) > 6: spec['prec'] = int(sys.argv[6])
for b in spec['boxes']: b['n'] = int(round(b['n'] * fac))
if len(sys.argv) > 7:
    base = sys.argv[7]; n = opt.write_basis(spec, base + '.txt')
    out = subprocess.run(['nice', os.path.join(opt.ENG, 'engine'), base + '.txt', 'eig', sigma, '8', base + '.vec'], capture_output=True, text=True, env=dict(os.environ, NT=str(nt))).stdout
    print(n, out.splitlines()[0]); print(out.splitlines()[-1])
else:
    print(sum(b['n'] for b in spec['boxes']), opt.evaluate(spec, K, sigma, nt=nt, niter=8))
