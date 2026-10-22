#!/usr/bin/env python3
"""Write a package object file (columns family, COGID, language, prediction) from official-format result files
<dir>/<fam>/result-<P>.tsv, families in the fixed order, rows in file order. Main session, run 2026-10-18-0202.
usage: python3 -I make_object.py RESULT_DIR P OUT"""
import sys, os
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
d, p, out = sys.argv[1:4]
lines = ["family\tCOGID\tlanguage\tprediction\n"]
for f in FAMS:
    rows = open(os.path.join(d, f, "result-%s.tsv" % p), encoding="utf-8").read().split("\n")
    head = rows[0].split("\t")
    for r in rows[1:]:
        if not r.strip():
            continue
        c = r.split("\t")
        filled = [(head[i], c[i]) for i in range(1, len(c)) if c[i].strip()]
        assert len(filled) == 1, (f, c[0], filled)
        lines.append("%s\t%s\t%s\t%s\n" % (f, c[0], filled[0][0], filled[0][1]))
open(out, "w", encoding="utf-8").write("".join(lines))
print(len(lines) - 1, "rows")
