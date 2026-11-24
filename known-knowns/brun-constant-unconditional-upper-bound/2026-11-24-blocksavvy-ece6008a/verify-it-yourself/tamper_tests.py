"""K6 tamper tests: build corrupted copies of cert_rho_p128.json and require check_rho.py to print FAIL (exit 1) on each.
Usage (from the package folder): python3 verify-it-yourself/tamper_tests.py [python executable] [certificate]"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.argv[1] if len(sys.argv) > 1 else sys.executable
CERT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "object", "a_bound_certificate.json")
base = json.load(open(CERT))
ri = [i for i, e in enumerate(base["intervals"]) if len(e) == 4]
i0 = ri[len(ri) // 2]
def mut(name, f):
    c = json.loads(json.dumps(base)); f(c["intervals"]); return name, c
def lower(iv): iv[i0][2] = "%.20e" % (float(iv[i0][2]) * (1 - 1e-6))
def raise_(iv): iv[i0][2] = "%.20e" % (float(iv[i0][2]) * (1 + 1e-4))
def unflag(iv): iv[i0] = iv[i0][:3]
def movez(iv): iv[i0][1] = float.hex(float.fromhex(iv[i0][1]) * 0.9)
def flag_big(iv):
    j = next(k for k, e in enumerate(iv) if len(e) == 3 and e[0] == "z" and float.fromhex(e[1]) > 20000); iv[j] = iv[j] + ["rho"]
ok = True
print("rho intervals:", len(ri), "; tampered interval index:", i0)
for name, c in [mut("rho term lowered by 1e-6 relative", lower), mut("rho term raised by 1e-4 relative", raise_),
                mut("'rho' flag removed (Lambda^2 used)", unflag), mut("z_i of a rho interval scaled by 0.9", movez),
                mut("'rho' flag added to an interval with z > 20000", flag_big)]:
    fd, p = tempfile.mkstemp(suffix=".json"); os.close(fd); json.dump(c, open(p, "w"), separators=(",", ":"))
    r = subprocess.run([PY, os.path.join(HERE, "check_rho.py"), p, "128"], capture_output=True, text=True); os.unlink(p)
    last = [l for l in r.stdout.split("\n") if l.strip()][-2:]
    good = r.returncode == 1 and last[-1] == "FAIL"; ok &= good
    print("%-50s exit=%d  %s  -> %s" % (name, r.returncode, last[0][:150], "rejected (ok)" if good else "NOT REJECTED"))
print("tamper tests: PASS" if ok else "tamper tests: FAIL")
