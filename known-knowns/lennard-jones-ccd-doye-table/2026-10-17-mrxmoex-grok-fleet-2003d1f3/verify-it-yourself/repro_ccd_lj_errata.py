#!/usr/bin/env python3
"""Repro for the CCD Lennard-Jones table errata N = 602, 486, 487, 813, 899.
Python 3 standard library only. Downloads everything from the live sources at run time; nothing is bundled.
  default         : CCD tables + CCD point files (~0.2 MB, a few seconds)
  --with-sources  : also the original authors' 2004 archive (Nankai, 4.6 MB) and the Barron 2005 PDF (hash only)
Energies: E = sum_{i<j} 4 (r^-12 - r^-6), epsilon = sigma = 1, on the coordinates exactly as posted.
(A tight L-BFGS polish moves these by < 4e-8; see how-we-built-it/. Not needed for any check here.)"""
import csv, hashlib, io, os, re, sys, tarfile, time, urllib.request
CCD = "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ"
NK = "https://chinfo.nankai.edu.cn/chmm/pubmats/LJ"
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = {r["url"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "SOURCES.csv")))}
fails = []
def get(url):
    for k in range(3):  # small retry: some mirrors drop TLS handshakes intermittently
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ccd-lj-errata-repro"}), timeout=180) as r:
                b = r.read(); lm = r.headers.get("Last-Modified", ""); break
        except OSError as e:
            if k == 2: raise
            print(f"    retry {url}: {e}"); time.sleep(5)
    h = hashlib.sha256(b).hexdigest(); exp = SRC.get(url, {}).get("sha256", "")
    note = "" if not exp else ("sha256 matches SOURCES.csv" if h == exp else "NOTE: sha256 differs from SOURCES.csv (file updated since 2026-10-17?)")
    print(f"  {url}\n    {len(b)} B  sha256 {h}  Last-Modified {lm or '-'}  {note}")
    return b
def coords(txt):  # 3-column (x y z) or all-numeric 4+-column (index x y z) rows; header lines skipped
    out = []
    for l in txt.splitlines():
        p = l.split()
        if len(p) >= 3 and all(re.fullmatch(r"[-+0-9.eEdD]+", x) for x in p):
            out.append(tuple(float(x.replace("D", "E").replace("d", "e")) for x in p[-3:]))
    return out
def lj(X):
    e = 0.0
    for i in range(len(X)):
        xi, yi, zi = X[i]
        for j in range(i + 1, len(X)):
            r2 = (xi - X[j][0]) ** 2 + (yi - X[j][1]) ** 2 + (zi - X[j][2]) ** 2; ir6 = 1.0 / r2 ** 3; e += ir6 * ir6 - ir6
    return 4 * e
def check(label, cond):
    print(f"  [{'ok' if cond else 'FAIL'}] {label}")
    if not cond: fails.append(label)
print("1. CCD tables")
tab = {}
for page in ("LJ310-561", "LJ562-1000"):
    t = get(f"{CCD}/{page}.html").decode("latin-1")
    for m in re.finditer(r'<a\s+href="([^"]+)"\s*>\s*(\d+)\s*</a>\s*</td>\s*<td>\s*(-\d+\.\d+)', t, re.I): tab[int(m.group(2))] = (m.group(1), float(m.group(3)))
for N in (601, 602, 486, 487, 813, 899): print(f"  row N={N}: href={tab[N][0]}  E_table={tab[N][1]}")
print("2. N=602 link")
check("row 602 links to LJ562-1000/601.TXT", tab[602][0] == "LJ562-1000/601.TXT")
X = coords(get(f"{CCD}/LJ562-1000/601.TXT").decode("latin-1")); E = lj(X)
print(f"  linked file: {len(X)} atoms, E = {E:.6f}  (row 601 table {tab[601][1]}, row 602 table {tab[602][1]})")
check("linked file has 601 atoms and the N=601 energy", len(X) == 601 and abs(E - tab[601][1]) < 1e-5)
X = coords(get(f"{CCD}/LJ562-1000/602.TXT").decode("latin-1")); E = lj(X)
print(f"  unlinked CCD 602.TXT: {len(X)} atoms, E = {E:.6f}")
check("CCD 602.TXT has 602 atoms and matches the 602 table value", len(X) == 602 and abs(E - tab[602][1]) < 1e-5)
print("3. table value above the posted file's own energy")
BARRON = {486: -3278.672947, 487: -3285.966242, 813: -5712.251749, 899: -6371.011483}
EXP = {486: -0.030769, 487: -0.040000, 813: -6.88e-4, 899: -6.96e-5}
for N in (486, 487, 813, 899):
    href, Et = tab[N]; X = coords(get(f"{CCD}/{href}").decode("latin-1")); E = lj(X); d = E - Et
    print(f"  N={N}: {len(X)} atoms  table {Et:.6f}  file {E:.6f}  file-table {d:+.6g}  (Barron 2005: {BARRON[N]})")
    check(f"N={N}: {N} atoms, file below table by {EXP[N]:+.3g} (+/-2%)", len(X) == N and abs(d - EXP[N]) < 0.02 * abs(EXP[N]) + 2e-6)
if "--with-sources" in sys.argv:
    print("4. original authors' 2004 archive and Barron 2005 (hash checks)")
    try: tgz = get(f"{NK}/LJ562-1000.tar.gz")
    except OSError as e: tgz = None; print(f"  SKIP: Nankai archive unreachable from here ({e}); not counted as FAIL")
    if tgz:
      m = tarfile.open(fileobj=io.BytesIO(tgz)).extractfile("./LJ562-1000/602.TXT").read(); X = coords(m.decode("latin-1"))
      check("Nankai 602.TXT: 602 atoms, energy = table 602, byte-identical to CCD 602.TXT", len(X) == 602 and abs(lj(X) - tab[602][1]) < 1e-5 and hashlib.sha256(m).hexdigest() == "9c7b80219a96e1552d2bf8521f2cdd98b1eb45939a5011dc1b74195bb9858043")
    try: get("https://academicos.azc.uam.mx/cbr/PDF/MSSEMSCO_CBR_tables.pdf")
    except OSError as e: print(f"  SKIP: Barron PDF unreachable from here ({e})")
    print("  Barron values are read from Tables 18-27 ('minimum' column), (`pdftotext -layout`, then find the row 'N  1  <initial>  <minimum> ...').")
print("PASS" if not fails else f"FAIL ({len(fails)}): " + "; ".join(fails))
sys.exit(1 if fails else 0)
