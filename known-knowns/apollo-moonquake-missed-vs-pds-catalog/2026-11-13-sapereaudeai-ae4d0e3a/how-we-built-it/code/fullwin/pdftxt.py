"""Crude PDF text dump: FlateDecode streams, then literal strings from text operators.
Usage: python -I pdftxt.py <file.pdf> [max_chars]"""
import sys, re, zlib

BS = chr(92)  # backslash
raw = open(sys.argv[1], 'rb').read()
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
out = []
for m in re.finditer(b'stream\r?\n', raw):
    s = m.end()
    e = raw.find(b'endstream', s)
    if e < 0:
        continue
    try:
        d = zlib.decompress(raw[s:e])
    except Exception:
        continue
    if b'Tj' not in d and b'TJ' not in d:
        continue
    txt = []
    depth = 0
    cur = []
    i = 0
    while i < len(d):
        ch = d[i:i + 1]
        if ch == BS.encode() and depth:
            cur.append(d[i + 1:i + 2].decode('latin-1'))
            i += 2
            continue
        if ch == b'(':
            depth += 1
            if depth == 1:
                cur = []
                i += 1
                continue
        elif ch == b')':
            depth -= 1
            if depth == 0:
                txt.append(''.join(cur))
                i += 1
                continue
        if depth:
            cur.append(ch.decode('latin-1'))
        i += 1
    line = ''.join(txt)
    if line.strip():
        out.append(line)
print(('\n'.join(out))[:limit])
