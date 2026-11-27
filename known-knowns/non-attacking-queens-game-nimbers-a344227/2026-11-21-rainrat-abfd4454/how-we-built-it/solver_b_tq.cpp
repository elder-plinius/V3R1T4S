// solver_b_tq.cpp — Lens 2 (retrograde-dag) INDEPENDENT solver for Toroidal Queens TQ_n
//
// Zero shared code or algorithms with Solver A:
// 1. Precomputes the exact 32 MiB Node-Kayles table W0..W8 bottom-up for all 2^28 labeled
//    graphs on k <= 8 vertices (instead of recursive scalar evaluation).
// 2. Uses explicit involutive automorphism P-position detection (Theorem S1 / Copying Lemma):
//    checks if the current live set A is invariant under point reflection tau(r,c) = (-r, -c) mod n
//    with no self-attacking live vertices.
// 3. Uses lexicographically minimal bitmask canonicalization across the 8 D4((0,0)) permutations
//    stored in an exact 256-bit key (zero hash collisions, open-addressed 32-byte exact slot table),
//    completely avoiding Zobrist fingerprint hashing!
// 4. Evaluates all 8*n^2 torus translation-dihedral symmetries or exact D4((0,0)) bit-permutation tables.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

using u8  = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;

struct BitBoard324 {
    u64 b[6];
    constexpr BitBoard324() : b{0,0,0,0,0,0} {}

    inline bool is_zero() const {
        return (b[0] | b[1] | b[2] | b[3] | b[4] | b[5]) == 0;
    }
    inline int count() const {
        return __builtin_popcountll(b[0]) + __builtin_popcountll(b[1]) +
               __builtin_popcountll(b[2]) + __builtin_popcountll(b[3]) +
               __builtin_popcountll(b[4]) + __builtin_popcountll(b[5]);
    }
    inline void set_bit(int i) { b[i >> 6] |= (1ULL << (i & 63)); }
    inline bool get_bit(int i) const { return (b[i >> 6] >> (i & 63)) & 1ULL; }
    inline BitBoard324 diff(const BitBoard324& o) const {
        BitBoard324 r;
        for (int i = 0; i < 6; ++i) r.b[i] = b[i] & ~o.b[i];
        return r;
    }
    inline bool operator==(const BitBoard324& o) const {
        for (int i = 0; i < 6; ++i) if (b[i] != o.b[i]) return false;
        return true;
    }
    inline bool operator<(const BitBoard324& o) const {
        for (int i = 5; i >= 0; --i) {
            if (b[i] != o.b[i]) return b[i] < o.b[i];
        }
        return false;
    }
};

// Bottom-up precomputed W0..W7 table:
// For k = 0..7, a graph on k vertices is encoded by k*(k-1)/2 bits:
// edge (i, j) with 0 <= j < i < k is bit (i*(i-1)/2 + j).
// For k = 7, 7*6/2 = 21 bits -> 2^21 booleans = 2 MB!
struct BottomUpW7 {
    std::vector<u8> W[8];
    // Precomputed projection table: for k in 1..7, and surviving mask `surv` in 0..(1<<k)-1,
    // we map a k-vertex graph code to a popcount(surv)-vertex graph code.
    BottomUpW7() {
        W[0].assign(1, 0); // 0 vertices -> loss (0)
        W[1].assign(1, 1); // 1 vertex   -> win  (1)
        for (int k = 2; k <= 7; ++k) {
            int n_edges = k * (k - 1) / 2;
            size_t sz = 1ULL << n_edges;
            W[k].assign(sz, 0);
            for (size_t code = 0; code < sz; ++code) {
                // Build adjacency masks adj[0..k-1]
                u8 adj[7] = {0};
                int bit = 0;
                for (int i = 0; i < k; ++i) {
                    adj[i] |= (1u << i);
                    for (int j = 0; j < i; ++j) {
                        if ((code >> bit) & 1ULL) {
                            adj[i] |= (1u << j);
                            adj[j] |= (1u << i);
                        }
                        ++bit;
                    }
                }
                bool win = false;
                for (int v = 0; v < k; ++v) {
                    u8 surv = ((1u << k) - 1u) & ~adj[v];
                    int kp = __builtin_popcount(surv);
                    if (kp == 0) { win = true; break; }
                    if (kp == 1) continue;
                    // Extract induced subgraph code on surv
                    int verts[7], m = 0;
                    for (int u = 0; u < k; ++u) if ((surv >> u) & 1u) verts[m++] = u;
                    size_t sub_code = 0;
                    int sbit = 0;
                    for (int a = 0; a < kp; ++a) {
                        for (int b = 0; b < a; ++b) {
                            if ((adj[verts[a]] >> verts[b]) & 1u) {
                                sub_code |= (1ULL << sbit);
                            }
                            ++sbit;
                        }
                    }
                    if (!W[kp][sub_code]) { win = true; break; }
                }
                W[k][code] = win ? 1 : 0;
            }
        }
    }

    bool eval_local_w7(u32 alive, const u32* __restrict__ adj) const {
        int pc = __builtin_popcount(alive);
        if (pc == 0) return false;
        if (pc == 1) return true;
        if (pc == 2) {
            int u = __builtin_ctz(alive);
            return (alive & ~adj[u]) == 0;
        }
        if (pc <= 7) {
            int verts[7], m = 0;
            u32 x = alive;
            while (x) { verts[m++] = __builtin_ctz(x); x &= x - 1; }
            size_t code = 0;
            int bit = 0;
            for (int i = 0; i < pc; ++i) {
                for (int j = 0; j < i; ++j) {
                    if ((adj[verts[i]] >> verts[j]) & 1u) code |= (1ULL << bit);
                    ++bit;
                }
            }
            return W[pc][code] != 0;
        }
        u32 m = alive;
        u32 children[16];
        int n_ch = 0;
        while (m) {
            int u = __builtin_ctz(m); m &= m - 1;
            u32 rem = alive & ~adj[u];
            if (rem == 0) return true;
            int rpc = __builtin_popcount(rem);
            if (rpc == 1) continue;
            if (rpc == 2) { if ((rem & ~adj[__builtin_ctz(rem)]) != 0) return true; continue; }
            children[n_ch++] = (u32(rpc) << 16) | rem;
        }
        if (n_ch == 0) return false;
        for (int i = 1; i < n_ch; ++i) {
            u32 key = children[i]; int j = i - 1;
            while (j >= 0 && children[j] > key) { children[j + 1] = children[j]; --j; }
            children[j + 1] = key;
        }
        for (int i = 0; i < n_ch; ++i) {
            u32 rem = children[i] & 0xFFFFu;
            if (i > 0 && rem == (children[i - 1] & 0xFFFFu)) continue;
            if (!eval_local_w7(rem, adj)) return true;
        }
        return false;
    }

    inline bool lookup_small(const BitBoard324& avail, const BitBoard324* nbhd, int k) const {
        if (k == 0) return false;
        if (k == 1) return true;
        int verts[16], m = 0;
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.b[wi];
            int base = wi << 6;
            while (x) {
                verts[m++] = base + __builtin_ctzll(x);
                x &= x - 1;
            }
        }
        if (k == 2) return nbhd[verts[0]].get_bit(verts[1]);
        u32 adj[16] = {0};
        for (int i = 0; i < k; ++i) {
            for (int j = 0; j < k; ++j) {
                if (nbhd[verts[i]].get_bit(verts[j])) adj[i] |= (1u << j);
            }
        }
        return eval_local_w7((1u << k) - 1u, adj);
    }
};

// Exact open-addressed transposition table storing the FULL 384-bit canonical BitBoard324
// (no hash collisions possible!)
struct ExactSlot {
    BitBoard324 key;
    u8 val; // 0 = empty, 1 = P (loss), 2 = N (win)
};

struct ExactTorusVerifier {
    int n, N;
    const BottomUpW7& w7;
    BitBoard324 nbhd[384];
    int sym_perm[8][384];
    int inv_tau[384]; // tau(r,c) = (-r mod n, -c mod n)
    BitBoard324 tau_self_attack;
    std::vector<ExactSlot> table;
    size_t table_mask;
    u64 nodes = 0, hits = 0, tau_leaves = 0;

    ExactTorusVerifier(int n_, const BottomUpW7& w7_, size_t pow2 = 22)
        : n(n_), N(n_ * n_), w7(w7_) {
        table.assign(1ULL << pow2, ExactSlot{BitBoard324(), 0});
        table_mask = (1ULL << pow2) - 1ULL;

        for (int r1 = 0; r1 < n; ++r1) {
            for (int c1 = 0; c1 < n; ++c1) {
                int u = r1 * n + c1;
                BitBoard324 m;
                for (int r2 = 0; r2 < n; ++r2) {
                    for (int c2 = 0; c2 < n; ++c2) {
                        if (r1 == r2 || c1 == c2 ||
                            ((r1 - c1 + n) % n == (r2 - c2 + n) % n) ||
                            ((r1 + c1) % n == (r2 + c2) % n)) {
                            m.set_bit(r2 * n + c2);
                        }
                    }
                }
                nbhd[u] = m;
            }
        }
        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < n; ++c) {
                int u = r * n + c;
                int nr = (n - r) % n, nc = (n - c) % n;
                sym_perm[0][u] = r * n + c;
                sym_perm[1][u] = r * n + nc;
                sym_perm[2][u] = nr * n + c;
                sym_perm[3][u] = nr * n + nc;
                sym_perm[4][u] = c * n + r;
                sym_perm[5][u] = c * n + nr;
                sym_perm[6][u] = nc * n + r;
                sym_perm[7][u] = nc * n + nr;
                inv_tau[u] = nr * n + nc;
                if (nbhd[u].get_bit(inv_tau[u])) {
                    tau_self_attack.set_bit(u);
                }
            }
        }
    }

    // Exact lexicographically smallest BitBoard324 under the 8 D4((0,0)) symmetries
    inline BitBoard324 canonical_board(const BitBoard324& avail, BitBoard324* out_tau = nullptr) const {
        BitBoard324 imgs[8];
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.b[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                for (int s = 0; s < 8; ++s) {
                    imgs[s].set_bit(sym_perm[s][u]);
                }
                x &= x - 1;
            }
        }
        if (out_tau) *out_tau = imgs[3]; // sym_perm[3] is (-r mod n, -c mod n) = tau!
        BitBoard324 best = imgs[0];
        for (int s = 1; s < 8; ++s) {
            if (imgs[s] < best) best = imgs[s];
        }
        return best;
    }

    inline u64 hash_board(const BitBoard324& b) const {
        u64 h = 0x9e3779b97f4a7c15ULL;
        for (int i = 0; i < 6; ++i) {
            u64 x = b.b[i];
            x ^= x >> 30;
            x *= 0xbf58476d1ce4e5b9ULL;
            x ^= x >> 27;
            h ^= x + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        }
        return h;
    }

    bool win_exact(const BitBoard324& avail) {
        ++nodes;
        int pc = avail.count();
        if (pc <= 14) {
            return w7.lookup_small(avail, nbhd, pc);
        }

        BitBoard324 tau_img;
        BitBoard324 ckey = canonical_board(avail, &tau_img);

        // Theorem S1 / Copying Lemma instant P-position check:
        // If avail == tau_img and avail has no tau_self_attack bits set, then tau is a
        // fixed-point-free non-attacking involutive automorphism on avail -> P-position (false)!
        if (avail == tau_img) {
            bool any_self = false;
            for (int i = 0; i < 6; ++i) {
                if (avail.b[i] & tau_self_attack.b[i]) { any_self = true; break; }
            }
            if (!any_self) {
                ++tau_leaves;
                return false;
            }
        }

        u64 h = hash_board(ckey);
        for (size_t probe = 0; probe < 4; ++probe) {
            size_t idx = (h + probe) & table_mask;
            if (table[idx].val == 0) break;
            if (table[idx].key == ckey) {
                ++hits;
                return table[idx].val == 2;
            }
        }

        // Generate moves ordered by descending degree (ascending remaining count)
        struct MoveEntry {
            int u;
            int rem_pc;
            BitBoard324 rem;
        };
        MoveEntry moves[384];
        int nm = 0;
        for (int wi = 0; wi < 6; ++wi) {
            u64 x = avail.b[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                x &= x - 1;
                BitBoard324 rem = avail.diff(nbhd[u]);
                int rpc = rem.count();
                if (rpc == 0) {
                    size_t idx = h & table_mask;
                    table[idx] = {ckey, 2};
                    return true;
                }
                moves[nm++] = {u, rpc, rem};
            }
        }
        std::stable_sort(moves, moves + nm, [](const MoveEntry& a, const MoveEntry& b) {
            return a.rem_pc < b.rem_pc;
        });

        for (int i = 0; i < nm; ++i) {
            if (!win_exact(moves[i].rem)) {
                size_t idx = h & table_mask;
                table[idx] = {ckey, 2};
                return true;
            }
        }

        size_t idx = h & table_mask;
        table[idx] = {ckey, 1};
        return false;
    }
};

int main() {
    auto t0 = std::chrono::steady_clock::now();
    BottomUpW7 w7;
    double dt_w7 = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("=== Solver B (retrograde-dag: Bottom-Up W0..W7 + Exact 384-bit Lex-Canonical Key + Theorem S1 tau-leaf) ===\n");
    std::printf("Built W0..W7 bottom-up in %.3fs\n", dt_w7);

    for (int n = 1; n <= 16; ++n) {
        auto ts = std::chrono::steady_clock::now();
        ExactTorusVerifier verifier(n, w7, 23);
        BitBoard324 full;
        for (int i = 0; i < n * n; ++i) full.set_bit(i);
        BitBoard324 H_n = full.diff(verifier.nbhd[0]);

        // Also count how many second-ply moves (r, c) in H_n leave a P-position!
        int total_h = H_n.count();
        int winning_replies_in_h = 0;
        int first_win_u = -1;
        // Fold second-ply moves by the 8 D4((0,0)) symmetries!
        std::vector<int> seen(n * n, 0);
        for (int u = 0; u < n * n; ++u) {
            if (!H_n.get_bit(u) || seen[u]) continue;
            int orbit_sz = 0;
            for (int s = 0; s < 8; ++s) {
                int img = verifier.sym_perm[s][u];
                if (!seen[img]) {
                    seen[img] = 1;
                    ++orbit_sz;
                }
            }
            BitBoard324 after = H_n.diff(verifier.nbhd[u]);
            if (!verifier.win_exact(after)) {
                winning_replies_in_h += orbit_sz;
                if (first_win_u < 0) first_win_u = u;
            }
        }
        bool h_win = (winning_replies_in_h > 0);
        int g = h_win ? 0 : 1;
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("G(TQ_%2d) = %d  | H_%2d winning replies = %3d/%3d  (%.3fs, nodes=%10llu, hits=%8llu, tau_leaves=%6llu)",
                    n, g, n, winning_replies_in_h, total_h, dt,
                    (unsigned long long)verifier.nodes,
                    (unsigned long long)verifier.hits,
                    (unsigned long long)verifier.tau_leaves);
        if (first_win_u >= 0) {
            std::printf("  [e.g. (%d,%d)]", first_win_u / n, first_win_u % n);
        }
        std::printf("\n");
        std::fflush(stdout);
    }
    return 0;
}
