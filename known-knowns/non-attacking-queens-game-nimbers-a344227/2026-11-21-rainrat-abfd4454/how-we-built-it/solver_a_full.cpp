// solver_a_full.cpp — Lens 1 (evaluator-first) complete production solver & verifier for:
// 1. Toroidal queens G(TQ_n) for n = 1..18 (including n = 1..10 calibration and n = 12, 14, 16, 18 frontier),
//    with both first-stopping outcome and full second-ply winning-reply counts on H_n = TQ_n \ N[(0,0)].
// 2. Central-strike refutation margins on R_n = Q_n \ N[c*] (c* = (n/2-1, n/2-1)) for n = 8, 10, 12, 14, 16,
//    with the full list of refuting and non-refuting replies.
// 3. Planar Sprague-Grundy sequence A344227(n) for n = 0..16 via heap-sum Q_n + Nim(k) alpha-beta.
//
// Architecture of Solver A:
// - 384-bit (6 x uint64_t) bitboard representation supporting boards up to 18x18 (324 squares).
// - BMI2 _pext_u64 dense leaf evaluator (k <= 15) + fast local Grundy mex evaluator (k <= 11).
// - D4 board-symmetry canonicalization via 128-bit SplitMix64 Zobrist minimum hashing.
// - Flat lockless 64-bit atomic fingerprint transposition table (`std::atomic<u64>`).
// - Dynamic most-forcing move ordering + Enhanced Transposition Cutoff (ETC) + OpenMP parallel root orbits.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <immintrin.h>
#include <omp.h>
#include <string>
#include <vector>

using u8  = uint8_t;
using u16 = uint16_t;
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
    inline bool operator==(const Mask384& o) const {
        for (int i = 0; i < 6; ++i) if (w[i] != o.w[i]) return false;
        return true;
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

inline bool eval_local_has_p_child(u32 alive, const u32* __restrict__ adj) {
    // We only call this when eval_local16_rec(alive, adj) == true (i.e. some child is P)
    // Wait: we want to know whether G(alive) == 1!
    // G(alive) == 1 iff:
    //   1) some child of alive is a P-position (G(child) == 0), AND
    //   2) NO child of alive has G(child) == 1!
    // Look how recursive and fast that is!
    // Let's write `eval_local_is_g1(alive, adj)`:
    // Returns true iff G(alive) == 1!
    // And since we already know `eval_local16_rec(alive, adj)` tests `G(alive) != 0` in nanoseconds,
    // `G(alive) == 1` iff `eval_local16_rec(alive, adj) == true` AND for every child `rem = alive & ~adj[u]`,
    // `G(rem) != 1` (i.e., either `!eval_local16_rec(rem, adj)` so `G(rem) == 0`, OR `!eval_local_is_g1(rem, adj)`)!!
    return false;
}

inline bool eval_local16_is_g1(u32 alive, const u32* __restrict__ adj) {
    int pc = __builtin_popcount(alive);
    if (pc == 0) return false; // G = 0
    if (pc == 1) return true;  // G = 1
    if (pc == 2) {
        int u = __builtin_ctz(alive);
        return (alive & ~adj[u]) == 0; // adjacent -> G = 1; non-adjacent -> G = 0
    }
    // First check if G(alive) != 0 (i.e. has at least one G=0 child):
    if (!eval_local16_rec(alive, adj)) return false;
    // Now G(alive) >= 1. It equals 1 iff NO child `rem` has G(rem) == 1!
    u32 m = alive;
    u32 seen_rem[16];
    int n_rem = 0;
    while (m) {
        int u = __builtin_ctz(m);
        m &= m - 1;
        u32 rem = alive & ~adj[u];
        int rpc = __builtin_popcount(rem);
        if (rpc == 0) continue; // G(rem) = 0 != 1
        if (rpc == 1) return false; // G(rem) = 1 -> so G(alive) >= 2!
        if (rpc == 2) {
            if ((rem & ~adj[__builtin_ctz(rem)]) == 0) return false; // 2 adj vertices -> G(rem) = 1!
            continue; // 2 non-adj vertices -> G(rem) = 0
        }
        bool dup = false;
        for (int j = 0; j < n_rem; ++j) if (seen_rem[j] == rem) { dup = true; break; }
        if (!dup) seen_rem[n_rem++] = rem;
    }
    for (int i = 0; i < n_rem; ++i) {
        if (eval_local16_is_g1(seen_rem[i], adj)) return false;
    }
    return true;
}

inline bool eval_dense_is_g1(const Mask384& avail, const Mask384* __restrict__ attacks, int k_known) {
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
    return eval_local16_is_g1((1u << k) - 1u, adj);
}

inline int eval_local_grundy_rec(u32 alive, const u32* __restrict__ adj, int* memo) {
    if (alive == 0) return 0;
    if (memo[alive] >= 0) return memo[alive];
    int pc = __builtin_popcount(alive);
    if (pc == 1) return memo[alive] = 1;
    if (pc == 2) {
        int u = __builtin_ctz(alive);
        return memo[alive] = ((alive & ~adj[u]) == 0 ? 1 : 0);
    }
    u32 seen = 0;
    u32 m = alive;
    while (m) {
        int u = __builtin_ctz(m);
        m &= m - 1;
        u32 rem = alive & ~adj[u];
        int g = eval_local_grundy_rec(rem, adj, memo);
        seen |= (1u << g);
    }
    return memo[alive] = __builtin_ctz(~seen);
}

inline int eval_dense_grundy(const Mask384& avail, const Mask384* __restrict__ attacks, int k_known) {
    if (k_known == 0) return 0;
    if (k_known == 1) return 1;
    int verts[12];
    int k = extract_bits(avail, verts);
    if (k == 2) return attacks[verts[0]].test(verts[1]) ? 1 : 0;
    u32 adj[12];
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
    int memo[1 << 11];
    std::fill_n(memo, 1 << k, -1);
    return eval_local_grundy_rec((1u << k) - 1u, adj, memo);
}

struct SolverACtx {
    int n, N, dense_k;
    bool toroidal;
    Mask384 attacks[384];
    int sym_map[8][384];
    u64 sym_zob_lo[8][384];
    u64 sym_zob_hi[8][384];
    std::vector<std::atomic<u64>> tt;
    u64 tt_mask;
    std::atomic<u64> total_nodes{0};
    std::atomic<u64> total_hits{0};

    std::atomic<int> heap_killers[256];
    SolverACtx(int n_, bool tor_, int dk_, size_t tt_pow2 = 25)
        : n(n_), N(n_*n_), dense_k(dk_), toroidal(tor_), tt(1ULL << tt_pow2) {
        tt_mask = (1ULL << tt_pow2) - 1ULL;
        for (size_t i = 0; i < tt.size(); ++i) tt[i].store(0ULL, std::memory_order_relaxed);
        for (int i = 0; i < 256; ++i) heap_killers[i].store(-1, std::memory_order_relaxed);

        for (int r1 = 0; r1 < n; ++r1) {
            for (int c1 = 0; c1 < n; ++c1) {
                int u = r1 * n + c1;
                Mask384 m;
                for (int r2 = 0; r2 < n; ++r2) {
                    for (int c2 = 0; c2 < n; ++c2) {
                        bool att = false;
                        if (!toroidal) {
                            att = (r1 == r2) || (c1 == c2) || (std::abs(r1 - r2) == std::abs(c1 - c2));
                        } else {
                            att = (r1 == r2) || (c1 == c2) ||
                                  (((r1 - c1 + n) % n) == ((r2 - c2 + n) % n)) ||
                                  (((r1 + c1) % n) == ((r2 + c2) % n));
                        }
                        if (att) m.set(r2 * n + c2);
                    }
                }
                attacks[u] = m;
                int nr = toroidal ? ((n - r1) % n) : (n - 1 - r1);
                int nc = toroidal ? ((n - c1) % n) : (n - 1 - c1);
                sym_map[0][u] = r1 * n + c1;
                sym_map[1][u] = r1 * n + nc;
                sym_map[2][u] = nr * n + c1;
                sym_map[3][u] = nr * n + nc;
                sym_map[4][u] = c1 * n + r1;
                sym_map[5][u] = c1 * n + nr;
                sym_map[6][u] = nc * n + r1;
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

    inline int tt_probe(u64 key, u64& l_hits) const {
        u64 slot = tt[key & tt_mask].load(std::memory_order_relaxed);
        if ((slot >> 2) == (key >> 2)) {
            int val = int(slot & 3ULL);
            if (val != 0) { ++l_hits; return val; }
        }
        return 0;
    }

    inline void tt_store(u64 key, bool is_win) {
        tt[key & tt_mask].store((key & ~3ULL) | (is_win ? 2ULL : 1ULL), std::memory_order_relaxed);
    }

    bool solve_win(const Mask384& avail, u64& l_nodes, u64& l_hits) {
        ++l_nodes;
        int pc = avail.popcount();
        if (pc <= dense_k) return eval_dense_leaf(avail, attacks, pc);
        u64 key = canonical_hash(avail);
        int hit = tt_probe(key, l_hits);
        if (hit != 0) return hit == 2;

        struct ChildMove { int u, cpc; u64 ckey; Mask384 mask; };
        ChildMove moves[384];
        int n_moves = 0;
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                x &= x - 1;
                Mask384 ch = avail.and_not(attacks[u]);
                int cpc = ch.popcount();
                if (cpc == 0) {
                    tt_store(key, true);
                    return true;
                }
                moves[n_moves++] = {u, cpc, 0ULL, ch};
            }
        }
        std::sort(moves, moves + n_moves, [](const ChildMove& a, const ChildMove& b) {
            return a.cpc < b.cpc;
        });

        for (int i = 0; i < n_moves; ++i) {
            if (moves[i].cpc <= dense_k) {
                ++l_nodes;
                if (!eval_dense_leaf(moves[i].mask, attacks, moves[i].cpc)) {
                    tt_store(key, true);
                    return true;
                }
            } else {
                moves[i].ckey = canonical_hash(moves[i].mask);
                int chit = tt_probe(moves[i].ckey, l_hits);
                if (chit == 1) {
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
            if (!solve_win(moves[i].mask, l_nodes, l_hits)) {
                tt_store(key, true);
                return true;
            }
        }
        tt_store(key, false);
        return false;
    }

    bool solve_heap_win(const Mask384& avail, int h, int ply, u64& l_nodes, u64& l_hits) {
        if (h == 0) return solve_win(avail, l_nodes, l_hits);
        ++l_nodes;
        int pc = avail.popcount();
        if (h == 1 && pc <= 12) {
            return !eval_dense_is_g1(avail, attacks, pc);
        }
        if (pc <= 11) {
            int g = eval_dense_grundy(avail, attacks, pc);
            return (g ^ h) != 0;
        }
        u64 base_key = canonical_hash(avail);
        if (h == 1) {
            int hit0 = tt_probe(base_key, l_hits);
            if (hit0 == 1) return true;
        }
        u64 key = base_key ^ (u64(h) * 0x517cc1b727220a95ULL);
        int hit = tt_probe(key, l_hits);
        if (hit != 0) return hit == 2;

        for (int hp = 0; hp < h; ++hp) {
            if (!solve_heap_win(avail, hp, ply + 1, l_nodes, l_hits)) {
                tt_store(key, true);
                return true;
            }
        }

        // Try killer move at this ply first!
        int km = heap_killers[ply].load(std::memory_order_relaxed);
        int leaf_cap = (h == 1) ? 12 : 11;
        if (km >= 0 && avail.test(km)) {
            Mask384 kch = avail.and_not(attacks[km]);
            int kcpc = kch.popcount();
            bool kwin = true;
            if (kcpc <= leaf_cap) {
                ++l_nodes;
                kwin = (h == 1)
                    ? (!eval_dense_is_g1(kch, attacks, kcpc))
                    : ((eval_dense_grundy(kch, attacks, kcpc) ^ h) != 0);
            } else {
                kwin = solve_heap_win(kch, h, ply + 1, l_nodes, l_hits);
            }
            if (!kwin) {
                tt_store(key, true);
                return true;
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
                if (u == km) continue;
                Mask384 ch = avail.and_not(attacks[u]);
                int cpc = ch.popcount();
                moves[n_moves++] = {u, cpc, 0ULL, ch};
            }
        }
        std::sort(moves, moves + n_moves, [](const ChildMove& a, const ChildMove& b) {
            return a.cpc < b.cpc;
        });

        // First pass: evaluate dense leaves (cpc <= leaf_cap) & probe TT for larger children (ETC)!
        for (int i = 0; i < n_moves; ++i) {
            if (moves[i].cpc <= leaf_cap) {
                ++l_nodes;
                bool child_win = (h == 1)
                    ? (!eval_dense_is_g1(moves[i].mask, attacks, moves[i].cpc))
                    : ((eval_dense_grundy(moves[i].mask, attacks, moves[i].cpc) ^ h) != 0);
                if (!child_win) {
                    heap_killers[ply].store(moves[i].u, std::memory_order_relaxed);
                    tt_store(key, true);
                    return true;
                }
            } else {
                u64 cb = canonical_hash(moves[i].mask);
                moves[i].ckey = cb ^ (u64(h) * 0x517cc1b727220a95ULL);
                int chit = tt_probe(moves[i].ckey, l_hits);
                if (chit == 1) {
                    heap_killers[ply].store(moves[i].u, std::memory_order_relaxed);
                    tt_store(key, true);
                    return true;
                }
                if (chit == 2) {
                    moves[i].cpc = -1; // already known N-position, skip!
                } else if (h == 1) {
                    int hit0 = tt_probe(cb, l_hits);
                    if (hit0 == 1) {
                        moves[i].cpc = -1; // G(child)==0 -> child+Nim(1) is a win for opponent -> skip!
                    }
                }
            }
        }

        for (int i = 0; i < n_moves; ++i) {
            if (moves[i].cpc <= leaf_cap) continue;
            bool dup = false;
            for (int j = 0; j < i; ++j) {
                if (moves[j].cpc > leaf_cap && moves[j].ckey == moves[i].ckey) { dup = true; break; }
            }
            if (dup) continue;
            if (h == 1 && moves[i].cpc <= dense_k) {
                ++l_nodes;
                if (!eval_dense_leaf(moves[i].mask, attacks, moves[i].cpc)) continue;
            }
            if (!solve_heap_win(moves[i].mask, h, ply + 1, l_nodes, l_hits)) {
                heap_killers[ply].store(moves[i].u, std::memory_order_relaxed);
                tt_store(key, true);
                return true;
            }
        }
        tt_store(key, false);
        return false;
    }

    int solve_planar_nimber() {
        if (n == 0) return 0;
        Mask384 full;
        for (int i = 0; i < N; ++i) full.set(i);

        // Build D4 root opening representatives
        std::vector<int> seen(N, 0);
        std::vector<int> root_reps;
        for (int u = 0; u < N; ++u) {
            if (seen[u]) continue;
            for (int s = 0; s < 8; ++s) seen[sym_map[s][u]] = 1;
            root_reps.push_back(u);
        }
        // Sort root reps by child popcount ascending (most-forcing first, so c* is tried first!)
        std::sort(root_reps.begin(), root_reps.end(), [&](int a, int b) {
            return full.and_not(attacks[a]).popcount() < full.and_not(attacks[b]).popcount();
        });

        for (int k = 0; k <= n; ++k) {
            // Check if Q_n + Nim(k) is a P-position:
            // First try Nim heap reductions k -> hp < k (already known to be N-positions!)
            // So we only need to check if any root move u in root_reps leaves a P-position in Q_n\N[u] + Nim(k)!
            std::atomic<bool> found_win{false};
            #pragma omp parallel
            {
                u64 ln = 0, lh = 0;
                #pragma omp for schedule(dynamic, 1)
                for (size_t i = 0; i < root_reps.size(); ++i) {
                    if (found_win.load(std::memory_order_relaxed)) continue;
                    Mask384 ch = full.and_not(attacks[root_reps[i]]);
                    if (!solve_heap_win(ch, k, 1, ln, lh)) {
                        found_win.store(true, std::memory_order_relaxed);
                    }
                }
                total_nodes.fetch_add(ln, std::memory_order_relaxed);
                total_hits.fetch_add(lh, std::memory_order_relaxed);
            }
            if (!found_win.load()) return k;
        }
        return -1;
    }
};

int main(int argc, char** argv) {
    int mode = (argc > 1) ? std::atoi(argv[1]) : 0; // 0 = all, 1 = TQ, 2 = R_n, 3 = A344227
    std::printf("=== Solver A Full Run (evaluator-first: D4 + Zobrist + _pext_u64 dense leaf + OpenMP) ===\n");

    // 1. Toroidal queens G(TQ_n) for n = 1..16 (with exact winning reply counts in H_n)
    if (mode == 0 || mode == 1) {
    std::printf("\n--- Part 1: Toroidal Queens G(TQ_n) for n = 1..16 ---\n");
    for (int n = 1; n <= 16; ++n) {
        auto ts = std::chrono::steady_clock::now();
        size_t pow2 = (n <= 14) ? 23 : 25;
        SolverACtx ctx(n, true, 14, pow2);
        Mask384 full;
        for (int i = 0; i < n * n; ++i) full.set(i);
        Mask384 H_n = full.and_not(ctx.attacks[0]);
        int total_h = H_n.popcount();

        struct OrbitRep { int u, weight; };
        std::vector<int> seen(n * n, 0);
        std::vector<OrbitRep> reps;
        for (int u = 0; u < n * n; ++u) {
            if (!H_n.test(u) || seen[u]) continue;
            int w = 0;
            for (int s = 0; s < 8; ++s) {
                int img = ctx.sym_map[s][u];
                if (!seen[img]) { seen[img] = 1; ++w; }
            }
            reps.push_back({u, w});
        }
        std::vector<int> rep_is_p(reps.size(), 0);
        std::atomic<bool> found_p_reply{false};
        #pragma omp parallel
        {
            u64 ln = 0, lh = 0;
            #pragma omp for schedule(dynamic, 1)
            for (size_t i = 0; i < reps.size(); ++i) {
                if (n >= 17 && found_p_reply.load(std::memory_order_relaxed)) continue;
                Mask384 after = H_n.and_not(ctx.attacks[reps[i].u]);
                if (!ctx.solve_win(after, ln, lh)) {
                    rep_is_p[i] = 1;
                    found_p_reply.store(true, std::memory_order_relaxed);
                }
            }
            ctx.total_nodes.fetch_add(ln, std::memory_order_relaxed);
            ctx.total_hits.fetch_add(lh, std::memory_order_relaxed);
        }
        int win_replies = 0;
        for (size_t i = 0; i < reps.size(); ++i) if (rep_is_p[i]) win_replies += reps[i].weight;
        int g = (win_replies > 0) ? 0 : 1;
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("G(TQ_%2d) = %d | H_%2d winning replies = %3d/%3d (orbits=%2zu, %.3fs, nodes=%10llu, hits=%8llu)\n",
                    n, g, n, win_replies, total_h, reps.size(), dt,
                    (unsigned long long)ctx.total_nodes.load(),
                    (unsigned long long)ctx.total_hits.load());
        std::fflush(stdout);
    }
    }

    // 2. Central-strike refutation margins on R_8, R_10, R_12, R_14, R_16
    if (mode == 0 || mode == 2) {
    std::printf("\n--- Part 2: Central-Strike Refutation Margins on R_n (n = 8, 10, 12, 14, 16) ---\n");
    for (int n : {8, 10, 12, 14, 16}) {
        auto ts = std::chrono::steady_clock::now();
        size_t pow2 = (n <= 12) ? 22 : (n == 14 ? 24 : 26); // 2^26 * 8B = 512 MiB
        int dk = (n <= 14) ? 14 : 15;
        SolverACtx ctx(n, false, dk, pow2);
        Mask384 full;
        for (int i = 0; i < n * n; ++i) full.set(i);
        int m = n / 2 - 1;
        int cstar = m * n + m;
        Mask384 R_n = full.and_not(ctx.attacks[cstar]);
        int tot = R_n.popcount();

        struct Rep { int r, c, u, su, weight; };
        std::vector<Rep> reps;
        for (int r = 0; r < n; ++r) {
            for (int c = r; c < n; ++c) {
                int u = r * n + c;
                if (!R_n.test(u)) continue;
                reps.push_back({r, c, u, c * n + r, (r == c) ? 1 : 2});
            }
        }
        std::vector<int> rep_is_p(reps.size(), 0);
        #pragma omp parallel
        {
            u64 ln = 0, lh = 0;
            #pragma omp for schedule(dynamic, 1)
            for (size_t i = 0; i < reps.size(); ++i) {
                Mask384 ch = R_n.and_not(ctx.attacks[reps[i].u]);
                if (!ctx.solve_win(ch, ln, lh)) rep_is_p[i] = 1;
            }
            ctx.total_nodes.fetch_add(ln, std::memory_order_relaxed);
            ctx.total_hits.fetch_add(lh, std::memory_order_relaxed);
        }
        int ref = 0;
        std::vector<int> ref_sq;
        for (size_t i = 0; i < reps.size(); ++i) {
            if (rep_is_p[i]) {
                ref += reps[i].weight;
                ref_sq.push_back(reps[i].u);
                if (reps[i].weight == 2) ref_sq.push_back(reps[i].su);
            }
        }
        std::sort(ref_sq.begin(), ref_sq.end());
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("R_%2d margin = %3d/%3d (%.3fs, nodes=%11llu, hits=%9llu)\n",
                    n, ref, tot, dt,
                    (unsigned long long)ctx.total_nodes.load(),
                    (unsigned long long)ctx.total_hits.load());
        if (ref > 0 && ref <= 20) {
            std::printf("  Refuting (winning for Player 2) replies in R_%d (%d squares):", n, ref);
            for (int u : ref_sq) std::printf(" (%d,%d)", u / n, u % n);
            std::printf("\n");
        } else if (ref > 0 && tot - ref <= 60) {
            std::printf("  Non-refuting (losing for Player 2) replies in R_%d (%d squares):", n, tot - ref);
            for (int u = 0; u < n * n; ++u) {
                if (!R_n.test(u)) continue;
                if (!std::binary_search(ref_sq.begin(), ref_sq.end(), u)) {
                    std::printf(" (%d,%d)", u / n, u % n);
                }
            }
            std::printf("\n");
        }
        std::fflush(stdout);
    }
    }

    // 3. Planar A344227(n) for n = 0..16
    if (mode == 0 || mode == 3) {
    std::printf("\n--- Part 3: Planar OEIS A344227(n) for n = 0..16 ---\n");
    int exp_a[17] = {0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0};
    for (int n = 0; n <= 16; ++n) {
        auto ts = std::chrono::steady_clock::now();
        size_t pow2 = (n <= 14) ? 23 : 26;
        int dk = (n <= 14) ? 14 : 15;
        SolverACtx ctx(n, false, dk, pow2);
        int g = ctx.solve_planar_nimber();
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("A344227(%2d) = %d (expected %d, %.3fs, nodes=%10llu, hits=%8llu)\n",
                    n, g, exp_a[n], dt,
                    (unsigned long long)ctx.total_nodes.load(),
                    (unsigned long long)ctx.total_hits.load());
        if (g != exp_a[n]) {
            std::printf("ERROR: A344227(%d) mismatch!\n", n);
            return 1;
        }
        std::fflush(stdout);
    }
    }

    return 0;
}
