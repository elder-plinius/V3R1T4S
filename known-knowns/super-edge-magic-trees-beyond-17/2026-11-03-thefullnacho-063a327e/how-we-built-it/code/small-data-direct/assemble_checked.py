import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../checker"))
from check_sem import check
# assemble_checked.py trees_file src1 src2 ... : one line per tree from the first source whose labeling passes check_sem
# (guards against a truncated last line from a stopped job); otherwise "n;edges;;RESIDUE". Stats on stderr.
trees = sys.argv[1]; srcs = sys.argv[2:]; got = {}; from_src = [0]*len(srcs)
for i, f in enumerate(srcs):
    for l in open(f):
        if not l.endswith("\n"): continue
        p = l.rstrip("\n").split(";")
        if len(p) < 3 or not p[2]: continue
        k = p[0] + ";" + p[1]
        if k in got: continue
        try:
            n = int(p[0]); es = [tuple(map(int, x.split("-"))) for x in p[1].split(",")]; ls = list(map(int, p[2].split(",")))
            if check(n, es, ls)[0]: got[k] = (i, l)
        except Exception: pass
res = 0
for l in open(trees):
    k = l.rstrip("\n")
    if k in got: from_src[got[k][0]] += 1; sys.stdout.write(got[k][1])
    else: res += 1; sys.stdout.write(k + ";;RESIDUE\n")
sys.stderr.write("labelled per source %s residue %d\n" % (from_src, res))
