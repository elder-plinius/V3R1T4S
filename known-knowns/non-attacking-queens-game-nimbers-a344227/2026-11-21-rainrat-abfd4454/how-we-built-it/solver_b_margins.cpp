// solver_b_margins.cpp — Lens 2 (retrograde-dag) INDEPENDENT solver for
// Central-Strike Refutation Margins on R_8, R_10, R_12, R_14, R_16
// and Planar Sprague-Grundy values A344227(0..16).
//
// Architectural distinctions from Solver A:
// 1. Precomputed Bottom-Up W0..W8 (32 MiB bitset for all 2^28 labeled graphs on k <= 8 vertices)
//    with 1-ply projection from k = 9..14 into W0..W8.
// 2. Embedded Odd-Subboard tau-Reflection Instant Leaf & Canonical Quotienting (H1):
//    For any subposition A contained in S = [0..n-2]^2 (zero border bits in row n-1 or col n-1),
//    checks if A is invariant under tau(r,c) = (n-2-r, n-2-c). Since N[c*] already deleted all
//    four self-mirroring lines of S, tau(A) == A immediately proves A is a P-position (Lemma 2)!
//    Furthermore, when A <= S, canonicalizes A under the 16-element dihedral group of S (or D4(S))
//    in addition to D4(Q_n)!
// 3. Exact 256-bit canonical board key stored in a collision-free open-addressed hash table
//    (40 bytes per slot: 32-byte Mask256 + 1-byte value), completely avoiding Zobrist fingerprint
//    approximation.
// 4. OpenMP parallel evaluation across the sigma-folded replies of R_n with a lock-striped
//    exact 256-bit transposition table.

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
#include <vector>

using u8  = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;

struct Board256 {
    u64 w[4];
    constexpr Board256() : w{0,0,0,0} {}
    constexpr Board256(u64 a, u64 b, u64 c, u64 d) : w{a,b,c,d} {}

    inline bool is_zero() const { return (w[0] | w[1] | w[2] | w[3]) == 0; }
    inline int count() const {
        return __builtin_popcountll(w[0]) + __builtin_popcountll(w[1]) +
               __builtin_popcountll(w[2]) + __builtin_popcountll(w[3]);
    }
    inline void set_bit(int i) { w[i >> 6] |= (1ULL << (i & 63)); }
    inline bool get_bit(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
    inline Board256 diff(const Board256& o) const {
        return Board256(w[0] & ~o.w[0], w[1] & ~o.w[1], w[2] & ~o.w[2], w[3] & ~o.w[3]);
    }
    inline bool intersects(const Board256& o) const {
        return ((w[0] & o.w[0]) | (w[1] & o.w[1]) | (w[2] & o.w[2]) | (w[3] & o.w[3])) != 0;
    }
    inline bool operator==(const Board256& o) const {
        return w[0] == o.w[0] && w[1] == o.w[1] && w[2] == o.w[2] && w[3] == o.w[3];
    }
    inline bool operator<(const Board256& o) const {
        for (int i = 3; i >= 0; --i) if (w[i] != o.w[i]) return w[i] < o.w[i];
        return false;
    }
};

// Bottom-up complete Node-Kayles table W0..W8 (all 2^28 graphs on <= 8 vertices, 32 MiB bitset)
struct BottomUpW8 {
    std::vector<u64> W[9]; // W[k] has 2^(k*(k-1)/2) bits packed in u64s
    u32 pair_bit[8][8];
    // For k = 1..8 and surviving mask `surv` in 0..(1<<k)-1:
    // pext_mask[k][surv] has 1s at the bit positions in the k-vertex code that correspond to
    // pairs (i, j) with 0 <= j < i < k such that BOTH i and j are in `surv`!
    // Wait: because our edge encoding orders pairs (i, j) lexicographically by (i, j) with j < i,
    // restricting to a subset `surv` preserves the relative order of all surviving pairs (i, j)!
    // That means `_pext_u32(code, pext_mask[k][surv])` extracts the exact induced subgraph code
    // of `surv` in ONE instruction!!
    u32 pext_proj[9][256];

    BottomUpW8() {
        int bit = 0;
        for (int i = 0; i < 8; ++i) {
            for (int j = 0; j < i; ++j) {
                pair_bit[i][j] = bit++;
                pair_bit[j][i] = pair_bit[i][j];
            }
        }
        for (int k = 0; k <= 8; ++k) {
            for (int surv = 0; surv < (1 << k); ++surv) {
                u32 pmask = 0;
                for (int i = 0; i < k; ++i) {
                    if (!((surv >> i) & 1)) continue;
                    for (int j = 0; j < i; ++j) {
                        if ((surv >> j) & 1) {
                            pmask |= (1u << pair_bit[i][j]);
                        }
                    }
                }
                pext_proj[k][surv] = pmask;
            }
        }

        W[0].assign(1, 0ULL); // 0 vertices -> loss (0)
        W[1].assign(1, 1ULL); // 1 vertex   -> win  (1)
        for (int k = 2; k <= 8; ++k) {
            int n_edges = k * (k - 1) / 2;
            size_t n_codes = 1ULL << n_edges;
            size_t n_words = (n_codes + 63) / 64;
            W[k].assign(n_words, 0ULL);

            // Parallel bottom-up build across codes
            #pragma omp parallel for schedule(static) if(k >= 7)
            for (size_t word_idx = 0; word_idx < n_words; ++word_idx) {
                size_t base_code = word_idx << 6;
                size_t lim = std::min(n_codes, base_code + 64);
                u64 word_val = 0ULL;
                for (size_t code = base_code; code < lim; ++code) {
                    u8 adj[8];
                    for (int i = 0; i < k; ++i) adj[i] = (1u << i);
                    for (int i = 1; i < k; ++i) {
                        for (int j = 0; j < i; ++j) {
                            if ((code >> pair_bit[i][j]) & 1ULL) {
                                adj[i] |= (1u << j);
                                adj[j] |= (1u << i);
                            }
                        }
                    }
                    bool win = false;
                    u8 full = (1u << k) - 1u;
                    for (int v = 0; v < k; ++v) {
                        u8 surv = full & ~adj[v];
                        int kp = __builtin_popcount(surv);
                        if (kp == 0) { win = true; break; }
                        if (kp == 1) continue;
                        u32 sub_code = _pext_u32(u32(code), pext_proj[k][surv]);
                        if (!((W[kp][sub_code >> 6] >> (sub_code & 63)) & 1ULL)) {
                            win = true;
                            break;
                        }
                    }
                    if (win) word_val |= (1ULL << (code - base_code));
                }
                W[k][word_idx] = word_val;
            }
        }
    }

    inline bool lookup_w8(int k, u32 code) const {
        return (W[k][code >> 6] >> (code & 63)) & 1ULL;
    }

    // Evaluate any local graph on k <= 16 vertices using W0..W8 as the base table!
    bool eval_local_with_w8(u32 alive, const u32* __restrict__ adj) const {
        int pc = __builtin_popcount(alive);
        if (pc == 0) return false;
        if (pc == 1) return true;
        if (pc == 2) {
            int u = __builtin_ctz(alive);
            return (alive & ~adj[u]) == 0;
        }
        if (pc <= 8) {
            // Pack the pc*(pc-1)/2 bit code using _pext_u32 on each surviving vertex row!
            u32 code = 0;
            int shift = 0;
            u32 m = alive;
            // First vertex i=0 has 0 lower bits
            int u0 = __builtin_ctz(m);
            m &= m - 1;
            u32 prefix_mask = (1u << u0);
            for (int i = 1; i < pc; ++i) {
                int ui = __builtin_ctz(m);
                m &= m - 1;
                code |= _pext_u32(adj[ui], prefix_mask) << shift;
                shift += i;
                prefix_mask |= (1u << ui);
            }
            return lookup_w8(pc, code);
        }

        // For 9 <= pc <= 16: try moves ordered by surviving popcount ascending;
        // children with rpc <= 8 jump directly into lookup_w8!
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
            if (!eval_local_with_w8(rem, adj)) return true;
        }
        return false;
    }

    inline bool eval_board_leaf(const Board256& avail, const Board256* __restrict__ nbhd, int pc) const {
        if (pc == 0) return false;
        if (pc == 1) return true;
        int verts[16], k = 0;
        for (int wi = 0; wi < 4; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                verts[k++] = base + __builtin_ctzll(x);
                x &= x - 1;
            }
        }
        if (k == 2) return nbhd[verts[0]].get_bit(verts[1]);
        u32 adj[16];
        for (int i = 0; i < k; ++i) {
            const Board256& att = nbhd[verts[i]];
            u32 mask = 0;
            int shift = 0;
            for (int wi = 0; wi < 4; ++wi) {
                u64 aw = avail.w[wi];
                if (aw) {
                    mask |= u32(_pext_u64(att.w[wi], aw)) << shift;
                    shift += __builtin_popcountll(aw);
                }
            }
            adj[i] = mask;
        }
        return eval_local_with_w8((1u << k) - 1u, adj);
    }
};

struct ExactBoardSlot {
    Board256 key;
    u8 val; // 0 = empty, 1 = P (loss), 2 = N (win)
};

struct RetrogradeMarginSolver {
    int n, N, dense_k;
    const BottomUpW8& w8;
    Board256 nbhd[256];
    Board256 border_mask;     // row n-1 or col n-1
    Board256 sub_self_mirror; // 4 central lines of S = [0..n-2]^2
    u32 sym_bit_word[8][256];
    u64 sym_bit_mask[8][256];
    u32 tau_bit_word[256];
    u64 tau_bit_mask[256];

    // Cross-reply killer moves published by prove-a-loss nodes
    std::atomic<int> shared_killers[256];

    std::vector<ExactBoardSlot> tt;
    size_t tt_mask;
    static constexpr size_t NUM_LOCKS = 65536;
    std::vector<std::atomic_flag> locks;
    std::atomic<u64> total_nodes{0};
    std::atomic<u64> total_hits{0};
    std::atomic<u64> total_tau_leaves{0};

    RetrogradeMarginSolver(int n_, const BottomUpW8& w8_, int dk_ = 14, size_t tt_pow2 = 24)
        : n(n_), N(n_ * n_), dense_k(dk_), w8(w8_), locks(NUM_LOCKS) {
        tt.assign(1ULL << tt_pow2, ExactBoardSlot{Board256(), 0});
        tt_mask = (1ULL << tt_pow2) - 1ULL;
        for (size_t i = 0; i < NUM_LOCKS; ++i) locks[i].clear();
        for (int i = 0; i < 256; ++i) shared_killers[i].store(-1, std::memory_order_relaxed);

        for (int r1 = 0; r1 < n; ++r1) {
            for (int c1 = 0; c1 < n; ++c1) {
                int u = r1 * n + c1;
                Board256 m;
                for (int r2 = 0; r2 < n; ++r2) {
                    for (int c2 = 0; c2 < n; ++c2) {
                        if (r1 == r2 || c1 == c2 || std::abs(r1 - r2) == std::abs(c1 - c2)) {
                            m.set_bit(r2 * n + c2);
                        }
                    }
                }
                nbhd[u] = m;
                if (r1 == n - 1 || c1 == n - 1) {
                    border_mask.set_bit(u);
                    tau_bit_word[u] = u >> 6;
                    tau_bit_mask[u] = 1ULL << (u & 63);
                } else {
                    int tr = (n - 2) - r1, tc = (n - 2) - c1;
                    int tu = tr * n + tc;
                    tau_bit_word[u] = tu >> 6;
                    tau_bit_mask[u] = 1ULL << (tu & 63);
                    int m_center = n / 2 - 1;
                    if (r1 == m_center || c1 == m_center || r1 == c1 || (r1 + c1 == n - 2)) {
                        sub_self_mirror.set_bit(u);
                    }
                }
                int nr = n - 1 - r1, nc = n - 1 - c1;
                int imgs[8] = {
                    r1 * n + c1, r1 * n + nc, nr * n + c1, nr * n + nc,
                    c1 * n + r1, c1 * n + nr, nc * n + r1, nc * n + nr
                };
                for (int s = 0; s < 8; ++s) {
                    sym_bit_word[s][u] = imgs[s] >> 6;
                    sym_bit_mask[s][u] = 1ULL << (imgs[s] & 63);
                }
            }
        }
    }

    // Compute exact lexicographically smallest 256-bit Board256 under D4 (and tau when inside S)
    inline Board256 canonicalize(const Board256& avail, bool& is_tau_p_leaf) const {
        is_tau_p_leaf = false;
        bool in_subboard = !avail.intersects(border_mask);
        Board256 imgs[8];
        imgs[0] = avail;
        Board256 tau_img;

        for (int wi = 0; wi < 4; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                imgs[1].w[sym_bit_word[1][u]] |= sym_bit_mask[1][u];
                imgs[2].w[sym_bit_word[2][u]] |= sym_bit_mask[2][u];
                imgs[3].w[sym_bit_word[3][u]] |= sym_bit_mask[3][u];
                imgs[4].w[sym_bit_word[4][u]] |= sym_bit_mask[4][u];
                imgs[5].w[sym_bit_word[5][u]] |= sym_bit_mask[5][u];
                imgs[6].w[sym_bit_word[6][u]] |= sym_bit_mask[6][u];
                imgs[7].w[sym_bit_word[7][u]] |= sym_bit_mask[7][u];
                if (in_subboard) {
                    tau_img.w[tau_bit_word[u]] |= tau_bit_mask[u];
                }
                x &= x - 1;
            }
        }

        if (in_subboard && (avail == tau_img) && !avail.intersects(sub_self_mirror)) {
            is_tau_p_leaf = true;
            return avail;
        }

        Board256 best = imgs[0];
        for (int s = 1; s < 8; ++s) {
            if (imgs[s] < best) best = imgs[s];
        }
        if (in_subboard && tau_img < best) {
            best = tau_img;
        }
        return best;
    }

    inline u64 hash_board(const Board256& b) const {
        u64 h = 0x9e3779b97f4a7c15ULL;
        for (int i = 0; i < 4; ++i) {
            u64 x = b.w[i];
            x ^= x >> 30;
            x *= 0xbf58476d1ce4e5b9ULL;
            x ^= x >> 27;
            h ^= x + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        }
        return h;
    }

    inline int tt_lookup(const Board256& ckey, u64 h) {
        size_t idx = h & tt_mask;
        size_t lock_id = idx & (NUM_LOCKS - 1);
        while (locks[lock_id].test_and_set(std::memory_order_acquire)) {}
        int res = 0;
        if (tt[idx].val != 0 && tt[idx].key == ckey) {
            res = tt[idx].val;
        }
        locks[lock_id].clear(std::memory_order_release);
        return res;
    }

    inline void tt_insert(const Board256& ckey, u64 h, bool win) {
        size_t idx = h & tt_mask;
        size_t lock_id = idx & (NUM_LOCKS - 1);
        while (locks[lock_id].test_and_set(std::memory_order_acquire)) {}
        tt[idx].key = ckey;
        tt[idx].val = win ? 2 : 1;
        locks[lock_id].clear(std::memory_order_release);
    }

    bool solve_node(const Board256& avail, int ply, u64& local_nodes, u64& local_hits, u64& local_tau) {
        ++local_nodes;
        int pc = avail.count();
        if (pc <= dense_k) {
            return w8.eval_board_leaf(avail, nbhd, pc);
        }

        bool is_tau_p = false;
        Board256 ckey = canonicalize(avail, is_tau_p);
        if (is_tau_p) {
            ++local_tau;
            return false; // Proven P-position by Lemma 2 / Theorem S1!
        }

        u64 h = hash_board(ckey);
        int hit = tt_lookup(ckey, h);
        if (hit != 0) {
            ++local_hits;
            return hit == 2;
        }

        // Check shared killer move at this ply first!
        int km = shared_killers[ply].load(std::memory_order_relaxed);
        if (km >= 0 && avail.get_bit(km)) {
            Board256 kch = avail.diff(nbhd[km]);
            int kcpc = kch.count();
            bool kwin = (kcpc <= dense_k)
                ? (++local_nodes, w8.eval_board_leaf(kch, nbhd, kcpc))
                : solve_node(kch, ply + 1, local_nodes, local_hits, local_tau);
            if (!kwin) {
                tt_insert(ckey, h, true);
                return true;
            }
        }

        struct ChildEntry {
            int u;
            int cpc;
            u64 chash;
            Board256 ckey;
            Board256 mask;
        };
        ChildEntry children[256];
        int n_ch = 0;

        for (int wi = 0; wi < 4; ++wi) {
            u64 x = avail.w[wi];
            int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x);
                x &= x - 1;
                if (u == km) continue;
                Board256 ch = avail.diff(nbhd[u]);
                int cpc = ch.count();
                if (cpc == 0) {
                    shared_killers[ply].store(u, std::memory_order_relaxed);
                    tt_insert(ckey, h, true);
                    return true;
                }
                children[n_ch++] = {u, cpc, 0ULL, Board256(), ch};
            }
        }

        std::sort(children, children + n_ch, [](const ChildEntry& a, const ChildEntry& b) {
            return a.cpc < b.cpc;
        });

        // First pass: evaluate dense leaves & check TT/tau for larger children (ETC)
        for (int i = 0; i < n_ch; ++i) {
            if (children[i].cpc <= dense_k) {
                ++local_nodes;
                if (!w8.eval_board_leaf(children[i].mask, nbhd, children[i].cpc)) {
                    shared_killers[ply].store(children[i].u, std::memory_order_relaxed);
                    tt_insert(ckey, h, true);
                    return true;
                }
            } else {
                bool ch_tau_p = false;
                children[i].ckey = canonicalize(children[i].mask, ch_tau_p);
                if (ch_tau_p) {
                    ++local_tau;
                    shared_killers[ply].store(children[i].u, std::memory_order_relaxed);
                    tt_insert(ckey, h, true);
                    return true;
                }
                children[i].chash = hash_board(children[i].ckey);
                int chit = tt_lookup(children[i].ckey, children[i].chash);
                if (chit == 1) {
                    ++local_hits;
                    shared_killers[ply].store(children[i].u, std::memory_order_relaxed);
                    tt_insert(ckey, h, true);
                    return true;
                }
                if (chit == 2) {
                    ++local_hits;
                    children[i].cpc = -1; // already known N-position, skip!
                }
            }
        }

        for (int i = 0; i < n_ch; ++i) {
            if (children[i].cpc <= dense_k) continue;
            bool dup = false;
            for (int j = 0; j < i; ++j) {
                if (children[j].cpc > dense_k && children[j].ckey == children[i].ckey) {
                    dup = true;
                    break;
                }
            }
            if (dup) continue;
            if (!solve_node(children[i].mask, ply + 1, local_nodes, local_hits, local_tau)) {
                shared_killers[ply].store(children[i].u, std::memory_order_relaxed);
                tt_insert(ckey, h, true);
                return true;
            }
        }

        tt_insert(ckey, h, false);
        return false;
    }

    void compute_refutation_margin(int& out_refuters, int& out_total, std::vector<int>& refuting_squares) {
        Board256 full;
        for (int i = 0; i < N; ++i) full.set_bit(i);
        int m = n / 2 - 1;
        int cstar = m * n + m;
        Board256 R_n = full.diff(nbhd[cstar]);
        out_total = R_n.count();

        // Fold replies by main-diagonal transpose sigma(r,c) = (c,r) which fixes c* = (m,m)!
        struct ReplyRep {
            int r, c, u, sym_u, weight;
        };
        std::vector<ReplyRep> reps;
        for (int r = 0; r < n; ++r) {
            for (int c = r; c < n; ++c) {
                int u = r * n + c;
                if (!R_n.get_bit(u)) continue;
                int su = c * n + r;
                reps.push_back({r, c, u, su, (r == c) ? 1 : 2});
            }
        }

        std::vector<int> rep_is_p(reps.size(), 0);
        #pragma omp parallel
        {
            u64 l_nodes = 0, l_hits = 0, l_tau = 0;
            #pragma omp for schedule(dynamic, 1)
            for (size_t idx = 0; idx < reps.size(); ++idx) {
                Board256 ch = R_n.diff(nbhd[reps[idx].u]);
                bool win = solve_node(ch, 0, l_nodes, l_hits, l_tau);
                if (!win) rep_is_p[idx] = 1;
            }
            total_nodes.fetch_add(l_nodes, std::memory_order_relaxed);
            total_hits.fetch_add(l_hits, std::memory_order_relaxed);
            total_tau_leaves.fetch_add(l_tau, std::memory_order_relaxed);
        }

        out_refuters = 0;
        refuting_squares.clear();
        for (size_t idx = 0; idx < reps.size(); ++idx) {
            if (rep_is_p[idx]) {
                out_refuters += reps[idx].weight;
                refuting_squares.push_back(reps[idx].u);
                if (reps[idx].weight == 2) {
                    refuting_squares.push_back(reps[idx].sym_u);
                }
            }
        }
        std::sort(refuting_squares.begin(), refuting_squares.end());
    }

    // Exact Grundy evaluation for small k <= 10 at heap-sum leaves
    int eval_local_grundy_b(u32 alive, const u32* __restrict__ adj, int* memo) const {
        if (alive == 0) return 0;
        if (memo[alive] >= 0) return memo[alive];
        int pc = __builtin_popcount(alive);
        if (pc == 1) return memo[alive] = 1;
        if (pc == 2) {
            int u = __builtin_ctz(alive);
            return memo[alive] = ((alive & ~adj[u]) == 0 ? 1 : 0);
        }
        u32 seen = 0, m = alive;
        while (m) {
            int u = __builtin_ctz(m); m &= m - 1;
            int g = eval_local_grundy_b(alive & ~adj[u], adj, memo);
            seen |= (1u << g);
        }
        return memo[alive] = __builtin_ctz(~seen);
    }

    bool solve_heap_node(const Board256& avail, int h, int ply, u64& local_nodes, u64& local_hits, u64& local_tau) {
        if (h == 0) return solve_node(avail, ply, local_nodes, local_hits, local_tau);
        ++local_nodes;
        int pc = avail.count();
        if (pc == 0) return h > 0;
        if (pc == 1) return (1 ^ h) != 0;
        if (pc <= 10) {
            int verts[10], k = 0;
            for (int wi = 0; wi < 4; ++wi) {
                u64 x = avail.w[wi]; int base = wi << 6;
                while (x) { verts[k++] = base + __builtin_ctzll(x); x &= x - 1; }
            }
            u32 adj[10];
            for (int i = 0; i < k; ++i) {
                const Board256& att = nbhd[verts[i]];
                u32 mask = 0; int shift = 0;
                for (int wi = 0; wi < 4; ++wi) {
                    u64 aw = avail.w[wi];
                    if (aw) {
                        mask |= u32(_pext_u64(att.w[wi], aw)) << shift;
                        shift += __builtin_popcountll(aw);
                    }
                }
                adj[i] = mask;
            }
            int memo[1 << 10];
            std::fill_n(memo, 1 << k, -1);
            int g = eval_local_grundy_b((1u << k) - 1u, adj, memo);
            return (g ^ h) != 0;
        }

        bool is_tau_p = false;
        Board256 ckey = canonicalize(avail, is_tau_p);
        if (is_tau_p) {
            ++local_tau;
            return h > 0; // G(avail) == 0 -> G(avail + Nim(h)) = h > 0 (win)!
        }
        if (h == 1) {
            int hit0 = tt_lookup(ckey, hash_board(ckey));
            if (hit0 == 1) {
                ++local_hits;
                return true; // G(avail) == 0 -> avail + Nim(1) is win!
            }
        }
        // Encode heap h in top bits of ckey.w[3] (since n <= 16 uses bits 0..255, for n <= 15 bits 225..255 are 0!)
        Board256 hkey = ckey;
        hkey.w[3] ^= (u64(h) * 0x517cc1b727220a95ULL);
        u64 hash = hash_board(hkey);
        int hit = tt_lookup(hkey, hash);
        if (hit != 0) {
            ++local_hits;
            return hit == 2;
        }

        // First try heap reductions h -> hp < h (starting at hp = 0)
        for (int hp = 0; hp < h; ++hp) {
            if (!solve_heap_node(avail, hp, ply + 1, local_nodes, local_hits, local_tau)) {
                tt_insert(hkey, hash, true);
                return true;
            }
        }

        struct ChildEntry { int u, cpc; u64 chash; Board256 ckey, mask; };
        ChildEntry children[256];
        int n_ch = 0;
        for (int wi = 0; wi < 4; ++wi) {
            u64 x = avail.w[wi]; int base = wi << 6;
            while (x) {
                int u = base + __builtin_ctzll(x); x &= x - 1;
                Board256 ch = avail.diff(nbhd[u]);
                children[n_ch++] = {u, ch.count(), 0ULL, Board256(), ch};
            }
        }
        std::sort(children, children + n_ch, [](const ChildEntry& a, const ChildEntry& b) {
            return a.cpc < b.cpc;
        });

        for (int i = 0; i < n_ch; ++i) {
            if (children[i].cpc <= 10) {
                ++local_nodes;
                if (children[i].cpc == 0) {
                    if (h == 0) { tt_insert(hkey, hash, true); return true; }
                    continue;
                }
                if (children[i].cpc == 1) {
                    if ((1 ^ h) == 0) { tt_insert(hkey, hash, true); return true; }
                    continue;
                }
                int verts[10], k = 0;
                for (int wi = 0; wi < 4; ++wi) {
                    u64 x = children[i].mask.w[wi]; int base = wi << 6;
                    while (x) { verts[k++] = base + __builtin_ctzll(x); x &= x - 1; }
                }
                u32 adj[10];
                for (int a = 0; a < k; ++a) {
                    const Board256& att = nbhd[verts[a]];
                    u32 mask = 0; int shift = 0;
                    for (int wi = 0; wi < 4; ++wi) {
                        u64 aw = children[i].mask.w[wi];
                        if (aw) {
                            mask |= u32(_pext_u64(att.w[wi], aw)) << shift;
                            shift += __builtin_popcountll(aw);
                        }
                    }
                    adj[a] = mask;
                }
                int memo[1 << 10];
                std::fill_n(memo, 1 << k, -1);
                int g = eval_local_grundy_b((1u << k) - 1u, adj, memo);
                if ((g ^ h) == 0) {
                    tt_insert(hkey, hash, true);
                    return true;
                }
            } else {
                bool ch_tau_p = false;
                Board256 cb = canonicalize(children[i].mask, ch_tau_p);
                if (ch_tau_p) {
                    ++local_tau;
                    if (h == 0) { tt_insert(hkey, hash, true); return true; }
                    children[i].cpc = -1; // G(child)==0 -> child+Nim(h) is win -> skip!
                    continue;
                }
                Board256 chk = cb;
                chk.w[3] ^= (u64(h) * 0x517cc1b727220a95ULL);
                u64 chh = hash_board(chk);
                children[i].ckey = chk;
                children[i].chash = chh;
                int chit = tt_lookup(chk, chh);
                if (chit == 1) {
                    ++local_hits;
                    tt_insert(hkey, hash, true);
                    return true;
                }
                if (chit == 2) {
                    ++local_hits;
                    children[i].cpc = -1;
                } else if (h == 1) {
                    int hit0 = tt_lookup(cb, hash_board(cb));
                    if (hit0 == 1) {
                        ++local_hits;
                        children[i].cpc = -1; // G(child)==0 -> child+Nim(1) is win -> skip!
                    }
                }
            }
        }

        for (int i = 0; i < n_ch; ++i) {
            if (children[i].cpc <= 10) continue;
            bool dup = false;
            for (int j = 0; j < i; ++j) {
                if (children[j].cpc > 10 && children[j].ckey == children[i].ckey) { dup = true; break; }
            }
            if (dup) continue;
            if (h == 1 && children[i].cpc <= dense_k) {
                ++local_nodes;
                if (!w8.eval_board_leaf(children[i].mask, nbhd, children[i].cpc)) continue;
            }
            if (!solve_heap_node(children[i].mask, h, ply + 1, local_nodes, local_hits, local_tau)) {
                tt_insert(hkey, hash, true);
                return true;
            }
        }
        tt_insert(hkey, hash, false);
        return false;
    }

    int solve_planar_nimber_b() {
        if (n == 0) return 0;
        Board256 full;
        for (int i = 0; i < N; ++i) full.set_bit(i);

        // Unique D4 root children
        std::vector<Board256> root_children;
        for (int u = 0; u < N; ++u) {
            Board256 ch = full.diff(nbhd[u]);
            bool dummy = false;
            Board256 ckey = canonicalize(ch, dummy);
            bool seen = false;
            for (const auto& rc : root_children) if (rc == ckey) { seen = true; break; }
            if (!seen) root_children.push_back(ckey);
        }
        std::sort(root_children.begin(), root_children.end(), [](const Board256& a, const Board256& b) {
            return a.count() < b.count();
        });

        for (int k = 0; k <= n; ++k) {
            std::atomic<bool> found_win{false};
            #pragma omp parallel
            {
                u64 ln = 0, lh = 0, lt = 0;
                #pragma omp for schedule(dynamic, 1)
                for (size_t i = 0; i < root_children.size(); ++i) {
                    if (found_win.load(std::memory_order_relaxed)) continue;
                    if (!solve_heap_node(root_children[i], k, 1, ln, lh, lt)) {
                        found_win.store(true, std::memory_order_relaxed);
                    }
                }
                total_nodes.fetch_add(ln, std::memory_order_relaxed);
                total_hits.fetch_add(lh, std::memory_order_relaxed);
                total_tau_leaves.fetch_add(lt, std::memory_order_relaxed);
            }
            if (!found_win.load()) return k;
        }
        return -1;
    }
};

int main(int argc, char** argv) {
    int mode = (argc > 1) ? std::atoi(argv[1]) : 0; // 0 = all, 1 = margins, 2 = A344227
    auto t0 = std::chrono::steady_clock::now();
    BottomUpW8 w8;
    double dt_w8 = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("=== Solver B (retrograde-dag: Bottom-Up 32 MiB W0..W8 + Exact 256-bit Key + tau-Reflection Leaf) ===\n");
    std::printf("Built W0..W8 (2^28 graphs) bottom-up in %.3fs\n", dt_w8);
    std::fflush(stdout);

    if (mode == 0 || mode == 1) {
    for (int n : {8, 10, 12, 14, 16}) {
        auto ts = std::chrono::steady_clock::now();
        size_t pow2 = (n <= 12) ? 21 : (n == 14 ? 23 : 25); // 2^25 * 40B = 1.25 GiB for n=16
        int dk = (n <= 14) ? 14 : 15;
        RetrogradeMarginSolver solver(n, w8, dk, pow2);
        int ref = 0, tot = 0;
        std::vector<int> ref_sq;
        solver.compute_refutation_margin(ref, tot, ref_sq);
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("R_%2d margin = %3d/%3d  (%.3fs, nodes=%11llu, hits=%9llu, tau_leaves=%6llu)\n",
                    n, ref, tot, dt,
                    (unsigned long long)solver.total_nodes.load(),
                    (unsigned long long)solver.total_hits.load(),
                    (unsigned long long)solver.total_tau_leaves.load());
        if (ref > 0 && ref <= 20) {
            std::printf("  Refuting (winning for Player 2) replies in R_%d (%d squares):", n, ref);
            for (int u : ref_sq) std::printf(" (%d,%d)", u / n, u % n);
            std::printf("\n");
        } else if (ref > 0 && tot - ref <= 60) {
            std::printf("  Non-refuting (losing for Player 2) replies in R_%d (%d squares):", n, tot - ref);
            Board256 full;
            for (int i = 0; i < n * n; ++i) full.set_bit(i);
            int m = n / 2 - 1;
            Board256 R_n = full.diff(solver.nbhd[m * n + m]);
            for (int u = 0; u < n * n; ++u) {
                if (!R_n.get_bit(u)) continue;
                if (!std::binary_search(ref_sq.begin(), ref_sq.end(), u)) {
                    std::printf(" (%d,%d)", u / n, u % n);
                }
            }
            std::printf("\n");
        }
        // Also add planar A344227(n) calibration (n = 0..16) to Solver B!
        std::fflush(stdout);
    }
    }

    if (mode == 0 || mode == 2) {
    std::printf("\n--- Solver B Planar OEIS A344227(n) Calibration (n = 0..16) ---\n");
    int exp_a[17] = {0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0};
    for (int n = 0; n <= 16; ++n) {
        auto ts = std::chrono::steady_clock::now();
        if (n == 0) {
            std::printf("A344227( 0) = 0 (0.000s, nodes=0)\n");
            continue;
        }
        // For n <= 8, compute exact mex on Q_n directly or via heap-sum
        size_t pow2 = (n <= 12) ? 21 : (n <= 14 ? 23 : 25);
        int dk = (n <= 14) ? 14 : 15;
        RetrogradeMarginSolver solver(n, w8, dk, pow2);
        Board256 full;
        for (int i = 0; i < n * n; ++i) full.set_bit(i);

        int g = solver.solve_planar_nimber_b();
        double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
        std::printf("A344227(%2d) = %d (expected %d, %.3fs, nodes=%10llu, hits=%8llu)\n",
                    n, g, exp_a[n], dt,
                    (unsigned long long)solver.total_nodes.load(),
                    (unsigned long long)solver.total_hits.load());
        if (g != exp_a[n]) {
            std::printf("ERROR: A344227(%d) mismatch!\n", n);
            return 1;
        }
        std::fflush(stdout);
    }
    }
    return 0;
}
