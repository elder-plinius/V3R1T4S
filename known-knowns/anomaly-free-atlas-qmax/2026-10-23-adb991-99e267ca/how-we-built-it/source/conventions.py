# Evaluate counting conventions against the published counts, from count's output file and fix.py.
import sys, re
from fix import fix
def mu(n):
    r, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
def load(path):
    N = {}
    for line in open(path):
        m = re.match(r"N (\d+) (\d) (\d+)", line)
        if m: N[int(m.group(1))] = int(m.group(3))
    return N
def conv(N, nu, Q):
    F = {q: fix(q, nu) for q in N0} if False else None
    N0 = dict(N); N0[0] = 1
    F = {q: fix(q, nu) for q in N0}
    N0 = dict(N); N0[0] = 1
    cls = {q: (N0[q] + F[q]) // 2 for q in N0}          # sign classes incl zero (Burnside)
    assert all((N0[q] + F[q]) % 2 == 0 for q in N0)
    prim = sum(mu(d) * (cls[Q // d] - 1) for d in range(1, Q+1))   # primitive nonzero classes
    return {"all_incl0": cls[Q], "all_excl0": cls[Q]-1, "prim_excl0": prim, "prim_incl0": prim+1,
            "nosign_all_excl0": N0[Q]-1}
if __name__ == "__main__":
    N = load(sys.argv[1]); nu = int(sys.argv[2])
    pub = {1: 8, 3: 82, 5: 626, 7: 3902, 10: 23800} if nu == 0 else {6: 435305, 7: 1358388, 8: 3612734, 9: 9587085, 10: 21546920}
    for Q in sorted(N):
        print(Q, conv(N, nu, Q), "published:", pub.get(Q, "-"))
