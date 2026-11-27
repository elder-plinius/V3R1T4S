"""Standard-library checker for one qubit stabilizer code [[n,k,5]] in the claim's object file.

Usage: python3 check_stabilizer.py OBJECT.json N K TABLE_EXCERPT.txt

The object file lists ten codes; this run selects the one with the given n and k.
Checks, from the definition (exact integer bit arithmetic, no sampling):
 1. the r generators (rows HX | HZ over GF(2)) pairwise commute (symplectic product 0);
 2. their GF(2) rank is r = n - k;
 3. the Pauli strings in the file agree with HX, HZ;
 4. pure distance at least 5: every Pauli error of weight 0, 1 or 2 (1 + 3n + 9*C(n,2)
    errors, identity included) has a distinct syndrome. A nonidentity Pauli of weight <= 4
    is a product of two errors of weight <= 2, so with all syndromes distinct no nonidentity
    Pauli of weight <= 4 commutes with every generator: the normalizer N(S), which contains
    S, has no nonidentity element of weight 1 to 4 (method A: syndromes from HX, HZ);
 5. the same enumeration done again by a separate implementation (method B: syndromes by
    direct commutation of each error, written as a Pauli string, with the generator strings);
 6. d = 5 exactly: an element of N(S) of weight exactly 5 that is not in the span of S
    (a nontrivial logical operator of weight 5) is found and verified by direct commutation.
    This witness search is a meet in the middle on syndromes (weight 2 plus weight 3,
    disjoint supports). d = 6 is therefore excluded;
 7. the live codetables.de cell excerpt: lower bound < 5 <= upper bound.
Prints a final line beginning RESULT."""
import sys, json, re, itertools

def reduce_with(basis, v):
    for b in basis:
        v = min(v, v ^ b)
    return v

def rank_basis(rows):
    basis = []
    for v in rows:
        v = reduce_with(basis, v)
        if v:
            basis.append(v)
    return len(basis), basis

def main(path, n, k, table_path):
    d = json.load(open(path))
    cs = [c for c in d['new_d5_codes'] if c['n'] == n and c['k'] == k]
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

    # ---- method A: syndromes from the binary rows
    def synd(op):
        return sum(sp(op, G[i]) << i for i in range(r))
    single = []  # per qubit: list of (operator, syndrome) for X, Z, Y
    for q in range(n):
        lst = []
        for (xb, zb) in ((1, 0), (0, 1), (1, 1)):
            op = ((xb << (n - 1 - q)) << n) | (zb << (n - 1 - q))
            lst.append((op, synd(op)))
        single.append(lst)
    seenA = {0: 1}
    collA = 0
    def note(s):
        nonlocal collA
        if s in seenA:
            collA += 1
        else:
            seenA[s] = 1
    for q in range(n):
        for _, s in single[q]:
            note(s)
    for q1 in range(n):
        for q2 in range(q1 + 1, n):
            for _, sa in single[q1]:
                for _, sb in single[q2]:
                    note(sa ^ sb)
    n_err = 1 + 3 * n + 9 * n * (n - 1) // 2

    # ---- method B: syndromes by direct commutation with the Pauli strings
    sx = [sum(1 << q for q, ch in enumerate(s) if ch in 'XY') for s in strs]
    sz = [sum(1 << q for q, ch in enumerate(s) if ch in 'ZY') for s in strs]
    def syndB(ox, oz):
        s = 0
        for i in range(r):
            s |= (bin((ox & sz[i]) ^ (oz & sx[i])).count('1') & 1) << i
        return s
    letters = ((1, 0), (0, 1), (1, 1))
    seenB = {0}
    collB = 0
    for q in range(n):
        for (a, b) in letters:
            s = syndB(a << q, b << q)
            if s in seenB: collB += 1
            else: seenB.add(s)
    for q1 in range(n):
        for q2 in range(q1 + 1, n):
            for (a1, b1) in letters:
                for (a2, b2) in letters:
                    s = syndB((a1 << q1) | (a2 << q2), (b1 << q1) | (b2 << q2))
                    if s in seenB: collB += 1
                    else: seenB.add(s)

    # ---- weight-5 element of N(S) outside span(S): weight 2 plus weight 3, disjoint supports
    wit = None
    if commute and rank_ok and agree and collA == 0 and collB == 0:
        pairs = {}
        for q1 in range(n):
            for q2 in range(q1 + 1, n):
                for a, sa in single[q1]:
                    for b, sb in single[q2]:
                        pairs.setdefault(sa ^ sb, []).append((a ^ b, q1, q2))
        for q1 in range(n):
            if wit: break
            for q2 in range(q1 + 1, n):
                if wit: break
                for q3 in range(q2 + 1, n):
                    if wit: break
                    for a, sa in single[q1]:
                        for b, sb in single[q2]:
                            for cc, sc in single[q3]:
                                lst = pairs.get(sa ^ sb ^ sc)
                                if not lst:
                                    continue
                                for (o2, p, q) in lst:
                                    if p in (q1, q2, q3) or q in (q1, q2, q3):
                                        continue
                                    op = a ^ b ^ cc ^ o2
                                    if reduce_with(basis, op) != 0:
                                        wit = op
                                        break
                                if wit: break
                            if wit: break
                        if wit: break
    wit_ok = False
    wit_str = None
    if wit is not None:
        chars = []
        for q in range(n):
            xb = (wit >> (n + n - 1 - q)) & 1
            zb = (wit >> (n - 1 - q)) & 1
            chars.append({(0, 0): 'I', (1, 0): 'X', (0, 1): 'Z', (1, 1): 'Y'}[(xb, zb)])
        wit_str = ''.join(chars)
        wt = sum(ch != 'I' for ch in chars)
        wx = sum(1 << q for q, ch in enumerate(wit_str) if ch in 'XY')
        wz = sum(1 << q for q, ch in enumerate(wit_str) if ch in 'ZY')
        wit_ok = (wt == 5 and synd(wit) == 0 and syndB(wx, wz) == 0 and reduce_with(basis, wit) != 0)
    # ---- live cell excerpt
    txt = open(table_path).read()
    m = re.search(r'Bounds on \[\[(\d+),(\d+)\]\].*?lower bound:\s*(\d+)\s*upper bound:\s*(\d+)', txt)
    assert m and int(m.group(1)) == n and int(m.group(2)) == k, 'table excerpt does not match n,k'
    lo, up = int(m.group(3)), int(m.group(4))
    pure_ok = (collA == 0 and collB == 0)
    d_found = 5 if (pure_ok and wit_ok) else None
    table_ok = d_found is not None and lo < d_found <= up
    print(f'code [[{n},{k}]] r={r}')
    print(f'generators pairwise commute: {commute}')
    print(f'GF(2) rank of generators: {rk} (need {r} = n-k = {n-k}): {rank_ok}')
    print(f'Pauli strings agree with HX, HZ: {agree}')
    print(f'errors of weight 0..2 enumerated: {n_err}; syndrome collisions: method A {collA}, method B {collB}')
    print(f'pure distance >= 5: {pure_ok}')
    print(f'weight-5 element of N(S) outside span(S) (logical of weight 5, so d = 5 and d = 6 excluded): {wit_str}  verified: {wit_ok}')
    print(f'live codetables.de cell: lower bound {lo}, upper bound {up}; d = {d_found}; strictly above lower and within upper: {table_ok}')
    ok = commute and rank_ok and agree and pure_ok and wit_ok and table_ok
    print(f'RESULT {"PASS" if ok else "FAIL"} [[{n},{k},{d_found}]] live [{lo},{up}]')
    sys.exit(0 if ok else 1)

main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
