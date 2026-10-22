"""Run tmcrit for n = n_from..n_to on one lattice and mode; append one result line per n to the output file.

usage: python run_series.py <lattice> <site|bond> <n_from> <n_to> <outfile> [exe]
exe: tmcrit.exe (default) or tmcrit_stream.exe (bit-identical roots, transitions streamed from disk through the
folder ../scratch; run 2026-10-16-1714, test_stream.py).
Each line of the output is tmcrit's stdout ("n .. mode .. pc .. bracket .. states_closed .. time ..").
Already finished n (present in outfile) are skipped, so a stopped series resumes where it ended.
Brackets: wide for the first values, then centred on a guess from the last two roots.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep  # noqa: E402

EXE = os.path.join(HERE, "tmcrit.exe")
PROGS = os.path.join(HERE, "..", "progs")


def done_values(outfile):
    vals = {}
    if os.path.exists(outfile):
        for line in open(outfile):
            t = line.split()
            if len(t) > 5 and t[0] == "n":
                vals[int(t[1])] = float(t[t.index("pc") + 1])
    return vals


def main():
    lat, mode, n0, n1, outfile = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    exe = os.path.join(HERE, sys.argv[6]) if len(sys.argv) > 6 else EXE
    extra = []
    if os.path.basename(exe).startswith("tmcrit_stream"):
        scratch = os.path.join(HERE, "..", "scratch")
        os.makedirs(scratch, exist_ok=True)
        extra = ["1e-15", scratch]
    os.makedirs(PROGS, exist_ok=True)
    tagname = "".join(ch for ch in lat if ch.isalnum())
    errfile = outfile + ".stderr"
    for n in range(n0, n1 + 1):
        vals = done_values(outfile)
        if n in vals:
            continue
        prog = sweep.build_program(sweep.LATTICES[lat](), n)
        path = os.path.join(PROGS, "%s_n%d.txt" % (tagname, n))
        sweep.write_program(prog, path)
        brackets = []
        if n - 1 in vals and n - 2 in vals:
            d = vals[n - 1] - vals[n - 2]
            g = vals[n - 1] + d * ((n - 1) / n) ** 5
            w = max(abs(d) * 3, 1e-9)
            brackets.append((g - w, g + w))
        brackets.append((0.05, 0.95))
        ok = False
        for (lo, hi) in brackets:
            t0 = time.time()
            with open(errfile, "a") as ef:
                ef.write("=== %s %s n=%d bracket %.17g %.17g started %s\n" % (
                    lat, mode, n, lo, hi, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
                ef.flush()
                out = subprocess.run([exe, path, mode, repr(lo), repr(hi)] + extra, stdout=subprocess.PIPE, stderr=ef,
                                     text=True)
            if out.returncode == 0 and out.stdout.startswith("n "):
                with open(outfile, "a", newline="\n") as of:
                    of.write(out.stdout.strip() + " wall %.1f\n" % (time.time() - t0))
                ok = True
                break
        if not ok:
            print("failed at n=%d" % n, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
