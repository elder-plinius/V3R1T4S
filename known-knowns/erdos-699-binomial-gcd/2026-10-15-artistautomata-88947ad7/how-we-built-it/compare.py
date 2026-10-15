"""Run third699 on the 200 n of PREREG (random.Random(6990).randrange(10**8, 10**9)) and seg699 on [n, n]; compare."""
import re, subprocess, sys
sys.path.insert(0, 'code'); import third699 as t, random
rng = random.Random(6990); ns = [rng.randrange(10**8, 10**9) for _ in range(200)]; bad = 0
with open('compare_output.txt', 'w') as f:
    for n in ns:
        c, k = t.one(n)
        o = subprocess.run(['nice', '-n', '10', '../scanner/code/seg699', str(n), str(n), '0'], capture_output=True, text=True, check=True).stdout
        d = dict(re.findall(r'(\w+)=(\d+)', [l for l in o.splitlines() if l.startswith('DONE')][0]))
        ok = int(d['cases']) == c and k == 0 and d['candidates'] == '0'; bad += not ok
        f.write('n=%d third cases=%d cand=%d | seg cases=%s cand=%s | %s\n' % (n, c, k, d['cases'], d['candidates'], 'AGREE' if ok else 'DISAGREE')); f.flush()
    f.write('SUMMARY n=%d disagree=%d\n' % (len(ns), bad))
