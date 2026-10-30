#!/usr/bin/env python3
"""Independent exact suffix-set DP, written before reading supplied verifier.

Definition: one a b c iNj per sorted triple, ith smallest never position j.
All orders are top-to-bottom. Build them from bottom to top. When adding v,
the number k of its two triple partners already in the suffix determines its
position as 3-k. Reject precisely when k == 3-j. Memoized suffix sets count
every possible completion, with arbitrary-precision Python integers.
"""
import argparse
import hashlib
import itertools
import math
import re
import time
from functools import lru_cache
from pathlib import Path


def parse(text, n):
    lines = text.splitlines()
    if len(lines) != math.comb(n, 3):
        raise ValueError('wrong line count')
    result = {}
    for line in lines:
        m = re.fullmatch(r'([1-9][0-9]*)\s+([1-9][0-9]*)\s+([1-9][0-9]*)\s+([123])N([123])', line)
        if not m:
            raise ValueError('malformed line')
        a, b, c, i, j = map(int, m.groups())
        if not (1 <= a < b < c <= n):
            raise ValueError('unordered or out of range')
        key = (a, b, c)
        if key in result:
            raise ValueError('duplicate triple')
        result[key] = (i, j)
    if set(result) != set(itertools.combinations(range(1, n + 1), 3)):
        raise ValueError('missing triple')
    return result


def exact_count(assignment, n):
    restrictions = [[] for _ in range(n)]
    for triple, (i, j) in assignment.items():
        v = triple[i-1]
        pair = sum(1 << (x-1) for x in triple if x != v)
        restrictions[v-1].append((pair, 3-j))
    full = (1 << n) - 1
    # A suffix mask is sufficient: each condition involves the relative
    # position of its forbidden alternative and its two partners only.
    @lru_cache(None)
    def count(suffix):
        if suffix == full:
            return 1
        answer = 0
        remaining = full ^ suffix
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            v = bit.bit_length()-1
            if all((suffix & pair).bit_count() != forbidden
                   for pair, forbidden in restrictions[v]):
                answer += count(suffix | bit)
        return answer
    answer = count(0)
    return answer, count.cache_info().currsize


def fishburn(n):
    return {t: (2, 1 if t[1] % 2 == 0 else 3)
            for t in itertools.combinations(range(1, n+1), 3)}


def brute(assignment, n):
    restrictions = [(triple[i-1], triple, j)
                    for triple, (i, j) in assignment.items()]
    total = 0
    for order in itertools.permutations(range(1, n+1)):
        pos = [0] * (n+1)
        for k, x in enumerate(order):
            pos[x] = k
        valid = True
        for v, triple, j in restrictions:
            rank = 1 + sum(pos[x] < pos[v] for x in triple if x != v)
            if rank == j:
                valid = False
                break
        total += valid
    return total


def negative_parser_tests(text, n):
    lines = text.splitlines()
    cases = {
        'missing': '\n'.join(lines[:-1]),
        'duplicate': '\n'.join(lines[:-1] + [lines[0]]),
        'extra': text + '\n' + lines[0],
        'unsorted': '\n'.join(['2 1 3 3N1'] + lines[1:]),
        'zero': '\n'.join(['0 2 3 3N1'] + lines[1:]),
        'out_of_range': '\n'.join([f'1 2 {n+1} 3N1'] + lines[1:]),
        'bad_i': '\n'.join(['1 2 3 4N1'] + lines[1:]),
        'bad_j': '\n'.join(['1 2 3 3N0'] + lines[1:]),
        'bad_syntax': '\n'.join(['1 2 3 3M1'] + lines[1:]),
        'extra_token': '\n'.join([lines[0] + ' extra'] + lines[1:]),
        'blank': '\n'.join([''] + lines[1:]),
    }
    for name, value in cases.items():
        try:
            parse(value, n)
        except ValueError:
            print('parser_negative', name, 'PASS', flush=True)
        else:
            raise AssertionError('accepted bad input: ' + name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('assignment')
    args = ap.parse_args()
    started = time.monotonic()
    data = Path(args.assignment).read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    print('SHA256', sha, flush=True)
    assert sha == '915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b'
    text = data.decode('utf-8')
    assignment = parse(text, 25)
    print('parsed_triples', len(assignment), flush=True)
    negative_parser_tests(text, 25)
    for n, expected in [(9, 488), (20, 2115186)]:
        value, states = exact_count(fishburn(n), n)
        print('Fishburn', n, value, 'states', states, flush=True)
        assert value == expected
    restricted = {t: condition for t, condition in assignment.items() if t[2] <= 9}
    small, states = exact_count(restricted, 9)
    exhaustive = brute(restricted, 9)
    print('first9_DP', small, 'brute_all_9factorial', exhaustive,
          'permutations', math.factorial(9), 'states', states, flush=True)
    assert small == exhaustive
    value, states = exact_count(assignment, 25)
    print('full_exact_count', value, 'states', states, flush=True)
    assert value == 180870896
    print('elapsed_seconds', round(time.monotonic()-started, 6), flush=True)
    print('PASS', flush=True)


if __name__ == '__main__':
    main()
