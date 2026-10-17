"""Density of a minimizer order for (w=12,k=3), using the published notebook's OWN composition.

Definition, quoted from greedymini_density.ipynb:
  cell 2 (random_density_function_dna_includes_tiebreaking):
      shift_8k = 8 * k
      ranks = [(function(km, w, k, seed) << shift_8k) + get_kmer_id_dna(k, km, seed) for km in kmers]
  cell 4 (GreedyMiniScheme.get_minimizer -> _fn):
      return (rank_train << (2 * k)) + kmer
Composed:  rank = (((order[bin_kmer] << (2*k)) + kmer) << (8*k)) + get_kmer_id_dna(k, km, seed)
bin_kmer uses the HIGH bit of each 2-bit base (bit = (nuc >> 1) & 1), i.e. bits 5,3,1 for k=3.
"""
import struct, hashlib, numpy as np
W, K = 12, 3
def load_gm(path):
    b = open(path, "rb").read(); n = struct.unpack("P", b[:struct.calcsize("P")])[0]
    return list(struct.unpack(f"{n}Q", b[struct.calcsize("P"):]))
def get_kmer_id_dna(k, kmer, seed):
    h = hashlib.sha256((kmer + seed).to_bytes(2 * k, byteorder="big")).digest()
    return (4 ** k) * (int.from_bytes(h, "big") % (4 ** k)) + kmer
def density(order, n_samples, seed):
    total = n_samples + W + K - 1
    nuc = np.random.default_rng(seed).integers(0, 4, size=total, dtype=np.uint32)
    n_kmers = total - K + 1
    km = np.zeros(n_kmers, dtype=np.int64); cur = 0
    for p in range(K): cur = (cur << 2) | int(nuc[p])
    km[0] = cur
    for i in range(1, n_kmers):
        cur = ((cur << 2) | int(nuc[i + K - 1])) & ((1 << (2 * K)) - 1); km[i] = cur
    # HIGH-bit projection: bin_kmer = bits 5,3,1
    bin_kmer = (((km >> 5) & 1) << 2) | (((km >> 3) & 1) << 1) | ((km >> 1) & 1)
    tb = np.array([get_kmer_id_dna(K, int(x), seed) for x in km], dtype=np.int64)
    inner = (np.array(order, dtype=np.int64)[bin_kmer] << (2 * K)) + km
    rank = (inner << (8 * K)) + tb
    win = np.lib.stride_tricks.sliding_window_view(rank, W)
    mn = win.argmin(axis=1) + np.arange(len(win))
    return (1 + int(np.count_nonzero(np.diff(mn)))) / n_kmers
if __name__ == "__main__":
    gm = load_gm("w12_k3.gm"); claimed = [int(x) for x in open("order.txt").read().split()]
    N = 2_000_000
    g = [density(gm, N, s) for s in (0, 1, 2)]
    c = [density(claimed, N, s) for s in (0, 1, 2)]
    print(f"n={N}, seeds 0,1,2 -- notebook's own composition")
    print(f"  GreedyMini  mean density = {np.mean(g):.12f}")
    print(f"  claimed     mean density = {np.mean(c):.12f}")
    print(f"  claimed vs GreedyMini    = {(np.mean(c)-np.mean(g))/np.mean(g)*100:+.4f}%")
