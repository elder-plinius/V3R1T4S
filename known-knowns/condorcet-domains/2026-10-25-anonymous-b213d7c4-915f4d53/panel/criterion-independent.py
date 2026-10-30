"""Criterion skeptic implementation, independently derived before reading claim verifier.
Append x to a prefix exactly when x's forbidden triple rank is not realized.
Usage: python3 panel/criterion-independent.py claim/assignment.txt
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import hashlib, json, sys

def verify(path, n=25):
    raw = Path(path).read_bytes()
    rules = [[] for _ in range(n)]
    seen = set()
    for line in raw.decode("ascii").splitlines():
        a, b, c, word = line.split()
        a, b, c = map(int, (a, b, c))
        assert 1 <= a < b < c <= n and (a, b, c) not in seen
        assert len(word) == 3 and word[0] in "123" and word[1] == "N" and word[2] in "123"
        seen.add((a, b, c))
        triple = (a, b, c)
        x = triple[int(word[0])-1]-1
        pair = sum(1 << (q-1) for q in triple if q != x+1)
        rules[x].append((pair, int(word[2])-1))
    assert seen == set(combinations(range(1, n+1), 3))
    full = (1 << n)-1
    layer = {0: 1}
    layers = [1]
    for depth in range(n):
        nxt = defaultdict(int)
        for mask, count in layer.items():
            remaining = full ^ mask
            while remaining:
                bit = remaining & -remaining
                remaining -= bit
                x = bit.bit_length()-1
                if all((mask & pair).bit_count() != position for pair, position in rules[x]):
                    nxt[mask | bit] += count
        layer = nxt
        layers.append(len(layer))
    return {"assignment_sha256": hashlib.sha256(raw).hexdigest(), "n": n,
            "triples": len(seen), "exact_count": layer.get(full, 0),
            "states_by_depth": layers, "total_states": sum(layers)}

if __name__ == "__main__":
    result = verify(sys.argv[1])
    assert result["assignment_sha256"] == "915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b"
    assert result["exact_count"] == 180870896
    print(json.dumps(result, indent=2))
    print("PASS")
