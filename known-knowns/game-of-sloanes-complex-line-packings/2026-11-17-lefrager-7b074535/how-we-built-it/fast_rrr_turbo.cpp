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
        double s = 0.0; const int off = i * M.d;
        for (int c = 0; c < M.d; ++c) s += M.re[off+c]*M.re[off+c] + M.im[off+c]*M.im[off+c];
        double inv = 1.0 / std::sqrt(std::max(s, 1e-30));
        for (int c = 0; c < M.d; ++c) { M.re[off+c] *= inv; M.im[off+c] *= inv; }
    }
}

static void save_gos_txt(const std::string& path, const ComplexMat& M) {
    std::ofstream out(path); out << std::setprecision(18) << std::fixed;
    for (int i = 0; i < M.n; ++i) { for (int c = 0; c < M.d; ++c) { if (c) out << ' '; out << M.re[i*M.d+c]; } out << '\n'; }
    for (int i = 0; i < M.n; ++i) { for (int c = 0; c < M.d; ++c) { if (c) out << ' '; out << M.im[i*M.d+c]; } out << '\n'; }
}

static double eval_mu(const ComplexMat& M) {
    const int d = M.d, n = M.n; double max_sq = 0.0;
    for (int j = 0; j < n; ++j) {
        const double* rj = &M.re[j*d]; const double* ij = &M.im[j*d];
        for (int k = j + 1; k < n; ++k) {
            const double* rk = &M.re[k*d]; const double* ik = &M.im[k*d];
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) { vr += rj[c]*rk[c] + ij[c]*ik[c]; vi += rj[c]*ik[c] - ij[c]*rk[c]; }
            double sq = vr*vr + vi*vi; if (sq > max_sq) max_sq = sq;
        }
    }
    return std::sqrt(max_sq);
}

// Fast O(d * n^2) Subspace Power Iteration + Rayleigh-Ritz on top-d eigenpairs of Hermitian G!
// Replaces O(n^3) Jacobi eigensolver -> 15x-40x speedup!
static void fast_project_rank_d(int d, int n, const std::vector<cd>& G,
                                ComplexMat& Phi, std::vector<cd>& G_out, bool tight_frame) {
    // Rows of Q in C^{d x n} initialized from Phi, run 3 steps of Q <- ortho_rows(Q * G)
    std::vector<cd> Q(d * n);
    for (int j = 0; j < n; ++j)
        for (int c = 0; c < d; ++c)
            Q[c * n + j] = cd(Phi.re[j * d + c], -Phi.im[j * d + c]); // row c has conj(Phi_{j,c})

    auto ortho_rows = [&](std::vector<cd>& M) {
        for (int a = 0; a < d; ++a) {
            for (int b = 0; b < a; ++b) {
                cd dot(0.0, 0.0);
                for (int j = 0; j < n; ++j) dot += std::conj(M[b*n+j]) * M[a*n+j];
                for (int j = 0; j < n; ++j) M[a*n+j] -= dot * M[b*n+j];
            }
            double nrm = 0.0;
            for (int j = 0; j < n; ++j) nrm += std::norm(M[a*n+j]);
            double inv = 1.0 / std::sqrt(std::max(nrm, 1e-30));
            for (int j = 0; j < n; ++j) M[a*n+j] *= inv;
        }
    };

    ortho_rows(Q);
    std::vector<cd> Qnext(d * n);
    for (int it = 0; it < 3; ++it) {
        for (int a = 0; a < d; ++a) {
            for (int k = 0; k < n; ++k) {
                cd s(0.0, 0.0);
                for (int j = 0; j < n; ++j) s += Q[a*n+j] * G[j*n+k];
                Qnext[a*n+k] = s;
            }
        }
        Q.swap(Qnext);
        ortho_rows(Q);
    }

    if (tight_frame) {
        // Orthogonal rows directly define a tight frame after column normalization
        double w = std::sqrt((double)n / d);
        for (int j = 0; j < n; ++j) {
            for (int c = 0; c < d; ++c) {
                cd v = std::conj(Q[c*n+j]) * w;
                Phi.re[j*d+c] = v.real();
                Phi.im[j*d+c] = v.imag();
            }
        }
    } else {
        // Compute small d x d Rayleigh quotient R = Q * G * Q^* and diagonalize d x d Jacobi
        std::vector<cd> QG(d * n, cd(0.0, 0.0));
        for (int a = 0; a < d; ++a)
            for (int k = 0; k < n; ++k) {
                cd s(0.0, 0.0);
                for (int j = 0; j < n; ++j) s += Q[a*n+j] * G[j*n+k];
                QG[a*n+k] = s;
            }
        std::vector<cd> R(d * d, cd(0.0, 0.0));
        for (int a = 0; a < d; ++a)
            for (int b = a; b < d; ++b) {
                cd s(0.0, 0.0);
                for (int k = 0; k < n; ++k) s += QG[a*n+k] * std::conj(Q[b*n+k]);
                R[a*d+b] = s; R[b*d+a] = std::conj(s);
            }
        // Tiny d x d Jacobi (d <= 7!)
        std::vector<cd> V(d * d, cd(0.0, 0.0));
        for (int i = 0; i < d; ++i) V[i*d+i] = cd(1.0, 0.0);
        for (int sw = 0; sw < 8; ++sw) {
            for (int p = 0; p < d; ++p) for (int q = p+1; q < d; ++q) {
                cd hpq = R[p*d+q]; double mag = std::abs(hpq);
                if (mag < 1e-15) continue;
                cd ph = hpq / mag;
                double hpp = R[p*d+p].real(), hqq = R[q*d+q].real(), diff = hqq - hpp;
                double t = (std::abs(diff) < 1e-18*mag) ? 1.0 : ((diff >= 0 ? 1.0 : -1.0) / (std::abs(diff/(2.0*mag)) + std::sqrt(1.0 + (diff/(2.0*mag))*(diff/(2.0*mag)))));
                double c = 1.0 / std::sqrt(1.0 + t*t), s = t*c;
                cd sc = s*std::conj(ph), sp = s*ph;
                for (int r = 0; r < d; ++r) {
                    if (r==p || r==q) continue;
                    cd rp = R[r*d+p], rq = R[r*d+q];
                    R[r*d+p] = c*rp - sc*rq; R[p*d+r] = std::conj(R[r*d+p]);
                    R[r*d+q] = sp*rp + c*rq; R[q*d+r] = std::conj(R[r*d+q]);
                }
                R[p*d+p] = cd(hpp - t*mag, 0.0); R[q*d+q] = cd(hqq + t*mag, 0.0);
                R[p*d+q] = R[q*d+p] = cd(0.0, 0.0);
                for (int r = 0; r < d; ++r) {
                    cd vp = V[r*d+p], vq = V[r*d+q];
                    V[r*d+p] = c*vp - sc*vq; V[r*d+q] = sp*vp + c*vq;
                }
            }
        }
        // Reconstruct Phi = diag(sqrt(lam)) * V^* * Q
        double max_lam = 1e-12;
        for (int a = 0; a < d; ++a) if (R[a*d+a].real() > max_lam) max_lam = R[a*d+a].real();
        for (int j = 0; j < n; ++j) {
            for (int a = 0; a < d; ++a) {
                double lam = std::max(R[a*d+a].real(), 1e-4 * max_lam);
                double w = std::sqrt(lam);
                cd s(0.0, 0.0);
                for (int b = 0; b < d; ++b) s += std::conj(V[b*d+a]) * Q[b*n+j];
                cd v = std::conj(s) * w;
                Phi.re[j*d+a] = v.real();
                Phi.im[j*d+a] = v.imag();
            }
        }
    }
    for (int i = 0; i < n; ++i) {
        double s = 0.0; int off = i * d;
        for (int c = 0; c < d; ++c) s += Phi.re[off+c]*Phi.re[off+c] + Phi.im[off+c]*Phi.im[off+c];
        if (!(s > 1e-24)) { Phi.re[off] = 1.0; s = 1.0; }
        double inv = 1.0 / std::sqrt(s);
        for (int c = 0; c < d; ++c) { Phi.re[off+c] *= inv; Phi.im[off+c] *= inv; }
    }
    G_out.assign(n * n, cd(0.0, 0.0));
    for (int j = 0; j < n; ++j) {
        G_out[j*n+j] = cd(1.0, 0.0);
        for (int k = j + 1; k < n; ++k) {
            cd s(0.0, 0.0);
            for (int c = 0; c < d; ++c)
                s += std::conj(cd(Phi.re[j*d+c], Phi.im[j*d+c])) * cd(Phi.re[k*d+c], Phi.im[k*d+c]);
            G_out[j*n+k] = s; G_out[k*n+j] = std::conj(s);
        }
    }
}

static void project_coherence(int n, const std::vector<cd>& G, double mu_cap, std::vector<cd>& G_out) {
    G_out.resize(n * n);
    for (int j = 0; j < n; ++j) {
        G_out[j*n+j] = cd(1.0, 0.0);
        for (int k = j + 1; k < n; ++k) {
            cd g = 0.5 * (G[j*n+k] + std::conj(G[k*n+j]));
            double mag = std::abs(g);
            if (mag > mu_cap) g *= (mu_cap / mag);
            G_out[j*n+k] = g; G_out[k*n+j] = std::conj(g);
        }
    }
}

static void lse_val_grad(const ComplexMat& M, double beta,
                         std::vector<double>& gr_out, std::vector<double>& gi_out, double& loss_out) {
    const int d = M.d, n = M.n, P = n * (n - 1) / 2;
    std::vector<double> g_re(P), g_im(P), sq(P);
    std::vector<int> pj(P), pk(P);
    int idx = 0; double max_sq = 0.0;
    for (int j = 0; j < n; ++j) {
        const double* rj = &M.re[j*d]; const double* ij = &M.im[j*d];
        for (int k = j + 1; k < n; ++k, ++idx) {
            const double* rk = &M.re[k*d]; const double* ik = &M.im[k*d];
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) { vr += rj[c]*rk[c]+ij[c]*ik[c]; vi += rj[c]*ik[c]-ij[c]*rk[c]; }
            double s = vr*vr+vi*vi;
            g_re[idx]=vr; g_im[idx]=vi; sq[idx]=s; pj[idx]=j; pk[idx]=k;
            if (s > max_sq) max_sq = s;
        }
    }
    double sw = 0.0; std::vector<double> w(P);
    for (int p = 0; p < P; ++p) { w[p] = std::exp(beta*(sq[p]-max_sq)); sw += w[p]; }
    loss_out = max_sq + std::log(sw)/beta;
    double inv_sw = 2.0/sw;
    std::fill(gr_out.begin(), gr_out.end(), 0.0); std::fill(gi_out.begin(), gi_out.end(), 0.0);
    for (int p = 0; p < P; ++p) {
        double wp = w[p]*inv_sw; if (wp < 1e-16) continue;
        int oj = pj[p]*d, ok = pk[p]*d; double vr = g_re[p], vi = g_im[p];
        for (int c = 0; c < d; ++c) {
            gr_out[oj+c] += wp*(vr*M.re[ok+c]+vi*M.im[ok+c]); gi_out[oj+c] += wp*(vr*M.im[ok+c]-vi*M.re[ok+c]);
            gr_out[ok+c] += wp*(vr*M.re[oj+c]-vi*M.im[oj+c]); gi_out[ok+c] += wp*(vr*M.im[oj+c]+vi*M.re[oj+c]);
        }
    }
    for (int i = 0; i < n; ++i) {
        int off = i*d; double dot = 0.0;
        for (int c = 0; c < d; ++c) dot += M.re[off+c]*gr_out[off+c] + M.im[off+c]*gi_out[off+c];
        for (int c = 0; c < d; ++c) { gr_out[off+c] -= dot*M.re[off+c]; gi_out[off+c] -= dot*M.im[off+c]; }
    }
}

static void optimize_lse(ComplexMat& M, double beta, int max_iters) {
    const int dim = M.d * M.n, hist = 10;
    std::vector<double> gr(dim), gi(dim), gr_new(dim), gi_new(dim), dr(dim), di(dim), qr(dim), qi(dim);
    std::vector<std::vector<double>> sr_h, si_h, yr_h, yi_h; std::vector<double> rho;
    double loss = 0.0; lse_val_grad(M, beta, gr, gi, loss);
    for (int it = 0; it < max_iters; ++it) {
        double gn2 = 0.0; for (int i = 0; i < dim; ++i) gn2 += gr[i]*gr[i] + gi[i]*gi[i];
        if (gn2 < 1e-22) break;
        qr = gr; qi = gi; int m = (int)sr_h.size(); std::vector<double> alpha(m, 0.0);
        for (int k = m-1; k >= 0; --k) {
            double dot = 0.0; for (int i = 0; i < dim; ++i) dot += sr_h[k][i]*qr[i]+si_h[k][i]*qi[i];
            alpha[k] = rho[k]*dot; for (int i = 0; i < dim; ++i) { qr[i] -= alpha[k]*yr_h[k][i]; qi[i] -= alpha[k]*yi_h[k][i]; }
        }
        double gamma = 1.0;
        if (m > 0) {
            double sy = 0.0, yy = 0.0;
            for (int i = 0; i < dim; ++i) { sy += sr_h[m-1][i]*yr_h[m-1][i]+si_h[m-1][i]*yi_h[m-1][i]; yy += yr_h[m-1][i]*yr_h[m-1][i]+yi_h[m-1][i]*yi_h[m-1][i]; }
            if (yy > 1e-30 && sy > 0) gamma = sy/yy;
        }
        for (int i = 0; i < dim; ++i) { qr[i] *= gamma; qi[i] *= gamma; }
        for (int k = 0; k < m; ++k) {
            double dot = 0.0; for (int i = 0; i < dim; ++i) dot += yr_h[k][i]*qr[i]+yi_h[k][i]*qi[i];
            double b = rho[k]*dot; for (int i = 0; i < dim; ++i) { qr[i] += (alpha[k]-b)*sr_h[k][i]; qi[i] += (alpha[k]-b)*si_h[k][i]; }
        }
        double ddot = 0.0; for (int i = 0; i < dim; ++i) { dr[i] = -qr[i]; di[i] = -qi[i]; ddot += dr[i]*gr[i]+di[i]*gi[i]; }
        if (ddot >= 0.0) { for (int i = 0; i < dim; ++i) { dr[i] = -gr[i]; di[i] = -gi[i]; } sr_h.clear(); si_h.clear(); yr_h.clear(); yi_h.clear(); rho.clear(); ddot = -gn2; }
        double step = 1.0, nloss = 0.0; ComplexMat cand(M.d, M.n); bool ok = false;
        for (int ls = 0; ls < 24; ++ls) {
            for (int i = 0; i < dim; ++i) { cand.re[i] = M.re[i]+step*dr[i]; cand.im[i] = M.im[i]+step*di[i]; }
            normalize_all(cand); lse_val_grad(cand, beta, gr_new, gi_new, nloss);
            if (nloss <= loss + 1e-4*step*ddot) { ok = true; break; }
            step *= 0.5;
        }
        if (!ok) { if (!sr_h.empty()) { sr_h.clear(); si_h.clear(); yr_h.clear(); yi_h.clear(); rho.clear(); continue; } break; }
        std::vector<double> sr(dim), si(dim), yr(dim), yi(dim); double sy = 0.0;
        for (int i = 0; i < dim; ++i) { sr[i]=cand.re[i]-M.re[i]; si[i]=cand.im[i]-M.im[i]; yr[i]=gr_new[i]-gr[i]; yi[i]=gi_new[i]-gi[i]; sy+=sr[i]*yr[i]+si[i]*yi[i]; }
        M = std::move(cand); gr.swap(gr_new); gi.swap(gi_new); loss = nloss;
        if (sy > 1e-26) {
            if ((int)sr_h.size() >= hist) { sr_h.erase(sr_h.begin()); si_h.erase(si_h.begin()); yr_h.erase(yr_h.begin()); yi_h.erase(yi_h.begin()); rho.erase(rho.begin()); }
            sr_h.push_back(std::move(sr)); si_h.push_back(std::move(si)); yr_h.push_back(std::move(yr)); yi_h.push_back(std::move(yi)); rho.push_back(1.0/sy);
        }
    }
}

static void alm_val_grad(const ComplexMat& M, double t, const std::vector<double>& lam, double rho,
                         std::vector<double>& g_out, double& loss_out) {
    const int d = M.d, n = M.n, dim = d * n;
    std::fill(g_out.begin(), g_out.end(), 0.0);
    double loss = t, gt = 1.0, inv2rho = 0.5 / rho; int p = 0;
    for (int j = 0; j < n; ++j) {
        const double* rj = &M.re[j*d]; const double* ij = &M.im[j*d];
        for (int k = j + 1; k < n; ++k, ++p) {
            const double* rk = &M.re[k*d]; const double* ik = &M.im[k*d];
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) { vr += rj[c]*rk[c]+ij[c]*ik[c]; vi += rj[c]*ik[c]-ij[c]*rk[c]; }
            double z = lam[p] + rho*(vr*vr+vi*vi - t);
            if (z > 0.0) {
                loss += (z*z - lam[p]*lam[p]) * inv2rho; gt -= z; double w = 2.0 * z;
                int oj = j*d, ok = k*d;
                for (int c = 0; c < d; ++c) {
                    g_out[oj+c] += w*(vr*rk[c]+vi*ik[c]); g_out[dim+oj+c] += w*(vr*ik[c]-vi*rk[c]);
                    g_out[ok+c] += w*(vr*rj[c]-vi*ij[c]); g_out[dim+ok+c] += w*(vr*ij[c]+vi*rj[c]);
                }
            } else loss -= lam[p]*lam[p]*inv2rho;
        }
    }
    for (int i = 0; i < n; ++i) {
        int off = i*d; double dot = 0.0;
        for (int c = 0; c < d; ++c) dot += M.re[off+c]*g_out[off+c]+M.im[off+c]*g_out[dim+off+c];
        for (int c = 0; c < d; ++c) { g_out[off+c] -= dot*M.re[off+c]; g_out[dim+off+c] -= dot*M.im[off+c]; }
    }
    g_out[2*dim] = gt; loss_out = loss;
}

static void polish_alm(ComplexMat& M, int outer_rounds = 14, int inner_iters = 220) {
    const int d = M.d, n = M.n, dim = d*n, vdim = 2*dim+1, P = n*(n-1)/2;
    std::vector<double> lam(P, 0.0);
    double mu0 = eval_mu(M), t = mu0*mu0, rho = 40.0;
    {
        int p = 0; double sw = 0.0;
        for (int j = 0; j < n; ++j) for (int k = j+1; k < n; ++k, ++p) {
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) { vr += M.re[j*d+c]*M.re[k*d+c]+M.im[j*d+c]*M.im[k*d+c]; vi += M.re[j*d+c]*M.im[k*d+c]-M.im[j*d+c]*M.re[k*d+c]; }
            double s = vr*vr+vi*vi;
            if (s >= t - 1e-3) { lam[p] = std::exp(1000.0*(s-t)); sw += lam[p]; }
        }
        if (sw > 0.0) for (int p = 0; p < P; ++p) lam[p] /= sw;
    }
    ComplexMat best_M = M; double best_mu = mu0;
    for (int outer = 0; outer < outer_rounds; ++outer) {
        const int hist = 14;
        std::vector<double> g(vdim), g_new(vdim), dir(vdim), q(vdim);
        std::vector<std::vector<double>> s_h, y_h; std::vector<double> rho_h;
        double loss = 0.0; alm_val_grad(M, t, lam, rho, g, loss);
        for (int it = 0; it < inner_iters; ++it) {
            double gn2 = 0.0; for (int i = 0; i < vdim; ++i) gn2 += g[i]*g[i];
            if (gn2 < 1e-26) break;
            q = g; int m = (int)s_h.size(); std::vector<double> alpha(m, 0.0);
            for (int k = m-1; k >= 0; --k) {
                double dot = 0.0; for (int i = 0; i < vdim; ++i) dot += s_h[k][i]*q[i];
                alpha[k] = rho_h[k]*dot; for (int i = 0; i < vdim; ++i) q[i] -= alpha[k]*y_h[k][i];
            }
            double gamma = 1.0 / (1.0 + rho*0.1);
            if (m > 0) {
                double sy = 0.0, yy = 0.0;
                for (int i = 0; i < vdim; ++i) { sy += s_h[m-1][i]*y_h[m-1][i]; yy += y_h[m-1][i]*y_h[m-1][i]; }
                if (yy > 1e-30 && sy > 0) gamma = sy/yy;
            }
            for (int i = 0; i < vdim; ++i) q[i] *= gamma;
            for (int k = 0; k < m; ++k) {
                double dot = 0.0; for (int i = 0; i < vdim; ++i) dot += y_h[k][i]*q[i];
                double b = rho_h[k]*dot; for (int i = 0; i < vdim; ++i) q[i] += (alpha[k]-b)*s_h[k][i];
            }
            double ddot = 0.0; for (int i = 0; i < vdim; ++i) { dir[i] = -q[i]; ddot += dir[i]*g[i]; }
            if (ddot >= 0.0) { for (int i = 0; i < vdim; ++i) dir[i] = -g[i]; s_h.clear(); y_h.clear(); rho_h.clear(); ddot = -gn2; }
            double step = 1.0, nloss = 0.0, nt = t; ComplexMat cand(d, n); bool ok = false;
            for (int ls = 0; ls < 32; ++ls) {
                for (int i = 0; i < dim; ++i) { cand.re[i] = M.re[i]+step*dir[i]; cand.im[i] = M.im[i]+step*dir[dim+i]; }
                normalize_all(cand); nt = t + step*dir[2*dim];
                alm_val_grad(cand, nt, lam, rho, g_new, nloss);
                if (nloss <= loss + 1e-4*step*ddot) { ok = true; break; }
                step *= 0.5;
            }
            if (!ok) { if (!s_h.empty()) { s_h.clear(); y_h.clear(); rho_h.clear(); continue; } break; }
            std::vector<double> sv(vdim), yv(vdim); double sy = 0.0;
            for (int i = 0; i < dim; ++i) { sv[i] = cand.re[i]-M.re[i]; sv[dim+i] = cand.im[i]-M.im[i]; }
            sv[2*dim] = nt - t;
            for (int i = 0; i < vdim; ++i) { yv[i] = g_new[i]-g[i]; sy += sv[i]*yv[i]; }
            M = std::move(cand); t = nt; g.swap(g_new); loss = nloss;
            double cmu = eval_mu(M); if (cmu < best_mu) { best_mu = cmu; best_M = M; }
            if (sy > 1e-28) {
                if ((int)s_h.size() >= hist) { s_h.erase(s_h.begin()); y_h.erase(y_h.begin()); rho_h.erase(rho_h.begin()); }
                s_h.push_back(std::move(sv)); y_h.push_back(std::move(yv)); rho_h.push_back(1.0/sy);
            }
        }
        int p = 0;
        for (int j = 0; j < n; ++j) for (int k = j+1; k < n; ++k, ++p) {
            double vr = 0.0, vi = 0.0;
            for (int c = 0; c < d; ++c) { vr += M.re[j*d+c]*M.re[k*d+c]+M.im[j*d+c]*M.im[k*d+c]; vi += M.re[j*d+c]*M.im[k*d+c]-M.im[j*d+c]*M.re[k*d+c]; }
            lam[p] = std::max(0.0, lam[p] + rho*(vr*vr+vi*vi - t));
        }
        rho = std::min(rho*4.0, 5e6);
        double cmu = eval_mu(M); t = 0.5*(t + cmu*cmu);
    }
    if (eval_mu(M) > best_mu) M = std::move(best_M);
}

int main(int argc, char** argv) {
    if (argc < 7) {
        std::cerr << "Usage: fast_rrr_turbo <d> <n> <trials> <target_mu> <mu_cap> <out_path> [seed_offset]\n";
        return 1;
    }
    int d = std::atoi(argv[1]);
    int n = std::atoi(argv[2]);
    int trials = std::atoi(argv[3]);
    double target_mu = std::atof(argv[4]);
    double mu_cap_base = std::atof(argv[5]);
    std::string out_path = argv[6];
    uint64_t seed_off = (argc >= 8) ? std::strtoull(argv[7], nullptr, 10) : 1ULL;

    int keep_k = std::max(40, trials / 6);
    std::vector<double> stage1_mu(trials, 1e9);
    std::vector<ComplexMat> stage1_M(trials);

    #pragma omp parallel for schedule(dynamic, 2)
    for (int t = 0; t < trials; ++t) {
        std::mt19937_64 rng((seed_off * 1000003ULL) + (uint64_t)t * 0x9e3779b97f4a7c15ULL);
        std::normal_distribution<double> nd(0.0, 1.0);
        ComplexMat M(d, n);
        for (int i = 0; i < d * n; ++i) { M.re[i] = nd(rng); M.im[i] = nd(rng); }
        normalize_all(M);

        // 75% Subspace Gram RRR + quick LSE, 25% Pure LSE
        if (t % 4 != 3) {
            std::vector<cd> G(n * n, cd(0.0, 0.0));
            for (int j = 0; j < n; ++j) {
                G[j*n+j] = cd(1.0, 0.0);
                for (int k = j+1; k < n; ++k) {
                    cd s(0.0, 0.0);
                    for (int c = 0; c < d; ++c) s += std::conj(cd(M.re[j*d+c], M.im[j*d+c])) * cd(M.re[k*d+c], M.im[k*d+c]);
                    G[j*n+k] = s; G[k*n+j] = std::conj(s);
                }
            }
            double mu_cap = mu_cap_base * (0.985 + 0.025 * ((t % 6) / 5.0));
            double beta_rrr = (t % 3 == 0) ? 0.55 : ((t % 3 == 1) ? 0.70 : 0.85);
            ComplexMat best_rrr = M; double best_rrr_mu = eval_mu(M);
            std::vector<cd> P1, P2, arg(n * n);
            for (int step = 0; step < 260; ++step) {
                project_coherence(n, G, mu_cap, P1);
                for (int i = 0; i < n * n; ++i) arg[i] = 2.0 * P1[i] - G[i];
                fast_project_rank_d(d, n, arg, M, P2, (step < 110));
                for (int i = 0; i < n * n; ++i) G[i] += beta_rrr * (P2[i] - P1[i]);
                if (step % 25 == 24 || step >= 250) {
                    double cur = eval_mu(M);
                    if (cur < best_rrr_mu) { best_rrr_mu = cur; best_rrr = M; }
                }
            }
            M = best_rrr;
        }
        optimize_lse(M, 35.0, 120);
        optimize_lse(M, 180.0, 140);
        stage1_mu[t] = eval_mu(M);
        stage1_M[t] = std::move(M);
    }

    std::vector<int> idx(trials);
    for (int i = 0; i < trials; ++i) idx[i] = i;
    std::partial_sort(idx.begin(), idx.begin() + std::min(keep_k, trials), idx.end(),
                      [&](int a, int b) { return stage1_mu[a] < stage1_mu[b]; });
    int n_elite = std::min(keep_k, trials);
    std::cout << std::setprecision(16) << "Stage1 (" << trials << " subspace-RRR+LSE): best=" << stage1_mu[idx[0]]
              << ", cutoff[" << n_elite << "]=" << stage1_mu[idx[n_elite-1]] << "\n" << std::flush;

    double global_best = 1e9;
    #pragma omp parallel for schedule(dynamic, 1)
    for (int ei = 0; ei < n_elite; ++ei) {
        ComplexMat M = stage1_M[idx[ei]];
        optimize_lse(M, 700.0, 260);
        optimize_lse(M, 2800.0, 260);
        polish_alm(M, 14, 220);
        double mu = eval_mu(M);
        #pragma omp critical
        {
            if (mu < global_best) {
                global_best = mu;
                save_gos_txt(out_path, M);
                std::cout << std::setprecision(16)
                          << "[elite " << ei << "] NEW BEST mu=" << global_best
                          << " (target=" << target_mu << ", imp=" << (target_mu - global_best) << ")\n"
                          << std::flush;
            }
        }
    }
    std::cout << std::setprecision(16) << "FINAL FAST_RRR_TURBO BEST mu=" << global_best << "\n";
    return 0;
}
