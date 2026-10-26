"""Exhaustive check of the turn-corner rule for all 24 ordered pairs of perpendicular steps.

For each ordered pair (dp, di) of perpendicular directions (step k-1 along dp, step k along di), build the
smallest open configuration that contains the turn and its corner: v_0 = 0, v_1 = e_dp, v_2 = e_dp + e_di, and the
corner u = v_0 + v_2 - v_1 = e_di, all open (everything else closed). Compute intrinsic distances by BFS and the
true parent of v_2 by the stated rule (smallest direction index, seen from the child). Then compare:
  truth : "u open makes v_1 NOT the parent of v_2"   (so u must be closed on a tree path through v_0 v_1 v_2)
  code  : (dp ^ 1) < (di ^ 1)                         (par/main.go), with u = v_2 - e_dp (par/main.go)
  defn  : dirindex(u - v_2) < dirindex(v_1 - v_2)     (PROOF.md, C(gamma))
All three must agree in every case, and the code's corner site must equal the geometric corner.
"""
from collections import deque

DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


rows = []
bad = 0
for dp in range(6):
    for di in range(6):
        if di >> 1 == dp >> 1:
            continue  # same axis: not a turn
        v0 = (0, 0, 0)
        v1 = DIRS[dp]
        v2 = add(v1, DIRS[di])
        u = add(v0, sub(v2, v1))
        u_code = sub(v2, DIRS[dp])
        opn = {v0, v1, v2, u}
        dist = {v0: 0}
        q = deque([v0])
        while q:
            x = q.popleft()
            for d in DIRS:
                y = add(x, d)
                if y in opn and y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)
        parent = None
        for k in range(6):  # smallest direction index seen from the child v2
            w = add(v2, DIRS[k])
            if dist.get(w) == dist[v2] - 1:
                parent = w
                break
        truth = parent != v1
        code = (dp ^ 1) < (di ^ 1)
        defn = DIRS.index(sub(u, v2)) < DIRS.index(sub(v1, v2))
        ok = truth == code == defn and u == u_code and dist[u] == 1 and dist[v2] == 2
        bad += not ok
        rows.append((dp, di, dist[u], truth, code, defn, ok))

print("dp di  d(u)  u_preferred(truth)  code  definition  ok")
for r in rows:
    print("%2d %2d   %d     %-5s               %-5s %-5s       %s" % r)
print("%d ordered perpendicular pairs; %d disagreements; corner forced in %d cases"
      % (len(rows), bad, sum(r[3] for r in rows)))
