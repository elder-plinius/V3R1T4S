#!/usr/bin/env python3
"""Standalone certified optimality verifier for QOBLIB instance po_a010_t10_orig_b004_l1e-03.
Evaluates exact rational arithmetic via Python Fraction, recomputing all 10 x 10,606 stage costs
and verifying all 5 Hasse-diagram Bellman optimality inequalities.
"""

import gzip
import hashlib
import json
import math
import os
import sys
import tempfile
import time
import urllib.request
from fractions import Fraction as F

CASH = F(1000000)
UNIT = F(100000)
DELTA = F("0.001")
NU = F("0.0001")
RHO = F("0.000025")
LAMBDA = F("0.001")
BUDGET = 4
MAX_UNITS = 3

PINNED_SHA256 = {
    "stock_prices.txt.gz": "80a583a0ccd63b9432b94ae3b8012df9661ab8bb5e6faf26df121f43adc588f3",
    "covariance_matrices.txt.gz": "41dab1816d7a8f9f50dc07fe60816d435f9dc085eaaee034d8ecc3721ee5c202",
}

BASE_URL = "https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/instances/po_a010_t10_orig"

def zround(q):
    """Round half away from zero in exact rational arithmetic."""
    a = abs(q)
    n = math.floor(a + F(1, 2))
    return int(n if q >= 0 else -n)

def parse_decimal(s):
    """Exact decimal parser returning Fraction."""
    s = s.strip()
    if not s:
        return None
    if 'e' in s or 'E' in s:
        parts = s.lower().split('e')
        mant, exp10 = parts[0], int(parts[1])
    else:
        mant, exp10 = s, 0
    neg = mant.startswith('-')
    if neg or mant.startswith('+'):
        mant = mant[1:]
    if '.' in mant:
        ipart, fpart = mant.split('.', 1)
    else:
        ipart, fpart = mant, ''
    digits = ipart + fpart
    if not digits:
        return None
    num = int(digits)
    scale = len(fpart) - exp10
    if scale >= 0:
        den = 10 ** scale
        num_f = F(num, den)
    else:
        num_f = F(num * (10 ** (-scale)), 1)
    return -num_f if neg else num_f

def ensure_data_files(pkg_root):
    """Retrieve instance data files, using isolated cache or download or local fallback."""
    cache_dir = os.path.join(tempfile.gettempdir(), "qoblib_po_a010_t10_orig")
    os.makedirs(cache_dir, exist_ok=True)
    fallback_dirs = [
        os.path.join(pkg_root, "..", "..", "runs", "2026-10-27-1610", "data"),
    ]
    
    files = {}
    for fname, expected_hash in PINNED_SHA256.items():
        target_path = os.path.join(cache_dir, fname)
        if os.path.exists(target_path):
            with open(target_path, "rb") as f:
                if hashlib.sha256(f.read()).hexdigest() == expected_hash:
                    files[fname] = target_path
                    continue
        # Download
        url = f"{BASE_URL}/{fname}"
        downloaded = False
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "portfolio-verifier/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if hashlib.sha256(data).hexdigest() == expected_hash:
                    with open(target_path, "wb") as f:
                        f.write(data)
                    files[fname] = target_path
                    downloaded = True
        except Exception:
            downloaded = False
        
        if not downloaded:
            for fb in fallback_dirs:
                p = os.path.join(fb, fname)
                if os.path.exists(p):
                    with open(p, "rb") as f:
                        data = f.read()
                    if hashlib.sha256(data).hexdigest() == expected_hash:
                        with open(target_path, "wb") as f:
                            f.write(data)
                        files[fname] = target_path
                        downloaded = True
                        break
        if not downloaded:
            raise FileNotFoundError(f"Cannot obtain valid instance file {fname} (expected SHA {expected_hash})")
    return files

def run_verification(pkg_dir):
    t_start = time.time()
    obj_dir = os.path.join(pkg_dir, "object")
    
    sol_file = os.path.join(obj_dir, "po_a010_t10_orig_b004_l1e-03.sol")
    cert_file = os.path.join(obj_dir, "po_a010_t10_orig_b004_l1e-03_bellman_certificate.json")
    d_file = os.path.join(obj_dir, "po_a010_t10_orig_b004_l1e-03_downward_meet_tables.json")
    u_file = os.path.join(obj_dir, "po_a010_t10_orig_b004_l1e-03_upward_join_tables.json")
    
    for f in (sol_file, cert_file, d_file, u_file):
        if not os.path.isfile(f):
            print(f"Error: Missing object file {f}")
            return False
            
    # 1. Obtain instance data
    data_files = ensure_data_files(pkg_dir)
    
    # Read stock prices
    with gzip.open(data_files["stock_prices.txt.gz"], "rt", encoding="utf-8") as f:
        symbols, index = [], {}
        entries = []
        max_day = 0
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            d, s, v = line.split()
            day = int(d)
            val = parse_decimal(v)
            if s not in index:
                index[s] = len(symbols)
                symbols.append(s)
            entries.append((index[s], day, val))
            if day > max_day:
                max_day = day
    periods = max_day + 1
    if len(symbols) != 10 or periods != 10:
        print(f"Error: Unexpected instance dimensions ({len(symbols)} assets, {periods} periods)")
        return False
    
    raw_prices = [[None] * periods for _ in symbols]
    for sid, day, val in entries:
        raw_prices[sid][day] = val
    unit_prices = [[raw_prices[i][t] * UNIT / raw_prices[i][0] for t in range(periods)] for i in range(10)]
    
    # Read covariance
    with gzip.open(data_files["covariance_matrices.txt.gz"], "rt", encoding="utf-8") as f:
        cov = {}
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            d, s1, s2, v = line.split()
            cov[(index[s1], index[s2], int(d))] = parse_decimal(v)
    if len(cov) != 1000:
        print(f"Error: Incomplete covariance matrix entries ({len(cov)})")
        return False
    
    # 2. Build discrete count state space S
    states = []
    cur = [0] * 20
    def backtrack(pos, rem):
        if pos == 20:
            states.append(tuple(cur))
            return
        m = min(rem, MAX_UNITS)
        for v in range(m + 1):
            cur[pos] = v
            backtrack(pos + 1, rem - v)
    backtrack(0, BUDGET)
    n_states = len(states)
    if n_states != 10606:
        print(f"Error: Unexpected state count {n_states}")
        return False
    state_to_idx = {st: i for i, st in enumerate(states)}
    
    # Build Hasse diagram cover relations
    up_edges = [[] for _ in range(n_states)]
    total_edges = 0
    for i, st in enumerate(states):
        if sum(st) < BUDGET:
            for g in range(20):
                if st[g] < MAX_UNITS:
                    nxt = list(st)
                    nxt[g] += 1
                    nxt_idx = state_to_idx.get(tuple(nxt))
                    if nxt_idx is not None:
                        up_edges[i].append((g, nxt_idx))
                        total_edges += 1
    if total_edges != 35400:
        print(f"Error: Unexpected Hasse edge count {total_edges}")
        return False
    
    # 3. Precompute model coefficients
    w_trans = [[zround(DELTA * unit_prices[i][t]) for i in range(10)] for t in range(periods)]
    w_short = [[zround(RHO * unit_prices[i][t]) for i in range(10)] for t in range(periods)]
    w_ret = [[zround(unit_prices[i][t + 1] - unit_prices[i][t]) for i in range(10)] for t in range(periods - 1)]
    coef_cash = [zround(NU * UNIT * (1 << k)) for k in range(4)]
    
    q_risk = [[[0] * 20 for _ in range(20)] for _ in range(periods)]
    for t in range(periods):
        for i in range(10):
            for tau_i_idx in range(2):
                tau_i = 1 if tau_i_idx == 0 else -1
                gi = 2 * i + tau_i_idx
                for j in range(10):
                    for tau_j_idx in range(2):
                        tau_j = 1 if tau_j_idx == 0 else -1
                        gj = 2 * j + tau_j_idx
                        c = cov.get((i, j, t))
                        if c is None:
                            print(f"Error: missing cov ({i}, {j}, {t})")
                            return False
                        sign = F(tau_i * tau_j)
                        base = LAMBDA * sign * c * unit_prices[i][t] * unit_prices[j][t]
                        q_risk[t][gi][gj] = zround(base)
                        
    # Precompute non-zero positions for fast evaluation
    state_pos_coords = []
    for st in states:
        pos_list = [(g, st[g]) for g in range(20) if st[g] > 0]
        net = sum(st[2*i] - st[2*i+1] for i in range(10))
        tot = sum(st)
        state_pos_coords.append((pos_list, net, tot))
        
    # Recompute all stage costs
    stage_cost = [[0] * n_states for _ in range(periods)]
    for t in range(periods):
        wt_trans = w_trans[t]
        wt_short = w_short[t]
        wt_ret = w_ret[t] if t < periods - 1 else None
        q_t = q_risk[t]
        for s_idx in range(n_states):
            pos_list, net, tot = state_pos_coords[s_idx]
            cost = 0
            # Risk
            for gi, ui in pos_list:
                row = q_t[gi]
                for gj, uj in pos_list:
                    cost += row[gj] * ui * uj
            # Cash slack
            slack1 = 10 - net
            if slack1 >= 0:
                for k in range(4):
                    if (slack1 >> k) & 1:
                        cost -= coef_cash[k]
            # Short fee
            for g, u in pos_list:
                if g % 2 == 1:
                    cost += wt_short[g // 2] * u
            # Expected return (t < 9)
            if wt_ret is not None:
                for g, u in pos_list:
                    if g % 2 == 0:
                        cost -= wt_ret[g // 2] * u
                    else:
                        cost += wt_ret[g // 2] * u
            # Initial buy-in at t=0
            if t == 0:
                for g, u in pos_list:
                    cost += wt_trans[g // 2] * u
            # Liquidation at t=9
            if t == periods - 1:
                for g, u in pos_list:
                    cost += wt_trans[g // 2] * u
            stage_cost[t][s_idx] = cost
            
    # 4. Parse & Verify Feasibility of Canonical Schedule
    sched_counts = {}
    with open(sol_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts_s = line.split()
            if parts_s[0] in ("instance", "budget", "lambda", "objective"):
                continue
            if len(parts_s) < 4:
                continue
            t = int(parts_s[0])
            sym = parts_s[1]
            lo, sh = int(parts_s[2]), int(parts_s[3])
            asset_idx = index.get(sym)
            if asset_idx is None:
                print(f"Error: Unknown symbol in schedule {sym}")
                return False
            sched_counts[(t, asset_idx)] = (lo, sh)
            
    sched_states = []
    for t in range(periods):
        st = [0] * 20
        for i in range(10):
            lo, sh = sched_counts.get((t, i), (0, 0))
            if not (0 <= lo <= 3 and 0 <= sh <= 3):
                print(f"Error: Schedule unit bound violated at t={t}, asset={i}: lo={lo}, sh={sh}")
                return False
            st[2*i] = lo
            st[2*i+1] = sh
        tot = sum(st)
        if tot > 4:
            print(f"Error: Schedule total budget violated at t={t}: total={tot}")
            return False
        net = sum(st[2*i] - st[2*i+1] for i in range(10))
        cslack = 10 - net
        bslack = 4 - tot
        if not (0 <= cslack <= 15):
            print(f"Error: Cash slack violated at t={t}: {cslack}")
            return False
        if not (0 <= bslack <= 127):
            print(f"Error: Budget slack violated at t={t}: {bslack}")
            return False
        s_idx = state_to_idx.get(tuple(st))
        if s_idx is None:
            print(f"Error: State not found in S at t={t}")
            return False
        sched_states.append(s_idx)
        
    # Recompute schedule objective and breakdown
    parts = dict(risk=0, ret=0, trans=0, cash=0, short=0, liq=0)
    for t in range(periods):
        s_idx = sched_states[t]
        pos_list, net, tot = state_pos_coords[s_idx]
        for gi, ui in pos_list:
            for gj, uj in pos_list:
                parts["risk"] += q_risk[t][gi][gj] * ui * uj
        cs = 10 - net
        parts["cash"] -= sum(coef_cash[k] for k in range(4) if (cs >> k) & 1)
        for g, u in pos_list:
            if g % 2 == 1:
                parts["short"] += w_short[t][g // 2] * u
        if t < periods - 1:
            for g, u in pos_list:
                if g % 2 == 0:
                    parts["ret"] -= w_ret[t][g // 2] * u
                else:
                    parts["ret"] += w_ret[t][g // 2] * u
        if t == 0:
            for g, u in pos_list:
                parts["trans"] += w_trans[0][g // 2] * u
        elif t < periods - 1:
            prev_st = states[sched_states[t-1]]
            cur_st = states[s_idx]
            for i in range(10):
                d = abs(prev_st[2*i] - cur_st[2*i]) + abs(prev_st[2*i+1] - cur_st[2*i+1])
                parts["trans"] += w_trans[t][i] * d
        else:
            for g, u in pos_list:
                parts["liq"] += w_trans[periods - 1][g // 2] * u
    tot_obj = sum(parts.values())
    expected_parts = {'risk': 25950, 'ret': -37218, 'trans': 3831, 'cash': -990, 'short': 30, 'liq': 0}
    if parts != expected_parts or tot_obj != -8397:
        print(f"Error: Objective mismatch. Got breakdown {parts}, total {tot_obj} (expected {expected_parts}, -8397)")
        return False
        
    # 5. Load certificate tables & verify Bellman inequalities
    with open(cert_file, "r", encoding="utf-8") as f:
        cert = json.load(f)
    with open(d_file, "r", encoding="utf-8") as f:
        d_tables = json.load(f)
    with open(u_file, "r", encoding="utf-8") as f:
        u_tables = json.load(f)
    v = cert.get("bellman_values_v")
    if not v or len(v) != 10:
        print(f"Error: Invalid bellman_values_v in certificate")
        return False
    
    # Inequality (a): V_0(s) <= stage_0(s)
    for s in range(n_states):
        if v[0][s] > stage_cost[0][s]:
            print(f"Error: Inequality (a) violated at state {s}: V_0={v[0][s]} > stage_0={stage_cost[0][s]}")
            return False
            
    # Inequality (b): D_t(p) <= V_{t-1}(p) and D_t(u) <= D_t(u+e_g) + w_{t,g}
    for t_idx in range(8):
        t = t_idx + 1
        dt = d_tables[t_idx]
        prev_v = v[t - 1]
        wt_g = [w_trans[t][g // 2] for g in range(20)]
        for p in range(n_states):
            if dt[p] > prev_v[p]:
                print(f"Error: Inequality (b) root violated at t={t}, p={p}")
                return False
        for u in range(n_states):
            dt_u = dt[u]
            for g, nxt in up_edges[u]:
                if dt_u > dt[nxt] + wt_g[g]:
                    print(f"Error: Inequality (b) cover relation violated at t={t}, u={u}, g={g}")
                    return False
                    
    # Inequality (c): U_t(m) <= D_t(m) and U_t(u+e_g) <= U_t(u) + w_{t,g}
    for t_idx in range(8):
        t = t_idx + 1
        ut = u_tables[t_idx]
        dt = d_tables[t_idx]
        wt_g = [w_trans[t][g // 2] for g in range(20)]
        for m in range(n_states):
            if ut[m] > dt[m]:
                print(f"Error: Inequality (c) root violated at t={t}, m={m}")
                return False
        for u in range(n_states):
            ut_u = ut[u]
            for g, nxt in up_edges[u]:
                if ut[nxt] > ut_u + wt_g[g]:
                    print(f"Error: Inequality (c) cover relation violated at t={t}, u={u}, g={g}")
                    return False
                    
    # Inequality (d): V_t(s) <= stage_t(s) + U_t(s) for t in 1..8
    for t_idx in range(8):
        t = t_idx + 1
        ut = u_tables[t_idx]
        vt = v[t]
        st = stage_cost[t]
        for s in range(n_states):
            if vt[s] > st[s] + ut[s]:
                print(f"Error: Inequality (d) violated at t={t}, s={s}")
                return False
                
    # Inequality (e): V_9(s) <= stage_9(s) + min V_8 and min V_9 == -8397
    min_v8 = min(v[8])
    for s in range(n_states):
        if v[9][s] > stage_cost[9][s] + min_v8:
            print(f"Error: Inequality (e) violated at s={s}")
            return False
    min_v9 = min(v[9])
    if min_v9 != -8397:
        print(f"Error: Inequality (e) min V_9={min_v9} != -8397")
        return False
        
    elapsed = time.time() - t_start
    print(f"Feasibility: VERIFIED (all constraints satisfied)")
    print(f"Breakdown: risk={parts['risk']}, return={parts['ret']}, transaction={parts['trans']}, cash_interest={parts['cash']}, short_cost={parts['short']}, liquidation={parts['liq']}, total={tot_obj}")
    print(f"Hasse Bellman Inequalities: ALL 5 PASS across all 10,606 states")
    print(f"Exact Global Optimality Certified: min V_9 = -8397 in {elapsed:.3f}s")
    return True

def main():
    pkg_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        ok = run_verification(pkg_dir)
    except Exception as e:
        print(f"Error during verification: {e}")
        ok = False
    if ok:
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
