#!/usr/bin/env python3
"""Regenerate the CNF named by object/cnf_spec.json with the shipped encoder and compare it with the spec.
The spec must name the cell (m,k,n) = (2,5,13); the regenerated file must have the recorded sha256 and header.
usage: spec_check.py cnf_spec.json encode_schutte.py out.cnf"""
import hashlib, json, subprocess, sys
spec_path, enc, out = sys.argv[1:4]
s = json.load(open(spec_path))
if (s.get("m"), s.get("k"), s.get("n")) != (2, 5, 13):
    print(f"spec names (m,k,n) = {(s.get('m'), s.get('k'), s.get('n'))}, not (2,5,13)"); sys.exit(1)
r = subprocess.run([sys.executable, enc, str(s["m"]), str(s["k"]), str(s["n"]), "--sb", s["sb"], "-o", out])
if r.returncode != 0: print("encoder failed"); sys.exit(1)
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
hdr = open(out).readlines()[1].split()
ok = h == s["cnf_sha256"] and hdr == ["p", "cnf", str(s["cnf_vars"]), str(s["cnf_clauses"])]
print(f"regenerated CNF: {hdr[2]} variables, {hdr[3]} clauses, sha256 {h}")
print("matches object/cnf_spec.json" if ok else "DOES NOT match object/cnf_spec.json")
sys.exit(0 if ok else 1)
