"""Run subper_a over the full mask range split into P processes; merge into one output in subper_a's format.
Usage: run_a.py MODE N PROCS OUTFILE"""
import subprocess, sys, time, os
mode, n, P, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subper_a")
total = 1 << (n - 1)
cuts = [total * i // P for i in range(P + 1)]
t0 = time.time()
procs = [subprocess.Popen([exe, mode, str(n), str(cuts[i]), str(cuts[i + 1])], stdout=subprocess.PIPE, text=True) for i in range(P)]
res = []
for p in procs:
    o, _ = p.communicate()
    res.append((p.returncode, o.splitlines()))
best, arg, hist, over = -1, None, {}, 0
for i, (rc, lines) in enumerate(res):
    if rc != 0:
        raise SystemExit("chunk %d exit %d" % (i, rc))
    h = lines[0].split()
    mx, am = int(h[h.index("max") + 1]), int(h[h.index("argmask") + 1])
    if mx > best:                       # chunks are in increasing mask order: keep the first maximiser
        best, arg = mx, am
    over += int(lines[1].split()[1])
    for l in lines[2:]:
        k, v = l.split(); hist[int(k)] = hist.get(int(k), 0) + int(v)
assert sum(hist.values()) == total, (sum(hist.values()), total)
sset = [s for s in range(1, n + 1) if arg >> (s - 1) & 1]
with open(out, "w") as f:
    f.write("mode %s n %d range 0 %d max %d argmask %d set %s\n" % (mode, n, total, best, arg, " ".join(map(str, sset))))
    f.write("overflow %d\n" % over)
    for k in sorted(hist): f.write("%d %d\n" % (k, hist[k]))
print("A", mode, n, "max", best, "set", sset, "sets", total, "periods", len(hist), "overflow", over, "%.1fs" % (time.time() - t0))
