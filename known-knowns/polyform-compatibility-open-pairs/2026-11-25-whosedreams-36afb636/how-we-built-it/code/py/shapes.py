"""Heptiamond library: honeycomb embedding, D6 aspects, board placements."""
from __future__ import annotations
import json
import math
import cmath
from pathlib import Path
from collections import defaultdict
from .grid import Cell, nbrs, neighbors, normalize, connected, make_board

ROOT = Path(__file__).resolve().parents[1]
_DATA = None
_ASPECTS: dict[str, list[list[Cell]]] = {}
SQRT3 = math.sqrt(3)


def load() -> dict:
    global _DATA
    if _DATA is None:
        _DATA = json.loads((ROOT / "data" / "heptiamonds.json").read_text())
    return _DATA


def letters() -> list[str]:
    return list(load()["letters"])


def piece_cells(letter: str) -> list[Cell]:
    return [tuple(p) for p in load()["pieces"][letter]["cells"]]


def center(r: int, c: int) -> complex:
    """Honeycomb embedding: 120° bond angles, equal edge lengths."""
    return complex(c, r * SQRT3 + ((r + c) & 1) * (SQRT3 / 3))


def dist_sig(cells) -> tuple:
    zs = [center(r, c) for r, c in cells]
    return tuple(
        sorted(
            round(abs(zs[i] - zs[j]), 6)
            for i in range(len(zs))
            for j in range(i + 1, len(zs))
        )
    )


def aspects_of(cells) -> list[list[Cell]]:
    """All distinct D6 (rotation+reflection) images, translation-normalized."""
    cells = list(map(tuple, cells))
    zs0 = [center(r, c) for r, c in cells]
    target = dist_sig(cells)
    seen: set[frozenset] = set()
    out: list[list[Cell]] = []
    omega6 = cmath.exp(1j * math.pi / 3)

    def snap_set(zs):
        rs = [z.imag for z in zs]
        xs = [z.real for z in zs]
        rmin, rmax = int(min(rs) / SQRT3) - 4, int(max(rs) / SQRT3) + 5
        cmin, cmax = int(min(xs)) - 4, int(max(xs)) + 5
        lk: dict[tuple, list] = defaultdict(list)
        for r in range(rmin, rmax + 1):
            for c in range(cmin, cmax + 1):
                z = center(r, c)
                lk[(round(z.real, 5), round(z.imag, 5))].append((r, c))
        z0 = zs[0]
        for r in range(rmin, rmax + 1):
            for c in range(cmin, cmax + 1):
                off = center(r, c) - z0
                snapped = []
                used = set()
                ok = True
                for z in zs:
                    zz = z + off
                    key = (round(zz.real, 5), round(zz.imag, 5))
                    opts = lk.get(key, [])
                    if not opts:
                        best = None
                        bd = 1e9
                        for rr in range(int(zz.imag / SQRT3) - 2, int(zz.imag / SQRT3) + 3):
                            for cc in range(int(zz.real) - 2, int(zz.real) + 3):
                                d = abs(center(rr, cc) - zz)
                                if d < bd:
                                    bd = d
                                    best = (rr, cc)
                        if bd > 1e-4:
                            ok = False
                            break
                        opts = [best]
                    cell = opts[0]
                    if cell in used:
                        ok = False
                        break
                    used.add(cell)
                    snapped.append(cell)
                if ok and len(snapped) == len(zs) and connected(snapped):
                    if dist_sig(snapped) == target:
                        return normalize(snapped)
        return None

    for refl in (False, True):
        base = [complex(-z.real, z.imag) for z in zs0] if refl else list(zs0)
        cen = sum(base) / len(base)
        base = [z - cen for z in base]
        for k in range(6):
            rot = omega6 ** k
            zs = [rot * z for z in base]
            got = snap_set(zs)
            if got is not None:
                key = frozenset(got)
                if key not in seen:
                    seen.add(key)
                    out.append(sorted(got))
    if not out:
        # always include original
        out.append(sorted(normalize(cells)))
    return out


def aspects_for(letter: str) -> list[list[Cell]]:
    if letter not in _ASPECTS:
        _ASPECTS[letter] = aspects_of(piece_cells(letter))
    return _ASPECTS[letter]


def all_placements(shape_or_letter, board: list[Cell]) -> list[list[Cell]]:
    """All congruent copies (rot/refl/translate) of piece on board."""
    if isinstance(shape_or_letter, str):
        aspects = aspects_for(shape_or_letter)
    else:
        aspects = aspects_of(shape_or_letter)
    board_set = set(map(tuple, board))
    if not board_set:
        return []
    brs = [r for r, c in board_set]
    bcs = [c for r, c in board_set]
    r0, r1 = min(brs), max(brs)
    c0, c1 = min(bcs), max(bcs)
    out = {}
    for asp in aspects:
        ars = [r for r, c in asp]
        acs = [c for r, c in asp]
        # translate so aspect fits in board bbox
        for dr in range(r0 - max(ars), r1 - min(ars) + 1):
            for dc in range(c0 - max(acs), c1 - min(acs) + 1):
                if (dr + dc) & 1:
                    continue  # preserve parity
                pl = [(r + dr, c + dc) for r, c in asp]
                if all(p in board_set for p in pl):
                    out[frozenset(pl)] = pl
    return list(out.values())


def placements_for(letter: str, board: list[Cell]) -> list[list[Cell]]:
    return all_placements(letter, board)
