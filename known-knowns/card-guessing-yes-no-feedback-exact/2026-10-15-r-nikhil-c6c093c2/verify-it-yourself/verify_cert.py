#!/usr/bin/env python3
"""Streaming verifier for a card-guessing Bellman certificate (yes/no feedback, Luo arXiv:2609.25062 Appendix A).

Written from the definition; shares no code with the solver. Python 3 standard library only.

Certificate format (gzip or plain text): header "# n=<n> m=<m> ...", then for each layer L = 0, 1, ..., n*m a line
"# L=<L> states=<count>" followed by one line per canonical state: "<g>|<r>:<f>,<r>:<f>,...|<W>" where the pairs
(r_i, f_i) list the labels with r_i >= 1 (r_i = remaining undetermined copies, f_i = positions forbidding i), g is
the number of positions forbidding an exhausted label, and W = C(r,f) * V+(r,f) (an integer: the total optimal
remaining score summed over the C(r,f) consistent arrangements). The number of exhausted labels is n - (#pairs).
M = sum r_i, L = M - sum f_i - g = number of future positions (Luo's L).

Checks, for EVERY listed state (no sampling):
  1. C(r,f) recomputed from Luo's (A.1) with exact integers, and C > 0 (zero-probability states must be absent).
  2. The state lies in the layer announced by L, and no state is listed twice.
  3. L = 0  =>  W = 0 (V+ = 0 when no free position remains).
  4. L >= 1: for every label i (one representative per class (r_i,f_i), and one exhausted label if any):
       yes_i = (r - e_i, f) [if r_i becomes 0 the label is dropped and its f_i joins g];  no_i = (r, f + e_i)
       [for an exhausted label the guess cannot succeed and no_i just adds 1 to g].
       Successor values come from the table's previous layer; a successor absent from the table must have
       C = 0 by the verifier's own (A.1) computation (an omitted positive-probability branch is a failure).
       The verifier checks C(r,f) = C(yes_i) + C(no_i) for every i (the arrangements split by the label at the
       next free position), and then Luo's recursion
         V+(r,f) = max_i { p_i [1 + V+(yes_i)] + (1 - p_i) V+(no_i) },  p_i = C(yes_i)/C(r,f),
       exactly: with V+ = W/C this reads  W(r,f) = max_i [ C(yes_i) + W(yes_i) + W(no_i) ]  (integers), and in
       --literal mode the rational right-hand side is also evaluated with fractions.Fraction and compared to W/C.
  5. The initial state (g = 0, all n labels (m, 0)) is in the top layer with V+ = W/C equal to --claimed.
Exit status 0 and last line "PASS" only if every check passes; otherwise "FAIL: <reason>".
"""
import sys, gzip, argparse
from fractions import Fraction
from math import comb, factorial

def open_any(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path, 'r')

_fact_cache = {}
_factor_cache = {}
def label_factor(r, f):
    """A_i(z) = sum_{k=0}^{min(r,f)} (-1)^k binom(f,k) (r)_k z^k  as a list of coefficients."""
    key = (r, f)
    a = _factor_cache.get(key)
    if a is None:
        a = []
        falling = 1
        for k in range(min(r, f) + 1):
            if k > 0: falling *= (r - k + 1)
            a.append((-1) ** k * comb(f, k) * falling)
        _factor_cache[key] = a
    return a

_C_cache = {}
def count_C(pairs):
    """Luo (A.1): C(r,f) = (1/prod r_i!) sum over k-vectors (-1)^K (M-K)! prod binom(f_i,k_i) (r_i)_{k_i}.
    The sum over k-vectors is regrouped by K as sum_K (M-K)! [z^K] prod_i A_i(z) (an identity of polynomials)."""
    c = _C_cache.get(pairs)
    if c is not None: return c
    M = sum(r for r, f in pairs)
    poly = [1]
    denom = 1
    for r, f in pairs:
        a = label_factor(r, f)
        new = [0] * (len(poly) + len(a) - 1)
        for i, pc in enumerate(poly):
            if pc:
                for j, ac in enumerate(a):
                    new[i + j] += pc * ac
        poly = new
        denom *= factorial(r)
    total = 0
    for K, coef in enumerate(poly):
        if coef: total += coef * factorial(M - K)
    if total % denom != 0: raise AssertionError("inexact division in (A.1)")
    c = total // denom
    if c < 0: raise AssertionError("negative count")
    if len(_C_cache) < 4000000: _C_cache[pairs] = c
    return c

def parse_state(s):
    g_s, pairs_s = s.split('|')
    g = int(g_s)
    pairs = tuple(tuple(int(x) for x in p.split(':')) for p in pairs_s.split(',')) if pairs_s else ()
    return g, pairs

def L_of(g, pairs):
    return sum(r for r, f in pairs) - sum(f for r, f in pairs) - g

def successors(g, pairs, idx):
    """yes/no successor keys when guessing the label of pairs[idx]."""
    r, f = pairs[idx]
    rest = pairs[:idx] + pairs[idx + 1:]
    if r - 1 >= 1:
        yes = (g, tuple(sorted(rest + ((r - 1, f),))))
    else:
        yes = (g + f, tuple(sorted(rest)))
    no = (g, tuple(sorted(rest + ((r, f + 1),))))
    return yes, no

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cert'); ap.add_argument('--claimed', help='claimed value NUM/DEN for the initial state')
    ap.add_argument('--literal', action='store_true', help='also evaluate the rational recursion with Fractions')
    ap.add_argument('--progress', type=int, default=0)
    ap.add_argument('--persistence', action='store_true', help='also test the Diaconis-Graham 1981 persistence conjecture on every state')
    args = ap.parse_args()
    n = m = None
    prev = {}      # previous layer: key -> (C, W) or (C, W, optset) with --persistence
    persist_pairs = 0; persist_viol = 0; first_viol = None
    cur = {}
    cur_L = None
    expected_count = None
    counted = 0
    total_states = 0
    actions = 0
    init_found = None
    fail = None
    def lookup(key):
        v = prev.get(key)
        if v is not None: return v[0], v[1]
        c = count_C(key[1])
        if c != 0:
            raise AssertionError(f"successor {key} missing from table but C={c}>0")
        return (0, 0)
    try:
        with open_any(args.cert) as fh:
            for line in fh:
                line = line.rstrip('\n')
                if not line: continue
                if line.startswith('#'):
                    if line.startswith('# n='):
                        parts = dict(p.split('=') for p in line[2:].split() if '=' in p)
                        n = int(parts['n']); m = int(parts['m'])
                        continue
                    if line.startswith('# L='):
                        parts = dict(p.split('=') for p in line[2:].split() if '=' in p)
                        L = int(parts['L'])
                        if cur_L is not None:
                            if counted != expected_count:
                                raise AssertionError(f"layer {cur_L}: announced {expected_count} states, read {counted}")
                            if L != cur_L + 1: raise AssertionError("layers not increasing by one")
                            prev = cur; cur = {}
                        elif L != 0: raise AssertionError("first layer must be L=0")
                        cur_L = L; expected_count = int(parts['states']); counted = 0
                        continue
                    continue
                if n is None or cur_L is None: raise AssertionError("state before header")
                state_s, W_s = line.rsplit('|', 1)
                g, pairs = parse_state(state_s)
                W = int(W_s)
                key = (g, pairs)
                if key in cur: raise AssertionError(f"duplicate state {key}")
                if len(pairs) > n: raise AssertionError("more labels than n")
                if tuple(sorted(pairs)) != pairs: raise AssertionError(f"state not canonical {key}")
                for r, f in pairs:
                    if not (1 <= r <= m) or f < 0: raise AssertionError(f"bad pair {key}")
                if L_of(g, pairs) != cur_L: raise AssertionError(f"state {key} not in layer {cur_L}")
                C = count_C(pairs)
                if C <= 0: raise AssertionError(f"state {key} has C={C}")
                if W < 0: raise AssertionError("negative W")
                if cur_L == 0:
                    if W != 0: raise AssertionError(f"terminal state {key} has W={W}")
                else:
                    best = None
                    best_lit = None
                    k = len(pairs)
                    for idx in range(k):
                        if idx > 0 and pairs[idx] == pairs[idx - 1]: continue
                        yes, no = successors(g, pairs, idx)
                        Cy, Wy = lookup(yes); Cn, Wn = lookup(no)
                        if Cy + Cn != C: raise AssertionError(f"count split fails at {key} label {pairs[idx]}: {Cy}+{Cn}!={C}")
                        cand = Cy + Wy + Wn
                        actions += 1
                        if best is None or cand > best: best = cand
                        if args.literal:
                            p = Fraction(Cy, C)
                            rhs = (p * (1 + Fraction(Wy, Cy)) if Cy else Fraction(0)) + ((1 - p) * Fraction(Wn, Cn) if Cn else Fraction(0))
                            if best_lit is None or rhs > best_lit: best_lit = rhs
                    if k < n:  # an exhausted label can be guessed: success probability 0, failure adds a vacuous forbidden position
                        no = (g + 1, pairs)
                        Cn, Wn = lookup(no)
                        if Cn != C: raise AssertionError(f"exhausted-label branch count mismatch at {key}")
                        cand = Wn
                        actions += 1
                        if best is None or cand > best: best = cand
                        if args.literal:
                            rhs = Fraction(Wn, Cn)
                            if best_lit is None or rhs > best_lit: best_lit = rhs
                    if best != W: raise AssertionError(f"recursion fails at {key}: table W={W}, max over labels={best}")
                    if args.persistence:
                        # optimal classes at this state; then: for each optimal class i, after a failed guess of i
                        # (successor no_i, present when C(no_i) > 0), class (r_i, f_i + 1) must be optimal at no_i.
                        optset = set()
                        for idx in range(k):
                            if idx > 0 and pairs[idx] == pairs[idx - 1]: continue
                            yes, no = successors(g, pairs, idx)
                            Cy, Wy = lookup(yes); Cn, Wn = lookup(no)
                            if Cy + Wy + Wn == best: optset.add(pairs[idx])
                        if k < n and lookup((g + 1, pairs))[1] == best: optset.add('exhausted')
                        for cls in optset:
                            if cls == 'exhausted': continue
                            idx = pairs.index(cls)
                            yes, no = successors(g, pairs, idx)
                            pv = prev.get(no)
                            if pv is None or cur_L - 1 < 1: continue  # failure has probability 0, or no guess remains
                            persist_pairs += 1
                            if (cls[0], cls[1] + 1) not in pv[2]:
                                persist_viol += 1
                                if first_viol is None: first_viol = (key, cls, no, sorted(pv[2], key=str))
                        cur[key] = (C, W, optset)
                        counted += 1; total_states += 1
                        if args.progress and total_states % args.progress == 0:
                            print(f"progress states={total_states} layer={cur_L}", file=sys.stderr, flush=True)
                        if cur_L == n * m:
                            init = (0, tuple((m, 0) for _ in range(n)))
                            if key == init: init_found = Fraction(W, C)
                        continue
                    if args.literal and best_lit != Fraction(W, C): raise AssertionError(f"literal recursion fails at {key}")
                cur[key] = (C, W, set()) if args.persistence else (C, W)
                counted += 1; total_states += 1
                if args.progress and total_states % args.progress == 0:
                    print(f"progress states={total_states} layer={cur_L}", file=sys.stderr, flush=True)
                if cur_L == n * m:
                    init = (0, tuple((m, 0) for _ in range(n)))
                    if key == init: init_found = Fraction(W, C)
        if counted != expected_count: raise AssertionError(f"layer {cur_L}: announced {expected_count} states, read {counted}")
        if cur_L != n * m: raise AssertionError(f"last layer is {cur_L}, expected {n*m}")
        if init_found is None: raise AssertionError("initial state missing")
        if args.claimed:
            num, den = args.claimed.split('/')
            if init_found != Fraction(int(num), int(den)): raise AssertionError(f"initial value {init_found} != claimed {args.claimed}")
    except AssertionError as e:
        fail = str(e)
    if fail:
        print(f"states_checked={total_states}")
        print(f"FAIL: {fail}")
        sys.exit(1)
    print(f"n={n} m={m} states={total_states} actions={actions} value={init_found} = {float(init_found):.12f}")
    if args.persistence:
        print(f"persistence: optimal-guess failure pairs={persist_pairs} violations={persist_viol} first_violation={first_viol}")
    print("PASS")

if __name__ == '__main__':
    main()
