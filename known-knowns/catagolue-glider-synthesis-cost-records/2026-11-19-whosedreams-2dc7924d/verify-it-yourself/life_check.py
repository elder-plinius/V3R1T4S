#!/usr/bin/env python3
"""Independent glider-synthesis checker for bank target catagolue-glider-synthesis-cost-records.

Standard library only (no lifelib, no Shinjuku). Written from the bank's success criterion:
 (1) generation 0 is only gliders, each its own 8-connected component;
 (2) rewinding every glider T generations along its own path gives no glider-glider interaction
     (checked for T = 4 x longer bounding-box side and T = 4 x ceil(bounding-box diagonal));
 (3) run forward until a state repeats exactly; the final cells must be exactly the target apgcode's
     object (decoded from the apgcode, compared under 8 symmetries and translation), nothing else;
 (4) count gliders and, if --table-cost is given, require count < table cost.
Usage:
  python3 life_check.py --rle FILE --target APGCODE [--table-cost N] [--controls] [--drop K]
Last output line: PASS or FAIL.
"""
import argparse, math, re, sys

def parse_rle(text):
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
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
        if ch == "b" or ch == ".":
            x += n
        elif ch == "o" or ch == "A":
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
            raise ValueError("unexpected RLE character %r" % ch)
    return rule, cells

def step(cells):
    counts = {}
    for (x, y) in cells:
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

def normalize(cells):
    if not cells:
        return frozenset()
    mx = min(x for x, _ in cells); my = min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)

TF = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
      lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]

def all_forms(cells):
    return {normalize({f(x, y) for x, y in cells}) for f in TF}

BASE_GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
GLIDER_SHAPES = set()
_g = set(BASE_GLIDER)
for _ in range(4):
    GLIDER_SHAPES |= all_forms(_g)
    _g = step(_g)

def components(cells):
    left, comps = set(cells), []
    while left:
        seed = left.pop(); comp = {seed}; stack = [seed]
        while stack:
            x, y = stack.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    k = (x + dx, y + dy)
                    if k in left:
                        left.remove(k); comp.add(k); stack.append(k)
        comps.append(comp)
    return comps

def glider_direction(comp):
    later = run(comp, 4)
    if normalize(later) != normalize(comp):
        return None
    dx = min(x for x, _ in later) - min(x for x, _ in comp)
    dy = min(y for _, y in later) - min(y for _, y in comp)
    return (dx, dy) if abs(dx) == 1 and abs(dy) == 1 else None

def decode_apgcode(code):
    m = re.fullmatch(r"x([sp])(\d+)_([0-9a-z]+)", code)
    if not m:
        raise ValueError("only xsN_ / xpN_ apgcodes are supported: %s" % code)
    kind, num, w = m.group(1), int(m.group(2)), m.group(3)
    cells = set()
    for s, strip in enumerate(w.split("z")):
        col, i = 0, 0
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

def rewind_ok(gliders, T):
    """Each glider moved back T/4 cells against its direction (same phase), run T generations;
    at every generation the whole must equal the union of the gliders run separately."""
    assert T % 4 == 0
    back = []
    for comp, (dx, dy) in gliders:
        k = T // 4
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

def forward_to_periodic(cells, max_gen=40000):
    seen = {}
    g = 0
    while g <= max_gen:
        key = frozenset(cells)
        if key in seen:
            return seen[key], g - seen[key], cells
        seen[key] = g
        if len(seen) > 300:   # keep memory small: only recent states matter for exact repeats of short period
            for k in [k for k, v in seen.items() if v < g - 256]:
                del seen[k]
        cells = step(cells)
        g += 1
    return None, None, cells

def check(cells, target, table_cost=None, quiet=False, skip_rewind=False):
    say = (lambda *a: None) if quiet else print
    res = {"ok": False, "target": target}
    comps = components(cells)
    gl = []
    for c in comps:
        if normalize(c) not in GLIDER_SHAPES:
            res["error"] = "generation-0 component of %d cells is not a glider" % len(c)
            return res
        d = glider_direction(c)
        if d is None:
            res["error"] = "glider direction not found"
            return res
        gl.append((c, d))
    res["n_gliders"] = len(gl)
    say("gen0: population %d, %d components, all gliders" % (len(cells), len(comps)))
    xs = [x for x, _ in cells]; ys = [y for _, y in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    t1 = 4 * max(w, h); t2 = 4 * math.ceil(math.hypot(w, h))
    for T in ([] if skip_rewind else sorted({t1 + (-t1) % 4, t2 + (-t2) % 4})):
        ok, at = rewind_ok(gl, T)
        say("rewind T=%d: %s" % (T, "ok" if ok else "interaction at rewound generation %d" % at))
        if not ok:
            res["error"] = "rewind failed at T=%d" % T
            return res
    res["rewind_ok"] = True
    start, period, final = forward_to_periodic(set(cells))
    if start is None:
        res["error"] = "no exact repeat within the generation cap (escaping ship or long transient)"
        return res
    res["periodic_from"], res["period"], res["final_population"] = start, period, len(final)
    say("forward: exact repeat from generation %d, period %d, population %d" % (start, period, len(final)))
    kind, num, tcells = decode_apgcode(target)
    want_period = 1 if kind == "s" else num
    if period != want_period:
        res["error"] = "period %d, target wants %d" % (period, want_period)
        return res
    phases, cur = [], set(final)
    for _ in range(period):
        phases.append(normalize(cur)); cur = step(cur)
    tforms = all_forms(tcells)
    tforms |= {f for p in range(1, want_period) for f in all_forms(run(tcells, p))}
    if not any(p in tforms for p in phases):
        res["error"] = "final cells are not the target object (or extra cells remain)"
        return res
    res["final_matches_target"] = True
    say("final object: matches %s exactly, nothing else live" % target)
    if table_cost is not None:
        res["table_cost"] = table_cost
        if not len(gl) < table_cost:
            res["error"] = "%d gliders is not strictly fewer than the table cost %d" % (len(gl), table_cost)
            return res
        say("cost: %d gliders < table cost %d" % (len(gl), table_cost))
    res["ok"] = True
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rle", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--table-cost", type=int)
    ap.add_argument("--controls", action="store_true", help="also run the drop-one-glider controls")
    ap.add_argument("--control-positive", help="apgcode expected when the last-arriving glider is dropped")
    ap.add_argument("--controls-skip-rewind", action="store_true",
                    help="skip the rewind test inside the drop-one controls (dropping a glider cannot add an interaction)")
    a = ap.parse_args()
    rule, cells = parse_rle(open(a.rle).read())
    if rule.upper().replace("/", "") not in ("B3S23",):
        print("rule %s is not B3/S23" % rule); print("FAIL"); return 1
    r = check(cells, a.target, a.table_cost)
    print("result:", {k: v for k, v in r.items()})
    good = r["ok"]
    if a.controls and good:
        gl = components(cells)
        hits = 0
        for i, c in enumerate(sorted(gl, key=lambda c: min(c))):
            sub = set(cells) - c
            rr = check(sub, a.target, None, quiet=True, skip_rewind=a.controls_skip_rewind)
            line = "control drop glider %2d at %s: target built? %s" % (i, min(c), rr["ok"])
            if a.control_positive and not rr["ok"]:
                rp = check(sub, a.control_positive, None, quiet=True, skip_rewind=a.controls_skip_rewind)
                if rp["ok"]:
                    hits += 1
                    line += "; builds %s (positive control)" % a.control_positive
            print(line)
            if rr["ok"]:
                good = False
        if a.control_positive:
            print("positive controls found: %d" % hits)
            if hits < 1:
                good = False
    print("PASS" if good else "FAIL")
    return 0 if good else 1

if __name__ == "__main__":
    sys.exit(main())
