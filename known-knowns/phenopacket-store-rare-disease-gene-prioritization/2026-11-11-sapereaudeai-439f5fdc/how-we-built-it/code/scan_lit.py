"""Lens novelty-scan: look for any published few-terms (small-profile) stratification of ranker performance on
phenopacket-store, especially Resnik/Phenomizer vs LIRICAL on 0.1.27. Reads the saved texts in data/lit (copies of
pages fetched once, honestly, in run 2026-11-11-1222) and prints every line that matches a term-count pattern,
with +-2 lines of context and whether the window also names a ranker. Usage: python -I scan_lit.py <lit_dir>"""
import os
import re
import sys

PAT = re.compile(r'(number of (observed |query |patient )?(hpo |phenotype )?(terms|features|phenotypes)|terms per case|'
                 r'per[- ]case term|profile size|query size|few(er)? (hpo )?(terms|phenotypes|features)|'
                 r'(<=|≤|\\leq|at most|up to|fewer than|less than) ?[1-5] (hpo |observed |query )?(terms|phenotypes|features)|'
                 r'[1-5] or fewer (hpo )?(terms|phenotypes)|information[- ]poor|sparse (profile|input|case|phenotype)|'
                 r'by term count|term count|stratif\w* by (the )?(number|count)|10-term cap|over the cap|under it)', re.I)
RANK = re.compile(r'(resnik|phenomizer|lirical|exomiser|phen2gene|phrank)', re.I)


def main(d):
    total = 0
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.html'):
            continue  # the .txt copy of the same page is scanned instead
        lines = open(os.path.join(d, fn), encoding='utf-8', errors='replace').read().splitlines()
        hits = [i for i, l in enumerate(lines) if PAT.search(l)]
        print('=== %s: %d lines, %d term-count hits' % (fn, len(lines), len(hits)))
        for i in hits:
            win = ' '.join(lines[max(0, i - 2): i + 3])
            names = sorted({m.group(1).lower() for m in RANK.finditer(win)})
            print('  L%d [rankers in window: %s] %s' % (i + 1, ','.join(names) or '-', lines[i].strip()[:220]))
        total += len(hits)
    print('TOTAL term-count hits: %d' % total)


if __name__ == '__main__':
    main(sys.argv[1])
