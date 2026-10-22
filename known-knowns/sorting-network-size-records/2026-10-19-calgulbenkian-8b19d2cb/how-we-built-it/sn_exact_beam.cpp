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

static void swap_sortedpatterns_fast(SinglePatternList_t &pl, const Pair_t &p, bool &was_noop) {
    const SortWord_t m1 = 1ULL << p.lo;
    const SortWord_t m2 = 1ULL << p.hi;
    const SortWord_t m = m1 | m2;

    static thread_local SinglePatternList_t keep, moved;
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
        if (n_clusters <= 6 && outputSize() <= target_singles) {
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
                if (n_clusters <= 6 && outputSize() <= target_singles) {
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

static void forward_wire_reduce_vec(u8 N, const Network_t &in_ces, int w0, int val, Network_t &out_ces) {
    int pi[64];
    for (int u = 0; u < (int)N; u++) {
        if (u == w0) pi[u] = -1;
        else pi[u] = (u < w0) ? u : (u - 1);
    }
    int p = w0;
    out_ces.clear();
    out_ces.reserve(in_ces.size());
    for (size_t k = 0; k < in_ces.size(); k++) {
        int i = in_ces[k].lo;
        int j = in_ces[k].hi;
        if (i == p || j == p) {
            int other = (i == p) ? j : i;
            int real_wire = pi[other];
            pi[other] = -1;
            if (val == 0) {
                p = i;
                pi[j] = real_wire;
            } else {
                p = j;
                pi[i] = real_wire;
            }
        } else {
            int u = pi[i], v = pi[j];
            int lo = (u < v) ? u : v;
            int hi = (u < v) ? v : u;
            pi[i] = lo;
            pi[j] = hi;
            Pair_t pr = {(u8)lo, (u8)hi};
            out_ces.push_back(pr);
        }
    }
}

/* 100% Exact 0-1 step-wise no-op + Leave-One-Out pruning via splitNetworkAuto + BitParallel */
static void exact_prune_loo(u8 N, const Network_t &in_nw, SortWord_t target_singles,
                            Network_t &out_nw, Network_t &out_noop_nw, int &out_noops, int &out_loo) {
    Network_t prefix, pairs;
    SinglePatternList_t singles;
    int pref_noops = 0;
    splitNetworkAuto(N, in_nw, target_singles, prefix, pairs, singles, pref_noops);

    static thread_local std::mt19937_64 rng(1234567ULL);
    std::shuffle(singles.begin(), singles.end(), rng);

    BitParallelList_t bpl;
    convertToBitParallel(N, singles, false, bpl);

    /* Linear pass over bpl to drop all exact step-wise no-ops in pairs */
    std::vector<uint8_t> active(pairs.size(), 0);
    BPWord_t data[NMAX];
    for (size_t idx = 0; idx < bpl.size(); idx += N) {
        for (size_t k = 0; k < N; k++) data[k] = bpl[idx + k];
        for (size_t n = 0; n < pairs.size(); n++) {
            u32 i = pairs[n].lo;
            u32 j = pairs[n].hi;
            BPWord_t iold = data[i];
            if ((iold & ~data[j]) != 0ULL) active[n] = 1;
            data[i] &= data[j];
            data[j] |= iold;
        }
    }
    Network_t active_pairs;
    active_pairs.reserve(pairs.size());
    int pair_noops = 0;
    for (size_t n = 0; n < pairs.size(); n++) {
        if (active[n]) active_pairs.push_back(pairs[n]);
        else pair_noops++;
    }
    pairs.swap(active_pairs);
    out_noops = pref_noops + pair_noops;
    concatNetwork(prefix, pairs, out_noop_nw);

    /* Exact Leave-One-Out on pairs */
    out_loo = 0;
    bool changed = true;
    while (changed) {
        changed = false;
        for (int i = (int)pairs.size() - 1; i >= 0; i--) {
            Network_t cand = pairs;
            cand.erase(cand.begin() + i);
            if (testPairs(N, cand, bpl)) {
                pairs.swap(cand);
                out_loo++;
                changed = true;
                break;
            }
        }
    }

    concatNetwork(prefix, pairs, out_nw);
}

/* Fast 16-group bit-parallel step-wise no-op pre-estimator (used only to pick top K children per parent when B*2*N is large) */
#define FAST_G 32
static uint64_t fast_bpl[65][FAST_G][64];
static bool fast_inited[65];

static void init_fast_bpl(int n) {
    if (fast_inited[n]) return;
    uint64_t s = 0x9e3779b97f4a7c15ULL ^ ((uint64_t)n * 0x517cc1b727220a95ULL);
    auto xs = [&]() {
        s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s;
    };
    memset(fast_bpl[n], 0, sizeof(fast_bpl[n]));
    for (int g = 0; g < FAST_G; g++) {
        for (int w = 0; w < n; w++) {
            uint64_t word = xs();
            int m = g % 6;
            if (m == 1) word &= xs();
            else if (m == 2) word |= xs();
            else if (m == 3) word &= xs() & xs();
            else if (m == 4) word |= xs() | xs();
            fast_bpl[n][g][w] = word;
        }
    }
    fast_inited[n] = true;
}

static int fast_noop_est(int n, const Network_t &ces) {
    init_fast_bpl(n);
    int m = (int)ces.size();
    uint8_t act[600];
    memset(act, 0, m);
    for (int g = 0; g < FAST_G; g++) {
        uint64_t d[64];
        for (int w = 0; w < n; w++) d[w] = fast_bpl[n][g][w];
        for (int k = 0; k < m; k++) {
            int u = ces[k].lo, v = ces[k].hi;
            uint64_t a = d[u], b = d[v];
            if ((a & ~b) != 0ULL) act[k] = 1;
            d[u] = a & b; d[v] = a | b;
        }
    }
    int cnt = 0;
    for (int k = 0; k < m; k++) cnt += act[k];
    return cnt;
}

static void save_nw(const char *dir, const char *tag, int n, int sz, int dp, int idx, const Network_t &nw) {
    char path[512];
    snprintf(path, sizeof(path), "%s/exact_%s_n%d_s%d_d%d_i%d.txt", dir, tag, n, sz, dp, idx);
    FILE *fp = fopen(path, "w");
    if (!fp) return;
    fprintf(fp, "%d %lu\n", n, nw.size());
    for (size_t k = 0; k < nw.size(); k++) {
        fprintf(fp, "%u %u\n", (unsigned)nw[k].lo, (unsigned)nw[k].hi);
    }
    fclose(fp);
}

struct BeamItem {
    u8 n;
    u32 size;
    u32 depth;
    Network_t nw;
    Network_t noop_nw;
};

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s <in_txt> <max_k> <out_dir> <tag> [beam_w=10] [target_singles=40000]\n", argv[0]);
        return 1;
    }
    const char *in_path = argv[1];
    int max_k = atoi(argv[2]);
    const char *out_dir = argv[3];
    const char *tag = argv[4];
    int beam_w = (argc >= 6) ? atoi(argv[5]) : 10;
    SortWord_t target_singles = (argc >= 7) ? (SortWord_t)atol(argv[6]) : 40000ULL;

    FILE *fp = fopen(in_path, "r");
    if (!fp) return 1;
    int n_in, m_in;
    if (fscanf(fp, "%d %d", &n_in, &m_in) != 2) { fclose(fp); return 1; }
    Network_t init_nw;
    for (int k = 0; k < m_in; k++) {
        int u, v;
        if (fscanf(fp, "%d %d", &u, &v) != 2) break;
        if (u > v) std::swap(u, v);
        Pair_t p = {(u8)u, (u8)v};
        init_nw.push_back(p);
    }
    fclose(fp);

    std::vector<BeamItem> beam;
    BeamItem root;
    root.n = (u8)n_in;
    int r_noops = 0, r_loo = 0;
    exact_prune_loo(root.n, init_nw, target_singles, root.nw, root.noop_nw, r_noops, r_loo);
    root.size = (u32)root.nw.size();
    root.depth = computeDepth(root.nw);
    if (r_noops > 0 || r_loo > 0) {
        printf("ROOT PRUNED n=%u (%d -> %u, d=%u) noops=%d loo=%d\n",
               (unsigned)root.n, m_in, root.size, root.depth, r_noops, r_loo);
        save_nw(out_dir, tag, root.n, root.size, root.depth, 0, root.nw);
    }
    beam.push_back(root);

    for (int step = 1; step <= max_k && !beam.empty() && beam[0].n > 13; step++) {
        u8 next_n = beam[0].n - 1;
        struct RawChild {
            int parent_idx;
            int raw_m;
            int est_m;
            u32 raw_d;
            Network_t raw_nw;
        };
        std::vector<RawChild> candidates;

        /* Generate all 2*N children for each beam item (from both nw and noop_nw if different) */
        for (size_t b = 0; b < beam.size(); b++) {
            u8 N = beam[b].n;
            std::vector<RawChild> p_cands;
            int num_variants = (beam[b].noop_nw.size() != beam[b].nw.size()) ? 2 : 1;
            for (int var = 0; var < num_variants; var++) {
                const Network_t &src_nw = (var == 0) ? beam[b].nw : beam[b].noop_nw;
                for (int sw = 0; sw < (int)N; sw++) {
                    int w0 = (sw % 2 == 0) ? (N / 2 + sw / 2) : (N / 2 - (sw + 1) / 2);
                    if (w0 < 0 || w0 >= (int)N) w0 = sw;
                    for (int val = 1; val >= 0; val--) {
                        RawChild rc;
                        rc.parent_idx = (int)b;
                        forward_wire_reduce_vec(N, src_nw, w0, val, rc.raw_nw);
                        rc.raw_m = (int)rc.raw_nw.size();
                        rc.est_m = fast_noop_est(next_n, rc.raw_nw);
                        rc.raw_d = computeDepth(rc.raw_nw);
                        /* Deduplicate within parent */
                        bool dup = false;
                        for (size_t j = 0; j < p_cands.size(); j++) {
                            if (p_cands[j].raw_m == rc.raw_m && p_cands[j].raw_d == rc.raw_d &&
                                memcmp(p_cands[j].raw_nw.data(), rc.raw_nw.data(), rc.raw_m * sizeof(Pair_t)) == 0) {
                                dup = true;
                                break;
                            }
                        }
                        if (!dup) p_cands.push_back(rc);
                    }
                }
            }
            /* Sort parent's children by exact (raw_m, raw_d, est_m) so Sort_LS_* low-swap comparators never bias ranking */
            std::sort(p_cands.begin(), p_cands.end(), [](const RawChild &a, const RawChild &b) {
                if (a.raw_m != b.raw_m) return a.raw_m < b.raw_m;
                if (a.raw_d != b.raw_d) return a.raw_d < b.raw_d;
                return a.est_m < b.est_m;
            });
            /* At step 1 (1 parent), evaluate ALL 100% of distinct children; at step >= 2, evaluate top 12 per parent */
            size_t cap = (beam.size() == 1) ? p_cands.size() : 12;
            for (size_t j = 0; j < p_cands.size() && j < cap; j++) {
                candidates.push_back(p_cands[j]);
            }
        }

        /* Deduplicate across parents before running exact_prune_loo */
        std::vector<BeamItem> next_all;
        for (size_t i = 0; i < candidates.size(); i++) {
            bool dup_raw = false;
            for (size_t j = 0; j < i; j++) {
                if (candidates[j].raw_m == candidates[i].raw_m &&
                    candidates[j].raw_d == candidates[i].raw_d &&
                    memcmp(candidates[j].raw_nw.data(), candidates[i].raw_nw.data(),
                           candidates[i].raw_m * sizeof(Pair_t)) == 0) {
                    dup_raw = true;
                    break;
                }
            }
            if (dup_raw) continue;

            BeamItem item;
            item.n = next_n;
            int noops = 0, loo = 0;
            exact_prune_loo(next_n, candidates[i].raw_nw, target_singles, item.nw, item.noop_nw, noops, loo);
            item.size = (u32)item.nw.size();
            item.depth = computeDepth(item.nw);

            bool dup_pruned = false;
            for (size_t j = 0; j < next_all.size(); j++) {
                if (next_all[j].size == item.size && next_all[j].depth == item.depth &&
                    memcmp(next_all[j].nw.data(), item.nw.data(), item.size * sizeof(Pair_t)) == 0) {
                    dup_pruned = true;
                    break;
                }
            }
            if (!dup_pruned) {
                next_all.push_back(item);
            }
        }

        std::sort(next_all.begin(), next_all.end(), [](const BeamItem &a, const BeamItem &b) {
            if (a.size != b.size) return a.size < b.size;
            return a.depth < b.depth;
        });

        /* Save best per depth and build next beam */
        u32 best_d[64];
        int saved_d[64];
        for (int d = 0; d < 64; d++) { best_d[d] = 999999; saved_d[d] = 0; }
        for (size_t j = 0; j < next_all.size(); j++) {
            u32 d = next_all[j].depth;
            if (next_all[j].size < best_d[d]) best_d[d] = next_all[j].size;
        }
        beam.clear();
        for (size_t j = 0; j < next_all.size(); j++) {
            u32 d = next_all[j].depth;
            if (next_all[j].size <= best_d[d] + 1 && saved_d[d] < 6) {
                saved_d[d]++;
                if (saved_d[d] == 1) {
                    printf("STEP k=%d n=%u exact_size=%u depth=%u\n",
                           step, (unsigned)next_n, next_all[j].size, d);
                }
                save_nw(out_dir, tag, next_n, next_all[j].size, d, saved_d[d], next_all[j].nw);
            }
            if ((int)beam.size() < beam_w && next_all[j].size <= best_d[d] + 1) {
                beam.push_back(next_all[j]);
            }
        }
    }

    return 0;
}
