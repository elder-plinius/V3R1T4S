"""Replay of the bank scan's union-free probe (unionfree_probe.py, copied unchanged from the scan's deep-check work
folder; contributor code from the scan). Runs its three seed modes and saves the best family found.
  python3 replay.py n seconds out.txt"""
import sys
from scan_unionfree_probe import run, verify
n, secs, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
best = (0, None)
for mode in ('middle', 'greedy', 'empty'):
    b, F, st = run(n, mode, secs)
    ok, bad = verify(F, n)
    print('n=%d seed=%s best=%d valid=%s steps=%d' % (n, mode, b, ok, st), flush=True)
    if ok and b > best[0]: best = (b, F)
F = best[1]
with open(out, 'w') as f:
    f.write('# union-free family on {1..%d}, %d members, from the scan probe replay\n' % (n, len(F)))
    for S in sorted(F, key=lambda x: (bin(x).count('1'), [i + 1 for i in range(n) if x >> i & 1])):
        f.write(' '.join(str(i + 1) for i in range(n) if S >> i & 1) + '\n')
print('best', best[0])
