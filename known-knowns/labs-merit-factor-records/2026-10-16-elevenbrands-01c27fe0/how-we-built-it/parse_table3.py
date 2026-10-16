#!/usr/bin/env python3
"""Parse Table 3 of arXiv:2607.09688v1 (text extracted with pypdf) into L, prevF, ourF, hex.
Decoding rule quoted from the paper: hex digit -> 4 bits, remove leading zero-padding to get length L, 0 -> -1.
We take the LAST L bits of the 4*len(hex) bit string (the padding is 4*len(hex)-L leading bits)."""
import re, sys, json
sys.path.insert(0, '.')
from labs_energy import energy, is_skew_symmetric
txt = open(sys.argv[1]).read()
start = txt.index('Table 3: Improved binary sequences'); end = txt.index('Conclusion', start)
lines = txt[start:end].splitlines()
rows = []; cur = None
for ln in lines:
    m = re.match(r'^(\d{3}) (\d\.\d{4}) (\d\.\d{4}) ([0-9a-f]+)$', ln.strip())
    if m:
        cur = dict(L=int(m[1]), prevF=m[2], ourF=m[3], hex=m[4]); rows.append(cur); continue
    if cur and re.fullmatch(r'[0-9a-f]+', ln.strip()) and not re.fullmatch(r'\d{1,2}', ln.strip()):  # skip pypdf page numbers
        cur['hex'] += ln.strip()
    else:
        cur = None
out = []
for r in rows:
    L, h = r['L'], r['hex']; nb = 4 * len(h); pad = nb - L
    bits = bin(int(h, 16))[2:].zfill(nb)
    ok_pad = pad >= 0 and pad < 4 and set(bits[:pad]) <= {'0'}
    s = [1 if b == '1' else -1 for b in bits[pad:]]
    E = energy(s); F = L * L / (2 * E)
    r.update(pad=pad, pad_ok=ok_pad, E=E, F_recomputed='%.4f' % F, F_match=('%.4f' % F) == r['ourF'], skew=is_skew_symmetric(s),
             seq=''.join('+' if x > 0 else '-' for x in s))
    out.append(r)
    print(L, 'pad', pad, ok_pad, 'E', E, 'F', '%.4f' % F, 'paperF', r['ourF'], 'match', r['F_match'], 'skew', r['skew'])
json.dump(out, open('table3_records.json', 'w'), indent=0)
print('rows', len(out), 'all_match', all(r['F_match'] and r['pad_ok'] for r in out))
