"""Parse Andw.html into {(n,d,w): cell text}. Usage: python3 -I andw_cells.py Andw.html n,d,w ..."""
import re, sys, html
s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
cells = {}
for m in re.finditer(r'<table border="1">(.*?)</table>', s, re.S):
    t = m.group(1)
    pre = s[:m.start()]
    hd = re.findall(r'<h[123]>(.*?)</h[123]>', pre, re.S)[-1]
    rows = re.findall(r'<tr>(.*?)</tr>', t, re.S)
    if not rows:
        continue
    hm = re.search(r'A\(n,(\d+),w\)', hd)
    hm2 = re.search(r'A\(n,(\d+),(\d+)\)', hd)
    head = [re.sub('<.*?>', '', c).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', rows[0], re.S)]
    if hm2 and not hm:
        D, W = int(hm2.group(1)), int(hm2.group(2))
        prev = None
        for r in rows:
            cs = [html.unescape(re.sub('<.*?>', '', c)).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]
            if cs and all(c.isdigit() for c in cs):
                prev = [int(c) for c in cs]
            elif prev and len(cs) == len(prev):
                for n, c in zip(prev, cs):
                    cells.setdefault((n, D, W), ('LB:' if 'Lower bounds' in hd else '') + c)
                prev = None
        continue
    for r in rows[1:]:
        cs = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)
        if not cs:
            continue
        n = re.sub('<.*?>', '', cs[0]).strip()
        if not n.isdigit():
            continue
        for j, c in enumerate(cs[1:], 1):
            txt = html.unescape(re.sub('<.*?>', '', c)).strip()
            if hm and j < len(head) and head[j].lstrip('w=').isdigit():
                cells.setdefault((int(n), int(hm.group(1)), int(head[j].lstrip('w='))), txt)
for q in sys.argv[2:]:
    n, d, w = map(int, q.split(','))
    print(q, '|', cells.get((n, d, w)), '| mirror', cells.get((n, d, n - w)))
