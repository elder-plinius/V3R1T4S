#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <random>
#include <thread>
#include <mutex>
#include <dirent.h>

// Exact Cu-Ag Gupta parameters (Nunez & Johnston 2010 / Rapallo et al. 2005 / CuAg_55.rar reference.txt)
// Type 0 = Cu-Cu, Type 1 = Cu-Ag, Type 2 = Ag-Ag
static const double A_P[3]  = {0.0894, 0.0980, 0.1031};
static const double XI_P[3] = {1.2799, 1.2274, 1.1895};
static const double P_P[3]  = {10.550, 10.700, 10.850};
static const double Q_P[3]  = {2.430,  2.805,  3.180};
static const double R0_P[3] = {2.556,  2.72405, 2.8921};

struct Cluster {
    int n_cu;
    double e_hdr;
    double e_best;
    std::vector<int> sp;
    std::vector<double> x; // 3*55 = 165
};

double eval_energy_only(const std::vector<double>& x, const std::vector<int>& sp) {
    const int n = 55;
    double rho[55] = {0.0};
    double e_rep = 0.0;
    for (int i = 0; i < n; ++i) {
        double xi = x[3*i], yi = x[3*i+1], zi = x[3*i+2];
        int si = sp[i];
        for (int j = i + 1; j < n; ++j) {
            double dx = xi - x[3*j];
            double dy = yi - x[3*j+1];
            double dz = zi - x[3*j+2];
            double r = std::sqrt(dx*dx + dy*dy + dz*dz);
            int t = si + sp[j];
            double u = r / R0_P[t] - 1.0;
            double rep = A_P[t] * std::exp(-P_P[t] * u);
            double phi = (XI_P[t] * XI_P[t]) * std::exp(-2.0 * Q_P[t] * u);
            e_rep += 2.0 * rep;
            rho[i] += phi;
            rho[j] += phi;
        }
    }
    double e_att = 0.0;
    for (int i = 0; i < n; ++i) e_att += std::sqrt(rho[i]);
    return e_rep - e_att;
}

double eval_eg(const std::vector<double>& x, const std::vector<int>& sp, std::vector<double>& g) {
    const int n = 55;
    g.assign(3*n, 0.0);
    double rho[55] = {0.0};
    double inv_sr[55] = {0.0};
    double r_mat[55][55];
    double rep_mat[55][55];
    double phi_mat[55][55];
    double e_rep = 0.0;
    for (int i = 0; i < n; ++i) {
        double xi = x[3*i], yi = x[3*i+1], zi = x[3*i+2];
        int si = sp[i];
        for (int j = i + 1; j < n; ++j) {
            double dx = xi - x[3*j];
            double dy = yi - x[3*j+1];
            double dz = zi - x[3*j+2];
            double r = std::sqrt(dx*dx + dy*dy + dz*dz);
            r_mat[i][j] = r;
            int t = si + sp[j];
            double u = r / R0_P[t] - 1.0;
            double rep = A_P[t] * std::exp(-P_P[t] * u);
            double phi = (XI_P[t] * XI_P[t]) * std::exp(-2.0 * Q_P[t] * u);
            rep_mat[i][j] = rep;
            phi_mat[i][j] = phi;
            e_rep += 2.0 * rep;
            rho[i] += phi;
            rho[j] += phi;
        }
    }
    double e_att = 0.0;
    for (int i = 0; i < n; ++i) {
        double sr = std::sqrt(rho[i]);
        e_att += sr;
        inv_sr[i] = 1.0 / sr;
    }
    for (int i = 0; i < n; ++i) {
        int si = sp[i];
        for (int j = i + 1; j < n; ++j) {
            int t = si + sp[j];
            double r = r_mat[i][j];
            double dE_dr = 2.0 * ((-P_P[t] / R0_P[t]) * rep_mat[i][j] + 0.5 * (inv_sr[i] + inv_sr[j]) * (Q_P[t] / R0_P[t]) * phi_mat[i][j]);
            double c = dE_dr / r;
            double dx = x[3*i] - x[3*j];
            double dy = x[3*i+1] - x[3*j+1];
            double dz = x[3*i+2] - x[3*j+2];
            g[3*i]   += c*dx; g[3*j]   -= c*dx;
            g[3*i+1] += c*dy; g[3*j+1] -= c*dy;
            g[3*i+2] += c*dz; g[3*j+2] -= c*dz;
        }
    }
    return e_rep - e_att;
}

double lbfgs_relax(std::vector<double>& x, const std::vector<int>& sp, int max_iter = 400) {
    const int d = 165;
    const int m = 8;
    std::vector<double> g(d), x_old(d), g_old(d), q(d), dir(d);
    std::vector<std::vector<double>> s_hist(m, std::vector<double>(d));
    std::vector<std::vector<double>> y_hist(m, std::vector<double>(d));
    std::vector<double> rho_hist(m), alpha(m);
    double f = eval_eg(x, sp, g);
    int h_cnt = 0;
    for (int it = 0; it < max_iter; ++it) {
        double gnorm = 0.0;
        for (double v : g) gnorm += v*v;
        gnorm = std::sqrt(gnorm);
        if (gnorm < 1e-11) break;
        q = g;
        int bound = std::min(h_cnt, m);
        for (int i = bound - 1; i >= 0; --i) {
            int idx = (h_cnt - 1 - (bound - 1 - i)) % m;
            double dot = 0.0;
            for (int k = 0; k < d; ++k) dot += s_hist[idx][k] * q[k];
            alpha[i] = rho_hist[idx] * dot;
            for (int k = 0; k < d; ++k) q[k] -= alpha[i] * y_hist[idx][k];
        }
        double gamma = 1.0;
        if (h_cnt > 0) {
            int last = (h_cnt - 1) % m;
            double sy = 0.0, yy = 0.0;
            for (int k = 0; k < d; ++k) {
                sy += s_hist[last][k] * y_hist[last][k];
                yy += y_hist[last][k] * y_hist[last][k];
            }
            if (yy > 1e-30) gamma = sy / yy;
        }
        for (int k = 0; k < d; ++k) dir[k] = gamma * q[k];
        for (int i = 0; i < bound; ++i) {
            int idx = (h_cnt - bound + i) % m;
            double dot = 0.0;
            for (int k = 0; k < d; ++k) dot += y_hist[idx][k] * dir[k];
            double beta = rho_hist[idx] * dot;
            for (int k = 0; k < d; ++k) dir[k] += s_hist[idx][k] * (alpha[i] - beta);
        }
        for (int k = 0; k < d; ++k) dir[k] = -dir[k];
        double dg = 0.0;
        for (int k = 0; k < d; ++k) dg += dir[k] * g[k];
        if (dg >= 0.0) {
            for (int k = 0; k < d; ++k) dir[k] = -g[k];
            dg = -gnorm * gnorm;
            h_cnt = 0;
        }
        x_old = x; g_old = g;
        double f_old = f;
        double step = (it == 0 && h_cnt == 0) ? std::min(1.0, 0.1 / gnorm) : 1.0;
        bool ok = false;
        for (int ls = 0; ls < 20; ++ls) {
            for (int k = 0; k < d; ++k) x[k] = x_old[k] + step * dir[k];
            f = eval_eg(x, sp, g);
            if (f <= f_old + 1e-4 * step * dg) { ok = true; break; }
            step *= 0.5;
        }
        if (!ok) { x = x_old; f = f_old; g = g_old; break; }
        int slot = h_cnt % m;
        double sy = 0.0;
        for (int k = 0; k < d; ++k) {
            s_hist[slot][k] = x[k] - x_old[k];
            y_hist[slot][k] = g[k] - g_old[k];
            sy += s_hist[slot][k] * y_hist[slot][k];
        }
        if (sy > 1e-28) {
            rho_hist[slot] = 1.0 / sy;
            h_cnt++;
        }
    }
    return f;
}

// Fast exact swap search on fixed geometry x:
void greedy_homotop_on_fixed_geom(const std::vector<double>& x, std::vector<int>& sp) {
    const int n = 55;
    int n_cu = 0;
    for (int s : sp) if (s == 0) n_cu++;
    if (n_cu == 0 || n_cu == 55) return;
    double r_mat[55][55];
    double rep_t[3][55][55], phi_t[3][55][55];
    for (int i = 0; i < n; ++i) {
        rep_t[0][i][i] = rep_t[1][i][i] = rep_t[2][i][i] = 0.0;
        phi_t[0][i][i] = phi_t[1][i][i] = phi_t[2][i][i] = 0.0;
        for (int j = i + 1; j < n; ++j) {
            double dx = x[3*i] - x[3*j], dy = x[3*i+1] - x[3*j+1], dz = x[3*i+2] - x[3*j+2];
            double r = std::sqrt(dx*dx + dy*dy + dz*dz);
            r_mat[i][j] = r_mat[j][i] = r;
            for (int t = 0; t < 3; ++t) {
                double u = r / R0_P[t] - 1.0;
                rep_t[t][i][j] = rep_t[t][j][i] = A_P[t] * std::exp(-P_P[t] * u);
                phi_t[t][i][j] = phi_t[t][j][i] = (XI_P[t]*XI_P[t]) * std::exp(-2.0 * Q_P[t] * u);
            }
        }
    }
    auto eval_fast = [&](const std::vector<int>& s) {
        double e_rep = 0.0, e_att = 0.0;
        for (int i = 0; i < n; ++i) {
            double rho = 0.0;
            int si = s[i];
            for (int j = 0; j < n; ++j) {
                if (i == j) continue;
                int t = si + s[j];
                e_rep += rep_t[t][i][j];
                rho += phi_t[t][i][j];
            }
            e_att += std::sqrt(rho);
        }
        return e_rep - e_att;
    };
    double best_e = eval_fast(sp);
    while (true) {
        int bi = -1, bj = -1;
        for (int i = 0; i < n; ++i) {
            if (sp[i] != 0) continue;
            for (int j = 0; j < n; ++j) {
                if (sp[j] != 1) continue;
                std::swap(sp[i], sp[j]);
                double e = eval_fast(sp);
                if (e < best_e - 1e-11) {
                    best_e = e; bi = i; bj = j;
                }
                std::swap(sp[i], sp[j]);
            }
        }
        if (bi != -1) {
            std::swap(sp[bi], sp[bj]);
        } else {
            break;
        }
    }
}

int main() {
    std::string arch_dir = "CuAg55";
    std::string imp_dir  = "bingupta_improved";
    std::vector<Cluster> clusters(56);
    for (int k = 0; k <= 55; ++k) {
        std::string fn = arch_dir + "/Cu" + std::to_string(k) + "Ag" + std::to_string(55 - k) + ".txt";
        std::ifstream f(fn);
        std::string line;
        std::getline(f, line);
        double eh = 0.0;
        std::stringstream ss(line);
        std::string tok;
        while (ss >> tok) {
            if (tok.rfind("E=", 0) == 0) eh = std::stod(tok.substr(2));
        }
        std::vector<int> sp;
        std::vector<double> x;
        while (std::getline(f, line)) {
            if (line.empty() || line.find("type") != std::string::npos) continue;
            std::stringstream ls(line);
            int s; double cx, cy, cz;
            if (ls >> s >> cx >> cy >> cz) {
                sp.push_back(s);
                x.push_back(cx); x.push_back(cy); x.push_back(cz);
            }
        }
        clusters[k].n_cu = k;
        clusters[k].e_hdr = eh;
        clusters[k].sp = sp;
        clusters[k].x = x;
        clusters[k].e_best = eval_energy_only(x, sp);
        // Check if we already have an improved file in imp_dir
        std::string ifn = imp_dir + "/CuAg55_Cu" + std::to_string(k) + "Ag" + std::to_string(55 - k) + ".txt";
        std::ifstream ifile(ifn);
        if (ifile.good()) {
            std::vector<int> isp;
            std::vector<double> ix;
            while (std::getline(ifile, line)) {
                std::stringstream ls(line);
                int s; double cx, cy, cz;
                if (ls >> s >> cx >> cy >> cz) {
                    isp.push_back(s);
                    ix.push_back(cx); ix.push_back(cy); ix.push_back(cz);
                }
            }
            if (isp.size() == 55) {
                double ie = lbfgs_relax(ix, isp, 600);
                if (ie < clusters[k].e_best - 1e-6) {
                    clusters[k].e_best = ie;
                    clusters[k].sp = isp;
                    clusters[k].x = ix;
                }
            }
        }
    }

    // Collect all geometry templates (all 56 archive + current bests + CuAu55 + AgAu55 rescaled)
    std::vector<std::vector<double>> templates;
    for (int k = 0; k <= 55; ++k) templates.push_back(clusters[k].x);

    // Phase 1: Test every template on every composition k = 1..54 with radial core-shell initial assignment + greedy swap + L-BFGS + greedy swap + L-BFGS
    std::mutex mtx;
    auto worker = [&](int tid) {
        std::mt19937 rng(12345 + tid * 997);
        for (int k = 1 + tid; k <= 54; k += 8) {
            double best_e = clusters[k].e_best;
            std::vector<int> best_sp = clusters[k].sp;
            std::vector<double> best_x = clusters[k].x;

            // Try all 56 templates + perturbed variants
            for (size_t t = 0; t < templates.size(); ++t) {
                std::vector<double> x = templates[t];
                // Compute center of mass and radial distances
                double cmx = 0, cmy = 0, cmz = 0;
                for (int i = 0; i < 55; ++i) { cmx += x[3*i]; cmy += x[3*i+1]; cmz += x[3*i+2]; }
                cmx /= 55.0; cmy /= 55.0; cmz /= 55.0;
                std::vector<std::pair<double, int>> rad(55);
                for (int i = 0; i < 55; ++i) {
                    double dx = x[3*i]-cmx, dy = x[3*i+1]-cmy, dz = x[3*i+2]-cmz;
                    rad[i] = {dx*dx + dy*dy + dz*dz, i};
                }
                std::sort(rad.begin(), rad.end());
                std::vector<int> sp(55, 1);
                for (int i = 0; i < k; ++i) sp[rad[i].second] = 0;

                greedy_homotop_on_fixed_geom(x, sp);
                double e = lbfgs_relax(x, sp, 300);
                greedy_homotop_on_fixed_geom(x, sp);
                e = lbfgs_relax(x, sp, 500);
                if (e < best_e - 1e-6) {
                    best_e = e; best_sp = sp; best_x = x;
                }

                // Also try 3 random homotop + swap starts on the best template if close
                if (e < best_e + 0.35) {
                    for (int r = 0; r < 4; ++r) {
                        std::vector<double> xr = best_x;
                        std::vector<int> spr = best_sp;
                        // Swap 2 random Cu/Ag pairs and perturb coordinates slightly
                        std::normal_distribution<double> nd(0.0, 0.08);
                        for (double& v : xr) v += nd(rng);
                        greedy_homotop_on_fixed_geom(xr, spr);
                        double er = lbfgs_relax(xr, spr, 300);
                        greedy_homotop_on_fixed_geom(xr, spr);
                        er = lbfgs_relax(xr, spr, 500);
                        if (er < best_e - 1e-6) {
                            best_e = er; best_sp = spr; best_x = xr;
                        }
                    }
                }
            }

            if (best_e < clusters[k].e_hdr - 1e-4) {
                std::lock_guard<std::mutex> lk(mtx);
                clusters[k].e_best = best_e;
                clusters[k].sp = best_sp;
                clusters[k].x = best_x;
                std::cout << "IMPROVED Cu" << k << "Ag" << (55-k)
                          << " | E_hdr=" << std::fixed << std::setprecision(8) << clusters[k].e_hdr
                          << " -> E_new=" << best_e
                          << " | dE=" << (best_e - clusters[k].e_hdr) << std::endl;
                std::string ofn = imp_dir + "/CuAg55_Cu" + std::to_string(k) + "Ag" + std::to_string(55 - k) + ".txt";
                std::ofstream out(ofn);
                out << std::fixed << std::setprecision(10);
                for (int i = 0; i < 55; ++i) {
                    out << best_sp[i] << " " << best_x[3*i] << " " << best_x[3*i+1] << " " << best_x[3*i+2] << "\n";
                }
            }
        }
    };

    std::vector<std::thread> threads;
    for (int t = 0; t < 8; ++t) threads.emplace_back(worker, t);
    for (auto& th : threads) th.join();
    return 0;
}
