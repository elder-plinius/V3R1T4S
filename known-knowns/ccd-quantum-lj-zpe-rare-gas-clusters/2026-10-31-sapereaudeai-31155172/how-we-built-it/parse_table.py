"""Parse the Calvo-Doye-Wales LJ+ZPE table (saved HTML) into rows: label, E_LJ, E_Xe, E_Ar, E_Ne, point group.
Usage: python -I parse_table.py <table.html> [out.tsv]"""
import re, sys, html
src = open(sys.argv[1], encoding="latin-1").read()
txt = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
txt = re.sub(r"<[^>]*>", " ", txt)
txt = html.unescape(txt).replace("\xa0", " ")
toks = txt.split()
rows = []
i = 0
num = re.compile(r"^-?\d+\.\d+$")
lab = re.compile(r"^(\d+)([A-Z])$")
while i < len(toks):
    m = lab.match(toks[i])
    if m and i + 4 < len(toks) and all(num.match(t) for t in toks[i+1:i+5]):
        # point group: tokens until next label or non-pg token
        j = i + 5; pg = []
        while j < len(toks) and not lab.match(toks[j]) and len(pg) < 4 and re.match(r"^[A-Za-z0-9]{1,3}$", toks[j]):
            pg.append(toks[j]); j += 1
        rows.append((toks[i], int(m.group(1)), m.group(2), toks[i+1], toks[i+2], toks[i+3], toks[i+4], "".join(pg)))
        i = j
    else:
        i += 1
out = sys.stdout if len(sys.argv) < 3 else open(sys.argv[2], "w")
out.write("label\tN\tletter\tE_LJ\tE_Xe\tE_Ar\tE_Ne\tpg\n")
for r in rows:
    out.write("\t".join(str(x) for x in r) + "\n")
if out is not sys.stdout:
    out.close()
sizes = sorted(set(r[1] for r in rows))
print("rows: %d, sizes: %d" % (len(rows), len(sizes)), file=sys.stderr)
print("sizes: " + " ".join(map(str, sizes)), file=sys.stderr)
