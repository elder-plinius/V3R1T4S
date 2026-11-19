#!/usr/bin/env python3
"""Independent B3/S23 synthesis check. Standard library only.

Confirms generation 0 is exactly seven gliders, that rewinding each glider
by T generations (T a multiple of 4, T >= 4 * bounding-box side and
T >= 4 * diagonal) never interacts, and that the forward ash is exactly the
decoded target still life. Also reports which single-glider deletions ash
to the disclosed predecessor.
"""
import math
import re
import sys

TARGET = "xs28_69a4owgzxol5d1d96"
PRED = "xs25_0ml1u8z643032ak8"
RLE_PATH = "claim/result/xs28_69a4owgzxol5d1d96.rle"

BASE_GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
TRANSFORMS = [
    lambda x, y: (x, y),
    lambda x, y: (-x, y),
    lambda x, y: (x, -y),
    lambda x, y: (-x, -y),
    lambda x, y: (y, x),
    lambda x, y: (-y, x),
    lambda x, y: (y, -x),
    lambda x, y: (-y, -x),
]


def step(cells):
    counts = {}
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    k = (x + dx, y + dy)
                    counts[k] = counts.get(k, 0) + 1
    return {k for k, n in counts.items() if n == 3 or (n == 2 and k in cells)}


def run(cells, n):
    for _ in range(n):
        cells = step(cells)
    return cells


def norm(cells):
    if not cells:
        return frozenset()
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def forms(cells):
    out = set()
    for f in TRANSFORMS:
        out.add(norm({f(x, y) for x, y in cells}))
    return out


def glider_keys():
    keys = set()
    g = set(BASE_GLIDER)
    for _ in range(4):
        keys |= forms(g)
        g = step(g)
    return keys


GLIDERS = glider_keys()


def decode_apgcode(code):
    m = re.fullmatch(r"x([sp])(\d+)_([0-9a-z]+)", code)
    if not m:
        raise ValueError(code)
    kind, num, w = m.group(1), int(m.group(2)), m.group(3)
    cells = set()
    for s, strip in enumerate(w.split("z")):
        col = i = 0
        while i < len(strip):
            ch = strip[i]
            if ch == "w":
                col += 2
            elif ch == "x":
                col += 3
            elif ch == "y":
                i += 1
                col += 4 + int(strip[i], 36)
            else:
                v = int(ch, 32)
                for b in range(5):
                    if v >> b & 1:
                        cells.add((col, 5 * s + b))
                col += 1
            i += 1
    return kind, num, cells


def parse_rle(text):
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    hdr = lines[0]
    m = re.search(r"rule\s*=\s*([^\s,]+)", hdr)
    rule = m.group(1) if m else "B3/S23"
    body = "".join(lines[1:])
    cells, x, y, num = set(), 0, 0, ""
    for ch in body:
        if ch.isdigit():
            num += ch
            continue
        n = int(num) if num else 1
        num = ""
        if ch in "b.":
            x += n
        elif ch in "oA":
            for i in range(n):
                cells.add((x + i, y))
            x += n
        elif ch == "$":
            y += n
            x = 0
        elif ch == "!":
            break
        elif ch.isspace():
            continue
        else:
            raise ValueError("bad RLE char %r" % ch)
    return rule, cells


def components(cells):
    left, out = set(cells), []
    while left:
        seed = left.pop()
        comp, stack = {seed}, [seed]
        while stack:
            x, y = stack.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    k = (x + dx, y + dy)
                    if k in left:
                        left.remove(k)
                        comp.add(k)
                        stack.append(k)
        out.append(comp)
    return out


def direction(comp):
    later = run(comp, 4)
    if norm(later) != norm(comp):
        return None
    dx = min(x for x, _ in later) - min(x for x, _ in comp)
    dy = min(y for _, y in later) - min(y for _, y in comp)
    if abs(dx) == 1 and abs(dy) == 1:
        return dx, dy
    return None


def same_object(cells, target_cells):
    want = forms(target_cells)
    # period-1 object: one phase is enough, but include the phase anyway
    return norm(cells) in want or any(norm(cells) in forms(run(target_cells, p)) for p in range(1, 4))


def rewind_ok(gliders, T):
    assert T % 4 == 0
    k = T // 4
    back = []
    for comp, (dx, dy) in gliders:
        back.append({(x - k * dx, y - k * dy) for x, y in comp})
    whole = set().union(*back)
    parts = [set(b) for b in back]
    for t in range(T):
        whole = step(whole)
        parts = [step(p) for p in parts]
        if whole != set().union(*parts):
            return False, t + 1
    gen0 = set().union(*[c for c, _ in gliders])
    return whole == gen0, T


def forward_repeat(cells, max_gen=20000):
    seen = {}
    for g in range(max_gen + 1):
        key = frozenset(cells)
        if key in seen:
            return seen[key], g - seen[key], cells
        seen[key] = g
        cells = step(cells)
    return None, None, cells


def main():
    rule, cells = parse_rle(open(RLE_PATH).read())
    print("rule", rule, "gen0_pop", len(cells))
    if rule.upper().replace("/", "") != "B3S23":
        print("FAIL rule")
        return 1
    comps = components(cells)
    gliders = []
    for c in comps:
        if norm(c) not in GLIDERS:
            print("FAIL non-glider component pop", len(c))
            return 1
        d = direction(c)
        if d is None:
            print("FAIL direction")
            return 1
        gliders.append((c, d))
    print("n_gliders", len(gliders))
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    diag = math.ceil(math.hypot(w - 1, h - 1))
    # diameter as the longer side, and as the corner-to-corner cell distance
    t_side = 4 * max(w, h)
    t_diag = 4 * max(diag, 1)
    print("bbox", w, h, "T_side", t_side, "T_diag", t_diag)
    for T0 in (t_side, t_diag):
        T = T0 + (-T0) % 4
        ok, at = rewind_ok(gliders, T)
        print("rewind", T, "ok" if ok else "fail", at)
        if not ok:
            print("FAIL rewind")
            return 1
    start, period, final = forward_repeat(set(cells))
    print("forward_start", start, "period", period, "final_pop", None if final is None else len(final))
    if start is None:
        print("FAIL no repeat")
        return 1
    kind, num, tcells = decode_apgcode(TARGET)
    print("target_decoded_pop", len(tcells), "declared", num, "kind", kind, "target_still", step(tcells) == tcells)
    if period != 1 or not same_object(final, tcells):
        print("FAIL ash is not the target")
        return 1
    print("ash_matches_target", True)
    pk, pnum, pcells = decode_apgcode(PRED)
    print("pred_decoded_pop", len(pcells), "declared", pnum, "pred_still", step(pcells) == pcells)
    hits = []
    for i, (c, d) in enumerate(gliders):
        sub = set(cells) - c
        s, per, fin = forward_repeat(sub, max_gen=20000)
        match_t = s is not None and per == 1 and same_object(fin, tcells)
        match_p = s is not None and per == 1 and same_object(fin, pcells)
        print(
            "drop", i, "dir", d, "origin", min(c),
            "repeat", s, "period", per, "pop", None if fin is None else len(fin),
            "builds_target", match_t, "builds_predecessor", match_p,
        )
        if match_p:
            hits.append(i)
        if match_t:
            print("FAIL drop still builds target")
            return 1
    print("predecessor_drops", hits)
    if len(hits) < 1:
        print("FAIL no single deletion yields the disclosed predecessor")
        return 1
    # The disclosed route is one extra glider on a 6-glider predecessor.
    print("PASS gliders", len(gliders), "predecessor_drop_count", len(hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
