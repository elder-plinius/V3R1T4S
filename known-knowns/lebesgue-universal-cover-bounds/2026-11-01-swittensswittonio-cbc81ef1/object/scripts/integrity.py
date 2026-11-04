# Stage 0: integrity + census of the shard set (independent of author's verifier code).
# - shard-set SHA256 (sorted relpath + NUL + bytes + NUL) vs shards_hash.json
# - per-record record_sha256 recomputation (canonical json: sort_keys, separators (',',':'), ensure_ascii)
# - census: record types, methods, sample configs, precision bits, depth, digits of box endpoints
import gzip, hashlib, json, os, sys, time, collections
root = sys.argv[1]            # .../certificate
out = sys.argv[2]
sh = os.path.join(root, 'shards')
t0 = time.time()
files = []
for dp, dn, fn in os.walk(sh):
    for f in fn:
        files.append(os.path.relpath(os.path.join(dp, f), sh).replace('\\', '/'))
files.sort()
h = hashlib.sha256(); nb = 0
for f in files:
    h.update(f.encode()); h.update(b'\0')
    b = open(os.path.join(sh, f), 'rb').read(); nb += len(b)
    h.update(b); h.update(b'\0')
claimed = json.load(open(os.path.join(root, 'shards_hash.json')))
res = {'files': len(files), 'bytes': nb, 'sha256': h.hexdigest(), 'claimed_sha256': claimed['sha256'],
       'claimed_files': claimed['file_count'], 'claimed_bytes': claimed['byte_count'],
       'shard_hash_ok': h.hexdigest() == claimed['sha256']}
print('shard hash', res, 't=%.0f' % (time.time() - t0), flush=True)
cnt = collections.Counter(); meth = collections.Counter(); cfg = collections.Counter(); badsha = 0
depth = collections.Counter(); maxdig = 0; per_part_leaf = collections.Counter()
keys = collections.Counter(); runkeys = collections.Counter()
def sha(rec):
    c = {k: v for k, v in rec.items() if k != 'record_sha256'}
    return hashlib.sha256(json.dumps(c, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
nrec = 0
for f in files:
    part = f.split('/')[0]
    for line in gzip.open(os.path.join(sh, f), 'rt', encoding='utf-8'):
        line = line.strip()
        if not line: continue
        r = json.loads(line); nrec += 1
        rt = r.get('record_type'); cnt[(part, rt)] += 1
        e = r.get('record_sha256')
        if e is None: badsha += 1000000
        elif e != sha(r): badsha += 1
        if rt == 'leaf':
            meth[(part, r['method'])] += 1
            cfg[(part, r.get('disk_samples'), r.get('r3_samples', r.get('reuleaux_samples')), r.get('r5_samples'), r.get('precision_bits'))] += 1
            depth[(part, r['depth'])] += 1
            runkeys[r.get('run_key')] += 1
            for v in r['box']['lo'] + r['box']['hi']:
                maxdig = max(maxdig, len(repr(v)))
    if nrec % 500000 < 10: print(nrec, f, 't=%.0f' % (time.time() - t0), flush=True)
res.update({'records': nrec, 'bad_record_sha': badsha, 'type_counts': {'%s|%s' % k: v for k, v in cnt.items()},
            'methods': {'%s|%s' % k: v for k, v in meth.items()}, 'configs': {str(k): v for k, v in cfg.items()},
            'depth': {'%s|%s' % k: v for k, v in sorted(depth.items())}, 'max_box_repr_len': maxdig, 'run_keys': dict(runkeys),
            'elapsed_s': time.time() - t0})
json.dump(res, open(out, 'w'), indent=1)
print('DONE', json.dumps({k: res[k] for k in ['records', 'bad_record_sha', 'shard_hash_ok', 'elapsed_s']}))
