#include <algorithm>
#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <omp.h>
#include <random>
#include <string>
#include <vector>

using cd = std::complex<double>;

struct ComplexMat {
    int d, n;
    std::vector<double> re, im;
    ComplexMat() : d(0), n(0) {}
    ComplexMat(int d_, int n_) : d(d_), n(n_), re(d_ * n_, 0.0), im(d_ * n_, 0.0) {}
};

static inline void normalize_all(ComplexMat& M) {
    for (int i = 0; i < M.n; ++i) {
        double s = 0.0;
        const int off = i * M.d;
        for (int c = 0; c < M.d; ++c) {
            s += M.re[off + c] * M.re[off + c] + M.im[off + c] * M.im[off + c];
        }
        double inv = 1.0 / std::sqrt(std::max(s, 1e-30));
        for (int c = 0; c < M.d; ++c) {
            M.re[off + c] *= inv;
            M.im[off + c] *= inv;
        }
    }
}

static bool load_gos_txt(const std::string& path, int d, int n, ComplexMat& M) {
    std::ifstream in(path);
    if (!in) return false;
    std::vector<double> vals;
    double x;
    while (in >> x) vals.push_back(x);
    if ((int)vals.size() != 2 * d * n) return false;
    M = ComplexMat(d, n);
    int half = d * n;
    for (int i = 0; i < half; ++i) {
        M.re[i] = vals[i];
        M.im[i] = vals[half + i];
    }
    normalize_all(M);
    return true;
}

static void save_gos_txt(const std::string& path, const ComplexMat& M) {
    std::ofstream out(path);
    out << std::setprecision(18) << std::fixed;
    for (int i = 0; i < M.n; ++i) {
        for (int c = 0; c < M.d; ++c) {
            if (c) out << ' ';
            out << M.re[i * M.d + c];
        }
        out << '\n';
    }
    for (int i = 0; i < M.n; ++i) {
        for (int c = 0; c < M.d; ++c) {
            if (c) out << ' ';
            out << M.im[i * M.d + c];
        }
        out << '\n';
    }
}

static double eval_mu(const ComplexMat& M) {
    const int d = M.d, n = M.n;
    double max_sq = 0.0;
    for (int j = 0; j < n; ++j) {
        const double* rj = &M.re[j * d];
        const double* ij = &M.im[j * d];
        for (int k = j + 1; k < n; ++k) {
            const double* rk = &M.re[k * d];
            const double* ik = &M.im[k * d];
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) {
                vr += rj[c] * rk[c] + ij[c] * ik[c];
                vi += rj[c] * ik[c] - ij[c] * rk[c];
            }
            double sq = vr * vr + vi * vi;
            if (sq > max_sq) max_sq = sq;
        }
    }
    return std::sqrt(max_sq);
}

static void hermitian_jacobi(int n, std::vector<cd>& H, std::vector<double>& evals, std::vector<cd>& U) {
    U.assign(n * n, cd(0.0, 0.0));
    for (int i = 0; i < n; ++i) U[i * n + i] = cd(1.0, 0.0);
    for (int sweep = 0; sweep < 14; ++sweep) {
        double off_sum = 0.0;
        for (int p = 0; p < n; ++p)
            for (int q = p + 1; q < n; ++q)
                off_sum += std::norm(H[p * n + q]);
        if (off_sum < 1e-26) break;
        double thresh = (sweep < 3) ? 0.1 * std::sqrt(off_sum) / n : 0.0;
        for (int p = 0; p < n; ++p) {
            for (int q = p + 1; q < n; ++q) {
                cd hpq = H[p * n + q];
                double mag = std::abs(hpq);
                if (mag <= thresh || mag < 1e-16) continue;
                cd phase = hpq / mag;
                double hpp = H[p * n + p].real(), hqq = H[q * n + q].real();
                double diff = hqq - hpp;
                double t;
                if (std::abs(diff) < 1e-18 * mag) t = 1.0;
                else {
                    double tau = diff / (2.0 * mag);
                    t = (tau >= 0.0 ? 1.0 : -1.0) / (std::abs(tau) + std::sqrt(1.0 + tau * tau));
                }
                double c = 1.0 / std::sqrt(1.0 + t * t), s = t * c;
                cd sph_conj = s * std::conj(phase), sph = s * phase;
                for (int r = 0; r < n; ++r) {
                    if (r == p || r == q) continue;
                    cd hrp = H[r * n + p], hrq = H[r * n + q];
                    cd np = c * hrp - sph_conj * hrq, nq = sph * hrp + c * hrq;
                    H[r * n + p] = np; H[p * n + r] = std::conj(np);
                    H[r * n + q] = nq; H[q * n + r] = std::conj(nq);
                }
                H[p * n + p] = cd(hpp - t * mag, 0.0);
                H[q * n + q] = cd(hqq + t * mag, 0.0);
                H[p * n + q] = H[q * n + p] = cd(0.0, 0.0);
                for (int r = 0; r < n; ++r) {
                    cd up = U[r * n + p], uq = U[r * n + q];
                    U[r * n + p] = c * up - sph_conj * uq;
                    U[r * n + q] = sph * up + c * uq;
                }
            }
        }
    }
    std::vector<int> perm(n);
    evals.resize(n);
    for (int i = 0; i < n; ++i) { evals[i] = H[i * n + i].real(); perm[i] = i; }
    std::sort(perm.begin(), perm.end(), [&](int a, int b) { return evals[a] > evals[b]; });
    std::vector<double> sevals(n);
    std::vector<cd> sU(n * n);
    for (int j = 0; j < n; ++j) {
        sevals[j] = evals[perm[j]];
        for (int r = 0; r < n; ++r) sU[r * n + j] = U[r * n + perm[j]];
    }
    evals.swap(sevals); U.swap(sU);
}

static void project_rank_d(int d, int n, const std::vector<cd>& G, ComplexMat& Phi_out, std::vector<cd>& G_out, bool tight_frame) {
    std::vector<cd> H = G;
    std::vector<double> evals;
    std::vector<cd> U;
    hermitian_jacobi(n, H, evals, U);
    Phi_out = ComplexMat(d, n);
    for (int k = 0; k < d; ++k) {
        double lam = tight_frame ? ((double)n / d) : std::max(evals[k], 0.0);
        double w = std::sqrt(lam);
        for (int j = 0; j < n; ++j) {
            cd v = std::conj(U[j * n + k]) * w;
            Phi_out.re[j * d + k] = v.real();
            Phi_out.im[j * d + k] = v.imag();
        }
    }
    normalize_all(Phi_out);
    G_out.assign(n * n, cd(0.0, 0.0));
    for (int j = 0; j < n; ++j) {
        G_out[j * n + j] = cd(1.0, 0.0);
        for (int k = j + 1; k < n; ++k) {
            cd s(0.0, 0.0);
            for (int c = 0; c < d; ++c) {
                s += std::conj(cd(Phi_out.re[j * d + c], Phi_out.im[j * d + c])) * cd(Phi_out.re[k * d + c], Phi_out.im[k * d + c]);
            }
            G_out[j * n + k] = s; G_out[k * n + j] = std::conj(s);
        }
    }
}

static void project_coherence(int n, const std::vector<cd>& G, double mu_cap, std::vector<cd>& G_out) {
    G_out.resize(n * n);
    for (int j = 0; j < n; ++j) {
        G_out[j * n + j] = cd(1.0, 0.0);
        for (int k = j + 1; k < n; ++k) {
            cd g = 0.5 * (G[j * n + k] + std::conj(G[k * n + j]));
            double mag = std::abs(g);
            if (mag > mu_cap) g *= (mu_cap / mag);
            G_out[j * n + k] = g; G_out[k * n + j] = std::conj(g);
        }
    }
}

// Smooth Exact-Minimax Augmented Lagrangian L-BFGS on (Phi, t)
// Minimizes t + (1/(2*rho)) sum (max(0, lam_p + rho*(f_p - t))^2 - lam_p^2)
static void alm_val_grad(const ComplexMat& M, double t, const std::vector<double>& lam, double rho,
                         std::vector<double>& g_out, double& gt_out, double& loss_out) {
    const int d = M.d, n = M.n, dim = d * n;
    std::fill(g_out.begin(), g_out.end(), 0.0);
    double loss = t;
    double gt = 1.0;
    int p = 0;
    double inv2rho = 0.5 / rho;
    for (int j = 0; j < n; ++j) {
        const double* rj = &M.re[j * d];
        const double* ij = &M.im[j * d];
        for (int k = j + 1; k < n; ++k, ++p) {
            const double* rk = &M.re[k * d];
            const double* ik = &M.im[k * d];
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) {
                vr += rj[c] * rk[c] + ij[c] * ik[c];
                vi += rj[c] * ik[c] - ij[c] * rk[c];
            }
            double sq = vr * vr + vi * vi;
            double z = lam[p] + rho * (sq - t);
            if (z > 0.0) {
                loss += (z * z - lam[p] * lam[p]) * inv2rho;
                gt -= z;
                double w = 2.0 * z;
                int oj = j * d, ok = k * d;
                for (int c = 0; c < d; ++c) {
                    g_out[oj + c]       += w * (vr * rk[c] + vi * ik[c]);
                    g_out[dim + oj + c] += w * (vr * ik[c] - vi * rk[c]);
                    g_out[ok + c]       += w * (vr * rj[c] - vi * ij[c]);
                    g_out[dim + ok + c] += w * (vr * ij[c] + vi * rj[c]);
                }
            } else {
                loss -= lam[p] * lam[p] * inv2rho;
            }
        }
    }
    // Project tangent for Phi
    for (int i = 0; i < n; ++i) {
        int off = i * d;
        double dot = 0.0;
        for (int c = 0; c < d; ++c) dot += M.re[off + c] * g_out[off + c] + M.im[off + c] * g_out[dim + off + c];
        for (int c = 0; c < d; ++c) {
            g_out[off + c]       -= dot * M.re[off + c];
            g_out[dim + off + c] -= dot * M.im[off + c];
        }
    }
    g_out[2 * dim] = gt;
    gt_out = gt;
    loss_out = loss;
}

static void polish_alm(ComplexMat& M, int outer_rounds = 10, int inner_iters = 160) {
    const int d = M.d, n = M.n, dim = d * n, vdim = 2 * dim + 1;
    const int P = n * (n - 1) / 2;
    std::vector<double> lam(P, 0.0);
    double mu0 = eval_mu(M);
    double t = mu0 * mu0;
    double rho = 25.0;

    // Initialize lam uniformly on near-max pairs for instant warm start
    {
        int p = 0; double sum_w = 0.0;
        std::vector<double> sqs(P);
        for (int j = 0; j < n; ++j) {
            for (int k = j + 1; k < n; ++k, ++p) {
                double vr = 0.0, vi = 0.0;
                for (int c = 0; c < d; ++c) {
                    vr += M.re[j*d+c]*M.re[k*d+c] + M.im[j*d+c]*M.im[k*d+c];
                    vi += M.re[j*d+c]*M.im[k*d+c] - M.im[j*d+c]*M.re[k*d+c];
                }
                double s = vr*vr + vi*vi;
                sqs[p] = s;
                if (s >= t - 1e-3) { lam[p] = std::exp(500.0 * (s - t)); sum_w += lam[p]; }
            }
        }
        if (sum_w > 0.0) for (int p = 0; p < P; ++p) lam[p] /= sum_w;
    }

    ComplexMat best_M = M;
    double best_mu = mu0;

    for (int outer = 0; outer < outer_rounds; ++outer) {
        const int hist = 14;
        std::vector<double> g(vdim), g_new(vdim), dir(vdim), q(vdim);
        std::vector<std::vector<double>> s_h, y_h;
        std::vector<double> rho_h;
        double gt = 0.0, loss = 0.0;
        alm_val_grad(M, t, lam, rho, g, gt, loss);

        for (int it = 0; it < inner_iters; ++it) {
            double gn2 = 0.0;
            for (int i = 0; i < vdim; ++i) gn2 += g[i] * g[i];
            if (gn2 < 1e-26) break;

            q = g;
            int m = (int)s_h.size();
            std::vector<double> alpha(m, 0.0);
            for (int k = m - 1; k >= 0; --k) {
                double dot = 0.0;
                for (int i = 0; i < vdim; ++i) dot += s_h[k][i] * q[i];
                alpha[k] = rho_h[k] * dot;
                for (int i = 0; i < vdim; ++i) q[i] -= alpha[k] * y_h[k][i];
            }
            double gamma = 1.0 / (1.0 + rho * 0.1);
            if (m > 0) {
                double sy = 0.0, yy = 0.0;
                for (int i = 0; i < vdim; ++i) { sy += s_h[m-1][i]*y_h[m-1][i]; yy += y_h[m-1][i]*y_h[m-1][i]; }
                if (yy > 1e-30 && sy > 0) gamma = sy / yy;
            }
            for (int i = 0; i < vdim; ++i) q[i] *= gamma;
            for (int k = 0; k < m; ++k) {
                double dot = 0.0;
                for (int i = 0; i < vdim; ++i) dot += y_h[k][i] * q[i];
                double b = rho_h[k] * dot;
                for (int i = 0; i < vdim; ++i) q[i] += (alpha[k] - b) * s_h[k][i];
            }
            double dir_dot = 0.0;
            for (int i = 0; i < vdim; ++i) { dir[i] = -q[i]; dir_dot += dir[i] * g[i]; }
            if (dir_dot >= 0.0) {
                for (int i = 0; i < vdim; ++i) dir[i] = -g[i];
                s_h.clear(); y_h.clear(); rho_h.clear();
                dir_dot = -gn2;
            }

            double step = 1.0, nloss = 0.0, ngt = 0.0, nt = t;
            ComplexMat cand(d, n);
            bool ok = false;
            for (int ls = 0; ls < 34; ++ls) {
                for (int i = 0; i < dim; ++i) {
                    cand.re[i] = M.re[i] + step * dir[i];
                    cand.im[i] = M.im[i] + step * dir[dim + i];
                }
                normalize_all(cand);
                nt = t + step * dir[2 * dim];
                alm_val_grad(cand, nt, lam, rho, g_new, ngt, nloss);
                if (nloss <= loss + 1e-4 * step * dir_dot) { ok = true; break; }
                step *= 0.5;
            }
            if (!ok) {
                if (!s_h.empty()) { s_h.clear(); y_h.clear(); rho_h.clear(); continue; }
                break;
            }
            std::vector<double> sv(vdim), yv(vdim);
            double sy = 0.0;
            for (int i = 0; i < dim; ++i) {
                sv[i] = cand.re[i] - M.re[i]; sv[dim + i] = cand.im[i] - M.im[i];
            }
            sv[2 * dim] = nt - t;
            for (int i = 0; i < vdim; ++i) { yv[i] = g_new[i] - g[i]; sy += sv[i] * yv[i]; }
            M = std::move(cand); t = nt; g.swap(g_new); loss = nloss; gt = ngt;
            double cmu = eval_mu(M);
            if (cmu < best_mu) { best_mu = cmu; best_M = M; }
            if (sy > 1e-28) {
                if ((int)s_h.size() >= hist) { s_h.erase(s_h.begin()); y_h.erase(y_h.begin()); rho_h.erase(rho_h.begin()); }
                s_h.push_back(std::move(sv)); y_h.push_back(std::move(yv)); rho_h.push_back(1.0 / sy);
            }
        }

        // Dual multiplier update
        int p = 0;
        double sum_lam = 0.0;
        for (int j = 0; j < n; ++j) {
            for (int k = j + 1; k < n; ++k, ++p) {
                double vr = 0.0, vi = 0.0;
                for (int c = 0; c < d; ++c) {
                    vr += M.re[j*d+c]*M.re[k*d+c] + M.im[j*d+c]*M.im[k*d+c];
                    vi += M.re[j*d+c]*M.im[k*d+c] - M.im[j*d+c]*M.re[k*d+c];
                }
                double sq = vr * vr + vi * vi;
                lam[p] = std::max(0.0, lam[p] + rho * (sq - t));
                sum_lam += lam[p];
            }
        }
        rho = std::min(rho * 3.5, 2e6);
        double cmu = eval_mu(M);
        t = 0.5 * (t + cmu * cmu);
    }
    if (eval_mu(M) > best_mu) M = std::move(best_M);
}

int main(int argc, char** argv) {
    if (argc < 5) {
        std::cerr << "Usage: gram_alm <d> <n> <mode: polish|rrr> ...\n";
        return 1;
    }
    int d = std::atoi(argv[1]);
    int n = std::atoi(argv[2]);
    std::string mode = argv[3];

    if (mode == "polish" && argc >= 6) {
        ComplexMat M;
        if (!load_gos_txt(argv[4], d, n, M)) return 1;
        double m0 = eval_mu(M);
        polish_alm(M, 12, 200);
        double m1 = eval_mu(M);
        std::cout << std::setprecision(16) << "before=" << m0 << " after_alm=" << m1 << " gain=" << (m0 - m1) << "\n";
        if (m1 < m0 - 1e-12) save_gos_txt(argv[5], M);
        return 0;
    }

    if (mode == "rrr" && argc >= 7) {
        int trials = std::atoi(argv[4]);
        double target_mu = std::atof(argv[5]);
        std::string out_path = argv[6];
        double mu_cap_base = (argc >= 8) ? std::atof(argv[7]) : (target_mu - 0.002);

        double global_best = 1e9;
        ComplexMat best_M;

        #pragma omp parallel for schedule(dynamic, 1)
        for (int t = 0; t < trials; ++t) {
            std::mt19937_64 rng(77777ULL + (uint64_t)t * 0x9e3779b97f4a7c15ULL);
            std::normal_distribution<double> nd(0.0, 1.0);
            ComplexMat M(d, n);
            for (int i = 0; i < d * n; ++i) { M.re[i] = nd(rng); M.im[i] = nd(rng); }
            normalize_all(M);

            std::vector<cd> G(n * n, cd(0.0, 0.0));
            for (int j = 0; j < n; ++j) {
                G[j * n + j] = cd(1.0, 0.0);
                for (int k = j + 1; k < n; ++k) {
                    cd s(0.0, 0.0);
                    for (int c = 0; c < d; ++c) s += std::conj(cd(M.re[j*d+c], M.im[j*d+c])) * cd(M.re[k*d+c], M.im[k*d+c]);
                    G[j * n + k] = s; G[k * n + j] = std::conj(s);
                }
            }

            double mu_cap = mu_cap_base * (0.985 + 0.025 * ((t % 5) / 4.0));
            double beta_rrr = 0.65;
            ComplexMat best_rrr_M = M;
            double best_rrr_mu = eval_mu(M);

            std::vector<cd> P1, P2, arg(n * n);
            ComplexMat Phi_tmp;
            for (int step = 0; step < 320; ++step) {
                project_coherence(n, G, mu_cap, P1);
                for (int idx = 0; idx < n * n; ++idx) arg[idx] = 2.0 * P1[idx] - G[idx];
                project_rank_d(d, n, arg, Phi_tmp, P2, (step < 140));
                for (int idx = 0; idx < n * n; ++idx) G[idx] += beta_rrr * (P2[idx] - P1[idx]);
                if (step % 16 == 15 || step >= 300) {
                    double cur = eval_mu(Phi_tmp);
                    if (cur < best_rrr_mu) { best_rrr_mu = cur; best_rrr_M = Phi_tmp; }
                }
            }

            M = best_rrr_M;
            polish_alm(M, 12, 200);
            double mu = eval_mu(M);

            #pragma omp critical
            {
                if (mu < global_best) {
                    global_best = mu;
                    best_M = M;
                    std::cout << std::setprecision(16)
                              << "[alm_rrr " << t << "] NEW BEST mu=" << global_best
                              << " (target=" << target_mu << ", imp=" << (target_mu - global_best) << ")\n"
                              << std::flush;
                    save_gos_txt(out_path, best_M);
                }
            }
        }
        std::cout << std::setprecision(16) << "FINAL ALM_RRR BEST mu=" << global_best << "\n";
    }
    return 0;
}
