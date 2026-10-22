"""Write and verify one object (lens lns-high).
Usage: python write_list.py N ASSIGN.npy OUTDIR MINSIZE [nolist]
  1. DP count (lsx count), assignment text (write_assign_txt.py) and its sha256.
  2. unless 'nolist': explicit list = lsx enum N ASSIGN.npy | gzip -1 > OUTDIR/nN_orders.txt.gz, then
     gzip -dc | hv - --stream --expect-n N --min-size MINSIZE --assign OUTDIR/nN_assignment.txt   (streaming check)
     gzip -dc | hv - --expect-n N --min-size MINSIZE                                               (sort check)
     and sha256 of the .gz file and of its content.
     with 'nolist': lsx enum | hv - --stream --expect-n N --min-size MINSIZE --assign ... (streaming check, no file).
Every external process runs under its own perl alarm; output goes to OUTDIR/nN_verify.txt.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = "<WORKDIR>/venv313/bin/python"


def al(cap, cmd):
    return ["nice", "-n", "10", "perl", "-e", "alarm shift; exec @ARGV", str(cap)] + cmd


def main():
    n, npy, out, mins = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
    nolist = len(sys.argv) > 5 and sys.argv[5] == "nolist"
    os.makedirs(out, exist_ok=True)
    vf = open(os.path.join(out, "n%d_verify.txt" % n), "a")

    def log(s):
        vf.write(s.rstrip("\n") + "\n")
        vf.flush()

    log("# %s write_list.py %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), " ".join(sys.argv[1:])))
    r = subprocess.run([os.path.join(HERE, "lsx"), "count", str(n), npy], capture_output=True, text=True)
    log("DP count (lsx count): " + r.stdout.strip())
    atxt = os.path.join(out, "n%d_assignment.txt" % n)
    subprocess.run([PY, os.path.join(HERE, "write_assign_txt.py"), npy, str(n), atxt], check=True)
    subprocess.run(["cp", npy, os.path.join(out, "n%d_assignment.npy" % n)], check=True)
    log("sha256 assignment: " + subprocess.run(["shasum", "-a", "256", atxt], capture_output=True, text=True).stdout.strip())
    hv = os.path.join(HERE, "hv")
    lsx = os.path.join(HERE, "lsx")
    if nolist:
        t0 = time.time()
        p1 = subprocess.Popen(al(3000, [lsx, "enum", str(n), npy]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(al(3000, [hv, "-", "--stream", "--expect-n", str(n), "--min-size", str(mins),
                                        "--assign", atxt]), stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
        o2 = p2.communicate()[0]
        e1 = p1.stderr.read().decode()
        p1.wait()
        log("enum: " + e1.strip())
        log("streaming check (lsx enum | hv - --stream ...), %.0f s:\n%s" % (time.time() - t0, o2.strip()))
        return
    gz = os.path.join(out, "n%d_orders.txt.gz" % n)
    t0 = time.time()
    with open(gz + ".tmp", "wb") as f:
        p1 = subprocess.Popen(al(3000, [lsx, "enum", str(n), npy]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(al(3000, ["gzip", "-1"]), stdin=p1.stdout, stdout=f)
        p1.stdout.close()
        p2.wait()
        e1 = p1.stderr.read().decode()
        p1.wait()
    os.rename(gz + ".tmp", gz)
    log("enum + gzip, %.0f s: %s" % (time.time() - t0, e1.strip()))
    log("sha256 list.gz: " + subprocess.run(["shasum", "-a", "256", gz], capture_output=True, text=True).stdout.strip())
    modes = [["--stream", "--assign", atxt]] + ([[]] if n <= 20 else [])  # sort-mode re-check only for n <= 20 (time)
    for mode in modes:
        t0 = time.time()
        p1 = subprocess.Popen(al(3000, ["gzip", "-dc", gz]), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(al(3000, [hv, "-", "--expect-n", str(n), "--min-size", str(mins)] + mode),
                              stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
        o2 = p2.communicate()[0]
        p1.wait()
        log("check gzip -dc | hv - %s (%.0f s):\n%s" % (" ".join(mode) or "(sort mode)", time.time() - t0, o2.strip()))
    if n > 21:
        return
    p1 = subprocess.Popen(al(3000, ["gzip", "-dc", gz]), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["shasum", "-a", "256"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
    p1.stdout.close()
    log("sha256 list content (uncompressed): " + p2.communicate()[0].strip())
    p1.wait()
    p1 = subprocess.Popen(al(3000, ["gzip", "-dc", gz]), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["wc", "-l"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
    p1.stdout.close()
    log("wc -l: " + p2.communicate()[0].strip())
    p1.wait()


if __name__ == "__main__":
    main()
