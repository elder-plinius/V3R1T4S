#!/usr/bin/env python3
"""Checker for bank target site-percolation-2-uniform-lattices-thresholds (run 2026-10-16-0245).

Written from the bank's success criterion before any attack output exists. Standard library only.

  q9_check.py table HTML                 parse the live Wikipedia '2-uniform lattices' table, print it as JSON
  q9_check.py lattice GAPS [W H]         build a row-type tiling on a W x H-period torus from its gap word
                                         (T = triangle strip, S = square strip), print degree counts,
                                         vertex-configuration fractions and z-bar computed from the graph
  q9_check.py claim CLAIM.json HTML      judge a claim file literally against the criterion (full win, p2)
  q9_check.py selftest HTML              known-positive and known-negative tests

Row-type tilings. Vertices sit on horizontal rows y = 0..R-1 (R = len(word) * H), x = 0..W-1 periodic.
Every row has edges (x,y)-(x+1,y). Gap y (between rows y and y+1) of type S adds (x,y)-(x,y+1);
type T adds (x,y)-(x,y+1) and (x+1,y)-(x,y+1). The faces above a vertex are then 3 triangles (T) or
2 squares (S), so a vertex between gaps (below, above) has configuration T/T 3^6, T/S 3^3.4^2, S/S 4^4.
The word's last gap wraps to row 0 (torus in both directions).
"""
import json, math, re, html as htmlmod, sys
from fractions import Fraction
from collections import Counter

KAGOME_SITE_EXACT = 1 - 2 * math.sin(math.pi / 18)            # = honeycomb bond (Sykes-Essam)
T3122_SITE_EXACT = math.sqrt(1 - 2 * math.sin(math.pi / 18))   # (3,12^2) site (Suding-Ziff 1999)

# --- thresholds frozen in PREREG.md -------------------------------------------------------------
SIGMA_MAX = 2e-6          # stated one-sigma uncertainty of the site value
AGREE_K = 3.0             # (a) methods agree within 3 combined sigma
TABLE_K = 3.0             # (b) within 3 sigma of the table value
BOND6_TOL = 1e-6          # (c) "reproduces ... to at least 6 digits": |delta| <= 1e-6 and sigma <= 1e-6
CAL6_TOL = 1e-6           # (c) calibration site value, same rule
P2_SIGMA_MAX = 5e-8       # p2 "to at least 7 digits": stated one-sigma <= 5e-8 (half a unit of the 7th decimal)


def sup_clean(x):
    x = re.sub(r'<sup[^>]*class="[^"]*reference[^"]*".*?</sup>',
               lambda m: '[ref:' + re.sub(r'<.*?>', '', m.group(0)) + ']', x, flags=re.S)
    x = re.sub(r'<sup[^>]*>(.*?)</sup>', r'^\1', x, flags=re.S)
    x = re.sub(r'<sub[^>]*>(.*?)</sub>', r'_\1', x, flags=re.S)
    x = re.sub(r'<.*?>', '', x, flags=re.S)
    return re.sub(r'\s+', ' ', htmlmod.unescape(x)).strip()


def parse_val(s):
    m = re.match(r'\s*([0-9]*\.[0-9]+)\((\d+)\)', s)
    if not m:
        return None
    v, e = m.group(1), m.group(2)
    dec = len(v.split('.')[1])
    return {"value": float(v), "sigma": int(e) * 10.0 ** (-dec), "text": v + '(' + e + ')',
            "citation_needed": 'citation needed' in s}


def parse_config(s):
    """'(1^⁄2)(3^6) + (1^⁄2)(3^3,4^2)' -> {'3^6': 1/2, '3^3.4^2': 1/2} (fractions as Fraction)."""
    out = {}
    s = s.replace('⁄', '/').replace(' ', '')
    for m in re.finditer(r'\((\d+)\^?/(\d+)\)\(([^)]*)\)(\*?)', s):
        num, den, cfg = int(m.group(1)), int(m.group(2)), m.group(3)
        parts = []
        for p in cfg.split(','):
            p = p.replace('^', '')
            # a part is a polygon size with an optional exponent; polygon sizes here are 3,4,6,12
            mm = re.fullmatch(r'(12|3|4|6)(\d*)', p)
            if not mm:
                parts.append('?' + p)
                continue
            parts.append(mm.group(1) + ('^' + mm.group(2) if mm.group(2) else ''))
        out['.'.join(parts)] = out.get('.'.join(parts), Fraction(0)) + Fraction(num, den)
    return out


def parse_table(path):
    s = open(path, encoding='utf-8').read()
    i = s.find('id="2-uniform_lattices"')
    if i < 0:
        raise SystemExit('2-uniform section not found')
    j = s.find('<table', i)
    k = s.find('</table>', j)
    rows = []
    for r in re.findall(r'<tr.*?</tr>', s[j:k], re.S):
        cells = [sup_clean(c) for c in re.findall(r'<t[hd].*?</t[hd]>', r, re.S)]
        if len(cells) < 6 or not cells[0].strip().isdigit():
            continue
        rows.append({"num": int(cells[0]), "lattice": cells[1], "config": {k2: str(v) for k2, v in parse_config(cells[1]).items()},
                     "starred": cells[1].rstrip().endswith('*'), "z": cells[2], "zbar_text": cells[3],
                     "site": parse_val(cells[4]), "bond": parse_val(cells[5])})
    return rows


def build_rowtype(word, W, H):
    """Explicit torus graph: returns (n_vertices, adjacency sets, per-vertex (below, above) gap types)."""
    R = len(word) * H
    idx = lambda x, y: (y % R) * W + (x % W)
    adj = [set() for _ in range(W * R)]
    def add(a, b):
        if a == b:
            raise ValueError('self loop')
        adj[a].add(b); adj[b].add(a)
    for y in range(R):
        g = word[y % len(word)]
        for x in range(W):
            add(idx(x, y), idx(x + 1, y))
            add(idx(x, y), idx(x, y + 1))
            if g == 'T':
                add(idx(x + 1, y), idx(x, y + 1))
    kinds = []
    for y in range(R):
        below, above = word[(y - 1) % len(word)], word[y % len(word)]
        for x in range(W):
            kinds.append((below, above))
    return W * R, adj, kinds


def rowtype_stats(word, W=12, H=4):
    n, adj, kinds = build_rowtype(word, W, H)
    deg = Counter(len(a) for a in adj)
    name = {('T', 'T'): '3^6', ('T', 'S'): '3^3.4^2', ('S', 'T'): '3^3.4^2', ('S', 'S'): '4^4'}
    cfg = Counter(name[k] for k in kinds)
    # consistency: configuration implies degree (3^6 -> 6, 3^3.4^2 -> 5, 4^4 -> 4)
    want = {'3^6': 6, '3^3.4^2': 5, '4^4': 4}
    for v, k in enumerate(kinds):
        if len(adj[v]) != want[name[k]]:
            raise AssertionError('degree/configuration mismatch at vertex %d' % v)
    fr = {k: Fraction(c, n) for k, c in cfg.items()}
    zbar = Fraction(sum(len(a) for a in adj), n)
    return {"n": n, "degrees": dict(sorted(deg.items())), "config": {k: str(v) for k, v in sorted(fr.items())},
            "zbar": str(zbar), "edges_per_vertex": str(Fraction(sum(len(a) for a in adj), 2 * n))}


def zbar_from_text(t):
    t = t.replace('⁄', '/').replace(' ', ' ').strip()
    m = re.fullmatch(r'(\d+)\s+(\d+)/(\d+)', t)
    if m:
        return Fraction(int(m.group(1))) + Fraction(int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r'(\d+)(\d)/(\d+)', t)          # '31⁄3' as rendered = 3 1/3
    if m:
        return Fraction(int(m.group(1))) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(t)


def judge(claim, rows):
    res, ok = [], True
    def chk(name, cond, detail):
        nonlocal ok
        res.append(("PASS" if cond else "FAIL") + "  " + name + ": " + detail)
        ok = ok and bool(cond)
    row = next((r for r in rows if r["num"] == int(claim["table_num"])), None)
    chk("table row exists", row is not None, "#%s" % claim["table_num"])
    if row is None:
        return False, res
    chk("row not starred twin", not row["starred"], row["lattice"])
    st = rowtype_stats(claim["gaps"], 12, 4)
    want_cfg = {k: str(Fraction(v)) for k, v in row["config"].items()}
    chk("vertex-configuration fractions match table", st["config"] == want_cfg, "graph %s vs table %s" % (st["config"], want_cfg))
    chk("z-bar matches table", Fraction(st["zbar"]) == zbar_from_text(row["zbar_text"]), "graph %s vs table %s" % (st["zbar"], row["zbar_text"]))
    p, s = float(claim["site"]["value"]), float(claim["site"]["sigma"])
    chk("sigma <= 2e-6", s <= SIGMA_MAX, "sigma = %.3g" % s)
    ms = claim["methods"]
    chk("two methods", len(ms) >= 2 and len({m["name"] for m in ms}) >= 2, ", ".join(m["name"] for m in ms))
    if len(ms) >= 2:
        a, b = ms[0], ms[1]
        d, cs = abs(a["value"] - b["value"]), math.hypot(a["sigma"], b["sigma"])
        chk("(a) methods agree within 3 combined sigma", d <= AGREE_K * cs, "|%.10f - %.10f| = %.3g vs 3*%.3g" % (a["value"], b["value"], d, cs))
    t = row["site"]
    d = abs(p - t["value"])
    chk("(b) within 3 sigma of table (combined)", d <= TABLE_K * math.hypot(s, t["sigma"]), "|%.8f - %s| = %.3g, table sigma %.1g" % (p, t["text"], d, t["sigma"]))
    bo = claim.get("bond_same_code")
    if bo:
        d = abs(bo["value"] - row["bond"]["value"])
        chk("(c) bond reproduced to 6 digits", d <= BOND6_TOL and bo["sigma"] <= BOND6_TOL,
            "|%.10f - %s| = %.3g, sigma %.3g (strict half-unit: %s)" % (bo["value"], row["bond"]["text"], d, bo["sigma"], "yes" if d <= 5e-7 else "no"))
    else:
        chk("(c) bond reproduced to 6 digits", False, "missing")
    ca = claim.get("calibration_site")
    if ca:
        exact = {"kagome": KAGOME_SITE_EXACT, "(3,12^2)": T3122_SITE_EXACT}[ca["lattice"]]
        d = abs(ca["value"] - exact)
        chk("(c) %s site reproduced to 6 digits" % ca["lattice"], d <= CAL6_TOL and ca["sigma"] <= CAL6_TOL,
            "|%.10f - %.10f| = %.3g, sigma %.3g" % (ca["value"], exact, d, ca["sigma"]))
    else:
        chk("(c) calibration site", False, "missing")
    chk("(d) literature search recorded", bool(claim.get("literature_search")), "manual: NOVELTY skeptic decides")
    return ok, res


def judge_p2(claim, rows):
    row = next(r for r in rows if r["num"] == int(claim["table_num"]))
    b, t = claim["bond"], row["bond"]
    out = []
    ok_cn = t["citation_needed"]
    out.append(("PASS" if ok_cn else "FAIL") + "  table bond value is 'citation needed': %s" % t["text"])
    ok_s = b["sigma"] <= P2_SIGMA_MAX
    out.append(("PASS" if ok_s else "FAIL") + "  stated sigma <= 5e-8: %.3g" % b["sigma"])
    d, cs = abs(b["value"] - t["value"]), math.hypot(b["sigma"], t["sigma"])
    verdict = "confirms" if d <= 3 * cs else ("discrepancy beyond the table error bar" if d > 3 * cs else "?")
    out.append("INFO  |%.10f - %s| = %.3g; combined sigma %.3g -> %s" % (b["value"], t["text"], d, cs, verdict))
    return ok_cn and ok_s, out


def selftest(html_path):
    rows = parse_table(html_path)
    assert len(rows) == 20, len(rows)
    nums = sorted(r["num"] for r in rows)
    print("table rows:", nums)
    # graph-level tests on lattices with known structure
    sq = rowtype_stats("S"); tri = rowtype_stats("T")
    assert sq["zbar"] == "4" and sq["config"] == {"4^4": "1"}, sq
    assert tri["zbar"] == "6" and tri["config"] == {"3^6": "1"}, tri
    words = {20: "TTTS", 21: "TTS", 22: "TSS", 23: "TSSS"}
    for num, w in words.items():
        row = next(r for r in rows if r["num"] == num)
        st = rowtype_stats(w)
        want = {k: str(Fraction(v)) for k, v in row["config"].items()}
        print("#%d %-6s graph %s zbar %s | table %s zbar %s" % (num, w, st["config"], st["zbar"], want, row["zbar_text"]))
        assert st["config"] == want and Fraction(st["zbar"]) == zbar_from_text(row["zbar_text"]), num
    # a wrong word for #23 must fail (known negative for lattice identity)
    bad = rowtype_stats("TSS")
    row23 = next(r for r in rows if r["num"] == 23)
    assert bad["config"] != {k: str(Fraction(v)) for k, v in row23["config"].items()}
    # synthetic claims: one that meets every numeric rule, and negatives
    tv = row23["site"]["value"]; bv = row23["bond"]["value"]
    good = {"table_num": 23, "gaps": "TSSS", "site": {"value": tv + 1e-5, "sigma": 1.5e-6},
            "methods": [{"name": "MC", "value": tv + 1e-5 + 1e-6, "sigma": 1.8e-6}, {"name": "TM", "value": tv + 1e-5, "sigma": 5e-7}],
            "bond_same_code": {"value": bv + 3e-7, "sigma": 2e-7},
            "calibration_site": {"lattice": "kagome", "value": KAGOME_SITE_EXACT + 2e-7, "sigma": 3e-7},
            "literature_search": "synthetic"}
    ok, res = judge(good, rows); print("\n".join(res)); assert ok, "known-positive synthetic claim failed"
    import copy
    negs = []
    n1 = copy.deepcopy(good); n1["gaps"] = "TSS"; negs.append(("wrong tiling", n1))
    n2 = copy.deepcopy(good); n2["site"]["sigma"] = 3e-6; negs.append(("sigma too big", n2))
    n3 = copy.deepcopy(good); n3["methods"][0]["value"] += 2e-5; negs.append(("methods disagree", n3))
    n4 = copy.deepcopy(good); n4["bond_same_code"]["value"] += 3e-6; negs.append(("bond off", n4))
    n5 = copy.deepcopy(good); n5["calibration_site"]["value"] += 5e-6; negs.append(("calibration off", n5))
    n6 = copy.deepcopy(good); n6["site"]["value"] = tv + 1e-3; n6["methods"][0]["value"] = tv + 1e-3; n6["methods"][1]["value"] = tv + 1e-3
    negs.append(("far from table", n6))
    for name, c in negs:
        ok, res = judge(c, rows)
        assert not ok, "known negative passed: " + name
        print("negative '%s' correctly FAILS: %s" % (name, [r for r in res if r.startswith("FAIL")][0]))
    ok, out = judge_p2({"table_num": 23, "bond": {"value": bv + 1e-8, "sigma": 3e-8}}, rows); print("\n".join(out)); assert ok
    ok, out = judge_p2({"table_num": 23, "bond": {"value": bv, "sigma": 2e-7}}, rows); assert not ok
    print("kagome site exact %.13f ; (3,12^2) site exact %.13f" % (KAGOME_SITE_EXACT, T3122_SITE_EXACT))
    print("SELFTEST PASS")


def main(a):
    if a[:1] == ["table"]:
        print(json.dumps(parse_table(a[1]), indent=1, ensure_ascii=False)); return 0
    if a[:1] == ["lattice"]:
        W = int(a[2]) if len(a) > 2 else 12; H = int(a[3]) if len(a) > 3 else 4
        print(json.dumps(rowtype_stats(a[1], W, H), indent=1)); return 0
    if a[:1] == ["claim"]:
        c = json.load(open(a[1])); rows = parse_table(a[2])
        if c.get("kind") == "p2":
            ok, out = judge_p2(c, rows)
        else:
            ok, out = judge(c, rows)
        print("\n".join(out)); print("VERDICT:", "MEETS NUMERIC RULES" if ok else "FAILS"); return 0 if ok else 1
    if a[:1] == ["selftest"]:
        selftest(a[1]); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
