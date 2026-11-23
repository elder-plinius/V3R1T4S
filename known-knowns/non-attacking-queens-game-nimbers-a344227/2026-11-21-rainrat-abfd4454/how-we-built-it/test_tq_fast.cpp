// test_tq_fast.cpp — Probe G(TQ_1..16) with Solver A
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <immintrin.h>
#include <vector>

using u32 = uint32_t;
using u64 = uint64_t;

struct Mask384 {
    u64 w[6];
    constexpr Mask384() : w{0,0,0,0,0,0} {}
    inline bool empty() const { return (w[0]|w[1]|w[2]|w[3]|w[4]|w[5]) == 0; }
    inline int popcount() const {
        return __builtin_popcountll(w[0]) + __builtin_popcountll(w[1]) +
               __builtin_popcountll(w[2]) + __builtin_popcountll(w[3]) +
               __builtin_popcountll(w[4]) + __builtin_popcountll(w[5]);
    }
    inline void set(int idx) { w[idx >> 6] |= (1ULL << (idx & 63)); }
    inline bool test(int idx) const { return (w[idx >> 6] >> (idx & 63)) & 1ULL; }
    inline Mask384 and_not(const Mask384& o) const {
        Mask384 r;
        for (int i = 0; i < 6; ++i) r.w[i] = w[i] & ~o.w[i];
        return r;
    }
};

inline int extract_bits(const Mask384& m, int* out) {
    int cnt = 0;
    for (int wi = 0; wi < 6; ++wi) {
        u64 x = m.w[wi];
        int base = wi << 6;
        while (x) {
            out[cnt++] = base + __builtin_ctzll(x);
            x &= x - 1;
        }
    }
    return cnt;
}

inline bool eval_local16_rec(u32 alive, const u32* __restrict__ adj) {
    int pc = __builtin_popcount(alive);
    if (pc == 0) return false;
    if (pc == 1) return true;
    if (pc == 2) {
        int u = __builtin_ctz(alive);
        return (alive & ~adj[u]) == 0;
    }
    if (pc == 3) {
        u32 m = alive;
        int u0 = __builtin_ctz(m); m &= m - 1;
        u32 r0 = alive & ~adj[u0];
        if (r0 == 0 || (__builtin_popcount(r0) == 2 && (r0 & ~adj[__builtin_ctz(r0)]) != 0)) return true;
        int u1 = __builtin_ctz(m); m &= m - 1;
        u32 r1 = alive & ~adj[u1];
        if (r1 == 0 || (__builtin_popcount(r1) == 2 && (r1 & ~adj[__builtin_ctz(r1)]) != 0)) return true;
        int u2 = __builtin_ctz(m);
        u32 r2 = alive & ~adj[u2];
        if (r2 == 0 || (__builtin_popcount(r2) == 2 && (r2 & ~adj[__builtin_ctz(r2)]) != 0)) return true;
        return false;
    }
    u32 m = alive;
    u32 children[16];
    int n_ch = 0;
    while (m) {
        int u = __builtin_ctz(m);
        m &= m - 1;
        u32 rem = alive & ~adj[u];
        if (rem == 0) return true;
        int rpc = __builtin_popcount(rem);
        if (rpc == 1) continue;
        if (rpc == 2) {
            if ((rem & ~adj[__builtin_ctz(rem)]) != 0) return true;
            continue;
        }
        children[n_ch++] = (u32(rpc) << 16) | rem;
    }
    if (n_ch == 0) return false;
    for (int i = 1; i < n_ch; ++i) {
        u32 key = children[i];
        int j = i - 1;
        while (j >= 0 && children[j] > key) { children[j + 1] = children[j]; --j; }
        children[j + 1] = key;
    }
    for (int i = 0; i < n_ch; ++i) {
        u32 rem = children[i] & 0xFFFFu;
        if (i > 0 && rem == (children[i - 1] & 0xFFFFu)) continue;
        if (!eval_local16_rec(rem, adj)) return true;
    }
    return false;
}

inline bool eval_dense_leaf(const Mask384& avail, const Mask384* __restrict__ attacks, int k_known) {
    if (k_known == 0) return false;
    if (k_known == 1) return true;
    int verts[16];
    int k = extract_bits(avail, verts);
    if (k == 2) return attacks[verts[0]].test(verts[1]);
    u32 adj[16];
    for (int i = 0; i < k; ++i) {
        const Mask384& att = attacks[verts[i]];
        u32 mask = 0;
        int shift = 0;
        for (int wi = 0; wi < 6; ++wi) {
            u64 aw = avail.w[wi];
            if (aw) {
                mask |= u32(_pext_u64(att.w[wi], aw)) << shift;
                shift += __builtin_popcountll(aw);
            }
        }
        adj[i] = mask;
    }
    return eval_local16_rec((1u << k) - 1u, adj);
}

struct TorusSolver {
    int n, N, dense_k;
    Mask384 attacks[384];
    u64 sym_zob_lo[8][384];
    u64 sym_zob_hi[8][384];
    std::vector<u64> tt;
    u64 tt_mask;
    u64 nodes = 0, hits = 0;
    int killers[128][2];
    int best_second_move = -1;

    TorusSolver(int n_, int dk_, size_t tt_pow2 = 25) : n(n_), N(n_*n_), dense_k(dk_) {
        tt.assign(1ULL << tt_pow2, 0ULL);
        tt_mask = (1ULL << tt_pow2) - 1ULL;
        std::memset(killers, -1, sizeof(killers));
        for (int r1 = 0; r1 < n; ++r1) {
            for (int c1 = 0; c1 < n; ++c1) {
                int u = r1 * n + c1;
                Mask384 m;
                for (int r2 = 0; r2 < n; ++r2) {
                    for (int c2 = 0; c2 < n; ++c2) {
                        if (r1 == r2 || c1 == c2 ||
                            ((r1 - c1 + n) % n == (r2 - c2 + n) % n) ||
                            ((r1 + c1) % n == (r2 + c2) % n)) {
                            m.set(r2 * n + c2);
                        }
                    }
                }
                attacks[u] = m;
            }
        }
        int sym_map[8][384];
        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < n; ++c) {
                int u = r * n + c;
                int nr = (n - r) % n, nc = (n - c) % n;
                sym_map[0][u] = r * n + c;
                sym_map[1][u] = r * n + nc;
                sym_map[2][u] = nr * n + c;
                sym_map[3][u] = nr * n + nc;
                sym_map[4][u] = c * n + r;
                sym_map[5][u] = c * n + nr;
                sym_map[6][u] = nc * n + r;
                sym_map[7][u] = nc * n + nr;
            }
        }
        auto splitmix64 = [](u64& state) {
            u64 z = (state += 0x9e3779b97f4a7c15ULL);
            z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
            z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
            return z ^ (z >> 31);
        };
        u64 seed = 0x344227A344227ULL;
        u64 zlo[384], zhi[384];
        for (int u = 0; u < 384; ++u) {
            zlo[u] = splitmix64(seed);
            zhi[u] = splitmix64(seed);
        }
        for (int s = 0; s < 8; ++s) {
            for (int u = 0; u < N; ++u) {
                sym_zob_lo[s][u] = zlo[sym_map[s][u]];
                sym_zob_hi[s][u] = zhi[sym_map[s][u]];
            }
        }
    }

    inline u64 canonical_hash(const Mask384& avail) const {
        u64 h_lo[8] = {0}, h_hi[8] = {0};
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                for (int s = 0; s < 8; ++s) {
                    h_lo[s] ^= sym_zob_lo[s][u];
                    h_hi[s] ^= sym_zob_hi[s][u];
                }
                x &= x - 1;
            }
        }
        u64 best_hi = h_hi[0], best_lo = h_lo[0];
        for (int s = 1; s < 8; ++s) {
            if (h_hi[s] < best_hi || (h_hi[s] == best_hi && h_lo[s] < best_lo)) {
                best_hi = h_hi[s];
                best_lo = h_lo[s];
            }
        }
        u64 k = best_lo ^ (best_hi * 0x9e3779b97f4a7c15ULL);
        k ^= (k >> 30);
        k *= 0xbf58476d1ce4e5b9ULL;
        k ^= (k >> 27);
        return k;
    }

    inline int tt_probe(u64 key) {
        u64 slot = tt[key & tt_mask];
        if ((slot >> 2) == (key >> 2)) {
            int val = int(slot & 3ULL);
            if (val != 0) { ++hits; return val; }
        }
        return 0;
    }
    inline void tt_store(u64 key, bool is_win) {
        tt[key & tt_mask] = (key & ~3ULL) | (is_win ? 2ULL : 1ULL);
    }

    bool solve_win(const Mask384& avail, int ply = 0) {
        ++nodes;
        int pc = avail.popcount();
        if (pc <= dense_k) return eval_dense_leaf(avail, attacks, pc);
        u64 key = canonical_hash(avail);
        int hit = tt_probe(key);
        if (hit != 0) return hit == 2;

        for (int ki = 0; ki < 2; ++ki) {
            int km = killers[ply][ki];
            if (km >= 0 && avail.test(km)) {
                Mask384 ch = avail.and_not(attacks[km]);
                int cpc = ch.popcount();
                bool cwin = (cpc <= dense_k) ? (++nodes, eval_dense_leaf(ch, attacks, cpc)) : solve_win(ch, ply + 1);
                if (!cwin) {
                    if (ply == 0) best_second_move = km;
                    tt_store(key, true);
                    return true;
                }
            }
        }

        struct ChildMove { int u, cpc; u64 ckey; Mask384 mask; };
        ChildMove moves[384];
        int n_moves = 0;
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                x &= x - 1;
                if (u == killers[ply][0] || u == killers[ply][1]) continue;
                Mask384 ch = avail.and_not(attacks[u]);
                int cpc = ch.popcount();
                if (cpc == 0) {
                    if (ply == 0) best_second_move = u;
                    killers[ply][1] = killers[ply][0]; killers[ply][0] = u;
                    tt_store(key, true);
                    return true;
                }
                moves[n_moves++] = {u, cpc, 0ULL, ch};
            }
        }
        std::sort(moves, moves + n_moves, [](const ChildMove& a, const ChildMove& b) { return a.cpc < b.cpc; });

        for (int i = 0; i < n_moves; ++i) {
            if (moves[i].cpc <= dense_k) {
                ++nodes;
                if (!eval_dense_leaf(moves[i].mask, attacks, moves[i].cpc)) {
                    if (ply == 0) best_second_move = moves[i].u;
                    killers[ply][1] = killers[ply][0]; killers[ply][0] = moves[i].u;
                    tt_store(key, true);
                    return true;
                }
            } else {
                moves[i].ckey = canonical_hash(moves[i].mask);
                int chit = tt_probe(moves[i].ckey);
                if (chit == 1) {
                    if (ply == 0) best_second_move = moves[i].u;
                    killers[ply][1] = killers[ply][0]; killers[ply][0] = moves[i].u;
                    tt_store(key, true);
                    return true;
                }
                if (chit == 2) moves[i].cpc = -1;
            }
        }
        for (int i = 0; i < n_moves; ++i) {
            if (moves[i].cpc <= dense_k) continue;
            bool dup = false;
            for (int j = 0; j < i; ++j) {
                if (moves[j].ckey == moves[i].ckey && moves[j].cpc != 0) { dup = true; break; }
            }
            if (dup) continue;
            if (!solve_win(moves[i].mask, ply + 1)) {
                if (ply == 0) best_second_move = moves[i].u;
                killers[ply][1] = killers[ply][0]; killers[ply][0] = moves[i].u;
                tt_store(key, true);
                return true;
            }
        }
        tt_store(key, false);
        return false;
    }
};

int main() {
    for (int n = 1; n <= 18; ++n) {
        auto ts = std::chrono::steady_clock::now();
        TorusSolver solver(n, 14, 24);
        Mask384 full;
        for (int i = 0; i < n * n; ++i) full.set(i);
        Mask384 H_n = full.and_not(solver.attacks[0]);
        bool h_win = solver.solve_win(H_n, 0);
        int g = h_win ? 0 : 1;
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("G(TQ_%2d) = %d  (%.3fs, nodes=%10llu, hits=%8llu)",
                    n, g, dt, (unsigned long long)solver.nodes, (unsigned long long)solver.hits);
        if (h_win && solver.best_second_move >= 0) {
            std::printf("  [H_%d winning reply: (%d,%d)]", n, solver.best_second_move / n, solver.best_second_move % n);
        }
        std::printf("\n");
        std::fflush(stdout);
    }
    return 0;
}
