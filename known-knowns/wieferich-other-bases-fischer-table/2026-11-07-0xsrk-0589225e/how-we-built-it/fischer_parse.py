"""V3R1T4S — parse Fischer's FermQ_Sorg.txt (fermatquotient.com, latin-1 German text).

Rows look like '   23,  13, 2481757, 13703077, ...'; an entry like '7^3' means the prime 7 (higher power of p
divides).  A line whose first number is not the next base (> previous base, <= 10125) is treated as a continuation.
Also returns the stated limit ('Die Basen sind gegenwaertig durchsucht bis 4.8E+12') and the recent-finds tail
('Basis: X  P: Y' / 'Primbasis: X  P: Y').
Usage: python fischer_parse.py FermQ_Sorg.txt   -> one JSON summary line
"""
import re, json, sys


def parse(path):
    txt = open(path, "rb").read().decode("latin-1").replace("\r", "")
    limit = None
    m = re.search(r"durchsucht bis\s+([0-9.]+E\+?\d+)", txt)
    if m:
        limit = float(m.group(1))
    rows, tail, prev, in_table = {}, [], 1, False
    for ln in txt.split("\n"):
        if ln.strip().startswith("Basis, Primzahlen"):
            in_table = True
            continue
        mm = re.match(r"^\s*(?:Basis|Primbasis):\s*(\d+)\s+P:\s*(\d+)", ln)
        if mm:
            tail.append((int(mm.group(1)), int(mm.group(2))))
            continue
        if not in_table:
            continue
        m2 = re.match(r"^\s*(\d+),(.*)$", ln)
        if not m2:
            if ln.strip() and rows:
                in_table = False
            continue
        first, rest = int(m2.group(1)), m2.group(2)
        if prev < first <= 10125 and first not in rows:
            base, entries = first, rest
            rows[base], prev = [], first
        else:
            base, entries = prev, m2.group(1) + "," + rest
        for e in entries.split(","):
            e = e.strip().split("^")[0]
            if e.isdigit():
                rows[base].append(int(e))
    return limit, rows, tail


if __name__ == "__main__":
    limit, rows, tail = parse(sys.argv[1])
    pairs = [(b, p) for b, ps in rows.items() for p in ps]
    print(json.dumps({"limit": limit, "n_bases": len(rows), "n_pairs": len(pairs), "min_base": min(rows),
                      "max_base": max(rows), "max_p": max(p for _, p in pairs), "tail_entries": len(tail)}))
