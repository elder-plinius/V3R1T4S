"""Build claim/ from the finished run. usage: build_claim.py OUT_DIR CLAIM_DIR"""
import sys, os, csv, json, hashlib, shutil, subprocess, numpy as np
out, claim = sys.argv[1], sys.argv[2]
obj = os.path.join(claim, 'object'); os.makedirs(obj, exist_ok=True)
PS = 'primesieve'
st = json.load(open(os.path.join(out, 'state.json')))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    return h.hexdigest()
# windows files
rows = list(csv.DictReader(open(os.path.join(out, 'windows.csv'))))
cols = ['w', 'lo', 'nprimes', 'cum_primes', 'chunks_done', 'win_max_depth', 'win_max_chunk']
per = 9000
for i in range(0, len(rows), per):
    with open(os.path.join(obj, f'windows_{i//per:02d}.csv'), 'w', newline='') as f:
        wr = csv.writer(f); wr.writerow(cols)
        for r in rows[i:i+per]: wr.writerow([r[c] for c in cols])
d = np.fromfile(os.path.join(out, 'depth.u16'), dtype='<u2')
cl = np.fromfile(os.path.join(out, 'clean1280.u8'), dtype='u1')
assert len(d) == st['chunks'] == len(cl), (len(d), st['chunks'], len(cl))
hist = np.bincount(d.astype(np.int64))
with open(os.path.join(obj, 'depth_histogram.csv'), 'w') as f:
    f.write('depth,count\n')
    for k in np.nonzero(hist)[0]: f.write(f'{k},{hist[k]}\n')
fp = list(csv.DictReader(open(os.path.join(out, 'chunk_first_primes.csv'))))
per = 20000
for i in range(0, len(fp), per):
    with open(os.path.join(obj, f'block_firstprimes_{i//per:02d}.csv'), 'w', newline='') as f:
        wr = csv.writer(f); wr.writerow(['block', 'first_prime', 'depth'])
        for r in fp[i:i+per]: wr.writerow([r['chunk'], r['first_prime'], int(d[int(r['chunk'])])])
fpd = {int(r['chunk']): int(r['first_prime']) for r in fp}
def first_prime_of(c):
    k0 = (c // 4096) * 4096; n = (c - k0) * 8192
    if n == 0: return fpd[k0]
    r = subprocess.run([PS, str(n), str(fpd[k0]), '-n', '-t1'], capture_output=True, text=True).stdout
    return int([l for l in r.splitlines() if l.startswith('Nth prime')][0].split(':')[1])
cmax = int(np.argmax(d)); dmax = int(d[cmax])
top = np.argsort(-d.astype(np.int64), kind='stable')[:5]
rng = np.random.default_rng(20261101)
samp = sorted(set([int(x) for x in top[:3]] + [int(x) for x in rng.integers(0, len(d), 9)] + [0, len(d) - 1, 4096 * 5000 + 17]))
with open(os.path.join(obj, 'sample_blocks.csv'), 'w', newline='') as f:
    wr = csv.writer(f); wr.writerow(['block', 'first_prime', 'depth'])
    for c in samp: wr.writerow([c, first_prime_of(c), int(d[c])])
A = 1_500_000_000_000_000
res = dict(range_first_prime=fpd[0], total_primes=st['cum'], blocks=int(len(d)), M=8192, O=1536, KSTAR=1280,
           max_depth=dmax, max_depth_block=cmax, max_depth_block_first_prime=first_prime_of(cmax),
           top5_depth=[int(d[i]) for i in top], unclean_row1280_blocks=int((cl == 0).sum()), flagged_blocks=int((d == 0xFFFF).sum()),
           min_depth=int(d.min()), median_depth=int(np.median(d)), windows=len(rows),
           last_owned_first_prime_of_stream=int(first_prime_of(len(d))),
           depth_u16_bytes=os.path.getsize(os.path.join(out, 'depth.u16')), depth_u16_sha256=sha(os.path.join(out, 'depth.u16')),
           clean1280_u8_bytes=os.path.getsize(os.path.join(out, 'clean1280.u8')), clean1280_u8_sha256=sha(os.path.join(out, 'clean1280.u8')))
json.dump(res, open(os.path.join(obj, 'RESULT.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
