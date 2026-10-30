"""Download the FunSearch 512-cap of F_3^8 (one plain request) and write it as checker/record_512_n8.txt
(one 8-digit vector per line), the input of code/build_n9_frame.py. Run from how-we-built-it/."""
import hashlib, os, re, urllib.request
URL = 'https://raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/n8_size512.txt'
WANT = '8d6df45c3039b6a7ee1aae7216b100c3f4c075179dc6471f4f51b968a26d8905'   # sha256 of the file as fetched 2026-10-24
req = urllib.request.Request(URL, headers={'User-Agent': 'V3R1T4S-reproduction (honest client)'})
raw = urllib.request.urlopen(req, timeout=60).read()
h = hashlib.sha256(raw).hexdigest()
print('sha256', h, 'matches the run' if h == WANT else 'DIFFERS from the run (the file changed upstream)')
rows = [re.sub(r'[^012]', '', l) for l in raw.decode().splitlines()]
rows = [r for r in rows if r]
assert len(rows) == 512 and all(len(r) == 8 for r in rows)
os.makedirs('checker', exist_ok=True)
with open('checker/record_512_n8.txt', 'w') as f:
    f.write('\n'.join(rows) + '\n')
print('wrote checker/record_512_n8.txt', len(rows))
