// FS_Cluster_Hunter.cc — C++17 Multi-Threaded Bidirectional Cascade & Newton Polisher
// for Finnis-Sinclair Molybdenum (1984) and Iron (1986) Nanoclusters (N = 3..100).

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

struct FSParams {
    std::string name;
    double d, A, beta, c, c0, c1, c2;
    double r0_nn;
};

static const FSParams MO_PARAMS = {
    "Mo", 4.114825, 1.887117, 0.0, 3.25, 43.4475218, -31.9332978, 6.0804249, 2.7255
};

static const FSParams FE_PARAMS = {
    "Fe", 3.569745, 1.828905, 1.8, 3.40, 1.2371147, -0.3592185, -0.0385607, 2.4824
};

inline double eval_fs_grad(int N, const double* xyz, double* grad, const FSParams& p, double* atom_e = nullptr, bool soft_core = true) {
    std::vector<double> rho(N, 0.0);
    std::vector<double> pair_i(N, 0.0);
    double pair_sum = 0.0;
    const double r_max = std::max(p.c, p.d);
    const double r_max2 = r_max * r_max;

    for (int i = 0; i < 3 * N; ++i) grad[i] = 0.0;

    for (int i = 0; i < N; ++i) {
        double xi = xyz[3 * i], yi = xyz[3 * i + 1], zi = xyz[3 * i + 2];
        for (int j = i + 1; j < N; ++j) {
            double dx = xi - xyz[3 * j];
            double dy = yi - xyz[3 * j + 1];
            double dz = zi - xyz[3 * j + 2];
            double r2 = dx * dx + dy * dy + dz * dz;
            if (r2 >= r_max2) continue;
            double r = std::sqrt(r2);
            if (r < p.c) {
                double rc = r - p.c;
                double v = (rc * rc) * (p.c0 + p.c1 * r + p.c2 * r * r);
                if (soft_core && r < 1.2) {
                    double dr = 1.2 - r;
                    v += 500.0 * dr * dr * dr;
                }
                pair_sum += v;
                if (atom_e) {
                    pair_i[i] += 0.5 * v;
                    pair_i[j] += 0.5 * v;
                }
            }
            if (r < p.d) {
                double rd = r - p.d;
                double phi = (rd * rd) + p.beta * (rd * rd * rd) / p.d;
                rho[i] += phi;
                rho[j] += phi;
            }
        }
    }

    std::vector<double> inv_sqrt_rho(N, 0.0);
    double emb_sum = 0.0;
    for (int i = 0; i < N; ++i) {
        if (rho[i] > 1e-30) {
            double sr = std::sqrt(rho[i]);
            emb_sum += sr;
            inv_sqrt_rho[i] = 1.0 / sr;
            if (atom_e) atom_e[i] = pair_i[i] - p.A * sr;
        } else if (atom_e) {
            atom_e[i] = pair_i[i];
        }
    }

    for (int i = 0; i < N; ++i) {
        double xi = xyz[3 * i], yi = xyz[3 * i + 1], zi = xyz[3 * i + 2];
        for (int j = i + 1; j < N; ++j) {
            double dx = xi - xyz[3 * j];
            double dy = yi - xyz[3 * j + 1];
            double dz = zi - xyz[3 * j + 2];
            double r2 = dx * dx + dy * dy + dz * dz;
            if (r2 >= r_max2 || r2 < 1e-24) continue;
            double r = std::sqrt(r2);
            double dE_dr = 0.0;
            if (r < p.c) {
                double rc = r - p.c;
                dE_dr += 2.0 * rc * (p.c0 + p.c1 * r + p.c2 * r * r) + (rc * rc) * (p.c1 + 2.0 * p.c2 * r);
                if (soft_core && r < 1.2) {
                    double dr = 1.2 - r;
                    dE_dr -= 1500.0 * dr * dr;
                }
            }
            if (r < p.d) {
                double rd = r - p.d;
                double dphi_dr = 2.0 * rd + 3.0 * p.beta * (rd * rd) / p.d;
                dE_dr -= 0.5 * p.A * (inv_sqrt_rho[i] + inv_sqrt_rho[j]) * dphi_dr;
            }
            double f = dE_dr / r;
            double fx = f * dx, fy = f * dy, fz = f * dz;
            grad[3 * i]     += fx; grad[3 * i + 1] += fy; grad[3 * i + 2] += fz;
            grad[3 * j]     -= fx; grad[3 * j + 1] -= fy; grad[3 * j + 2] -= fz;
        }
    }
    return pair_sum - p.A * emb_sum;
}

double lbfgs_optimize(int N, std::vector<double>& x, const FSParams& p, int max_iter = 1000, double gtol = 1e-13) {
    const int D = 3 * N;
    const int m = 14;
    std::vector<double> g(D), g_old(D), x_old(D), q(D), dir(D);
    std::vector<std::vector<double>> s_hist(m, std::vector<double>(D));
    std::vector<std::vector<double>> y_hist(m, std::vector<double>(D));
    std::vector<double> rho_hist(m, 0.0), alpha(m, 0.0);

    double f = eval_fs_grad(N, x.data(), g.data(), p);
    int hist_len = 0, hist_idx = 0;

    for (int iter = 0; iter < max_iter; ++iter) {
        double gnorm = 0.0;
        for (int i = 0; i < D; ++i) gnorm += g[i] * g[i];
        gnorm = std::sqrt(gnorm);
        if (gnorm < gtol) break;

        q = g;
        int bound = std::min(hist_len, m);
        for (int k = 0; k < bound; ++k) {
            int idx = (hist_idx - 1 - k + m) % m;
            double dot = 0.0;
            for (int i = 0; i < D; ++i) dot += s_hist[idx][i] * q[i];
            alpha[idx] = rho_hist[idx] * dot;
            for (int i = 0; i < D; ++i) q[i] -= alpha[idx] * y_hist[idx][i];
        }
        double gamma = 1.0;
        if (hist_len > 0) {
            int last = (hist_idx - 1 + m) % m;
            double sy = 0.0, yy = 0.0;
            for (int i = 0; i < D; ++i) {
                sy += s_hist[last][i] * y_hist[last][i];
                yy += y_hist[last][i] * y_hist[last][i];
            }
            if (yy > 1e-30 && sy > 1e-30) gamma = sy / yy;
        }
        for (int i = 0; i < D; ++i) dir[i] = gamma * q[i];
        for (int k = bound - 1; k >= 0; --k) {
            int idx = (hist_idx - 1 - k + m) % m;
            double dot = 0.0;
            for (int i = 0; i < D; ++i) dot += y_hist[idx][i] * dir[i];
            double beta = rho_hist[idx] * dot;
            for (int i = 0; i < D; ++i) dir[i] += s_hist[idx][i] * (alpha[idx] - beta);
        }
        for (int i = 0; i < D; ++i) dir[i] = -dir[i];

        double dg = 0.0, dnorm = 0.0;
        for (int i = 0; i < D; ++i) {
            dg += dir[i] * g[i];
            dnorm += dir[i] * dir[i];
        }
        dnorm = std::sqrt(dnorm);
        if (dg >= 0.0) {
            for (int i = 0; i < D; ++i) dir[i] = -g[i];
            dg = -gnorm * gnorm;
            dnorm = gnorm;
            hist_len = 0;
        }
        double step = (dnorm > 0.35) ? (0.35 / dnorm) : 1.0;
        x_old = x;
        g_old = g;
        double f_old = f;
        bool accepted = false;
        for (int ls = 0; ls < 25; ++ls) {
            for (int i = 0; i < D; ++i) x[i] = x_old[i] + step * dir[i];
            double f_new = eval_fs_grad(N, x.data(), g.data(), p);
            if (f_new <= f_old + 1e-4 * step * dg) {
                f = f_new;
                accepted = true;
                break;
            }
            step *= 0.5;
        }
        if (!accepted) {
            x = x_old;
            g = g_old;
            f = f_old;
            hist_len = 0;
            continue;
        }
        double sy = 0.0;
        for (int i = 0; i < D; ++i) {
            s_hist[hist_idx][i] = x[i] - x_old[i];
            y_hist[hist_idx][i] = g[i] - g_old[i];
            sy += s_hist[hist_idx][i] * y_hist[hist_idx][i];
        }
        if (sy > 1e-28) {
            rho_hist[hist_idx] = 1.0 / sy;
            hist_idx = (hist_idx + 1) % m;
            hist_len++;
        }
    }
    return eval_fs_grad(N, x.data(), g.data(), p, nullptr, false);
}

// Damped Cholesky Newton-Raphson polisher driving ||grad E||_2 < 1e-13
double newton_polish(int N, std::vector<double>& x, const FSParams& p, int max_steps = 12) {
    const int D = 3 * N;
    std::vector<double> g(D), gp(D), gm(D), H(D * D, 0.0), L(D * D, 0.0), y(D), dx(D), x_try(D);
    double f = eval_fs_grad(N, x.data(), g.data(), p, nullptr, false);

    for (int step = 0; step < max_steps; ++step) {
        double gnorm = 0.0;
        for (int i = 0; i < D; ++i) gnorm += g[i] * g[i];
        gnorm = std::sqrt(gnorm);
        if (gnorm < 1e-13) break;

        const double eps = 1e-6;
        const double inv_2eps = 1.0 / (2.0 * eps);
        for (int k = 0; k < D; ++k) {
            double orig = x[k];
            x[k] = orig + eps;
            eval_fs_grad(N, x.data(), gp.data(), p, nullptr, false);
            x[k] = orig - eps;
            eval_fs_grad(N, x.data(), gm.data(), p, nullptr, false);
            x[k] = orig;
            for (int i = 0; i < D; ++i) {
                H[i * D + k] = (gp[i] - gm[i]) * inv_2eps;
            }
        }
        for (int i = 0; i < D; ++i) {
            for (int j = i + 1; j < D; ++j) {
                double avg = 0.5 * (H[i * D + j] + H[j * D + i]);
                H[i * D + j] = H[j * D + i] = avg;
            }
        }

        double lambda = 1e-8;
        bool chol_ok = false;
        for (int tries = 0; tries < 25; ++tries) {
            std::fill(L.begin(), L.end(), 0.0);
            chol_ok = true;
            for (int i = 0; i < D; ++i) {
                for (int j = 0; j <= i; ++j) {
                    double sum = H[i * D + j] + (i == j ? lambda : 0.0);
                    for (int k = 0; k < j; ++k) sum -= L[i * D + k] * L[j * D + k];
                    if (i == j) {
                        if (sum <= 1e-13) { chol_ok = false; break; }
                        L[i * D + j] = std::sqrt(sum);
                    } else {
                        L[i * D + j] = sum / L[j * D + j];
                    }
                }
                if (!chol_ok) break;
            }
            if (chol_ok) break;
            lambda *= 10.0;
        }
        if (!chol_ok) break;

        for (int i = 0; i < D; ++i) {
            double sum = -g[i];
            for (int k = 0; k < i; ++k) sum -= L[i * D + k] * y[k];
            y[i] = sum / L[i * D + i];
        }
        for (int i = D - 1; i >= 0; --i) {
            double sum = y[i];
            for (int k = i + 1; k < D; ++k) sum -= L[k * D + i] * dx[k];
            dx[i] = sum / L[i * D + i];
        }

        double alpha = 1.0;
        bool improved = false;
        for (int ls = 0; ls < 20; ++ls) {
            for (int i = 0; i < D; ++i) x_try[i] = x[i] + alpha * dx[i];
            double f_try = eval_fs_grad(N, x_try.data(), gp.data(), p, nullptr, false);
            double gnorm_try = 0.0;
            for (int i = 0; i < D; ++i) gnorm_try += gp[i] * gp[i];
            gnorm_try = std::sqrt(gnorm_try);
            if (f_try <= f + 1e-14 && gnorm_try < gnorm) {
                x = x_try;
                f = f_try;
                g = gp;
                improved = true;
                break;
            }
            alpha *= 0.5;
        }
        if (!improved) break;
    }
    return f;
}

std::vector<double> load_points(const std::string& path, int expected_N) {
    std::ifstream in(path);
    if (!in.is_open()) return {};
    std::vector<double> xyz;
    double x, y, z;
    while (in >> x >> y >> z) {
        xyz.push_back(x);
        xyz.push_back(y);
        xyz.push_back(z);
    }
    if ((int)xyz.size() != 3 * expected_N) return {};
    return xyz;
}

void center_cluster(int N, std::vector<double>& xyz) {
    double cx = 0, cy = 0, cz = 0;
    for (int i = 0; i < N; ++i) {
        cx += xyz[3 * i]; cy += xyz[3 * i + 1]; cz += xyz[3 * i + 2];
    }
    cx /= N; cy /= N; cz /= N;
    for (int i = 0; i < N; ++i) {
        xyz[3 * i] -= cx; xyz[3 * i + 1] -= cy; xyz[3 * i + 2] -= cz;
    }
}

void save_xyz(const std::string& path, int N, const std::vector<double>& xyz) {
    std::ofstream out(path);
    out << std::setprecision(16);
    for (int i = 0; i < N; ++i) {
        out << std::setw(24) << xyz[3 * i] << " "
            << std::setw(24) << xyz[3 * i + 1] << " "
            << std::setw(24) << xyz[3 * i + 2] << "\n";
    }
}

std::vector<std::array<double, 3>> generate_hollow_sites(int M, const std::vector<double>& xyz, double r0) {
    std::vector<std::array<double, 3>> sites;
    double cx = 0, cy = 0, cz = 0;
    for (int i = 0; i < M; ++i) {
        cx += xyz[3 * i]; cy += xyz[3 * i + 1]; cz += xyz[3 * i + 2];
    }
    cx /= M; cy /= M; cz /= M;

    double r_cut = 1.42 * r0;
    for (int i = 0; i < M; ++i) {
        for (int j = i + 1; j < M; ++j) {
            double dxij = xyz[3 * i] - xyz[3 * j], dyij = xyz[3 * i + 1] - xyz[3 * j + 1], dzij = xyz[3 * i + 2] - xyz[3 * j + 2];
            double rij = std::sqrt(dxij * dxij + dyij * dyij + dzij * dzij);
            if (rij > r_cut) continue;
            for (int k = j + 1; k < M; ++k) {
                double dxik = xyz[3 * i] - xyz[3 * k], dyik = xyz[3 * i + 1] - xyz[3 * k + 1], dzik = xyz[3 * i + 2] - xyz[3 * k + 2];
                double rik = std::sqrt(dxik * dxik + dyik * dyik + dzik * dzik);
                if (rik > r_cut) continue;
                double dxjk = xyz[3 * j] - xyz[3 * k], dyjk = xyz[3 * j + 1] - xyz[3 * k + 1], dzjk = xyz[3 * j + 2] - xyz[3 * k + 2];
                double rjk = std::sqrt(dxjk * dxjk + dyjk * dyjk + dzjk * dzjk);
                if (rjk > r_cut) continue;

                double mx = (xyz[3 * i] + xyz[3 * j] + xyz[3 * k]) / 3.0;
                double my = (xyz[3 * i + 1] + xyz[3 * j + 1] + xyz[3 * k + 1]) / 3.0;
                double mz = (xyz[3 * i + 2] + xyz[3 * j + 2] + xyz[3 * k + 2]) / 3.0;
                double ux = xyz[3 * j] - xyz[3 * i], uy = xyz[3 * j + 1] - xyz[3 * i + 1], uz = xyz[3 * j + 2] - xyz[3 * i + 2];
                double vx = xyz[3 * k] - xyz[3 * i], vy = xyz[3 * k + 1] - xyz[3 * i + 1], vz = xyz[3 * k + 2] - xyz[3 * i + 2];
                double nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
                double nlen = std::sqrt(nx * nx + ny * ny + nz * nz);
                if (nlen < 1e-8) continue;
                nx /= nlen; ny /= nlen; nz /= nlen;
                if (nx * (mx - cx) + ny * (my - cy) + nz * (mz - cz) < 0) {
                    nx = -nx; ny = -ny; nz = -nz;
                }
                for (double h_fac : {0.74, 0.82}) {
                    double h = h_fac * r0;
                    double sx = mx + h * nx, sy = my + h * ny, sz = mz + h * nz;
                    bool clash = false;
                    for (int m = 0; m < M; ++m) {
                        double d2 = (sx - xyz[3 * m]) * (sx - xyz[3 * m]) +
                                    (sy - xyz[3 * m + 1]) * (sy - xyz[3 * m + 1]) +
                                    (sz - xyz[3 * m + 2]) * (sz - xyz[3 * m + 2]);
                        if (d2 < (0.70 * r0) * (0.70 * r0)) { clash = true; break; }
                    }
                    if (!clash) sites.push_back({sx, sy, sz});
                }
            }
        }
    }
    return sites;
}

int main(int argc, char** argv) {
    std::vector<std::vector<double>> mo_ref(101), fe_ref(101);
    std::vector<double> mo_tab(101, 0.0), fe_tab(101, 0.0);
    std::vector<double> mo_best_e(101, 0.0), fe_best_e(101, 0.0);
    std::vector<std::vector<double>> mo_best_x(101), fe_best_x(101);

    std::vector<double> g_tmp(300);
    for (int N = 3; N <= 100; ++N) {
        mo_ref[N] = load_points("/tmp/ccd_fs/mo_pts/points/" + std::to_string(N), N);
        fe_ref[N] = load_points("/tmp/ccd_fs/fe_pts/points/" + std::to_string(N), N);
        center_cluster(N, mo_ref[N]);
        center_cluster(N, fe_ref[N]);
        mo_tab[N] = eval_fs_grad(N, mo_ref[N].data(), g_tmp.data(), MO_PARAMS, nullptr, false);
        fe_tab[N] = eval_fs_grad(N, fe_ref[N].data(), g_tmp.data(), FE_PARAMS, nullptr, false);

        auto xm = mo_ref[N];
        double em = lbfgs_optimize(N, xm, MO_PARAMS, 1000, 1e-13);
        mo_best_e[N] = em;
        mo_best_x[N] = xm;

        auto xf = fe_ref[N];
        double ef = lbfgs_optimize(N, xf, FE_PARAMS, 1000, 1e-13);
        fe_best_e[N] = ef;
        fe_best_x[N] = xf;

        // Also check if a saved best_<metal>_<N>.xyz already exists on disk
        auto saved_mo = load_points("/tmp/ccd_fs/best_Mo_" + std::to_string(N) + ".xyz", N);
        if (!saved_mo.empty()) {
            double es = lbfgs_optimize(N, saved_mo, MO_PARAMS, 1000, 1e-13);
            if (es < mo_best_e[N] - 1e-6) {
                es = newton_polish(N, saved_mo, MO_PARAMS);
                mo_best_e[N] = es;
                mo_best_x[N] = saved_mo;
                save_xyz("/tmp/ccd_fs/best_Mo_" + std::to_string(N) + ".xyz", N, saved_mo);
            }
        }
        auto saved_fe = load_points("/tmp/ccd_fs/best_Fe_" + std::to_string(N) + ".xyz", N);
        if (!saved_fe.empty()) {
            double es = lbfgs_optimize(N, saved_fe, FE_PARAMS, 1000, 1e-13);
            if (es < fe_best_e[N] - 1e-6) {
                es = newton_polish(N, saved_fe, FE_PARAMS);
                fe_best_e[N] = es;
                fe_best_x[N] = saved_fe;
                save_xyz("/tmp/ccd_fs/best_Fe_" + std::to_string(N) + ".xyz", N, saved_fe);
            }
        }
    }

    std::mutex mtx;
    std::atomic<int> new_improvements{0};

    auto check_update = [&](bool is_mo, int N, const std::vector<double>& cand_in, const char* tag) -> bool {
        const FSParams& p = is_mo ? MO_PARAMS : FE_PARAMS;
        std::vector<double> x = cand_in;
        double e = lbfgs_optimize(N, x, p, 800, 1e-12);
        double tab_e = is_mo ? mo_tab[N] : fe_tab[N];
        double& best_e = is_mo ? mo_best_e[N] : fe_best_e[N];
        auto& best_x = is_mo ? mo_best_x[N] : fe_best_x[N];
        if (e < best_e - 1e-6) {
            std::lock_guard<std::mutex> lk(mtx);
            if (e < best_e - 1e-6) {
                e = newton_polish(N, x, p);
                center_cluster(N, x);
                std::vector<double> g_check(3 * N);
                eval_fs_grad(N, x.data(), g_check.data(), p, nullptr, false);
                double gnorm = 0.0;
                for (double v : g_check) gnorm += v * v;
                gnorm = std::sqrt(gnorm);

                best_e = e;
                best_x = x;
                double diff_tab = e - tab_e;
                if (diff_tab < -1e-4) {
                    std::printf("!!! NEW RECORD [%s_%d via %s]: E* = %.10f vs CCD = %.10f (delta = %+.6f eV, ||g||_2 = %.2e) !!!\n",
                                p.name.c_str(), N, tag, e, tab_e, diff_tab, gnorm);
                    std::fflush(stdout);
                    save_xyz("/tmp/ccd_fs/best_" + p.name + "_" + std::to_string(N) + ".xyz", N, x);
                    new_improvements++;
                    return true;
                }
            }
        }
        return false;
    };

    int n_threads = 10;
    for (int pass = 1; pass <= 4; ++pass) {
        int before = new_improvements.load();
        std::printf("=== Cascade Pass %d: Cross-Seeding + Downward Etch (100->3) + Upward Grow (3->100) ===\n", pass);

        // 1. Cross-seeding current best Mo <-> Fe
        for (int N = 3; N <= 100; ++N) {
            for (double s : {0.89, 0.9108, 0.93}) {
                std::vector<double> x = mo_best_x[N];
                for (double& v : x) v *= s;
                check_update(false, N, x, "CrossSeed(Mo->Fe)");
            }
            for (double s : {1.075, 1.0979, 1.12}) {
                std::vector<double> x = fe_best_x[N];
                for (double& v : x) v *= s;
                check_update(true, N, x, "CrossSeed(Fe->Mo)");
            }
        }

        // 2. Sequential Downward Etch Cascade N = 99 down to 3 (parallelized over candidate removals!)
        for (int N = 99; N >= 3; --N) {
            for (int is_mo = 0; is_mo < 2; ++is_mo) {
                const FSParams& p = is_mo ? MO_PARAMS : FE_PARAMS;
                struct Task { std::vector<double> cand; const char* tag; };
                std::vector<Task> tasks;

                // Single-atom etch from N+1 (both same-metal and cross-metal)
                for (int src_mo = 0; src_mo < 2; ++src_mo) {
                    double scale = (is_mo == src_mo) ? 1.0 : (is_mo ? 1.0979 : 0.9108);
                    const auto& parent = src_mo ? mo_best_x[N + 1] : fe_best_x[N + 1];
                    for (int rm = 0; rm < N + 1; ++rm) {
                        std::vector<double> cand;
                        cand.reserve(3 * N);
                        for (int i = 0; i < N + 1; ++i) {
                            if (i == rm) continue;
                            cand.push_back(parent[3 * i] * scale);
                            cand.push_back(parent[3 * i + 1] * scale);
                            cand.push_back(parent[3 * i + 2] * scale);
                        }
                        tasks.push_back({std::move(cand), "Etch1(N+1->N)"});
                    }
                }
                // Two-atom etch from N+2
                if (N + 2 <= 100) {
                    const auto& parent2 = is_mo ? mo_best_x[N + 2] : fe_best_x[N + 2];
                    std::vector<double> g2(3 * (N + 2)), ae(N + 2);
                    eval_fs_grad(N + 2, parent2.data(), g2.data(), p, ae.data(), false);
                    std::vector<int> ord(N + 2);
                    std::iota(ord.begin(), ord.end(), 0);
                    std::sort(ord.begin(), ord.end(), [&](int a, int b) { return ae[a] > ae[b]; });
                    int K = std::min(N + 2, 18);
                    for (int a = 0; a < K; ++a) {
                        for (int b = a + 1; b < K; ++b) {
                            int r1 = ord[a], r2 = ord[b];
                            std::vector<double> cand;
                            cand.reserve(3 * N);
                            for (int i = 0; i < N + 2; ++i) {
                                if (i == r1 || i == r2) continue;
                                cand.push_back(parent2[3 * i]);
                                cand.push_back(parent2[3 * i + 1]);
                                cand.push_back(parent2[3 * i + 2]);
                            }
                            tasks.push_back({std::move(cand), "Etch2(N+2->N)"});
                        }
                    }
                }

                std::atomic<size_t> idx{0};
                std::vector<std::thread> workers;
                for (int t = 0; t < n_threads; ++t) {
                    workers.emplace_back([&]() {
                        while (true) {
                            size_t k = idx.fetch_add(1);
                            if (k >= tasks.size()) break;
                            check_update(is_mo, N, tasks[k].cand, tasks[k].tag);
                        }
                    });
                }
                for (auto& w : workers) w.join();
            }
        }

        // 3. Sequential Upward Grow Cascade N = 4 up to 100 (parallelized over candidate hollow sites!)
        for (int N = 4; N <= 100; ++N) {
            for (int is_mo = 0; is_mo < 2; ++is_mo) {
                const FSParams& p = is_mo ? MO_PARAMS : FE_PARAMS;
                struct Task { std::vector<double> cand; const char* tag; };
                std::vector<Task> tasks;
                for (int src_mo = 0; src_mo < 2; ++src_mo) {
                    double scale = (is_mo == src_mo) ? 1.0 : (is_mo ? 1.0979 : 0.9108);
                    std::vector<double> base = src_mo ? mo_best_x[N - 1] : fe_best_x[N - 1];
                    for (double& v : base) v *= scale;
                    auto sites = generate_hollow_sites(N - 1, base, p.r0_nn);
                    int stride = std::max(1, (int)sites.size() / 120);
                    for (size_t s = 0; s < sites.size(); s += stride) {
                        std::vector<double> cand = base;
                        cand.push_back(sites[s][0]);
                        cand.push_back(sites[s][1]);
                        cand.push_back(sites[s][2]);
                        tasks.push_back({std::move(cand), "Grow1(N-1->N)"});
                    }
                }
                std::atomic<size_t> idx{0};
                std::vector<std::thread> workers;
                for (int t = 0; t < n_threads; ++t) {
                    workers.emplace_back([&]() {
                        while (true) {
                            size_t k = idx.fetch_add(1);
                            if (k >= tasks.size()) break;
                            check_update(is_mo, N, tasks[k].cand, tasks[k].tag);
                        }
                    });
                }
                for (auto& w : workers) w.join();
            }
        }

        if (new_improvements.load() == before && pass >= 2) {
            std::printf("Cascade converged after Pass %d.\n", pass);
            break;
        }
    }

    int mo_wins = 0, fe_wins = 0;
    std::printf("\n================ FINAL FINNIS-SINCLAIR RECORD TABLE ================\n");
    for (int N = 3; N <= 100; ++N) {
        if (mo_best_e[N] < mo_tab[N] - 1e-4) {
            std::printf("Mo_%-3d : E* = %15.10f vs CCD %15.10f (delta = %+11.6f eV)\n",
                        N, mo_best_e[N], mo_tab[N], mo_best_e[N] - mo_tab[N]);
            mo_wins++;
        }
    }
    for (int N = 3; N <= 100; ++N) {
        if (fe_best_e[N] < fe_tab[N] - 1e-4) {
            std::printf("Fe_%-3d : E* = %15.10f vs CCD %15.10f (delta = %+11.6f eV)\n",
                        N, fe_best_e[N], fe_tab[N], fe_best_e[N] - fe_tab[N]);
            fe_wins++;
        }
    }
    std::printf("Total new Finnis-Sinclair global minima: %d (Mo: %d, Fe: %d)\n", mo_wins + fe_wins, mo_wins, fe_wins);
    return 0;
}
