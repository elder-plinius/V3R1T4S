/*
 * snake_coil_opt.c — Native C 512-Bit Bitboard Evaluator, Optimizer & Sparse-Coordinate Lifter
 *
 * Modes:
 *   1. lift_coil  [n_in] [seed_file] [out_prefix]
 *      Unrestricted Reversed-Layer Sparse-Coordinate Coil Lifter (Q_{n_in} -> Q_{n_in+1})
 *   2. lift_snake [n_in] [seed_file] [out_prefix]
 *      Single-Flip Sparse-Coordinate Snake Doubling Lifter (Q_{n_in} -> Q_{n_in+1})
 *   3. drift_opt  [n] [is_coil] [seed_file] [out_file]
 *      Window-DFS Neutral Drift (p3 inequivalent equal-record generator) + Positive-Gain Search
 *   4. boost_coil [n] <b36_coil_file> [out_prefix]
 *      Deep +2/+4 Window & Neutral-Perturbation Booster on a lifted coil in Q_n
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#define MAX_N 14
#define MAX_V (1 << MAX_N)
#define MAX_LEN 8192
#define MAX_K 512

typedef struct {
    uint64_t w[8];
} u512;

static inline u512 u512_zero(void) { return (u512){{0,0,0,0,0,0,0,0}}; }
static inline bool u512_is_zero(u512 a) {
    return (a.w[0]|a.w[1]|a.w[2]|a.w[3]|a.w[4]|a.w[5]|a.w[6]|a.w[7]) == 0;
}
static inline bool u512_eq(u512 a, u512 b) {
    return ((a.w[0]^b.w[0])|(a.w[1]^b.w[1])|(a.w[2]^b.w[2])|(a.w[3]^b.w[3])|
            (a.w[4]^b.w[4])|(a.w[5]^b.w[5])|(a.w[6]^b.w[6])|(a.w[7]^b.w[7])) == 0;
}
static inline u512 u512_or(u512 a, u512 b) {
    u512 r;
    for (int i = 0; i < 8; i++) r.w[i] = a.w[i] | b.w[i];
    return r;
}
static inline u512 u512_and(u512 a, u512 b) {
    u512 r;
    for (int i = 0; i < 8; i++) r.w[i] = a.w[i] & b.w[i];
    return r;
}
static inline u512 u512_andnot(u512 a, u512 b) {
    u512 r;
    for (int i = 0; i < 8; i++) r.w[i] = a.w[i] & ~b.w[i];
    return r;
}
static inline void u512_set(u512 *a, int bit) { a->w[bit >> 6] |= (1ULL << (bit & 63)); }
static inline int u512_test(u512 a, int bit) { return (int)((a.w[bit >> 6] >> (bit & 63)) & 1ULL); }
static inline int u512_popcnt(u512 a) {
    int s = 0;
    for (int i = 0; i < 8; i++) s += __builtin_popcountll(a.w[i]);
    return s;
}
static inline int u512_ctz(u512 a) {
    for (int i = 0; i < 8; i++) {
        if (a.w[i]) return (i << 6) + __builtin_ctzll(a.w[i]);
    }
    return 512;
}
static inline void u512_clear_lsb(u512 *a) {
    for (int i = 0; i < 8; i++) {
        if (a->w[i]) { a->w[i] &= a->w[i] - 1; return; }
    }
}
static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return *s = x;
}

typedef struct {
    int n;
    int N;
    uint64_t rng;
    int used[MAX_V];
    int cnt[MAX_V];
    int K;
    int w_verts[MAX_K];
    int d1[MAX_K];
    u512 adj[MAX_K];
    u512 even_mask;
    u512 odd_mask;
    u512 orig_mask;
    int nodes;
    int limit;
    int route_idx[MAX_K];
    int route_len;
} Engine;

static void add_vert(Engine *s, int v, int sign) {
    s->used[v] += sign;
    int n = s->n;
    for (int b = 0; b < n; b++) {
        s->cnt[v ^ (1 << b)] += sign;
    }
}

static bool verify_coil_ring(int n, const int *ring, int L) {
    int N = 1 << n;
    int *pos = (int *)malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) pos[i] = -1;
    for (int i = 0; i < L; i++) {
        int u = ring[i];
        int v = ring[(i + 1) % L];
        int diff = u ^ v;
        if (diff <= 0 || (diff & (diff - 1)) != 0) { free(pos); return false; }
        if (pos[u] != -1) { free(pos); return false; }
        pos[u] = i;
    }
    for (int i = 0; i < L; i++) {
        int u = ring[i];
        for (int b = 0; b < n; b++) {
            int j = pos[u ^ (1 << b)];
            if (j != -1) {
                int d = (i - j + L) % L;
                if (d != 1 && d != L - 1) { free(pos); return false; }
            }
        }
    }
    free(pos);
    return true;
}

static bool verify_snake_verts(int n, const int *verts, int L) {
    int N = 1 << n;
    int *pos = (int *)malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) pos[i] = -1;
    for (int i = 0; i <= L; i++) {
        int u = verts[i];
        if (i < L) {
            int v = verts[i + 1];
            int diff = u ^ v;
            if (diff <= 0 || (diff & (diff - 1)) != 0) { free(pos); return false; }
        }
        if (pos[u] != -1) { free(pos); return false; }
        pos[u] = i;
    }
    for (int i = 0; i <= L; i++) {
        int u = verts[i];
        for (int b = 0; b < n; b++) {
            int j = pos[u ^ (1 << b)];
            if (j != -1 && abs(i - j) != 1) { free(pos); return false; }
        }
    }
    free(pos);
    return true;
}

static void save_coil_file(const char *fn, const int *ring, int L) {
    FILE *f = fopen(fn, "w");
    if (!f) return;
    const char *b36 = "0123456789abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < L; i++) {
        int diff = ring[i] ^ ring[(i + 1) % L];
        int step = __builtin_ctz((unsigned)diff);
        fputc(b36[step], f);
    }
    fputc('\n', f);
    fclose(f);
}

static void save_snake_file(const char *fn, const int *verts, int L) {
    FILE *f = fopen(fn, "w");
    if (!f) return;
    const char *b36 = "0123456789abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < L; i++) {
        int diff = verts[i] ^ verts[i + 1];
        int step = __builtin_ctz((unsigned)diff);
        fputc(b36[step], f);
    }
    fputc('\n', f);
    fclose(f);
}

static bool bitset_dfs(Engine *s, int u, int rem, u512 avail, u512 visited_mask) {
    if (++s->nodes > s->limit) return false;
    if (rem == 2) {
        u512 cands = u512_and(u512_and(s->adj[u], s->adj[1]), avail);
        while (!u512_is_zero(cands)) {
            int v = u512_ctz(cands);
            u512_clear_lsb(&cands);
            u512 final_mask = visited_mask;
            u512_set(&final_mask, v);
            if (!u512_is_zero(s->orig_mask) && u512_eq(final_mask, s->orig_mask)) continue;
            s->route_idx[s->route_len++] = v;
            return true;
        }
        return false;
    }
    u512 goal_nbrs = u512_and(s->adj[1], avail);
    if (u512_is_zero(goal_nbrs)) return false;
    if (rem >= 4) {
        u512 reach = u512_zero(); u512_set(&reach, u);
        int dist_goal = -1, step = 1;
        u512 cur_f = u512_and(s->adj[u], avail);
        while (!u512_is_zero(cur_f)) {
            if (dist_goal < 0 && !u512_is_zero(u512_and(cur_f, goal_nbrs))) dist_goal = step + 1;
            reach = u512_or(reach, cur_f);
            if (step >= rem - 1) break;
            u512 nxt = u512_zero(), tmp = cur_f;
            while (!u512_is_zero(tmp)) {
                int idx = u512_ctz(tmp);
                u512_clear_lsb(&tmp);
                nxt = u512_or(nxt, s->adj[idx]);
            }
            cur_f = u512_andnot(u512_and(nxt, avail), reach);
            step++;
        }
        if (dist_goal < 0 || dist_goal > rem) return false;
        int u_par = u512_test(s->even_mask, u);
        int need_opp = rem / 2, need_same = (rem - 1) / 2;
        u512 u_bit = u512_zero(); u512_set(&u_bit, u);
        u512 interior_reach = u512_andnot(reach, u_bit);
        int cnt_even = u512_popcnt(u512_and(interior_reach, s->even_mask));
        int cnt_odd  = u512_popcnt(u512_and(interior_reach, s->odd_mask));
        if (u_par == 1) { if (cnt_odd < need_opp || cnt_even < need_same) return false; }
        else { if (cnt_even < need_opp || cnt_odd < need_same) return false; }
    }
    u512 cands = u512_andnot(u512_and(s->adj[u], avail), s->adj[1]);
    if (u512_is_zero(cands)) return false;
    int cand_list[16], nc = 0;
    while (!u512_is_zero(cands)) {
        int v = u512_ctz(cands);
        u512_clear_lsb(&cands);
        if (s->d1[v] <= rem - 1) cand_list[nc++] = v;
    }
    if (nc == 0) return false;
    for (int i = nc - 1; i > 0; i--) {
        int j = (int)(xorshift64(&s->rng) % (uint64_t)(i + 1));
        int tmp = cand_list[i]; cand_list[i] = cand_list[j]; cand_list[j] = tmp;
    }
    u512 block_u = s->adj[u];
    for (int idx = 0; idx < nc; idx++) {
        int v = cand_list[idx];
        u512 v_bit = u512_zero(); u512_set(&v_bit, v);
        u512 forbid = u512_or(block_u, v_bit);
        u512 next_avail = u512_andnot(avail, forbid);
        s->route_idx[s->route_len++] = v;
        if (bitset_dfs(s, v, rem - 1, next_avail, u512_or(visited_mask, v_bit))) return true;
        s->route_len--;
        if (s->nodes > s->limit) break;
    }
    return false;
}

static bool solve_candidate_graph(Engine *s, int start_v, int target_v, int new_w, int budget,
                                  const int *forbid_layer, const int *orig_interior, int orig_int_len) {
    int *cand_v = (int *)malloc(sizeof(int) * s->N);
    int *v_to_idx = (int *)malloc(sizeof(int) * s->N);
    for (int v = 0; v < s->N; v++) v_to_idx[v] = -1;
    cand_v[0] = start_v; v_to_idx[start_v] = 0;
    cand_v[1] = target_v; v_to_idx[target_v] = 1;
    int M = 2;
    for (int v = 0; v < s->N; v++) {
        if (s->used[v]) continue;
        if (forbid_layer && forbid_layer[v]) continue;
        int d_s = __builtin_popcount((unsigned)(v ^ start_v));
        int d_t = __builtin_popcount((unsigned)(v ^ target_v));
        if (d_s + d_t > new_w) continue;
        int adj_s = (d_s == 1), adj_t = (d_t == 1);
        if (adj_s + adj_t == 2 && new_w != 2) continue;
        if (s->cnt[v] != adj_s + adj_t) continue;
        cand_v[M] = v; v_to_idx[v] = M; M++;
    }
    int *dist0 = (int *)malloc(sizeof(int) * M);
    int *dist1 = (int *)malloc(sizeof(int) * M);
    int *q = (int *)malloc(sizeof(int) * M);
    for (int i = 0; i < M; i++) { dist0[i] = 999999; dist1[i] = 999999; }
    int qh = 0, qt = 0;
    dist0[0] = 0; q[qt++] = 0;
    while (qh < qt) {
        int u_idx = q[qh++], d = dist0[u_idx];
        if (d >= new_w - 1) continue;
        int u = cand_v[u_idx];
        for (int b = 0; b < s->n; b++) {
            int nb = v_to_idx[u ^ (1 << b)];
            if (nb >= 0 && dist0[nb] > d + 1) { dist0[nb] = d + 1; if (nb != 1) q[qt++] = nb; }
        }
    }
    if (dist0[1] > new_w) { free(cand_v); free(v_to_idx); free(dist0); free(dist1); free(q); return false; }
    qh = 0; qt = 0; dist1[1] = 0; q[qt++] = 1;
    while (qh < qt) {
        int u_idx = q[qh++], d = dist1[u_idx];
        if (d >= new_w - 1) continue;
        int u = cand_v[u_idx];
        for (int b = 0; b < s->n; b++) {
            int nb = v_to_idx[u ^ (1 << b)];
            if (nb >= 0 && dist1[nb] > d + 1) { dist1[nb] = d + 1; if (nb != 0) q[qt++] = nb; }
        }
    }
    char *keep = (char *)calloc(M, 1);
    keep[0] = 1; keep[1] = 1;
    /* If too many vertices satisfy dist0 + dist1 <= new_w, tighten threshold until <= MAX_K - 2 */
    int max_sum = new_w;
    while (max_sum >= dist0[1]) {
        int cnt_k = 0;
        for (int i = 2; i < M; i++) {
            if (dist0[i] + dist1[i] <= max_sum) cnt_k++;
        }
        if (cnt_k <= MAX_K - 2 || max_sum == dist0[1]) break;
        max_sum -= 2;
    }
    for (int i = 2; i < M; i++) if (dist0[i] + dist1[i] <= max_sum) keep[i] = 1;
    bool changed = true;
    while (changed) {
        changed = false;
        for (int i = 2; i < M; i++) {
            if (!keep[i]) continue;
            int u = cand_v[i], deg = 0;
            for (int b = 0; b < s->n; b++) {
                int nb = v_to_idx[u ^ (1 << b)];
                if (nb >= 0 && keep[nb]) deg++;
            }
            if (deg < 2) { keep[i] = 0; changed = true; }
        }
    }
    int K = 2;
    s->w_verts[0] = start_v; s->w_verts[1] = target_v;
    s->d1[0] = dist1[0]; s->d1[1] = 0;
    for (int v = 0; v < s->N; v++) v_to_idx[v] = -1;
    v_to_idx[start_v] = 0; v_to_idx[target_v] = 1;
    for (int i = 2; i < M && K < MAX_K; i++) {
        if (keep[i]) {
            s->w_verts[K] = cand_v[i]; s->d1[K] = dist1[i]; v_to_idx[cand_v[i]] = K; K++;
        }
    }
    free(cand_v); free(dist0); free(dist1); free(keep); free(q);
    if (K - 2 < new_w - 1) { free(v_to_idx); return false; }
    s->K = K;
    s->even_mask = u512_zero(); s->odd_mask = u512_zero();
    for (int i = 0; i < K; i++) {
        s->adj[i] = u512_zero();
        int u = s->w_verts[i];
        if (__builtin_popcount((unsigned)u) & 1) u512_set(&s->odd_mask, i);
        else u512_set(&s->even_mask, i);
        for (int b = 0; b < s->n; b++) {
            int nb = v_to_idx[u ^ (1 << b)];
            if (nb >= 0) u512_set(&s->adj[i], nb);
        }
    }
    s->orig_mask = u512_zero();
    if (orig_interior && orig_int_len > 0) {
        bool all_in = true;
        for (int k = 0; k < orig_int_len; k++) {
            int idx = v_to_idx[orig_interior[k]];
            if (idx >= 2) u512_set(&s->orig_mask, idx);
            else all_in = false;
        }
        if (!all_in) s->orig_mask = u512_zero();
    }
    free(v_to_idx);
    u512 avail = u512_zero();
    for (int i = 2; i < K; i++) u512_set(&avail, i);
    s->route_len = 0; s->nodes = 0; s->limit = budget;
    return bitset_dfs(s, 0, new_w, avail, u512_zero());
}

static bool coil_window_replace(Engine *s, int *ring, int *L_ptr, int a, int w, int gain,
                                int budget, const int *forbid_layer, bool forbid_orig) {
    int L = *L_ptr, new_w = w + gain;
    if (w < 2 || w > L - 4 || new_w < 2 || new_w > 200) return false;
    int start_v = ring[a % L], target_v = ring[(a + w) % L];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;

    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    for (int i = 0; i < L; i++) add_vert(s, ring[i], 1);
    int orig_int[256];
    for (int k = 1; k < w; k++) {
        int v = ring[(a + k) % L];
        add_vert(s, v, -1);
        orig_int[k - 1] = v;
    }

    if (!solve_candidate_graph(s, start_v, target_v, new_w, budget, forbid_layer,
                               forbid_orig ? orig_int : NULL, w - 1)) {
        return false;
    }

    int new_L = L + gain;
    int new_ring[MAX_LEN];
    new_ring[0] = start_v;
    for (int k = 0; k < new_w - 1; k++) new_ring[k + 1] = s->w_verts[s->route_idx[k]];
    for (int k = w; k < L; k++) new_ring[new_w + (k - w)] = ring[(a + k) % L];
    int rot_back = (new_L - (a % new_L)) % new_L;
    for (int i = 0; i < new_L; i++) ring[i] = new_ring[(i + rot_back) % new_L];
    *L_ptr = new_L;
    return true;
}

static bool snake_window_replace(Engine *s, int *verts, int *L_ptr, int a, int w, int gain,
                                 int budget, const int *forbid_layer, bool forbid_orig) {
    int L = *L_ptr, new_w = w + gain;
    if (a < 0 || a + w > L || w < 2 || new_w < 2 || new_w > 200) return false;
    int start_v = verts[a], target_v = verts[a + w];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;

    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    for (int i = 0; i <= L; i++) add_vert(s, verts[i], 1);
    int orig_int[256];
    for (int k = 1; k < w; k++) {
        int v = verts[a + k];
        add_vert(s, v, -1);
        orig_int[k - 1] = v;
    }

    if (!solve_candidate_graph(s, start_v, target_v, new_w, budget, forbid_layer,
                               forbid_orig ? orig_int : NULL, w - 1)) {
        return false;
    }

    int new_L = L + gain;
    int new_verts[MAX_LEN];
    int idx = 0;
    for (int i = 0; i <= a; i++) new_verts[idx++] = verts[i];
    for (int k = 0; k < new_w - 1; k++) new_verts[idx++] = s->w_verts[s->route_idx[k]];
    for (int i = a + w; i <= L; i++) new_verts[idx++] = verts[i];
    memcpy(verts, new_verts, sizeof(int) * (new_L + 1));
    *L_ptr = new_L;
    return true;
}

static void post_lift_coil_sweep(Engine *e_out, int n_out, int *test_ring, int *test_L_ptr,
                                 int *best_out_L_ptr, const char *out_prefix) {
    int test_L = *test_L_ptr;
    bool improved = true;
    while (improved) {
        improved = false;
        for (int gw = 8; gw <= 72 && !improved; gw += 2) {
            for (int ga = 0; ga < test_L; ga++) {
                if (coil_window_replace(e_out, test_ring, &test_L, ga, gw, 2, 40000, NULL, false)) {
                    if (verify_coil_ring(n_out, test_ring, test_L)) {
                        printf("    [POST-LIFT +2!] new Q_%d Coil L=%d at ga=%d gw=%d!\n",
                               n_out, test_L, ga, gw);
                        fflush(stdout);
                        if (test_L > *best_out_L_ptr) {
                            *best_out_L_ptr = test_L;
                            char fn[256];
                            snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, n_out, *best_out_L_ptr);
                            save_coil_file(fn, test_ring, test_L);
                        }
                        improved = true;
                        break;
                    }
                }
            }
        }
    }
    *test_L_ptr = test_L;
}

static int run_lift_coil(int n_in, const char *seed_file, const char *out_prefix) {
    int n_out = n_in + 1;
    FILE *f = fopen(seed_file, "r");
    if (!f) { perror("fopen"); return 1; }
    int steps[MAX_LEN], L0 = 0, val;
    while (fscanf(f, "%d", &val) == 1) steps[L0++] = val;
    fclose(f);

    int orig_ring[MAX_LEN], v = 0;
    for (int i = 0; i < L0; i++) { orig_ring[i] = v; v ^= (1 << steps[i]); }

    Engine *e_in = (Engine *)calloc(1, sizeof(Engine));
    Engine *e_out = (Engine *)calloc(1, sizeof(Engine));
    e_in->n = n_in; e_in->N = 1 << n_in; e_in->rng = 101ULL;
    e_out->n = n_out; e_out->N = 1 << n_out; e_out->rng = 202ULL;

    int best_out_L = 0;

    for (int b = 0; b < n_in; b++) {
        int flips[16], nf = 0;
        for (int i = 0; i < L0; i++) {
            if (steps[i] == b && nf < 16) flips[nf++] = i;
        }
        if (nf != 2) continue;
        int delta = 1 << b;
        printf("=== [LIFT_COIL] n_in=%d -> n_out=%d coord b=%d (delta=%d) flips=(%d, %d) ===\n",
               n_in, n_out, b, delta, flips[0], flips[1]);
        fflush(stdout);

        for (int dir = 0; dir < 2; dir++) {
            int c_bridge = flips[dir];
            int c_detour = flips[1 - dir];

            int *forbid = (int *)calloc(e_in->N, sizeof(int));
            for (int i = 0; i < L0; i++) forbid[orig_ring[i] ^ delta] = 1;

            bool found_detour = false;
            int det_ring[MAX_LEN], L_det = L0;
            for (int gain1 = 2; gain1 >= -22 && !found_detour; gain1 -= 2) {
                for (int w1 = 6; w1 <= 62 && !found_detour; w1 += 2) {
                    for (int k1 = 2; k1 <= w1 - 2; k1++) {
                        int a = (c_detour - k1 + L0) % L0;
                        L_det = L0;
                        memcpy(det_ring, orig_ring, sizeof(int) * L0);
                        if (coil_window_replace(e_in, det_ring, &L_det, a, w1, gain1, 25000, forbid, false)) {
                            if (verify_coil_ring(n_in, det_ring, L_det)) {
                                found_detour = true;
                                printf("  [STEP 1] bridge=%d detour=%d: w1=%d gain1=%d -> L_det=%d\n",
                                       c_bridge, c_detour, w1, gain1, L_det);
                                fflush(stdout);
                                break;
                            }
                        }
                    }
                }
            }
            free(forbid);
            if (!found_detour) continue;

            int cb0 = -1;
            int u_bridge = orig_ring[c_bridge];
            int v_bridge = orig_ring[(c_bridge + 1) % L0];
            for (int i = 0; i < L_det; i++) {
                if (det_ring[i] == u_bridge && det_ring[(i + 1) % L_det] == v_bridge) {
                    cb0 = i;
                    break;
                }
            }
            if (cb0 < 0) continue;

            int L_raw = L_det + L0;
            int high_bit = 1 << n_in;
            int full[MAX_LEN];
            for (int k = 0; k < L_det; k++) {
                full[k] = det_ring[(cb0 + 1 + k) % L_det];
            }
            for (int k = 0; k < L0; k++) {
                full[L_det + k] = (orig_ring[(c_bridge + 1 + k) % L0] ^ delta) | high_bit;
            }

            for (int junc = 0; junc < 2; junc++) {
                int base_ring[MAX_LEN];
                int junc_idx = (junc == 0) ? (L_det - 1) : (L0 - 1);
                for (int i = 0; i < L_raw; i++) {
                    base_ring[i] = (junc == 0) ? full[i] : full[(i + L_det) % L_raw];
                }

                bool bridged = false;
                for (int gain2 = 2; gain2 >= -22 && !bridged; gain2 -= 2) {
                    for (int w2 = 4; w2 <= 124 && !bridged; w2 += 2) {
                        for (int k1 = 2; k1 <= w2 - 2; k1++) {
                            int a = (junc_idx - k1 + 1 + L_raw) % L_raw;
                            int test_ring[MAX_LEN], test_L = L_raw;
                            memcpy(test_ring, base_ring, sizeof(int) * L_raw);
                            if (coil_window_replace(e_out, test_ring, &test_L, a, w2, gain2, 80000, NULL, false)) {
                                if (verify_coil_ring(n_out, test_ring, test_L)) {
                                    printf("  [STEP 2] junc=%d Valid Q_%d Coil L=%d (w2=%d gain2=%d)!\n",
                                           junc, n_out, test_L, w2, gain2);
                                    fflush(stdout);
                                    if (test_L > best_out_L) {
                                        best_out_L = test_L;
                                        char fn[256];
                                        snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                        save_coil_file(fn, test_ring, test_L);
                                    }
                                    post_lift_coil_sweep(e_out, n_out, test_ring, &test_L, &best_out_L, out_prefix);
                                    bridged = true;
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    printf("[SUMMARY LIFT_COIL] n_out=%d best_L=%d\n", n_out, best_out_L);
    free(e_in); free(e_out);
    return 0;
}

static int run_lift_snake(int n_in, const char *seed_file, const char *out_prefix) {
    int n_out = n_in + 1;
    FILE *f = fopen(seed_file, "r");
    if (!f) { perror("fopen"); return 1; }
    int steps[MAX_LEN], L0 = 0, val;
    while (fscanf(f, "%d", &val) == 1) steps[L0++] = val;
    fclose(f);

    int orig_verts[MAX_LEN], v = 0;
    for (int i = 0; i <= L0; i++) {
        orig_verts[i] = v;
        if (i < L0) v ^= (1 << steps[i]);
    }

    Engine *e_in = (Engine *)calloc(1, sizeof(Engine));
    Engine *e_out = (Engine *)calloc(1, sizeof(Engine));
    e_in->n = n_in; e_in->N = 1 << n_in; e_in->rng = 303ULL;
    e_out->n = n_out; e_out->N = 1 << n_out; e_out->rng = 404ULL;

    int best_out_L = 0;

    for (int b = 0; b < n_in; b++) {
        int flips[16], nf = 0;
        for (int i = 0; i < L0; i++) {
            if (steps[i] == b && nf < 16) flips[nf++] = i;
        }
        if (nf != 1) continue;
        int c1 = flips[0];
        int delta = 1 << b;
        printf("=== [LIFT_SNAKE] n_in=%d -> n_out=%d coord b=%d (delta=%d) flip=%d ===\n",
               n_in, n_out, b, delta, c1);
        fflush(stdout);

        int *forbid = (int *)calloc(e_in->N, sizeof(int));
        for (int i = 0; i <= L0; i++) forbid[orig_verts[i] ^ delta] = 1;

        bool found_detour = false;
        int det_verts[MAX_LEN], L_det = L0;
        for (int gain1 = 2; gain1 >= -22 && !found_detour; gain1 -= 2) {
            for (int w1 = 6; w1 <= 62 && !found_detour; w1 += 2) {
                for (int k1 = 2; k1 <= w1 - 2; k1++) {
                    int a = c1 - k1;
                    if (a < 1 || a + w1 >= L0) continue;
                    L_det = L0;
                    memcpy(det_verts, orig_verts, sizeof(int) * (L0 + 1));
                    if (snake_window_replace(e_in, det_verts, &L_det, a, w1, gain1, 25000, forbid, false)) {
                        if (verify_snake_verts(n_in, det_verts, L_det)) {
                            found_detour = true;
                            printf("  [STEP 1] flip=%d: w1=%d gain1=%d -> L_det=%d\n",
                                   c1, w1, gain1, L_det);
                            fflush(stdout);
                            break;
                        }
                    }
                }
            }
        }
        free(forbid);
        if (!found_detour) continue;

        int high_bit = 1 << n_in;
        for (int end_dir = 0; end_dir < 2; end_dir++) {
            int full[MAX_LEN];
            int L_raw = L_det + 1 + L0;
            if (end_dir == 0) {
                for (int i = 0; i <= L_det; i++) full[i] = det_verts[i];
                for (int i = 0; i <= L0; i++) full[L_det + 1 + i] = (orig_verts[L0 - i] ^ delta) | high_bit;
            } else {
                for (int i = 0; i <= L_det; i++) full[i] = det_verts[L_det - i];
                for (int i = 0; i <= L0; i++) full[L_det + 1 + i] = (orig_verts[i] ^ delta) | high_bit;
            }

            bool bridged = false;
            for (int gain2 = 3; gain2 >= -23 && !bridged; gain2 -= 2) {
                for (int w2 = 4; w2 <= 124 && !bridged; w2 += 2) {
                    for (int k0 = 1; k0 <= w2 - 2; k0++) {
                        int a = L_det - k0;
                        if (a < 1 || a + w2 >= L_raw) continue;
                        int test_verts[MAX_LEN], test_L = L_raw;
                        memcpy(test_verts, full, sizeof(int) * (L_raw + 1));
                        if (snake_window_replace(e_out, test_verts, &test_L, a, w2, gain2, 80000, NULL, false)) {
                            if (verify_snake_verts(n_out, test_verts, test_L)) {
                                printf("  [STEP 2] end_dir=%d Valid Q_%d Snake L=%d (w2=%d gain2=%d)!\n",
                                       end_dir, n_out, test_L, w2, gain2);
                                fflush(stdout);
                                if (test_L > best_out_L) {
                                    best_out_L = test_L;
                                    char fn[256];
                                    snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                    save_snake_file(fn, test_verts, test_L);
                                }
                                bool improved = true;
                                while (improved) {
                                    improved = false;
                                    for (int gw = 8; gw <= 72 && !improved; gw += 2) {
                                        for (int ga = 0; ga + gw <= test_L; ga++) {
                                            if (snake_window_replace(e_out, test_verts, &test_L, ga, gw, 2, 40000, NULL, false)) {
                                                if (verify_snake_verts(n_out, test_verts, test_L)) {
                                                    printf("    [POST-LIFT +2!] new Q_%d Snake L=%d at ga=%d gw=%d!\n",
                                                           n_out, test_L, ga, gw);
                                                    fflush(stdout);
                                                    if (test_L > best_out_L) {
                                                        best_out_L = test_L;
                                                        char fn[256];
                                                        snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                                        save_snake_file(fn, test_verts, test_L);
                                                    }
                                                    improved = true;
                                                    break;
                                                }
                                            }
                                        }
                                    }
                                }
                                bridged = true;
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
    printf("[SUMMARY LIFT_SNAKE] n_out=%d best_L=%d\n", n_out, best_out_L);
    free(e_in); free(e_out);
    return 0;
}

static int run_boost_coil(int n, const char *b36_file, const char *out_prefix) {
    FILE *f = fopen(b36_file, "r");
    if (!f) { perror("fopen"); return 1; }
    int steps[MAX_LEN], L = 0, ch;
    while ((ch = fgetc(f)) != EOF) {
        if (isdigit(ch)) steps[L++] = ch - '0';
        else if ( ch >= 'a' && ch <= 'z') steps[L++] = 10 + (ch - 'a');
        else if ( ch >= 'A' && ch <= 'Z') steps[L++] = 10 + (ch - 'A');
    }
    fclose(f);
    int ring[MAX_LEN], v = 0;
    for (int i = 0; i < L; i++) { ring[i] = v; v ^= (1 << steps[i]); }
    int best_L = L;
    printf("=== [BOOST_COIL] n=%d initial L=%d ===\n", n, L);
    Engine *e = (Engine *)calloc(1, sizeof(Engine));
    e->n = n; e->N = 1 << n; e->rng = 999ULL;

    post_lift_coil_sweep(e, n, ring, &L, &best_L, out_prefix);

    /* Neutral drift rounds followed by +2/+4 sweeps */
    int best_ring[MAX_LEN];
    memcpy(best_ring, ring, sizeof(int) * L);
    for (int round = 0; round < 12; round++) {
        int cur_ring[MAX_LEN], cur_L = best_L;
        memcpy(cur_ring, best_ring, sizeof(int) * best_L);
        int drifted = 0;
        for (int tries = 0; tries < 400 && drifted < 6; tries++) {
            int w = 10 + 2 * (int)(xorshift64(&e->rng) % 24);
            int a = (int)(xorshift64(&e->rng) % (uint64_t)cur_L);
            if (coil_window_replace(e, cur_ring, &cur_L, a, w, 0, 30000, NULL, true)) {
                drifted++;
            }
        }
        int prev_best = best_L;
        post_lift_coil_sweep(e, n, cur_ring, &cur_L, &best_L, out_prefix);
        if (cur_L >= prev_best) {
            memcpy(best_ring, cur_ring, sizeof(int) * cur_L);
        }
        printf("  [BOOST ROUND %d] drifted=%d cur_L=%d best_L=%d\n", round, drifted, cur_L, best_L);
        fflush(stdout);
    }
    free(e);
    return 0;
}

static int run_drift_opt(int n, int is_coil, const char *seed_file, const char *out_file) {
    FILE *f = fopen(seed_file, "r");
    if (!f) { perror("fopen"); return 1; }
    int steps[MAX_LEN], L = 0, val;
    while (fscanf(f, "%d", &val) == 1) steps[L++] = val;
    fclose(f);

    Engine *e = (Engine *)calloc(1, sizeof(Engine));
    e->n = n; e->N = 1 << n; e->rng = 777ULL;

    if (is_coil) {
        int ring[MAX_LEN], v = 0;
        for (int i = 0; i < L; i++) { ring[i] = v; v ^= (1 << steps[i]); }
        int moves = 0;
        for (int w = 6; w <= 120 && moves < 1; w += 2) {
            for (int a = 0; a < L && moves < 1; a++) {
                if (coil_window_replace(e, ring, &L, a, w, 0, 25000, NULL, true)) {
                    if (verify_coil_ring(n, ring, L)) moves++;
                }
            }
        }
        save_coil_file(out_file, ring, L);
        printf("[DRIFT_OPT COIL] n=%d L=%d neutral_moves=%d saved to %s\n", n, L, moves, out_file);
    } else {
        int verts[MAX_LEN], v = 0;
        for (int i = 0; i <= L; i++) {
            verts[i] = v;
            if (i < L) v ^= (1 << steps[i]);
        }
        int moves = 0;
        for (int w = 6; w <= 120 && moves < 1; w += 2) {
            for (int a = 0; a + w <= L && moves < 1; a++) {
                if (snake_window_replace(e, verts, &L, a, w, 0, 25000, NULL, true)) {
                    if (verify_snake_verts(n, verts, L)) moves++;
                }
            }
        }
        save_snake_file(out_file, verts, L);
        printf("[DRIFT_OPT SNAKE] n=%d L=%d neutral_moves=%d saved to %s\n", n, L, moves, out_file);
    }
    free(e);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage:\n  %s lift_coil [n_in] <seed> [out_prefix]\n  %s lift_snake [n_in] <seed> [out_prefix]\n  %s drift_opt [n] [is_coil] <seed> [out_file]\n  %s boost_coil [n] <b36_file> [out_prefix]\n",
                argv[0], argv[0], argv[0], argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "lift_coil") == 0) {
        return run_lift_coil(atoi(argv[2]), argv[3], argv[4]);
    } else if (strcmp(argv[1], "lift_snake") == 0) {
        return run_lift_snake(atoi(argv[2]), argv[3], argv[4]);
    } else if (strcmp(argv[1], "drift_opt") == 0) {
        return run_drift_opt(atoi(argv[2]), atoi(argv[3]), argv[4], argv[5]);
    } else if (strcmp(argv[1], "boost_coil") == 0) {
        return run_boost_coil(atoi(argv[2]), argv[3], argv[4]);
    }
    return 1;
}
