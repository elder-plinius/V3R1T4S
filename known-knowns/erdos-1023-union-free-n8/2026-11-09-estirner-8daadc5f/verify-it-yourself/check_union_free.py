"""Standalone check of a union-free family (OEIS A347025 / Erdos problem #1023). Python standard library only.
  python3 verify-it-yourself/check_union_free.py object/union_free_n8_80.txt 8 80
Definition: a family of nonempty subsets of {1..N} in which no member equals the union of other members. Any union
of other members equal to S uses only members contained in S, so S is fine iff the union of all members that are
proper subsets of S is not S; this covers unions of any number of members. Checks, in order:
 0. the object's sha256 equals verify-it-yourself/expected_sha256.txt;
 1. calibration: exhaustive search over all families on {1..n} gives the known a(1..4) = 1, 2, 4, 7;
 2. every line is a set of distinct integers in 1..N (no repeats within a line, nothing out of range, no empty
    member); members are pairwise distinct;
 3. the union condition for every member, by two methods (maximal union of proper sub-members; and per element:
    S needs an element lying in no other member inside S);
 4. size >= MIN_SIZE.  Last line: PASS or FAIL."""
import hashlib, itertools, os, sys
path, N, need = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
here = os.path.dirname(os.path.abspath(__file__))
exp = dict((l.split()[1], l.split()[0]) for l in open(os.path.join(here, 'expected_sha256.txt')) if l.strip())
got = hashlib.sha256(open(path, 'rb').read()).hexdigest()
key = os.path.relpath(os.path.abspath(path), os.path.dirname(here))
ok0 = exp.get(key) == got
print('0. sha256 %s %s' % (got, 'matches expected_sha256.txt' if ok0 else 'DIFFERS from expected_sha256.txt'))
def uf_max(F):
    return all(frozenset().union(*[T for T in F if T < S]) != S for S in F)
def uf_elem(F):
    return all(any(all(e not in T for T in F if T < S) for e in S) for S in F)
def brute(n):
    subs = [frozenset(c) for k in range(1, n + 1) for c in itertools.combinations(range(1, n + 1), k)]
    best = 0
    for m in range(1 << len(subs)):
        F = [subs[i] for i in range(len(subs)) if m >> i & 1]
        if len(F) > best and uf_max(F): best = len(F)
    return best
cal = [brute(n) for n in (1, 2, 3, 4)]
ok1 = cal == [1, 2, 4, 7]
print('1. calibration a(1..4) by exhaustive search: %s (expected [1, 2, 4, 7])' % cal)
F, ok2 = [], True
for ln, line in enumerate(open(path), 1):
    if line.lstrip().startswith('#'): continue
    if not line.strip():
        ok2 = False; print('   line %d: empty line' % ln); continue
    xs = [int(x) for x in line.split()]
    if len(set(xs)) != len(xs) or not all(1 <= x <= N for x in xs):
        ok2 = False; print('   line %d: repeated or out-of-range element: %s' % (ln, line.strip()))
    F.append(frozenset(xs))
ok2 = ok2 and len(set(F)) == len(F)
print('2. %d members, all distinct sets of distinct elements of {1..%d}: %s' % (len(F), N, ok2))
a, b = uf_max(F), uf_elem(F)
print('3. union-free: maximal-union test %s, per-element test %s' % (a, b))
print('   size profile: %s' % {k: sum(1 for S in F if len(S) == k) for k in sorted({len(S) for S in F})})
ok4 = len(F) >= need
print('4. size %d >= %d: %s' % (len(F), need, ok4))
ok = ok0 and ok1 and ok2 and a and b and ok4
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
