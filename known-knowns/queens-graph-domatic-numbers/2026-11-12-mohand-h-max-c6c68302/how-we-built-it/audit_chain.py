"""Audit of the proof chain from the files alone: no encoder is imported, no solver is run.

For one encoding (F.cnf, Fprime.cnf, and the chain directories <root>/<enc>-cNN-l12 and <root>/<enc>-cNN-a4):
 A. Fprime.cnf is F.cnf followed by exactly 3K extra clauses, the lemma clauses a1, a2, a3 of class 0, 1, ..., K-1.
 B. For every class:
    L1.cnf       every clause is a clause of F, or a unit clause that negates a literal of a1;
    L2.cnf       every clause is a clause of F, or a1, or a unit clause that negates a literal of a2;
    piece-i.cnf  the file ends with a run of unit clauses; Q_i is DEFINED as the clause of their negations;
                 every clause before that run is a clause of F, or a1, or a2, or one of Q_0 .. Q_(i-1);
    glue.cnf     every clause is a clause of F, or a1, or a2, or one of the Q_i, or a unit clause that negates a
                 literal of a3.
 C. Each of these files has the sha256 that is recorded next to a drat-trim verdict "s VERIFIED" (l12.json,
    state.json); the proof file exists with the recorded size (and, with --hash-proofs, the recorded sha256).
What follows, if the recorded drat-trim verdicts are right: a file of type B is unsatisfiable, so F implies a1, then
a2, then Q_0, Q_1, ... in turn, then a3, for every class; stage B says that F plus all lemma clauses is
unsatisfiable; hence F is unsatisfiable.  Whether F says "a domatic K-partition exists" is NOT checked here.
Options: --hash-proofs (re-hash every proof file), --reverify N --drat EXE [--seed S] (run drat-trim again on N of
the checks chosen at random), --proofB FILE --drat-text EXE (run drat-trim again on stage B).
Usage: python audit_chain.py F.cnf Fprime.cnf chain_root enc_label K [options]"""
import argparse, hashlib, json, os, random, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument('F'); ap.add_argument('Fprime'); ap.add_argument('root'); ap.add_argument('enc'); ap.add_argument('K', type=int)
ap.add_argument('--hash-proofs', action='store_true')
ap.add_argument('--reverify', type=int, default=0); ap.add_argument('--drat'); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--proofB'); ap.add_argument('--drat-text')
ap.add_argument('--first', type=int, help='audit only the first classes (a partial audit never prints PASS)')
A = ap.parse_args()
fails = []


def bad(msg):
    fails.append(msg); print('  FAIL: ' + msg, flush=True)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_cnf(path):
    """One clause per line, each ended by 0. Returns (number of variables, list of clauses as sorted tuples)."""
    nv, nc, out = None, None, []
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t or t[0] == 'c':
                continue
            if t[0] == 'p':
                nv, nc = int(t[2]), int(t[3]); continue
            lits = [int(x) for x in t]
            assert lits[-1] == 0 and 0 not in lits[:-1], 'not one clause per line in ' + path
            out.append(tuple(sorted(set(lits[:-1]))))
    assert nc == len(out), 'clause count differs from the header in ' + path
    return nv, out


def neg_units(clause):
    return set((-l,) for l in clause)


def run_drat(exe, cnf, proof):
    r = subprocess.run([os.path.abspath(exe), cnf, proof], capture_output=True, text=True)
    lines = [l.strip() for l in r.stdout.replace('\r', '\n').split('\n') if l.strip().startswith('s ')]
    return lines[-1] if lines else 'no status line (exit %d)' % r.returncode


t0 = time.time()
nvF, Fl = read_cnf(A.F)
nvP, Pl = read_cnf(A.Fprime)
print('F: %d variables, %d clauses, sha256 %s' % (nvF, len(Fl), sha(A.F)))
print('Fprime: %d variables, %d clauses, sha256 %s' % (nvP, len(Pl), sha(A.Fprime)))
if not (nvF == nvP and len(Pl) == len(Fl) + 3 * A.K and Pl[:len(Fl)] == Fl):
    bad('Fprime is not F followed by %d clauses' % (3 * A.K))
lem = Pl[len(Fl):]
Fset = set(Fl)
checks = []          # (cnf path, proof path) of every drat-trim verdict relied upon
nfiles = 0
for c in range(A.K if A.first is None else A.first):
    a1, a2, a3 = lem[3 * c], lem[3 * c + 1], lem[3 * c + 2]
    d12 = os.path.join(A.root, '%s-c%02d-l12' % (A.enc, c)); d4 = os.path.join(A.root, '%s-c%02d-a4' % (A.enc, c))
    before = len(fails)
    if not (os.path.exists(os.path.join(d12, 'l12.json')) and os.path.exists(os.path.join(d4, 'state.json'))):
        bad('class %d: chain not finished (l12.json or state.json missing)' % c); continue
    rec12 = {r['lemma']: r for r in json.load(open(os.path.join(d12, 'l12.json')))}
    st = json.load(open(os.path.join(d4, 'state.json')))
    recp = {r['piece']: r for r in st['pieces']}           # the last record of a piece wins

    def recorded(rec, cnf, proof, what):
        global nfiles
        nfiles += 1
        if rec is None or rec.get('drat_trim') != 's VERIFIED':
            bad('class %d %s: no recorded verdict s VERIFIED' % (c, what)); return
        if rec['cnf_sha256'] != sha(cnf):
            bad('class %d %s: the formula file is not the one that was checked' % (c, what))
        if not os.path.exists(proof) or ('proof_bytes' in rec and os.path.getsize(proof) != rec['proof_bytes']):
            bad('class %d %s: proof file missing or of another size' % (c, what))
        elif A.hash_proofs and sha(proof) != rec['proof_sha256']:
            bad('class %d %s: the proof file is not the one that was checked' % (c, what))
        checks.append((cnf, proof))

    # L1, L2
    for name, allowed_extra, target in (('L1', set(), a1), ('L2', {a1}, a2)):
        cnf = os.path.join(d12, name + '.cnf')
        _, cl = read_cnf(cnf)
        ok = allowed_extra | neg_units(target)
        n_bad = sum(1 for x in cl if x not in Fset and x not in ok)
        if n_bad:
            bad('class %d %s: %d clauses are neither in F nor allowed' % (c, name, n_bad))
        recorded(rec12.get(name), cnf, os.path.join(d12, name + '.bin'), name)
    # pieces
    Q = []
    i = 0
    while os.path.exists(os.path.join(d4, 'piece-%02d.cnf' % i)):
        cnf = os.path.join(d4, 'piece-%02d.cnf' % i)
        _, cl = read_cnf(cnf)
        k = len(cl)
        while k > 0 and len(cl[k - 1]) == 1:
            k -= 1
        qi = tuple(sorted(-u[0] for u in cl[k:]))
        if len(set(qi)) != len(cl) - k or any(-l in qi for l in qi):
            bad('class %d piece %d: the final unit clauses repeat or contradict each other' % (c, i))
        ok = {a1, a2} | set(Q)
        n_bad = sum(1 for x in cl[:k] if x not in Fset and x not in ok)
        if n_bad:
            bad('class %d piece %d: %d clauses are neither in F nor allowed' % (c, i, n_bad))
        recorded(recp.get(i), cnf, os.path.join(d4, 'piece-%02d.bin' % i), 'piece %d' % i)
        Q.append(qi); i += 1
    if st.get('verified') != len(Q):
        bad('class %d: %d piece files but %s pieces recorded as verified' % (c, len(Q), st.get('verified')))
    # glue
    cnf = os.path.join(d4, 'glue.cnf')
    if not os.path.exists(cnf):
        bad('class %d: glue.cnf missing' % c); continue
    _, cl = read_cnf(cnf)
    ok = {a1, a2} | set(Q) | neg_units(a3)
    n_bad = sum(1 for x in cl if x not in Fset and x not in ok)
    if n_bad:
        bad('class %d glue: %d clauses are neither in F nor allowed' % (c, n_bad))
    recorded(st.get('glue'), cnf, os.path.join(d4, 'glue.bin'), 'glue')
    print('class %2d: L1, L2, %d pieces, glue: %s' % (c, len(Q), 'ok' if len(fails) == before else 'NOT ok'), flush=True)

print('%d formula files audited, %d recorded drat-trim verdicts relied upon (stage B not counted), %.0fs' % (nfiles, len(checks), time.time() - t0))
if A.reverify and A.drat:
    rnd = random.Random(A.seed)
    for cnf, proof in rnd.sample(checks, min(A.reverify, len(checks))):
        t = time.time(); s = run_drat(A.drat, cnf, proof)
        print('re-run drat-trim on %s: %s in %.1fs' % (os.path.relpath(cnf, A.root), s, time.time() - t), flush=True)
        if s != 's VERIFIED':
            bad('re-run failed on ' + cnf)
final = False
if A.proofB and A.drat_text:
    t = time.time(); s = run_drat(A.drat_text, A.Fprime, A.proofB)
    print('final step, drat-trim on (Fprime, %s, sha256 %s): %s in %.1fs' % (os.path.basename(A.proofB), sha(A.proofB), s, time.time() - t), flush=True)
    final = True
    if s != 's VERIFIED':
        bad('the final step is not verified')
if A.first is not None and not fails:
    print('AUDIT %s: PARTIAL, the first %d classes only, no problem found' % (A.enc, A.first)); sys.exit(0)
if fails:
    print('AUDIT %s: FAIL (%d problems)' % (A.enc, len(fails)))
elif final:
    print('AUDIT %s: PASS (lemma chain audited for all %d classes; final step re-run and verified here)' % (A.enc, A.K))
else:
    print('AUDIT %s: PASS FOR THE LEMMA CHAIN ONLY (all %d classes; the final step was not re-run here, give --proofB and --drat-text)' % (A.enc, A.K))
sys.exit(0 if not fails else 1)
