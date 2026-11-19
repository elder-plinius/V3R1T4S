/*
 * fast_opt.c — Ultra-Fast 128-Bit Corridor Bitboard Optimizer & Multi-Candidate Lifter
 * for Snakes, Coils, and Symmetric Coils in Q_n (n <= 14).
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
#define MAX_K 128

typedef struct {
    uint64_t w[2];
} u128;

static inline u128 u128_zero(void) { return (u128){{0, 0}}; }
static inline bool u128_is_zero(u128 a) { return (a.w[0] | a.w[1]) == 0; }
static inline bool u128_eq(u128 a, u128 b) { return ((a.w[0] ^ b.w[0]) | (a.w[1] ^ b.w[1])) == 0; }
static inline u128 u128_or(u128 a, u128 b) { return (u128){{a.w[0] | b.w[0], a.w[1] | b.w[1]}}; }
static inline u128 u128_and(u128 a, u128 b) { return (u128){{a.w[0] & b.w[0], a.w[1] & b.w[1]}}; }
static inline u128 u128_andnot(u128 a, u128 b) { return (u128){{a.w[0] & ~b.w[0], a.w[1] & ~b.w[1]}}; }
static inline void u128_set(u128 *a, int bit) { a->w[bit >> 6] |= (1ULL << (bit & 63)); }
static inline int u128_test(u128 a, int bit) { return (int)((a.w[bit >> 6] >> (bit & 63)) & 1ULL); }
static inline int u128_popcnt(u128 a) {
    return __builtin_popcountll(a.w[0]) + __builtin_popcountll(a.w[1]);
}
static inline int u128_ctz(u128 a) {
    if (a.w[0]) return __builtin_ctzll(a.w[0]);
    return 64 + __builtin_ctzll(a.w[1]);
}
static inline void u128_clear_lsb(u128 *a) {
    if (a->w[0]) { a->w[0] &= a->w[0] - 1; return; }
    a->w[1] &= a->w[1] - 1;
}
static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return *s = x;
}

typedef struct {
    int n;
    int N;
    int is_sym;
    int t;
    uint64_t rng;
    int used[MAX_V];
    int cnt[MAX_V];
    int v_to_idx[MAX_V];
    int cand_v[MAX_V];
    int dist0[MAX_V];
    int dist1[MAX_V];
    int q[MAX_V];
    char keep[MAX_V];
    int K;
    int w_verts[MAX_K];
    int d1[MAX_K];
    u128 adj[MAX_K];
    u128 twin_conflict[MAX_K];
    u128 even_mask;
    u128 odd_mask;
    u128 orig_mask;
    int nodes;
    int limit;
    int route_idx[MAX_K];
    int route_len;
} FastEngine;

static void engine_init(FastEngine *s, int n, int is_sym, uint64_t seed) {
    memset(s, 0, sizeof(FastEngine));
    s->n = n;
    s->N = 1 << n;
    s->is_sym = is_sym;
    s->rng = seed ? seed : 42ULL;
    for (int v = 0; v < MAX_V; v++) s->v_to_idx[v] = -1;
}

static inline void add_vert(FastEngine *s, int v, int sign) {
    s->used[v] += sign;
    int n = s->n;
    for (int b = 0; b < n; b++) {
        s->cnt[v ^ (1 << b)] += sign;
    }
}

static inline void add_pair(FastEngine *s, int v, int sign) {
    int vt = v ^ s->t;
    s->used[v] += sign;
    s->used[vt] += sign;
    int n = s->n;
    for (int b = 0; b < n; b++) {
        int bit = 1 << b;
        s->cnt[v ^ bit] += sign;
        s->cnt[vt ^ bit] += sign;
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
        if (u < 0 || u >= N || pos[u] != -1) { free(pos); return false; }
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

static bool verify_sym_ring(int n, const int *ring, int h) {
    int L = 2 * h;
    if (!verify_coil_ring(n, ring, L)) return false;
    int t = ring[0] ^ ring[h];
    if (__builtin_popcount((unsigned)t) < 2) return false;
    for (int i = 0; i < h; i++) {
        if ((ring[i] ^ ring[i + h]) != t) return false;
    }
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
        if (u < 0 || u >= N || pos[u] != -1) { free(pos); return false; }
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

static int load_any_sequence(const char *fn, int *steps) {
    FILE *f = fopen(fn, "r");
    if (!f) { perror("fopen"); exit(1); }
    char buf[65536];
    size_t nr = fread(buf, 1, sizeof(buf) - 1, f);
    buf[nr] = '\0';
    fclose(f);

    bool has_space = false;
    for (size_t i = 0; i < nr; i++) {
        if (buf[i] == ' ' || buf[i] == '\t') { has_space = true; break; }
    }
    int L = 0;
    if (has_space) {
        char *p = buf;
        while (*p) {
            while (*p && isspace((unsigned char)*p)) p++;
            if (!*p) break;
            steps[L++] = (int)strtol(p, &p, 10);
        }
    } else {
        for (size_t i = 0; i < nr; i++) {
            char ch = buf[i];
            if (isdigit((unsigned char)ch)) steps[L++] = ch - '0';
            else if (ch >= 'a' && ch <= 'z') steps[L++] = 10 + (ch - 'a');
            else if (ch >= 'A' && ch <= 'Z') steps[L++] = 10 + (ch - 'A');
        }
    }
    return L;
}

static bool bitset_dfs(FastEngine *s, int u, int rem, u128 avail, u128 visited_mask) {
    if (++s->nodes > s->limit) return false;
    if (rem == 2) {
        u128 cands = u128_and(u128_and(s->adj[u], s->adj[1]), avail);
        while (!u128_is_zero(cands)) {
            int v = u128_ctz(cands);
            u128_clear_lsb(&cands);
            u128 final_mask = visited_mask;
            u128_set(&final_mask, v);
            if (!u128_is_zero(s->orig_mask) && u128_eq(final_mask, s->orig_mask)) continue;
            s->route_idx[s->route_len++] = v;
            return true;
        }
        return false;
    }
    u128 goal_nbrs = u128_and(s->adj[1], avail);
    if (u128_is_zero(goal_nbrs)) return false;
    if (rem >= 4) {
        u128 reach = u128_zero(); u128_set(&reach, u);
        int dist_goal = -1, step = 1;
        u128 cur_f = u128_and(s->adj[u], avail);
        while (!u128_is_zero(cur_f)) {
            if (dist_goal < 0 && !u128_is_zero(u128_and(cur_f, goal_nbrs))) dist_goal = step + 1;
            reach = u128_or(reach, cur_f);
            if (step >= rem - 1) break;
            u128 nxt = u128_zero(), tmp = cur_f;
            while (!u128_is_zero(tmp)) {
                int idx = u128_ctz(tmp);
                u128_clear_lsb(&tmp);
                nxt = u128_or(nxt, s->adj[idx]);
            }
            cur_f = u128_andnot(u128_and(nxt, avail), reach);
            step++;
        }
        if (dist_goal < 0 || dist_goal > rem) return false;
        int u_par = u128_test(s->even_mask, u);
        int need_opp = rem / 2, need_same = (rem - 1) / 2;
        u128 u_bit = u128_zero(); u128_set(&u_bit, u);
        u128 interior_reach = u128_andnot(reach, u_bit);
        int cnt_even = u128_popcnt(u128_and(interior_reach, s->even_mask));
        int cnt_odd  = u128_popcnt(u128_and(interior_reach, s->odd_mask));
        if (u_par == 1) { if (cnt_odd < need_opp || cnt_even < need_same) return false; }
        else { if (cnt_even < need_opp || cnt_odd < need_same) return false; }
    }
    u128 cands = u128_andnot(u128_and(s->adj[u], avail), s->adj[1]);
    if (u128_is_zero(cands)) return false;
    int cand_list[16], nc = 0;
    while (!u128_is_zero(cands)) {
        int v = u128_ctz(cands);
        u128_clear_lsb(&cands);
        if (s->d1[v] <= rem - 1) cand_list[nc++] = v;
    }
    if (nc == 0) return false;
    for (int i = nc - 1; i > 0; i--) {
        int j = (int)(xorshift64(&s->rng) % (uint64_t)(i + 1));
        int tmp = cand_list[i]; cand_list[i] = cand_list[j]; cand_list[j] = tmp;
    }
    u128 block_u = s->adj[u];
    for (int idx = 0; idx < nc; idx++) {
        int v = cand_list[idx];
        u128 v_bit = u128_zero(); u128_set(&v_bit, v);
        u128 forbid = s->is_sym ? u128_or(u128_or(block_u, v_bit), s->twin_conflict[v])
                                : u128_or(block_u, v_bit);
        u128 next_avail = u128_andnot(avail, forbid);
        s->route_idx[s->route_len++] = v;
        if (bitset_dfs(s, v, rem - 1, next_avail, u128_or(visited_mask, v_bit))) return true;
        s->route_len--;
        if (s->nodes > s->limit) break;
    }
    return false;
}

static bool solve_candidate_graph_fast(FastEngine *s, int start_v, int target_v, int new_w, int budget,
                                       const int *forbid_layer, const int *orig_interior, int orig_int_len) {
    s->cand_v[0] = start_v; s->v_to_idx[start_v] = 0; s->dist0[0] = 0;
    s->cand_v[1] = target_v; s->v_to_idx[target_v] = 1; s->dist0[1] = 999999;
    int M = 2;
    int qh = 0, qt = 0;
    s->q[qt++] = 0;
    int n = s->n;

    while (qh < qt) {
        int u_idx = s->q[qh++];
        int d = s->dist0[u_idx];
        if (d >= new_w - 1) continue;
        int u = s->cand_v[u_idx];
        for (int b = 0; b < n; b++) {
            int nb_v = u ^ (1 << b);
            if (nb_v == target_v) {
                if (d + 1 > 1 || new_w == 1) {
                    if (d + 1 < s->dist0[1]) s->dist0[1] = d + 1;
                }
                continue;
            }
            int nb_idx = s->v_to_idx[nb_v];
            if (nb_idx < 0) {
                if (s->used[nb_v]) continue;
                if (forbid_layer && forbid_layer[nb_v]) continue;
                int d_t = __builtin_popcount((unsigned)(nb_v ^ target_v));
                if (d + 1 + d_t > new_w) continue;
                int d_s = __builtin_popcount((unsigned)(nb_v ^ start_v));
                int adj_s = (d_s == 1), adj_t = (d_t == 1);
                if (adj_s + adj_t == 2 && new_w != 2) continue;
                if (s->cnt[nb_v] != adj_s + adj_t) continue;
                nb_idx = M++;
                s->cand_v[nb_idx] = nb_v;
                s->v_to_idx[nb_v] = nb_idx;
                s->dist0[nb_idx] = d + 1;
                s->dist1[nb_idx] = 999999;
                if (d + 1 < new_w - 1) s->q[qt++] = nb_idx;
            }
        }
    }

    if (s->dist0[1] > new_w || M - 2 < new_w - 1) {
        for (int i = 0; i < M; i++) s->v_to_idx[s->cand_v[i]] = -1;
        return false;
    }

    s->dist1[0] = 999999;
    s->dist1[1] = 0;
    qh = 0; qt = 0;
    s->q[qt++] = 1;
    while (qh < qt) {
        int u_idx = s->q[qh++];
        int d = s->dist1[u_idx];
        if (d >= new_w - 1) continue;
        int u = s->cand_v[u_idx];
        for (int b = 0; b < n; b++) {
            int nb = s->v_to_idx[u ^ (1 << b)];
            if (nb >= 0 && s->dist1[nb] > d + 1) {
                s->dist1[nb] = d + 1;
                if (nb != 0 && d + 1 < new_w - 1) s->q[qt++] = nb;
            }
        }
    }

    int max_sum = new_w;
    if (M > MAX_K && new_w - s->dist0[1] <= 6) {
        while (max_sum >= s->dist0[1]) {
            int cnt_k = 0;
            for (int i = 2; i < M; i++) {
                if (s->dist0[i] + s->dist1[i] <= max_sum) cnt_k++;
            }
            if (cnt_k <= MAX_K - 2 || max_sum == s->dist0[1]) break;
            max_sum -= 2;
        }
    }

    s->keep[0] = 1; s->keep[1] = 1;
    for (int i = 2; i < M; i++) {
        s->keep[i] = (s->dist0[i] + s->dist1[i] <= max_sum) ? 1 : 0;
    }
    bool changed = true;
    while (changed) {
        changed = false;
        for (int i = 2; i < M; i++) {
            if (!s->keep[i]) continue;
            int u = s->cand_v[i], deg = 0;
            for (int b = 0; b < n; b++) {
                int nb = s->v_to_idx[u ^ (1 << b)];
                if (nb >= 0 && s->keep[nb]) deg++;
            }
            if (deg < 2) { s->keep[i] = 0; changed = true; }
        }
    }

    for (int i = 0; i < M; i++) s->v_to_idx[s->cand_v[i]] = -1;

    int K = 2;
    s->w_verts[0] = start_v; s->w_verts[1] = target_v;
    s->d1[0] = s->dist1[0]; s->d1[1] = 0;
    s->v_to_idx[start_v] = 0; s->v_to_idx[target_v] = 1;
    for (int i = 2; i < M; i++) {
        if (s->keep[i]) {
            if (K >= MAX_K) {
                for (int j = 0; j < K; j++) s->v_to_idx[s->w_verts[j]] = -1;
                return false;
            }
            int u = s->cand_v[i];
            s->w_verts[K] = u;
            s->d1[K] = s->dist1[i];
            s->v_to_idx[u] = K;
            K++;
        }
    }
    if (K - 2 < new_w - 1) {
        for (int i = 0; i < K; i++) s->v_to_idx[s->w_verts[i]] = -1;
        return false;
    }

    s->K = K;
    s->even_mask = u128_zero(); s->odd_mask = u128_zero();
    for (int i = 0; i < K; i++) {
        s->adj[i] = u128_zero();
        int u = s->w_verts[i];
        if (__builtin_popcount((unsigned)u) & 1) u128_set(&s->odd_mask, i);
        else u128_set(&s->even_mask, i);
        for (int b = 0; b < n; b++) {
            int nb = s->v_to_idx[u ^ (1 << b)];
            if (nb >= 0) u128_set(&s->adj[i], nb);
        }
        if (s->is_sym) {
            s->twin_conflict[i] = u128_zero();
            int ut = u ^ s->t;
            int twin_idx = s->v_to_idx[ut];
            if (twin_idx >= 0) u128_set(&s->twin_conflict[i], twin_idx);
            for (int b = 0; b < n; b++) {
                int tnb = s->v_to_idx[ut ^ (1 << b)];
                if (tnb >= 0) u128_set(&s->twin_conflict[i], tnb);
            }
        }
    }

    s->orig_mask = u128_zero();
    if (orig_interior && orig_int_len > 0) {
        bool all_in = true;
        for (int k = 0; k < orig_int_len; k++) {
            int idx = s->v_to_idx[orig_interior[k]];
            if (idx >= 2) u128_set(&s->orig_mask, idx);
            else all_in = false;
        }
        if (!all_in) s->orig_mask = u128_zero();
    }

    for (int i = 0; i < K; i++) s->v_to_idx[s->w_verts[i]] = -1;

    u128 avail = u128_zero();
    for (int i = 2; i < K; i++) u128_set(&avail, i);
    s->route_len = 0; s->nodes = 0; s->limit = budget;
    return bitset_dfs(s, 0, new_w, avail, u128_zero());
}

static void sync_snake_state(FastEngine *s, const int *verts, int L) {
    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    for (int i = 0; i <= L; i++) add_vert(s, verts[i], 1);
}

static void sync_coil_state(FastEngine *s, const int *ring, int L) {
    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    for (int i = 0; i < L; i++) add_vert(s, ring[i], 1);
}

static void sync_sym_state(FastEngine *s, const int *ring, int h) {
    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    s->t = ring[0] ^ ring[h];
    for (int i = 0; i < h; i++) add_pair(s, ring[i], 1);
}

static bool fast_snake_window(FastEngine *s, int *verts, int *L_ptr, int a, int w, int gain,
                              int budget, const int *forbid_layer, bool forbid_orig) {
    int L = *L_ptr, new_w = w + gain;
    if (a < 0 || a + w > L || w < 2 || new_w < 2 || new_w > 124) return false;
    int start_v = verts[a], target_v = verts[a + w];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;

    int orig_int[128];
    for (int k = 1; k < w; k++) {
        int v = verts[a + k];
        add_vert(s, v, -1);
        orig_int[k - 1] = v;
    }

    bool ok = solve_candidate_graph_fast(s, start_v, target_v, new_w, budget, forbid_layer,
                                         forbid_orig ? orig_int : NULL, w - 1);
    if (!ok) {
        for (int k = 1; k < w; k++) add_vert(s, orig_int[k - 1], 1);
        return false;
    }

    for (int k = 0; k < new_w - 1; k++) add_vert(s, s->w_verts[s->route_idx[k]], 1);

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

static bool fast_coil_window(FastEngine *s, int *ring, int *L_ptr, int a, int w, int gain,
                             int budget, const int *forbid_layer, bool forbid_orig) {
    int L = *L_ptr, new_w = w + gain;
    if (w < 2 || w > L - 4 || new_w < 2 || new_w > 124) return false;
    int start_v = ring[a % L], target_v = ring[(a + w) % L];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;

    int orig_int[128];
    for (int k = 1; k < w; k++) {
        int v = ring[(a + k) % L];
        add_vert(s, v, -1);
        orig_int[k - 1] = v;
    }

    bool ok = solve_candidate_graph_fast(s, start_v, target_v, new_w, budget, forbid_layer,
                                         forbid_orig ? orig_int : NULL, w - 1);
    if (!ok) {
        for (int k = 1; k < w; k++) add_vert(s, orig_int[k - 1], 1);
        return false;
    }

    for (int k = 0; k < new_w - 1; k++) add_vert(s, s->w_verts[s->route_idx[k]], 1);

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

static bool fast_sym_window(FastEngine *s, int *ring, int *h_ptr, int a, int w, int gain,
                            int budget, const int *forbid_layer, bool forbid_orig) {
    int h = *h_ptr, L = 2 * h, new_w = w + gain;
    if (w < 2 || w > h - 2 || new_w < 2 || new_w > 120) return false;
    int start_v = ring[a % L], target_v = ring[(a + w) % L];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;

    int orig_int[128];
    for (int k = 1; k < w; k++) {
        int v = ring[(a + k) % L];
        add_pair(s, v, -1);
        orig_int[k - 1] = v;
    }

    bool ok = solve_candidate_graph_fast(s, start_v, target_v, new_w, budget, forbid_layer,
                                         forbid_orig ? orig_int : NULL, w - 1);
    if (!ok) {
        for (int k = 1; k < w; k++) add_pair(s, orig_int[k - 1], 1);
        return false;
    }

    for (int k = 0; k < new_w - 1; k++) add_pair(s, s->w_verts[s->route_idx[k]], 1);

    int new_h = h + gain, new_L = 2 * new_h;
    int new_ring[MAX_LEN];
    new_ring[0] = start_v;
    for (int k = 0; k < new_w - 1; k++) new_ring[k + 1] = s->w_verts[s->route_idx[k]];
    for (int k = w; k < h; k++) new_ring[new_w + (k - w)] = ring[(a + k) % L];
    for (int i = 0; i < new_h; i++) new_ring[i + new_h] = new_ring[i] ^ s->t;
    int rot_back = (new_L - (a % new_L)) % new_L;
    for (int i = 0; i < new_L; i++) ring[i] = new_ring[(i + rot_back) % new_L];
    *h_ptr = new_h;
    return true;
}

static void sweep_snake_plus(FastEngine *s, int *verts, int *L_ptr, int *best_L_ptr, const char *out_prefix) {
    int L = *L_ptr;
    sync_snake_state(s, verts, L);
    bool improved = true;
    while (improved) {
        improved = false;
        for (int gw = 6; gw <= 64 && !improved; gw += 2) {
            for (int ga = 0; ga + gw <= L; ga++) {
                if (fast_snake_window(s, verts, &L, ga, gw, 2, 15000, NULL, false)) {
                    if (verify_snake_verts(s->n, verts, L)) {
                        printf("  [SNAKE +2!] Q_%d Snake L=%d at ga=%d gw=%d!\n", s->n, L, ga, gw);
                        fflush(stdout);
                        if (L > *best_L_ptr) {
                            *best_L_ptr = L;
                            char fn[256];
                            snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, s->n, L);
                            save_snake_file(fn, verts, L);
                        }
                        improved = true;
                        break;
                    } else {
                        sync_snake_state(s, verts, L);
                    }
                }
            }
        }
    }
    *L_ptr = L;
}

static void sweep_coil_plus(FastEngine *s, int *ring, int *L_ptr, int *best_L_ptr, const char *out_prefix) {
    int L = *L_ptr;
    sync_coil_state(s, ring, L);
    bool improved = true;
    while (improved) {
        improved = false;
        for (int gw = 6; gw <= 64 && !improved; gw += 2) {
            for (int ga = 0; ga < L; ga++) {
                if (fast_coil_window(s, ring, &L, ga, gw, 2, 15000, NULL, false)) {
                    if (verify_coil_ring(s->n, ring, L)) {
                        printf("  [COIL +2!] Q_%d Coil L=%d at ga=%d gw=%d!\n", s->n, L, ga, gw);
                        fflush(stdout);
                        if (L > *best_L_ptr) {
                            *best_L_ptr = L;
                            char fn[256];
                            snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, s->n, L);
                            save_coil_file(fn, ring, L);
                        }
                        improved = true;
                        break;
                    } else {
                        sync_coil_state(s, ring, L);
                    }
                }
            }
        }
    }
    *L_ptr = L;
}

static void sweep_sym_plus(FastEngine *s, int *ring, int *h_ptr, int *best_L_ptr, const char *out_prefix) {
    int h = *h_ptr;
    sync_sym_state(s, ring, h);
    bool improved = true;
    while (improved) {
        improved = false;
        for (int gw = 6; gw <= 64 && gw <= h - 4 && !improved; gw += 2) {
            for (int ga = 0; ga < h; ga++) {
                if (fast_sym_window(s, ring, &h, ga, gw, 2, 15000, NULL, false)) {
                    if (verify_sym_ring(s->n, ring, h)) {
                        printf("  [SYM_COIL +4!] Q_%d SymCoil L=%d (h=%d) at ga=%d gw=%d!\n",
                               s->n, 2 * h, h, ga, gw);
                        fflush(stdout);
                        if (2 * h > *best_L_ptr) {
                            *best_L_ptr = 2 * h;
                            char fn[256];
                            snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, s->n, 2 * h);
                            save_coil_file(fn, ring, 2 * h);
                        }
                        improved = true;
                        break;
                    } else {
                        sync_sym_state(s, ring, h);
                    }
                }
            }
        }
    }
    *h_ptr = h;
}

static int run_ils_snake(int n, int rounds, const char *seed_file, const char *out_prefix) {
    int steps[MAX_LEN];
    int L = load_any_sequence(seed_file, steps);
    int verts[MAX_LEN], v = 0;
    for (int i = 0; i <= L; i++) {
        verts[i] = v;
        if (i < L) v ^= (1 << steps[i]);
    }
    if (!verify_snake_verts(n, verts, L)) {
        fprintf(stderr, "Invalid initial snake L=%d\n", L);
        return 1;
    }
    FastEngine *s = (FastEngine *)malloc(sizeof(FastEngine));
    engine_init(s, n, 0, 1001ULL);
    int best_L = L;
    int best_verts[MAX_LEN];
    memcpy(best_verts, verts, sizeof(int) * (L + 1));

    printf("=== [ILS_SNAKE] n=%d initial L=%d rounds=%d ===\n", n, L, rounds);
    fflush(stdout);
    sweep_snake_plus(s, verts, &L, &best_L, out_prefix);
    if (L >= best_L) memcpy(best_verts, verts, sizeof(int) * (L + 1));

    for (int r = 0; r < rounds; r++) {
        int cur_L = best_L;
        memcpy(verts, best_verts, sizeof(int) * (cur_L + 1));
        sync_snake_state(s, verts, cur_L);
        int drifted = 0;
        for (int tries = 0; tries < 500 && drifted < 12; tries++) {
            int w = 8 + 2 * (int)(xorshift64(&s->rng) % 28);
            if (w >= cur_L - 2) continue;
            int a = (int)(xorshift64(&s->rng) % (uint64_t)(cur_L - w));
            if (fast_snake_window(s, verts, &cur_L, a, w, 0, 15000, NULL, true)) {
                drifted++;
            }
        }
        int prev_best = best_L;
        sweep_snake_plus(s, verts, &cur_L, &best_L, out_prefix);
        if (cur_L >= prev_best && verify_snake_verts(n, verts, cur_L)) {
            memcpy(best_verts, verts, sizeof(int) * (cur_L + 1));
            if (r < 3 && drifted > 0) {
                char fn[256];
                snprintf(fn, sizeof(fn), "%s_drifted_r%d_Q%d_%d.txt", out_prefix, r, n, cur_L);
                save_snake_file(fn, verts, cur_L);
            }
        }
        printf("  [ILS_SNAKE round %d/%d] drifted=%d cur_L=%d best_L=%d\n", r + 1, rounds, drifted, cur_L, best_L);
        fflush(stdout);
    }
    free(s);
    return 0;
}

static int run_ils_coil(int n, int rounds, const char *seed_file, const char *out_prefix) {
    int steps[MAX_LEN];
    int L = load_any_sequence(seed_file, steps);
    int ring[MAX_LEN], v = 0;
    for (int i = 0; i < L; i++) {
        ring[i] = v;
        v ^= (1 << steps[i]);
    }
    if (!verify_coil_ring(n, ring, L)) {
        fprintf(stderr, "Invalid initial coil L=%d\n", L);
        return 1;
    }
    FastEngine *s = (FastEngine *)malloc(sizeof(FastEngine));
    engine_init(s, n, 0, 2002ULL);
    int best_L = L;
    int best_ring[MAX_LEN];
    memcpy(best_ring, ring, sizeof(int) * L);

    printf("=== [ILS_COIL] n=%d initial L=%d rounds=%d ===\n", n, L, rounds);
    fflush(stdout);
    sweep_coil_plus(s, ring, &L, &best_L, out_prefix);
    if (L >= best_L) memcpy(best_ring, ring, sizeof(int) * L);

    for (int r = 0; r < rounds; r++) {
        int cur_L = best_L;
        memcpy(ring, best_ring, sizeof(int) * cur_L);
        sync_coil_state(s, ring, cur_L);
        int drifted = 0;
        for (int tries = 0; tries < 500 && drifted < 12; tries++) {
            int w = 8 + 2 * (int)(xorshift64(&s->rng) % 28);
            int a = (int)(xorshift64(&s->rng) % (uint64_t)cur_L);
            if (fast_coil_window(s, ring, &cur_L, a, w, 0, 15000, NULL, true)) {
                drifted++;
            }
        }
        int prev_best = best_L;
        sweep_coil_plus(s, ring, &cur_L, &best_L, out_prefix);
        if (cur_L >= prev_best && verify_coil_ring(n, ring, cur_L)) {
            memcpy(best_ring, ring, sizeof(int) * cur_L);
            if (r < 3 && drifted > 0) {
                char fn[256];
                snprintf(fn, sizeof(fn), "%s_drifted_r%d_Q%d_%d.txt", out_prefix, r, n, cur_L);
                save_coil_file(fn, ring, cur_L);
            }
        }
        printf("  [ILS_COIL round %d/%d] drifted=%d cur_L=%d best_L=%d\n", r + 1, rounds, drifted, cur_L, best_L);
        fflush(stdout);
    }
    free(s);
    return 0;
}

static int run_ils_sym(int n, int rounds, const char *seed_file, const char *out_prefix) {
    int steps[MAX_LEN];
    int L = load_any_sequence(seed_file, steps);
    int h = L / 2;
    int ring[MAX_LEN], v = 0;
    for (int i = 0; i < L; i++) {
        ring[i] = v;
        v ^= (1 << steps[i]);
    }
    if (!verify_sym_ring(n, ring, h)) {
        fprintf(stderr, "Invalid initial sym_coil L=%d\n", L);
        return 1;
    }
    FastEngine *s = (FastEngine *)malloc(sizeof(FastEngine));
    engine_init(s, n, 1, 3003ULL);
    int best_L = L;
    int best_ring[MAX_LEN];
    memcpy(best_ring, ring, sizeof(int) * L);

    printf("=== [ILS_SYM] n=%d initial L=%d (h=%d) rounds=%d ===\n", n, L, h, rounds);
    fflush(stdout);
    sweep_sym_plus(s, ring, &h, &best_L, out_prefix);
    if (2 * h >= best_L) memcpy(best_ring, ring, sizeof(int) * (2 * h));

    for (int r = 0; r < rounds; r++) {
        int cur_h = best_L / 2;
        memcpy(ring, best_ring, sizeof(int) * (2 * cur_h));
        sync_sym_state(s, ring, cur_h);
        int drifted = 0;
        for (int tries = 0; tries < 500 && drifted < 12; tries++) {
            int w = 8 + 2 * (int)(xorshift64(&s->rng) % 26);
            if (w >= cur_h - 4) continue;
            int a = (int)(xorshift64(&s->rng) % (uint64_t)cur_h);
            if (fast_sym_window(s, ring, &cur_h, a, w, 0, 15000, NULL, true)) {
                drifted++;
            }
        }
        int prev_best = best_L;
        sweep_sym_plus(s, ring, &cur_h, &best_L, out_prefix);
        if (2 * cur_h >= prev_best && verify_sym_ring(n, ring, cur_h)) {
            memcpy(best_ring, ring, sizeof(int) * (2 * cur_h));
            if (r < 3 && drifted > 0) {
                char fn[256];
                snprintf(fn, sizeof(fn), "%s_drifted_r%d_Q%d_%d.txt", out_prefix, r, n, 2 * cur_h);
                save_coil_file(fn, ring, 2 * cur_h);
            }
        }
        printf("  [ILS_SYM round %d/%d] drifted=%d cur_L=%d best_L=%d\n", r + 1, rounds, drifted, 2 * cur_h, best_L);
        fflush(stdout);
    }
    free(s);
    return 0;
}

static uint64_t hash_ring_set(const int *ring, int L) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < L; i++) {
        uint64_t v = (uint64_t)(unsigned int)ring[i];
        v ^= v >> 33;
        v *= 0xff51afd7ed558ccdULL;
        v ^= v >> 33;
        h ^= v;
    }
    return h ^ ((uint64_t)L << 48);
}

static int run_multi_lift_sym(int n_in, int max_detours, const char *seed_file, const char *out_prefix) {
    int n_out = n_in + 1;
    int steps[MAX_LEN];
    int L = load_any_sequence(seed_file, steps);
    int h = L / 2;
    int orig_ring[MAX_LEN], v = 0;
    for (int i = 0; i < L; i++) { orig_ring[i] = v; v ^= (1 << steps[i]); }
    int t = orig_ring[0] ^ orig_ring[h];

    FastEngine *s_in = (FastEngine *)malloc(sizeof(FastEngine));
    FastEngine *s_out = (FastEngine *)malloc(sizeof(FastEngine));
    engine_init(s_in, n_in, 1, 42ULL);
    engine_init(s_out, n_out, 1, 42ULL);

    int best_out_L = 0;
    for (int b = n_in - 1; b >= 0; b--) {
        if ((t >> b) & 1) continue;
        int flips[16], nf = 0;
        for (int i = 0; i < h; i++) {
            if (steps[i] == b && nf < 16) flips[nf++] = i;
        }
        if (nf != 2) continue;
        int delta = 1 << b;
        printf("=== [MULTI_LIFT_SYM] n_in=%d -> n_out=%d coord b=%d (delta=%d) flips=(%d, %d) ===\n",
               n_in, n_out, b, delta, flips[0], flips[1]);
        fflush(stdout);

        for (int dir = 0; dir < 2; dir++) {
            int c_bridge = flips[dir];
            int c_detour = flips[1 - dir];

            int forbid[MAX_V] = {0};
            for (int i = 0; i < L; i++) forbid[orig_ring[i] ^ delta] = 1;

            int detours_found = 0;
            int best_gain1 = -999;
            uint64_t seen_det[64];
            for (int gain = 2; gain >= -14 && detours_found < max_detours; gain -= 2) {
                if (best_gain1 > -999 && gain < best_gain1 - 2) break;
                for (int w = 6; w <= 60 && w <= h - 4 && detours_found < max_detours; w += 2) {
                    for (int k1 = 2; k1 <= w - 3 && detours_found < max_detours; k1++) {
                        int a = (c_detour - k1 + L) % L;
                        for (int r_try = 0; r_try < max_detours && detours_found < max_detours; r_try++) {
                            int det_ring[MAX_LEN], det_h = h;
                            memcpy(det_ring, orig_ring, sizeof(int) * L);
                            sync_sym_state(s_in, det_ring, det_h);
                            if (!fast_sym_window(s_in, det_ring, &det_h, a, w, gain, 40000, forbid, false)) {
                                if (r_try == 0) break;
                                continue;
                            }
                            if (!verify_sym_ring(n_in, det_ring, det_h)) continue;
                            uint64_t dh = hash_ring_set(det_ring, 2 * det_h);
                            bool dup = false;
                            for (int z = 0; z < detours_found; z++) if (seen_det[z] == dh) { dup = true; break; }
                            if (dup) continue;
                            seen_det[detours_found++] = dh;
                            if (gain > best_gain1) best_gain1 = gain;

                            printf("  [STEP 1 #%d] bridge=%d detour=%d: w=%d k1=%d gain=%d -> det_h=%d\n",
                                   detours_found, c_bridge, c_detour, w, k1, gain, det_h);
                            fflush(stdout);

                            int cb0 = -1;
                            for (int i = 0; i < 2 * det_h; i++) {
                                if (det_ring[i] == orig_ring[c_bridge]) { cb0 = i; break; }
                            }
                            if (cb0 < 0) continue;

                            int H_raw = det_h + h;
                            int q_half[MAX_LEN], full[MAX_LEN], rot_full[MAX_LEN];
                            int high_bit = 1 << n_in;
                            for (int k = 0; k < det_h; k++) q_half[k] = det_ring[(cb0 + 1 + k) % (2 * det_h)];
                            for (int k = 0; k < h; k++) q_half[det_h + k] = (orig_ring[(c_bridge + h + 1 + k) % L] ^ delta) | high_bit;
                            for (int i = 0; i < H_raw; i++) {
                                full[i] = q_half[i];
                                full[i + H_raw] = q_half[i] ^ t;
                            }
                            int L_out = 2 * H_raw;
                            for (int i = 0; i < L_out; i++) rot_full[i] = full[(i + det_h) % L_out];

                            int bridges_found = 0;
                            int best_gain2 = -999;
                            uint64_t seen_br[32];
                            for (int gain2 = 3; gain2 >= -25 && bridges_found < 6; gain2 -= 2) {
                                if (best_gain2 > -999 && gain2 < best_gain2 - 2) break;
                                if (2 * (H_raw + gain2) + 20 < best_out_L) break;
                                for (int w2 = 4; w2 <= 68 && w2 <= H_raw - 4 && bridges_found < 6; w2 += 2) {
                                    for (int k2 = 2; k2 <= w2 - 2 && bridges_found < 6; k2++) {
                                        int a2 = h - k2;
                                        for (int b_try = 0; b_try < 6 && bridges_found < 6; b_try++) {
                                            int test_ring[MAX_LEN], test_h = H_raw;
                                            memcpy(test_ring, rot_full, sizeof(int) * L_out);
                                            sync_sym_state(s_out, test_ring, test_h);
                                            if (!fast_sym_window(s_out, test_ring, &test_h, a2, w2, gain2, 60000, NULL, false)) {
                                                if (b_try == 0) break;
                                                continue;
                                            }
                                            if (!verify_sym_ring(n_out, test_ring, test_h)) continue;
                                            uint64_t bh = hash_ring_set(test_ring, 2 * test_h);
                                            bool bdup = false;
                                            for (int z = 0; z < bridges_found; z++) if (seen_br[z] == bh) { bdup = true; break; }
                                            if (bdup) continue;
                                            seen_br[bridges_found++] = bh;
                                            if (gain2 > best_gain2) best_gain2 = gain2;

                                            printf("    [STEP 2 #%d] Valid Q_%d SymCoil L=%d (h=%d) w2=%d k2=%d gain2=%d!\n",
                                                   bridges_found, n_out, 2 * test_h, test_h, w2, k2, gain2);
                                            fflush(stdout);
                                            if (2 * test_h > best_out_L) {
                                                best_out_L = 2 * test_h;
                                                char out_fn[256];
                                                snprintf(out_fn, sizeof(out_fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                                save_coil_file(out_fn, test_ring, 2 * test_h);
                                            }
                                            sweep_sym_plus(s_out, test_ring, &test_h, &best_out_L, out_prefix);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    printf("[SUMMARY MULTI_LIFT_SYM] n_out=%d best_L=%d\n", n_out, best_out_L);
    free(s_in); free(s_out);
    return 0;
}

static int run_multi_lift_coil(int n_in, int max_detours, const char *seed_file, const char *out_prefix) {
    int n_out = n_in + 1;
    int steps[MAX_LEN];
    int L0 = load_any_sequence(seed_file, steps);
    int orig_ring[MAX_LEN], v = 0;
    for (int i = 0; i < L0; i++) { orig_ring[i] = v; v ^= (1 << steps[i]); }

    FastEngine *e_in = (FastEngine *)malloc(sizeof(FastEngine));
    FastEngine *e_out = (FastEngine *)malloc(sizeof(FastEngine));
    engine_init(e_in, n_in, 0, 101ULL);
    engine_init(e_out, n_out, 0, 202ULL);

    int best_out_L = 0;
    for (int b = n_in - 1; b >= 0; b--) {
        int flips[16], nf = 0;
        for (int i = 0; i < L0; i++) {
            if (steps[i] == b && nf < 16) flips[nf++] = i;
        }
        if (nf != 2) continue;
        int delta = 1 << b;
        printf("=== [MULTI_LIFT_COIL] n_in=%d -> n_out=%d coord b=%d (delta=%d) flips=(%d, %d) ===\n",
               n_in, n_out, b, delta, flips[0], flips[1]);
        fflush(stdout);

        for (int dir = 0; dir < 2; dir++) {
            int c_bridge = flips[dir];
            int c_detour = flips[1 - dir];

            int forbid[MAX_V] = {0};
            for (int i = 0; i < L0; i++) forbid[orig_ring[i] ^ delta] = 1;

            int detours_found = 0;
            int best_gain1 = -999;
            uint64_t seen_det[64];
            for (int gain1 = 2; gain1 >= -22 && detours_found < max_detours; gain1 -= 2) {
                if (best_gain1 > -999 && gain1 < best_gain1 - 2) break;
                for (int w1 = 6; w1 <= 62 && detours_found < max_detours; w1 += 2) {
                    for (int k1 = 2; k1 <= w1 - 2 && detours_found < max_detours; k1++) {
                        int a = (c_detour - k1 + L0) % L0;
                        for (int r_try = 0; r_try < max_detours && detours_found < max_detours; r_try++) {
                            int det_ring[MAX_LEN], L_det = L0;
                            memcpy(det_ring, orig_ring, sizeof(int) * L0);
                            sync_coil_state(e_in, det_ring, L_det);
                            if (!fast_coil_window(e_in, det_ring, &L_det, a, w1, gain1, 30000, forbid, false)) {
                                if (r_try == 0) break;
                                continue;
                            }
                            if (!verify_coil_ring(n_in, det_ring, L_det)) continue;
                            uint64_t dh = hash_ring_set(det_ring, L_det);
                            bool dup = false;
                            for (int z = 0; z < detours_found; z++) if (seen_det[z] == dh) { dup = true; break; }
                            if (dup) continue;
                            seen_det[detours_found++] = dh;
                            if (gain1 > best_gain1) best_gain1 = gain1;

                            printf("  [STEP 1 #%d] bridge=%d detour=%d: w1=%d k1=%d gain1=%d -> L_det=%d\n",
                                   detours_found, c_bridge, c_detour, w1, k1, gain1, L_det);
                            fflush(stdout);

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
                            for (int k = 0; k < L_det; k++) full[k] = det_ring[(cb0 + 1 + k) % L_det];
                            for (int k = 0; k < L0; k++) full[L_det + k] = (orig_ring[(c_bridge + 1 + k) % L0] ^ delta) | high_bit;

                            for (int junc = 0; junc < 2; junc++) {
                                int base_ring[MAX_LEN];
                                int junc_idx = (junc == 0) ? (L_det - 1) : (L0 - 1);
                                for (int i = 0; i < L_raw; i++) {
                                    base_ring[i] = (junc == 0) ? full[i] : full[(i + L_det) % L_raw];
                                }

                                int bridges_found = 0;
                                int best_gain2 = -999;
                                uint64_t seen_br[32];
                                for (int gain2 = 2; gain2 >= -22 && bridges_found < 4; gain2 -= 2) {
                                    if (best_gain2 > -999 && gain2 < best_gain2 - 2) break;
                                    if (L_raw + gain2 + 16 < best_out_L) break;
                                    for (int w2 = 4; w2 <= 120 && bridges_found < 4; w2 += 2) {
                                        for (int k2 = 2; k2 <= w2 - 2 && bridges_found < 4; k2++) {
                                            int a2 = (junc_idx - k2 + 1 + L_raw) % L_raw;
                                            for (int b_try = 0; b_try < 4 && bridges_found < 4; b_try++) {
                                                int test_ring[MAX_LEN], test_L = L_raw;
                                                memcpy(test_ring, base_ring, sizeof(int) * L_raw);
                                                sync_coil_state(e_out, test_ring, test_L);
                                                if (!fast_coil_window(e_out, test_ring, &test_L, a2, w2, gain2, 60000, NULL, false)) {
                                                    if (b_try == 0) break;
                                                    continue;
                                                }
                                                if (!verify_coil_ring(n_out, test_ring, test_L)) continue;
                                                uint64_t bh = hash_ring_set(test_ring, test_L);
                                                bool bdup = false;
                                                for (int z = 0; z < bridges_found; z++) if (seen_br[z] == bh) { bdup = true; break; }
                                                if (bdup) continue;
                                                seen_br[bridges_found++] = bh;
                                                if (gain2 > best_gain2) best_gain2 = gain2;

                                                printf("    [STEP 2 junc=%d #%d] Valid Q_%d Coil L=%d (w2=%d k2=%d gain2=%d)!\n",
                                                       junc, bridges_found, n_out, test_L, w2, k2, gain2);
                                                fflush(stdout);
                                                if (test_L > best_out_L) {
                                                    best_out_L = test_L;
                                                    char fn[256];
                                                    snprintf(fn, sizeof(fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                                    save_coil_file(fn, test_ring, test_L);
                                                }
                                                sweep_coil_plus(e_out, test_ring, &test_L, &best_out_L, out_prefix);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    printf("[SUMMARY MULTI_LIFT_COIL] n_out=%d best_L=%d\n", n_out, best_out_L);
    free(e_in); free(e_out);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage:\n"
                        "  %s ils_snake <n> <rounds> <seed_file> <out_prefix>\n"
                        "  %s ils_coil  <n> <rounds> <seed_file> <out_prefix>\n"
                        "  %s ils_sym   <n> <rounds> <seed_file> <out_prefix>\n"
                        "  %s lift_sym  <n_in> <max_detours> <seed_file> <out_prefix>\n"
                        "  %s lift_coil <n_in> <max_detours> <seed_file> <out_prefix>\n",
                argv[0], argv[0], argv[0], argv[0], argv[0]);
        return 1;
    }
    const char *mode = argv[1];
    int p1 = atoi(argv[2]);
    int p2 = atoi(argv[3]);
    const char *seed = argv[4];
    const char *out = argv[5];

    if (strcmp(mode, "ils_snake") == 0) return run_ils_snake(p1, p2, seed, out);
    if (strcmp(mode, "ils_coil") == 0)  return run_ils_coil(p1, p2, seed, out);
    if (strcmp(mode, "ils_sym") == 0)   return run_ils_sym(p1, p2, seed, out);
    if (strcmp(mode, "lift_sym") == 0)  return run_multi_lift_sym(p1, p2, seed, out);
    if (strcmp(mode, "lift_coil") == 0) return run_multi_lift_coil(p1, p2, seed, out);
    fprintf(stderr, "Unknown mode: %s\n", mode);
    return 1;
}
