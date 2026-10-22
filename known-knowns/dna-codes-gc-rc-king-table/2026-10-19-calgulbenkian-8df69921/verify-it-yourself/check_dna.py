"""Standalone DNA-code checker (standard library only).
usage: python3 -I check_dna.py CODEFILE N D MODE
MODE is gc (constant GC content) or gcrc (constant GC content plus reverse-complement constraint).
Conditions checked: every word has length N, alphabet ACGT, words are distinct, exactly floor(N/2) letters
from {C,G} per word, pairwise Hamming distance >= D; for gcrc also Hamming(x, rc(y)) >= D for all ordered
pairs x, y including x = y, where rc reverses the word and swaps A and T swapped, C and G swapped.
The last output line is a JSON record."""
import sys, json

COMP = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}


def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


def rc(w):
    return ''.join(COMP[c] for c in reversed(w))


def main():
    path, n, d, mode = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    words = [l.strip() for l in open(path) if l.strip()]
    w = n // 2
    res = {}
    res['size'] = len(words)
    res['c_length'] = all(len(x) == n for x in words)
    res['c_alphabet'] = all(set(x) <= set('ACGT') for x in words)
    res['c_distinct'] = len(set(words)) == len(words)
    res['c_gc'] = res['c_length'] and all(sum(c in 'CG' for c in x) == w for x in words)
    ok_basic = res['c_length'] and res['c_alphabet']
    mh = min((ham(words[i], words[j]) for i in range(len(words)) for j in range(i + 1, len(words))), default=None) if ok_basic else None
    res['min_hamming'] = mh
    res['c_hamming'] = mh is not None and mh >= d
    if mode == 'gcrc':
        mr = min((ham(x, rc(y)) for x in words for y in words), default=None) if ok_basic else None
        res['min_rc_distance'] = mr
        res['c_rc'] = mr is not None and mr >= d
    else:
        res['c_rc'] = True
    for k in ('c_length', 'c_alphabet', 'c_distinct', 'c_gc', 'c_hamming', 'c_rc'):
        print('%s: %s' % (k, 'PASS' if res[k] else 'FAIL'))
    res['n'], res['d'], res['w'], res['mode'] = n, d, w, mode
    res['VALID'] = all(res[k] for k in ('c_length', 'c_alphabet', 'c_distinct', 'c_gc', 'c_hamming', 'c_rc'))
    print(json.dumps(res, sort_keys=True))


main()
