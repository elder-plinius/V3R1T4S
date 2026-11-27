#!/usr/bin/env python3
"""Svdp.S_all by the C program svdp (same DP, modulo a Mersenne prime 2^E-1); falls back to Python Svdp for other moduli."""
import os, subprocess
import Svdp
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svdp')
BIN2 = BIN + '_n2'  # 2026-11-24: same program built with NL=2 limbs (E <= 127): 16 B values instead of 80 B


def S_all(d, side, n, shifts, P=None):
    shifts = [tuple(s) for s in shifts]
    E = P.bit_length() if P else 0
    if not P or P != (1 << E) - 1 or not shifts:
        return Svdp.S_all(d, side, n, shifts, P)
    inp = f"{len(shifts)}\n" + "\n".join(" ".join(map(str, s)) for s in shifts) + "\n"
    o = subprocess.run([BIN2 if E <= 127 and os.path.exists(BIN2) else BIN, str(d), str(side), str(n), str(E)], input=inp, capture_output=True, text=True)
    if o.returncode == 3:
        raise MemoryError('svdp: out of memory')
    if o.returncode:
        raise RuntimeError('svdp failed: ' + o.stderr[-300:])
    vals = o.stdout.split()
    assert len(vals) == len(shifts)
    return {s: int(x, 16) for s, x in zip(shifts, vals)}
