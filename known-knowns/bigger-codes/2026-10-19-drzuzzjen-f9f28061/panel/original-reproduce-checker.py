#!/usr/bin/env python3
"""Independent exact constant-weight checker, Python standard library only.

Definition: M distinct binary n-tuples of weight w, Hamming distance >= d.
Interpret text coordinate i as bit i; XOR marks precisely differing coordinates,
so (x ^ y).bit_count() equals the Hamming distance. Enumerate j > i once.
No source/Windows checker is read, imported or invoked.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def check(path, n, d, w, count, expected_hash, progress=None):
    start = time.monotonic()
    result = dict(started_utc=utc(), pid=os.getpid(), n=n, d=d, w=w,
                  expected_M=count, source=str(path), pass_=False,
                  pairs_checked=0, expected_pairs=count * (count - 1) // 2)
    # No exception/assertion bypass: every validation is explicit.
    raw = path.read_bytes()
    result['object_sha256'] = hashlib.sha256(raw).hexdigest()
    if result['object_sha256'] != expected_hash:
        result['failure'] = 'hash_mismatch'
        return result
    try:
        rows = raw.decode('ascii').splitlines()
    except UnicodeDecodeError:
        result['failure'] = 'non_ascii'
        return result
    result['observed_M'] = len(rows)
    if len(rows) != count:
        result['failure'] = 'count_mismatch'
        return result
    values = []
    for i, row in enumerate(rows):
        if len(row) != n or set(row) - {'0', '1'}:
            result.update(failure='invalid_binary_width', row=i)
            return result
        value = int(row[::-1], 2)
        if value.bit_count() != w:
            result.update(failure='invalid_weight', row=i,
                          observed_weight=value.bit_count())
            return result
        values.append(value)
    result['distinct_M'] = len(set(values))
    if result['distinct_M'] != count:
        result['failure'] = 'duplicate'
        return result
    histogram = collections.Counter()
    minimum = n + 1
    witness = None
    pairs = 0
    for i, x in enumerate(values):
        for j in range(i + 1, len(values)):
            distance = (x ^ values[j]).bit_count()
            pairs += 1
            histogram[distance] += 1
            if distance < minimum:
                minimum, witness = distance, [i, j]
            if distance < d:
                result.update(failure='distance_violation', pair=[i, j],
                              observed_distance=distance, pairs_checked=pairs)
                return result
        if i % 200 == 0:
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if rss > 256 * 1024 * 1024:
                result.update(failure='rss_budget_exceeded', max_rss_bytes=rss)
                return result
            if time.monotonic() - start > 890:
                result['failure'] = 'wall_budget_exceeded'
                return result
            if progress:
                tmp = progress.with_suffix('.tmp')
                tmp.write_text(json.dumps(dict(utc=utc(), outer_row=i,
                                               pairs_checked=pairs,
                                               max_rss_bytes=rss)) + '\n')
                tmp.replace(progress)
    if pairs != result['expected_pairs']:
        result.update(failure='pair_count_mismatch', pairs_checked=pairs)
        return result
    result.update(pass_=True, pairs_checked=pairs,
                  min_distance=minimum if count > 1 else None,
                  min_distance_witness=witness,
                  distance_histogram=dict(sorted(histogram.items())),
                  unique_pair_convention='all unordered pairs 0 <= i < j < M',
                  count_convention='number of distinct explicit codewords; not orbits')
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('object', type=Path)
    p.add_argument('--n', type=int, required=True)
    p.add_argument('--d', type=int, required=True)
    p.add_argument('--w', type=int, required=True)
    p.add_argument('--count', type=int, required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--progress', type=Path)
    a = p.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU, (880, 880))
    resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
    started = time.monotonic()
    r = check(a.object, a.n, a.d, a.w, a.count, a.sha256, a.progress)
    r['pass'] = r.pop('pass_')
    r.update(ended_utc=utc(), elapsed_seconds=time.monotonic() - started,
             max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             python_version=sys.version, threading='one main Python thread; no libraries or workers')
    a.output.write_text(json.dumps(r, indent=2, sort_keys=True) + '\n')
    print(json.dumps(r, sort_keys=True), flush=True)
    return 0 if r['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
