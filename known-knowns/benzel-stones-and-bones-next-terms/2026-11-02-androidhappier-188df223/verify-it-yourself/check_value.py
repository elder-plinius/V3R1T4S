"""Standalone checks for object/VALUE.txt (Python 3 standard library only). Run from the package folder.

  python3 verify-it-yourself/check_value.py pins          VALUE.txt hash = INDEX.csv; every pin line; field formats
  python3 verify-it-yourself/check_value.py evidence      the run's saved outputs agree with VALUE.txt
  python3 verify-it-yourself/check_value.py fresh FILE    fresh results (lines "SEQ N PROGRAM VALUE") vs published terms

Every mode prints one line per finding and ends with "ok" or exits with status 1."""
import csv, hashlib, os, re, sys

VAL = "object/VALUE.txt"
BAD = []


def bad(msg):
    BAD.append(msg)
    print("BAD  " + msg)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load():
    text = open(VAL, encoding="utf-8").read()
    kv, pins = {}, []
    for line in text.splitlines():
        if line.startswith("pin "):
            m = re.fullmatch(r"pin ([0-9a-f]{64})  (\S+)", line)
            if not m:
                bad("malformed pin line: " + line)
            else:
                pins.append((m.group(1), m.group(2)))
        elif line and not line.startswith("#"):
            k, _, v = line.partition(": ")
            kv[k] = v
    return text, kv, pins


def seq(kv, key):
    return [int(x) for x in kv[key].split(",")]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pins"
    text, kv, pins = load()
    value = int(kv.get("value", "-1"))
    A16 = seq(kv, "published A364416 n=3..20")
    A17 = seq(kv, "published A364417 n=3..19")
    pub = {"A364416": {n + 3: v for n, v in enumerate(A16)}, "A364417": {n + 3: v for n, v in enumerate(A17)}}
    if mode == "pins":
        rows = list(csv.reader(open("INDEX.csv", encoding="utf-8")))
        row = dict(zip(rows[0], rows[1]))
        if row.get("file") != VAL or row.get("sha256") != sha(VAL):
            bad("sha256 of %s (%s) differs from INDEX.csv (%s)" % (VAL, sha(VAL), row.get("sha256")))
        else:
            print("ok   %s sha256 %s matches INDEX.csv" % (VAL, row["sha256"]))
        if row.get("value") != str(value) or kv.get("cell") != "A364417(20) = T113(20,37)":
            bad("INDEX.csv value/cell disagree with VALUE.txt")
        if kv.get("target") != "benzel-stones-and-bones-next-terms":
            bad("target line changed")
        for line in ("run A", "run B"):
            if ("result %d;" % value) not in kv.get(line, "") or "exit 0; overflow 0" not in kv.get(line, ""):
                bad("'%s' line does not state result %d with exit 0, overflow 0" % (line, value))
        if len(A16) != 18 or len(A17) != 17:
            bad("published term lists have the wrong length")
        if value in A16 or value in A17:
            bad("the value is one of the published terms")
        n_ok = 0
        for h, p in pins:
            if not os.path.isfile(p):
                bad("pinned file missing: " + p)
            elif sha(p) != h:
                bad("pin mismatch: " + p)
            else:
                n_ok += 1
        if len(pins) < 200:
            bad("too few pin lines (%d)" % len(pins))
        print("ok   %d pinned files match" % n_ok if n_ok == len(pins) else "BAD  %d of %d pins match" % (n_ok, len(pins)))
    elif mode == "evidence":
        def run(pre):
            out = open(pre + ".out").read().split()
            tm = open(pre + ".time").read().split()[0]
            err = open(pre + ".err").read()
            return int(out[0]), tm, ("overflow=0" in err or "overflow 0" in err), err
        a = run("object/evidence/A_final/A364417_n20")
        b = run("object/evidence/B_final/B_A364417_n20")
        for name, r in (("A (benzZQ.c)", a), ("B (benzB64.c)", b)):
            if r[0] == value and r[1] == "exit=0" and r[2]:
                print("ok   n=20 run %s: %d, exit 0, overflow 0" % (name, r[0]))
            else:
                bad("n=20 run %s: got %s %s overflow0=%s, VALUE.txt says %d" % (name, r[0], r[1], r[2], value))
        if "resumed t=210" not in a[3]:
            bad("run A log does not show the declared resume at t=210")
        seg = open("object/evidence/A_final/A364417_n20.seg1.time").read().split()[0]
        if seg != "exit=143":
            bad("run A first segment should be the declared SIGTERM stop (exit=143), got " + seg)
        for prog, d, top in (("benzZQ.c", "A_repro", {"A364416": 20, "A364417": 19}),
                             ("benzB128.c", "B_repro", {"A364416": 18, "A364417": 18})):
            k = 0
            for s, terms in pub.items():
                for n in range(3, top[s] + 1):
                    r = run("object/evidence/%s/%s_n%d" % (d, s, n))
                    if r[0] != terms[n] or r[1] != "exit=0" or not r[2]:
                        bad("%s %s(%d): got %d %s overflow0=%s, published %d" % (prog, s, n, r[0], r[1], r[2], terms[n]))
                    else:
                        k += 1
            print("ok   %s saved runs: %d published terms reproduced" % (prog, k))
        ck = int(open("object/evidence/A_ckpt_test/r2.out").read().split()[0])
        if ck != pub["A364416"][16]:
            bad("checkpoint-resume test gives %d, A364416(16) is %d" % (ck, pub["A364416"][16]))
        else:
            print("ok   checkpoint-resume test (16,28) gives A364416(16)")
        k = 0
        for f in ("out_indep_n3_8.txt", "out_indep_n9_11.txt"):
            for line in open("object/evidence/" + f):
                w = line.split()
                if len(w) >= 6 and w[0] == "n":
                    n = int(w[1])
                    for s, v in ((w[2], int(w[3])), (w[4], int(w[5]))):
                        if pub[s][n] != v:
                            bad("saved indep_check %s(%d) = %d, published %d" % (s, n, v, pub[s][n]))
                        else:
                            k += 1
        print("ok   saved indep_check outputs: %d terms" % k)
    elif mode == "fresh":
        k = 0
        for line in open(sys.argv[2]):
            w = line.split()
            if len(w) != 4:
                continue
            s, n, prog, v = w[0], int(w[1]), w[2], w[3]
            if not v.isdigit() or pub[s].get(n) != int(v):
                bad("fresh %s %s(%d) = %s, published %s" % (prog, s, n, v, pub[s].get(n)))
            else:
                k += 1
        if k == 0:
            bad("no fresh results")
        print("ok   %d fresh values equal the published terms" % k)
    else:
        bad("unknown mode " + mode)
    if BAD:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # any parse failure is a failure
        print("BAD  %s: %s" % (type(e).__name__, e))
        sys.exit(1)
