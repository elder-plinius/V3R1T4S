"""Parse Dimitrov arXiv:2206.12070 record tables -> JSON; verify each witness energy exactly."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
tex = open(src, encoding='utf-8', errors='replace').read()
rows = []
for m in re.finditer(r'^[ \t]*\$(\d+)\$\s*&(.*?)&\s*([0-9a-fA-F][0-9a-fA-F ]*?)\s*&\s*([0-9.]+|-|--|)\s*&\s*([0-9.]+)\s*\\\\', tex, re.M):
    n, cls, hx, old, new = int(m.group(1)), m.group(2).strip(), m.group(3).replace(' ', ''), m.group(4), m.group(5)
    rows.append(dict(L=n, cls=cls, hex=hx, old_F=old, new_F=float(new)))
def energy(bits):
    s = [1 if b == '1' else -1 for b in bits]; L = len(s); E = 0
    for k in range(1, L):
        c = sum(s[i] * s[i + k] for i in range(L - k)); E += c * c
    return E
res, bad = [], []
for r in rows:
    L = r['L']; b = bin(int(r['hex'], 16))[2:]
    if len(b) > L: bad.append((L, 'hex longer than L', len(b))); continue
    variants = {'left_pad': b.zfill(L)}
    hb = ''.join(f'{int(c,16):04b}' for c in r['hex'])          # literal nibbles, then trim/pad on the right
    if len(hb) >= L: variants['right_trim'] = hb[:L]
    E_claim = round(L * L / (2 * r['new_F']))
    hit = None
    for name, bits in variants.items():
        E = energy(bits)
        if E == E_claim: hit = (name, bits, E); break
    if hit is None: bad.append((L, 'no encoding matches claimed F', E_claim)); continue
    res.append(dict(L=L, E=hit[2], F=r['new_F'], old_F=r['old_F'], encoding=hit[0], bits=hit[1], cls=r['cls']))
json.dump(res, open(out, 'w'), indent=0)
print(f"rows parsed {len(rows)}, verified {len(res)}, failed {len(bad)}")
for b_ in bad[:20]: print("FAIL", b_)
Ls = sorted(r['L'] for r in res)
print("lengths:", Ls[0], "..", Ls[-1]); print(' '.join(map(str, Ls)))
