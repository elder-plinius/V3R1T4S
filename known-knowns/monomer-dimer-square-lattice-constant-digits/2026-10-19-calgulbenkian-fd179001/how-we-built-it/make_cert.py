"""Producer of the p1 certificate (uses the C tools; the CHECKER does not).  Writes parts, MANIFEST.txt.
For m in 22, 24: double power vector -> exact integer vector (scale 2^72, 8 exact refinements, mdtm_ex cw with VECOUT) -> values at dihedral orbit
representatives (ascending) as 10-byte big-endian integers."""
import subprocess, os, struct, hashlib, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("MDTM_BIN_DIR", "{WORKDIR}/src") + "/"
src = open(HERE + "/check_p1.py").read().replace("\nmain()\n", "\n")
g = {"__file__": HERE + "/check_p1.py", "__name__": "chk"}; exec(compile(src, "check_p1", "exec"), g)
stream = b""; widths = []
for m in (22, 24):
    vd = HERE + "/tmp%d.dbl" % m; vx = HERE + "/tmp%d.u128" % m
    subprocess.check_call([SRC + "mdtm_dbl", "pow", str(m), "1", "80", vd], stdout=subprocess.DEVNULL)
    subprocess.check_call([SRC + "mdtm_ex", "cw", str(m), "1", vd, "8"], stdout=subprocess.DEVNULL, env=dict(os.environ, NTH="12", SC="72", VECOUT=vx))
    raw = open(vx, "rb").read(); os.remove(vd); os.remove(vx)
    reps = g["orbit_reps"](m); out = b""
    for s, imgs in reps:
        lo, hi = struct.unpack_from("<QQ", raw, 16 * s); v = lo | (hi << 64)
        assert 0 < v < (1 << 80)
        out += v.to_bytes(10, "big")
    widths.append((m, len(reps))); stream += out
    print("width", m, "orbits", len(reps), "bytes", len(out), flush=True)
parts = []; lines = []
for i in range(0, len(stream), 900000):
    b = stream[i:i + 900000]; name = "cert_part%02d.bin" % (i // 900000)
    open(HERE + "/" + name, "wb").write(b)
    lines.append("part %s %d %s" % (name, len(b), hashlib.sha256(b).hexdigest()))
lines.append("whole %d %s" % (len(stream), hashlib.sha256(stream).hexdigest()))
for m, n in widths: lines.append("width %d %d" % (m, n))
open(HERE + "/MANIFEST.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
