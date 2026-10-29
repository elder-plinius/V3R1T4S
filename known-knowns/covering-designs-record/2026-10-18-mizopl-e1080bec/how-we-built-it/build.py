#!/usr/bin/env python3
"""Build the combining design from a splitopt plan (JSON line). Usage: build.py PLAN.jsonl LINE_NO OUT.txt
Writes 0-based blocks, one per line, deduplicated. Also writes OUT.parts (part id per block) for pruning orders."""
import sys, json, math
RUN = './runs/2026-10-18-0304'

def pad(blk, k, n):
    s = set(blk)
    assert len(s) <= k <= n, (len(s), k, n)
    x = 0
    while len(s) < k:
        if x not in s: s.add(x)
        x += 1
    return tuple(sorted(s))

def design(n, kk, tt, E):
    """list of kk-subsets of range(n) forming an (n,kk,tt) covering, from source E=(count,src)."""
    cnt, src = E
    kind = src[0]
    if kind == 'triv0':
        out = [tuple(range(kk))]
    elif kind == 'whole':
        out = [tuple(range(n))]
    elif kind == 'triv1':
        out = []
        for i in range(math.ceil(n / kk)):
            s = min(i * kk, n - kk)
            out.append(tuple(range(s, s + kk)))
    else:
        _, a, b, t = src
        rows = [list(map(int, l.replace(',', ' ').split())) for l in open(f'{RUN}/data/ljcr_designs/C_{a}_{b}_{t}.txt') if l.strip()]
        lo = min(min(r) for r in rows); hi = max(max(r) for r in rows)
        base = 0 if (lo == 0 or hi <= a - 1) else 1
        out = []
        for r in rows:
            r = [x - base for x in r]
            assert len(r) == b and all(0 <= x < a for x in r)
            out.append(pad([x for x in r if x < n], kk, n))
        out = sorted(set(out))
        assert len(out) <= cnt, (len(out), cnt)
    out = sorted(set(out))
    assert all(len(b) == kk for b in out)
    return out

def main():
    plan = [json.loads(l) for l in open(sys.argv[1])][int(sys.argv[2])]
    out = sys.argv[3]
    v, k, t, v1 = plan['v'], plan['k'], plan['t'], plan['v1']; v2 = v - v1
    blocks = {}  # block -> part
    def add(b, part):
        b = tuple(sorted(b)); assert len(b) == k and len(set(b)) == k
        if b not in blocks: blocks[b] = part
    if plan['head']:
        _, h, E = plan['head']
        for a in design(v1, k - v2, h, E): add(list(a) + [v1 + x for x in range(v2)], 'H')
    for j, (k1, A, B) in plan['terms']:
        DA = design(v1, k1, j, A) if k1 > 0 else [()]
        DB = design(v2, k - k1, t - j, B) if k - k1 > 0 else [()]
        for a in DA:
            for b in DB: add(list(a) + [v1 + x for x in b], f'j{j}')
    if plan['tail']:
        _, a0, E = plan['tail']
        for b in design(v2, k - v1, t - a0, E): add(list(range(v1)) + [v1 + x for x in b], 'T')
    with open(out, 'w') as f, open(out + '.parts', 'w') as g:
        for b, p in blocks.items():
            f.write(' '.join(map(str, b)) + '\n'); g.write(p + '\n')
    print(f'built v={v} k={k} t={t} v1={v1} b_pred={plan["b_pred"]} blocks={len(blocks)} -> {out}')

main()
