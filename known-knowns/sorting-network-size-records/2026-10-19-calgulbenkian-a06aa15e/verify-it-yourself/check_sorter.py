#!/usr/bin/env python3
"""Exact 0-1 principle checker for a sorting network (standard library only).

Usage: python3 check_sorter.py NETWORK_FILE EXPECT_N EXPECT_SIZE EXPECT_DEPTH LISTED_JSON [--neg]

File format: first line "n size", then one comparator "i j" per line (0 <= i < j < n,
the minimum goes to wire i). The network is applied to all 2**n binary inputs, but not by
enumerating them: the checker tracks the exact set of reachable states of each connected
group of wires. Wires that have never been compared (directly or through other wires) are
independent, so the reachable set of a union of two groups is the product of their sets.
The network sorts all 2**n binary inputs if and only if, after the last comparator, all
wires form one group and the reachable set is exactly the n+1 sorted states 0...01...1
(every weight 0..n occurs, because the 2**n inputs include every weight).
Wire w is bit w of a state; a sorted state with k ones has the k highest wires set.

The size, the greedy (as-soon-as-possible) layering depth, and the comparison with the
listed (size, depth) pairs of LISTED_JSON are reported. --neg deletes the middle
comparator before checking (a negative control: the result must be SORTS false).
The last output line is a JSON object.
"""
import sys, json


def run(path, neg):
    toks = open(path).read().split()
    n, size = int(toks[0]), int(toks[1])
    vals = [int(t) for t in toks[2:]]
    if len(vals) % 2:
        return {"SORTS": False, "why": "odd number of integers"}
    ces = [(vals[k], vals[k + 1]) for k in range(0, len(vals), 2)]
    res = {"file": path.split("/")[-1], "n": n, "size": len(ces), "header_size": size}
    if neg:
        del ces[len(ces) // 2]
        res["negative_control_deleted_comparator_index"] = size // 2
        res["size"] = len(ces)
    if any(not (0 <= a < b < n) for a, b in ces) or (len(ces) != size and not neg):
        res.update(SORTS=False, why="bad comparator or header size mismatch")
        return res
    lay = [0] * n
    depth = 0
    for i, j in ces:
        l = 1 + max(lay[i], lay[j])
        lay[i] = lay[j] = l
        if l > depth:
            depth = l
    res["depth"] = depth
    comp = list(range(n))
    members = {w: [w] for w in range(n)}
    S = {w: {0, 1 << w} for w in range(n)}
    maxstates = 0
    for i, j in ces:
        ci, cj = comp[i], comp[j]
        if ci != cj:
            A, B = S[ci], S[cj]
            S[ci] = {x | y for x in A for y in B}
            for w in members[cj]:
                comp[w] = ci
            members[ci] += members.pop(cj)
            del S[cj]
        both = (1 << i) | (1 << j)
        V = S[ci]
        moved = {x for x in V if (x & both) == (1 << i)}
        if moved:
            V -= moved
            V |= {x ^ both for x in moved}
        if len(V) > maxstates:
            maxstates = len(V)
    res["max_states_tracked"] = maxstates
    if len(S) != 1:
        res.update(SORTS=False, why="wires not all connected: %d groups" % len(S))
        return res
    V = next(iter(S.values()))
    full = (1 << n) - 1
    sorted_states = {full ^ ((1 << (n - k)) - 1) for k in range(n + 1)}
    res["final_states"] = len(V)
    res["SORTS"] = (V == sorted_states)
    return res


def main():
    path = sys.argv[1]
    en, es, ed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    listed = json.load(open(sys.argv[5]))
    neg = "--neg" in sys.argv
    res = run(path, neg)
    if not neg and res.get("SORTS"):
        res["matches_stated_n_size_depth"] = (res["n"], res["size"], res["depth"]) == (en, es, ed)
        pairs = [tuple(p) for p in listed["listed_pairs"]]
        res["listed_pairs"] = [list(p) for p in pairs]
        res["listed_pairs_that_weakly_dominate_this_pair"] = [list(p) for p in pairs if p[0] <= es and p[1] <= ed]
        res["listed_pairs_that_this_pair_weakly_dominates"] = [list(p) for p in pairs if es <= p[0] and ed <= p[1]]
        res["not_dominated_by_any_listed_pair"] = not res["listed_pairs_that_weakly_dominate_this_pair"]
        res["smaller_size_than_every_listed_pair"] = all(es < p[0] for p in pairs)
        res["smaller_depth_than_every_listed_pair"] = all(ed < p[1] for p in pairs)
    print(json.dumps(res))
    return 0


sys.exit(main())
