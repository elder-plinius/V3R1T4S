#!/usr/bin/env python3
"""T4: direct construction from a 2-group-like structure at composite order 28, seeking > 3324.

The 3324 result is 2 x 14. The n=14 factor (391) is itself close to its bound of 637 (61%). If we could find a
better order-14 square, the product would rise. So:
  1. hill-climb the ORDER-14 square itself (small: 14x14) with cycle switches, from the posted 391.
  2. for every better 14-square found, rebuild 2 x 14 and recount.
This is a cheap, high-yield line: the 14-square is the bottleneck, and it is tiny.
"""
import sys, json, random, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from countA import count_intercalates, is_latin
from t3_cycleswitch import cycle_switch
from t5_products_composite import product, to_int

p92 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsed_092.json')))
B14 = [r[:] for r in p92['14']['sq']]
A2 = p92['2']['sq']

def climb14(L0, seed, time_cap=60, kmax=5):
    rng = random.Random(seed); n = len(L0); L = [r[:] for r in L0]
    cur = count_intercalates(L); best = cur; bestL = [r[:] for r in L]
    t0 = time.time(); it = 0; acc = 0
    while time.time() - t0 < time_cap:
        it += 1
        k = rng.randrange(2, kmax+1)
        rs = rng.sample(range(n), k); cs = rng.sample(range(n), k)
        snap = [[L[r][c] for c in cs] for r in rs]
        cycle_switch(L, rs, cs, rng)
        if is_latin(L):
            v = count_intercalates(L)
            if v >= cur or rng.random() < 0.01:
                cur = v; acc += 1
                if cur > best: best, bestL = cur, [r[:] for r in L]
            else:
                for i, r in enumerate(rs):
                    for j, c in enumerate(cs): L[r][c] = snap[i][j]
        else:
            for i, r in enumerate(rs):
                for j, c in enumerate(cs): L[r][c] = snap[i][j]
    return bestL, best, it, acc

print("start n=14:", count_intercalates(B14), "bound:", 14*14*13//4)
best14, bestv = B14, count_intercalates(B14)
for seed in range(4):
    L, v, it, acc = climb14(B14, seed, time_cap=20)
    print(f"  seed {seed}: n=14 best={v} iters={it} acc={acc}")
    if v > bestv: bestv, best14 = v, L

# rebuild 2x14 with the best 14
P = to_int(product(A2, best14))
print("best n=14:", bestv, "-> 2x14 =", count_intercalates(P), "latin:", is_latin(P))
json.dump({"n14": bestv, "square14": best14, "prod28": count_intercalates(P)}, open("best14.json", "w"))
