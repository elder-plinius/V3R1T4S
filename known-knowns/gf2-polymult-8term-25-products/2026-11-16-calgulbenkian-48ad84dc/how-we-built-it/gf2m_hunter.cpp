// gf2m_hunter.cpp
// Unified Algebraic + Exact Steiner-Closure SLP + Coset Product-Exchange Solver
// for Standard-Basis Binary Field Multipliers GF(2^m) = GF(2)[x]/(P(x)), m <= 8.
//
// Strictly single/dual-thread friendly (single-threaded per process, < 50 MB RAM).
// Outputs NIST-compatible .slp files over {AND, XOR} with inputs A0..A(m-1), B0..B(m-1)
// and outputs C0..C(m-1).

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using u8 = uint8_t;
using u32 = uint32_t;
using u64 = uint64_t;

struct Bitset256 {
    u64 w[4] = {0, 0, 0, 0};
    inline bool test(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
    inline void set(int i) { w[i >> 6] |= (1ULL << (i & 63)); }
    inline void reset(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
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
    for (int i = 0; i < m; ++i) {
        if ((u >> i) & 1) {
            mask |= (u64(v) << (i * m));
        }
    }
    return mask;
}

static std::vector<u64> build_targets(int m, int poly) {
    std::vector<u64> tgt(m, 0ULL);
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < m; ++j) {
            int rem = gf2_poly_mul_mod(1 << i, 1 << j, m, poly);
            for (int k = 0; k < m; ++k) {
                if ((rem >> k) & 1) {
                    tgt[k] |= (1ULL << (i * m + j));
                }
            }
        }
    }
    return tgt;
}

// Solve M * W^T = targets over GF(2), where M has K columns (u64 vectors in GF(2)^(m^2)).
// Returns true if solvable, filling W_rows[0..m-1] (each a u64 mask over 0..K-1)
// and null_basis (each a u64 mask over 0..K-1 such that sum_{t in mask} M_t == 0).
static bool solve_W(const std::vector<u64>& M, int m, const std::vector<u64>& targets,
                    std::vector<u64>& W_rows, std::vector<u64>* null_basis = nullptr) {
    int K = (int)M.size();
    if (K > 62) return false;
    // Pivot basis over 64-bit space: each basis element has (vec, comb_mask)
    u64 basis_vec[64] = {0};
    u64 basis_comb[64] = {0};
    bool has_pivot[64] = {false};

    if (null_basis) null_basis->clear();

    for (int t = 0; t < K; ++t) {
        u64 v = M[t];
        u64 c = (1ULL << t);
        while (v) {
            int p = __builtin_ctzll(v);
            if (!has_pivot[p]) {
                has_pivot[p] = true;
                basis_vec[p] = v;
                basis_comb[p] = c;
                v = 0;
                break;
            }
            v ^= basis_vec[p];
            c ^= basis_comb[p];
        }
        if (v == 0 && c != 0 && null_basis) {
            // Note: only added when dependent
            if ((c & (1ULL << t)) && basis_vec[__builtin_ctzll(M[t] ? M[t] : 1)] != M[t]) {
                // Check if c actually reduced v to 0 without inserting
            }
        }
    }
    // Re-extract exact nullspace cleanly if requested
    if (null_basis) {
        null_basis->clear();
        u64 bv[64] = {0}, bc[64] = {0};
        bool hp[64] = {false};
        for (int t = 0; t < K; ++t) {
            u64 v = M[t], c = (1ULL << t);
            bool inserted = false;
            while (v) {
                int p = __builtin_ctzll(v);
                if (!hp[p]) {
                    hp[p] = true;
                    bv[p] = v;
                    bc[p] = c;
                    inserted = true;
                    break;
                }
                v ^= bv[p];
                c ^= bc[p];
            }
            if (!inserted) null_basis->push_back(c);
        }
    }

    W_rows.assign(m, 0ULL);
    for (int k = 0; k < m; ++k) {
        u64 v = targets[k];
        u64 c = 0;
        while (v) {
            int p = __builtin_ctzll(v);
            if (!has_pivot[p]) return false;
            v ^= basis_vec[p];
            c ^= basis_comb[p];
        }
        W_rows[k] = c;
    }
    return true;
}

// Linear SLP on m inputs (m <= 8): nodes 0..m-1 are inputs, nodes >= m are XOR gates.
struct LinearSLP {
    int m = 0;
    std::vector<std::pair<int, int>> gates; // indices into node list (0..m+g-1)
    std::vector<u8> node_val;               // value in GF(2)^m for each node
    int val_to_node[256];                   // -1 if not computed
    LinearSLP() { std::fill(std::begin(val_to_node), std::end(val_to_node), -1); }
};

// Monotone XOR closure on m-bit vectors: starts with B = {1<<0 .. 1<<(m-1)},
// repeatedly adds elements of allowed_pool (= S U H) that are XORs of two elements in B.
static void monotone_closure(int m, const Bitset256& allowed, Bitset256& B,
                             std::vector<u8>& order, std::pair<u8, u8>* parent_vals = nullptr) {
    B = Bitset256{};
    u8 B_list[256];
    int B_len = 0;
    for (int i = 0; i < m; ++i) {
        u8 v = u8(1 << i);
        B.set(v);
        B_list[B_len++] = v;
    }
    order.clear();

    // Collect candidates in allowed \ B
    u8 cands[256];
    int n_cands = 0;
    int lim = 1 << m;
    for (int v = 1; v < lim; ++v) {
        if (allowed.test(v) && !B.test(v)) {
            cands[n_cands++] = u8(v);
        }
    }

    bool progress = true;
    while (progress && n_cands > 0) {
        progress = false;
        for (int ci = 0; ci < n_cands; ) {
            u8 target = cands[ci];
            bool found = false;
            u8 px = 0, py = 0;
            for (int i = 0; i < B_len; ++i) {
                u8 x = B_list[i];
                u8 y = target ^ x;
                if (B.test(y)) {
                    found = true;
                    px = x;
                    py = y;
                    break;
                }
            }
            if (found) {
                B.set(target);
                B_list[B_len++] = target;
                order.push_back(target);
                if (parent_vals) parent_vals[target] = {px, py};
                cands[ci] = cands[--n_cands];
                progress = true;
            } else {
                ++ci;
            }
        }
    }
}

// Fast check-only monotone closure (no parent tracking)
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
    for (int v = 1; v < lim; ++v) {
        if (allowed.test(v) && !B_out.test(v)) cands[n_cands++] = u8(v);
    }
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

// IDA* search for minimum helpers H subset GF(2)^m \ (I U S) up to max_excess
static bool ida_helpers(int m, const Bitset256& S, Bitset256 allowed, const Bitset256& B_cur,
                        const u8* B_list, int B_len, int rem_depth, Bitset256& best_allowed,
                        int& nodes_visited, int max_nodes) {
    if (rem_depth == 0) return B_cur.contains(S);
    if (++nodes_visited > max_nodes) return false;

    // Every missing element of S needs to be covered; if rem_depth == 1, only test h in (B_cur + B_cur) \ B_cur
    // that ALSO equals s ^ b for some unreached s in S and b in B_cur (or creates chain)!
    // Wait: even simpler and 100% exact: the NEXT helper added MUST lie in (B_cur + B_cur) \ allowed!
    Bitset256 cand_H{};
    for (int i = 0; i < B_len; ++i) {
        for (int j = i + 1; j < B_len; ++j) {
            u8 h = B_list[i] ^ B_list[j];
            if (h != 0 && !allowed.test(h) && !B_cur.test(h)) {
                cand_H.set(h);
            }
        }
    }

    // Rank candidate helpers by how many unreached targets in S look like h ^ b for b in B_cur!
    struct HCand { u8 h; int score; };
    HCand hlist[256];
    int nh = 0;
    int lim = 1 << m;
    u8 missing[256];
    int n_miss = 0;
    for (int v = 1; v < lim; ++v)
        if (S.test(v) && !B_cur.test(v)) missing[n_miss++] = u8(v);

    for (int h = 1; h < lim; ++h) {
        if (!cand_H.test(h)) continue;
        int sc = 0;
        for (int mi = 0; mi < n_miss; ++mi) {
            u8 need = missing[mi] ^ u8(h);
            if (B_cur.test(need)) sc += 4;
        }
        // Also bonus if h has small popcount
        sc += (8 - __builtin_popcount(h));
        hlist[nh++] = {u8(h), sc};
    }
    std::sort(hlist, hlist + nh, [](const HCand& a, const HCand& b) { return a.score > b.score; });

    for (int idx = 0; idx < nh; ++idx) {
        u8 h = hlist[idx].h;
        Bitset256 next_allowed = allowed;
        next_allowed.set(h);
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

// Fallback Boyar-Peralta / greedy Steiner builder on m-bit vectors when excess > max_exact_excess
static LinearSLP build_slp_greedy_bp(int m, const std::vector<u8>& targets_vec, std::mt19937& rng, bool randomize) {
    LinearSLP slp;
    slp.m = m;
    for (int i = 0; i < m; ++i) {
        slp.node_val.push_back(u8(1 << i));
        slp.val_to_node[1 << i] = i;
    }
    Bitset256 S{};
    for (u8 t : targets_vec) {
        if (t != 0 && __builtin_popcount(t) > 1) S.set(t);
    }
    if (S.count() == 0) return slp;

    // Compute min XOR distance from current basis B to each target via BFS/1-2-3 sum check
    while (true) {
        // First absorb all 0-cost closures!
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
        // Check remaining targets
        std::vector<u8> rem;
        for (int v = 1; v < (1 << m); ++v)
            if (S.test(v) && slp.val_to_node[v] == -1) rem.push_back(u8(v));
        if (rem.empty()) break;

        // Evaluate all candidate pairs (i, j) from current basis
        int n_nodes = (int)slp.node_val.size();
        // Precompute pairwise sums of current basis for distance-2 check
        Bitset256 pair_sums{};
        for (int i = 0; i < n_nodes; ++i)
            for (int j = i + 1; j < n_nodes; ++j)
                pair_sums.set(slp.node_val[i] ^ slp.node_val[j]);

        int best_score = -1;
        std::vector<std::pair<int, int>> ties;
        for (int i = 0; i < n_nodes; ++i) {
            for (int j = i + 1; j < n_nodes; ++j) {
                u8 cand = slp.node_val[i] ^ slp.node_val[j];
                if (cand == 0 || slp.val_to_node[cand] != -1) continue;
                int sc = 0;
                for (u8 t : rem) {
                    u8 diff = t ^ cand;
                    if (slp.val_to_node[diff] != -1) sc += 100;       // makes t distance 1!
                    else if (pair_sums.test(diff)) sc += 10;          // makes t distance 2!
                    else sc -= __builtin_popcount(diff);
                }
                if (sc > best_score) {
                    best_score = sc;
                    ties.clear();
                    ties.push_back({i, j});
                } else if (sc == best_score) {
                    ties.push_back({i, j});
                }
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
                                    int max_ida_nodes, std::mt19937& rng, int rnbp_tries = 4) {
    Bitset256 S{};
    Bitset256 allowed0{};
    for (int i = 0; i < m; ++i) allowed0.set(1 << i);
    for (u8 r : rows) {
        if (r != 0 && __builtin_popcount(r) > 1) {
            S.set(r);
            allowed0.set(r);
        }
    }
    int s_cnt = S.count();
    if (s_cnt == 0) {
        LinearSLP slp;
        slp.m = m;
        for (int i = 0; i < m; ++i) {
            slp.node_val.push_back(u8(1 << i));
            slp.val_to_node[1 << i] = i;
        }
        return slp;
    }

    Bitset256 B0;
    u8 B0_list[256];
    int B0_len = 0;
    Bitset256 winning_allowed{};
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
        Bitset256 B_fin;
        std::vector<u8> order;
        std::pair<u8, u8> parents[256];
        monotone_closure(m, winning_allowed, B_fin, order, parents);

        // Prune unused helpers via backward reachability from S!
        bool needed[256] = {false};
        for (int v = 1; v < (1 << m); ++v)
            if (S.test(v)) needed[v] = true;
        for (int idx = (int)order.size() - 1; idx >= 0; --idx) {
            u8 v = order[idx];
            if (needed[v]) {
                needed[parents[v].first] = true;
                needed[parents[v].second] = true;
            }
        }

        LinearSLP slp;
        slp.m = m;
        for (int i = 0; i < m; ++i) {
            slp.node_val.push_back(u8(1 << i));
            slp.val_to_node[1 << i] = i;
        }
        for (u8 v : order) {
            if (!needed[v]) continue;
            int u1 = slp.val_to_node[parents[v].first];
            int u2 = slp.val_to_node[parents[v].second];
            int id = (int)slp.node_val.size();
            slp.gates.push_back({u1, u2});
            slp.node_val.push_back(v);
            slp.val_to_node[v] = id;
        }
        return slp;
    }

    // Fallback: best of deterministic + RNBP tries
    LinearSLP best = build_slp_greedy_bp(m, rows, rng, false);
    for (int t = 0; t < rnbp_tries; ++t) {
        LinearSLP cand = build_slp_greedy_bp(m, rows, rng, true);
        if (cand.gates.size() < best.gates.size()) best = std::move(cand);
    }
    return best;
}

// Fast exact/near-exact cost estimator for a single m-input layer (returns number of XOR gates)
static int estimate_layer_cost(int m, const std::vector<u8>& rows, int max_ida_excess,
                               int max_ida_nodes, std::mt19937& rng) {
    LinearSLP slp = solve_linear_layer(m, rows, max_ida_excess, max_ida_nodes, rng, 1);
    return (int)slp.gates.size();
}

struct FullCircuit {
    int m = 0;
    int poly = 0;
    struct Gate {
        std::string op, out, in1, in2;
    };
    std::vector<Gate> gates;
    int n_and = 0;
    int n_xor = 0;
    int depth = 0;
};

// Build complete verified FullCircuit from (U, V, W_rows) using exact U, V, and transposed W^T!
static FullCircuit build_full_circuit(int m, int poly, const std::vector<u8>& U_in, const std::vector<u8>& V_in,
                                      const std::vector<u64>& W_rows_in, std::mt19937& rng,
                                      int max_ida_excess = 3, int max_ida_nodes = 40000) {
    // Filter out any unused products (where column t of W is 0)
    std::vector<u8> U, V, WT;
    int K_orig = (int)U_in.size();
    for (int t = 0; t < K_orig; ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) {
            if ((W_rows_in[r] >> t) & 1ULL) col |= u8(1 << r);
        }
        if (col == 0) continue; // drop dead product!
        U.push_back(U_in[t]);
        V.push_back(V_in[t]);
        WT.push_back(col);
    }
    int K = (int)U.size();

    LinearSLP slpU = solve_linear_layer(m, U, max_ida_excess, max_ida_nodes, rng, 12);
    LinearSLP slpV = (U == V) ? slpU : solve_linear_layer(m, V, max_ida_excess, max_ida_nodes, rng, 12);
    LinearSLP slpWT = solve_linear_layer(m, WT, max_ida_excess, max_ida_nodes, rng, 16);

    FullCircuit fc;
    fc.m = m;
    fc.poly = poly;
    int t_idx = 1;
    auto new_wire = [&]() { return "t" + std::to_string(t_idx++); };

    // 1. Emit top A gates
    std::vector<std::string> nodeU(slpU.node_val.size());
    for (int i = 0; i < m; ++i) nodeU[i] = "A" + std::to_string(i);
    for (size_t g = 0; g < slpU.gates.size(); ++g) {
        std::string w = new_wire();
        auto [i1, i2] = slpU.gates[g];
        fc.gates.push_back({"XOR", w, nodeU[i1], nodeU[i2]});
        nodeU[m + g] = w;
        fc.n_xor++;
    }

    // 2. Emit top B gates
    std::vector<std::string> nodeV(slpV.node_val.size());
    for (int i = 0; i < m; ++i) nodeV[i] = "B" + std::to_string(i);
    for (size_t g = 0; g < slpV.gates.size(); ++g) {
        std::string w = new_wire();
        auto [i1, i2] = slpV.gates[g];
        fc.gates.push_back({"XOR", w, nodeV[i1], nodeV[i2]});
        nodeV[m + g] = w;
        fc.n_xor++;
    }

    // 3. Emit K AND gates
    std::vector<std::string> prod_wire(K);
    for (int t = 0; t < K; ++t) {
        std::string w = new_wire();
        int u_node = slpU.val_to_node[U[t]];
        int v_node = slpV.val_to_node[V[t]];
        fc.gates.push_back({"AND", w, nodeU[u_node], nodeV[v_node]});
        prod_wire[t] = w;
        fc.n_and++;
    }

    // 4. Exact 15-line DAG Transposition of slpWT into bottom layer!
    int num_wt_nodes = (int)slpWT.node_val.size();
    int g_wt = (int)slpWT.gates.size();
    std::vector<std::vector<std::string>> accum_list(num_wt_nodes);
    for (int t = 0; t < K; ++t) {
        int out_node = slpWT.val_to_node[WT[t]];
        accum_list[out_node].push_back(prod_wire[t]);
    }

    // Helper to fold a list of wires into a single wire using balanced binary XOR tree (minimizes depth too!)
    std::unordered_map<std::string, int> wire_depth;
    for (int i = 0; i < m; ++i) {
        wire_depth["A" + std::to_string(i)] = 0;
        wire_depth["B" + std::to_string(i)] = 0;
    }
    for (const auto& gt : fc.gates) {
        wire_depth[gt.out] = std::max(wire_depth[gt.in1], wire_depth[gt.in2]) + 1;
    }

    auto fold_wires = [&](std::vector<std::string>& wl, const std::string& final_name = "") -> std::string {
        while (wl.size() > 1) {
            // Pick two shallowest wires to keep depth minimal for free!
            std::sort(wl.begin(), wl.end(), [&](const std::string& a, const std::string& b) {
                return wire_depth[a] > wire_depth[b]; // smallest at back
            });
            std::string w1 = wl.back(); wl.pop_back();
            std::string w2 = wl.back(); wl.pop_back();
            std::string out = (wl.empty() && !final_name.empty()) ? final_name : new_wire();
            fc.gates.push_back({"XOR", out, w1, w2});
            fc.n_xor++;
            wire_depth[out] = std::max(wire_depth[w1], wire_depth[w2]) + 1;
            wl.push_back(out);
        }
        if (!final_name.empty() && wl[0] != final_name) {
            // Should only happen if C_i equals a single wire directly (fan-in 1); in GF(2^m) C_i always sums >= m products
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
            // Extremely rare case where C_i has 1 term: rewrite last gate defining res to out_c
            for (auto it = fc.gates.rbegin(); it != fc.gates.rend(); ++it) {
                if (it->out == res) {
                    wire_depth[out_c] = wire_depth[res];
                    it->out = out_c;
                    break;
                }
            }
        }
        max_d = std::max(max_d, wire_depth[out_c]);
    }
    fc.depth = max_d;
    return fc;
}

static bool verify_circuit_exhaustive(const FullCircuit& fc) {
    int m = fc.m;
    int n_pairs = 1 << (2 * m);
    // Evaluate in chunks of 64 input pairs!
    for (int base = 0; base < n_pairs; base += 64) {
        int cnt = std::min(64, n_pairs - base);
        u64 mask_valid = (cnt == 64) ? ~0ULL : ((1ULL << cnt) - 1ULL);
        std::unordered_map<std::string, u64> val;
        u64 ref[8] = {0};
        for (int lane = 0; lane < cnt; ++lane) {
            int idx = base + lane;
            int a = idx & ((1 << m) - 1);
            int b = idx >> m;
            for (int i = 0; i < m; ++i) {
                if ((a >> i) & 1) val["A" + std::to_string(i)] |= (1ULL << lane);
                if ((b >> i) & 1) val["B" + std::to_string(i)] |= (1ULL << lane);
            }
            int p = gf2_poly_mul_mod(a, b, m, fc.poly);
            for (int k = 0; k < m; ++k)
                if ((p >> k) & 1) ref[k] |= (1ULL << lane);
        }
        for (const auto& g : fc.gates) {
            u64 v1 = val[g.in1], v2 = val[g.in2];
            if (g.op == "XOR") val[g.out] = v1 ^ v2;
            else if (g.op == "AND") val[g.out] = v1 & v2;
            else if (g.op == "XNOR") val[g.out] = (v1 ^ v2) ^ mask_valid;
        }
        for (int k = 0; k < m; ++k) {
            if ((val["C" + std::to_string(k)] & mask_valid) != ref[k]) return false;
        }
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
    for (const auto& g : fc.gates) {
        out << g.op << " " << g.out << " " << g.in1 << " " << g.in2 << "\n";
    }
    out << "end SLP\n";
    out << "end circuit\n";
}

// Parse product set (U, V) from an existing NIST .slp file!
static bool extract_products_from_slp(const std::string& path, int m, std::vector<u8>& U_out, std::vector<u8>& V_out) {
    std::ifstream in(path);
    if (!in) return false;
    std::unordered_map<std::string, std::pair<u8, u8>> lin; // wire -> (a_mask, b_mask)
    for (int i = 0; i < m; ++i) {
        lin["A" + std::to_string(i)] = {u8(1 << i), 0};
        lin["B" + std::to_string(i)] = {0, u8(1 << i)};
    }
    U_out.clear();
    V_out.clear();
    std::string line;
    bool in_slp = false;
    while (std::getline(in, line)) {
        auto pos = line.find('#');
        if (pos != std::string::npos) line = line.substr(0, pos);
        std::istringstream iss(line);
        std::string tok;
        if (!(iss >> tok)) continue;
        if (tok == "begin") {
            std::string t2; iss >> t2;
            if (t2 == "SLP") in_slp = true;
            continue;
        }
        if (tok == "end") { if (in_slp) break; continue; }
        if (!in_slp) continue;
        std::string out, w1, w2;
        iss >> out >> w1 >> w2;
        if (tok == "XOR") {
            if (lin.count(w1) && lin.count(w2)) {
                lin[out] = {u8(lin[w1].first ^ lin[w2].first), u8(lin[w1].second ^ lin[w2].second)};
            }
        } else if (tok == "AND") {
            auto p1 = lin[w1], p2 = lin[w2];
            if (p1.second == 0 && p2.first == 0) {
                U_out.push_back(p1.first);
                V_out.push_back(p2.second);
            } else if (p1.first == 0 && p2.second == 0) {
                U_out.push_back(p2.first);
                V_out.push_back(p1.second);
            }
        }
    }
    return !U_out.empty();
}

// Evaluate exact layered score (fast) for a product set (U, V)
static int score_product_set(int m, const std::vector<u64>& targets,
                             std::vector<u8>& U, std::vector<u8>& V,
                             std::vector<u64>& W_rows, std::mt19937& rng,
                             int max_ida_exc = 2, int max_ida_nodes = 4000) {
    int K_in = (int)U.size();
    std::vector<u64> M(K_in);
    for (int t = 0; t < K_in; ++t) M[t] = outer_prod(U[t], V[t], m);
    std::vector<u64> null_b;
    if (!solve_W(M, m, targets, W_rows, &null_b)) return 999999;

    // If nullspace is small (1..4), try shifting W_rows to kill columns or shrink distinct WT!
    if (!null_b.empty() && null_b.size() <= 4) {
        int nb = (int)null_b.size();
        // Check if any single column can be zeroed or merged
        u64 best_W[8];
        for (int r = 0; r < m; ++r) best_W[r] = W_rows[r];
        auto wt_floor = [&](const u64* wr) {
            Bitset256 S{};
            int live_k = 0;
            for (int t = 0; t < K_in; ++t) {
                u8 col = 0;
                for (int r = 0; r < m; ++r) if ((wr[r] >> t) & 1ULL) col |= u8(1 << r);
                if (col != 0) {
                    live_k++;
                    if (__builtin_popcount(col) > 1) S.set(col);
                }
            }
            return 2 * live_k + S.count();
        };
        int best_fl = wt_floor(best_W);
        // Coordinate descent over nullspace choices per row!
        for (int pass = 0; pass < 2; ++pass) {
            for (int r = 0; r < m; ++r) {
                u64 orig = best_W[r];
                for (int mask = 1; mask < (1 << nb); ++mask) {
                    u64 cand = orig;
                    for (int b = 0; b < nb; ++b) if ((mask >> b) & 1) cand ^= null_b[b];
                    best_W[r] = cand;
                    int fl = wt_floor(best_W);
                    if (fl < best_fl) { best_fl = fl; orig = cand; }
                    best_W[r] = orig;
                }
            }
        }
        for (int r = 0; r < m; ++r) W_rows[r] = best_W[r];
    }

    // Prune zero columns in-place!
    std::vector<u8> U2, V2, WT;
    std::vector<u64> W2(m, 0ULL);
    for (int t = 0; t < K_in; ++t) {
        u8 col = 0;
        for (int r = 0; r < m; ++r) if ((W_rows[r] >> t) & 1ULL) col |= u8(1 << r);
        if (col == 0) continue;
        int new_t = (int)U2.size();
        for (int r = 0; r < m; ++r) if ((col >> r) & 1) W2[r] |= (1ULL << new_t);
        U2.push_back(U[t]);
        V2.push_back(V[t]);
        WT.push_back(col);
    }
    U = std::move(U2);
    V = std::move(V2);
    W_rows = std::move(W2);
    int K = (int)U.size();

    // Quick lower-bound prune before running IDA*!
    Bitset256 SU{}, SV{}, SWT{};
    for (u8 x : U) if (__builtin_popcount(x) > 1) SU.set(x);
    if (U == V) SV = SU;
    else for (u8 x : V) if (__builtin_popcount(x) > 1) SV.set(x);
    for (u8 x : WT) if (__builtin_popcount(x) > 1) SWT.set(x);

    int lu = estimate_layer_cost(m, U, max_ida_exc, max_ida_nodes, rng);
    int lv = (U == V) ? lu : estimate_layer_cost(m, V, max_ida_exc, max_ida_nodes, rng);
    int lwt = estimate_layer_cost(m, WT, max_ida_exc, max_ida_nodes, rng);
    return (2 * K - m) + lu + lv + lwt;
}

// Compute all valid 1-for-1 (or 2-for-1) rank-1 replacements u' (x) v' in R + span(V_rem)!
// Given basis of V_rem and missing target vector R not in V_rem:
// Find all (u', v') with u' in cand_u such that u' (x) v' in R + V_rem.
static void find_coset_replacements(int m, const std::vector<u64>& V_rem, u64 R,
                                    const std::vector<u8>& cand_u,
                                    std::vector<std::pair<u8, u8>>& out_pairs) {
    out_pairs.clear();
    int d = m * m;
    // Row-echelon basis of V_rem over d bits
    u64 piv[64] = {0};
    bool has_p[64] = {false};
    for (u64 vec : V_rem) {
        u64 v = vec;
        while (v) {
            int p = __builtin_ctzll(v);
            if (!has_p[p]) { has_p[p] = true; piv[p] = v; break; }
            v ^= piv[p];
        }
    }
    auto reduce = [&](u64 v) {
        while (v) {
            int p = __builtin_ctzll(v);
            if (!has_p[p]) break;
            v ^= piv[p];
        }
        // Further reduce non-leading bits at pivot positions!
        return v;
    };
    // Put piv in full RREF so residual modulo V_rem is a unique linear map!
    for (int p = 63; p >= 0; --p) {
        if (!has_p[p]) continue;
        for (int q = 0; q < p; ++q) {
            if (has_p[q] && ((piv[q] >> p) & 1ULL)) piv[q] ^= piv[p];
        }
    }
    auto rref_rem = [&](u64 v) {
        for (int p = 0; p < d; ++p) {
            if (has_p[p] && ((v >> p) & 1ULL)) v ^= piv[p];
        }
        return v;
    };

    u64 R_rem = rref_rem(R);
    if (R_rem == 0) return;

    // For each candidate u', map basis vectors e_0..e_{m-1} of v' to rref_rem(u' x e_j)
    for (u8 u : cand_u) {
        if (u == 0) continue;
        u64 col_rem[8];
        for (int j = 0; j < m; ++j) {
            col_rem[j] = rref_rem(outer_prod(u, u8(1 << j), m));
        }
        // Solve sum_{j} v_j col_rem[j] == R_rem over GF(2) (m <= 8 variables -> tiny!)
        // Even simpler for m <= 8: Gray-code / linear solve! Let's do 8-var Gaussian elimination!
        u64 b_vec[8] = {0};
        u8 b_comb[8] = {0};
        int b_piv[8];
        int nb = 0;
        u8 null_v[8];
        int n_null = 0;
        for (int j = 0; j < m; ++j) {
            u64 vec = col_rem[j];
            u8 comb = u8(1 << j);
            bool dep = true;
            for (int bi = 0; bi < nb; ++bi) {
                if ((vec >> b_piv[bi]) & 1ULL) {
                    vec ^= b_vec[bi];
                    comb ^= b_comb[bi];
                }
            }
            if (vec != 0) {
                int p = __builtin_ctzll(vec);
                // Reduce earlier basis vectors
                for (int bi = 0; bi < nb; ++bi) {
                    if ((b_vec[bi] >> p) & 1ULL) {
                        b_vec[bi] ^= vec;
                        b_comb[bi] ^= comb;
                    }
                }
                b_vec[nb] = vec;
                b_comb[nb] = comb;
                b_piv[nb] = p;
                nb++;
            } else {
                null_v[n_null++] = comb;
            }
        }
        u64 target = R_rem;
        u8 v0 = 0;
        for (int bi = 0; bi < nb; ++bi) {
            if ((target >> b_piv[bi]) & 1ULL) {
                target ^= b_vec[bi];
                v0 ^= b_comb[bi];
            }
        }
        if (target == 0 && v0 != 0) {
            int lim_n = 1 << std::min(n_null, 4);
            for (int nm = 0; nm < lim_n; ++nm) {
                u8 v = v0;
                for (int b = 0; b < std::min(n_null, 4); ++b)
                    if ((nm >> b) & 1) v ^= null_v[b];
                if (v != 0) out_pairs.push_back({u, v});
            }
        }
    }
}

// Local coset-walk + Karatsuba contraction/expansion + SA optimizer on ANY seed (U, V)!
static void optimize_product_set(int m, int poly, const std::vector<u64>& targets,
                                 std::vector<u8> U, std::vector<u8> V,
                                 int& global_best_gates, FullCircuit& global_best_fc,
                                 const std::string& out_path, std::mt19937& rng,
                                 int walk_steps = 400, bool verbose = true) {
    std::vector<u64> W_rows;
    int cur_score = score_product_set(m, targets, U, V, W_rows, rng, 2, 4000);
    if (cur_score >= 999999) return;

    auto check_and_record = [&](const std::vector<u8>& cU, const std::vector<u8>& cV,
                                const std::vector<u64>& cW, int est_sc) {
        if (est_sc <= global_best_gates + 2) {
            FullCircuit fc = build_full_circuit(m, poly, cU, cV, cW, rng, 3, 50000);
            int g = (int)fc.gates.size();
            if (g < global_best_gates) {
                if (verify_circuit_exhaustive(fc)) {
                    global_best_gates = g;
                    global_best_fc = fc;
                    save_slp(fc, out_path);
                    if (verbose) {
                        std::cout << "  [NEW RECORD m=" << m << " poly=0x" << std::hex << poly << std::dec
                                  << "] gates=" << g << " (AND=" << fc.n_and << ", XOR=" << fc.n_xor
                                  << ", depth=" << fc.depth << ")!\n" << std::flush;
                    }
                } else {
                    std::cerr << "  [BUG] Exhaustive check failed on built circuit!\n";
                }
            }
        }
    };

    check_and_record(U, V, W_rows, cur_score);

    // Precompute all non-zero m-bit vectors
    std::vector<u8> all_u;
    for (int x = 1; x < (1 << m); ++x) all_u.push_back(u8(x));

    for (int step = 0; step < walk_steps; ++step) {
        int K = (int)U.size();
        if (K == 0) break;

        // 1. Try 2-for-1 Contraction Moves (both symmetric Karatsuba AND general coset 2-for-1!)
        if (step % 4 == 0 && K > m) {
            // Check all symmetric pairs (u1, u2), (u2, u1) where (u1,u1) and (u2,u2) exist -> contract to (u1^u2, u1^u2)!
            bool contracted = false;
            std::vector<int> perm(K);
            std::iota(perm.begin(), perm.end(), 0);
            std::shuffle(perm.begin(), perm.end(), rng);

            for (int ii = 0; ii < std::min(K, 16) && !contracted; ++ii) {
                int i = perm[ii];
                for (int jj = ii + 1; jj < K && !contracted; ++jj) {
                    int j = perm[jj];
                    // Build V_{-ij}
                    std::vector<u64> V_rem;
                    V_rem.reserve(K - 2);
                    for (int t = 0; t < K; ++t)
                        if (t != i && t != j) V_rem.push_back(outer_prod(U[t], V[t], m));

                    // Check rank deficiency of targets modulo V_rem
                    u64 piv[64] = {0};
                    bool hp[64] = {false};
                    for (u64 vec : V_rem) {
                        u64 v = vec;
                        while (v) {
                            int p = __builtin_ctzll(v);
                            if (!hp[p]) { hp[p] = true; piv[p] = v; break; }
                            v ^= piv[p];
                        }
                    }
                    u64 R1 = 0;
                    int rem_dim = 0;
                    for (int r = 0; r < m; ++r) {
                        u64 v = targets[r];
                        while (v) {
                            int p = __builtin_ctzll(v);
                            if (!hp[p]) break;
                            v ^= piv[p];
                        }
                        if (v != 0) {
                            if (rem_dim == 0) {
                                R1 = v;
                                int p = __builtin_ctzll(v);
                                hp[p] = true;
                                piv[p] = v;
                                rem_dim = 1;
                            } else {
                                rem_dim = 2;
                                break;
                            }
                        }
                    }
                    if (rem_dim <= 1) {
                        std::vector<std::pair<u8, u8>> pairs;
                        if (rem_dim == 0) {
                            pairs.push_back({0, 0});
                        } else {
                            find_coset_replacements(m, V_rem, R1, all_u, pairs);
                        }
                        if (!pairs.empty()) {
                            std::shuffle(pairs.begin(), pairs.end(), rng);
                            int tries = std::min((int)pairs.size(), 12);
                            for (int pi = 0; pi < tries; ++pi) {
                                std::vector<u8> nU, nV;
                                for (int t = 0; t < K; ++t)
                                    if (t != i && t != j) { nU.push_back(U[t]); nV.push_back(V[t]); }
                                if (pairs[pi].first != 0) {
                                    nU.push_back(pairs[pi].first);
                                    nV.push_back(pairs[pi].second);
                                }
                                std::vector<u64> nW;
                                int sc = score_product_set(m, targets, nU, nV, nW, rng, 2, 3000);
                                if (sc <= cur_score) {
                                    U = std::move(nU); V = std::move(nV); W_rows = std::move(nW);
                                    cur_score = sc;
                                    check_and_record(U, V, W_rows, cur_score);
                                    contracted = true;
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            if (contracted) continue;
        }

        // 2. Symmetric 1-for-1 or Karatsuba Expansion move (when U == V, preserve symmetry half the time!)
        if (U == V && (rng() % 2 == 0)) {
            // Pick a symmetric Karatsuba contraction or expansion move!
            // Expansion: pick t with popcount(U[t]) >= 2 where U[t] = x ^ y for two forms x, y already in U
            // and (x,x), (y,y) are in U -> replace (x^y, x^y) by (x, y) and (y, x)!
            Bitset256 diag{};
            for (int t = 0; t < K; ++t) if (U[t] == V[t]) diag.set(U[t]);
            std::vector<int> cands;
            for (int t = 0; t < K; ++t) if (U[t] == V[t] && __builtin_popcount(U[t]) >= 2) cands.push_back(t);
            if (!cands.empty()) {
                int t = cands[rng() % cands.size()];
                u8 z = U[t];
                for (int x = 1; x < (1 << m); ++x) {
                    int y = z ^ x;
                    if (y > x && diag.test(x) && diag.test(y)) {
                        std::vector<u8> nU = U, nV = V;
                        nU[t] = u8(x); nV[t] = u8(y);
                        nU.push_back(u8(y)); nV.push_back(u8(x));
                        std::vector<u64> nW;
                        int sc = score_product_set(m, targets, nU, nV, nW, rng, 2, 3000);
                        if (sc < cur_score || (sc == cur_score && (rng() % 4 == 0))) {
                            U = std::move(nU); V = std::move(nV); W_rows = std::move(nW);
                            cur_score = sc;
                            check_and_record(U, V, W_rows, cur_score);
                            break;
                        }
                    }
                }
            }
        }

        // 3. General 1-for-1 Coset Replacement Move (including ASYMMETRIC u' != v'!)
        K = (int)U.size();
        int idx = rng() % K;
        std::vector<u64> V_rem;
        V_rem.reserve(K - 1);
        for (int t = 0; t < K; ++t)
            if (t != idx) V_rem.push_back(outer_prod(U[t], V[t], m));

        // Find missing target coset R
        u64 piv[64] = {0};
        bool hp[64] = {false};
        for (u64 vec : V_rem) {
            u64 v = vec;
            while (v) {
                int p = __builtin_ctzll(v);
                if (!hp[p]) { hp[p] = true; piv[p] = v; break; }
                v ^= piv[p];
            }
        }
        u64 R = 0;
        for (int r = 0; r < m; ++r) {
            u64 v = targets[r];
            while (v) {
                int p = __builtin_ctzll(v);
                if (!hp[p]) break;
                v ^= piv[p];
            }
            if (v != 0) { R = v; break; }
        }
        if (R == 0) {
            // Free drop!
            U.erase(U.begin() + idx);
            V.erase(V.begin() + idx);
            cur_score = score_product_set(m, targets, U, V, W_rows, rng, 2, 3000);
            check_and_record(U, V, W_rows, cur_score);
            continue;
        }

        std::vector<std::pair<u8, u8>> pairs;
        find_coset_replacements(m, V_rem, R, all_u, pairs);
        if (pairs.empty()) continue;

        // Prioritize (u', v') where u' is already in U or unit, and v' is already in V or unit!
        Bitset256 inU{}, inV{};
        for (int i = 0; i < m; ++i) { inU.set(1 << i); inV.set(1 << i); }
        for (int t = 0; t < K; ++t) if (t != idx) { inU.set(U[t]); inV.set(V[t]); }

        std::sort(pairs.begin(), pairs.end(), [&](const auto& a, const auto& b) {
            int ca = (!inU.test(a.first)) + (!inV.test(a.second));
            int cb = (!inU.test(b.first)) + (!inV.test(b.second));
            return ca < cb;
        });

        int sample_n = std::min((int)pairs.size(), 16);
        int best_sc = 999999;
        std::vector<u8> best_U, best_V;
        std::vector<u64> best_W;

        for (int pi = 0; pi < sample_n; ++pi) {
            int pick = (pi < 10) ? pi : (rng() % pairs.size());
            if (pairs[pick].first == U[idx] && pairs[pick].second == V[idx]) continue;
            std::vector<u8> nU = U, nV = V;
            nU[idx] = pairs[pick].first;
            nV[idx] = pairs[pick].second;
            std::vector<u64> nW;
            int sc = score_product_set(m, targets, nU, nV, nW, rng, 2, 2500);
            if (sc < best_sc) {
                best_sc = sc;
                best_U = std::move(nU);
                best_V = std::move(nV);
                best_W = std::move(nW);
            }
        }
        // Accept strict improvements + plateau moves (and rare +1 uphill moves to escape basins!)
        if (best_sc < cur_score ||
            (best_sc == cur_score && (rng() % 3 == 0)) ||
            (best_sc == cur_score + 1 && (rng() % 25 == 0))) {
            U = std::move(best_U);
            V = std::move(best_V);
            W_rows = std::move(best_W);
            cur_score = best_sc;
            check_and_record(U, V, W_rows, cur_score);
        }
    }
}

// ---------- Algebraic Seed Generators ----------

// Generate all 168 invertible 3x3 matrices over GF(2)
static std::vector<std::array<u8, 3>> gen_gl3() {
    std::vector<std::array<u8, 3>> res;
    for (int r0 = 1; r0 < 8; ++r0)
        for (int r1 = 1; r1 < 8; ++r1)
            if (r1 != r0)
                for (int r2 = 1; r2 < 8; ++r2)
                    if (r2 != r0 && r2 != r1 && r2 != (r0 ^ r1))
                        res.push_back({u8(r0), u8(r1), u8(r2)});
    return res;
}

// 3x3 block with 3-bit mask of which pairs {0,1}, {0,2}, {1,2} use Karatsuba (1) vs Schoolbook (0)
static void append_3x3_block(const std::array<u8, 3>& fA, const std::array<u8, 3>& fB, int kara_mask,
                             std::vector<u8>& U, std::vector<u8>& V) {
    for (int i = 0; i < 3; ++i) { U.push_back(fA[i]); V.push_back(fB[i]); }
    int pairs[3][2] = {{0, 1}, {0, 2}, {1, 2}};
    for (int p = 0; p < 3; ++p) {
        int i = pairs[p][0], j = pairs[p][1];
        if ((kara_mask >> p) & 1) {
            U.push_back(fA[i] ^ fA[j]);
            V.push_back(fB[i] ^ fB[j]);
        } else {
            U.push_back(fA[i]); V.push_back(fB[j]);
            U.push_back(fA[j]); V.push_back(fB[i]);
        }
    }
}

static void hunt_gf64(const std::string& data_slp, const std::string& out_slp) {
    const int m = 6, poly = 0x49;
    auto targets = build_targets(m, poly);
    std::mt19937 rng(20261115);
    int best_gates = 57; // NIST & Swapnil Jain world record = 57
    FullCircuit best_fc;

    std::cout << "=== Hunting GF(2^6) mod x^6 + x^3 + 1 (0x49), record = 57 gates ===\n";

    // 1. Seed from CMT gf64-630-mult.slp + walk!
    std::vector<u8> cmtU, cmtV;
    if (extract_products_from_slp(data_slp, m, cmtU, cmtV)) {
        std::cout << "Loaded CMT seed with K=" << cmtU.size() << " ANDs\n";
        optimize_product_set(m, poly, targets, cmtU, cmtV, best_gates, best_fc, out_slp, rng, 800);
    }

    // 2. GF(4) = GF(2)[x^3] 5-point evaluation (0, inf, 1, w, w^2) -> K = 15..20!
    // alpha_j = (a_j, a_{j+3}) for j=0,1,2.
    {
        auto add_gf4_prod = [](u8 a0, u8 a1, u8 b0, u8 b1, bool kara, std::vector<u8>& U, std::vector<u8>& V) {
            U.push_back(a0); V.push_back(b0);
            U.push_back(a1); V.push_back(b1);
            if (kara) {
                U.push_back(a0 ^ a1); V.push_back(b0 ^ b1);
            } else {
                U.push_back(a0); V.push_back(b1);
                U.push_back(a1); V.push_back(b0);
            }
        };
        u8 al0[2] = {1 << 0, 1 << 3};
        u8 al1[2] = {1 << 1, 1 << 4};
        u8 al2[2] = {1 << 2, 1 << 5};
        // Points: 0 -> al0; inf -> al2; 1 -> al0+al1+al2;
        // w*u = (u1, u0^u1); w^2*u = (u0^u1, u0).
        u8 pts[5][2] = {
            {al0[0], al0[1]},
            {al2[0], al2[1]},
            {u8(al0[0] ^ al1[0] ^ al2[0]), u8(al0[1] ^ al1[1] ^ al2[1])},
            {u8(al0[0] ^ al1[1] ^ al2[0] ^ al2[1]), u8(al0[1] ^ al1[0] ^ al1[1] ^ al2[0])},
            {u8(al0[0] ^ al1[0] ^ al1[1] ^ al2[1]), u8(al0[1] ^ al1[0] ^ al2[0] ^ al2[1])}
        };
        for (int mask = 0; mask < 32; ++mask) {
            std::vector<u8> U, V;
            for (int p = 0; p < 5; ++p)
                add_gf4_prod(pts[p][0], pts[p][1], pts[p][0], pts[p][1], (mask >> p) & 1, U, V);
            optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 300);
        }

        // Also 6-block GF(4) Karatsuba (K = 18..24):
        u8 kpts[6][2] = {
            {al0[0], al0[1]},
            {al1[0], al1[1]},
            {al2[0], al2[1]},
            {u8(al0[0] ^ al1[0]), u8(al0[1] ^ al1[1])},
            {u8(al0[0] ^ al2[0]), u8(al0[1] ^ al2[1])},
            {u8(al1[0] ^ al2[0]), u8(al1[1] ^ al2[1])}
        };
        for (int mask = 0; mask < 64; ++mask) {
            std::vector<u8> U, V;
            for (int p = 0; p < 6; ++p)
                add_gf4_prod(kpts[p][0], kpts[p][1], kpts[p][0], kpts[p][1], (mask >> p) & 1, U, V);
            optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 200);
        }
    }

    // 3. Sweep GL_3(GF(2)) x 512 Karatsuba masks on (A_0, A_1) split!
    auto gl3 = gen_gl3();
    struct CandSeed { int sc; std::vector<u8> U, V; };
    std::vector<CandSeed> top_seeds;

    for (const auto& mat : gl3) {
        std::array<u8, 3> B0 = {mat[0], mat[1], mat[2]};
        std::array<u8, 3> B1 = {u8(mat[0] << 3), u8(mat[1] << 3), u8(mat[2] << 3)};
        std::array<u8, 3> B01 = {u8(B0[0] ^ B1[0]), u8(B0[1] ^ B1[1]), u8(B0[2] ^ B1[2])};

        for (int m0 = 0; m0 < 8; ++m0) {
            for (int m1 = 0; m1 < 8; ++m1) {
                for (int m2 = 0; m2 < 8; ++m2) {
                    // Quick symmetric filter: m0 == m1 first, plus sampled asymmetric
                    if (m0 != m1 && ((m0 + m1 + m2) & 3) != 0) continue;
                    std::vector<u8> U, V;
                    append_3x3_block(B0, B0, m0, U, V);
                    append_3x3_block(B1, B1, m1, U, V);
                    append_3x3_block(B01, B01, m2, U, V);
                    std::vector<u64> W_rows;
                    int sc = score_product_set(m, targets, U, V, W_rows, rng, 1, 500);
                    if (sc <= best_gates + 1) {
                        top_seeds.push_back({sc, U, V});
                    }
                }
            }
        }
    }
    std::sort(top_seeds.begin(), top_seeds.end(), [](const CandSeed& a, const CandSeed& b) { return a.sc < b.sc; });
    std::cout << "  GF(2^6) GL_3 x Karatsuba sweep found " << top_seeds.size() << " promising seeds (best raw="
              << (top_seeds.empty() ? -1 : top_seeds[0].sc) << ")\n";
    for (size_t i = 0; i < std::min<size_t>(top_seeds.size(), 40); ++i) {
        optimize_product_set(m, poly, targets, top_seeds[i].U, top_seeds[i].V, best_gates, best_fc, out_slp, rng, 600);
    }

    // 4. All 63 field generator polynomial bases x^i -> g^i in GF(2^6)!
    for (int g = 2; g < 64; ++g) {
        // Check if g generates GF(2^6) or proper subfield; build 6 powers 1, g, g^2..g^5
        u8 pws[6];
        int cur = 1;
        int rank_chk = 0;
        u8 basis[6] = {0};
        for (int i = 0; i < 6; ++i) {
            pws[i] = u8(cur);
            u8 v = u8(cur);
            for (int b = 0; b < 6; ++b) {
                if ((v >> b) & 1) {
                    if (!basis[b]) { basis[b] = v; rank_chk++; break; }
                    v ^= basis[b];
                }
            }
            cur = gf2_poly_mul_mod(cur, g, m, poly);
        }
        if (rank_chk < 6) continue;
        // Invert 6x6 change of basis so inputs remain standard basis!
        // Specifically, A(x) in new basis has coords c_j = <dual_j, a>. Any invertible 6x6 matrix rows pws[0..5] works directly as linear forms!
        std::array<u8, 3> L0 = {pws[0], pws[1], pws[2]};
        std::array<u8, 3> L1 = {pws[3], pws[4], pws[5]};
        std::array<u8, 3> L01 = {u8(pws[0]^pws[3]), u8(pws[1]^pws[4]), u8(pws[2]^pws[5])};
        for (int km : {0, 7}) {
            std::vector<u8> U, V;
            append_3x3_block(L0, L0, km, U, V);
            append_3x3_block(L1, L1, km, U, V);
            append_3x3_block(L01, L01, km, U, V);
            optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 250);
        }
    }
    std::cout << "=== Finished GF(2^6) 0x49: best_gates = " << best_gates << " ===\n\n";
}

static void hunt_gf128(int poly, int record_gates, const std::string& data_slp, const std::string& out_slp) {
    const int m = 7;
    auto targets = build_targets(m, poly);
    std::mt19937 rng(20261115 + poly);
    int best_gates = record_gates;
    FullCircuit best_fc;

    std::cout << "=== Hunting GF(2^7) mod 0x" << std::hex << poly << std::dec
              << ", world record = " << record_gates << " gates ===\n";

    // 1. Seed from CMT .slp + systematic Karatsuba contractions + coset walk!
    std::vector<u8> cmtU, cmtV;
    if (extract_products_from_slp(data_slp, m, cmtU, cmtV)) {
        std::cout << "Loaded CMT seed with K=" << cmtU.size() << " ANDs\n";
        // First check exact rebuild of CMT seed itself!
        optimize_product_set(m, poly, targets, cmtU, cmtV, best_gates, best_fc, out_slp, rng, 1000);

        // Identify all symmetric pairs in cmtU/cmtV whose diagonals exist, and sample contractions!
        Bitset256 diag{};
        for (size_t t = 0; t < cmtU.size(); ++t) if (cmtU[t] == cmtV[t]) diag.set(cmtU[t]);
        struct SymPair { int i, j; };
        std::vector<SymPair> spairs;
        std::vector<bool> paired(cmtU.size(), false);
        for (size_t i = 0; i < cmtU.size(); ++i) {
            if (paired[i] || cmtU[i] == cmtV[i]) continue;
            for (size_t j = i + 1; j < cmtU.size(); ++j) {
                if (!paired[j] && cmtU[i] == cmtV[j] && cmtV[i] == cmtU[j] &&
                    diag.test(cmtU[i]) && diag.test(cmtV[i])) {
                    spairs.push_back({(int)i, (int)j});
                    paired[i] = paired[j] = true;
                    break;
                }
            }
        }
        std::cout << "  Found " << spairs.size() << " contractible symmetric pairs in CMT seed!\n";
        int np = (int)spairs.size();
        int total_masks = 1 << np;
        struct SubCand { int sc; std::vector<u8> U, V; };
        std::vector<SubCand> best_subs;
        int step_stride = std::max(1, total_masks / 4096);
        for (int mask = 0; mask < total_masks; mask += step_stride) {
            std::vector<bool> skip(cmtU.size(), false);
            std::vector<u8> U, V;
            for (int b = 0; b < np; ++b) {
                if ((mask >> b) & 1) {
                    int i = spairs[b].i, j = spairs[b].j;
                    skip[i] = skip[j] = true;
                    U.push_back(cmtU[i] ^ cmtV[i]);
                    V.push_back(cmtU[i] ^ cmtV[i]);
                }
            }
            for (size_t t = 0; t < cmtU.size(); ++t)
                if (!skip[t]) { U.push_back(cmtU[t]); V.push_back(cmtV[t]); }
            std::vector<u64> W_rows;
            int sc = score_product_set(m, targets, U, V, W_rows, rng, 1, 500);
            if (sc <= best_gates + 3) best_subs.push_back({sc, U, V});
        }
        // Also test structured masks (contract all 9 pairs in the 3x3 blocks, or 6 pairs, etc.)
        for (int trial = 0; trial < 1000; ++trial) {
            int mask = rng() % total_masks;
            std::vector<bool> skip(cmtU.size(), false);
            std::vector<u8> U, V;
            for (int b = 0; b < np; ++b) {
                if ((mask >> b) & 1) {
                    int i = spairs[b].i, j = spairs[b].j;
                    skip[i] = skip[j] = true;
                    U.push_back(cmtU[i] ^ cmtV[i]);
                    V.push_back(cmtU[i] ^ cmtV[i]);
                }
            }
            for (size_t t = 0; t < cmtU.size(); ++t)
                if (!skip[t]) { U.push_back(cmtU[t]); V.push_back(cmtV[t]); }
            std::vector<u64> W_rows;
            int sc = score_product_set(m, targets, U, V, W_rows, rng, 1, 500);
            if (sc <= best_gates + 3) best_subs.push_back({sc, U, V});
        }
        std::sort(best_subs.begin(), best_subs.end(), [](const SubCand& a, const SubCand& b) { return a.sc < b.sc; });
        std::cout << "  CMT contraction sweep best raw score = "
                  << (best_subs.empty() ? -1 : best_subs[0].sc) << " (from " << best_subs.size() << " hits)\n";
        for (size_t i = 0; i < std::min<size_t>(best_subs.size(), 30); ++i) {
            optimize_product_set(m, poly, targets, best_subs[i].U, best_subs[i].V, best_gates, best_fc, out_slp, rng, 700);
        }
    }

    // 2. General 1 + 3 + 3 splits across ALL 7 singleton positions & stride choices + 8-bit padded S/K splits!
    for (int sing = 0; sing < 7; ++sing) {
        std::vector<u8> rem;
        for (int i = 0; i < 7; ++i) if (i != sing) rem.push_back(u8(1 << i));
        // Split rem into two 3-tuples: contiguous {0,1,2}/{3,4,5} and interleaved {0,2,4}/{1,3,5}
        int splits[2][6] = {{0, 1, 2, 3, 4, 5}, {0, 2, 4, 1, 3, 5}};
        for (int sp = 0; sp < 2; ++sp) {
            std::array<u8, 3> B0 = {rem[splits[sp][0]], rem[splits[sp][1]], rem[splits[sp][2]]};
            std::array<u8, 3> B1 = {rem[splits[sp][3]], rem[splits[sp][4]], rem[splits[sp][5]]};
            std::array<u8, 3> B01 = {u8(B0[0]^B1[0]), u8(B0[1]^B1[1]), u8(B0[2]^B1[2])};
            u8 sbit = u8(1 << sing);
            for (int km : {0, 3, 5, 6, 7}) {
                for (int sing_kara = 0; sing_kara < 2; ++sing_kara) {
                    std::vector<u8> U, V;
                    U.push_back(sbit); V.push_back(sbit);
                    for (u8 rbit : rem) {
                        if (sing_kara) {
                            U.push_back(sbit ^ rbit); V.push_back(sbit ^ rbit);
                        } else {
                            U.push_back(sbit); V.push_back(rbit);
                            U.push_back(rbit); V.push_back(sbit);
                        }
                    }
                    append_3x3_block(B0, B0, km, U, V);
                    append_3x3_block(B1, B1, km, U, V);
                    append_3x3_block(B01, B01, km, U, V);
                    optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 350);
                }
            }
        }
    }

    // 3. Padded 8-bit cube S/K splits (all 8 schemes x 8 dropped positions)!
    for (int scheme = 0; scheme < 8; ++scheme) {
        for (int drop = 0; drop < 8; ++drop) {
            auto map_idx = [&](int idx8) -> u8 {
                if (idx8 == drop) return 0;
                int real_i = (idx8 < drop) ? idx8 : (idx8 - 1);
                return u8(1 << real_i);
            };
            // Recursive build across 3 cube dimensions
            struct PairUV { u8 u, v; };
            std::vector<PairUV> list = {{0, 0}}; // bitmasks over 8-bit index? Build recursively on vectors of length 8!
            std::vector<std::pair<u8, u8>> forms8 = {{1, 1}}; // over 8 bits -> use uint8_t mask!
            for (int dim = 0; dim < 3; ++dim) {
                int step = 1 << dim;
                bool is_k = (scheme >> dim) & 1;
                std::vector<std::pair<u8, u8>> next;
                for (auto [fu, fv] : forms8) {
                    u8 fu_hi = u8(fu << step), fv_hi = u8(fv << step);
                    next.push_back({fu, fv});
                    next.push_back({fu_hi, fv_hi});
                    if (is_k) {
                        next.push_back({u8(fu ^ fu_hi), u8(fv ^ fv_hi)});
                    } else {
                        next.push_back({fu, fv_hi});
                        next.push_back({fu_hi, fv});
                    }
                }
                forms8 = std::move(next);
            }
            std::vector<u8> U, V;
            for (auto [fu8, fv8] : forms8) {
                u8 u7 = 0, v7 = 0;
                for (int b = 0; b < 8; ++b) {
                    if ((fu8 >> b) & 1) u7 ^= map_idx(b);
                    if ((fv8 >> b) & 1) v7 ^= map_idx(b);
                }
                if (u7 != 0 && v7 != 0) { U.push_back(u7); V.push_back(v7); }
            }
            std::vector<u64> W_rows;
            int sc = score_product_set(m, targets, U, V, W_rows, rng, 1, 800);
            if (sc <= best_gates + 3) {
                optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 500);
            }
        }
    }
    std::cout << "=== Finished GF(2^7) 0x" << std::hex << poly << std::dec << ": best_gates = " << best_gates << " ===\n\n";
}

static void hunt_gf256_aes(const std::string& data_slp, const std::string& out_slp) {
    const int m = 8, poly = 0x11B;
    auto targets = build_targets(m, poly);
    std::mt19937 rng(20261115 + 0x11B);
    int best_gates = 107; // Swapnil Jain Oct 2026 world record = 107 (NIST = 117)
    FullCircuit best_fc;

    std::cout << "=== Hunting GF(2^8) AES mod 0x11B, world record = 107 gates (NIST = 117) ===\n";

    // 1. Build all 8 S/K cube-split schemes (especially S x K x K -> K=36 and 1-leaf Karatsuba -> K=35!)
    // and check EXACT Steiner-closure scores + run asymmetric coset walks!
    for (int scheme = 0; scheme < 8; ++scheme) {
        std::vector<std::pair<u8, u8>> forms = {{1, 1}};
        for (int dim = 0; dim < 3; ++dim) {
            int step = 1 << dim;
            bool is_k = (scheme >> dim) & 1;
            std::vector<std::pair<u8, u8>> next;
            for (auto [fu, fv] : forms) {
                u8 fu_hi = u8(fu << step), fv_hi = u8(fv << step);
                next.push_back({fu, fv});
                next.push_back({fu_hi, fv_hi});
                if (is_k) {
                    next.push_back({u8(fu ^ fu_hi), u8(fv ^ fv_hi)});
                } else {
                    next.push_back({fu, fv_hi});
                    next.push_back({fu_hi, fv});
                }
            }
            forms = std::move(next);
        }
        std::vector<u8> U, V;
        for (auto [u, v] : forms) { U.push_back(u); V.push_back(v); }
        std::vector<u64> W_rows;
        int sc = score_product_set(m, targets, U, V, W_rows, rng, 3, 50000);
        std::cout << "  Cube scheme " << scheme << " (K=" << U.size() << ") exact/IDA score = " << sc << "\n";
        if (sc <= 112) {
            optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 1500);
        }
    }

    // 2. Also test GF(16)^2 tower bases & non-dyadic 2 + 3 + 3 / 1 + 3 + 4 splits!
    // Find elements of order 15 (generating GF(16) inside GF(256)): x^(255/15) = x^17!
    int g16 = 1;
    for (int e = 0; e < 17; ++e) g16 = gf2_poly_mul_mod(g16, 3, m, poly); // 3 = x+1 is primitive in AES field!
    // Build tower basis {1, g16, g16^2, g16^3, theta, theta*g16, theta*g16^2, theta*g16^3}
    for (int theta : {2, 3, 6, 7}) {
        u8 tb[8];
        int cur = 1;
        for (int i = 0; i < 4; ++i) {
            tb[i] = u8(cur);
            tb[4 + i] = u8(gf2_poly_mul_mod(cur, theta, m, poly));
            cur = gf2_poly_mul_mod(cur, g16, m, poly);
        }
        // Check invertibility of tb[0..7]
        u8 piv[8] = {0}; int rk = 0;
        for (int i = 0; i < 8; ++i) {
            u8 v = tb[i];
            for (int b = 0; b < 8; ++b) if ((v >> b) & 1) { if (!piv[b]) { piv[b] = v; rk++; break; } v ^= piv[b]; }
        }
        if (rk < 8) continue;
        // Apply K x K x K (27 ANDs) and K x S x K (36 ANDs) and S x K x K (36 ANDs) in this tower basis!
        for (int scheme : {6, 5, 7}) {
            std::vector<std::pair<u8, u8>> forms = {{1, 1}};
            for (int dim = 0; dim < 3; ++dim) {
                int step = 1 << dim;
                bool is_k = (scheme >> dim) & 1;
                std::vector<std::pair<u8, u8>> next;
                for (auto [fu, fv] : forms) {
                    u8 fu_hi = u8(fu << step), fv_hi = u8(fv << step);
                    next.push_back({fu, fv});
                    next.push_back({fu_hi, fv_hi});
                    if (is_k) next.push_back({u8(fu ^ fu_hi), u8(fv ^ fv_hi)});
                    else { next.push_back({fu, fv_hi}); next.push_back({fu_hi, fv}); }
                }
                forms = std::move(next);
            }
            std::vector<u8> U, V;
            for (auto [fu, fv] : forms) {
                u8 u = 0, v = 0;
                for (int b = 0; b < 8; ++b) {
                    if ((fu >> b) & 1) u ^= tb[b];
                    if ((fv >> b) & 1) v ^= tb[b];
                }
                U.push_back(u); V.push_back(v);
            }
            optimize_product_set(m, poly, targets, U, V, best_gates, best_fc, out_slp, rng, 600);
        }
    }
    std::cout << "=== Finished GF(2^8) 0x11B: best_gates = " << best_gates << " ===\n\n";
}

int main(int argc, char** argv) {
    std::string mode = (argc > 1) ? argv[1] : "all";
    std::string data_dir = (argc > 2) ? argv[2] : "data";
    std::string out_dir = (argc > 3) ? argv[3] : "attempts/algebraic-bilinear-slp/result";

    if (mode == "gf64" || mode == "all") {
        hunt_gf64(data_dir + "/gf64-630-mult.slp", out_dir + "/gf64_0x49_best.slp");
    }
    if (mode == "gf128_91" || mode == "all") {
        hunt_gf128(0x91, 84, data_dir + "/gf128-740-mult.slp", out_dir + "/gf128_0x91_best.slp");
    }
    if (mode == "gf128_89" || mode == "all") {
        hunt_gf128(0x89, 83, data_dir + "/gf128-730-mult.slp", out_dir + "/gf128_0x89_best.slp");
    }
    if (mode == "gf256" || mode == "all") {
        hunt_gf256_aes(data_dir + "/gf256-84310-mult.slp", out_dir + "/gf256_0x11B_best.slp");
    }
    return 0;
}
