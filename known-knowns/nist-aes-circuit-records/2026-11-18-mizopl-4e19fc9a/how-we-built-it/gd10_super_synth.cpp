// gd10_super_synth.cpp
// Coordinate-Descent Norm-Sharing + Exact Quotient-GF(2)^8 Affine RNBP Synthesizer
// for Zero-NOT, Zero-Constant Gate-Depth-10 AES InvS-box ({AND, XOR, XNOR} strictly).
// Multi-threaded coordinate-descent + quotient-GF(2)^8 RNBP synthesizer at GD = 10.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <functional>
#include <mutex>
#include <random>
#include <set>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

struct TT256 {
    uint64_t w[4];
    bool operator==(const TT256& o) const {
        return w[0] == o.w[0] && w[1] == o.w[1] && w[2] == o.w[2] && w[3] == o.w[3];
    }
    bool operator!=(const TT256& o) const { return !(*this == o); }
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
        return (size_t)(h ^ (h >> 32));
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
    while (e > 0) { if (e & 1) r = gf_mul(r, a); a = gf_mul(a, a); e >>= 1; }
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
    uint8_t opL, opR;
    uint16_t Lu, Lv, Ru, Rv;
    uint8_t top_op_for_pol0;
    int and_count_est;
};

struct OutGate {
    uint8_t op; // 0=IN, 1=XOR, 2=XNOR, 3=AND
    int u, v;
    int gd, ad;
    TT256 tt;
};

static bool solve_gf2_256(const std::vector<TT256>& cols, const TT256& rhs, std::vector<uint8_t>& coeff) {
    int M = (int)cols.size();
    uint64_t mat[256];
    uint8_t bvec[256];
    for (int r = 0; r < 256; ++r) {
        uint64_t row = 0;
        for (int c = 0; c < M; ++c) if (cols[c].bit(r)) row |= (1ULL << c);
        mat[r] = row;
        bvec[r] = (uint8_t)rhs.bit(r);
    }
    int piv_row[64];
    memset(piv_row, -1, sizeof(piv_row));
    int r = 0;
    for (int c = 0; c < M && r < 256; ++c) {
        int sel = -1;
        for (int i = r; i < 256; ++i) if ((mat[i] >> c) & 1ULL) { sel = i; break; }
        if (sel < 0) continue;
        std::swap(mat[r], mat[sel]);
        std::swap(bvec[r], bvec[sel]);
        piv_row[c] = r;
        for (int i = 0; i < 256; ++i) {
            if (i != r && ((mat[i] >> c) & 1ULL)) { mat[i] ^= mat[r]; bvec[i] ^= bvec[r]; }
        }
        r++;
    }
    for (int i = r; i < 256; ++i) if (bvec[i] != 0) return false;
    coeff.assign(M, 0);
    for (int c = 0; c < M; ++c) if (piv_row[c] >= 0) coeff[c] = bvec[piv_row[c]];
    return true;
}

static void write_ncff(const std::string& path, const std::vector<OutGate>& circ, const std::array<int, 8>& outs) {
    if (circ.empty()) return;
    int A = 0, XOR_c = 0, XNOR_c = 0, GD = 0, AD = 0;
    for (size_t i = 8; i < circ.size(); ++i) {
        if (circ[i].op == 3) A++;
        else if (circ[i].op == 1) XOR_c++;
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
        if (out_idx.count((int)i)) wname[i] = "y" + std::to_string(out_idx[(int)i]);
        else if (circ[i].op == 3) wname[i] = "a" + std::to_string(++a_id);
        else wname[i] = "t" + std::to_string(++t_id);
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
        const char* op_s = (circ[i].op == 1) ? "XOR" : (circ[i].op == 2) ? "XNOR" : "AND";
        f << op_s << " " << wname[i] << " " << wname[circ[i].u] << " " << wname[circ[i].v] << "\n";
    }
    f << "end SLP\nend circuit\n";
}

int main(int argc, char** argv) {
    auto t0 = std::chrono::steady_clock::now();
    std::string out_dir = (argc >= 2) ? argv[1] : ".";
    double budget_sec = (argc >= 3) ? std::stod(argv[2]) : 22.0;

    TT256 in_tt[8], inv_sbox_tt[8];
    for (int k = 0; k < 8; ++k) { in_tt[k] = tt_zero(); inv_sbox_tt[k] = tt_zero(); }
    uint8_t inv_sbox_byte[256], inv_aff[256];
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

    // Build larger D<=2 zero-NOT pool (up to 16 realizations per TT256 so sharing across norm & aff is much richer.)
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
            if (vec.size() < 12) {
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

    struct D3Pair { uint8_t op; uint16_t u, v; uint8_t n_and; };
    std::unordered_map<TT256, std::vector<D3Pair>, TTHash> d3_multi;
    d3_multi.reserve(1 << 20);
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
            if (vec.size() < 64) vec.push_back({1, (uint16_t)i, (uint16_t)j, na});
        }
    }

    // Norm truth tables
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
                for (const auto& pL : d3_multi[u_tt]) {
                    for (const auto& pR : itR->second) {
                        int tot_a = pL.n_and + pR.n_and;
                        if (tot_a > 5) continue;
                        if (cands[m].size() < 12000) {
                            cands[m].push_back({pL.op, pR.op, pL.u, pL.v, pR.u, pR.v,
                                                (uint8_t)(flip == 0 ? 1 : 2), tot_a});
                        }
                    }
                }
            }
        }
        std::sort(cands[m].begin(), cands[m].end(), [](const NormCand& a, const NormCand& b) {
            return a.and_count_est < b.and_count_est;
        });
        printf("Mask %2d: %zu candidates\n", m, cands[m].size());
    }

    // All 8 cyclic rotations of the two normal bases [7,12,4,9] and [15,9,7,10].
    int base_sets[2][4] = {{7, 12, 4, 9}, {15, 9, 7, 10}};
    struct BasisConfig {
        int m[4];
        int pol_inv;
        uint16_t aff_mask[8][4];
        uint8_t out_xnor[8];
    };
    std::vector<BasisConfig> configs;

    for (int g = 0; g < 2; ++g) {
        for (int rot = 0; rot < 4; ++rot) {
            int m0 = base_sets[g][rot], m1 = base_sets[g][(rot + 1) & 3];
            int m2 = base_sets[g][(rot + 2) & 3], m3 = base_sets[g][(rot + 3) & 3];

            TT256 t49 = norm_mask_tt[m0], t50 = tt_not(t49);
            TT256 t51 = norm_mask_tt[m1];
            TT256 t52 = norm_mask_tt[m2], t53 = tt_not(t52);
            TT256 t54 = norm_mask_tt[m3], t55 = tt_not(t54);

            TT256 t60 = tt_xor(t49, t51);
            TT256 a16 = tt_and(t49, t51), a17 = tt_and(t50, t53), a18 = tt_and(t52, t55), a19 = tt_and(t51, t54);
            TT256 t62 = tt_xor(a17, a18), t63 = tt_xor(t60, a17), t64 = tt_xor(t52, a19), t65 = tt_xor(t54, a16);
            TT256 a20 = tt_and(a16, t55), a21 = tt_and(a19, t52), a22 = tt_and(a16, t52), a23 = tt_and(a18, t49);
            TT256 inv_raw[4] = {tt_xor(a20, t62), tt_xor(a21, t63), tt_xor(a22, t64), tt_xor(a23, t65)};

            for (int pol_inv = 0; pol_inv < 16; ++pol_inv) {
                TT256 v[4];
                for (int j = 0; j < 4; ++j) v[j] = ((pol_inv >> j) & 1) ? tt_not(inv_raw[j]) : inv_raw[j];
                std::vector<TT256> cols;
                for (int j = 0; j < 4; ++j) {
                    for (int i = 0; i < 8; ++i) cols.push_back(tt_and(in_tt[i], v[j]));
                    cols.push_back(v[j]);
                }
                cols.push_back(tt_ones());

                BasisConfig bc_item{};
                bc_item.m[0] = m0; bc_item.m[1] = m1; bc_item.m[2] = m2; bc_item.m[3] = m3;
                bc_item.pol_inv = pol_inv;
                bool ok = true;
                for (int b = 0; b < 8; ++b) {
                    std::vector<uint8_t> cf;
                    if (!solve_gf2_256(cols, inv_sbox_tt[b], cf)) { ok = false; break; }
                    for (int j = 0; j < 4; ++j) {
                        uint16_t am = 0;
                        for (int i = 0; i < 8; ++i) if (cf[j * 9 + i]) am |= (1U << i);
                        if (cf[j * 9 + 8]) am |= (1U << 8);
                        bc_item.aff_mask[b][j] = am;
                    }
                    bc_item.out_xnor[b] = cf[36];
                }
                if (ok) configs.push_back(bc_item);
            }
        }
    }
    printf("Total valid (normal_basis_rotation, pol_inv) configs: %zu\n", configs.size());
    fflush(stdout);

    // Evaluation function for a given (cfg_idx, idx[4], rnbp_seed) using EXACT GF(2)^8 quotient RNBP at GD <= 7.
    auto evaluate_tuple = [&](const BasisConfig& cfg, const int idx[4], std::mt19937& rng, int n_aff_runs,
                              std::vector<OutGate>& out_circ, std::array<int, 8>& out_outs,
                              int& ret_G, int& ret_A) -> bool {
        std::vector<OutGate> prefix;
        std::unordered_map<TT256, int, TTHash> wire_by_tt;
        for (int k = 0; k < 8; ++k) {
            prefix.push_back({0, -1, -1, 0, 0, in_tt[k]});
            wire_by_tt[in_tt[k]] = k;
        }
        auto emit_p = [&](uint8_t op, int u, int v) -> int {
            TT256 t = (op == 3) ? tt_and(prefix[u].tt, prefix[v].tt)
                    : (op == 1) ? tt_xor(prefix[u].tt, prefix[v].tt)
                                : tt_xnor(prefix[u].tt, prefix[v].tt);
            int gd = std::max(prefix[u].gd, prefix[v].gd) + 1;
            int ad = std::max(prefix[u].ad, prefix[v].ad) + (op == 3 ? 1 : 0);
            auto it = wire_by_tt.find(t);
            if (it != wire_by_tt.end() && prefix[it->second].gd <= gd && prefix[it->second].ad <= ad) {
                return it->second;
            }
            int id = (int)prefix.size();
            prefix.push_back({op, u, v, gd, ad, t});
            if (it == wire_by_tt.end() || gd < prefix[it->second].gd) wire_by_tt[t] = id;
            return id;
        };

        std::function<int(int)> build_d2 = [&](int p_idx) -> int {
            const D2Node& nd = pool[p_idx];
            if (nd.op == 0) return (int)nd.u;
            int wu = build_d2(nd.u);
            int wv = build_d2(nd.v);
            return emit_p(nd.op, wu, wv);
        };
        auto build_d3 = [&](uint8_t op, uint16_t u, uint16_t v) -> int {
            if (op == 0) return build_d2(u);
            return emit_p(op, build_d2(u), build_d2(v));
        };

        int w_pol0[4], w_pol1[4];
        for (int q = 0; q < 4; ++q) {
            const NormCand& nc = cands[cfg.m[q]][idx[q]];
            int wL = build_d3(nc.opL, nc.Lu, nc.Lv);
            int wR = build_d3(nc.opR, nc.Ru, nc.Rv);
            uint8_t op0 = nc.top_op_for_pol0;
            uint8_t op1 = (op0 == 1) ? 2 : 1;
            w_pol0[q] = emit_p(op0, wL, wR);
            if (q != 1) w_pol1[q] = emit_p(op1, wL, wR);
        }

        int wt60 = emit_p(1, w_pol0[0], w_pol0[1]);
        int wa16 = emit_p(3, w_pol0[0], w_pol0[1]);
        int wa17 = emit_p(3, w_pol1[0], w_pol1[2]);
        int wa18 = emit_p(3, w_pol0[2], w_pol1[3]);
        int wa19 = emit_p(3, w_pol0[1], w_pol0[3]);
        int wt62 = emit_p(1, wa17, wa18);
        int wt63 = emit_p(1, wt60, wa17);
        int wt64 = emit_p(1, w_pol0[2], wa19);
        int wt65 = emit_p(1, w_pol0[3], wa16);
        int wa20 = emit_p(3, wa16, w_pol1[3]);
        int wa21 = emit_p(3, wa19, w_pol0[2]);
        int wa22 = emit_p(3, wa16, w_pol0[2]);
        int wa23 = emit_p(3, wa18, w_pol0[0]);
        int raw_pair[4][2] = {{wa20, wt62}, {wa21, wt63}, {wa22, wt64}, {wa23, wt65}};
        int w_inv[4];
        for (int j = 0; j < 4; ++j) {
            bool flip = ((cfg.pol_inv >> j) & 1) != 0;
            w_inv[j] = emit_p(flip ? 2 : 1, raw_pair[j][0], raw_pair[j][1]);
            if (prefix[w_inv[j]].gd > 7) return false;
        }

        // Extract all pure-affine wires already in `prefix` with gd <= 7.
        int existing_mc[256][2];
        memset(existing_mc, -1, sizeof(existing_mc));
        uint8_t base_lin_dep[256];
        memset(base_lin_dep, 99, sizeof(base_lin_dep));
        int base_lin_wire[256];
        uint8_t base_lin_cst[256];
        memset(base_lin_wire, -1, sizeof(base_lin_wire));

        for (int id = 0; id < (int)prefix.size(); ++id) {
            if (prefix[id].ad == 0 && prefix[id].gd <= 7) {
                uint8_t lm = 0;
                int c0 = prefix[id].tt.bit(0);
                for (int k = 0; k < 8; ++k) {
                    if ((prefix[id].tt.bit(1 << (7 - k)) ^ c0) != 0) lm |= (uint8_t)(1u << k);
                }
                if (lm == 0) continue;
                if (existing_mc[lm][c0] < 0 || prefix[id].gd < prefix[existing_mc[lm][c0]].gd) {
                    existing_mc[lm][c0] = id;
                }
                if (prefix[id].gd < base_lin_dep[lm]) {
                    base_lin_dep[lm] = (uint8_t)prefix[id].gd;
                    base_lin_wire[lm] = id;
                    base_lin_cst[lm] = (uint8_t)c0;
                }
            }
        }

        // Determine required 8-bit linear masks and polarities among cfg.aff_mask[b][j]
        uint8_t req_cst0[256] = {0}, req_cst1[256] = {0};
        std::vector<uint8_t> lin_targets;
        for (int b = 0; b < 8; ++b) {
            for (int j = 0; j < 4; ++j) {
                uint16_t am = cfg.aff_mask[b][j];
                if (am == 0 || am == 256U) continue;
                uint8_t lm = (uint8_t)(am & 0xFF);
                uint8_t c = (uint8_t)(am >> 8);
                if (c == 0) req_cst0[lm] = 1; else req_cst1[lm] = 1;
                if (base_lin_wire[lm] < 0) {
                    if (std::find(lin_targets.begin(), lin_targets.end(), lm) == lin_targets.end()) {
                        lin_targets.push_back(lm);
                    }
                }
            }
        }

        // Run `n_aff_runs` Exact-Distance GF(2)^8 RNBP runs (respecting gd <= 7.)
        int best_G_local = 9999, best_A_local = 9999;
        for (int r = 0; r < n_aff_runs; ++r) {
            std::vector<OutGate> cg = prefix;
            int mc_w[256][2];
            memcpy(mc_w, existing_mc, sizeof(mc_w));

            std::vector<uint8_t> S_masks;
            std::vector<int> S_wires;
            std::vector<uint8_t> S_csts;
            std::vector<int> S_deps;
            uint8_t len_B[256];
            for (int v = 0; v < 256; ++v) len_B[v] = (uint8_t)__builtin_popcount(v);
            bool in_S[256] = {false};

            for (int m = 1; m < 256; ++m) {
                if (base_lin_wire[m] >= 0) {
                    in_S[m] = true;
                    S_masks.push_back((uint8_t)m);
                    S_wires.push_back(base_lin_wire[m]);
                    S_csts.push_back(base_lin_cst[m]);
                    S_deps.push_back(base_lin_dep[m]);
                    if (len_B[m] > 1) {
                        len_B[m] = 1;
                        uint32_t bit = m & -m;
                        for (uint32_t blk = 0; blk < 256; blk += (bit << 1)) {
                            for (uint32_t i = blk; i < blk + bit; ++i) {
                                uint32_t j = i ^ m;
                                if (len_B[j] + 1 < len_B[i]) len_B[i] = len_B[j] + 1;
                                if (len_B[i] + 1 < len_B[j]) len_B[j] = len_B[i] + 1;
                            }
                        }
                    }
                }
            }

            std::vector<uint8_t> rem = lin_targets;
            bool ok_run = true;
            while (!rem.empty()) {
                // Check distance-1 targets buildable at gd <= 7.
                std::vector<int> quick;
                for (size_t u = 0; u < rem.size(); ++u) {
                    uint8_t t = rem[u];
                    if (len_B[t] == 2) {
                        for (size_t i = 0; i < S_masks.size(); ++i) {
                            if (S_deps[i] > 6) continue;
                            uint8_t partner = t ^ S_masks[i];
                            if (in_S[partner]) {
                                auto it = std::find(S_masks.begin(), S_masks.end(), partner);
                                size_t j = (size_t)(it - S_masks.begin());
                                if (j != i && S_deps[j] <= 6) { quick.push_back((int)u); break; }
                            }
                        }
                    }
                }

                uint8_t chosen_m = 0;
                int chosen_a = -1, chosen_b = -1;
                if (!quick.empty()) {
                    uint8_t t = rem[quick[rng() % quick.size()]];
                    int best_d = 99;
                    for (size_t i = 0; i < S_masks.size(); ++i) {
                        if (S_deps[i] > 6) continue;
                        for (size_t j = i + 1; j < S_masks.size(); ++j) {
                            if (S_deps[j] > 6) continue;
                            if ((S_masks[i] ^ S_masks[j]) == t) {
                                int d = std::max(S_deps[i], S_deps[j]) + 1;
                                if (d < best_d) { best_d = d; chosen_m = t; chosen_a = (int)i; chosen_b = (int)j; }
                            }
                        }
                    }
                }
                if (chosen_a < 0) {
                    struct Cand { uint8_t m; int a, b, drop, norm2, dep; };
                    std::vector<Cand> cs;
                    int max_drop = -1;
                    for (size_t i = 0; i < S_masks.size(); ++i) {
                        if (S_deps[i] > 5) continue; // intermediate wire needs gd <= 6 to feed another XOR.
                        for (size_t j = i + 1; j < S_masks.size(); ++j) {
                            if (S_deps[j] > 5) continue;
                            uint8_t cm = S_masks[i] ^ S_masks[j];
                            if (cm == 0 || in_S[cm]) continue;
                            int drop = 0, norm2 = 0;
                            for (uint8_t t : rem) {
                                int ol = len_B[t];
                                int nl = std::min(ol, 1 + (int)len_B[t ^ cm]);
                                drop += (ol - nl);
                                norm2 += (nl - 1) * (nl - 1);
                            }
                            if (drop <= 0) continue;
                            if (drop > max_drop) max_drop = drop;
                            cs.push_back({cm, (int)i, (int)j, drop, norm2, std::max(S_deps[i], S_deps[j]) + 1});
                        }
                    }
                    if (cs.empty()) { ok_run = false; break; }
                    bool use_norm = (rng() & 1) != 0;
                    int bn = -1;
                    if (use_norm) for (auto& x : cs) if (x.drop == max_drop && x.norm2 > bn) bn = x.norm2;
                    std::vector<int> pool_idx;
                    for (size_t k = 0; k < cs.size(); ++k) {
                        if (cs[k].drop == max_drop && (!use_norm || cs[k].norm2 == bn)) pool_idx.push_back((int)k);
                    }
                    int pk = pool_idx[rng() % pool_idx.size()];
                    chosen_m = cs[pk].m; chosen_a = cs[pk].a; chosen_b = cs[pk].b;
                }

                uint8_t want_c = (req_cst1[chosen_m] && !req_cst0[chosen_m]) ? 1 : 0;
                uint8_t op = ((S_csts[chosen_a] ^ S_csts[chosen_b]) == want_c) ? 1 : 2;
                int wa = S_wires[chosen_a], wb = S_wires[chosen_b];
                int wid = (int)cg.size();
                int gd = std::max(cg[wa].gd, cg[wb].gd) + 1;
                TT256 t = (op == 1) ? tt_xor(cg[wa].tt, cg[wb].tt) : tt_xnor(cg[wa].tt, cg[wb].tt);
                cg.push_back({op, wa, wb, gd, 0, t});
                mc_w[chosen_m][want_c] = wid;
                in_S[chosen_m] = true;
                S_masks.push_back(chosen_m);
                S_wires.push_back(wid);
                S_csts.push_back(want_c);
                S_deps.push_back(gd);

                len_B[chosen_m] = 1;
                uint32_t bit = chosen_m & -chosen_m;
                for (uint32_t blk = 0; blk < 256; blk += (bit << 1)) {
                    for (uint32_t i = blk; i < blk + bit; ++i) {
                        uint32_t j = i ^ chosen_m;
                        if (len_B[j] + 1 < len_B[i]) len_B[i] = len_B[j] + 1;
                        if (len_B[i] + 1 < len_B[j]) len_B[j] = len_B[i] + 1;
                    }
                }
                rem.erase(std::remove(rem.begin(), rem.end(), chosen_m), rem.end());
            }
            if (!ok_run) continue;

            // Ensure any dual-polarity or complemented-input (m, c) is materialized in 1 gate at gd <= 7.
            auto get_aff_wire = [&](uint16_t am) -> int {
                uint8_t lm = (uint8_t)(am & 0xFF);
                uint8_t c = (uint8_t)(am >> 8);
                if (mc_w[lm][c] >= 0) return mc_w[lm][c];
                // If opposite polarity gate `w_opp` exists with op in {1,2} and gd <= 7, clone its inputs with flipped op.
                int w_opp = mc_w[lm][c ^ 1];
                if (w_opp >= 8 && cg[w_opp].ad == 0 && cg[w_opp].gd <= 7) {
                    uint8_t nop = (cg[w_opp].op == 1) ? 2 : 1;
                    int u = cg[w_opp].u, v = cg[w_opp].v;
                    int wid = (int)cg.size();
                    cg.push_back({nop, u, v, cg[w_opp].gd, 0, tt_not(cg[w_opp].tt)});
                    mc_w[lm][c] = wid;
                    return wid;
                }
                // Otherwise (e.g. w_opp < 8, i.e. ~x_k.), find any pair in S_masks with mask_a ^ mask_b == lm and gd <= 6.
                for (size_t a = 0; a < S_masks.size(); ++a) {
                    if (S_deps[a] > 6) continue;
                    for (size_t b = a + 1; b < S_masks.size(); ++b) {
                        if (S_deps[b] > 6) continue;
                        if ((S_masks[a] ^ S_masks[b]) == lm) {
                            uint8_t nop = ((S_csts[a] ^ S_csts[b]) == c) ? 1 : 2;
                            int wid = (int)cg.size();
                            int gd = std::max(S_deps[a], S_deps[b]) + 1;
                            TT256 t = (nop == 1) ? tt_xor(cg[S_wires[a]].tt, cg[S_wires[b]].tt)
                                                 : tt_xnor(cg[S_wires[a]].tt, cg[S_wires[b]].tt);
                            cg.push_back({nop, S_wires[a], S_wires[b], gd, 0, t});
                            mc_w[lm][c] = wid;
                            return wid;
                        }
                    }
                }
                // Fallback for ~x_k: create XOR(x_k, x_{(k+1)&7}) at gd=1 then XNOR at gd=2.
                int k = __builtin_ctz(lm), k2 = (k + 1) & 7;
                int w1 = (int)cg.size();
                cg.push_back({1, k, k2, 1, 0, tt_xor(cg[k].tt, cg[k2].tt)});
                int w2 = (int)cg.size();
                uint8_t op2 = c ? 2 : 1;
                cg.push_back({op2, w1, k2, 2, 0, op2 == 1 ? tt_xor(cg[w1].tt, cg[k2].tt) : tt_xnor(cg[w1].tt, cg[k2].tt)});
                mc_w[lm][c] = w2;
                return w2;
            };

            // Emit Level 8 (ANDs), Level 9 (XORs), Level 10 (XOR/XNORs) with CSE.
            std::unordered_map<uint64_t, int> bot_cse;
            auto emit_b = [&](uint8_t op, int u, int v) -> int {
                if (u > v) std::swap(u, v);
                uint64_t key = ((uint64_t)op << 40) | ((uint64_t)u << 20) | (uint64_t)v;
                auto it = bot_cse.find(key);
                if (it != bot_cse.end()) return it->second;
                int gd = std::max(cg[u].gd, cg[v].gd) + 1;
                int ad = std::max(cg[u].ad, cg[v].ad) + (op == 3 ? 1 : 0);
                TT256 t = (op == 3) ? tt_and(cg[u].tt, cg[v].tt)
                        : (op == 1) ? tt_xor(cg[u].tt, cg[v].tt)
                                    : tt_xnor(cg[u].tt, cg[v].tt);
                int wid = (int)cg.size();
                cg.push_back({op, u, v, gd, ad, t});
                bot_cse[key] = wid;
                return wid;
            };

            std::array<int, 8> outs;
            bool depth_ok = true;
            for (int b = 0; b < 8; ++b) {
                std::vector<int> terms;
                for (int j = 0; j < 4; ++j) {
                    uint16_t am = cfg.aff_mask[b][j];
                    if (am == 0) continue;
                    if (am == 256U) terms.push_back(w_inv[j]);
                    else {
                        int lw = get_aff_wire(am);
                        if (lw < 0 || cg[lw].gd > 7) { depth_ok = false; break; }
                        terms.push_back(emit_b(3, lw, w_inv[j]));
                    }
                }
                if (!depth_ok) break;
                while (terms.size() > 2) {
                    std::vector<int> nxt;
                    for (size_t k = 0; k + 1 < terms.size(); k += 2) nxt.push_back(emit_b(1, terms[k], terms[k + 1]));
                    if (terms.size() & 1) nxt.push_back(terms.back());
                    terms = nxt;
                }
                int fw = -1;
                if (terms.size() == 2) fw = emit_b(cfg.out_xnor[b] ? 2 : 1, terms[0], terms[1]);
                else { depth_ok = false; break; }
                if (cg[fw].gd > 10 || cg[fw].tt != inv_sbox_tt[b]) { depth_ok = false; break; }
                outs[b] = fw;
            }
            if (!depth_ok) continue;

            // Sweep dead gates.
            std::vector<uint8_t> live(cg.size(), 0);
            for (int b = 0; b < 8; ++b) live[outs[b]] = 1;
            for (int id = (int)cg.size() - 1; id >= 8; --id) {
                if (live[id]) { live[cg[id].u] = 1; live[cg[id].v] = 1; }
            }
            std::vector<int> remap(cg.size(), -1);
            std::vector<OutGate> clean;
            for (int k = 0; k < 8; ++k) { remap[k] = k; clean.push_back(cg[k]); }
            int cnt_G = 0, cnt_A = 0, max_gd = 0;
            for (size_t id = 8; id < cg.size(); ++id) {
                if (!live[id]) continue;
                OutGate g = cg[id];
                g.u = remap[g.u]; g.v = remap[g.v];
                g.gd = std::max(clean[g.u].gd, clean[g.v].gd) + 1;
                g.ad = std::max(clean[g.u].ad, clean[g.v].ad) + (g.op == 3 ? 1 : 0);
                remap[id] = (int)clean.size();
                clean.push_back(g);
                cnt_G++;
                if (g.op == 3) cnt_A++;
                max_gd = std::max(max_gd, g.gd);
            }
            if (max_gd > 10) continue;
            std::array<int, 8> co;
            for (int b = 0; b < 8; ++b) co[b] = remap[outs[b]];

            if (cnt_G < best_G_local || (cnt_G == best_G_local && cnt_A < best_A_local)) {
                best_G_local = cnt_G; best_A_local = cnt_A;
                out_circ = std::move(clean); out_outs = co;
            }
        }
        if (best_G_local >= 9999) return false;
        ret_G = best_G_local; ret_A = best_A_local;
        return true;
    };

    // Multi-threaded Coordinate Descent over (config, idx[0..3]).
    std::mutex best_mtx;
    int global_best_G = 9999, global_best_G_A = 9999;
    int global_best_A = 9999, global_best_A_G = 9999;
    std::vector<OutGate> best_G_circ, best_A_circ;
    std::array<int, 8> best_G_outs, best_A_outs;

    int n_threads = std::max(1u, std::thread::hardware_concurrency());
    std::vector<std::thread> workers;
    for (int tid = 0; tid < n_threads; ++tid) {
        workers.emplace_back([&, tid]() {
            std::mt19937 rng(77777u + tid * 31337u);
            while (true) {
                double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
                if (el >= budget_sec) break;

                const BasisConfig& cfg = configs[rng() % configs.size()];
                int idx[4];
                for (int q = 0; q < 4; ++q) {
                    int lim = std::min((int)cands[cfg.m[q]].size(), 3000);
                    idx[q] = (int)(rng() % lim);
                }

                std::vector<OutGate> cur_c, cand_c;
                std::array<int, 8> cur_o, cand_o;
                int cur_G = 9999, cur_A = 9999;
                if (!evaluate_tuple(cfg, idx, rng, 2, cur_c, cur_o, cur_G, cur_A)) continue;

                // Coordinate descent: sweep 180 candidates per coordinate q in 0..3 for 3 passes.
                bool prio_A = (tid >= (n_threads * 3) / 4);
                for (int pass = 0; pass < 3; ++pass) {
                    bool changed = false;
                    for (int q = 0; q < 4; ++q) {
                        int lim = (int)cands[cfg.m[q]].size();
                        int old_iq = idx[q];
                        for (int probe = 0; probe < 160; ++probe) {
                            // Bias 50% toward low-AND front of cands.
                            int cand_iq = (probe < 80) ? (int)(rng() % std::min(lim, 800)) : (int)(rng() % lim);
                            idx[q] = cand_iq;
                            int g = 9999, a = 9999;
                            if (evaluate_tuple(cfg, idx, rng, 1, cand_c, cand_o, g, a)) {
                                bool imp = prio_A ? (a < cur_A || (a == cur_A && g <= cur_G))
                                                  : (g < cur_G || (g == cur_G && a <= cur_A));
                                if (imp) {
                                    if (g < cur_G || a < cur_A) changed = true;
                                    cur_G = g; cur_A = a;
                                    cur_c = std::move(cand_c); cur_o = cand_o;
                                    old_iq = cand_iq;
                                } else {
                                    idx[q] = old_iq;
                                }
                            } else {
                                idx[q] = old_iq;
                            }
                        }
                    }
                    if (!changed) break;
                }

                // Deep 24-restart affine RNBP polish on converged norm tuple.
                int fg = 9999, fa = 9999;
                if (evaluate_tuple(cfg, idx, rng, 24, cand_c, cand_o, fg, fa)) {
                    if (fg < cur_G || (fg == cur_G && fa < cur_A)) {
                        cur_G = fg; cur_A = fa; cur_c = std::move(cand_c); cur_o = cand_o;
                    }
                }

                std::lock_guard<std::mutex> lk(best_mtx);
                if (cur_G < global_best_G || (cur_G == global_best_G && cur_A < global_best_G_A)) {
                    global_best_G = cur_G; global_best_G_A = cur_A;
                    best_G_circ = cur_c; best_G_outs = cur_o;
                    double el2 = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
                    printf("  [T%d NEW GD=10 MIN-G @ %.2fs] G=%d, A=%d, AD=4, GD=10 (pol=%d)\n",
                           tid, el2, cur_G, cur_A, cfg.pol_inv);
                    fflush(stdout);
                    write_ncff(out_dir + "/gd10_super_minG.circ.txt", best_G_circ, best_G_outs);
                }
                if (cur_A < global_best_A || (cur_A == global_best_A && cur_G < global_best_A_G)) {
                    global_best_A = cur_A; global_best_A_G = cur_G;
                    best_A_circ = cur_c; best_A_outs = cur_o;
                    double el2 = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
                    printf("  [T%d NEW GD=10 MIN-A @ %.2fs] A=%d, G=%d, AD=4, GD=10 (pol=%d)\n",
                           tid, el2, cur_A, cur_G, cfg.pol_inv);
                    fflush(stdout);
                    write_ncff(out_dir + "/gd10_super_minA.circ.txt", best_A_circ, best_A_outs);
                }
            }
        });
    }
    for (auto& th : workers) th.join();

    printf("=== GD=10 SUPER SYNTH DONE: best_G=(A=%d, G=%d, GD=10), best_A=(A=%d, G=%d, GD=10) ===\n",
           global_best_G_A, global_best_G, global_best_A, global_best_A_G);
    return 0;
}
