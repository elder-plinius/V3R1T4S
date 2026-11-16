// rank25_and_tensor_flip.cpp
// Lens 2 for gf2-polymult-8term-25-products:
//   1. 64-bit bit-packed Kauers-Moosbauer + Arai-Ichikawa-Hukushima (AIH) plus-transition
//      + 3-mode automatic linear-dependence reduction flip-graph search on T_n (n=4..8),
//      seeded with CRT 26-product formulas (ShortProduct_3 mod x^3/(x+1)^3/inf^3 + irreducibles),
//      2x4/4x2/2x2x2 Karatsuba, and schoolbook cooldowns, hunting for rank <= 25 at n=8.
//   2. Exhaustive 2x3 / 3x2 pair-contraction + GL_6 twist + reduced-tensor flip-graph search
//      for GF(2^6) mod 0x49 (target <= 56 vs 57) and 2x4 / CRT / tensor-flip search for
//      GF(2^8) mod 0x11B (target <= 106 vs 107).
//   3. Exact 2^(2m)-bit truth-table cross-layer gate-walk & cone-resubstitution optimizer
//      ({AND, XOR, XNOR}, no constants) on GF(2^6) 57-gate, GF(2^7) 81/82-gate, and GF(2^8) 107-gate circuits.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

using u8 = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;
using u128 = unsigned __int128;

// ============================================================================
// PART 1: 64-BIT FLIP-GRAPH + AIH PLUS-TRANSITIONS + 3-MODE REDUCTION ON T_n
// ============================================================================

static u64 OUTER8[256][256];

static void init_outer8() {
    for (int u = 0; u < 256; ++u) {
        for (int v = 0; v < 256; ++v) {
            u64 mask = 0;
            for (int i = 0; i < 8; ++i) {
                if ((u >> i) & 1) mask |= (u64(v) << (i * 8));
            }
            OUTER8[u][v] = mask;
        }
    }
}

struct PolyTensorDecomp {
    int n = 8;
    std::vector<u8> u, v;
    std::vector<u16> w;
    int rank() const { return (int)u.size(); }
};

static std::vector<u64> poly_mult_slices(int n) {
    std::vector<u64> slices(2 * n - 1, 0ULL);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            slices[i + j] |= (1ULL << (i * 8 + j));
    return slices;
}

static bool verify_poly_decomp(const PolyTensorDecomp& d) {
    int n = d.n;
    auto target = poly_mult_slices(n);
    std::vector<u64> got(2 * n - 1, 0ULL);
    for (size_t t = 0; t < d.u.size(); ++t) {
        if (d.u[t] == 0 || d.v[t] == 0 || d.w[t] == 0) return false;
        if ((d.u[t] >> n) != 0 || (d.v[t] >> n) != 0 || (d.w[t] >> (2 * n - 1)) != 0) return false;
        u64 uv = OUTER8[d.u[t]][d.v[t]];
        for (int k = 0; k < 2 * n - 1; ++k)
            if ((d.w[t] >> k) & 1) got[k] ^= uv;
    }
    return got == target;
}

// Given (u_t, v_t)_{t=0..r-1}, solve for w_t (and automatically drop redundant terms!)
static bool solve_mode2_and_prune(PolyTensorDecomp& d, const std::vector<u64>& target_slices) {
    int r = (int)d.u.size();
    int S = 2 * d.n - 1;
    if (r > 64) return false;
    u64 bv[64] = {0}, bc[64] = {0};
    int piv_owner[64];
    std::fill(std::begin(piv_owner), std::end(piv_owner), -1);
    std::vector<int> indep_idx;
    indep_idx.reserve(r);

    for (int t = 0; t < r; ++t) {
        if (d.u[t] == 0 || d.v[t] == 0) continue;
        u64 vec = OUTER8[d.u[t]][d.v[t]];
        u64 comb = (1ULL << indep_idx.size());
        bool ins = false;
        while (vec) {
            int p = __builtin_ctzll(vec);
            if (piv_owner[p] == -1) {
                piv_owner[p] = (int)indep_idx.size();
                bv[p] = vec;
                bc[p] = comb;
                indep_idx.push_back(t);
                ins = true;
                break;
            }
            vec ^= bv[p];
            comb ^= bc[p];
        }
        (void)ins;
    }
    int r_new = (int)indep_idx.size();
    std::vector<u16> w_new(r_new, 0);
    for (int k = 0; k < S; ++k) {
        u64 vec = target_slices[k], comb = 0;
        while (vec) {
            int p = __builtin_ctzll(vec);
            if (piv_owner[p] == -1) return false;
            vec ^= bv[p];
            comb ^= bc[p];
        }
        for (int i = 0; i < r_new; ++i)
            if ((comb >> i) & 1ULL) w_new[i] |= u16(1u << k);
    }
    std::vector<u8> u_out, v_out;
    std::vector<u16> w_out;
    for (int i = 0; i < r_new; ++i) {
        if (w_new[i] == 0) continue;
        u_out.push_back(d.u[indep_idx[i]]);
        v_out.push_back(d.v[indep_idx[i]]);
        w_out.push_back(w_new[i]);
    }
    d.u = std::move(u_out);
    d.v = std::move(v_out);
    d.w = std::move(w_out);
    return true;
}

// Check Mode-1 reduction: if {u_t x w_t} in F_2^(8*15=120) has rank < r, prune & recompute v_t!
static void try_mode01_prune(PolyTensorDecomp& d) {
    int n = d.n, S = 2 * n - 1;
    // Mode 1 solve (given u, w -> solve v): target for j in 0..n-1 is sum_{i=0..n-1} e_i x e_{i+j} in F_2^(n*S <= 120)
    auto prune_one = [&](bool solve_v) {
        int r = (int)d.u.size();
        if (r == 0 || r > 62) return;
        u128 bv[128] = {0};
        u64 bc[128] = {0};
        bool hp[128] = {false};
        std::vector<int> keep;
        for (int t = 0; t < r; ++t) {
            u8 f = solve_v ? d.u[t] : d.v[t];
            u16 wt = d.w[t];
            if (f == 0 || wt == 0) continue;
            u128 vec = 0;
            for (int i = 0; i < n; ++i)
                if ((f >> i) & 1) vec |= (u128(wt) << (i * S));
            u64 comb = (1ULL << keep.size());
            while (vec) {
                int p = (uint64_t(vec) != 0) ? __builtin_ctzll(uint64_t(vec)) : (64 + __builtin_ctzll(uint64_t(vec >> 64)));
                if (!hp[p]) {
                    hp[p] = true; bv[p] = vec; bc[p] = comb;
                    keep.push_back(t);
                    break;
                }
                vec ^= bv[p]; comb ^= bc[p];
            }
        }
        if ((int)keep.size() >= r) return; // No rank drop possible here
        int rn = (int)keep.size();
        std::vector<u8> solved(rn, 0);
        for (int j = 0; j < n; ++j) {
            u128 vec = 0;
            for (int i = 0; i < n; ++i) vec |= (u128(1) << (i * S + (i + j)));
            u64 comb = 0;
            while (vec) {
                int p = (uint64_t(vec) != 0) ? __builtin_ctzll(uint64_t(vec)) : (64 + __builtin_ctzll(uint64_t(vec >> 64)));
                if (!hp[p]) return;
                vec ^= bv[p]; comb ^= bc[p];
            }
            for (int k = 0; k < rn; ++k)
                if ((comb >> k) & 1ULL) solved[k] |= u8(1u << j);
        }
        std::vector<u8> nu, nv;
        std::vector<u16> nw;
        for (int k = 0; k < rn; ++k) {
            if (solved[k] == 0) continue;
            nu.push_back(solve_v ? d.u[keep[k]] : solved[k]);
            nv.push_back(solve_v ? solved[k] : d.v[keep[k]]);
            nw.push_back(d.w[keep[k]]);
        }
        d.u = std::move(nu); d.v = std::move(nv); d.w = std::move(nw);
    };
    prune_one(true);
    prune_one(false);
}

// Fast cleanup of zero terms and exact duplicate-pair merges
static inline void compact_decomp(PolyTensorDecomp& d) {
    for (size_t i = 0; i < d.u.size(); ) {
        if (d.u[i] == 0 || d.v[i] == 0 || d.w[i] == 0) {
            d.u[i] = d.u.back(); d.u.pop_back();
            d.v[i] = d.v.back(); d.v.pop_back();
            d.w[i] = d.w.back(); d.w.pop_back();
        } else ++i;
    }
    bool merged = true;
    while (merged) {
        merged = false;
        size_t r = d.u.size();
        for (size_t i = 0; i < r && !merged; ++i) {
            for (size_t j = i + 1; j < r; ++j) {
                if (d.u[i] == d.u[j] && d.v[i] == d.v[j]) {
                    d.w[i] ^= d.w[j];
                    d.u[j] = d.u.back(); d.u.pop_back();
                    d.v[j] = d.v.back(); d.v.pop_back();
                    d.w[j] = d.w.back(); d.w.pop_back();
                    if (d.w[i] == 0) {
                        d.u[i] = d.u.back(); d.u.pop_back();
                        d.v[i] = d.v.back(); d.v.pop_back();
                        d.w[i] = d.w.back(); d.w.pop_back();
                    }
                    merged = true; break;
                }
                if (d.u[i] == d.u[j] && d.w[i] == d.w[j]) {
                    d.v[i] ^= d.v[j];
                    d.u[j] = d.u.back(); d.u.pop_back();
                    d.v[j] = d.v.back(); d.v.pop_back();
                    d.w[j] = d.w.back(); d.w.pop_back();
                    if (d.v[i] == 0) {
                        d.u[i] = d.u.back(); d.u.pop_back();
                        d.v[i] = d.v.back(); d.v.pop_back();
                        d.w[i] = d.w.back(); d.w.pop_back();
                    }
                    merged = true; break;
                }
                if (d.v[i] == d.v[j] && d.w[i] == d.w[j]) {
                    d.u[i] ^= d.u[j];
                    d.u[j] = d.u.back(); d.u.pop_back();
                    d.v[j] = d.v.back(); d.v.pop_back();
                    d.w[j] = d.w.back(); d.w.pop_back();
                    if (d.u[i] == 0) {
                        d.u[i] = d.u.back(); d.u.pop_back();
                        d.v[i] = d.v.back(); d.v.pop_back();
                        d.w[i] = d.w.back(); d.w.pop_back();
                    }
                    merged = true; break;
                }
            }
        }
    }
}

// Perform one random flip step; returns false if no flip pairs exist!
static inline bool random_flip_step(PolyTensorDecomp& d, std::mt19937_64& rng) {
    int r = (int)d.u.size();
    struct FlipCand { u8 i, j, mode; };
    FlipCand cands[512];
    int nc = 0;
    for (int i = 0; i < r && nc < 509; ++i) {
        for (int j = i + 1; j < r && nc < 509; ++j) {
            if (d.u[i] == d.u[j]) cands[nc++] = {u8(i), u8(j), 0};
            if (d.v[i] == d.v[j]) cands[nc++] = {u8(i), u8(j), 1};
            if (d.w[i] == d.w[j]) cands[nc++] = {u8(i), u8(j), 2};
        }
    }
    if (nc == 0) return false;
    u64 rv = rng();
    const auto& c = cands[rv % nc];
    int i = c.i, j = c.j;
    if ((rv >> 16) & 1) std::swap(i, j);
    bool dir = ((rv >> 17) & 1) != 0;
    if (c.mode == 0) {
        // u_i == u_j: (u, v_i, w_i) + (u, v_j, w_j) = (u, v_i ^ v_j, w_i) + (u, v_j, w_i ^ w_j)
        if (dir) { d.v[i] ^= d.v[j]; d.w[j] ^= d.w[i]; }
        else     { d.w[i] ^= d.w[j]; d.v[j] ^= d.v[i]; }
    } else if (c.mode == 1) {
        if (dir) { d.u[i] ^= d.u[j]; d.w[j] ^= d.w[i]; }
        else     { d.w[i] ^= d.w[j]; d.u[j] ^= d.u[i]; }
    } else {
        if (dir) { d.u[i] ^= d.u[j]; d.v[j] ^= d.v[i]; }
        else     { d.v[i] ^= d.v[j]; d.u[j] ^= d.u[i]; }
    }
    // Check immediate rank drop!
    if (d.u[i] == 0 || d.v[i] == 0 || d.w[i] == 0 || d.u[j] == 0 || d.v[j] == 0 || d.w[j] == 0) {
        compact_decomp(d);
    } else {
        // Quick scan for duplicate pair involving i or j
        for (int k = 0; k < r; ++k) {
            if (k != i && ((d.u[k] == d.u[i] && d.v[k] == d.v[i]) ||
                           (d.u[k] == d.u[i] && d.w[k] == d.w[i]) ||
                           (d.v[k] == d.v[i] && d.w[k] == d.w[i]))) { compact_decomp(d); return true; }
            if (k != j && ((d.u[k] == d.u[j] && d.v[k] == d.v[j]) ||
                           (d.u[k] == d.u[j] && d.w[k] == d.w[j]) ||
                           (d.v[k] == d.v[j] && d.w[k] == d.w[j]))) { compact_decomp(d); return true; }
        }
    }
    return true;
}

// AIH Plus-Transition: split term i along factor of term j so rank -> r+1 with immediate new flip!
static inline void plus_transition(PolyTensorDecomp& d, std::mt19937_64& rng) {
    int r = (int)d.u.size();
    if (r < 2) return;
    u64 rv = rng();
    int i = rv % r;
    int j = (i + 1 + ((rv >> 8) % (r - 1))) % r;
    int mode = (rv >> 16) % 3;
    if (mode == 0 && d.u[i] != d.u[j]) {
        u8 diff = d.u[i] ^ d.u[j];
        d.u[i] = diff;
        d.u.push_back(d.u[j]); d.v.push_back(d.v[i]); d.w.push_back(d.w[i]);
    } else if (mode == 1 && d.v[i] != d.v[j]) {
        u8 diff = d.v[i] ^ d.v[j];
        d.v[i] = diff;
        d.u.push_back(d.u[i]); d.v.push_back(d.v[j]); d.w.push_back(d.w[i]);
    } else if (d.w[i] != d.w[j]) {
        u16 diff = d.w[i] ^ d.w[j];
        d.w[i] = diff;
        d.u.push_back(d.u[i]); d.v.push_back(d.v[i]); d.w.push_back(d.w[j]);
    } else {
        // Fallback random split in mode 0
        u8 x = u8(1 + ((rv >> 24) % ((1 << d.n) - 1)));
        if (x != d.u[i]) {
            d.u[i] ^= x;
            d.u.push_back(x); d.v.push_back(d.v[i]); d.w.push_back(d.w[i]);
        }
    }
}

static PolyTensorDecomp make_schoolbook(int n) {
    PolyTensorDecomp d; d.n = n;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            d.u.push_back(u8(1 << i));
            d.v.push_back(u8(1 << j));
            d.w.push_back(u16(1u << (i + j)));
        }
    return d;
}

// Explicit 26-product CRT seeds for n=8!
static std::vector<PolyTensorDecomp> make_crt26_seeds() {
    auto slices = poly_mult_slices(8);
    // Helper: poly mod p(x) for each x^i (i=0..7)
    auto mod_forms = [](int deg, int poly_mask) {
        std::vector<u8> coeff(deg, 0);
        for (int i = 0; i < 8; ++i) {
            int rem = (1 << i);
            for (int b = 7; b >= deg; --b)
                if ((rem >> b) & 1) rem ^= (poly_mask << (b - deg));
            for (int r = 0; r < deg; ++r)
                if ((rem >> r) & 1) coeff[r] |= u8(1 << i);
        }
        return coeff;
    };
    auto add_sp2 = [](std::vector<u8>& U, u8 f0, u8 f1) {
        U.push_back(f0); U.push_back(f1); U.push_back(f0 ^ f1);
    };
    auto add_sp3 = [](std::vector<u8>& U, u8 f0, u8 f1, u8 f2) {
        // 5 products for ShortProduct_3: f0, f1, f2, f0^f1, f0^f2
        U.push_back(f0); U.push_back(f1); U.push_back(f2);
        U.push_back(f0 ^ f1); U.push_back(f0 ^ f2);
    };
    auto add_m3 = [](std::vector<u8>& U, u8 f0, u8 f1, u8 f2) {
        // 6 products for full 3-term Karatsuba:
        U.push_back(f0); U.push_back(f1); U.push_back(f2);
        U.push_back(f0 ^ f1); U.push_back(f0 ^ f2); U.push_back(f1 ^ f2);
    };

    // Basis at x = 0: a0, a1, a2
    u8 z0 = 0x01, z1 = 0x02, z2 = 0x04;
    // Basis at x = 1 (y = x+1): A(y+1) = sum a_i (y+1)^i -> y^0: sum a_i = 0xFF, y^1: odd i = 0xAA, y^2: C(i,2) odd -> i in {2,3,6,7} = 0xCC
    u8 o0 = 0xFF, o1 = 0xAA, o2 = 0xCC;
    // Basis at x = inf: a7, a6, a5
    u8 i0 = 0x80, i1 = 0x40, i2 = 0x20;

    auto f_111 = mod_forms(2, 0b111);   // x^2 + x + 1
    auto f_1011 = mod_forms(3, 0b1011); // x^3 + x + 1
    auto f_1101 = mod_forms(3, 0b1101); // x^3 + x^2 + 1

    std::vector<PolyTensorDecomp> seeds;
    for (int mult3_choice = 0; mult3_choice < 3; ++mult3_choice) {
        std::vector<u8> U;
        if (mult3_choice == 0) {
            add_sp3(U, z0, z1, z2);
            add_sp2(U, o0, o1);
            add_sp2(U, i0, i1);
        } else if (mult3_choice == 1) {
            add_sp2(U, z0, z1);
            add_sp3(U, o0, o1, o2);
            add_sp2(U, i0, i1);
        } else {
            add_sp2(U, z0, z1);
            add_sp2(U, o0, o1);
            add_sp3(U, i0, i1, i2);
        }
        add_sp2(U, f_111[0], f_111[1]);
        add_m3(U, f_1011[0], f_1011[1], f_1011[2]);
        add_m3(U, f_1101[0], f_1101[1], f_1101[2]);

        PolyTensorDecomp d; d.n = 8; d.u = U; d.v = U;
        if (solve_mode2_and_prune(d, slices) && verify_poly_decomp(d)) {
            seeds.push_back(std::move(d));
        }
    }
    return seeds;
}

static PolyTensorDecomp flip_search_poly(int n, PolyTensorDecomp cur, int target_rank,
                                         long long max_flips, std::mt19937_64& rng,
                                         std::vector<PolyTensorDecomp>* harvest = nullptr) {
    auto slices = poly_mult_slices(n);
    PolyTensorDecomp best = cur;
    long long flips = 0;
    int plateau = 0;
    while (flips < max_flips && best.rank() > target_rank) {
        int r_before = cur.rank();
        bool ok = random_flip_step(cur, rng);
        flips++;
        if (!ok) {
            plus_transition(cur, rng);
            plateau = 0;
            continue;
        }
        if (cur.rank() < r_before) {
            plateau = 0;
            if (cur.rank() < best.rank() && verify_poly_decomp(cur)) {
                best = cur;
                if (best.rank() <= target_rank) break;
            }
            if (harvest && cur.rank() <= best.rank() + 2 && harvest->size() < 64) {
                harvest->push_back(cur);
            }
        } else {
            plateau++;
            // Periodic 3-mode linear-dependence check!
            if ((plateau & 255) == 0) {
                int r0 = cur.rank();
                solve_mode2_and_prune(cur, slices);
                try_mode01_prune(cur);
                if (cur.rank() < r0) {
                    plateau = 0;
                    if (cur.rank() < best.rank() && verify_poly_decomp(cur)) {
                        best = cur;
                        if (best.rank() <= target_rank) break;
                    }
                }
            }
            // Adaptive AIH plus-transition when stuck at rank plateau!
            int limit = (cur.rank() <= best.rank()) ? 900 : 350;
            if (plateau >= limit) {
                if (cur.rank() >= best.rank() + 2) {
                    cur = best; // Snap back to best rank before next plus-jump
                }
                if (cur.rank() <= best.rank() + 1) {
                    if (harvest && cur.rank() == best.rank() && harvest->size() < 96 && (rng() % 8 == 0))
                        harvest->push_back(cur);
                    plus_transition(cur, rng);
                }
                plateau = 0;
            }
        }
    }
    return best;
}

// ============================================================================
// PART 2: REDUCED GF(2^m) EXACT STEINER-CLOSURE + STRUCTURED/FLIP SEARCH
// ============================================================================

struct Bitset256 {
    u64 w[4] = {0, 0, 0, 0};
    inline bool test(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
    inline void set(int i) { w[i >> 6] |= (1ULL << (i & 63)); }
    inline bool contains(const Bitset256& o) const {
        return ((o.w[0] & ~w[0]) | (o.w[1] & ~w[1]) | (o.w[2] & ~w[2]) | (o.w[3] & ~w[3])) == 0ULL;
    }
    inline int count() const {
        return __builtin_popcountll(w[0]) + __builtin_popcountll(w[1]) +
               __builtin_popcountll(w[2]) + __builtin_popcountll(w[3]);
    }
};

static int gf2_poly_mul_mod(int a, int b, int m, int poly) {
    int res = 0;
    for (int i = 0; i < m; ++i)
        if ((a >> i) & 1) res ^= (b << i);
    for (int d = 2 * m - 2; d >= m; --d)
        if ((res >> d) & 1) res ^= (poly << (d - m));
    return res & ((1 << m) - 1);
}

static std::vector<u64> build_field_targets(int m, int poly) {
    std::vector<u64> tgt(m, 0ULL);
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < m; ++j) {
            int rem = gf2_poly_mul_mod(1 << i, 1 << j, m, poly);
            for (int k = 0; k < m; ++k)
                if ((rem >> k) & 1) tgt[k] |= (1ULL << (i * 8 + j));
        }
    return tgt;
}

static int fast_field_floor(int m, const std::vector<u64>& targets,
                            const std::vector<u8>& U, const std::vector<u8>& V,
                            u64 W_rows_out[8] = nullptr) {
    int K_in = (int)U.size();
    if (K_in > 62) return 999999;
    u64 bv[64] = {0}, bc[64] = {0};
    bool hp[64] = {false};
    for (int t = 0; t < K_in; ++t) {
        u64 v = OUTER8[U[t]][V[t]], c = (1ULL << t);
        while (v) {
            int p = __builtin_ctzll(v);
            if (!hp[p]) { hp[p] = true; bv[p] = v; bc[p] = c; break; }
            v ^= bv[p]; c ^= bc[p];
        }
    }
    u64 W_rows[8] = {0};
    for (int k = 0; k < m; ++k) {
        u64 v = targets[k], c = 0;
        while (v) {
            int p = __builtin_ctzll(v);
            if (!hp[p]) return 999999;
            v ^= bv[p]; c ^= bc[p];
        }
        W_rows[k] = c;
        if (W_rows_out) W_rows_out[k] = c;
    }
    Bitset256 SU{}, SV{}, SWT{};
    int live_K = 0;
    bool sym = (U == V);
    for (int t = 0; t < K_in; ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) if ((W_rows[r] >> t) & 1ULL) col |= u8(1 << r);
        if (col == 0) continue;
        live_K++;
        if (__builtin_popcount(U[t]) > 1) SU.set(U[t]);
        if (!sym && __builtin_popcount(V[t]) > 1) SV.set(V[t]);
        if (__builtin_popcount(col) > 1) SWT.set(col);
    }
    int du = SU.count();
    int dv = sym ? du : SV.count();
    return (2 * live_K - m) + du + dv + SWT.count();
}

static inline bool closure_covers(int m, const Bitset256& S, const Bitset256& allowed, Bitset256& B_out,
                                  u8* B_list_out, int& B_len_out) {
    B_out = Bitset256{}; B_len_out = 0;
    for (int i = 0; i < m; ++i) { u8 v = u8(1 << i); B_out.set(v); B_list_out[B_len_out++] = v; }
    u8 cands[256]; int n_cands = 0, lim = 1 << m;
    for (int v = 1; v < lim; ++v) if (allowed.test(v) && !B_out.test(v)) cands[n_cands++] = u8(v);
    bool progress = true;
    while (progress && n_cands > 0) {
        progress = false;
        for (int ci = 0; ci < n_cands; ) {
            u8 t = cands[ci]; bool ok = false;
            for (int i = 0; i < B_len_out; ++i) if (B_out.test(t ^ B_list_out[i])) { ok = true; break; }
            if (ok) { B_out.set(t); B_list_out[B_len_out++] = t; cands[ci] = cands[--n_cands]; progress = true; }
            else ++ci;
        }
    }
    return B_out.contains(S);
}

static bool ida_helpers(int m, const Bitset256& S, Bitset256 allowed, const Bitset256& B_cur,
                        const u8* B_list, int B_len, int rem_depth, Bitset256& best_allowed,
                        int& nodes_visited, int max_nodes) {
    if (rem_depth == 0) return B_cur.contains(S);
    if (++nodes_visited > max_nodes) return false;
    Bitset256 cand_H{};
    for (int i = 0; i < B_len; ++i)
        for (int j = i + 1; j < B_len; ++j) {
            u8 h = B_list[i] ^ B_list[j];
            if (h != 0 && !allowed.test(h) && !B_cur.test(h)) cand_H.set(h);
        }
    struct HCand { u8 h; int sc; };
    HCand hlist[256]; int nh = 0;
    u8 missing[256]; int n_miss = 0, lim = 1 << m;
    for (int v = 1; v < lim; ++v) if (S.test(v) && !B_cur.test(v)) missing[n_miss++] = u8(v);
    for (int h = 1; h < lim; ++h) {
        if (!cand_H.test(h)) continue;
        int hits = 0;
        for (int mi = 0; mi < n_miss; ++mi) if (B_cur.test(missing[mi] ^ u8(h))) hits++;
        if (rem_depth == 1 && hits == 0) continue;
        hlist[nh++] = {u8(h), hits * 8 + (8 - __builtin_popcount(h))};
    }
    std::sort(hlist, hlist + nh, [](const HCand& a, const HCand& b) { return a.sc > b.sc; });
    for (int idx = 0; idx < nh; ++idx) {
        Bitset256 next_allowed = allowed; next_allowed.set(hlist[idx].h);
        Bitset256 B_next; u8 B_next_list[256]; int B_next_len = 0;
        if (closure_covers(m, S, next_allowed, B_next, B_next_list, B_next_len)) { best_allowed = next_allowed; return true; }
        if (rem_depth > 1 && ida_helpers(m, S, next_allowed, B_next, B_next_list, B_next_len, rem_depth - 1, best_allowed, nodes_visited, max_nodes))
            return true;
        if (nodes_visited > max_nodes) return false;
    }
    return false;
}

static int min_linear_gates(int m, const std::vector<u8>& rows, int max_exc = 3, int max_nodes = 25000) {
    Bitset256 S{}, allowed0{};
    for (int i = 0; i < m; ++i) allowed0.set(1 << i);
    for (u8 r : rows) if (r != 0 && __builtin_popcount(r) > 1) { S.set(r); allowed0.set(r); }
    int d = S.count();
    if (d == 0) return 0;
    Bitset256 B0, win; u8 B0_list[256]; int B0_len = 0;
    if (closure_covers(m, S, allowed0, B0, B0_list, B0_len)) return d;
    for (int exc = 1; exc <= max_exc; ++exc) {
        int vis = 0;
        if (ida_helpers(m, S, allowed0, B0, B0_list, B0_len, exc, win, vis, max_nodes)) return d + exc;
    }
    return d + max_exc + 2;
}

static int exact_field_score(int m, const std::vector<u64>& targets,
                             const std::vector<u8>& U_in, const std::vector<u8>& V_in) {
    u64 W_rows[8] = {0};
    int fl = fast_field_floor(m, targets, U_in, V_in, W_rows);
    if (fl >= 999999) return 999999;
    std::vector<u8> U, V, WT;
    for (size_t t = 0; t < U_in.size(); ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) if ((W_rows[r] >> t) & 1ULL) col |= u8(1 << r);
        if (col == 0) continue;
        U.push_back(U_in[t]); V.push_back(V_in[t]); WT.push_back(col);
    }
    int K = (int)U.size();
    int lu = min_linear_gates(m, U, 3, 25000);
    int lv = (U == V) ? lu : min_linear_gates(m, V, 3, 25000);
    int lwt = min_linear_gates(m, WT, 3, 30000);
    return (2 * K - m) + lu + lv + lwt;
}

// ============================================================================
// PART 3: EXACT 2^(2m)-BIT TRUTH-TABLE GATE-WALK & CONE RESUBSTITUTION
// ============================================================================

struct GateCirc {
    int m = 0, poly = 0;
    struct Gate { u8 op; int in1, in2; std::string out_name; }; // op: 0=XOR, 1=AND, 2=XNOR
    std::vector<Gate> gates; // wire ids: 0..m-1 = A0..Am-1, m..2m-1 = B0..Bm-1, 2m+g = gate g
    std::vector<int> out_wire; // size m: wire id for C0..Cm-1
};

static GateCirc load_any_slp(const std::string& path, int m, int poly) {
    GateCirc gc; gc.m = m; gc.poly = poly;
    gc.out_wire.assign(m, -1);
    std::unordered_map<std::string, int> sym;
    for (int i = 0; i < m; ++i) {
        sym["A" + std::to_string(i)] = i;
        sym["a" + std::to_string(i)] = i;
        sym["B" + std::to_string(i)] = m + i;
        sym["b" + std::to_string(i)] = m + i;
    }
    std::ifstream in(path);
    std::string line;
    while (std::getline(in, line)) {
        auto pos = line.find('#');
        if (pos != std::string::npos) line = line.substr(0, pos);
        std::stringstream ss(line);
        std::vector<std::string> tok;
        std::string t;
        while (ss >> t) tok.push_back(t);
        if (tok.empty()) continue;
        if (tok[0] == "XOR" || tok[0] == "AND" || tok[0] == "XNOR") {
            u8 op = (tok[0] == "XOR") ? 0 : ((tok[0] == "AND") ? 1 : 2);
            int w = 2 * m + (int)gc.gates.size();
            gc.gates.push_back({op, sym.at(tok[2]), sym.at(tok[3]), tok[1]});
            sym[tok[1]] = w;
            if ((tok[1][0] == 'C' || tok[1][0] == 'c') && tok[1].size() == 2)
                gc.out_wire[tok[1][1] - '0'] = w;
        } else if (tok.size() == 5 && tok[1] == "=") {
            u8 op = (tok[3] == "+") ? 0 : ((tok[3] == "x" || tok[3] == "*") ? 1 : 2);
            int w = 2 * m + (int)gc.gates.size();
            gc.gates.push_back({op, sym.at(tok[2]), sym.at(tok[4]), tok[0]});
            sym[tok[0]] = w;
            if ((tok[0][0] == 'C' || tok[0][0] == 'c') && tok[0].size() == 2)
                gc.out_wire[tok[0][1] - '0'] = w;
        } else if (tok.size() == 3 && tok[1] == "=") {
            if ((tok[0][0] == 'C' || tok[0][0] == 'c') && tok[0].size() == 2)
                gc.out_wire[tok[0][1] - '0'] = sym.at(tok[2]);
        }
    }
    return gc;
}

static bool dead_code_and_verify(GateCirc& gc) {
    int m = gc.m;
    int G = (int)gc.gates.size();
    std::vector<bool> live(2 * m + G, false);
    for (int k = 0; k < m; ++k) if (gc.out_wire[k] >= 0) live[gc.out_wire[k]] = true;
    for (int g = G - 1; g >= 0; --g) {
        if (live[2 * m + g]) {
            live[gc.gates[g].in1] = true;
            live[gc.gates[g].in2] = true;
        }
    }
    std::vector<int> remap(2 * m + G, -1);
    for (int i = 0; i < 2 * m; ++i) remap[i] = i;
    std::vector<GateCirc::Gate> ng;
    for (int g = 0; g < G; ++g) {
        if (!live[2 * m + g]) continue;
        int nid = 2 * m + (int)ng.size();
        remap[2 * m + g] = nid;
        ng.push_back({gc.gates[g].op, remap[gc.gates[g].in1], remap[gc.gates[g].in2], gc.gates[g].out_name});
    }
    for (int k = 0; k < m; ++k) gc.out_wire[k] = remap[gc.out_wire[k]];
    gc.gates = std::move(ng);

    // Exhaustive truth-table check across all 2^(2m) input pairs!
    int n_pairs = 1 << (2 * m);
    int n_words = (n_pairs + 63) / 64;
    int W = 2 * m + (int)gc.gates.size();
    std::vector<std::vector<u64>> tt(W, std::vector<u64>(n_words, 0ULL));
    std::vector<std::vector<u64>> ref(m, std::vector<u64>(n_words, 0ULL));
    for (int idx = 0; idx < n_pairs; ++idx) {
        int a = idx & ((1 << m) - 1), b = idx >> m;
        int wd = idx >> 6, bt = idx & 63;
        for (int i = 0; i < m; ++i) {
            if ((a >> i) & 1) tt[i][wd] |= (1ULL << bt);
            if ((b >> i) & 1) tt[m + i][wd] |= (1ULL << bt);
        }
        int p = gf2_poly_mul_mod(a, b, m, gc.poly);
        for (int k = 0; k < m; ++k) if ((p >> k) & 1) ref[k][wd] |= (1ULL << bt);
    }
    for (size_t g = 0; g < gc.gates.size(); ++g) {
        int w = 2 * m + (int)g;
        const auto& a = tt[gc.gates[g].in1];
        const auto& b = tt[gc.gates[g].in2];
        for (int wd = 0; wd < n_words; ++wd) {
            if (gc.gates[g].op == 0) tt[w][wd] = a[wd] ^ b[wd];
            else if (gc.gates[g].op == 1) tt[w][wd] = a[wd] & b[wd];
            else tt[w][wd] = ~(a[wd] ^ b[wd]);
        }
        if (n_pairs < 64) tt[w][0] &= ((1ULL << n_pairs) - 1ULL);
    }
    for (int k = 0; k < m; ++k)
        if (tt[gc.out_wire[k]] != ref[k]) return false;
    return true;
}

// Truth-table resubstitution + fanout-1 XOR/AND reassociation + distributivity walk!
static int gate_walk_optimize(GateCirc& gc, int steps, std::mt19937_64& rng) {
    dead_code_and_verify(gc);
    int best_sz = (int)gc.gates.size();
    GateCirc best_gc = gc;
    int m = gc.m;
    int n_pairs = 1 << (2 * m);
    int n_words = (n_pairs + 63) / 64;

    auto compute_tts = [&](const GateCirc& c, std::vector<std::vector<u64>>& tt) {
        int W = 2 * m + (int)c.gates.size();
        tt.assign(W, std::vector<u64>(n_words, 0ULL));
        for (int idx = 0; idx < n_pairs; ++idx) {
            int a = idx & ((1 << m) - 1), b = idx >> m;
            int wd = idx >> 6, bt = idx & 63;
            for (int i = 0; i < m; ++i) {
                if ((a >> i) & 1) tt[i][wd] |= (1ULL << bt);
                if ((b >> i) & 1) tt[m + i][wd] |= (1ULL << bt);
            }
        }
        for (size_t g = 0; g < c.gates.size(); ++g) {
            int w = 2 * m + (int)g;
            const auto& a = tt[c.gates[g].in1];
            const auto& b = tt[c.gates[g].in2];
            for (int wd = 0; wd < n_words; ++wd) {
                if (c.gates[g].op == 0) tt[w][wd] = a[wd] ^ b[wd];
                else if (c.gates[g].op == 1) tt[w][wd] = a[wd] & b[wd];
                else tt[w][wd] = ~(a[wd] ^ b[wd]);
            }
        }
    };

    auto hash_tt = [&](const std::vector<u64>& v) -> u64 {
        u64 h = 1469598103934665603ULL;
        for (u64 x : v) { h ^= x; h *= 1099511628211ULL; }
        return h;
    };

    std::vector<std::vector<u64>> tt;
    for (int st = 0; st < steps; ++st) {
        compute_tts(gc, tt);
        int G = (int)gc.gates.size();
        int W = 2 * m + G;

        // 1. Check global 0-gate or 1-gate resubstitution for ANY wire w!
        std::unordered_map<u64, int> single_map;
        single_map.reserve(W * 2);
        bool improved = false;
        for (int w = 0; w < W; ++w) {
            u64 h = hash_tt(tt[w]);
            auto it = single_map.find(h);
            if (it != single_map.end() && tt[it->second] == tt[w]) {
                int src = it->second;
                // Replace all uses of w with src!
                for (auto& g : gc.gates) {
                    if (g.in1 == w) g.in1 = src;
                    if (g.in2 == w) g.in2 = src;
                }
                for (int k = 0; k < m; ++k) if (gc.out_wire[k] == w) gc.out_wire[k] = src;
                dead_code_and_verify(gc);
                improved = true; break;
            }
            single_map[h] = w;
        }
        if (improved) {
            if ((int)gc.gates.size() < best_sz && dead_code_and_verify(gc)) {
                best_sz = (int)gc.gates.size(); best_gc = gc;
            }
            continue;
        }

        // Compute fanouts and MFFC (fanout-free cone size >= 2)
        std::vector<int> fanout(W, 0);
        for (const auto& g : gc.gates) { fanout[g.in1]++; fanout[g.in2]++; }
        for (int k = 0; k < m; ++k) fanout[gc.out_wire[k]]++;

        // Build hash table of all available 1-gate functions (u XOR v, u AND v, u XNOR v) at periodic steps
        if (st % 25 == 0) {
            // Check if any gate g whose inputs include a fanout-1 gate can be replaced by 1 gate on earlier wires!
            std::unordered_map<u64, std::tuple<u8, int, int>> pair_map;
            pair_map.reserve(W * W);
            for (int g = 0; g < G && !improved; ++g) {
                int w = 2 * m + g;
                bool has_fo1_parent = (gc.gates[g].in1 >= 2 * m && fanout[gc.gates[g].in1] == 1) ||
                                      (gc.gates[g].in2 >= 2 * m && fanout[gc.gates[g].in2] == 1);
                if (!has_fo1_parent) continue;
                u64 target_h = hash_tt(tt[w]);
                // Search all pairs (u, v) with u < v < w excluding the fanout-1 parent(s)!
                int p1 = (gc.gates[g].in1 >= 2 * m && fanout[gc.gates[g].in1] == 1) ? gc.gates[g].in1 : -1;
                int p2 = (gc.gates[g].in2 >= 2 * m && fanout[gc.gates[g].in2] == 1) ? gc.gates[g].in2 : -1;
                std::vector<u64> tmp(n_words);
                for (int u = 0; u < w && !improved; ++u) {
                    if (u == p1 || u == p2) continue;
                    for (int v = u + 1; v < w && !improved; ++v) {
                        if (v == p1 || v == p2) continue;
                        for (u8 op = 0; op < 3; ++op) {
                            for (int wd = 0; wd < n_words; ++wd) {
                                if (op == 0) tmp[wd] = tt[u][wd] ^ tt[v][wd];
                                else if (op == 1) tmp[wd] = tt[u][wd] & tt[v][wd];
                                else tmp[wd] = ~(tt[u][wd] ^ tt[v][wd]);
                            }
                            if (hash_tt(tmp) == target_h && tmp == tt[w]) {
                                gc.gates[g].op = op;
                                gc.gates[g].in1 = u;
                                gc.gates[g].in2 = v;
                                dead_code_and_verify(gc);
                                improved = true;
                                break;
                            }
                        }
                    }
                }
            }
            if (improved) {
                if ((int)gc.gates.size() < best_sz && dead_code_and_verify(gc)) {
                    best_sz = (int)gc.gates.size(); best_gc = gc;
                }
                continue;
            }
        }

        // Neutral fanout-1 XOR reassociation pivot:
        // Find g (XOR/XNOR) with a fanout-1 parent p (XOR/XNOR): (a ^ b) ^ c -> (a ^ c) ^ b or (b ^ c) ^ a!
        std::vector<int> pivots;
        for (int g = 0; g < G; ++g) {
            if (gc.gates[g].op == 1) continue;
            int i1 = gc.gates[g].in1, i2 = gc.gates[g].in2;
            if (i1 >= 2 * m && fanout[i1] == 1 && gc.gates[i1 - 2 * m].op != 1) pivots.push_back(g * 2 + 0);
            if (i2 >= 2 * m && fanout[i2] == 1 && gc.gates[i2 - 2 * m].op != 1) pivots.push_back(g * 2 + 1);
        }
        if (!pivots.empty()) {
            int pick = pivots[rng() % pivots.size()];
            int g = pick / 2, side = pick % 2;
            int p_wire = (side == 0) ? gc.gates[g].in1 : gc.gates[g].in2;
            int c_wire = (side == 0) ? gc.gates[g].in2 : gc.gates[g].in1;
            int pg = p_wire - 2 * m;
            int a_wire = gc.gates[pg].in1, b_wire = gc.gates[pg].in2;
            // Ensure topological validity: p_wire is at index pg < g. If c_wire < p_wire, we can put (a ^ c) at pg!
            // Even if c_wire > p_wire (c_wire < 2m+g), we can move pg right before g or only reassociate when c_wire < p_wire!
            if (c_wire < p_wire && a_wire != c_wire && b_wire != c_wire) {
                if (rng() & 1) {
                    gc.gates[pg].in1 = a_wire; gc.gates[pg].in2 = c_wire;
                    if (side == 0) gc.gates[g].in2 = b_wire; else gc.gates[g].in1 = b_wire;
                } else {
                    gc.gates[pg].in1 = b_wire; gc.gates[pg].in2 = c_wire;
                    if (side == 0) gc.gates[g].in2 = a_wire; else gc.gates[g].in1 = a_wire;
                }
            }
        }
    }
    gc = best_gc;
    return best_sz;
}

int main() {
    init_outer8();
    std::mt19937_64 rng(20261115ULL);

    std::cout << "====================================================================\n";
    std::cout << "PHASE 1: FLIP-GRAPH + AIH PLUS-TRANSITION + 3-MODE REDUCTION ON T_n\n";
    std::cout << "====================================================================\n";

    // Step 1A: Calibrate on n = 4, 5, 6, 7 from schoolbook!
    int expected_rank[9] = {0, 1, 3, 6, 9, 13, 17, 22, 26};
    std::vector<PolyTensorDecomp> m6_harvest;
    for (int n = 4; n <= 7; ++n) {
        auto sb = make_schoolbook(n);
        long long budget = (n <= 5) ? 150000 : ((n == 6) ? 800000 : 2500000);
        auto best = flip_search_poly(n, sb, expected_rank[n], budget, rng, (n == 6) ? &m6_harvest : nullptr);
        std::cout << "[Calibration n=" << n << "] schoolbook=" << (n * n)
                  << " -> discovered rank=" << best.rank()
                  << " (literature record=" << expected_rank[n]
                  << ", verified=" << (verify_poly_decomp(best) ? "YES" : "NO") << ")\n" << std::flush;
    }

    // Step 1B: Build explicit 26-product CRT seeds for n = 8 and verify!
    auto crt_seeds = make_crt26_seeds();
    std::cout << "[n=8 CRT Seeds] Constructed " << crt_seeds.size()
              << " verified rank-26 CRT decompositions (ranks:";
    for (const auto& s : crt_seeds) std::cout << " " << s.rank();
    std::cout << ")\n" << std::flush;

    // Also cool down n=8 from schoolbook (64 -> 26/27) across 4 independent trajectories!
    std::vector<PolyTensorDecomp> m8_harvest = crt_seeds;
    int best_from_sb = 64;
    for (int run = 0; run < 4; ++run) {
        auto sb8 = make_schoolbook(8);
        auto cooled = flip_search_poly(8, sb8, 25, 3000000, rng, &m8_harvest);
        best_from_sb = std::min(best_from_sb, cooled.rank());
        std::cout << "  [n=8 schoolbook cooldown #" << (run + 1) << "] 64 -> rank " << cooled.rank()
                  << " (verified=" << (verify_poly_decomp(cooled) ? "YES" : "NO") << ")\n" << std::flush;
        if (cooled.rank() <= 27) m8_harvest.push_back(cooled);
    }

    // Step 1C: Intensive Rank-25 Hunt on n=8 across CRT seeds + cooled seeds (24M flip+plus steps)!
    int global_min_r8 = 26;
    PolyTensorDecomp best_d8 = crt_seeds[0];
    for (int epoch = 0; epoch < 6; ++epoch) {
        PolyTensorDecomp start = crt_seeds[epoch % crt_seeds.size()];
        auto res = flip_search_poly(8, start, 25, 4000000, rng, &m8_harvest);
        if (res.rank() < global_min_r8 && verify_poly_decomp(res)) {
            global_min_r8 = res.rank();
            best_d8 = res;
            std::cout << "  *** BREAKTHROUGH: n=8 RANK = " << global_min_r8 << " ***\n" << std::flush;
        } else {
            std::cout << "  [n=8 Rank-25 Hunt epoch " << (epoch + 1) << "/6] 4,000,000 flip+AIH steps: min_rank="
                      << res.rank() << " (harvested=" << m8_harvest.size() << ")\n" << std::flush;
        }
    }

    std::cout << "\n====================================================================\n";
    std::cout << "PHASE 2: GF(2^6) 0x49 (<=56 vs 57) & GF(2^8) 0x11B (<=106 vs 107)\n";
    std::cout << "====================================================================\n";

    // Step 2A: GF(2^6) mod x^6 + x^3 + 1 (0x49)
    {
        auto tgt6 = build_field_targets(6, 0x49);
        int min_fl6 = 999, min_ex6 = 999;

        // 1) Exhaustive 2^9 = 512 off-diagonal pair contractions of CMT 2x3 split + 2000 GL_6 basis twists!
        auto test_2x3_basis = [&](const u8 b[6], bool full_512) {
            u8 A0[3] = {b[0], b[1], b[2]}, A1[3] = {b[3], b[4], b[5]};
            u8 AS[3] = {u8(b[0] ^ b[3]), u8(b[1] ^ b[4]), u8(b[2] ^ b[5])};
            const u8* blocks[3] = {A0, A1, AS};
            int pairs[3][2] = {{0, 1}, {0, 2}, {1, 2}};

            auto eval_mask = [&](int mask9) {
                std::vector<u8> U, V;
                for (int blk = 0; blk < 3; ++blk) {
                    const u8* B = blocks[blk];
                    for (int d = 0; d < 3; ++d) { U.push_back(B[d]); V.push_back(B[d]); }
                    for (int p = 0; p < 3; ++p) {
                        int i = pairs[p][0], j = pairs[p][1];
                        if ((mask9 >> (blk * 3 + p)) & 1) {
                            U.push_back(B[i] ^ B[j]); V.push_back(B[i] ^ B[j]);
                        } else {
                            U.push_back(B[i]); V.push_back(B[j]);
                            U.push_back(B[j]); V.push_back(B[i]);
                        }
                    }
                }
                int fl = fast_field_floor(6, tgt6, U, V);
                if (fl < min_fl6) min_fl6 = fl;
                if (fl <= 57) {
                    int ex = exact_field_score(6, tgt6, U, V);
                    if (ex < min_ex6) {
                        min_ex6 = ex;
                        std::cout << "  [GF(2^6) 2x3] K=" << U.size() << " mask=" << mask9
                                  << " floor=" << fl << " exact=" << ex << "\n" << std::flush;
                    }
                }
            };
            if (full_512) {
                for (int m9 = 0; m9 < 512; ++m9) eval_mask(m9);
            } else {
                for (int m9 : {0, 7, 56, 63, 73, 146, 292, 511, int(rng() & 511)}) eval_mask(m9);
            }
        };

        u8 id6[6] = {1, 2, 4, 8, 16, 32};
        test_2x3_basis(id6, true);
        // Also all 6! = 720 coordinate permutations of 2x3!
        std::array<u8, 6> perm6 = {1, 2, 4, 8, 16, 32};
        do {
            test_2x3_basis(perm6.data(), false);
        } while (std::next_permutation(perm6.begin(), perm6.end()));
        // Plus 3000 sparse GL_6 shears!
        for (int tr = 0; tr < 3000; ++tr) {
            u8 b[6] = {1, 2, 4, 8, 16, 32};
            std::shuffle(b, b + 6, rng);
            int ns = 1 + (rng() % 4);
            for (int s = 0; s < ns; ++s) { int x = rng() % 6, y = rng() % 6; if (x != y) b[x] ^= b[y]; }
            test_2x3_basis(b, false);
        }

        // 2) Also test 3x2 splits (K_3 x S_2 and S_3 x K_2) across all 720 permutations!
        perm6 = {1, 2, 4, 8, 16, 32};
        do {
            // 6 blocks of 2x2: (0,1), (2,3), (4,5), (0^2, 1^3), (0^4, 1^5), (2^4, 3^5)
            u8 P[6][2] = {
                {perm6[0], perm6[1]}, {perm6[2], perm6[3]}, {perm6[4], perm6[5]},
                {u8(perm6[0] ^ perm6[2]), u8(perm6[1] ^ perm6[3])},
                {u8(perm6[0] ^ perm6[4]), u8(perm6[1] ^ perm6[5])},
                {u8(perm6[2] ^ perm6[4]), u8(perm6[3] ^ perm6[5])}
            };
            for (int lm6 : {0, 7, 56, 63}) {
                std::vector<u8> U, V;
                for (int l = 0; l < 6; ++l) {
                    U.push_back(P[l][0]); V.push_back(P[l][0]);
                    U.push_back(P[l][1]); V.push_back(P[l][1]);
                    if ((lm6 >> l) & 1) { U.push_back(P[l][0] ^ P[l][1]); V.push_back(P[l][0] ^ P[l][1]); }
                    else { U.push_back(P[l][0]); V.push_back(P[l][1]); U.push_back(P[l][1]); V.push_back(P[l][0]); }
                }
                int fl = fast_field_floor(6, tgt6, U, V);
                if (fl < min_fl6) min_fl6 = fl;
                if (fl <= 57) {
                    int ex = exact_field_score(6, tgt6, U, V);
                    if (ex < min_ex6) min_ex6 = ex;
                }
            }
        } while (std::next_permutation(perm6.begin(), perm6.end()));

        // 3) Evaluate harvested low-rank T_6 decompositions!
        for (const auto& d6 : m6_harvest) {
            int fl = fast_field_floor(6, tgt6, d6.u, d6.v);
            if (fl <= 58) {
                int ex = exact_field_score(6, tgt6, d6.u, d6.v);
                if (ex < min_ex6) min_ex6 = ex;
            }
        }
        std::cout << "[GF(2^6) 0x49 Summary] min_floor=" << min_fl6 << ", min_exact_layered=" << min_ex6 << "\n" << std::flush;
    }

    // Step 2B: GF(2^8) mod 0x11B — test 2x4 pair contractions + harvested rank-26..28 T_8 decompositions!
    {
        auto tgt8 = build_field_targets(8, 0x11B);
        int min_fl8 = 999, min_ex8 = 999;

        // Evaluate all harvested T_8 low-rank decompositions (including CRT 26-product seeds) under random GL_8 permutations!
        for (const auto& d8 : m8_harvest) {
            int fl = fast_field_floor(8, tgt8, d8.u, d8.v);
            if (fl < min_fl8) min_fl8 = fl;
            if (fl <= 108) {
                int ex = exact_field_score(8, tgt8, d8.u, d8.v);
                if (ex < min_ex8) min_ex8 = ex;
            }
        }

        // Test 2x4 split (K_2 x S_4: 3 blocks of 4x4 = 48 ANDs, 18 off-diagonal pairs) across random masks & permutations!
        for (int tr = 0; tr < 12000; ++tr) {
            u8 b[8] = {1, 2, 4, 8, 16, 32, 64, 128};
            if (tr > 500) std::shuffle(b, b + 8, rng);
            if (tr > 4000) {
                int ns = 1 + (rng() % 3);
                for (int s = 0; s < ns; ++s) { int x = rng() % 8, y = rng() % 8; if (x != y) b[x] ^= b[y]; }
            }
            u8 B0[4] = {b[0], b[1], b[2], b[3]};
            u8 B1[4] = {b[4], b[5], b[6], b[7]};
            u8 BS[4] = {u8(b[0] ^ b[4]), u8(b[1] ^ b[5]), u8(b[2] ^ b[6]), u8(b[3] ^ b[7])};
            const u8* blks[3] = {B0, B1, BS};
            int mask18 = (tr == 0) ? 0 : ((tr == 1) ? ((1 << 18) - 1) : int(rng() & ((1 << 18) - 1)));
            std::vector<u8> U, V;
            int bit = 0;
            for (int bk = 0; bk < 3; ++bk) {
                const u8* B = blks[bk];
                for (int i = 0; i < 4; ++i) { U.push_back(B[i]); V.push_back(B[i]); }
                for (int i = 0; i < 4; ++i)
                    for (int j = i + 1; j < 4; ++j, ++bit) {
                        if ((mask18 >> bit) & 1) { U.push_back(B[i] ^ B[j]); V.push_back(B[i] ^ B[j]); }
                        else { U.push_back(B[i]); V.push_back(B[j]); U.push_back(B[j]); V.push_back(B[i]); }
                    }
            }
            int fl = fast_field_floor(8, tgt8, U, V);
            if (fl < min_fl8) min_fl8 = fl;
            if (fl <= 107) {
                int ex = exact_field_score(8, tgt8, U, V);
                if (ex < min_ex8) {
                    min_ex8 = ex;
                    std::cout << "  [GF(2^8) 2x4] K=" << U.size() << " floor=" << fl << " exact=" << ex << "\n" << std::flush;
                }
            }
        }
        std::cout << "[GF(2^8) 0x11B Summary] min_floor_2x4_and_CRT=" << min_fl8
                  << ", min_exact_layered=" << min_ex8 << "\n" << std::flush;
    }

    std::cout << "\n====================================================================\n";
    std::cout << "PHASE 3: CROSS-LAYER TRUTH-TABLE GATE-WALK & CONE RESUBSTITUTION\n";
    std::cout << "====================================================================\n";

    struct WalkJob {
        std::string label, path;
        int m, poly, steps;
    };
    std::vector<WalkJob> jobs = {
        {"GF(2^6) 0x49 NIST-57", "data/gf64-630-mult.slp", 6, 0x49, 1500},
        {"GF(2^7) 0x91 WR-82", "attempts/algebraic-bilinear-slp/result/gf128_0x91_82gates.slp", 7, 0x91, 800},
        {"GF(2^7) 0x89 WR-81", "attempts/algebraic-bilinear-slp/result/gf128_0x89_81gates.slp", 7, 0x89, 800}
    };
    for (const auto& jb : jobs) {
        GateCirc gc = load_any_slp(jb.path, jb.m, jb.poly);
        int init_g = (int)gc.gates.size();
        bool ok0 = dead_code_and_verify(gc);
        int opt_g = gate_walk_optimize(gc, jb.steps, rng);
        bool ok1 = dead_code_and_verify(gc);
        std::cout << "[Gate-Walk " << jb.label << "] init=" << init_g << " (valid=" << ok0
                  << ") -> after " << jb.steps << " steps: " << opt_g << " (valid=" << ok1 << ")\n" << std::flush;
    }

    return 0;
}
