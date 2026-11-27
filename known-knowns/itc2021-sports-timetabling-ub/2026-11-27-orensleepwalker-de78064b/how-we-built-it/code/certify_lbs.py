"""
ITC2021 Deterministic CP-SAT Lower-Bound Certifier (`itc2021-lower-bound-certificate`)
(scans/2026-11-26-itc2021-charlie/certify_lbs.py)

Follows V3R1T4S `itc2021-lower-bound-certificate` rules & Bobby's 3-skeptic-approved Early 14 / Early 9 protocol:
  1. Builds two exact relaxation / full models from the unmodified original XML:
     - `venue_relax`: Exact necessary Home/Away (`H[s,t]`) + de Werra 0-break parity + pairwise 2RR/Phased
       compatibility + HARD CA1/BR1/BR2/FA2/GA1, minimizing non-negative soft venue penalties (`CA1+BR1+BR2+FA2`).
       Since all opponent soft penalties are >= 0, any valid lower bound on `soft_venue` is a valid lower bound
       on total penalty `venue + opp`!
     - `full_exact`: Complete 0-hard ITC2021 CP-SAT formulation (`x[s,i,j]` + `H[s,t]`) minimizing `venue + opp`.
  2. Mandatory Incumbent Admissibility Check: Before solving for a bound, verifies on a copy of the model
     with `H == home0` (and `x == record` for `full_exact`) that the posted Best UB timetable is FEASIBLE with
     exact score `sp0['venue']` (or `ub`), ruling out any over-constraining bug!
  3. Deterministic Certificate Export & Fresh Replay:
     Exports un-hinted `.pbtxt`, solves with `num_workers = 1` (100% deterministic CP-SAT) and fixed `seed`,
     saves solver log, and re-loads `.pbtxt` into a brand-new `CpModel` to confirm the exact dual bound replays!
"""
import argparse
import hashlib
import itertools
import json
import math
import os
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANS_DIR = os.path.dirname(CHARLIE_DIR)
SCOUT_DIR = os.path.join(SCANS_DIR, "2026-11-25-itc2021-scout")
CERTS_DIR = os.path.join(CHARLIE_DIR, "certs")

sys.path.insert(0, CHARLIE_DIR)
sys.path.insert(0, SCOUT_DIR)

from ortools.sat.python import cp_model  # noqa: E402
import split as split_eval  # noqa: E402
import solve_itc as base  # noqa: E402


def build_venue_relax_model(root, n, R, phased):
    """Exact necessary venue relaxation over H[s, t] in {0, 1}."""
    m = cp_model.CpModel()
    H = {(s, t): m.NewBoolVar(f"H_{s}_{t}") for s in range(R) for t in range(n)}
    br_h, br_a, br_ha = {}, {}, {}
    has_break = {t: m.NewBoolVar(f"hb_{t}") for t in range(n)}

    for s in range(R):
        m.Add(sum(H[s, t] for t in range(n)) == n // 2)
    for t in range(n):
        m.Add(sum(H[s, t] for s in range(R)) == n - 1)
        for s in range(1, R):
            bh = m.NewBoolVar(f"bh_{t}_{s}")
            ba = m.NewBoolVar(f"ba_{t}_{s}")
            bha = m.NewBoolVar(f"bha_{t}_{s}")
            m.Add(bh >= H[s, t] + H[s - 1, t] - 1)
            m.Add(bh <= H[s, t])
            m.Add(bh <= H[s - 1, t])
            m.Add(ba >= (1 - H[s, t]) + (1 - H[s - 1, t]) - 1)
            m.Add(ba <= 1 - H[s, t])
            m.Add(ba <= 1 - H[s - 1, t])
            m.Add(bha == bh + ba)
            br_h[t, s] = bh
            br_a[t, s] = ba
            br_ha[t, s] = bha
        m.AddMaxEquality(has_break[t], [br_ha[t, s] for s in range(1, R)])

    # De Werra parity: at most 1 alternating team starting Away (0), at most 1 starting Home (1)
    m.Add(sum(has_break.values()) >= n - 2)
    for first in (0, 1):
        alt = []
        for t in range(n):
            a_v = m.NewBoolVar(f"alt_{t}_{first}")
            st_lit = H[0, t] if first == 1 else H[0, t].Not()
            m.AddBoolAnd([st_lit, has_break[t].Not()]).OnlyEnforceIf(a_v)
            m.AddBoolOr([st_lit.Not(), has_break[t]]).OnlyEnforceIf(a_v.Not())
            alt.append(a_v)
        m.AddAtMostOne(alt)

    # Exact slot break-pair parity: since sum_t H[s,t] == sum_t H[s-1,t] == n//2,
    # sum_t br_h[t,s] == sum_t br_a[t,s] in every slot s >= 1!
    ks_list = []
    for s in range(1, R):
        ks = m.NewIntVar(0, n // 2, f"kpair_{s}")
        m.Add(sum(br_h[t, s] for t in range(n)) == ks)
        m.Add(sum(br_a[t, s] for t in range(n)) == ks)
        m.Add(sum(br_ha[t, s] for t in range(n)) == 2 * ks)
        ks_list.append(ks)
    tot_kpairs = m.NewIntVar(0, n * R, "tot_kpairs")
    m.Add(tot_kpairs == sum(ks_list))
    m.Add(sum(br_ha.values()) == 2 * tot_kpairs)

    # Exact per-team minimum breaks deduced from team t's own HARD CA1/BR1/single-slot GA1 rules
    for t in range(n):
        mt = cp_model.CpModel()
        ht = [mt.NewBoolVar("") for _ in range(R)]
        mt.Add(sum(ht) == n - 1)
        brh_t, bra_t, brha_t = {}, {}, {}
        for s in range(1, R):
            bh = mt.NewBoolVar(""); ba = mt.NewBoolVar(""); bha = mt.NewBoolVar("")
            mt.Add(bh >= ht[s] + ht[s - 1] - 1); mt.Add(bh <= ht[s]); mt.Add(bh <= ht[s - 1])
            mt.Add(ba >= (1 - ht[s]) + (1 - ht[s - 1]) - 1); mt.Add(ba <= 1 - ht[s]); mt.Add(ba <= 1 - ht[s - 1])
            mt.Add(bha == bh + ba)
            brh_t[s] = bh; bra_t[s] = ba; brha_t[s] = bha
        for e in root.find("Constraints").iter():
            a = e.attrib
            if a.get("type") != "HARD":
                continue
            if e.tag == "CA1" and t in base.parse_ids(a["teams"]):
                sl = base.parse_ids(a["slots"]); is_h = (a["mode"] == "H")
                c = sum((ht[s] if is_h else 1 - ht[s]) for s in sl)
                mt.Add(c >= int(a.get("min", 0)))
                if "max" in a: mt.Add(c <= int(a["max"]))
            elif e.tag == "BR1" and t in base.parse_ids(a["teams"]):
                sl = [s for s in base.parse_ids(a["slots"]) if s > 0]; mx = int(a["intp"])
                bd = brh_t if a["mode2"] == "H" else (bra_t if a["mode2"] == "A" else brha_t)
                mt.Add(sum(bd[s] for s in sl) <= mx)
            elif e.tag == "GA1":
                p = base.parse_ids(a["meetings"]); sl = base.parse_ids(a["slots"])
                if len(sl) == 1 and int(a.get("min", 0)) == len(p) // 2:
                    for h_tm, a_tm in zip(p[::2], p[1::2]):
                        if h_tm == t: mt.Add(ht[sl[0]] == 1)
                        elif a_tm == t: mt.Add(ht[sl[0]] == 0)
        mt.Minimize(sum(brha_t.values()))
        sv_t = cp_model.CpSolver()
        st_t = sv_t.Solve(mt)
        assert st_t == cp_model.OPTIMAL
        mb_t = round(sv_t.ObjectiveValue())
        if mb_t >= 1:
            m.Add(has_break[t] == 1)
            m.Add(sum(br_ha[t, s] for s in range(1, R)) >= mb_t)
        else:
            m.Add(sum(br_ha[t, s] for s in range(1, R)) >= has_break[t])

    # Recursive prefix Home sums for FA2
    pref = {(0, t): H[0, t] for t in range(n)}
    for t in range(n):
        for s in range(1, R):
            pv = m.NewIntVar(0, s + 1, f"pref_{s}_{t}")
            m.Add(pv == pref[s - 1, t] + H[s, t])
            pref[s, t] = pv

    p10 = {}

    def get_p10(h_tm, a_tm, s):
        if (s, h_tm, a_tm) not in p10:
            b = m.NewBoolVar(f"p10_{s}_{h_tm}_{a_tm}")
            m.Add(b >= H[s, h_tm] - H[s, a_tm])
            m.Add(b <= H[s, h_tm])
            m.Add(b <= 1 - H[s, a_tm])
            p10[s, h_tm, a_tm] = b
        return p10[s, h_tm, a_tm]

    soft_terms = []

    def add_v_rule(expr_list, lo, hi, hard, w):
        if not expr_list:
            return
        expr = sum(expr_list)
        ub_m = len(expr_list)
        if hard:
            if hi is not None:
                m.Add(expr <= hi)
            if lo:
                m.Add(expr >= lo)
            return
        if hi is not None and ub_m > hi:
            o = m.NewIntVar(0, ub_m, "")
            m.Add(o >= expr - hi)
            soft_terms.append(w * o)
        if lo > 0:
            u = m.NewIntVar(0, lo, "")
            m.Add(u >= lo - expr)
            soft_terms.append(w * u)

    for e in root.find("Constraints").iter():
        a = e.attrib
        if "type" not in a:
            continue
        k = e.tag
        hard = a["type"] == "HARD"
        w = int(a["penalty"])
        lo = int(a.get("min", 0))
        hi = int(a["max"]) if "max" in a else None

        if k == "CA1":
            sl = base.parse_ids(a["slots"])
            is_h = (a["mode"] == "H")
            for t in base.parse_ids(a["teams"]):
                add_v_rule([(H[s, t] if is_h else 1 - H[s, t]) for s in sl], lo, hi, hard, w)
        elif k == "BR1":
            mx = int(a["intp"])
            sl = [s for s in base.parse_ids(a["slots"]) if s > 0]
            bd = br_h if a["mode2"] == "H" else (br_a if a["mode2"] == "A" else br_ha)
            for t in base.parse_ids(a["teams"]):
                add_v_rule([bd[t, s] for s in sl], 0, mx, hard, w)
        elif k == "BR2":
            mx = int(a["intp"])
            sl = [s for s in base.parse_ids(a["slots"]) if s > 0]
            T_ids = base.parse_ids(a["teams"])
            if len(sl) == R - 1 and len(T_ids) == n:
                if hard:
                    m.Add(2 * tot_kpairs <= mx)
                else:
                    o = m.NewIntVar(0, n * R, "br2_ov")
                    m.Add(o >= 2 * tot_kpairs - mx)
                    soft_terms.append(w * o)
            else:
                add_v_rule([br_ha[t, s] for t in T_ids for s in sl], 0, mx, hard, w)
        elif k == "FA2" and hard:
            T_ids = base.parse_ids(a["teams"])
            sl = sorted(base.parse_ids(a["slots"]))
            ip = int(a["intp"])
            for s in sl:
                lo_s = m.NewIntVar(0, s + 1, "")
                for t in T_ids:
                    m.Add(pref[s, t] >= lo_s)
                    m.Add(pref[s, t] <= lo_s + ip)
        elif k == "GA1" and hard and lo > 0:
            p = base.parse_ids(a["meetings"])
            sl = base.parse_ids(a["slots"])
            compat = [get_p10(i_m, j_m, s) for i_m, j_m in zip(p[::2], p[1::2]) for s in sl]
            if compat:
                m.Add(sum(compat) >= lo)

    obj = sum(soft_terms) if soft_terms else 0
    m.Minimize(obj)
    return m, H, obj


def build_full_exact_model(root, n, R, phased):
    """Complete exact 0-hard ITC2021 CP-SAT formulation."""
    m = cp_model.CpModel()
    x = {(s, i, j): m.NewBoolVar(f"x_{s}_{i}_{j}") for s in range(R) for i in range(n) for j in range(n) if i != j}
    H = {(s, t): m.NewBoolVar(f"H_{s}_{t}") for s in range(R) for t in range(n)}

    for s in range(R):
        for t in range(n):
            h_lits = [x[s, t, j] for j in range(n) if j != t]
            a_lits = [x[s, j, t] for j in range(n) if j != t]
            m.AddExactlyOne(h_lits + a_lits)
            m.Add(H[s, t] == sum(h_lits))

    for i in range(n):
        for j in range(n):
            if i != j:
                m.AddExactlyOne([x[s, i, j] for s in range(R)])

    if phased:
        half = R // 2
        for i, j in itertools.combinations(range(n), 2):
            m.Add(sum(x[s, i, j] + x[s, j, i] for s in range(half)) == 1)

    br_h, br_a, br_ha = {}, {}, {}
    for t in range(n):
        for s in range(1, R):
            bh = m.NewBoolVar(""); ba = m.NewBoolVar(""); bha = m.NewBoolVar("")
            m.Add(bh >= H[s, t] + H[s - 1, t] - 1); m.Add(bh <= H[s, t]); m.Add(bh <= H[s - 1, t])
            m.Add(ba >= (1 - H[s, t]) + (1 - H[s - 1, t]) - 1); m.Add(ba <= 1 - H[s, t]); m.Add(ba <= 1 - H[s - 1, t])
            m.Add(bha == bh + ba)
            br_h[t, s] = bh; br_a[t, s] = ba; br_ha[t, s] = bha

    soft_terms = []

    def add_rule(v_list, lo, hi, hard, w):
        if not v_list:
            return
        expr = sum(v_list)
        ub_m = len(v_list)
        if hard:
            if hi is not None: m.Add(expr <= hi)
            if lo: m.Add(expr >= lo)
            return
        if hi is not None and ub_m > hi:
            o = m.NewIntVar(0, ub_m, ""); m.Add(o >= expr - hi); soft_terms.append(w * o)
        if lo > 0:
            u = m.NewIntVar(0, lo, ""); m.Add(u >= lo - expr); soft_terms.append(w * u)

    def g_vars(t, group, slots, mode):
        res = []
        for s in slots:
            if mode in ("H", "HA"):
                res.extend(x[s, t, j] for j in group if j != t)
            if mode in ("A", "HA"):
                res.extend(x[s, j, t] for j in group if j != t)
        return res

    for e in root.find("Constraints").iter():
        a = e.attrib
        if "type" not in a:
            continue
        k = e.tag
        hard = a["type"] == "HARD"; w = int(a["penalty"])
        lo = int(a.get("min", 0)); hi = int(a["max"]) if "max" in a else None

        if k == "CA1":
            sl = base.parse_ids(a["slots"]); is_h = (a["mode"] == "H")
            for t in base.parse_ids(a["teams"]):
                add_rule([(H[s, t] if is_h else 1 - H[s, t]) for s in sl], lo, hi, hard, w)
        elif k == "BR1":
            mx = int(a["intp"]); sl = [s for s in base.parse_ids(a["slots"]) if s > 0]
            bd = br_h if a["mode2"] == "H" else (br_a if a["mode2"] == "A" else br_ha)
            for t in base.parse_ids(a["teams"]):
                add_rule([bd[t, s] for s in sl], 0, mx, hard, w)
        elif k == "BR2":
            mx = int(a["intp"]); sl = [s for s in base.parse_ids(a["slots"]) if s > 0]
            T_ids = base.parse_ids(a["teams"])
            add_rule([br_ha[t, s] for t in T_ids for s in sl], 0, mx, hard, w)
        elif k == "FA2":
            T_ids = base.parse_ids(a["teams"]); sl = sorted(base.parse_ids(a["slots"])); ip = int(a["intp"])
            for t1, t2 in itertools.combinations(T_ids, 2):
                d = m.NewIntVar(0, R, "")
                for s in sl:
                    diff = sum(H[q, t1] for q in range(s + 1)) - sum(H[q, t2] for q in range(s + 1))
                    m.Add(d >= diff - ip); m.Add(d >= -diff - ip)
                if hard: m.Add(d == 0)
                else: soft_terms.append(w * d)
        elif k == "CA2":
            T2 = set(base.parse_ids(a["teams2"])); sl = base.parse_ids(a["slots"])
            for t in base.parse_ids(a["teams1"]):
                add_rule(g_vars(t, T2, sl, a["mode1"]), lo, hi, hard, w)
        elif k == "CA3":
            Lw = int(a["intp"]); T2 = set(base.parse_ids(a["teams2"]))
            for t in base.parse_ids(a["teams1"]):
                for s0 in range(R - Lw + 1):
                    add_rule(g_vars(t, T2, range(s0, s0 + Lw), a["mode1"]), lo, hi, hard, w)
        elif k == "CA4":
            T1 = base.parse_ids(a["teams1"]); T2 = set(base.parse_ids(a["teams2"])); sl = base.parse_ids(a["slots"])
            for sg in ([sl] if a["mode2"] == "GLOBAL" else [[s] for s in sl]):
                vl = []
                for t in T1: vl.extend(g_vars(t, T2, sg, a["mode1"]))
                add_rule(vl, lo, hi, hard, w)
        elif k == "GA1":
            p = base.parse_ids(a["meetings"]); sl = base.parse_ids(a["slots"])
            vl = [x[s, i_m, j_m] for i_m, j_m in zip(p[::2], p[1::2]) for s in sl]
            add_rule(vl, lo, hi, hard, w)
        elif k == "SE1":
            mn = int(a["min"])
            for i_t, j_t in itertools.combinations(base.parse_ids(a["teams"]), 2):
                S1 = sum(s * x[s, i_t, j_t] for s in range(R))
                S2 = sum(s * x[s, j_t, i_t] for s in range(R))
                d = m.NewIntVar(-R, R, ""); m.Add(d == S1 - S2)
                ad = m.NewIntVar(0, R, ""); m.AddAbsEquality(ad, d)
                if hard: m.Add(ad - 1 >= mn)
                else:
                    dev = m.NewIntVar(0, mn, ""); m.Add(dev >= mn - (ad - 1)); soft_terms.append(w * dev)

    obj = sum(soft_terms) if soft_terms else 0
    m.Minimize(obj)
    return m, x, H, obj


def certify_instance(tag, board_lb, board_ub, venue_secs=25.0, full_secs=45.0, seed=20261126):
    os.makedirs(CERTS_DIR, exist_ok=True)
    stem = "ITC2021_" + tag.replace(" ", "_")
    inst_path = os.path.join(base.INST_DIR, f"{stem}.xml")
    sol_path = os.path.join(base.SOL_DIR, f"{stem}.record.xml")

    root, _, n, R, phased, opp0, home0 = base.load_instance_and_start(inst_path, sol_path)
    sp0 = split_eval.evaluate(inst_path, sol_path)
    assert sp0["hard"] == 0 and (sp0["venue"] + sp0["opp"]) == board_ub

    best_cert = None

    # 1. Try Venue Relaxation first (if sp0["venue"] > board_lb)
    if sp0["venue"] > board_lb:
        m_chk, H_chk, _ = build_venue_relax_model(root, n, R, phased)
        for s in range(R):
            for t in range(n):
                m_chk.Add(H_chk[s, t] == int(home0[s, t]))
        sv_chk = cp_model.CpSolver()
        st_chk = sv_chk.Solve(m_chk)
        assert st_chk == cp_model.OPTIMAL and round(sv_chk.ObjectiveValue()) <= sp0["venue"], \
            f"Incumbent check failed on {tag}: {sv_chk.StatusName(st_chk)} {sv_chk.ObjectiveValue()} vs {sp0['venue']}"

        m_v, _, _ = build_venue_relax_model(root, n, R, phased)
        t0 = time.time()
        sv = cp_model.CpSolver()
        sv.parameters.num_workers = 1
        sv.parameters.linearization_level = 2
        sv.parameters.random_seed = seed
        sv.parameters.max_deterministic_time = float(venue_secs)
        sv.parameters.max_time_in_seconds = float(venue_secs * 4.0)
        st = sv.Solve(m_v)
        raw_v = sv.BestObjectiveBound() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.UNKNOWN) else 0.0
        bnd = int(math.ceil(raw_v - 1e-9)) if raw_v > 0 else 0
        assert bnd <= sp0["venue"], f"Invalid venue bound {bnd} > {sp0['venue']} on {tag}"
        print(f"  [{tag:10s}] venue_relax (1w, {time.time()-t0:.1f}s): status={sv.StatusName(st)} dual_bound={bnd} vs board_lb={board_lb} (rec_v={sp0['venue']})", flush=True)
        if bnd > board_lb:
            pb_path = os.path.join(CERTS_DIR, f"{stem}_venue_relax.pbtxt")
            log_path = os.path.join(CERTS_DIR, f"{stem}_venue_relax.log")
            assert m_v.export_to_file(pb_path)
            # Fresh-session replay check with identical deterministic time limit!
            m_rep = cp_model.CpModel()
            assert m_rep.proto.parse_text_format(open(pb_path, "r").read())
            sv_rep = cp_model.CpSolver()
            sv_rep.parameters.num_workers = 1
            sv_rep.parameters.linearization_level = 2
            sv_rep.parameters.random_seed = seed
            sv_rep.parameters.max_deterministic_time = float(venue_secs)
            sv_rep.parameters.max_time_in_seconds = float(venue_secs * 4.0)
            sv_rep.parameters.log_search_progress = True
            sv_rep.parameters.log_to_stdout = False
            rep_lines = []
            sv_rep.log_callback = rep_lines.append
            st_rep = sv_rep.Solve(m_rep)
            open(log_path, "w").write("\n".join(rep_lines) + "\n")
            raw_rep = sv_rep.BestObjectiveBound() if st_rep in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.UNKNOWN) else 0.0
            bnd_rep = int(math.ceil(raw_rep - 1e-9)) if raw_rep > 0 else 0
            if bnd_rep > board_lb:
                best_cert = dict(
                    inst=tag, mode="venue_relax", board_lb=board_lb, proved_lb=min(bnd, bnd_rep), board_ub=board_ub,
                    status=sv_rep.StatusName(st_rep), seed=seed, workers=1, det_time=float(venue_secs), secs=round(time.time() - t0, 2),
                    model_pbtxt=pb_path, log_path=log_path,
                    model_sha256=hashlib.sha256(open(pb_path, "rb").read()).hexdigest(),
                    replay_verified=True, replay_bound=bnd_rep,
                )

    # 2. Try Full Exact 1-worker CP-SAT dual bound if full_secs > 0
    if full_secs > 0:
        cur_target_lb = best_cert["proved_lb"] if best_cert else board_lb
        m_fchk, x_fchk, _, _ = build_full_exact_model(root, n, R, phased)
        for s in range(R):
            for i in range(n):
                if home0[s, i] == 1:
                    m_fchk.Add(x_fchk[s, i, int(opp0[s, i])] == 1)
        sv_fchk = cp_model.CpSolver()
        st_fchk = sv_fchk.Solve(m_fchk)
        assert st_fchk == cp_model.OPTIMAL and round(sv_fchk.ObjectiveValue()) == board_ub

        m_f, _, _, _ = build_full_exact_model(root, n, R, phased)
        t0 = time.time()
        sv = cp_model.CpSolver()
        sv.parameters.num_workers = 1
        sv.parameters.linearization_level = 2
        sv.parameters.random_seed = seed
        sv.parameters.max_deterministic_time = float(full_secs)
        sv.parameters.max_time_in_seconds = float(full_secs * 4.0)
        st = sv.Solve(m_f)
        raw_b = sv.BestObjectiveBound() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.UNKNOWN) else 0.0
        bnd_f = int(math.ceil(raw_b - 1e-9)) if raw_b > 0 else 0
        assert bnd_f <= board_ub
        print(f"  [{tag:10s}] full_exact  (1w, {time.time()-t0:.1f}s): status={sv.StatusName(st)} dual_bound={bnd_f} vs cur_lb={cur_target_lb}", flush=True)
        if bnd_f > cur_target_lb:
            pb_path = os.path.join(CERTS_DIR, f"{stem}_full_exact.pbtxt")
            log_path = os.path.join(CERTS_DIR, f"{stem}_full_exact.log")
            assert m_f.export_to_file(pb_path)
            m_rep = cp_model.CpModel()
            assert m_rep.proto.parse_text_format(open(pb_path, "r").read())
            sv_rep = cp_model.CpSolver()
            sv_rep.parameters.num_workers = 1
            sv_rep.parameters.linearization_level = 2
            sv_rep.parameters.random_seed = seed
            sv_rep.parameters.max_deterministic_time = float(full_secs)
            sv_rep.parameters.max_time_in_seconds = float(full_secs * 4.0)
            sv_rep.parameters.log_search_progress = True
            sv_rep.parameters.log_to_stdout = False
            rep_lines = []
            sv_rep.log_callback = rep_lines.append
            st_rep = sv_rep.Solve(m_rep)
            open(log_path, "w").write("\n".join(rep_lines) + "\n")
            raw_rep = sv_rep.BestObjectiveBound() if st_rep in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.UNKNOWN) else 0.0
            bnd_rep = int(math.ceil(raw_rep - 1e-9)) if raw_rep > 0 else 0
            if bnd_rep > cur_target_lb:
                best_cert = dict(
                    inst=tag, mode="full_exact", board_lb=board_lb, proved_lb=min(bnd_f, bnd_rep), board_ub=board_ub,
                    status=sv_rep.StatusName(st_rep), seed=seed, workers=1, secs=round(time.time() - t0, 2),
                    model_pbtxt=pb_path, log_path=log_path,
                    model_sha256=hashlib.sha256(open(pb_path, "rb").read()).hexdigest(),
                    replay_verified=True, replay_bound=bnd_rep,
                )
    return best_cert


def main():
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", type=str, required=True, help="Comma-separated Inst Name")
    parser.add_argument("--venue-secs", type=float, default=25.0)
    parser.add_argument("--full-secs", type=float, default=35.0)
    parser.add_argument("--parallel", type=int, default=3)
    args = parser.parse_args()

    board = {b["n"]: b for b in json.load(open(os.path.join(SCOUT_DIR, "data/board.json")))}
    out_jsonl = os.path.join(CERTS_DIR, "lb_certificates.jsonl")
    os.makedirs(CERTS_DIR, exist_ok=True)
    lock = threading.Lock()

    tags = [raw.strip() for raw in args.targets.split(",") if raw.strip()]
    wins = 0
    t0 = time.time()
    print(f"=== LB CERTIFICATION SWEEP START ({len(tags)} targets, parallel={args.parallel}, 1w deterministic) ===", flush=True)
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = {
            ex.submit(certify_instance, tag, board[tag]["lb"], board[tag]["ub"], args.venue_secs, args.full_secs): tag
            for tag in tags
        }
        for fut in as_completed(futs):
            tag = futs[fut]
            cert = fut.result()
            if cert:
                with lock:
                    wins += 1
                    with open(out_jsonl, "a") as jf:
                        jf.write(json.dumps(cert) + "\n")
                print(f"  *** CERTIFIED LB IMPROVEMENT: {tag} LB {board[tag]['lb']} -> {cert['proved_lb']} (+{cert['proved_lb']-board[tag]['lb']}, {cert['mode']}, replay={cert['replay_bound']})!! ***", flush=True)
    print(f"=== LB CERTIFICATION COMPLETE in {(time.time()-t0)/60.0:.1f}m: {wins}/{len(tags)} strict LB improvements certified ===", flush=True)


if __name__ == "__main__":
    main()
