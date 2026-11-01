# Builds tampered MINI certificates (frontier 255 of core5d and r3_collar + r5_collar) under work/tamper/<name>/ for the negative controls.
# Records are re-hashed (record_sha256 recomputed with the documented canonical-JSON scheme) so that only the geometric/coverage checker can catch the tamper.
import gzip, json, os, shutil, hashlib, random, sys
SRC = 'work/certificate'; DST = 'work/tamper'
CORE = 'shards/core5d/00000255.jsonl.gz'; R3 = 'shards/r3_collar/00000255.jsonl.gz'; R5 = 'shards/r5_collar/00000255.jsonl.gz'
def sha(rec):
    c = {k: v for k, v in rec.items() if k != 'record_sha256'}
    return hashlib.sha256(json.dumps(c, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
def load(rel): return [json.loads(l) for l in gzip.open(os.path.join(SRC, rel), 'rt') if l.strip()]
def save(root, rel, recs, rehash=True):
    p = os.path.join(root, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with gzip.open(p, 'wt', encoding='utf-8') as f:
        for r in recs:
            if rehash: r['record_sha256'] = sha(r)
            f.write(json.dumps(r, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n')
def mk(name, mut_core=None, mut_r3=None, raw=None):
    root = os.path.join(DST, name)
    if os.path.exists(root): shutil.rmtree(root)
    for rel in (CORE, R3, R5):
        recs = load(rel)
        if rel == CORE and mut_core: recs = mut_core(recs)
        if rel == R3 and mut_r3: recs = mut_r3(recs)
        save(root, rel, recs)
    if raw: raw(root)
    return root
leaves = lambda recs: [r for r in recs if r['record_type'] == 'leaf']
def drop100(recs): L = leaves(recs); drop = {id(x) for x in L[1000:1100]}; return [r for r in recs if id(r) not in drop]
def dup1(recs): L = leaves(recs); i = recs.index(L[500]); return recs[:i + 1] + [json.loads(json.dumps(L[500]))] + recs[i + 1:]
def shrink(recs): L = leaves(recs); L[300]['box']['hi'][0] = float(L[300]['box']['hi'][0]) - 1e-4; return recs
def grow(recs): L = leaves(recs); L[300]['box']['hi'][0] = float(L[300]['box']['hi'][0]) + 1e-4; return recs
def shift(recs): L = leaves(recs); b = L[300]['box']; b['lo'][0] += 1e-3; b['hi'][0] += 1e-3; return recs
def samples32(recs):
    for r in leaves(recs): r['disk_samples'] = 32; r['r3_samples'] = 32; r['r5_samples'] = 32
    return recs
def psi_big(recs):
    for r in leaves(recs):
        if r['box']['hi'][2] == 0.6283185307179586: r['box']['hi'][2] = 0.7
    for r in recs:
        if r['record_type'] == 'frontier_summary' and r['root_box']['hi'][2] == 0.6283185307179586: r['root_box']['hi'][2] = 0.7
    return recs
def swap_lohi(recs): L = leaves(recs); b = L[200]['box']; b['lo'][3], b['hi'][3] = b['hi'][3], b['lo'][3]; return recs
def count_lie(recs):
    for r in recs:
        if r['record_type'] == 'frontier_summary': r['leaf_count'] += 1
    return recs
def bitflip(root):
    p = os.path.join(root, CORE); b = bytearray(open(p, 'rb').read()); b[len(b) // 2] ^= 0x10; open(p, 'wb').write(bytes(b))
def trunc(root):
    p = os.path.join(root, CORE); b = open(p, 'rb').read(); open(p, 'wb').write(b[: int(len(b) * 0.6)])
def fixcount(recs):
    n = len(leaves(recs))
    for r in recs:
        if r['record_type'] == 'frontier_summary': r['leaf_count'] = n
    return recs
mk('c3b_drop100_countfixed', mut_core=lambda r: fixcount(drop100(r))); mk('c4b_dup1_countfixed', mut_core=lambda r: fixcount(dup1(r)))
mk('c0_baseline'); mk('c1_bitflip', raw=bitflip); mk('c2_truncate', raw=trunc); mk('c3_drop100', mut_core=drop100); mk('c4_dup1', mut_core=dup1)
mk('c5_shrink', mut_core=shrink); mk('c6_grow', mut_core=grow); mk('c8_samples32', mut_core=samples32); mk('c9_psi07', mut_core=psi_big)
mk('c12_swap_lohi', mut_core=swap_lohi); mk('c14_shift', mut_core=shift); mk('c15_countlie', mut_core=count_lie)
print(sorted(os.listdir(DST)))
