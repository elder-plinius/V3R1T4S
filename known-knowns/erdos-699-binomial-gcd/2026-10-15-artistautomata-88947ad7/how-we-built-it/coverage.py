"""Check that the finished seg699 chunks cover every n in [4, 10^9] contiguously, each with candidates=0, overflow=0
and no ERROR line; print totals."""
import glob, re
iv, bad, cases, enum = [], [], 0, 0
for f in glob.glob('chunks/s_*.txt'):
    t = open(f).read(); d = dict(re.findall(r'(\w+)=(\d+)', [l for l in t.splitlines() if l.startswith('DONE')][0]))
    if 'ERROR' in t or 'CANDIDATE' in t or d['candidates'] != '0' or d['overflow'] != '0' or d['strict'] != '0': bad.append(f)
    iv.append((int(d['A']), int(d['B']))); cases += int(d['cases']); enum += int(d['enumerated'])
iv.sort(); gaps = []
cur = iv[0][0]
assert cur <= 4, iv[0]
end = iv[0][1]
for a, b in iv[1:]:
    if a != end + 1: gaps.append((end + 1, a - 1))
    end = max(end, b)
print('chunks=%d first_A=%d last_B=%d gaps=%s bad=%s' % (len(iv), iv[0][0], end, gaps, bad))
print('total (n,i) cases=%d enumerated_j=%d' % (cases, enum))
print('COVERAGE_COMPLETE_4_TO_1e9' if not gaps and not bad and iv[0][0] <= 4 and end >= 10**9 else 'COVERAGE_INCOMPLETE')
