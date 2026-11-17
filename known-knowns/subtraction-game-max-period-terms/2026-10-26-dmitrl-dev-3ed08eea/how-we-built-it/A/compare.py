"""Compare A and B outputs for one (mode, n). Usage: compare.py FILE_A FILE_B"""
import sys, json
def parse(p):
    L = open(p).read().splitlines(); h = L[0].split()
    mx = int(h[h.index("max") + 1]); st = [int(x) for x in h[h.index("set") + 1:]]
    hist = {}
    for l in L[1:]:
        if l.startswith("overflow"):
            assert l.split()[1] == "0"; continue
        k, v = l.split(); hist[int(k)] = int(v)
    return mx, st, hist
a, b = parse(sys.argv[1]), parse(sys.argv[2])
r = dict(max_A=a[0], max_B=b[0], set_A=a[1], set_B=b[1], max_equal=a[0] == b[0], set_equal=a[1] == b[1],
         hist_equal=a[2] == b[2], sets_A=sum(a[2].values()), sets_B=sum(b[2].values()), distinct_periods=len(a[2]))
print(json.dumps(r))
