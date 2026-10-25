#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <array>
#include <string>
#include <algorithm>
#include <random>
#include <chrono>
#include <unordered_map>
#include <unordered_set>
#include <thread>
#include <mutex>
#include <atomic>
#include <cstring>
#include <cassert>

struct Gate {
    int i1;
    int s1;
    int i2;
    int s2;
};

struct Vec64 {
    std::array<int8_t, 64> v{};
    uint64_t h = 0;      // Raw linear hash
    uint64_t ch = 0;     // Canonical hash = min(h, -h)
    int8_t csgn = 1;     // Sign to multiply v by to get canonical form
    int wt = 0;
};

struct PairInfo {
    int i;
    int j;
    int8_t rel;          // v_i + rel * v_j
    int8_t csgn;         // canonical sign of (v_i + rel * v_j)
    uint64_t raw_h;      // raw hash of canonical vector
    int wt;
};

struct BlockProblem {
    int nout;
    int nin;
    std::array<uint64_t, 64> R{};
    std::vector<Vec64> raw_targets;     // size nout
    std::vector<Vec64> unique_targets;  // deduplicated up to sign, weight >= 2
    int nz_rows = 0;
    int nz_cols = 0;
};

static inline Vec64 make_vec(const int8_t* arr, int nin, const std::array<uint64_t, 64>& R) {
    Vec64 res;
    uint64_t h = 0;
    int wt = 0;
    int first_nz = 0;
    for (int i = 0; i < nin; ++i) {
        int8_t val = arr[i];
        res.v[i] = val;
        if (val != 0) {
            wt += (val > 0 ? val : -val);
            if (first_nz == 0) first_nz = (val > 0 ? 1 : -1);
            h += static_cast<uint64_t>(static_cast<int64_t>(val)) * R[i];
        }
    }
    res.wt = wt;
    res.h = h;
    res.csgn = (first_nz >= 0) ? 1 : -1;
    res.ch = std::min(h, -h);
    return res;
}

static inline bool add_vec_checked(const Vec64& a, const Vec64& b, int8_t rel, int nin,
                                   const std::array<uint64_t, 64>& R, Vec64& out, int max_entry = 2) {
    int wt = 0;
    int first_nz = 0;
    for (int i = 0; i < nin; ++i) {
        int val = static_cast<int>(a.v[i]) + static_cast<int>(rel) * static_cast<int>(b.v[i]);
        if (val > max_entry || val < -max_entry) return false;
        out.v[i] = static_cast<int8_t>(val);
        if (val != 0) {
            wt += (val > 0 ? val : -val);
            if (first_nz == 0) first_nz = (val > 0 ? 1 : -1);
        }
    }
    if (wt == 0) return false;
    out.wt = wt;
    out.h = (rel == 1) ? (a.h + b.h) : (a.h - b.h);
    out.csgn = (first_nz >= 0) ? 1 : -1;
    out.ch = std::min(out.h, -out.h);
    return true;
}

struct SynthResult {
    int cost = 999999999;
    std::vector<Gate> fresh;
    std::vector<Vec64> stepping_stones; // non-target, non-unit intermediate canonical vectors
};

SynthResult synthesize_block(const BlockProblem& prob, std::mt19937_64* rng,
                             const std::vector<Vec64>* warm_stepping = nullptr,
                             int warm_keep = 0) {
    const int nin = prob.nin;
    std::vector<Vec64> B;
    B.reserve(nin + prob.unique_targets.size() + 128);
    std::vector<Gate> fresh;
    fresh.reserve(prob.unique_targets.size() + 128);

    std::unordered_map<uint64_t, std::pair<int, int8_t>> vec_to_idx;
    vec_to_idx.reserve(512);

    for (int i = 0; i < nin; ++i) {
        int8_t arr[64] = {0};
        arr[i] = 1;
        Vec64 v = make_vec(arr, nin, prob.R);
        B.push_back(v);
        vec_to_idx[v.ch] = {i, v.csgn};
    }

    // Track remaining unique targets
    std::vector<Vec64> rem = prob.unique_targets;
    std::unordered_set<uint64_t> rem_hashes;
    rem_hashes.reserve(rem.size() * 2 + 16);
    for (const auto& t : rem) rem_hashes.insert(t.ch);

    // Pair map: canonical hash ch -> PairInfo
    std::unordered_map<uint64_t, PairInfo> pair_map;
    pair_map.reserve(16384);

    auto add_node_to_pairs = [&](int new_idx) {
        const Vec64& v_new = B[new_idx];
        Vec64 v_sum;
        for (int i = 0; i < new_idx; ++i) {
            const Vec64& vi = B[i];
            for (int8_t rel : {int8_t(1), int8_t(-1)}) {
                if (!add_vec_checked(vi, v_new, rel, nin, prob.R, v_sum, 2)) continue;
                if (pair_map.find(v_sum.ch) == pair_map.end()) {
                    pair_map[v_sum.ch] = PairInfo{i, new_idx, rel, v_sum.csgn, v_sum.ch, v_sum.wt};
                }
            }
        }
    };

    for (int i = 0; i < nin; ++i) add_node_to_pairs(i);

    std::vector<Vec64> used_stepping;

    auto create_gate = [&](int i, int j, int8_t rel, bool is_stepping) {
        int new_idx = static_cast<int>(B.size());
        fresh.push_back(Gate{i, 1, j, rel});
        Vec64 v_new;
        add_vec_checked(B[i], B[j], rel, nin, prob.R, v_new, 4);
        B.push_back(v_new);
        vec_to_idx[v_new.ch] = {new_idx, v_new.csgn};
        if (is_stepping) {
            used_stepping.push_back(v_new);
        }
        add_node_to_pairs(new_idx);
    };

    auto run_cl1_closure = [&]() {
        bool progress = true;
        while (progress && !rem.empty()) {
            progress = false;
            for (size_t ti = 0; ti < rem.size(); ++ti) {
                uint64_t ch = rem[ti].ch;
                auto it = pair_map.find(ch);
                if (it != pair_map.end() && vec_to_idx.find(ch) == vec_to_idx.end()) {
                    PairInfo pi = it->second;
                    create_gate(pi.i, pi.j, pi.rel, false);
                    rem_hashes.erase(ch);
                    rem[ti] = rem.back();
                    rem.pop_back();
                    progress = true;
                    break;
                }
            }
        }
    };

    // Initial Cl_1 closure
    run_cl1_closure();

    // If warm_stepping provided, replay up to warm_keep stepping stones that are available in pair_map
    if (warm_stepping != nullptr && warm_keep > 0 && !rem.empty()) {
        int kept = 0;
        for (const auto& ws : *warm_stepping) {
            if (kept >= warm_keep || rem.empty()) break;
            if (vec_to_idx.find(ws.ch) != vec_to_idx.end()) continue;
            auto it = pair_map.find(ws.ch);
            if (it != pair_map.end()) {
                PairInfo pi = it->second;
                create_gate(pi.i, pi.j, pi.rel, true);
                kept++;
                run_cl1_closure();
            }
        }
    }

    std::uniform_real_distribution<double> noise_dist(0.0, 1.0);
    int mode = rng ? static_cast<int>((*rng)() % 4) : 0;
    double noise_scale = (rng == nullptr) ? 0.0 : (mode == 0 ? 0.3 : (mode == 1 ? 1.5 : (mode == 2 ? 4.0 : 12.0)));

    while (!rem.empty()) {
        // 1. Find all distance-2 stepping stone candidates: w in (B +- B) \cap (rem +- B)
        std::unordered_map<uint64_t, int> d2_hits;
        d2_hits.reserve(512);

        const int nB = static_cast<int>(B.size());
        for (const auto& t : rem) {
            uint64_t ht = t.h;
            for (int k = 0; k < nB; ++k) {
                uint64_t hbk = B[k].h;
                uint64_t h1 = ht + hbk;
                uint64_t ch1 = std::min(h1, -h1);
                if (ch1 != 0 && vec_to_idx.find(ch1) == vec_to_idx.end() && pair_map.find(ch1) != pair_map.end()) {
                    d2_hits[ch1]++;
                }
                uint64_t h2 = ht - hbk;
                uint64_t ch2 = std::min(h2, -h2);
                if (ch2 != 0 && ch2 != ch1 && vec_to_idx.find(ch2) == vec_to_idx.end() && pair_map.find(ch2) != pair_map.end()) {
                    d2_hits[ch2]++;
                }
            }
        }

        struct Cand {
            uint64_t ch;
            int d2;
            int wt;
            double pre_score;
        };
        std::vector<Cand> cands;

        if (!d2_hits.empty()) {
            cands.reserve(d2_hits.size());
            for (const auto& kv : d2_hits) {
                const auto& pi = pair_map[kv.first];
                double sc = kv.second * 20.0 - pi.wt * 0.5 + (rng ? noise_dist(*rng) * noise_scale : 0.0);
                cands.push_back(Cand{kv.first, kv.second, pi.wt, sc});
            }
            std::sort(cands.begin(), cands.end(), [](const Cand& a, const Cand& b) {
                return a.pre_score > b.pre_score;
            });
            if (cands.size() > 28) cands.resize(28);
        } else {
            // Distance >= 3! Use exact residual reduction r(t) = t - s* B[k*] across t in rem!
            std::unordered_map<uint64_t, int> res_gain;
            for (const auto& t : rem) {
                int best_d1 = t.wt + 1;
                int best_k = -1;
                int8_t best_s = 1;
                for (int k = 0; k < nB; ++k) {
                    int l1_p = 0, l1_m = 0;
                    for (int c = 0; c < nin; ++c) {
                        int dp = static_cast<int>(t.v[c]) - static_cast<int>(B[k].v[c]);
                        int dm = static_cast<int>(t.v[c]) + static_cast<int>(B[k].v[c]);
                        l1_p += (dp >= 0 ? dp : -dp);
                        l1_m += (dm >= 0 ? dm : -dm);
                    }
                    if (l1_p < best_d1) { best_d1 = l1_p; best_k = k; best_s = 1; }
                    if (l1_m < best_d1) { best_d1 = l1_m; best_k = k; best_s = -1; }
                }
                if (best_k < 0) continue;
                int8_t rvec[64];
                std::vector<int> nz_pos;
                for (int c = 0; c < nin; ++c) {
                    rvec[c] = static_cast<int8_t>(t.v[c] - best_s * B[best_k].v[c]);
                    if (rvec[c] != 0) nz_pos.push_back(c);
                }
                // (1) Weight-2 sub-vectors of rvec: e_a +- e_b (shared across residuals)
                for (size_t ia = 0; ia < nz_pos.size(); ++ia) {
                    int a = nz_pos[ia];
                    int8_t sa = (rvec[a] > 0 ? 1 : -1);
                    for (size_t ib = ia + 1; ib < nz_pos.size(); ++ib) {
                        int b = nz_pos[ib];
                        int8_t sb = (rvec[b] > 0 ? 1 : -1);
                        int8_t rel = sa * sb;
                        uint64_t h_pair = (rel == 1) ? (B[a].h + B[b].h) : (B[a].h - B[b].h);
                        uint64_t ch_pair = std::min(h_pair, -h_pair);
                        if (vec_to_idx.find(ch_pair) == vec_to_idx.end() && pair_map.find(ch_pair) != pair_map.end()) {
                            res_gain[ch_pair] += 3;
                        }
                    }
                }
                // (2) Direct extension of B[best_k] by B[j] that reduces ||rvec||_1
                for (int j = 0; j < nB; ++j) {
                    if (j == best_k) continue;
                    int l1_p = 0, l1_m = 0;
                    for (int c = 0; c < nin; ++c) {
                        int dp = static_cast<int>(rvec[c]) - static_cast<int>(B[j].v[c]);
                        int dm = static_cast<int>(rvec[c]) + static_cast<int>(B[j].v[c]);
                        l1_p += (dp >= 0 ? dp : -dp);
                        l1_m += (dm >= 0 ? dm : -dm);
                    }
                    int best_r = std::min(l1_p, l1_m);
                    if (best_r < best_d1) {
                        int8_t s_j = (l1_p <= l1_m) ? 1 : -1;
                        // We want w = best_s * B[best_k] + s_j * B[j], so up to sign B[best_k] + (best_s * s_j) * B[j]
                        int8_t rel = best_s * s_j;
                        uint64_t hw = (rel == 1) ? (B[best_k].h + B[j].h) : (B[best_k].h - B[j].h);
                        uint64_t chw = std::min(hw, -hw);
                        if (vec_to_idx.find(chw) == vec_to_idx.end() && pair_map.find(chw) != pair_map.end()) {
                            int red = best_d1 - best_r;
                            res_gain[chw] += red * 4;
                        }
                    }
                }
            }
            for (const auto& kv : res_gain) {
                const PairInfo& pi = pair_map[kv.first];
                double sc = kv.second * 5.0 - pi.wt * 0.5 + (rng ? noise_dist(*rng) * noise_scale : 0.0);
                cands.push_back(Cand{kv.first, kv.second, pi.wt, sc});
            }
            if (cands.empty()) {
                for (const auto& kv : pair_map) {
                    if (vec_to_idx.find(kv.first) == vec_to_idx.end()) {
                        cands.push_back(Cand{kv.first, 1, kv.second.wt, -double(kv.second.wt)});
                        if (cands.size() >= 8) break;
                    }
                }
            }
            if (cands.empty()) break;
            std::sort(cands.begin(), cands.end(), [](const Cand& a, const Cand& b) {
                return a.pre_score > b.pre_score;
            });
            if (cands.size() > 16) cands.resize(16);
        }

        // Evaluate top candidates with full Cl_1 cascade simulation + new Distance-2 creation count!
        uint64_t best_chw = cands[0].ch;
        double best_eval = -1e18;

        for (const auto& cand : cands) {
            const PairInfo& pi = pair_map[cand.ch];
            Vec64 vw;
            add_vec_checked(B[pi.i], B[pi.j], pi.rel, nin, prob.R, vw, 2);

            // Simulate Cl_1 cascade starting from vw
            std::vector<uint64_t> sim_B_hashes;
            sim_B_hashes.reserve(B.size() + 16);
            for (const auto& b : B) sim_B_hashes.push_back(b.h);
            sim_B_hashes.push_back(vw.h);

            std::unordered_set<uint64_t> sim_rem = rem_hashes;
            std::vector<uint64_t> queue_h = {vw.h};
            int absorbed = 0;

            while (!queue_h.empty()) {
                uint64_t h_new = queue_h.back();
                queue_h.pop_back();
                size_t cur_sz = sim_B_hashes.size();
                for (size_t bi = 0; bi < cur_sz; ++bi) {
                    uint64_t hb = sim_B_hashes[bi];
                    for (uint64_t hsum : {h_new + hb, h_new - hb}) {
                        uint64_t ch_sum = std::min(hsum, -hsum);
                        auto it = sim_rem.find(ch_sum);
                        if (it != sim_rem.end()) {
                            sim_rem.erase(it);
                            sim_B_hashes.push_back(hsum);
                            queue_h.push_back(hsum);
                            absorbed++;
                        }
                    }
                }
            }

            // Count how many remaining targets in sim_rem become distance-2 via the newly added nodes
            // (i.e. t +- b_new is in pair_map!)
            int new_d2 = 0;
            int d3_mitm = 0;
            for (uint64_t rem_ch : sim_rem) {
                // Note: rem_ch is canonical hash (+- h_t), so rem_ch +- h_new covers both signs!
                for (size_t bi = B.size(); bi < sim_B_hashes.size(); ++bi) {
                    uint64_t h_new = sim_B_hashes[bi];
                    uint64_t h1 = rem_ch + h_new;
                    uint64_t ch1 = std::min(h1, -h1);
                    if (pair_map.find(ch1) != pair_map.end()) {
                        new_d2++;
                        break;
                    }
                    uint64_t h2 = rem_ch - h_new;
                    uint64_t ch2 = std::min(h2, -h2);
                    if (pair_map.find(ch2) != pair_map.end()) {
                        new_d2++;
                        break;
                    }
                }
            }

            double noise = rng ? noise_dist(*rng) * noise_scale : 0.0;
            double eval = (mode == 0)
                ? (absorbed * 100.0 + cand.d2 * 10.0 - cand.wt * 1.0 + noise)
                : (absorbed * 200.0 + new_d2 * 15.0 + cand.d2 * 10.0 - cand.wt * 1.5 + noise);
            if (eval > best_eval) {
                best_eval = eval;
                best_chw = cand.ch;
            }
        }

        PairInfo best_pi = pair_map[best_chw];
        create_gate(best_pi.i, best_pi.j, best_pi.rel, true);
        run_cl1_closure();
    }

    // Prune any dead gates in `fresh` backwards!
    int nf = static_cast<int>(fresh.size());
    std::vector<int> use_cnt(nin + nf, 0);
    for (const auto& t : prob.raw_targets) {
        if (t.wt >= 2) {
            auto it = vec_to_idx.find(t.ch);
            assert(it != vec_to_idx.end());
            use_cnt[it->second.first]++;
        }
    }
    for (int fi = nf - 1; fi >= 0; --fi) {
        int u = nin + fi;
        if (use_cnt[u] > 0) {
            use_cnt[fresh[fi].i1]++;
            use_cnt[fresh[fi].i2]++;
        }
    }
    std::vector<int> old_to_new(nin + nf, -1);
    for (int i = 0; i < nin; ++i) old_to_new[i] = i;
    std::vector<Gate> pruned_fresh;
    for (int fi = 0; fi < nf; ++fi) {
        int u = nin + fi;
        if (use_cnt[u] > 0) {
            int new_u = nin + static_cast<int>(pruned_fresh.size());
            old_to_new[u] = new_u;
            Gate g = fresh[fi];
            g.i1 = old_to_new[g.i1];
            g.i2 = old_to_new[g.i2];
            assert(g.i1 >= 0 && g.i2 >= 0);
            pruned_fresh.push_back(g);
        }
    }

    SynthResult res;
    res.cost = static_cast<int>(pruned_fresh.size());
    res.fresh = std::move(pruned_fresh);
    res.stepping_stones = std::move(used_stepping);
    return res;
}

BlockProblem build_problem(int nout, int nin, const std::vector<int>& flat_mat) {
    BlockProblem prob;
    prob.nout = nout;
    prob.nin = nin;
    std::mt19937_64 rgen(0x9E3779B97F4A7C15ULL ^ (uint64_t(nout) << 16) ^ uint64_t(nin));
    for (int i = 0; i < nin; ++i) {
        prob.R[i] = (rgen() | 1ULL);
    }
    std::unordered_set<uint64_t> seen_ch;
    for (int i = 0; i < nin; ++i) {
        int8_t arr[64] = {0};
        arr[i] = 1;
        Vec64 u = make_vec(arr, nin, prob.R);
        seen_ch.insert(u.ch);
    }

    std::vector<int> col_nz(nin, 0);
    for (int r = 0; r < nout; ++r) {
        int8_t arr[64] = {0};
        bool row_has_nz = false;
        for (int c = 0; c < nin; ++c) {
            int v = flat_mat[r * nin + c];
            arr[c] = static_cast<int8_t>(v);
            if (v != 0) {
                row_has_nz = true;
                col_nz[c] = 1;
            }
        }
        if (row_has_nz) prob.nz_rows++;
        Vec64 tv = make_vec(arr, nin, prob.R);
        prob.raw_targets.push_back(tv);
        if (tv.wt >= 2 && seen_ch.find(tv.ch) == seen_ch.end()) {
            seen_ch.insert(tv.ch);
            prob.unique_targets.push_back(tv);
        }
    }
    for (int c = 0; c < nin; ++c) prob.nz_cols += col_nz[c];
    return prob;
}

SynthResult optimize_block_parallel(const BlockProblem& prob, int target_budget_trials, int num_threads = 8) {
    SynthResult global_best = synthesize_block(prob, nullptr, nullptr, 0);
    int lb = static_cast<int>(prob.unique_targets.size());
    if (global_best.cost <= lb || target_budget_trials <= 0) return global_best;
    std::mutex mtx;
    std::atomic<bool> hit_lb{false};

    auto worker = [&](int tid) {
        std::mt19937_64 rng(0x202610220355ULL + tid * 10007ULL);
        SynthResult local_best;
        {
            std::lock_guard<std::mutex> lk(mtx);
            local_best = global_best;
        }
        int trials_per_thread = (target_budget_trials + num_threads - 1) / num_threads;
        for (int t = 0; t < trials_per_thread; ++t) {
            if (hit_lb.load(std::memory_order_relaxed)) break;
            SynthResult cand;
            int S = static_cast<int>(local_best.stepping_stones.size());
            if (S > 1 && (t % 3 != 0)) {
                // Stepping-Stone LNS!
                std::vector<Vec64> warm = local_best.stepping_stones;
                if (t % 2 == 1) {
                    // Random subset order
                    std::shuffle(warm.begin(), warm.end(), rng);
                }
                int keep = 1 + static_cast<int>(rng() % (S - 1));
                cand = synthesize_block(prob, &rng, &warm, keep);
            } else {
                cand = synthesize_block(prob, &rng, nullptr, 0);
            }
            if (cand.cost < local_best.cost) {
                local_best = cand;
                std::lock_guard<std::mutex> lk(mtx);
                if (local_best.cost < global_best.cost) {
                    global_best = local_best;
                    if (global_best.cost <= lb) hit_lb.store(true, std::memory_order_relaxed);
                }
            } else {
                std::lock_guard<std::mutex> lk(mtx);
                if (global_best.cost < local_best.cost) {
                    local_best = global_best;
                }
            }
        }
    };

    std::vector<std::thread> threads;
    for (int tid = 0; tid < num_threads; ++tid) threads.emplace_back(worker, tid);
    for (auto& th : threads) th.join();
    return global_best;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " [trials=240] <scheme1.txt> [scheme2.txt ...]\n";
        return 1;
    }
    int trials = 240;
    int start_arg = 1;
    if (std::string(argv[1]).find(".txt") == std::string::npos) {
        trials = std::atoi(argv[1]);
        start_arg = 2;
    } else if (argc == 3 && std::string(argv[2]).find(".txt") == std::string::npos) {
        trials = std::atoi(argv[2]);
    }

    for (int argi = start_arg; argi < argc; ++argi) {
        std::string path = argv[argi];
        if (path.find(".txt") == std::string::npos) continue;

        std::ifstream fin(path);
        if (!fin) continue;
        int n1, n2, n3, rank;
        if (!(fin >> n1 >> n2 >> n3 >> rank)) continue;

        int nin_u = n1 * n2;
        int nin_v = n2 * n3;
        int nin_w = n1 * n3; // For W (rank x (n1*n3)), transposed via Tellegen to W^T!

        std::vector<int> U_mat(rank * nin_u);
        std::vector<int> V_mat(rank * nin_v);
        std::vector<int> W_mat(rank * nin_w);

        for (int i = 0; i < rank * nin_u; ++i) fin >> U_mat[i];
        for (int i = 0; i < rank * nin_v; ++i) fin >> V_mat[i];
        for (int i = 0; i < rank * nin_w; ++i) fin >> W_mat[i];

        BlockProblem probU = build_problem(rank, nin_u, U_mat);
        BlockProblem probV = build_problem(rank, nin_v, V_mat);
        BlockProblem probW = build_problem(rank, nin_w, W_mat);

        SynthResult resU = optimize_block_parallel(probU, trials);
        SynthResult resV = optimize_block_parallel(probV, trials);
        SynthResult resW = optimize_block_parallel(probW, trials);

        // By Tellegen's Theorem: cr(W^T) = cr(W) + nz_rows(W) - nz_cols(W)
        int cr_U = resU.cost;
        int cr_V = resV.cost;
        int cr_WT = resW.cost + probW.nz_rows - probW.nz_cols;
        int total_cr = cr_U + cr_V + cr_WT;

        std::string bn = path.substr(path.find_last_of('/') + 1);
        std::cout << bn
                  << " -> U=" << cr_U << " (lb=" << probU.unique_targets.size() << ")"
                  << " V=" << cr_V << " (lb=" << probV.unique_targets.size() << ")"
                  << " W^T=" << cr_WT << " [W=" << resW.cost << ", lb=" << probW.unique_targets.size() << "]"
                  << " TOTAL=" << total_cr << std::endl;

        const char* exp_dir = std::getenv("EXPORT_GATES_DIR");
        if (exp_dir != nullptr) {
            std::string stem = bn.substr(0, bn.find_last_of('.'));
            std::string out_p = std::string(exp_dir) + "/" + stem + ".gates.json";
            std::ofstream fout(out_p);
            auto dump_gates = [&](const char* key, const std::vector<Gate>& gs, bool comma) {
                fout << "  \"" << key << "\": [";
                for (size_t gi = 0; gi < gs.size(); ++gi) {
                    if (gi > 0) fout << ", ";
                    fout << "[" << gs[gi].i1 << "," << gs[gi].s1 << "," << gs[gi].i2 << "," << gs[gi].s2 << "]";
                }
                fout << "]" << (comma ? ",\n" : "\n");
            };
            fout << "{\n";
            fout << "  \"n\": [" << n1 << ", " << n2 << ", " << n3 << "],\n";
            fout << "  \"m\": " << rank << ",\n";
            fout << "  \"cr_U\": " << cr_U << ",\n";
            fout << "  \"cr_V\": " << cr_V << ",\n";
            fout << "  \"cr_WT\": " << cr_WT << ",\n";
            fout << "  \"total_cr\": " << total_cr << ",\n";
            dump_gates("u_gates", resU.fresh, true);
            dump_gates("v_gates", resV.fresh, true);
            dump_gates("wT_gates", resW.fresh, false);
            fout << "}\n";
        }
    }
    return 0;
}
