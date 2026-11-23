"""Standard-library checker for one qubit stabilizer code [[n,k,4]] in the claim's object file.

Usage: python3 check_stabilizer.py OBJECT.json N K TABLE_EXCERPT.txt

The object file lists several codes; this run selects the one with the given n and k.
Checks, from the definition (exact integer bit arithmetic, no sampling):
 1. the r generators (rows HX | HZ over GF(2)) pairwise commute (symplectic product 0);
 2. their GF(2) rank is r = n - k;
 3. the Pauli strings in the file agree with HX, HZ;
 4. no Pauli of weight 1, 2 or 3 commutes with every generator, so the normalizer N(S)
    (which contains S) has no nonidentity element of weight 3 or less, hence no nontrivial
    logical of weight <= 3 and d >= 4 (method A: syndrome table from HX, HZ);
 5. the same weight 1..3 search done again by a separate implementation (method B: direct
    commutation of each candidate with the Pauli strings, no syndrome table);
 6. an element of N(S) of weight exactly 4 that is not in the span of S exists (a logical
    operator of weight 4), so d = 4 exactly;
 7. the live codetables.de cell excerpt: lower bound < 4 <= upper bound.
Prints a final line beginning RESULT."""
import sys, json, re, itertools
from collections import defaultdict

def rank_basis(rows):
    basis = []
    for v in rows:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis), basis

def main(path, n, k, table_path):
    d = json.load(open(path))
    cs = [c for c in d['new_optimal_codes'] if c['n'] == n and c['k'] == k]
    assert len(cs) == 1, 'code not found exactly once'
    c = cs[0]
    r = c['r']; HX = c['HX']; HZ = c['HZ']; strs = c['stabilizer_generators']
    assert len(HX) == r == len(HZ) == len(strs) and all(len(x) == n for x in HX + HZ)
    assert all(v in (0, 1) for row in HX + HZ for v in row)
    mask = (1 << n) - 1
    def enc(x, z):  # X part in high n bits, Z part in low n bits; qubit q is bit n-1-q
        return (int(''.join(map(str, x)), 2) << n) | int(''.join(map(str, z)), 2)
    def sp(u, v):
        return bin(((u >> n) & (v & mask)) ^ ((u & mask) & (v >> n))).count('1') & 1
    G = [enc(HX[i], HZ[i]) for i in range(r)]
    commute = all(sp(G[i], G[j]) == 0 for i in range(r) for j in range(r))
    rk, basis = rank_basis(G)
    rank_ok = (rk == r and n - r == k)
    code = {'I': (0, 0), 'X': (1, 0), 'Z': (0, 1), 'Y': (1, 1)}
    agree = all(len(s) == n and all((HX[i][q], HZ[i][q]) == code[ch] for q, ch in enumerate(s))
                for i, s in enumerate(strs))
    # method A: syndromes of single-qubit Paulis
    def synd(op):
        return sum(sp(op, G[i]) << i for i in range(r))
    single = defaultdict(list)  # qubit -> list of (op, syndrome)
    for q in range(n):
        for (xb, zb) in ((1, 0), (0, 1), (1, 1)):
            op = ((xb << (n - 1 - q)) << n) | (zb << (n - 1 - q))
            single[q].append((op, synd(op)))
    badA = 0
    for w in (1, 2, 3):
        for comb in itertools.combinations(range(n), w):
            for sel in itertools.product(*[single[q] for q in comb]):
                sy = 0
                for _, s in sel:
                    sy ^= s
                if sy == 0:
                    badA += 1
    # method B: direct commutation with the Pauli strings (separate encoding, no syndromes)
    sx = []; sz = []
    for s in strs:
        sx.append(sum(1 << q for q, ch in enumerate(s) if ch in 'XY'))
        sz.append(sum(1 << q for q, ch in enumerate(s) if ch in 'ZY'))
    badB = 0
    for w in (1, 2, 3):
        for comb in itertools.combinations(range(n), w):
            for paulis in itertools.product('XYZ', repeat=w):
                ox = sum(1 << q for q, p in zip(comb, paulis) if p in 'XY')
                oz = sum(1 << q for q, p in zip(comb, paulis) if p in 'ZY')
                if all((bin((ox & sz[i]) ^ (oz & sx[i])).count('1') & 1) == 0 for i in range(r)):
                    badB += 1
    # weight-4 element of N(S) outside span(S): meet in the middle on syndromes of pairs
    pairs = defaultdict(list)
    for q1 in range(n):
        for q2 in range(q1 + 1, n):
            for a, sa in single[q1]:
                for b, sb in single[q2]:
                    pairs[sa ^ sb].append((a ^ b, q1, q2))
    witness = None
    for lst in pairs.values():
        if witness:
            break
        for i in range(len(lst)):
            if witness:
                break
            for j in range(i + 1, len(lst)):
                o1, a1, b1 = lst[i]; o2, a2, b2 = lst[j]
                if len({a1, b1, a2, b2}) == 4:
                    op = o1 ^ o2
                    v = op
                    for bb in basis:
                        v = min(v, v ^ bb)
                    if v != 0:
                        witness = op
                        break
    wit_ok = False
    wit_str = None
    if witness is not None:
        chars = []
        for q in range(n):
            xb = (witness >> (n + n - 1 - q)) & 1
            zb = (witness >> (n - 1 - q)) & 1
            chars.append({(0, 0): 'I', (1, 0): 'X', (0, 1): 'Z', (1, 1): 'Y'}[(xb, zb)])
        wit_str = ''.join(chars)
        wt = sum(ch != 'I' for ch in chars)
        wit_ok = (wt == 4 and synd(witness) == 0)
    # live cell excerpt
    txt = open(table_path).read()
    m = re.search(r'Bounds on \[\[(\d+),(\d+)\]\].*?lower bound:\s*(\d+)\s*upper bound:\s*(\d+)', txt)
    assert m and int(m.group(1)) == n and int(m.group(2)) == k, 'table excerpt does not match n,k'
    lo, up = int(m.group(3)), int(m.group(4))
    d_found = 4 if (badA == 0 and badB == 0 and wit_ok) else None
    table_ok = d_found is not None and lo < d_found <= up
    print(f'code [[{n},{k}]] r={r}')
    print(f'generators pairwise commute: {commute}')
    print(f'GF(2) rank of generators: {rk} (need {r} = n-k = {n-k}): {rank_ok}')
    print(f'Pauli strings agree with HX, HZ: {agree}')
    print(f'weight 1..3 Paulis commuting with every generator: method A {badA}, method B {badB}')
    print(f'weight-4 element of N(S) outside span(S) (logical of weight 4): {wit_str}  verified: {wit_ok}')
    print(f'live codetables.de cell: lower bound {lo}, upper bound {up}; d = {d_found}; strictly above lower and within upper: {table_ok}')
    ok = commute and rank_ok and agree and badA == 0 and badB == 0 and wit_ok and table_ok
    print(f'RESULT {"PASS" if ok else "FAIL"} [[{n},{k},{d_found}]] live [{lo},{up}]')
    sys.exit(0 if ok else 1)

main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
