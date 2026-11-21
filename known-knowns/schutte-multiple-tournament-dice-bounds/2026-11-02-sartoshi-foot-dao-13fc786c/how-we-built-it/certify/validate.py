"""Pre-launch validation (D-023). Usage (workspace root): nice -n 19 venv-schutte/bin/python -I certify/validate.py
1. Builds all 63 cover-lemma CNFs (this also asserts, for every child CNF of every refined node, that it is the parent CNF plus
   unit clauses on arc variables plus exactly the encoder's seqcounter constraints R_j) and records their sha256.
2. Cover-lemma controls: each cover CNF without its child clauses must be SAT (NF is not contradictory), and with one child clause
   removed it must be SAT unless that child is empty; tested on one cover per level (first, last, a random child).
3. NF faithfulness (level 1): random tournament triples / pairs are normalised by the procedure of SOUNDNESS_NOTE.md; their honest
   extension must satisfy every NF clause and falsify the clause of exactly the child (d,a,b) they land in.
4. Full pipeline on small jobs (positive) and negative controls (truncated / tampered proofs, a unit replaced, a satisfiable cube)."""
import sys, os, json, random, itertools, hashlib, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certlib, driver
from pysat.solvers import Solver
WS = driver.WS; OUT = os.path.join(driver.WORK, 'validate'); os.makedirs(OUT, exist_ok=True)
log = open(os.path.join(driver.CERT, 'validation.out'), 'w')
def say(*a):
    s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()

certlib.check_encoder()
# ---- 1
leaves, covers = certlib.tree(WS)
say('[1] building all', len(covers), 'cover lemmas (structure asserts on every child)')
cov = {}
for cell, lv, p in covers:
    nv, cl, meta = certlib.cover_cnf(cell, lv, p); j = certlib.cover_id(cell, lv, p)
    cov[j] = (nv, cl, meta['children'])
nchild = sum(v[2] for v in cov.values())
say('[1] PASS: all cover CNFs built;', nchild, 'child relations checked (= leaves + refined nodes - 2 roots:', len(leaves) + len(covers) - 2, ')')
assert nchild == len(leaves) + len(covers) - 2
# ---- 2
def solve(cl, nv=None):
    with Solver(name='cadical195', bootstrap_with=cl) as s: return s.solve()
big2 = max((j for j in cov if '/COVER2/' in j), key=lambda j: cov[j][2]); big3 = max((j for j in cov if '/COVER3/' in j), key=lambda j: cov[j][2])
for j in ['m3k6n12/COVER2/10_0_0', big2, 'm3k6n12/COVER3/10_0_0_0-0-0-0', big3, 'm3k6n12/COVER1', 'm2k5n13/COVER1']:
    nv, cl, k = cov[j]
    body, kids = cl[:len(cl) - k], cl[len(cl) - k:]
    r0 = solve(body)
    picks = sorted({0, k - 1, random.Random(1).randrange(k)})
    if j == 'm2k5n13/COVER1': picks = [certlib.l1_cubes(13).index((7, 0, 0)), k - 1]  # d=6 children with a+b<6 are empty only by counting
    rs = [solve(body + kids[:i] + kids[i + 1:]) for i in picks]
    say(f'[2] {j}: children {k}; without child clauses SAT={r0}; one child clause removed (indices {picks}) SAT={rs}')
    assert r0 and all(rs)
# ---- 3
def norm_and_check(m, n, trials, seed):
    rnd = random.Random(seed); kids = certlib.l1_cubes(n)
    _, c0, lit = certlib.leaf_cnf(f'm{m}k{5 if m == 2 else 6}n{n}', 1, kids[0])
    cell = f'm{m}k{5 if m == 2 else 6}n{n}'
    nv, cl, k = cov[f'{cell}/COVER1']; nx = m * n * (n - 1) // 2
    # rebuild the counters' honest values by unit propagation: fix the arc variables, propagate, check no conflict
    s = Solver(name='cadical195', bootstrap_with=cl[:len(cl) - k]); kidcl = cl[len(cl) - k:]
    for _ in range(trials):
        T = []
        for t in range(m):  # random tournament, biased to skewed degrees sometimes
            pbeat = rnd.choice([0.5, 0.3, 0.7]); A = [[0] * n for _ in range(n)]
            for i in range(n):
                for j2 in range(i + 1, n):
                    if rnd.random() < pbeat: A[i][j2] = 1
                    else: A[j2][i] = 1
            T.append(A)
        deg = lambda t, v: sum(T[t][v])
        t0, v0 = max(((t, v) for t in range(m) for v in range(n)), key=lambda x: deg(*x))
        order_t = [t0] + sorted([t for t in range(m) if t != t0], key=lambda t: -deg(t, v0))
        T = [T[t] for t in order_t]
        A1 = [u for u in range(n) if u != v0 and T[0][v0][u]]; B1 = [u for u in range(n) if u != v0 and not T[0][v0][u]]
        A1.sort(key=lambda u: -T[1][v0][u]); B1.sort(key=lambda u: -T[1][v0][u])
        perm = [v0] + A1 + B1  # new label i <- old vertex perm[i]
        Tn = [[[T[t][perm[i]][perm[j2]] for j2 in range(n)] for i in range(n)] for t in range(m)]
        assum = []
        for t in range(m):
            for i in range(n):
                for j2 in range(i + 1, n):
                    l = lit(t, i, j2); assum.append(l if Tn[t][i][j2] else -l)
        assert s.solve(assumptions=assum), 'normalised tuple violates NF'
        model = set(s.get_model())
        d = sum(Tn[0][0]); a = sum(Tn[1][0][1:d + 1]); b = sum(Tn[1][0][d + 1:])
        falsified = [i for i, c in enumerate(kidcl) if not any(x in model for x in c)]
        assert falsified == [kids.index((d, a, b))], (falsified, (d, a, b))
    s.delete()
norm_and_check(3, 12, 300, 1); norm_and_check(2, 13, 300, 2)
say('[3] PASS: 300 random normalised triples (3,6,12) and 300 pairs (2,5,13): every NF clause holds and exactly the clause of their own cube (d,a,b) is falsified')
# ---- 4
def pipe(job, tag, attempt=1, keep=True):
    wd = os.path.join(OUT, tag); shutil.rmtree(wd, ignore_errors=True)
    r = driver.run_job(job, wd, attempt, 900, 6 * driver.GB, keep=keep)
    say(f'[4] {tag}: {job}: verdict {r["verdict"]} solve {r["solve_s"]} s, convert {r["convert_s"]} s, check {r["check_s"]} s, '
        f'proof {r["proof_bytes"]} B, lrat {r["lrat_bytes"]} B, peak RSS {r["peak_rss_mb"]} MB, cnf {r["cnf_sha256"][:16]} {r["note"]}')
    return r, wd
pos = ['m3k6n12/COVER1', 'm3k6n12/COVER2/10_0_0', 'm3k6n12/COVER3/10_0_0_0-0-0-0', 'm3k6n12/11_4_0', 'm3k6n12/9_1_2_1-0-1-0',
       'm3k6n12/8_0_1_0-0-0-1_L3_4_2_1', 'm2k5n13/6_1_4']
res = {}
for i, j in enumerate(pos):
    r, wd = pipe(j, f'pos{i}', keep=(i == 5)); res[j] = (r, wd); assert r['verdict'] == 'VERIFIED'
say('[4] PASS: all', len(pos), 'positive jobs VERIFIED by cake_lpr')
# negative controls on pos5 (L3 leaf): re-create its proof files (kept), then tamper
r, wd = res[pos[5]]
cnf = os.path.join(wd, 'f.cnf'); lrat = os.path.join(wd, 'proof.lrat')
def cake(c, p):
    q = subprocess.run([driver.CAKE, '--CML_HEAP_SIZE=4500', '--CML_STACK_SIZE=1000', c, p], capture_output=True, text=True)
    return q.stdout.strip(), q.stderr.strip()[:120]
ok = cake(cnf, lrat); say('[5] control: original proof:', ok); assert ok[0] == 's VERIFIED UNSAT'
L = open(lrat).read().splitlines()
open(os.path.join(wd, 'trunc.lrat'), 'w').write('\n'.join(L[:int(len(L) * 0.9)]) + '\n')
v = cake(cnf, os.path.join(wd, 'trunc.lrat')); say('[5] truncated LRAT (first 90% of lines):', v); assert v[0] != 's VERIFIED UNSAT'
# tamper: in a middle addition line, flip the sign of the first literal
idx = next(i for i in range(len(L) // 2, len(L)) if ' d ' not in L[i] and len(L[i].split()) > 4 and L[i].split()[1] != '0')
f = L[idx].split(); f[1] = str(-int(f[1])); T2 = L[:idx] + [' '.join(f)] + L[idx + 1:]
open(os.path.join(wd, 'tamper.lrat'), 'w').write('\n'.join(T2) + '\n')
v = cake(cnf, os.path.join(wd, 'tamper.lrat')); say(f'[5] tampered LRAT (line {idx}: first literal sign flipped):', v); assert v[0] != 's VERIFIED UNSAT'
# one cube literal dropped: replace the first unit clause of the cube by a copy of clause 1 (keeps clause ids)
C = open(cnf).read().splitlines(); hdr, body = C[0], C[1:]
ui = next(i for i in range(len(body) - 1, -1, -1) if len(body[i].split()) == 2)  # last unit clause = a cube literal
dropped = body[ui]; body2 = body[:ui] + [body[0]] + body[ui + 1:]
open(os.path.join(wd, 'drop.cnf'), 'w').write('\n'.join([hdr] + body2) + '\n')
v = cake(os.path.join(wd, 'drop.cnf'), lrat); say(f'[5] original LRAT against the cube with unit "{dropped}" replaced by a copy of clause 1:', v); assert v[0] != 's VERIFIED UNSAT'
# the same through the whole pipeline (re-solve the weakened CNF is a different question; here: does drat-trim accept the old DRAT?)
r2, wd2 = pipe('FILE:' + os.path.join(wd, 'drop.cnf'), 'drop_resolve')
say('[5] (info) weakened cube re-solved from scratch:', r2['verdict'], '(a weaker cube may still be UNSAT; this is not the control)')
# satisfiable variant: the (3,6,13) cube 11_7_0 that contains the composition witness of run 0844
sys.path.insert(0, os.path.join(WS, 'certify', 'encoder')); import cube3
nv, cl, _ = cube3.build3(3, 6, 13, 11, 7, 0, None, None)
certlib.write_dimacs(os.path.join(OUT, 'sat_3_6_13.cnf'), nv, cl)
r3, _ = pipe('FILE:' + os.path.join(OUT, 'sat_3_6_13.cnf'), 'sat_3_6_13')
assert r3['verdict'] == 'SAT'
v = cake(os.path.join(OUT, 'sat_3_6_13.cnf'), lrat); say('[5] satisfiable (3,6,13) cube 11_7_0 against the L3 proof:', v); assert v[0] != 's VERIFIED UNSAT'
# truncated DRAT through drat-trim + cake_lpr: re-solve pos5 keeping the DRAT
wd3 = os.path.join(OUT, 'dtrunc'); shutil.rmtree(wd3, ignore_errors=True); os.makedirs(wd3)
subprocess.run([driver.PY, '-I', os.path.join(driver.CERT, 'solve.py'), pos[5], wd3], capture_output=True)
D = open(os.path.join(wd3, 'proof.drat'), 'rb').read(); open(os.path.join(wd3, 't.drat'), 'wb').write(D[:len(D) // 2])
q = subprocess.run([driver.DRAT_TRIM, os.path.join(wd3, 'f.cnf'), os.path.join(wd3, 't.drat'), '-i', '-w', '-L', os.path.join(wd3, 't.lrat')], capture_output=True, text=True)
dt = [l for l in q.stdout.splitlines() if l.startswith('s ')]
v = cake(os.path.join(wd3, 'f.cnf'), os.path.join(wd3, 't.lrat')) if os.path.exists(os.path.join(wd3, 't.lrat')) else ('no lrat', '')
say('[5] DRAT truncated to its first half: drat-trim', dt, '; cake_lpr on its output:', v); assert v[0] != 's VERIFIED UNSAT'
say('[5] PASS: every negative control rejected by cake_lpr')
for d in (wd, wd3): shutil.rmtree(d, ignore_errors=True)
say('validation complete')
