"""Write a layout JSON as an official-format IEA37 YAML (template: data/cs1-2/iea37-ex{n}.yaml), coordinates as full
float repr, with per-direction and total AEP from the official calculator filled in. Usage: to_yaml.py IN.json OUT.yaml"""
import sys, os, json, subprocess, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import DATA
d = json.load(open(sys.argv[1])); x, y = d['x'], d['y']; n = len(x); out = os.path.abspath(sys.argv[2])
t = open(os.path.join(DATA, 'iea37-ex%d.yaml' % n)).read()
t = re.sub(r'xc: \[[^\]]*\]', 'xc: [' + ', '.join(repr(float(v)) for v in x) + ']', t)
t = re.sub(r'yc: \[[^\]]*\]', 'yc: [' + ', '.join(repr(float(v)) for v in y) + ']', t)
t = t.replace('%d turbine example' % n, '%d turbine layout (V3R1T4S run)' % n)
open(out, 'w').write(t)
tmp = os.path.join(DATA, '_tmp_check.yaml'); open(tmp, 'w').write(t)
o = subprocess.run([sys.executable, 'iea37-aepcalc.py', '_tmp_check.yaml'], cwd=DATA, capture_output=True, text=True).stdout
os.remove(tmp)
lines = o.strip().split('\n'); total = lines[-1]; bins = ' '.join(lines[:-1]).strip()
t = re.sub(r'binned: \[[^\]]*\]', lambda m: 'binned: ' + bins, t)
t = re.sub(r'(binned: \[[^\]]*\]\s*\n\s*default: )[0-9.]+', lambda m: m.group(1) + total, t)
open(out, 'w').write(t)
print('official AEP', total)
