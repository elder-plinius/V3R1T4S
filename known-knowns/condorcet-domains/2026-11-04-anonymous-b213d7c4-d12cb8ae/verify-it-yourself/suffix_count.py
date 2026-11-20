"""Parent verification derived directly from the never-position definition.

Build a ranking from bottom to top. When x is placed above the current suffix,
its rank on a triple naming x is 3 minus the number of its partners in that
suffix. The suffix set determines all future transitions; multiplicities count
all rankings exactly. This is verification, not a research search.
"""
import argparse
import datetime
import functools
import hashlib
import itertools
import json
import math
import re
from pathlib import Path


def count(n, rules):
    tests = [[] for _ in range(n)]
    for triple, i, j in rules:
        x = triple[i - 1]
        mask = sum(1 << y for y in triple if y != x)
        tests[x].append((mask, 3 - j))

    @functools.lru_cache(None)
    def suffix(mask):
        if mask == (1 << n) - 1:
            return 1
        total = 0
        for x in range(n):
            bit = 1 << x
            if mask & bit:
                continue
            if all((mask & pair).bit_count() != forbidden
                   for pair, forbidden in tests[x]):
                total += suffix(mask | bit)
        return total

    result = suffix(0)
    return result, suffix.cache_info().currsize


def parse(path, n):
    triples = set(itertools.combinations(range(n), 3))
    seen = set()
    rules = []
    for line in path.read_text(encoding='ascii').splitlines():
        match = re.fullmatch(r'([1-9][0-9]*) ([1-9][0-9]*) ([1-9][0-9]*) ([1-3])N([1-3])', line)
        if not match:
            raise ValueError('malformed assignment row')
        a, b, c, i, j = map(int, match.groups())
        triple = (a - 1, b - 1, c - 1)
        if triple not in triples or triple in seen:
            raise ValueError('missing, unsorted, duplicate or out-of-range triple')
        seen.add(triple)
        rules.append((triple, i, j))
    if seen != triples:
        raise ValueError('incomplete assignment')
    return rules


def calibrate():
    triples = list(itertools.combinations(range(4), 3))
    perms = list(itertools.permutations(range(4)))
    choices = list(itertools.product(range(1, 4), repeat=2))
    for selected in itertools.product(choices, repeat=4):
        rules = [(triple, *choice) for triple, choice in zip(triples, selected)]
        brute = 0
        for order in perms:
            pos = {x: k for k, x in enumerate(order)}
            if all(sorted(triple, key=pos.get).index(triple[i - 1]) + 1 != j
                   for triple, i, j in rules):
                brute += 1
        exact, _ = count(4, rules)
        if exact != brute:
            raise AssertionError((rules, exact, brute))
    fishburn = {}
    for n, expected in ((9, 488), (20, 2115186)):
        rules = [(t, 2, 1 if (t[1] + 1) % 2 == 0 else 3)
                 for t in itertools.combinations(range(n), 3)]
        actual, _ = count(n, rules)
        assert actual == expected, (n, actual, expected)
        fishburn[n] = actual
    impossible = [((0, 1, 2), 1, j) for j in (1, 2, 3)]
    assert count(3, impossible)[0] == 0
    assert count(3, [((0, 1, 2), 1, 1)])[0] == 4
    return dict(all_n4_assignments=9 ** math.comb(4, 3),
                fishburn=fishburn, impossible_domain=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('assignment', type=Path)
    parser.add_argument('--n', type=int, default=25)
    args = parser.parse_args()
    calibration = calibrate()
    rules = parse(args.assignment, args.n)
    exact, states = count(args.n, rules)
    print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                          assignment=str(args.assignment), n=args.n,
                          sha256=hashlib.sha256(args.assignment.read_bytes()).hexdigest(),
                          triples=len(rules), count=exact, suffix_states=states,
                          calibration=calibration), indent=2))
