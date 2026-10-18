"""Run ice.exe in modes A and B for n = lo..hi, CRT-combine residues, compare with the OEIS b-file, append JSON lines."""
import subprocess, sys, json, time, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
RUN = HERE.parents[2]
primes = {l.split()[0]: [int(x) for x in l.split()[1:]] for l in (RUN / 'primes.txt').read_text().splitlines()}
bfile = {int(l.split()[0]): int(l.split()[1]) for l in (RUN / 'data/b054759.txt').read_text().splitlines()
         if l.strip() and not l.startswith('#')}

def crt(res):
    x, m = 0, 1
    for p, r in res:
        t = ((r - x) * pow(m, -1, p)) % p
        x, m = x + m * t, m * p
    return x, m

def run(mode, n, threads):
    t0 = time.time()
    out = subprocess.run([str(HERE / 'ice.exe'), mode, str(n), str(threads)] + [str(p) for p in primes[mode]],
                         capture_output=True, text=True, check=True)
    res = [tuple(int(v) for v in l.split()) for l in out.stdout.split('\n') if l.strip()]
    assert [p for p, _ in res] == primes[mode]
    x, m = crt(res)
    return {'mode': mode, 'residues': [str(r) for _, r in res], 'value': str(x), 'modulus_digits': len(str(m)),
            'seconds': round(time.time() - t0, 2), 'log': out.stderr.strip()}

if __name__ == '__main__':
    lo, hi, threads = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    W = (4 / 3) ** 1.5
    with open(RUN / 'attempts/transfer_matrix/results.jsonl', 'a') as f:
        for n in range(lo, hi + 1):
            a, b = run('A', n, threads), run('B', n, threads)
            v = int(a['value'])
            row = {'n': n, 'A': a, 'B': b, 'A_equals_B': a['value'] == b['value'],
                   'published': str(bfile[n]) if n in bfile else None,
                   'matches_published': (bfile[n] == v) if n in bfile else None,
                   'digits': len(str(v)), 'root': v ** (1 / n ** 2) if v.bit_length() < 1000 else None,
                   'W_lieb': W}
            row['headroom_ok'] = len(str(v)) + 6 < min(a['modulus_digits'], b['modulus_digits'])
            f.write(json.dumps(row) + '\n'); f.flush()
            print(n, v, 'A==B' if row['A_equals_B'] else 'A!=B', 'pub:', row['matches_published'],
                  'tA', a['seconds'], 'tB', b['seconds'], flush=True)
