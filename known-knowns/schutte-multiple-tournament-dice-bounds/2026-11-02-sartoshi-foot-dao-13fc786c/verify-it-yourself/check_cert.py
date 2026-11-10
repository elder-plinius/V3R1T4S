"""Check the certificate list in object/certificate_m3k6n12.tsv against the code that built it.
Usage (from the package folder): python -I verify-it-yourself/check_cert.py [sample size | all] [seed]
Needs python-sat 1.9.dev17 (the encoder's cardinality constraints). Checks, in order:
1. the encoder files are byte-identical to the ones the certificate was made with (certlib.check_encoder);
2. the job list in the object is exactly the cover tree for (m,k,n) = (3,6,12): the root cover lemma, every level-2/3
   cover lemma, and every leaf, no job missing, none extra, none twice;
3. for a seeded sample of jobs (or all), the CNF rebuilt now has the sha256, variable count and clause count in the object.
Last line: PASS or FAIL."""
import sys, os, random, hashlib, tempfile
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(PKG, 'how-we-built-it')
sys.path.insert(0, os.path.join(CODE, 'certify'))
import certlib, solve  # noqa: E402

def fail(msg):
    print(msg); print('FAIL'); sys.exit(1)

rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(PKG, 'object', 'certificate_m3k6n12.tsv'))]
head, rows = rows[0], rows[1:]
col = {h: i for i, h in enumerate(head)}
jobs = [r[col['job']] for r in rows]

try:
    certlib.check_encoder()
except AssertionError as e:
    fail(f'1. encoder: {e}')
print('1. encoder files: sha256 as recorded (cube.py, cube3.py, checker.py)')

leaves, covers = certlib.tree(CODE)
need = [certlib.leaf_id(c, lv, p) for c, lv, p, _ in leaves if c == 'm3k6n12'] + \
       [certlib.cover_id(c, lv, p) for c, lv, p in covers if c == 'm3k6n12']
if len(set(jobs)) != len(jobs):
    fail('2. the object lists a job twice')
miss, extra = set(need) - set(jobs), set(jobs) - set(need)
if miss or extra:
    fail(f'2. job list differs from the cover tree: {len(miss)} missing (e.g. {sorted(miss)[:3]}), {len(extra)} extra (e.g. {sorted(extra)[:3]})')
kinds = {}
for j in jobs:
    k = 'cover' if '/COVER' in j else 'leaf L3' if '_L3_' in j else 'leaf L2' if j.count('_') == 3 else 'leaf L1'
    kinds[k] = kinds.get(k, 0) + 1
print(f'2. job list = cover tree of (3,6,12): {len(jobs)} jobs ({", ".join(f"{v} {k}" for k, v in sorted(kinds.items()))})')

arg = sys.argv[1] if len(sys.argv) > 1 else '40'
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261101
pick = rows if arg == 'all' else random.Random(seed).sample(rows, int(arg))
tmp = tempfile.mkdtemp()
for r in pick:
    nv, cl = solve.build(r[col['job']])
    p = os.path.join(tmp, 'f.cnf'); sha, nv, ncl = certlib.write_dimacs(p, nv, cl)
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != sha:
        fail(f'3. CNF of {r[col["job"]]}: file hash differs from the hash computed while writing')
    os.remove(p)
    got = (sha, str(nv), str(ncl))
    want = (r[col['cnf_sha256']], r[col['vars']], r[col['clauses']])
    if got != want:
        fail(f'3. CNF of {r[col["job"]]} rebuilt as {got}, object says {want}')
os.rmdir(tmp)
print(f'3. CNFs rebuilt and matched (sha256, variables, clauses): {len(pick)} of {len(rows)} jobs' + ('' if arg == 'all' else f' (seed {seed})'))
print('PASS')
