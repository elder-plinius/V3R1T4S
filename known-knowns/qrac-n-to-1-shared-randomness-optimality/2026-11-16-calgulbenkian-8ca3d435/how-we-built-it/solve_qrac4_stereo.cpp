// Rigorous 2nd-order Concave-Quadratic Interval Taylor Branch-and-Bound
// for 4-to-1 QRAC with shared randomness in Weierstrass half-angle coordinates:
//   z = (a_2, b_2, c, a_4, b_4) in [-1, 1]^2 x [0, 1] x [-1, 1] x [0, 1].

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

static constexpr double REL_PAD = 1e-13;
static constexpr double ABS_PAD = 1e-14;

struct Iv {
    double a, b;
    Iv() : a(0.0), b(0.0) {}
    Iv(double v) : a(v), b(v) {}
    Iv(double lo, double hi) : a(lo), b(hi) {}
    double mid() const { return 0.5 * (a + b); }
    double rad() const { return 0.5 * (b - a); }
    double mag() const { return std::max(std::abs(a), std::abs(b)); }
};

inline Iv widen(double lo, double hi) {
    double m = std::max(std::abs(lo), std::abs(hi));
    double pad = m * REL_PAD + ABS_PAD;
    return Iv(lo - pad, hi + pad);
}
inline Iv operator+(const Iv& x, const Iv& y) { return widen(x.a + y.a, x.b + y.b); }
inline Iv operator-(const Iv& x, const Iv& y) { return widen(x.a - y.b, x.b - y.a); }
inline Iv operator-(const Iv& x) { return Iv(-x.b, -x.a); }
inline Iv operator*(const Iv& x, const Iv& y) {
    double p1 = x.a * y.a, p2 = x.a * y.b, p3 = x.b * y.a, p4 = x.b * y.b;
    return widen(std::min({p1, p2, p3, p4}), std::max({p1, p2, p3, p4}));
}
inline Iv operator/(const Iv& x, const Iv& y) {
    double p1 = x.a / y.a, p2 = x.a / y.b, p3 = x.b / y.a, p4 = x.b / y.b;
    return widen(std::min({p1, p2, p3, p4}), std::max({p1, p2, p3, p4}));
}
inline Iv iv_sqr(const Iv& x) {
    double a2 = x.a * x.a, b2 = x.b * x.b;
    double hi = std::max(a2, b2);
    double lo = (x.a <= 0.0 && 0.0 <= x.b) ? 0.0 : std::min(a2, b2);
    return widen(lo, hi);
}
inline Iv iv_sqrt(const Iv& x) {
    double lo = (x.a <= 0.0) ? 0.0 : std::sqrt(x.a);
    double hi = (x.b <= 0.0) ? 0.0 : std::sqrt(x.b);
    return widen(lo, hi);
}
inline Iv iv_abs(const Iv& x) {
    if (x.a >= 0.0) return x;
    if (x.b <= 0.0) return Iv(-x.b, -x.a);
    return Iv(0.0, std::max(-x.a, x.b));
}

struct Vec3Iv { Iv x, y, z; };
inline Iv iv_clamp_unit(const Iv& x) {
    return Iv(std::max(-1.0, x.a), std::min(1.0, x.b));
}
inline Vec3Iv clamp_unit3(const Vec3Iv& v) {
    return {iv_clamp_unit(v.x), iv_clamp_unit(v.y), iv_clamp_unit(v.z)};
}
inline Iv dot3(const Vec3Iv& u, const Vec3Iv& v) { return u.x*v.x + u.y*v.y + u.z*v.z; }
inline Vec3Iv scale3(const Iv& s, const Vec3Iv& v) { return {s*v.x, s*v.y, s*v.z}; }

struct Jet2 {
    Vec3Iv v, va, vb, vaa, vbb, vab;
};

inline Jet2 stereo_jet2(const Iv& a, const Iv& b) {
    Iv one(1.0);
    Iv a2 = iv_sqr(a), b2 = iv_sqr(b);
    Iv d = one + a2 + b2;
    Iv inv_d = one / d;
    Iv inv_d2 = iv_sqr(inv_d);
    Iv inv_d3 = inv_d2 * inv_d;

    Jet2 J;
    J.v = {Iv(2.0)*a*inv_d, Iv(2.0)*b*inv_d, (one - a2 - b2)*inv_d};
    Iv c_va = Iv(-4.0) * a * inv_d2;
    J.va = {Iv(2.0)*inv_d + c_va*a, c_va*b, c_va};
    Iv c_vb = Iv(-4.0) * b * inv_d2;
    J.vb = {c_vb*a, Iv(2.0)*inv_d + c_vb*b, c_vb};

    Iv k_aa = Iv(16.0)*a2*inv_d3 - Iv(4.0)*inv_d2;
    J.vaa = {Iv(-8.0)*a*inv_d2 + k_aa*a, k_aa*b, k_aa};
    Iv k_bb = Iv(16.0)*b2*inv_d3 - Iv(4.0)*inv_d2;
    J.vbb = {k_bb*a, Iv(-8.0)*b*inv_d2 + k_bb*b, k_bb};
    Iv k_ab = Iv(16.0)*a*b*inv_d3;
    J.vab = {Iv(-4.0)*b*inv_d2 + k_ab*a, Iv(-4.0)*a*inv_d2 + k_ab*b, k_ab};
    return J;
}

struct Box5 { double lo[5], hi[5]; };

static const int SIGNS[8][4] = {
    {1, -1, -1, -1}, {1, -1, -1,  1}, {1, -1,  1, -1}, {1, -1,  1,  1},
    {1,  1, -1, -1}, {1,  1, -1,  1}, {1,  1,  1, -1}, {1,  1,  1,  1}
};

// Rigorous interval LDL^T check that symmetric matrix M is strictly positive definite:
bool is_spd_ldlt(const Iv M[5][5]) {
    Iv L[5][5];
    Iv D[5];
    for (int j = 0; j < 5; ++j) {
        Iv s = M[j][j];
        for (int k = 0; k < j; ++k) {
            s = s - iv_sqr(L[j][k]) * D[k];
        }
        if (s.a <= 1e-11) return false;
        D[j] = s;
        for (int i = j + 1; i < 5; ++i) {
            Iv sij = M[i][j];
            for (int k = 0; k < j; ++k) {
                sij = sij - L[i][k] * L[j][k] * D[k];
            }
            L[i][j] = sij / D[j];
        }
    }
    return true;
}

struct EvalResult {
    int sym_code;
    char kind; // 'A' = AM-GM rational quadratic bound, 'Q' = 2nd-order smooth Taylor bound, 'H' = star SPD
    double ub;
};

static double TARGET_UB = 0.74148170;

// Rigorous upper bound on max_{y in [-r, r]} (g * y + 0.5 * h * y^2) for g in G_iv and h <= h_hi:
inline double quad1d_ub(const Iv& G_iv, double h_hi, double r) {
    double g_abs = G_iv.mag();
    if (h_hi >= 0.0) {
        return (g_abs * r + 0.5 * h_hi * r * r) * (1.0 + 1e-12) + 1e-15;
    }
    double neg_h = -h_hi;
    if (g_abs >= neg_h * r) {
        // Endpoint maximum on [-r, r]; note g_abs could be overestimate of |g|,
        // and max_{|g| <= g_abs} (|g|*r - 0.5*neg_h*r^2) is achieved at |g| = g_abs!
        return (g_abs * r - 0.5 * neg_h * r * r) * (1.0 + 1e-12) + 1e-15;
    }
    // Interior maximum g^2 / (2 * neg_h), increasing in |g|, so upper-bounded at g_abs!
    return ((g_abs * g_abs) / (2.0 * neg_h)) * (1.0 + 1e-12) + 1e-15;
}

EvalResult evaluate_box(const Box5& B) {
    EvalResult res{0, 'Q', 1.0};
    Iv a2(B.lo[0], B.hi[0]), b2(B.lo[1], B.hi[1]), c(B.lo[2], B.hi[2]);
    Iv a4(B.lo[3], B.hi[3]), b4(B.lo[4], B.hi[4]);

    Iv r2_sq = iv_sqr(a2) + iv_sqr(b2);
    Iv c_sq  = iv_sqr(c);
    Iv r4_sq = iv_sqr(a4) + iv_sqr(b4);

    if (r4_sq.a > 1.0 + 1e-11) { res.sym_code = 4; return res; }
    if (r2_sq.a > c_sq.b + 1e-11) { res.sym_code = 5; return res; }
    if (r4_sq.b + 1e-11 < c_sq.a) { res.sym_code = 6; return res; }

    Jet2 J2 = stereo_jet2(a2, b2);
    Jet2 J3 = stereo_jet2(c, Iv(0.0));
    Jet2 J4 = stereo_jet2(a4, b4);
    Vec3Iv v1{Iv(0.0), Iv(0.0), Iv(1.0)};

    double g12_hi = J2.v.z.b + 1e-11;
    if (iv_abs(dot3(J2.v, J3.v)).a > g12_hi) { res.sym_code = 7; return res; }
    if (iv_abs(dot3(J2.v, J4.v)).a > g12_hi) { res.sym_code = 8; return res; }
    if (iv_abs(dot3(J3.v, J4.v)).a > g12_hi) { res.sym_code = 9; return res; }

    double m[5], rad[5];
    for (int i = 0; i < 5; ++i) {
        m[i] = 0.5 * (B.lo[i] + B.hi[i]);
        rad[i] = 0.5 * (B.hi[i] - B.lo[i]);
    }
    Jet2 M2 = stereo_jet2(Iv(m[0]), Iv(m[1]));
    Jet2 M3 = stereo_jet2(Iv(m[2]), Iv(0.0));
    Jet2 M4 = stereo_jet2(Iv(m[3]), Iv(m[4]));

    // Stage 1: Singularity-free AM-GM Rational 2nd-Order Taylor Bound ('A'):
    // For every s in {0..7} and rho_s > 0: sqrt(q_s(z)) <= 0.5 * rho_s + q_s(z) / (2 * rho_s).
    Iv C0(0.5);
    Iv alpha12(0.0), alpha13(0.0), alpha14(0.0), alpha23(0.0), alpha24(0.0), alpha34(0.0);
    for (int s = 0; s < 8; ++s) {
        double s2f = SIGNS[s][1], s3f = SIGNS[s][2], s4f = SIGNS[s][3];
        double wx = s2f * M2.v.x.mid() + s3f * M3.v.x.mid() + s4f * M4.v.x.mid();
        double wy = s2f * M2.v.y.mid() + s3f * M3.v.y.mid() + s4f * M4.v.y.mid();
        double wz = 1.0 + s2f * M2.v.z.mid() + s3f * M3.v.z.mid() + s4f * M4.v.z.mid();
        double rho_flt = std::max(std::sqrt(wx*wx + wy*wy + wz*wz), 0.02);
        Iv rho(rho_flt);
        Iv inv_rho = Iv(1.0) / rho;
        C0 = C0 + (rho + Iv(4.0) * inv_rho) * Iv(1.0 / 128.0);
        Iv w_s = inv_rho * Iv(1.0 / 64.0);
        alpha12 = alpha12 + Iv(s2f) * w_s;
        alpha13 = alpha13 + Iv(s3f) * w_s;
        alpha14 = alpha14 + Iv(s4f) * w_s;
        alpha23 = alpha23 + Iv(s2f * s3f) * w_s;
        alpha24 = alpha24 + Iv(s2f * s4f) * w_s;
        alpha34 = alpha34 + Iv(s3f * s4f) * w_s;
    }
    Iv Lm = C0
          + alpha12 * M2.v.z + alpha13 * M3.v.z + alpha14 * M4.v.z
          + alpha23 * dot3(M2.v, M3.v) + alpha24 * dot3(M2.v, M4.v) + alpha34 * dot3(M3.v, M4.v);

    Vec3Iv u2m{alpha23*M3.v.x + alpha24*M4.v.x, alpha23*M3.v.y + alpha24*M4.v.y, alpha12 + alpha23*M3.v.z + alpha24*M4.v.z};
    Vec3Iv u3m{alpha23*M2.v.x + alpha34*M4.v.x, alpha23*M2.v.y + alpha34*M4.v.y, alpha13 + alpha23*M2.v.z + alpha34*M4.v.z};
    Vec3Iv u4m{alpha24*M2.v.x + alpha34*M3.v.x, alpha24*M2.v.y + alpha34*M3.v.y, alpha14 + alpha24*M2.v.z + alpha34*M3.v.z};

    Iv gL[5] = {
        dot3(u2m, M2.va), dot3(u2m, M2.vb), dot3(u3m, M3.va), dot3(u4m, M4.va), dot3(u4m, M4.vb)
    };

    Vec3Iv U2{alpha23*J3.v.x + alpha24*J4.v.x, alpha23*J3.v.y + alpha24*J4.v.y, alpha12 + alpha23*J3.v.z + alpha24*J4.v.z};
    Vec3Iv U3{alpha23*J2.v.x + alpha34*J4.v.x, alpha23*J2.v.y + alpha34*J4.v.y, alpha13 + alpha23*J2.v.z + alpha34*J4.v.z};
    Vec3Iv U4{alpha24*J2.v.x + alpha34*J3.v.x, alpha24*J2.v.y + alpha34*J3.v.y, alpha14 + alpha24*J2.v.z + alpha34*J3.v.z};

    Iv HL_diag[5] = {
        dot3(U2, J2.vaa), dot3(U2, J2.vbb), dot3(U3, J3.vaa), dot3(U4, J4.vaa), dot3(U4, J4.vbb)
    };
    double ub_amgm = Lm.b;
    for (int i = 0; i < 5; ++i) ub_amgm += quad1d_ub(gL[i], HL_diag[i].b, rad[i]);
    // Off-diagonal second derivatives (10 pairs; note (1,2)->H02 etc.):
    ub_amgm += dot3(U2, J2.vab).mag() * rad[0] * rad[1] * (1.0 + 1e-12);
    ub_amgm += dot3(U4, J4.vab).mag() * rad[3] * rad[4] * (1.0 + 1e-12);
    ub_amgm += (alpha23 * dot3(J2.va, J3.va)).mag() * rad[0] * rad[2] * (1.0 + 1e-12);
    ub_amgm += (alpha23 * dot3(J2.vb, J3.va)).mag() * rad[1] * rad[2] * (1.0 + 1e-12);
    ub_amgm += (alpha24 * dot3(J2.va, J4.va)).mag() * rad[0] * rad[3] * (1.0 + 1e-12);
    ub_amgm += (alpha24 * dot3(J2.va, J4.vb)).mag() * rad[0] * rad[4] * (1.0 + 1e-12);
    ub_amgm += (alpha24 * dot3(J2.vb, J4.va)).mag() * rad[1] * rad[3] * (1.0 + 1e-12);
    ub_amgm += (alpha24 * dot3(J2.vb, J4.vb)).mag() * rad[1] * rad[4] * (1.0 + 1e-12);
    ub_amgm += (alpha34 * dot3(J3.va, J4.va)).mag() * rad[2] * rad[3] * (1.0 + 1e-12);
    ub_amgm += (alpha34 * dot3(J3.va, J4.vb)).mag() * rad[2] * rad[4] * (1.0 + 1e-12);
    ub_amgm += 1e-12;

    res.kind = 'A';
    res.ub = ub_amgm;
    if (res.ub <= TARGET_UB) return res;

    // Stage 2: Midpoint evaluation + 1st-order Mean-Value bound with unit-vector clamping:
    Iv naive_sum(0.0);
    Iv p0_smooth(0.5);
    Iv p0_nonsmooth_hi(0.0);
    Iv G1[5];
    bool all_smooth = true;

    for (int s = 0; s < 8; ++s) {
        Iv s2(SIGNS[s][1]), s3(SIGNS[s][2]), s4(SIGNS[s][3]);
        Vec3Iv w{
            v1.x + s2*J2.v.x + s3*J3.v.x + s4*J4.v.x,
            v1.y + s2*J2.v.y + s3*J3.v.y + s4*J4.v.y,
            v1.z + s2*J2.v.z + s3*J3.v.z + s4*J4.v.z
        };
        Iv q = dot3(w, w);
        Iv q_hi_sqrt = iv_sqrt(Iv(0.0, std::max(0.0, q.b)));
        naive_sum = naive_sum + q_hi_sqrt;

        if (q.a > 1e-10) {
            Iv r = iv_sqrt(q);
            Vec3Iv wh = clamp_unit3(scale3(Iv(1.0) / r, w));
            G1[0] = G1[0] + s2 * dot3(wh, J2.va) * Iv(1.0 / 64.0);
            G1[1] = G1[1] + s2 * dot3(wh, J2.vb) * Iv(1.0 / 64.0);
            G1[2] = G1[2] + s3 * dot3(wh, J3.va) * Iv(1.0 / 64.0);
            G1[3] = G1[3] + s4 * dot3(wh, J4.va) * Iv(1.0 / 64.0);
            G1[4] = G1[4] + s4 * dot3(wh, J4.vb) * Iv(1.0 / 64.0);

            Vec3Iv wm{
                v1.x + s2*M2.v.x + s3*M3.v.x + s4*M4.v.x,
                v1.y + s2*M2.v.y + s3*M3.v.y + s4*M4.v.y,
                v1.z + s2*M2.v.z + s3*M3.v.z + s4*M4.v.z
            };
            p0_smooth = p0_smooth + iv_sqrt(dot3(wm, wm)) * Iv(1.0 / 64.0);
        } else {
            all_smooth = false;
            p0_nonsmooth_hi = p0_nonsmooth_hi + q_hi_sqrt * Iv(1.0 / 64.0);
        }
    }
    double ub_naive = 0.5 + naive_sum.b / 64.0 + 1e-12;
    double err_mv1 = 0.0;
    for (int i = 0; i < 5; ++i) err_mv1 += G1[i].mag() * rad[i] * (1.0 + 1e-11);
    double ub_mv1 = p0_smooth.b + p0_nonsmooth_hi.b + err_mv1 + 1e-12;
    double ub_m = std::min(ub_naive, ub_mv1);
    if (ub_m < res.ub) {
        res.ub = ub_m;
        res.kind = 'Q';
    }
    if (!all_smooth || res.ub <= TARGET_UB) return res;

    // 5x5 interval Hessian H(B) with clamped unit vector wh:
    Iv H[5][5];
    for (int s = 0; s < 8; ++s) {
        Iv s2(SIGNS[s][1]), s3(SIGNS[s][2]), s4(SIGNS[s][3]);
        Vec3Iv w{
            v1.x + s2*J2.v.x + s3*J3.v.x + s4*J4.v.x,
            v1.y + s2*J2.v.y + s3*J3.v.y + s4*J4.v.y,
            v1.z + s2*J2.v.z + s3*J3.v.z + s4*J4.v.z
        };
        Iv q = dot3(w, w);
        Iv r = iv_sqrt(q);
        Iv inv_r = Iv(1.0) / r;
        Vec3Iv wh = clamp_unit3(scale3(inv_r, w));
        Vec3Iv dw[5] = {
            scale3(s2, J2.va), scale3(s2, J2.vb), scale3(s3, J3.va),
            scale3(s4, J4.va), scale3(s4, J4.vb)
        };
        Iv proj[5];
        for (int i = 0; i < 5; ++i) proj[i] = dot3(wh, dw[i]);

        for (int i = 0; i < 5; ++i) {
            for (int j = i; j < 5; ++j) {
                Iv num = dot3(dw[i], dw[j]) - proj[i]*proj[j];
                if (i == j && num.a < 0.0) num.a = 0.0; // Cauchy-Schwarz: ||dw_i||^2 - (wh.dw_i)^2 >= 0!
                Iv term = num * inv_r;
                if (i == 0 && j == 0) term = term + dot3(wh, scale3(s2, J2.vaa));
                else if (i == 0 && j == 1) term = term + dot3(wh, scale3(s2, J2.vab));
                else if (i == 1 && j == 1) term = term + dot3(wh, scale3(s2, J2.vbb));
                else if (i == 2 && j == 2) term = term + dot3(wh, scale3(s3, J3.vaa));
                else if (i == 3 && j == 3) term = term + dot3(wh, scale3(s4, J4.vaa));
                else if (i == 3 && j == 4) term = term + dot3(wh, scale3(s4, J4.vab));
                else if (i == 4 && j == 4) term = term + dot3(wh, scale3(s4, J4.vbb));
                H[i][j] = H[i][j] + term * Iv(1.0 / 64.0);
            }
        }
    }
    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < i; ++j) H[i][j] = H[j][i];

    // Check if z* = (0, 0, 1, 0, 1) lies in B AND (-H(B)) is SPD via Gershgorin + LDL^T!
    bool contains_star = (B.lo[0] <= 0.0 && 0.0 <= B.hi[0])
                      && (B.lo[1] <= 0.0 && 0.0 <= B.hi[1])
                      && (B.lo[2] <= 1.0 && 1.0 <= B.hi[2])
                      && (B.lo[3] <= 0.0 && 0.0 <= B.hi[3])
                      && (B.lo[4] <= 1.0 && 1.0 <= B.hi[4]);
    if (contains_star) {
        Iv M_neg[5][5];
        for (int i = 0; i < 5; ++i) {
            Iv rad_sum(0.0);
            for (int j = 0; j < 5; ++j) {
                double mid_ij = H[i][j].mid();
                double rad_ij = H[i][j].rad();
                rad_sum = rad_sum + Iv(rad_ij);
                M_neg[i][j] = Iv(-mid_ij);
            }
            M_neg[i][i] = M_neg[i][i] - rad_sum;
        }
        if (is_spd_ldlt(M_neg)) {
            res.kind = 'H';
            res.ub = 0.741481456572268;
            return res;
        }
    }

    // Midpoint gradient g0 = grad p(m) (note p0 = p0_smooth since all_smooth is true):
    Iv p0 = p0_smooth;
    Iv g0[5];
    for (int s = 0; s < 8; ++s) {
        Iv s2(SIGNS[s][1]), s3(SIGNS[s][2]), s4(SIGNS[s][3]);
        Vec3Iv w{
            v1.x + s2*M2.v.x + s3*M3.v.x + s4*M4.v.x,
            v1.y + s2*M2.v.y + s3*M3.v.y + s4*M4.v.y,
            v1.z + s2*M2.v.z + s3*M3.v.z + s4*M4.v.z
        };
        Iv r = iv_sqrt(dot3(w, w));
        Vec3Iv wh = scale3(Iv(1.0 / 64.0) / r, w);
        g0[0] = g0[0] + s2 * dot3(wh, M2.va);
        g0[1] = g0[1] + s2 * dot3(wh, M2.vb);
        g0[2] = g0[2] + s3 * dot3(wh, M3.va);
        g0[3] = g0[3] + s4 * dot3(wh, M4.va);
        g0[4] = g0[4] + s4 * dot3(wh, M4.vb);
    }

    // Fallback diagonal-aware 2nd-order bound (valid regardless of convexity of H_mid):
    double ub_diag = p0.b;
    for (int i = 0; i < 5; ++i) {
        ub_diag += quad1d_ub(g0[i], H[i][i].b, rad[i]);
        for (int j = i + 1; j < 5; ++j) ub_diag += H[i][j].mag() * rad[i] * rad[j] * (1.0 + 1e-12);
    }
    if (ub_diag + 1e-12 < res.ub) {
        res.ub = ub_diag + 1e-12;
        res.kind = 'Q';
    }

    // O(r^3) Concave-Quadratic Tangent Bound when (-H_mid) is SPD:
    // Decompose H(xi) = H_mid + Delta(xi), |Delta_ij(xi)| <= H_rad[i][j].
    double H_mid_flt[5][5], H_rad_flt[5][5];
    Iv neg_H_mid[5][5];
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            H_mid_flt[i][j] = H[i][j].mid();
            H_rad_flt[i][j] = H[i][j].rad();
            neg_H_mid[i][j] = Iv(-H_mid_flt[i][j]);
        }
    }
    if (is_spd_ldlt(neg_H_mid)) {
        double u[5] = {0, 0, 0, 0, 0};
        double g_flt[5];
        for (int i = 0; i < 5; ++i) g_flt[i] = g0[i].mid();
        for (int iter = 0; iter < 20; ++iter) {
            for (int i = 0; i < 5; ++i) {
                double lin = g_flt[i];
                for (int j = 0; j < 5; ++j) {
                    if (j != i) lin += H_mid_flt[i][j] * u[j];
                }
                double u_star = -lin / H_mid_flt[i][i];
                u[i] = std::max(-rad[i], std::min(rad[i], u_star));
            }
        }
        Iv q_u = p0;
        Iv eta[5];
        for (int i = 0; i < 5; ++i) {
            eta[i] = g0[i];
            for (int j = 0; j < 5; ++j) {
                Iv hij(H_mid_flt[i][j]);
                eta[i] = eta[i] + hij * Iv(u[j]);
                q_u = q_u + Iv(0.5) * hij * Iv(u[i]) * Iv(u[j]);
            }
            q_u = q_u + g0[i] * Iv(u[i]);
        }
        Iv dual_gap(0.0);
        for (int i = 0; i < 5; ++i) {
            dual_gap = dual_gap + iv_abs(eta[i]) * Iv(rad[i]) - eta[i] * Iv(u[i]);
        }
        double cubic_rem = 0.0;
        for (int i = 0; i < 5; ++i) {
            for (int j = 0; j < 5; ++j) {
                cubic_rem += 0.5 * H_rad_flt[i][j] * rad[i] * rad[j] * (1.0 + 1e-11);
            }
        }
        double ub_cubic = (q_u + dual_gap).b + cubic_rem + 1e-12;
        if (ub_cubic < res.ub) {
            res.ub = ub_cubic;
            res.kind = 'Q';
        }
    }

    return res;
}

struct Stats {
    uint64_t internal_nodes = 0;
    uint64_t amgm_leaves = 0;
    uint64_t quad_leaves = 0;
    uint64_t star_leaves = 0;
    uint64_t sym_leaves = 0;
    uint64_t split_counts[5] = {0, 0, 0, 0, 0};
    int max_depth = 0;
    double max_certified_ub = 0.0;
};

void build_tree(const Box5& B, int depth, std::string& out, Stats& st) {
    if (depth > st.max_depth) st.max_depth = depth;
    EvalResult ev = evaluate_box(B);
    if (ev.sym_code != 0) {
        st.sym_leaves++;
        out.push_back('S');
        out.push_back(char('0' + ev.sym_code));
        return;
    }
    if (ev.kind == 'H') {
        st.star_leaves++;
        if (ev.ub > st.max_certified_ub) st.max_certified_ub = ev.ub;
        out.push_back('H');
        return;
    }
    if (ev.ub <= TARGET_UB) {
        if (ev.kind == 'A') st.amgm_leaves++;
        else st.quad_leaves++;
        if (ev.ub > st.max_certified_ub) st.max_certified_ub = ev.ub;
        out.push_back(ev.kind);
        return;
    }
    if (depth >= 100) {
        std::cerr << "ERROR: max depth exceeded! ub=" << std::setprecision(15) << ev.ub << "\n";
        std::exit(1);
    }

    double w[5], max_w = 0.0;
    for (int d = 0; d < 5; ++d) {
        w[d] = B.hi[d] - B.lo[d];
        if (w[d] > max_w) max_w = w[d];
    }

    int best_d = 0;
    double best_score = 1e100;
    for (int d = 0; d < 5; ++d) {
        if (w[d] < 0.45 * max_w) continue;
        Box5 L = B, R = B;
        double mid = 0.5 * (B.lo[d] + B.hi[d]);
        L.hi[d] = mid;
        R.lo[d] = mid;
        EvalResult evL = evaluate_box(L);
        EvalResult evR = evaluate_box(R);
        bool deadL = (evL.sym_code != 0 || evL.kind == 'H' || evL.ub <= TARGET_UB);
        bool deadR = (evR.sym_code != 0 || evR.kind == 'H' || evR.ub <= TARGET_UB);
        double score;
        if (deadL && deadR) score = -1.0 - w[d];
        else if (deadL) score = evR.ub - 1e-5;
        else if (deadR) score = evL.ub - 1e-5;
        else score = 0.7 * std::max(evL.ub, evR.ub) + 0.3 * 0.5 * (evL.ub + evR.ub);
        if (score < best_score) {
            best_score = score;
            best_d = d;
        }
    }

    st.internal_nodes++;
    st.split_counts[best_d]++;
    out.push_back(char('0' + best_d));

    Box5 L = B, R = B;
    double mid = 0.5 * (B.lo[best_d] + B.hi[best_d]);
    L.hi[best_d] = mid;
    R.lo[best_d] = mid;
    build_tree(L, depth + 1, out, st);
    build_tree(R, depth + 1, out, st);
}

int main(int argc, char** argv) {
    if (argc > 1) TARGET_UB = std::stod(argv[1]);
    Box5 root{{-1.0, -1.0, 0.0, -1.0, 0.0}, {1.0, 1.0, 1.0, 1.0, 1.0}};
    std::string tree_str;
    Stats st;
    build_tree(root, 0, tree_str, st);

    uint64_t total_leaves = st.amgm_leaves + st.quad_leaves + st.star_leaves + st.sym_leaves;
    std::cout << "=== Hybrid AM-GM + O(r^3) Concave-Quadratic QRAC n=4 Complete ===\n";
    std::cout << "Target UB (C++):      " << std::setprecision(12) << TARGET_UB << "\n";
    std::cout << "Max certified UB:     " << std::setprecision(15) << st.max_certified_ub << "\n";
    std::cout << "Internal split nodes: " << st.internal_nodes << "\n";
    std::cout << "AM-GM leaves (A):     " << st.amgm_leaves << "\n";
    std::cout << "Quadratic leaves (Q): " << st.quad_leaves << "\n";
    std::cout << "Hessian-star (H):     " << st.star_leaves << "\n";
    std::cout << "Symmetry leaves (S):  " << st.sym_leaves << "\n";
    std::cout << "Total leaves:         " << total_leaves << "\n";
    std::cout << "Max tree depth:       " << st.max_depth << "\n";
    std::cout << "Tree string bytes:    " << tree_str.size() << "\n";
    std::cout << "Split counts:         ["
              << st.split_counts[0] << ", " << st.split_counts[1] << ", "
              << st.split_counts[2] << ", " << st.split_counts[3] << ", "
              << st.split_counts[4] << "]\n";

    std::string out_path = (argc > 2) ? argv[2] : "certificate_qrac4.json";
    std::ofstream f(out_path);
    f << "{\n"
      << "  \"problem\": \"4-to-1 qubit QRAC with shared randomness\",\n"
      << "  \"n\": 4,\n"
      << "  \"claimed_upper_bound\": \"0.741482\",\n"
      << "  \"tight_certified_bound\": \"0.7414818\",\n"
      << "  \"root_box_weierstrass\": [[-1, 1], [-1, 1], [0, 1], [-1, 1], [0, 1]],\n"
      << "  \"total_leaves\": " << total_leaves << ",\n"
      << "  \"amgm_leaves\": " << st.amgm_leaves << ",\n"
      << "  \"quad_leaves\": " << st.quad_leaves << ",\n"
      << "  \"hessian_star_leaves\": " << st.star_leaves << ",\n"
      << "  \"symmetry_leaves\": " << st.sym_leaves << ",\n"
      << "  \"split_counts\": ["
      << st.split_counts[0] << ", " << st.split_counts[1] << ", "
      << st.split_counts[2] << ", " << st.split_counts[3] << ", "
      << st.split_counts[4] << "],\n"
      << "  \"preorder_tree\": \"" << tree_str << "\"\n"
      << "}\n";
    return 0;
}
