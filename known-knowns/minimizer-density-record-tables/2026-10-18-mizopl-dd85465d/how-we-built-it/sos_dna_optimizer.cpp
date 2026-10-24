#include <iostream>
#include <vector>
#include <cstdint>
#include <fstream>
#include <algorithm>
#include <numeric>
#include <random>
#include <chrono>
#include <iomanip>
#include <cmath>
#include <string>

// Load and save .gm binary files (exact format of OrensteinLab/GreedyMini and 10-minimizers)
std::vector<uint64_t> load_gm(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Cannot open " + filename);
    }
    size_t size = 0;
    file.read(reinterpret_cast<char*>(&size), sizeof(size));
    std::vector<uint64_t> vec(size);
    file.read(reinterpret_cast<char*>(vec.data()), size * sizeof(uint64_t));
    return vec;
}

void save_gm(const std::string& filename, const std::vector<uint64_t>& vec) {
    std::ofstream file(filename, std::ios::binary);
    size_t size = vec.size();
    file.write(reinterpret_cast<const char*>(&size), sizeof(size));
    file.write(reinterpret_cast<const char*>(vec.data()), size * sizeof(uint64_t));
}

// Precompute SOS-DP lookup table lut[0..2^(w+1)-1] for exact secondary-bit survival count
// Matches GreedyMini/code/density_and_gc.cpp get_special_case_expected_gc bit-for-bit when 2^(w+k) <= 100,000,000
std::vector<uint64_t> build_lut_wt(uint32_t w, uint32_t k) {
    uint64_t total_seq = 1ULL << (w + k);
    uint64_t mask = (1ULL << k) - 1;
    uint64_t M = 1ULL << (w - 1);

    std::vector<uint64_t> pref_cnt(M, 0);
    std::vector<uint64_t> suff_cnt(M, 0);
    std::vector<uint64_t> both_cnt(M, 0);

    for (uint64_t seq = 0; seq < total_seq; ++seq) {
        uint64_t first_kmer = seq >> w;
        uint64_t last_kmer = seq & mask;
        uint64_t pref_ruin = 0;
        uint64_t suff_ruin = 0;
        for (uint32_t j = 1; j < w; ++j) {
            uint64_t km_j = (seq >> (w - j)) & mask;
            if (km_j < first_kmer) pref_ruin |= (1ULL << (j - 1));
            if (km_j <= last_kmer) suff_ruin |= (1ULL << (j - 1));
        }
        uint64_t both_ruin = pref_ruin & suff_ruin;
        pref_cnt[pref_ruin]++;
        suff_cnt[suff_ruin]++;
        both_cnt[both_ruin]++;
    }

    // SOS DP over submasks of {0..w-2}
    for (uint32_t bit = 0; bit < w - 1; ++bit) {
        uint64_t step = 1ULL << bit;
        for (uint64_t i = 0; i < M; i += (step << 1)) {
            for (uint64_t j = i; j < i + step; ++j) {
                pref_cnt[j + step] += pref_cnt[j];
                suff_cnt[j + step] += suff_cnt[j];
                both_cnt[j + step] += both_cnt[j];
            }
        }
    }

    std::vector<uint64_t> lut(1ULL << (w + 1), 0);
    for (uint64_t wt = 0; wt < (1ULL << (w + 1)); ++wt) {
        bool has_first = (wt & 1ULL) != 0;
        bool has_last = (wt & (1ULL << w)) != 0;
        if (!has_first && !has_last) continue;
        uint64_t mid_m = (wt >> 1) & (M - 1);
        if (mid_m == 0) {
            lut[wt] = total_seq;
        } else {
            uint64_t comp = (M - 1) ^ mid_m;
            if (has_first && has_last) lut[wt] = both_cnt[comp];
            else if (has_first) lut[wt] = pref_cnt[comp];
            else lut[wt] = suff_cnt[comp];
        }
    }
    return lut;
}

// Fast DFS evaluation of prob_gc_dna using precomputed lut
struct FastDnaEvaluator {
    uint32_t w, k;
    uint64_t n_kmers, n_kmers_mask, total_seq;
    std::vector<uint64_t> lut;

    FastDnaEvaluator(uint32_t w_, uint32_t k_)
        : w(w_), k(k_), n_kmers(1ULL << k_), n_kmers_mask((1ULL << k_) - 1),
          total_seq(1ULL << (w_ + k_)), lut(build_lut_wt(w_, k_)) {}

    uint64_t dfs(const uint64_t* order, uint64_t kmer, uint64_t min_order, uint64_t min_indices,
                 uint32_t lev, bool is_first_min, bool is_middle_min) const {
        if (lev == w) {
            uint64_t ok = order[kmer];
            if (ok < min_order) {
                return total_seq; // pure suffix GC
            }
            bool is_last_min = false;
            if (ok == min_order) {
                min_indices |= (1ULL << lev);
                is_last_min = true;
            }
            if (is_first_min || is_last_min) {
                if (is_middle_min) {
                    return lut[min_indices];
                } else {
                    return total_seq;
                }
            }
            return 0;
        } else {
            uint64_t next_kmer = (kmer << 1) & n_kmers_mask;
            uint64_t ok = order[kmer];
            if (ok < min_order) {
                uint64_t mi = (1ULL << lev);
                return dfs(order, next_kmer, ok, mi, lev + 1, false, true) +
                       dfs(order, next_kmer + 1, ok, mi, lev + 1, false, true);
            } else if (ok == min_order) {
                uint64_t mi = min_indices | (1ULL << lev);
                return dfs(order, next_kmer, min_order, mi, lev + 1, is_first_min, true) +
                       dfs(order, next_kmer + 1, min_order, mi, lev + 1, is_first_min, true);
            } else {
                return dfs(order, next_kmer, min_order, min_indices, lev + 1, is_first_min, is_middle_min) +
                       dfs(order, next_kmer + 1, min_order, min_indices, lev + 1, is_first_min, is_middle_min);
            }
        }
    }

    uint64_t eval_gc(const std::vector<uint64_t>& order) const {
        const uint64_t* ord_ptr = order.data();
        uint64_t total = 0;
        for (uint64_t pref = 0; pref < n_kmers; ++pref) {
            uint64_t next_kmer = (pref << 1) & n_kmers_mask;
            uint64_t op = ord_ptr[pref];
            total += dfs(ord_ptr, next_kmer, op, 1ULL, 1, true, false) +
                     dfs(ord_ptr, next_kmer + 1, op, 1ULL, 1, true, false);
        }
        return total;
    }

    double eval_density(const std::vector<uint64_t>& order) const {
        uint64_t gc = eval_gc(order);
        return static_cast<double>(gc) / std::ldexp(1.0, 2 * (w + k));
    }
};

std::vector<uint64_t> reverse_order(const std::vector<uint64_t>& order, uint32_t k) {
    uint64_t n = 1ULL << k;
    std::vector<uint64_t> rev(n);
    for (uint64_t x = 0; x < n; ++x) {
        uint64_t rx = 0;
        for (uint32_t b = 0; b < k; ++b) {
            if ((x >> b) & 1ULL) rx |= (1ULL << (k - 1 - b));
        }
        rev[rx] = order[x];
    }
    return rev;
}

std::vector<uint64_t> complement_order(const std::vector<uint64_t>& order, uint32_t k) {
    uint64_t n = 1ULL << k;
    uint64_t mask = n - 1;
    std::vector<uint64_t> comp(n);
    for (uint64_t x = 0; x < n; ++x) {
        comp[x ^ mask] = order[x];
    }
    return comp;
}

int main(int argc, char** argv) {
    uint32_t w = (argc > 1) ? std::stoul(argv[1]) : 12;
    uint32_t k = (argc > 2) ? std::stoul(argv[2]) : 4;
    double seconds = (argc > 3) ? std::stod(argv[3]) : 15.0;
    std::string gm_dir = "GM";

    FastDnaEvaluator evaluator(w, k);
    std::string gm_path = gm_dir + "/w" + std::to_string(w) + "_k" + std::to_string(k) + ".gm";
    std::vector<uint64_t> orig_gm = load_gm(gm_path);
    uint64_t orig_gc = evaluator.eval_gc(orig_gm);
    double orig_den = evaluator.eval_density(orig_gm);

    std::cout << std::fixed << std::setprecision(8);
    std::cout << "=== (w=" << w << ", k=" << k << ") ===" << std::endl;
    std::cout << "Published GM order GC = " << orig_gc << " / 2^" << (2*(w+k))
              << " -> density = " << orig_den << std::endl;

    uint64_t n_kmers = 1ULL << k;

    // 1. Search strict permutations of 0..2^k-1 (no ties between distinct binary k-mers!)
    // Start from several seeds: resolved orig_gm, reverse, complement, random permutations
    std::vector<uint64_t> best_perm(n_kmers);
    uint64_t best_perm_gc = UINT64_MAX;

    auto make_perm_from_order = [&](const std::vector<uint64_t>& ord, std::mt19937_64& rng) {
        std::vector<uint64_t> idx(n_kmers);
        std::iota(idx.begin(), idx.end(), 0);
        std::shuffle(idx.begin(), idx.end(), rng);
        std::stable_sort(idx.begin(), idx.end(), [&](uint64_t a, uint64_t b) {
            return ord[a] < ord[b];
        });
        std::vector<uint64_t> p(n_kmers);
        for (uint64_t r = 0; r < n_kmers; ++r) p[idx[r]] = r;
        return p;
    };

    std::mt19937_64 rng(20261018ULL + w * 100 + k);
    std::vector<std::vector<uint64_t>> starts;
    starts.push_back(make_perm_from_order(orig_gm, rng));
    starts.push_back(make_perm_from_order(reverse_order(orig_gm, k), rng));
    starts.push_back(make_perm_from_order(complement_order(orig_gm, k), rng));
    starts.push_back(make_perm_from_order(reverse_order(complement_order(orig_gm, k), k), rng));
    for (int s = 0; s < 16; ++s) {
        std::vector<uint64_t> p(n_kmers);
        std::iota(p.begin(), p.end(), 0);
        std::shuffle(p.begin(), p.end(), rng);
        starts.push_back(p);
    }

    auto t_start = std::chrono::steady_clock::now();
    uint64_t evals = 0;
    int restart_idx = 0;

    while (true) {
        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t_start).count();
        if (elapsed >= seconds * 0.6) break;

        std::vector<uint64_t> cur;
        if (restart_idx < (int)starts.size()) {
            cur = starts[restart_idx++];
        } else {
            if (restart_idx % 2 == 0) {
                cur = best_perm;
                // Perturb 2 or 3 random pairs
                for (int q = 0; q < 2; ++q) {
                    uint64_t a = rng() % n_kmers;
                    uint64_t b = rng() % n_kmers;
                    std::swap(cur[a], cur[b]);
                }
            } else {
                cur = make_perm_from_order(orig_gm, rng);
            }
            restart_idx++;
        }

        uint64_t cur_gc = evaluator.eval_gc(cur);
        evals++;

        // Steepest/first-improvement 2-opt & adjacent rank swap + insertion local search
        bool improved = true;
        while (improved) {
            improved = false;
            // Check all pairwise swaps (i, j)
            for (uint64_t i = 0; i < n_kmers; ++i) {
                for (uint64_t j = i + 1; j < n_kmers; ++j) {
                    std::swap(cur[i], cur[j]);
                    uint64_t gc = evaluator.eval_gc(cur);
                    evals++;
                    if (gc < cur_gc) {
                        cur_gc = gc;
                        improved = true;
                    } else {
                        std::swap(cur[i], cur[j]);
                    }
                }
            }
            if (!improved && n_kmers <= 64) {
                // Try rank-insertion moves (remove rank r1 and insert at r2)
                std::vector<uint64_t> inv(n_kmers);
                for (uint64_t x = 0; x < n_kmers; ++x) inv[cur[x]] = x;
                for (uint64_t r1 = 0; r1 < n_kmers && !improved; ++r1) {
                    for (uint64_t r2 = 0; r2 < n_kmers && !improved; ++r2) {
                        if (r1 == r2) continue;
                        auto inv2 = inv;
                        uint64_t val = inv2[r1];
                        inv2.erase(inv2.begin() + r1);
                        inv2.insert(inv2.begin() + r2, val);
                        std::vector<uint64_t> cand(n_kmers);
                        for (uint64_t r = 0; r < n_kmers; ++r) cand[inv2[r]] = r;
                        uint64_t gc = evaluator.eval_gc(cand);
                        evals++;
                        if (gc < cur_gc) {
                            cur = cand;
                            cur_gc = gc;
                            improved = true;
                        }
                    }
                }
            }
        }

        if (cur_gc < best_perm_gc) {
            best_perm_gc = cur_gc;
            best_perm = cur;
            double d = evaluator.eval_density(best_perm);
            double rel = (orig_den - d) / orig_den * 100.0;
            std::cout << "[StrictPerm] New best GC = " << best_perm_gc
                      << " density = " << d << " (rel = -" << std::setprecision(4) << rel << "%)"
                      << std::setprecision(8) << std::endl;
        }
    }

    // 2. Now also search general .gm orders (allowing rank ties in 0..n_kmers) starting from best_perm and orig_gm
    std::vector<uint64_t> best_any = best_perm;
    uint64_t best_any_gc = best_perm_gc;
    if (orig_gc < best_any_gc) {
        best_any = orig_gm;
        best_any_gc = orig_gc;
    }

    while (true) {
        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t_start).count();
        if (elapsed >= seconds) break;

        std::vector<uint64_t> cur = best_any;
        // Random perturbation
        int n_mut = 1 + (rng() % 3);
        for (int m = 0; m < n_mut; ++m) {
            uint64_t i = rng() % n_kmers;
            cur[i] = rng() % (n_kmers + 1);
        }
        uint64_t cur_gc = evaluator.eval_gc(cur);
        evals++;

        bool improved = true;
        while (improved) {
            improved = false;
            // Coordinate descent over each kmer's rank in 0..n_kmers
            for (uint64_t i = 0; i < n_kmers; ++i) {
                uint64_t old_r = cur[i];
                for (uint64_t r = 0; r <= n_kmers; ++r) {
                    if (r == old_r) continue;
                    cur[i] = r;
                    uint64_t gc = evaluator.eval_gc(cur);
                    evals++;
                    if (gc < cur_gc) {
                        cur_gc = gc;
                        old_r = r;
                        improved = true;
                    }
                }
                cur[i] = old_r;
            }
            // Pairwise swaps
            for (uint64_t i = 0; i < n_kmers; ++i) {
                for (uint64_t j = i + 1; j < n_kmers; ++j) {
                    if (cur[i] == cur[j]) continue;
                    std::swap(cur[i], cur[j]);
                    uint64_t gc = evaluator.eval_gc(cur);
                    evals++;
                    if (gc < cur_gc) {
                        cur_gc = gc;
                        improved = true;
                    } else {
                        std::swap(cur[i], cur[j]);
                    }
                }
            }
        }

        if (cur_gc < best_any_gc) {
            best_any_gc = cur_gc;
            best_any = cur;
            double d = evaluator.eval_density(best_any);
            double rel = (orig_den - d) / orig_den * 100.0;
            std::cout << "[GeneralGM]  New best GC = " << best_any_gc
                      << " density = " << d << " (rel = -" << std::setprecision(4) << rel << "%)"
                      << std::setprecision(8) << std::endl;
        }
    }

    std::cout << "Total exact evaluations: " << evals << std::endl;
    std::cout << "Best StrictPerm Order: [";
    for (size_t i = 0; i < best_perm.size(); ++i) std::cout << best_perm[i] << (i + 1 < best_perm.size() ? ", " : "");
    std::cout << "]" << std::endl;
    std::cout << "Best GeneralGM  Order: [";
    for (size_t i = 0; i < best_any.size(); ++i) std::cout << best_any[i] << (i + 1 < best_any.size() ? ", " : "");
    std::cout << "]" << std::endl;

    save_gm("data/best_perm_w" + std::to_string(w) + "_k" + std::to_string(k) + ".gm", best_perm);
    save_gm("data/best_gm_w" + std::to_string(w) + "_k" + std::to_string(k) + ".gm", best_any);
    return 0;
}
