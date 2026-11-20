"""Enumerate subgroups (up to conjugacy) of G = AGL(1, Z_n) on coordinates x Sym on symbols, write element files.

usage: python gen_groups.py n q outdir [min_order]
Symbol group: S_q for q <= 4, AGL(1, q) for q = 5. Each subgroup class rep is written as outdir/g<k>.txt with one
element per line (coordinate permutation then symbol permutation), and outdir/manifest.tsv lists k, order, generators.
Every subgroup is reached: classes are grown by adding one element of G at a time to class reps, to a fixpoint.
"""
import itertools, math, os, sys


def main():
    n, q, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    min_order = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    os.makedirs(out, exist_ok=True)
    coords = [(a, b) for a in range(1, n) if math.gcd(a, n) == 1 for b in range(n)]
    if n == 1:
        coords = [(1, 0)]
    if q <= 4:
        syms = list(itertools.permutations(range(q)))
    else:
        syms = [tuple((e * x + c) % q for x in range(q)) for e in range(1, q) for c in range(q)]
    cperm = [tuple((a * i + b) % n for i in range(n)) for a, b in coords]
    clabel = [f'{a}i+{b}' for a, b in coords]
    elems = [(p, s) for p in cperm for s in syms]
    labels = [f'({cl};{"".join(map(str, s))})' for cl in clabel for s in syms]
    index = {e: i for i, e in enumerate(elems)}
    M = len(elems)

    def comp(g, h):  # g after h
        pg, sg = elems[g]; ph, sh = elems[h]
        return index[(tuple(pg[ph[i]] for i in range(n)), tuple(sg[sh[x]] for x in range(q)))]

    table = [[comp(g, h) for h in range(M)] for g in range(M)]
    ident = index[(tuple(range(n)), tuple(range(q)))]
    inv = [next(h for h in range(M) if table[g][h] == ident) for g in range(M)]

    def closure(gens):
        S = {ident}; frontier = [ident]
        while frontier:
            nf = []
            for x in frontier:
                for g in gens:
                    y = table[g][x]
                    if y not in S:
                        S.add(y); nf.append(y)
            frontier = nf
        return frozenset(S)

    seen = set(); reps = []  # (subgroup, gens)

    def add(S, gens):
        if S in seen:
            return False
        for g in range(M):
            seen.add(frozenset(table[table[g][s]][inv[g]] for s in S))
        reps.append((S, gens)); return True

    add(frozenset([ident]), [])
    i = 0
    while i < len(reps):
        S, gens = reps[i]; i += 1
        done = set(S)  # <S, h> depends only on the double coset S h S
        for h in range(M):
            if h in done:
                continue
            done.update(table[table[a][h]][b] for a in S for b in S)
            T = closure(gens + [h])
            add(T, gens + [h])
    reps.sort(key=lambda r: -len(r[0]))
    with open(os.path.join(out, 'manifest.tsv'), 'w') as mf:
        k = 0
        for S, gens in reps:
            if len(S) < min_order:
                continue
            with open(os.path.join(out, f'g{k}.txt'), 'w') as f:
                for e in sorted(S):
                    p, s = elems[e]
                    f.write(' '.join(map(str, p)) + ' ' + ' '.join(map(str, s)) + '\n')
            mf.write(f'{k}\t{len(S)}\t{" ".join(labels[g] for g in gens)}\n')
            k += 1
    print(f'G order {M}, subgroup classes {len(reps)}, written {k} (order >= {min_order})')


if __name__ == '__main__':
    main()
