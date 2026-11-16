#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <algorithm>
#include <numeric>
#include <random>
#include <chrono>
#include <iomanip>

struct Dna4AryEvaluator {
    int w, k, N, mask;
    std::vector<int> fwd;
    std::vector<int> bwd;

    Dna4AryEvaluator(int w_, int k_) : w(w_), k(k_), N(1 << (2 * k_)), mask((1 << (2 * k_)) - 1) {
        fwd.resize(N * 4);
        bwd.resize(N * 4);
        for (int u = 0; u < N; ++u) {
            for (int b = 0; b < 4; ++b) {
                fwd[u * 4 + b] = ((u << 2) & mask) | b;
                bwd[u * 4 + b] = (u >> 2) | (b << (2 * (k - 1)));
            }
        }
    }

    uint64_t eval_gc(const std::vector<int>& rank_of) const {
        std::vector<int> inv(N);
        for (int u = 0; u < N; ++u) inv[rank_of[u]] = u;

        uint64_t total_gc = 0;
        std::vector<uint64_t> dp(N), nxt(N);
        std::vector<uint8_t> active(N, 1);

        for (int r = 0; r < N; ++r) {
            int u0 = inv[r];
            std::fill(dp.begin(), dp.end(), 0);
            dp[u0] = 1;
            bool any = true;
            for (int step = 0; step < w; ++step) {
                std::fill(nxt.begin(), nxt.end(), 0);
                any = false;
                for (int u = 0; u < N; ++u) {
                    uint64_t val = dp[u];
                    if (!val) continue;
                    const int* f = &fwd[u * 4];
                    for (int b = 0; b < 4; ++b) {
                        int v = f[b];
                        if (active[v]) {
                            nxt[v] += val;
                            any = true;
                        }
                    }
                }
                dp.swap(nxt);
                if (!any) break;
            }
            if (any) {
                for (int u = 0; u < N; ++u) total_gc += dp[u];
            }

            active[u0] = 0;

            std::fill(dp.begin(), dp.end(), 0);
            dp[u0] = 1;
            any = true;
            for (int step = 0; step < w; ++step) {
                std::fill(nxt.begin(), nxt.end(), 0);
                any = false;
                for (int u = 0; u < N; ++u) {
                    uint64_t val = dp[u];
                    if (!val) continue;
                    const int* bw = &bwd[u * 4];
                    for (int b = 0; b < 4; ++b) {
                        int v = bw[b];
                        if (active[v]) {
                            nxt[v] += val;
                            any = true;
                        }
                    }
                }
                dp.swap(nxt);
                if (!any) break;
            }
            if (any) {
                for (int u = 0; u < N; ++u) total_gc += dp[u];
            }
        }
        return total_gc;
    }
};

std::vector<int> gm_to_4ary(const std::vector<int>& order_bin, int k) {
    int N = 1 << (2 * k);
    std::vector<std::pair<int, int>> keys(N);
    for (int km = 0; km < N; ++km) {
        int bin_km = 0, low_km = 0;
        for (int i = 0; i < k; ++i) {
            int nuc = (km >> (2 * (k - 1 - i))) & 3;
            bin_km = (bin_km << 1) | ((nuc >> 1) & 1);
            low_km = (low_km << 1) | (nuc & 1);
        }
        keys[km] = {order_bin[bin_km], low_km};
    }
    std::vector<int> idx(N);
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return keys[a] < keys[b]; });
    std::vector<int> rank_4ary(N);
    for (int r = 0; r < N; ++r) rank_4ary[idx[r]] = r;
    return rank_4ary;
}

int main() {
    int w = 12, k = 4;
    Dna4AryEvaluator eval(w, k);
    std::vector<int> bin_order = {15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5};
    auto cur = gm_to_4ary(bin_order, k);
    uint64_t cur_gc = eval.eval_gc(cur);

    std::mt19937_64 rng(42);
    int N = 1 << (2 * k);
    auto t0 = std::chrono::steady_clock::now();

    std::vector<int> inv(N);
    for (int u = 0; u < N; ++u) inv[cur[u]] = u;

    uint64_t best_gc = cur_gc;
    std::vector<int> best_rank = cur;

    for (int iter = 0; iter < 35267; ++iter) {
        int r1 = rng() % 115;
        int r2 = rng() % N;
        if (r1 == r2) continue;
        int u1 = inv[r1], u2 = inv[r2];
        std::swap(cur[u1], cur[u2]);
        std::swap(inv[r1], inv[r2]);
        uint64_t gc = eval.eval_gc(cur);
        if (gc <= cur_gc) {
            if (gc < best_gc) {
                best_gc = gc;
                best_rank = cur;
            }
            cur_gc = gc;
        } else {
            std::swap(cur[u1], cur[u2]);
            std::swap(inv[r1], inv[r2]);
        }
    }
    std::cout << "Best GC = " << best_gc << " / 2^32 = " << std::fixed << std::setprecision(10)
              << (double)best_gc / (double)(1ULL << 32) << std::endl;
    return 0;
}
