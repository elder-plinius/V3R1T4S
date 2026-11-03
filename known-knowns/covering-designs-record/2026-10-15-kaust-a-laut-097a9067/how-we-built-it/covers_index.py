"""Index and extract designs from the LJCR Zenodo covers.json (format: {"C(v,k,t)": [[...],[...]], ...}).
index:   python -I covers_index.py index <covers.json> <index.tsv>      (name, byte offset, byte length, nblocks)
extract: python -I covers_index.py extract <covers.json> <index.tsv> v k t <out.txt>   (1-based blocks, one per line)"""
import sys, re

def build_index(path, out):
    pat = re.compile(rb'^"(C\(\d+,\d+,\d+\))": \[')
    res = []
    cur = None; start = 0; nb = 0
    with open(path, 'rb') as f:
        pos = 0
        for line in f:
            m = pat.match(line)
            if m:
                if cur:
                    res.append((cur, start, pos - start, nb))
                cur = m.group(1).decode(); start = pos; nb = 0
            elif line.lstrip().startswith(b'['):
                nb += 1
            pos += len(line)
        if cur:
            res.append((cur, start, pos - start, nb))
    with open(out, 'w', encoding='utf-8', newline='\n') as g:
        for r in res:
            g.write('%s\t%d\t%d\t%d\n' % r)
    print('cells indexed', len(res))

def extract(path, index, v, k, t, out):
    name = 'C(%d,%d,%d)' % (v, k, t)
    for line in open(index, encoding='utf-8'):
        n, off, ln, nb = line.rstrip('\n').split('\t')
        if n == name:
            with open(path, 'rb') as f:
                f.seek(int(off)); raw = f.read(int(ln)).decode()
            blocks = re.findall(r'\[([\d,\s]+)\]', raw)
            with open(out, 'w', encoding='utf-8', newline='\n') as g:
                for b in blocks:
                    g.write(' '.join(x.strip() for x in b.split(',')) + '\n')
            print(name, 'blocks', len(blocks), '->', out)
            return len(blocks)
    print(name, 'not found'); return 0

if __name__ == '__main__':
    if sys.argv[1] == 'index':
        build_index(sys.argv[2], sys.argv[3])
    else:
        extract(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
