# Independent sanity check of the sample-point tables: every enclosure [lo,hi] must contain the 90-digit mpmath.mp value of the point
# (computed with plain mp arithmetic, a different code path from mpmath.iv), and the exact membership inequality |p-c_i|^2 <= 1 must hold at 50 digits.
import sys
from mpmath import mp, mpf, cos, sin, pi
mp.dps = 90
lines = open(sys.argv[1]).read().split('\n'); i = 0; bad = 0; npts = 0; sets = 0
cent = {}
while i < len(lines):
    f = lines[i].split()
    if not f or f[0] == 'const': i += 1; continue
    if f[0] == 'cent':
        n = int(f[1]); R = 1 / (2 * sin((n // 2) * pi / n)); cent[n] = [(R * cos(2 * pi * j / n), R * sin(2 * pi * j / n)) for j in range(n)]
        for j in range(n):
            v = list(map(float, lines[i + 1 + j].split())); c = cent[n][j]
            ok = mpf(v[0]) <= c[0] <= mpf(v[1]) and mpf(v[2]) <= c[1] <= mpf(v[3]); bad += (not ok)
        i += 1 + n; continue
    kind, a, s, cnt = f[0], int(f[1]), int(f[2]), int(f[3]); sets += 1
    P = [list(map(float, lines[i + 1 + j].split())) for j in range(cnt)]
    if kind == 'disk':
        for k, v in enumerate(P):
            t = 2 * pi * k / s; x = mpf('0.5') * cos(t); y = mpf('0.5') * sin(t); npts += 1
            bad += not (mpf(v[0]) <= x <= mpf(v[1]) and mpf(v[2]) <= y <= mpf(v[3]))
    else:
        # reconstruct the kept points in order (centre-major) and compare 1:1
        r = mpf('0.999999999999'); kept = []
        for c in cent[a]:
            for k in range(s):
                t = 2 * pi * k / s; x = c[0] + r * cos(t); y = c[1] + r * sin(t)
                if all((x - d[0]) ** 2 + (y - d[1]) ** 2 <= 1 for d in cent[a]): kept.append((x, y))
        assert len(kept) == cnt, (a, s, len(kept), cnt)
        for (x, y), v in zip(kept, P):
            npts += 1; bad += not (mpf(v[0]) <= x <= mpf(v[1]) and mpf(v[2]) <= y <= mpf(v[3]))
    i += 1 + cnt
print('sets', sets, 'points', npts, 'enclosure violations', bad)
