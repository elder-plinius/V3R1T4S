"""Notes clause evidence for 663 #523. Usage: python3 notes_check.py <data_dir>
Images: mirror (L<->R) x all 120 permutations of states B..F (A stays the start state). Searches the fetched
Holdouts_lists page, BB(6) page and both annotated-sheet CSVs; lists 663-file relatives within 2 differing
transitions together with their sheet rows."""
import sys, os, itertools, csv, hashlib
M = "1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB"
S = "ABCDEF"
def parse(m):
    return [[m[i*7+b*3:i*7+b*3+3] for b in (0,1)] for i in range(6)]
def fmt(t): return "_".join(t[i][0]+t[i][1] for i in range(6))
def image(m, perm, mirror):
    t = parse(m); inv = {old: new for old, new in zip(S, perm)}
    out = [None]*6
    for i, row in enumerate(t):
        nr = []
        for c in row:
            if c == "---": nr.append(c); continue
            d = c[1]
            if mirror: d = {"L": "R", "R": "L"}[d]
            nr.append(c[0] + d + inv[c[2]])
        out[S.index(inv[S[i]])] = nr
    return fmt(out)
imgs = set()
for p in itertools.permutations("BCDEF"):
    for mir in (0, 1):
        imgs.add(image(M, "A" + "".join(p), mir))
assert image(M, "ABCDEF", 0) == M
print("images:", len(imgs), "(including the machine itself)")
d = sys.argv[1]
files = ["holdouts_lists.html", "notes/bb6_page.html", "notes/sheet_gid1330361301.csv", "notes/sheet_gid806905077.csv", "notes/sheet_4319.csv",
         "BB6_holdouts_663.txt"]
for f in files:
    p = os.path.join(d, f); txt = open(p, encoding="utf-8", errors="replace").read()
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    hits = []
    for im in sorted(imgs):
        i = txt.find(im)
        while i >= 0:
            line = txt.count("\n", 0, i) + 1
            hits.append((im, line)); i = txt.find(im, i + 1)
    print(f"{f} sha256={h} hits={len(hits)}")
    for im, line in hits:
        print(f"   {'SELF ' if im == M else 'IMAGE'} {im} at line {line}")
# sheet row for the machine
rows = list(csv.reader(open(os.path.join(d, "notes/sheet_gid1330361301.csv"), encoding="utf-8")))
hdr = rows[0]; print("sheet header:", hdr)
sheet = {r[0]: r for r in rows[1:] if r}
r = sheet.get(M); print("sheet row for machine:", r)
print("notes_empty:", r is not None and r[3].strip() == "" and r[4].strip() == "" and r[1].strip() == "")
# relatives in the 663 list
L = [l.strip() for l in open(os.path.join(d, "BB6_holdouts_663.txt")) if l.strip()]
base = parse(M)
def dist(a, b):
    ta, tb = parse(a), parse(b)
    return sum(ta[i][j] != tb[i][j] for i in range(6) for j in (0, 1))
rel = []
for n, m in enumerate(L, 1):
    best = min(dist(im, m) for im in imgs)
    if 0 < best <= 2 or (best == 0 and m != M): rel.append((best, n, m))
print("relatives within 2 transitions (up to equivalence):", len(rel))
for best, n, m in sorted(rel):
    sr = sheet.get(m)
    print(f"   dist={best} line={n} {m} sheet={sr[1:] if sr else 'NOT IN SHEET'}")
