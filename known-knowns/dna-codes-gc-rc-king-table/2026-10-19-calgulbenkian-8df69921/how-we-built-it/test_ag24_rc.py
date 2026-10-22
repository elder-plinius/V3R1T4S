#!/usr/bin/env python3
"""
Search all fixed-point-free involutions sigma in the full collineation group A*Gamma*L(2, 4)
of AG(2, 4) (size 5760) to maximize the GC,RC(16, 12, 8) code size!
"""
import itertools

RC_MAP = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
def rc(s):
    return ''.join(RC_MAP[c] for c in reversed(s))

def dist(x, y):
    return sum(a != b for a, b in zip(x, y))

ADD4 = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
MUL4 = [[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]
FROB = [0, 1, 3, 2] # z -> z^2

pts_all = [(x, y) for x in range(4) for y in range(4)]

def eval_pencil(m, x, y):
    if m < 4:
        return ADD4[x][MUL4[m][y]]
    else:
        return y

perms_sym = list(itertools.permutations('ACGT'))

# Enumerate all collineations sigma(x, y) = M * (f(x), f(y)) + (dx, dy)
# where f is identity or FROB, M in GL(2, 4) (180 matrices), (dx, dy) in F_4^2 (16 shifts)
fpf_involutions = []
for use_frob in [False, True]:
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    det = ADD4[MUL4[a][d]][MUL4[b][c]]
                    if det == 0:
                        continue
                    for dx in range(4):
                        for dy in range(4):
                            # Map each point
                            mp = {}
                            for x, y in pts_all:
                                fx = FROB[x] if use_frob else x
                                fy = FROB[y] if use_frob else y
                                nx = ADD4[ADD4[MUL4[a][fx]][MUL4[b][fy]]][dx]
                                ny = ADD4[ADD4[MUL4[c][fx]][MUL4[d][fy]]][dy]
                                mp[(x, y)] = (nx, ny)
                            # Check involution and fixed-point-free
                            if all(mp[mp[p]] == p and mp[p] != p for p in pts_all):
                                fpf_involutions.append((use_frob, (a,b,c,d), (dx,dy), mp))

print(f"Found {len(fpf_involutions)} fixed-point-free involutions in A*Gamma*L(2, 4)!")

# Test each conjugacy class / involution
seen_Pencil_actions = set()
best_overall = []

for use_frob, mat, sh, mp in fpf_involutions:
    used = set()
    left, right = [], []
    for p in pts_all:
        if p in used:
            continue
        q = mp[p]
        used.add(p)
        used.add(q)
        left.append(p)
        right.append(q)
    pts_order = left + list(reversed(right))

    # Build all 5 * 24 = 120 balanced pencil words
    # Wait: if sigma swaps pencil m1 <-> m2, we must solve the clique on (words_{m1} U words_{m2}) together!
    # Since 5 * 24 = 120 is tiny, and words in different pencils automatically have dist(x, y) = 12,
    # let's check which pencils are swapped by sigma!
    all_words = []
    for m in range(5):
        for p in perms_sym:
            w = ''.join(p[eval_pencil(m, x, y)] for x, y in pts_order)
            if dist(w, rc(w)) >= 12:
                all_words.append((m, w))

    # Group pencils into orbits under sigma
    # Actually let's just group words by their pencil pair {m, m_rc}!
    # Which pencil does rc(w) belong to?
    # Let's check for each m
    pencil_words = {m: [w for pm, w in all_words if pm == m] for m in range(5)}
    # Check if any word in pencil m has rc in pencil m'
    visited_m = set()
    code_this = []
    for m in range(5):
        if m in visited_m:
            continue
        # Find m' such that rc of pencil m lands in pencil m'
        # Test by checking if dist(w, u) != 12 for some u in pencil m'
        partner = m
        for m2 in range(5):
            if m2 == m:
                continue
            # Two lines from the same pencil have distance 0 or 16
            if pencil_words[m] and pencil_words[m2]:
                w0_rc = rc(pencil_words[m][0])
                if any(dist(w0_rc, u) in (0, 16) for u in pencil_words[m2]):
                    partner = m2
                    break
        if partner != m:
            visited_m.add(m)
            visited_m.add(partner)
            # We can take a 12-word A_4 code from pencil m, and its RC lands in partner,
            # wait: if we take 12 words from pencil m and 0 from partner, we get 12 words!
            # Can we get > 12 from pencil_words[m] + pencil_words[partner]?
            # No, because max clique in a single pencil is 12, and by halving bound on m U partner (max GC size 24),
            # max GC,RC size in m U partner is 24 / 2 = 12!
            # And taking 12 words of A_4 from pencil m achieves 12 immediately!
            clq_m = []
            for w in pencil_words[m]:
                if all(dist(w, u) >= 12 and dist(w, rc(u)) >= 12 for u in clq_m):
                    clq_m.append(w)
            code_this.extend(clq_m)
        else:
            visited_m.add(m)
            words_m = pencil_words[m]
            best_clq = []
            def bt(idx, cur):
                global best_clq
                if len(cur) > len(best_clq):
                    best_clq = list(cur)
                if len(cur) + (len(words_m) - idx) <= len(best_clq):
                    return
                for i in range(idx, len(words_m)):
                    w = words_m[i]
                    if all(dist(w, u) >= 12 and dist(w, rc(u)) >= 12 for u in cur):
                        cur.append(w)
                        bt(i + 1, cur)
                        cur.pop()
            bt(0, [])
            code_this.extend(best_clq)

    if len(code_this) > len(best_overall):
        best_overall = code_this
        print(f"NEW BEST GC,RC(16, 12, 8) = {len(best_overall)} (frob={use_frob}, mat={mat}, sh={sh})!")
        if len(best_overall) == 30:
            break

if len(best_overall) >= 25:
    for i in range(len(best_overall)):
        assert dist(best_overall[i], rc(best_overall[i])) >= 12
        for j in range(i + 1, len(best_overall)):
            assert dist(best_overall[i], best_overall[j]) >= 12
            assert dist(best_overall[i], rc(best_overall[j])) >= 12
    fn = f"results/gc_rc_16_12_8_{len(best_overall)}.txt"
    with open(fn, "w") as f:
        for w in best_overall:
            f.write(w + "\n")
    print(f"Verified and saved {fn}!")
