#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define MAX_N 14
#define MAX_V (1 << MAX_N)
#define MAX_LEN 8192
#define MAX_K 256

typedef struct {
    uint64_t w[4];
} u256;

static inline u256 u256_zero(void) { return (u256){{0, 0, 0, 0}}; }
static inline bool u256_is_zero(u256 a) { return (a.w[0] | a.w[1] | a.w[2] | a.w[3]) == 0; }
static inline bool u256_eq(u256 a, u256 b) { return ((a.w[0] ^ b.w[0]) | (a.w[1] ^ b.w[1]) | (a.w[2] ^ b.w[2]) | (a.w[3] ^ b.w[3])) == 0; }
static inline u256 u256_or(u256 a, u256 b) { return (u256){{a.w[0] | b.w[0], a.w[1] | b.w[1], a.w[2] | b.w[2], a.w[3] | b.w[3]}}; }
static inline u256 u256_and(u256 a, u256 b) { return (u256){{a.w[0] & b.w[0], a.w[1] & b.w[1], a.w[2] & b.w[2], a.w[3] & b.w[3]}}; }
static inline u256 u256_andnot(u256 a, u256 b) { return (u256){{a.w[0] & ~b.w[0], a.w[1] & ~b.w[1], a.w[2] & ~b.w[2], a.w[3] & ~b.w[3]}}; }
static inline void u256_set(u256 *a, int bit) { a->w[bit >> 6] |= (1ULL << (bit & 63)); }
static inline int u256_test(u256 a, int bit) { return (int)((a.w[bit >> 6] >> (bit & 63)) & 1ULL); }
static inline int u256_popcnt(u256 a) {
    return __builtin_popcountll(a.w[0]) + __builtin_popcountll(a.w[1]) +
           __builtin_popcountll(a.w[2]) + __builtin_popcountll(a.w[3]);
}
static inline int u256_ctz(u256 a) {
    if (a.w[0]) return __builtin_ctzll(a.w[0]);
    if (a.w[1]) return 64 + __builtin_ctzll(a.w[1]);
    if (a.w[2]) return 128 + __builtin_ctzll(a.w[2]);
    return 192 + __builtin_ctzll(a.w[3]);
}
static inline void u256_clear_lsb(u256 *a) {
    for (int i = 0; i < 4; i++) {
        if (a->w[i]) { a->w[i] &= a->w[i] - 1; return; }
    }
}
static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    *s = x; return x;
}

typedef struct {
    int n;
    int N;
    int t;
    uint64_t rng;
    int used[MAX_V];
    int cnt[MAX_V];
    int K;
    int w_verts[MAX_K];
    int d1[MAX_K];
    u256 adj[MAX_K];
    u256 twin_conflict[MAX_K];
    u256 even_mask;
    u256 odd_mask;
    u256 orig_mask;
    int nodes;
    int limit;
    int route_idx[MAX_K];
    int route_len;
} SymSearch;

static void add_pair(SymSearch *s, int v, int sign) {
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

static bool verify_sym_ring(int n, const int *ring, int h) {
    if (h < 2 || 2 * h >= MAX_LEN) return false;
    int L = 2 * h;
    int N = 1 << n;
    int *pos = (int *)malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) pos[i] = -1;
    int t = ring[0] ^ ring[h];
    if (__builtin_popcount((unsigned)t) < 2) { free(pos); return false; }
    for (int i = 0; i < L; i++) {
        int v = ring[i];
        if (v < 0 || v >= N || pos[v] >= 0) { free(pos); return false; }
        pos[v] = i;
        int next_v = ring[(i + 1) % L];
        if (__builtin_popcount((unsigned)(v ^ next_v)) != 1) { free(pos); return false; }
        if ((ring[(i + h) % L] ^ v) != t) { free(pos); return false; }
    }
    for (int i = 0; i < L; i++) {
        int u = ring[i];
        for (int b = 0; b < n; b++) {
            int j = pos[u ^ (1 << b)];
            if (j >= 0) {
                int diff = (i - j + L) % L;
                if (diff != 1 && diff != L - 1) { free(pos); return false; }
            }
        }
    }
    free(pos);
    return true;
}

static void reset_sym_ring(SymSearch *s, const int *ring, int h) {
    memset(s->used, 0, sizeof(int) * s->N);
    memset(s->cnt, 0, sizeof(int) * s->N);
    s->t = ring[0] ^ ring[h];
    for (int i = 0; i < h; i++) add_pair(s, ring[i], 1);
}

static bool bitset_dfs(SymSearch *s, int u, int rem, u256 avail, u256 visited_mask) {
    if (++s->nodes > s->limit) return false;
    if (rem == 2) {
        u256 cands = u256_and(u256_and(s->adj[u], s->adj[1]), avail);
        while (!u256_is_zero(cands)) {
            int v = u256_ctz(cands);
            u256_clear_lsb(&cands);
            u256 final_mask = visited_mask;
            u256_set(&final_mask, v);
            if (u256_eq(final_mask, s->orig_mask)) continue;
            s->route_idx[s->route_len++] = v;
            return true;
        }
        return false;
    }
    u256 goal_nbrs = u256_and(s->adj[1], avail);
    if (u256_is_zero(goal_nbrs)) return false;
    if (rem >= 4) {
        u256 reach = u256_zero(); u256_set(&reach, u);
        int dist_goal = -1, step = 1;
        u256 cur_f = u256_and(s->adj[u], avail);
        while (!u256_is_zero(cur_f)) {
            if (dist_goal < 0 && !u256_is_zero(u256_and(cur_f, goal_nbrs))) dist_goal = step + 1;
            reach = u256_or(reach, cur_f);
            if (step >= rem - 1) break;
            u256 nxt = u256_zero(), tmp = cur_f;
            while (!u256_is_zero(tmp)) {
                int idx = u256_ctz(tmp);
                u256_clear_lsb(&tmp);
                nxt = u256_or(nxt, s->adj[idx]);
            }
            cur_f = u256_andnot(u256_and(nxt, avail), reach);
            step++;
        }
        if (dist_goal < 0 || dist_goal > rem) return false;
        int u_par = u256_test(s->even_mask, u);
        int need_opp = rem / 2, need_same = (rem - 1) / 2;
        u256 u_bit = u256_zero(); u256_set(&u_bit, u);
        u256 interior_reach = u256_andnot(reach, u_bit);
        int cnt_even = u256_popcnt(u256_and(interior_reach, s->even_mask));
        int cnt_odd  = u256_popcnt(u256_and(interior_reach, s->odd_mask));
        if (u_par == 1) { if (cnt_odd < need_opp || cnt_even < need_same) return false; }
        else { if (cnt_even < need_opp || cnt_odd < need_same) return false; }
    }
    u256 cands = u256_andnot(u256_and(s->adj[u], avail), s->adj[1]);
    if (u256_is_zero(cands)) return false;
    int cand_list[16], nc = 0;
    while (!u256_is_zero(cands)) {
        int v = u256_ctz(cands);
        u256_clear_lsb(&cands);
        if (s->d1[v] <= rem - 1) cand_list[nc++] = v;
    }
    if (nc == 0) return false;
    for (int i = nc - 1; i > 0; i--) {
        int j = (int)(xorshift64(&s->rng) % (uint64_t)(i + 1));
        int tmp = cand_list[i]; cand_list[i] = cand_list[j]; cand_list[j] = tmp;
    }
    u256 block_u = s->adj[u];
    for (int idx = 0; idx < nc; idx++) {
        int v = cand_list[idx];
        u256 v_bit = u256_zero(); u256_set(&v_bit, v);
        u256 forbid = u256_or(u256_or(block_u, v_bit), s->twin_conflict[v]);
        u256 next_avail = u256_andnot(avail, forbid);
        s->route_idx[s->route_len++] = v;
        if (bitset_dfs(s, v, rem - 1, next_avail, u256_or(visited_mask, v_bit))) return true;
        s->route_len--;
        if (s->nodes > s->limit) break;
    }
    return false;
}

static bool detour_avoiding_layer(SymSearch *s, int *ring, int *h_ptr, int a, int w, int gain, int budget, const int *forbid_layer) {
    int h = *h_ptr, L = 2 * h, new_w = w + gain;
    if (w < 2 || w > h - 2 || new_w < 2 || new_w > 120) return false;
    reset_sym_ring(s, ring, h);
    int start_v = ring[a], target_v = ring[(a + w) % L];
    int hd0 = __builtin_popcount((unsigned)(start_v ^ target_v));
    if (hd0 > new_w || ((hd0 ^ new_w) & 1)) return false;
    for (int k = 1; k < w; k++) add_pair(s, ring[(a + k) % L], -1);

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
    for (int i = 2; i < M; i++) if (dist0[i] + dist1[i] <= new_w) keep[i] = 1;
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
    for (int i = 2; i < M; i++) {
        if (keep[i]) {
            if (K >= MAX_K) { free(cand_v); free(v_to_idx); free(dist0); free(dist1); free(keep); free(q); return false; }
            s->w_verts[K] = cand_v[i]; s->d1[K] = dist1[i]; v_to_idx[cand_v[i]] = K; K++;
        }
    }
    free(cand_v); free(dist0); free(dist1); free(keep); free(q);
    if (K - 2 < new_w - 1) { free(v_to_idx); return false; }
    s->K = K;
    s->even_mask = u256_zero(); s->odd_mask = u256_zero();
    for (int i = 0; i < K; i++) {
        s->adj[i] = u256_zero(); s->twin_conflict[i] = u256_zero();
        int u = s->w_verts[i];
        if (__builtin_popcount((unsigned)u) & 1) u256_set(&s->odd_mask, i);
        else u256_set(&s->even_mask, i);
        for (int b = 0; b < s->n; b++) {
            int nb = v_to_idx[u ^ (1 << b)];
            if (nb >= 0) u256_set(&s->adj[i], nb);
        }
        int ut = u ^ s->t, twin_idx = v_to_idx[ut];
        if (twin_idx >= 0) u256_set(&s->twin_conflict[i], twin_idx);
        for (int b = 0; b < s->n; b++) {
            int tnb = v_to_idx[ut ^ (1 << b)];
            if (tnb >= 0) u256_set(&s->twin_conflict[i], tnb);
        }
    }
    s->orig_mask = u256_zero();
    free(v_to_idx);
    u256 avail = u256_zero();
    for (int i = 2; i < K; i++) u256_set(&avail, i);
    s->route_len = 0; s->nodes = 0; s->limit = budget;
    if (!bitset_dfs(s, 0, new_w, avail, u256_zero())) return false;

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

static void save_coil_ring(const char *out_path, const int *ring, int h) {
    FILE *f = fopen(out_path, "w");
    if (!f) return;
    int L = 2 * h;
    const char *b36 = "0123456789abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < L; i++) {
        int diff = ring[i] ^ ring[(i + 1) % L];
        int step = __builtin_ctz((unsigned)diff);
        fputc(b36[step], f);
    }
    fputc('\n', f);
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s [n_in] [seed_file] [out_prefix]\n", argv[0]);
        return 1;
    }
    int n_in = atoi(argv[1]);
    int n_out = n_in + 1;
    const char *seed_file = argv[2];
    const char *out_prefix = argv[3];

    FILE *f = fopen(seed_file, "r");
    if (!f) { perror("fopen"); return 1; }
    int steps[MAX_LEN], L = 0, val;
    while (fscanf(f, "%d", &val) == 1) steps[L++] = val;
    fclose(f);
    int h = L / 2;
    int orig_ring[MAX_LEN], v = 0;
    for (int i = 0; i < L; i++) { orig_ring[i] = v; v ^= (1 << steps[i]); }
    int t = orig_ring[0] ^ orig_ring[h];

    SymSearch s_in, s_out;
    memset(&s_in, 0, sizeof(s_in));
    s_in.n = n_in; s_in.N = 1 << n_in; s_in.rng = 42ULL;
    memset(&s_out, 0, sizeof(s_out));
    s_out.n = n_out; s_out.N = 1 << n_out; s_out.rng = 42ULL;

    int best_out_L = 0;
    for (int b = 0; b < n_in; b++) {
        if ((t >> b) & 1) continue;
        int flips[16], nf = 0;
        for (int i = 0; i < h; i++) {
            if (steps[i] == b && nf < 16) flips[nf++] = i;
        }
        if (nf != 2) continue;
        int delta = 1 << b;
        printf("=== Testing n_in=%d -> n_out=%d on coord b=%d (delta=%d) flips=(%d, %d) ===\n",
               n_in, n_out, b, delta, flips[0], flips[1]);

        for (int dir = 0; dir < 2; dir++) {
            int c_bridge = flips[dir];
            int c_detour = flips[1 - dir];

            int forbid[MAX_V] = {0};
            for (int i = 0; i < L; i++) forbid[orig_ring[i] ^ delta] = 1;

            bool found_detour = false;
            int det_ring[MAX_LEN], det_h = h;
            for (int gain = 2; gain >= -14 && !found_detour; gain -= 2) {
                for (int w = 6; w <= 60 && w <= h - 4 && !found_detour; w += 2) {
                    for (int k1 = 2; k1 <= w - 3; k1++) {
                        int a = (c_detour - k1 + L) % L;
                        det_h = h;
                        memcpy(det_ring, orig_ring, sizeof(int) * L);
                        if (detour_avoiding_layer(&s_in, det_ring, &det_h, a, w, gain, 50000, forbid)) {
                            found_detour = true;
                            printf("  [STEP 1] bridge=%d detour=%d: w=%d gain=%d -> det_h=%d\n",
                                   c_bridge, c_detour, w, gain, det_h);
                            break;
                        }
                    }
                }
            }
            if (!found_detour) continue;

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

            bool bridged = false;
            for (int gain2 = 3; gain2 >= -25 && !bridged; gain2 -= 2) {
                for (int w2 = 4; w2 <= 64 && w2 <= H_raw - 4 && !bridged; w2 += 2) {
                    for (int k1 = 2; k1 <= w2 - 2; k1++) {
                        int a = h - k1;
                        int test_ring[MAX_LEN], test_h = H_raw;
                        memcpy(test_ring, rot_full, sizeof(int) * L_out);
                        if (detour_avoiding_layer(&s_out, test_ring, &test_h, a, w2, gain2, 80000, NULL)) {
                            if (verify_sym_ring(n_out, test_ring, test_h)) {
                                printf("  [STEP 2] Valid Q_%d Symmetric Coil L=%d (h=%d) w2=%d gain2=%d!\n",
                                       n_out, 2 * test_h, test_h, w2, gain2);
                                fflush(stdout);
                                if (2 * test_h > best_out_L) {
                                    best_out_L = 2 * test_h;
                                    char out_fn[256];
                                    snprintf(out_fn, sizeof(out_fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                    save_coil_ring(out_fn, test_ring, test_h);
                                }
                                bool improved = true;
                                while (improved) {
                                    improved = false;
                                    for (int gw = 8; gw <= 64 && gw <= test_h - 4 && !improved; gw += 2) {
                                        for (int ga = 0; ga < test_h; ga++) {
                                            if (detour_avoiding_layer(&s_out, test_ring, &test_h, ga, gw, 2, 40000, NULL)) {
                                                if (verify_sym_ring(n_out, test_ring, test_h)) {
                                                    printf("    [POST-LIFT +2!] new L=%d (h=%d) at ga=%d gw=%d!\n",
                                                           2 * test_h, test_h, ga, gw);
                                                    fflush(stdout);
                                                    if (2 * test_h > best_out_L) {
                                                        best_out_L = 2 * test_h;
                                                        char out_fn[256];
                                                        snprintf(out_fn, sizeof(out_fn), "%s_Q%d_%d.txt", out_prefix, n_out, best_out_L);
                                                        save_coil_ring(out_fn, test_ring, test_h);
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
    printf("[SUMMARY] n_out=%d best_L=%d\n", n_out, best_out_L);
    return 0;
}
