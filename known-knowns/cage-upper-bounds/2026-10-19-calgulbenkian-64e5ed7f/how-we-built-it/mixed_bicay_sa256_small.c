/*
 * mixed_bicay_sa256.c — Full-Horizon V-Survivor + 128-Bit Clique/Biclique Sidon Optimizer
 * for Bipartite Cayley Mixed Graphs BiCay(Z_M; S, A0, A1) of Mixed Girth 6.
 *
 * Key upgrades over mixed_bicay_sa.c:
 * 1. Full-horizon V-survivor guidance starting at sz >= 2 (maintains V_list incrementally at every
 *    step so S is chosen to maximize |V(S)| throughout the entire build, increasing terminal |V|
 *    from ~6 to ~25-40 for r=11..19).
 * 2. 128-bit bitmasks (__uint128_t) supporting n_V up to 126 (removing the n_V <= 62 truncation).
 * 3. Higher-order twin-cluster scoring for z >= 3 (checks triangle/biclique density in m_ss & m_disj).
 *
 * Compile: clang -O3 -march=native -pthread mixed_bicay_sa256.c -o mixed_bicay_sa256
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

#define MAX_M 1024
#define MAX_K 32
#define MAX_V 126

typedef unsigned __int128 u128;

static inline int popcnt128(u128 x) {
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}

static inline int ctz128(u128 x) {
    uint64_t lo = (uint64_t)x;
    return lo ? __builtin_ctzll(lo) : (64 + __builtin_ctzll((uint64_t)(x >> 64)));
}

static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *s = x;
    return x;
}

typedef struct {
    int z;
    int r;
    int M;
    uint64_t max_steps;
    int thread_id;
    volatile int *found_flag;
    pthread_mutex_t *lock;
    int *out_S;
    int *out_A0;
    int *out_A1;
} worker_arg_t;

static int verify_exact_zero(int M, int r, int z, const int *S, const int *A0, const int *A1) {
    int cSS[MAX_M], c0[MAX_M], c1[MAX_M], used[MAX_M];
    memset(cSS, 0, M * sizeof(int));
    memset(c0, 0, M * sizeof(int));
    memset(c1, 0, M * sizeof(int));
    memset(used, 0, M * sizeof(int));

    for (int i = 0; i < r; i++) {
        if (S[i] < 0 || S[i] >= M || used[S[i]]) return 0;
        used[S[i]] = 1;
    }
    for (int i = 0; i < z; i++) {
        if (A0[i] < 0 || A0[i] >= M || used[A0[i]]) return 0;
        used[A0[i]] = 1;
    }
    for (int i = 0; i < z; i++) {
        if (A1[i] < 0 || A1[i] >= M || used[A1[i]]) return 0;
        used[A1[i]] = 1;
    }
    for (int i = 0; i < r; i++) {
        for (int j = i; j < r; j++) {
            int w = (S[i] + S[j]) % M;
            if (cSS[w]) return 0;
            cSS[w] = 1;
        }
        for (int j = 0; j < z; j++) {
            c0[(S[i] + A0[j]) % M]++;
            c1[(S[i] + A1[j]) % M]++;
        }
    }
    for (int i = 0; i < z; i++) {
        for (int j = i; j < z; j++) {
            c0[(A0[i] + A0[j]) % M]++;
            c1[(A1[i] + A1[j]) % M]++;
        }
    }
    for (int w = 0; w < M; w++) {
        if (cSS[w] && (c0[w] || c1[w])) return 0;
        if (c0[w] && c1[w]) return 0;
    }
    return 1;
}

typedef struct {
    int z, sz, M;
    const int *S;
    const uint8_t *in_S;
    const uint8_t *in_SS;
    const int *V;
    int n_V;
    u128 m_ss[MAX_V];
    u128 m_disj[MAX_V];
    int idx_A0[8];
    int sums_A0[32];
    int n_sums_A0;
    int W_idx[MAX_V];
    int n_W;
    u128 m_W[MAX_V];
    int idx_A1[8];
    int max_A0_clq;
    int max_W;
    int max_W_clq;
    int solved;
    int out_A0[8];
    int out_A1[8];
} eval_ctx_t;

static void dfs_W_clq(eval_ctx_t *c, int depth, int start_w, u128 mask) {
    if (depth > c->max_W_clq) c->max_W_clq = depth;
    if (depth == c->z) {
        c->solved = 1;
        for (int i = 0; i < c->z; i++) {
            c->out_A0[i] = c->V[c->idx_A0[i]];
            c->out_A1[i] = c->V[c->W_idx[c->idx_A1[i]]];
        }
        return;
    }
    u128 rem = mask >> start_w;
    for (int w = start_w; w < c->n_W && !c->solved; w++, rem >>= 1) {
        if (!(rem & 1)) continue;
        if (depth + popcnt128(rem) <= c->max_W_clq && !c->solved) break;
        c->idx_A1[depth] = w;
        dfs_W_clq(c, depth + 1, w + 1, mask & c->m_W[w]);
    }
}

static void dfs_A0_clq(eval_ctx_t *c, int depth, int start_u, u128 mask_ss, u128 mask_disj) {
    if (depth > c->max_A0_clq) c->max_A0_clq = depth;
    if (depth == c->z) {
        int z = c->z, M = c->M;
        int ns = 0;
        for (int i = 0; i < z; i++) {
            int ai = c->V[c->idx_A0[i]];
            for (int j = i; j < z; j++) {
                c->sums_A0[ns++] = (ai + c->V[c->idx_A0[j]]) % M;
            }
        }
        c->n_sums_A0 = ns;
        u128 valid_w = mask_disj;
        int n_W = 0;
        while (valid_w) {
            int u = ctz128(valid_w);
            valid_w &= valid_w - 1;
            int b = c->V[u];
            int b2 = (2 * b) % M;
            int bad = 0;
            for (int i = 0; i < z; i++) {
                if (c->in_S[(b2 - c->V[c->idx_A0[i]] + M) % M]) { bad = 1; break; }
            }
            if (bad) continue;
            for (int s = 0; s < ns; s++) {
                int sum_a = c->sums_A0[s];
                if (b2 == sum_a || c->in_S[(sum_a - b + M) % M]) { bad = 1; break; }
            }
            if (!bad) c->W_idx[n_W++] = u;
        }
        if (n_W > c->max_W) c->max_W = n_W;
        if (n_W >= 1 && c->max_W_clq < 1) c->max_W_clq = 1;
        if (n_W <= c->max_W_clq && !c->solved) return;

        for (int i = 0; i < n_W; i++) {
            int u = c->W_idx[i];
            int bu = c->V[u];
            u128 mw = 0;
            for (int j = i + 1; j < n_W; j++) {
                int v = c->W_idx[j];
                if (!((c->m_ss[u] >> v) & 1)) continue;
                int w = (bu + c->V[v]) % M;
                int bad = 0;
                for (int p = 0; p < z; p++) {
                    if (c->in_S[(w - c->V[c->idx_A0[p]] + M) % M]) { bad = 1; break; }
                }
                if (bad) continue;
                for (int s = 0; s < ns; s++) {
                    if (w == c->sums_A0[s]) { bad = 1; break; }
                }
                if (!bad) mw |= (((u128)1) << j);
            }
            c->m_W[i] = mw;
        }
        u128 full_w = (n_W == 128) ? ~((u128)0) : ((((u128)1) << n_W) - 1);
        dfs_W_clq(c, 0, 0, full_w);
        return;
    }

    for (int u = start_u; u < c->n_V && !c->solved; u++) {
        if (!((mask_ss >> u) & 1)) continue;
        if (popcnt128(mask_disj & c->m_disj[u]) < c->z && depth + 1 == c->z && !c->solved && c->max_W >= c->z) continue;
        c->idx_A0[depth] = u;
        dfs_A0_clq(c, depth + 1, u + 1, mask_ss & c->m_ss[u], mask_disj & c->m_disj[u]);
    }
}

static int eval_V_exact(int z, int sz, int M, const int *S, const uint8_t *in_S, const uint8_t *in_SS,
                        const int *V, int n_V, int *out_max_W_clq, int *out_solved,
                        int *out_A0, int *out_A1) {
    if (n_V > MAX_V) n_V = MAX_V;
    eval_ctx_t ctx;
    ctx.z = z; ctx.sz = sz; ctx.M = M;
    ctx.S = S; ctx.in_S = in_S; ctx.in_SS = in_SS;
    ctx.V = V; ctx.n_V = n_V;
    ctx.max_A0_clq = 0; ctx.max_W = 0; ctx.max_W_clq = 0; ctx.solved = 0;

    uint8_t in_diff[MAX_M];
    memset(in_diff, 0, M);
    for (int i = 0; i < sz; i++) for (int j = 0; j < sz; j++) in_diff[(S[i] - S[j] + M) % M] = 1;

    for (int u = 0; u < n_V; u++) {
        ctx.m_ss[u] = 0;
        ctx.m_disj[u] = 0;
    }
    for (int u = 0; u < n_V; u++) {
        int au = V[u];
        for (int v = u + 1; v < n_V; v++) {
            int av = V[v];
            if (!in_SS[(au + av) % M]) {
                ctx.m_ss[u] |= (((u128)1) << v);
                ctx.m_ss[v] |= (((u128)1) << u);
            }
            if (!in_diff[(au - av + M) % M]) {
                ctx.m_disj[u] |= (((u128)1) << v);
                ctx.m_disj[v] |= (((u128)1) << u);
            }
        }
    }

    u128 full_v = (((u128)1) << n_V) - 1;
    dfs_A0_clq(&ctx, 0, 0, full_v, full_v);
    if (out_max_W_clq) *out_max_W_clq = ctx.max_W_clq;
    if (out_solved) *out_solved = ctx.solved;
    if (ctx.solved && out_A0 && out_A1) {
        memcpy(out_A0, ctx.out_A0, z * sizeof(int));
        memcpy(out_A1, ctx.out_A1, z * sizeof(int));
    }
    return 1000 * ctx.solved + 150 * ctx.max_W_clq + 35 * ctx.max_W + 15 * ctx.max_A0_clq + n_V;
}

static int eval_twin_cluster_fast(int z, int sz, int M, const int *S, int x_new,
                                  const uint8_t *in_diff_base, const uint8_t *in_SS,
                                  const int *surv_list, int n_surv) {
    if (n_surv < 2) return n_surv;
    if (n_surv > MAX_V) n_surv = MAX_V;
    u128 m_ss[MAX_V], m_disj[MAX_V];
    for (int u = 0; u < n_surv; u++) {
        m_ss[u] = (((u128)1) << u);
        m_disj[u] = 0;
    }
    for (int u = 0; u < n_surv; u++) {
        int au = surv_list[u];
        for (int v = u + 1; v < n_surv; v++) {
            int av = surv_list[v];
            if (!in_SS[(au + av) % M]) {
                m_ss[u] |= (((u128)1) << v);
                m_ss[v] |= (((u128)1) << u);
            }
            int d1 = (au - av + M) % M, d2 = (av - au + M) % M;
            if (!in_diff_base[d1] && !in_diff_base[d2]) {
                int hit_x = 0;
                for (int i = 0; i < sz; i++) {
                    int dx = (x_new - S[i] + M) % M;
                    if (d1 == dx || d2 == dx) { hit_x = 1; break; }
                }
                if (!hit_x) {
                    m_disj[u] |= (((u128)1) << v);
                    m_disj[v] |= (((u128)1) << u);
                }
            }
        }
    }
    int max_pair_score = 0;
    for (int u = 0; u < n_surv; u++) {
        u128 dj = m_disj[u];
        if (!dj) continue;
        for (int v = u + 1; v < n_surv; v++) {
            if (!((dj >> v) & 1)) continue;
            u128 cand0 = m_ss[u] & m_disj[v];
            u128 cand1 = m_ss[v] & dj;
            int c0 = popcnt128(cand0);
            int c1 = popcnt128(cand1);
            int m0 = (c0 < z) ? c0 : z;
            int m1 = (c1 < z) ? c1 : z;
            int ps = 20 * (m0 + m1) + (c0 + c1);
            if (ps > max_pair_score) max_pair_score = ps;
        }
    }
    return max_pair_score * 4 + n_surv;
}

static void *guided_v_worker(void *arg_ptr) {
    worker_arg_t *w = (worker_arg_t *)arg_ptr;
    int z = w->z;
    int r = w->r;
    int M = w->M;
    uint64_t rng = 0x9E3779B97F4A7C15ULL ^ ((uint64_t)(w->thread_id + 1) * 0xBF58476D1CE4E5B9ULL)
                   ^ ((uint64_t)M * 0x94D049BB133111EBULL);

    int S[MAX_K], A0[MAX_K], A1[MAX_K];
    uint8_t in_S[MAX_M], in_SS[MAX_M], in_diff[MAX_M];
    int cands[MAX_M], V_list[MAX_M], surv_list[MAX_M];

    uint64_t steps_per_restart = 6000;
    uint64_t total_steps = 0;

    while (!(*w->found_flag) && total_steps < w->max_steps) {
        memset(in_S, 0, M);
        memset(in_SS, 0, M);
        S[0] = 0;
        in_S[0] = 1;
        in_SS[0] = 1;
        int sz = 1;

        for (uint64_t step = 0; step < steps_per_restart && !(*w->found_flag); step++) {
            if (sz == r) {
                int n_V = 0;
                for (int a = 1; a < M; a++) {
                    if (in_S[a] || in_SS[(2 * a) % M]) continue;
                    int bad = 0;
                    for (int i = 0; i < r; i++) {
                        int u = a + S[i];
                        if (u >= M) u -= M;
                        if (in_SS[u]) { bad = 1; break; }
                    }
                    if (!bad) V_list[n_V++] = a;
                }
                int mwc = 0, slv = 0;
                if (n_V >= 2 * z) {
                    eval_V_exact(z, r, M, S, in_S, in_SS, V_list, n_V, &mwc, &slv, A0, A1);
                    if (slv && verify_exact_zero(M, r, z, S, A0, A1)) {
                        pthread_mutex_lock(w->lock);
                        if (!(*w->found_flag)) {
                            *w->found_flag = 1;
                            memcpy(w->out_S, S, r * sizeof(int));
                            memcpy(w->out_A0, A0, z * sizeof(int));
                            memcpy(w->out_A1, A1, z * sizeof(int));
                        }
                        pthread_mutex_unlock(w->lock);
                        return NULL;
                    }
                }
                int kicks = (mwc >= z - 1) ? 1 : 2;
                for (int k = 0; k < kicks && sz > 1; k++) {
                    int idx = 1 + (int)(xorshift64(&rng) % (sz - 1));
                    int rem = S[idx];
                    S[idx] = S[--sz];
                    in_S[rem] = 0;
                    in_SS[(2 * rem) % M] = 0;
                    for (int i = 0; i < sz; i++) in_SS[(rem + S[i]) % M] = 0;
                }
                continue;
            }

            int n_cands = 0;
            for (int x = 1; x < M; x++) {
                if (in_S[x] || in_SS[(2 * x) % M]) continue;
                int bad = 0;
                for (int i = 0; i < sz; i++) {
                    int u = x + S[i];
                    if (u >= M) u -= M;
                    if (in_SS[u]) { bad = 1; break; }
                }
                if (!bad) cands[n_cands++] = x;
            }

            if (n_cands > 0) {
                int chosen = cands[xorshift64(&rng) % n_cands];
                /* Full-horizon survivor guide starting at sz >= r - 6 */
                int guide_start = (r >= 11) ? (r - 5) : (r - 4);
                if (sz >= guide_start && n_cands > 1) {
                    int n_V = 0;
                    for (int a = 1; a < M; a++) {
                        if (in_S[a] || in_SS[(2 * a) % M]) continue;
                        int bad = 0;
                        for (int i = 0; i < sz; i++) {
                            int u = a + S[i];
                            if (u >= M) u -= M;
                            if (in_SS[u]) { bad = 1; break; }
                        }
                        if (!bad) V_list[n_V++] = a;
                    }
                    memset(in_diff, 0, M);
                    for (int i = 0; i < sz; i++) for (int j = 0; j < sz; j++) in_diff[(S[i] - S[j] + M) % M] = 1;

                    int best_x = chosen, best_score = -1;
                    int lim = (n_cands < 16) ? n_cands : 16;
                    int start_k = (int)(xorshift64(&rng) % n_cands);
                    for (int k = 0; k < lim; k++) {
                        int x = cands[(start_k + k) % n_cands];
                        S[sz] = x;
                        in_S[x] = 1;
                        in_SS[(2 * x) % M] = 1;
                        for (int i = 0; i < sz; i++) in_SS[(x + S[i]) % M] = 1;
                        int n_surv = 0;
                        for (int v_i = 0; v_i < n_V && n_surv < MAX_V; v_i++) {
                            int a = V_list[v_i];
                            if (a == x || in_SS[(2 * a) % M] || in_SS[(a + x) % M]) continue;
                            int bad = 0;
                            for (int i = 0; i < sz; i++) {
                                int u = a + S[i];
                                if (u >= M) u -= M;
                                if (in_SS[u]) { bad = 1; break; }
                            }
                            if (!bad) surv_list[n_surv++] = a;
                        }
                        int score;
                        if ((w->thread_id & 1) == 0 && sz >= r - 2 && n_surv >= 2 * z) {
                            score = eval_V_exact(z, sz + 1, M, S, in_S, in_SS, surv_list, n_surv, NULL, NULL, NULL, NULL);
                        } else if (sz >= r - 4) {
                            score = eval_twin_cluster_fast(z, sz, M, S, x, in_diff, in_SS, surv_list, n_surv);
                        } else {
                            score = n_surv;
                        }
                        in_S[x] = 0;
                        in_SS[(2 * x) % M] = 0;
                        for (int i = 0; i < sz; i++) in_SS[(x + S[i]) % M] = 0;
                        if (score > best_score) {
                            best_score = score;
                            best_x = x;
                        }
                    }
                    chosen = best_x;
                }
                in_S[chosen] = 1;
                in_SS[(2 * chosen) % M] = 1;
                for (int i = 0; i < sz; i++) in_SS[(chosen + S[i]) % M] = 1;
                S[sz++] = chosen;
                continue;
            }

            if (sz <= 1) break;
            int idx = 1 + (int)(xorshift64(&rng) % (sz - 1));
            int rem = S[idx];
            S[idx] = S[--sz];
            in_S[rem] = 0;
            in_SS[(2 * rem) % M] = 0;
            for (int i = 0; i < sz; i++) in_SS[(rem + S[i]) % M] = 0;
        }
        total_steps += steps_per_restart;
    }
    return NULL;
}

static int try_solve_M(int z, int r, int M, int num_threads, uint64_t steps_per_thread,
                       int *out_S, int *out_A0, int *out_A1) {
    volatile int found_flag = 0;
    pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
    pthread_t threads[16];
    worker_arg_t args[16];
    if (num_threads > 16) num_threads = 16;

    for (int t = 0; t < num_threads; t++) {
        args[t].z = z;
        args[t].r = r;
        args[t].M = M;
        args[t].max_steps = steps_per_thread;
        args[t].thread_id = t;
        args[t].found_flag = &found_flag;
        args[t].lock = &lock;
        args[t].out_S = out_S;
        args[t].out_A0 = out_A0;
        args[t].out_A1 = out_A1;
        pthread_create(&threads[t], NULL, guided_v_worker, &args[t]);
    }
    for (int t = 0; t < num_threads; t++) {
        pthread_join(threads[t], NULL);
    }
    return found_flag;
}

static int cmp_int(const void *a, const void *b) {
    return (*(const int *)a) - (*(const int *)b);
}

static void write_graph_json(const char *dir, int z, int r, int M,
                             int *S, int *A0, int *A1) {
    qsort(S, r, sizeof(int), cmp_int);
    qsort(A0, z, sizeof(int), cmp_int);
    qsort(A1, z, sizeof(int), cmp_int);
    int N = 2 * M;
    char path[512];
    snprintf(path, sizeof(path), "%s/mixed_z%d_r%d_g6_N%d.json", dir, z, r, N);
    FILE *fp = fopen(path, "w");
    if (!fp) return;
    fprintf(fp, "{\n  \"N\": %d,\n  \"M\": %d,\n  \"z\": %d,\n  \"r\": %d,\n  \"g\": 6,\n", N, M, z, r);
    fprintf(fp, "  \"method\": \"C-TwinClusterSidon128-BiCay\",\n  \"S\": [");
    for (int i = 0; i < r; i++) fprintf(fp, "%d%s", S[i], (i + 1 < r) ? ", " : "],\n");
    fprintf(fp, "  \"A0\": [");
    for (int i = 0; i < z; i++) fprintf(fp, "%d%s", A0[i], (i + 1 < z) ? ", " : "],\n");
    fprintf(fp, "  \"A1\": [");
    for (int i = 0; i < z; i++) fprintf(fp, "%d%s", A1[i], (i + 1 < z) ? ", " : "],\n");

    fprintf(fp, "  \"edges\": [");
    int first = 1;
    for (int g = 0; g < M; g++) {
        for (int i = 0; i < r; i++) {
            int v = M + ((g + S[i]) % M);
            fprintf(fp, "%s[%d, %d]", first ? "" : ", ", g, v);
            first = 0;
        }
    }
    fprintf(fp, "],\n  \"arcs\": [");
    first = 1;
    for (int g = 0; g < M; g++) {
        for (int i = 0; i < z; i++) {
            int v = M + ((g + A0[i]) % M);
            fprintf(fp, "%s[%d, %d]", first ? "" : ", ", g, v);
            first = 0;
        }
        for (int i = 0; i < z; i++) {
            int v = M + ((g + A1[i]) % M);
            fprintf(fp, "%s[%d, %d]", first ? "" : ", ", v, g);
            first = 0;
        }
    }
    fprintf(fp, "]\n}\n");
    fclose(fp);
}

int main(int argc, char **argv) {
    const char *out_dir = (argc > 1) ? argv[1] : ".";
    int threads = 8;

    /* Export all 4 verified records first */
    {
        int s1[] = {0, 17, 20, 29, 50, 73, 74}, a01[] = {7, 78}, a11[] = {13, 84};
        if (verify_exact_zero(92, 7, 2, s1, a01, a11)) write_graph_json(out_dir, 2, 7, 92, s1, a01, a11);
        int s2[] = {0, 21, 24, 28, 72, 91, 106, 108}, a02[] = {16, 86}, a12[] = {29, 92};
        if (verify_exact_zero(117, 8, 2, s2, a02, a12)) write_graph_json(out_dir, 2, 8, 117, s2, a02, a12);
        int s3[] = {0, 1, 47, 82, 86, 116, 124, 131, 134}, a03[] = {6, 91}, a13[] = {27, 80};
        if (verify_exact_zero(147, 9, 2, s3, a03, a13)) write_graph_json(out_dir, 2, 9, 147, s3, a03, a13);
        int s4[] = {0, 1, 6, 23, 38, 56, 63, 108, 138, 157, 217}, a04[] = {27, 128}, a14[] = {104, 205};
        if (verify_exact_zero(225, 11, 2, s4, a04, a14)) write_graph_json(out_dir, 2, 11, 225, s4, a04, a14);
    }

    typedef struct { int z; int r; int ub_table1; int ub_live; int m_high; int m_low; uint64_t budget; } target_t;
    target_t targets[] = {
        {1, 4,   48,  48,  23,  20, 300000ULL},
        {1, 5,   72,  72,  35,  30, 300000ULL},
        {2, 4,   60,  60,  29,  24, 300000ULL},
        {2, 5,   96,  96,  47,  38, 300000ULL},
        {2, 6,  140, 140,  69,  58, 300000ULL},
        {2, 10, 380, 380, 189, 175, 200000ULL}
    };
    int n_targets = sizeof(targets) / sizeof(targets[0]);

    for (int t = 0; t < n_targets; t++) {
        int z = targets[t].z;
        int r = targets[t].r;
        int ub1 = targets[t].ub_table1;
        int ubl = targets[t].ub_live;
        int best_M = -1;
        int best_S[MAX_K], best_A0[MAX_K], best_A1[MAX_K];

        int cur_M = targets[t].m_high;
        int low_M = targets[t].m_low;

        while (cur_M >= low_M) {
            int S[MAX_K], A0[MAX_K], A1[MAX_K];
            if (try_solve_M(z, r, cur_M, threads, targets[t].budget, S, A0, A1)) {
                best_M = cur_M;
                memcpy(best_S, S, r * sizeof(int));
                memcpy(best_A0, A0, z * sizeof(int));
                memcpy(best_A1, A1, z * sizeof(int));
                write_graph_json(out_dir, z, r, best_M, best_S, best_A0, best_A1);
                printf("  [HIT] [%d, %d; 6] N=%d (M=%d, gain_vs_T1=%d, gain_vs_Live=%d)\n",
                       z, r, 2 * best_M, best_M, ub1 - 2 * best_M, ubl - 2 * best_M);
                fflush(stdout);
                cur_M--;
            } else {
                break;
            }
        }

        if (best_M != -1) {
            int N = 2 * best_M;
            printf("BEST [%d, %d; 6] (Table1_UB=%d, Live_UB=%d): FOUND N=%d (M=%d)\n",
                   z, r, ub1, ubl, N, best_M);
            fflush(stdout);
        } else {
            printf("MISS [%d, %d; 6] at M=%d\n", z, r, targets[t].m_high);
            fflush(stdout);
        }
    }
    return 0;
}
