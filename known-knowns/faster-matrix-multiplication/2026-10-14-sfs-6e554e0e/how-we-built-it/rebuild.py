#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Replay the original source order and random stream for one frozen result."""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import sys
import urllib.request

parser=argparse.ArgumentParser()
parser.add_argument('--source-cache',type=pathlib.Path)
args=parser.parse_args()
here=pathlib.Path(__file__).resolve().parent
source_dir=here/'sources/schemes'
source_dir.mkdir(parents=True,exist_ok=True)
manifest=json.loads((here/'source-manifest.json').read_text())
for record in manifest:
    cached=args.source_cache/record['file'] if args.source_cache else None
    if cached and cached.exists():
        body=cached.read_bytes()
    else:
        request=urllib.request.Request(record['url'],headers={'User-Agent':'V3R1T4S reproducible-source fetch'})
        with urllib.request.urlopen(request,timeout=45) as response:
            body=response.read()
    if hashlib.sha256(body).hexdigest()!=record['sha256']:
        raise ValueError('source hash mismatch: '+record['file'])
    (source_dir/record['file']).write_bytes(body)
for name in ['output','result']:
    (here/name).mkdir(exist_ok=True)
sys.path.insert(0,str(here/'code'))
import synth
import dag_search
synth.ROOT=here
synth.HERE=here
sys.argv=['dag_search.py','--seconds','240','--trials','16','--seed','1','--max-rank','51']
dag_search.main()
artifact=here/'result/dag_2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json'
expected='6e554e0ee89a3fda23f7c59d261ca1f27bcb089e141db911246437ca50e931e9'
if not artifact.exists() or hashlib.sha256(artifact.read_bytes()).hexdigest()!=expected:
    raise ValueError('replayed object does not match frozen candidate')
shutil.copyfile(artifact,here/'rebuilt-scheme.json')
print('REBUILD PASS')
