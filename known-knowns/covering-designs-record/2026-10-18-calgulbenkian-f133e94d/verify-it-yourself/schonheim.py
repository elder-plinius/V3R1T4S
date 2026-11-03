"""Schonheim lower bound L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), L(v,k,0) = 1, and the block-count comparison."""
import json, sys
from math import ceil
from functools import lru_cache
@lru_cache(None)
def L(v, k, t):
    if t == 0:
        return 1
    # ceil(v * L(v-1,k-1,t-1) / k) in exact integer arithmetic
    num = v * L(v - 1, k - 1, t - 1)
    return -(-num // k)
d = json.load(open(sys.argv[1]))
v, k, t, b = d['v'], d['k'], d['t'], d['b']
lb = L(v, k, t)
in_range = v <= 99 and k <= 25 and t <= 8
print(f"Schonheim L({v},{k},{t}) = {lb}; blocks b = {b}; b >= L: {b >= lb}; parameters within v<=99,k<=25,t<=8: {in_range}")
print("SCHONHEIM PASS" if b >= lb and in_range else "SCHONHEIM FAIL")
sys.exit(0 if b >= lb and in_range else 1)
