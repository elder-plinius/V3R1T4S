# L9 part C: decode cert_B_08344 (gz) and report max split depth (number of 1-bits on a root-to-node path) per block,
# global max depth (+22 root splits), node/leaf counts. numba, single thread.
import numpy as np, gzip, struct, time, numba as nb, sys, hashlib
path = r"data/cert_B_08344.bin.gz"
t0 = time.time()
raw = gzip.open(path, 'rb').read()
print("uncompressed bytes", len(raw), "sha256", hashlib.sha256(raw).hexdigest())
assert raw[:8] == b"LEBCERTB"
target, thresh, tmax, m, K, depth, nseed = struct.unpack("<dddiiii", raw[8:48])
(inflate,) = struct.unpack("<d", raw[48:56]); (nblk,) = struct.unpack("<Q", raw[56:64])
print("header: target", target, "thresh", thresh, "tmax", tmax, "m", m, "K", K, "depth", depth, "nseed", nseed, "inflate", inflate, "nblk", nblk)
sizes = np.frombuffer(raw, dtype='<u4', count=nblk, offset=64).astype(np.int64)
base = 64 + 4*nblk
offs = base + np.concatenate([[0], np.cumsum(sizes)[:-1]])
buf = np.frombuffer(raw, dtype=np.uint8)
@nb.njit(cache=True)
def scan(buf, offs, sizes):
    nblk = len(offs); maxd = 0; nodes = 0; leaves = 0; bad = 0
    stack = np.empty(256, np.int64); hist = np.zeros(256, np.int64)
    for b in range(nblk):
        o = offs[b]; nbits = sizes[b]*8; pos = 0; sp = 0; stack[0] = 0; sp = 1
        while sp > 0 and pos < nbits:
            d = stack[sp-1]; sp -= 1
            bit = (buf[o + (pos >> 3)] >> (7 - (pos & 7))) & 1
            pos += 1; nodes += 1
            if bit == 0:
                leaves += 1
            else:
                if d + 1 > maxd: maxd = d + 1
                hist[d] += 1
                stack[sp] = d+1; stack[sp+1] = d+1; sp += 2
        if sp != 0 or (nbits - pos) >= 8: bad += 1
    return maxd, nodes, leaves, bad, hist
maxd, nodes, leaves, bad, hist = scan(buf, offs, sizes)
print(f"nodes {nodes} leaves {leaves} blocks_inconsistent {bad}  forest identity 2L-s = {2*leaves-nseed} (== nodes: {2*leaves-nseed==nodes})")
print("max depth below seed (deepest SPLIT is at depth maxd-1 below the seed):", maxd, " -> total split depth from root incl. 22 root splits:", maxd+22-0, "(deepest split node index below seed =", maxd-1, ")")
print("splits per seed-relative depth (nonzero tail):", [(i, int(hist[i])) for i in range(len(hist)) if hist[i] and i >= maxd-6])
print("elapsed", time.time()-t0)
