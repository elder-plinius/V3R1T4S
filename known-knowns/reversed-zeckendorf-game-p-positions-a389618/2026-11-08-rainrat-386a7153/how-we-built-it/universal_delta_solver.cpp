// Universal h_1-Eliminated Deficit-Stratified 256-Bit Word-Parallel Solver
// for the Reversed Zeckendorf Game (OEIS A389617, A389618, A389619) for n = 2..250.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

static constexpr int MAX_N = 250;
static constexpr int F[13] = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233};
static constexpr int SHIFT[13] = {0, 0, 0, 8, 15, 21, 26, 31, 35, 38, 41, 43, 44};
static constexpr int BITS[13]  = {0, 0, 8, 7,  6,  5,  5,  4,  3,  3,  2,  1,  1};
static constexpr uint64_t STEP[13] = {
    0ULL, 0ULL,
    1ULL << 0,  1ULL << 8,  1ULL << 15, 1ULL << 21, 1ULL << 26,
    1ULL << 31, 1ULL << 35, 1ULL << 38, 1ULL << 41, 1ULL << 43, 1ULL << 44
};

struct WinBits {
    uint64_t w[4];
};

struct StateNode {
    uint64_t key;
    uint16_t m;
    uint16_t wsum;
};

struct FlatHash {
    uint64_t mask = 0;
    std::vector<uint64_t> keys;
    std::vector<uint32_t> vals;

    void init(size_t n) {
        size_t cap = 16;
        while (cap < n * 2 + 8) cap <<= 1;
        mask = cap - 1;
        keys.assign(cap, UINT64_MAX);
        vals.assign(cap, 0);
    }

    static inline uint64_t mix(uint64_t k) {
        k ^= k >> 30;
        k *= 0xbf58476d1ce4e5b9ULL;
        k ^= k >> 27;
        k *= 0x94d049bb133111ebULL;
        k ^= k >> 31;
        return k;
    }

    inline void insert(uint64_t k, uint32_t v) {
        size_t idx = mix(k) & mask;
        while (keys[idx] != UINT64_MAX) {
            idx = (idx + 1) & mask;
        }
        keys[idx] = k;
        vals[idx] = v;
    }

    inline uint32_t find(uint64_t k) const {
        size_t idx = mix(k) & mask;
        while (keys[idx] != k) {
            if (keys[idx] == UINT64_MAX) {
                std::cerr << "Fatal: missing key in FlatHash::find\n";
                std::exit(1);
            }
            idx = (idx + 1) & mask;
        }
        return vals[idx];
    }
};

static inline void or_not_ge(WinBits &dst, const WinBits &src, int min_n) {
    for (int b = 0; b < 4; ++b) {
        int lo = b * 64;
        int hi = lo + 63;
        if (hi < min_n || lo > MAX_N) continue;
        uint64_t mask = ~0ULL;
        if (min_n > lo) {
            mask &= (~0ULL) << (min_n - lo);
        }
        if (MAX_N < hi) {
            int keep = MAX_N - lo + 1;
            if (keep < 64) mask &= (1ULL << keep) - 1ULL;
        }
        dst.w[b] |= (~src.w[b]) & mask;
    }
}

static void gen_level(int idx, int rem_delta, int cur_m, int cur_w, uint64_t cur_key,
                      std::vector<StateNode> &out) {
    if (idx == 2) {
        int h2 = rem_delta; // since F[2] - 1 == 1
        int m = cur_m + 2 * h2;
        if (m <= MAX_N) {
            uint64_t key = cur_key | (uint64_t(h2) << SHIFT[2]);
            uint16_t wsum = uint16_t(cur_w + 2 * h2);
            out.push_back({key, uint16_t(m), wsum});
        }
        return;
    }
    int df = F[idx] - 1;
    int max_h = rem_delta / df;
    int rem_m = (MAX_N - cur_m) / F[idx];
    if (rem_m < max_h) max_h = rem_m;
    for (int h = 0; h <= max_h; ++h) {
        gen_level(idx - 1,
                  rem_delta - h * df,
                  cur_m + h * F[idx],
                  cur_w + h * idx,
                  cur_key | (uint64_t(h) << SHIFT[idx]),
                  out);
    }
}

static uint64_t zeck_key_and_delta(int n, int &out_delta, int &out_m) {
    int rem = n;
    uint64_t key = 0;
    int delta = 0;
    int m = 0;
    for (int i = 12; i >= 1; --i) {
        if (F[i] <= rem) {
            rem -= F[i];
            if (i >= 2) {
                key |= STEP[i];
                delta += (F[i] - 1);
                m += F[i];
            }
        }
    }
    assert(rem == 0);
    out_delta = delta;
    out_m = m;
    return key;
}

int main(int argc, char **argv) {
    auto t0 = std::chrono::steady_clock::now();

    std::vector<uint64_t> verts_at_m(MAX_N + 1, 0);
    std::vector<uint64_t> edges_entering_at_n(MAX_N + 1, 0);

    // Precompute Zeckendorf starting states for n = 2..250
    std::vector<uint64_t> z_key(MAX_N + 1, 0);
    std::vector<int> z_delta(MAX_N + 1, 0);
    std::vector<int> winner(MAX_N + 1, 0);
    for (int n = 2; n <= MAX_N; ++n) {
        int d = 0, m = 0;
        z_key[n] = zeck_key_and_delta(n, d, m);
        z_delta[n] = d;
    }

    FlatHash prev_hash;
    std::vector<WinBits> prev_win;

    uint64_t total_states = 0;
    size_t max_level_size = 0;

    for (int d = 0; d <= MAX_N; ++d) {
        std::vector<StateNode> nodes;
        gen_level(12, d, 0, 0, 0ULL, nodes);
        if (nodes.empty()) {
            prev_hash = FlatHash();
            prev_win.clear();
            continue;
        }
        total_states += nodes.size();
        if (nodes.size() > max_level_size) max_level_size = nodes.size();

        // Sort descending by (m, wsum) so every Combine move points to an earlier index in `nodes`
        std::sort(nodes.begin(), nodes.end(), [](const StateNode &a, const StateNode &b) {
            if (a.m != b.m) return a.m > b.m;
            if (a.wsum != b.wsum) return a.wsum > b.wsum;
            return a.key > b.key;
        });

        FlatHash cur_hash;
        cur_hash.init(nodes.size());
        for (uint32_t idx = 0; idx < nodes.size(); ++idx) {
            cur_hash.insert(nodes[idx].key, idx);
        }

        std::vector<WinBits> cur_win(nodes.size(), WinBits{{0ULL, 0ULL, 0ULL, 0ULL}});

        for (uint32_t idx = 0; idx < nodes.size(); ++idx) {
            const uint64_t key = nodes[idx].key;
            const int m = nodes[idx].m;
            verts_at_m[m] += 1;

            WinBits wb{{0ULL, 0ULL, 0ULL, 0ULL}};

            // Unpack counts h[2..12]
            int h[13];
            for (int i = 2; i <= 12; ++i) {
                h[i] = int((key >> SHIFT[i]) & ((1ULL << BITS[i]) - 1ULL));
            }

            // 1. Split moves (into level d - 1)
            if (h[2] >= 1) {
                uint64_t nk = key - STEP[2];
                uint32_t nidx = prev_hash.find(nk);
                or_not_ge(wb, prev_win[nidx], std::max(2, m));
                edges_entering_at_n[std::max(2, m)] += 1;
            }
            if (h[3] >= 1) {
                uint64_t nk = key - STEP[3] + STEP[2];
                uint32_t nidx = prev_hash.find(nk);
                or_not_ge(wb, prev_win[nidx], std::max(2, m));
                edges_entering_at_n[std::max(2, m)] += 1;
            }
            for (int i = 3; i <= 11; ++i) {
                if (h[i + 1] >= 1) {
                    uint64_t nk = key - STEP[i + 1] + STEP[i] + STEP[i - 1];
                    uint32_t nidx = prev_hash.find(nk);
                    or_not_ge(wb, prev_win[nidx], std::max(2, m));
                    edges_entering_at_n[std::max(2, m)] += 1;
                }
            }

            // 2. Combine moves (within level d, already evaluated at < idx)
            // i = 2: F_1 + F_3 -> 2 F_2 (requires h_1 = n - m >= 1, so n >= m + 1)
            if (h[3] >= 1 && m + 1 <= MAX_N) {
                uint64_t nk = key - STEP[3] + 2 * STEP[2];
                uint32_t nidx = cur_hash.find(nk);
                assert(nidx < idx);
                or_not_ge(wb, cur_win[nidx], m + 1);
                edges_entering_at_n[m + 1] += 1;
            }
            // i = 3: F_1 + F_4 -> 2 F_3 (requires h_1 = n - m >= 1, so n >= m + 1)
            if (h[4] >= 1 && m + 1 <= MAX_N) {
                uint64_t nk = key - STEP[4] + 2 * STEP[3];
                uint32_t nidx = cur_hash.find(nk);
                assert(nidx < idx);
                or_not_ge(wb, cur_win[nidx], m + 1);
                edges_entering_at_n[m + 1] += 1;
            }
            // i = 4..11: F_{i-2} + F_{i+1} -> 2 F_i (i - 2 >= 2, legal for all n >= max(2, m))
            for (int i = 4; i <= 11; ++i) {
                if (h[i - 2] >= 1 && h[i + 1] >= 1) {
                    uint64_t nk = key - STEP[i - 2] - STEP[i + 1] + 2 * STEP[i];
                    uint32_t nidx = cur_hash.find(nk);
                    assert(nidx < idx);
                    or_not_ge(wb, cur_win[nidx], std::max(2, m));
                    edges_entering_at_n[std::max(2, m)] += 1;
                }
            }

            cur_win[idx] = wb;
        }

        // Extract winners for any n whose Zeckendorf decomposition lies at deficit d
        for (int n = 2; n <= MAX_N; ++n) {
            if (z_delta[n] == d) {
                uint32_t idx = cur_hash.find(z_key[n]);
                bool is_p1 = (cur_win[idx].w[n >> 6] >> (n & 63)) & 1ULL;
                winner[n] = is_p1 ? 1 : 2;
            }
        }

        prev_hash = std::move(cur_hash);
        prev_win = std::move(cur_win);
    }

    std::vector<uint64_t> total_verts(MAX_N + 1, 0);
    std::vector<uint64_t> total_edges(MAX_N + 1, 0);
    uint64_t v_acc = verts_at_m[0] + verts_at_m[1];
    uint64_t e_acc = 0;
    for (int n = 2; n <= MAX_N; ++n) {
        v_acc += verts_at_m[n];
        e_acc += edges_entering_at_n[n];
        total_verts[n] = v_acc;
        total_edges[n] = e_acc;
    }

    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "total_universal_states: " << total_states << "\n";
    std::cout << "max_delta_level_states: " << max_level_size << "\n";
    std::cout << "elapsed_seconds: " << sec << "\n";

    std::string out_path = (argc > 1) ? argv[1] : "universal_delta_n2_250.tsv";
    std::ofstream out(out_path);
    if (!out) {
        std::cerr << "Fatal: failed to open output file " << out_path << "\n";
        return 1;
    }
    out << "n\twinner\tedges\tvertices\n";
    for (int n = 2; n <= MAX_N; ++n) {
        out << n << "\t" << winner[n] << "\t" << total_edges[n] << "\t" << total_verts[n] << "\n";
    }
    out.flush();
    if (!out.good()) {
        std::cerr << "Fatal: I/O error writing output file " << out_path << "\n";
        return 1;
    }
    out.close();
    return 0;
}
