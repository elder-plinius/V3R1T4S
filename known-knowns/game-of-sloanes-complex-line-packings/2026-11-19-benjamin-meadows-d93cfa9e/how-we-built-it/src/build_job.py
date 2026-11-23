#!/usr/bin/env python3
"""Rebuild job.json, the exact input of the search job for this cell, from job_inputs.json.

job_inputs.json names every packing the job was given (same-cell seeds, (d, n+1) parents for delete moves,
(d, n-1) children for add moves) by a public URL and the sha256 of the file's bytes; this script fetches each
file, checks the sha256, parses the 2*d*m numbers and writes job.json in the form gos_kernel.py reads.
usage: python3 build_job.py            (run in this folder; needs network access; standard library only)
"""
import hashlib, json, urllib.request

spec = json.load(open('job_inputs.json'))
d, n = spec['d'], spec['n']
job = {k: v for k, v in spec.items() if k not in ('seeds', 'parents', 'children')}
for role, m in (('seeds', n), ('parents', n + 1), ('children', n - 1)):
    job[role] = []
    for x in spec[role]:
        data = urllib.request.urlopen(x['url'], timeout=60).read()
        h = hashlib.sha256(data).hexdigest()
        if h != x['sha256']:
            raise SystemExit('sha256 mismatch for %s: got %s' % (x['url'], h))
        vals = [float(t) for line in data.decode().splitlines() if line.strip() and not line.startswith('#') for t in line.split()]
        if len(vals) != 2 * d * m:
            raise SystemExit('%s: %d numbers, expected %d' % (x['url'], len(vals), 2 * d * m))
        job[role].append(dict(src=x['src'], vals=vals))
        print('ok %-8s %-28s %s' % (role, x['src'], h[:16]))
json.dump([job], open('job.json', 'w'))
print('wrote job.json')
