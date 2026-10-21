# Aggregate the 1% sample units output/s/p<pass>_c<chunk>.sum and compare with the user's chunk summaries.
import glob, os, sys
user = {}
for f in glob.glob("../../../../data-user/langton6x6-out6/chunk_*.sum"):
    t = open(f).read().split(); kv = dict(zip(t[0::2], t[1::2]))
    user[int(kv["chunk"])] = (int(kv["maxtcap"]), int(kv["maxtcap_mask"]))
units = {}
for f in glob.glob("output/s/p*_c*.sum"):
    t = open(f).read().split(); kv = dict(zip(t[0::2], t[1::2]))
    units[(int(kv["pass"]), int(kv["chunk"]))] = {k: kv[k] for k in kv}
noncap = sorted(glob.glob("output/s/*.noncap"))
tot = dict(n=0, CAP=0, UNCAP=0, OOB=0, steps=0, sumtcap=0)
over = []; gmax = (-1, None)
for p in range(4):
    done = [c for c in range(4096) if (p, c) in units]
    pt = dict(n=0, CAP=0, UNCAP=0, OOB=0)
    for c in done:
        u = units[(p, c)]
        for k in pt: pt[k] += int(u[k])
        for k in tot: tot[k] += int(u[k])
        mt = int(u["maxtcap"])
        if mt > user[c][0]: over.append((p, c, mt, u["maxtcap_mask"], user[c]))
        if mt > gmax[0]: gmax = (mt, int(u["maxtcap_mask"]))
    print("pass %d: chunks %d/4096 %s masks %d CAP %d UNCAP %d OOB %d" % (p, len(done), "COMPLETE" if len(done) == 4096 else "partial", pt["n"], pt["CAP"], pt["UNCAP"], pt["OOB"]))
print("TOTAL sampled masks checked %d (of 2^36 = %d; fraction %.6f%%) CAP %d UNCAP %d OOB %d" % (tot["n"], 1 << 36, 100.0 * tot["n"] / (1 << 36), tot["CAP"], tot["UNCAP"], tot["OOB"]))
print("simulated steps %d, mean steps/mask %.1f, mean tcap %.1f" % (tot["steps"], tot["steps"] / max(1, tot["n"]), tot["sumtcap"] / max(1, tot["CAP"])))
print("max sampled tcap %d at mask %s" % gmax)
print("units with sample maxtcap > user's chunk maxtcap: %d" % len(over))
for o in over: print("OVER", o)
print("noncap files: %d" % len(noncap))
for f in noncap: print("NONCAP", f, open(f).read().strip())
