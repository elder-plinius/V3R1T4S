// certify_orbits_a.cpp
// Independent Exact Orbit-Enumeration Certifier (Implementation A)
// Method: Canonical minimum-integer antiperiodic necklace generation +
//         reflection quotient on Alice + Four-Russians 3x8-bit byte lookup tables on Bob.
// Strictly uses at most 2 worker threads.

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

static inline uint32_t shift_antiperiodic(uint32_t u, int m) {
    uint32_t mask = (1u << m) - 1u;
    uint32_t bit0 = u & 1u;
    return ((u >> 1) | ((bit0 ^ 1u) << (m - 1))) & mask;
}

static inline uint32_t reflect_antiperiodic(uint32_t u, int m) {
    uint32_t out = u & 1u;
    for (int i = 1; i < m; ++i) {
        uint32_t b = (u >> (m - i)) & 1u;
        out |= ((b ^ 1u) << i);
    }
    return out;
}

static inline uint32_t canonical_c2m(uint32_t u, int m) {
    uint32_t best = u;
    uint32_t cur = u;
    for (int s = 1; s < 2 * m; ++s) {
        cur = shift_antiperiodic(cur, m);
        if (cur < best) best = cur;
    }
    return best;
}

struct OrbitSetA {
    std::vector<uint32_t> c2m_reps;
    std::vector<uint32_t> red_reps;
};

static OrbitSetA build_alice_orbits_canonical(int mA) {
    OrbitSetA res;
    const uint32_t total = 1u << mA;
    for (uint32_t u = 0; u < total; ++u) {
        if (canonical_c2m(u, mA) == u) {
            res.c2m_reps.push_back(u);
        }
    }
    for (uint32_t u : res.c2m_reps) {
        uint32_t ru = canonical_c2m(reflect_antiperiodic(u, mA), mA);
        if (u <= ru) {
            res.red_reps.push_back(u);
        }
    }
    return res;
}

static std::vector<uint32_t> build_bob_orbits_canonical(int mB) {
    std::vector<uint32_t> reps;
    const uint32_t total = 1u << mB;
    for (uint32_t u = 0; u < total; ++u) {
        if (canonical_c2m(u, mB) == u) {
            reps.push_back(u);
        }
    }
    return reps;
}

static std::vector<int64_t> build_F_table(int mC, const std::vector<int64_t>& w) {
    int N2 = 2 * mC;
    int half = mC / 2;
    std::vector<int64_t> F(N2, 0);
    for (int s = 0; s < N2; ++s) {
        int s1 = (s <= mC) ? s : (N2 - s);
        if (mC % 2 == 0) {
            if (s1 < half) F[s] = w[s1];
            else if (s1 > half) F[s] = -w[mC - s1];
            else F[s] = 0;
        } else {
            if (s1 <= half) F[s] = w[s1];
            else F[s] = -w[mC - s1];
        }
    }
    return F;
}

static int64_t eval_pair_direct(
    int mA, int mB, int mC, int stA, int stB,
    const std::vector<int64_t>& F, uint32_t uA, uint32_t uB
) {
    int N2 = 2 * mC;
    int64_t total = 0;
    for (int k = 0; k < mC; ++k) {
        int64_t sk = 0;
        for (int i = 0; i < mA; ++i) {
            int64_t ai = ((uA >> i) & 1u) ? 1 : -1;
            for (int j = 0; j < mB; ++j) {
                int64_t bj = ((uB >> j) & 1u) ? 1 : -1;
                int s = (stA * i + stB * j + k) % N2;
                sk += F[s] * ai * bj;
            }
        }
        total += (sk >= 0) ? sk : -sk;
    }
    return total;
}

static int64_t brute_force_small(
    int mA, int mB, int mC, int stA, int stB, const std::vector<int64_t>& w
) {
    auto F = build_F_table(mC, w);
    // Fix highest bit = 1 for both Alice and Bob (since L(-a, b) = L(a, -b) = L(a, b))
    uint32_t halfA = 1u << (mA - 1);
    uint32_t halfB = 1u << (mB - 1);
    int64_t best = -1;
    for (uint32_t uA = 0; uA < halfA; ++uA) {
        std::vector<int64_t> W(mB * mC, 0);
        for (int i = 0; i < mA; ++i) {
            int64_t ai = ((uA >> i) & 1u) ? 1 : -1;
            for (int j = 0; j < mB; ++j) {
                for (int k = 0; k < mC; ++k) {
                    W[j * mC + k] += ai * F[(stA * i + stB * j + k) % (2 * mC)];
                }
            }
        }
        for (uint32_t uB = 0; uB < halfB; ++uB) {
            int64_t sum = 0;
            for (int k = 0; k < mC; ++k) {
                int64_t sk = 0;
                for (int j = 0; j < mB; ++j) {
                    int64_t bj = ((uB >> j) & 1u) ? 1 : -1;
                    sk += bj * W[j * mC + k];
                }
                sum += (sk >= 0) ? sk : -sk;
            }
            if (sum > best) best = sum;
        }
    }
    return best;
}

static int64_t orbit_eval_generic(
    int mA, int mB, int mC, int stA, int stB, const std::vector<int64_t>& w
) {
    auto F = build_F_table(mC, w);
    auto orbA = build_alice_orbits_canonical(mA);
    auto orbB = build_bob_orbits_canonical(mB);
    int64_t best = -1;
    for (uint32_t uA : orbA.red_reps) {
        std::vector<int64_t> W(mB * mC, 0);
        for (int i = 0; i < mA; ++i) {
            int64_t ai = ((uA >> i) & 1u) ? 1 : -1;
            for (int j = 0; j < mB; ++j) {
                for (int k = 0; k < mC; ++k) {
                    W[j * mC + k] += ai * F[(stA * i + stB * j + k) % (2 * mC)];
                }
            }
        }
        for (uint32_t uB : orbB) {
            int64_t sum = 0;
            for (int k = 0; k < mC; ++k) {
                int64_t sk = 0;
                for (int j = 0; j < mB; ++j) {
                    int64_t bj = ((uB >> j) & 1u) ? 1 : -1;
                    sk += bj * W[j * mC + k];
                }
                sum += (sk >= 0) ? sk : -sk;
            }
            if (sum > best) best = sum;
        }
    }
    return best;
}

static bool run_calibrations() {
    // 1. Mermin 2x2x2 (4 nonzero terms: L = 2, Q_GHZ = 4, v* = 0.5)
    {
        std::vector<int64_t> w = {1};
        int64_t lb = brute_force_small(2, 2, 2, 1, 1, w);
        int64_t lo = orbit_eval_generic(2, 2, 2, 1, 1, w);
        if (lb != 2 || lo != 2) return false;
    }
    // 2. Asymmetric 6x8x24
    {
        std::vector<int64_t> w = {19, -7, 13, 5, -11, 3, -2, 8, -17, 6, -4, 9};
        int64_t lb = brute_force_small(6, 8, 24, 4, 3, w);
        int64_t lo = orbit_eval_generic(6, 8, 24, 4, 3, w);
        if (lb != lo) return false;
    }
    // 3. Asymmetric 8x12x24
    {
        std::vector<int64_t> w = {31, 14, -22, 9, -5, 18, -27, 11, 4, -16, 7, -13};
        int64_t lb = brute_force_small(8, 12, 24, 3, 2, w);
        int64_t lo = orbit_eval_generic(8, 12, 24, 3, 2, w);
        if (lb != lo) return false;
    }
    return true;
}

static int64_t parse_int_after(const std::string& s, const std::string& key) {
    size_t pos = s.find("\"" + key + "\"");
    if (pos == std::string::npos) {
        std::cerr << "Missing key: " << key << "\n";
        std::exit(2);
    }
    pos = s.find(':', pos);
    return std::stoll(s.substr(pos + 1));
}

static std::vector<int64_t> parse_int_array(const std::string& s, const std::string& key) {
    size_t pos = s.find("\"" + key + "\"");
    if (pos == std::string::npos) {
        std::cerr << "Missing array key: " << key << "\n";
        std::exit(2);
    }
    size_t lb = s.find('[', pos);
    size_t rb = s.find(']', lb);
    std::string body = s.substr(lb + 1, rb - lb - 1);
    for (char& c : body) {
        if (c == ',') c = ' ';
    }
    std::stringstream ss(body);
    std::vector<int64_t> out;
    int64_t v;
    while (ss >> v) out.push_back(v);
    return out;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <json_path>\n";
        return 2;
    }

    auto t0 = std::chrono::steady_clock::now();
    if (!run_calibrations()) {
        std::cerr << "Calibration failed!\n";
        return 1;
    }

    std::ifstream ifs(argv[1]);
    if (!ifs) {
        std::cerr << "Cannot open " << argv[1] << "\n";
        return 2;
    }
    std::string content((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());

    int mA = (int)parse_int_after(content, "mA");
    int mB = (int)parse_int_after(content, "mB");
    int mC = (int)parse_int_after(content, "mC");
    int stA = (int)parse_int_after(content, "stepA");
    int stB = (int)parse_int_after(content, "stepB");
    std::vector<int64_t> w = parse_int_array(content, "w_int");

    if (mA != 18 || mB != 24 || mC != 72 || (int)w.size() != 36) {
        std::cerr << "Expected 18x24x72 with 36 weights\n";
        return 2;
    }

    // Check int32 safety bound: max |sum_{i,j} M_ijk a_i b_j| <= 18 * 24 * max|w|
    int64_t max_w = 0;
    for (int64_t x : w) max_w = std::max(max_w, std::llabs(x));
    if (18LL * 24LL * max_w >= (1LL << 30)) {
        std::cerr << "Weights exceed int32 fast-table safety bound\n";
        return 2;
    }

    auto F = build_F_table(mC, w);
    auto orbA = build_alice_orbits_canonical(mA);
    auto orbB = build_bob_orbits_canonical(mB);

    const size_t nA = orbA.red_reps.size();
    const size_t nB = orbB.size();

    std::atomic<size_t> next_idx{0};
    const int n_threads = 2;
    std::vector<int64_t> thread_best(n_threads, -1);
    std::vector<uint32_t> thread_bestA(n_threads, 0);
    std::vector<uint32_t> thread_bestB(n_threads, 0);

    auto worker = [&](int tid) {
        alignas(64) int32_t T0[256][80];
        alignas(64) int32_t T1[256][80];
        alignas(64) int32_t T2[256][80];
        int32_t W[24][80];

        int64_t local_best = -1;
        uint32_t best_uA = 0, best_uB = 0;

        while (true) {
            size_t idx = next_idx.fetch_add(1, std::memory_order_relaxed);
            if (idx >= nA) break;
            uint32_t uA = orbA.red_reps[idx];

            for (int j = 0; j < 24; ++j) {
                for (int k = 0; k < 80; ++k) W[j][k] = 0;
            }
            for (int i = 0; i < 18; ++i) {
                int32_t ai = ((uA >> i) & 1u) ? 1 : -1;
                for (int j = 0; j < 24; ++j) {
                    for (int k = 0; k < 72; ++k) {
                        W[j][k] += ai * (int32_t)F[(stA * i + stB * j + k) % 144];
                    }
                }
            }

            // Build Four-Russians 3 x 8-bit tables (padded to 80 for clean 8-wide SIMD)
            for (int block = 0; block < 3; ++block) {
                int32_t (*T)[80] = (block == 0) ? T0 : ((block == 1) ? T1 : T2);
                int base_j = block * 8;
                for (int b = 0; b < 256; ++b) {
                    for (int k = 0; k < 80; ++k) T[b][k] = 0;
                    for (int bit = 0; bit < 8; ++bit) {
                        int32_t sgn = ((b >> bit) & 1) ? 1 : -1;
                        const int32_t* row = W[base_j + bit];
                        for (int k = 0; k < 72; ++k) {
                            T[b][k] += sgn * row[k];
                        }
                    }
                }
            }

            for (size_t bi = 0; bi < nB; ++bi) {
                uint32_t uB = orbB[bi];
                const int32_t* r0 = T0[uB & 0xFFu];
                const int32_t* r1 = T1[(uB >> 8) & 0xFFu];
                const int32_t* r2 = T2[(uB >> 16) & 0xFFu];
                int64_t sum = 0;
                for (int k = 0; k < 72; ++k) {
                    int32_t v = r0[k] + r1[k] + r2[k];
                    sum += (v >= 0) ? v : -v;
                }
                if (sum > local_best) {
                    local_best = sum;
                    best_uA = uA;
                    best_uB = uB;
                }
            }
        }
        thread_best[tid] = local_best;
        thread_bestA[tid] = best_uA;
        thread_bestB[tid] = best_uB;
    };

    std::vector<std::thread> threads;
    for (int t = 0; t < n_threads; ++t) threads.emplace_back(worker, t);
    for (auto& th : threads) th.join();

    int64_t exact_L = -1;
    uint32_t winA = 0, winB = 0;
    for (int t = 0; t < n_threads; ++t) {
        if (thread_best[t] > exact_L) {
            exact_L = thread_best[t];
            winA = thread_bestA[t];
            winB = thread_bestB[t];
        }
    }

    // Re-verify winning witness directly from scratch in int64:
    int64_t check_L = eval_pair_direct(mA, mB, mC, stA, stB, F, winA, winB);
    if (check_L != exact_L) {
        std::cerr << "Internal witness mismatch!\n";
        return 1;
    }

    auto t1 = std::chrono::steady_clock::now();
    double elapsed = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "IMPL_A_CALIBRATIONS=PASS\n";
    std::cout << "ALICE_C2M_ORBITS=" << orbA.c2m_reps.size() << "\n";
    std::cout << "ALICE_RED_ORBITS=" << nA << "\n";
    std::cout << "BOB_C2M_ORBITS=" << nB << "\n";
    std::cout << "TOTAL_ORBIT_PAIRS=" << (uint64_t)nA * (uint64_t)nB << "\n";
    std::cout << "EXACT_L=" << exact_L << "\n";
    std::cout << "WITNESS_UA=" << winA << "\n";
    std::cout << "WITNESS_UB=" << winB << "\n";
    std::cout << "ELAPSED_SEC=" << elapsed << "\n";
    return 0;
}
