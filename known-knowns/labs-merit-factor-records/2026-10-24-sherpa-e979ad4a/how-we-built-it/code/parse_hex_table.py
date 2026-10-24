"""Parse 'L & F & HEX ...' LaTeX table rows; decode HEX under each padding convention; keep the one whose
exact integer energy reproduces the printed F (rounded to the printed decimals)."""
import re, json, sys
def energy(bits):
    s = [1 if b == '1' else -1 for b in bits]; L = len(s); E = 0
    for k in range(1, L):
        c = sum(s[i] * s[i + k] for i in range(L - k)); E += c * c
    return E
def decode_variants(hx, L):
    nib = ''.join(f'{int(c,16):04b}' for c in hx)
    v = {}
    iv = bin(int(hx, 16))[2:]
    if len(iv) <= L: v['int_leftpad'] = iv.zfill(L)
    if len(nib) >= L: v['nibble_keep_last'] = nib[len(nib)-L:]; v['nibble_keep_first'] = nib[:L]
    return v
src, out, label = sys.argv[1], sys.argv[2], sys.argv[3]
rows = [(a, b, c.replace(' ', '')) for a, b, c in re.findall(r'^\s*(\d{2,4})\s*&\s*([0-9.]+)[^&]*&\s*([0-9A-Fa-f][0-9A-Fa-f ]*[0-9A-Fa-f])\s*(?:&|\\\\)', open(src).read(), re.M)]
res, bad = [], []
for Ls, Fs, hx in rows:
    L = int(Ls); dec = len(Fs.split('.')[1]) if '.' in Fs else 0; ok = None
    for name, bits in decode_variants(hx, L).items():
        E = energy(bits)
        if round(L*L/(2*E), dec) == round(float(Fs), dec): ok = (name, bits, E); break
    if ok: res.append(dict(L=L, E=ok[2], F_printed=Fs, encoding=ok[0], bits=ok[1], source=label))
    else: bad.append((L, Fs))
json.dump(res, open(out, 'w'), indent=0)
print(f"{label}: rows {len(rows)} verified {len(res)} failed {len(bad)} {bad[:10]}")
print(' '.join(f"{r['L']}:{r['E']}" for r in res))
