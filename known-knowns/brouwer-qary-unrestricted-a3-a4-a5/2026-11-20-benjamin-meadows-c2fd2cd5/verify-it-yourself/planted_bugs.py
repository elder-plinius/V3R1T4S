#!/usr/bin/env python3
"""Planted-bug test: the checker must reject damaged copies of the code.

usage: python3 planted_bugs.py OBJECT_FILE q n d claimed_size table_lower_bound table_upper_bound

Builds three damaged copies in a temporary folder and runs check_code.py (next to this script) on each, without the
sha256 argument, so that only the code checks can reject them:
  1. one changed symbol: a pair of words at distance exactly d is found and one symbol of the first word, at a
     position where the two differ, is replaced by the second word's symbol (their distance becomes d - 1);
  2. a duplicated word: the first word is written twice (the claimed size is raised by one to match the line count,
     so only the distinctness check can catch it);
  3. a symbol outside the alphabet: one symbol of the last word is replaced by q.
Each must end in FAIL. Prints PASS on the last line if all three were rejected.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run_checker(path, args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_code.py"), path] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace").strip().splitlines()
    return r.returncode, out[-1] if out else ""


def main(argv):
    path = argv[1]
    q, n, d, claimed, lb, ub = (int(x) for x in argv[2:8])
    lines = open(path).read().splitlines()
    head = [l for l in lines if l.startswith("#")]
    words = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
    pair = None
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            diff = [k for k in range(n) if words[i][k] != words[j][k]]
            if len(diff) == d:
                pair = (i, j, diff[0])
                break
        if pair:
            break
    cases = []
    if pair is None:
        print("no pair at distance exactly %d; cannot plant the changed-symbol bug" % d)
        print("FAIL")
        return 1
    i, j, k = pair
    w = list(words)
    w[i] = w[i][:k] + w[j][k] + w[i][k + 1:]
    cases.append(("one changed symbol (word %d, position %d, %s -> %s)" % (i + 1, k, words[i][k], words[j][k]), w, claimed))
    cases.append(("duplicated word (word 1 written twice)", words + [words[0]], claimed + 1))
    w = list(words)
    w[-1] = str(q) + w[-1][1:]
    cases.append(("symbol %d outside the alphabet (last word, position 0)" % q, w, claimed))
    tmp = tempfile.mkdtemp(prefix="planted_")
    all_rejected = True
    try:
        for idx, (name, ws, size) in enumerate(cases):
            p = os.path.join(tmp, "case%d.txt" % idx)
            with open(p, "w") as f:
                f.write("\n".join(head + ws) + "\n")
            rc, last = run_checker(p, [str(q), str(n), str(d), str(size), str(lb), str(ub)])
            rejected = rc != 0 and last == "FAIL"
            all_rejected = all_rejected and rejected
            print("planted bug: %s -> checker exit %d, last line %s (%s)" % (name, rc, last, "rejected, as required" if rejected else "NOT REJECTED"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("PASS" if all_rejected else "FAIL")
    return 0 if all_rejected else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
