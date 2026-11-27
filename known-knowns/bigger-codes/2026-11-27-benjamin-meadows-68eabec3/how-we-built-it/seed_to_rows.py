#!/usr/bin/env python3
"""Convert a code file from Brouwer's site to plain 0/1 rows, keeping the file's word order.

usage: python3 seed_to_rows.py CODE_FILE n > rows.txt

Formats handled: plain rows of 0/1, and files starting with the line $BASE=16, where each line is one word written
as a hexadecimal number whose binary expansion, padded on the left to n digits, is the word.
"""
import sys


def main(argv):
    path, n = argv[1], int(argv[2])
    lines = [l.strip() for l in open(path) if l.strip() and not l.startswith('#')]
    hexmode = lines and lines[0] == '$BASE=16'
    if hexmode:
        lines = lines[1:]
    for l in lines:
        if hexmode:
            v = int(l, 16)
            if v >> n:
                sys.exit('word %s has more than %d binary digits' % (l, n))
            print(format(v, '0%db' % n))
        else:
            if len(l) != n or set(l) - {'0', '1'}:
                sys.exit('line %r is not a 0/1 word of length %d' % (l, n))
            print(l)


if __name__ == '__main__':
    main(sys.argv)
