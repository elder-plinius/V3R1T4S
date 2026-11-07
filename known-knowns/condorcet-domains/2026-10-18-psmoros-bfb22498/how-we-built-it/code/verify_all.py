"""Write and verify the final objects one at a time (lens lns-high).  For each n: copy best/nN.npy, then
write_list.py (explicit list for n <= 22, streaming check only for n >= 23).  MINSIZE = max(Table 4, wave-1 best
verified size) + 1.  Usage: python verify_all.py LENSDIR N1,N2,..."""
import os
import subprocess
import sys
import time

L = sys.argv[1]
ns = [int(x) for x in sys.argv[2].split(",")]
T4 = {15: 59430, 16: 131536, 17: 292015, 18: 649079, 19: 1432836, 20: 3155366, 21: 6674931, 22: 15037178,
      23: 33162136, 24: 73279872, 25: 160316046}
W1 = {17: 297146, 18: 665630, 19: 1468255, 20: 3252095, 21: 7402109, 22: 16140934, 23: 34582516, 24: 76653380,
      25: 169570159}
PY = "<WORKDIR>/venv313/bin/python"
for n in ns:
    src = os.path.join(L, "best", "n%d.npy" % n)
    snap = os.path.join(L, "result", "n%d_src.npy" % n)
    subprocess.run(["cp", src, snap], check=True)
    mins = max(T4[n], W1.get(n, 0)) + 1
    args = [PY, os.path.join(L, "code", "write_list.py"), str(n), snap, os.path.join(L, "result"), str(mins)]
    if n >= 23:
        args.append("nolist")
    t0 = time.time()
    subprocess.run(args)
    os.remove(snap)
    print("%s n %d done in %.0f s" % (time.strftime("%H:%M:%S", time.gmtime()), n, time.time() - t0), flush=True)
