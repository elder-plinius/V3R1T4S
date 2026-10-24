#!/usr/bin/env python3
"""Independent LABS checker (Python standard library only).
Definition (bank): C_k = sum_i s_i s_{i+k}; E = sum_{k=1}^{L-1} C_k^2; F = L^2/(2E). Integer arithmetic only.
usage: check_labs.py SEQFILE [--L L] [--E claimed_E] [--below bar_E]
SEQFILE holds one line of '0'/'1' symbols ('1' = +1, '0' = -1) or '+'/'-' symbols. Prints PASS or FAIL."""
import sys
def read_seq(path):
    t = ''.join(open(path).read().split())
    if set(t) <= {'0', '1'}: return [1 if c == '1' else -1 for c in t]
    if set(t) <= {'+', '-'}: return [1 if c == '+' else -1 for c in t]
    raise SystemExit('FAIL: alphabet must be 0/1 or +/-')
def energy(s):
    L = len(s); E = 0
    for k in range(1, L):
        c = 0
        for i in range(L - k): c += s[i] * s[i + k]
        E += c * c
    return E
def main(argv):
    path = argv[1]; opts = dict(zip(argv[2::2], argv[3::2]))
    s = read_seq(path); L = len(s); E = energy(s); ok = True
    print(f"L = {L}\nE = {E}\nF = L^2/(2E) = {L*L}/{2*E} = {L*L/(2*E):.6f}")
    if '--L' in opts and int(opts['--L']) != L: print(f"length mismatch: expected {opts['--L']}"); ok = False
    if '--E' in opts and int(opts['--E']) != E: print(f"energy mismatch: claimed {opts['--E']}"); ok = False
    if '--below' in opts:
        bar = int(opts['--below']); print(f"bar = {bar}; strictly below: {E < bar}"); ok = ok and E < bar
    print('PASS' if ok else 'FAIL'); return 0 if ok else 1
if __name__ == '__main__': sys.exit(main(sys.argv))
