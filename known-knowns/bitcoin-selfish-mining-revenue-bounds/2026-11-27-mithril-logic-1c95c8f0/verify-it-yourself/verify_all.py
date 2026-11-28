#!/usr/bin/env python3
"""Package verifier (Python standard library only). Run from anywhere: python3 verify_all.py
1. every file under object/ matches object/MANIFEST.txt (a changed digit anywhere is caught),
2. the 32 parts of the headline certificate are joined, the join has the pinned sha256,
3. check_cert.py (exact Fractions, rebuilds N_rho^T itself) gives CERT_OK for the T = 2000 headline certificate
   and the T = 250 certificate, under the printed and the corrected compensation,
4. negative controls fail as they must (tampered certificate, rho = 0.66, exact positive-gain policy at the old rho),
5. the exact numbers: rho = 67005787/10^8 <= 0.70099 and g < 0.
Last output line: PASS or FAIL (exit status 1 on FAIL)."""
import gzip, hashlib, os, shutil, subprocess, sys, tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(os.path.dirname(HERE), "object")
sys.path.insert(0, HERE)
TMP = tempfile.mkdtemp(prefix="ssz_cert_")
import check_cert as cc

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def run(args):
    r = subprocess.run([sys.executable] + args, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode().replace(OBJ + os.sep, "object/").replace(TMP + os.sep, "")
    return r.returncode, out

def main():
    ok = True
    def need(cond, msg):
        nonlocal ok
        print(("ok:   " if cond else "FAIL: ") + msg)
        ok = ok and cond
    man = {}
    for line in open(os.path.join(OBJ, "MANIFEST.txt")):
        if line.strip():
            h, name = line.split(None, 1)
            man[name.strip()] = h
    pin = man.pop("JOINED upper_a45_T2000_rho67005787.txt.gz")
    for name, h in sorted(man.items()):
        p = os.path.join(OBJ, name)
        need(os.path.isfile(p) and sha(p) == h, "sha256 of object/%s" % name)
    tmp = TMP
    joined = os.path.join(tmp, "upper_a45_T2000_rho67005787.txt.gz")
    with open(joined, "wb") as out:
        for name in sorted(n for n in man if n.startswith("parts/")):
            with open(os.path.join(OBJ, name), "rb") as f:
                out.write(f.read())
    need(sha(joined) == pin, "joined T=2000 certificate has sha256 %s" % pin)
    for path, label in ((joined, "headline T=2000"), (os.path.join(OBJ, "upper_a45_T250_rho67078.txt.gz"), "T=250")):
        rc, out = run(["check_cert.py", path, "both"])
        print(out.strip())
        need(rc == 0 and out.strip().endswith("CERT_OK") and "CERT_FAIL" not in out, "%s certificate CERT_OK, printed and corrected" % label)
    hdr, H = cc.load(joined)
    g, where, pairs = cc.check(hdr, H, "corrected")
    need(F(hdr["alpha"]) == F(9, 20) and F(hdr["rho"]) == F(67005787, 10**8) and hdr["T"] == 2000, "header alpha 9/20, rho 67005787/10^8, T 2000")
    need(g < 0 and F(hdr["rho"]) <= F(70099, 100000), "g = %s < 0 and rho <= 0.70099 (exact)" % g)
    for name in ("NEG_dual_a45_T95_rho66.txt.gz", "NEG_tampered_a45_T250_rho67078.txt.gz"):
        rc, out = run(["check_cert.py", os.path.join(OBJ, "controls", name), "both"])
        print(out.strip())
        need(out.strip().endswith("CERT_FAIL"), "negative control %s is rejected" % name)
    rc, out = run(["check_policy.py", os.path.join(OBJ, "controls", "NEG_pol_a45_T250_rho67045.txt.gz"),
                   os.path.join(OBJ, "controls", "NEG_pol_a45_T250_rho67045.pol.gz"), "corrected"])
    print(out.strip())
    need(out.strip().endswith("POLICY_GAIN_POSITIVE"), "old claim point rho=0.67045, T=250: exact positive-gain policy in corrected N (no certificate possible)")
    shutil.rmtree(TMP, ignore_errors=True)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # any unexpected condition (for example a damaged file) is a FAIL, never a crash
        print("FAIL: %s: %s" % (type(e).__name__, e))
        shutil.rmtree(TMP, ignore_errors=True)
        print("FAIL")
        sys.exit(1)
