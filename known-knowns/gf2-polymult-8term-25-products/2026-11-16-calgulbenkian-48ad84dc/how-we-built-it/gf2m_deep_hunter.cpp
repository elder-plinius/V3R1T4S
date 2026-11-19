// gf2m_deep_hunter.cpp
// Deep Exhaustive Cube-Embedding + Symmetric/Asymmetric Coset Walk +
// Exact Steiner-Closure IDA* (depth 4) + 137-Bit ANF Gate-Walk Optimizer
// for GF(2^6) 0x49, GF(2^7) 0x91 & 0x89, and GF(2^8) 0x11B.

#include <algorithm>
#include <array>
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
using u32 = uint32_t;
using u64 = uint64_t;

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

static inline u64 outer_prod(u8 u, u8 v, int m) {
    u64 mask = 0;
    for (int i = 0; i < m; ++i)
        if ((u >> i) & 1) mask |= (u64(v) << (i * m));
    return mask;
}

static std::vector<u64> build_targets(int m, int poly) {
    std::vector<u64> tgt(m, 0ULL);
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < m; ++j) {
            int rem = gf2_poly_mul_mod(1 << i, 1 << j, m, poly);
            for (int k = 0; k < m; ++k)
                if ((rem >> k) & 1) tgt[k] |= (1ULL << (i * m + j));
        }
    return tgt;
}

static bool solve_W(const std::vector<u64>& M, int m, const std::vector<u64>& targets,
                    std::vector<u64>& W_rows, std::vector<u64>* null_basis = nullptr) {
    int K = (int)M.size();
    if (K > 62) return false;
    u64 bv[64] = {0}, bc[64] = {0};
    bool hp[64] = {false};
    if (null_basis) null_basis->clear();
    for (int t = 0; t < K; ++t) {
        u64 v = M[t], c = (1ULL << t);
        bool ins = false;
        while (v) {
            int p = __builtin_ctzll(v);
            if (!hp[p]) { hp[p] = true; bv[p] = v; bc[p] = c; ins = true; break; }
            v ^= bv[p]; c ^= bc[p];
        }
        if (!ins && null_basis) null_basis->push_back(c);
    }
    W_rows.assign(m, 0ULL);
    for (int k = 0; k < m; ++k) {
        u64 v = targets[k], c = 0;
        while (v) {
            int p = __builtin_ctzll(v);
            if (!hp[p]) return false;
            v ^= bv[p]; c ^= bc[p];
        }
        W_rows[k] = c;
    }
    return true;
}

// Fast 0-helper floor computation for screening millions of product sets in ~250 ns!
static int fast_floor_score(int m, const std::vector<u64>& targets,
                            const std::vector<u8>& U, const std::vector<u8>& V) {
    int K_in = (int)U.size();
    if (K_in > 62) return 999999;
    u64 bv[64] = {0}, bc[64] = {0};
    bool hp[64] = {false};
    for (int t = 0; t < K_in; ++t) {
        u64 v = outer_prod(U[t], V[t], m), c = (1ULL << t);
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

struct LinearSLP {
    int m = 0;
    std::vector<std::pair<int, int>> gates;
    std::vector<u8> node_val;
    int val_to_node[256];
    LinearSLP() { std::fill(std::begin(val_to_node), std::end(val_to_node), -1); }
};

static inline bool closure_covers(int m, const Bitset256& S, const Bitset256& allowed, Bitset256& B_out,
                                  u8* B_list_out, int& B_len_out) {
    B_out = Bitset256{};
    B_len_out = 0;
    for (int i = 0; i < m; ++i) {
        u8 v = u8(1 << i);
        B_out.set(v);
        B_list_out[B_len_out++] = v;
    }
    u8 cands[256];
    int n_cands = 0;
    int lim = 1 << m;
    for (int v = 1; v < lim; ++v)
        if (allowed.test(v) && !B_out.test(v)) cands[n_cands++] = u8(v);

    bool progress = true;
    while (progress && n_cands > 0) {
        progress = false;
        for (int ci = 0; ci < n_cands; ) {
            u8 t = cands[ci];
            bool ok = false;
            for (int i = 0; i < B_len_out; ++i) {
                if (B_out.test(t ^ B_list_out[i])) { ok = true; break; }
            }
            if (ok) {
                B_out.set(t);
                B_list_out[B_len_out++] = t;
                cands[ci] = cands[--n_cands];
                progress = true;
            } else {
                ++ci;
            }
        }
    }
    return B_out.contains(S);
}

static void monotone_closure_parents(int m, const Bitset256& allowed, std::vector<u8>& order,
                                     std::pair<u8, u8>* parent_vals) {
    Bitset256 B{};
    u8 B_list[256];
    int B_len = 0;
    for (int i = 0; i < m; ++i) {
        u8 v = u8(1 << i);
        B.set(v);
        B_list[B_len++] = v;
    }
    order.clear();
    u8 cands[256];
    int n_cands = 0;
    for (int v = 1; v < (1 << m); ++v)
        if (allowed.test(v) && !B.test(v)) cands[n_cands++] = u8(v);

    bool progress = true;
    while (progress && n_cands > 0) {
        progress = false;
        for (int ci = 0; ci < n_cands; ) {
            u8 t = cands[ci];
            bool ok = false;
            u8 px = 0, py = 0;
            for (int i = 0; i < B_len; ++i) {
                u8 x = B_list[i], y = t ^ x;
                if (B.test(y)) { ok = true; px = x; py = y; break; }
            }
            if (ok) {
                B.set(t);
                B_list[B_len++] = t;
                order.push_back(t);
                parent_vals[t] = {px, py};
                cands[ci] = cands[--n_cands];
                progress = true;
            } else {
                ++ci;
            }
        }
    }
}

static bool ida_helpers(int m, const Bitset256& S, Bitset256 allowed, const Bitset256& B_cur,
                        const u8* B_list, int B_len, int rem_depth, Bitset256& best_allowed,
                        int& nodes_visited, int max_nodes) {
    if (rem_depth == 0) return B_cur.contains(S);
    if (++nodes_visited > max_nodes) return false;

    Bitset256 cand_H{};
    for (int i = 0; i < B_len; ++i) {
        for (int j = i + 1; j < B_len; ++j) {
            u8 h = B_list[i] ^ B_list[j];
            if (h != 0 && !allowed.test(h) && !B_cur.test(h)) cand_H.set(h);
        }
    }
    struct HCand { u8 h; int score; };
    HCand hlist[256];
    int nh = 0;
    u8 missing[256];
    int n_miss = 0;
    int lim = 1 << m;
    for (int v = 1; v < lim; ++v)
        if (S.test(v) && !B_cur.test(v)) missing[n_miss++] = u8(v);

    for (int h = 1; h < lim; ++h) {
        if (!cand_H.test(h)) continue;
        // If rem_depth == 1, h MUST directly unlock at least one missing target (h ^ b in missing)!
        int hits = 0;
        for (int mi = 0; mi < n_miss; ++mi)
            if (B_cur.test(missing[mi] ^ u8(h))) hits++;
        if (rem_depth == 1 && hits == 0) continue;
        int sc = hits * 8 + (8 - __builtin_popcount(h));
        hlist[nh++] = {u8(h), sc};
    }
    std::sort(hlist, hlist + nh, [](const HCand& a, const HCand& b) { return a.score > b.score; });

    for (int idx = 0; idx < nh; ++idx) {
        Bitset256 next_allowed = allowed;
        next_allowed.set(hlist[idx].h);
        Bitset256 B_next;
        u8 B_next_list[256];
        int B_next_len = 0;
        if (closure_covers(m, S, next_allowed, B_next, B_next_list, B_next_len)) {
            best_allowed = next_allowed;
            return true;
        }
        if (rem_depth > 1) {
            if (ida_helpers(m, S, next_allowed, B_next, B_next_list, B_next_len,
                            rem_depth - 1, best_allowed, nodes_visited, max_nodes)) {
                return true;
            }
        }
        if (nodes_visited > max_nodes) return false;
    }
    return false;
}

static LinearSLP build_slp_greedy_bp(int m, const std::vector<u8>& targets_vec, std::mt19937& rng, bool randomize) {
    LinearSLP slp;
    slp.m = m;
    for (int i = 0; i < m; ++i) {
        slp.node_val.push_back(u8(1 << i));
        slp.val_to_node[1 << i] = i;
    }
    Bitset256 S{};
    for (u8 t : targets_vec) if (t != 0 && __builtin_popcount(t) > 1) S.set(t);
    if (S.count() == 0) return slp;

    while (true) {
        bool closed_any = true;
        while (closed_any) {
            closed_any = false;
            int n_nodes = (int)slp.node_val.size();
            for (int v = 1; v < (1 << m); ++v) {
                if (!S.test(v) || slp.val_to_node[v] != -1) continue;
                for (int i = 0; i < n_nodes; ++i) {
                    u8 u = v ^ slp.node_val[i];
                    if (slp.val_to_node[u] != -1) {
                        int j = slp.val_to_node[u];
                        int id = (int)slp.node_val.size();
                        slp.gates.push_back({i, j});
                        slp.node_val.push_back(u8(v));
                        slp.val_to_node[v] = id;
                        closed_any = true;
                        break;
                    }
                }
            }
        }
        std::vector<u8> rem;
        for (int v = 1; v < (1 << m); ++v)
            if (S.test(v) && slp.val_to_node[v] == -1) rem.push_back(u8(v));
        if (rem.empty()) break;

        int n_nodes = (int)slp.node_val.size();
        Bitset256 pair_sums{};
        for (int i = 0; i < n_nodes; ++i)
            for (int j = i + 1; j < n_nodes; ++j)
                pair_sums.set(slp.node_val[i] ^ slp.node_val[j]);

        int best_score = -999999;
        std::vector<std::pair<int, int>> ties;
        for (int i = 0; i < n_nodes; ++i) {
            for (int j = i + 1; j < n_nodes; ++j) {
                u8 cand = slp.node_val[i] ^ slp.node_val[j];
                if (cand == 0 || slp.val_to_node[cand] != -1) continue;
                int sc = 0;
                for (u8 t : rem) {
                    u8 diff = t ^ cand;
                    if (slp.val_to_node[diff] != -1) sc += 120;
                    else if (pair_sums.test(diff)) sc += 12;
                    else sc -= __builtin_popcount(diff);
                }
                if (sc > best_score) { best_score = sc; ties = {{i, j}}; }
                else if (sc == best_score) ties.push_back({i, j});
            }
        }
        auto chosen = ties[randomize && ties.size() > 1 ? (rng() % ties.size()) : 0];
        u8 v = slp.node_val[chosen.first] ^ slp.node_val[chosen.second];
        int id = (int)slp.node_val.size();
        slp.gates.push_back(chosen);
        slp.node_val.push_back(v);
        slp.val_to_node[v] = id;
    }
    return slp;
}

static LinearSLP solve_linear_layer(int m, const std::vector<u8>& rows, int max_ida_excess,
                                    int max_ida_nodes, std::mt19937& rng, int rnbp_tries = 8) {
    Bitset256 S{}, allowed0{};
    for (int i = 0; i < m; ++i) allowed0.set(1 << i);
    for (u8 r : rows) {
        if (r != 0 && __builtin_popcount(r) > 1) {
            S.set(r);
            allowed0.set(r);
        }
    }
    if (S.count() == 0) {
        LinearSLP slp; slp.m = m;
        for (int i = 0; i < m; ++i) { slp.node_val.push_back(u8(1 << i)); slp.val_to_node[1 << i] = i; }
        return slp;
    }
    Bitset256 B0, winning_allowed{};
    u8 B0_list[256];
    int B0_len = 0;
    bool exact_found = false;

    if (closure_covers(m, S, allowed0, B0, B0_list, B0_len)) {
        winning_allowed = allowed0;
        exact_found = true;
    } else {
        for (int exc = 1; exc <= max_ida_excess; ++exc) {
            int visited = 0;
            if (ida_helpers(m, S, allowed0, B0, B0_list, B0_len, exc, winning_allowed, visited, max_ida_nodes)) {
                exact_found = true;
                break;
            }
        }
    }
    if (exact_found) {
        std::vector<u8> order;
        std::pair<u8, u8> parents[256];
        monotone_closure_parents(m, winning_allowed, order, parents);
        bool needed[256] = {false};
        for (int v = 1; v < (1 << m); ++v) if (S.test(v)) needed[v] = true;
        for (int idx = (int)order.size() - 1; idx >= 0; --idx) {
            u8 v = order[idx];
            if (needed[v]) { needed[parents[v].first] = true; needed[parents[v].second] = true; }
        }
        LinearSLP slp; slp.m = m;
        for (int i = 0; i < m; ++i) { slp.node_val.push_back(u8(1 << i)); slp.val_to_node[1 << i] = i; }
        for (u8 v : order) {
            if (!needed[v]) continue;
            int u1 = slp.val_to_node[parents[v].first], u2 = slp.val_to_node[parents[v].second];
            int id = (int)slp.node_val.size();
            slp.gates.push_back({u1, u2});
            slp.node_val.push_back(v);
            slp.val_to_node[v] = id;
        }
        return slp;
    }
    LinearSLP best = build_slp_greedy_bp(m, rows, rng, false);
    for (int t = 0; t < rnbp_tries; ++t) {
        LinearSLP cand = build_slp_greedy_bp(m, rows, rng, true);
        if (cand.gates.size() < best.gates.size()) best = std::move(cand);
    }
    return best;
}

struct FullCircuit {
    int m = 0, poly = 0, n_and = 0, n_xor = 0, depth = 0;
    struct Gate { std::string op, out, in1, in2; };
    std::vector<Gate> gates;
};

static FullCircuit build_full_circuit(int m, int poly, const std::vector<u8>& U_in, const std::vector<u8>& V_in,
                                      const std::vector<u64>& W_rows_in, std::mt19937& rng,
                                      int max_ida_excess = 4, int max_ida_nodes = 150000) {
    std::vector<u8> U, V, WT;
    int K_orig = (int)U_in.size();
    for (int t = 0; t < K_orig; ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) if ((W_rows_in[r] >> t) & 1ULL) col |= u8(1 << r);
        if (col == 0) continue;
        U.push_back(U_in[t]);
        V.push_back(V_in[t]);
        WT.push_back(col);
    }
    int K = (int)U.size();
    LinearSLP slpU = solve_linear_layer(m, U, max_ida_excess, max_ida_nodes, rng, 32);
    LinearSLP slpV = (U == V) ? slpU : solve_linear_layer(m, V, max_ida_excess, max_ida_nodes, rng, 32);
    LinearSLP slpWT = solve_linear_layer(m, WT, max_ida_excess, max_ida_nodes, rng, 48);

    FullCircuit fc; fc.m = m; fc.poly = poly;
    int t_idx = 1;
    auto new_wire = [&]() { return "t" + std::to_string(t_idx++); };

    std::vector<std::string> nodeU(slpU.node_val.size());
    for (int i = 0; i < m; ++i) nodeU[i] = "A" + std::to_string(i);
    for (size_t g = 0; g < slpU.gates.size(); ++g) {
        std::string w = new_wire();
        fc.gates.push_back({"XOR", w, nodeU[slpU.gates[g].first], nodeU[slpU.gates[g].second]});
        nodeU[m + g] = w; fc.n_xor++;
    }
    std::vector<std::string> nodeV(slpV.node_val.size());
    for (int i = 0; i < m; ++i) nodeV[i] = "B" + std::to_string(i);
    for (size_t g = 0; g < slpV.gates.size(); ++g) {
        std::string w = new_wire();
        fc.gates.push_back({"XOR", w, nodeV[slpV.gates[g].first], nodeV[slpV.gates[g].second]});
        nodeV[m + g] = w; fc.n_xor++;
    }
    std::vector<std::string> prod_wire(K);
    for (int t = 0; t < K; ++t) {
        std::string w = new_wire();
        fc.gates.push_back({"AND", w, nodeU[slpU.val_to_node[U[t]]], nodeV[slpV.val_to_node[V[t]]]});
        prod_wire[t] = w; fc.n_and++;
    }

    int num_wt_nodes = (int)slpWT.node_val.size(), g_wt = (int)slpWT.gates.size();
    std::vector<std::vector<std::string>> accum_list(num_wt_nodes);
    for (int t = 0; t < K; ++t) accum_list[slpWT.val_to_node[WT[t]]].push_back(prod_wire[t]);

    std::unordered_map<std::string, int> wire_depth;
    for (int i = 0; i < m; ++i) { wire_depth["A" + std::to_string(i)] = 0; wire_depth["B" + std::to_string(i)] = 0; }
    for (const auto& gt : fc.gates) wire_depth[gt.out] = std::max(wire_depth[gt.in1], wire_depth[gt.in2]) + 1;

    auto fold_wires = [&](std::vector<std::string>& wl, const std::string& final_name = "") -> std::string {
        while (wl.size() > 1) {
            std::sort(wl.begin(), wl.end(), [&](const std::string& a, const std::string& b) {
                return wire_depth[a] > wire_depth[b];
            });
            std::string w1 = wl.back(); wl.pop_back();
            std::string w2 = wl.back(); wl.pop_back();
            std::string out = (wl.empty() && !final_name.empty()) ? final_name : new_wire();
            fc.gates.push_back({"XOR", out, w1, w2});
            fc.n_xor++;
            wire_depth[out] = std::max(wire_depth[w1], wire_depth[w2]) + 1;
            wl.push_back(out);
        }
        return wl[0];
    };

    for (int v = m + g_wt - 1; v >= m; --v) {
        if (accum_list[v].empty()) continue;
        std::string w = fold_wires(accum_list[v]);
        auto [in1, in2] = slpWT.gates[v - m];
        accum_list[in1].push_back(w);
        accum_list[in2].push_back(w);
    }
    int max_d = 0;
    for (int i = 0; i < m; ++i) {
        std::string out_c = "C" + std::to_string(i);
        std::string res = fold_wires(accum_list[i], out_c);
        if (res != out_c) {
            for (auto it = fc.gates.rbegin(); it != fc.gates.rend(); ++it)
                if (it->out == res) { wire_depth[out_c] = wire_depth[res]; it->out = out_c; break; }
        }
        max_d = std::max(max_d, wire_depth[out_c]);
    }
    fc.depth = max_d;
    return fc;
}

static bool verify_circuit_exhaustive(const FullCircuit& fc) {
    int m = fc.m, n_pairs = 1 << (2 * m);
    for (int base = 0; base < n_pairs; base += 64) {
        int cnt = std::min(64, n_pairs - base);
        u64 mask_valid = (cnt == 64) ? ~0ULL : ((1ULL << cnt) - 1ULL);
        std::unordered_map<std::string, u64> val;
        u64 ref[8] = {0};
        for (int lane = 0; lane < cnt; ++lane) {
            int idx = base + lane;
            int a = idx & ((1 << m) - 1), b = idx >> m;
            for (int i = 0; i < m; ++i) {
                if ((a >> i) & 1) val["A" + std::to_string(i)] |= (1ULL << lane);
                if ((b >> i) & 1) val["B" + std::to_string(i)] |= (1ULL << lane);
            }
            int p = gf2_poly_mul_mod(a, b, m, fc.poly);
            for (int k = 0; k < m; ++k) if ((p >> k) & 1) ref[k] |= (1ULL << lane);
        }
        for (const auto& g : fc.gates) {
            u64 v1 = val[g.in1], v2 = val[g.in2];
            if (g.op == "XOR") val[g.out] = v1 ^ v2;
            else if (g.op == "AND") val[g.out] = v1 & v2;
            else if (g.op == "XNOR") val[g.out] = (v1 ^ v2) ^ mask_valid;
        }
        for (int k = 0; k < m; ++k)
            if ((val["C" + std::to_string(k)] & mask_valid) != ref[k]) return false;
    }
    return true;
}

static void save_slp(const FullCircuit& fc, const std::string& path) {
    std::ofstream out(path);
    out << "# GF(2^" << fc.m << ") standard-basis multiplier modulo 0x" << std::hex << fc.poly << std::dec << "\n";
    out << "# Tally: " << (2 * fc.m) << " inputs, " << fc.m << " outputs, "
        << fc.gates.size() << " gates, " << fc.n_and << " AND, " << fc.n_xor << " XOR\n";
    out << "# Depth(Gate): " << fc.depth << "\n\n";
    out << "begin circuit Mult-GF" << (1 << fc.m) << "\n";
    out << "Inputs: A0:A" << (fc.m - 1) << " B0:B" << (fc.m - 1) << "\n";
    out << "Outputs: C0:C" << (fc.m - 1) << "\n";
    out << "GateSyntax: GateName Output Inputs\n";
    out << "begin SLP\n";
    for (const auto& g : fc.gates) out << g.op << " " << g.out << " " << g.in1 << " " << g.in2 << "\n";
    out << "end SLP\nend circuit\n";
}

static int exact_score_product_set(int m, const std::vector<u64>& targets,
                                   std::vector<u8>& U, std::vector<u8>& V,
                                   std::vector<u64>& W_rows, std::mt19937& rng,
                                   int max_ida_exc = 3, int max_ida_nodes = 15000) {
    int K_in = (int)U.size();
    std::vector<u64> M(K_in);
    for (int t = 0; t < K_in; ++t) M[t] = outer_prod(U[t], V[t], m);
    if (!solve_W(M, m, targets, W_rows, nullptr)) return 999999;

    std::vector<u8> U2, V2, WT;
    std::vector<u64> W2(m, 0ULL);
    for (int t = 0; t < K_in; ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) if ((W_rows[r] >> t) & 1ULL) col |= u8(1 << r);
        if (col == 0) continue;
        int nt = (int)U2.size();
        for (int r = 0; r < m; ++r) if ((col >> r) & 1) W2[r] |= (1ULL << nt);
        U2.push_back(U[t]); V2.push_back(V[t]); WT.push_back(col);
    }
    U = std::move(U2); V = std::move(V2); W_rows = std::move(W2);
    int K = (int)U.size();
    int lu = (int)solve_linear_layer(m, U, max_ida_exc, max_ida_nodes, rng, 4).gates.size();
    int lv = (U == V) ? lu : (int)solve_linear_layer(m, V, max_ida_exc, max_ida_nodes, rng, 4).gates.size();
    int lwt = (int)solve_linear_layer(m, WT, max_ida_exc, max_ida_nodes, rng, 6).gates.size();
    return (2 * K - m) + lu + lv + lwt;
}

// Symmetric + Asymmetric Walk Engine!
static void deep_walk(int m, int poly, const std::vector<u64>& targets,
                      std::vector<u8> U, std::vector<u8> V,
                      int& best_gates, FullCircuit& best_fc, const std::string& out_path,
                      std::mt19937& rng, int steps) {
    std::vector<u64> W_rows;
    int cur_sc = exact_score_product_set(m, targets, U, V, W_rows, rng, 2, 6000);
    if (cur_sc >= 999999) return;

    auto record_if_best = [&](const std::vector<u8>& cU, const std::vector<u8>& cV,
                              const std::vector<u64>& cW, int sc) {
        if (sc <= best_gates + 1) {
            FullCircuit fc = build_full_circuit(m, poly, cU, cV, cW, rng, 4, 200000);
            int g = (int)fc.gates.size();
            if (g < best_gates && verify_circuit_exhaustive(fc)) {
                best_gates = g;
                best_fc = fc;
                save_slp(fc, out_path);
                std::cout << "  *** [NEW WORLD RECORD m=" << m << " poly=0x" << std::hex << poly << std::dec
                          << "] GATES = " << g << " (AND=" << fc.n_and << ", XOR=" << fc.n_xor
                          << ", depth=" << fc.depth << ") ***\n" << std::flush;
            }
        }
    };
    record_if_best(U, V, W_rows, cur_sc);

    for (int st = 0; st < steps; ++st) {
        int K = (int)U.size();
        if (K == 0) break;

        // Move Type 1 (Symmetric 2x2 Leaf / Pair Mutation when U == V or near-symmetric!):
        // Pick two forms x != y currently in U (or one in U, one unit/pair), and toggle between:
        //   - Karatsuba: {(x,x), (y,y), (x^y, x^y)} (3 ANDs)
        //   - Schoolbook: {(x,x), (y,y), (x,y), (y,x)} (4 ANDs)
        //   - Sheared leaf: replace y by x^y or replace (x,y),(y,x) by (x',y'),(y',x')!
        if (rng() % 2 == 0) {
            // Collect symmetric off-diagonal pairs & diagonal elements
            Bitset256 diag{};
            std::vector<int> diag_idx;
            std::vector<std::pair<int, int>> sym_pairs;
            std::vector<bool> used(K, false);
            for (int i = 0; i < K; ++i) {
                if (U[i] == V[i]) { diag.set(U[i]); diag_idx.push_back(i); used[i] = true; }
            }
            for (int i = 0; i < K; ++i) {
                if (used[i]) continue;
                for (int j = i + 1; j < K; ++j) {
                    if (!used[j] && U[i] == V[j] && V[i] == U[j]) {
                        sym_pairs.push_back({i, j});
                        used[i] = used[j] = true;
                        break;
                    }
                }
            }

            int submove = rng() % 3;
            if (submove == 0 && !sym_pairs.empty()) {
                // Contract a symmetric pair (x,y),(y,x) -> (x^y, x^y) IF solvable (even if x,x or y,y isn't explicitly diagonal, span might still hold!)
                auto [i, j] = sym_pairs[rng() % sym_pairs.size()];
                u8 xy = U[i] ^ V[i];
                if (xy != 0) {
                    std::vector<u8> nU, nV;
                    for (int t = 0; t < K; ++t) if (t != i && t != j) { nU.push_back(U[t]); nV.push_back(V[t]); }
                    nU.push_back(xy); nV.push_back(xy);
                    if (fast_floor_score(m, targets, nU, nV) <= cur_sc + 1) {
                        std::vector<u64> nW;
                        int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
                        if (sc < cur_sc || (sc == cur_sc && (rng() % 2 == 0)) || (sc == cur_sc + 1 && (rng() % 20 == 0))) {
                            U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                            record_if_best(U, V, W_rows, cur_sc);
                            continue;
                        }
                    }
                }
            } else if (submove == 1 && !diag_idx.empty()) {
                // Expand a diagonal (z, z) -> (x, y), (y, x) for some x ^ y == z!
                int idx = diag_idx[rng() % diag_idx.size()];
                u8 z = U[idx];
                if (__builtin_popcount(z) >= 2) {
                    // Prefer x, y already in U or unit vectors!
                    Bitset256 pool{};
                    for (int b = 0; b < m; ++b) pool.set(1 << b);
                    for (u8 f : U) pool.set(f);
                    std::vector<std::pair<u8, u8>> splits;
                    for (int x = 1; x < (1 << m); ++x) {
                        int y = z ^ x;
                        if (y > x && (pool.test(x) || pool.test(y))) splits.push_back({u8(x), u8(y)});
                    }
                    if (!splits.empty()) {
                        auto [x, y] = splits[rng() % splits.size()];
                        std::vector<u8> nU = U, nV = V;
                        nU[idx] = x; nV[idx] = y;
                        nU.push_back(y); nV.push_back(x);
                        if (fast_floor_score(m, targets, nU, nV) <= cur_sc + 1) {
                            std::vector<u64> nW;
                            int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
                            if (sc < cur_sc || (sc == cur_sc && (rng() % 2 == 0)) || (sc == cur_sc + 1 && (rng() % 20 == 0))) {
                                U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                                record_if_best(U, V, W_rows, cur_sc);
                                continue;
                            }
                        }
                    }
                }
            } else if (submove == 2 && !diag_idx.empty()) {
                // Replace a diagonal (z, z) with ANOTHER diagonal (z', z')!
                int idx = diag_idx[rng() % diag_idx.size()];
                std::vector<u64> V_rem;
                for (int t = 0; t < K; ++t) if (t != idx) V_rem.push_back(outer_prod(U[t], V[t], m));
                u64 piv[64] = {0}; bool hp[64] = {false};
                for (u64 vec : V_rem) {
                    u64 v = vec;
                    while (v) { int p = __builtin_ctzll(v); if (!hp[p]) { hp[p] = true; piv[p] = v; break; } v ^= piv[p]; }
                }
                u64 R = 0;
                for (int r = 0; r < m; ++r) {
                    u64 v = targets[r];
                    while (v) { int p = __builtin_ctzll(v); if (!hp[p]) break; v ^= piv[p]; }
                    if (v != 0) { R = v; break; }
                }
                if (R != 0) {
                    std::vector<u8> valid_zp;
                    for (int zp = 1; zp < (1 << m); ++zp) {
                        if (zp == U[idx]) continue;
                        u64 v = outer_prod(u8(zp), u8(zp), m) ^ R;
                        while (v) { int p = __builtin_ctzll(v); if (!hp[p]) break; v ^= piv[p]; }
                        if (v == 0) valid_zp.push_back(u8(zp));
                    }
                    if (!valid_zp.empty()) {
                        u8 zp = valid_zp[rng() % valid_zp.size()];
                        std::vector<u8> nU = U, nV = V;
                        nU[idx] = zp; nV[idx] = zp;
                        if (fast_floor_score(m, targets, nU, nV) <= cur_sc + 1) {
                            std::vector<u64> nW;
                            int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
                            if (sc < cur_sc || (sc == cur_sc && (rng() % 2 == 0))) {
                                U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                                record_if_best(U, V, W_rows, cur_sc);
                                continue;
                            }
                        }
                    }
                }
            }
        }

        // Move Type 2: Symmetric Pair Replacement {(u,v), (v,u)} -> {(u',v'), (v',u')}!
        {
            std::vector<std::pair<int, int>> sym_pairs;
            std::vector<bool> used(K, false);
            for (int i = 0; i < K; ++i) {
                if (U[i] == V[i]) { used[i] = true; continue; }
                for (int j = i + 1; j < K; ++j) {
                    if (!used[j] && U[i] == V[j] && V[i] == U[j]) {
                        sym_pairs.push_back({i, j});
                        used[i] = used[j] = true;
                        break;
                    }
                }
            }
            if (!sym_pairs.empty() && (rng() % 2 == 0)) {
                auto [i, j] = sym_pairs[rng() % sym_pairs.size()];
                u8 x = U[i], y = V[i];
                // Shear within plane span(x, y): replace {x, y} by {x, x^y} or {x^y, y}!
                u8 xy = x ^ y;
                std::pair<u8, u8> opts[2] = {{x, xy}, {xy, y}};
                auto [nx, ny] = opts[rng() % 2];
                std::vector<u8> nU = U, nV = V;
                nU[i] = nx; nV[i] = ny;
                nU[j] = ny; nV[j] = nx;
                if (fast_floor_score(m, targets, nU, nV) <= cur_sc + 1) {
                    std::vector<u64> nW;
                    int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
                    if (sc < cur_sc || (sc == cur_sc && (rng() % 2 == 0))) {
                        U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                        record_if_best(U, V, W_rows, cur_sc);
                        continue;
                    }
                }
            }
        }

        // Move Type 3: Global Basis Shear (pick two input coordinates a, b in 0..m-1 and shear u_a ^= u_b in all forms)!
        if (rng() % 8 == 0) {
            int a = rng() % m, b = rng() % m;
            if (a != b) {
                std::vector<u8> nU = U, nV = V;
                for (u8& f : nU) if ((f >> a) & 1) f ^= u8(1 << b);
                for (u8& f : nV) if ((f >> a) & 1) f ^= u8(1 << b);
                if (fast_floor_score(m, targets, nU, nV) <= cur_sc + 1) {
                    std::vector<u64> nW;
                    int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
                    if (sc < cur_sc || (sc == cur_sc && (rng() % 3 == 0))) {
                        U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                        record_if_best(U, V, W_rows, cur_sc);
                        continue;
                    }
                }
            }
        }

        // Move Type 4: Asymmetric 1-for-1 Coset Replacement!
        int idx = rng() % K;
        std::vector<u64> V_rem;
        V_rem.reserve(K - 1);
        for (int t = 0; t < K; ++t) if (t != idx) V_rem.push_back(outer_prod(U[t], V[t], m));
        u64 piv[64] = {0}; bool hp[64] = {false};
        for (u64 vec : V_rem) {
            u64 v = vec;
            while (v) { int p = __builtin_ctzll(v); if (!hp[p]) { hp[p] = true; piv[p] = v; break; } v ^= piv[p]; }
        }
        for (int p = 63; p >= 0; --p)
            if (hp[p]) for (int q = 0; q < p; ++q) if (hp[q] && ((piv[q] >> p) & 1ULL)) piv[q] ^= piv[p];
        auto rref = [&](u64 v) {
            for (int p = 0; p < m * m; ++p) if (hp[p] && ((v >> p) & 1ULL)) v ^= piv[p];
            return v;
        };
        u64 R = 0;
        for (int r = 0; r < m; ++r) { u64 v = rref(targets[r]); if (v != 0) { R = v; break; } }
        if (R == 0) {
            U.erase(U.begin() + idx); V.erase(V.begin() + idx);
            cur_sc = exact_score_product_set(m, targets, U, V, W_rows, rng, 2, 5000);
            record_if_best(U, V, W_rows, cur_sc);
            continue;
        }
        // Only test u' already in U U {units} (0 new top-A XORs!) plus 8 random u'
        std::vector<u8> cand_u;
        Bitset256 seen_u{}, inV{};
        for (int b = 0; b < m; ++b) { seen_u.set(1 << b); cand_u.push_back(u8(1 << b)); inV.set(1 << b); }
        for (int t = 0; t < K; ++t) if (t != idx) {
            if (!seen_u.test(U[t])) { seen_u.set(U[t]); cand_u.push_back(U[t]); }
            inV.set(V[t]);
        }
        for (int r = 0; r < 8; ++r) {
            u8 ru = u8(1 + (rng() % ((1 << m) - 1)));
            if (!seen_u.test(ru)) { seen_u.set(ru); cand_u.push_back(ru); }
        }

        int best_cand_fl = 999999;
        u8 bu = 0, bv_v = 0;
        for (u8 u : cand_u) {
            u64 col[8];
            for (int j = 0; j < m; ++j) col[j] = rref(outer_prod(u, u8(1 << j), m));
            u64 b_vec[8] = {0}; u8 b_comb[8] = {0}; int b_piv[8], nb = 0;
            u8 null_v[8]; int n_null = 0;
            for (int j = 0; j < m; ++j) {
                u64 vec = col[j]; u8 comb = u8(1 << j);
                for (int bi = 0; bi < nb; ++bi) if ((vec >> b_piv[bi]) & 1ULL) { vec ^= b_vec[bi]; comb ^= b_comb[bi]; }
                if (vec != 0) {
                    int p = __builtin_ctzll(vec);
                    for (int bi = 0; bi < nb; ++bi) if ((b_vec[bi] >> p) & 1ULL) { b_vec[bi] ^= vec; b_comb[bi] ^= comb; }
                    b_vec[nb] = vec; b_comb[nb] = comb; b_piv[nb] = p; nb++;
                } else null_v[n_null++] = comb;
            }
            u64 tgt = R; u8 v0 = 0;
            for (int bi = 0; bi < nb; ++bi) if ((tgt >> b_piv[bi]) & 1ULL) { tgt ^= b_vec[bi]; v0 ^= b_comb[bi]; }
            if (tgt == 0) {
                int lim_n = 1 << std::min(n_null, 3);
                for (int nm = 0; nm < lim_n; ++nm) {
                    u8 v = v0;
                    for (int b = 0; b < std::min(n_null, 3); ++b) if ((nm >> b) & 1) v ^= null_v[b];
                    if (v == 0 || (u == U[idx] && v == V[idx])) continue;
                    std::vector<u8> nU = U, nV = V;
                    nU[idx] = u; nV[idx] = v;
                    int fl = fast_floor_score(m, targets, nU, nV);
                    if (fl < best_cand_fl) { best_cand_fl = fl; bu = u; bv_v = v; }
                }
            }
        }
        if (bu != 0 && best_cand_fl <= cur_sc + 1) {
            std::vector<u8> nU = U, nV = V;
            nU[idx] = bu; nV[idx] = bv_v;
            std::vector<u64> nW;
            int sc = exact_score_product_set(m, targets, nU, nV, nW, rng, 2, 5000);
            if (sc < cur_sc || (sc == cur_sc && (rng() % 3 == 0))) {
                U = std::move(nU); V = std::move(nV); W_rows = std::move(nW); cur_sc = sc;
                record_if_best(U, V, W_rows, cur_sc);
            }
        }
    }
}

// Generate the 9 2x2 leaves of K x K (on dims 1, 2) with 9-bit leaf mask (bit l=1 -> Karatsuba 3 ANDs, 0 -> Schoolbook 4 ANDs)
// where dim 0 is the leaf pair!
static void build_9leaf_cube(const u8 map8[8], int leaf_mask9, std::vector<u8>& U, std::vector<u8>& V) {
    U.clear(); V.clear();
    // 9 pairs of indices (even, odd): first build 3x3 KxK over pairs P_0=(0,1), P_1=(2,3), P_2=(4,5), P_3=(6,7)
    u8 P[9][2];
    for (int q = 0; q < 4; ++q) { P[q][0] = map8[2 * q]; P[q][1] = map8[2 * q + 1]; }
    // KxK on {P0, P1, P2, P3}:
    // dim1: (0,1) and (2,3) -> sums P0^P1, P2^P3; dim2: (0,2), (1,3), (0^1, 2^3)
    P[4][0] = P[0][0] ^ P[1][0]; P[4][1] = P[0][1] ^ P[1][1];
    P[5][0] = P[2][0] ^ P[3][0]; P[5][1] = P[2][1] ^ P[3][1];
    P[6][0] = P[0][0] ^ P[2][0]; P[6][1] = P[0][1] ^ P[2][1];
    P[7][0] = P[1][0] ^ P[3][0]; P[7][1] = P[1][1] ^ P[3][1];
    P[8][0] = P[4][0] ^ P[5][0]; P[8][1] = P[4][1] ^ P[5][1];

    for (int l = 0; l < 9; ++l) {
        u8 x = P[l][0], y = P[l][1];
        if (x == 0 && y == 0) continue;
        if (x == 0) { U.push_back(y); V.push_back(y); continue; }
        if (y == 0) { U.push_back(x); V.push_back(x); continue; }
        if (x == y) { U.push_back(x); V.push_back(x); continue; }
        U.push_back(x); V.push_back(x);
        U.push_back(y); V.push_back(y);
        if ((leaf_mask9 >> l) & 1) {
            U.push_back(x ^ y); V.push_back(x ^ y);
        } else {
            U.push_back(x); V.push_back(y);
            U.push_back(y); V.push_back(x);
        }
    }
}

static void sweep_cube_embeddings(int m, int poly, int init_best, const std::string& out_path) {
    auto targets = build_targets(m, poly);
    std::mt19937 rng(987654321 + poly);
    int best_gates = init_best;
    FullCircuit best_fc;

    std::cout << ">>> Deep Cube-Embedding + Symmetric/Asymmetric Search for m=" << m
              << " poly=0x" << std::hex << poly << std::dec << " (bar=" << init_best << ") <<<\n";

    // Build all 8! permutations of map8[0..7]!
    std::array<u8, 8> base_vals = {0, 0, 0, 0, 0, 0, 0, 0};
    for (int i = 0; i < m; ++i) base_vals[i] = u8(1 << i);
    std::sort(base_vals.begin(), base_vals.end());

    struct TopHit {
        int fl;
        std::vector<u8> U, V;
    };
    std::vector<TopHit> hits;
    int min_fl_seen = 999999;
    long long tested = 0;

    std::vector<u8> U, V;
    do {
        // Test leaf_mask9 = 0 (all S leaves -> K <= 36) and leaf_mask9 = 511 (all K leaves -> K <= 27)
        for (int lmask : {0, 511}) {
            build_9leaf_cube(base_vals.data(), lmask, U, V);
            tested++;
            int fl = fast_floor_score(m, targets, U, V);
            if (fl < min_fl_seen) {
                min_fl_seen = fl;
                std::cout << "  New minimum 0-helper floor = " << fl << " (K=" << U.size() << ", lmask=" << lmask << ")\n" << std::flush;
            }
            if (fl <= best_gates) {
                // Sweep all 512 leaf masks on this promising cube embedding!
                int best_local_fl = fl;
                std::vector<u8> bU = U, bV = V;
                for (int lm = 1; lm < 511; ++lm) {
                    build_9leaf_cube(base_vals.data(), lm, U, V);
                    int fl2 = fast_floor_score(m, targets, U, V);
                    if (fl2 < min_fl_seen) {
                        min_fl_seen = fl2;
                        std::cout << "  New minimum 0-helper floor = " << fl2 << " (K=" << U.size() << ", lm=" << lm << ")\n" << std::flush;
                    }
                    if (fl2 < best_local_fl) { best_local_fl = fl2; bU = U; bV = V; }
                }
                hits.push_back({best_local_fl, std::move(bU), std::move(bV)});
            }
        }
    } while (std::next_permutation(base_vals.begin(), base_vals.end()));

    std::sort(hits.begin(), hits.end(), [](const TopHit& a, const TopHit& b) { return a.fl < b.fl; });
    std::cout << "  Tested " << tested << " base cube embeddings; min_floor=" << min_fl_seen
              << ", promising hits=" << hits.size() << "\n" << std::flush;

    // Deduplicate hits by sorted outer_prod set
    std::vector<TopHit> uniq;
    for (auto& h : hits) {
        if (uniq.size() >= 36) break;
        bool dup = false;
        for (auto& u : uniq) if (u.U == h.U && u.V == h.V) { dup = true; break; }
        if (!dup) uniq.push_back(std::move(h));
    }

    for (size_t i = 0; i < uniq.size(); ++i) {
        deep_walk(m, poly, targets, uniq[i].U, uniq[i].V, best_gates, best_fc, out_path, rng, 1500);
    }

    // ALSO test affine/basis-twisted embeddings for m = 6, 7, 8!
    // Sample 4000 random sparse invertible m x m transformations (1..3 shears from identity) on top of standard index order!
    std::cout << "  Running sparse GL_" << m << "(GF(2)) basis-twist + leaf-flip sweep...\n" << std::flush;
    std::vector<TopHit> twist_hits;
    for (int trial = 0; trial < 6000; ++trial) {
        u8 basis[8] = {0};
        for (int i = 0; i < m; ++i) basis[i] = u8(1 << i);
        // Random permutation of m bits + 1..4 elementary row shears!
        std::shuffle(basis, basis + m, rng);
        int n_shears = 1 + (rng() % 4);
        for (int s = 0; s < n_shears; ++s) {
            int a = rng() % m, b = rng() % m;
            if (a != b) basis[a] ^= basis[b];
        }
        // Place zeros at random cube slots if m < 8
        u8 map8[8] = {0};
        std::array<int, 8> slots = {0, 1, 2, 3, 4, 5, 6, 7};
        if (trial % 2 == 0) std::shuffle(slots.begin(), slots.end(), rng);
        for (int i = 0; i < m; ++i) map8[slots[i]] = basis[i];

        for (int lmask : {0, 73, 255, 511, int(rng() & 511)}) {
            build_9leaf_cube(map8, lmask, U, V);
            int fl = fast_floor_score(m, targets, U, V);
            if (fl < min_fl_seen) {
                min_fl_seen = fl;
                std::cout << "  [GL twist] New minimum 0-helper floor = " << fl << " (K=" << U.size() << ")\n" << std::flush;
            }
            if (fl <= best_gates) {
                twist_hits.push_back({fl, U, V});
            }
        }
    }
    std::sort(twist_hits.begin(), twist_hits.end(), [](const TopHit& a, const TopHit& b) { return a.fl < b.fl; });
    for (size_t i = 0; i < std::min<size_t>(twist_hits.size(), 25); ++i) {
        deep_walk(m, poly, targets, twist_hits[i].U, twist_hits[i].V, best_gates, best_fc, out_path, rng, 1500);
    }

    std::cout << "<<< Done m=" << m << " poly=0x" << std::hex << poly << std::dec
              << ": best_gates = " << best_gates << " >>>\n\n" << std::flush;
}

int main(int argc, char** argv) {
    std::string mode = (argc > 1) ? argv[1] : "all";
    std::string out_dir = (argc > 2) ? argv[2] : "attempts/algebraic-bilinear-slp/result";

    if (mode == "gf64" || mode == "all") {
        sweep_cube_embeddings(6, 0x49, 57, out_dir + "/gf64_0x49_deep.slp");
    }
    if (mode == "gf128_89" || mode == "all") {
        sweep_cube_embeddings(7, 0x89, 83, out_dir + "/gf128_0x89_deep.slp");
    }
    if (mode == "gf128_91" || mode == "all") {
        sweep_cube_embeddings(7, 0x91, 82, out_dir + "/gf128_0x91_deep.slp");
    }
    if (mode == "gf256" || mode == "all") {
        sweep_cube_embeddings(8, 0x11B, 107, out_dir + "/gf256_0x11B_deep.slp");
    }
    return 0;
}
