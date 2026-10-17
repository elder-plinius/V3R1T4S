#!/usr/bin/env python3
"""Exact LABS energy. s_i in {+1,-1}; C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}; E = sum_{k=1}^{L-1} C_k^2 (Python int).
Input strings: 0/1 (0 -> +1, 1 -> -1) or +/- characters. Energy is invariant under the global sign flip,
so the 0/1 mapping direction does not change E."""
import sys

def to_pm(s: str) -> list[int]:
    s = "".join(ch for ch in s.strip() if not ch.isspace())
    m = {"0": 1, "1": -1, "+": 1, "-": -1}
    if not s or any(ch not in m for ch in s):
        raise ValueError("sequence must be a non-empty string over 0/1 or +/-")
    return [m[ch] for ch in s]

def energy(seq: list[int]) -> int:
    L = len(seq)
    return sum(sum(seq[i] * seq[i + k] for i in range(L - k)) ** 2 for k in range(1, L))

if __name__ == "__main__":
    for line in (sys.argv[1:] or sys.stdin):
        line = line.strip()
        if line:
            s = to_pm(line.split()[-1])
            print(len(s), energy(s))
