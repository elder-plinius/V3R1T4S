// Fast 128-bit bit-parallel Node-Kayles Sprague-Grundy solver
// Uses: connected-component XOR splitting, O(1) path/cycle octal .137 folding,
// true-twin collapse, 1-WL + individualization-refinement exact canonical keys,
// and an open-addressed arena-backed transposition table.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>

using u128 = __uint128_t;
using u64 = uint64_t;
using u32 = uint32_t;
using u16 = uint16_t;
using u8 = uint8_t;

static inline int ctz128(u128 x) {
    u64 lo = (u64)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((u64)(x >> 64));
}

static inline int popcnt128(u128 x) {
    return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64));
}

static inline u64 splitmix64(u64 x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

// Precompute octal .137 (Node-Kayles on paths P_n) up to MAXN
static constexpr int MAXN = 128;
static int path_nimber[MAXN + 1];

static void init_paths() {
    path_nimber[0] = 0;
    path_nimber[1] = 1;
    path_nimber[2] = 1;
    for (int n = 3; n <= MAXN; ++n) {
        u64 seen = 0;
        // remove vertex i in 0..n-1: leaves P_{max(0, i-1)} + P_{max(0, n-i-2)}
        for (int i = 0; i <= n / 2; ++i) {
            int left = (i >= 2) ? (i - 1) : 0;
            int right = (n - 1 - i >= 2) ? (n - 2 - i) : 0;
            int g = path_nimber[left] ^ path_nimber[right];
            if (g < 64) seen |= (1ULL << g);
        }
        int mex = 0;
        while (seen & (1ULL << mex)) ++mex;
        path_nimber[n] = mex;
    }
}

// Arena-backed exact canonical graph hash table
struct Entry {
    u64 hash;
    u32 offset; // offset in arena (0 = empty, 1-based)
    u16 len;    // number of u16s: [k, m, edge_0, ..., edge_{m-1}]
    u8 val;
};

struct TransTable {
    std::vector<Entry> table;
    std::vector<u16> arena;
    size_t mask;
    size_t count = 0;

    TransTable(size_t pow2_size = (1ULL << 22)) {
        table.assign(pow2_size, Entry{0, 0, 0, 0});
        mask = pow2_size - 1;
        arena.reserve(1 << 23);
        arena.push_back(0); // dummy 0 so offset >= 1
    }

    void rehash() {
        size_t new_sz = table.size() * 2;
        std::vector<Entry> nt(new_sz, Entry{0, 0, 0, 0});
        size_t nm = new_sz - 1;
        for (const auto& e : table) {
            if (e.offset == 0) continue;
            size_t idx = e.hash & nm;
            while (nt[idx].offset != 0) idx = (idx + 1) & nm;
            nt[idx] = e;
        }
        table.swap(nt);
        mask = nm;
    }

    int lookup(u64 h, const u16* key, u16 len) const {
        size_t idx = h & mask;
        while (true) {
            const auto& e = table[idx];
            if (e.offset == 0) return -1;
            if (e.hash == h && e.len == len) {
                if (std::memcmp(&arena[e.offset], key, len * sizeof(u16)) == 0) {
                    return e.val;
                }
            }
            idx = (idx + 1) & mask;
        }
    }

    void insert(u64 h, const u16* key, u16 len, u8 val) {
        if ((count + 1) * 10 >= table.size() * 7) {
            rehash();
        }
        size_t idx = h & mask;
        while (table[idx].offset != 0) {
            if (table[idx].hash == h && table[idx].len == len &&
                std::memcmp(&arena[table[idx].offset], key, len * sizeof(u16)) == 0) {
                return;
            }
            idx = (idx + 1) & mask;
        }
        u32 off = (u32)arena.size();
        arena.insert(arena.end(), key, key + len);
        table[idx] = Entry{h, off, len, val};
        ++count;
    }
};

struct LocalGraph {
    int k;
    u128 adj[MAXN];
    int deg[MAXN];
};

// 1-WL color refinement starting from color[] (modifies color[] in place, returns num_colors)
static int wl_refine(const LocalGraph& g, int* color) {
    int k = g.k;
    u64 sig[MAXN];
    std::pair<u64, int> order[MAXN];
    int ncolors = 0;

    // Initial normalize
    for (int i = 0; i < k; ++i) order[i] = {(u64)color[i], i};
    std::sort(order, order + k);
    int cur = -1;
    u64 prev = ~0ULL;
    for (int i = 0; i < k; ++i) {
        if (order[i].first != prev) { ++cur; prev = order[i].first; }
        color[order[i].second] = cur;
    }
    ncolors = cur + 1;
    if (ncolors == k) return k;

    for (int round = 0; round < k; ++round) {
        int nbc[MAXN];
        for (int u = 0; u < k; ++u) {
            int d = 0;
            u128 m = g.adj[u];
            while (m) {
                int v = ctz128(m);
                m &= m - 1;
                nbc[d++] = color[v];
            }
            std::sort(nbc, nbc + d);
            u64 h = splitmix64((u64)color[u] * 0x9e3779b97f4a7c15ULL + (u64)d);
            for (int j = 0; j < d; ++j) {
                h = splitmix64(h ^ ((u64)nbc[j] + 0x517cc1b727220a95ULL + (u64)j * 1315423911ULL));
            }
            sig[u] = h;
            order[u] = {h, u};
        }
        std::sort(order, order + k);
        int nc = -1;
        prev = ~0ULL;
        for (int i = 0; i < k; ++i) {
            if (order[i].first != prev) { ++nc; prev = order[i].first; }
            color[order[i].second] = nc;
        }
        if (nc + 1 == k) return k;
        if (nc + 1 <= ncolors) break;
        ncolors = nc + 1;
    }
    return ncolors;
}

struct CanonResult {
    u16 key[2 + MAXN * 4]; // max edges <= 2*MAXN for degree<=4, buffer generous
    u16 len;
    u64 hash;
};

static void build_key_from_perm(const LocalGraph& g, const int* inv_perm, u16* out_edges, int& out_m) {
    // inv_perm[old_u] = new_id in 0..k-1
    // perm[new_id] = old_u
    int perm[MAXN];
    for (int u = 0; u < g.k; ++u) perm[inv_perm[u]] = u;
    int m = 0;
    for (int nu = 0; nu < g.k; ++nu) {
        int u = perm[nu];
        u128 nb = g.adj[u];
        u16 local_nbs[MAXN];
        int cnt = 0;
        while (nb) {
            int v = ctz128(nb);
            nb &= nb - 1;
            int nv = inv_perm[v];
            if (nv > nu) local_nbs[cnt++] = (u16)nv;
        }
        std::sort(local_nbs, local_nbs + cnt);
        for (int j = 0; j < cnt; ++j) {
            out_edges[m++] = (u16)((nu << 8) | local_nbs[j]);
        }
    }
    out_m = m;
}

static void canon_dfs(const LocalGraph& g, int* color, int ncolors,
                      u16* best_edges, int& best_m, bool& has_best, int depth_limit) {
    int k = g.k;
    if (ncolors == k) {
        u16 edges[MAXN * 4];
        int m = 0;
        build_key_from_perm(g, color, edges, m);
        if (!has_best || std::lexicographical_compare(edges, edges + m, best_edges, best_edges + best_m)) {
            std::memcpy(best_edges, edges, m * sizeof(u16));
            best_m = m;
            has_best = true;
        }
        return;
    }

    // Find smallest non-singleton color class
    int counts[MAXN] = {0};
    for (int i = 0; i < k; ++i) counts[color[i]]++;
    int best_c = -1, best_sz = k + 1;
    for (int c = 0; c < ncolors; ++c) {
        if (counts[c] > 1 && counts[c] < best_sz) {
            best_sz = counts[c];
            best_c = c;
        }
    }

    int members[MAXN], nm = 0;
    for (int i = 0; i < k; ++i) {
        if (color[i] == best_c) members[nm++] = i;
    }

    // Cap branching at large symmetry depths to avoid factorial blowup on symmetric subgraphs
    int limit = (depth_limit > 0) ? nm : 1;
    for (int idx = 0; idx < limit; ++idx) {
        int u = members[idx];
        int next_color[MAXN];
        for (int i = 0; i < k; ++i) {
            if (i == u) next_color[i] = color[i] * 2;
            else if (color[i] == best_c) next_color[i] = color[i] * 2 + 1;
            else next_color[i] = color[i] * 2;
        }
        int nc = wl_refine(g, next_color);
        canon_dfs(g, next_color, nc, best_edges, best_m, has_best, depth_limit - 1);
    }
}

static void canonicalize(const LocalGraph& g, CanonResult& res) {
    int color[MAXN];
    for (int i = 0; i < g.k; ++i) color[i] = g.deg[i];
    int nc = wl_refine(g, color);

    u16 best_edges[MAXN * 4];
    int best_m = 0;
    bool has_best = false;
    canon_dfs(g, color, nc, best_edges, best_m, has_best, 6);

    res.key[0] = (u16)g.k;
    res.key[1] = (u16)best_m;
    std::memcpy(res.key + 2, best_edges, best_m * sizeof(u16));
    res.len = (u16)(2 + best_m);

    u64 h = splitmix64(((u64)g.k << 16) | (u64)best_m);
    for (int i = 0; i < best_m; ++i) {
        h = splitmix64(h ^ ((u64)best_edges[i] + (u64)i * 0x9e3779b97f4a7c15ULL));
    }
    res.hash = h;
}

struct Solver {
    int n_verts;
    u128 adj[MAXN];
    u128 closed_nb[MAXN];
    TransTable tt;
    u64 nodes = 0;
    u64 tt_hits = 0;
    u64 path_folds = 0;

    Solver(int n, const std::vector<u128>& a) : n_verts(n), tt(1ULL << 23) {
        for (int i = 0; i < n; ++i) {
            adj[i] = a[i];
            closed_nb[i] = a[i] | ((u128)1 << i);
        }
    }

    int solve_mask(u128 mask) {
        if (mask == 0) return 0;

        // Split into connected components
        u128 rem = mask;
        int total_xor = 0;
        while (rem) {
            u128 lsb = rem & (~rem + 1);
            u128 comp = 0;
            u128 stk = lsb;
            while (stk) {
                int v = ctz128(stk);
                u128 bit = (u128)1 << v;
                stk ^= bit;
                if (!(comp & bit)) {
                    comp |= bit;
                    stk |= (adj[v] & rem) & ~comp;
                }
            }
            rem ^= comp;
            total_xor ^= solve_connected(comp);
        }
        return total_xor;
    }

    int solve_connected(u128 comp) {
        int k = popcnt128(comp);
        if (k == 0) return 0;
        if (k <= 2) return 1;

        // Extract vertices and check path / cycle / true twins
        int verts[MAXN];
        int idx_of[MAXN];
        int cnt = 0;
        u128 tmp = comp;
        while (tmp) {
            int v = ctz128(tmp);
            tmp &= tmp - 1;
            idx_of[v] = cnt;
            verts[cnt++] = v;
        }

        int maxd = 0, d1 = 0, d2 = 0;
        LocalGraph lg;
        lg.k = k;
        for (int i = 0; i < k; ++i) {
            int v = verts[i];
            u128 nb = adj[v] & comp;
            int d = popcnt128(nb);
            lg.deg[i] = d;
            if (d > maxd) maxd = d;
            if (d == 1) ++d1;
            else if (d == 2) ++d2;
            u128 lm = 0;
            while (nb) {
                int u = ctz128(nb);
                nb &= nb - 1;
                lm |= ((u128)1 << idx_of[u]);
            }
            lg.adj[i] = lm;
        }

        if (maxd <= 2) {
            if (d1 == 2 && d1 + d2 == k) {
                ++path_folds;
                return path_nimber[k];
            }
            if (d2 == k) {
                ++path_folds;
                return (path_nimber[k - 3] == 0) ? 1 : 0;
            }
        }

        // True-twin collapse: if N[i] == N[j], delete j
        u128 keep = (((u128)1 << k) - 1);
        bool collapsed = false;
        for (int i = 0; i < k; ++i) {
            if (!(keep & ((u128)1 << i))) continue;
            u128 ci = lg.adj[i] | ((u128)1 << i);
            for (int j = i + 1; j < k; ++j) {
                if (!(keep & ((u128)1 << j))) continue;
                u128 cj = lg.adj[j] | ((u128)1 << j);
                if (ci == cj) {
                    keep ^= ((u128)1 << j);
                    collapsed = true;
                }
            }
        }
        if (collapsed) {
            u128 new_comp = 0;
            for (int i = 0; i < k; ++i) {
                if (keep & ((u128)1 << i)) new_comp |= ((u128)1 << verts[i]);
            }
            return solve_connected(new_comp);
        }

        CanonResult cr;
        canonicalize(lg, cr);
        int cached = tt.lookup(cr.hash, cr.key, cr.len);
        if (cached >= 0) {
            ++tt_hits;
            return cached;
        }

        ++nodes;
        // Order moves by descending degree in comp
        std::pair<int, int> moves[MAXN];
        for (int i = 0; i < k; ++i) {
            moves[i] = {-lg.deg[i], verts[i]};
        }
        std::sort(moves, moves + k);

        u64 seen = 0;
        for (int i = 0; i < k; ++i) {
            int v = moves[i].second;
            int g = solve_mask(comp & ~closed_nb[v]);
            if (g < 64) seen |= (1ULL << g);
        }
        int mex = 0;
        while (seen & (1ULL << mex)) ++mex;
        tt.insert(cr.hash, cr.key, cr.len, (u8)mex);
        return mex;
    }
};

static std::vector<u128> make_lattice(int m, int n) {
    std::vector<u128> adj(m * n, 0);
    for (int r = 0; r < m; ++r) {
        for (int c = 0; c < n; ++c) {
            int u = r * n + c;
            int dr[4] = {-1, 1, 0, 0};
            int dc[4] = {0, 0, -1, 1};
            for (int d = 0; d < 4; ++d) {
                int rr = r + dr[d], cc = c + dc[d];
                if (rr >= 0 && rr < m && cc >= 0 && cc < n) {
                    adj[u] |= ((u128)1 << (rr * n + cc));
                }
            }
        }
    }
    return adj;
}

static std::vector<u128> make_gp(int n, int k = 2) {
    std::vector<u128> adj(2 * n, 0);
    for (int i = 0; i < n; ++i) {
        int u = i, v = n + i;
        int un = (i + 1) % n, up = (i + n - 1) % n;
        int vn = n + (i + k) % n, vp = n + (i + n - k) % n;
        adj[u] |= ((u128)1 << un) | ((u128)1 << up) | ((u128)1 << v);
        adj[v] |= ((u128)1 << u) | ((u128)1 << vn) | ((u128)1 << vp);
    }
    return adj;
}

int main(int argc, char** argv) {
    init_paths();
    std::string mode = (argc > 1) ? argv[1] : "calibrate";

    if (mode == "calibrate") {
        std::cout << "A316632 (3 x n, n=1..17):\n";
        for (int n = 1; n <= 17; ++n) {
            auto t0 = std::chrono::steady_clock::now();
            auto adj = make_lattice(3, n);
            Solver s(3 * n, adj);
            // Use D2 root symmetry for L_{3 x n}
            u128 all = (3 * n == 128) ? ~((u128)0) : (((u128)1 << (3 * n)) - 1);
            u64 seen = 0;
            for (int r = 0; r <= 1; ++r) {
                for (int c = 0; c < (n + 1) / 2; ++c) {
                    int v = r * n + c;
                    int g = s.solve_mask(all & ~s.closed_nb[v]);
                    if (g < 64) seen |= (1ULL << g);
                }
            }
            int mex = 0;
            while (seen & (1ULL << mex)) ++mex;
            double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
            std::cout << "  n=" << n << " G=" << mex << " (" << ms << " ms, nodes=" << s.nodes << ", tt=" << s.tt.count << ")\n" << std::flush;
        }

        std::cout << "A316533 (GP(n,2), odd n=5..25):\n";
        for (int n = 5; n <= 25; n += 2) {
            auto t0 = std::chrono::steady_clock::now();
            auto adj = make_gp(n, 2);
            Solver s(2 * n, adj);
            u128 all = (((u128)1 << (2 * n)) - 1);
            int g0 = s.solve_mask(all & ~s.closed_nb[0]);
            int g1 = s.solve_mask(all & ~s.closed_nb[n]);
            int mex = 0;
            while (mex == g0 || mex == g1) ++mex;
            double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
            std::cout << "  n=" << n << " G=" << mex << " (g_u=" << g0 << ", g_v=" << g1 << ", " << ms << " ms, nodes=" << s.nodes << ", tt=" << s.tt.count << ")\n" << std::flush;
        }

        std::cout << "Table 1 shaded L_{5x5}, L_{5x6}, L_{5x7}:\n";
        for (auto [m, n] : std::vector<std::pair<int,int>>{{5,5}, {5,6}, {5,7}}) {
            auto t0 = std::chrono::steady_clock::now();
            auto adj = make_lattice(m, n);
            Solver s(m * n, adj);
            u128 all = (((u128)1 << (m * n)) - 1);
            u64 seen = 0;
            for (int r = 0; r < (m + 1) / 2; ++r) {
                for (int c = 0; c < (n + 1) / 2; ++c) {
                    int v = r * n + c;
                    int g = s.solve_mask(all & ~s.closed_nb[v]);
                    if (g < 64) seen |= (1ULL << g);
                }
            }
            int mex = 0;
            while (seen & (1ULL << mex)) ++mex;
            double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
            std::cout << "  L_{" << m << "x" << n << "} G=" << mex << " (" << ms << " ms, nodes=" << s.nodes << ", tt=" << s.tt.count << ")\n" << std::flush;
        }
    } else if (mode == "grid" && argc == 4) {
        int m = std::stoi(argv[2]), n = std::stoi(argv[3]);
        if (m <= 0 || n <= 0 || m * n > MAXN) {
            std::cerr << "Invalid grid dimensions\n";
            return 1;
        }
        auto t0 = std::chrono::steady_clock::now();
        auto adj = make_lattice(m, n);
        Solver s(m * n, adj);
        u128 all = (m * n == 128) ? ~((u128)0) : (((u128)1 << (m * n)) - 1);
        u64 seen = 0;
        for (int r = 0; r < (m + 1) / 2; ++r) {
            for (int c = 0; c < (n + 1) / 2; ++c) {
                int v = r * n + c;
                int g = s.solve_mask(all & ~s.closed_nb[v]);
                if (g < 64) seen |= (1ULL << g);
            }
        }
        int mex = 0;
        while (seen & (1ULL << mex)) ++mex;
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "L_{" << m << "x" << n << "} G=" << mex << " (" << ms << " ms, nodes=" << s.nodes << ", tt=" << s.tt.count << ")\n";
    } else if (mode == "gp" && argc == 3) {
        int n = std::stoi(argv[2]);
        if (n < 5 || 2 * n > MAXN) {
            std::cerr << "Invalid GP(n,2) parameter\n";
            return 1;
        }
        auto t0 = std::chrono::steady_clock::now();
        auto adj = make_gp(n, 2);
        Solver s(2 * n, adj);
        u128 all = (2 * n == 128) ? ~((u128)0) : (((u128)1 << (2 * n)) - 1);
        int g0 = s.solve_mask(all & ~s.closed_nb[0]);
        int g1 = s.solve_mask(all & ~s.closed_nb[n]);
        int mex = 0;
        while (mex == g0 || mex == g1) ++mex;
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "GP(" << n << ",2) G=" << mex << " (g_u=" << g0 << ", g_v=" << g1 << ", " << ms << " ms, nodes=" << s.nodes << ", tt=" << s.tt.count << ")\n";
    }
    return 0;
}
