// certify_orbits_b.cpp
// Independent Exact Orbit-Enumeration Certifier (Implementation B)
// Completely independent from certify_orbits_a.cpp:
//   1. Uses explicit full-domain visited-bitmap partition traversal (verifying sum |O| = 2^m)
//      and verifies closed-form Burnside counts (7286, 3771, 349536 for 18x24x72).
//   2. Selects the MAXIMUM integer representative in each orbit (disjoint bitmasks from Impl A's
//      minimum representatives, directly testing orbit invariance end-to-end!).
//   3. Evaluates L(a, b) in pure 64-bit integer arithmetic (int64_t) via incremental Hamming-diff
//      column updates between consecutive representatives (no Four-Russians byte tables).
// Strictly uses at most 2 worker threads.

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

static uint32_t step_T(uint32_t x, int m) {
    // Antiperiodic shift: x'_i = x_{i+1} (i < m-1), x'_{m-1} = 1 - x_0
    uint32_t mask = (1u << m) - 1u;
    return ((x >> 1) | (((x & 1u) ^ 1u) << (m - 1))) & mask;
}

static uint32_t apply_R(uint32_t x, int m) {
    // Antiperiodic reflection: (R x)_0 = x_0, (R x)_i = 1 - x_{m-i} for 1 <= i < m
    uint32_t r = x & 1u;
    for (int i = 1; i < m; ++i) {
        uint32_t bit = (x >> (m - i)) & 1u;
        r |= ((bit ^ 1u) << i);
    }
    return r;
}

static uint64_t burnside_c2m(int m) {
    uint64_t sum_fix = (1ULL << m);
    for (int s = 1; s < 2 * m; ++s) {
        int g2 = std::gcd(s, 2 * m);
        int len = (2 * m) / g2;
        if (len % 2 == 1) {
            int gm = std::gcd(s, m);
            sum_fix += (1ULL << gm);
        }
    }
    if (sum_fix % (2 * m) != 0) return 0;
    return sum_fix / (2 * m);
}

static uint64_t burnside_d4m(int m) {
    uint64_t sum_fix = (1ULL << m);
    for (int s = 1; s < 2 * m; ++s) {
        int g2 = std::gcd(s, 2 * m);
        int len = (2 * m) / g2;
        if (len % 2 == 1) {
            sum_fix += (1ULL << std::gcd(s, m));
        }
    }
    // Reflections R * T^s for s = 0..2m-1:
    // If m is even: even s has fixed index s/2 and anti-fixed index s/2 + m/2 -> 0 fixed points;
    //               odd s pairs all 2m indices into m antiperiodic pairs -> 2^(m/2) fixed points.
    // If m is odd: every s has 1 fixed index and (m-1)/2 pairs -> 2^((m+1)/2) fixed points? Wait:
    // Let's count reflection fixed points directly by exact cycle check on {0..m-1}!
    for (int s = 0; s < 2 * m; ++s) {
        // Test action of R * T^s on indices 0..m-1 with sign:
        // Under T^s, bit i comes from index (i + s) mod 2m.
        // Under R after T^s: index 0 comes from 0 -> (s) mod 2m;
        //                    index i>0 comes from flipped (m - i) -> m + (m - i) + s = (2m - i + s) mod 2m = (-i + s) mod 2m!
        // So for ALL i in 0..m-1, new bit i is tilde_x_{(s - i) mod 2m}!
        bool possible = true;
        std::vector<int> vis(m, 0);
        int free_vars = 0;
        for (int i = 0; i < m; ++i) {
            int raw = (s - i) % (2 * m);
            if (raw < 0) raw += 2 * m;
            int j = raw % m;
            int flip = (raw >= m) ? 1 : 0;
            if (j == i) {
                if (flip == 1) { possible = false; break; }
                if (!vis[i]) { vis[i] = 1; ++free_vars; }
            } else {
                if (!vis[i] && !vis[j]) {
                    vis[i] = vis[j] = 1;
                    ++free_vars;
                }
            }
        }
        if (possible) sum_fix += (1ULL << free_vars);
    }
    if (sum_fix % (4 * m) != 0) return 0;
    return sum_fix / (4 * m);
}

static std::vector<uint32_t> enumerate_c2m_max_reps_partition(int m) {
    const uint32_t N = 1u << m;
    std::vector<uint8_t> seen(N, 0);
    std::vector<uint32_t> max_reps;
    uint64_t total_covered = 0;

    for (uint32_t start = 0; start < N; ++start) {
        if (seen[start]) continue;
        uint32_t cur = start;
        uint32_t mx = start;
        uint32_t cnt = 0;
        while (!seen[cur]) {
            seen[cur] = 1;
            if (cur > mx) mx = cur;
            ++cnt;
            cur = step_T(cur, m);
        }
        total_covered += cnt;
        max_reps.push_back(mx);
    }
    if (total_covered != N || max_reps.size() != burnside_c2m(m)) {
        std::cerr << "C2m partition/Burnside mismatch for m=" << m << "\n";
        std::exit(1);
    }
    std::sort(max_reps.begin(), max_reps.end());
    return max_reps;
}

static std::vector<uint32_t> enumerate_d4m_max_reps_partition(int m) {
    const uint32_t N = 1u << m;
    std::vector<uint8_t> seen(N, 0);
    std::vector<uint32_t> max_reps;
    uint64_t total_covered = 0;

    for (uint32_t start = 0; start < N; ++start) {
        if (seen[start]) continue;
        std::vector<uint32_t> stack = {start};
        seen[start] = 1;
        uint32_t mx = start;
        uint32_t cnt = 0;
        while (!stack.empty()) {
            uint32_t u = stack.back();
            stack.pop_back();
            ++cnt;
            if (u > mx) mx = u;
            uint32_t v1 = step_T(u, m);
            if (!seen[v1]) { seen[v1] = 1; stack.push_back(v1); }
            uint32_t v2 = apply_R(u, m);
            if (!seen[v2]) { seen[v2] = 1; stack.push_back(v2); }
        }
        total_covered += cnt;
        max_reps.push_back(mx);
    }
    if (total_covered != N || max_reps.size() != burnside_d4m(m)) {
        std::cerr << "D4m partition/Burnside mismatch for m=" << m
                  << " got=" << max_reps.size() << " exp=" << burnside_d4m(m) << "\n";
        std::exit(1);
    }
    std::sort(max_reps.begin(), max_reps.end());
    return max_reps;
}

static std::vector<int64_t> build_explicit_tensor(
    int mA, int mB, int mC, int stA, int stB, const std::vector<int64_t>& w
) {
    int N2 = 2 * mC;
    int half = mC / 2;
    std::vector<int64_t> M((size_t)mA * mB * mC, 0);
    for (int i = 0; i < mA; ++i) {
        for (int j = 0; j < mB; ++j) {
            for (int k = 0; k < mC; ++k) {
                int s = (stA * i + stB * j + k) % N2;
                int s1 = (s <= mC) ? s : (N2 - s);
                int64_t val = 0;
                if (mC % 2 == 0) {
                    if (s1 < half) val = w[s1];
                    else if (s1 > half) val = -w[mC - s1];
                } else {
                    if (s1 <= half) val = w[s1];
                    else val = -w[mC - s1];
                }
                M[((size_t)i * mB + j) * mC + k] = val;
            }
        }
    }
    return M;
}

static int64_t eval_incremental_orbits(
    int mA, int mB, int mC, const std::vector<int64_t>& M,
    const std::vector<uint32_t>& repsA, const std::vector<uint32_t>& repsB,
    int n_threads, uint32_t* out_uA = nullptr, uint32_t* out_uB = nullptr
) {
    const size_t nA = repsA.size();
    const size_t nB = repsB.size();
    std::atomic<size_t> next_a{0};
    std::vector<int64_t> t_best(n_threads, -1);
    std::vector<uint32_t> t_uA(n_threads, 0), t_uB(n_threads, 0);

    auto worker = [&](int tid) {
        std::vector<int64_t> W((size_t)mB * mC, 0);
        std::vector<int64_t> W2((size_t)mB * mC, 0);
        std::vector<int64_t> acc(mC, 0);
        int64_t loc_best = -1;
        uint32_t loc_uA = 0, loc_uB = 0;

        while (true) {
            size_t ia = next_a.fetch_add(1, std::memory_order_relaxed);
            if (ia >= nA) break;
            uint32_t uA = repsA[ia];

            std::fill(W.begin(), W.end(), 0);
            for (int i = 0; i < mA; ++i) {
                int64_t ai = ((uA >> i) & 1u) ? 1 : -1;
                const int64_t* Mi = &M[(size_t)i * mB * mC];
                for (int jk = 0; jk < mB * mC; ++jk) {
                    W[jk] += ai * Mi[jk];
                }
            }
            for (int jk = 0; jk < mB * mC; ++jk) W2[jk] = 2 * W[jk];

            // Initialize acc for repsB[0]
            uint32_t prevB = repsB[0];
            std::fill(acc.begin(), acc.end(), 0);
            for (int j = 0; j < mB; ++j) {
                int64_t bj = ((prevB >> j) & 1u) ? 1 : -1;
                const int64_t* row = &W[(size_t)j * mC];
                for (int k = 0; k < mC; ++k) acc[k] += bj * row[k];
            }
            int64_t s0 = 0;
            for (int k = 0; k < mC; ++k) s0 += (acc[k] >= 0) ? acc[k] : -acc[k];
            if (s0 > loc_best) { loc_best = s0; loc_uA = uA; loc_uB = prevB; }

            for (size_t ib = 1; ib < nB; ++ib) {
                uint32_t curB = repsB[ib];
                uint32_t diff = curB ^ prevB;
                while (diff != 0u) {
                    int j = __builtin_ctz(diff);
                    diff &= (diff - 1u);
                    const int64_t* row2 = &W2[(size_t)j * mC];
                    if ((curB >> j) & 1u) {
                        // changed 0 -> 1 (-1 -> +1): +2 * W[j]
                        for (int k = 0; k < mC; ++k) acc[k] += row2[k];
                    } else {
                        // changed 1 -> 0 (+1 -> -1): -2 * W[j]
                        for (int k = 0; k < mC; ++k) acc[k] -= row2[k];
                    }
                }
                prevB = curB;
                int64_t sum = 0;
                for (int k = 0; k < mC; ++k) {
                    int64_t v = acc[k];
                    sum += (v >= 0) ? v : -v;
                }
                if (sum > loc_best) {
                    loc_best = sum;
                    loc_uA = uA;
                    loc_uB = curB;
                }
            }
        }
        t_best[tid] = loc_best;
        t_uA[tid] = loc_uA;
        t_uB[tid] = loc_uB;
    };

    std::vector<std::thread> pool;
    for (int t = 0; t < n_threads; ++t) pool.emplace_back(worker, t);
    for (auto& th : pool) th.join();

    int64_t best = -1;
    for (int t = 0; t < n_threads; ++t) {
        if (t_best[t] > best) {
            best = t_best[t];
            if (out_uA) *out_uA = t_uA[t];
            if (out_uB) *out_uB = t_uB[t];
        }
    }
    return best;
}

static int64_t brute_force_tensor(int mA, int mB, int mC, const std::vector<int64_t>& M) {
    uint32_t nA = 1u << (mA - 1);
    uint32_t nB = 1u << (mB - 1);
    int64_t best = -1;
    for (uint32_t uA = 0; uA < nA; ++uA) {
        for (uint32_t uB = 0; uB < nB; ++uB) {
            int64_t sum = 0;
            for (int k = 0; k < mC; ++k) {
                int64_t sk = 0;
                for (int i = 0; i < mA; ++i) {
                    int64_t ai = ((uA >> i) & 1u) ? 1 : -1;
                    for (int j = 0; j < mB; ++j) {
                        int64_t bj = ((uB >> j) & 1u) ? 1 : -1;
                        sk += ai * bj * M[((size_t)i * mB + j) * mC + k];
                    }
                }
                sum += (sk >= 0) ? sk : -sk;
            }
            if (sum > best) best = sum;
        }
    }
    return best;
}

static bool run_calibrations() {
    struct Case { int mA, mB, mC, stA, stB; std::vector<int64_t> w; };
    std::vector<Case> cases = {
        {2, 2, 2, 1, 1, {1}},
        {6, 8, 24, 4, 3, {19, -7, 13, 5, -11, 3, -2, 8, -17, 6, -4, 9}},
        {9, 6, 18, 2, 3, {12, -5, 8, -19, 4, 7, -3, 15, -6}},
    };
    for (const auto& c : cases) {
        auto M = build_explicit_tensor(c.mA, c.mB, c.mC, c.stA, c.stB, c.w);
        auto rA = enumerate_d4m_max_reps_partition(c.mA);
        auto rB = enumerate_c2m_max_reps_partition(c.mB);
        int64_t lo = eval_incremental_orbits(c.mA, c.mB, c.mC, M, rA, rB, 1);
        int64_t lb = brute_force_tensor(c.mA, c.mB, c.mC, M);
        if (lo != lb) return false;
    }
    return true;
}

static int64_t parse_int_after(const std::string& s, const std::string& key) {
    size_t pos = s.find("\"" + key + "\"");
    if (pos == std::string::npos) std::exit(2);
    pos = s.find(':', pos);
    return std::stoll(s.substr(pos + 1));
}

static std::vector<int64_t> parse_int_array(const std::string& s, const std::string& key) {
    size_t pos = s.find("\"" + key + "\"");
    if (pos == std::string::npos) std::exit(2);
    size_t lb = s.find('[', pos);
    size_t rb = s.find(']', lb);
    std::string body = s.substr(lb + 1, rb - lb - 1);
    for (char& c : body) if (c == ',') c = ' ';
    std::stringstream ss(body);
    std::vector<int64_t> out;
    int64_t v;
    while (ss >> v) out.push_back(v);
    return out;
}

int main(int argc, char** argv) {
    if (argc < 2) return 2;
    auto t0 = std::chrono::steady_clock::now();

    if (!run_calibrations()) {
        std::cerr << "Impl B calibration failed!\n";
        return 1;
    }

    std::ifstream ifs(argv[1]);
    if (!ifs) return 2;
    std::string content((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());

    int mA = (int)parse_int_after(content, "mA");
    int mB = (int)parse_int_after(content, "mB");
    int mC = (int)parse_int_after(content, "mC");
    int stA = (int)parse_int_after(content, "stepA");
    int stB = (int)parse_int_after(content, "stepB");
    std::vector<int64_t> w = parse_int_array(content, "w_int");

    if (mC % mA != 0 || mC % mB != 0 || stA != mC / mA || stB != mC / mB) {
        std::cerr << "Invalid step dividers\n";
        return 2;
    }

    auto M = build_explicit_tensor(mA, mB, mC, stA, stB, w);
    auto repsA = enumerate_d4m_max_reps_partition(mA);
    auto repsB = enumerate_c2m_max_reps_partition(mB);

    uint32_t winA = 0, winB = 0;
    int64_t exact_L = eval_incremental_orbits(mA, mB, mC, M, repsA, repsB, 2, &winA, &winB);

    auto t1 = std::chrono::steady_clock::now();
    double elapsed = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "IMPL_B_CALIBRATIONS=PASS\n";
    std::cout << "BURNSIDE_ALICE_C2M=" << burnside_c2m(mA) << "\n";
    std::cout << "BURNSIDE_ALICE_D4M=" << repsA.size() << "\n";
    std::cout << "BURNSIDE_BOB_C2M=" << repsB.size() << "\n";
    std::cout << "TOTAL_ORBIT_PAIRS=" << (uint64_t)repsA.size() * (uint64_t)repsB.size() << "\n";
    std::cout << "EXACT_L=" << exact_L << "\n";
    std::cout << "WITNESS_UA=" << winA << "\n";
    std::cout << "WITNESS_UB=" << winB << "\n";
    std::cout << "ELAPSED_SEC=" << elapsed << "\n";
    return 0;
}
