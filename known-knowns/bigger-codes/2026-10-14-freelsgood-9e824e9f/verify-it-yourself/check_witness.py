#!/usr/bin/env python3
"""Independent exhaustive checker; uses only the stated binary-code definition."""
import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path
import time


def check(data, n, w, d, expected):
    lines = data.decode('ascii').splitlines()
    assert len(lines) == expected, ('cardinality', len(lines), expected)
    for i, line in enumerate(lines):
        assert len(line) == n, ('length', i, len(line))
        assert set(line) <= {'0', '1'}, ('alphabet', i)
        assert line.count('1') == w, ('weight', i, line.count('1'))
    words = [int(line, 2) for line in lines]
    assert len(set(words)) == expected, 'duplicate vectors'
    histogram = collections.Counter()
    for i, x in enumerate(words):
        for j in range(i):
            distance = (x ^ words[j]).bit_count()
            assert distance >= d, ('distance', i, j, distance)
            histogram[distance] += 1
    pairs = sum(histogram.values())
    assert pairs == expected * (expected - 1) // 2
    return dict(cardinality=len(words), length=n, weight=w,
                pair_count=pairs, minimum_distance=min(histogram) if histogram else None,
                distance_histogram=dict(sorted(histogram.items())),
                sha256=hashlib.sha256(data).hexdigest(), byte_count=len(data))


def controls():
    positive = check(b'111000\n000111\n', 6, 3, 6, 2)
    assert positive['minimum_distance'] == 6 and positive['pair_count'] == 1
    cases = {
        'distance_two': (b'111000\n110100\n', 6, 3, 6, 2),
        'duplicate': (b'111000\n111000\n', 6, 3, 6, 2),
        'wrong_weight': (b'110000\n000111\n', 6, 3, 6, 2),
        'wrong_length': (b'11100\n000111\n', 6, 3, 6, 2),
        'nonbinary': (b'11100x\n000111\n', 6, 3, 6, 2),
        'wrong_count': (b'111000\n', 6, 3, 6, 2),
    }
    rejected = {}
    for name, args in cases.items():
        try:
            check(*args)
        except AssertionError as exc:
            rejected[name] = str(exc)
        else:
            raise AssertionError('negative control accepted: ' + name)
    print(json.dumps({'positive_control': positive, 'negative_controls_rejected': rejected}, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('witness', type=Path)
    args = parser.parse_args()
    print('started_utc:', datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
    controls()
    started = time.monotonic()
    result = check(args.witness.read_bytes(), 27, 10, 6, 13026)
    result['elapsed_seconds'] = time.monotonic() - started
    print(json.dumps(result, sort_keys=True), flush=True)
    print('INDEPENDENT_CHECK: PASS', flush=True)

if __name__ == '__main__':
    main()
