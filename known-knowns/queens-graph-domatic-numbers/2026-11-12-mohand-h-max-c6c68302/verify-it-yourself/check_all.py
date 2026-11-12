"""Standalone check of the package (Python 3 standard library only, about half a minute).
It cannot re-check the proofs: they are about 80 GB and are not in the package. What it does check:
 1. object/certificate.txt has the expected sha256, and the two manifests have the sha256 the certificate gives;
 2. for each encoding, the base formula rebuilt by the generator (how-we-built-it/enc1.py, enc2.py, with the lists in
    how-we-built-it/lists/) has the sha256 the certificate gives;
 3. every one of the 2 x 680 formulas of the chain, rebuilt from the generator without a solver, has the sha256 its
    manifest line gives, is recorded there as VERIFIED, and is composed as the claim says (clauses of the base formula,
    earlier lemmas and case clauses, unit clauses negating its own target).
It writes no file. What remains to be believed or redone: that each of those formulas is unsatisfiable (the recorded
drat-trim verdicts, or hours of computing: RUN_IT_YOURSELF.md), the final step of each encoding, and what the base
formula consists of (how-we-built-it/formula_audit.py with dump_varmap.py: two commands, a few seconds, in
RUN_IT_YOURSELF.md).
Usage: python3 check_all.py EXPECTED_SHA256_OF_CERTIFICATE     (run from the package folder; last line PASS or FAIL)"""
import hashlib, os, subprocess, sys

ok = True
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
hb = os.path.join(root, 'how-we-built-it')


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def run(args):
    env = dict(os.environ); env['PYTHONPATH'] = hb
    r = subprocess.run([sys.executable, '-B'] + args, capture_output=True, text=True, env=env, cwd=root)
    out = [l for l in r.stdout.split('\n') if l.strip()]
    return r.returncode, out


cert_path = os.path.join(root, 'object', 'certificate.txt')
got = sha(cert_path)
print('certificate sha256', got, 'OK' if got == sys.argv[1] else 'MISMATCH')
ok = ok and got == sys.argv[1]
cert = {}
for line in open(cert_path):
    t = line.split()
    if len(t) == 4 and t[0] in ('enc1', 'enc2') and len(t[2]) == 64:
        cert[(t[0], t[1])] = t[2]
lists = [os.path.join('how-we-built-it', 'lists', 'e2-Q11-m5.txt'), os.path.join('how-we-built-it', 'lists', 'e2-Q11-m6-minimal.txt')]
for e in ('enc1', 'enc2'):
    man = os.path.join('object', 'chain-manifest-%s.txt' % e)
    good = cert.get((e, 'chain-manifest-%s.txt' % e)) == sha(os.path.join(root, man))
    print(e, 'manifest sha256', 'OK' if good else 'MISMATCH'); ok = ok and good
    code, out = run([os.path.join(hb, 'regen_formulas.py'), e, '11', 'dom', '20', '7', man] + lists)
    for l in out[-3:]:
        print(' ', l)
    base_sha = [l.split('sha256 of its DIMACS text ')[1].rstrip(')') for l in out if 'sha256 of its DIMACS text' in l]
    good = code == 0 and out and out[-1] == 'REGEN %s: PASS' % e and base_sha and base_sha[0] == cert.get((e, 'Fbase.cnf'))
    print(e, 'chain formulas and base formula rebuilt from the generator:', 'OK' if good else 'MISMATCH'); ok = ok and bool(good)
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
