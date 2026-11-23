#!/usr/bin/env python3
"""Baseline definition checker for Euler bricks and perfect cuboids (RUN.md Step 3 / LESSONS #16)."""
import math

def check_cuboid(a: int, b: int, c: int):
    if not (a > 0 and b > 0 and c > 0):
        return {"valid_edges": False, "euler_brick": False, "perfect_cuboid": False}
    d_ab2 = a * a + b * b
    d_bc2 = b * b + c * c
    d_ac2 = a * a + c * c
    d_sp2 = d_ab2 + c * c
    is_sq = lambda n: math.isqrt(n) ** 2 == n
    eb = is_sq(d_ab2) and is_sq(d_bc2) and is_sq(d_ac2)
    pc = eb and is_sq(d_sp2)
    return {
        "valid_edges": True,
        "euler_brick": eb,
        "perfect_cuboid": pc,
        "d_ab2": d_ab2,
        "d_bc2": d_bc2,
        "d_ac2": d_ac2,
        "d_sp2": d_sp2,
    }

def check_four_square_tuple(x2: int, y2: int, z2: int):
    """Synthetic algebraic check on 4-square predicate (x2, y2, z2 > 0)."""
    is_sq = lambda n: n > 0 and math.isqrt(n) ** 2 == n
    return (
        is_sq(x2) and is_sq(y2) and is_sq(z2)
        and is_sq(x2 + y2) and is_sq(y2 + z2) and is_sq(x2 + z2)
        and is_sq(x2 + y2 + z2)
    )

if __name__ == "__main__":
    # Known positive Euler brick (Halcke 1719): (44, 117, 240), negative for perfect cuboid
    r_halcke = check_cuboid(44, 117, 240)
    assert r_halcke["euler_brick"] is True and r_halcke["perfect_cuboid"] is False, r_halcke
    # Known Saunderson brick at (u,v,w)=(3,4,5): (240, 117, 44) scaled / (240, 252, 275) non-Saunderson
    r_240 = check_cuboid(240, 252, 275)
    assert r_240["euler_brick"] is True and r_240["perfect_cuboid"] is False, r_240
    # Known face cuboid (104, 153, 672): a^2+b^2=185^2, a^2+c^2=680^2, a^2+b^2+c^2=697^2, b^2+c^2 non-square
    r_face = check_cuboid(104, 153, 672)
    assert r_face["euler_brick"] is False and math.isqrt(r_face["d_sp2"]) ** 2 == r_face["d_sp2"], r_face
    # Degenerate zero-edge tuple (0, 3, 4) rejected
    r_deg = check_cuboid(0, 3, 4)
    assert r_deg["perfect_cuboid"] is False
    print("BASELINE_CHECKER: PASS (Halcke Euler brick=True/PC=False, (240,252,275)=True/False, face cuboid=False, degenerate=False)")
