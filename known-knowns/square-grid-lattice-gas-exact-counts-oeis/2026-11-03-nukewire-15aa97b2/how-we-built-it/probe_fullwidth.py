"""Full-width probe: run_dp_sliced(28, A-prime #1); every column total must equal
Run A's saved residue (p_A1, k=j, j=28) for j=1..27, and a(28) mod p for j=28."""
import os, sys, time, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runB_chunked import run_dp_sliced

P = 2305843009214693957  # set-A prime #1
want = {}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runA_residues.txt'),
                 encoding='utf-8'):
    if line.startswith('p='):
        f = dict(t.split('=') for t in line.split())
        if int(f['p']) == P and int(f['j']) == 28:
            want[int(f['k'])] = int(f['r'])
a28 = int(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-record-we-beat', '' + '
               r'a28_anchor.txt')).read().strip())
want[28] = a28 % P
t0 = time.time()
tot = run_dp_sliced(28, P)
dtl = time.time() - t0
bad = 0
for j in range(1, 29):
    got = int(tot[j - 1])
    if got != want[j]:
        bad += 1
        print(f"MISMATCH j={j}: sliced={got} runA={want[j]}", flush=True)
print(f"PROBE {'PASS' if bad == 0 else 'FAIL'}: 28/28 columns match Run A "
      f"(prime {P}) in {dtl:.0f}s [{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%SZ')}]",
      flush=True)
