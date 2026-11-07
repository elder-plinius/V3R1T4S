// Dzugutov_Cluster_Hunter.cc
// Self-contained C++17 Multi-Threaded Polytetrahedral Cluster Solver for:
//   1. Dzugutov (N = 3..100, Doye, Wales & Simdyankin, Faraday Discuss. 118, 159, 2001)
//   2. mDzugutov (N = 3..250, Doye & Wales, PRL 86, 5719, 2001)
//   3. Z1 (N = 3..80, Doye, Wales, Zetterling & Dzugutov, JCP 118, 2792, 2003)
//   4. Z2 (N = 3..80, Doye, Wales, Zetterling & Dzugutov, JCP 118, 2792, 2003)
//
// Implements:
//   - Cross-potential seeding across Dzugutov, mDzugutov, Z1, Z2 (and rescaled Zn/Cd/Pb/Co/Mo/Fe)
//   - Downward 1-atom (N+1 -> N) and 2-atom (N+2 -> N) peripheral etching
//   - Upward tetrahedral capping (N-1 -> N) at regular-tetrahedron height sqrt(2/3) * r_eq
//   - Same-N 1-atom peripheral-to-tetrahedral-cap relocation (1-atom hop)
//   - Multi-threaded 2-stage L-BFGS tournament (coarse 180-iter screen -> top-8 2500-iter deep polish)

#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <regex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

namespace fs = std::filesystem;

template <typename Func>
void parallel_for(int count, Func fn) {
    if (count <= 0) return;
    int nthreads = std::min((int)std::thread::hardware_concurrency(), count);
    if (nthreads <= 1) {
        for (int i = 0; i < count; ++i) fn(i);
        return;
    }
    std::atomic<int> next_idx{0};
    std::vector<std::thread> pool;
    pool.reserve(nthreads);
    for (int t = 0; t < nthreads; ++t) {
        pool.emplace_back([&]() {
            while (true) {
                int i = next_idx.fetch_add(1, std::memory_order_relaxed);
                if (i >= count) break;
                fn(i);
            }
        });
    }
    for (auto& th : pool) th.join();
}

enum PotType { POT_DZUG, POT_MDZUG, POT_Z1, POT_Z2 };

struct PotSpec {
    std::string name;
    PotType type;
    int min_N;
    int max_N;
    double r_eq;
    // Dzugutov / mDzugutov params: A, B, a, b, c, d, m
    double A, B, a, b, c, d;
    int m_exp;
    // Z1 / Z2 params: a_z, alpha_z, kF, b_z, sigma, n_z, rc, v0
    double a_z, alpha_z, kF, b_z, sigma, n_z, rc, v0;
};

static const PotSpec POTS[] = {
    {"Dzugutov",  POT_DZUG,  3, 100, 1.130,
     5.82, 1.280, 1.87, 1.94, 1.10, 0.27, 16,
     0, 0, 0, 0, 0, 0, 1.94, 0},
    {"Z1",        POT_Z1,    3,  80, 1.078,
     0, 0, 0, 0, 0, 0, 0,
     1.58, -0.22, 4.120, 4.2e8, 0.331, 18.0, 2.649085591313801, 0.046826324124149},
    {"Z2",        POT_Z2,    3,  80, 1.133,
     0, 0, 0, 0, 0, 0, 0,
     1.04,  0.33, 4.139, 4.2e6, 0.348, 14.5, 2.644877841213031, 0.133915425377427},
    {"mDzugutov", POT_MDZUG, 3, 250, 1.153,
     3.00, 2.109, 1.65, 1.94, 0.52, 0.55, 4,
     0, 0, 0, 0, 0, 0, 1.94, 0},
};

inline void pair_pot(double r, const PotSpec& P, double& v, double& dv) {
    v = 0.0;
    dv = 0.0;
    if (P.type == POT_DZUG || P.type == POT_MDZUG) {
        if (r >= P.b) return;
        if (r < 0.45) r = 0.45;
        if (r < P.a) {
            double uma = r - P.a;
            double e1 = std::exp(P.c / uma);
            double rm = (P.m_exp == 16) ? (1.0 / ((r*r)*(r*r)*(r*r)*(r*r)*(r*r)*(r*r)*(r*r)*(r*r)))
                                        : (1.0 / ((r*r)*(r*r)));
            double rm_B = rm - P.B;
            v += P.A * rm_B * e1;
            dv += P.A * (-P.m_exp * (rm / r) - rm_B * P.c / (uma * uma)) * e1;
        }
        double umb = r - P.b;
        double e2 = P.B * std::exp(P.d / umb);
        v += e2;
        dv += -e2 * P.d / (umb * umb);
    } else {
        if (r >= P.rc) return;
        if (r < 0.45) r = 0.45;
        double ear = P.a_z * std::exp(P.alpha_z * r) / (r * r * r);
        double kr = 2.0 * P.kF * r;
        double cs = std::cos(kr);
        double sn = std::sin(kr);
        double rep = P.b_z * std::pow(P.sigma / r, P.n_z);
        v = ear * cs + rep + P.v0;
        dv = ear * ((P.alpha_z - 3.0 / r) * cs - 2.0 * P.kF * sn) - P.n_z * rep / r;
    }
}

double eval_energy_grad(const double* x, int N, const PotSpec& P, double* g) {
    if (g) std::fill(g, g + 3 * N, 0.0);
    double E = 0.0;
    double r_cut = (P.type == POT_DZUG || P.type == POT_MDZUG) ? P.b : P.rc;
    double r_cut2 = r_cut * r_cut;

    for (int i = 0; i < N; ++i) {
        const double xi = x[3 * i], yi = x[3 * i + 1], zi = x[3 * i + 2];
        for (int j = i + 1; j < N; ++j) {
            double dx = xi - x[3 * j];
            double dy = yi - x[3 * j + 1];
            double dz = zi - x[3 * j + 2];
            double r2 = dx * dx + dy * dy + dz * dz;
            if (r2 >= r_cut2) continue;
            double r = std::sqrt(r2);
            double v, dv;
            pair_pot(r, P, v, dv);
            E += v;
            if (g) {
                double fac = dv / (r > 1e-12 ? r : 1e-12);
                g[3 * i]     += fac * dx;
                g[3 * i + 1] += fac * dy;
                g[3 * i + 2] += fac * dz;
                g[3 * j]     -= fac * dx;
                g[3 * j + 1] -= fac * dy;
                g[3 * j + 2] -= fac * dz;
            }
        }
    }
    return E;
}

void compute_atom_energies(const std::vector<double>& x, int N, const PotSpec& P, std::vector<double>& e_atom) {
    e_atom.assign(N, 0.0);
    double r_cut = (P.type == POT_DZUG || P.type == POT_MDZUG) ? P.b : P.rc;
    double r_cut2 = r_cut * r_cut;
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = x[3 * i] - x[3 * j];
            double dy = x[3 * i + 1] - x[3 * j + 1];
            double dz = x[3 * i + 2] - x[3 * j + 2];
            double r2 = dx * dx + dy * dy + dz * dz;
            if (r2 >= r_cut2) continue;
            double v, dv;
            pair_pot(std::sqrt(r2), P, v, dv);
            e_atom[i] += 0.5 * v;
            e_atom[j] += 0.5 * v;
        }
    }
}

double lbfgs_minimize(std::vector<double>& x, int N, const PotSpec& P, int max_iter = 2200, double gtol = 1e-12) {
    const int D = 3 * N;
    const int M = 10;
    std::vector<double> g(D), x_old(D), g_old(D), d(D), q(D), alpha(M);
    std::vector<std::vector<double>> s_hist(M, std::vector<double>(D));
    std::vector<std::vector<double>> y_hist(M, std::vector<double>(D));
    std::vector<double> rho_hist(M, 0.0);

    double f = eval_energy_grad(x.data(), N, P, g.data());
    int hist_len = 0, hist_idx = 0;

    for (int iter = 0; iter < max_iter; ++iter) {
        double gnorm2 = 0.0;
        for (int i = 0; i < D; ++i) gnorm2 += g[i] * g[i];
        if (!std::isfinite(gnorm2) || std::sqrt(gnorm2) < gtol) break;

        q = g;
        for (int k = hist_len - 1; k >= 0; --k) {
            int idx = (hist_idx - 1 - (hist_len - 1 - k) + M * 100) % M;
            double dot = 0.0;
            for (int i = 0; i < D; ++i) dot += s_hist[idx][i] * q[i];
            alpha[k] = rho_hist[idx] * dot;
            for (int i = 0; i < D; ++i) q[i] -= alpha[k] * y_hist[idx][i];
        }
        double gamma = 1.0;
        if (hist_len > 0) {
            int last = (hist_idx - 1 + M) % M;
            double sy = 0.0, yy = 0.0;
            for (int i = 0; i < D; ++i) {
                sy += s_hist[last][i] * y_hist[last][i];
                yy += y_hist[last][i] * y_hist[last][i];
            }
            if (yy > 1e-30 && sy > 1e-30) gamma = sy / yy;
        }
        for (int i = 0; i < D; ++i) d[i] = -gamma * q[i];
        for (int k = 0; k < hist_len; ++k) {
            int idx = (hist_idx - hist_len + k + M * 100) % M;
            double dot = 0.0;
            for (int i = 0; i < D; ++i) dot += y_hist[idx][i] * d[i];
            double beta = rho_hist[idx] * dot;
            for (int i = 0; i < D; ++i) d[i] -= s_hist[idx][i] * (alpha[k] - beta);
        }
        double dg = 0.0, dnorm2 = 0.0;
        for (int i = 0; i < D; ++i) {
            dg += d[i] * g[i];
            dnorm2 += d[i] * d[i];
        }
        if (dg >= 0.0 || !std::isfinite(dg)) {
            for (int i = 0; i < D; ++i) d[i] = -g[i];
            dg = -gnorm2;
            dnorm2 = gnorm2;
            hist_len = 0;
        }
        double dnorm = std::sqrt(dnorm2);
        double step = (dnorm > 0.12) ? (0.12 / dnorm) : 1.0;

        x_old = x;
        g_old = g;
        double f_old = f;
        bool ok = false;
        for (int ls = 0; ls < 24; ++ls) {
            for (int i = 0; i < D; ++i) x[i] = x_old[i] + step * d[i];
            f = eval_energy_grad(x.data(), N, P, g.data());
            if (std::isfinite(f) && f <= f_old + 1e-4 * step * dg) {
                ok = true;
                break;
            }
            step *= 0.5;
        }
        if (!ok) {
            x = x_old;
            f = f_old;
            break;
        }
        double sy = 0.0;
        for (int i = 0; i < D; ++i) {
            s_hist[hist_idx][i] = x[i] - x_old[i];
            y_hist[hist_idx][i] = g[i] - g_old[i];
            sy += s_hist[hist_idx][i] * y_hist[hist_idx][i];
        }
        if (sy > 1e-28) {
            rho_hist[hist_idx] = 1.0 / sy;
            hist_idx = (hist_idx + 1) % M;
            if (hist_len < M) hist_len++;
        } else {
            hist_len = 0;
        }
    }
    double cx = 0.0, cy = 0.0, cz = 0.0;
    for (int i = 0; i < N; ++i) {
        cx += x[3 * i]; cy += x[3 * i + 1]; cz += x[3 * i + 2];
    }
    cx /= N; cy /= N; cz /= N;
    for (int i = 0; i < N; ++i) {
        x[3 * i] -= cx; x[3 * i + 1] -= cy; x[3 * i + 2] -= cz;
    }
    return eval_energy_grad(x.data(), N, P, nullptr);
}

void run_tournament(std::vector<std::vector<double>>& cands, int n, const PotSpec& P,
                    double& cand_best_e, std::vector<double>& cand_best_x, int top_k = 8) {
    int C = (int)cands.size();
    if (C == 0) return;
    std::vector<double> coarse_e(C, 1e30);
    parallel_for(C, [&](int i) {
        coarse_e[i] = lbfgs_minimize(cands[i], n, P, 180, 1e-5);
    });
    std::vector<int> idx(C);
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return coarse_e[a] < coarse_e[b]; });
    int K = std::min(C, top_k);
    std::mutex mtx;
    parallel_for(K, [&](int k) {
        int i = idx[k];
        double e = lbfgs_minimize(cands[i], n, P, 2500, 1e-12);
        if (e < cand_best_e - 1e-7) {
            std::lock_guard<std::mutex> lk(mtx);
            if (e < cand_best_e - 1e-7) {
                cand_best_e = e;
                cand_best_x = cands[i];
            }
        }
    });
}

void save_xyz(const std::string& name, int n, const std::vector<double>& x) {
    std::string out_path = "./ccd_dzugutov/wins/" + name + "_" + std::to_string(n) + ".xyz";
    std::ofstream out(out_path);
    out << std::setprecision(17);
    for (int i = 0; i < n; ++i) {
        out << x[3 * i] << " " << x[3 * i + 1] << " " << x[3 * i + 2] << "\n";
    }
}

std::vector<double> load_coords(const std::string& path, bool fix_z = true) {
    std::ifstream in(path);
    std::vector<double> c;
    std::string line;
    while (std::getline(in, line)) {
        if (line.find('=') != std::string::npos) continue;
        std::istringstream iss(line);
        std::vector<std::string> toks;
        std::string tok;
        while (iss >> tok) toks.push_back(tok);
        if (toks.size() == 3 || toks.size() == 4) {
            int off = (toks.size() == 4) ? 1 : 0;
            try {
                double x = std::stod(toks[off]);
                double y = std::stod(toks[off + 1]);
                double z = std::stod(toks[off + 2]);
                if (fix_z) {
                    if (std::abs(x) > 10.0) x *= 1e-10;
                    if (std::abs(y) > 10.0) y *= 1e-10;
                    if (std::abs(z) > 10.0) z *= 1e-10;
                }
                c.push_back(x); c.push_back(y); c.push_back(z);
            } catch (...) {}
        }
    }
    return c;
}

std::vector<double> rescale_to_req(const std::vector<double>& x, double target_req) {
    int N = (int)x.size() / 3;
    if (N < 2) return x;
    double sum_nn = 0.0;
    for (int i = 0; i < N; ++i) {
        double best_r = 1e30;
        for (int j = 0; j < N; ++j) {
            if (i == j) continue;
            double dx = x[3 * i] - x[3 * j];
            double dy = x[3 * i + 1] - x[3 * j + 1];
            double dz = x[3 * i + 2] - x[3 * j + 2];
            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (r < best_r) best_r = r;
        }
        sum_nn += best_r;
    }
    double avg_nn = sum_nn / N;
    std::vector<double> out = x;
    if (avg_nn > 0.1) {
        double scale = target_req / avg_nn;
        for (double& v : out) v *= scale;
    }
    return out;
}

void generate_tetrahedral_caps(const std::vector<double>& x, int N, double r_eq, std::vector<double>& sites) {
    sites.clear();
    double max_edge2 = (1.36 * r_eq) * (1.36 * r_eq);
    double clash2 = (0.78 * r_eq) * (0.78 * r_eq);
    double dup2 = (0.32 * r_eq) * (0.32 * r_eq);
    double h_tet = 0.8165 * r_eq;

    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dxij = x[3 * i] - x[3 * j], dyij = x[3 * i + 1] - x[3 * j + 1], dzij = x[3 * i + 2] - x[3 * j + 2];
            if (dxij * dxij + dyij * dyij + dzij * dzij > max_edge2) continue;
            for (int k = j + 1; k < N; ++k) {
                double dxik = x[3 * i] - x[3 * k], dyik = x[3 * i + 1] - x[3 * k + 1], dzik = x[3 * i + 2] - x[3 * k + 2];
                if (dxik * dxik + dyik * dyik + dzik * dzik > max_edge2) continue;
                double dxjk = x[3 * j] - x[3 * k], dyjk = x[3 * j + 1] - x[3 * k + 1], dzjk = x[3 * j + 2] - x[3 * k + 2];
                if (dxjk * dxjk + dyjk * dyjk + dzjk * dzjk > max_edge2) continue;

                double mx = (x[3 * i] + x[3 * j] + x[3 * k]) / 3.0;
                double my = (x[3 * i + 1] + x[3 * j + 1] + x[3 * k + 1]) / 3.0;
                double mz = (x[3 * i + 2] + x[3 * j + 2] + x[3 * k + 2]) / 3.0;

                double ux = x[3 * j] - x[3 * i], uy = x[3 * j + 1] - x[3 * i + 1], uz = x[3 * j + 2] - x[3 * i + 2];
                double vx = x[3 * k] - x[3 * i], vy = x[3 * k + 1] - x[3 * i + 1], vz = x[3 * k + 2] - x[3 * i + 2];
                double nx = uy * vz - uz * vy;
                double ny = uz * vx - ux * vz;
                double nz = ux * vy - uy * vx;
                double nn = std::sqrt(nx * nx + ny * ny + nz * nz);
                if (nn < 1e-8) continue;
                nx /= nn; ny /= nn; nz /= nn;

                // Try both sides (+h_tet and -h_tet) since polytetrahedral clusters are non-convex chains/rings/networks!
                for (int sgn : {-1, 1}) {
                    double px = mx + sgn * h_tet * nx;
                    double py = my + sgn * h_tet * ny;
                    double pz = mz + sgn * h_tet * nz;

                    bool clash = false;
                    for (int m = 0; m < N; ++m) {
                        double dx = px - x[3 * m], dy = py - x[3 * m + 1], dz = pz - x[3 * m + 2];
                        if (dx * dx + dy * dy + dz * dz < clash2) {
                            clash = true;
                            break;
                        }
                    }
                    if (clash) continue;
                    bool dup = false;
                    for (size_t s = 0; s < sites.size() / 3; ++s) {
                        double dx = px - sites[3 * s], dy = py - sites[3 * s + 1], dz = pz - sites[3 * s + 2];
                        if (dx * dx + dy * dy + dz * dz < dup2) {
                            dup = true;
                            break;
                        }
                    }
                    if (!dup) {
                        sites.push_back(px); sites.push_back(py); sites.push_back(pz);
                    }
                }
            }
        }
    }
}

std::map<int, double> parse_table_generic(const std::string& path, const std::string& pattern) {
    std::ifstream in(path);
    std::string txt((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    std::map<int, double> res;
    std::regex re(pattern);
    auto begin = std::sregex_iterator(txt.begin(), txt.end(), re);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; ++it) {
        int n = std::stoi((*it)[1].str());
        double e = std::stod((*it)[2].str());
        res[n] = e;
    }
    return res;
}

int main(int argc, char** argv) {
    std::string filter_pot = (argc > 1) ? argv[1] : "";
    fs::create_directories("./ccd_dzugutov/wins");

    std::map<int, std::vector<std::pair<std::string, std::vector<double>>>> seed_lib;
    auto add_seed = [&](int N, const std::string& tag, const std::vector<double>& c) {
        if ((int)c.size() == 3 * N) {
            seed_lib[N].push_back({tag, c});
        }
    };

    for (int n = 3; n <= 100; ++n) {
        std::string p = "./ccd_dzugutov/dzug_pts/" + std::to_string(n);
        if (fs::exists(p)) add_seed(n, "Dzug", load_coords(p));
    }
    for (int n = 3; n <= 250; ++n) {
        std::string p = "./ccd_dzugutov/mdzug_pts/" + std::to_string(n);
        if (fs::exists(p)) add_seed(n, "mDzug", load_coords(p));
    }
    for (int n = 3; n <= 80; ++n) {
        std::string p1 = "./ccd_dzugutov/z1_pts/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Z1", load_coords(p1));
        std::string p2 = "./ccd_dzugutov/z2_pts/" + std::to_string(n);
        if (fs::exists(p2)) add_seed(n, "Z2", load_coords(p2));
    }

    std::map<std::string, std::map<int, double>> ref_energy;
    ref_energy["Dzugutov"]  = parse_table_generic("./ccd_dzugutov/dzug_table.html", "points/(\\d+)[^>]*>\\s*\\d+\\s*</[aA]>[^-]*(-?\\d+\\.\\d+)");
    ref_energy["mDzugutov"] = parse_table_generic("./ccd_dzugutov/mdzug_table.html", "<TD[^>]*>\\s*(\\d+)\\s*</TD>\\s*<TD[^>]*>\\s*(?:<A[^>]*>)?\\s*(-?\\d+\\.\\d+)");
    ref_energy["Z1"]        = parse_table_generic("./ccd_dzugutov/zett_table.html", "Z1points/(\\d+)\">\\s*(-?\\d+\\.\\d+)");
    ref_energy["Z2"]        = parse_table_generic("./ccd_dzugutov/zett_table.html", "Z2points/(\\d+)\">\\s*(-?\\d+\\.\\d+)");

    std::mutex print_mtx;

    for (const auto& P : POTS) {
        if (!filter_pot.empty() && P.name != filter_pot) continue;
        std::cout << "\n======================================================\n";
        std::cout << "HUNTING POTENTIAL: " << P.name << " (N = " << P.min_N << ".." << P.max_N << ")\n";
        std::cout << "======================================================\n";

        std::vector<std::vector<double>> best_x(P.max_N + 1);
        std::vector<double> best_e(P.max_N + 1, 1e30);
        std::vector<double> posted_pol_e(P.max_N + 1, 1e30);

        std::string own_tag = (P.name == "Dzugutov") ? "Dzug" : ((P.name == "mDzugutov") ? "mDzug" : P.name);

        // Phase 1: Cross-potential seeding in parallel
        std::vector<int> ns;
        for (int n = P.min_N; n <= P.max_N; ++n) ns.push_back(n);
        parallel_for((int)ns.size(), [&](int idx) {
            int n = ns[idx];
            double ref = ref_energy[P.name][n];
            for (const auto& kv : seed_lib[n]) {
                for (double s : {0.96, 1.00, 1.04}) {
                    if (kv.first == own_tag && s != 1.00) continue;
                    std::vector<double> c = rescale_to_req(kv.second, P.r_eq * s);
                    if (kv.first == own_tag && s == 1.00) c = kv.second;
                    double e = lbfgs_minimize(c, n, P, 2200, 1e-12);
                    if (kv.first == own_tag && s == 1.00) posted_pol_e[n] = e;
                    if (e < best_e[n]) {
                        best_e[n] = e;
                        best_x[n] = c;
                    }
                }
            }
            double bar = std::min(ref, posted_pol_e[n]);
            if (best_e[n] < bar - 1e-4) {
                std::lock_guard<std::mutex> lk(print_mtx);
                save_xyz(P.name, n, best_x[n]);
                std::printf("  [CROSS-SEED WIN] %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f)\n",
                            P.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                std::fflush(stdout);
            }
        });

        // Phase 2: Bidirectional Etch / Tetrahedral Cap / 1-Atom Hop Cascade
        for (int pass = 1; pass <= 2; ++pass) {
            std::cout << "--- Pass " << pass << " (Downward Etch + Upward Tetrahedral Cap + 1-Atom Hop) ---\n";
            int improved = 0;

            // 1. Downward pass: N = max_N - 1 down to min_N
            for (int n = P.max_N - 1; n >= P.min_N; --n) {
                std::vector<std::vector<double>> cands;
                if (!best_x[n + 1].empty()) {
                    const std::vector<double>& xp1 = best_x[n + 1];
                    for (int rm = 0; rm < n + 1; ++rm) {
                        std::vector<double> c;
                        c.reserve(3 * n);
                        for (int i = 0; i < n + 1; ++i) {
                            if (i == rm) continue;
                            c.push_back(xp1[3 * i]);
                            c.push_back(xp1[3 * i + 1]);
                            c.push_back(xp1[3 * i + 2]);
                        }
                        cands.push_back(std::move(c));
                    }
                }
                if (n + 2 <= P.max_N && !best_x[n + 2].empty() && n >= 20) {
                    const std::vector<double>& xp2 = best_x[n + 2];
                    std::vector<double> ea;
                    compute_atom_energies(xp2, n + 2, P, ea);
                    std::vector<int> ord(n + 2);
                    std::iota(ord.begin(), ord.end(), 0);
                    std::sort(ord.begin(), ord.end(), [&](int a, int b) { return ea[a] > ea[b]; });
                    int K = std::min(n + 2, 16);
                    for (int a = 0; a < K; ++a) {
                        for (int b = a + 1; b < K; ++b) {
                            int r1 = ord[a], r2 = ord[b];
                            std::vector<double> c;
                            c.reserve(3 * n);
                            for (int i = 0; i < n + 2; ++i) {
                                if (i == r1 || i == r2) continue;
                                c.push_back(xp2[3 * i]);
                                c.push_back(xp2[3 * i + 1]);
                                c.push_back(xp2[3 * i + 2]);
                            }
                            cands.push_back(std::move(c));
                        }
                    }
                }

                double cand_best_e = best_e[n];
                std::vector<double> cand_best_x;
                run_tournament(cands, n, P, cand_best_e, cand_best_x, 8);

                if (!cand_best_x.empty() && cand_best_e < best_e[n] - 1e-6) {
                    best_e[n] = cand_best_e;
                    best_x[n] = cand_best_x;
                    improved++;
                    double ref = ref_energy[P.name][n];
                    double bar = std::min(ref, posted_pol_e[n]);
                    if (best_e[n] < bar - 1e-4) {
                        save_xyz(P.name, n, best_x[n]);
                        seed_lib[n].push_back({P.name + "_win", best_x[n]});
                        std::printf("  [DOWNWARD WIN] %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f)\n",
                                    P.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                        std::fflush(stdout);
                    }
                }
            }

            // 2. Upward pass: N = min_N + 1 up to max_N
            for (int n = P.min_N + 1; n <= P.max_N; ++n) {
                if (best_x[n - 1].empty()) continue;
                const std::vector<double>& xm1 = best_x[n - 1];
                std::vector<double> sites;
                generate_tetrahedral_caps(xm1, n - 1, P.r_eq, sites);
                int num_sites = (int)sites.size() / 3;
                if (num_sites == 0) continue;

                std::vector<std::pair<double, int>> site_order;
                for (int s = 0; s < num_sites; ++s) {
                    std::vector<double> c = xm1;
                    c.push_back(sites[3 * s]);
                    c.push_back(sites[3 * s + 1]);
                    c.push_back(sites[3 * s + 2]);
                    double e0 = eval_energy_grad(c.data(), n, P, nullptr);
                    site_order.push_back({e0, s});
                }
                std::sort(site_order.begin(), site_order.end());
                int S_try = std::min((int)site_order.size(), 36);

                std::vector<std::vector<double>> cands;
                for (int idx = 0; idx < S_try; ++idx) {
                    int s = site_order[idx].second;
                    std::vector<double> c = xm1;
                    c.push_back(sites[3 * s]);
                    c.push_back(sites[3 * s + 1]);
                    c.push_back(sites[3 * s + 2]);
                    cands.push_back(std::move(c));
                }

                double cand_best_e = best_e[n];
                std::vector<double> cand_best_x;
                run_tournament(cands, n, P, cand_best_e, cand_best_x, 8);

                if (!cand_best_x.empty() && cand_best_e < best_e[n] - 1e-6) {
                    best_e[n] = cand_best_e;
                    best_x[n] = cand_best_x;
                    improved++;
                    double ref = ref_energy[P.name][n];
                    double bar = std::min(ref, posted_pol_e[n]);
                    if (best_e[n] < bar - 1e-4) {
                        save_xyz(P.name, n, best_x[n]);
                        seed_lib[n].push_back({P.name + "_win", best_x[n]});
                        std::printf("  [UPWARD WIN]   %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f)\n",
                                    P.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                        std::fflush(stdout);
                    }
                }
            }

            // 3. Same-N 1-Atom Hop (relocate weakest-bound peripheral atoms to best tetrahedral cap sites)
            for (int n = 14; n <= P.max_N; ++n) {
                if (best_x[n].empty()) continue;
                const std::vector<double>& xn = best_x[n];
                std::vector<double> ea;
                compute_atom_energies(xn, n, P, ea);
                std::vector<int> ord(n);
                std::iota(ord.begin(), ord.end(), 0);
                std::sort(ord.begin(), ord.end(), [&](int a, int b) { return ea[a] > ea[b]; });
                int K_rm = std::min(n, 6);

                std::vector<std::vector<double>> cands;
                for (int a = 0; a < K_rm; ++a) {
                    int rm = ord[a];
                    std::vector<double> core;
                    core.reserve(3 * (n - 1));
                    for (int i = 0; i < n; ++i) {
                        if (i == rm) continue;
                        core.push_back(xn[3 * i]);
                        core.push_back(xn[3 * i + 1]);
                        core.push_back(xn[3 * i + 2]);
                    }
                    std::vector<double> sites;
                    generate_tetrahedral_caps(core, n - 1, P.r_eq, sites);
                    int num_sites = (int)sites.size() / 3;
                    std::vector<std::pair<double, int>> site_order;
                    for (int s = 0; s < num_sites; ++s) {
                        std::vector<double> c = core;
                        c.push_back(sites[3 * s]);
                        c.push_back(sites[3 * s + 1]);
                        c.push_back(sites[3 * s + 2]);
                        double e0 = eval_energy_grad(c.data(), n, P, nullptr);
                        site_order.push_back({e0, s});
                    }
                    std::sort(site_order.begin(), site_order.end());
                    int S_try = std::min((int)site_order.size(), 10);
                    for (int idx = 0; idx < S_try; ++idx) {
                        int s = site_order[idx].second;
                        std::vector<double> c = core;
                        c.push_back(sites[3 * s]);
                        c.push_back(sites[3 * s + 1]);
                        c.push_back(sites[3 * s + 2]);
                        cands.push_back(std::move(c));
                    }
                }

                double cand_best_e = best_e[n];
                std::vector<double> cand_best_x;
                run_tournament(cands, n, P, cand_best_e, cand_best_x, 8);

                if (!cand_best_x.empty() && cand_best_e < best_e[n] - 1e-6) {
                    best_e[n] = cand_best_e;
                    best_x[n] = cand_best_x;
                    improved++;
                    double ref = ref_energy[P.name][n];
                    double bar = std::min(ref, posted_pol_e[n]);
                    if (best_e[n] < bar - 1e-4) {
                        save_xyz(P.name, n, best_x[n]);
                        seed_lib[n].push_back({P.name + "_win", best_x[n]});
                        std::printf("  [1-HOP WIN]    %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f)\n",
                                    P.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                        std::fflush(stdout);
                    }
                }
            }
            if (improved == 0) break;
        }

        int win_count = 0;
        for (int n = P.min_N; n <= P.max_N; ++n) {
            double ref = ref_energy[P.name][n];
            double bar = std::min(ref, posted_pol_e[n]);
            if (best_e[n] < bar - 1e-4) {
                win_count++;
                save_xyz(P.name, n, best_x[n]);
                std::printf("FINAL WIN %s_%d: E* = %.10f | ref = %.10f | pol_own = %.10f | dE = %+.6f\n",
                            P.name.c_str(), n, best_e[n], ref, posted_pol_e[n], best_e[n] - bar);
            }
        }
        std::printf("=== %s SUMMARY: %d NEW GLOBAL MINIMA DISCOVERED ===\n", P.name.c_str(), win_count);
        std::fflush(stdout);
    }
    return 0;
}
