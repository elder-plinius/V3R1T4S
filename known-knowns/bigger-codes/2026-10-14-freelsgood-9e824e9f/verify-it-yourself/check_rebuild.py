#!/usr/bin/env python3
"""Run the inspected author module and compare reconstructed bytes twice."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('author_code', type=Path)
p.add_argument('witness', type=Path)
a = p.parse_args()
spec = importlib.util.spec_from_file_location('author_reconstruction', a.author_code)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
expected = a.witness.read_bytes()
for run in range(1, 3):
    words = m.rebuild_code()
    assert m.verify_code(words)
    rebuilt = ''.join(f'{word:027b}\n' for word in words).encode('ascii')
    assert rebuilt == expected, 'reconstruction differs from saved witness bytes'
    print(json.dumps({'run':run,'count':len(words),'bytes':len(rebuilt),'sha256':hashlib.sha256(rebuilt).hexdigest(),'exact_byte_match':True,'author_verifier':True}),flush=True)
print('REPRODUCTION: PASS')
