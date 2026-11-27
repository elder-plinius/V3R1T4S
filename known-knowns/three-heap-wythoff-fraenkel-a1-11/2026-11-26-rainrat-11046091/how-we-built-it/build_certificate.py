"""Build the unified m = 0..12 certificate JSON from the verified P-position table."""
from bisect import bisect_right
from collections import defaultdict
from itertools import permutations
from math import isqrt
from pathlib import Path
import json
import sys


ALPHA = (0, -4, -10, -16, -20, -26, -32, -39, -46, -52, -56, -61, -67)
TABLE = [
    (1, 1, (), ()),
    (21, 28, (1,), (2, 17, 22)),
    (28, 58, (), (1, 5, 8, 24, 26, 32)),
    (48, 73, (1, 2, 3), (2, 3, 4, 5, 8, 10, 11, 12, 28, 41, 57)),
    (126, 208, (3, 6), (2, 5, 6, 7, 8, 9, 11, 12, 14, 17, 46, 48, 59)),
    (71, 123, (4, 7, 10), (1, 3, 5, 6, 8, 10, 11, 12, 15, 16, 17, 18, 19, 28, 56, 77, 83)),
    (113, 232, (2, 3, 4, 6), (1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 18, 21, 44, 58, 95, 96, 132)),
    (227, 343, (1, 4, 6, 7, 9), (0, 1, 2, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 24, 28, 30, 86, 88, 232, 251)),
    (388, 648, (3, 5, 10, 13), (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 19, 20, 21, 22, 24, 26, 27, 28, 33, 34, 46, 155, 257, 390, 415)),
    (645, 645, (4, 6, 11, 15), (0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 24, 25, 26, 27, 30, 36, 37, 44, 48, 62, 254, 388, 421, 676)),
    (656, 656, (6, 7, 8, 9, 13), (0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 27, 28, 29, 30, 31, 32, 34, 39, 50, 53, 103, 391, 424, 690)),
]


def phi(k):
    return (k + isqrt(5 * k * k)) // 2


def first_free(used, least):
    while least in used:
        least += 1
    return least


def read_rows(path, cap):
    rows = [[] for _ in ALPHA]
    for row in Path(path).read_text().splitlines():
        m, y, z = map(int, row.split())
        assert 0 <= m <= y <= z <= cap
        rows[m].append((y, z))
    for m, row in enumerate(rows):
        row.sort()
        assert len({y for y, _ in row}) == len(row)
        assert row[0][0] >= m
    return rows


def covered_rays(rows, m, gaps, threshold):
    """Build explicit lower-layer P-position witnesses [a, A0, B0] across [threshold, threshold + p_m]."""
    period = 1 << m.bit_length()
    destinations = defaultdict(list)
    for i in range(m):
        for u, v in rows[i]:
            orig = [i, u - i, v - u]
            for x, b, c in set(permutations((i, u, v))):
                if x <= m:
                    destinations[c - b].append(((x, b, c), orig))
    witnesses = []
    for gap in gaps:
        dests = []
        for y in range(threshold, threshold + period + 1):
            source = (m, y, y + gap)
            found = None
            for g in range(gap - m, gap + m + 1):
                for dest, orig in destinations[g]:
                    d, e, f = (a - b for a, b in zip(source, dest))
                    if min(d, e, f) >= 0 and (d ^ e ^ f) == 0 and (d or e or f):
                        found = orig
                        break
                if found is not None:
                    break
            if found is None:
                raise AssertionError(("uncovered lower-layer ray", m, gap, y))
            dests.append(found)
        witnesses.append({
            "c": gap,
            "ray_start_Y": threshold,
            "period": period,
            "destinations": dests,
        })
    return witnesses


def build_cert(path, cap):
    rows = read_rows(path, cap)
    assert rows[0][:3] == [(0, 0), (1, 2), (3, 5)]
    details = []
    for m, row in enumerate(rows):
        gap = [z - y for y, z in row]
        offset = [y - phi(g) for (y, _), g in zip(row, gap)]
        eps = [v - ALPHA[m] for v in offset]
        assert len(set(gap)) == len(gap)
        t = sorted({z - m for i in range(m) for y, z in rows[i] if y == m})
        cutoff = len(row) - 100
        n_gap = max((j + 2 for j in range(cutoff) if gap[j + 1] != gap[j] + 1), default=1)
        n_eps = max((j + 2 for j in range(cutoff) if abs(eps[j]) > 1), default=1)
        s = sorted(set(range(gap[cutoff])) - set(gap[:cutoff + 1]))
        if m < len(TABLE):
            assert (n_gap, n_eps, tuple(t), tuple(s)) == TABLE[m]

        used = set(range(m)) | {m + b for b in t}
        least = m
        for y, z in row[:cutoff + 1]:
            least = first_free(used, least)
            assert y == least and z not in used
            used.update((y, z))

        start = 2 if m == 0 else n_gap
        prefix = row[:start - 1]
        forbidden_max = max([m - 1, *[m + b for b in t], *[z for _, z in prefix]])
        assert row[start - 1][1] > forbidden_max
        assert all(g < gap[start - 1] for g in gap[:start - 1])

        last_triple = max((j + 1 for j in range(2, cutoff) if all(eps[j - 2:j + 1])), default=0)
        base = max(start + 4, n_eps + 4, last_triple + 5,
                   bisect_right([y for y, _ in row], forbidden_max) + 4)
        end = bisect_right([y for y, _ in row], row[base - 1][1]) + 1
        if m > 0:
            end = max(end, base + 2)
            earlier_bounds = [max(item["early_gaps"], default=-1) for item in details]
            lower_floor = max(g + m - i for i, g in enumerate(earlier_bounds))
            lower_n3_gap = max(item["B_N3"] for item in details)
            lower_n3_p1_gap = max(item["B_N3_plus_1"] for item in details)
            while (gap[end - 1] <= max(lower_floor, lower_n3_gap, lower_n3_p1_gap)
                   or row[end - 1][0] - m <= row[base + 2][1] - m):
                end += 1
        first_above_forbidden = bisect_right([y for y, _ in row], forbidden_max)
        while (eps[end - 1] != 0
               or row[end - 4][0] <= row[first_above_forbidden][1]
               or row[end - 4][0] - 1 <= row[base - 6][1]
               or (m > 0 and (min(offset[base - 1:end]) + max(offset[base - 1:end])) // 2 != ALPHA[m])):
            end += 1
        assert end < cutoff and base >= start + 4
        assert all(row[end][0] <= lower[-101][0] for lower in rows[:m])
        assert all(gap[j + 1] == gap[j] + 1 for j in range(start - 1, end))
        assert row[end - 1][0] > row[base - 1][1]
        assert all(abs(eps[j]) <= 1 for j in range(base - 5, end))
        assert all(not all(eps[j - 2:j + 1]) for j in range(base - 3, end))
        n3 = max((j + 1 for j in range(1, end) if eps[j] and eps[j - 1]), default=1)
        assert all(abs(eps[j]) <= 1 for j in range(n3, end))

        pm = 1 if m == 0 else (1 << m.bit_length())
        item = {
            "m": m,
            "p_m": pm,
            "T": t,
            "S": s,
            "alpha": ALPHA[m],
            "N1": n_gap,
            "N2": n_eps,
            "N3": n3,
            "B_N3": gap[n3 - 1],
            "B_N3_plus_1": gap[n3],
            "N_claim34": base - 1,
            "n2": base,
            "n1": end,
            "A_n1": row[end - 1][0] - m,
            "B_n1": gap[end - 1],
            "P_n2_plus_3": [m, row[base + 2][0] - m, gap[base + 2]],
            "P_n1": [m, row[end - 1][0] - m, gap[end - 1]],
            "next_middle": row[end][0],
            "next_gap": gap[end],
            "Wythoff_forbidden_max": forbidden_max,
            "early_gaps": gap[:n3],
        }
        if m > 0:
            small_two_max = max(z for i in range(m) for y, z in rows[i] if y <= m)
            max_t = max(v for entry in [t, *[d["T"] for d in details]] for v in entry)
            item["small_two_max"] = small_two_max
            item["max_T_through_m"] = max_t
            item["offset_slack"] = [ALPHA[i] - ALPHA[m] - phi(m - i) - 3 for i in range(m)]
            item["S1_n1"] = s
            item["S1_n1_witnesses"] = covered_rays(rows, m, s, row[end - 1][0])
        details.append(item)

    for row in details:
        del row["early_gaps"]

    out = {
        "target_id": "three-heap-wythoff-fraenkel-a1-11",
        "target_A1": 12,
        "conventions": {
            "coordinates": "[m, A, B] denotes sorted physical heaps (m, m + A, m + A + B) with 1-based layer indexing j >= 1 (A_j = Y_j - m, B_j = Z_j - Y_j), following Sun & Zeilberger (Ann. Comb. 8, 2004, pp. 225-238).",
            "threshold_indexing": "N1, N2, N3 follow the Table 1 >= convention (first index from which the condition holds continuously up to the verified horizon).",
            "midpoint_formula_note": "On p. 235 of Sun & Zeilberger (2004), alpha' is printed as floor((max - min)/2), a typographical minus sign for floor((max + min)/2). Table 1 and Claim 3.5's separation hypothesis alpha_0 - alpha' >= 4m (with alpha_0 = 0) require (max + min)//2. Both the half-sum Claim 3.5 checks and the direct Lemma 2.6 induction proof are verified.",
        },
        "levels": details,
    }
    return out


if __name__ == "__main__":
    cert = build_cert(sys.argv[1], int(sys.argv[2]))
    Path(sys.argv[3]).write_text(json.dumps(cert, separators=(",", ":")))
    print(f"Wrote {sys.argv[3]} ({Path(sys.argv[3]).stat().st_size} bytes)")
