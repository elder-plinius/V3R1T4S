"""Standalone checker for the Erdos #699 certificate (Python standard library only), written from the definition:
"for every 1 <= i < j <= n/2 there is a prime p >= i dividing gcd(C(n,i), C(n,j))".
1. Definition check: for every n <= N_SMALL and every pair, exact gcd of the exact binomials, primes < i removed,
   must be > 1; the strict variant (primes <= i removed) must fail exactly at the known exceptions.
2. Certificate check (object/seg699_chunk_summaries.txt): the chunks cover [0, 10^9] contiguously, strict=0, and each
   reports candidates=0 and overflow=0.
3. Independent recount: a chunk's "cases" is the number of (n,i) with i < floor(n/2) and no prime in [n-i+1, n],
   i.e. the sum over n of min(G(n), floor(n/2)-1) with G(n) = n - (largest prime <= n). It is recomputed here for
   every chunk with this file's own segmented sieve and must match the certificate exactly.
4. object/coverage_output.txt (the scan's own coverage summary) must agree with the chunk lines: chunk count, range,
   no gaps, no bad chunks, and the totals of cases and enumerated.
Prints PASS or FAIL as its last line. Usage: python3 verify699.py [path to seg699_chunk_summaries.txt]"""
import itertools, math, os, re, sys

def small_primes(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b"\0\0"
    for p in range(2, math.isqrt(N) + 1):
        if s[p]: s[p * p::p] = bytes(len(range(p * p, N + 1, p)))
    return [p for p in range(N + 1) if s[p]]

def definition_check(N=200):
    P = small_primes(N); strict_fail = []
    for n in range(4, N + 1):
        for i in range(1, n // 2):
            for j in range(i + 1, n // 2 + 1):
                g = math.gcd(math.comb(n, i), math.comb(n, j))
                if not any(g % p == 0 for p in P if p >= i): return 'counterexample %r' % ((n, i, j),)
                if not any(g % p == 0 for p in P if p > i): strict_fail.append((n, i, j))
    if strict_fail != [(10, 3, 5), (16, 2, 6), (28, 3, 14), (28, 5, 14)]: return 'strict list %r' % strict_fail
    return None

BASE = small_primes(31623)   # sqrt(10^9) < 31623

def chunk_cases(A, B):
    lo = max(A - 1000, 0); L = B - lo + 1
    s = bytearray([1]) * L
    for p in BASE:
        if p * p > B: break
        st = max(p * p, (lo + p - 1) // p * p)
        if st <= B: s[st - lo::p] = bytes(len(range(st - lo, L, p)))
    for x in (0, 1):
        if lo <= x <= B: s[x - lo] = 0
    total, prev = 0, None
    if A < 2000:   # direct per-n count where floor(n/2)-1 can be smaller than G(n)
        for n in range(lo, B + 1):
            if s[n - lo]: prev = n
            if n >= max(A, 4): total += min(n - prev, n // 2 - 1)
        return total
    idx = s.find(1); assert 0 <= idx and lo + idx < A, 'no prime in the margin below the chunk'
    ps = list(itertools.compress(range(lo, B + 1), s))
    ps.append(B + 1)           # sentinel: n runs up to B
    for p, q in zip(ps, ps[1:]):
        a, b = max(p, A), min(q - 1, B)   # n in [a, b] has G(n) = n - p
        if a <= b: total += (a - p + b - p) * (b - a + 1) // 2
    return total

def main(path):
    err = definition_check()
    if err: print('definition check FAILED:', err); return False
    print('definition check: n <= 200, all pairs: no counterexample; strict exceptions exactly (10,3,5) (16,2,6) (28,3,14) (28,5,14)')
    rows = []
    for line in open(path):
        if not line.strip(): continue
        d = dict(re.findall(r'(\w+)=(\d+)', line))
        if not line.startswith('DONE') or set(d) != {'A', 'B', 'strict', 'cases', 'enumerated', 'overflow', 'candidates'}:
            print('malformed line:', line.strip()[:80]); return False
        rows.append({k: int(v) for k, v in d.items()})
    rows.sort(key=lambda r: r['A']); end = -1
    for r in rows:
        if r['A'] != end + 1 or r['B'] < r['A'] or r['strict'] != 0 or r['candidates'] != 0 or r['overflow'] != 0:
            print('certificate check FAILED at', r); return False
        end = r['B']
    if rows[0]['A'] > 4 or end < 10 ** 9: print('certificate check FAILED: coverage ends at', end); return False
    print('certificate check: %d chunks cover [%d, %d] contiguously, candidates=0 and overflow=0 in all' % (len(rows), rows[0]['A'], end))
    bad = [(r['A'], r['B'], r['cases']) for r in rows if chunk_cases(r['A'], r['B']) != r['cases']]
    if bad: print('recount FAILED at', bad[:3]); return False
    print('recount: case counts recomputed independently for all %d chunks; total %d' % (len(rows), sum(r['cases'] for r in rows)))
    cov = open(os.path.join(os.path.dirname(path), 'coverage_output.txt')).read()
    want = ('chunks=%d first_A=%d last_B=%d gaps=[] bad=[]\ntotal (n,i) cases=%d enumerated_j=%d\nCOVERAGE_COMPLETE_4_TO_1e9\n'
            % (len(rows), rows[0]['A'], end, sum(r['cases'] for r in rows), sum(r['enumerated'] for r in rows)))
    if cov != want: print('coverage summary check FAILED: object/coverage_output.txt disagrees with the chunk lines'); return False
    print('coverage summary check: object/coverage_output.txt agrees with the chunk lines (counts, range, totals)')
    return True

if __name__ == '__main__':
    ok = main(sys.argv[1] if len(sys.argv) > 1 else 'object/seg699_chunk_summaries.txt')
    print('PASS' if ok else 'FAIL')
