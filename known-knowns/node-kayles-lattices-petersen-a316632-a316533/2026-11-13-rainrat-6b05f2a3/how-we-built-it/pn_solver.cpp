// Independent Algorithm 2: G + *k P/N Alpha-Beta Nimber Prover
// Uses geometric D_4 (grid) / D_n (GP(n,2)) canonicalization (no 1-WL)
// and short-circuiting P/N search with smallest-component-first XORing (no octal .137 table).

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>

using u128 = __uint128_t;
using u64 = uint64_t;
using u32 = uint32_t;
using u8 = uint8_t;

static inline int ctz128(u128 x) {
    u64 lo = (u64)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((u64)(x >> 64));
}

static inline int popcnt128(u128 x) {
    return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64));
}

static inline u64 hash128(u128 x) {
    u64 a = (u64)x;
    u64 b = (u64)(x >> 64);
    a += 0x9e3779b97f4a7c15ULL;
    a = (a ^ (a >> 30)) * 0xbf58476d1ce4e5b9ULL;
    b += 0x517cc1b727220a95ULL;
    b = (b ^ (b >> 27)) * 0x94d049bb133111ebULL;
    u64 h = a ^ b;
    h = (h ^ (h >> 31)) * 0x9e3779b97f4a7c15ULL;
    return h ^ (h >> 31);
}

struct PNEntry {
    u128 key;
    u64 not_mask; // bit k set => G(C) != k
    int8_t exact_g; // >= 0 if G(C) known, -1 otherwise
    uint8_t used;
};

struct PNTable {
    std::vector<PNEntry> tab;
    size_t mask;
    size_t count = 0;

    PNTable(size_t pow2 = (1ULL << 22)) {
        tab.assign(pow2, PNEntry{0, 0, -1, 0});
        mask = pow2 - 1;
    }

    void rehash() {
        size_t ns = tab.size() * 2;
        std::vector<PNEntry> nt(ns, PNEntry{0, 0, -1, 0});
        size_t nm = ns - 1;
        for (const auto& e : tab) {
            if (!e.used) continue;
            size_t idx = (size_t)hash128(e.key) & nm;
            while (nt[idx].used) idx = (idx + 1) & nm;
            nt[idx] = e;
        }
        tab.swap(nt);
        mask = nm;
    }

    PNEntry* find_or_insert(u128 key) {
        if ((count + 1) * 10 >= tab.size() * 7) rehash();
        size_t idx = (size_t)hash128(key) & mask;
        while (tab[idx].used) {
            if (tab[idx].key == key) return &tab[idx];
            idx = (idx + 1) & mask;
        }
        tab[idx] = PNEntry{key, 0, -1, 1};
        ++count;
        return &tab[idx];
    }

    const PNEntry* find(u128 key) const {
        size_t idx = (size_t)hash128(key) & mask;
        while (tab[idx].used) {
            if (tab[idx].key == key) return &tab[idx];
            idx = (idx + 1) & mask;
        }
        return nullptr;
    }
};

static constexpr int MAXN = 128;

struct PNSolver {
    bool is_grid;
    int M, N; // grid dimensions (or N for GP(N,2))
    int n_verts;
    u128 adj[MAXN];
    u128 closed_nb[MAXN];
    PNTable tt;
    u64 nodes = 0;

    PNSolver(int m, int n) : is_grid(true), M(m), N(n), n_verts(m * n), tt(1ULL << 22) {
        for (int r = 0; r < M; ++r) {
            for (int c = 0; c < N; ++c) {
                int u = r * N + c;
                u128 a = 0;
                if (r > 0) a |= ((u128)1 << ((r - 1) * N + c));
                if (r + 1 < M) a |= ((u128)1 << ((r + 1) * N + c));
                if (c > 0) a |= ((u128)1 << (r * N + (c - 1)));
                if (c + 1 < N) a |= ((u128)1 << (r * N + (c + 1)));
                adj[u] = a;
                closed_nb[u] = a | ((u128)1 << u);
            }
        }
    }

    PNSolver(int n) : is_grid(false), M(2), N(n), n_verts(2 * n), tt(1ULL << 22) {
        for (int i = 0; i < N; ++i) {
            int u = i, v = N + i;
            int un = (i + 1) % N, up = (i + N - 1) % N;
            int vn = N + (i + 2) % N, vp = N + (i + N - 2) % N;
            adj[u] = ((u128)1 << un) | ((u128)1 << up) | ((u128)1 << v);
            adj[v] = ((u128)1 << u) | ((u128)1 << vn) | ((u128)1 << vp);
            closed_nb[u] = adj[u] | ((u128)1 << u);
            closed_nb[v] = adj[v] | ((u128)1 << v);
        }
    }

    // Geometric canonicalization:
    // For grids: pack into tight bounding box in row-major width W = max(M, N) (or 11) and take min over D4.
    // Specifically, encode (h, w) in top bits or pack into a fixed stride S = 11 (since 11*11 = 121 < 128!).
    // Wait: for 3 x n with n <= 22, 3*22 = 66, so stride can be max(M, N) when we only compare within same (M,N) or fixed stride!
    // Even simpler: for grid, pack as (r * stride + c) where stride = 11 for Table 1 (<=10x10) or stride = N for 3 x n!
    // Wait: if we transpose in D4, h and w swap, so if max(h,w) <= 11 we use stride=11; if n > 11 (like 3xn), only use D2 (4 symmetries) with stride=N!
    u128 canon_comp(u128 comp) const {
        if (is_grid) {
            int min_r = M, max_r = -1, min_c = N, max_c = -1;
            int pts_r[MAXN], pts_c[MAXN], np = 0;
            u128 tmp = comp;
            while (tmp) {
                int v = ctz128(tmp);
                tmp &= tmp - 1;
                int r = v / N, c = v % N;
                pts_r[np] = r;
                pts_c[np] = c;
                ++np;
                if (r < min_r) min_r = r;
                if (r > max_r) max_r = r;
                if (c < min_c) min_c = c;
                if (c > max_c) max_c = c;
            }
            int h = max_r - min_r + 1;
            int w = max_c - min_c + 1;
            int stride = (M <= 11 && N <= 11) ? 11 : N;
            bool allow_transpose = (M <= 11 && N <= 11);
            u128 best = ~((u128)0);
            for (int sym = 0; sym < (allow_transpose ? 8 : 4); ++sym) {
                u128 m = 0;
                for (int i = 0; i < np; ++i) {
                    int r = pts_r[i] - min_r;
                    int c = pts_c[i] - min_c;
                    if (sym & 1) r = h - 1 - r;
                    if (sym & 2) c = w - 1 - c;
                    if (sym & 4) std::swap(r, c);
                    m |= ((u128)1 << (r * stride + c));
                }
                if (m < best) best = m;
            }
            return best;
        } else {
            // GP(N, 2): D_N symmetry (rotations + reflection)
            // Find minimal cyclic rotation/reflection of comp
            int us[MAXN], vs[MAXN], nu = 0, nv = 0;
            u128 tmp = comp;
            while (tmp) {
                int idx = ctz128(tmp);
                tmp &= tmp - 1;
                if (idx < N) us[nu++] = idx;
                else vs[nv++] = idx - N;
            }
            u128 best = ~((u128)0);
            for (int rev = 0; rev < 2; ++rev) {
                for (int shift = 0; shift < N; ++shift) {
                    u128 m = 0;
                    for (int i = 0; i < nu; ++i) {
                        int x = rev ? (N - 1 - us[i]) : us[i];
                        x = (x + shift) % N;
                        m |= ((u128)1 << x);
                    }
                    for (int i = 0; i < nv; ++i) {
                        int x = rev ? (N - 1 - vs[i]) : vs[i];
                        x = (x + shift) % N;
                        m |= ((u128)1 << (N + x));
                    }
                    if (m < best) best = m;
                }
            }
            return best;
        }
    }

    // Returns true iff G(comp) != k (i.e. comp + *k is N-position)
    bool is_N(u128 comp, int k) {
        int cnt = popcnt128(comp);
        if (cnt == 0) return (0 != k);
        if (cnt <= 2) return (1 != k);

        u128 ck = canon_comp(comp);
        if (const PNEntry* e = tt.find(ck)) {
            if (e->exact_g >= 0) return (e->exact_g != k);
            if (k < 64 && (e->not_mask & (1ULL << k))) return true;
        }

        // First ensure G(comp) != kp for all kp < k
        for (int kp = 0; kp < k; ++kp) {
            if (!is_N(comp, kp)) {
                // G(comp) == kp < k!
                PNEntry* e = tt.find_or_insert(ck);
                e->exact_g = (int8_t)kp;
                return true;
            }
        }

        ++nodes;
        // Collect moves ordered by descending degree in comp
        std::pair<int, int> moves[MAXN];
        int nm = 0;
        u128 tmp = comp;
        while (tmp) {
            int v = ctz128(tmp);
            tmp &= tmp - 1;
            int d = popcnt128(adj[v] & comp);
            moves[nm++] = {-d, v};
        }
        std::sort(moves, moves + nm);

        for (int i = 0; i < nm; ++i) {
            int v = moves[i].second;
            u128 nxt = comp & ~closed_nb[v];
            if (nxt == 0) {
                if (k == 0) {
                    PNEntry* e = tt.find_or_insert(ck);
                    if (k < 64) e->not_mask |= (1ULL << k);
                    return true;
                }
                continue;
            }

            // Split nxt into connected components
            u128 comps[MAXN];
            int sizes[MAXN];
            int nc = 0;
            u128 rem = nxt;
            while (rem) {
                u128 lsb = rem & (~rem + 1);
                u128 c = 0;
                u128 stk = lsb;
                while (stk) {
                    int u = ctz128(stk);
                    u128 bit = (u128)1 << u;
                    stk ^= bit;
                    if (!(c & bit)) {
                        c |= bit;
                        stk |= (adj[u] & rem) & ~c;
                    }
                }
                rem ^= c;
                comps[nc] = c;
                sizes[nc] = popcnt128(c);
                ++nc;
            }

            // Sort components by size ascending so we solve smallest first
            int order[MAXN];
            for (int j = 0; j < nc; ++j) order[j] = j;
            std::sort(order, order + nc, [&](int a, int b) { return sizes[a] < sizes[b]; });

            int s = 0;
            for (int j = 0; j < nc - 1; ++j) {
                s ^= nimber(comps[order[j]]);
            }
            if (!is_N(comps[order[nc - 1]], k ^ s)) {
                // Found winning move! G(nxt) == k
                PNEntry* e = tt.find_or_insert(ck);
                if (k < 64) e->not_mask |= (1ULL << k);
                return true;
            }
        }

        // No move had nimber k, and all kp < k failed => G(comp) == k
        PNEntry* e = tt.find_or_insert(ck);
        e->exact_g = (int8_t)k;
        return false;
    }

    int nimber(u128 comp) {
        if (comp == 0) return 0;
        if (popcnt128(comp) <= 2) return 1;
        u128 ck = canon_comp(comp);
        if (const PNEntry* e = tt.find(ck)) {
            if (e->exact_g >= 0) return e->exact_g;
        }
        int k = 0;
        while (is_N(comp, k)) ++k;
        return k;
    }
};

int main(int argc, char** argv) {
    std::string mode = (argc > 1) ? argv[1] : "calibrate";
    if (mode == "calibrate") {
        std::cout << "P/N Alpha-Beta Calibration:\n";
        std::cout << "A316632 (1..12): ";
        for (int n = 1; n <= 12; ++n) {
            PNSolver s(3, n);
            u128 all = (((u128)1 << (3 * n)) - 1);
            std::cout << s.nimber(all) << (n == 12 ? "\n" : ", ") << std::flush;
        }
        std::cout << "A316533 odd (5..17): ";
        for (int n = 5; n <= 17; n += 2) {
            PNSolver s(n);
            u128 all = (((u128)1 << (2 * n)) - 1);
            int g = 0;
            while (s.is_N(all, g)) ++g;
            std::cout << g << (n == 17 ? "\n" : ", ") << std::flush;
        }
        for (auto [m, n] : std::vector<std::pair<int,int>>{{5,5}, {5,6}, {5,7}}) {
            auto t0 = std::chrono::steady_clock::now();
            PNSolver s(m, n);
            u128 all = (((u128)1 << (m * n)) - 1);
            int g = s.nimber(all);
            double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
            std::cout << "L_{" << m << "x" << n << "} G=" << g << " (" << ms << " ms, nodes=" << s.nodes << ")\n" << std::flush;
        }
    } else if (mode == "grid" && argc == 4) {
        int m = std::stoi(argv[2]), n = std::stoi(argv[3]);
        if (m <= 0 || n <= 0 || m * n > MAXN) {
            std::cerr << "Invalid grid dimensions\n";
            return 1;
        }
        auto t0 = std::chrono::steady_clock::now();
        PNSolver s(m, n);
        u128 all = (m * n == 128) ? ~((u128)0) : (((u128)1 << (m * n)) - 1);
        int g = s.nimber(all);
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "L_{" << m << "x" << n << "} G=" << g << " (" << ms << " ms, nodes=" << s.nodes << ")\n";
    } else if (mode == "gp" && argc == 3) {
        int n = std::stoi(argv[2]);
        if (n < 5 || 2 * n > MAXN) {
            std::cerr << "Invalid GP(n,2) parameter\n";
            return 1;
        }
        auto t0 = std::chrono::steady_clock::now();
        PNSolver s(n);
        u128 all = (2 * n == 128) ? ~((u128)0) : (((u128)1 << (2 * n)) - 1);
        int g = 0;
        while (s.is_N(all, g)) ++g;
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "GP(" << n << ",2) G=" << g << " (" << ms << " ms, nodes=" << s.nodes << ")\n";
    }
    return 0;
}
