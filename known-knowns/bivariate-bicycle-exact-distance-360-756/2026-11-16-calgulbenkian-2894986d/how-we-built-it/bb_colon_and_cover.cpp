// bb_colon_and_cover.cpp
// Lens 2: Exact F_2[x,y]/(x^l - 1, y^m - 1) Annihilator/Colon Sequence Decomposition,
// Gray-Code Exhaustive One-Sided Annihilator Enumeration, Anchored Colon-Lift Coset Search,
// and Odd/Even Sheet Covering-Torus Quotient Audit for Bivariate Bicycle Codes.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Vec768 {
    uint64_t w[12] = {0};
    bool is_zero() const noexcept {
        uint64_t a = 0;
        for (int i = 0; i < 12; ++i) a |= w[i];
        return a == 0;
    }
    void set_bit(int b) noexcept { w[b >> 6] |= (1ULL << (b & 63)); }
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
    int weight() const noexcept {
        int s = 0;
        for (int i = 0; i < 12; ++i) s += __builtin_popcountll(w[i]);
        return s;
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

struct Echelon {
    int n = 0;
    std::vector<int> piv;
    std::vector<Vec768> basis;
    std::vector<int> row_at_piv;

    void build(int cols, const std::vector<Vec768>& gens) {
        n = cols;
        piv.clear();
        basis.clear();
        row_at_piv.assign(n, -1);
        for (Vec768 v : gens) {
            for (size_t r = 0; r < basis.size(); ++r) {
                if (v.get_bit(piv[r])) v ^= basis[r];
            }
            int p = -1;
            for (int c = 0; c < n; ++c) if (v.get_bit(c)) { p = c; break; }
            if (p >= 0) {
                for (size_t r = 0; r < basis.size(); ++r) {
                    if (basis[r].get_bit(p)) basis[r] ^= v;
                }
                int idx = static_cast<int>(basis.size());
                piv.push_back(p);
                basis.push_back(v);
                row_at_piv[p] = idx;
            }
        }
    }
    int dim() const { return static_cast<int>(basis.size()); }
    bool contains(Vec768 v) const noexcept {
        for (size_t r = 0; r < basis.size(); ++r) {
            if (v.get_bit(piv[r])) v ^= basis[r];
        }
        return v.is_zero();
    }
};

// Multiply polynomial vector `f` (size N = l*m) by polynomial `P` (terms) in F_2[x,y]/(x^l-1, y^m-1)
Vec768 mul_poly(int l, int m, const Vec768& f, const std::vector<Term>& P) {
    int N = l * m;
    Vec768 res;
    for (int x = 0; x < l; ++x) {
        for (int y = 0; y < m; ++y) {
            if (!f.get_bit(x * m + y)) continue;
            for (const auto& t : P) {
                int nx = ((x + t.dx) % l + l) % l;
                int ny = ((y + t.dy) % m + m) % m;
                int bit = nx * m + ny;
                res.w[bit >> 6] ^= (1ULL << (bit & 63));
            }
        }
    }
    (void)N;
    return res;
}

// Compute right kernel of N x N multiplication by `P`: { u in R : P * u == 0 }
std::vector<Vec768> poly_annihilator(int l, int m, const std::vector<Term>& P) {
    int N = l * m;
    // Rows of M(P): row r = (rx, ry) has 1s at cols (rx - dx, ry - dy)
    std::vector<Vec768> rows(N);
    for (int rx = 0; rx < l; ++rx) {
        for (int ry = 0; ry < m; ++ry) {
            int r = rx * m + ry;
            for (const auto& t : P) {
                int cx = ((rx - t.dx) % l + l) % l;
                int cy = ((ry - t.dy) % m + m) % m;
                rows[r].set_bit(cx * m + cy);
            }
        }
    }
    Echelon ec;
    ec.build(N, rows);
    std::vector<Vec768> ker;
    for (int c = 0; c < N; ++c) {
        if (ec.row_at_piv[c] != -1) continue;
        Vec768 kv;
        kv.set_bit(c);
        for (int r = 0; r < ec.dim(); ++r) {
            if (ec.basis[r].get_bit(c)) kv.set_bit(ec.piv[r]);
        }
        ker.push_back(kv);
    }
    return ker;
}

// Solve M(A) * u = rhs over F_2^N; returns true if solvable and sets u0!
bool solve_poly_eq(int l, int m, const std::vector<Term>& A, const Vec768& rhs, Vec768& u0) {
    int N = l * m;
    // Augmented columns: 0..N-1 for variables, column N for rhs!
    // Since N <= 378, N + 1 <= 379 <= 768 fits in Vec768!
    std::vector<Vec768> aug(N);
    for (int rx = 0; rx < l; ++rx) {
        for (int ry = 0; ry < m; ++ry) {
            int r = rx * m + ry;
            for (const auto& t : A) {
                int cx = ((rx - t.dx) % l + l) % l;
                int cy = ((ry - t.dy) % m + m) % m;
                aug[r].set_bit(cx * m + cy);
            }
            if (rhs.get_bit(r)) aug[r].set_bit(N);
        }
    }
    Echelon ec;
    ec.build(N + 1, aug);
    // Inconsistent iff there is a pivot in column N!
    if (ec.row_at_piv[N] != -1) return false;
    u0 = Vec768{};
    for (int r = 0; r < ec.dim(); ++r) {
        if (ec.basis[r].get_bit(N)) {
            u0.set_bit(ec.piv[r]);
        }
    }
    return true;
}

// Compute k(l', m') for a quotient BB code
int compute_quotient_k(int lp, int mp, const std::vector<Term>& A, const std::vector<Term>& B) {
    int N = lp * mp;
    int n = 2 * N;
    std::vector<Vec768> HX(N), HZ(N);
    auto idx = [&](int x, int y) {
        return (((x % lp) + lp) % lp) * mp + (((y % mp) + mp) % mp);
    };
    for (int rx = 0; rx < lp; ++rx) {
        for (int ry = 0; ry < mp; ++ry) {
            int r = idx(rx, ry);
            for (const auto& t : A) {
                HX[r].w[idx(rx - t.dx, ry - t.dy) >> 6] ^= (1ULL << (idx(rx - t.dx, ry - t.dy) & 63));
                int zb = N + idx(rx + t.dx, ry + t.dy);
                HZ[r].w[zb >> 6] ^= (1ULL << (zb & 63));
            }
            for (const auto& t : B) {
                int xb = N + idx(rx - t.dx, ry - t.dy);
                HX[r].w[xb >> 6] ^= (1ULL << (xb & 63));
                HZ[r].w[idx(rx + t.dx, ry + t.dy) >> 6] ^= (1ULL << (idx(rx + t.dx, ry + t.dy) & 63));
            }
        }
    }
    Echelon ex, ez;
    ex.build(n, HX);
    ez.build(n, HZ);
    return n - ex.dim() - ez.dim();
}

int main(int argc, char** argv) {
    std::string out_dir = (argc >= 2) ? argv[1] : ".";

    std::vector<BBSpec> specs = {
        {"BB_288_12_18_ctrl", 12, 12, {{3,0},{0,2},{0,7}},   {{0,3},{1,0},{2,0}},   18, true},
        {"BB_360_12_le24",    30,  6, {{9,0},{0,1},{0,2}},   {{0,3},{25,0},{26,0}}, 24, false},
        {"BB_432_12_le24",    18, 12, {{15,0},{0,7},{0,2}},  {{0,9},{7,0},{14,0}},  24, false},
        {"BB_504_12_le30",    42,  6, {{27,0},{0,1},{0,2}},  {{0,3},{37,0},{38,0}}, 30, false},
        {"BB_756_16_le34",    21, 18, {{3,0},{0,10},{0,17}}, {{0,5},{3,0},{19,0}},  34, false},
    };

    std::cout << "=============================================================================\n";
    std::cout << "THEOREM-1 ANNIHILATOR/COLON PROFILE & COVERING-TORUS AUDIT FOR BB CODES\n";
    std::cout << "=============================================================================\n";

    for (const auto& sp : specs) {
        auto t0 = std::chrono::steady_clock::now();
        int N = sp.l * sp.m;
        int n = 2 * N;

        // Build full HX, HZ for exact logical verification & stabilizer reduction
        std::vector<Vec768> HX(N), HZ(N);
        auto idx = [&](int x, int y) {
            return (((x % sp.l) + sp.l) % sp.l) * sp.m + (((y % sp.m) + sp.m) % sp.m);
        };
        for (int rx = 0; rx < sp.l; ++rx) {
            for (int ry = 0; ry < sp.m; ++ry) {
                int r = idx(rx, ry);
                for (const auto& t : sp.A) {
                    HX[r].set_bit(idx(rx - t.dx, ry - t.dy));
                    HZ[r].set_bit(N + idx(rx + t.dx, ry + t.dy));
                }
                for (const auto& t : sp.B) {
                    HX[r].set_bit(N + idx(rx - t.dx, ry - t.dy));
                    HZ[r].set_bit(idx(rx + t.dx, ry + t.dy));
                }
            }
        }
        Echelon spanHX, spanHZ;
        spanHX.build(n, HX);
        spanHZ.build(n, HZ);
        int k = n - spanHX.dim() - spanHZ.dim();

        auto pack_two = [&](const Vec768& u, const Vec768& v) {
            Vec768 z = u;
            for (int i = 0; i < N; ++i) if (v.get_bit(i)) z.set_bit(N + i);
            return z;
        };

        auto reduce_stab = [&](Vec768& z) {
            int cw = z.weight();
            bool imp = true;
            while (imp) {
                imp = false;
                for (const auto& hz : HZ) {
                    Vec768 c = z ^ hz;
                    int w = c.weight();
                    if (w < cw) { z = c; cw = w; imp = true; }
                }
            }
        };

        // 1. Compute ann(A), B*ann(A), ann(B), A*ann(B), ideal (A), and colon (A:B)!
        auto annA = poly_annihilator(sp.l, sp.m, sp.A);
        auto annB = poly_annihilator(sp.l, sp.m, sp.B);

        std::vector<Vec768> BannA_gens;
        for (const auto& f : annA) BannA_gens.push_back(mul_poly(sp.l, sp.m, f, sp.B));
        Echelon spanBannA;
        spanBannA.build(N, BannA_gens);

        std::vector<Vec768> AannB_gens;
        for (const auto& f : annB) AannB_gens.push_back(mul_poly(sp.l, sp.m, f, sp.A));
        Echelon spanAannB;
        spanAannB.build(N, AannB_gens);

        // Ideal (A): spanned by A * e_i for 0 <= i < N, and ker(M(A)^T) = ann(A_recip) for O(1) solvability screen!
        std::vector<Vec768> idealA_gens(N);
        for (int i = 0; i < N; ++i) {
            Vec768 e; e.set_bit(i);
            idealA_gens[i] = mul_poly(sp.l, sp.m, e, sp.A);
        }
        Echelon spanIdealA;
        spanIdealA.build(N, idealA_gens);

        std::vector<Term> A_recip;
        for (const auto& t : sp.A) A_recip.push_back({-t.dx, -t.dy});
        auto kerAT = poly_annihilator(sp.l, sp.m, A_recip);

        int r_A = static_cast<int>(annA.size()) - spanBannA.dim();
        int r_B = static_cast<int>(annB.size()) - spanAannB.dim();

        // 2. Exhaustive Gray-code enumeration of one-sided logicals in ann(A) \ B*ann(A) and ann(B) \ A*ann(B)!
        int w_ann_left = 999999, w_ann_right = 999999;
        int best_coset_wt = 999999;
        Vec768 best_logical;

        auto enum_ann = [&](const std::vector<Vec768>& basis, const Echelon& sub, bool is_left, int& w_raw_out) {
            int d = static_cast<int>(basis.size());
            if (d == 0 || d > 26) return; // up to 67M Gray steps
            uint64_t total = 1ULL << d;
            Vec768 cur;
            uint64_t prev_g = 0;
            for (uint64_t step = 1; step < total; ++step) {
                uint64_t g = step ^ (step >> 1);
                int bit = __builtin_ctzll(g ^ prev_g);
                cur ^= basis[bit];
                prev_g = g;
                int w = cur.weight();
                if (w < w_raw_out || w <= sp.pub_ub + 6) {
                    if (!sub.contains(cur)) {
                        if (w < w_raw_out) w_raw_out = w;
                        if (w <= best_coset_wt + 6) {
                            Vec768 z = is_left ? pack_two(cur, Vec768{}) : pack_two(Vec768{}, cur);
                            reduce_stab(z);
                            int zw = z.weight();
                            if (zw < best_coset_wt && !spanHZ.contains(z)) {
                                best_coset_wt = zw;
                                best_logical = z;
                            }
                        }
                    }
                }
            }
        };

        enum_ann(annA, spanBannA, true, w_ann_left);
        enum_ann(annB, spanAannB, false, w_ann_right);

        // 3. Anchored Sparse Colon-Lift Search: v with v_0 = 1 and wt(v) in {1, 2, 3}, v not in (A), solvable A*u = B*v!
        int colon_solvable = 0;
        int best_colon_wt = 999999;
        auto test_v = [&](const Vec768& v) {
            if (spanIdealA.contains(v)) return;
            Vec768 Bv = mul_poly(sp.l, sp.m, v, sp.B);
            for (const auto& kw : kerAT) {
                uint64_t acc = 0;
                for (int q = 0; q < 12; ++q) acc ^= (kw.w[q] & Bv.w[q]);
                if (__builtin_popcountll(acc) & 1) return;
            }
            Vec768 u0;
            if (!solve_poly_eq(sp.l, sp.m, sp.A, Bv, u0)) return;
            colon_solvable++;
            // Minimize wt(u0 ^ t) over t in annA (exact Gray code if dim(annA) <= 18, else greedy/pairwise!)
            Vec768 best_u = u0;
            int min_uw = u0.weight();
            int da = static_cast<int>(annA.size());
            if (da > 0 && da <= 18) {
                uint64_t tot = 1ULL << da;
                Vec768 cur = u0;
                uint64_t pg = 0;
                for (uint64_t s = 1; s < tot; ++s) {
                    uint64_t g = s ^ (s >> 1);
                    cur ^= annA[__builtin_ctzll(g ^ pg)];
                    pg = g;
                    int cw = cur.weight();
                    if (cw < min_uw) { min_uw = cw; best_u = cur; }
                }
            } else {
                bool imp = true;
                while (imp) {
                    imp = false;
                    for (const auto& a_vec : annA) {
                        Vec768 c = best_u ^ a_vec;
                        if (c.weight() < min_uw) { best_u = c; min_uw = c.weight(); imp = true; }
                    }
                }
            }
            Vec768 z = pack_two(best_u, v);
            reduce_stab(z);
            int zw = z.weight();
            if (zw < best_colon_wt && !spanHZ.contains(z)) {
                best_colon_wt = zw;
                if (zw < best_coset_wt) {
                    best_coset_wt = zw;
                    best_logical = z;
                }
            }
        };

        // wt(v) = 1, 2, 3 anchored at bit 0 (and symmetric swap A <-> B for wt <= 2)
        {
            Vec768 v1; v1.set_bit(0);
            test_v(v1);
            for (int i = 1; i < N; ++i) {
                Vec768 v2 = v1; v2.set_bit(i);
                test_v(v2);
                for (int j = i + 1; j < N; ++j) {
                    Vec768 v3 = v2; v3.set_bit(j);
                    test_v(v3);
                }
            }
        }

        // 4. Covering-Torus Quotient Audit: all proper divisors (lp | l, mp | m)
        std::vector<std::string> covers;
        for (int lp = 1; lp <= sp.l; ++lp) {
            if (sp.l % lp != 0) continue;
            for (int mp = 1; mp <= sp.m; ++mp) {
                if (sp.m % mp != 0) continue;
                if (lp == sp.l && mp == sp.m) continue;
                int h = (sp.l / lp) * (sp.m / mp);
                int kp = compute_quotient_k(lp, mp, sp.A, sp.B);
                if (kp > 0) {
                    std::ostringstream oss;
                    oss << "(" << lp << "x" << mp << ", n'=" << (2 * lp * mp)
                        << ", k'=" << kp << ", h=" << h << ((h % 2 == 1 && kp == k) ? " ODD_SAME_K!" : "") << ")";
                    covers.push_back(oss.str());
                }
            }
        }

        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        std::cout << "\n[" << sp.name << "] [[n=" << n << ", k=" << k << ", pub_ub=" << sp.pub_ub << "]] ("
                  << std::fixed << std::setprecision(2) << elapsed << "s)\n"
                  << "  Theorem-1: dim(annA)=" << annA.size() << ", dim(B*annA)=" << spanBannA.dim()
                  << " => r_A=" << r_A << " | dim(annB)=" << annB.size() << ", r_B=" << r_B
                  << " | dim(idealA)=" << spanIdealA.dim() << " => r_C=" << (k - r_A) << "\n"
                  << "  Exact one-sided annihilator weights: w_ann_left=" << w_ann_left
                  << ", w_ann_right=" << w_ann_right << "\n"
                  << "  Anchored sparse colon lifts (wt(v)<=3): solvable=" << colon_solvable
                  << ", best_colon_coset_wt=" << best_colon_wt
                  << " | overall_best_wt=" << best_coset_wt << "\n"
                  << "  Nontrivial quotient tori (k'>0): ";
        if (covers.empty()) std::cout << "none";
        for (size_t i = 0; i < covers.size(); ++i) std::cout << (i ? ", " : "") << covers[i];
        std::cout << "\n" << std::flush;

        if (!sp.is_control && best_coset_wt < sp.pub_ub) {
            std::string fn = out_dir + "/p1_colon_witness_" + sp.name + "_wt" + std::to_string(best_coset_wt) + ".json";
            std::ofstream out(fn);
            out << "{\n  \"code\": \"" << sp.name << "\",\n  \"l\": " << sp.l << ",\n  \"m\": " << sp.m
                << ",\n  \"n\": " << n << ",\n  \"k\": " << k << ",\n  \"weight\": " << best_coset_wt << ",\n  \"support\": [";
            bool first = true;
            for (int q = 0; q < n; ++q) {
                if (best_logical.get_bit(q)) {
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
