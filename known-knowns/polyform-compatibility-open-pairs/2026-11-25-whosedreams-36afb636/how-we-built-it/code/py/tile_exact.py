"""Exact-cover tiling check / search by backtracking (independent of SAT)."""
from __future__ import annotations
from .grid import Cell


def can_tile(figure: set[Cell], placements: list[list[Cell]]) -> list[list[Cell]] | None:
    fig = set(map(tuple, figure))
    pls = [tuple(sorted(map(tuple, p))) for p in placements if set(map(tuple, p)) <= fig]
    # cell -> placement indices
    cover = {c: [] for c in fig}
    for i, p in enumerate(pls):
        for c in p:
            cover[c].append(i)
    order = sorted(fig, key=lambda c: len(cover[c]))
    used_pl = [False] * len(pls)
    chosen: list[int] = []

    def bt(remaining: set) -> bool:
        if not remaining:
            return True
        # pick most constrained cell
        c = min(remaining, key=lambda x: len([i for i in cover[x] if not used_pl[i]]))
        opts = [i for i in cover[c] if not used_pl[i]]
        for i in opts:
            cells = pls[i]
            if any(x not in remaining for x in cells):
                continue
            used_pl[i] = True
            chosen.append(i)
            for x in cells:
                remaining.remove(x)
            if bt(remaining):
                return True
            for x in cells:
                remaining.add(x)
            chosen.pop()
            used_pl[i] = False
        return False

    rem = set(fig)
    if not bt(rem):
        return None
    return [list(pls[i]) for i in chosen]
