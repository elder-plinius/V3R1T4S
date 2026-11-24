#!/usr/bin/env python3
"""Mutation test: inflate each minor constant of cert_arb.certify by a huge factor; the verdict at Y=29.735 must not change.
Inflate the I3/I4 constants slightly; the verdict must flip (shows where the threshold comes from)."""
import re, sys, io, contextlib, types
src = open(sys.argv[1] if len(sys.argv) > 1 else '../../density/code/cert_arb.py').read()
def run(repl):
    s = src
    for a, b in repl: 
        assert a in s, a; s = s.replace(a, b)
    m = types.ModuleType('m'); exec(compile(s, 'mut', 'exec'), m.__dict__)
    with contextlib.redirect_stdout(io.StringIO()):
        ok, out = m.certify('29.735', '51.34', 'thm11', 256, verbose=False)
    return ok
cases = [
 ('K x 1e100', [("K = A('2.4798')", "K = A('2.4798e100')")], True),
 ('KLN C1 x 1e100, C2 x 1e100', [("C1k = A('17.418')", "C1k = A('17.418e100')"), ("C2k = A('5.272')", "C2k = A('5.272e100')")], True),
 ('theta const log4 -> 1e100', [("RT = arb(4).log()", "RT = A('1e100')")], True),
 ('h lower bound 2.99 -> 1e-50 (RE, RT)', [("3*K/A('2.99')", "3*K/A('1e-50')"), ("/A('2.99')*(arb(2)", "/A('1e-50')*(arb(2)")], True),
 ('Bellotti C1 x 1.2', [("A('9.77e21')", "A('11.724e21')")], False),
 ('Bellotti C2 x 1e6', [("A('7.65e10')", "A('7.65e16')")], True),
]
allok = True
for name, repl, expect in cases:
    r = run(repl); good = (r == expect); allok &= good
    print(f"{'ok ' if good else 'BAD'} {name}: verdict {'PASS' if r else 'FAIL'} (expected {'PASS' if expect else 'FAIL'})")
print('MUTATIONS_AS_EXPECTED' if allok else 'MUTATION_SURPRISE')
