#!/usr/bin/env python3
"""Scan the saved V3R1T4S pull-request listing, PR file lists, main tree, INDEX.csv, TROPHY_CASE.md and the two arXiv
API results for one format (any axis order) and for given rank numbers. Standard library only.

Usage: novelty_scan.py DATA_DIR n1 n2 n3 RANK [RANK ...]
DATA_DIR holds prs/ (pulls_all_p*.json, files/pr<N>.json, v3r1t4s_tree_main.json, fmm_INDEX.csv, TROPHY_CASE.md) and
lit/ (arxiv_*.xml). Matching is on title and body text, with the formats written as 20x21x21, 20×21×21, <20,21,21>,
(20, 21, 21), [20,21,21], 20,21,21 or 20 21 21, and on the bare rank numbers (not inside longer numbers)."""
import sys, os, re, json, glob, itertools

D = sys.argv[1]; key = tuple(int(x) for x in sys.argv[2:5]); ranks = [int(x) for x in sys.argv[5:]]
perms = sorted(set(itertools.permutations(key)))
fmt_pats = []
for p in perms:
    a, b, c = p
    fmt_pats += [re.compile(x) for x in (r"(?<!\d)%d\s*[x×]\s*%d\s*[x×]\s*%d(?!\d)" % p, r"[<(\[]\s*%d\s*,\s*%d\s*,\s*%d\s*[>)\]]" % p,
                                         r"(?<![\d,])%d\s*,\s*%d\s*,\s*%d(?![\d,])" % p, r"(?<!\d)%d\s+%d\s+%d(?!\d)" % p)]
rank_pats = {r: re.compile(r"(?<![\d.,])%d(?![\d])" % r) for r in ranks}

prs = []
for f in sorted(glob.glob(os.path.join(D, "prs", "pulls_all_p*.json")), key=lambda x: int(re.search(r"_p(\d+)\.json", x).group(1))):
    prs += json.load(open(f))
st = {}
for p in prs: st["merged" if p.get("merged_at") else p["state"]] = st.get("merged" if p.get("merged_at") else p["state"], 0) + 1
print("== pull requests of elder-plinius/V3R1T4S (all states): %d (#%d to #%d); %s" % (len(prs), min(p["number"] for p in prs), max(p["number"] for p in prs), st))
fmt_hits, rank_hits = [], []
for p in prs:
    t = (p["title"] or "") + "\n" + (p["body"] or "")
    if any(x.search(t) for x in fmt_pats): fmt_hits.append(p)
    r = [k for k, x in rank_pats.items() if x.search(t)]
    if r: rank_hits.append((p, r))
def desc(p): return "#%d (%s, created %s) %s" % (p["number"], "merged" if p.get("merged_at") else p["state"], p["created_at"], (p["title"] or "")[:100])
print("PRs whose title or body names the format in any order and notation: %d" % len(fmt_hits))
for p in fmt_hits: print("   " + desc(p))
print("PRs whose title or body contains one of the numbers %s: %d" % (ranks, len(rank_hits)))
for p, r in rank_hits: print("   %s  [numbers %s]" % (desc(p), r))

print("\n== file names of the FMM-related pull requests (first page of up to 100 files each)")
files = sorted(glob.glob(os.path.join(D, "prs", "files", "pr*.json")), key=lambda x: int(re.search(r"pr(\d+)\.json", x).group(1)))
tot = 0; trunc = []; fh = []; mx = {}
name_pat = re.compile(r"(?<![0-9a-f])(\d+)x(\d+)x(\d+)(?![0-9a-z])")
for f in files:
    n = int(re.search(r"pr(\d+)\.json", f).group(1)); L = json.load(open(f)); tot += len(L)
    if len(L) >= 100: trunc.append(n)
    for e in L:
        for m in name_pat.finditer(e["filename"]):
            t = tuple(int(x) for x in m.groups())
            mx[n] = max(mx.get(n, 0), max(t))
            if tuple(sorted(t)) == tuple(sorted(key)): fh.append((n, e["filename"]))
        if any(rank_pats[r].search(e["filename"]) for r in ranks): fh.append((n, e["filename"]))
print("%d pull requests, %d file names; PRs with 100 or more files (only the first 100 listed, a limit of this scan): %s" % (len(files), tot, trunc))
print("file names naming the format (any order) or containing one of the numbers: %s" % (fh or "none"))
print("largest NxMxP in an FMM PR's file names, PRs with a dimension of 17 or more:", {k: v for k, v in sorted(mx.items()) if v >= 17})

print("\n== main branch")
tr = json.load(open(os.path.join(D, "prs", "v3r1t4s_tree_main.json")))
paths = [e["path"] for e in tr["tree"]]
ph = [p for p in paths if any(x.search(p) for x in fmt_pats[::4] + fmt_pats[1::4])]
print("tree: %d paths, truncated %s; paths naming the format: %s" % (len(paths), tr.get("truncated"), ph or "none"))
for f in ("fmm_INDEX.csv", "TROPHY_CASE.md"):
    t = open(os.path.join(D, "prs", f), encoding="utf-8").read()
    print("%s: names the format: %s; contains one of the numbers: %s" % (f, any(x.search(t) for x in fmt_pats), [k for k, x in rank_pats.items() if x.search(t)]))

print("\n== arXiv API results")
for f in sorted(glob.glob(os.path.join(D, "lit", "arxiv_*.xml"))):
    t = open(f, encoding="utf-8").read()
    ents = re.findall(r"<entry>(.*?)</entry>", t, re.S)
    dates = sorted(re.search(r"<published>(.*?)</published>", e).group(1)[:10] for e in ents)
    h = []
    for e in ents:
        tx = re.sub(r"\s+", " ", e).replace("×", "x")
        if any(x.search(tx) for x in fmt_pats) or any(x.search(tx) for x in rank_pats.values()):
            h.append(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1)))
    print("%s: %d entries, published %s to %s; entries naming the format or one of the numbers: %s" % (os.path.basename(f), len(ents), dates[0], dates[-1], h or "none"))
