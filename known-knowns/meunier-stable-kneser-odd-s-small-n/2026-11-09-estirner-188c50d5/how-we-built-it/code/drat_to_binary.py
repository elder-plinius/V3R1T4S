"""Convert a text DRAT proof (lemma lines, optional 'd' deletions) to binary DRAT: 'a'/'d' byte, then each literal
as the variable-length unsigned encoding of 2*|lit| + (lit < 0), then a 0 byte. Usage: drat_to_binary.py in out"""
import sys
out = bytearray()
for line in open(sys.argv[1]):
    t = line.split()
    if not t: continue
    if t[0] == 'd': out.append(ord('d')); t = t[1:]
    else: out.append(ord('a'))
    for x in map(int, t):
        if x == 0: break
        u = 2 * abs(x) + (x < 0)
        while u > 127: out.append((u & 127) | 128); u >>= 7
        out.append(u)
    out.append(0)
open(sys.argv[2], 'wb').write(out)
