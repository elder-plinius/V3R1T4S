"""Exhaustive tests of the two cardinality facts the cover lemmas rely on (README.md, 'Trusted'). Usage: python -I test_encodings.py
(1) certlib.counter: for every input assignment of L <= 12 literals, the honest assignment of its auxiliaries
    (s[i][k] = at least k of the first i inputs true) satisfies every clause, and ge(k) is true iff count >= k.
(2) pysat seqcounter CardEnc.atmost(lits, b) (the encoder's R_j): for every assignment of L <= 12 inputs and every b in 1..L-1,
    the encoding plus the input units is satisfiable iff count <= b (only 'if' is needed for soundness)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certlib
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def test_counter(L):
    F = certlib.Cnf(L); ge = certlib.counter(F, list(range(1, L + 1)))
    # recover the s-variable layout: counter allocates s[i][k] for i = 1..L, k = 1..i in order
    idx = {}; v = L
    for i in range(1, L + 1):
        for k in range(1, i + 1): v += 1; idx[v] = (i, k)
    assert v == F.top
    for bits in itertools.product([0, 1], repeat=L):
        pref = [0]
        for b in bits: pref.append(pref[-1] + b)
        val = lambda x: (bits[abs(x) - 1] if abs(x) <= L else int(pref[idx[abs(x)][0]] >= idx[abs(x)][1])) == (1 if x > 0 else 0)
        for c in F.cl: assert any(val(x) for x in c), (L, bits, c)
        for k in range(0, L + 2):
            g = ge(k); want = pref[-1] >= k
            if g in (certlib.TRUE, certlib.FALSE): assert (g == certlib.TRUE) == want
            else: assert val(g) == want
    return 2 ** L

def test_seq(L):
    n = 0
    for b in range(1, L):
        enc = CardEnc.atmost(lits=list(range(1, L + 1)), bound=b, top_id=L, encoding=EncType.seqcounter)
        with Solver(name='cadical195', bootstrap_with=enc.clauses) as s:
            for bits in itertools.product([0, 1], repeat=L):
                r = s.solve(assumptions=[i + 1 if x else -(i + 1) for i, x in enumerate(bits)])
                assert r == (sum(bits) <= b), (L, b, bits); n += 1
    return n

if __name__ == '__main__':
    tot = 0
    for L in range(1, 13): tot += test_counter(L)
    print('counter: honest assignment satisfies all clauses and ge(k) is exact, L=1..12,', tot, 'assignments: PASS', flush=True)
    tot = 0
    for L in range(2, 13): tot += test_seq(L)
    print('seqcounter atmost: satisfiable iff count <= bound, L=2..12, all bounds 1..L-1,', tot, 'cases: PASS', flush=True)
