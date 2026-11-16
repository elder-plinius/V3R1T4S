#!/usr/bin/env python3
"""CEGIS + HiGHS (scipy.optimize.milp) exact synthesizer for Even-Projection DFA Invariants."""
import sys
import os
import numpy as np
from collections import deque
from scipy.optimize import milp, LinearConstraint, Bounds

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfa_synthesizer import minimize_dfa, verify_dfa_invariant


def even_dfa_to_full_dfa(n, delta_e, F0, F1):
    """Convert an even-projection DFA (Q_e, delta_e, F0, F1) into a standard total DFA over Sigma*.
    Remember:
      - empty word (len=0, p=0) -> MUST reject
      - 1-char word (len=1, p=1) -> MUST reject
      - len >= 2, p=0 -> accept iff q_e in F0
      - len >= 3, p=1 -> accept iff q_e in F1
    State tuple: (par, lcap, q_e) where lcap in {0, 1, 2} (lcap=2 means len >= 2!).
    Wait: at len=2, par=0 (even >= 2 -> accept iff q_e in F0).
    At len=3, par=1 (odd >= 3 -> lcap=2 and par=1 -> accept iff q_e in F1!).
    Let's check len=1: par=1, lcap=1 -> NOT lcap==2, so rejected!
    Let's check len=0: par=0, lcap=0 -> NOT lcap==2, so rejected!
    """
    states = [(0, 0, 0)]
    smap = {states[0]: 0}
    trans = []
    acc = set()
    idx = 0
    while idx < len(states):
        par, lcap, qe = states[idx]
        row = []
        for ch in range(n):
            nlcap = min(2, lcap + 1)
            if par == 0:
                nqe = delta_e[qe][ch]
                nst = (1, nlcap, nqe)
            else:
                nst = (0, nlcap, qe)
            if nst not in smap:
                smap[nst] = len(states)
                states.append(nst)
            row.append(smap[nst])
        trans.append(row)
        if lcap == 2:
            if par == 0 and qe in F0:
                acc.add(idx)
            elif par == 1 and qe in F1:
                acc.add(idx)
        idx += 1
    return minimize_dfa(n, trans, acc)


def check_even_dfa(rules, delta_e, F0, F1):
    """Check closure on (s, p) directly and return shortest counterexample ((s, p), (s', p')) if any!"""
    n = len(rules)
    K = len(delta_e)
    # Precompute rule action on (a, p): -> (appended_even_tuple, new_p)
    rule_act = {}
    for a in range(n):
        wa = rules[a]
        rule_act[(a, 0)] = (wa[0::2], len(wa) % 2)
        rule_act[(a, 1)] = (wa[1::2], (1 + len(wa)) % 2)

    # Check every non-halting (s, p) in L:
    # Note: halting (s, p) are ("", 0), ("", 1), and ((a,), 1) for a in 0..n-1.
    if 0 in F0 or 0 in F1:
        return (("HALT", ((), 0 if 0 in F0 else 1)))
    for a in range(n):
        if delta_e[0][a] in F1:
            return (("HALT", ((a,), 1)))

    # Product BFS for s = (a,) + u:
    for a in range(n):
        qa = delta_e[0][a]
        for p in (0, 1):
            # If p == 1 and u == (), s = (a,) which we already checked is not in F1!
            app, np_par = rule_act[(a, p)]
            Fp = F0 if p == 0 else F1
            Fnp = F0 if np_par == 0 else F1

            start = (qa, 0, 0)  # (q_on_au, q_on_u, min(|u|, 1))
            parent = {start: None}
            queue = deque([start])
            while queue:
                q1, q2, ucap = queue.popleft()
                if not (p == 1 and ucap == 0):
                    if q1 in Fp:
                        # compute delta_e*(q2, app)
                        q_after = q2
                        for ch in app:
                            q_after = delta_e[q_after][ch]
                        # Also check if (u + app, np_par) is halting!
                        # Halt iff (np_par == 0 and |u| + |app| == 0) or (np_par == 1 and |u| + |app| <= 1)
                        # Wait: if it is halting, then since halting words are rejected (checked above!),
                        # q_after will NOT be in Fnp anyway -- EXCEPT when np_par == 1 and |u|+|app| == 1,
                        # wait: we ALREADY enforced delta_e[0][c] not in F1 and 0 not in F0, F1, so ANY halting
                        # (s', np_par) has q_after NOT in Fnp automatically!!
                        if q_after not in Fnp:
                            u = []
                            cur = (q1, q2, ucap)
                            while parent[cur] is not None:
                                cur, ch = parent[cur]
                                u.append(ch)
                            u.reverse()
                            s_bad = (a,) + tuple(u)
                            s_nxt = tuple(u) + app
                            return ("STEP", (s_bad, p), (s_nxt, np_par))
                for c in range(n):
                    nxt = (delta_e[q1][c], delta_e[q2][c], 1)
                    if nxt not in parent:
                        parent[nxt] = ((q1, q2, ucap), c)
                        queue.append(nxt)
    return None


def solve_cegis(rules, t0=20, max_K=9):
    n = len(rules)
    tape = (0, 0)
    traj = [tape]
    for _ in range(300):
        tape = tape[2:] + rules[tape[0]]
        traj.append(tape)

    pos_samples = set()
    for w in traj[t0 : t0 + 25]:
        pos_samples.add((w[0::2], len(w) % 2))
    neg_samples = {((), 0), ((), 1)} | {((a,), 1) for a in range(n)}
    implications = []  # pairs ((s1, p1), (s2, p2)): s1,p1 in L => s2,p2 in L

    # Also pre-collect backwards-halting words on (s, p) up to depth 5!
    rule_act = {}
    for a in range(n):
        wa = rules[a]
        rule_act[(a, 0)] = (wa[0::2], len(wa) % 2)
        rule_act[(a, 1)] = (wa[1::2], (1 + len(wa)) % 2)

    for K in range(2, max_K + 1):
        print(f"Trying CEGIS with K = {K} even-projection states...", flush=True)
        # Variables:
        #   d[q, c, q'] in {0, 1}  (K * n * K)
        #   F0[q] in {0, 1}        (K)
        #   F1[q] in {0, 1}        (K)
        # And for each word w in words_pool (len L), state vars x[w_id, pos, q] in {0, 1}!
        words_pool = {}

        def get_wid(s):
            if s not in words_pool:
                words_pool[s] = len(words_pool)
            return words_pool[s]

        for s, _ in pos_samples | neg_samples:
            get_wid(s)
        for (s1, _), (s2, _) in implications:
            get_wid(s1)
            get_wid(s2)

        for cegis_iter in range(200):
            # Build MILP
            num_d = K * n * K
            num_F = 2 * K
            base_vars = num_d + num_F
            w_offsets = {}
            cur_v = base_vars
            for s, wid in sorted(words_pool.items(), key=lambda x: x[1]):
                w_offsets[s] = cur_v
                cur_v += (len(s) + 1) * K
            # Also auxiliary accept var acc_var[(s, p)]? No, acc(s, p) = sum_q z_{s, p, q} where z <= x[end, q] and z <= Fp[q]!
            sp_list = sorted(pos_samples | neg_samples | {x[0] for x in implications} | {x[1] for x in implications})
            sp_acc_off = {}
            for sp in sp_list:
                sp_acc_off[sp] = cur_v
                cur_v += K  # z_q = x[s, len(s), q] AND F_p[q]

            total_vars = cur_v
            rows_idx, cols_idx, vals, lbs, ubs = [], [], [], [], []
            row_cnt = 0

            def add_row(entries, lb, ub):
                nonlocal row_cnt
                for col, val in entries:
                    rows_idx.append(row_cnt)
                    cols_idx.append(col)
                    vals.append(val)
                lbs.append(lb)
                ubs.append(ub)
                row_cnt += 1

            def d_var(q, c, qp):
                return (q * n + c) * K + qp

            def f_var(p, q):
                return num_d + p * K + q

            # 1. Exact one target per (q, c)
            for q in range(K):
                for c in range(n):
                    add_row([(d_var(q, c, qp), 1.0) for qp in range(K)], 1.0, 1.0)

            # Symmetry breaking: state 0 on char 0 goes to 0 or 1
            if K >= 3:
                for qp in range(2, K):
                    add_row([(d_var(0, 0, qp), 1.0)], 0.0, 0.0)

            # 2. Word run constraints
            for s, off in w_offsets.items():
                # pos 0 is state 0!
                add_row([(off + 0, 1.0)], 1.0, 1.0)
                for q in range(1, K):
                    add_row([(off + q, 1.0)], 0.0, 0.0)
                for i, ch in enumerate(s):
                    cur_base = off + i * K
                    nxt_base = off + (i + 1) * K
                    # sum_q x[i+1, q] == 1
                    add_row([(nxt_base + q, 1.0) for q in range(K)], 1.0, 1.0)
                    # x[i, q] + d[q, ch, qp] - x[i+1, qp] <= 1
                    for q in range(K):
                        for qp in range(K):
                            add_row([(cur_base + q, 1.0), (d_var(q, ch, qp), 1.0), (nxt_base + qp, -1.0)], -np.inf, 1.0)

            # 3. Linearize z_q = x[end, q] * F_p[q] for sp = (s, p)
            for (s, p), zoff in sp_acc_off.items():
                end_base = w_offsets[s] + len(s) * K
                for q in range(K):
                    zv = zoff + q
                    xv = end_base + q
                    fv = f_var(p, q)
                    # z <= x, z <= f, z >= x + f - 1
                    add_row([(zv, 1.0), (xv, -1.0)], -np.inf, 0.0)
                    add_row([(zv, 1.0), (fv, -1.0)], -np.inf, 0.0)
                    add_row([(xv, 1.0), (fv, 1.0), (zv, -1.0)], -np.inf, 1.0)

            # 4. Positives: sum_q z_q == 1
            for sp in pos_samples:
                zoff = sp_acc_off[sp]
                add_row([(zoff + q, 1.0) for q in range(K)], 1.0, 1.0)

            # 5. Negatives: sum_q z_q == 0
            for sp in neg_samples:
                zoff = sp_acc_off[sp]
                add_row([(zoff + q, 1.0) for q in range(K)], 0.0, 0.0)

            # 6. Implications: sum_q z(sp1) - sum_q z(sp2) <= 0
            for sp1, sp2 in implications:
                z1 = sp_acc_off[sp1]
                z2 = sp_acc_off[sp2]
                add_row([(z1 + q, 1.0) for q in range(K)] + [(z2 + q, -1.0) for q in range(K)], -np.inf, 0.0)

            from scipy.sparse import csc_matrix
            A = csc_matrix((vals, (rows_idx, cols_idx)), shape=(row_cnt, total_vars))
            res = milp(
                c=np.zeros(total_vars),
                integrality=np.ones(total_vars),
                bounds=Bounds(np.zeros(total_vars), np.ones(total_vars)),
                constraints=LinearConstraint(A, lbs, ubs),
            )
            if not res.success:
                print(f"  UNSAT at K = {K} after {cegis_iter} CEGIS rounds!", flush=True)
                break

            sol = np.rint(res.x).astype(int)
            delta_e = [[0] * n for _ in range(K)]
            for q in range(K):
                for c in range(n):
                    for qp in range(K):
                        if sol[d_var(q, c, qp)] == 1:
                            delta_e[q][c] = qp
            F0 = {q for q in range(K) if sol[f_var(0, q)] == 1}
            F1 = {q for q in range(K) if sol[f_var(1, q)] == 1}

            ce = check_even_dfa(rules, delta_e, F0, F1)
            if ce is None:
                tr, ac = even_dfa_to_full_dfa(n, delta_e, F0, F1)
                cert = {"type": "DFA_INVARIANT", "entry_step": t0, "num_states": len(tr), "transitions": tr, "accepting": ac}
                ok, msg = verify_dfa_invariant(rules, cert)
                print(f"  FOUND CLOSED DFA AT K={K} (full states={len(tr)})! verify={ok} ({msg})", flush=True)
                if ok:
                    return cert
            _, sp1, sp2 = ce
            # Check if sp2 actually halts quickly -> promote sp1 directly to neg_samples!
            s_cur, p_cur = sp2
            halted_fast = False
            for _ in range(30):
                if (p_cur == 0 and len(s_cur) == 0) or (p_cur == 1 and len(s_cur) <= 1):
                    halted_fast = True
                    break
                if len(s_cur) > 40:
                    break
                app, p_cur = rule_act[(s_cur[0], p_cur)]
                s_cur = s_cur[1:] + app
            get_wid(sp1[0])
            if halted_fast:
                neg_samples.add(sp1)
                neg_samples.add(sp2)
                get_wid(sp2[0])
            else:
                get_wid(sp2[0])
                implications.append((sp1, sp2))
    return None


if __name__ == "__main__":
    cert = solve_cegis(((1, 0, 1), (2, 0), (1,)), t0=50, max_K=8)
    print("Final result:", cert)
