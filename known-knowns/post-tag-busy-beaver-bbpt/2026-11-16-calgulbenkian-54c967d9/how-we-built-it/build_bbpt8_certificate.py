#!/usr/bin/env python3
"""Generate the complete machine-checkable BB_PT(8) = 19 certificate JSON."""
import json
import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_and_inspect import canonicalize_bfs, enumerate_all_raw, format_system
from dfa_synthesizer import minimize_dfa, synthesize_dfa_for_system, verify_dfa_invariant


def find_exact_cycle_or_halt(rules, max_steps=60000, max_len=100000):
    tape = (0, 0)
    seen = {tape: 0}
    for t in range(1, max_steps + 1):
        if len(tape) < 2:
            return {"type": "HALT", "steps": t - 1}
        tape = tape[2:] + rules[tape[0]]
        if len(tape) < 2:
            return {"type": "HALT", "steps": t}
        if len(tape) > max_len:
            return None
        if tape in seen:
            t1 = seen[tape]
            return {"type": "CYCLE", "entry_step": t1, "period": t - t1, "cycle_tape_len": len(tape)}
        seen[tape] = t
    return None


def compute_dfa_witness_stats(rules, entry_step, trans, acc):
    n = len(rules)
    K = len(trans)
    acc_set = set(acc)
    tape = (0, 0)
    for _ in range(entry_step):
        tape = tape[2:] + rules[tape[0]]
    q = 0
    for ch in tape:
        q = trans[q][ch]
    assert q in acc_set

    total_pairs = 0
    for a in range(n):
        qa = trans[0][a]
        for b in range(n):
            qab = trans[qa][b]
            start = (qab, 0)
            visited = {start}
            queue = deque([start])
            while queue:
                p1, p2 = queue.popleft()
                for c in range(n):
                    nxt = (trans[p1][c], trans[p2][c])
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            total_pairs += len(visited)
    return len(tape), q, total_pairs


def main():
    S = 8
    canon_mult = {}
    raw_count = 0
    for r in enumerate_all_raw(S):
        raw_count += 1
        c, _ = canonicalize_bfs(r)
        canon_mult[c] = canon_mult.get(c, 0) + 1

    assert raw_count == 19693
    assert len(canon_mult) == 1728

    records = []
    halted_raw = 0
    cycle_raw = 0
    dfa_raw = 0
    max_halt_steps = 0
    champions_canon = []

    for c in sorted(canon_mult.keys(), key=format_system):
        mult = canon_mult[c]
        name = format_system(c)
        n = len(c)

        if all(len(w) >= 2 for w in c):
            tr, ac = minimize_dfa(n, [[1] * n, [2] * n, [2] * n], {2})
            cert = {
                "canon_id": name,
                "alphabet_size": n,
                "raw_multiplicity": mult,
                "status": "DFA_INVARIANT",
                "entry_step": 0,
                "num_states": len(tr),
                "transitions": tr,
                "accepting": ac,
            }
            ok, msg = verify_dfa_invariant(c, cert)
            assert ok, msg
            elen, eq, vpairs = compute_dfa_witness_stats(c, 0, tr, ac)
            cert["entry_tape_len"] = elen
            cert["entry_accept_state"] = eq
            cert["verified_product_pairs"] = vpairs
            records.append(cert)
            dfa_raw += mult
            continue

        hc = find_exact_cycle_or_halt(c, max_steps=50000, max_len=20000)
        if hc is not None and hc["type"] == "HALT":
            steps = hc["steps"]
            if steps > max_halt_steps:
                max_halt_steps = steps
                champions_canon = [name]
            elif steps == max_halt_steps:
                champions_canon.append(name)
            records.append({
                "canon_id": name,
                "alphabet_size": n,
                "raw_multiplicity": mult,
                "status": "HALT",
                "steps": steps,
            })
            halted_raw += mult
        elif hc is not None and hc["type"] == "CYCLE":
            records.append({
                "canon_id": name,
                "alphabet_size": n,
                "raw_multiplicity": mult,
                "status": "CYCLE",
                "entry_step": hc["entry_step"],
                "period": hc["period"],
                "cycle_tape_len": hc["cycle_tape_len"],
            })
            cycle_raw += mult
        else:
            dcert = synthesize_dfa_for_system(c, sim_steps=800, max_tape_len=900)
            assert dcert is not None and dcert["type"] == "DFA_INVARIANT", f"Failed DFA for {name}"
            tr, ac = minimize_dfa(n, dcert["transitions"], set(dcert["accepting"]))
            t0 = dcert["entry_step"]
            cert = {
                "canon_id": name,
                "alphabet_size": n,
                "raw_multiplicity": mult,
                "status": "DFA_INVARIANT",
                "entry_step": t0,
                "num_states": len(tr),
                "transitions": tr,
                "accepting": ac,
            }
            ok, msg = verify_dfa_invariant(c, cert)
            assert ok, f"Verification failed for {name}: {msg}"
            elen, eq, vpairs = compute_dfa_witness_stats(c, t0, tr, ac)
            cert["entry_tape_len"] = elen
            cert["entry_accept_state"] = eq
            cert["verified_product_pairs"] = vpairs
            records.append(cert)
            dfa_raw += mult

    assert halted_raw + cycle_raw + dfa_raw == raw_count
    assert max_halt_steps == 19

    out_obj = {
        "problem": "BB_PT(8)",
        "convention": "wiki.bbchallenge.org/wiki/Post_Tag_System (deletion_number=2, size=|A|+sum|w_a|, initial_tape=00, halt_when_len_lt_2)",
        "size": 8,
        "exact_bb_pt_8": max_halt_steps,
        "canonical_champions": champions_canon,
        "counts": {
            "total_raw_systems": raw_count,
            "total_canonical_classes": len(records),
            "halted_raw_systems": halted_raw,
            "cycle_raw_systems": cycle_raw,
            "dfa_invariant_raw_systems": dfa_raw,
            "halted_canonical_classes": sum(1 for r in records if r["status"] == "HALT"),
            "cycle_canonical_classes": sum(1 for r in records if r["status"] == "CYCLE"),
            "dfa_invariant_canonical_classes": sum(1 for r in records if r["status"] == "DFA_INVARIANT"),
        },
        "canonical_classes": records,
    }

    res_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "result")
    os.makedirs(res_dir, exist_ok=True)
    out_path = os.path.join(res_dir, "bbpt8_certificates.json")
    # Compact one-line-per-class JSON formatting for readability and small file size (<200 KB)
    lines = [
        "{",
        f'  "problem": {json.dumps(out_obj["problem"])},',
        f'  "convention": {json.dumps(out_obj["convention"])},',
        f'  "size": {out_obj["size"]},',
        f'  "exact_bb_pt_8": {out_obj["exact_bb_pt_8"]},',
        f'  "canonical_champions": {json.dumps(out_obj["canonical_champions"])},',
        f'  "counts": {json.dumps(out_obj["counts"])},',
        '  "canonical_classes": [',
    ]
    for i, rec in enumerate(records):
        comma = "," if i + 1 < len(records) else ""
        lines.append("    " + json.dumps(rec, separators=(",", ":")) + comma)
    lines.append("  ]")
    lines.append("}\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Wrote compact certificate JSON bytes:", os.path.getsize(out_path))
    print("Exact BB_PT(8) =", out_obj["exact_bb_pt_8"], "champion =", out_obj["canonical_champions"])


if __name__ == "__main__":
    main()
