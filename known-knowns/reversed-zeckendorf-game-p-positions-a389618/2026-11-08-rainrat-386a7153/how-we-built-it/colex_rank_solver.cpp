// Independent Colexicographic DP-Rank Solver for the Reversed Zeckendorf Game (n = 2..250)
//
// Representation & Algorithm (completely distinct from universal_delta_solver.cpp):
// 1. Represents each partition of a fixed n explicitly as (h_1, h_2, ..., h_12) with sum_{k=1}^{12} h_k F_k = n.
// 2. Uses theColexicographic Topological Identity: every Split move (F_{i+1} -> F_i + F_{i-1}) and every
//    Combine move (F_{i-2} + F_{i+1} -> 2 F_i) strictly decreases the highest modified coordinate h_{i+1} by 1
//     while leaving all higher coordinates unchanged. Therefore, colexicographic rank r in [0, A003107(n) - 1]
//    is a strict topological order for G_n, with r = 0 as the unique terminal state (n, 0, ..., 0) and
//    r = A003107(n) - 1 as the starting Zeckendorf decomposition of n.
// 3. Evaluates each n in [2, 250] independently:
//    - Pass 1 (Bottom-Up Retrograde): visits r = 0 .. A003107(n) - 1 in colexicographic order, computing
//      win[r] = OR_{(r -> r')} (!win[r']) in a flat bitset of size A003107(n) bits (2,736,376 bytes at n=250)
//      and counting outgoing edges from every state.
//    - Pass 2 (Top-Down Forward Reachability from Zeckendorf Seed): initializes reach[A003107(n) - 1] = 1
//      in a second bitset of the same size and propagates reach[r'] |= reach[r] from r = A003107(n) - 1
//      down to 0, verifying that every partition of n is reachable from the initial Zeckendorf state.

#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <omp.h>

static constexpr int MAX_N = 250;
static constexpr int F[13] = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233};

// dp[k][s] = number of partitions of s using {F_1, ..., F_k}
static uint32_t dp[13][MAX_N + 1];
// off[k][s][c] = sum_{j=0}^{c-1} dp[k-1][s - j * F_k], the colex offset at coordinate k
static uint32_t off_tbl[13][MAX_N + 1][MAX_N + 1];

static void init_dp() {
    for (int s = 0; s <= MAX_N; ++s) {
        dp[1][s] = 1;
    }
    for (int k = 2; k <= 12; ++k) {
        for (int s = 0; s <= MAX_N; ++s) {
            uint32_t sum = 0;
            int max_c = s / F[k];
            for (int c = 0; c <= max_c; ++c) {
                off_tbl[k][s][c] = sum;
                sum += dp[k - 1][s - c * F[k]];
            }
            dp[k][s] = sum;
        }
    }
}

struct SolverContext {
    int n;
    std::vector<uint64_t> win_bits;
    std::vector<uint64_t> reach_bits;
    uint64_t total_edges = 0;
    uint64_t reachable_verts = 0;
    uint64_t reachable_edges = 0;
    int h[13] = {0};
    int rem[13] = {0};
    uint32_t cur_off[13] = {0};

    inline bool get_win(uint32_t r) const {
        return (win_bits[r >> 6] >> (r & 63)) & 1ULL;
    }
    inline void set_win(uint32_t r) {
        win_bits[r >> 6] |= (1ULL << (r & 63));
    }
    inline bool get_reach(uint32_t r) const {
        return (reach_bits[r >> 6] >> (r & 63)) & 1ULL;
    }
    inline void set_reach(uint32_t r) {
        reach_bits[r >> 6] |= (1ULL << (r & 63));
    }

    // Compute neighbor rank for Split at i (1 <= i <= 11): F_{i+1} -> F_i + F_{i-1} (or 2 F_1 for i=1)
    inline uint32_t split_rank(uint32_t r, int i) const {
        if (i == 1) {
            // h[2] -= 1, h[1] += 2; rem[2] unchanged, off[2] decreases by 1
            return r - 1;
        }
        // Only coordinates k in {i-1, i, i+1} intersect [2, 12]
        uint32_t old_part = cur_off[i] + cur_off[i + 1];
        int rem_i_new = rem[i] + F[i] + F[i - 1];
        uint32_t new_part = off_tbl[i][rem_i_new][h[i] + 1]
                          + off_tbl[i + 1][rem[i + 1]][h[i + 1] - 1];
        if (i - 1 >= 2) {
            old_part += cur_off[i - 1];
            int rem_im1_new = rem[i - 1] + F[i - 1];
            new_part += off_tbl[i - 1][rem_im1_new][h[i - 1] + 1];
        }
        return r - old_part + new_part;
    }

    // Compute neighbor rank for Combine at i (2 <= i <= 11): F_{i-2} + F_{i+1} -> 2 F_i (F_1 + F_3 -> 2 F_2 for i=2)
    inline uint32_t combine_rank(uint32_t r, int i) const {
        if (i == 2) {
            // h[1] -= 1, h[3] -= 1, h[2] += 2; only k = 2, 3 change
            uint32_t old_part = cur_off[2] + cur_off[3];
            int rem_2_new = rem[2] - 1 + 2 * F[2]; // rem[2] + 3
            uint32_t new_part = off_tbl[2][rem_2_new][h[2] + 2]
                              + off_tbl[3][rem[3]][h[3] - 1];
            return r - old_part + new_part;
        }
        // i >= 3: coordinates k in {i-2, i-1, i, i+1} intersect [2, 12]
        // Note h[i-2] -= 1, h[i-1] unchanged (but rem[i-1] decreases by F[i-2]), h[i] += 2, h[i+1] -= 1
        uint32_t old_part = cur_off[i - 1] + cur_off[i] + cur_off[i + 1];
        int rem_im1_new = rem[i - 1] - F[i - 2];
        int rem_i_new   = rem[i] - F[i - 2] + 2 * F[i]; // rem[i] + F[i+1]
        uint32_t new_part = off_tbl[i - 1][rem_im1_new][h[i - 1]]
                          + off_tbl[i][rem_i_new][h[i] + 2]
                          + off_tbl[i + 1][rem[i + 1]][h[i + 1] - 1];
        if (i - 2 >= 2) {
            old_part += cur_off[i - 2];
            int rem_im2_new = rem[i - 2] - F[i - 2];
            new_part += off_tbl[i - 2][rem_im2_new][h[i - 2] - 1];
        }
        return r - old_part + new_part;
    }

    void dfs_forward_retrograde(int k, int s, uint32_t base_r) {
        rem[k] = s;
        if (k == 1) {
            h[1] = s;
            uint32_t r = base_r;
            bool w = false;

            // Split moves: i = 1..11
            for (int i = 1; i <= 11; ++i) {
                if (h[i + 1] >= 1) {
                    uint32_t nr = split_rank(r, i);
                    assert(nr < r);
                    total_edges += 1;
                    if (!w && !get_win(nr)) w = true;
                }
            }
            // Combine moves: i = 2..11
            if (h[1] >= 1 && h[3] >= 1) {
                uint32_t nr = combine_rank(r, 2);
                assert(nr < r);
                total_edges += 1;
                if (!w && !get_win(nr)) w = true;
            }
            for (int i = 3; i <= 11; ++i) {
                if (h[i - 2] >= 1 && h[i + 1] >= 1) {
                    uint32_t nr = combine_rank(r, i);
                    assert(nr < r);
                    total_edges += 1;
                    if (!w && !get_win(nr)) w = true;
                }
            }
            if (w) set_win(r);
            return;
        }
        int max_c = s / F[k];
        for (int c = 0; c <= max_c; ++c) {
            h[k] = c;
            cur_off[k] = off_tbl[k][s][c];
            dfs_forward_retrograde(k - 1, s - c * F[k], base_r + cur_off[k]);
        }
    }

    void dfs_backward_reach(int k, int s, uint32_t base_r) {
        rem[k] = s;
        if (k == 1) {
            h[1] = s;
            uint32_t r = base_r;
            if (!get_reach(r)) return;
            reachable_verts += 1;

            for (int i = 1; i <= 11; ++i) {
                if (h[i + 1] >= 1) {
                    uint32_t nr = split_rank(r, i);
                    set_reach(nr);
                    reachable_edges += 1;
                }
            }
            if (h[1] >= 1 && h[3] >= 1) {
                uint32_t nr = combine_rank(r, 2);
                set_reach(nr);
                reachable_edges += 1;
            }
            for (int i = 3; i <= 11; ++i) {
                if (h[i - 2] >= 1 && h[i + 1] >= 1) {
                    uint32_t nr = combine_rank(r, i);
                    set_reach(nr);
                    reachable_edges += 1;
                }
            }
            return;
        }
        int max_c = s / F[k];
        for (int c = max_c; c >= 0; --c) {
            h[k] = c;
            cur_off[k] = off_tbl[k][s][c];
            dfs_backward_reach(k - 1, s - c * F[k], base_r + cur_off[k]);
        }
    }
};

int main(int argc, char **argv) {
    auto t0 = std::chrono::steady_clock::now();
    init_dp();

    std::vector<int> winner(MAX_N + 1, 0);
    std::vector<uint64_t> edges(MAX_N + 1, 0);
    std::vector<uint64_t> verts(MAX_N + 1, 0);

    // Verify all n = 2..250 in parallel with dynamic scheduling (largest n first)
    #pragma omp parallel for schedule(dynamic, 1)
    for (int n = MAX_N; n >= 2; --n) {
        uint32_t V = dp[12][n];
        SolverContext ctx;
        ctx.n = n;
        ctx.win_bits.assign((V + 63) >> 6, 0ULL);
        ctx.reach_bits.assign((V + 63) >> 6, 0ULL);

        ctx.dfs_forward_retrograde(12, n, 0);

        // Starting Zeckendorf decomposition of n has colex rank V - 1
        ctx.set_reach(V - 1);
        ctx.dfs_backward_reach(12, n, 0);

        if (ctx.reachable_verts != V || ctx.reachable_edges != ctx.total_edges) {
            std::cerr << "Fatal: reachability mismatch at n=" << n
                      << " (verts " << ctx.reachable_verts << "/" << V
                      << ", edges " << ctx.reachable_edges << "/" << ctx.total_edges << ")\n";
            std::exit(1);
        }

        winner[n] = ctx.get_win(V - 1) ? 1 : 2;
        edges[n] = ctx.reachable_edges;
        verts[n] = ctx.reachable_verts;
    }

    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "colex_rank_solver completed n=2.." << MAX_N << " in " << sec << " seconds\n";

    std::string out_path = (argc > 1) ? argv[1] : "colex_rank_n2_250.tsv";
    std::ofstream out(out_path);
    if (!out) {
        std::cerr << "Fatal: failed to open output file " << out_path << "\n";
        return 1;
    }
    out << "n\twinner\tedges\tvertices\n";
    for (int n = 2; n <= MAX_N; ++n) {
        out << n << "\t" << winner[n] << "\t" << edges[n] << "\t" << verts[n] << "\n";
    }
    out.flush();
    if (!out.good()) {
        std::cerr << "Fatal: I/O error writing output file " << out_path << "\n";
        return 1;
    }
    out.close();
    return 0;
}
