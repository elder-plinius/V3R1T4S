"""Triangular-lattice cells for heptiamonds."""
from __future__ import annotations
from collections import deque
from typing import Iterable

Cell = tuple[int, int]
DIRS = {0: ((0, -1), (0, 1), (-1, 0)), 1: ((0, -1), (0, 1), (1, 0))}


def nbrs(r: int, c: int) -> list[Cell]:
    return [(r + dr, c + dc) for dr, dc in DIRS[(r + c) & 1]]


def neighbors(cell: Cell) -> list[Cell]:
    return nbrs(cell[0], cell[1])


def connected(cells: Iterable[Cell]) -> bool:
    cells = set(map(tuple, cells))
    if not cells:
        return True
    s = next(iter(cells))
    seen = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in neighbors(u):
            if v in cells and v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == len(cells)


def normalize(cells: Iterable[Cell]) -> frozenset[Cell]:
    cells = set(map(tuple, cells))
    best = None
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    for dr in range(min(rs) - 1, max(rs) + 2):
        for dc in range(min(cs) - 3, max(cs) + 4):
            if (dr + dc) & 1:
                continue
            sh = frozenset((r - dr, c - dc) for r, c in cells)
            if min(r for r, c in sh) != 0:
                continue
            if min(c for r, c in sh) < 0:
                continue
            key = tuple(sorted(sh))
            if best is None or key < best[0]:
                best = (key, sh)
    return frozenset(best[1])


def holeless(cells: Iterable[Cell], bbox_pad: int = 2) -> bool:
    """True iff the finite component of the complement is empty
    (every non-figure cell in a padded bbox reaches the bbox boundary)."""
    cells = set(map(tuple, cells))
    if not cells:
        return True
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    r0, r1 = min(rs) - bbox_pad, max(rs) + bbox_pad
    c0, c1 = min(cs) - bbox_pad, max(cs) + bbox_pad
    exterior = set()
    for r in range(r0, r1 + 1):
        for c in (c0, c1):
            if (r, c) not in cells:
                exterior.add((r, c))
    for c in range(c0, c1 + 1):
        for r in (r0, r1):
            if (r, c) not in cells:
                exterior.add((r, c))
    seen = set()
    q = deque(exterior)
    seen.update(exterior)
    while q:
        u = q.popleft()
        for v in neighbors(u):
            vr, vc = v
            if vr < r0 or vr > r1 or vc < c0 or vc > c1:
                continue
            if v in cells or v in seen:
                continue
            seen.add(v)
            q.append(v)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if (r, c) not in cells and (r, c) not in seen:
                return False
    return True


def make_board(nrows: int, ncols: int) -> list[Cell]:
    return [(r, c) for r in range(nrows) for c in range(ncols)]


def figure_ascii(cells: Iterable[Cell], marks: dict[Cell, str] | None = None) -> str:
    cells = set(map(tuple, cells))
    if not cells:
        return "(empty)"
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    lines = []
    for r in range(min(rs), max(rs) + 1):
        row = []
        for c in range(min(cs), max(cs) + 1):
            if (r, c) in cells:
                row.append((marks or {}).get((r, c), "#"))
            else:
                row.append(".")
        lines.append("".join(row))
    return "\n".join(lines)
