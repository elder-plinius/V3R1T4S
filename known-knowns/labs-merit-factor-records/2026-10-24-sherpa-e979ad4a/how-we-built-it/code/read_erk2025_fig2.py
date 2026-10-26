"""Read Figure 2 of Psenicnik-Boskovic-Brest, ERK'2025 ("Integer Partitions and the Merit Factor Problem") from the
PDF's vector data. Each length L has a vertical segment from the previous best F (Dimitrov) up to the new F.
x and y are calibrated by least squares on the five lengths whose values Table 3 prints (both endpoints), then every
segment is converted to (L, F_old, F_new), and F_new to the nearest integer energy round(L^2 / (2 F)).
usage: read_erk2025_fig2.py PAPER.pdf OUT.json"""
import sys, re, json
import numpy as np, pypdf
pdf, out = sys.argv[1], sys.argv[2]
r = pypdf.PdfReader(pdf)
form = None
for p in r.pages:
    xo = p.get('/Resources', {}).get('/XObject', {})
    for k in xo:
        o = xo[k].get_object()
        if o.get('/Subtype') == '/Form' and float(o['/BBox'][2]) < 500 and len(o.get_data()) > 5000: form = o
s = form.get_data().decode('latin-1').splitlines()
seg = []
for i in range(len(s) - 1):
    a = re.fullmatch(r'(-?[\d.]+) (-?[\d.]+) m', s[i].strip()); b = re.fullmatch(r'(-?[\d.]+) (-?[\d.]+) l', s[i + 1].strip())
    if a and b and abs(float(a[1]) - float(b[1])) < 1e-6 and abs(float(a[2]) - float(b[2])) > 1e-3:
        x = float(a[1]); y0, y1 = sorted((float(a[2]), float(b[2]))); seg.append((x, y0, y1))
seg = sorted(set(seg))
xs = np.array([q[0] for q in seg]); dx = np.diff(xs)
print('vertical segments:', len(seg), '| x spacing min/median/max', dx.min().round(6), np.median(dx).round(6), dx.max().round(6))
table = {405: (7.0908, 7.5199), 422: (7.0584, 7.5981), 433: (7.0548, 7.8016), 441: (7.2546, 7.4823), 450: (7.0152, 7.3577)}
step = np.median(dx)
best = None
for L0 in range(380, 421):                       # which L the first segment is
    Ls = np.rint((xs - xs[0]) / step).astype(int) + L0
    if not all(L in Ls for L in table): continue
    Y, F = [], []
    for L, (fo, fn) in table.items():
        k = int(np.where(Ls == L)[0][0]); Y += [seg[k][1], seg[k][2]]; F += [fo, fn]
    A = np.vstack([F, np.ones(len(F))]).T; coef, res, *_ = np.linalg.lstsq(A, np.array(Y), rcond=None)
    rr = float(np.max(np.abs(A @ coef - np.array(Y))))
    if best is None or rr < best[0]: best = (rr, L0, coef, Ls)
rr, L0, (a, b), Ls = best
print(f'first segment is L = {L0}; y = {a:.6f} F + {b:.6f}; max calibration residual {rr:.3e} pt over the 10 table endpoints')
rows = []
for (x, y0, y1), L in zip(seg, Ls):
    if not 400 <= L <= 450: continue                 # the figure's stated range; outside it the segments are axis lines
    fo, fn = (y0 - b) / a, (y1 - b) / a
    rows.append(dict(L=int(L), F_old=round(fo, 5), F_new=round(fn, 5), E_new_nearest=int(round(L * L / (2 * fn))), E_old_nearest=int(round(L * L / (2 * fo)))))
json.dump(dict(source=pdf.split('/')[-1], calibration=dict(a=a, b=b, max_residual_pt=rr), rows=rows), open(out, 'w'), indent=1)
for q in rows:
    if q['L'] in (400, 401, 403, 405, 449): print(q)
print('lengths read:', rows[0]['L'], '..', rows[-1]['L'], '(', len(rows), ')')
