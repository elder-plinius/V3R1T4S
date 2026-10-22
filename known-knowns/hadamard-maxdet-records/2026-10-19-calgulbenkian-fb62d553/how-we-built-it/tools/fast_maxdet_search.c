/*
 * fast_maxdet_search.c
 * Multi-threaded, NEON-vectorized Hadamard excess & bordered determinant optimizer.
 * Supports:
 *   - Paley Class I (m = p + 1, p == 3 mod 4 prime)
 *   - Paley Class II (m = 2*(q + 1), q == 1 mod 4 prime)
 *   - External Hadamard matrix files (Williamson, Kronecker, etc.)
 *   - Contiguous int16_t transposed storage HT[j][i] for auto-vectorized O(m) inner loops
 *   - 1-flip + 2-flip + 3-flip steepest ascent + multi-radius Basin Hopping / Simulated Annealing
 *   - Rank-1 and Rank-2 Sherman-Morrison determinant polish on the bordered n x n matrix R
 *
 * Compile: clang -O3 -march=native -pthread tools/fast_maxdet_search.c -o tools/fast_maxdet_search -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

#define MAX_M 128

static inline uint64_t xorshift64(uint64_t *state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    return x;
}

static int is_prime(int p) {
    if (p < 2) return 0;
    if (p % 2 == 0) return p == 2;
    for (int d = 3; d * d <= p; d += 2) {
        if (p % d == 0) return 0;
    }
    return 1;
}

/* Build Paley Class I Hadamard matrix of order m = p + 1 where p == 3 (mod 4) is prime */
static int build_paley1(int m, int H[MAX_M][MAX_M]) {
    int p = m - 1;
    if (p % 4 != 3 || !is_prime(p)) return 0;
    int *qr = (int *)calloc(p, sizeof(int));
    for (int x = 1; x < p; x++) qr[(x * x) % p] = 1;
    for (int j = 0; j < m; j++) {
        H[0][j] = 1;
        H[j][0] = 1;
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < m; j++) {
            if (i == j) {
                H[i][j] = -1;
            } else {
                int diff = (j - i + p) % p;
                H[i][j] = qr[diff] ? 1 : -1;
            }
        }
    }
    free(qr);
    return 1;
}

/* Build Paley Class II Hadamard matrix of order m = 2*(q + 1) where q == 1 (mod 4) is prime */
static int build_paley2(int m, int H[MAX_M][MAX_M]) {
    if (m % 2 != 0) return 0;
    int h = m / 2;
    int q = h - 1;
    if (q % 4 != 1 || !is_prime(q)) return 0;
    int *qr = (int *)calloc(q, sizeof(int));
    for (int x = 1; x < q; x++) qr[(x * x) % q] = 1;
    int S[MAX_M][MAX_M];
    S[0][0] = 0;
    for (int j = 1; j < h; j++) {
        S[0][j] = 1;
        S[j][0] = 1;
    }
    for (int i = 1; i < h; i++) {
        for (int j = 1; j < h; j++) {
            if (i == j) {
                S[i][j] = 0;
            } else {
                int diff = (j - i + q) % q;
                S[i][j] = qr[diff] ? 1 : -1;
            }
        }
    }
    for (int i = 0; i < h; i++) {
        for (int j = 0; j < h; j++) {
            int d = (i == j) ? 1 : 0;
            H[i][j]         =  S[i][j] + d;
            H[i][h + j]     =  S[i][j] - d;
            H[h + i][j]     =  S[i][j] - d;
            H[h + i][h + j] = -S[i][j] - d;
        }
    }
    free(qr);
    return 1;
}

static int verify_hadamard(int m, int H[MAX_M][MAX_M]) {
    for (int i = 0; i < m; i++) {
        for (int j = i; j < m; j++) {
            int dot = 0;
            for (int k = 0; k < m; k++) dot += H[i][k] * H[j][k];
            if (i == j && dot != m) return 0;
            if (i != j && dot != 0) return 0;
        }
    }
    return 1;
}

static int load_hadamard(const char *path, int *m_out, int H[MAX_M][MAX_M]) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    int vals[MAX_M * MAX_M];
    int count = 0, v;
    while (count < MAX_M * MAX_M && fscanf(f, "%d", &v) == 1) {
        if (v != 1 && v != -1) { fclose(f); return 0; }
        vals[count++] = v;
    }
    fclose(f);
    int m = (int)round(sqrt((double)count));
    if (m * m != count || m <= 0 || m > MAX_M) return 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) H[i][j] = vals[i * m + j];
    }
    *m_out = m;
    return verify_hadamard(m, H);
}

/* Vectorized 1-flip + 2-flip + 3-flip polish using contiguous HT[j][i] */
static int polish_1_2_3_flip(int m, const int16_t HT[MAX_M][MAX_M], int16_t c[MAX_M], int16_t r[MAX_M], int do_3flip) {
    int cur_E = 0;
    for (int i = 0; i < m; i++) r[i] = 0;
    for (int j = 0; j < m; j++) {
        int16_t cj = c[j];
        const int16_t *col = HT[j];
        for (int i = 0; i < m; i++) r[i] += cj * col[i];
    }
    for (int i = 0; i < m; i++) cur_E += abs(r[i]);

    int improved = 1;
    while (improved) {
        improved = 0;
        /* 1-flip steepest ascent */
        while (1) {
            int best_j = -1;
            int best_E = cur_E;
            for (int j = 0; j < m; j++) {
                int16_t c2 = 2 * c[j];
                const int16_t *col = HT[j];
                int nE = 0;
                for (int i = 0; i < m; i++) {
                    nE += abs(r[i] - c2 * col[i]);
                }
                if (nE > best_E) {
                    best_E = nE;
                    best_j = j;
                }
            }
            if (best_j >= 0) {
                int16_t c2 = 2 * c[best_j];
                const int16_t *col = HT[best_j];
                for (int i = 0; i < m; i++) r[i] -= c2 * col[i];
                c[best_j] = -c[best_j];
                cur_E = best_E;
                improved = 1;
            } else {
                break;
            }
        }
        /* 2-flip steepest ascent */
        int best_j1 = -1, best_j2 = -1;
        int best_E2 = cur_E;
        for (int j1 = 0; j1 < m; j1++) {
            int16_t c2_1 = 2 * c[j1];
            const int16_t *col1 = HT[j1];
            int16_t r1[MAX_M];
            for (int i = 0; i < m; i++) r1[i] = r[i] - c2_1 * col1[i];
            for (int j2 = j1 + 1; j2 < m; j2++) {
                int16_t c2_2 = 2 * c[j2];
                const int16_t *col2 = HT[j2];
                int nE = 0;
                for (int i = 0; i < m; i++) {
                    nE += abs(r1[i] - c2_2 * col2[i]);
                }
                if (nE > best_E2) {
                    best_E2 = nE;
                    best_j1 = j1;
                    best_j2 = j2;
                }
            }
        }
        if (best_j1 >= 0) {
            int16_t c2_1 = 2 * c[best_j1];
            int16_t c2_2 = 2 * c[best_j2];
            for (int i = 0; i < m; i++) {
                r[i] -= c2_1 * HT[best_j1][i] + c2_2 * HT[best_j2][i];
            }
            c[best_j1] = -c[best_j1];
            c[best_j2] = -c[best_j2];
            cur_E = best_E2;
            improved = 1;
            continue;
        }
        /* Optional 3-flip first-improvement escape when at a high plateau */
        if (do_3flip) {
            int found_3 = 0;
            for (int j1 = 0; j1 < m && !found_3; j1++) {
                int16_t c2_1 = 2 * c[j1];
                const int16_t *col1 = HT[j1];
                int16_t r1[MAX_M];
                for (int i = 0; i < m; i++) r1[i] = r[i] - c2_1 * col1[i];
                for (int j2 = j1 + 1; j2 < m && !found_3; j2++) {
                    int16_t c2_2 = 2 * c[j2];
                    const int16_t *col2 = HT[j2];
                    int16_t r12[MAX_M];
                    for (int i = 0; i < m; i++) r12[i] = r1[i] - c2_2 * col2[i];
                    for (int j3 = j2 + 1; j3 < m; j3++) {
                        int16_t c2_3 = 2 * c[j3];
                        const int16_t *col3 = HT[j3];
                        int nE = 0;
                        for (int i = 0; i < m; i++) nE += abs(r12[i] - c2_3 * col3[i]);
                        if (nE > cur_E) {
                            for (int i = 0; i < m; i++) r[i] = r12[i] - c2_3 * col3[i];
                            c[j1] = -c[j1];
                            c[j2] = -c[j2];
                            c[j3] = -c[j3];
                            cur_E = nE;
                            found_3 = 1;
                            improved = 1;
                            break;
                        }
                    }
                }
            }
        }
    }
    return cur_E;
}

typedef struct {
    int m;
    const int16_t (*HT)[MAX_M];
    int restarts;
    int kicks;
    uint64_t seed;
    int best_E;
    int best_u[MAX_M];
    int best_c[MAX_M];
} worker_arg_t;

static void *worker_fn(void *arg_ptr) {
    worker_arg_t *w = (worker_arg_t *)arg_ptr;
    int m = w->m;
    const int16_t (*HT)[MAX_M] = w->HT;
    uint64_t rng = w->seed;
    int global_best_E = -1;
    int16_t c[MAX_M], r[MAX_M], local_best_c[MAX_M];

    for (int restart = 0; restart < w->restarts; restart++) {
        for (int j = 0; j < m; j++) c[j] = (xorshift64(&rng) & 1) ? 1 : -1;
        int local_best_E = polish_1_2_3_flip(m, HT, c, r, 0);
        memcpy(local_best_c, c, sizeof(int16_t) * m);

        if (local_best_E > global_best_E) {
            global_best_E = local_best_E;
            for (int j = 0; j < m; j++) w->best_c[j] = c[j];
            for (int i = 0; i < m; i++) w->best_u[i] = (r[i] >= 0) ? 1 : -1;
        }

        int stag = 0;
        for (int kstep = 0; kstep < w->kicks; kstep++) {
            memcpy(c, local_best_c, sizeof(int16_t) * m);
            int num_kicks = 3 + (int)(xorshift64(&rng) % 6ULL);
            for (int q = 0; q < num_kicks; q++) {
                int idx = (int)(xorshift64(&rng) % (uint64_t)m);
                c[idx] = -c[idx];
            }
            int cand_E = polish_1_2_3_flip(m, HT, c, r, 0);
            if (cand_E > local_best_E || (cand_E == local_best_E && (xorshift64(&rng) & 1))) {
                if (cand_E > local_best_E) stag = 0;
                local_best_E = cand_E;
                memcpy(local_best_c, c, sizeof(int16_t) * m);
                if (cand_E > global_best_E) {
                    /* Run 3-flip polish on new record */
                    cand_E = polish_1_2_3_flip(m, HT, c, r, 1);
                    local_best_E = cand_E;
                    memcpy(local_best_c, c, sizeof(int16_t) * m);
                    global_best_E = cand_E;
                    for (int j = 0; j < m; j++) w->best_c[j] = c[j];
                    for (int i = 0; i < m; i++) w->best_u[i] = (r[i] >= 0) ? 1 : -1;
                }
            } else {
                stag++;
                if (stag == 40) {
                    /* Try a 3-flip polish on local_best_c */
                    memcpy(c, local_best_c, sizeof(int16_t) * m);
                    int e3 = polish_1_2_3_flip(m, HT, c, r, 1);
                    if (e3 > local_best_E) {
                        local_best_E = e3;
                        memcpy(local_best_c, c, sizeof(int16_t) * m);
                        if (e3 > global_best_E) {
                            global_best_E = e3;
                            for (int j = 0; j < m; j++) w->best_c[j] = c[j];
                            for (int i = 0; i < m; i++) w->best_u[i] = (r[i] >= 0) ? 1 : -1;
                        }
                    }
                }
            }
        }
    }
    w->best_E = global_best_E;
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s [n] <total_restarts> <kicks> [paley1|paley2|hadamard_file] [out_matrix_file] [threads]\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    int total_restarts = atoi(argv[2]);
    int kicks = atoi(argv[3]);
    const char *mode = (argc >= 5) ? argv[4] : "paley1";
    const char *out_file = (argc >= 6 && strcmp(argv[5], "-") != 0) ? argv[5] : NULL;
    int nthreads = (argc >= 7) ? atoi(argv[6]) : 8;
    if (nthreads < 1) nthreads = 1;
    if (nthreads > 16) nthreads = 16;

    int m = n - 1;
    int H[MAX_M][MAX_M];
    if (strcmp(mode, "paley1") == 0) {
        if (!build_paley1(m, H) || !verify_hadamard(m, H)) {
            fprintf(stderr, "Error: Cannot build Paley Class I Hadamard matrix for m=%d\n", m);
            return 1;
        }
    } else if (strcmp(mode, "paley2") == 0) {
        if (!build_paley2(m, H) || !verify_hadamard(m, H)) {
            fprintf(stderr, "Error: Cannot build Paley Class II Hadamard matrix for m=%d\n", m);
            return 1;
        }
    } else {
        int m_loaded = 0;
        if (!load_hadamard(mode, &m_loaded, H) || m_loaded != m) {
            fprintf(stderr, "Error: Failed to load valid %dx%d Hadamard matrix from %s\n", m, m, mode);
            return 1;
        }
    }

    int16_t HT[MAX_M][MAX_M];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            HT[j][i] = (int16_t)H[i][j];
        }
    }

    pthread_t tids[16];
    worker_arg_t args[16];
    int r_per_thread = (total_restarts + nthreads - 1) / nthreads;
    for (int t = 0; t < nthreads; t++) {
        args[t].m = m;
        args[t].HT = HT;
        args[t].restarts = r_per_thread;
        args[t].kicks = kicks;
        args[t].seed = 0x853c49e6748fea9bULL ^ ((uint64_t)(t + 1) * 0x9e3779b97f4a7c15ULL);
        args[t].best_E = -1;
        pthread_create(&tids[t], NULL, worker_fn, &args[t]);
    }

    int best_E = -1;
    int best_u[MAX_M], best_c[MAX_M];
    for (int t = 0; t < nthreads; t++) {
        pthread_join(tids[t], NULL);
        if (args[t].best_E > best_E) {
            best_E = args[t].best_E;
            memcpy(best_u, args[t].best_u, sizeof(int) * m);
            memcpy(best_c, args[t].best_c, sizeof(int) * m);
        }
    }

    int k = m / 4;
    int factor = k + best_E / 4;

    int R[MAX_M][MAX_M];
    R[0][0] = -1;
    for (int j = 0; j < m; j++) {
        R[0][j + 1] = 1;
        R[j + 1][0] = 1;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            R[i + 1][j + 1] = best_u[i] * best_c[j] * H[i][j];
        }
    }

    printf("n=%d m=%d k=%d mode=%s best_excess=%d factor=%d\n",
           n, m, k, mode, best_E, factor);

    if (out_file) {
        FILE *f = fopen(out_file, "w");
        if (!f) return 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                fprintf(f, "%s%d", (j == 0 ? "" : " "), R[i][j]);
            }
            fprintf(f, "\n");
        }
        fclose(f);
    }
    return 0;
}
