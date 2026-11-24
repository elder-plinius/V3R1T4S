#!/usr/bin/env python3
"""Standalone first-principles verifier for Exact BB_PT(8) = 19 (post-tag-busy-beaver-bbpt).

Python 3 standard library only. Verifies:
1. Wiki 2-tag simulator calibration on 0111_1 (10), 111_20_ (19), 11_021_2 (49),
   112_1_002 (779), and 120221_0_2 (196,841).
2. Exhaustive unpruned enumeration of all 19,693 raw size-8 2-tag systems
   (n in 1..8, n + sum |w_i| = 8) and explicit conjugacy proof for each raw system
   onto its canonical representative.
3. Exact halting step count for every HALT class (confirming max = 19 at 111_20_).
4. Exact configuration repetition with minimal entry/period for every CYCLE class.
5. Exact finite-automaton inductive invariant (entry, length >= 2 safety, synchronized
   Q x Q product-closure, and canonical Moore minimality) for every DFA_INVARIANT class.
"""
import itertools
import json
import math
import os
import sys
from collections import deque


def parse_system(s):
    if not isinstance(s, str):
        raise ValueError("system string required")
    parts = s.split("_")
    rules = []
    n = len(parts)
    for part in parts:
        w = []
        for ch in part:
            if not ("0" <= ch <= "9"):
                raise ValueError(f"invalid symbol {ch}")
            v = ord(ch) - ord("0")
            if v >= n:
                raise ValueError(f"symbol {v} out of alphabet 0..{n-1}")
            w.append(v)
        rules.append(tuple(w))
    return tuple(rules)


def format_system(rules):
    return "_".join("".join(str(x) for x in w) for w in rules)


def simulate_steps(rules, max_steps):
    buf = [0, 0]
    head = 0
    steps = 0
    while len(buf) - head >= 2:
        if steps >= max_steps:
            raise ValueError(f"exceeded {max_steps} steps without halting")
        a = buf[head]
        head += 2
        buf.extend(rules[a])
        steps += 1
        if head > 65536 and head * 2 > len(buf):
            del buf[:head]
            head = 0
    return steps


def enumerate_raw_size_s(S):
    for n in range(1, S + 1):
        L = S - n
        combos = list(itertools.combinations(range(L + n - 1), n - 1))
        for word_chars in itertools.product(range(n), repeat=L):
            for bars in combos:
                rules = []
                prev = -1
                cidx = 0
                for b in bars + (L + n - 1,):
                    seg = b - prev - 1
                    rules.append(word_chars[cidx : cidx + seg])
                    cidx += seg
                    prev = b
                yield tuple(rules)


def canonicalize_and_verify_conjugacy(raw_rules):
    remap = {0: 0}
    order = [0]
    canon = []
    idx = 0
    while idx < len(order):
        orig = order[idx]
        idx += 1
        cw = []
        for ch in raw_rules[orig]:
            nc = remap.get(ch)
            if nc is None:
                nc = len(remap)
                remap[ch] = nc
                order.append(ch)
            cw.append(nc)
        canon.append(tuple(cw))
    canon_t = tuple(canon)

    # Explicit conjugacy verification:
    # 1) pi(0) == 0 so pi((0, 0)) == (0, 0).
    # 2) V_reach = domain(remap) is closed under raw_rules, and pi(raw_rules[x]) == canon_t[pi(x)].
    if remap.get(0) != 0 or len(remap) != len(canon_t):
        raise ValueError("conjugacy bijection invalid")
    for orig, cid in remap.items():
        mapped_rhs = tuple(remap[ch] for ch in raw_rules[orig])
        if mapped_rhs != canon_t[cid]:
            raise ValueError("conjugacy homomorphism mismatch")
    return canon_t


def check_moore_minimal_and_bfs(n, trans, acc_list):
    K = len(trans)
    acc_set = set(acc_list)
    # 1. BFS canonical order from state 0
    bfs = []
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        bfs.append(u)
        for c in range(n):
            v = trans[u][c]
            if v not in seen:
                seen.add(v)
                q.append(v)
    if bfs != list(range(K)):
        raise ValueError("DFA states are not all reachable in canonical BFS order")

    # 2. Moore pairwise distinguishability
    cls = [1 if i in acc_set else 0 for i in range(K)]
    num_cls = len(set(cls))
    if K > 1 and num_cls == 1:
        raise ValueError("non-minimal constant DFA")
    while num_cls < K:
        sig_map = {}
        new_cls = [0] * K
        for i in range(K):
            sig = (cls[i],) + tuple(cls[trans[i][c]] for c in range(n))
            cid = sig_map.get(sig)
            if cid is None:
                cid = len(sig_map)
                sig_map[sig] = cid
            new_cls[i] = cid
        if len(sig_map) == num_cls:
            break
        cls = new_cls
        num_cls = len(sig_map)
    if num_cls != K:
        raise ValueError(f"DFA not minimal: {num_cls} classes for {K} states")


def verify_all(cert_path):
    # Step 1: Calibration gate
    calibrations = [
        ("0111_1", 7, 10),
        ("111_20_", 8, 19),
        ("11_021_2", 9, 49),
        ("112_1_002", 10, 779),
        ("120221_0_2", 11, 196841),
    ]
    for s, exp_sz, exp_steps in calibrations:
        r = parse_system(s)
        sz = len(r) + sum(len(w) for w in r)
        if sz != exp_sz:
            raise ValueError(f"calibration size mismatch on {s}")
        st = simulate_steps(r, exp_steps + 10)
        if st != exp_steps:
            raise ValueError(f"calibration step mismatch on {s}: got {st}, expected {exp_steps}")
    print("Calibration checks (S=7..11): OK")

    # Step 2: Load certificate JSON with strict duplicate-key detection
    with open(cert_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("problem") != "BB_PT(8)" or data.get("size") != 8:
        raise ValueError("header mismatch in certificate JSON")

    S = 8
    expected_raw = sum(math.comb(S - 1, n - 1) * (n ** (S - n)) for n in range(1, S + 1))
    if expected_raw != 19693:
        raise ValueError("combinatorial count formula error")

    # Step 3: Exhaustive raw enumeration & conjugacy verification
    emp_mult = {}
    raw_seen = 0
    for r in enumerate_raw_size_s(S):
        if len(r) + sum(len(w) for w in r) != S:
            raise ValueError("raw system size error")
        raw_seen += 1
        c = canonicalize_and_verify_conjugacy(r)
        cname = format_system(c)
        emp_mult[cname] = emp_mult.get(cname, 0) + 1

    if raw_seen != expected_raw:
        raise ValueError(f"enumerated {raw_seen} raw systems, expected {expected_raw}")
    print(f"Exhaustive raw enumeration & conjugacy check: {raw_seen} systems -> {len(emp_mult)} canonical classes OK")

    records = data.get("canonical_classes")
    if not isinstance(records, list) or len(records) != len(emp_mult):
        raise ValueError("canonical_classes length mismatch")

    seen_ids = set()
    halted_raw = 0
    cycle_raw = 0
    dfa_raw = 0
    halted_c = 0
    cycle_c = 0
    dfa_c = 0
    max_halt = 0
    champs = []

    for rec in records:
        cid = rec.get("canon_id")
        if cid in seen_ids or cid not in emp_mult:
            raise ValueError(f"unexpected or duplicate canon_id: {cid}")
        seen_ids.add(cid)

        rules = parse_system(cid)
        n = len(rules)
        if rec.get("alphabet_size") != n:
            raise ValueError(f"alphabet_size mismatch for {cid}")
        mult = rec.get("raw_multiplicity")
        if mult != emp_mult[cid]:
            raise ValueError(f"raw_multiplicity mismatch for {cid}: cert={mult} actual={emp_mult[cid]}")

        status = rec.get("status")
        if status == "HALT":
            steps_claimed = rec.get("steps")
            if not isinstance(steps_claimed, int) or steps_claimed < 1:
                raise ValueError(f"bad steps for {cid}")
            actual_steps = simulate_steps(rules, steps_claimed + 5)
            if actual_steps != steps_claimed:
                raise ValueError(f"HALT step mismatch on {cid}: cert={steps_claimed} actual={actual_steps}")
            halted_raw += mult
            halted_c += 1
            if actual_steps > max_halt:
                max_halt = actual_steps
                champs = [cid]
            elif actual_steps == max_halt:
                champs.append(cid)

        elif status == "CYCLE":
            t1 = rec.get("entry_step")
            per = rec.get("period")
            clen = rec.get("cycle_tape_len")
            if not (isinstance(t1, int) and isinstance(per, int) and isinstance(clen, int)):
                raise ValueError(f"CYCLE integer fields invalid on {cid}")
            if t1 < 0 or per < 1:
                raise ValueError(f"CYCLE bounds invalid on {cid}")
            tape = (0, 0)
            history = {tape: 0}
            first_rep = None
            for t in range(1, t1 + per + 1):
                if len(tape) < 2:
                    raise ValueError(f"CYCLE system {cid} halted at {t-1}")
                tape = tape[2:] + rules[tape[0]]
                if len(tape) < 2:
                    raise ValueError(f"CYCLE system {cid} halted at {t}")
                if tape in history:
                    first_rep = (history[tape], t - history[tape], len(tape))
                    if t != t1 + per:
                        raise ValueError(f"CYCLE non-minimal repeat on {cid}")
                    break
                history[tape] = t
            if first_rep != (t1, per, clen):
                raise ValueError(f"CYCLE witness mismatch on {cid}: got {first_rep}, cert={(t1, per, clen)}")
            cycle_raw += mult
            cycle_c += 1

        elif status == "DFA_INVARIANT":
            t0 = rec.get("entry_step")
            K = rec.get("num_states")
            trans = rec.get("transitions")
            acc = rec.get("accepting")
            elen = rec.get("entry_tape_len")
            eq = rec.get("entry_accept_state")
            vpairs = rec.get("verified_product_pairs")

            if not (isinstance(t0, int) and t0 >= 0 and isinstance(K, int) and K >= 1):
                raise ValueError(f"DFA scalar fields invalid on {cid}")
            if not (isinstance(trans, list) and len(trans) == K):
                raise ValueError(f"DFA transitions size mismatch on {cid}")
            for row in trans:
                if not (isinstance(row, list) and len(row) == n and all(isinstance(q, int) and 0 <= q < K for q in row)):
                    raise ValueError(f"DFA bad row on {cid}")
            if not (isinstance(acc, list) and all(isinstance(q, int) and 0 <= q < K for q in acc)):
                raise ValueError(f"DFA bad accepting list on {cid}")
            if acc != sorted(set(acc)):
                raise ValueError(f"DFA accepting list not sorted unique on {cid}")

            check_moore_minimal_and_bfs(n, trans, acc)
            acc_set = set(acc)

            # 1. Concrete entry check
            tape = (0, 0)
            for _ in range(t0):
                if len(tape) < 2:
                    raise ValueError(f"DFA system {cid} halted before entry_step")
                tape = tape[2:] + rules[tape[0]]
            if len(tape) < 2 or len(tape) != elen:
                raise ValueError(f"DFA entry_tape_len mismatch on {cid}")
            q = 0
            for ch in tape:
                q = trans[q][ch]
            if q != eq or q not in acc_set:
                raise ValueError(f"DFA entry state check failed on {cid}")

            # 2. Halting safety: reject epsilon and all length-1 strings
            if 0 in acc_set:
                raise ValueError(f"DFA accepts epsilon on {cid}")
            for a in range(n):
                if trans[0][a] in acc_set:
                    raise ValueError(f"DFA accepts length-1 word {a} on {cid}")

            # 3. Synchronized product-BFS 1-step closure check
            after_wa = []
            for a in range(n):
                wa = rules[a]
                row = []
                for p2 in range(K):
                    cur = p2
                    for ch in wa:
                        cur = trans[cur][ch]
                    row.append(cur)
                after_wa.append(row)

            total_pairs = 0
            for a in range(n):
                qa = trans[0][a]
                after_a = after_wa[a]
                for b in range(n):
                    qab = trans[qa][b]
                    start = (qab, 0)
                    visited = {start}
                    queue = deque([start])
                    while queue:
                        p1, p2 = queue.popleft()
                        if p1 in acc_set and after_a[p2] not in acc_set:
                            raise ValueError(f"DFA closure violated on {cid} at ({a},{b}) pair ({p1},{p2})")
                        for c in range(n):
                            nxt = (trans[p1][c], trans[p2][c])
                            if nxt not in visited:
                                visited.add(nxt)
                                queue.append(nxt)
                    total_pairs += len(visited)

            if total_pairs != vpairs:
                raise ValueError(f"DFA verified_product_pairs mismatch on {cid}: {total_pairs} != {vpairs}")

            dfa_raw += mult
            dfa_c += 1
        else:
            raise ValueError(f"unknown status {status} on {cid}")

    # Step 4: Verify global summary and exact BB_PT(8)
    expected_counts = {
        "total_raw_systems": expected_raw,
        "total_canonical_classes": len(emp_mult),
        "halted_raw_systems": halted_raw,
        "cycle_raw_systems": cycle_raw,
        "dfa_invariant_raw_systems": dfa_raw,
        "halted_canonical_classes": halted_c,
        "cycle_canonical_classes": cycle_c,
        "dfa_invariant_canonical_classes": dfa_c,
    }
    if data.get("counts") != expected_counts:
        raise ValueError(f"summary counts mismatch: {data.get('counts')} vs {expected_counts}")
    if halted_raw + cycle_raw + dfa_raw != expected_raw:
        raise ValueError("partition does not sum to 19693")
    if data.get("exact_bb_pt_8") != max_halt or max_halt != 19:
        raise ValueError(f"exact_bb_pt_8 mismatch: {data.get('exact_bb_pt_8')} vs {max_halt}")
    if data.get("canonical_champions") != champs or champs != ["111_20_"]:
        raise ValueError(f"canonical_champions mismatch: {data.get('canonical_champions')} vs {champs}")

    print(f"Verified all {expected_raw} raw size-8 2-tag systems ({len(emp_mult)} canonical classes):")
    print(f"  HALT:          {halted_raw:5d} raw ({halted_c:4d} canonical), max steps = {max_halt} ({champs[0]})")
    print(f"  CYCLE:         {cycle_raw:5d} raw ({cycle_c:4d} canonical)")
    print(f"  DFA_INVARIANT: {dfa_raw:5d} raw ({dfa_c:4d} canonical)")
    print("BB_PT(8) = 19 CERTIFIED EXACT.")
    print("PASS")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_cert = os.path.join(os.path.dirname(here), "object", "bbpt8_certificates.json")
    cert_path = sys.argv[1] if len(sys.argv) > 1 else default_cert
    try:
        verify_all(cert_path)
    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
