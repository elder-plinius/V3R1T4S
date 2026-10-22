"""Standalone checker (Python standard library only), written from the IEA Wind Task 37 case study 1 definition:
- object/layout16.json and the xc/yc lists in object/iea37-v3r1t4s-opt16.yaml hold the same 16 coordinates;
- the YAML's sha256 matches the expected value;
- every hub within 1300 m of (0,0); every pair >= 2 rotor diameters (260 m); float64, no tolerance;
- AEP from the simplified Bastankhah Gaussian wake model (iea37-wakemodel.pdf: CT = 8/9, k = 0.0324555,
  sigma = k*dx + D/sqrt(8), deficit = (1 - sqrt(1 - CT/(8 sigma^2/D^2))) exp(-0.5 (dy/sigma)^2), root-sum-square
  superposition, 16-bin wind rose, 9.8 m/s, IEA 3.35 MW turbine) must exceed the record value given on the command line.
Usage: check_layout.py object/layout16.json object/iea37-v3r1t4s-opt16.yaml EXPECTED_SHA256 RECORD_VALUE"""
import sys, json, math, re, hashlib
jf, yf, sha, record = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
d = json.load(open(jf)); X, Y = [float(v) for v in d['x']], [float(v) for v in d['y']]
yb = open(yf, 'rb').read(); yt = yb.decode()
gx = [float(v) for v in re.search(r'xc: \[([^\]]*)\]', yt).group(1).split(',')]
gy = [float(v) for v in re.search(r'yc: \[([^\]]*)\]', yt).group(1).split(',')]
ok = True
if hashlib.sha256(yb).hexdigest() != sha: print('sha256 mismatch'); ok = False
if gx != X or gy != Y or len(X) != 16: print('coordinate mismatch between JSON and YAML (or not 16 turbines)'); ok = False
n = len(X)
mr = max(math.hypot(a, b) for a, b in zip(X, Y)); md = min(math.hypot(X[i]-X[j], Y[i]-Y[j]) for i in range(n) for j in range(i+1, n))
print('max_radius %r (limit 1300.0)  min_spacing %r (limit 260.0)' % (mr, md))
if not (mr <= 1300.0 and md >= 260.0): print('constraint violated'); ok = False
freq = [.025, .024, .029, .036, .063, .065, .100, .122, .063, .038, .039, .083, .213, .046, .032, .022]
U, D, ci, rws, co, P, ct, k = 9.8, 130.0, 4.0, 9.8, 25.0, 3.35e6, 8/9, 0.0324555
tot = 0.0
for b, fr in enumerate(freq):
    a = math.radians(270.0 - 22.5*b); c, s = math.cos(-a), math.sin(-a)
    xs = [X[i]*c - Y[i]*s for i in range(n)]; ys = [X[i]*s + Y[i]*c for i in range(n)]
    pw = 0.0
    for i in range(n):
        q = 0.0
        for j in range(n):
            dx = xs[i]-xs[j]
            if dx > 0:
                sg = k*dx + D/math.sqrt(8)
                q += ((1-math.sqrt(1-ct/(8*sg*sg/(D*D))))*math.exp(-0.5*((ys[i]-ys[j])/sg)**2))**2
        v = U*(1-math.sqrt(q))
        pw += P*((v-ci)/(rws-ci))**3 if ci <= v < rws else (P if rws <= v < co else 0.0)
    tot += fr*pw*8760/1e6
print('AEP %.5f MWh (record %.5f)' % (tot, record))
if not tot > record: print('not above the record'); ok = False
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
