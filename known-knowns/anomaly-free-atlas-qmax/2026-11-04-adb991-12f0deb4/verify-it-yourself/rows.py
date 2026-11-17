#!/usr/bin/env python3
"""Read object/counts.txt of a census package, check that it is internally consistent, and print one normalised
line per row for run_checks.sh:

    content q_max count lines sha256 listers independent_count shipped_file

listers is a comma-separated list of the listers that the file says produced exactly this sha256;
independent_count is the count the file records for the no-list counters ("-" if the file records none);
shipped_file is the path of a list stored in the package ("-" if none).

Usage: rows.py COUNTS_FILE ROW [ROW ...]   where ROW is CONTENT:QMAX, e.g. SM:11 SMnuR:11.
The rows named on the command line are the claim; the file must hold exactly those rows.
Checks: count = lines + 1 (the all-zero assignment is counted, not listed), sha256 is 64 lowercase hex digits,
content is SM or SMnuR, 1 <= Q_max <= 40, no duplicate row, and the recorded independent count (if any) equals
the count. Standard library only. Exit status 0 when all hold, 1 otherwise."""
import os
import re
import sys

HEX = re.compile(r"^[0-9a-f]{64}$")
NUM = re.compile(r"^[0-9]+$")


def die(msg):
    print("counts file: %s" % msg)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        die("usage: rows.py COUNTS_FILE CONTENT:QMAX ...")
    path, want = sys.argv[1], sys.argv[2:]
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    headers, rows = [], []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            body = s.lstrip("#").strip()
            if body.startswith("columns:"):
                headers.append(body[len("columns:"):].strip())
            continue
        tok = s.split(None, 7)
        if tok[0] == "content":
            headers.append(s)
            continue
        rows.append((s, tok))
    htext = " ".join(headers)
    if not headers:
        fmt = "D"            # no header (claim of run 2026-11-03-0919): content Q_max count lines sha256 lister[(note)] checklist:PASS mitm.c:<count> [count.c:<count>(note)]
    elif "list_file" in htext:
        fmt = "A"            # content Q_max count lines sha256 list_file
    elif "lister_acclist" in htext:
        fmt = "B"            # content Q_max count lines sha256 lister_acclist lister_csenum independent_count
    elif "independent_counters" in htext:
        fmt = "C"            # content Q_max count lines sha256 lister checker independent_counters
    else:
        die("unknown column layout: %s" % htext)
    seen, out = set(), []
    for s, tok in rows:
        if len(tok) < 5:
            die("short row: %s" % s)
        content, q, count, nlines, sha = tok[:5]
        if content not in ("SM", "SMnuR"):
            die("unknown content %r" % content)
        for name, v in (("Q_max", q), ("count", count), ("lines", nlines)):
            if not NUM.match(v):
                die("%s %r is not a decimal integer in row: %s" % (name, v, s))
        q, count, nlines = int(q), int(count), int(nlines)
        if not 1 <= q <= 40:
            die("Q_max %d out of range" % q)
        if count != nlines + 1:
            die("%s Q_max %d: count %d is not lines %d + 1" % (content, q, count, nlines))
        if not HEX.match(sha):
            die("%s Q_max %d: %r is not a sha256" % (content, q, sha))
        key = "%s:%d" % (content, q)
        if key in seen:
            die("duplicate row %s" % key)
        seen.add(key)
        listers, indep, shipped = [], "-", "-"
        if fmt == "A":
            rest = s.split(None, 5)[5] if len(s.split(None, 5)) > 5 else ""
            listers = ["acclist"]
            if rest.startswith("object/"):
                shipped = rest.split()[0]
                if not os.path.isfile(shipped):
                    die("%s: the list file %s named in the row is not in the package" % (key, shipped))
        elif fmt == "B":
            t = s.split()
            if len(t) != 8:
                die("row %s has %d fields, expected 8" % (key, len(t)))
            for name, v in (("acclist", t[5]), ("csenum", t[6])):
                if v == "same":
                    listers.append(name)
                elif v != "-":
                    die("%s: lister column %s is %r (expected 'same' or '-')" % (key, name, v))
            m = re.match(r"^([0-9]+)\(ok\)$", t[7])
            if not m:
                die("%s: independent_count %r is not of the form <count>(ok)" % (key, t[7]))
            indep = m.group(1)
        elif fmt == "D":
            t = s.split()
            m = re.match(r"^([a-z0-9]+)", t[5]) if len(t) > 5 else None
            if not m:
                die("%s: lister %r" % (key, t[5] if len(t) > 5 else ""))
            listers = [m.group(1)]
            if "checklist:PASS" not in t:
                die("%s: no checklist:PASS field" % key)
            mm = [x for x in t if x.startswith("mitm.c:")]
            if len(mm) != 1 or not re.match(r"^mitm\.c:([0-9]+)$", mm[0]):
                die("%s: no single mitm.c:<count> field" % key)
            indep = mm[0].split(":")[1]
            for x in t[6:]:   # every other recorded counter value (e.g. count.c:<n>(note)) must also equal the count
                mc = re.match(r"^([a-z0-9.]+):([0-9]+)", x)
                if mc and mc.group(1) != "checklist" and int(mc.group(2)) != count:
                    die("%s: recorded %s count %s differs from count %d" % (key, mc.group(1), mc.group(2), count))
        else:
            t = s.split()
            if len(t) != 8:
                die("row %s has %d fields, expected 8" % (key, len(t)))
            if not re.match(r"^[a-z0-9]+$", t[5]):
                die("%s: lister %r" % (key, t[5]))
            listers = [t[5]]
            if t[6] != "checklist:PASS":
                die("%s: checker column %r" % (key, t[6]))
            m = re.match(r"^[^:]+:([0-9]+)$", t[7])
            if not m:
                die("%s: independent_counters %r does not end in :<count>" % (key, t[7]))
            indep = m.group(1)
        if indep != "-" and int(indep) != count:
            die("%s: recorded independent count %s differs from count %d" % (key, indep, count))
        if not listers:
            die("%s: no lister recorded" % key)
        out.append("%s %d %d %d %s %s %s %s" % (content, q, count, nlines, sha, ",".join(listers), indep, shipped))
    if sorted(seen) != sorted(set(want)) or len(want) != len(set(want)):
        die("rows in file (%s) differ from the claimed rows (%s)" % (" ".join(sorted(seen)), " ".join(sorted(want))))
    order = {k: i for i, k in enumerate(want)}
    out.sort(key=lambda r: order["%s:%s" % tuple(r.split()[:2])])
    print("\n".join(out))


if __name__ == "__main__":
    main()
