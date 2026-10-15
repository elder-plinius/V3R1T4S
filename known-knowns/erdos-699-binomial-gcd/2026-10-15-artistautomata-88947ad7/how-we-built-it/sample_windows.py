"""Sampler lens: fast699 (independent code) vs seg699 on 300 windows of 2,000 consecutive n, starts drawn by
random.Random(699).randrange(100000, 999998000) as frozen in PREREG.md. Per window: fast699's nontrivial_i must equal
seg699's cases, and both must report candidates=0. Writes one line per window and a summary."""
import random, re, subprocess, sys
SEG = '../scanner/code/seg699'; FAST = './code/fast699'
rng = random.Random(699); starts = [rng.randrange(100000, 999998000) for _ in range(300)]
def done(out):
    return dict(re.findall(r'(\w+)=(\d+)', [l for l in out.splitlines() if l.startswith('DONE')][0]))
bad = 0
with open('out/windows.txt', 'w') as f:
    for k, a in enumerate(starts):
        b = a + 1999
        s = done(subprocess.run(['nice', '-n', '10', SEG, str(a), str(b), '0'], capture_output=True, text=True, check=True).stdout)
        g = done(subprocess.run(['nice', '-n', '10', FAST, str(a), str(b), '0'], capture_output=True, text=True, check=True).stdout)
        ok = s['cases'] == g['nontrivial_i'] and s['candidates'] == '0' and g['candidates'] == '0' and g['fallbacks'] == '0'
        bad += not ok
        f.write('%d %d-%d seg cases=%s cand=%s | fast nontrivial_i=%s cand=%s fallbacks=%s | %s\n' % (
            k, a, b, s['cases'], s['candidates'], g['nontrivial_i'], g['candidates'], g['fallbacks'], 'AGREE' if ok else 'DISAGREE'))
        f.flush()
    f.write('SUMMARY windows=%d disagree=%d\n' % (len(starts), bad))
print('windows=%d disagree=%d' % (len(starts), bad))
