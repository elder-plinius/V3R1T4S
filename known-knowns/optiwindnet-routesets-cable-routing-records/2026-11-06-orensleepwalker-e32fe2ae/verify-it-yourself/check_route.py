"""Standalone (Python standard library only) verifier for one OptiWindNet RouteSets claim.

Instance: see NAME and CAP below (release r26.10-v4, radial).
It downloads the hash-pinned release file once (one honest request, no retries), reads the nodeset and the stored
route sets with sqlite3, and checks the claimed segments: length, radial capacitated structure, feeders, no proper
crossings, every segment inside the closed site border and outside every obstacle interior, and the strict comparison with every stored set.
The official optiwindnet validator is not run here (it needs third-party packages); see the panel reports.
"""
import argparse, ast, hashlib, json, lzma, math, os, sqlite3, struct, tempfile, urllib.request
from pathlib import Path

OBJECT_SHA256 = 'e32fe2ae1720bce727f998837f8b58ea3cfe67b4e84528816d77b26104194bd8'
PACKED_SHA256 = '0d806efa86eea5637aa0929287a1c9f3a569219622879eeae207c7af624b7ef7'  # object/routeset-packed.json (same route set, optiwindnet storage format)
RELEASE = {'url': 'https://zenodo.org/api/records/23537067/files/optiwindnet-routesets-r26.10-v4.sqlite.xz/content',
           'sha256': 'c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a',
           'filename': 'optiwindnet-routesets-r26.10-v4.sqlite.xz'}
NAME, CAP, EXPECTED = 'Yi-2019.1_OSS', 11, 129717.36569882008


def release_path(ref_dir):
    if ref_dir:
        p = Path(ref_dir) / RELEASE['filename']
    else:
        p = Path(tempfile.gettempdir()) / 'own-routesets-cache' / RELEASE['sha256']
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(RELEASE['url'], headers={'User-Agent': 'V3R1T4S-route-verifier'})
            with urllib.request.urlopen(req, timeout=120) as r:
                if r.status != 200: raise ValueError('release HTTP %d' % r.status)
                p.write_bytes(r.read(60_000_000))
    data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != RELEASE['sha256']: raise ValueError('release sha256 mismatch')
    return data


def read_npy(blob):
    if blob[:6] != b'\x93NUMPY': raise ValueError('not an .npy blob')
    major = blob[6]
    hlen, off = (struct.unpack('<H', blob[8:10])[0], 10) if major == 1 else (struct.unpack('<I', blob[8:12])[0], 12)
    hdr = ast.literal_eval(blob[off:off + hlen].decode('latin1'))
    if hdr['descr'] != '<f8' or hdr['fortran_order']: raise ValueError('unexpected npy layout %r' % hdr)
    n, k = hdr['shape']; vals = struct.unpack('<%dd' % (n * k), blob[off + hlen: off + hlen + 8 * n * k])
    return [tuple(vals[i * k:(i + 1) * k]) for i in range(n)]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper_cross(p1, p2, q1, q2):
    """True if segments cross at a single interior point (shared endpoints and collinear overlaps excluded)."""
    if {p1, p2} & {q1, q2}: return False
    d1, d2, d3, d4 = orient(q1, q2, p1), orient(q1, q2, p2), orient(p1, p2, q1), orient(p1, p2, q2)
    return (d1 > 0) != (d2 > 0) and d1 != 0 and d2 != 0 and (d3 > 0) != (d4 > 0) and d3 != 0 and d4 != 0


def on_segment(p, a, b, eps=1e-6):
    return abs(orient(a, b, p)) <= eps * math.dist(a, b) and min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps \
        and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps


def inside_closed(p, poly):
    n = len(poly)
    if any(on_segment(p, poly[i], poly[(i + 1) % n]) for i in range(n)): return True
    c = False
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % n]
        if (ay > p[1]) != (by > p[1]) and p[0] < ax + (p[1] - ay) * (bx - ax) / (by - ay): c = not c
    return c


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--object', default=str(Path(__file__).resolve().parents[1] / 'object/segments.json'))
    ap.add_argument('--reference-dir'); a = ap.parse_args()
    raw = Path(a.object).read_bytes()
    if hashlib.sha256(raw).hexdigest() != OBJECT_SHA256: raise ValueError('frozen object hash mismatch')
    packed = Path(a.object).with_name('routeset-packed.json')
    if hashlib.sha256(packed.read_bytes()).hexdigest() != PACKED_SHA256: raise ValueError('packed route set hash mismatch')
    obj = json.loads(raw); segs = [(s['u'], s['v'], tuple(s['a']), tuple(s['b'])) for s in obj['segments']]
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / 'release.sqlite'; db.write_bytes(lzma.decompress(release_path(a.reference_dir)))
        c = sqlite3.connect(str(db))
        digest, T, R, VertexC, groups, cverts = c.execute('select digest, T, R, VertexC, constraint_groups, constraint_vertices from nodeset where name=?', (NAME,)).fetchone()
        stored = [(L, json.loads(f), json.loads(m).get('topology')) for L, f, m in
                  c.execute('select length, feeders_per_root, misc from routeset where nodes_id=? and capacity=?', (digest, CAP))]
        c.close()
    VC = read_npy(VertexC); groups = json.loads(groups); cverts = json.loads(cverts)
    border = [VC[i] for i in cverts[:groups[0]]]
    bounds = [0]
    for g in groups: bounds.append(bounds[-1] + g)
    obstacles = [[VC[i] for i in cverts[bounds[k]:bounds[k + 1]]] for k in range(1, len(groups))]
    turbines, subs = VC[:T], VC[-R:]
    # endpoints must sit on instance points (turbines, substations or border vertices)
    allowed = set(VC)
    if any(p not in allowed for _, _, a1, b1 in segs for p in (a1, b1)): raise ValueError('segment endpoint not on an instance point')
    # graph on labels; turbines 0..T-1, substations -R..-1, others are detour clones
    adj = {}
    for u, v, _, _ in segs: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    if set(range(T)) - set(adj): raise ValueError('turbine missing from the route set')
    if any(len(adj[t]) > 2 for t in range(T)): raise ValueError('turbine degree > 2: not radial')
    if any(len(adj[n]) != 2 for n in adj if n >= T): raise ValueError('detour clone is not a pass-through node')
    feeders = [len(adj.get(r, [])) for r in range(-R, 0)]
    seen, strings = set(), []
    for r in range(-R, 0):
        for start in adj.get(r, []):
            comp, stack, edges = set(), [start], 0
            while stack:
                n = stack.pop()
                if n in comp: continue
                comp.add(n); stack.extend(m for m in adj[n] if m >= 0 and m not in comp)
            if comp & seen: raise ValueError('string reached twice (cycle)')
            seen |= comp; strings.append(sum(1 for n in comp if n < T))
    if len(seen & set(range(T))) != T: raise ValueError('not every turbine is connected to a substation')
    if max(strings) > CAP: raise ValueError('string over capacity')
    n_edges = len(segs); n_nodes = len(adj)
    if n_edges != n_nodes - R: raise ValueError('not a forest rooted at the substations')
    length = sum(math.dist(a1, b1) for _, _, a1, b1 in segs)
    crossings = sum(1 for i in range(n_edges) for j in range(i + 1, n_edges) if proper_cross(segs[i][2], segs[i][3], segs[j][2], segs[j][3]))
    outside = 0
    for _, _, a1, b1 in segs:
        mid = ((a1[0] + b1[0]) / 2, (a1[1] + b1[1]) / 2)
        if not (inside_closed(a1, border) and inside_closed(b1, border) and inside_closed(mid, border)): outside += 1
        elif any(proper_cross(a1, b1, border[k], border[(k + 1) % len(border)]) for k in range(len(border))): outside += 1
    in_obstacle = 0
    for _, _, a1, b1 in segs:
        pts = [(a1[0] + (b1[0] - a1[0]) * t / 20, a1[1] + (b1[1] - a1[1]) * t / 20) for t in range(21)]
        for ob in obstacles:
            strictly = lambda p: inside_closed(p, ob) and not any(on_segment(p, ob[i], ob[(i + 1) % len(ob)]) for i in range(len(ob)))
            if any(strictly(p) for p in pts) or any(proper_cross(a1, b1, ob[k], ob[(k + 1) % len(ob)]) for k in range(len(ob))):
                in_obstacle += 1; break
    radial = [s for s in stored if s[2] == 'radial']; best_rad = min(radial, key=lambda s: s[0])
    best_all = min(stored, key=lambda s: s[0])
    report = {'instance': NAME, 'capacity': CAP, 'length_m': length, 'feeders': feeders, 'strings': len(strings), 'max_string': max(strings),
              'proper_crossings': crossings, 'segments_outside_closed_border': outside, 'obstacles': len(obstacles), 'segments_entering_obstacles': in_obstacle,
              'stored_radial_best_m': best_rad[0], 'stored_radial_best_feeders': best_rad[1], 'stored_overall_best_m': best_all[0], 'stored_overall_best_topology': best_all[2],
              'margin_vs_radial_m': best_rad[0] - length, 'margin_vs_overall_m': best_all[0] - length}
    print(json.dumps(report, indent=2))
    ok = (abs(length - EXPECTED) < 1e-6 and crossings == 0 and outside == 0 and in_obstacle == 0 and length < best_rad[0] * (1 - 1e-6)
          and all(f <= g for f, g in zip(feeders, best_rad[1])))
    if not ok: raise ValueError('criterion check failed')
    print('PASS')


if __name__ == '__main__':
    try: main()
    except Exception as e:
        print('FAIL:', e); raise SystemExit(1)
