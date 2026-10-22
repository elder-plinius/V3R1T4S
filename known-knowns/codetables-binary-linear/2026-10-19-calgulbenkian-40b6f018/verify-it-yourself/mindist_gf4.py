"""Exact minimum distance of a linear code over GF(4) by full enumeration of all 4^k messages.
Standard library only.  Usage: python3 mindist_gf4.py object.json [--quiet]
Object: JSON with keys q (4), n, k, d (claimed), G (k rows of n symbols in 0..3).
Symbol encoding: v = a + 2b stands for a + b*w, with w*w = w + 1 (so 2 = w, 3 = w+1).
Addition of symbols is XOR of the 2-bit codes.  A word is held as one integer: bit j = low bit of
symbol j, bit n+j = high bit of symbol j.  Multiplying a word by w: (a, b) -> (b, a xor b).
Weight of a word = number of positions with a nonzero symbol = popcount((x | x >> n) & mask).
Meet in the middle: rows are split in two halves; every message is a pair (message of the first half,
message of the second half); all 4^k pairs are visited, the zero message is excluded.
The last line printed is a JSON object with the result."""
import sys, json


def mulw(x, n, mask):
    lo = x & mask
    hi = (x >> n) & mask
    return hi | ((lo ^ hi) << n)


def span_words(rows, n, mask):
    """All 4^len(rows) combinations, index = sum c_i * 4^i with c_i in 0..3; index 0 is the zero message."""
    words = [0]
    for r in rows:
        m1 = r
        m2 = mulw(m1, n, mask)
        m3 = mulw(m2, n, mask)
        if mulw(m3, n, mask) != m1:
            raise SystemExit("field self-check failed: w^3 != 1")
        new = []
        for c in (0, m1, m2, m3):
            new.extend(w ^ c for w in words)
        words = new
    return words


def main(path):
    d = json.load(open(path))
    q, n, k, G = d["q"], d["n"], d["k"], d["G"]
    assert q == 4, "this checker is for GF(4)"
    assert len(G) == k and all(len(r) == n for r in G), "generator shape"
    assert all(isinstance(v, int) and 0 <= v <= 3 for r in G for v in r), "symbol range"
    mask = (1 << n) - 1
    rows = []
    for r in G:
        x = 0
        for j, v in enumerate(r):
            if v & 1:
                x |= 1 << j
            if v & 2:
                x |= 1 << (n + j)
        rows.append(x)
    h = k // 2
    A = span_words(rows[:h], n, mask)
    B = span_words(rows[h:], n, mask)
    best = n + 1
    cnt = 0
    zero_words = 0
    total = 0
    for ia, a in enumerate(A):
        for ib, b in enumerate(B):
            if ia == 0 and ib == 0:
                continue
            x = a ^ b
            w = bin((x | (x >> n)) & mask).count("1")
            total += 1
            if w == 0:
                zero_words += 1
            elif w < best:
                best = w
                cnt = 1
            elif w == best:
                cnt += 1
    res = {"n": n, "k": k, "messages_nonzero": total, "expected": 4 ** k - 1,
           "rank_k": zero_words == 0 and total == 4 ** k - 1, "min_distance": best, "A_d": cnt,
           "claimed_d": d["d"]}
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1])
