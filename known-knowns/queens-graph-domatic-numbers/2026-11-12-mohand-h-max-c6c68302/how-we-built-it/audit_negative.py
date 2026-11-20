"""Controls for audit_chain.py on copies of class 0: the audit must accept the untouched copy and must fail when a
chain file is altered, even when the recorded hash is altered to match (so the failure comes from the logical check,
not from the hash). Proof files are hard links, nothing is duplicated; nothing is deleted (tmpdir must not exist).
 P  untouched copy                                             -> no problem found
 N1 one literal flipped in a clause of the body of piece 5      -> fail
 N2 the last unit clause of piece 7 removed (Q_7 is weakened)   -> fail (later pieces use the real Q_7)
 N3 in L2.cnf the premise a1 replaced by another unit clause    -> fail
 N4 a recorded verdict changed to "s NOT VERIFIED"              -> fail
 N5 the lemma a3 in "F plus lemmas" loses a literal             -> fail (the glue file negates the weaker, proved lemma)
 N6 the record of piece 3 removed                               -> fail
 N7 a proof file replaced by another of the same size           -> fail with --hash-proofs
Usage: python audit_negative.py F.cnf Fprime.cnf chain_root enc K tmpdir"""
import hashlib, json, os, shutil, subprocess, sys

F, Fp, root, enc, K, tmp = sys.argv[1:7]
here = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(tmp), 'tmpdir exists already; choose a new one'


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def copy_class0(dst, skip=()):
    for suffix in ('l12', 'a4'):
        s = os.path.join(root, '%s-c00-%s' % (enc, suffix)); d = os.path.join(dst, '%s-c00-%s' % (enc, suffix))
        os.makedirs(d)
        for name in os.listdir(s):
            p = os.path.join(s, name)
            if os.path.isfile(p) and name not in skip:
                (os.link if name.endswith('.bin') else shutil.copyfile)(p, os.path.join(d, name))


def lines_of(path):
    return open(path).read().split('\n')


def write(path, lines):
    open(path, 'w', newline='\n').write('\n'.join(lines))


def audit(dst, fprime=None):
    r = subprocess.run([sys.executable, '-B', os.path.join(here, 'audit_chain.py'), F, fprime or Fp, dst, enc, K, '--first', '1'], capture_output=True, text=True)
    return r.returncode, r.stdout


results = []
# P
d = os.path.join(tmp, 'P'); copy_class0(d)
code, out = audit(d)
results.append(('P  untouched copy', code == 0 and 'no problem found' in out, out.strip().split('\n')[-1]))
# N1
d = os.path.join(tmp, 'N1'); copy_class0(d)
p = os.path.join(d, '%s-c00-a4' % enc, 'piece-05.cnf'); L = lines_of(p)
t = L[10].split(); t[0] = str(-int(t[0])); L[10] = ' '.join(t); write(p, L)
sp = os.path.join(d, '%s-c00-a4' % enc, 'state.json'); st = json.load(open(sp))
[r for r in st['pieces'] if r['piece'] == 5][-1]['cnf_sha256'] = sha(p); json.dump(st, open(sp, 'w'))
code, out = audit(d)
results.append(('N1 literal flipped in piece 5', code == 1 and 'piece 5: 1 clauses are neither in F nor allowed' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N2
d = os.path.join(tmp, 'N2'); copy_class0(d)
p = os.path.join(d, '%s-c00-a4' % enc, 'piece-07.cnf'); L = lines_of(p)
while L[-1] == '':
    L.pop()
L.pop(); h = L[0].split(); h[3] = str(int(h[3]) - 1); L[0] = ' '.join(h); write(p, L + [''])
sp = os.path.join(d, '%s-c00-a4' % enc, 'state.json'); st = json.load(open(sp))
[r for r in st['pieces'] if r['piece'] == 7][-1]['cnf_sha256'] = sha(p); json.dump(st, open(sp, 'w'))
code, out = audit(d)
results.append(('N2 Q_7 weakened', code == 1 and 'piece 8: 1 clauses are neither in F nor allowed' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N3
d = os.path.join(tmp, 'N3'); copy_class0(d)
p = os.path.join(d, '%s-c00-l12' % enc, 'L2.cnf'); L = lines_of(p)
a1 = open(Fp).read().split('\n')[len(open(F).read().split('\n')) - 1]           # first lemma clause of Fprime (class 0)
i = max(k for k, l in enumerate(L) if l == a1)
L[i] = '1 0'; write(p, L)
jp = os.path.join(d, '%s-c00-l12' % enc, 'l12.json'); rec = json.load(open(jp))
[r for r in rec if r['lemma'] == 'L2'][0]['cnf_sha256'] = sha(p); json.dump(rec, open(jp, 'w'))
code, out = audit(d)
results.append(('N3 premise of L2 replaced', code == 1 and 'L2: 1 clauses are neither in F nor allowed' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N4 (added after an outside review): a recorded verdict that is not "s VERIFIED"
d = os.path.join(tmp, 'N4'); copy_class0(d)
sp = os.path.join(d, '%s-c00-a4' % enc, 'state.json'); st = json.load(open(sp))
[r for r in st['pieces'] if r['piece'] == 12][-1]['drat_trim'] = 's NOT VERIFIED'; json.dump(st, open(sp, 'w'))
code, out = audit(d)
results.append(('N4 a verdict is NOT VERIFIED', code == 1 and 'piece 12: no recorded verdict s VERIFIED' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N5: the third lemma of class 0 in "F plus lemmas" loses a literal (a stronger lemma than the one that was proved)
d = os.path.join(tmp, 'N5'); copy_class0(d)
L = lines_of(Fp); nF = len(lines_of(F)) - 1                      # line nF is the first lemma clause
t = L[nF + 2].split(); L[nF + 2] = ' '.join(t[:-2] + ['0'])
fp2 = os.path.join(d, 'Fprime-altered.cnf'); write(fp2, L)
code, out = audit(d, fp2)
results.append(('N5 lemma a3 strengthened', code == 1 and 'glue: 1 clauses are neither in F nor allowed' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N6: the record of piece 3 is missing
d = os.path.join(tmp, 'N6'); copy_class0(d)
sp = os.path.join(d, '%s-c00-a4' % enc, 'state.json'); st = json.load(open(sp))
st['pieces'] = [r for r in st['pieces'] if r['piece'] != 3]; json.dump(st, open(sp, 'w'))
code, out = audit(d)
results.append(('N6 record of piece 3 missing', code == 1 and 'piece 3: no recorded verdict s VERIFIED' in out, [l for l in out.split('\n') if 'FAIL' in l][:2]))
# N7: a proof file replaced by another one of the same size (needs --hash-proofs)
d = os.path.join(tmp, 'N7'); copy_class0(d, skip=('glue.bin',))
p = os.path.join(d, '%s-c00-a4' % enc, 'glue.bin'); open(p, 'wb').write(b'a\x01')
r = subprocess.run([sys.executable, '-B', os.path.join(here, 'audit_chain.py'), F, Fp, d, enc, K, '--first', '1', '--hash-proofs'], capture_output=True, text=True)
results.append(('N7 a proof file replaced', r.returncode == 1 and 'glue: the proof file is not the one that was checked' in r.stdout, [l for l in r.stdout.split('\n') if 'FAIL' in l][:2]))

ok = True
for name, good, detail in results:
    print('%-32s %s   %s' % (name, 'as expected' if good else 'UNEXPECTED', detail)); ok &= good
print('AUDIT CONTROLS:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
