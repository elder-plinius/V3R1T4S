#!/usr/bin/env python3
"""Extract every published LABS row (L, printed E/F, sequence) from the fetched sources, decode the sequence
with the convention that reproduces the printed value, and write baseline/rows.tsv.

Decoding conventions tried (picked per row by matching the printed value, never assumed):
  hex-full : hex -> integer -> binary, left-padded with zeros to L (or the last/first L bits if longer)
  hex-half : same to n = (L+1)/2 bits, then skew-symmetric expansion (odd L)
  runs     : run lengths, alternating signs (full, or half + skew expansion)
Energy comes from tools/labs_energy.py (exact integers)."""
import re, sys, glob, html
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from labs_energy import energy

SRC = Path(sys.argv[1])      # extracted arXiv sources: SRC/<arxiv id>/...
DATA = Path(sys.argv[2])     # run data dir (git_labs/ html)
OUT = Path(sys.argv[3])

def skew(half):              # half = s_0..s_{n-1}; s_{n-1+i} = (-1)^i s_{n-1-i}
    n = len(half); s = list(half)
    for i in range(1, n):
        s.append((-1) ** i * half[n - 1 - i])
    return s

def bits_to_pm(b): return [1 if c == "0" else -1 for c in b]

def hex_cands(h, L):
    h = h.lower()
    v = int(h, 16); nb = 4 * len(h); full = bin(v)[2:].zfill(nb)
    out = []
    for n, kind in ((L, "hex-full"), ((L + 1) // 2, "hex-half")):
        if kind == "hex-half" and L % 2 == 0: continue
        cands = set()
        if nb >= n: cands |= {full[nb - n:], full[:n]}
        else: cands.add(full.zfill(n))
        for b in cands:
            s = bits_to_pm(b)
            out.append((kind, skew(s) if kind == "hex-half" else s))
    return out

def runs_cands(runs, L):
    out = []
    seq = []; sg = 1
    for r in runs: seq += [sg] * r; sg = -sg
    if len(seq) == L: out.append(("runs-full", seq))
    if L % 2 and len(seq) == (L + 1) // 2: out.append(("runs-half", skew(seq)))
    return out

def f_matches(L, E, F, dec):
    return abs(Fraction(L * L, 2 * E) - Fraction(F)) <= max(Fraction(1, 2 * 10 ** dec), Fraction(1, 10 ** 12))

def emin_from_f(L, F, dec):  # smallest integer E whose F rounds to the printed value
    hi = Fraction(F) + max(Fraction(1, 2 * 10 ** dec), Fraction(1, 10 ** 12))
    E = -(-Fraction(L * L) // (2 * hi))  # ceil(L^2/(2*hi))
    return int(E)

rows = []
def add(src, L, cands, pE=None, pF=None, note=""):
    L = int(L); best = None
    dec = len(pF.split(".")[1]) if pF and "." in pF else 0
    for kind, s in cands:
        E = energy(s)
        ok = (pE is not None and E == int(pE)) or (pE is None and pF and f_matches(L, E, pF, dec))
        if ok: best = (kind, s, E); break
    if best is None and cands:   # keep the lowest-energy decoding but mark it unverified
        kind, s = min(cands, key=lambda c: energy(c[1])); best = (kind + "?", s, energy(s))
    implied = int(pE) if pE is not None else (emin_from_f(L, pF, dec) if pF else None)
    seq = "".join("0" if x > 0 else "1" for x in best[1]) if best else ""
    rows.append(dict(src=src, L=L, pE=pE or "", pF=pF or "", implied=implied if implied is not None else "",
                     kind=best[0] if best else "", E=best[2] if best else "", seq=seq, note=note))

def clean(t): return re.sub(r"\\allowbreak|\\-|\{|\}|\$|\\mathbf|\\textbf", "", t)

# Knauer 2004 table (git_labs copy)
t = html.unescape(re.sub(r"<[^>]*>", " ", (DATA / "git_labs/2004-Knauer-original.html").read_text(errors="replace")))
hdr = list(re.finditer(r"^\s*(\d{2,3})(\*?)\s+(\d+)\s+(\d+\.\d+)\s", t, re.M))
for j, m in enumerate(hdr):
    L, star, E, F = m.groups()
    body = t[m.end(): hdr[j + 1].start() if j + 1 < len(hdr) else len(t)]
    runs, tot = [], 0
    for x in re.findall(r"\d+", body):          # runs until they sum to L (or to (L+1)/2 for a skew half)
        if tot >= int(L): break
        runs.append(int(x)); tot += int(x)
    add("knauer2004", L, runs_cands(runs, int(L)) + runs_cands(runs[:next((i + 1 for i in range(len(runs)) if sum(runs[:i + 1]) == (int(L) + 1) // 2), 0)], int(L)), pE=E, note="starred" if star else "")

# 1406.5301 (Boskovic, Brglez, Brest) new records, run-length half coordinates
t = (SRC / "1406.5301/Tables/tb_new_records.tex").read_text()
for m in re.finditer(r"^(\d{3}) & ([\d.]+) & (\d+) &\s*\n([\d,]+)", t, re.M):
    L, F, E, rl = m.groups(); add("1406.5301", L, runs_cands([int(x) for x in rl.split(",") if x], int(L)), pE=E, pF=F)

# 1512.02475 (Packebusch, Mertens) digit-run tables
t = (SRC / "1512.02475/labs-15.tex").read_text()
for m in re.finditer(r"^\s*(\d{2,3}) & (\d+) & ([\d.]+)\S* & ([0-9A-Za-z]+)", t, re.M):
    L, E, F, rl = m.groups()
    if int(L) < 67: continue
    runs = [int(c, 36) for c in rl]
    add("1512.02475", L, runs_cands(runs, int(L)), pE=E, pF=F)

# 2011.00068 (Brest, Boskovic) L 201..303
t = (SRC / "2011.00068/tb_best201-303--PSL.tex").read_text()
for m in re.finditer(r"^(\d{3}) & ([\d.]+)\S* & ([0-9A-Fa-f]+) &", t, re.M):
    L, F, h = m.groups(); add("2011.00068", L, hex_cands(h, int(L)), pF=F)

# 2206.12070 (Dimitrov et al.): new MF with sequence; old MF printed without sequence
t = clean((SRC / "2206.12070/bare_jrnl.tex").read_text())
for m in re.finditer(r"^\s*(\d{3,4})\s*&[^&]*&\s*([0-9A-Fa-f ]+?)\s*&\s*([\d.]+|-+|)\s*&\s*([\d.]+)", t, re.M):
    L, h, old, new = m.groups()
    add("2206.12070", L, hex_cands(h.replace(" ", ""), int(L)), pF=new)
    if re.match(r"^\d+\.\d+$", old): add("2206.12070-oldMF", L, [], pF=old, note="cited previous value, no sequence")

# 2210.15962 (Boskovic et al., GPU solver): E printed, half sequence in hex
t = (SRC / "2210.15962/paper.tex").read_text()
for m in re.finditer(r"^\s*(\d{3}) & (\d+) & ([\d.]+) & .*?0x([0-9A-Fa-f]+)", t, re.M):
    L, E, F, h = m.groups(); add("2210.15962", L, hex_cands(h, int(L)), pE=E, pF=F)

# 2409.07222 (Dual-step) 450..527: previous F, new F, hex
t = clean((SRC / "2409.07222/table.tex").read_text())
for m in re.finditer(r"^(\d{3}) & ([\d.]+) & ([\d.]+) & ([0-9a-fA-F ]+)", t, re.M):
    L, old, new, h = m.groups(); add("2409.07222", L, hex_cands(h.replace(" ", ""), int(L)), pF=new)
    add("2409.07222-prevF", L, [], pF=old, note="cited previous value, no sequence")

# 2607.09688 (Psenicnik et al.) 450..527, 573
t = clean((SRC / "2607.09688/TAB_RECORDS.tex").read_text())
for m in re.finditer(r"^(\d{3}) & ([\d.]+) & ([\d.]+) & ([0-9a-fA-F \n]+?)(\\\\|$)", t, re.M):
    L, old, new, h, _ = m.groups(); add("2607.09688", L, hex_cands(re.sub(r"\s", "", h), int(L)), pF=new)
    add("2607.09688-prevF", L, [], pF=old, note="cited previous value, no sequence")

# 2106.03377 (Dimitrov et al.): one example sequence (hex over several lines, then MF)
t = (SRC / "2106.03377/bare_jrnl.tex").read_text()
for m in re.finditer(r"^(\d{3}) &\s*\n([0-9a-fA-F\s]+?)\s*&\s*([\d.]+)", t, re.M):
    L, h, F = m.groups(); add("2106.03377", L, hex_cands(re.sub(r"\s", "", h), int(L)), pF=F)

# 2504.00987 (GPU memetic tabu) 92..120: previous E, new E, previous F, new F, hex (continuation rows)
t = (SRC / "2504.00987/main.tex").read_text(); curL = None; curE = None
for line in t.splitlines():
    m = re.match(r"^\s*(\d*)\s*&\s*(\d*)\s*&\s*(\d*)\s*&\s*([\d.]*)\s*&\s*([\d.]*)\s*&\s*([0-9A-F]{15,})\s*&", line)
    if not m: continue
    L, oldE, newE, oldF, newF, h = m.groups()
    if L: curL, curE = int(L), newE; add("2504.00987-prevE", L, [], pE=oldE, note="cited previous value")
    add("2504.00987", curL, hex_cands(h, curL), pE=curE)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w") as f:
    cols = ["src", "L", "pE", "pF", "implied", "kind", "E", "seq", "note"]
    f.write("\t".join(cols) + "\n")
    for r in rows: f.write("\t".join(str(r[c]) for c in cols) + "\n")
from collections import Counter
print("rows", len(rows)); print(Counter((r["src"], r["kind"]) for r in rows))
