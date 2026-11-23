// synthesize_invsbox_gd10.cpp
// Exact Zero-NOT, Zero-Constant Gate-Depth-10 Synthesizer & Joint Gate-Minimizer for AES InvS-box.
// Searches over Galois Hits #1 ([7,12,4,9]) and #2 ([15,9,7,10]), inverter output polarities,
// thousands of exact Depth<=4 zero-NOT norm decompositions (maximizing shared Level-1/2 AND & XOR gates),
// and depth-bounded (<=7) Boyar-Peralta (RNBP) synthesis of all 32 bilinear affine forms L_{b,j}(x).

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <functional>
#include <random>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>

struct TT256 {
    uint64_t w[4];
    bool operator==(const TT256& o) const {
        return w[0] == o.w[0] && w[1] == o.w[1] && w[2] == o.w[2] && w[3] == o.w[3];
    }
    bool operator!=(const TT256& o) const { return !(*this == o); }
    bool is_zero() const { return (w[0] | w[1] | w[2] | w[3]) == 0; }
    int bit(int idx) const { return (int)((w[idx >> 6] >> (idx & 63)) & 1ULL); }
};

static inline TT256 tt_zero() { return {{0, 0, 0, 0}}; }
static inline TT256 tt_ones() { return {{~0ULL, ~0ULL, ~0ULL, ~0ULL}}; }
static inline TT256 tt_and(const TT256& a, const TT256& b) {
    return {{a.w[0] & b.w[0], a.w[1] & b.w[1], a.w[2] & b.w[2], a.w[3] & b.w[3]}};
}
static inline TT256 tt_xor(const TT256& a, const TT256& b) {
    return {{a.w[0] ^ b.w[0], a.w[1] ^ b.w[1], a.w[2] ^ b.w[2], a.w[3] ^ b.w[3]}};
}
static inline TT256 tt_xnor(const TT256& a, const TT256& b) {
    return {{~(a.w[0] ^ b.w[0]), ~(a.w[1] ^ b.w[1]), ~(a.w[2] ^ b.w[2]), ~(a.w[3] ^ b.w[3])}};
}
static inline TT256 tt_not(const TT256& a) {
    return {{~a.w[0], ~a.w[1], ~a.w[2], ~a.w[3]}};
}

struct TTHash {
    size_t operator()(const TT256& t) const noexcept {
        uint64_t h = t.w[0] * 0x9E3779B97F4A7C15ULL;
        h ^= t.w[1] * 0xBF58476D1CE4E5B9ULL;
        h ^= t.w[2] * 0x94D049BB133111EBULL;
        h ^= t.w[3] * 0xD6E8FEB86659FD93ULL;
        return static_cast<size_t>(h ^ (h >> 32));
    }
};

static uint8_t gf_mul(uint8_t a, uint8_t b) {
    uint8_t p = 0;
    for (int i = 0; i < 8; ++i) {
        if (b & 1) p ^= a;
        uint8_t hi = a & 0x80;
        a <<= 1;
        if (hi) a ^= 0x1B;
        b >>= 1;
    }
    return p;
}
static uint8_t gf_pow(uint8_t a, int e) {
    uint8_t r = 1;
    while (e > 0) {
        if (e & 1) r = gf_mul(r, a);
        a = gf_mul(a, a);
        e >>= 1;
    }
    return r;
}
static uint8_t fips_affine(uint8_t inv) {
    uint8_t y = 0;
    for (int i = 0; i < 8; ++i) {
        uint8_t bit = ((inv >> i) & 1) ^ ((inv >> ((i + 4) % 8)) & 1) ^
                      ((inv >> ((i + 5) % 8)) & 1) ^ ((inv >> ((i + 6) % 8)) & 1) ^
                      ((inv >> ((i + 7) % 8)) & 1) ^ ((0x63 >> i) & 1);
        y |= (bit << i);
    }
    return y;
}

struct D2Node {
    uint8_t op;    // 0=IN, 1=XOR, 2=XNOR, 3=AND
    uint8_t depth; // 0..2
    uint8_t ad;    // 0..1
    uint16_t u, v;
    TT256 tt;
};

struct NormCand {
    // target(pol=0) = leaf[0] ^ leaf[1] ^ leaf[2] ^ leaf[3] ^ top_flip
    // (if 3-leaf or 2-leaf, leaf indices are -1; here we represent as two D3 nodes L and R)
    uint8_t opL, opR; // 0=direct D2(u), 1=XOR(u,v), 2=XNOR(u,v)
    uint16_t Lu, Lv, Ru, Rv;
    uint8_t top_op_for_pol0; // 1=XOR(L,R), 2=XNOR(L,R)
    int and_count_est;
};

// Solve 256 x M linear system over GF(2): cols[0..M-1] * coeff = rhs
static bool solve_gf2_256(const std::vector<TT256>& cols, const TT256& rhs, std::vector<uint8_t>& coeff) {
    int M = (int)cols.size();
    // Transpose into 256 rows of bitmasks (M <= 64)
    uint64_t mat[256];
    uint8_t bvec[256];
    for (int r = 0; r < 256; ++r) {
        uint64_t row = 0;
        for (int c = 0; c < M; ++c) {
            if (cols[c].bit(r)) row |= (1ULL << c);
        }
        mat[r] = row;
        bvec[r] = (uint8_t)rhs.bit(r);
    }
    int piv_row_for_col[64];
    memset(piv_row_for_col, -1, sizeof(piv_row_for_col));
    int r = 0;
    for (int c = 0; c < M && r < 256; ++c) {
        int sel = -1;
        for (int i = r; i < 256; ++i) {
            if ((mat[i] >> c) & 1ULL) { sel = i; break; }
        }
        if (sel < 0) continue;
        std::swap(mat[r], mat[sel]);
        std::swap(bvec[r], bvec[sel]);
        piv_row_for_col[c] = r;
        for (int i = 0; i < 256; ++i) {
            if (i != r && ((mat[i] >> c) & 1ULL)) {
                mat[i] ^= mat[r];
                bvec[i] ^= bvec[r];
            }
        }
        r++;
    }
    for (int i = r; i < 256; ++i) {
        if (bvec[i] != 0) return false;
    }
    coeff.assign(M, 0);
    for (int c = 0; c < M; ++c) {
        if (piv_row_for_col[c] >= 0) coeff[c] = bvec[piv_row_for_col[c]];
    }
    return true;
}

struct OutGate {
    std::string op; // "AND", "XOR", "XNOR"
    int u, v;       // wire indices
    int gd, ad;
    TT256 tt;
};

int main(int argc, char** argv) {
    std::string out_g_path = (argc >= 2) ? argv[1] : "invsbox_gd10_bestG.circ.txt";
    std::string out_a_path = (argc >= 3) ? argv[2] : "invsbox_gd10_bestA.circ.txt";
    auto t0 = std::chrono::steady_clock::now();

    // 1. Build MSB-first inputs x0..x7 and target INVSBOX_OUT_TT[0..7]
    TT256 in_tt[8], inv_sbox_tt[8];
    for (int k = 0; k < 8; ++k) { in_tt[k] = tt_zero(); inv_sbox_tt[k] = tt_zero(); }

    uint8_t inv_sbox_byte[256];
    uint8_t inv_aff[256];
    for (int z = 0; z < 256; ++z) {
        uint8_t s = fips_affine(z == 0 ? 0 : gf_pow((uint8_t)z, 254));
        inv_sbox_byte[s] = (uint8_t)z;
        inv_aff[fips_affine((uint8_t)z)] = (uint8_t)z;
    }
    for (int val = 0; val < 256; ++val) {
        uint8_t out_v = inv_sbox_byte[val];
        for (int k = 0; k < 8; ++k) {
            int bp = 7 - k;
            if ((val >> bp) & 1) in_tt[k].w[val >> 6] |= (1ULL << (val & 63));
            if ((out_v >> bp) & 1) inv_sbox_tt[k].w[val >> 6] |= (1ULL << (val & 63));
        }
    }

    // 2. Build D<=2 zero-NOT pool (strictly u .= v, AD <= 1), keeping up to 6 realizations per TT256.
    std::vector<D2Node> pool;
    std::unordered_map<TT256, std::vector<int>, TTHash> seen;
    for (int k = 0; k < 8; ++k) {
        seen[in_tt[k]].push_back((int)pool.size());
        pool.push_back({0, 0, 0, (uint16_t)k, 0, in_tt[k]});
    }
    auto add_node = [&](uint8_t op, int u, int v, const TT256& t) {
        uint8_t d = std::max(pool[u].depth, pool[v].depth) + 1;
        uint8_t ad = std::max(pool[u].ad, pool[v].ad) + (op == 3 ? 1 : 0);
        if (d == 2 && ad > 1) return;
        auto& vec = seen[t];
        if (d == 1) {
            if (vec.empty()) {
                vec.push_back((int)pool.size());
                pool.push_back({op, d, ad, (uint16_t)u, (uint16_t)v, t});
            }
        } else {
            if (vec.size() < 6) {
                vec.push_back((int)pool.size());
                pool.push_back({op, d, ad, (uint16_t)u, (uint16_t)v, t});
            }
        }
    };
    int n0 = (int)pool.size();
    for (int i = 0; i < n0; ++i)
        for (int j = i + 1; j < n0; ++j) {
            add_node(1, i, j, tt_xor(pool[i].tt, pool[j].tt));
            add_node(2, i, j, tt_xnor(pool[i].tt, pool[j].tt));
            add_node(3, i, j, tt_and(pool[i].tt, pool[j].tt));
        }
    int n1 = (int)pool.size();
    for (int i = 0; i < n1; ++i)
        for (int j = i + 1; j < n1; ++j) {
            if (pool[i].depth == 0 && pool[j].depth == 0) continue;
            add_node(1, i, j, tt_xor(pool[i].tt, pool[j].tt));
            add_node(2, i, j, tt_xnor(pool[i].tt, pool[j].tt));
            add_node(3, i, j, tt_and(pool[i].tt, pool[j].tt));
        }
    int n2 = (int)pool.size();
    printf("D<=2 pool size: %d (n1=%d)\n", n2, n1);

    // Count ANDs inside a D2 node
    std::vector<std::vector<int>> node_ands(n2);
    for (int i = 0; i < n2; ++i) {
        std::set<int> s;
        if (pool[i].op != 0) {
            for (int a : node_ands[pool[i].u]) s.insert(a);
            for (int a : node_ands[pool[i].v]) s.insert(a);
            if (pool[i].op == 3) s.insert(i);
        }
        node_ands[i].assign(s.begin(), s.end());
    }

    // 3. Build D<=3 multimap (storing up to 6 lowest-AND pairs per D3 truth table so we get rich sharing.)
    struct D3Pair { uint8_t op; uint16_t u, v; uint8_t n_and; };
    std::unordered_map<TT256, std::vector<D3Pair>, TTHash> d3_multi;
    d3_multi.reserve(1 << 22);
    for (int i = 0; i < n2; ++i) {
        d3_multi[pool[i].tt].push_back({0, (uint16_t)i, 0, (uint8_t)node_ands[i].size()});
    }
    for (int i = 0; i < n2; ++i) {
        for (int j = i + 1; j < n2; ++j) {
            if (pool[i].depth <= 1 && pool[j].depth <= 1) continue;
            uint8_t na = (uint8_t)(node_ands[i].size() + node_ands[j].size());
            if (na > 3) continue;
            TT256 tx = tt_xor(pool[i].tt, pool[j].tt);
            auto& vec = d3_multi[tx];
            if (vec.size() < 48) vec.push_back({1, (uint16_t)i, (uint16_t)j, na});
        }
    }
    printf("D<=3 multimap keys: %zu\n", d3_multi.size());

    // 4. Construct norm coordinate truth tables matching our earlier basis4
    std::vector<uint8_t> gf16;
    for (int x = 1; x < 256; ++x) {
        uint8_t nm = gf_pow((uint8_t)x, 17);
        if (std::find(gf16.begin(), gf16.end(), nm) == gf16.end()) gf16.push_back(nm);
    }
    uint8_t basis4[4] = {0}, piv[4] = {0};
    int bc = 0;
    for (uint8_t e : gf16) {
        uint8_t v = e;
        for (int k = 0; k < bc; ++k) if ((v ^ piv[k]) < v) v ^= piv[k];
        if (v) {
            piv[bc] = v; basis4[bc] = e; bc++;
            std::sort(piv, piv + bc, std::greater<uint8_t>());
            if (bc == 4) break;
        }
    }
    uint8_t coord_map[256] = {0};
    for (int m = 0; m < 16; ++m) {
        uint8_t val = 0;
        for (int b = 0; b < 4; ++b) if ((m >> b) & 1) val ^= basis4[b];
        coord_map[val] = (uint8_t)m;
    }
    TT256 norm_mask_tt[16];
    for (int m = 0; m < 16; ++m) norm_mask_tt[m] = tt_zero();
    for (int x = 0; x < 256; ++x) {
        uint8_t z = inv_aff[x];
        uint8_t c4 = coord_map[z == 0 ? 0 : gf_pow(z, 17)];
        for (int m = 1; m < 16; ++m) {
            if (__builtin_parity(m & c4)) norm_mask_tt[m].w[x >> 6] |= (1ULL << (x & 63));
        }
    }

    // Collect candidate D4 decompositions for masks {4, 7, 9, 10, 12, 15}
    int needed_masks[6] = {4, 7, 9, 10, 12, 15};
    std::vector<NormCand> cands[16];
    std::vector<TT256> d3_keys;
    d3_keys.reserve(d3_multi.size());
    for (const auto& kv : d3_multi) d3_keys.push_back(kv.first);

    for (int mi = 0; mi < 6; ++mi) {
        int m = needed_masks[mi];
        TT256 targ = norm_mask_tt[m];
        TT256 tbar = tt_not(targ);
        for (const auto& u_tt : d3_keys) {
            for (int flip = 0; flip < 2; ++flip) {
                TT256 need = (flip == 0) ? tt_xor(targ, u_tt) : tt_xor(tbar, u_tt);
                if (!(u_tt.w[0] < need.w[0] || (u_tt.w[0] == need.w[0] && u_tt.w[1] < need.w[1]))) continue;
                auto itR = d3_multi.find(need);
                if (itR == d3_multi.end()) continue;
                const auto& vecL = d3_multi[u_tt];
                const auto& vecR = itR->second;
                for (const auto& pL : vecL) {
                    for (const auto& pR : vecR) {
                        int tot_a = pL.n_and + pR.n_and;
                        if (tot_a > 5) continue;
                        if (cands[m].size() < 4000) {
                            cands[m].push_back({pL.op, pR.op, pL.u, pL.v, pR.u, pR.v,
                                                (uint8_t)(flip == 0 ? 1 : 2), tot_a});
                        }
                    }
                }
            }
        }
        // Sort candidates by fewest ANDs first
        std::sort(cands[m].begin(), cands[m].end(), [](const NormCand& a, const NormCand& b) {
            return a.and_count_est < b.and_count_est;
        });
        printf("Mask %2d: collected %zu Depth<=4 zero-NOT candidates (min_and_est=%d)\n",
               m, cands[m].size(), cands[m].empty() ? -1 : cands[m][0].and_count_est);
    }

    // 5. Evaluate Galois Hit #1 ([7, 12, 4, 9]) and Galois Hit #2 ([15, 9, 7, 10])
    int galois_sets[2][4] = {{7, 12, 4, 9}, {15, 9, 7, 10}};

    int best_G = 999999;
    int best_A = 999999;
    std::vector<OutGate> best_circuit_G;
    std::array<int, 8> best_outs_G;
    std::vector<OutGate> best_circuit_A;
    std::array<int, 8> best_outs_A;

    std::mt19937 rng(20261117);

    for (int g_idx = 0; g_idx < 2; ++g_idx) {
        int m0 = galois_sets[g_idx][0];
        int m1 = galois_sets[g_idx][1];
        int m2 = galois_sets[g_idx][2];
        int m3 = galois_sets[g_idx][3];
        if (cands[m0].empty() || cands[m1].empty() || cands[m2].empty() || cands[m3].empty()) continue;

        // Compute exact truth tables of NIST's GF(2^4) inverter outputs (a20^t62, a21^t63, a22^t64, a23^t65)
        TT256 t49 = norm_mask_tt[m0], t50 = tt_not(t49);
        TT256 t51 = norm_mask_tt[m1];
        TT256 t52 = norm_mask_tt[m2], t53 = tt_not(t52);
        TT256 t54 = norm_mask_tt[m3], t55 = tt_not(t54);

        TT256 t60 = tt_xor(t49, t51);
        TT256 a16 = tt_and(t49, t51);
        TT256 a17 = tt_and(t50, t53);
        TT256 a18 = tt_and(t52, t55);
        TT256 a19 = tt_and(t51, t54);
        TT256 t62 = tt_xor(a17, a18);
        TT256 t63 = tt_xor(t60, a17);
        TT256 t64 = tt_xor(t52, a19);
        TT256 t65 = tt_xor(t54, a16);
        TT256 a20 = tt_and(a16, t55);
        TT256 a21 = tt_and(a19, t52);
        TT256 a22 = tt_and(a16, t52);
        TT256 a23 = tt_and(a18, t49);

        TT256 inv_raw[4] = {
            tt_xor(a20, t62),
            tt_xor(a21, t63),
            tt_xor(a22, t64),
            tt_xor(a23, t65)
        };

        // Precompute bilinear affine forms L_{b,j}(x) for each of the 16 inverter polarity masks pol_inv in 0..15
        struct PolSolution {
            bool valid;
            int pol_inv;
            uint16_t aff_mask[8][4]; // bit 0..7 = x0..x7, bit 8 = constant 1
            uint8_t out_xnor[8];     // 1 if Level-10 output gate is XNOR
        };
        std::vector<PolSolution> pol_sols;

        for (int pol_inv = 0; pol_inv < 16; ++pol_inv) {
            TT256 v[4];
            for (int j = 0; j < 4; ++j) {
                v[j] = ((pol_inv >> j) & 1) ? tt_not(inv_raw[j]) : inv_raw[j];
            }
            // Columns: for j=0..3: (x0&vj .. x7&vj, vj), plus col 36 = constant 1
            std::vector<TT256> cols;
            for (int j = 0; j < 4; ++j) {
                for (int i = 0; i < 8; ++i) cols.push_back(tt_and(in_tt[i], v[j]));
                cols.push_back(v[j]);
            }
            cols.push_back(tt_ones());

            PolSolution ps{};
            ps.valid = true;
            ps.pol_inv = pol_inv;
            for (int b = 0; b < 8; ++b) {
                std::vector<uint8_t> cf;
                if (!solve_gf2_256(cols, inv_sbox_tt[b], cf)) {
                    ps.valid = false;
                    break;
                }
                for (int j = 0; j < 4; ++j) {
                    uint16_t am = 0;
                    for (int i = 0; i < 8; ++i) if (cf[j * 9 + i]) am |= (1U << i);
                    if (cf[j * 9 + 8]) am |= (1U << 8);
                    ps.aff_mask[b][j] = am;
                }
                ps.out_xnor[b] = cf[36];
            }
            if (ps.valid) pol_sols.push_back(ps);
        }
        printf("Galois set #%d [%d,%d,%d,%d]: %zu / 16 inverter polarities give exact bilinear span.\n",
               g_idx + 1, m0, m1, m2, m3, pol_sols.size());
        if (pol_sols.empty()) continue;

        // Run 2,500 multi-start randomized joint optimizations of (4 norm trees + RNBP affine synthesis)
        int lim0 = std::min((int)cands[m0].size(), 4000);
        int lim1 = std::min((int)cands[m1].size(), 4000);
        int lim2 = std::min((int)cands[m2].size(), 4000);
        int lim3 = std::min((int)cands[m3].size(), 4000);

        for (int iter = 0; iter < 6000; ++iter) {
            int i0 = (iter == 0) ? 0 : (int)(rng() % lim0);
            int i1 = (iter == 0) ? 0 : (int)(rng() % lim1);
            int i2 = (iter == 0) ? 0 : (int)(rng() % lim2);
            int i3 = (iter == 0) ? 0 : (int)(rng() % lim3);
            const PolSolution& ps = pol_sols[iter % pol_sols.size()];

            // Assemble circuit DAG with automatic structural/truth-table CSE
            std::vector<OutGate> cg; // index 0..7 reserved as virtual inputs x0..x7
            std::unordered_map<TT256, int, TTHash> wire_by_tt;
            for (int k = 0; k < 8; ++k) {
                cg.push_back({"IN", -1, -1, 0, 0, in_tt[k]});
                wire_by_tt[in_tt[k]] = k;
            }

            auto emit_gate = [&](const std::string& op, int u, int v) -> int {
                TT256 t = (op == "AND") ? tt_and(cg[u].tt, cg[v].tt)
                        : (op == "XOR") ? tt_xor(cg[u].tt, cg[v].tt)
                                        : tt_xnor(cg[u].tt, cg[v].tt);
                int gd = std::max(cg[u].gd, cg[v].gd) + 1;
                int ad = std::max(cg[u].ad, cg[v].ad) + (op == "AND" ? 1 : 0);
                auto it = wire_by_tt.find(t);
                if (it != wire_by_tt.end() && cg[it->second].gd <= gd && cg[it->second].ad <= ad) {
                    return it->second;
                }
                int id = (int)cg.size();
                cg.push_back({op, u, v, gd, ad, t});
                if (it == wire_by_tt.end()) wire_by_tt[t] = id;
                return id;
            };

            std::function<int(int)> build_d2 = [&](int idx) -> int {
                const D2Node& nd = pool[idx];
                if (nd.op == 0) return (int)nd.u;
                int wu = build_d2(nd.u);
                int wv = build_d2(nd.v);
                std::string op = (nd.op == 1) ? "XOR" : (nd.op == 2) ? "XNOR" : "AND";
                return emit_gate(op, wu, wv);
            };

            auto build_d3 = [&](uint8_t op, uint16_t u, uint16_t v) -> int {
                if (op == 0) return build_d2(u);
                int wu = build_d2(u);
                int wv = build_d2(v);
                return emit_gate(op == 1 ? "XOR" : "XNOR", wu, wv);
            };

            const NormCand* sel[4] = {&cands[m0][i0], &cands[m1][i1], &cands[m2][i2], &cands[m3][i3]};
            int w_pol0[4], w_pol1[4];
            for (int q = 0; q < 4; ++q) {
                int wL = build_d3(sel[q]->opL, sel[q]->Lu, sel[q]->Lv);
                int wR = build_d3(sel[q]->opR, sel[q]->Ru, sel[q]->Rv);
                std::string op0 = (sel[q]->top_op_for_pol0 == 1) ? "XOR" : "XNOR";
                std::string op1 = (sel[q]->top_op_for_pol0 == 1) ? "XNOR" : "XOR";
                w_pol0[q] = emit_gate(op0, wL, wR);
                if (q != 1) w_pol1[q] = emit_gate(op1, wL, wR); // q==1 (t51) never needs pol=1.
            }

            // Emit 3-level GF(2^4) inverter (Levels 5, 6, 7)
            int wt60 = emit_gate("XOR", w_pol0[0], w_pol0[1]);
            int wa16 = emit_gate("AND", w_pol0[0], w_pol0[1]);
            int wa17 = emit_gate("AND", w_pol1[0], w_pol1[2]);
            int wa18 = emit_gate("AND", w_pol0[2], w_pol1[3]);
            int wa19 = emit_gate("AND", w_pol0[1], w_pol0[3]);

            int wt62 = emit_gate("XOR", wa17, wa18);
            int wt63 = emit_gate("XOR", wt60, wa17);
            int wt64 = emit_gate("XOR", w_pol0[2], wa19);
            int wt65 = emit_gate("XOR", w_pol0[3], wa16);

            int wa20 = emit_gate("AND", wa16, w_pol1[3]);
            int wa21 = emit_gate("AND", wa19, w_pol0[2]);
            int wa22 = emit_gate("AND", wa16, w_pol0[2]);
            int wa23 = emit_gate("AND", wa18, w_pol0[0]);

            int w_inv[4];
            int raw_pair[4][2] = {{wa20, wt62}, {wa21, wt63}, {wa22, wt64}, {wa23, wt65}};
            for (int j = 0; j < 4; ++j) {
                bool inv_flip = ((ps.pol_inv >> j) & 1) != 0;
                w_inv[j] = emit_gate(inv_flip ? "XNOR" : "XOR", raw_pair[j][0], raw_pair[j][1]);
            }

            // Collect all pure-affine wires (9-bit mask: bit 0..7 = x0..x7, bit 8 = const 1) already in cg with gd <= 7
            std::unordered_map<uint16_t, int> aff_wire;
            for (int id = 0; id < (int)cg.size(); ++id) {
                if (cg[id].ad == 0 && cg[id].gd <= 7) {
                    // Check if cg[id].tt is affine (it is since ad == 0.)
                    uint16_t mask = 0;
                    int c0 = cg[id].tt.bit(0);
                    if (c0) mask |= (1U << 8);
                    for (int k = 0; k < 8; ++k) {
                        int x_single = 1 << (7 - k);
                        if ((cg[id].tt.bit(x_single) ^ c0) != 0) mask |= (1U << k);
                    }
                    if (aff_wire.find(mask) == aff_wire.end() || cg[id].gd < cg[aff_wire[mask]].gd) {
                        aff_wire[mask] = id;
                    }
                }
            }

            // Determine remaining needed 9-bit affine masks among ps.aff_mask[b][j]
            std::vector<uint16_t> targets_aff;
            for (int b = 0; b < 8; ++b) {
                for (int j = 0; j < 4; ++j) {
                    uint16_t am = ps.aff_mask[b][j];
                    if (am == 0 || am == (1U << 8)) continue;
                    // Also note: if ~am is already in aff_wire? No, AND(1^L, v) .= AND(L, v), we need exact am.
                    if (aff_wire.find(am) == aff_wire.end()) {
                        if (std::find(targets_aff.begin(), targets_aff.end(), am) == targets_aff.end()) {
                            targets_aff.push_back(am);
                        }
                    }
                }
            }

            // Depth-bounded (<= 7) RNBP / greedy pair-sharing synthesis of targets_aff over 9-bit affine space.
            // Note: XOR(mA, mB) = mA ^ mB; XNOR(mA, mB) = mA ^ mB ^ 256.
            // So we track linear 8-bit base masks in aff_wire: if EITHER m or (m^256) is needed,
            // XNOR gives the flipped constant bit in ONE gate.
            while (!targets_aff.empty()) {
                // Check if any target can be made in 1 step (XOR or XNOR of two existing aff_wire entries with gd <= 6)
                int best_t_idx = -1;
                std::string best_op;
                int best_u = -1, best_v = -1;
                for (int ti = 0; ti < (int)targets_aff.size(); ++ti) {
                    uint16_t tm = targets_aff[ti];
                    for (const auto& kv1 : aff_wire) {
                        if (cg[kv1.second].gd > 6) continue;
                        uint16_t need_xor = tm ^ kv1.first;
                        auto itx = aff_wire.find(need_xor);
                        if (itx != aff_wire.end() && itx->second != kv1.second && cg[itx->second].gd <= 6) {
                            best_t_idx = ti; best_op = "XOR"; best_u = kv1.second; best_v = itx->second; break;
                        }
                        uint16_t need_xnor = tm ^ kv1.first ^ 256U;
                        auto itxn = aff_wire.find(need_xnor);
                        if (itxn != aff_wire.end() && itxn->second != kv1.second && cg[itxn->second].gd <= 6) {
                            best_t_idx = ti; best_op = "XNOR"; best_u = kv1.second; best_v = itxn->second; break;
                        }
                    }
                    if (best_t_idx >= 0) break;
                }
                if (best_t_idx >= 0) {
                    int wid = emit_gate(best_op, best_u, best_v);
                    uint16_t tm = targets_aff[best_t_idx];
                    aff_wire[tm] = wid;
                    targets_aff.erase(targets_aff.begin() + best_t_idx);
                    continue;
                }

                // Otherwise, pick a candidate pair (u, v) at gd <= 5 that maximizes coverage/overlap toward remaining targets.
                std::vector<std::pair<uint16_t, int>> avail;
                for (const auto& kv : aff_wire) {
                    if (cg[kv.second].gd <= 5) avail.push_back(kv);
                }
                int best_score = -1;
                uint16_t add_m = 0;
                std::string add_op = "XOR";
                int add_u = -1, add_v = -1;

                for (size_t a = 0; a < avail.size(); ++a) {
                    for (size_t b = a + 1; b < avail.size(); ++b) {
                        for (int use_xnor = 0; use_xnor < 2; ++use_xnor) {
                            uint16_t cand_m = avail[a].first ^ avail[b].first ^ (use_xnor ? 256U : 0U);
                            if (cand_m == 0 || aff_wire.find(cand_m) != aff_wire.end()) continue;
                            // Score: how many targets_aff become 1-step reachable, plus bit-overlap reduction
                            int sc = 0;
                            uint8_t lin_c = (uint8_t)(cand_m & 0xFF);
                            for (uint16_t tm : targets_aff) {
                                if (aff_wire.count(tm ^ cand_m) || aff_wire.count(tm ^ cand_m ^ 256U)) {
                                    sc += 100;
                                } else if (lin_c != 0 && ((tm & lin_c) == lin_c)) {
                                    sc += 10 * __builtin_popcount(lin_c);
                                }
                            }
                            if (sc > 0) sc += (int)(rng() % 45); // wider RNBP exploration.
                            if (sc > best_score) {
                                best_score = sc;
                                add_m = cand_m;
                                add_op = use_xnor ? "XNOR" : "XOR";
                                add_u = avail[a].second;
                                add_v = avail[b].second;
                            }
                        }
                    }
                }
                int wid = emit_gate(add_op, add_u, add_v);
                aff_wire[add_m] = wid;
            }

            // Emit Level 8 (32 ANDs), Level 9 (16 XORs), Level 10 (8 XOR/XNORs)
            std::array<int, 8> out_wires;
            bool depth_ok = true;
            for (int b = 0; b < 8; ++b) {
                std::vector<int> prod_terms;
                for (int j = 0; j < 4; ++j) {
                    uint16_t am = ps.aff_mask[b][j];
                    if (am == 0) continue;
                    if (am == 256U) {
                        prod_terms.push_back(w_inv[j]);
                    } else {
                        int lw = aff_wire[am];
                        int pw = emit_gate("AND", lw, w_inv[j]);
                        prod_terms.push_back(pw);
                    }
                }
                while (prod_terms.size() > 2) {
                    std::vector<int> nxt;
                    for (size_t k = 0; k + 1 < prod_terms.size(); k += 2) {
                        nxt.push_back(emit_gate("XOR", prod_terms[k], prod_terms[k + 1]));
                    }
                    if (prod_terms.size() % 2 == 1) nxt.push_back(prod_terms.back());
                    prod_terms = nxt;
                }
                int final_w = -1;
                if (prod_terms.size() == 2) {
                    final_w = emit_gate(ps.out_xnor[b] ? "XNOR" : "XOR", prod_terms[0], prod_terms[1]);
                } else {
                    depth_ok = false; break;
                }
                if (cg[final_w].gd > 10 || cg[final_w].tt != inv_sbox_tt[b]) {
                    depth_ok = false; break;
                }
                out_wires[b] = final_w;
            }
            if (!depth_ok) continue;

            // Dead-gate sweep to retain ONLY live gates feeding out_wires[0..7].
            std::vector<uint8_t> live(cg.size(), 0);
            for (int b = 0; b < 8; ++b) live[out_wires[b]] = 1;
            for (int id = (int)cg.size() - 1; id >= 8; --id) {
                if (live[id]) {
                    live[cg[id].u] = 1;
                    live[cg[id].v] = 1;
                }
            }
            std::vector<int> remap(cg.size(), -1);
            std::vector<OutGate> clean;
            for (int k = 0; k < 8; ++k) { remap[k] = k; clean.push_back(cg[k]); }
            int cnt_A = 0, cnt_G = 0, max_gd = 0, max_ad = 0;
            for (int id = 8; id < (int)cg.size(); ++id) {
                if (!live[id]) continue;
                OutGate g = cg[id];
                g.u = remap[g.u];
                g.v = remap[g.v];
                g.gd = std::max(clean[g.u].gd, clean[g.v].gd) + 1;
                g.ad = std::max(clean[g.u].ad, clean[g.v].ad) + (g.op == "AND" ? 1 : 0);
                remap[id] = (int)clean.size();
                clean.push_back(g);
                cnt_G++;
                if (g.op == "AND") cnt_A++;
                if (g.gd > max_gd) max_gd = g.gd;
                if (g.ad > max_ad) max_ad = g.ad;
            }
            if (max_gd > 10) continue;
            std::array<int, 8> clean_outs;
            for (int b = 0; b < 8; ++b) clean_outs[b] = remap[out_wires[b]];

            if (cnt_G < best_G || (cnt_G == best_G && cnt_A < (int)std::count_if(best_circuit_G.begin()+8, best_circuit_G.end(), [](const OutGate& x){return x.op=="AND";}))) {
                best_G = cnt_G;
                best_circuit_G = clean;
                best_outs_G = clean_outs;
                printf("  [NEW MIN-G @ GD=%d] G=%d, A=%d, AD=%d (galois=#%d, iter=%d, pol_inv=%d)\n",
                       max_gd, cnt_G, cnt_A, max_ad, g_idx + 1, iter, ps.pol_inv);
            }
            if (cnt_A < best_A || (cnt_A == best_A && cnt_G < (int)best_circuit_A.size() - 8)) {
                best_A = cnt_A;
                best_circuit_A = clean;
                best_outs_A = clean_outs;
                printf("  [NEW MIN-A @ GD=%d] A=%d, G=%d, AD=%d (galois=#%d, iter=%d, pol_inv=%d)\n",
                       max_gd, cnt_A, cnt_G, max_ad, g_idx + 1, iter, ps.pol_inv);
            }
        }
    }

    auto write_ncff = [&](const std::string& path, const std::vector<OutGate>& circ, const std::array<int, 8>& outs) {
        if (circ.empty()) return;
        int A = 0, XOR_c = 0, XNOR_c = 0, GD = 0, AD = 0;
        for (size_t i = 8; i < circ.size(); ++i) {
            if (circ[i].op == "AND") A++;
            else if (circ[i].op == "XOR") XOR_c++;
            else XNOR_c++;
            GD = std::max(GD, circ[i].gd);
            AD = std::max(AD, circ[i].ad);
        }
        int G = A + XOR_c + XNOR_c;
        char cname[128];
        snprintf(cname, sizeof(cname), "aes-invsbox-a%d-ad%d-g%d-gd%d-xx%d-%d",
                 A, AD, G, GD, XOR_c + XNOR_c, XNOR_c);

        std::vector<std::string> wname(circ.size());
        for (int k = 0; k < 8; ++k) wname[k] = "x" + std::to_string(k);
        std::unordered_map<int, int> out_idx;
        for (int b = 0; b < 8; ++b) out_idx[outs[b]] = b;
        int a_id = 0, t_id = 0;
        for (size_t i = 8; i < circ.size(); ++i) {
            if (out_idx.count((int)i)) {
                wname[i] = "y" + std::to_string(out_idx[(int)i]);
            } else if (circ[i].op == "AND") {
                wname[i] = "a" + std::to_string(++a_id);
            } else {
                wname[i] = "t" + std::to_string(++t_id);
            }
        }
        std::ofstream f(path);
        f << "%NCFF-0.1-2026 (NIST Circuit File Format)\n\n";
        f << "## Index of circuits (circuitName numOutputs numInputs)\n";
        f << "  % " << cname << " 8 8\n\n";
        f << "## Circuit\n";
        f << "begin circuit " << cname << "\n";
        f << "  % Description: AES Sbox Inverse, compatible with NIST-FIPS 197\n";
        f << "  % Tally of gates (" << G << "): " << A << " AND; " << XOR_c << " XOR; " << XNOR_c << " XNOR\n";
        f << "  % Gate depth " << GD << "; AND depth " << AD << "\n\n";
        f << "Inputs: x0:x7\n";
        f << "Outputs: y0:y7\n";
        f << "Internal: a1:a" << a_id << " t1:t" << t_id << "\n";
        f << "GateSyntax: GateName Output Inputs\n\n";
        f << "begin SLP\n";
        for (size_t i = 8; i < circ.size(); ++i) {
            f << circ[i].op << " " << wname[i] << " " << wname[circ[i].u] << " " << wname[circ[i].v] << "\n";
        }
        f << "end SLP\nend circuit\n";
        printf("Wrote %s (%s)\n", path.c_str(), cname);
    };

    write_ncff(out_g_path, best_circuit_G, best_outs_G);
    write_ncff(out_a_path, best_circuit_A, best_outs_A);

    double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    printf("Finished in %.3f s\n", sec);
    return 0;
}
