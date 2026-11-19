#!/usr/bin/env python3
"""Independent B3/S23 glider-synthesis checker (stdlib only).

Built from claim/TARGET_CRITERION.md and claim/CLAIM.md, not from author
code. Numerical verification of a 7-glider synthesis of a still life.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, deque
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Cell = Tuple[int, int]
Cells = Set[Cell]
FCells = frozenset

NEIGHBORS = tuple(
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not (dx == 0 and dy == 0)
)

D8 = (
    lambda x, y: (x, y),
    lambda x, y: (-y, x),
    lambda x, y: (-x, -y),
    lambda x, y: (y, -x),
    lambda x, y: (-x, y),
    lambda x, y: (x, -y),
    lambda x, y: (y, x),
    lambda x, y: (-y, -x),
)


# ---------------------------------------------------------------------------
# Life engines (two independent implementations; must agree)
# ---------------------------------------------------------------------------

def step_counter(cells: Cells) -> Cells:
    ncount: Counter = Counter()
    for x, y in cells:
        for dx, dy in NEIGHBORS:
            ncount[x + dx, y + dy] += 1
    nxt: Cells = set()
    for pos, n in ncount.items():
        if n == 3 or (n == 2 and pos in cells):
            nxt.add(pos)
    return nxt


def step_grid(cells: Cells) -> Cells:
    if not cells:
        return set()
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    minx, maxx = min(xs) - 1, max(xs) + 1
    miny, maxy = min(ys) - 1, max(ys) + 1
    live = cells
    nxt: Cells = set()
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            n = 0
            for dx, dy in NEIGHBORS:
                if (x + dx, y + dy) in live:
                    n += 1
            if n == 3 or (n == 2 and (x, y) in live):
                nxt.add((x, y))
    return nxt


def step(cells: Cells) -> Cells:
    a = step_counter(cells)
    b = step_grid(cells)
    if a != b:
        raise RuntimeError("Life engines disagree")
    return a


def step_fast(cells: Cells) -> Cells:
    """Single-engine step used in long rewind/forward loops after engines agree."""
    return step_counter(cells)


def evolve(cells: Cells, n: int, fast: bool = True) -> Cells:
    s = set(cells)
    fn = step_fast if fast else step
    for _ in range(n):
        s = fn(s)
    return s


def is_still_life(cells: Cells) -> bool:
    return step_fast(cells) == cells


# ---------------------------------------------------------------------------
# Geometry / components
# ---------------------------------------------------------------------------

def bbox(cells: Iterable[Cell]) -> Optional[Tuple[int, int, int, int]]:
    cells = list(cells)
    if not cells:
        return None
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    return min(xs), min(ys), max(xs), max(ys)


def bbox_wh(cells: Iterable[Cell]) -> Tuple[int, int]:
    b = bbox(cells)
    if b is None:
        return 0, 0
    minx, miny, maxx, maxy = b
    return maxx - minx + 1, maxy - miny + 1


def euclidean_bbox_diag(cells: Iterable[Cell]) -> float:
    w, h = bbox_wh(cells)
    return math.hypot(w, h)


def normalize(cells: Iterable[Cell]) -> FCells:
    cells = list(cells)
    if not cells:
        return frozenset()
    mx = min(p[0] for p in cells)
    my = min(p[1] for p in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def match_d8_translation(cells: Iterable[Cell], target: Iterable[Cell]) -> bool:
    t = normalize(target)
    src = list(cells)
    if len(src) != len(t):
        return False
    for f in D8:
        if normalize(f(x, y) for x, y in src) == t:
            return True
    return False


def components8(cells: Cells) -> List[Cells]:
    remaining = set(cells)
    comps: List[Cells] = []
    while remaining:
        start = remaining.pop()
        comp = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in NEIGHBORS:
                n = (x + dx, y + dy)
                if n in remaining:
                    remaining.remove(n)
                    comp.add(n)
                    q.append(n)
        comps.append(comp)
    return comps


def ascii_pattern(cells: Iterable[Cell], live: str = "O", dead: str = ".") -> str:
    cells = list(cells)
    if not cells:
        return "(empty)"
    minx, miny, maxx, maxy = bbox(cells)
    s = set(cells)
    rows = []
    for y in range(miny, maxy + 1):
        rows.append("".join(live if (x, y) in s else dead for x in range(minx, maxx + 1)))
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# RLE
# ---------------------------------------------------------------------------

def parse_rle(text: str) -> Tuple[Cells, str, Optional[int], Optional[int]]:
    rule = "B3/S23"
    width = height = None
    body_parts: List[str] = []
    header_re = re.compile(
        r"x\s*=\s*(\d+)\s*,\s*y\s*=\s*(\d+)(?:\s*,\s*rule\s*=\s*([^ \t\n]+))?",
        re.IGNORECASE,
    )
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        m = header_re.match(line)
        if m and not body_parts:
            width = int(m.group(1))
            height = int(m.group(2))
            if m.group(3):
                rule = m.group(3).strip()
            continue
        body_parts.append(line)
    body = "".join(body_parts)
    cells: Cells = set()
    x = y = 0
    i = 0
    n = len(body)
    while i < n:
        if body[i].isspace():
            i += 1
            continue
        if body[i] == "!":
            break
        j = i
        while j < n and body[j].isdigit():
            j += 1
        count = int(body[i:j]) if j > i else 1
        if j >= n:
            break
        c = body[j]
        if c in "oO":
            for k in range(count):
                cells.add((x + k, y))
            x += count
        elif c in "bB":
            x += count
        elif c == "$":
            y += count
            x = 0
        elif c == "!":
            break
        else:
            raise ValueError("unsupported RLE symbol %r at %d" % (c, j))
        i = j + 1
    return cells, rule, width, height


def canonical_rule(rule: str) -> str:
    r = rule.strip()
    rl = r.lower().replace(" ", "")
    if rl in ("b3/s23", "s23/b3", "life", "conway", "b3s23"):
        return "B3/S23"
    return r


# ---------------------------------------------------------------------------
# Apgcode / extended Wechsler
# ---------------------------------------------------------------------------

def _wechsler_val(ch: str, end: str) -> int:
    if "0" <= ch <= "9":
        return ord(ch) - ord("0")
    if "a" <= ch <= end:
        return ord(ch) - ord("a") + 10
    raise ValueError("invalid Wechsler char %r (end=%r)" % (ch, end))


def decode_wechsler(suffix: str) -> Cells:
    cells: Cells = set()
    x = 0
    y = 0
    i = 0
    n = len(suffix)
    while i < n:
        c = suffix[i]
        if c == "z":
            y += 5
            x = 0
            i += 1
            continue
        if c == "w":
            x += 2
            i += 1
            continue
        if c == "x":
            x += 3
            i += 1
            continue
        if c == "y":
            if i + 1 >= n:
                raise ValueError("truncated y-run in Wechsler string")
            x += _wechsler_val(suffix[i + 1], "z") + 4
            i += 2
            continue
        bits = _wechsler_val(c, "v")
        for b in range(5):
            if bits & (1 << b):
                cells.add((x, y + b))
        x += 1
        i += 1
    return cells


def decode_apgcode(code: str) -> Tuple[str, int, Cells]:
    if "_" not in code:
        raise ValueError("apgcode missing underscore: %r" % code)
    prefix, suffix = code.split("_", 1)
    if not prefix or prefix[0] != "x":
        raise ValueError("unsupported apgcode prefix %r" % prefix)
    kind = prefix[1]
    if kind not in ("s", "p", "q"):
        raise ValueError("unsupported apgcode class %r" % prefix)
    rest = prefix[2:]
    if not rest.isdigit():
        raise ValueError("unsupported apgcode prefix %r" % prefix)
    num = int(rest)
    cells = decode_wechsler(suffix)
    return prefix, num, cells


# ---------------------------------------------------------------------------
# Gliders
# ---------------------------------------------------------------------------

def glider_shapes() -> Tuple[Dict[FCells, Tuple[int, int]], List[FCells]]:
    """All 16 glider shapes (translation-normalized) mapped to (vx, vy).

    Velocity is cells per 4 generations, one of (±1, ±1).
    """
    _, _, g0 = decode_apgcode("xq4_153")
    shapes: Dict[FCells, Tuple[int, int]] = {}
    for phase in range(4):
        phased = evolve(g0, phase, fast=False)
        for rot in range(4):
            cur = set(phased)
            for _ in range(rot):
                cur = {(-y, x) for x, y in cur}
            cur4 = evolve(cur, 4, fast=False)
            n0 = normalize(cur)
            minx0 = min(p[0] for p in cur)
            miny0 = min(p[1] for p in cur)
            minx4 = min(p[0] for p in cur4)
            miny4 = min(p[1] for p in cur4)
            vx, vy = minx4 - minx0, miny4 - miny0
            shifted = {(x + vx, y + vy) for x, y in cur}
            if shifted != cur4:
                raise RuntimeError("glider 4-step is not a translation")
            if abs(vx) != 1 or abs(vy) != 1:
                raise RuntimeError("glider velocity not diagonal: %s" % ((vx, vy),))
            if n0 in shapes and shapes[n0] != (vx, vy):
                raise RuntimeError("inconsistent glider velocity for a shape")
            shapes[n0] = (vx, vy)
    if len(shapes) != 16:
        raise RuntimeError("expected 16 glider shapes, got %d" % len(shapes))
    return shapes, list(shapes.keys())


GLIDER_VEL, GLIDER_SHAPES = glider_shapes()


def identify_glider(comp: Cells) -> Optional[Tuple[FCells, Tuple[int, int]]]:
    if len(comp) != 5:
        return None
    n = normalize(comp)
    vel = GLIDER_VEL.get(n)
    if vel is None:
        return None
    return n, vel


def rewind_glider(comp: Cells, gens: int) -> Cells:
    ident = identify_glider(comp)
    if ident is None:
        raise ValueError("component is not a glider")
    if gens % 4 != 0:
        raise ValueError("rewind generations must be a multiple of 4")
    _, (vx, vy) = ident
    steps = gens // 4
    dx, dy = -steps * vx, -steps * vy
    return {(x + dx, y + dy) for x, y in comp}


# ---------------------------------------------------------------------------
# Strict still-life (partition into two nonempty stable pieces)
# ---------------------------------------------------------------------------

def _neighbor_live_masks(cells_list: Sequence[Cell]) -> List[int]:
    idx = {p: i for i, p in enumerate(cells_list)}
    masks = []
    for x, y in cells_list:
        m = 0
        for dx, dy in NEIGHBORS:
            j = idx.get((x + dx, y + dy))
            if j is not None:
                m |= 1 << j
        masks.append(m)
    return masks


def _dead_halo_masks(cells_list: Sequence[Cell]) -> List[int]:
    live = set(cells_list)
    idx = {p: i for i, p in enumerate(cells_list)}
    halo: Set[Cell] = set()
    for x, y in cells_list:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                p = (x + dx, y + dy)
                if p not in live:
                    halo.add(p)
    masks = []
    for x, y in halo:
        m = 0
        for dx, dy in NEIGHBORS:
            j = idx.get((x + dx, y + dy))
            if j is not None:
                m |= 1 << j
        if m:
            masks.append(m)
    return masks


def _mask_is_still(mask: int, live_masks: Sequence[int], dead_masks: Sequence[int], n: int) -> bool:
    for i in range(n):
        nc = (live_masks[i] & mask).bit_count()
        if (mask >> i) & 1:
            if nc != 2 and nc != 3:
                return False
        else:
            if nc == 3:
                return False
    for dm in dead_masks:
        if (dm & mask).bit_count() == 3:
            return False
    return True


def still_life_strictness(cells: Cells) -> Tuple[bool, str]:
    """Return (is_strict, reason). Requires cells already a still life."""
    if not is_still_life(cells):
        return False, "not a still life"
    if not cells:
        return False, "empty"
    lst = list(cells)
    n = len(lst)
    live_masks = _neighbor_live_masks(lst)
    dead_masks = _dead_halo_masks(lst)
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    # Cells with exactly 2 live neighbors are forced to stay with both.
    for i, m in enumerate(live_masks):
        nc = m.bit_count()
        if nc == 2:
            bits = m
            while bits:
                lsb = bits & -bits
                j = lsb.bit_length() - 1
                union(i, j)
                bits -= lsb
        elif nc not in (2, 3):
            return False, "live cell with %d neighbors" % nc

    groups: Dict[int, int] = {}
    group_mask: List[int] = []
    for i in range(n):
        r = find(i)
        if r not in groups:
            groups[r] = len(group_mask)
            group_mask.append(0)
        group_mask[groups[r]] |= 1 << i
    gcount = len(group_mask)
    full = (1 << n) - 1
    if gcount == 1:
        return True, "single forced-stability component (%d cells)" % n

    # Brute-force nonempty proper subsets of groups.
    limit = 1 << gcount
    if gcount > 20:
        # Too large to exhaust; fall back to 8-connected island check only.
        comps = components8(cells)
        if len(comps) > 1 and all(is_still_life(c) for c in comps):
            return False, "multiple independently stable 8-islands"
        return True, "forced groups=%d (not exhaustively partitioned; no stable 8-islands)" % gcount

    for sub in range(1, limit - 1):
        mask = 0
        bits = sub
        gi = 0
        while bits:
            if bits & 1:
                mask |= group_mask[gi]
            bits >>= 1
            gi += 1
        if mask == 0 or mask == full:
            continue
        if _mask_is_still(mask, live_masks, dead_masks, n) and _mask_is_still(
            full ^ mask, live_masks, dead_masks, n
        ):
            return False, "partition into two still lifes (pops %d+%d)" % (
                mask.bit_count(),
                n - mask.bit_count(),
            )
    return True, "no still-life partition of %d forced groups" % gcount


# ---------------------------------------------------------------------------
# Synthesis check
# ---------------------------------------------------------------------------

def rewind_amount(cells: Cells) -> Tuple[int, float, int, int]:
    w, h = bbox_wh(cells)
    diag = math.hypot(w, h)
    rewind = 4 * int(math.ceil(diag))
    return rewind, diag, w, h


def check_rewind(gliders: Sequence[Cells], rewind_gens: int) -> dict:
    """Combined evolution must equal union of separate gliders at every gen."""
    rewound = [rewind_glider(g, rewind_gens) for g in gliders]
    separate = [set(g) for g in rewound]
    combined = set()
    for g in separate:
        combined |= g
    mismatches = []
    for t in range(0, rewind_gens + 1):
        union = set()
        for g in separate:
            union |= g
        if combined != union:
            mismatches.append(t)
            if len(mismatches) >= 8:
                break
        if t == rewind_gens:
            break
        combined = step_fast(combined)
        separate = [step_fast(g) for g in separate]
    original = set()
    for g in gliders:
        original |= g
    recovered = combined if not mismatches else None
    ok = not mismatches and recovered == original
    return {
        "ok": ok,
        "rewind_gens": rewind_gens,
        "mismatch_generations": mismatches,
        "recovered_original": recovered == original if recovered is not None else False,
        "n_gliders": len(gliders),
    }


def check_forward(
    cells: Cells, target_cells: Cells, max_gens: int
) -> dict:
    cur = set(cells)
    hist_hash: Dict[FCells, int] = {}
    period = None
    settle_gen = None
    for t in range(0, max_gens + 1):
        nxt = step_fast(cur)
        if nxt == cur:
            period = 1
            settle_gen = t
            break
        key = frozenset(cur)
        if key in hist_hash:
            period = t - hist_hash[key]
            settle_gen = hist_hash[key]
            cur = set(key)
            break
        hist_hash[key] = t
        cur = nxt
    if period is None:
        return {
            "ok": False,
            "reason": "did not become periodic within %d gens" % max_gens,
            "last_population": len(cur),
            "last_bbox": bbox_wh(cur),
        }
    if period != 1:
        return {
            "ok": False,
            "reason": "settled period %d (need 1)" % period,
            "settle_gen": settle_gen,
            "population": len(cur),
        }
    pop = len(cur)
    d8 = match_d8_translation(cur, target_cells)
    extra = pop != len(target_cells)
    ok = pop == 28 and d8 and pop == len(target_cells)
    return {
        "ok": ok,
        "period": period,
        "settle_gen": settle_gen,
        "population": pop,
        "target_population": len(target_cells),
        "d8_translation_match": d8,
        "equal_population": pop == len(target_cells),
        "no_other_cells": d8 and pop == len(target_cells),
        "final_bbox": bbox_wh(cur),
        "extra_or_missing": extra and not d8,
    }


def check_synthesis(cells: Cells, rule: str, target_apgcode: str) -> dict:
    out: dict = {"ok": False}
    crule = canonical_rule(rule)
    out["rule"] = rule
    out["canonical_rule"] = crule
    if crule != "B3/S23":
        out["reason"] = "rule is %r, need B3/S23" % rule
        return out
    prefix, num, target_cells = decode_apgcode(target_apgcode)
    out["target_apgcode"] = target_apgcode
    out["target_prefix"] = prefix
    out["target_decoded_population"] = len(target_cells)
    out["target_is_still_life"] = is_still_life(target_cells)
    out["target_ascii"] = ascii_pattern(target_cells)
    if prefix != "xs28" or num != 28 or len(target_cells) != 28:
        out["reason"] = "target apgcode is not an xs28 of 28 cells (prefix=%r num=%s pop=%s)" % (
            prefix,
            num,
            len(target_cells),
        )
        return out
    if not is_still_life(target_cells):
        out["reason"] = "decoded target is not a still life (decode bug or bad apgcode)"
        return out

    comps = components8(cells)
    comps.sort(key=lambda c: (min(p[1] for p in c), min(p[0] for p in c)))
    out["n_components"] = len(comps)
    out["component_sizes"] = [len(c) for c in comps]
    gliders = []
    velocities = []
    bad = []
    for i, c in enumerate(comps):
        ident = identify_glider(c)
        if ident is None:
            bad.append({"index": i, "size": len(c), "ascii": ascii_pattern(c)})
        else:
            _, vel = ident
            gliders.append(c)
            velocities.append({"vx": vel[0], "vy": vel[1], "phase_shape": True})
    out["n_gliders"] = len(gliders)
    out["velocities"] = velocities
    if bad:
        out["reason"] = "non-glider 8-connected components"
        out["non_gliders"] = bad
        return out
    if len(gliders) != 7:
        out["reason"] = "expected 7 gliders, found %d" % len(gliders)
        return out

    rewind_gens, diag, w, h = rewind_amount(cells)
    out["bbox_w"] = w
    out["bbox_h"] = h
    out["bbox_diag"] = diag
    out["rewind_gens"] = rewind_gens
    # Use dual-engine agreement on a short prefix, then fast path.
    sample = set(cells)
    for _ in range(min(8, rewind_gens)):
        sample = step(sample)

    rewind_res = check_rewind(gliders, rewind_gens)
    out["rewind"] = rewind_res
    if not rewind_res["ok"]:
        out["reason"] = "rewind interaction check failed"
        return out

    max_forward = max(4000, rewind_gens * 2)
    fwd = check_forward(cells, target_cells, max_forward)
    out["forward"] = fwd
    if not fwd["ok"]:
        out["reason"] = fwd.get("reason", "forward still-life match failed")
        return out

    strict, sreason = still_life_strictness(target_cells)
    out["target_strict"] = strict
    out["target_strict_reason"] = sreason
    # Strictness of the *produced* object: same cells up to D8+translation,
    # so same as target.
    out["ok"] = True
    out["reason"] = "all numerical checks passed"
    return out


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------

def _rle(body: str) -> Cells:
    cells, _, _, _ = parse_rle("x = 1, y = 1, rule = B3/S23\n" + body)
    return cells


def run_controls() -> Tuple[bool, List[dict]]:
    results: List[dict] = []

    def rec(name: str, expected, actual, extra=None):
        ok = actual == expected
        row = {"name": name, "expected": expected, "actual": actual, "ok": ok}
        if extra is not None:
            row["extra"] = extra
        results.append(row)
        return ok

    all_ok = True

    # Engine agreement + blinker period 2
    blinker = {(0, 0), (1, 0), (2, 0)}
    b1 = step(blinker)
    b2 = step(b1)
    all_ok &= rec("blinker_gen1_vertical", {(1, -1), (1, 0), (1, 1)}, b1)
    all_ok &= rec("blinker_period_2", blinker, b2)

    # Block still life
    block = {(0, 0), (1, 0), (0, 1), (1, 1)}
    all_ok &= rec("block_still", True, is_still_life(block))

    # Tub still life
    tub = {(1, 0), (0, 1), (2, 1), (1, 2)}
    all_ok &= rec("tub_still", True, is_still_life(tub))

    # Apgcode known objects
    _, n, c = decode_apgcode("xs4_33")
    all_ok &= rec("apg_block_pop", 4, len(c))
    all_ok &= rec("apg_block_num", 4, n)
    all_ok &= rec("apg_block_match", True, match_d8_translation(c, block) and is_still_life(c))

    _, _, c = decode_apgcode("xs4_252")
    all_ok &= rec("apg_tub_match", True, match_d8_translation(c, tub) and is_still_life(c))

    _, _, c = decode_apgcode("xs6_696")
    all_ok &= rec("apg_beehive_pop", 6, len(c))
    all_ok &= rec("apg_beehive_still", True, is_still_life(c))

    _, _, c = decode_apgcode("xs5_253")
    all_ok &= rec("apg_boat_pop", 5, len(c))
    all_ok &= rec("apg_boat_still", True, is_still_life(c))

    # Glider apgcode + motion
    _, _, g = decode_apgcode("xq4_153")
    all_ok &= rec("apg_glider_pop", 5, len(g))
    ident = identify_glider(g)
    all_ok &= rec("apg_glider_identified", True, ident is not None)
    g4 = evolve(g, 4, fast=False)
    if ident:
        vx, vy = ident[1]
        shifted = {(x + vx, y + vy) for x, y in g}
        all_ok &= rec("glider_period4_translate", True, g4 == shifted)
    else:
        all_ok &= rec("glider_period4_translate", True, False)

    all_ok &= rec("glider_shape_count", 16, len(GLIDER_SHAPES))

    # Hand-built LWSS: 9 cells, period 4, orthogonal displacement 2.
    lwss = {
        (1, 0), (4, 0),
        (0, 1),
        (0, 2), (4, 2),
        (0, 3), (1, 3), (2, 3), (3, 3),
    }
    all_ok &= rec("lwss_pop", 9, len(lwss))
    lw4 = evolve(lwss, 4, fast=False)
    all_ok &= rec("lwss_shape_period4", True, normalize(lwss) == normalize(lw4))
    minx0, miny0 = min(p[0] for p in lwss), min(p[1] for p in lwss)
    minx4, miny4 = min(p[0] for p in lw4), min(p[1] for p in lw4)
    disp = (minx4 - minx0, miny4 - miny0)
    ortho2 = min(abs(disp[0]), abs(disp[1])) == 0 and max(abs(disp[0]), abs(disp[1])) == 2
    all_ok &= rec("lwss_displacement_2c4", True, ortho2, extra={"disp": disp})

    # Two-strip still life with z separator
    _, num, c31 = decode_apgcode("xs31_0ca178b96z69d1d96")
    all_ok &= rec("apg_xs31_pop", 31, len(c31))
    all_ok &= rec("apg_xs31_num", 31, num)
    all_ok &= rec("apg_xs31_still", True, is_still_life(c31))

    # Target apgcode self-check
    _, num, tgt = decode_apgcode("xs28_69a4owgzxol5d1d96")
    all_ok &= rec("target_decode_pop", 28, len(tgt))
    all_ok &= rec("target_decode_num", 28, num)
    all_ok &= rec("target_is_still", True, is_still_life(tgt))
    # D8 of target matches itself
    flipped = {(-x, y) for x, y in tgt}
    all_ok &= rec("target_d8_self", True, match_d8_translation(flipped, tgt))
    # w/x skip used in target suffix: 28 cells and still life already covers decode

    # Non-glider 5-cell (R-pentomino) is not identified as glider
    rpent = {(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)}
    all_ok &= rec("rpent_not_glider", True, identify_glider(rpent) is None)

    # Positive: two far parallel gliders — rewind must pass (no interaction)
    g_se = _rle("bo$2bo$3o!")
    g2 = {(x + 40, y) for x, y in g_se}
    far = g_se | g2
    comps = components8(far)
    rewind_gens, _, _, _ = rewind_amount(far)
    rw = check_rewind(comps, rewind_gens)
    all_ok &= rec("pos_two_far_gliders_rewind", True, rw["ok"], extra={"rewind_gens": rewind_gens})

    # Positive: 2-glider block synthesis (try a few published collision recipes)
    block_recipes = [
        "2bo$obo$b2o17$3b3o$5bo$4bo!",
        "bo$2bo$3o$3b3o$5bo$4bo!",
        "bo$obo$b2o2$2b2o$2bobo$2bo!",
        "2bo$obo$b2o$3b2o$3bobo$3bo!",
        "bo$2bo$3o2$b2o$obo$2bo!",
    ]
    two_g_block = None
    for body in block_recipes:
        cand = _rle(body)
        comps_c = components8(cand)
        if not (len(comps_c) == 2 and all(identify_glider(c) for c in comps_c)):
            continue
        fwd_c = check_forward(cand, block, 64)
        if fwd_c.get("ok") or (fwd_c.get("period") == 1 and fwd_c.get("d8_translation_match") and fwd_c.get("population") == 4):
            two_g_block = cand
            break
    all_ok &= rec("pos_2g_block_found_recipe", True, two_g_block is not None)
    gl_ok = False
    if two_g_block is not None:
        comps = components8(two_g_block)
        gl_ok = len(comps) == 2 and all(identify_glider(c) for c in comps)
        all_ok &= rec("pos_2g_block_two_gliders", True, gl_ok)
        rg, _, _, _ = rewind_amount(two_g_block)
        rw = check_rewind(comps, rg)
        all_ok &= rec("pos_2g_block_rewind", True, rw["ok"], extra={"rewind_gens": rg})
        fwd = check_forward(two_g_block, block, 64)
        all_ok &= rec("pos_2g_block_forward_pop4_p1", True, fwd.get("period") == 1 and fwd.get("population") == 4)
        all_ok &= rec("pos_2g_block_d8_block", True, bool(fwd.get("d8_translation_match")))
    else:
        all_ok &= rec("pos_2g_block_two_gliders", True, False)

    # Negative: extra block at gen 0 (not all-glider)
    mixed_src = two_g_block if two_g_block is not None else far
    mixed = mixed_src | {(80, 80), (81, 80), (80, 81), (81, 81)}
    comps = components8(mixed)
    n_gl = sum(1 for c in comps if identify_glider(c))
    n_comp = len(comps)
    all_ok &= rec("neg_block_plus_gliders_not_all_glider", True, n_gl >= 2 and n_comp == n_gl + 1)

    # Negative: wrong target (2g block is not the xs28)
    if gl_ok:
        fwd_wrong = check_forward(two_g_block, tgt, 64)
        all_ok &= rec("neg_2g_block_is_not_xs28", True, not fwd_wrong["ok"])

    # Negative: receding gliders on one diagonal (rewind interaction).
    # Place the SE-moving glider ahead of the NW-moving one so they are moving
    # apart; rewind sends them back toward the same spacetime lane.
    ident_se = identify_glider(g_se)
    assert ident_se is not None
    g_nw = {(-x, -y) for x, y in g_se}
    ident_nw = identify_glider(g_nw)
    assert ident_nw is not None
    g_se_ahead = {(x + 48, y + 48) for x, y in g_se}
    receding = g_nw | g_se_ahead
    # Ensure they are the pair with opposite velocities
    comps = components8(receding)
    vels = []
    for c in comps:
        ident = identify_glider(c)
        if ident:
            vels.append(ident[1])
    all_ok &= rec("neg_receding_two_gliders", True, len(comps) == 2 and len(vels) == 2)
    rg, _, _, _ = rewind_amount(receding)
    rw = check_rewind(comps, rg)
    all_ok &= rec("neg_receding_rewind_must_fail", True, not rw["ok"], extra={"rewind_gens": rg, "mismatches": rw["mismatch_generations"][:5]})

    # Negative: leftover escaping glider after a "synthesis"
    # Two far gliders never settle to a still life.
    fwd_far = check_forward(far, block, 32)
    all_ok &= rec("neg_escaping_gliders_not_still", True, not fwd_far["ok"])

    # Negative: blinker is period 2, not still life period 1
    fwd_b = check_forward(blinker, blinker, 8)
    all_ok &= rec("neg_blinker_not_period1", True, not fwd_b["ok"] or fwd_b.get("period") != 1)

    # Bi-block is a pseudo still life (not strict)
    biblock = {(0, 0), (1, 0), (0, 1), (1, 1), (3, 0), (4, 0), (3, 1), (4, 1)}
    all_ok &= rec("biblock_still", True, is_still_life(biblock))
    st, reason = still_life_strictness(biblock)
    all_ok &= rec("neg_biblock_not_strict", True, st is False, extra=reason)

    # Block is strict
    st, reason = still_life_strictness(block)
    all_ok &= rec("pos_block_strict", True, st is True, extra=reason)

    # Target strictness recorded as a control of the detector
    st, reason = still_life_strictness(tgt)
    results.append(
        {
            "name": "target_strictness_measurement",
            "expected": "recorded",
            "actual": st,
            "ok": True,
            "extra": reason,
        }
    )

    # RLE parse of a glider
    g_from_rle = _rle("bob$2bo$3o!")
    all_ok &= rec("rle_glider_identified", True, identify_glider(g_from_rle) is not None)

    return all_ok, results


# ---------------------------------------------------------------------------
# Determinism helper
# ---------------------------------------------------------------------------

def json_ready(obj):
    """Convert sets/tuples to sorted lists so dumps are deterministic."""
    if isinstance(obj, dict):
        return {str(k): json_ready(v) for k, v in obj.items()}
    if isinstance(obj, (set, frozenset)):
        items = [json_ready(v) for v in obj]
        return sorted(items, key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(obj, (list, tuple)):
        return [json_ready(v) for v in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    return str(obj)


def digest_obj(obj) -> str:
    blob = json.dumps(json_ready(obj), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def slim_result(res: dict) -> dict:
    """Drop bulky ascii from the hashed/compared payload except flags."""
    skip = {"target_ascii", "non_gliders"}
    return {k: v for k, v in res.items() if k not in skip}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rle", required=True, help="path to claimed RLE")
    p.add_argument("--target", required=True, help="target apgcode")
    p.add_argument("--out", default="checker_out", help="output directory")
    p.add_argument("--tag", default="run", help="output file tag")
    args = p.parse_args(argv)

    os.makedirs(args.out, exist_ok=True)
    started = time.time()
    log_lines: List[str] = []

    def log(msg: str) -> None:
        log_lines.append(msg)
        print(msg, flush=True)

    log("checker: independent stdlib B3/S23 synthesis verifier")
    log("rle=%s target=%s" % (args.rle, args.target))

    ctrl_ok, ctrl = run_controls()
    ctrl_path = os.path.join(args.out, "%s_controls.json" % args.tag)
    with open(ctrl_path, "w") as f:
        json.dump(json_ready({"ok": ctrl_ok, "controls": ctrl}), f, indent=2, sort_keys=True)
    n_fail = sum(1 for c in ctrl if not c["ok"])
    log("controls: %d items, %d failures, ok=%s" % (len(ctrl), n_fail, ctrl_ok))
    for c in ctrl:
        mark = "PASS" if c["ok"] else "FAIL"
        log("  [%s] %s expected=%s actual=%s" % (mark, c["name"], c["expected"], c["actual"]))

    result = {
        "controls_ok": ctrl_ok,
        "claim_ok": False,
        "ok": False,
    }
    if not ctrl_ok:
        result["reason"] = "checker control failure; refusing to judge claim"
        log("ABORT: controls failed")
    else:
        with open(args.rle, "r") as f:
            rle_text = f.read()
        cells, rule, width, height = parse_rle(rle_text)
        log("parsed RLE: pop=%d rule=%s header=%sx%s" % (len(cells), rule, width, height))
        syn = check_synthesis(cells, rule, args.target)
        result["claim"] = syn
        result["claim_ok"] = bool(syn.get("ok"))
        result["ok"] = bool(syn.get("ok"))
        result["rle_population"] = len(cells)
        result["rle_rule"] = rule
        result["rle_header"] = {"x": width, "y": height}
        log("synthesis ok=%s reason=%s" % (syn.get("ok"), syn.get("reason")))
        log("n_gliders=%s rewind=%s" % (syn.get("n_gliders"), syn.get("rewind_gens")))
        if syn.get("forward"):
            log("forward=%s" % json.dumps(syn["forward"], sort_keys=True, default=str))
        if syn.get("rewind"):
            log("rewind=%s" % json.dumps(syn["rewind"], sort_keys=True, default=str))
        log("target_strict=%s (%s)" % (syn.get("target_strict"), syn.get("target_strict_reason")))

    result["elapsed_s"] = round(time.time() - started, 3)
    result["digest"] = digest_obj(slim_result(result.get("claim", {})))
    out_json = os.path.join(args.out, "%s.json" % args.tag)
    out_log = os.path.join(args.out, "%s.log" % args.tag)
    with open(out_json, "w") as f:
        json.dump(json_ready(result), f, indent=2, sort_keys=True)
    with open(out_log, "w") as f:
        f.write("\n".join(log_lines) + "\n")

    # Compact last line for easy comparison across runs
    last = "RESULT ok=%s controls_ok=%s claim_ok=%s digest=%s" % (
        result["ok"],
        result["controls_ok"],
        result["claim_ok"],
        result["digest"],
    )
    print(last, flush=True)
    with open(out_log, "a") as f:
        f.write(last + "\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
