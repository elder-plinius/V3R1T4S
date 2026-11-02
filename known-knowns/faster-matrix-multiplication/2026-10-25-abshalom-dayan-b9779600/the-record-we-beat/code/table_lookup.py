#!/usr/bin/env python3
"""Look one format up in every saved comparator (standard library only; reads the pages saved by the run's fetch scripts, not shipped).

Usage: table_lookup.py DATA_DIR n1 n2 n3 BUILT_RANK
DATA_DIR holds tables/ (fmm_sota.json, lille_index.html, lille_<sorted>.html and the 404 pages of the other orders,
matmulcatalog_catalog.json, matmulcatalog_COVERAGE.md, perminov_*, merlijn_tree.json, lita_schemes_listing.json).
Prints every value found for the format in any axis order, the Lille construction text, and the verdict against the
built rank. Exit status 0 if the built rank is strictly below every value found, 1 otherwise."""
import sys, os, re, json, html, itertools

D = sys.argv[1]; key = tuple(int(x) for x in sys.argv[2:5]); built = int(sys.argv[5])
T = os.path.join(D, "tables")
perms = sorted(set(itertools.permutations(key)))
name = lambda p: "x".join(map(str, p))
srt = tuple(sorted(key))
values = []   # (source, value)

def rd(f): return open(os.path.join(T, f), encoding="utf-8", errors="replace").read()
def plain(t): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", t)))
def pats(c): return [re.compile(r"(?<!\d)%d\s*[x×,]\s*%d\s*[x×,]\s*%d(?!\d)" % p) for p in perms]
def hits(text): return sum(len(p.findall(text)) for p in pats(key))
def maxdim(text): return max([max(map(int, m)) for m in re.findall(r"(?<!\d)(\d+)x(\d+)x(\d+)(?!\d)", text) if max(map(int, m)) <= 64] + [0])

print("== fmm_sota.json (sedoglavic/fmm_digest)")
s = json.load(open(os.path.join(T, "fmm_sota.json")))
S = {tuple(e["format"]): e["rank"] for e in s["entries"]}
print("createdAt", s.get("createdAt"), "entries", len(S))
for p in perms:
    print("  %s: %s" % (name(p), ("rank %d" % S[p]) if p in S else "no entry"))
    if p in S: values.append(("fmm_sota.json %s" % name(p), S[p]))
cont = sorted((r, f) for f, r in S.items() if f != key and any(all(f[i] >= p[i] for i in range(3)) for p in perms))
print("lowest formats containing the cell componentwise (restricting them gives the cell at the same or a lower rank):", cont[:5])

print("\n== Lille index https://fmm.univ-lille.fr/ (the bank's status_source)")
ct = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", rd("lille_index.html"))))
starts = list(re.finditer(r"⟨ ?(\d+) ?× ?(\d+) ?× ?(\d+) ?: ?(\d+) ?⟩ (\d+) (\d+)", ct))
rows = {}
for k, m in enumerate(starts):
    end = starts[k + 1].start() if k + 1 < len(starts) else m.end() + 400
    rows[tuple(int(x) for x in m.groups()[:3])] = (int(m.group(4)), ct[m.start():end].strip())
print("rows parsed:", len(rows))
for p in perms:
    if p in rows:
        print("  row %s: rank %d; text: %s" % (name(p), rows[p][0], rows[p][1])); values.append(("Lille index row %s" % name(p), rows[p][0]))
    else: print("  %s: no row" % name(p))

print("\n== Lille per-format pages https://fmm.univ-lille.fr/<format>.html")
for p in perms:
    f = os.path.join(T, "lille_%s.html" % name(p))
    if not os.path.exists(f): print("  %s: not fetched" % name(p)); continue
    hdr = open(f + ".headers").read().split("\n")[0].strip()
    if "404" in hdr:
        print("  %s: %s (the catalogue has pages for sorted formats only)" % (name(p), hdr)); continue
    t = plain(rd("lille_%s.html" % name(p)))
    m = re.search(r"Description of fast matrix multiplication algorithm: ⟨ ?(\d+) ?× ?(\d+) ?× ?(\d+) ?: ?(\d+) ?⟩", t)
    d = re.search(r"Algorithm definition (.*?) Algorithm description", t)
    d = re.split(r" This decomposition is defined", d.group(1))[0] if d else None
    print("  %s: %s; rank %s; definition: %s" % (name(p), hdr, m.group(4) if m else None, d))
    if m: values.append(("Lille per-format page %s" % name(p), int(m.group(4))))

print("\n== matmulcatalog docs/catalog.json (Chatain Lacelle)")
cat = json.load(open(os.path.join(T, "matmulcatalog_catalog.json")))["schemes"]
mine = sorted((e["rank"], e["lineage_compact"], ",".join(e["fields"]), e.get("external_best_rank"), e.get("external_best_source")) for e in cat if sorted(e["format"]) == list(srt))
print("schemes in the file:", len(cat))
for r, lin, fl, eb, es in mine:
    print("  rank %d  fields %s  lineage %s  (external_best_rank %s from %s)" % (r, fl, lin, eb, es)); values.append(("matmulcatalog catalog.json (%s)" % lin[:40], r))

print("\n== matmulcatalog generated/COVERAGE.md")
cov = rd("matmulcatalog_COVERAGE.md")
secs = [int(x) for x in re.findall(r"^## Section (\d+)", cov, re.M)]
print("sections up to max-dimension", max(secs), "; hits for the format in any order:", hits(cov))

print("\n== Perminov FastMatrixMultiplication")
for f in ("perminov_docs_ranks.md", "perminov_docs_additions.md", "perminov_README.md"):
    t = rd(f); print("  %s: hits %d; largest dimension in any NxMxP name %d" % (f, hits(t), maxdim(t)))
    if hits(t): values.append((f, None))
pt = json.load(open(os.path.join(T, "perminov_tree.json")))
pp = [e["path"] for e in pt["tree"] if hits(e["path"])]
print("  repository tree: %d paths, truncated %s, largest dimension in any path %d; paths for the format: %s" % (len(pt["tree"]), pt.get("truncated"), max(maxdim(e["path"]) for e in pt["tree"]), pp[:5]))

print("\n== MerlijnW70/fmm-schemes")
mt = json.load(open(os.path.join(T, "merlijn_tree.json")))
print("  tree: %d paths, truncated %s, largest dimension %d; paths for the format: %s" % (len(mt["tree"]), mt.get("truncated"), max(maxdim(e["path"]) for e in mt["tree"]), [e["path"] for e in mt["tree"] if hits(e["path"])]))

print("\n== khoruzhii/lita schemes/ listing")
ls = [e["name"] for e in json.load(open(os.path.join(T, "lita_schemes_listing.json")))]
print("  %d files; formats: %s" % (len(ls), ", ".join(re.sub(r"\.npz$", "", n) for n in ls)))
print("  rectangular schemes:", [n for n in ls if len(set(re.match(r"(\d+)x(\d+)x(\d+)", n).groups())) > 1])

vals = [(k, v) for k, v in values if v is not None]
low = min(v for k, v in vals) if vals else None
print("\n== verdict")
print("lowest value for the format in any axis order, over the sources above: %s (%s)" % (low, [k for k, v in vals if v == low][0]))
print("built rank %d; margin below the lowest value %d" % (built, low - built))
ok = low is not None and built < low and not any(v is None for k, v in values)
print("built rank strictly below every value found:", "YES" if ok else "NO")
sys.exit(0 if ok else 1)
