# One pass over all shards: minimum RECORDED lower_bound per part (compare paper S14.1 table), number of leaves touching the float(pi/n) top endpoint (bridge users),
# and per-part leaf depth / sample statistics. Uses json.loads with parse_float=str to keep exact decimals.
import gzip, json, os, sys, collections
root = sys.argv[1]; res = {}
for part, topidx, toptxt in (('r3_collar', 1, '1.0471975511965976'), ('r5_collar', 1, '0.6283185307179586'), ('core5d', 2, '0.6283185307179586')):
    d = os.path.join(root, 'shards', part); mn = None; mnleaf = None; top = 0; n = 0; mnmid = None
    for f in sorted(os.listdir(d)):
        if not f[0].isdigit(): continue
        for line in gzip.open(os.path.join(d, f), 'rt'):
            if '"record_type":"leaf"' not in line: continue
            r = json.loads(line, parse_float=str); n += 1
            v = float(r['lower_bound'].lstrip('[').split(' ')[0])
            if mn is None or v < mn: mn = v; mnleaf = r['leaf_id']; mnstr = r['lower_bound']
            if r['box']['hi'][topidx] == toptxt: top += 1
    res[part] = {'leaves': n, 'min_recorded_lower': mn, 'min_leaf': mnleaf, 'min_str': mnstr, 'leaves_touching_float_pi_top': top}
    print(part, res[part], flush=True)
json.dump(res, open('out/recorded_census.json', 'w'), indent=1)
