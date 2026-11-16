// bb_isd_hunter.cpp
// Lens 1: 64-bit Bit-Packed Quantum ISD (Randomized Information-Set Pivoting on ker(H_X)
// + Weight-Filtered Pair/Triple Combinations + Stabilizer-Coset Tabu Walk)
// for Bivariate Bicycle Codes [[288,12,18]], [[360,12,<=24]], [[432,12,<=24]], [[504,12,<=30]], [[756,16,<=34]].

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <vector>

struct Vec768 {
    uint64_t w[12] = {0};

    void clear() noexcept {
        for (int i = 0; i < 12; ++i) w[i] = 0;
    }
    bool is_zero() const noexcept {
        uint64_t acc = 0;
        for (int i = 0; i < 12; ++i) acc |= w[i];
        return acc == 0;
    }
    void set_bit(int b) noexcept { w[b >> 6] |= (1ULL << (b & 63)); }
    void flip_bit(int b) noexcept { w[b >> 6] ^= (1ULL << (b & 63)); }
    bool get_bit(int b) const noexcept { return (w[b >> 6] >> (b & 63)) & 1ULL; }

    Vec768 operator^(const Vec768& o) const noexcept {
        Vec768 r;
        for (int i = 0; i < 12; ++i) r.w[i] = w[i] ^ o.w[i];
        return r;
    }
    Vec768& operator^=(const Vec768& o) noexcept {
        for (int i = 0; i < 12; ++i) w[i] ^= o.w[i];
        return *this;
    }
    bool operator==(const Vec768& o) const noexcept {
        for (int i = 0; i < 12; ++i) if (w[i] != o.w[i]) return false;
        return true;
    }
    int weight() const noexcept {
        int s = 0;
        for (int i = 0; i < 12; ++i) s += __builtin_popcountll(w[i]);
        return s;
    }
    int dot_mod2(const Vec768& o) const noexcept {
        uint64_t acc = 0;
        for (int i = 0; i < 12; ++i) acc ^= (w[i] & o.w[i]);
        return __builtin_popcountll(acc) & 1;
    }
};

struct Term { int dx, dy; };

struct BBSpec {
    std::string name;
    int l, m;
    std::vector<Term> A, B;
    int pub_ub;
    bool is_control;
};

struct EchelonSpace {
    int n = 0;
    std::vector<int> piv_of_row;
    std::vector<Vec768> basis;
    std::vector<int> row_at_piv; // size n, -1 if non-pivot

    void build(int num_cols, const std::vector<Vec768>& gens) {
        n = num_cols;
        piv_of_row.clear();
        basis.clear();
        row_at_piv.assign(n, -1);

        for (Vec768 v : gens) {
            for (size_t r = 0; r < basis.size(); ++r) {
                if (v.get_bit(piv_of_row[r])) v ^= basis[r];
            }
            int p = -1;
            for (int c = 0; c < n; ++c) {
                if (v.get_bit(c)) { p = c; break; }
            }
            if (p >= 0) {
                // Eliminate upward too for clean RREF
                for (size_t r = 0; r < basis.size(); ++r) {
                    if (basis[r].get_bit(p)) basis[r] ^= v;
                }
                int idx = static_cast<int>(basis.size());
                piv_of_row.push_back(p);
                basis.push_back(v);
                row_at_piv[p] = idx;
            }
        }
    }

    int dim() const { return static_cast<int>(basis.size()); }

    bool contains(Vec768 v) const noexcept {
        for (size_t r = 0; r < basis.size(); ++r) {
            if (v.get_bit(piv_of_row[r])) v ^= basis[r];
        }
        return v.is_zero();
    }
};

struct BBInstance {
    BBSpec spec;
    int N, n, k;
    std::vector<Vec768> HX, HZ;
    EchelonSpace spanHZ;
    std::vector<Vec768> kerHX;      // basis of ker(H_X)
    std::vector<Vec768> stab_moves; // weight-6 HZ rows + weight-8/10 overlapping pairs!

    void init(const BBSpec& s) {
        spec = s;
        N = s.l * s.m;
        n = 2 * N;
        HX.assign(N, Vec768{});
        HZ.assign(N, Vec768{});

        auto idx = [&](int x, int y) {
            int rx = ((x % s.l) + s.l) % s.l;
            int ry = ((y % s.m) + s.m) % s.m;
            return rx * s.m + ry;
        };

        // Column-multiplication matrix M(P): column (x,y) has 1s at rows (x + dx, y + dy)
        // Equivalently row (rx, ry) of A has 1s at columns (rx - dx, ry - dy),
        // while row (rx, ry) of A^T has 1s at columns (rx + dx, ry + dy)!
        for (int rx = 0; rx < s.l; ++rx) {
            for (int ry = 0; ry < s.m; ++ry) {
                int r = idx(rx, ry);
                for (const auto& t : s.A) {
                    HX[r].set_bit(idx(rx - t.dx, ry - t.dy));
                    HZ[r].set_bit(N + idx(rx + t.dx, ry + t.dy));
                }
                for (const auto& t : s.B) {
                    HX[r].set_bit(N + idx(rx - t.dx, ry - t.dy));
                    HZ[r].set_bit(idx(rx + t.dx, ry + t.dy));
                }
            }
        }

        // Verify H_X * H_Z^T == 0 mod 2
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                if (HX[i].dot_mod2(HZ[j]) != 0) {
                    std::cerr << "FATAL: CSS commutation failed for " << s.name << "\n";
                    std::exit(1);
                }
            }
        }

        EchelonSpace spanHX;
        spanHX.build(n, HX);
        spanHZ.build(n, HZ);
        k = n - spanHX.dim() - spanHZ.dim();

        // Compute basis of ker(H_X) from RREF of spanHX!
        kerHX.clear();
        for (int c = 0; c < n; ++c) {
            if (spanHX.row_at_piv[c] != -1) continue; // free column!
            Vec768 kv;
            kv.set_bit(c);
            for (int r = 0; r < spanHX.dim(); ++r) {
                if (spanHX.basis[r].get_bit(c)) {
                    kv.set_bit(spanHX.piv_of_row[r]);
                }
            }
            kerHX.push_back(kv);
        }

        // Build stabilizer local moves: all N weight-6 rows of H_Z, plus pairs overlapping in >= 2 qubits (weight <= 8)!
        stab_moves = HZ;
        for (int i = 0; i < N; ++i) {
            for (int j = i + 1; j < N; ++j) {
                Vec768 p = HZ[i] ^ HZ[j];
                int pw = p.weight();
                if (pw > 0 && pw <= 8) {
                    stab_moves.push_back(p);
                }
            }
        }
    }

    bool verify_logical(const Vec768& z) const {
        for (const auto& r : HX) {
            if (r.dot_mod2(z) != 0) return false;
        }
        return !spanHZ.contains(z);
    }

    // Greedy + plateau stabilizer coset reduction!
    void reduce_by_stabilizers(Vec768& z, std::mt19937_64& rng) const {
        int cur_w = z.weight();
        bool improved = true;
        while (improved) {
            improved = false;
            for (const auto& sm : stab_moves) {
                Vec768 cand = z ^ sm;
                int cw = cand.weight();
                if (cw < cur_w) {
                    z = cand;
                    cur_w = cw;
                    improved = true;
                }
            }
        }
        // Short neutral plateau walk (overlap == wt(sm)/2) followed by greedy descent
        Vec768 best = z;
        int best_w = cur_w;
        int msz = static_cast<int>(stab_moves.size());
        for (int step = 0; step < 24 && msz > 0; ++step) {
            // Try 12 random stabilizers for a neutral or improving move
            bool moved = false;
            for (int tr = 0; tr < 16; ++tr) {
                const Vec768& sm = stab_moves[rng() % msz];
                Vec768 cand = z ^ sm;
                int cw = cand.weight();
                if (cw <= cur_w) {
                    z = cand;
                    cur_w = cw;
                    moved = true;
                    break;
                }
            }
            if (moved) {
                bool imp2 = true;
                while (imp2) {
                    imp2 = false;
                    for (const auto& sm : stab_moves) {
                        Vec768 cand = z ^ sm;
                        int cw = cand.weight();
                        if (cw < cur_w) {
                            z = cand;
                            cur_w = cw;
                            imp2 = true;
                        }
                    }
                }
                if (cur_w < best_w) {
                    best = z;
                    best_w = cur_w;
                }
            }
        }
        z = best;
    }
};

int main(int argc, char** argv) {
    int piv_iters = (argc >= 2) ? std::stoi(argv[1]) : 12000;
    std::string out_dir = (argc >= 3) ? argv[2] : ".";

    std::vector<BBSpec> specs = {
        {"BB_288_12_18_ctrl", 12, 12, {{3,0},{0,2},{0,7}},   {{0,3},{1,0},{2,0}},   18, true},
        {"BB_360_12_le24",    30,  6, {{9,0},{0,1},{0,2}},   {{0,3},{25,0},{26,0}}, 24, false},
        {"BB_432_12_le24",    18, 12, {{15,0},{0,7},{0,2}},  {{0,9},{7,0},{14,0}},  24, false},
        {"BB_504_12_le30",    42,  6, {{27,0},{0,1},{0,2}},  {{0,3},{37,0},{38,0}}, 30, false},
        {"BB_756_16_le34",    21, 18, {{3,0},{0,10},{0,17}}, {{0,5},{3,0},{19,0}},  34, false},
    };

    std::cout << "=============================================================================\n";
    std::cout << "QUANTUM STERN-LEON ISD + STABILIZER-COSET TABU HUNTER FOR BIVARIATE BICYCLE\n";
    std::cout << "Pivots per code: " << piv_iters << "\n";
    std::cout << "=============================================================================\n";

    std::mt19937_64 rng(0xB1C7C1E20261115ULL);

    for (const auto& sp : specs) {
        auto t0 = std::chrono::steady_clock::now();
        BBInstance bb;
        bb.init(sp);

        int dimK = static_cast<int>(bb.kerHX.size());
        std::vector<int> perm(bb.n);
        std::iota(perm.begin(), perm.end(), 0);

        int best_wt = 999999;
        Vec768 best_vec;
        int hits_at_best = 0;

        int iters_this = (bb.n >= 700) ? (piv_iters / 2) : piv_iters;
        std::vector<Vec768> mat(dimK);

        for (int it = 0; it < iters_this; ++it) {
            std::shuffle(perm.begin(), perm.end(), rng);
            mat = bb.kerHX;

            // Partial/full Gauss-Jordan along column order `perm`!
            int row = 0;
            for (int ci = 0; ci < bb.n && row < dimK; ++ci) {
                int col = perm[ci];
                int sel = -1;
                for (int r = row; r < dimK; ++r) {
                    if (mat[r].get_bit(col)) { sel = r; break; }
                }
                if (sel < 0) continue;
                if (sel != row) std::swap(mat[sel], mat[row]);
                const Vec768 pv = mat[row];
                int w_idx = col >> 6;
                uint64_t bit_mask = 1ULL << (col & 63);
                for (int r = 0; r < dimK; ++r) {
                    if (r != row && (mat[r].w[w_idx] & bit_mask)) {
                        mat[r] ^= pv;
                    }
                }
                ++row;
            }

            // Collect light rows (wt <= pub_ub + 14) that are NOT stabilizers (or all light rows for pairing)
            std::vector<int> light_idx;
            light_idx.reserve(64);
            int single_cap = sp.pub_ub + 12;

            for (int r = 0; r < dimK; ++r) {
                int w = mat[r].weight();
                if (w <= single_cap + 6) light_idx.push_back(r);
                if (w <= single_cap && !bb.spanHZ.contains(mat[r])) {
                    Vec768 cand = mat[r];
                    if (w <= best_wt + 6) bb.reduce_by_stabilizers(cand, rng);
                    int cw = cand.weight();
                    if (cw < best_wt && bb.verify_logical(cand)) {
                        best_wt = cw;
                        best_vec = cand;
                        hits_at_best = 1;
                    } else if (cw == best_wt) {
                        hits_at_best++;
                    }
                }
            }

            // Check pairwise sums of light rows!
            int lsz = static_cast<int>(light_idx.size());
            for (int i = 0; i < lsz; ++i) {
                const Vec768& u = mat[light_idx[i]];
                for (int j = i + 1; j < lsz; ++j) {
                    Vec768 p = u ^ mat[light_idx[j]];
                    int pw = p.weight();
                    if (pw <= best_wt + 6 && pw <= sp.pub_ub + 8) {
                        if (!bb.spanHZ.contains(p)) {
                            bb.reduce_by_stabilizers(p, rng);
                            int cw = p.weight();
                            if (cw < best_wt && bb.verify_logical(p)) {
                                best_wt = cw;
                                best_vec = p;
                                hits_at_best = 1;
                            } else if (cw == best_wt) {
                                hits_at_best++;
                            }
                        }
                    }
                }
            }
        }

        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "[" << std::setw(18) << sp.name << "] [[n=" << bb.n << ", k=" << bb.k << "]] "
                  << "dim(kerHX)=" << dimK << " dim(HZ)=" << bb.spanHZ.dim()
                  << " stab_moves=" << bb.stab_moves.size()
                  << " | pub_ub=" << sp.pub_ub
                  << " -> min_logical_wt=" << best_wt
                  << " (hits=" << hits_at_best << ", " << std::fixed << std::setprecision(2) << elapsed << "s)\n"
                  << std::flush;

        if (!sp.is_control && best_wt < sp.pub_ub && bb.verify_logical(best_vec)) {
            std::string fn = out_dir + "/p1_witness_" + sp.name + "_wt" + std::to_string(best_wt) + ".json";
            std::ofstream out(fn);
            out << "{\n  \"code\": \"" << sp.name << "\",\n"
                << "  \"l\": " << sp.l << ",\n  \"m\": " << sp.m << ",\n"
                << "  \"n\": " << bb.n << ",\n  \"k\": " << bb.k << ",\n"
                << "  \"weight\": " << best_wt << ",\n  \"support\": [";
            bool first = true;
            for (int q = 0; q < bb.n; ++q) {
                if (best_vec.get_bit(q)) {
                    if (!first) out << ", ";
                    out << q;
                    first = false;
                }
            }
            out << "]\n}\n";
            std::cout << "  *** P1 BREAKTHROUGH SAVED TO " << fn << " ***\n" << std::flush;
        }
    }

    return 0;
}
