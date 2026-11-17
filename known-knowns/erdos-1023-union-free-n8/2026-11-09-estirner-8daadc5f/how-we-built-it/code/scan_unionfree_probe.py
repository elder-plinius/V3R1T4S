#!/usr/bin/env python3
"""Probe: how hard is a(n) for the A347025 union-free family, n=8?

Family F of nonempty subsets of {1..8}; bad iff some S in F equals the union
of the other members contained in S. Equivalent: S has no element uncovered by
chosen proper subsets. Local search on 255 booleans with incremental counters.
"""
import random, sys, time

def build(n):
    U = list(range(1, 1 << n))
    sup = {s: [t for t in U if t != s and (t & s) == s] for s in U}
    elems = {s: [e for e in range(n) if s >> e & 1] for s in U}
    return U, sup, elems

def run(n, seed_mode, seconds, lam=3.0):
    U, sup, elems = build(n)
    chosen = {s: False for s in U}
    cnt = {s: {e: 0 for e in elems[s]} for s in U}
    zeros = {s: len(elems[s]) for s in U}   # elements of s uncovered by chosen proper subsets
    unsafe = {s: False for s in U}
    V = 0
    size = 0

    def add(s):
        nonlocal V, size
        chosen[s] = True; size += 1
        if zeros[s] == 0:
            unsafe[s] = True; V += 1
        for t in sup[s]:
            for e in elems[s]:
                if cnt[t][e] == 0:
                    zeros[t] -= 1
                    if chosen[t] and zeros[t] == 0:
                        unsafe[t] = True; V += 1
                cnt[t][e] += 1
    def rem(s):
        nonlocal V, size
        for t in sup[s]:
            for e in elems[s]:
                cnt[t][e] -= 1
                if cnt[t][e] == 0:
                    zeros[t] += 1
                    if chosen[t] and zeros[t] == 1:
                        unsafe[t] = False; V -= 1
        chosen[s] = False; size -= 1
        if unsafe[s]:
            unsafe[s] = False; V -= 1

    if seed_mode == 'middle':
        for s in U:
            if bin(s).count('1') == n // 2: add(s)
    elif seed_mode == 'greedy':
        for s in sorted(U, key=lambda x: -bin(x).count('1')):
            before = V
            add(s)
            if V > before:
                rem(s)
    # else empty

    best = size; bestF = [s for s in U if chosen[s]]
    rng = random.Random(12345)
    t0 = time.time(); T0 = 1.2; steps = 0
    order = U[:]
    while time.time() - t0 < seconds:
        T = T0 * (1 - (time.time() - t0) / seconds) + 0.02
        rng.shuffle(order)
        for s in order:
            d = (1 if not chosen[s] else -1)  # +1 add, -1 remove
            old_V = V; old_size = size
            if d == 1: add(s)
            else: rem(s)
            de = -(size - old_size) + lam * (V - old_V)
            if de <= 0 or rng.random() < pow(2.718281828, -de / T):
                steps += 1
                if V == 0 and size > best:
                    best = size; bestF = [t for t in U if chosen[t]]
            else:
                if d == 1: rem(s)
                else: add(s)
    return best, bestF, steps

def verify(F, n, program=True):
    F = set(F)
    for s in F:
        allrest = 0
        for r in F:
            if r != s and (r & s) == r:
                allrest |= r
        if allrest == s:
            return False, s
    return True, None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 20
    for mode in ('middle', 'greedy', 'empty'):
        b, F, st = run(n, mode, secs)
        ok, bad = verify(F, n)
        print(f"n={n} seed={mode:6s} best={b:3d} valid={ok} bad={bad} steps={st}")
        if b >= 79:
            print('  FAMILY:', sorted(F))
