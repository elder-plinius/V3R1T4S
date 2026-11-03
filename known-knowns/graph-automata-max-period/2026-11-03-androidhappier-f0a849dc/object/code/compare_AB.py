#!/usr/bin/env python3
"""Compare Program A (all graphs, 64 residue files A11_r*of64.txt) with Program B (connected graphs, merged
B_order11.txt) and B's combine.py output. Usage: compare_AB.py <A_dir> <B_order11.txt> <combine_output.txt>"""
import glob, re, sys
A = sorted(glob.glob(sys.argv[1] + '/A11_r*of64.txt')); assert len(A) == 64, len(A)
tot = con = 0; best = 0; hall = {}; hcon = {}; highA = set()
for f in A:
    for l in open(f):
        p = l.split()
        if l.startswith('n=11'):
            d = dict(x.split('=', 1) for x in p); tot += int(d['graphs']); con += int(d['connected']); best = max(best, int(d['maxperiod']))
        elif p[0] == 'hist_all': hall[int(p[1])] = hall.get(int(p[1]), 0) + int(p[2])
        elif p[0] == 'hist_conn': hcon[int(p[1])] = hcon.get(int(p[1]), 0) + int(p[2])
        elif p[0] == 'high' and p[3] == '1': highA.add((p[1], int(p[2])))
B = open(sys.argv[2]).read()
btot = int(re.search(r'connected_graphs=(\d+)', B).group(1)); bmax = int(re.search(r'max_cycle=(\d+)', B).group(1))
hB = {int(a): int(b) for a, b in re.findall(r'^hist (\d+) (\d+)$', B, re.M)}
highB = {(g, int(v)) for g, v in re.findall(r'^high (\S+) (\d+)$', B, re.M)}
m = re.search(r'^n=11 a\(n\)=(\d+)', open(sys.argv[3]).read(), re.M)
print('A total graphs', tot, '== A000088(11) 1018997864:', tot == 1018997864)
print('A connected', con, 'B connected', btot, '== A001349(11) 1006700565:', con == btot == 1006700565)
print('A max (all graphs)', best, '| B connected max', bmax, '| B combine a(11)', m and m.group(1))
print('hist_conn(A) == hist(B):', hcon == hB, 'sum', sum(hB.values()))
print('high connected (>=40) A', len(highA), 'B', len(highB), 'identical:', highA == highB)
print('hist_all(A) sum', sum(hall.values()), 'max', max(hall))
ok = tot == 1018997864 and con == btot == 1006700565 and hcon == hB and highA == highB and m and int(m.group(1)) == best
print('VERDICT', 'AGREE' if ok else 'DISAGREE')
