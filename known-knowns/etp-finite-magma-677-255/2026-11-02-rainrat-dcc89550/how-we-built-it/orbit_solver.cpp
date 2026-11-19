// Fast exact backtracking + constraint propagation solver for Equation 677 counterexamples
// by right-multiplication orbit (k, s) of 0:
//   0 -> 1 -> 2 -> ... -> k -> s  (1 <= s <= k <= n - 1)
// where f(y) = y ◇ 0, and 0 has no fixer (y ◇ 0 != 0 for all y).
// Also includes a full-model calibration mode (--calibrate) where y ◇ 0 == 0 is allowed,
// verifying that the exact same propagator + search finds valid Eq677 magmas at n=5 and n=7.
#include <iostream>
#include <vector>
#include <cstdint>
#include <cstring>
#include <chrono>
#include <algorithm>
#include <omp.h>

static const int MAXN = 12;

struct State {
    int n;
    bool forbid_zero_fixer;
    int8_t op[MAXN][MAXN];       // op[x][y] = x ◇ y, -1 if unassigned
    int8_t invL[MAXN][MAXN];     // invL[y][z] = x such that y ◇ x = z, -1 if unassigned
    uint16_t row_used[MAXN];     // bitmask of values used in row x
    uint64_t nodes = 0;

    void init(int n_, bool forbid_zero_fixer_ = true) {
        n = n_;
        forbid_zero_fixer = forbid_zero_fixer_;
        std::memset(op, -1, sizeof(op));
        std::memset(invL, -1, sizeof(invL));
        std::memset(row_used, 0, sizeof(row_used));
        nodes = 0;
    }

    inline bool assign(int x, int y, int v) {
        int8_t cur = op[x][y];
        if (cur != -1) return cur == v;
        if (v < 0 || v >= n) return false;
        // Row x is L_x: must be injective
        if ((row_used[x] >> v) & 1) return false;
        // In counterexample search mode, column 0 cannot take value 0 (y ◇ 0 != 0)
        if (forbid_zero_fixer && y == 0 && v == 0) return false;
        op[x][y] = v;
        invL[x][v] = y;
        row_used[x] |= (1u << v);
        return true;
    }
};

// Propagate all Equation 677 and derived identities until fixed point or contradiction
bool propagate(State& st) {
    int n = st.n;
    bool changed = true;
    while (changed) {
        changed = false;
        // 1. If N-1 entries in row x are assigned, the last one is forced
        for (int x = 0; x < n; ++x) {
            if (__builtin_popcount(st.row_used[x]) == n - 1) {
                int missing_val = __builtin_ctz((~st.row_used[x]) & ((1u << n) - 1));
                for (int y = 0; y < n; ++y) {
                    if (st.op[x][y] == -1) {
                        if (!st.assign(x, y, missing_val)) return false;
                        changed = true;
                        break;
                    }
                }
            }
        }

        // 2. Equation 677: y ◇ (x ◇ ((y ◇ x) ◇ y)) = x
        //    Equivalent to: x ◇ ((y ◇ x) ◇ y) = invL[y][x]
        //    and:           (y ◇ x) ◇ y = invL[x][ invL[y][x] ]
        for (int x = 0; x < n; ++x) {
            for (int y = 0; y < n; ++y) {
                int yx = st.op[y][x];
                int ly_inv_x = st.invL[y][x]; // u such that y ◇ u = x
                int yxy = (yx != -1) ? st.op[yx][y] : -1;

                if (yxy != -1) {
                    int xyxy = st.op[x][yxy];
                    if (xyxy != -1) {
                        if (st.op[y][xyxy] == -1) {
                            if (!st.assign(y, xyxy, x)) return false;
                            changed = true;
                        } else if (st.op[y][xyxy] != x) {
                            return false;
                        }
                    }
                    if (ly_inv_x != -1) {
                        if (st.op[x][yxy] == -1) {
                            if (!st.assign(x, yxy, ly_inv_x)) return false;
                            changed = true;
                        } else if (st.op[x][yxy] != ly_inv_x) {
                            return false;
                        }
                    }
                }

                if (ly_inv_x != -1) {
                    int lx_inv_u = st.invL[x][ly_inv_x]; // w such that x ◇ w = ly_inv_x
                    if (lx_inv_u != -1 && yx != -1) {
                        if (st.op[yx][y] == -1) {
                            if (!st.assign(yx, y, lx_inv_u)) return false;
                            changed = true;
                        } else if (st.op[yx][y] != lx_inv_u) {
                            return false;
                        }
                    }
                }
            }
        }

        // 3. Backward recurrence: x = (y ◇ x) ◇ ((y ◇ (y ◇ x)) ◇ y)
        //    Equivalent to: (y ◇ (y ◇ x)) ◇ y = invL[y ◇ x][x]
        for (int x = 0; x < n; ++x) {
            for (int y = 0; y < n; ++y) {
                int yx = st.op[y][x];
                if (yx == -1) continue;
                int yyx = st.op[y][yx];
                int inv_yx_x = st.invL[yx][x];
                if (yyx != -1 && inv_yx_x != -1) {
                    if (st.op[yyx][y] == -1) {
                        if (!st.assign(yyx, y, inv_yx_x)) return false;
                        changed = true;
                    } else if (st.op[yyx][y] != inv_yx_x) {
                        return false;
                    }
                }
                if (yyx != -1 && st.op[yyx][y] != -1) {
                    int w = st.op[yyx][y];
                    if (st.op[yx][w] == -1) {
                        if (!st.assign(yx, w, x)) return false;
                        changed = true;
                    } else if (st.op[yx][w] != x) {
                        return false;
                    }
                }
            }
        }

        // 4. Fixer uniqueness: if y ◇ x = x, then y = (x ◇ x) ◇ x
        //    and by Issue #1464 lemma: if (c ◇ c) ◇ c = c ◇ c, then c ◇ c = c.
        for (int x = 0; x < n; ++x) {
            int xx = st.op[x][x];
            int xxx = (xx != -1) ? st.op[xx][x] : -1;
            if (xx != -1 && xxx != -1 && xxx == xx && xx != x) {
                return false;
            }
            for (int y = 0; y < n; ++y) {
                if (st.op[y][x] == x) {
                    if (xxx != -1 && xxx != y) return false;
                    if (xx != -1 && st.op[xx][x] == -1) {
                        if (!st.assign(xx, x, y)) return false;
                        changed = true;
                    }
                }
            }
        }
    }
    return true;
}

bool solve_rec(State& st) {
    st.nodes++;
    if (!propagate(st)) return false;

    int n = st.n;
    // Compute mask of touched labels (labels that appear as row, col, or value of any assigned entry)
    uint16_t touched = 1u; // 0 is always touched
    for (int x = 0; x < n; ++x) {
        if (st.row_used[x] != 0) {
            touched |= (1u << x) | st.row_used[x];
            for (int y = 0; y < n; ++y) {
                if (st.op[x][y] != -1) {
                    touched |= (1u << y);
                }
            }
        }
    }

    int best_x = -1, best_y = -1, best_cnt = 1000000;
    for (int x = 0; x < n; ++x) {
        int rem = n - __builtin_popcount(st.row_used[x]);
        if (rem == 0) continue;
        bool x_touched = (touched >> x) & 1;
        for (int y = 0; y < n; ++y) {
            if (st.op[x][y] == -1) {
                bool y_touched = (touched >> y) & 1;
                int score = rem * 2 + (x_touched ? 0 : 10) + (y_touched ? 0 : 10);
                if (score < best_cnt) {
                    best_cnt = score;
                    best_x = x;
                    best_y = y;
                }
            }
        }
    }
    if (best_x == -1) {
        return true; // Complete table found!
    }

    // All labels not in (touched | (1<<best_x) | (1<<best_y)) are mutually symmetric;
    // we only need to try at most the first such untouched label.
    uint16_t active = touched | (1u << best_x) | (1u << best_y);
    bool tried_untouched = false;
    for (int v = 0; v < n; ++v) {
        if ((st.row_used[best_x] >> v) & 1) continue;
        if (st.forbid_zero_fixer && best_y == 0 && v == 0) continue;
        bool is_active = (active >> v) & 1;
        if (!is_active) {
            if (tried_untouched) continue;
            tried_untouched = true;
        }
        State next = st;
        next.nodes = 0;
        if (next.assign(best_x, best_y, v)) {
            if (solve_rec(next)) {
                uint64_t tot = st.nodes + next.nodes;
                st = next;
                st.nodes = tot;
                return true;
            }
        }
        st.nodes += next.nodes;
    }
    return false;
}

int main(int argc, char** argv) {
    std::cout << "=== Part 1: Calibration (Full Eq677 Spectrum Search for n=1..8) ===" << std::endl;
    for (int n = 1; n <= 8; ++n) {
        auto t0 = std::chrono::steady_clock::now();
        State st;
        st.init(n, false); // allow y ◇ 0 == 0
        bool sat = solve_rec(st);
        auto t1 = std::chrono::steady_clock::now();
        double sec = std::chrono::duration<double>(t1 - t0).count();
        std::cout << "Calibrate n=" << n
                  << " | model_exists=" << (sat ? "YES" : "NO")
                  << " | nodes=" << st.nodes
                  << " | time=" << sec << "s" << std::endl;
    }

    int max_n = (argc > 1) ? std::atoi(argv[1]) : 9;
    std::cout << "\n=== Part 2: Exhaustive Orbit-Case Counterexample Search for Eq677 => Eq255 (n=2.." << max_n << ") ===" << std::endl;
    for (int n = 2; n <= max_n; ++n) {
        auto t0 = std::chrono::steady_clock::now();
        int total_orbits = (n - 1) * n / 2;
        int prop_killed = 0;
        uint64_t total_nodes = 0;
        bool found = false;

        std::vector<std::pair<int, int>> orbits;
        for (int k = 1; k < n; ++k) {
            for (int s = 1; s <= k; ++s) {
                orbits.push_back({k, s});
            }
        }

        #pragma omp parallel for schedule(dynamic, 1) reduction(+:prop_killed, total_nodes)
        for (size_t idx = 0; idx < orbits.size(); ++idx) {
            int k = orbits[idx].first;
            int s = orbits[idx].second;
            State st;
            st.init(n, true);
            bool ok = true;
            for (int i = 0; i < k; ++i) {
                if (!st.assign(i, 0, i + 1)) ok = false;
            }
            if (ok && !st.assign(k, 0, s)) ok = false;
            if (ok && !propagate(st)) {
                ok = false;
                prop_killed++;
            }
            if (ok) {
                if (solve_rec(st)) {
                    #pragma omp critical
                    {
                        std::cout << "FOUND COUNTEREXAMPLE at n=" << n << " k=" << k << " s=" << s << std::endl;
                        found = true;
                    }
                }
                total_nodes += st.nodes;
            }
        }
        auto t1 = std::chrono::steady_clock::now();
        double sec = std::chrono::duration<double>(t1 - t0).count();
        std::cout << "n=" << n
                  << " | orbits=" << total_orbits
                  << " | killed_at_root_by_prop=" << prop_killed << "/" << total_orbits
                  << " | total_nodes=" << total_nodes
                  << " | status=" << (found ? "SAT" : "UNSAT")
                  << " | time=" << sec << "s" << std::endl;
    }
    return 0;
}
