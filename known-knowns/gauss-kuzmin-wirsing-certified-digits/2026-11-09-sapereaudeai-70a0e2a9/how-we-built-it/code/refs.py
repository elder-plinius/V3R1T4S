"""Build reference digit strings (decimals after '0.') from the fetched files; run with python -I.
usage: refs.py data_dir out.json"""
import sys, re, json, hashlib, os
d = sys.argv[1]
b = open(os.path.join(d, 'b038517.txt'), encoding='ascii').read().split('\n')
pairs = [l.split() for l in b if len(l.split()) == 2]
assert [int(p[0]) for p in pairs] == list(range(len(pairs)))
oeis = ''.join(p[1] for p in pairs)          # offset 0: C = 0.3036...
md = open(os.path.join(d, '83a.md'), encoding='utf-8').read()
i = md.index('The full 175-digit center value')
seg = md[i:i + 600]
groups = re.findall(r'\d+', seg.split('-0.')[1].split('with')[0])
nis = ''.join(groups)
out = {"oeis_b038517_digits": oeis, "n_oeis": len(oeis), "nisoli_centre_digits": nis, "n_nisoli": len(nis)}
bt = os.path.join(d, 'wirsing.txt') if os.path.exists(os.path.join(d, 'wirsing.txt')) else os.path.join(d, '..', 'work', 'wirsing.txt')
if os.path.exists(bt):
    t = open(bt, encoding='latin-1').read()
    for tag in ('Result 1', 'Result 2'):
        s = t[t.index(tag):]
        s = s[s.index('-0.') + 3:]
        s = s[:s.index('This value')]
        out['briggs_' + tag.replace(' ', '')] = ''.join(re.findall(r'\d', s))
json.dump(out, open(sys.argv[2], 'w'), indent=1)
for k, v in out.items():
    if isinstance(v, str): print(k, len(v), v[:20], '...', v[-10:])
