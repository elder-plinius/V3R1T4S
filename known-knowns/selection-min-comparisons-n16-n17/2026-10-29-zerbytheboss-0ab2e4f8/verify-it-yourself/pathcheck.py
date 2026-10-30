#!/usr/bin/env python3
"""Independent path-sensitive checker (audit).  Own parser (exact generator layout,
PLAIN dialect only, with let), own semantics.  For each (function, exact known
poset on its arguments) reached from the root it checks: leaf rank exact, every
dropped element's rank interval excludes r, callee rank = r - #dropped-below.
No intersection of preconditions; memoised on (function, poset).  Returns exact
feasible worst case."""
import re, sys
sys.setrecursionlimit(10000)
W = r"[a-z][a-z0-9_]*"
FN = re.compile(rf"/// n = (\d+)(?:, i = (\d+))?(?:, {W} < {W})*\nfn (select_\d+)\(\[([a-z0-9_, ]*)\]: \[usize; (\d+)\]\) -> usize \{{\n(.*?)\n\}}\n", re.S)
RUN = re.compile(r"pub fn run\(input: \[usize; (\d+)\]\) -> usize \{\n\s*(select_\d+)\(input\)\n\}")
CONST = re.compile(r"pub const (N|I): usize = (\d+);")
def names(s): return [t.strip() for t in s.strip().strip("()").split(",")]
def parse_stmt(s):
    m = re.fullmatch(r"(select_\d+)\(\[([a-z0-9_, ]*)\]\)", s)
    if m: return ("call", m.group(1), names(m.group(2)))
    assert re.fullmatch(W, s), s
    return ("ret", s)
def load(text):
    F = {}
    for m in FN.finditer(text):
        n, i, name, ps, ar, body = m.groups()
        ps = names(ps); assert len(ps) == int(ar) == int(n)
        i = int(i) if i else 0
        b = [x.strip() for x in body.split("\n")]
        if len(b) == 1:
            F[name] = (ps, i, None, [(parse_stmt(b[0]), {})])
        elif len(b) == 5:
            c = re.fullmatch(rf"if ({W}) < ({W}) \{{", b[0]); assert c and b[2] == "} else {" and b[4] == "}"
            F[name] = (ps, i, (c.group(1), c.group(2)), [(parse_stmt(b[1]), {}), (parse_stmt(b[3]), {})])
        elif len(b) == 6:
            c = re.fullmatch(rf"let ({W}|\([a-z0-9_, ]+\)) = if ({W}) < ({W}) \{{", b[0]); assert c and b[2] == "} else {" and b[4] == "};"
            pat = names(c.group(1)); tv = names(b[1]); ev = names(b[3]); assert len(pat) == len(tv) == len(ev)
            after = parse_stmt(b[5])
            F[name] = (ps, i, (c.group(2), c.group(3)), [(after, dict(zip(pat, tv))), (after, dict(zip(pat, ev)))])
        else:
            raise SystemExit(f"cannot parse body of {name}")
    nfn = len(re.findall(r"^fn select_", text, re.M))
    assert nfn == len(F), (nfn, len(F))
    r = RUN.search(text); consts = dict((k, int(v)) for k, v in CONST.findall(text))
    return F, r.group(2), consts
def pc(x): return bin(x).count("1")
def add(Q, lo, hi):
    up = Q[hi] | (1 << hi)
    return tuple(a | up if (u == lo or (a >> lo) & 1) else a for u, a in enumerate(Q))
def main(path):
    text = open(path, encoding="ascii").read()
    F, root, consts = load(text)
    memo = {}; visited_fn = set()
    def solve(f, Q):
        key = (f, Q)
        if key in memo: return memo[key]
        visited_fn.add(f)
        ps, r, cmp, branches = F[f]
        m = len(ps); idx = {p: k for k, p in enumerate(ps)}
        below = [0] * m
        for u in range(m):
            for v in range(m):
                if (Q[u] >> v) & 1: below[v] |= 1 << u
        if cmp is None:
            outs = [(Q, branches[0])]
        else:
            x, y = idx[cmp[0]], idx[cmp[1]]
            outs = []
            if not (Q[y] >> x) & 1: outs.append((add(Q, x, y) if not (Q[x] >> y) & 1 else Q, branches[0]))
            if not (Q[x] >> y) & 1: outs.append((add(Q, y, x) if not (Q[y] >> x) & 1 else Q, branches[1]))
        worst = 0
        for Qb, (st, bind) in outs:
            bl = [0] * m
            for u in range(m):
                for v in range(m):
                    if (Qb[u] >> v) & 1: bl[v] |= 1 << u
            if st[0] == "ret":
                p = idx[bind.get(st[1], st[1])]
                assert pc(bl[p]) == r and pc(Qb[p]) == m - 1 - r, f"{f}: wrong leaf"
                c = 0
            else:
                g = st[1]; args = [idx[bind.get(a, a)] for a in st[2]]
                assert len(set(args)) == len(args) == len(F[g][0]), f"{f}: bad args"
                kb = 0
                for e in range(m):
                    if e in args: continue
                    lo_rank, hi_rank = pc(bl[e]), m - 1 - pc(Qb[e])
                    if hi_rank < r: kb += 1
                    elif lo_rank > r: pass
                    else: raise AssertionError(f"{f}: drops possible answer {ps[e]}")
                assert F[g][1] == r - kb, f"{f}: callee {g} rank {F[g][1]} != {r-kb}"
                k = len(args)
                Qg = tuple(sum(1 << l for l in range(k) if (Qb[args[j]] >> args[l]) & 1) for j in range(k))
                c = solve(g, Qg)
            worst = max(worst, c)
        res = worst + (1 if cmp is not None else 0)
        memo[key] = res
        return res
    n = len(F[root][0])
    w = solve(root, tuple([0] * n))
    print(f"{path.split('/')[-1]}: n={n} i1={F[root][1]+1} constI={consts.get('I')} exact_worst={w} "
          f"states={len(memo)} fns_reached={len(visited_fn)}/{len(F)}")
if __name__ == "__main__":
    for p in sys.argv[1:]: main(p)
