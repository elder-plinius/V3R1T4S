from flint import arb
import os
def load_row(n, path=None):
    path = path or os.environ.get('ICS_FILE', '../object/ics_row2.txt')
    for l in open(path):
        p = l.split()
        if p[0] == '%d)' % n:
            return [arb(x) for x in p[1:5]], p[1:5]
    raise KeyError(n)
def x0_of(vx, vy):
    z = vx * 0
    return [z - 1, z, z, z, z + 1, z, vx, vy, -2 * vx, -2 * vy, vx, vy]
def G_of(X):
    # (x2, y2, (v1 - v3) . q1)
    return [X[2], X[3], (X[6] - X[10]) * X[0] + (X[7] - X[11]) * X[1]]
