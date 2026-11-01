"""Assert the expected accept/reject pattern of the negative controls (reads out/controls/summary.json written by run_controls.py).
Entry value True = the checker REJECTED the (tampered) input. Expected: baseline accepted, every structural tamper rejected,
tau 0.84 rejected; the three loose-tau accepts on the one-frontier mini certificate are documented in object/REPLAY_NOTE.md section 3."""
import json, sys
s = json.load(open(sys.argv[1]))
must_reject = ["c1_bitflip", "c2_truncate", "c3_drop100", "c3b_drop100_countfixed", "c4_dup1", "c4b_dup1_countfixed", "c5_shrink", "c6_grow", "c8_samples32", "c9_psi07", "c12_swap_lohi", "c14_shift", "c15_countlie", "tau_0.84"]
must_accept = ["baseline"]
bad = [k for k in must_reject if s.get(k) is not True] + [k for k in must_accept if s.get(k) is not False]
if bad:
    print("controls: unexpected outcome for", bad); sys.exit(1)
print("controls: %d tampers rejected, baseline accepted" % len(must_reject))
