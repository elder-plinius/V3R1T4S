#!/usr/bin/env python3
"""Planted-bug test: the checker must reject damaged copies of the code.

usage: python3 planted_bugs.py CODE_FILE n d w claimed_size table_lower_bound table_upper_bound

Builds damaged copies in a temporary folder and runs check_cw.py (next to this script) on each, without the
sha256 argument, so that only the code checks can reject them:
  1. a pair moved too close: a pair of words at distance exactly d is found, and in the first word one 1 is moved
     to a position where the second word has its 1 (weight stays w, the pair's distance becomes d - 2);
  2. a changed weight: one 0 of the first word is turned into a 1;
  3. a duplicated word: the first word replaces the last one (the size stays the same, so only the
     distinctness check can catch it).
Each must end in FAIL. Prints PASS on the last line if all were rejected.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run_checker(path, args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_cw.py"), path] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace").strip().splitlines()
    return r.returncode, out[-1] if out else ""


def main(argv):
    path = argv[1]
    n, d, w, claimed, lb, ub = (int(x) for x in argv[2:8])
    lines = open(path).read().splitlines()
    head = [l for l in lines if l.startswith("#")]
    words = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
    pair = None
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if sum(a != b for a, b in zip(words[i], words[j])) == d:
                pair = (i, j)
                break
        if pair:
            break
    if pair is None:
        print("no pair at distance exactly %d; cannot plant the first bug" % d)
        print("FAIL")
        return 1
    i, j = pair
    a, b = words[i], words[j]
    p = next(k for k in range(n) if a[k] == "1" and b[k] == "0")
    q = next(k for k in range(n) if a[k] == "0" and b[k] == "1")
    x = list(a)
    x[p], x[q] = "0", "1"
    cases = []
    ws = list(words)
    ws[i] = "".join(x)
    cases.append(("pair moved too close (word %d: 1 moved from position %d to %d)" % (i + 1, p, q), ws))
    ws = list(words)
    z = ws[0].index("0")
    ws[0] = ws[0][:z] + "1" + ws[0][z + 1:]
    cases.append(("changed weight (word 1, position %d, 0 -> 1)" % z, ws))
    ws = list(words)
    ws[-1] = ws[0]
    cases.append(("duplicated word (word 1 written over the last word)", ws))
    tmp = tempfile.mkdtemp(prefix="planted_")
    all_rejected = True
    try:
        for k, (label, ws) in enumerate(cases):
            f = os.path.join(tmp, "case%d.txt" % k)
            with open(f, "w") as fh:
                fh.write("\n".join(head + ws) + "\n")
            rc, last = run_checker(f, [str(v) for v in (n, d, w, claimed, lb, ub)])
            rejected = rc != 0 and last == "FAIL"
            all_rejected &= rejected
            print("planted bug: %s -> checker exit %d, last line %s (%s)" % (label, rc, last, "rejected, as required" if rejected else "NOT rejected"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("PASS" if all_rejected else "FAIL")
    return 0 if all_rejected else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
