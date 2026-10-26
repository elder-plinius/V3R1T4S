#!/usr/bin/env python3
"""Checker for bank target dna-codes-gc-king-table (written from the bank definition).
Usage: check_gc_code.py CODEFILE N D [TABLE_HTML]
Checks: every word has length N over {A,C,G,T}; exactly w = floor(N/2) letters in {G,C}; words distinct;
all-pairs Hamming distance >= D. If TABLE_HTML is given, parses the A_4^GC(n,d,w) table (first table on the
page) and reports the cell value, whether it is marked optimal ('.' or ':'), and whether size > cell.
Exit 0 = code valid (and, with a table, strictly larger than an unmarked cell); exit 1 otherwise."""
import sys, re, html, itertools

def load(path):
    return [l.strip().upper() for l in open(path) if l.strip() and not l.startswith('#')]

def table_cell(path, n, d):
    t = open(path, encoding='latin-1').read()
    a = t.find('GC</sup>(n,d,w)'); b = t.find('GC,RC</sup>(n,d,w)')
    if a < 0: return None, None
    sec = t[a:b if b > a else len(t)]
    for row in re.findall(r'<tr>(.*?)</tr>', sec, re.S):
        cells = re.findall(r'<td>(.*?)</td>', row, re.S)
        cells = [html.unescape(re.sub(r'<[^>]*>', '', re.sub(r'<sup>.*?</sup>', '', c, flags=re.S))).strip() for c in cells]
        if cells and cells[0] == str(n):
            if d - 2 >= len(cells): return None, None
            raw = cells[d - 2]
            m = re.match(r'(\d+)\s*([.:]?)', raw)
            return (int(m.group(1)), m.group(2)) if m else (None, raw)
    return None, None

def selftest(a):
    """--selftest CODEFILE N D: the object must pass, and a corrupted copy made here (one letter of word 0 changed so its
    GC count breaks, plus word 1 replaced by word 0) must be rejected. Exit 0 only if both hold."""
    import tempfile, os
    code = load(a[0])
    bad = list(code); x = bad[0]; i = 0
    sub = {'A': 'G', 'T': 'C', 'G': 'A', 'C': 'T'}
    bad[0] = sub[x[0]] + x[1:]
    if len(bad) > 1: bad[1] = bad[0]
    fd, tmp = tempfile.mkstemp(suffix='.txt'); os.write(fd, ('\n'.join(bad) + '\n').encode()); os.close(fd)
    r_ok = main([a[0], a[1], a[2]]); r_bad = main([tmp, a[1], a[2]]); os.unlink(tmp)
    print('SELFTEST: original_exit=%d corrupted_exit=%d -> %s' % (r_ok, r_bad, 'PASS' if (r_ok == 0 and r_bad == 1) else 'FAIL'))
    return 0 if (r_ok == 0 and r_bad == 1) else 1

def main(a):
    if a and a[0] == '--selftest': return selftest(a[1:])
    code, n, d = load(a[0]), int(a[1]), int(a[2])
    w, ok, errs = n // 2, True, []
    for i, x in enumerate(code):
        if len(x) != n: errs.append('word %d length %d != %d' % (i, len(x), n))
        if set(x) - set('ACGT'): errs.append('word %d has letters outside ACGT' % i)
        if sum(c in 'GC' for c in x) != w: errs.append('word %d GC count %d != %d' % (i, sum(c in 'GC' for c in x), w))
    if len(set(code)) != len(code): errs.append('duplicate words: %d' % (len(code) - len(set(code))))
    mind = n + 1
    for x, y in itertools.combinations(code, 2):
        if len(x) == len(y):
            mind = min(mind, sum(p != q for p, q in zip(x, y)))
    if mind < d: errs.append('minimum Hamming distance %d < %d' % (mind, d))
    print('n=%d d=%d w=%d size=%d min_distance=%s' % (n, d, w, len(code), mind if len(code) > 1 else 'n/a'))
    for e in errs[:10]: print('ERROR:', e)
    if errs:
        print('VERDICT: INVALID'); return 1
    if len(a) > 3:
        val, mark = table_cell(a[3], n, d)
        print('table cell A4GC(%d,%d,%d) = %s marker=%r' % (n, d, w, val, mark))
        if val is None: print('VERDICT: VALID, table cell unreadable'); return 1
        if mark: print('VERDICT: VALID, cell already proven optimal; beats=%s' % (len(code) > val)); return 1
        beats = len(code) > val
        print('VERDICT: VALID, beats_table=%s' % beats); return 0 if beats else 1
    print('VERDICT: VALID'); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
