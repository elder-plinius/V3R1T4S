#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <algorithm>
#include <random>

#include "htypes.h"
#include "hutils.h"
#include "prefix_processor.h"

using namespace std;

u32 Verbosity = 0;
static std::mt19937_64 mtRand(42);

#define RANDIDX(v) (mtRand() % (v).size())
#define RANDELEM(v) ((v)[RANDIDX(v)])

static void computeDepthAndCrit(u8 N, const Network_t &nw, u32 &out_dp, u32 &out_crit_cnt,
                                u32 &out_zs_cnt, uint8_t crit_wires[64]) {
    u32 w_asap[64];
    memset(w_asap, 0, sizeof(w_asap));
    u32 asap[1024];
    u32 max_d = 0;
    size_t m = nw.size();
    for (size_t k = 0; k < m; k++) {
        u8 u = nw[k].lo, v = nw[k].hi;
        u32 nd = ((w_asap[u] > w_asap[v]) ? w_asap[u] : w_asap[v]) + 1;
        w_asap[u] = w_asap[v] = nd;
        asap[k] = nd;
        if (nd > max_d) max_d = nd;
    }
    out_dp = max_d;
    u32 w_alap[64];
    for (u8 w = 0; w < N; w++) w_alap[w] = max_d;
    u32 c_cnt = 0, zs_cnt = 0;
    u32 min_top_l = (max_d > 4) ? (max_d - 4) : 1;
    memset(crit_wires, 0, 64);
    for (int k = (int)m - 1; k >= 0; k--) {
        u8 u = nw[k].lo, v = nw[k].hi;
        u32 al = (w_alap[u] < w_alap[v]) ? w_alap[u] : w_alap[v];
        w_alap[u] = w_alap[v] = al - 1;
        if (asap[k] == max_d) c_cnt++;
        if (asap[k] == al && asap[k] >= min_top_l) {
            zs_cnt++;
            crit_wires[u] = 1;
            crit_wires[v] = 1;
        }
    }
    out_crit_cnt = c_cnt;
    out_zs_cnt = zs_cnt;
}

static void swap_sortedpatterns_fast(SinglePatternList_t &pl, const Pair_t &p, bool &was_noop) {
    const SortWord_t m1 = 1ULL << p.lo;
    const SortWord_t m2 = 1ULL << p.hi;
    const SortWord_t m = m1 | m2;

    static SinglePatternList_t keep, moved;
    keep.clear();
    moved.clear();
    keep.reserve(pl.size());

    for (size_t i = 0; i < pl.size(); i++) {
        SortWord_t el = pl[i];
        if ((el & m) == m1) {
            moved.push_back(el ^ m);
        } else {
            keep.push_back(el);
        }
    }
    if (moved.empty()) {
        was_noop = true;
        return;
    }
    was_noop = false;

    SinglePatternList_t out;
    out.reserve(keep.size() + moved.size());
    size_t i = 0, j = 0;
    while (i < keep.size() && j < moved.size()) {
        if (keep[i] < moved[j]) {
            out.push_back(keep[i++]);
        } else if (moved[j] < keep[i]) {
            out.push_back(moved[j++]);
        } else {
            out.push_back(keep[i]);
            i++;
            j++;
        }
    }
    while (i < keep.size()) out.push_back(keep[i++]);
    while (j < moved.size()) out.push_back(moved[j++]);
    pl.swap(out);
}

static void splitNetworkAuto(u8 ninputs, const Network_t &full_nw, SortWord_t target_singles,
                             Network_t &out_prefix, Network_t &out_pairs,
                             SinglePatternList_t &patterns, int &noop_dropped) {
    SinglePatternList_t patternlists[NMAX];
    SortWord_t masks[NMAX];
    u32 clusterAlloc[NMAX];
    u32 n_clusters = ninputs;

    for (u32 k = 0; k < ninputs; k++) {
        masks[k] = 1ULL << k;
        clusterAlloc[k] = k;
        patternlists[k].push_back(0ULL);
        patternlists[k].push_back(1ULL << k);
    }

    auto outputSize = [&]() -> SortWord_t {
        double acc = 1.0;
        for (u32 k = 0; k < ninputs; k++) {
            if (masks[k] != 0) acc *= (double)patternlists[k].size();
        }
        return (acc > 1e18) ? ~0ULL : (SortWord_t)acc;
    };

    auto preSort = [&](const Pair_t &p, bool &was_noop) {
        u32 ci = clusterAlloc[p.lo];
        u32 cj = clusterAlloc[p.hi];
        if (ci != cj) {
            if (cj < ci) { u32 t = ci; ci = cj; cj = t; }
            SinglePatternList_t &p1 = patternlists[ci];
            SinglePatternList_t &p2 = patternlists[cj];
            for (u32 k = 0; k < ninputs; k++) {
                if (clusterAlloc[k] == cj) clusterAlloc[k] = ci;
            }
            masks[ci] |= masks[cj];
            SinglePatternList_t cp;
            cp.reserve(p1.size() * p2.size());
            for (size_t i = 0; i < p1.size(); i++)
                for (size_t j = 0; j < p2.size(); j++)
                    cp.push_back(p1[i] | p2[j]);
            std::sort(cp.begin(), cp.end());
            p1.swap(cp);
            masks[cj] = 0;
            p2.clear();
            n_clusters--;
        }
        swap_sortedpatterns_fast(patternlists[ci], p, was_noop);
    };

    out_prefix.clear();
    out_pairs.clear();
    noop_dropped = 0;
    Network_t todo = full_nw;

    while (todo.size() > 0) {
        if (outputSize() <= target_singles) {
            break;
        }
        bool was_noop = false;
        preSort(todo[0], was_noop);
        if (!was_noop) out_prefix.push_back(todo[0]);
        else noop_dropped++;

        Network_t postponed;
        SortWord_t visitmask = 0;
        for (size_t k = 1; k < todo.size(); k++) {
            Pair_t el = todo[k];
            SortWord_t elmask = (1ULL << el.lo) | (1ULL << el.hi);
            if (((visitmask & elmask) == 0) && (clusterAlloc[el.lo] == clusterAlloc[el.hi])) {
                if (outputSize() <= target_singles) {
                    postponed.push_back(el);
                } else {
                    bool wn = false;
                    preSort(el, wn);
                    if (!wn) out_prefix.push_back(el);
                    else noop_dropped++;
                }
            } else {
                postponed.push_back(el);
            }
            visitmask |= elmask;
        }
        todo.swap(postponed);
    }

    out_pairs = todo;

    const SinglePatternList_t *pLists[NMAX];
    int n_to_combine = 0;
    for (u32 k = 0; k < ninputs; k++) {
        if (masks[k] != 0) pLists[n_to_combine++] = &patternlists[k];
    }
    patterns.clear();
    if (n_to_combine == 1) {
        patterns = *pLists[0];
    } else {
        int level = 0;
        size_t indices[NMAX] = {0};
        SortWord_t outmasks[NMAX] = {0};
        while (level >= 0) {
            if (indices[level] < pLists[level]->size()) {
                outmasks[level] = (level == 0) ? (*pLists[level])[indices[level]]
                                               : (outmasks[level - 1] | (*pLists[level])[indices[level]]);
                if (level < (n_to_combine - 1)) {
                    indices[level + 1] = 0;
                    indices[level]++;
                    level++;
                } else {
                    patterns.push_back(outmasks[level]);
                    indices[level]++;
                }
            } else {
                level--;
            }
        }
    }
}

static void applyBitParallelSortRange(BPWord_t data[], const Network_t &nw, size_t start, size_t end) {
    for (size_t n = start; n < end; n++) {
        u32 i = nw[n].lo;
        u32 j = nw[n].hi;
        BPWord_t iold = data[i];
        data[i] &= data[j];
        data[j] |= iold;
    }
}

static void bumpVectorPosition(u8 N, BitParallelList_t &bpl, size_t failvector) {
    size_t groupno = failvector / PARWORDSIZE;
    size_t idx = N * groupno;
    if (groupno > 1) {
        size_t delta = N * ((groupno + 7) / 8);
        for (size_t k = 0; k < N; k++) {
            BPWord_t z = bpl[idx + k - delta];
            bpl[idx + k - delta] = bpl[idx + k];
            bpl[idx + k] = z;
        }
    } else if (groupno == 1) {
        BPWord_t m0 = 1ULL << (PARWORDSIZE - 1);
        BPWord_t m1 = 1ULL << (failvector % PARWORDSIZE);
        int shift = (PARWORDSIZE - 1) - (failvector % PARWORDSIZE);
        for (size_t k = 0; k < N; k++) {
            BPWord_t old0 = bpl[k];
            BPWord_t old1 = bpl[k + N];
            bpl[k] = (old0 & ~m0) | ((old1 & m1) << shift);
            bpl[k + N] = (old1 & ~m1) | ((old0 & m0) >> shift);
        }
    } else if (failvector > 0) {
        BPWord_t m0 = 1ULL << (failvector - 1);
        BPWord_t m1 = 1ULL << failvector;
        for (size_t k = 0; k < N; k++) {
            BPWord_t old = bpl[k];
            bpl[k] = (old & ~m0 & ~m1) | ((old & m1) >> 1) | ((old & m0) << 1);
        }
    }
}

static bool testPairs(u8 N, const Network_t &pairs, BitParallelList_t &bpl) {
    size_t idx = 0;
    size_t failvector = 0;
    BPWord_t data[NMAX];
    while (idx < bpl.size()) {
        BPWord_t accum = 0;
        for (size_t k = 0; k < N; k++) data[k] = bpl[idx + k];
        applyBitParallelSortRange(data, pairs, 0, pairs.size());
        for (size_t k = 0; k < (size_t)(N - 1u); k++) {
            accum |= data[k] & ~data[k + 1];
        }
        if (accum != 0ULL) {
            while ((accum & 1ULL) == 0) {
                accum >>= 1;
                failvector++;
            }
            bumpVectorPosition(N, bpl, failvector);
            return false;
        }
        idx += N;
        failvector += PARWORDSIZE;
    }
    return true;
}

static u32 pickPairIdx(const Network_t &newpairs, const uint8_t crit_wires[64], bool bias_crit) {
    if (!bias_crit || newpairs.empty()) return RANDIDX(newpairs);
    for (int tries = 0; tries < 8; tries++) {
        u32 idx = RANDIDX(newpairs);
        if (crit_wires[newpairs[idx].lo] || crit_wires[newpairs[idx].hi]) return idx;
    }
    return RANDIDX(newpairs);
}

static u32 attemptMutation(u8 N, Network_t &newpairs, const Network_t &alphabet,
                           const std::vector<u8> &mutationSelector,
                           const uint8_t crit_wires[64], bool bias_crit) {
    u32 applied = 0;
    u32 mtype = 1 + RANDELEM(mutationSelector);
    switch (mtype) {
        case 1: /* Remove random pair */
            if (newpairs.size() > 0) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                newpairs.erase(newpairs.begin() + a);
                applied = mtype;
            }
            break;
        case 2: /* Swap two pairs */
            if (newpairs.size() > 1) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                u32 b = RANDIDX(newpairs);
                if (a > b) std::swap(a, b);
                if (newpairs[a] != newpairs[b]) {
                    bool Dependent = false;
                    u8 l1 = newpairs[a].lo, h1 = newpairs[a].hi;
                    u8 l2 = newpairs[b].lo, h2 = newpairs[b].hi;
                    if (l1 == l2 || l1 == h2 || h1 == l2 || h1 == h2) {
                        Dependent = true;
                    } else {
                        for (u32 k = a + 1; k < b; k++) {
                            u8 l3 = newpairs[k].lo, h3 = newpairs[k].hi;
                            if (l1 == l3 || l1 == h3 || h1 == l3 || h1 == h3 ||
                                l2 == l3 || l2 == h3 || h2 == l3 || h2 == h3) {
                                Dependent = true;
                                break;
                            }
                        }
                    }
                    if (Dependent) {
                        Pair_t t = newpairs[a];
                        newpairs[a] = newpairs[b];
                        newpairs[b] = t;
                        applied = mtype;
                    }
                }
            }
            break;
        case 3: /* Replace pair */
            if (newpairs.size() > 0) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                Pair_t p = RANDELEM(alphabet);
                if (newpairs[a] != p) {
                    newpairs[a] = p;
                    applied = mtype;
                }
            }
            break;
        case 4: /* Cross two pairs */
            if (newpairs.size() > 1) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                u32 b = RANDIDX(newpairs);
                u8 i1 = newpairs[a].lo, j1 = newpairs[a].hi;
                u8 i2 = newpairs[b].lo, j2 = newpairs[b].hi;
                if (i1 != i2 && i1 != j2 && j1 != i2 && j1 != j2) {
                    u8 r = mtRand() % 2;
                    u8 t1 = r ? i2 : j2;
                    u8 t2 = r ? j2 : i2;
                    Pair_t p1 = {min(i1, t1), max(i1, t1)};
                    Pair_t p2 = {min(j1, t2), max(j1, t2)};
                    newpairs[a] = p1;
                    newpairs[b] = p2;
                    applied = mtype;
                }
            }
            break;
        case 5: /* Swap intersecting pairs with no intermediate touches */
            if (newpairs.size() > 1) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                u8 i1 = newpairs[a].lo, j1 = newpairs[a].hi;
                u8 i2, j2;
                u32 b = a;
                u32 k = a + 1;
                for (; k < newpairs.size(); k++) {
                    i2 = newpairs[k].lo; j2 = newpairs[k].hi;
                    if (i1 == i2 || i1 == j2 || j1 == i2 || j1 == j2) {
                        if (newpairs[k] != newpairs[a]) b = k;
                        break;
                    }
                }
                if (b > a) {
                    bool touch = false;
                    for (k = a + 1; k < b; k++) {
                        u8 il = newpairs[k].lo, jl = newpairs[k].hi;
                        if (il == i2 || il == j2 || jl == i2 || jl == j2) {
                            touch = true;
                            break;
                        }
                    }
                    if (!touch) {
                        Pair_t t = newpairs[a];
                        newpairs[a] = newpairs[b];
                        newpairs[b] = t;
                        applied = mtype;
                    }
                }
            }
            break;
        case 6: /* Change one endpoint of a pair */
            if (newpairs.size() > 0) {
                u32 a = pickPairIdx(newpairs, crit_wires, bias_crit);
                Pair_t p = newpairs[a];
                Pair_t q;
                do {
                    q = RANDELEM(alphabet);
                } while (q.lo != p.lo && q.hi != p.lo && q.lo != p.hi && q.hi != p.hi);
                if (q != p) {
                    newpairs[a] = q;
                    applied = mtype;
                }
            }
            break;
    }
    return applied;
}

static void save_network(const char *path, u8 N, const Network_t &nw) {
    FILE *fp = fopen(path, "w");
    if (!fp) return;
    fprintf(fp, "%u %lu\n", (unsigned)N, nw.size());
    for (size_t k = 0; k < nw.size(); k++) {
        fprintf(fp, "%u %u\n", (unsigned)nw[k].lo, (unsigned)nw[k].hi);
    }
    fclose(fp);
}

static int run_loo_on_pairs(u8 N, const Network_t &prefix, Network_t &pairs,
                            BitParallelList_t &bpl, u32 max_allowed_depth) {
    int dropped = 0;
    bool changed = true;
    Network_t tot;
    while (changed) {
        changed = false;
        for (int i = (int)pairs.size() - 1; i >= 0; i--) {
            Network_t cand = pairs;
            cand.erase(cand.begin() + i);
            if (testPairs(N, cand, bpl)) {
                concatNetwork(prefix, cand, tot);
                if (computeDepth(tot) <= max_allowed_depth) {
                    pairs.swap(cand);
                    dropped++;
                    changed = true;
                    break;
                }
            }
        }
    }
    return dropped;
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <input_txt> <target_singles> <output_txt> [max_iters=0] [max_depth=0] [max_size=0] [seed=42]\n", argv[0]);
        return 1;
    }
    const char *in_path = argv[1];
    long arg2 = atol(argv[2]);
    const char *out_path = argv[3];
    uint64_t max_iters = (argc >= 5) ? strtoull(argv[4], NULL, 10) : 0ULL;
    u32 arg_max_depth = (argc >= 6) ? (u32)atoi(argv[5]) : 0;
    u32 arg_max_size = (argc >= 7) ? (u32)atoi(argv[6]) : 0;
    uint64_t seed = (argc >= 8) ? strtoull(argv[7], NULL, 10) : 42ULL;
    mtRand.seed(seed);

    FILE *fp = fopen(in_path, "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }
    int n_in, m_in;
    if (fscanf(fp, "%d %d", &n_in, &m_in) != 2) {
        fclose(fp);
        return 1;
    }
    u8 N = (u8)n_in;
    Network_t full_nw;
    for (int k = 0; k < m_in; k++) {
        int u, v;
        if (fscanf(fp, "%d %d", &u, &v) != 2) break;
        if (u > v) { int t = u; u = v; v = t; }
        if (u >= 0 && v < n_in && u < v) {
            Pair_t p = {(u8)u, (u8)v};
            full_nw.push_back(p);
        }
    }
    fclose(fp);

    Network_t prefix, pairs;
    SinglePatternList_t singles;
    int pref_noops = 0;
    SortWord_t target_singles = (arg2 > 500) ? (SortWord_t)arg2 : 250000ULL;
    splitNetworkAuto(N, full_nw, target_singles, prefix, pairs, singles, pref_noops);

    std::shuffle(singles.begin(), singles.end(), mtRand);

    BitParallelList_t bpl;
    convertToBitParallel(N, singles, false, bpl);

    /* Single linear pass over bpl to drop exact step-wise no-ops in pairs */
    std::vector<uint8_t> active(pairs.size(), 0);
    BPWord_t data[NMAX];
    for (size_t idx = 0; idx < bpl.size(); idx += N) {
        for (size_t k = 0; k < N; k++) data[k] = bpl[idx + k];
        for (size_t n = 0; n < pairs.size(); n++) {
            u32 i = pairs[n].lo, j = pairs[n].hi;
            BPWord_t iold = data[i];
            if ((iold & ~data[j]) != 0ULL) active[n] = 1;
            data[i] &= data[j];
            data[j] |= iold;
        }
    }
    Network_t act_pairs;
    int pair_noops = 0;
    for (size_t n = 0; n < pairs.size(); n++) {
        if (active[n]) act_pairs.push_back(pairs[n]);
        else pair_noops++;
    }
    pairs.swap(act_pairs);
    int noop_dropped = pref_noops + pair_noops;

    Network_t totalnw;
    concatNetwork(prefix, pairs, totalnw);
    u32 init_size = (u32)totalnw.size();
    u32 init_depth = 0, init_crit = 0, init_zs = 0;
    uint8_t init_cw[64];
    computeDepthAndCrit(N, totalnw, init_depth, init_crit, init_zs, init_cw);
    u32 max_allowed_depth = (arg_max_depth > 0) ? arg_max_depth : init_depth;
    u32 EffMaxDepth = std::max(init_depth, max_allowed_depth);

    /* Only run startup LOO / 2-for-1 if not resuming a depth-drop checkpoint, or if it preserves crit */
    int pruned_loo = 0;
    int pruned_2for1 = 0;
    if (init_depth <= max_allowed_depth) {
        /* Pass 1: Exhaustive Leave-One-Out Redundancy Pruning on pairs */
        pruned_loo = run_loo_on_pairs(N, prefix, pairs, bpl, EffMaxDepth);

        /* Pass 2: Full-Suffix 2-for-1 Compression across all pairs within window 35 */
        bool c2 = true;
        while (c2) {
            c2 = false;
            int p_len = (int)pairs.size();
            for (int a = p_len - 2; a >= 0 && !c2; a--) {
                int b_lim = std::min(p_len - 1, a + 35);
                for (int b = b_lim; b > a && !c2; b--) {
                    u8 la = pairs[a].lo, ha = pairs[a].hi;
                    u8 lb = pairs[b].lo, hb = pairs[b].hi;
                    bool share = (la == lb || la == hb || ha == lb || ha == hb);
                    if (!share && (b - a) > 12) continue;

                    Network_t base = pairs;
                    base.erase(base.begin() + b);
                    base.erase(base.begin() + a);
                    u8 w[4] = {la, ha, lb, hb};
                    int pos_opts[2] = {a, b - 1};
                    for (int pi = 0; pi < 2 && !c2; pi++) {
                        int ins_pos = pos_opts[pi];
                        if (pi == 1 && ins_pos == a) continue;
                        for (int wi = 0; wi < 4 && !c2; wi++) {
                            u8 u0 = w[wi];
                            for (u8 v0 = 0; v0 < N; v0++) {
                                if (u0 == v0) continue;
                                Pair_t rep = {(u8)min(u0, v0), (u8)max(u0, v0)};
                                base.insert(base.begin() + ins_pos, rep);
                                if (testPairs(N, base, bpl)) {
                                    concatNetwork(prefix, base, totalnw);
                                    if (computeDepth(totalnw) <= EffMaxDepth) {
                                        pairs.swap(base);
                                        pruned_2for1++;
                                        c2 = true;
                                        break;
                                    }
                                }
                                base.erase(base.begin() + ins_pos);
                            }
                        }
                    }
                }
            }
        }
    }

    concatNetwork(prefix, pairs, totalnw);
    u32 best_size = (u32)totalnw.size();
    u32 best_depth = 0, best_crit = 0, best_zs = 0;
    uint8_t crit_wires[64];
    computeDepthAndCrit(N, totalnw, best_depth, best_crit, best_zs, crit_wires);
    u32 max_allowed_size = (arg_max_size > 0) ? arg_max_size : best_size;

    printf("[sn_opt] N=%u pref=%lu pairs=%lu singles=%lu noops=%d loo=%d 2for1=%d final=(%u, %u) crit=%u zs=%u\n",
           (unsigned)N, prefix.size(), pairs.size(), singles.size(), noop_dropped, pruned_loo, pruned_2for1, best_size, best_depth, best_crit, best_zs);
    fflush(stdout);
    if (best_size <= max_allowed_size) {
        save_network(out_path, N, totalnw);
    }

    /* Pass 3: Guided Critical-Path + Deterministic-LOO SorterHunter Evolutionary Search */
    if (max_iters > 0 && pairs.size() > 0) {
        Network_t alphabet;
        for (u8 i = 0; i < N - 1; i++) {
            for (u8 j = i + 1; j < N; j++) {
                Pair_t p = {i, j};
                alphabet.push_back(p);
            }
        }
        Network_t best_pairs = pairs;
        u32 cur_dp = best_depth, cur_crit = best_crit, cur_zs = best_zs;
        uint64_t last_imp_iter = 0;
        std::vector<u8> mutationSelector = {0, 1, 2, 3, 4, 4, 5, 5};

        uint64_t accepted_cnt = 0;
        for (uint64_t iter = 1; iter <= max_iters; iter++) {
            bool want_depth_drop = (cur_dp > max_allowed_depth);
            bool bias_crit = want_depth_drop ? ((mtRand() % 4) != 0) : ((mtRand() % 4) == 0);
            u32 nmods = 1 + (mtRand() % 2);
            Network_t newpairs = pairs;
            u32 modcount = 0;
            while (modcount < nmods) {
                if (attemptMutation(N, newpairs, alphabet, mutationSelector, crit_wires, bias_crit) != 0) {
                    modcount++;
                }
            }
            if (newpairs.size() > 0 && testPairs(N, newpairs, bpl)) {
                concatNetwork(prefix, newpairs, totalnw);
                u32 dp = 0, crit = 0, zs = 0;
                uint8_t new_cw[64];
                computeDepthAndCrit(N, totalnw, dp, crit, zs, new_cw);

                bool accept = false;
                if (want_depth_drop) {
                    u32 best_score = best_depth * 1000 + best_crit;
                    u32 new_score = dp * 1000 + crit;
                    u32 slack = (best_crit <= 2) ? 3 : 2;
                    if (dp <= best_depth && new_score <= best_score + slack &&
                        totalnw.size() <= (size_t)(max_allowed_size + 1)) {
                        accept = true;
                    }
                } else {
                    if (dp <= max_allowed_depth && totalnw.size() <= (size_t)best_size) {
                        accept = true;
                    }
                }

                if (accept) {
                    accepted_cnt++;
                    bool commit_loo = false;
                    Network_t test_loo;
                    u32 loo_dp = dp, loo_crit = crit, loo_zs = zs;
                    uint8_t loo_cw[64];
                    if ((accepted_cnt & 15ULL) == 0ULL || (prefix.size() + newpairs.size()) < best_size || dp < best_depth) {
                        test_loo = newpairs;
                        int extra_loo = run_loo_on_pairs(N, prefix, test_loo, bpl, std::max(dp, max_allowed_depth));
                        u32 loo_sz = (u32)(prefix.size() + test_loo.size());
                        if (extra_loo > 0) {
                            concatNetwork(prefix, test_loo, totalnw);
                            computeDepthAndCrit(N, totalnw, loo_dp, loo_crit, loo_zs, loo_cw);
                            if (want_depth_drop) {
                                if (loo_sz <= max_allowed_size + 1 &&
                                    (loo_dp < best_depth || (loo_dp == best_depth && loo_crit < best_crit))) {
                                    commit_loo = true;
                                } else if (dp == best_depth && crit <= best_crit &&
                                           loo_dp == dp && loo_crit <= crit && loo_sz <= max_allowed_size) {
                                    commit_loo = true;
                                }
                            } else {
                                if (loo_dp <= max_allowed_depth && loo_sz <= best_size) {
                                    commit_loo = true;
                                }
                            }
                        }
                    }

                    if (commit_loo) {
                        pairs.swap(test_loo);
                        cur_dp = loo_dp;
                        cur_crit = loo_crit;
                        cur_zs = loo_zs;
                        memcpy(crit_wires, loo_cw, 64);
                    } else {
                        pairs.swap(newpairs);
                        cur_dp = dp;
                        cur_crit = crit;
                        cur_zs = zs;
                        memcpy(crit_wires, new_cw, 64);
                    }
                    u32 sz = (u32)(prefix.size() + pairs.size());

                    bool is_new_best = false;
                    if (want_depth_drop) {
                        if (cur_dp < best_depth && sz <= max_allowed_size + 1) {
                            is_new_best = true;
                        } else if (cur_dp == best_depth && sz <= max_allowed_size + 1 && cur_crit < best_crit) {
                            best_crit = cur_crit;
                            best_zs = cur_zs;
                            best_pairs = pairs;
                            last_imp_iter = iter;
                            printf("[sn_opt] iter=%llu N=%u (%u, %u) crit=%u zs=%u\n",
                                   (unsigned long long)iter, (unsigned)N, sz, cur_dp, cur_crit, cur_zs);
                            fflush(stdout);
                            concatNetwork(prefix, pairs, totalnw);
                            char crit_path[512];
                            snprintf(crit_path, sizeof(crit_path), "%s.crit", out_path);
                            save_network(crit_path, N, totalnw);
                            if (sz <= max_allowed_size) {
                                save_network(out_path, N, totalnw);
                            }
                        }
                    } else {
                        if (cur_dp <= max_allowed_depth && sz < best_size) {
                            is_new_best = true;
                        } else if (cur_dp < best_depth && sz <= max_allowed_size + 1) {
                            is_new_best = true;
                        }
                    }

                    if (is_new_best) {
                        best_size = sz;
                        best_depth = cur_dp;
                        best_crit = cur_crit;
                        best_zs = cur_zs;
                        best_pairs = pairs;
                        last_imp_iter = iter;
                        concatNetwork(prefix, pairs, totalnw);
                        printf("[sn_opt] NEW PARETO AT ITER %llu: N=%u (%u, %u) crit=%u zs=%u\n",
                               (unsigned long long)iter, (unsigned)N, sz, cur_dp, cur_crit, cur_zs);
                        fflush(stdout);
                        if (sz <= max_allowed_size) {
                            save_network(out_path, N, totalnw);
                        } else {
                            char plus1_path[512];
                            snprintf(plus1_path, sizeof(plus1_path), "%s.plus1", out_path);
                            save_network(plus1_path, N, totalnw);
                        }
                    }
                }
            }

            /* Controlled 1-comparator escape ONLY during depth-drop stage */
            if (cur_dp > max_allowed_depth && (iter % 200) == 0 &&
                (prefix.size() + pairs.size()) <= (size_t)max_allowed_size) {
                int a = mtRand() % (pairs.size() + 1);
                if (a < (int)pairs.size()) {
                    pairs.insert(pairs.begin() + a, pairs[a]);
                }
            }

            /* Restart to best_pairs if stagnant for 100000 iterations during depth-drop stage */
            if (best_depth > max_allowed_depth && iter - last_imp_iter >= 100000) {
                pairs = best_pairs;
                if ((prefix.size() + pairs.size()) < (size_t)max_allowed_size) {
                    int a = mtRand() % pairs.size();
                    pairs.insert(pairs.begin() + a, pairs[a]);
                }
                concatNetwork(prefix, pairs, totalnw);
                computeDepthAndCrit(N, totalnw, cur_dp, cur_crit, cur_zs, crit_wires);
                last_imp_iter = iter;
            }
        }
    }

    return 0;
}
