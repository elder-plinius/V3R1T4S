"""Regression net: tmcrit_stream.exe must print the same root, bracket and state counts as the frozen tmcrit.exe.

Runs both on the same sweep programs and brackets (site and bond, several lattices and n) and compares every field
of the result line except the run time. The streamed version keeps the arithmetic order, so equality is exact.

usage: python test_stream.py <scratch folder>
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep  # noqa: E402

CASES = [("square", "site", 6), ("square", "site", 8), ("square", "bond", 6), ("kagome", "bond", 4),
         ("(3,12^2)", "site", 3), ("honeycomb", "bond", 4), ("triangular", "site", 5),
         ("(3^3,4^2)", "site", 9), ("(3^3,4^2)", "bond", 8), ("#23", "site", 9), ("#23", "bond", 7),
         ("#20", "site", 8), ("#21", "bond", 6), ("#22", "site", 8), ("#15", "site", 6)]


def fields(line):
    t = line.split()
    d = dict(zip(t[0::2], t[1::2]))
    d.pop("time", None)
    return d


def main():
    scratch = sys.argv[1]
    os.makedirs(scratch, exist_ok=True)
    fails = 0
    for (name, mode, n) in CASES:
        prog = sweep.build_program(sweep.LATTICES[name](), n)
        path = os.path.join(scratch, "%s_n%d.txt" % ("".join(c for c in name if c.isalnum()), n))
        sweep.write_program(prog, path)
        out = []
        for exe in ("tmcrit.exe", "tmcrit_stream.exe"):
            args = [os.path.join(HERE, exe), path, mode, "0.05", "0.95"]
            if exe == "tmcrit_stream.exe":
                args += ["1e-15", scratch]
            r = subprocess.run(args, capture_output=True, text=True)
            out.append(r.stdout.strip() if r.returncode == 0 else "exit %d: %s" % (r.returncode, r.stderr[-200:]))
        same = out[0].startswith("n ") and fields(out[0]) == fields(out[1])
        fails += not same
        print("%-4s %-10s %s n=%-2d  %s%s" % ("ok" if same else "FAIL", name, mode, n, out[0][:95],
                                           "" if same else "\n     stream: " + out[1][:95]))
    left = [f for f in os.listdir(scratch) if f.startswith("tmcrit_stream_")]
    print("scratch files left behind: %d" % len(left))
    print("TMCRIT_STREAM REGRESSION: %s (%d failures of %d cases)" % ("PASS" if fails == 0 and not left else "FAIL", fails, len(CASES)))
    return 1 if fails or left else 0


if __name__ == "__main__":
    sys.exit(main())
