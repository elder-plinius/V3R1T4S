#!/usr/bin/env python3
"""Run DFA invariant synthesizer across ALL 134 non-cycler canonical classes of size 8."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_and_inspect import canonicalize_bfs, enumerate_all_raw, format_system, simulate_brent, system_size
from dfa_synthesizer import synthesize_dfa_for_system, verify_dfa_invariant


def main():
    t_start = time.time()
    canon_classes = {}
    for r in enumerate_all_raw(8):
        c, _ = canonicalize_bfs(r)
        canon_classes[c] = canon_classes.get(c, 0) + 1

    unknowns = []
    for c, mult in sorted(canon_classes.items(), key=lambda x: format_system(x[0])):
        if all(len(w) >= 2 for w in c):
            continue
        st, _, _ = simulate_brent(c, max_steps=50000, max_len=100000)
        if st not in ("HALT", "CYCLE"):
            unknowns.append((c, mult))

    print(f"Testing DFA synthesizer on {len(unknowns)} canonical growing classes at S=8...", flush=True)
    solved = []
    unsolved = []
    for idx, (c, mult) in enumerate(unknowns):
        name = format_system(c)
        cert = synthesize_dfa_for_system(c, sim_steps=800, max_tape_len=900)
        if cert is not None and cert["type"] == "DFA_INVARIANT":
            ok, msg = verify_dfa_invariant(c, cert)
            assert ok, f"Verifier rejected {name}: {msg}"
            solved.append((c, mult, cert))
            print(f"  [{idx+1:3d}/{len(unknowns)}] SOLVED {name:12s} (size_c={system_size(c)}, mult={mult}) -> DFA states={cert['num_states']}, t0={cert['entry_step']}", flush=True)
        else:
            unsolved.append((c, mult))
            print(f"  [{idx+1:3d}/{len(unknowns)}] UNSOLVED {name:12s} (size_c={system_size(c)}, mult={mult})", flush=True)

    print(f"\n=== S=8 Summary ({time.time() - t_start:.1f}s) ===")
    print(f"Solved by DFA_INVARIANT: {len(solved)} / {len(unknowns)} canonical classes")
    print(f"Remaining unsolved:      {len(unsolved)} canonical classes:")
    for c, mult in unsolved:
        print(f"  {format_system(c)} (size_c={system_size(c)}, mult={mult})")


if __name__ == "__main__":
    main()
