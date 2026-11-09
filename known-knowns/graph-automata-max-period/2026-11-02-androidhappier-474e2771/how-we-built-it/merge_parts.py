"""Merge the 8 residue-class outputs of Program A and Program B (n = 9) into the two summary files.
Usage (from the folder holding A_n9_part0..7.txt and B_n9_part0..7.txt):  python3 merge_parts.py [dir]
Writes A_n9_merged.txt and B_n9_merged.txt in that folder. Python 3 standard library only."""
import os, re, sys
d = sys.argv[1] if len(sys.argv) > 1 else "."
A001349_9 = 261080
# Program A parts: first line "n=9 mode=neighbours graphs=G maxperiod=P witness_graph6=W witness_rule_mask=M witness_state=S rule={..}", then "hist k c"
tot = 0; best = None; hist = {}
for r in range(8):
    lines = open(os.path.join(d, "A_n9_part%d.txt" % r)).read().splitlines()
    m = re.match(r"n=9 mode=neighbours graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+) witness_rule_mask=\d+ witness_state=(\d+) rule=(\{[0-9,]*\})", lines[0])
    g, p, w, s, rule = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4), m.group(5)
    tot += g
    if best is None or p > best[0]: best = (p, w, rule, s)
    for l in lines[1:]:
        if l.startswith("hist "):
            _, k, c = l.split(); hist[int(k)] = hist.get(int(k), 0) + int(c)
with open(os.path.join(d, "A_n9_merged.txt"), "w") as f:
    f.write("total_connected_graphs %d (A001349(9)=%d) %s\n" % (tot, A001349_9, "match" if tot == A001349_9 else "MISMATCH"))
    f.write("max_period %r\n" % (best,))
    f.write("graphs_by_max_period_over_rules %r\n" % sorted(hist.items()))
# Program B parts: "order=9 connected_graphs=G max_cycle=P witness W rule_mask M state S", then "lengths: ..."
tot = 0; best = None; lengths = set()
for r in range(8):
    lines = open(os.path.join(d, "B_n9_part%d.txt" % r)).read().splitlines()
    m = re.match(r"order=9 connected_graphs=(\d+) max_cycle=(\d+) witness (\S+) rule_mask (\d+) state (\d+)", lines[0])
    g, p, w, mask, s = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    tot += g
    if best is None or p > best[0]: best = (p, w, mask, s)
    lengths |= set(int(x) for x in lines[1].split(":")[1].split())
with open(os.path.join(d, "B_n9_merged.txt"), "w") as f:
    f.write("total_connected_graphs %d %s\n" % (tot, "match" if tot == A001349_9 else "MISMATCH"))
    f.write("max_cycle %r rule %r\n" % (best, [k for k in range(9) if best[2] >> k & 1]))
    f.write("cycle_lengths_seen %r\n" % sorted(lengths))
