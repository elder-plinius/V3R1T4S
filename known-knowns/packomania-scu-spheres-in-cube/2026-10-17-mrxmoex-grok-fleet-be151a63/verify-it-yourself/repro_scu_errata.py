#!/usr/bin/env python3
"""Repro for the Packomania scu data-integrity erratum (N=83, N=507). Python 3 stdlib only.

Re-downloads every source from packomania.com at run time (no Packomania data ships in
this package), prints sha256 + Last-Modified of what it got, compares with SOURCES.csv,
and recomputes r* = min(min_{i<j}|c_i-c_j|/2, 1/2 - max|coord|) on [-1/2,1/2]^3
with Decimal (60 digits).

  python3 verify-it-yourself/repro_scu_errata.py            # N=83 and N=507 (~3 small files)
  python3 verify-it-yourself/repro_scu_errata.py --rowcount # also re-derive the N-1 row list
                                                            # (downloads scu_coords.tar.gz, ~182 MB)
Exit 0 and last line 'PASS' when both N are short of radius.txt by > 1e-9.
"""
import csv, json, hashlib, io, itertools, os, sys, tarfile, urllib.request
from decimal import Decimal as D, getcontext
getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
BASE = "https://packomania.com/scu/txt/"
CLAIM = json.load(open(os.path.join(HERE, "CLAIM.json")))
def fsha(p): return hashlib.sha256(open(os.path.join(PKG, p), "rb").read()).hexdigest()
ok = True
for p, h in CLAIM["object_sha256"].items():
    if fsha(p) != h: print("%s: sha256 differs from CLAIM.json (package altered)" % p); ok = False
CELLS = {int(r["N"]): r for r in csv.DictReader(open(os.path.join(PKG, "object", "scu_errata_cells.csv")))}
EXPECT = {N: CELLS[N]["rstar_posted_coords"] for N in (83, 507)}
MARGIN = D("1e-9")
REC = {r["url"]: r for r in csv.DictReader(open(os.path.join(PKG, "SOURCES.csv")))}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-scu-errata-repro"})
    with urllib.request.urlopen(req, timeout=300) as r:
        b = r.read(); lm = r.headers.get("Last-Modified", "?")
    h = hashlib.sha256(b).hexdigest(); rec = REC.get(url)
    note = "" if rec is None else ("matches SOURCES.csv" if rec["sha256"] == h else
           "DIFFERS from SOURCES.csv (%s): Packomania has changed this file since packaging" % rec["sha256"][:12])
    print("fetched %s  sha256 %s  Last-Modified %s  %s" % (url, h, lm, note))
    return b

def centres(text):
    out = []
    for line in text.splitlines():
        p = line.split()
        if len(p) >= 4 and not p[0].startswith("#"): out.append([D(x) for x in p[1:4]])
    return out

def rstar(P):
    w = min(D("0.5") - max(abs(x) for x in c) for c in P)
    d2 = min(sum((a - b) ** 2 for a, b in zip(P[i], P[j])) for i, j in itertools.combinations(range(len(P)), 2))
    return min(d2.sqrt() / 2, w)

tab = {}
for line in fetch(BASE + "radius.txt").decode().splitlines():
    s = line.split()
    if len(s) >= 2 and s[0].isdigit(): tab[int(s[0])] = s[1]
for N in (83, 507):
    P = centres(fetch(BASE + "scu%d.txt" % N).decode())
    if len(P) != N: print("N=%d: file has %d rows, expected %d" % (N, len(P), N)); ok = False; continue
    r = rstar(P); cell = D(tab[N]); gap = r - cell
    if tab[N] != CELLS[N]["radius_txt"]: print("N=%d: live radius.txt %s differs from packaged %s" % (N, tab[N], CELLS[N]["radius_txt"])); ok = False
    print("N=%d  r*(posted coords) %s  radius.txt %s  gap %.3e" % (N, r, cell, gap))
    if not str(r).startswith(EXPECT[N][:-1]): print("N=%d: r* differs from the packaged value %s" % (N, EXPECT[N])); ok = False
    if not gap < -MARGIN: print("N=%d: posted coordinates now certify the posted radius (gap >= -1e-9)" % N); ok = False

if "--rowcount" in sys.argv:
    tf = tarfile.open(fileobj=io.BytesIO(fetch(BASE + "scu_coords.tar.gz")), mode="r:gz")
    short = []
    for m in tf.getmembers():
        b = os.path.basename(m.name)
        if not (m.isfile() and b.startswith("scu") and b.endswith(".txt") and b[3:-4].isdigit()): continue
        N = int(b[3:-4])
        if N > 1000: continue
        n = len(centres(tf.extractfile(m).read().decode()))
        if n == N - 1: short.append(N)
        elif n != N: print("N=%d: %d coordinate rows (neither N nor N-1)" % (N, n))
    short.sort()
    ref = [int(r["N"]) for r in csv.DictReader(open(os.path.join(PKG, "object", "scu_files_with_N-1_rows.csv")))]
    print("files (N<=1000) with only N-1 coordinate rows: %d; %s object/scu_files_with_N-1_rows.csv"
          % (len(short), "identical to" if short == ref else "DIFFERENT from"))
    if short != ref: ok = False
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
