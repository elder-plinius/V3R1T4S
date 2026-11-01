"""Check cumulative sieved prime counts at window ends against primecount. usage: verify_counts.py out_dir step [threads]"""
import sys, csv, subprocess, time
out, step = sys.argv[1], int(sys.argv[2]); th = sys.argv[3] if len(sys.argv) > 3 else '2'
PC = 'primecount'
A = 1_500_000_000_000_000
def pi(x):
    return int(subprocess.run([PC, str(x), '-t', th], capture_output=True, text=True).stdout.strip())
rows = list(csv.DictReader(open(out + '/windows.csv')))
base = pi(A - 1)
NB = 1 << 30
res = []; bad = 0
sel = [r for r in rows if int(r['w']) % step == 0] + [rows[-1]]
seen = set()
for r in sel:
    w = int(r['w'])
    if w in seen: continue
    seen.add(w)
    hi = int(r['lo']) + 2*NB - 2          # last odd number sieved in window w
    got = int(r['cum_primes'])
    exp = pi(hi) - base - 0               # primes in [A, hi]; 2 is below A
    ok = got == exp
    bad += (not ok)
    print(f'w={w} hi={hi} sieved={got} primecount={exp} ok={ok}', flush=True)
print('windows checked', len(seen), 'mismatches', bad)
