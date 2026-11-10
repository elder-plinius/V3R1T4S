#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

/*
 * Fast Exact + Randomized-Restart / Backtracking Solver for Linear OOA(3^m, s, F_3, 2, k)
 * over F_3 (depth T = 2).
 *
 * Vector encoding: x in 0 .. 3^m - 1 (base-3 digits d_0 .. d_{m-1} in {0,1,2}).
 * Precomputed addition table add3[x][y] and negation neg3[x] for m <= 9 (3^9 = 19,683).
 */
#define MAX_M 9
#define MAX_POW3 19683
#define MAX_S 20

static int POW3[MAX_M + 1];
static uint16_t *ADD3 = NULL; /* [POW3[m] * POW3[m]] when m <= 8, or helper */
static int g_m, g_N, g_s, g_k;

static inline int vec_add(int x, int y) {
    int res = 0, p = 1;
    for (int i = 0; i < g_m; i++) {
        int s = (x % 3) + (y % 3);
        if (s >= 3) s -= 3;
        res += s * p;
        x /= 3; y /= 3; p *= 3;
    }
    return res;
}

static inline int vec_sub(int x, int y) {
    int res = 0, p = 1;
    for (int i = 0; i < g_m; i++) {
        int s = (x % 3) - (y % 3);
        if (s < 0) s += 3;
        res += s * p;
        x /= 3; y /= 3; p *= 3;
    }
    return res;
}

static void init_f3(int m) {
    g_m = m;
    POW3[0] = 1;
    for (int i = 1; i <= m; i++) POW3[i] = POW3[i - 1] * 3;
    g_N = POW3[m];
    if (ADD3) { free(ADD3); ADD3 = NULL; }
    if (g_N <= 6561) {
        ADD3 = malloc((size_t)g_N * (size_t)g_N * sizeof(uint16_t));
        for (int x = 0; x < g_N; x++)
            for (int y = 0; y < g_N; y++)
                ADD3[(size_t)x * (size_t)g_N + (size_t)y] = (uint16_t)vec_add(x, y);
    }
}

static inline int fast_add(int x, int y) {
    if (ADD3) return ADD3[(size_t)x * (size_t)g_N + (size_t)y];
    return vec_add(x, y);
}

/* Canonical representative under scalar multiplication {1, 2} in F_3^*: first non-zero coord == 1 */
static int is_proj_rep(int x) {
    if (x == 0) return 0;
    while (x > 0) {
        int d = x % 3;
        if (d != 0) return (d == 1);
        x /= 3;
    }
    return 0;
}

static void apply_block_dp(const uint8_t * restrict cur_cost, int u, int v, uint8_t * restrict nxt_cost, int k_lim) {
    int u2 = fast_add(u, u);
    int v2 = fast_add(v, v);
    int vu = fast_add(v, u);
    int vu2 = fast_add(v, u2);
    int v2u = fast_add(v2, u);
    int v2u2 = fast_add(v2, u2);

    memcpy(nxt_cost, cur_cost, (size_t)g_N);
    for (int x = 0; x < g_N; x++) {
        uint8_t c = cur_cost[x];
        if (c >= k_lim) continue;
        uint8_t c1 = (uint8_t)(c + 1);
        int y1 = fast_add(x, u);
        if (c1 < nxt_cost[y1]) nxt_cost[y1] = c1;
        int y2 = fast_add(x, u2);
        if (c1 < nxt_cost[y2]) nxt_cost[y2] = c1;

        if (c + 2 <= k_lim) {
            uint8_t c2 = (uint8_t)(c + 2);
            int z1 = fast_add(x, v);    if (c2 < nxt_cost[z1]) nxt_cost[z1] = c2;
            int z2 = fast_add(x, v2);   if (c2 < nxt_cost[z2]) nxt_cost[z2] = c2;
            int z3 = fast_add(x, vu);   if (c2 < nxt_cost[z3]) nxt_cost[z3] = c2;
            int z4 = fast_add(x, vu2);  if (c2 < nxt_cost[z4]) nxt_cost[z4] = c2;
            int z5 = fast_add(x, v2u);  if (c2 < nxt_cost[z5]) nxt_cost[z5] = c2;
            int z6 = fast_add(x, v2u2); if (c2 < nxt_cost[z6]) nxt_cost[z6] = c2;
        }
    }
}

static inline int block_valid(const uint8_t * restrict cur_cost, int u, int v, int k) {
    if (u == 0 || v == 0 || cur_cost[u] < k) return 0;
    if (cur_cost[v] < k - 1) return 0;
    int vu = fast_add(v, u);
    if (vu == 0 || cur_cost[vu] < k - 1) return 0;
    int u2 = fast_add(u, u);
    int vu2 = fast_add(v, u2);
    if (vu2 == 0 || cur_cost[vu2] < k - 1) return 0;
    return 1;
}

static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return (rng_state = x);
}

static int sol_u[MAX_S], sol_v[MAX_S];
static uint8_t dp_stack[MAX_S + 1][MAX_POW3];
static uint64_t g_nodes = 0, g_node_cap = 0;

static int dfs_search(int blk_idx, int fixed_blocks, int randomize) {
    if (blk_idx == g_s) return 1;
    if (g_node_cap && ++g_nodes > g_node_cap) return 0;

    const uint8_t *cur = dp_stack[blk_idx];

    /* Collect valid projective u candidates */
    int u_list[MAX_POW3];
    int n_u = 0;
    for (int u = 1; u < g_N; u++) {
        if (!is_proj_rep(u)) continue;
        if (cur[u] >= g_k) {
            /* symmetry break when not randomized: u >= sol_u[blk_idx-1] if after fixed blocks?
               Careful: blocks can be permuted! So sol_u[fixed_blocks .. s-1] CAN be sorted in non-decreasing order! */
            if (!randomize && blk_idx > fixed_blocks && u < sol_u[blk_idx - 1]) continue;
            u_list[n_u++] = u;
        }
    }
    if (n_u == 0) return 0;

    if (randomize) {
        for (int i = n_u - 1; i > 0; i--) {
            int j = (int)(xorshift64() % (uint64_t)(i + 1));
            int t = u_list[i]; u_list[i] = u_list[j]; u_list[j] = t;
        }
    }

    int u_try_lim = (randomize && blk_idx > fixed_blocks + 1 && n_u > 24) ? 24 : n_u;
    for (int ui = 0; ui < u_try_lim; ui++) {
        int u = u_list[ui];
        int v_list[MAX_POW3];
        int n_v = 0;
        for (int v = 1; v < g_N; v++) {
            /* Note: scaling v by 2 in F_3^* preserves span(u) and span(u, v), so we ONLY need is_proj_rep(v)!! */
            if (!is_proj_rep(v)) continue;
            if (block_valid(cur, u, v, g_k)) v_list[n_v++] = v;
        }
        if (n_v == 0) continue;
        if (randomize) {
            for (int i = n_v - 1; i > 0; i--) {
                int j = (int)(xorshift64() % (uint64_t)(i + 1));
                int t = v_list[i]; v_list[i] = v_list[j]; v_list[j] = t;
            }
        }
        int v_try_lim = (randomize && blk_idx > fixed_blocks + 1 && n_v > 24) ? 24 : n_v;
        for (int vi = 0; vi < v_try_lim; vi++) {
            int v = v_list[vi];
            sol_u[blk_idx] = u;
            sol_v[blk_idx] = v;
            apply_block_dp(cur, u, v, dp_stack[blk_idx + 1], g_k);
            if (dfs_search(blk_idx + 1, fixed_blocks, randomize)) return 1;
            if (g_node_cap && g_nodes > g_node_cap) return 0;
        }
    }
    return 0;
}

static void print_vec(int x, int m) {
    printf("[");
    for (int i = 0; i < m; i++) {
        printf("%d%s", x % 3, (i + 1 == m) ? "" : ",");
        x /= 3;
    }
    printf("]");
}

static int try_cell(int m, int s, int k, int exhaustive_if_small) {
    init_f3(m);
    g_s = s; g_k = k;

    memset(dp_stack[0], 255, (size_t)g_N);
    dp_stack[0][0] = 0;

    /* Canonical GL_m(F_3) prefix: fix floor(k/2) full blocks [e_{2i}, e_{2i+1}] */
    int full_b = k / 2;
    for (int b = 0; b < full_b; b++) {
        int u = POW3[2 * b];
        int v = POW3[2 * b + 1];
        sol_u[b] = u; sol_v[b] = v;
        apply_block_dp(dp_stack[b], u, v, dp_stack[b + 1], k);
    }

    if (exhaustive_if_small) {
        /* If k is odd, we can ALSO fix sol_u[full_b] = e_{k-1}! Let's handle odd k directly! */
        g_nodes = 0; g_node_cap = 20000000ULL;
        if (k % 2 == 1) {
            int b = full_b;
            int u = POW3[k - 1];
            sol_u[b] = u;
            /* Also by remaining GL(m - k) basis freedom, if k < m, either v in span(e_0..e_{k-1}) OR v = e_k! */
            for (int v = 1; v < g_N; v++) {
                if (!is_proj_rep(v)) continue;
                /* Check if coords k..m-1 are non-zero: if so, WLOG coords k..m-1 == e_k (i.e. v / 3^k == 1 and arbitrary on 0..k-1? Even simpler: try all proj_rep v with coords k+1..m-1 == 0!) */
                if ((v / POW3[k + 1 < m ? k + 1 : m]) != 0) continue;
                if (!block_valid(dp_stack[b], u, v, k)) continue;
                sol_v[b] = v;
                apply_block_dp(dp_stack[b], u, v, dp_stack[b + 1], k);
                if (dfs_search(b + 1, b + 1, 0)) {
                    printf("FOUND EXHAUSTIVE OOA(3^%d, %d, F_3, 2, %d)! nodes=%llu\n", m, s, k, (unsigned long long)g_nodes);
                    return 1;
                }
            }
            if (g_nodes <= g_node_cap) {
                printf("EXHAUSTIVELY UNSAT OOA(3^%d, %d, F_3, 2, %d) in %llu nodes!\n", m, s, k, (unsigned long long)g_nodes);
                return -1;
            }
        } else {
            if (dfs_search(full_b, full_b, 0)) {
                printf("FOUND EXHAUSTIVE OOA(3^%d, %d, F_3, 2, %d)! nodes=%llu\n", m, s, k, (unsigned long long)g_nodes);
                return 1;
            }
            if (g_nodes <= g_node_cap) {
                printf("EXHAUSTIVELY UNSAT OOA(3^%d, %d, F_3, 2, %d) in %llu nodes!\n", m, s, k, (unsigned long long)g_nodes);
                return -1;
            }
        }
    }

    /* Randomized restarts (200 restarts x 50,000 nodes each) */
    for (int rest = 0; rest < 80; rest++) {
        g_nodes = 0; g_node_cap = 8000ULL;
        int start_b = full_b;
        if (k % 2 == 1) {
            int u = POW3[k - 1];
            sol_u[start_b] = u;
            int v_cands[MAX_POW3], nv = 0;
            for (int v = 1; v < g_N; v++) {
                if (!is_proj_rep(v)) continue;
                if (block_valid(dp_stack[start_b], u, v, k)) v_cands[nv++] = v;
            }
            if (nv == 0) break;
            int v = v_cands[xorshift64() % (uint64_t)nv];
            sol_v[start_b] = v;
            apply_block_dp(dp_stack[start_b], u, v, dp_stack[start_b + 1], k);
            start_b++;
        }
        if (dfs_search(start_b, start_b, 1)) {
            printf("FOUND RANDOMIZED OOA(3^%d, %d, F_3, 2, %d) on restart %d!\n", m, s, k, rest);
            for (int b = 0; b < s; b++) {
                printf("  Block %2d: u=", b); print_vec(sol_u[b], m);
                printf(" v="); print_vec(sol_v[b], m); printf("\n");
            }
            return 1;
        }
    }
    fflush(stdout); printf("MISS OOA(3^%d, %d, F_3, 2, %d) after 250 restarts.\n", m, s, k);
    return 0;
}

int main(void) {
    /* Candidate base-3 depth-2 gap cells (m, s, target_k = m - live_t + 1) */
    printf("--- Probing Base-3 Depth-2 MinT Gap Cells ---\n");
    fflush(stdout);
    if (try_cell(6, 8, 5, 0) == 1) goto done;
    fflush(stdout);
    if (try_cell(8, 8, 7, 0) == 1) goto done;
    if (try_cell(7, 12, 5, 0) == 1) goto done;
    if (try_cell(8, 10, 6, 0) == 1) goto done;
    if (try_cell(9, 10, 7, 0) == 1) goto done;
    if (try_cell(8, 19, 5, 0) == 1) goto done;
    if (try_cell(9, 14, 6, 0) == 1) goto done;
    if (try_cell(10, 9, 8, 0) == 1) goto done;
    if (try_cell(10, 12, 7, 0) == 1) goto done;
done:
    if (ADD3) free(ADD3);
    return 0;
}
