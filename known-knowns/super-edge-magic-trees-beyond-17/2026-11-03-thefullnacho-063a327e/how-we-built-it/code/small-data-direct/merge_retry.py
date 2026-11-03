import sys
# merge_retry.py cert retry > merged : replace UNLABELED lines of cert by labelled lines (same n;edges) from retry
cert, retry = sys.argv[1], sys.argv[2]
fix = {}
for l in open(retry):
    p = l.rstrip("\n").split(";")
    if p[2]: fix[p[0] + ";" + p[1]] = l
for l in open(cert):
    p = l.rstrip("\n").split(";")
    k = p[0] + ";" + p[1]
    sys.stdout.write(fix[k] if (not p[2] and k in fix) else l)
