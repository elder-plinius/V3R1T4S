#!/usr/bin/env python3
"""Independent B3/S23 glider-synthesis + strict-still-life checker.

Stdlib only. Does not import claim/code. Written from TARGET_CRITERION.md:
  (1) gen0 is only gliders, each an 8-connected component
  (2) rewind each glider T gens along its trajectory, T >= 4*diameter,
      and every generation of the rewound interval has no interaction
  (3) forward to an exact periodic state: cells are exactly the target
      still life (apgcode, 8 symmetries + translation), no debris
  (4) target is a strict still life (cannot be partitioned into two
      nonempty still lifes)
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path


def parse_rle(text: str):
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    hdr = lines[0]
    m = re.search(r"rule\s*=\s*([^\s,]+)", hdr, re.I)
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
            raise ValueError("unexpected RLE character %r" % ch)
    return rule, cells


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


def neighbors8(x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                yield x + dx, y + dy


def live_neighbor_count(cells, p):
    x, y = p
    return sum(1 for q in neighbors8(x, y) if q in cells)


def normalize(cells):
    if not cells:
        return frozenset()
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


TF = [
    lambda x, y: (x, y),
    lambda x, y: (-x, y),
    lambda x, y: (x, -y),
    lambda x, y: (-x, -y),
    lambda x, y: (y, x),
    lambda x, y: (-y, x),
    lambda x, y: (y, -x),
    lambda x, y: (-y, -x),
]


def all_forms(cells):
    return {normalize({f(x, y) for x, y in cells}) for f in TF}


# Standard glider (SE-going, one phase) and its 4 phases, all 8 symmetries.
BASE_GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
GLIDER_SHAPES = set()
_g = set(BASE_GLIDER)
for _ in range(4):
    GLIDER_SHAPES |= all_forms(_g)
    _g = step(_g)


def components(cells):
    left, comps = set(cells), []
    while left:
        seed = left.pop()
        comp = {seed}
        stack = [seed]
        while stack:
            x, y = stack.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    k = (x + dx, y + dy)
                    if k in left:
                        left.remove(k)
                        comp.add(k)
                        stack.append(k)
        comps.append(comp)
    return comps


def glider_direction(comp):
    later = run(comp, 4)
    if normalize(later) != normalize(comp):
        return None
    dx = min(x for x, _ in later) - min(x for x, _ in comp)
    dy = min(y for _, y in later) - min(y for _, y in later)
    # min() over y of later vs comp
    dy = min(y for _, y in later) - min(y for _, y in comp)
    if abs(dx) == 1 and abs(dy) == 1:
        return (dx, dy)
    return None


def decode_apgcode(code: str):
    m = re.fullmatch(r"x([spq])(\d+)_([0-9a-z]+)", code)
    if not m:
        raise ValueError("unsupported apgcode: %s" % code)
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
                if i >= len(strip):
                    raise ValueError("truncated y-skip in %s" % code)
                col += 4 + int(strip[i], 36)
            else:
                v = int(ch, 32)
                for b in range(5):
                    if v >> b & 1:
                        cells.add((col, 5 * s + b))
                col += 1
            i += 1
    return kind, num, cells


def is_still_life(cells) -> bool:
    return step(cells) == cells


def bbox(cells):
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    return min(xs), min(ys), max(xs), max(ys)


class UF:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def strict_still_life(cells) -> tuple[bool, str]:
    """A still life is strict iff it cannot be partitioned into two nonempty still lifes.

    Forced grouping: any live cell with exactly 2 live neighbours in S, together
    with those two neighbours, must lie in the same part of any still-life partition
    (otherwise that cell would have fewer than 2 neighbours in its part and die).
    We then enumerate subsets of the resulting forced components.
    """
    cells = set(cells)
    if not cells:
        return False, "empty"
    if not is_still_life(cells):
        return False, "not a still life (step differs)"
    if any(live_neighbor_count(cells, p) not in (2, 3) for p in cells):
        return False, "a live cell has neighbour count outside {2,3}"

    uf = UF(cells)
    for p in cells:
        nbs = [q for q in neighbors8(*p) if q in cells]
        if len(nbs) == 2:
            uf.union(p, nbs[0])
            uf.union(p, nbs[1])
            uf.union(nbs[0], nbs[1])

    groups = {}
    for p in cells:
        groups.setdefault(uf.find(p), []).append(p)
    keys = list(groups)
    m = len(keys)
    islands = components(cells)

    # Any 8-island of a still life is itself a still life (survival is local to
    # the island; births cannot appear in a subset of a still life).
    if len(islands) >= 2:
        if all(is_still_life(isl) for isl in islands):
            return False, "pseudo: %d 8-islands, each a still life" % len(islands)

    if m == 1:
        return True, "strict: single forced component (%d cells, %d island(s))" % (
            len(cells),
            len(islands),
        )

    if m > 20:
        return False, "too many forced components (%d) to enumerate" % m

    # Enumerate nonempty proper subsets of forced components.
    n_sub = 1 << m
    for mask in range(1, n_sub - 1):
        A = set()
        for i, k in enumerate(keys):
            if mask & (1 << i):
                A.update(groups[k])
        B = cells - A
        if is_still_life(A) and is_still_life(B):
            return False, "pseudo: partition %d+%d cells" % (len(A), len(B))
    return True, "strict: %d forced components, no still-life partition" % m


def rewind_ok(gliders, T):
    """Translate each glider back T/4 cells, then check every generation 1..T
    that the union of independently evolved gliders equals the jointly evolved
    pattern, and that generation T recovers gen0.
    """
    if T % 4:
        raise ValueError("T must be a multiple of 4")
    k = T // 4
    back = []
    for comp, (dx, dy) in gliders:
        back.append({(x - k * dx, y - k * dy) for x, y in comp})
    whole = set().union(*back)
    parts = [set(b) for b in back]
    for t in range(T):
        whole = step(whole)
        parts = [step(p) for p in parts]
        union_parts = set().union(*parts)
        if whole != union_parts:
            return False, t + 1
    gen0 = set().union(*(c for c, _ in gliders))
    if whole != gen0:
        return False, T
    return True, T


def forward_to_periodic(cells, max_gen=40000):
    seen = {}
    g = 0
    while g <= max_gen:
        key = frozenset(cells)
        if key in seen:
            return seen[key], g - seen[key], cells
        seen[key] = g
        if len(seen) > 400:
            for k in [k for k, v in seen.items() if v < g - 300]:
                del seen[k]
        cells = step(cells)
        g += 1
    return None, None, cells


def encode_apgcode_xs(cells) -> str:
    """Canonical xs apgcode (minimum among 8 symmetries), for cross-check."""
    best = None
    for f in TF:
        form = {f(x, y) for x, y in cells}
        mx = min(x for x, _ in form)
        my = min(y for _, y in form)
        form = {(x - mx, y - my) for x, y in form}
        maxy = max(y for _, y in form)
        nstrips = (maxy // 5) + 1
        maxx = max(x for x, _ in form)
        parts = []
        for s in range(nstrips):
            cols = []
            for col in range(maxx + 1):
                v = 0
                for b in range(5):
                    if (col, 5 * s + b) in form:
                        v |= 1 << b
                cols.append(v)
            # trim trailing zeros
            while cols and cols[-1] == 0:
                cols.pop()
            # encode skips of zero columns using w/x/y, nonempty as base32
            enc = []
            i = 0
            while i < len(cols):
                if cols[i] == 0:
                    zrun = 0
                    while i < len(cols) and cols[i] == 0:
                        zrun += 1
                        i += 1
                    # remaining zeros to skip before next nonzero / end
                    # w=+2, x=+3, yK=+4+int(K,36). Also a '0' column is a zero quintet.
                    # Standard: zero quintet character is '0'; long skips use w/x/y
                    # We emit skip tokens then the next value. At end, trailing zeros already trimmed.
                    # For interior zeros, apgcode uses:
                    #  1 zero col: '0'
                    #  2: 'w'
                    #  3: 'x'
                    #  4+n: 'y' + base36(n)
                    # Mix: actually '0' is a zero-valued column that occupies 1 column
                    # and w/x/y are extra skips WITHOUT a column symbol.
                    # Common implementation: encode each nonzero as base32 char,
                    # and between them skip with w/x/y (not including a '0').
                    # Zero columns in the middle: if we want 1 zero column we can
                    # emit '0'. Let's emit:
                    while zrun:
                        if zrun == 1:
                            enc.append("0")
                            zrun = 0
                        elif zrun == 2:
                            enc.append("w")
                            zrun = 0
                        elif zrun == 3:
                            enc.append("x")
                            zrun = 0
                        else:
                            extra = min(zrun - 4, 35)
                            enc.append("y" + "0123456789abcdefghijklmnopqrstuvwxyz"[extra])
                            zrun -= 4 + extra
                else:
                    enc.append("0123456789abcdefghijklmnopqrstuv"[cols[i]])
                    i += 1
            parts.append("".join(enc))
        # strip trailing empty strips
        while parts and parts[-1] == "":
            parts.pop()
        code = "xs%d_%s" % (len(form), "z".join(parts))
        if best is None or code < best:
            best = code
    return best


def check(rle_text: str, target: str):
    out = {"ok": False, "target": target, "errors": []}
    rule, cells = parse_rle(rle_text)
    ru = rule.upper().replace("/", "")
    if ru not in ("B3S23",):
        out["errors"].append("rule %s is not B3/S23" % rule)
        return out
    out["rule"] = rule
    out["gen0_population"] = len(cells)

    comps = components(cells)
    gl = []
    for c in comps:
        if normalize(c) not in GLIDER_SHAPES:
            out["errors"].append(
                "gen0 component of %d cells is not a glider" % len(c)
            )
            return out
        d = glider_direction(c)
        if d is None:
            out["errors"].append("glider direction not found")
            return out
        gl.append((c, d))
    out["n_gliders"] = len(gl)
    out["glider_dirs"] = [d for _, d in gl]

    mn_x, mn_y, mx_x, mx_y = bbox(cells)
    w, h = mx_x - mn_x + 1, mx_y - mn_y + 1
    side = max(w, h)
    diag = math.hypot(w, h)
    # Criterion: at least 4 * bounding-box diameter. Use both the long side
    # and the Euclidean diagonal; both must pass, every generation.
    T_side = 4 * side
    T_diag = 4 * math.ceil(diag)
    Ts = sorted({T_side + (-T_side) % 4, T_diag + (-T_diag) % 4})
    out["bbox_wh"] = [w, h]
    out["diameter_side"] = side
    out["diameter_diag_ceil"] = math.ceil(diag)
    out["rewind_T"] = Ts
    for T in Ts:
        ok, at = rewind_ok(gl, T)
        if not ok:
            out["errors"].append("rewind interaction at generation %d of T=%d" % (at, T))
            return out
    out["rewind_ok"] = True

    start, period, final = forward_to_periodic(set(cells))
    if start is None:
        out["errors"].append("no exact repeat within generation cap")
        return out
    out["periodic_from"] = start
    out["period"] = period
    out["final_population"] = len(final)

    kind, num, tcells = decode_apgcode(target)
    out["decoded_pop"] = len(tcells)
    out["decoded_kind"] = kind
    out["decoded_num"] = num
    if kind != "s":
        out["errors"].append("target apgcode is not xs (kind=%s)" % kind)
        return out
    if len(tcells) != num:
        out["errors"].append(
            "apgcode xs%d has %d decoded cells" % (num, len(tcells))
        )
        return out
    if period != 1:
        out["errors"].append("final period %d, still life wants 1" % period)
        return out
    if not is_still_life(tcells):
        out["errors"].append("decoded target cells are not a still life")
        return out
    if not is_still_life(final):
        out["errors"].append("final pattern is period 1 but step disagrees")
        return out

    tforms = all_forms(tcells)
    if normalize(final) not in tforms:
        out["errors"].append("final cells are not the target (or extra cells remain)")
        return out
    out["final_matches_target"] = True

    # Independent apgcode of the final pattern (canonical xs).
    try:
        got_code = encode_apgcode_xs(final)
        out["final_apgcode_encoded"] = got_code
        # encoding of skips can differ in equivalent skip notation; also compare forms
        out["final_apgcode_matches_target"] = got_code == target
        if got_code != target:
            # still OK if decoded forms match (skip-encoding variants)
            _k, _n, rec = decode_apgcode(got_code)
            if normalize(rec) not in tforms:
                out["errors"].append(
                    "re-encoded apgcode %s does not match target form" % got_code
                )
                return out
    except Exception as e:
        out["encode_warning"] = str(e)

    strict, reason = strict_still_life(tcells)
    out["strict"] = strict
    out["strict_reason"] = reason
    if not strict:
        out["errors"].append("target is not a strict still life: %s" % reason)
        return out

    # Also confirm the evolved object, not only the decoded apgcode, is strict.
    strict_f, reason_f = strict_still_life(final)
    out["final_strict"] = strict_f
    out["final_strict_reason"] = reason_f
    if not strict_f:
        out["errors"].append("evolved object is not a strict still life: %s" % reason_f)
        return out

    out["ok"] = True
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rle", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--table", help="xs28 textcensus file to scan")
    ap.add_argument("--object-html", help="saved object page to scan for #CSYNTH")
    args = ap.parse_args()
    rle = Path(args.rle).read_text()
    result = check(rle, args.target)
    if args.table:
        text = Path(args.table).read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        hits = []
        for i, line in enumerate(lines):
            if args.target in line:
                hits.append((i + 1, line[:240]))
        result["table_lines"] = len(lines)
        result["table_header"] = lines[0] if lines else ""
        result["table_hits"] = hits
        result["table_absent"] = len(hits) == 0
        if hits:
            result["errors"].append("apgcode present in class table")
            result["ok"] = False
    if args.object_html:
        html = Path(args.object_html).read_text(encoding="utf-8", errors="replace")
        has_csynth = bool(re.search(r"#CSYNTH", html))
        costs = re.findall(
            rf"#CSYNTH\s+{re.escape(args.target)}\s+costs\s+(\d+)\s+gliders", html
        )
        result["object_bytes"] = len(html.encode("utf-8"))
        result["object_has_csynth"] = has_csynth
        result["object_csynth_costs"] = costs
        result["object_title_ok"] = args.target in html
        still = bool(re.search(r"still-life", html, re.I))
        result["object_page_says_still_life"] = still
        if has_csynth or costs:
            result["errors"].append("object page contains #CSYNTH: %s" % costs)
            result["ok"] = False
        # error-page heuristic
        if re.search(r"404|not found|error", html, re.I) and not still:
            result["errors"].append("object page looks like an error page")
            result["ok"] = False
    print("n_gliders", result.get("n_gliders"))
    print("rewind_ok", result.get("rewind_ok"), "T", result.get("rewind_T"))
    print("period", result.get("period"), "from", result.get("periodic_from"), "pop", result.get("final_population"))
    print("final_matches_target", result.get("final_matches_target"))
    print("final_apgcode_encoded", result.get("final_apgcode_encoded"))
    print("strict", result.get("strict"), result.get("strict_reason"))
    print("table_absent", result.get("table_absent"), "hits", result.get("table_hits"))
    print("object_has_csynth", result.get("object_has_csynth"), "costs", result.get("object_csynth_costs"))
    print("errors", result.get("errors"))
    print("ok", result.get("ok"))
    print("PASS" if result.get("ok") else "FAIL")
    # dump compact
    keys = [
        "ok",
        "n_gliders",
        "glider_dirs",
        "bbox_wh",
        "diameter_side",
        "diameter_diag_ceil",
        "rewind_T",
        "rewind_ok",
        "periodic_from",
        "period",
        "final_population",
        "decoded_pop",
        "decoded_kind",
        "final_matches_target",
        "final_apgcode_encoded",
        "final_apgcode_matches_target",
        "strict",
        "strict_reason",
        "final_strict",
        "final_strict_reason",
        "table_lines",
        "table_header",
        "table_absent",
        "object_bytes",
        "object_has_csynth",
        "object_page_says_still_life",
        "errors",
    ]
    for k in keys:
        if k in result:
            print("  %s: %s" % (k, result[k]))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
