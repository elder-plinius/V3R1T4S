# Re-computes shards_hash.json under the documented rule and the variants (documents defect D1: path prefix).
import os, sys, hashlib, json
root = sys.argv[1]; sh = os.path.join(root, 'shards')
files = sorted(os.path.relpath(os.path.join(dp, f), sh).replace('\\', '/') for dp, dn, fn in os.walk(sh) for f in fn)
claimed = json.load(open(os.path.join(root, 'shards_hash.json')))
def H(prefix):
    h = hashlib.sha256()
    for f in files:
        h.update((prefix + f).encode()); h.update(b'\0'); h.update(open(os.path.join(sh, f), 'rb').read()); h.update(b'\0')
    return h.hexdigest()
for prefix, label in (('', 'paths relative to shards/ (as written in the README/paper)'), ('shards/', "paths relative to certificate dir, i.e. with 'shards/' prefix")):
    d = H(prefix); print('%-70s %s  match=%s' % (label, d, d == claimed['sha256']))
print('claimed', claimed['sha256'], 'files', len(files), 'claimed_files', claimed['file_count'])
