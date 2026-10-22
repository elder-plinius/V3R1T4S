/*
 * mixed_bicay_general.c — Dual-Mode Multi-Threaded Solver for Bipartite Cayley Mixed Graphs
 * BiCay(Z_M; S, A0, A1) of Mixed Girth 6.
 *
 * Mode A (AP-Arcs + Lookahead Incremental Sidon Search):
 *   Fixes A0 = {0, 1, ..., z-1} and A1 = {b0, b0+d1, ..., b0+(z-1)d1} (with d1=1 or random)
 *   so |A0+A0| = 2z-1, |A1+A1| = 2z-1, and |A0-A1| = 2z-1 (when d1=1), then grows S of size r
 *   using exact incremental conflict arrays (cSS, c0, c1) + 1-step survivor lookahead + Tabu kicks.
 *
 * Compile: clang -O3 -march=native -pthread mixed_bicay_general.c -o mixed_bicay_general
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

#define MAX_M 1024
#define MAX_K 32

static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *s = x;
    return x;
}

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
    int z;
    int r;
    int M;
    uint64_t max_restarts;
    int thread_id;
    volatile int *found_flag;
    pthread_mutex_t *lock;
    int *out_S;
    int *out_A0;
    int *out_A1;
} worker_arg_t;

static inline int can_add_x(int x, int sz, int z, int M,
                            const int *S, const int *A0, const int *A1,
                            const uint8_t *used, const int *cSS, const int *c0, const int *c1) {
    if (used[x]) return 0;
    int x2 = x + x;
    if (x2 >= M) x2 -= M;
    if (cSS[x2] || c0[x2] || c1[x2]) return 0;

    for (int i = 0; i < sz; i++) {
        int w = x + S[i];
        if (w >= M) w -= M;
        if (cSS[w] || c0[w] || c1[w]) return 0;
    }
    for (int j = 0; j < z; j++) {
        int w0 = x + A0[j];
        if (w0 >= M) w0 -= M;
        if (cSS[w0] || c1[w0]) return 0;

        int w1 = x + A1[j];
        if (w1 >= M) w1 -= M;
        if (cSS[w1] || c0[w1]) return 0;
    }
    return 1;
}

static inline void do_add_x(int x, int *sz_ptr, int z, int M,
                            int *S, const int *A0, const int *A1,
                            uint8_t *used, int *cSS, int *c0, int *c1) {
    int sz = *sz_ptr;
    used[x] = 1;
    int x2 = (x + x) % M;
    cSS[x2] = 1;
    for (int i = 0; i < sz; i++) {
        cSS[(x + S[i]) % M] = 1;
    }
    for (int j = 0; j < z; j++) {
        c0[(x + A0[j]) % M]++;
        c1[(x + A1[j]) % M]++;
    }
    S[sz] = x;
    *sz_ptr = sz + 1;
}

static inline void do_rem_idx(int idx, int *sz_ptr, int z, int M,
                              int *S, const int *A0, const int *A1,
                              uint8_t *used, int *cSS, int *c0, int *c1) {
    int sz = *sz_ptr - 1;
    int x = S[idx];
    S[idx] = S[sz];
    *sz_ptr = sz;
    used[x] = 0;
    cSS[(x + x) % M] = 0;
    for (int i = 0; i < sz; i++) {
        cSS[(x + S[i]) % M] = 0;
    }
    for (int j = 0; j < z; j++) {
        c0[(x + A0[j]) % M]--;
        c1[(x + A1[j]) % M]--;
    }
}

static void *ap_sidon_worker(void *arg_ptr) {
    worker_arg_t *w = (worker_arg_t *)arg_ptr;
    int z = w->z;
    int r = w->r;
    int M = w->M;
    uint64_t rng = 0x9E3779B97F4A7C15ULL ^ ((uint64_t)(w->thread_id + 1) * 0xBF58476D1CE4E5B9ULL)
                   ^ ((uint64_t)M * 0x94D049BB133111EBULL);

    int S[MAX_K], A0[MAX_K], A1[MAX_K];
    int cSS[MAX_M], c0[MAX_M], c1[MAX_M];
    uint8_t used[MAX_M];
    uint64_t tabu[MAX_M];
    int cands[MAX_M];

    for (uint64_t restart = 0; restart < w->max_restarts && !(*w->found_flag); restart++) {
        memset(cSS, 0, M * sizeof(int));
        memset(c0, 0, M * sizeof(int));
        memset(c1, 0, M * sizeof(int));
        memset(used, 0, M * sizeof(uint8_t));
        memset(tabu, 0, M * sizeof(uint64_t));

        /* Initialize A0 and A1:
         * 75% of restarts: A0 = {0, 1, ..., z-1} and A1 = {b0, b0+d1, ...} with d1=1 or small
         * 25% of restarts: A0 = {0, d0, ...}, A1 random disjoint
         */
        for (int i = 0; i < z; i++) {
            A0[i] = i;
            used[i] = 1;
        }
        for (int i = 0; i < z; i++) {
            for (int j = i; j < z; j++) {
                c0[(A0[i] + A0[j]) % M]++;
            }
        }

        int ok_A1 = 0;
        for (int tries = 0; tries < 200 && !ok_A1; tries++) {
            int mode = (int)(xorshift64(&rng) & 3);
            int d1 = 1;
            if (mode == 1) d1 = 2;
            else if (mode == 2) d1 = 1 + (int)(xorshift64(&rng) % (M / 2));
            int b0 = z + (int)(xorshift64(&rng) % (M - z));

            int valid = 1;
            for (int i = 0; i < z; i++) {
                int v = (mode == 3) ? (z + (int)(xorshift64(&rng) % (M - z))) : ((b0 + i * d1) % M);
                if (used[v]) { valid = 0; break; }
                for (int k = 0; k < i; k++) if (A1[k] == v) { valid = 0; break; }
                A1[i] = v;
            }
            if (!valid) continue;
            for (int i = 0; i < z && valid; i++) {
                for (int j = i; j < z; j++) {
                    if (c0[(A1[i] + A1[j]) % M]) { valid = 0; break; }
                }
            }
            if (valid) ok_A1 = 1;
        }
        if (!ok_A1) continue;

        for (int i = 0; i < z; i++) {
            used[A1[i]] = 1;
            for (int j = i; j < z; j++) {
                c1[(A1[i] + A1[j]) % M]++;
            }
        }

        int sz = 0;
        uint64_t max_steps = 8000;
        for (uint64_t step = 1; step <= max_steps && !(*w->found_flag); step++) {
            int n_cands = 0;
            for (int x = 0; x < M; x++) {
                if (can_add_x(x, sz, z, M, S, A0, A1, used, cSS, c0, c1)) {
                    cands[n_cands++] = x;
                }
            }

            if (n_cands > 0) {
                if (sz + 1 == r) {
                    int chosen = cands[0];
                    do_add_x(chosen, &sz, z, M, S, A0, A1, used, cSS, c0, c1);
                    if (verify_exact_zero(M, r, z, S, A0, A1)) {
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

                /* Filter non-tabu candidates if possible */
                int chosen = cands[xorshift64(&rng) % n_cands];
                if (sz >= r - 5 && n_cands > 1) {
                    int best_x = -1;
                    int best_surv = -1;
                    int lim = (n_cands < 16) ? n_cands : 16;
                    int start_k = (int)(xorshift64(&rng) % n_cands);
                    for (int k = 0; k < lim; k++) {
                        int x = cands[(start_k + k) % n_cands];
                        if (tabu[x] > step && best_x != -1) continue;
                        do_add_x(x, &sz, z, M, S, A0, A1, used, cSS, c0, c1);
                        int surv = 0;
                        for (int idx = 0; idx < n_cands; idx++) {
                            int y = cands[idx];
                            if (y != x && can_add_x(y, sz, z, M, S, A0, A1, used, cSS, c0, c1)) {
                                surv++;
                            }
                        }
                        do_rem_idx(sz - 1, &sz, z, M, S, A0, A1, used, cSS, c0, c1);
                        if (surv > best_surv) {
                            best_surv = surv;
                            best_x = x;
                        }
                    }
                    if (best_x != -1) chosen = best_x;
                }
                do_add_x(chosen, &sz, z, M, S, A0, A1, used, cSS, c0, c1);
                continue;
            }

            /* Dead end: kick 1 or 2 elements from S */
            if (sz == 0) break;
            int kicks = (sz >= r - 1) ? 1 : (1 + (int)(xorshift64(&rng) & 1));
            for (int k = 0; k < kicks && sz > 0; k++) {
                int idx = (int)(xorshift64(&rng) % sz);
                int rem_val = S[idx];
                tabu[rem_val] = step + 7 + (xorshift64(&rng) & 7);
                do_rem_idx(idx, &sz, z, M, S, A0, A1, used, cSS, c0, c1);
            }
        }
    }
    return NULL;
}

static int try_solve_M(int z, int r, int M, int num_threads, uint64_t restarts_per_thread,
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
        args[t].max_restarts = restarts_per_thread;
        args[t].thread_id = t;
        args[t].found_flag = &found_flag;
        args[t].lock = &lock;
        args[t].out_S = out_S;
        args[t].out_A0 = out_A0;
        args[t].out_A1 = out_A1;
        pthread_create(&threads[t], NULL, ap_sidon_worker, &args[t]);
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
    fprintf(fp, "  \"method\": \"C-AP-Arcs-Incremental-Sidon-BiCay\",\n  \"S\": [");
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

    typedef struct { int z; int r; int ub_table1; int ub_live; int m_high; int m_low; uint64_t restarts; } target_t;
    target_t targets[] = {
        {3, 11, 484, 484, 241, 210, 60},
        {3, 13, 672, 672, 335, 300, 60},
        {4, 16, 1020, 1020, 509, 470, 50},
        {4, 17, 1152, 1152, 575, 530, 50},
        {2, 7,  196, 184,  91,  85, 80},
        {2, 8,  252, 234, 116, 110, 80},
        {2, 9,  320, 294, 146, 140, 80},
        {2, 11, 480, 450, 224, 215, 60},
        {1, 7,  192, 146,  72,  66, 100}
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
            if (try_solve_M(z, r, cur_M, threads, targets[t].restarts, S, A0, A1)) {
                best_M = cur_M;
                memcpy(best_S, S, r * sizeof(int));
                memcpy(best_A0, A0, z * sizeof(int));
                memcpy(best_A1, A1, z * sizeof(int));
                write_graph_json(out_dir, z, r, best_M, best_S, best_A0, best_A1);
                printf("  [HIT] [%d, %d; 6] N=%d (M=%d < UB_T1=%d, gain=%d)\n",
                       z, r, 2 * best_M, best_M, ub1, ub1 - 2 * best_M);
                fflush(stdout);
                cur_M--;
            } else {
                break;
            }
        }

        if (best_M != -1) {
            int N = 2 * best_M;
            printf("BEST [%d, %d; 6] (Table1_UB=%d, Live_UB=%d): N=%d (M=%d, gain_vs_T1=%d, gain_vs_Live=%d)\n",
                   z, r, ub1, ubl, N, best_M, ub1 - N, ubl - N);
            fflush(stdout);
        } else {
            printf("MISS [%d, %d; 6] at M=%d\n", z, r, targets[t].m_high);
            fflush(stdout);
        }
    }
    return 0;
}
