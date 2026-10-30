"""Parse codetables.de's GF(9) range page (Tables.php, one GET, saved in data/) into {(n,k): [lb, ub]}.
Usage: parse_range.py PAGE.html OUT.json"""
import sys, re, json, html
t = open(sys.argv[1], encoding='latin-1').read()
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S | re.I)
res = {}
for r in rows:
    cells = [html.unescape(re.sub(r'<[^>]*>', '', c)).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S | re.I)]
    if not cells or not cells[0].isdigit(): continue
    n = int(cells[0])
    for k, c in enumerate(cells[1:], start=1):
        c = c.replace('\xa0', '').strip()
        m = re.match(r'^(\d+)(?:-(\d+))?', c)
        if m: res[f"{n},{k}"] = [int(m.group(1)), int(m.group(2) or m.group(1))]
json.dump(res, open(sys.argv[2], 'w'), indent=0)
print(len(res), "cells;", "(31,18) =", res.get("31,18"), "(32,18) =", res.get("32,18"), "(28,14) =", res.get("28,14"))
