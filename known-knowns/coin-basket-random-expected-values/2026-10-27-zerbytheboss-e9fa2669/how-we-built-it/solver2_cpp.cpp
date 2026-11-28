// Exact Integer Backward Induction Solver for Jehn's Random-Basket Coin Game
// Solver 2 (Lens 2): Independent Multi-Threaded C++20 Implementation
// Target: coin-basket-random-expected-values (A391791, A391792, Jehn Conjecture)

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <algorithm>
#include <cstdint>
#include <numeric>

using namespace std;
using namespace std::chrono;

// Binomial coefficient table
static uint64_t C[35][35];

void init_comb() {
    for (int i = 0; i <= 32; ++i) {
        C[i][0] = 1;
        for (int j = 1; j <= i; ++j) {
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j];
        }
    }
}

// Compute colex rank of an m-combination
inline uint64_t colex_rank(const uint8_t* bits, int m) {
    uint64_t r = 0;
    for (int i = 0; i < m; ++i) {
        r += C[bits[i]][i + 1];
    }
    return r;
}

// Generate all combinations of size m in colex order
void generate_combs_colex(int n, int m, vector<uint32_t>& out_masks) {
    uint64_t total = C[n][m];
    out_masks.resize(total);

    vector<uint8_t> bits;
    bits.reserve(m);

    auto dfs = [&](auto& self, int idx, int m_rem, uint32_t mask) -> void {
        if (m_rem == 0) {
            uint64_t r = colex_rank(bits.data(), m);
            out_masks[r] = mask;
            return;
        }
        if (n - idx < m_rem) return;

        // Choose idx
        bits.push_back((uint8_t)idx);
        self(self, idx + 1, m_rem - 1, mask | (1u << idx));
        bits.pop_back();

        // Do not choose idx
        self(self, idx + 1, m_rem, mask);
    };

    dfs(dfs, 0, m, 0u);
}

// Result structure for k=2
struct K2Result {
    int n;
    uint64_t a_n;
    vector<int> optimal_first_coins;
    bool conjecture_holds;
    int conjecture_coin;
};

// Solve k=2 (A391791)
K2Result solve_k2_cpp(int n, bool verbose) {
    auto t0 = steady_clock::now();
    int s_n = n * (n + 1) / 2;
    unsigned int num_threads = thread::hardware_concurrency();
    if (num_threads == 0) num_threads = 8;

    // Layer 0: m = 0
    int num_h_0 = s_n / 2 + 1;
    vector<uint64_t> prev_layer(num_h_0);
    for (int h = 0; h < num_h_0; ++h) {
        int d = (s_n % 2) + 2 * h;
        prev_layer[h] = (s_n + d) / 2;
    }
    vector<size_t> prev_offsets = {0, (size_t)num_h_0};

    vector<int> optimal_first_coins;

    for (int m = 1; m <= n; ++m) {
        vector<uint32_t> curr_masks;
        generate_combs_colex(n, m, curr_masks);
        size_t num_subsets = curr_masks.size();

        vector<size_t> curr_offsets(num_subsets + 1, 0);
        for (size_t i = 0; i < num_subsets; ++i) {
            uint32_t mask = curr_masks[i];
            int sum_r = 0;
            for (int b = 0; b < n; ++b) {
                if ((mask >> b) & 1) sum_r += (b + 1);
            }
            int p_r = s_n - sum_r;
            curr_offsets[i + 1] = curr_offsets[i] + (p_r / 2 + 1);
        }

        vector<uint64_t> curr_layer(curr_offsets.back(), 0);

        // Capture first moves at m == n
        if (m == n) {
            uint32_t full_mask = curr_masks[0];
            uint64_t best_val = 0;
            for (int coin = 1; coin <= n; ++coin) {
                uint32_t rem_mask = full_mask ^ (1u << (coin - 1));
                uint8_t rem_bits[32];
                int count = 0;
                for (int b = 0; b < n; ++b) {
                    if ((rem_mask >> b) & 1) rem_bits[count++] = (uint8_t)b;
                }
                uint64_t rem_rank = colex_rank(rem_bits, count);
                size_t rem_off = prev_offsets[rem_rank];
                int h_coin = coin / 2;
                uint64_t val = prev_layer[rem_off + h_coin];
                if (val > best_val) {
                    best_val = val;
                    optimal_first_coins = {coin};
                } else if (val == best_val) {
                    optimal_first_coins.push_back(coin);
                }
            }
        }

        // Multi-threaded chunk processing
        size_t chunk_size = (num_subsets + num_threads - 1) / num_threads;
        vector<thread> workers;

        for (unsigned int tid = 0; tid < num_threads; ++tid) {
            size_t start_idx = tid * chunk_size;
            size_t end_idx = min(start_idx + chunk_size, num_subsets);
            if (start_idx >= end_idx) continue;

            workers.emplace_back([&, start_idx, end_idx]() {
                uint8_t bits[32];
                uint8_t rem_bits[32];

                for (size_t r = start_idx; r < end_idx; ++r) {
                    uint32_t mask = curr_masks[r];
                    size_t off = curr_offsets[r];

                    int k = 0;
                    int sum_r = 0;
                    for (int b = 0; b < n; ++b) {
                        if ((mask >> b) & 1) {
                            bits[k++] = (uint8_t)b;
                            sum_r += (b + 1);
                        }
                    }

                    int p_r = s_n - sum_r;
                    int num_h = p_r / 2 + 1;
                    int p_mod = p_r % 2;

                    vector<uint64_t> best_b1(num_h, 0);
                    vector<uint64_t> best_b2(num_h, 0);

                    for (int j = 0; j < k; ++j) {
                        int coin = bits[j] + 1;
                        int rc = 0;
                        for (int l = 0; l < k; ++l) {
                            if (l != j) rem_bits[rc++] = bits[l];
                        }
                        uint64_t rem_rank = colex_rank(rem_bits, rc);
                        size_t rem_off = prev_offsets[rem_rank];
                        const uint64_t* prev_ptr = &prev_layer[rem_off];

                        for (int h = 0; h < num_h; ++h) {
                            int d = p_mod + 2 * h;

                            // Basket 1: d + coin
                            int h1 = (d + coin) / 2;
                            uint64_t v1 = prev_ptr[h1];
                            if (v1 > best_b1[h]) best_b1[h] = v1;

                            // Basket 2: |d - coin|
                            int d2 = (d >= coin) ? (d - coin) : (coin - d);
                            int h2 = d2 / 2;
                            uint64_t v2 = prev_ptr[h2];
                            if (v2 > best_b2[h]) best_b2[h] = v2;
                        }
                    }

                    for (int h = 0; h < num_h; ++h) {
                        curr_layer[off + h] = best_b1[h] + best_b2[h];
                    }
                }
            });
        }

        for (auto& w : workers) {
            w.join();
        }

        prev_layer = std::move(curr_layer);
        prev_offsets = std::move(curr_offsets);
    }

    uint64_t a_n = prev_layer[0] / 2;
    int conj_coin = (n + 3) / 2;
    bool conj_holds = (find(optimal_first_coins.begin(), optimal_first_coins.end(), conj_coin) != optimal_first_coins.end());

    if (verbose) {
        auto elapsed = duration_cast<milliseconds>(steady_clock::now() - t0).count();
        cout << "Solver 2 (C++) k=2, n=" << n << ": a(n)=" << a_n
             << " | opt first: [";
        for (size_t i = 0; i < optimal_first_coins.size(); ++i) {
            if (i > 0) cout << ", ";
            cout << optimal_first_coins[i];
        }
        cout << "] (conj=" << conj_coin << ", match=" << (conj_holds ? "true" : "false") << ") ["
             << elapsed << " ms]" << endl;
    }

    return {n, a_n, optimal_first_coins, conj_holds, conj_coin};
}

// Solve k=3 (A391792)
uint64_t solve_k3_cpp(int n, bool verbose) {
    auto t0 = steady_clock::now();
    int s_n = n * (n + 1) / 2;
    unsigned int num_threads = thread::hardware_concurrency();
    if (num_threads == 0) num_threads = 8;

    struct Triple {
        uint16_t s1, s2, s3;
    };

    // Precompute sorted triples for each P <= S_n
    vector<vector<Triple>> p_triples(s_n + 1);
    for (int p = 0; p <= s_n; ++p) {
        int min_s1 = (p + 2) / 3;
        for (int s1 = min_s1; s1 <= p; ++s1) {
            int min_s2 = (p - s1 + 1) / 2;
            int max_s2 = min(s1, p - s1);
            for (int s2 = min_s2; s2 <= max_s2; ++s2) {
                int s3 = p - s1 - s2;
                p_triples[p].push_back({(uint16_t)s1, (uint16_t)s2, (uint16_t)s3});
            }
        }
    }

    // Direct lookup: offset[p][s1] + (s2 - min_s2(p, s1))
    vector<vector<uint16_t>> p_s1_offset(s_n + 1);
    vector<vector<uint16_t>> p_s1_min_s2(s_n + 1);

    for (int p = 0; p <= s_n; ++p) {
        int min_s1 = (p + 2) / 3;
        p_s1_offset[p].assign(p + 1, 0);
        p_s1_min_s2[p].assign(p + 1, 0);
        uint16_t cur_idx = 0;

        for (int s1 = min_s1; s1 <= p; ++s1) {
            int min_s2 = (p - s1 + 1) / 2;
            int max_s2 = min(s1, p - s1);
            p_s1_offset[p][s1] = cur_idx;
            p_s1_min_s2[p][s1] = (uint16_t)min_s2;
            if (max_s2 >= min_s2) {
                cur_idx += (max_s2 - min_s2 + 1);
            }
        }
    }

    auto get_triple_idx = [&](int a, int b, int c) -> size_t {
        if (a < b) swap(a, b);
        if (b < c) swap(b, c);
        if (a < b) swap(a, b);
        int p = a + b + c;
        int off = p_s1_offset[p][a];
        int min_s2 = p_s1_min_s2[p][a];
        return (size_t)(off + (b - min_s2));
    };

    // Layer 0: m = 0
    size_t num_trips_0 = p_triples[s_n].size();
    vector<uint64_t> prev_layer(num_trips_0);
    for (size_t i = 0; i < num_trips_0; ++i) {
        prev_layer[i] = p_triples[s_n][i].s1;
    }
    vector<size_t> prev_offsets = {0, num_trips_0};

    for (int m = 1; m <= n; ++m) {
        vector<uint32_t> curr_masks;
        generate_combs_colex(n, m, curr_masks);
        size_t num_subsets = curr_masks.size();

        vector<size_t> curr_offsets(num_subsets + 1, 0);
        for (size_t i = 0; i < num_subsets; ++i) {
            uint32_t mask = curr_masks[i];
            int sum_r = 0;
            for (int b = 0; b < n; ++b) {
                if ((mask >> b) & 1) sum_r += (b + 1);
            }
            int p_r = s_n - sum_r;
            curr_offsets[i + 1] = curr_offsets[i] + p_triples[p_r].size();
        }

        vector<uint64_t> curr_layer(curr_offsets.back(), 0);

        size_t chunk_size = (num_subsets + num_threads - 1) / num_threads;
        vector<thread> workers;

        for (unsigned int tid = 0; tid < num_threads; ++tid) {
            size_t start_idx = tid * chunk_size;
            size_t end_idx = min(start_idx + chunk_size, num_subsets);
            if (start_idx >= end_idx) continue;

            workers.emplace_back([&, start_idx, end_idx]() {
                uint8_t bits[32];
                uint8_t rem_bits[32];

                for (size_t r = start_idx; r < end_idx; ++r) {
                    uint32_t mask = curr_masks[r];
                    size_t off = curr_offsets[r];

                    int k = 0;
                    int sum_r = 0;
                    for (int b = 0; b < n; ++b) {
                        if ((mask >> b) & 1) {
                            bits[k++] = (uint8_t)b;
                            sum_r += (b + 1);
                        }
                    }
                    int p_r = s_n - sum_r;
                    const auto& trips = p_triples[p_r];
                    size_t num_trips = trips.size();

                    vector<uint64_t> best_b1(num_trips, 0);
                    vector<uint64_t> best_b2(num_trips, 0);
                    vector<uint64_t> best_b3(num_trips, 0);

                    for (int j = 0; j < k; ++j) {
                        int coin = bits[j] + 1;
                        int rc = 0;
                        for (int l = 0; l < k; ++l) {
                            if (l != j) rem_bits[rc++] = bits[l];
                        }
                        uint64_t rem_rank = colex_rank(rem_bits, rc);
                        size_t rem_off = prev_offsets[rem_rank];
                        const uint64_t* prev_ptr = &prev_layer[rem_off];

                        for (size_t t_idx = 0; t_idx < num_trips; ++t_idx) {
                            int u1 = trips[t_idx].s1;
                            int u2 = trips[t_idx].s2;
                            int u3 = trips[t_idx].s3;

                            size_t idx1 = get_triple_idx(u1 + coin, u2, u3);
                            uint64_t v1 = prev_ptr[idx1];
                            if (v1 > best_b1[t_idx]) best_b1[t_idx] = v1;

                            size_t idx2 = get_triple_idx(u1, u2 + coin, u3);
                            uint64_t v2 = prev_ptr[idx2];
                            if (v2 > best_b2[t_idx]) best_b2[t_idx] = v2;

                            size_t idx3 = get_triple_idx(u1, u2, u3 + coin);
                            uint64_t v3 = prev_ptr[idx3];
                            if (v3 > best_b3[t_idx]) best_b3[t_idx] = v3;
                        }
                    }

                    for (size_t t = 0; t < num_trips; ++t) {
                        curr_layer[off + t] = best_b1[t] + best_b2[t] + best_b3[t];
                    }
                }
            });
        }

        for (auto& w : workers) {
            w.join();
        }

        prev_layer = std::move(curr_layer);
        prev_offsets = std::move(curr_offsets);
    }

    uint64_t a_n = prev_layer[0] / 3;
    if (verbose) {
        auto elapsed = duration_cast<milliseconds>(steady_clock::now() - t0).count();
        cout << "Solver 2 (C++) k=3, n=" << n << ": a(n)=" << a_n << " [" << elapsed << " ms]" << endl;
    }
    return a_n;
}

int main(int argc, char* argv[]) {
    init_comb();
    string mode = "all";
    if (argc > 1) mode = argv[1];

    cout << "=== Solver 2 (C++): Exact Integer Backward Induction ===" << endl;
    cout << "Target: coin-basket-random-expected-values" << endl;

    if (mode == "k2" || mode == "all") {
        cout << "\n--- Computing OEIS A391791 (k=2) for n=1..25 ---" << endl;
        vector<K2Result> res;
        for (int n = 1; n <= 25; ++n) {
            res.push_back(solve_k2_cpp(n, true));
        }

        cout << "\n=== Summary A391791 (k=2) ===" << endl;
        for (const auto& r : res) {
            cout << "A391791(" << r.n << ") = " << r.a_n << endl;
        }

        cout << "\n=== Jehn Conjecture Audit (n=10..25) ===" << endl;
        bool all_hold = true;
        for (const auto& r : res) {
            if (r.n >= 10) {
                bool holds = (r.optimal_first_coins == vector<int>{r.conjecture_coin});
                cout << "n=" << r.n << ": opt=[";
                for (size_t i = 0; i < r.optimal_first_coins.size(); ++i) {
                    if (i > 0) cout << ",";
                    cout << r.optimal_first_coins[i];
                }
                cout << "], conj=" << r.conjecture_coin << ", unique=" << (holds ? "true" : "false") << endl;
                if (!r.conjecture_holds) all_hold = false;
            }
        }
        cout << "Jehn conjecture holds for all n=10..25: " << (all_hold ? "true" : "false") << endl;
    }

    if (mode == "k3" || mode == "all") {
        cout << "\n--- Computing OEIS A391792 (k=3) for n=1..21 ---" << endl;
        for (int n = 1; n <= 21; ++n) {
            solve_k3_cpp(n, true);
        }
    }

    return 0;
}
