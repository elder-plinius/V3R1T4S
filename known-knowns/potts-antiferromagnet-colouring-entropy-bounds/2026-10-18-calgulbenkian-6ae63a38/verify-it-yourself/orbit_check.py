"""Format validation on a small certificate: rebuild the S_q x D_m orbit quotient of the proper q-colourings
of the cycle C_m independently, number the orbits by first appearance in lexicographic order of colourings,
and test that the file's y equals (quotient transfer matrix) applied to the file's v, exactly in integers.
usage: orbit_check.py CERT.bin Q M [lsb|msb]"""
import sys, struct, itertools
path, q, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
order = sys.argv[4] if len(sys.argv) > 4 else 'msb'
raw = open(path, 'rb').read()
n = struct.unpack('<I', raw[:4])[0]
v = [int.from_bytes(raw[4+32*i:36+32*i], 'little') for i in range(n)]
y = [int.from_bytes(raw[4+32*n+32*i:36+32*n+32*i], 'little') for i in range(n)]
def canon(w):
    best = None
    for r in range(m):
        for rev in (0, 1):
            u = w[r:] + w[:r]
            if rev: u = u[::-1]
            mp = {}; out = []
            for c in u:
                if c not in mp: mp[c] = len(mp)
                out.append(mp[c])
            out = tuple(out)
            if best is None or out < best: best = out
    return best
cols = [w for w in itertools.product(range(q), repeat=m) if all(w[i] != w[(i+1) % m] for i in range(m))]
if order == 'lsb': cols.sort(key=lambda w: w[::-1])
orb = {}; reps = []
for w in cols:
    c = canon(w)
    if c not in orb: orb[c] = len(orb); reps.append(w)
print('orbits found: %d, file has %d' % (len(orb), n))
if len(orb) != n: print('ORBIT CHECK FAILED (count)'); sys.exit(1)
allv = {w: v[orb[canon(w)]] for w in cols}
good = True
for i, r in enumerate(reps):
    s = sum(allv[w2] for w2 in cols if all(w2[k] != r[k] for k in range(m)))
    if s != y[i]: good = False
print('ORBIT CHECK OK: y = C v holds exactly for all %d orbits' % n if good else 'ORBIT CHECK FAILED (y != C v under this numbering)')
sys.exit(0 if good else 1)
