# Rigorous (mpmath.iv, outward) enclosures of the fixed sample points used by leaf records, written as doubles rounded outward.
# Sample sets (definition read from leaf fields disk_samples / r3_samples / r5_samples / reuleaux_samples):
#   disk(s):  0.5*(cos(2 pi k/s), sin(2 pi k/s)), k<s                       (points ON the disk of radius 1/2)
#   reul(n,s): for each vertex c_j of the regular n-gon of diameter 1 (circumradius 1/(2 sin(floor(n/2) pi/n))), k<s:
#              p = c_j + (1-1e-12)*(cos(2 pi k/s), sin(2 pi k/s)); kept iff |p-c_i|^2 <= 1 for ALL vertices c_i (interval upper bound <= 1)
#              => p lies in the intersection of the unit discs about the vertices = the regular Reuleaux n-gon of width 1.
import sys, math
from mpmath import iv
iv.prec = 200
def dn(x): return math.nextafter(float(x.a), -math.inf)
def up(x): return math.nextafter(float(x.b), math.inf)
def fmt(p): return ' '.join(repr(v) for v in (dn(p[0]), up(p[0]), dn(p[1]), up(p[1]), float(p[0].mid), float(p[1].mid)))
def disk(s):
    pi = iv.pi
    return [(iv.mpf('0.5') * iv.cos(2 * pi * k / s), iv.mpf('0.5') * iv.sin(2 * pi * k / s)) for k in range(s)]
def reul(n, s):
    pi = iv.pi
    R = 1 / (2 * iv.sin((n // 2) * pi / n))
    cs = [(R * iv.cos(2 * pi * j / n), R * iv.sin(2 * pi * j / n)) for j in range(n)]
    r = iv.mpf('0.999999999999')
    pts = []; rej = 0
    for c in cs:
        for k in range(s):
            th = 2 * pi * k / s
            p = (c[0] + r * iv.cos(th), c[1] + r * iv.sin(th))
            ok = all(((p[0] - d[0]) ** 2 + (p[1] - d[1]) ** 2).b <= 1 for d in cs)
            if ok: pts.append(p)
            else: rej += 1
    return pts, rej
if __name__ == '__main__':
    out = sys.argv[1]; sizes = [int(x) for x in sys.argv[2].split(',')]
    with open(out, 'w') as f:
        for n in (3, 5):
            pi = iv.pi; R = 1 / (2 * iv.sin((n // 2) * pi / n))
            cs = [(R * iv.cos(2 * pi * j / n), R * iv.sin(2 * pi * j / n)) for j in range(n)]
            f.write('cent %d %d\n' % (n, n))
            for c in cs: f.write(fmt(c) + '\n')
        for s in sizes:
            d = disk(s); f.write('disk 0 %d %d\n' % (s, len(d)))
            for p in d: f.write(fmt(p) + '\n')
            for n in (3, 5):
                pts, rej = reul(n, s); f.write('reul %d %d %d\n' % (n, s, len(pts)))
                for p in pts: f.write(fmt(p) + '\n')
                print('n=%d s=%d kept=%d rejected=%d' % (n, s, len(pts), rej))
        # constants: pi/5, pi/3 upper enclosures, as doubles
        pi = iv.pi
        f.write('const pi5_up %r pi3_up %r pi5_lo %r pi3_lo %r\n' % (up(pi / 5), up(pi / 3), dn(pi / 5), dn(pi / 3)))
