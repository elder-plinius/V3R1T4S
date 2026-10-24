"""Decode the five Table 3 sequences of ERK'2025 (Psenicnik-Boskovic-Brest) from the PDF text; keep each only if its exact
energy reproduces the printed F to 4 decimals. usage: parse_erk2025.py PAPER.pdf OUT.json"""
import sys, re, json
import numpy as np, pypdf
t = '\n'.join(p.extract_text() for p in pypdf.PdfReader(sys.argv[1]).pages)
seg = t[t.index('L Our F Previous F'):t.index('Figure 2: Merit factor values')]
rows = re.findall(r'(\d{3}) (\d\.\d{4}) (\d\.\d{4}) ([0-9a-f]+)\s*\n([0-9a-f]+)\s*\n', seg)
def E(b):
    s = np.array([1 if c == '1' else -1 for c in b], dtype=np.int64); c = np.correlate(s, s, 'full')[len(s):]; return int(np.dot(c, c))
out = []
for L, fn, fo, h1, h2 in rows:
    L = int(L); hx = h1 + h2; nib = ''.join(f'{int(c, 16):04b}' for c in hx)
    for name, b in (('last_L_bits', nib[-L:]), ('int_leftpad', bin(int(hx, 16))[2:].zfill(L))):
        if len(b) == L and abs(L * L / (2 * E(b)) - float(fn)) < 1e-4:          # the paper rounds or truncates to 4 decimals
            out.append(dict(L=L, E=E(b), F_printed=fn, previous_F=fo, encoding=name, bits=b)); break
    else: print('NOT reproduced:', L, fn)
json.dump(out, open(sys.argv[2], 'w'), indent=0)
for r in out: print(r['L'], r['E'], r['F_printed'], r['encoding'])
