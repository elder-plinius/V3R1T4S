import sys
# assemble.py trees_file alpha1 alpha2 ... : print one line per tree from the first file that labels it,
# else "n;edges;;RESIDUE" (to be labelled by direct search). Also prints stats to stderr.
trees = sys.argv[1]; srcs = sys.argv[2:]; got = {}; from_src = [0]*len(srcs)
for i, f in enumerate(srcs):
    for l in open(f):
        p = l.rstrip("\n").split(";")
        if len(p) >= 3 and p[2]:
            k = p[0] + ";" + p[1]
            if k not in got: got[k] = (i, l)
res = 0
for l in open(trees):
    k = l.rstrip("\n")
    if k in got: from_src[got[k][0]] += 1; sys.stdout.write(got[k][1])
    else: res += 1; sys.stdout.write(k + ";;RESIDUE\n")
sys.stderr.write("labelled per source %s residue %d\n" % (from_src, res))
