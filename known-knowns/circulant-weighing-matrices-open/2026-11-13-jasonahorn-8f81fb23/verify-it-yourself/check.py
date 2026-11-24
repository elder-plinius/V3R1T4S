#!/usr/bin/env python3
"""Fail-closed verification: contraction identity, C search, independent search.

Requires Python 3, NumPy and a C compiler. No downloads and no package writes.
The compiled C executable lives in a temporary directory, never in the package.
"""
import itertools
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def contractions():
    seen = set()
    orbits = []
    for x in range(13):
        if x in seen:
            continue
        orbit = []
        y = x
        while y not in seen:
            seen.add(y)
            orbit.append(y)
            y = 3 * y % 13
        orbits.append(orbit)
    rows = []
    for b in range(-3, 4):
        q, s = 27 - 3 * b * b, 3 - b
        # Energy bounds each of the four values by floor(sqrt(27)) = 5.
        for vals in itertools.product(range(-5, 6), repeat=4):
            if sum(vals) != s or sum(v * v for v in vals) != q:
                continue
            seq = [0] * 13
            seq[0] = 3 * b
            for orbit, value in zip(orbits[1:], vals):
                for p in orbit:
                    seq[p] = value
            if all(sum(seq[j] * seq[(j + t) % 13] for j in range(13)) == 0
                   for t in range(1, 13)):
                rows.append(tuple(seq))
    return sorted(set(rows))


def parse_rows(text):
    rows = [tuple(map(int, line.split())) for line in text.splitlines() if line.strip()]
    if len(rows) != 25 or any(len(row) != 13 for row in rows) or len(set(rows)) != 25:
        raise ValueError('expected 25 distinct contraction rows of length 13')
    if any(sum(row) != 9 or sum(v*v for v in row) != 81 for row in rows):
        raise ValueError('contraction normalization or energy incorrect')
    return sorted(rows)


def parse_summary(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or not lines[-1].startswith('END '):
        raise ValueError('missing final END record')
    fields = {}
    for word in lines[-1].split()[1:]:
        match = re.fullmatch(r'([a-z]+)=([0-9]+)', word)
        if not match or match[1] in fields:
            raise ValueError('malformed or duplicate END field')
        fields[match[1]] = int(match[2])
    required = {'nodes', 'hits', 'capped', 'elapsed', 'targets', 'completed', 'matches'}
    if set(fields) != required:
        raise ValueError('unexpected or missing END fields')
    if fields['hits'] != 0 or fields['capped'] != 0:
        raise ValueError('search found a solution or did not finish')
    if fields['targets'] != 25 or fields['completed'] != 25:
        raise ValueError('incomplete target coverage')
    # Counts bind this exact finite search, not merely its declared target count.
    if fields['nodes'] != 43196762 or fields['matches'] != 5519232:
        raise ValueError('unexpected search counts')
    return fields


def execute(argv, timeout):
    result = subprocess.run([str(x) for x in argv], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, timeout=timeout)
    if result.returncode:
        raise ValueError(f'command failed (exit {result.returncode}): {argv[0]}\n{result.stdout}')
    return result.stdout


def main():
    expected = contractions()
    packaged = parse_rows((ROOT / 'object/contractions.txt').read_text())
    if packaged != expected:
        raise ValueError('packaged contraction list differs from independent enumeration')
    try:
        import numpy  # noqa: F401; fail early, never install dependencies implicitly
    except ImportError as exc:
        raise ValueError('NumPy is required; see RUN_IT_YOURSELF.md') from exc
    with tempfile.TemporaryDirectory(prefix='cw208-check-') as tmp:
        binary = Path(tmp) / 'liftjoin'
        execute(['cc', '-std=c11', '-O3', '-Wall', '-Wextra', '-Werror', '-o', binary,
                 ROOT / 'how-we-built-it/liftjoin.c'], 60)
        generated = parse_rows(execute([binary, '--contractions'], 30))
        if generated != expected:
            raise ValueError('C target set differs from packaged and Python sets')
        print('CONTRACTIONS PASS: object = Python = C (25 distinct rows)', flush=True)
        selftest = execute([binary, '--selftest'], 30)
        print(selftest, end='', flush=True)
        # C self-tests exit nonzero on either positive- or negative-control failure.
        output = execute([binary, 'all', '180'], 210)
        parse_summary(output)
        print(output.splitlines()[-1], flush=True)
    independent = execute([sys.executable, ROOT / 'verify-it-yourself/independent.py', '--verify'], 180)
    print(independent, end='', flush=True)
    if not independent.rstrip().endswith('INDEPENDENT PASS: positive control, negative control, target'):
        raise ValueError('independent checker did not finish')
    print('PASS')


def cli():
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc))
        print('FAIL')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(cli())
