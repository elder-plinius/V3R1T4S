"""Standalone check of the (k,s) = (3,5) certificates, n = 17..22 (run from the package folder).
  python3 verify-it-yourself/verify.py
1. Regenerates each CNF 'KG(n,3)_{5-stab} is (n-11)-colourable' with verify-it-yourself/gen_cnf.py (the encoding of
   README.md) and compares its sha256 with object/cnf_sha256.txt (stops at the first mismatch).
2. Checks each colouring in object/: the lines are exactly the 5-stable 3-subsets of [n], each once, colours in
   0..n-11 (n-10 colours), disjoint subsets coloured differently. Python standard library only.
3. Proofs, with drat-trim (environment variable DRAT_TRIM, or drat-trim on PATH):
   n = 17..21: decompresses object/proof_n<n>_c<C>.drat.xz (binary DRAT) and requires 's VERIFIED';
   n = 22: the proof (752 MB) is not shipped. With CADICAL set to a CaDiCaL 3.0.1 binary, it is regenerated as
   object/proof_n22_c11_not_shipped.txt says (about 5 minutes), its sha256 is compared, and drat-trim must print
   's VERIFIED' (about 5 minutes; 1.5 GB of temporary disk). Without CADICAL the default check stops short of that
   step and says so on the n = 22 line; the CNF and the colouring are still checked.
   A missing drat-trim makes the result FAIL. drat-trim: one C file, https://github.com/marijnheule/drat-trim;
   CaDiCaL: https://github.com/arminbiere/cadical, tag rel-3.0.1.
Last line: PASS or FAIL; exit status 0 only on PASS."""
import hashlib, itertools, lzma, os, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE); import gen_cnf
N22_PROOF_SHA = 'd24a47fc195dbc48aa70d8fad7c970c18780a40ab878c08d8ce0a8e088af0c7b'
want = {}
for line in open(os.path.join(PKG, 'object', 'cnf_sha256.txt')):
    if line.strip() and not line.startswith('#'):
        h, name = line.split()[:2]; want[name] = h
dt = os.environ.get('DRAT_TRIM') or shutil.which('drat-trim')
cd = os.environ.get('CADICAL')
tmp = tempfile.mkdtemp()
ok = True
def verified(cnf, proof):
    out = subprocess.run([dt, cnf, proof], capture_output=True, text=True).stdout.replace('\r', '\n')
    return any(l.strip() == 's VERIFIED' for l in out.splitlines())
try:
    for n in range(17, 23):
        C = n - 11
        V, E, cl = gen_cnf.build(n, 3, 5, C)
        cnf = os.path.join(tmp, 'n%d.cnf' % n)
        with open(cnf, 'w') as f:
            f.write('p cnf %d %d\n' % (len(V) * C, len(cl)))
            for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
        h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
        if h != want.get('n%d_k3_s5_c%d.cnf' % (n, C)):
            print('n=%d: CNF sha256 DIFFERS from object/cnf_sha256.txt' % n); ok = False; break
        rows = [tuple(map(int, l.split())) for l in open(os.path.join(PKG, 'object', 'colouring_n%d_%dcolours.txt' % (n, C + 1))) if l.strip() and not l.startswith('#')]
        verts = sorted(A for A in itertools.combinations(range(1, n + 1), 3) if all(min(j - i, n + i - j) >= 5 for i, j in itertools.combinations(A, 2)))
        col = {r[:3]: r[3] for r in rows}
        cok = sorted(r[:3] for r in rows) == verts and len(col) == len(rows) and set(col.values()) <= set(range(C + 1)) \
            and all(col[A] != col[B] for A, B in itertools.combinations(verts, 2) if not set(A) & set(B))
        if not dt:
            pok, ptxt = False, 'drat-trim not found (set DRAT_TRIM)'
        elif n < 22:
            pf = os.path.join(tmp, 'n%d.drat' % n)
            open(pf, 'wb').write(lzma.open(os.path.join(PKG, 'object', 'proof_n%d_c%d.drat.xz' % (n, C))).read())
            pok = verified(cnf, pf); ptxt = 's VERIFIED' if pok else 'NOT verified'
        elif not cd:
            pok, ptxt = True, 'not regenerated in this default check (set CADICAL=the CaDiCaL 3.0.1 binary for the full check, about 10 minutes)'
        else:
            pf = os.path.join(tmp, 'n22.drat')
            r = subprocess.run([cd, '-q', '--no-binary', cnf, pf], capture_output=True, text=True)
            ph = hashlib.sha256(open(pf, 'rb').read()).hexdigest()
            pok = r.returncode == 20 and verified(cnf, pf)
            ptxt = 'regenerated (exit %d, sha256 %s %s), %s' % (r.returncode, ph[:16], 'as recorded' if ph == N22_PROOF_SHA else 'differs from the recorded hash', 's VERIFIED' if pok else 'NOT verified')
            os.remove(pf)
        print('n=%d: %d vertices, %d edges, C=%d: CNF sha256 matches; colouring with %d colours %s; proof %s' % (
            n, len(V), len(E), C, C + 1, 'proper' if cok else 'NOT proper', ptxt), flush=True)
        ok = ok and cok and pok
finally:
    shutil.rmtree(tmp)
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
