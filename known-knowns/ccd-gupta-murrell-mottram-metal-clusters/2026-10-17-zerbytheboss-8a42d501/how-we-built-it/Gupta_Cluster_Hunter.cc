// Gupta_Cluster_Hunter.cc
// Self-contained C++17 Multi-Threaded Top-6 Tournament Solver for Gupta Metal Nanoclusters:
//   - Cd (N = 3..125, Doye PRB 2003)
//   - Zn (N = 3..125, Doye PRB 2003)
//   - Pb (N = 3..150, Doye CMS 2006 + Lai et al. Pb_Gupta.rar)
//   - Na (N = 3..379, Noya, Doye, Wales & Aguado EPJD 2006)
//   - Co (N = 2..200, Zhan et al. JCP 2005 + Lai et al. Co.zip)

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

struct GuptaParams {
    std::string name;
    double p;
    double q;
    double A;
    double xi;
    int min_N;
    int max_N;
};

static const GuptaParams METALS[] = {
    {"Cd",       10.612, 5.206, 0.1420,    0.8117,    3, 125},
    {"Zn",        9.689, 4.602, 0.1477,    0.8900,    3, 125},
    {"Pb",        9.576, 3.648, 0.0980,    0.9140,    3, 150},
    {"Na_Gupta", 10.130, 1.300, 0.0159554019, 0.2911347198, 3, 379},
    {"Co",       11.604, 2.286, 0.0950,    1.4880,    2, 200},
};

double eval_energy_grad(const double* x, int N, const GuptaParams& P, double* g) {
    if (g) std::fill(g, g + 3 * N, 0.0);
    std::vector<double> rho(N, 0.0);

    for (int i = 0; i < N; ++i) {
        const double xi = x[3 * i], yi = x[3 * i + 1], zi = x[3 * i + 2];
        for (int j = i + 1; j < N; ++j) {
            double dx = xi - x[3 * j];
            double dy = yi - x[3 * j + 1];
            double dz = zi - x[3 * j + 2];
            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (r < 0.35) r = 0.35;
            double e2q = std::exp(-2.0 * P.q * (r - 1.0));
            rho[i] += e2q;
            rho[j] += e2q;
        }
    }

    double E_emb = 0.0;
    std::vector<double> inv_sqrt_rho(N, 0.0);
    for (int i = 0; i < N; ++i) {
        if (rho[i] > 1e-30) {
            double sr = std::sqrt(rho[i]);
            E_emb -= P.xi * sr;
            inv_sqrt_rho[i] = 1.0 / sr;
        }
    }

    double E_pair = 0.0;
    for (int i = 0; i < N; ++i) {
        const double xi = x[3 * i], yi = x[3 * i + 1], zi = x[3 * i + 2];
        for (int j = i + 1; j < N; ++j) {
            double dx = xi - x[3 * j];
            double dy = yi - x[3 * j + 1];
            double dz = zi - x[3 * j + 2];
            double r2 = dx * dx + dy * dy + dz * dz;
            if (r2 < 0.35 * 0.35) r2 = 0.35 * 0.35;
            double r = std::sqrt(r2);
            double u = r - 1.0;
            double ep = std::exp(-P.p * u);
            double e2q = std::exp(-2.0 * P.q * u);
            E_pair += 2.0 * P.A * ep;
            if (g) {
                double dEdr = -2.0 * P.A * P.p * ep + P.xi * P.q * (inv_sqrt_rho[i] + inv_sqrt_rho[j]) * e2q;
                double fac = dEdr / r;
                g[3 * i]     += fac * dx;
                g[3 * i + 1] += fac * dy;
                g[3 * i + 2] += fac * dz;
                g[3 * j]     -= fac * dx;
                g[3 * j + 1] -= fac * dy;
                g[3 * j + 2] -= fac * dz;
            }
        }
    }
    return E_pair + E_emb;
}

void compute_atom_energies(const std::vector<double>& x, int N, const GuptaParams& P, std::vector<double>& e_atom) {
    e_atom.assign(N, 0.0);
    std::vector<double> rho(N, 0.0);
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = x[3 * i] - x[3 * j];
            double dy = x[3 * i + 1] - x[3 * j + 1];
            double dz = x[3 * i + 2] - x[3 * j + 2];
            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            double u = r - 1.0;
            double ep = P.A * std::exp(-P.p * u);
            double e2q = std::exp(-2.0 * P.q * u);
            e_atom[i] += ep;
            e_atom[j] += ep;
            rho[i] += e2q;
            rho[j] += e2q;
        }
    }
    for (int i = 0; i < N; ++i) {
        if (rho[i] > 0.0) e_atom[i] -= P.xi * std::sqrt(rho[i]);
    }
}

double lbfgs_minimize(std::vector<double>& x, int N, const GuptaParams& P, int max_iter = 2000, double gtol = 1e-12) {
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
        double step = (dnorm > 0.15) ? (0.15 / dnorm) : 1.0;

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

void run_tournament(std::vector<std::vector<double>>& cands, int n, const GuptaParams& M,
                    double& cand_best_e, std::vector<double>& cand_best_x, int top_k = 6) {
    int C = (int)cands.size();
    if (C == 0) return;
    std::vector<double> coarse_e(C, 1e30);
    parallel_for(C, [&](int i) {
        coarse_e[i] = lbfgs_minimize(cands[i], n, M, 150, 1e-5);
    });
    std::vector<int> idx(C);
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return coarse_e[a] < coarse_e[b]; });
    int K = std::min(C, top_k);
    std::mutex mtx;
    parallel_for(K, [&](int k) {
        int i = idx[k];
        double e = lbfgs_minimize(cands[i], n, M, 2000, 1e-12);
        if (e < cand_best_e - 1e-7) {
            std::lock_guard<std::mutex> lk(mtx);
            if (e < cand_best_e - 1e-7) {
                cand_best_e = e;
                cand_best_x = cands[i];
            }
        }
    });
}

void save_xyz(const std::string& metal, int n, const std::vector<double>& x) {
    std::string out_path = "./ccd_gupta/wins/" + metal + "_" + std::to_string(n) + ".xyz";
    std::ofstream out(out_path);
    out << std::setprecision(17);
    for (int i = 0; i < n; ++i) {
        out << x[3 * i] << " " << x[3 * i + 1] << " " << x[3 * i + 2] << "\n";
    }
}

std::vector<double> load_coords(const std::string& path, bool rescale_nn = false) {
    std::ifstream in(path);
    std::vector<double> c;
    std::string line;
    while (std::getline(in, line)) {
        if (line.find('=') != std::string::npos) continue;
        std::istringstream iss(line);
        double x, y, z;
        if (iss >> x >> y >> z) {
            c.push_back(x); c.push_back(y); c.push_back(z);
        }
    }
    int N = (int)c.size() / 3;
    if (rescale_nn && N >= 2) {
        double sum_nn = 0.0;
        for (int i = 0; i < N; ++i) {
            double best_r = 1e30;
            for (int j = 0; j < N; ++j) {
                if (i == j) continue;
                double dx = c[3 * i] - c[3 * j];
                double dy = c[3 * i + 1] - c[3 * j + 1];
                double dz = c[3 * i + 2] - c[3 * j + 2];
                double r = std::sqrt(dx * dx + dy * dy + dz * dz);
                if (r < best_r) best_r = r;
            }
            sum_nn += best_r;
        }
        double avg_nn = sum_nn / N;
        if (avg_nn > 0.1) {
            for (double& v : c) v /= avg_nn;
        }
    }
    return c;
}

std::map<int, double> parse_html_table(const std::string& path) {
    std::ifstream in(path);
    std::string txt((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    std::map<int, double> res;
    std::regex re("points/(\\d+)[^>]*>\\s*\\d+\\s*</[aA]>[^-]*(-?\\d+\\.\\d+)");
    auto begin = std::sregex_iterator(txt.begin(), txt.end(), re);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; ++it) {
        int n = std::stoi((*it)[1].str());
        double e = std::stod((*it)[2].str());
        res[n] = e;
    }
    return res;
}

void generate_hollow_sites(const std::vector<double>& x, int N, std::vector<double>& sites) {
    sites.clear();
    double cx = 0.0, cy = 0.0, cz = 0.0;
    for (int i = 0; i < N; ++i) {
        cx += x[3 * i]; cy += x[3 * i + 1]; cz += x[3 * i + 2];
    }
    cx /= N; cy /= N; cz /= N;

    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dxij = x[3 * i] - x[3 * j], dyij = x[3 * i + 1] - x[3 * j + 1], dzij = x[3 * i + 2] - x[3 * j + 2];
            double rij2 = dxij * dxij + dyij * dyij + dzij * dzij;
            if (rij2 > 1.38 * 1.38) continue;
            for (int k = j + 1; k < N; ++k) {
                double dxik = x[3 * i] - x[3 * k], dyik = x[3 * i + 1] - x[3 * k + 1], dzik = x[3 * i + 2] - x[3 * k + 2];
                if (dxik * dxik + dyik * dyik + dzik * dzik > 1.38 * 1.38) continue;
                double dxjk = x[3 * j] - x[3 * k], dyjk = x[3 * j + 1] - x[3 * k + 1], dzjk = x[3 * j + 2] - x[3 * k + 2];
                if (dxjk * dxjk + dyjk * dyjk + dzjk * dzjk > 1.38 * 1.38) continue;

                double mx = (x[3 * i] + x[3 * j] + x[3 * k]) / 3.0;
                double my = (x[3 * i + 1] + x[3 * j + 1] + x[3 * k + 1]) / 3.0;
                double mz = (x[3 * i + 2] + x[3 * j + 2] + x[3 * k + 2]) / 3.0;

                double ux = x[3 * j] - x[3 * i], uy = x[3 * j + 1] - x[3 * i + 1], uz = x[3 * j + 2] - x[3 * i + 2];
                double vx = x[3 * k] - x[3 * i], vy = x[3 * k + 1] - x[3 * i + 1], vz = x[3 * k + 2] - x[3 * k + 2];
                double nx = uy * vz - uz * vy;
                double ny = uz * vx - ux * vz;
                double nz = ux * vy - uy * vx;
                double nn = std::sqrt(nx * nx + ny * ny + nz * nz);
                if (nn < 1e-8) continue;
                nx /= nn; ny /= nn; nz /= nn;
                if (nx * (mx - cx) + ny * (my - cy) + nz * (mz - cz) < 0.0) {
                    nx = -nx; ny = -ny; nz = -nz;
                }
                double px = mx + 0.80 * nx;
                double py = my + 0.80 * ny;
                double pz = mz + 0.80 * nz;

                bool clash = false;
                for (int m = 0; m < N; ++m) {
                    double dx = px - x[3 * m], dy = py - x[3 * m + 1], dz = pz - x[3 * m + 2];
                    if (dx * dx + dy * dy + dz * dz < 0.68 * 0.68) {
                        clash = true;
                        break;
                    }
                }
                if (clash) continue;
                bool dup = false;
                for (size_t s = 0; s < sites.size() / 3; ++s) {
                    double dx = px - sites[3 * s], dy = py - sites[3 * s + 1], dz = pz - sites[3 * s + 2];
                    if (dx * dx + dy * dy + dz * dz < 0.35 * 0.35) {
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

int main(int argc, char** argv) {
    std::string filter_metal = (argc > 1) ? argv[1] : "";
    fs::create_directories("./ccd_gupta/wins");

    std::map<int, std::vector<std::pair<std::string, std::vector<double>>>> seed_lib;
    auto add_seed = [&](int N, const std::string& tag, const std::vector<double>& c) {
        if ((int)c.size() == 3 * N) {
            seed_lib[N].push_back({tag, c});
        }
    };

    for (int n = 2; n <= 200; ++n) {
        std::string p = "./ccd_cobalt/co_pts/points/" + std::to_string(n);
        if (fs::exists(p)) add_seed(n, "Co_tab", load_coords(p));
        std::string pz = "./ccd_cobalt/co_zip_pts/Co/Co" + std::to_string(n) + ".txt";
        if (fs::exists(pz)) add_seed(n, "Co_zip", load_coords(pz));
    }
    for (int n = 3; n <= 125; ++n) {
        std::string p1 = "./ccd_gupta/zn_pts/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Zn_tab", load_coords(p1));
        std::string p2 = "./ccd_gupta/cd_pts/" + std::to_string(n);
        if (fs::exists(p2)) add_seed(n, "Cd_tab", load_coords(p2));
    }
    for (int n = 3; n <= 150; ++n) {
        std::string p1 = "./ccd_gupta/pb_pts/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Pb_tab", load_coords(p1));
        std::string p2 = "./ccd_gupta/pb_lai_pts/Pb_Gupta/Pb" + std::to_string(n) + ".txt";
        if (fs::exists(p2)) add_seed(n, "Pb_lai", load_coords(p2));
    }
    for (int n = 3; n <= 379; ++n) {
        std::string p1 = "./ccd_gupta/na_gupta_pts/all/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Na_Gupta", load_coords(p1));
    }
    for (int n = 10; n <= 380; ++n) {
        std::string p1 = "./ccd_gupta/na_mm_pts/all/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Na_MM", load_coords(p1, true));
    }
    for (int n = 141; n <= 310; ++n) {
        std::string p1 = "./ccd_gupta/ag_pts/Gupta_Ag141-Ag310/Ag" + std::to_string(n) + ".txt";
        if (fs::exists(p1)) add_seed(n, "Ag_lai", load_coords(p1));
    }
    for (int n = 3; n <= 100; ++n) {
        std::string p1 = "./ccd_fs/mo_pts/" + std::to_string(n);
        if (fs::exists(p1)) add_seed(n, "Mo_FS", load_coords(p1, true));
        std::string p2 = "./ccd_fs/fe_pts/" + std::to_string(n);
        if (fs::exists(p2)) add_seed(n, "Fe_FS", load_coords(p2, true));
    }
    if (fs::exists("./ccd_gupta/wins/Zn_106.xyz")) {
        add_seed(106, "Zn_win", load_coords("./ccd_gupta/wins/Zn_106.xyz"));
    }

    std::map<std::string, std::map<int, double>> ref_energy;
    ref_energy["Co"] = parse_html_table("./ccd_cobalt/cobalt.html");
    std::map<int, double> co_zip_e = {
        {84, -315.648487}, {95, -359.863606}, {101, -384.329400}, {113, -432.488220},
        {121, -464.596853}, {122, -468.804546}, {196, -770.572025}, {197, -774.347649},
        {198, -778.402743}, {200, -786.638464}
    };
    for (auto& kv : co_zip_e) {
        if (kv.second < ref_energy["Co"][kv.first]) ref_energy["Co"][kv.first] = kv.second;
    }

    ref_energy["Zn"] = parse_html_table("./ccd_gupta/zn_table.html");
    ref_energy["Cd"] = parse_html_table("./ccd_gupta/cd_table.html");
    ref_energy["Pb"] = parse_html_table("./ccd_gupta/pb_table.html");
    std::map<int, double> pb_lai_e = {
        {83, -155.743751}, {85, -159.562232}, {93, -175.01790977}, {96, -180.777375},
        {106, -200.24125822}, {109, -206.076441}, {119, -225.52796368}, {123, -233.32709026}, {142, -270.26251303}
    };
    for (auto& kv : pb_lai_e) {
        if (kv.second < ref_energy["Pb"][kv.first]) ref_energy["Pb"][kv.first] = kv.second;
    }
    ref_energy["Na_Gupta"] = parse_html_table("./ccd_gupta/na_gupta_table.html");

    std::mutex print_mtx;

    for (const auto& M : METALS) {
        if (!filter_metal.empty() && M.name != filter_metal) continue;
        std::cout << "\n======================================================\n";
        std::cout << "HUNTING METAL: " << M.name << " (N = " << M.min_N << ".." << M.max_N << ")\n";
        std::cout << "======================================================\n";

        std::vector<std::vector<double>> best_x(M.max_N + 1);
        std::vector<double> best_e(M.max_N + 1, 1e30);
        std::vector<double> posted_pol_e(M.max_N + 1, 1e30);

        int count_N = M.max_N - M.min_N + 1;
        parallel_for(count_N, [&](int idx) {
            int n = M.min_N + idx;
            double best_own = 1e30;
            for (const auto& item : seed_lib[n]) {
                bool is_own = (item.first.rfind(M.name.substr(0, 2), 0) == 0 && item.first.find("_win") == std::string::npos);
                if (is_own) {
                    std::vector<double> c = item.second;
                    double e = lbfgs_minimize(c, n, M, 2000, 1e-12);
                    if (e < best_own) best_own = e;
                    if (e < best_e[n]) {
                        best_e[n] = e;
                        best_x[n] = c;
                    }
                }
            }
            posted_pol_e[n] = best_own;
            // Screen cross-potential seeds
            std::vector<std::vector<double>> cross_cands;
            for (const auto& item : seed_lib[n]) {
                bool is_own = (item.first.rfind(M.name.substr(0, 2), 0) == 0 && item.first.find("_win") == std::string::npos);
                if (!is_own) cross_cands.push_back(item.second);
            }
            for (auto& c : cross_cands) {
                double ec = lbfgs_minimize(c, n, M, 180, 1e-5);
                if (ec < best_e[n] + 0.05) {
                    double ef = lbfgs_minimize(c, n, M, 2000, 1e-12);
                    if (ef < best_e[n]) {
                        best_e[n] = ef;
                        best_x[n] = c;
                    }
                }
            }
            double ref = ref_energy[M.name][n];
            double bar = std::min(ref, posted_pol_e[n]);
            if (best_e[n] < bar - 1e-4) {
                std::lock_guard<std::mutex> lk(print_mtx);
                save_xyz(M.name, n, best_x[n]);
                std::printf("  [CROSS-SEED WIN] %s_%d: E* = %.10f vs ref %.10f (pol_own %.10f, diff = %+.6f eV)\n",
                            M.name.c_str(), n, best_e[n], ref, posted_pol_e[n], best_e[n] - bar);
                std::fflush(stdout);
            }
        });

        // Bidirectional Top-6 Tournament Cascade
        for (int pass = 0; pass < 2; ++pass) {
            int improved = 0;
            // 1. Downward pass: N = max_N - 1 down to min_N
            for (int n = M.max_N - 1; n >= M.min_N; --n) {
                if (best_x[n + 1].empty()) continue;
                const std::vector<double>& xp1 = best_x[n + 1];
                std::vector<std::vector<double>> cands;

                // Top 36 1-atom removals ranked by atom energy
                std::vector<double> ea1;
                compute_atom_energies(xp1, n + 1, M, ea1);
                std::vector<int> ord1(n + 1);
                std::iota(ord1.begin(), ord1.end(), 0);
                std::sort(ord1.begin(), ord1.end(), [&](int a, int b) { return ea1[a] > ea1[b]; });
                int K1 = std::min(n + 1, 36);
                for (int k = 0; k < K1; ++k) {
                    int rm = ord1[k];
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

                // Top 36 2-atom removals from N+2 (top 9 highest-energy atoms)
                if (n + 2 <= M.max_N && !best_x[n + 2].empty()) {
                    const std::vector<double>& xp2 = best_x[n + 2];
                    std::vector<double> ea2;
                    compute_atom_energies(xp2, n + 2, M, ea2);
                    std::vector<int> ord2(n + 2);
                    std::iota(ord2.begin(), ord2.end(), 0);
                    std::sort(ord2.begin(), ord2.end(), [&](int a, int b) { return ea2[a] > ea2[b]; });
                    int K2 = std::min(n + 2, 9);
                    for (int a = 0; a < K2; ++a) {
                        for (int b = a + 1; b < K2; ++b) {
                            int r1 = ord2[a], r2 = ord2[b];
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
                run_tournament(cands, n, M, cand_best_e, cand_best_x, 6);

                if (!cand_best_x.empty() && cand_best_e < best_e[n] - 1e-6) {
                    best_e[n] = cand_best_e;
                    best_x[n] = cand_best_x;
                    improved++;
                    double ref = ref_energy[M.name][n];
                    double bar = std::min(ref, posted_pol_e[n]);
                    if (best_e[n] < bar - 1e-4) {
                        save_xyz(M.name, n, best_x[n]);
                        seed_lib[n].push_back({M.name + "_win", best_x[n]});
                        std::printf("  [DOWNWARD WIN] %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f eV)\n",
                                    M.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                        std::fflush(stdout);
                    }
                }
            }

            // 2. Upward pass: N = min_N + 1 up to max_N
            for (int n = M.min_N + 1; n <= M.max_N; ++n) {
                if (best_x[n - 1].empty()) continue;
                const std::vector<double>& xm1 = best_x[n - 1];
                std::vector<double> sites;
                generate_hollow_sites(xm1, n - 1, sites);
                int num_sites = (int)sites.size() / 3;
                if (num_sites == 0) continue;

                std::vector<std::pair<double, int>> site_order;
                for (int s = 0; s < num_sites; ++s) {
                    std::vector<double> c = xm1;
                    c.push_back(sites[3 * s]);
                    c.push_back(sites[3 * s + 1]);
                    c.push_back(sites[3 * s + 2]);
                    double e0 = eval_energy_grad(c.data(), n, M, nullptr);
                    site_order.push_back({e0, s});
                }
                std::sort(site_order.begin(), site_order.end());
                int S_try = std::min((int)site_order.size(), 28);

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
                run_tournament(cands, n, M, cand_best_e, cand_best_x, 6);

                if (!cand_best_x.empty() && cand_best_e < best_e[n] - 1e-6) {
                    best_e[n] = cand_best_e;
                    best_x[n] = cand_best_x;
                    improved++;
                    double ref = ref_energy[M.name][n];
                    double bar = std::min(ref, posted_pol_e[n]);
                    if (best_e[n] < bar - 1e-4) {
                        save_xyz(M.name, n, best_x[n]);
                        seed_lib[n].push_back({M.name + "_win", best_x[n]});
                        std::printf("  [UPWARD WIN]   %s_%d: E* = %.10f vs bar %.10f (diff = %+.6f eV)\n",
                                    M.name.c_str(), n, best_e[n], bar, best_e[n] - bar);
                        std::fflush(stdout);
                    }
                }
            }
            if (improved == 0) break;
        }

        int win_count = 0;
        for (int n = M.min_N; n <= M.max_N; ++n) {
            double ref = ref_energy[M.name][n];
            double bar = std::min(ref, posted_pol_e[n]);
            if (best_e[n] < bar - 1e-4) {
                win_count++;
                save_xyz(M.name, n, best_x[n]);
                std::printf("FINAL WIN %s_%d: E* = %.10f | ref = %.10f | pol_own = %.10f | dE = %+.6f eV\n",
                            M.name.c_str(), n, best_e[n], ref, posted_pol_e[n], best_e[n] - bar);
            }
        }
        std::printf("=== %s SUMMARY: %d NEW GLOBAL MINIMA DISCOVERED ===\n", M.name.c_str(), win_count);
        std::fflush(stdout);
    }
    return 0;
}
