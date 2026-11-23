#!/usr/bin/env python3
"""Independent Checker 1 (Python standard library):
Verifies from first principles using explicit Python frozenset operations:
1. Calibration on Szykula-Vorel 4-letter series A_m at n=5 (rt=11), n=9 (rt=39), n=13 (rt=83),
   and Cerny automaton C_5 (non-Eulerian rejected, rt=16).
2. Completeness, alphabet/state bounds (3 <= n <= 30, k >= 1), Eulerian in-degree = k at every state,
   all-pairs strong connectivity, explicit Hierholzer Eulerian directed cycle of length n*k,
   pair-automaton synchronizability, and exact forward + backward power-set BFS reset threshold
   strictly exceeding floor((n^2 - 3) / 2).
"""
import json
import sys
from collections import deque


def evaluate_dfa_frozenset(n, k, trans):
    if not isinstance(n, int) or not isinstance(k, int) or n < 3 or n > 30 or k < 1:
        return False, "invalid n or k", -1, None
    if not isinstance(trans, list) or len(trans) != k:
        return False, "transition row count != k", -1, None
    for a in range(k):
        row = trans[a]
        if not isinstance(row, list) or len(row) != n:
            return False, f"row {a} length != n", -1, None
        for q in range(n):
            v = row[q]
            if not isinstance(v, int) or isinstance(v, bool) or v < 0 or v >= n:
                return False, f"invalid state entry at ({a}, {q})", -1, None

    indeg = [0] * n
    for a in range(k):
        for q in range(n):
            indeg[trans[a][q]] += 1
    in_deg_ok = all(d == k for d in indeg)

    sc_ok = True
    for s in range(n):
        seen = {s}
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for a in range(k):
                w = trans[a][u]
                if w not in seen:
                    seen.add(w)
                    dq.append(w)
        if len(seen) != n:
            sc_ok = False
            break

    is_eulerian = in_deg_ok and sc_ok

    if is_eulerian:
        idx = [0] * n
        stack = [(0, None)]
        circuit = []
        while stack:
            u, edge = stack[-1]
            if idx[u] < k:
                a = idx[u]
                idx[u] += 1
                stack.append((trans[a][u], (u, a, trans[a][u])))
            else:
                stack.pop()
                if edge is not None:
                    circuit.append(edge)
        circuit.reverse()
        if len(circuit) != n * k or len({(u, a) for (u, a, _) in circuit}) != n * k:
            return False, "Eulerian cycle edge bijection failed", -1, None
        for i in range(len(circuit)):
            if circuit[i][2] != circuit[(i + 1) % len(circuit)][0]:
                return False, "Eulerian cycle continuity failed", -1, None

    pre = [[[] for _ in range(n)] for _ in range(k)]
    for a in range(k):
        for u in range(n):
            pre[a][trans[a][u]].append(u)
    merged = set()
    pq = deque()
    for a in range(k):
        for q in range(n):
            ps = pre[a][q]
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    pair = (min(ps[i], ps[j]), max(ps[i], ps[j]))
                    if pair not in merged:
                        merged.add(pair)
                        pq.append(pair)
    while pq:
        u, v = pq.popleft()
        for a in range(k):
            for x in pre[a][u]:
                for y in pre[a][v]:
                    if x != y:
                        pair = (min(x, y), max(x, y))
                        if pair not in merged:
                            merged.add(pair)
                            pq.append(pair)
    pair_sync = (len(merged) == n * (n - 1) // 2)
    if not pair_sync:
        return is_eulerian, "not pair-synchronizing", -1, None

    full = frozenset(range(n))
    dist = {full: 0}
    parent = {full: None}
    dq = deque([full])
    rt_fwd = -1
    best_word = None
    while dq:
        S = dq.popleft()
        d = dist[S]
        if len(S) == 1:
            rt_fwd = d
            letters = []
            cur = S
            while parent[cur] is not None:
                prev_s, act = parent[cur]
                letters.append(act)
                cur = prev_s
            best_word = list(reversed(letters))
            break
        for a in range(k):
            row = trans[a]
            S2 = frozenset(row[x] for x in S)
            if S2 not in dist:
                dist[S2] = d + 1
                parent[S2] = (S, a)
                dq.append(S2)

    if rt_fwd < 0 or best_word is None:
        return is_eulerian, "forward subset BFS found no singleton", -1, None

    sim = set(range(n))
    for a in best_word:
        sim = {trans[a][x] for x in sim}
    if len(sim) != 1 or len(best_word) != rt_fwd:
        return is_eulerian, "reset word replay mismatch", -1, None

    if n <= 15:
        bdist = {}
        bdq = deque()
        for q in range(n):
            sq = frozenset([q])
            bdist[sq] = 0
            bdq.append(sq)
        rt_bwd = -1
        while bdq:
            S = bdq.popleft()
            d = bdist[S]
            if S == full:
                rt_bwd = d
                break
            for a in range(k):
                P = frozenset(q for q in range(n) if trans[a][q] in S)
                if len(P) > 0 and P not in bdist:
                    bdist[P] = d + 1
                    bdq.append(P)
        if rt_bwd != rt_fwd:
            return is_eulerian, f"forward/backward mismatch {rt_fwd} != {rt_bwd}", -1, None

    return is_eulerian, "ok", rt_fwd, best_word


def run_calibrations():
    for m, expected_rt in ((1, 11), (2, 39), (3, 83)):
        N = 4 * m + 1
        alpha = [(-q - 1) % N for q in range(N)]
        beta = [(-q + 1) % N for q in range(N)]
        om0 = [0 if q == 1 else q for q in range(N)]
        om1 = [1 if q == 0 else q for q in range(N)]
        eul, msg, rt, _ = evaluate_dfa_frozenset(N, 4, [alpha, beta, om0, om1])
        if not eul or rt != expected_rt:
            raise RuntimeError(f"Calibration failed on Szykula-Vorel A_{m}: eul={eul}, rt={rt}, msg={msg}")
        print(f"[PY-CALIB] Szykula-Vorel A_{m} (n={N}, k=4): eulerian={eul}, rt={rt} == {expected_rt}")

    c5_a = [1 if q == 0 else q for q in range(5)]
    c5_b = [(q + 1) % 5 for q in range(5)]
    eul_c5, _, rt_c5, _ = evaluate_dfa_frozenset(5, 2, [c5_a, c5_b])
    if eul_c5 or rt_c5 != 16:
        raise RuntimeError(f"Calibration failed on Cerny C_5: eul={eul_c5}, rt={rt_c5}")
    print(f"[PY-CALIB] Cerny C_5 (n=5, k=2): eulerian={eul_c5} (expected False), rt={rt_c5} == 16")


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_python_set_bfs.py <object.json>")
        print("FAIL")
        sys.exit(1)
    try:
        run_calibrations()
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            obj = json.load(f)
        if obj.get("target_id") != "eulerian-synchronizing-szykula-vorel-bound":
            raise ValueError("unexpected target_id")
        n = obj["n"]
        k = obj["k"]
        claimed_bound = obj["szykula_vorel_bound"]
        claimed_rt = obj["claimed_reset_threshold"]
        trans = obj["transitions"]

        true_bound = (n * n - 3) // 2
        if claimed_bound != true_bound:
            raise ValueError(f"szykula_vorel_bound {claimed_bound} != floor((n^2-3)/2) = {true_bound}")

        eul, msg, rt, word = evaluate_dfa_frozenset(n, k, trans)
        if not eul:
            raise ValueError(f"DFA is NOT Eulerian ({msg})")
        if rt != claimed_rt:
            raise ValueError(f"exact reset threshold {rt} != claimed_reset_threshold {claimed_rt}")
        if rt <= true_bound:
            raise ValueError(f"reset threshold {rt} does not strictly exceed floor((n^2-3)/2) = {true_bound}")

        w_str = "".join(str(a) for a in word)
        print(f"[PY-CHECK] Verified complete Eulerian synchronizing DFA: n={n}, k={k}, "
              f"rt={rt} > floor(({n}^2-3)/2)={true_bound}, shortest_reset_word={w_str} (len={len(word)})")
        print("PY_VERIFY_OK")
    except Exception as exc:
        print(f"[PY-ERROR] {exc}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
