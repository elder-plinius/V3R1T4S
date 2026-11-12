#!/usr/bin/env python3
"""Korobov-style pseudo-random exponent boxes.  usage: mkbasis.py spec.json > basis.txt
spec: {"L":1,"prec":384,"masses":[m1,m2,m3],"charges":[1,1,-1],"sym":-1,
       "boxes":[{"n":50,"type":0,"a":[lo,hi],"b":[lo,hi],"c":[lo,hi],"ai":[lo,hi],"bi":..,"ci":..,"seed":1}, ...]}"""
import json, sys
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60
SQ = {'a': Decimal(2).sqrt(), 'b': Decimal(3).sqrt(), 'c': Decimal(5).sqrt(), 'ai': Decimal(7).sqrt(), 'bi': Decimal(11).sqrt(), 'ci': Decimal(13).sqrt()}
def frac(i, key, seed):
    v = (Decimal(i * (i + 1)) / 2) * SQ[key] * (1 + Decimal(seed) / 7)
    return v - int(v)
def gen(spec):
    rows = []
    for bx in spec['boxes']:
        seed = bx.get('seed', 0)
        for i in range(1, bx['n'] + 1):
            vals = []
            for key in ('a', 'ai', 'b', 'bi', 'c', 'ci'):
                lo, hi = bx.get(key, [0, 0])
                vals.append(Decimal(str(lo)) + (Decimal(str(hi)) - Decimal(str(lo))) * frac(i, key, seed))
            rows.append((bx['type'], vals))
    return rows
if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    rows = gen(spec)
    print('L', spec['L']); print('prec', spec.get('prec', 384)); print('masses', *spec['masses'])
    print('charges', *spec.get('charges', [1, 1, -1])); print('sym', spec.get('sym', 0)); print('N', len(rows))
    for t, vals in rows:
        print(t, *['%.30f' % v for v in vals])
