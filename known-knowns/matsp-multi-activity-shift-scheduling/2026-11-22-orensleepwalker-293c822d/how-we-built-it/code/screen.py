"""Hidden-zero screen (Andy, 2026-11-22). For every instance: total minimum work W_min = sum_e ceil(min_minutes_e / 15) intervals
(each employee must work at least that many 15-minute intervals, each assigned to exactly one task), total maximum demand
M = sum over tasks and intervals of the max cover, total minimum demand V = sum of the min cover. Zero overstaffing needs W_min <= M.
If W_min > M, the total excess X = W_min - M must sit on over-max slots, and since each over slot costs y^2 >= y, the penalty is at
least X: a valid lower bound. Output zero/screen.tsv and a printed summary."""
import zipfile, os, sys, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'code')); import matsp
Z = zipfile.ZipFile(os.path.join(H, '..', 'raw/instances1_225.zip'))
board = {l.split('\t')[0]: l.split('\t') for l in open(os.path.join(H, '..', 'out/board.tsv')).read().split('\n') if l}
rows = []
for name in sorted(Z.namelist()):
    if not name.endswith('.txt'): continue
    stem = os.path.basename(name)[:-4]; num = stem.split('_')[0]; I = matsp.read_instance(Z.read(name).decode())
    wmin = sum(math.ceil(b / 15) for b, c in I['staff'].values()); wmax = sum(c // 15 for b, c in I['staff'].values())
    M = sum(sum(v) for v in I['vmax'].values()); V = sum(sum(v) for v in I['vmin'].values())
    X = wmin - M; rec = int(board[num][4])
    rows.append((int(num), stem, rec, wmin, wmax, V, M, X, max(0, X)))
rows.sort()
with open(os.path.join(H, 'screen.tsv'), 'w') as f:
    f.write('id\tstem\trecord\tmin_work\tmax_work\tmin_demand\tmax_demand\texcess\tlower_bound\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
zero_possible = [r for r in rows if r[7] <= 0]
print('instances', len(rows), '| zero not excluded (min work <= max demand):', len(zero_possible))
print('  of which record > 0:', [(r[0], r[2]) for r in zero_possible if r[2] > 0])
print('lower bound equals the record (record proved optimal by counting):', [(r[0], r[2]) for r in rows if r[8] > 0 and r[8] == r[2]])
print('lower bound above the record (would mean a checker or reading bug):', [(r[0], r[2], r[8]) for r in rows if r[8] > r[2]])
gap = sorted(((r[2] - r[8]) / r[2], r[0], r[2], r[8]) for r in rows if r[2] > 0 and r[8] > 0)[:12]
print('closest records to the counting bound:', [(n, rec, lb, '%.1f%%' % (100 * g)) for g, n, rec, lb in gap])
