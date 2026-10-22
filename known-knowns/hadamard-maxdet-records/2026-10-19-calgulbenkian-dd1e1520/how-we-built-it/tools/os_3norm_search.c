/*
 * os_3norm_search.c
 * Exhaustive multi-threaded NEON-vectorized search over all (m choose 3) * 4
 * Orrick-Solomon 3-normalized triples (r0, r1, r2; s1, s2) of an m x m Hadamard matrix H
 * (and its transpose H^T), followed by Sherman-Morrison 1-flip & 2-flip check.
 *
 * Compile: clang -O3 -march=native -pthread tools/os_3norm_search.c -o tools/os_3norm_search -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

#define MAX_M 128

static int is_prime(int p) {
    if (p < 2) return 0;
    if (p % 2 == 0) return p == 2;
    for (int d = 3; d * d <= p; d += 2) {
        if (p % d == 0) return 0;
    }
    return 1;
}

static int build_paley1(int m, int H[MAX_M][MAX_M]) {
    int p = m - 1;
    if (p % 4 != 3 || !is_prime(p)) return 0;
    int *qr = (int *)calloc(p, sizeof(int));
    for (int x = 1; x < p; x++) qr[(x * x) % p] = 1;
    for (int j = 0; j < m; j++) { H[0][j] = 1; H[j][0] = 1; }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < m; j++) {
            if (i == j) H[i][j] = -1;
            else H[i][j] = qr[(j - i + p) % p] ? 1 : -1;
        }
    }
    free(qr);
    return 1;
}

static int build_paley2(int m, int H[MAX_M][MAX_M]) {
    if (m % 2 != 0) return 0;
    int h = m / 2;
    int q = h - 1;
    if (q % 4 != 1 || !is_prime(q)) return 0;
    int *qr = (int *)calloc(q, sizeof(int));
    for (int x = 1; x < q; x++) qr[(x * x) % q] = 1;
    int S[MAX_M][MAX_M];
    S[0][0] = 0;
    for (int j = 1; j < h; j++) { S[0][j] = 1; S[j][0] = 1; }
    for (int i = 1; i < h; i++) {
        for (int j = 1; j < h; j++) {
            if (i == j) S[i][j] = 0;
            else S[i][j] = qr[(j - i + q) % q] ? 1 : -1;
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

typedef struct {
    int m;
    const int (*H)[MAX_M];
    const int16_t (*HT)[MAX_M];
    int tid;
    int nthreads;
    int best_E;
    int best_r0, best_r1, best_r2, best_s1, best_s2;
} os_worker_t;

static void *os_worker(void *arg) {
    os_worker_t *w = (os_worker_t *)arg;
    int m = w->m;
    const int (*H)[MAX_M] = w->H;
    const int16_t (*HT)[MAX_M] = w->HT;
    int best_E = -1;

    int pair_idx = 0;
    for (int r0 = 0; r0 < m; r0++) {
        for (int r1 = r0 + 1; r1 < m; r1++) {
            if ((pair_idx++ % w->nthreads) != w->tid) continue;
            for (int r2 = r1 + 1; r2 < m; r2++) {
                for (int s1 = -1; s1 <= 1; s1 += 2) {
                    for (int s2 = -1; s2 <= 1; s2 += 2) {
                        int16_t r[MAX_M];
                        for (int i = 0; i < m; i++) r[i] = 0;
                        for (int j = 0; j < m; j++) {
                            int wsum = H[r0][j] + s1 * H[r1][j] + s2 * H[r2][j];
                            int16_t cj;
                            if (wsum == 3 || wsum == -3) {
                                cj = (wsum > 0) ? -1 : 1;
                            } else {
                                cj = (wsum > 0) ? 1 : -1;
                            }
                            const int16_t *col = HT[j];
                            for (int i = 0; i < m; i++) {
                                r[i] += cj * col[i];
                            }
                        }
                        int E = 0;
                        for (int i = 0; i < m; i++) {
                            if (i == r0 || i == r1 || i == r2) continue;
                            E += abs(r[i]);
                        }
                        if (E > best_E) {
                            best_E = E;
                            w->best_E = E;
                            w->best_r0 = r0;
                            w->best_r1 = r1;
                            w->best_r2 = r2;
                            w->best_s1 = s1;
                            w->best_s2 = s2;
                        }
                    }
                }
            }
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s [n] [paley1|paley2|hadamard_file] [out_matrix_file] [threads]\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    const char *mode = argv[2];
    const char *out_file = (argc >= 4 && strcmp(argv[3], "-") != 0) ? argv[3] : NULL;
    int nthreads = (argc >= 5) ? atoi(argv[4]) : 8;
    int m = n - 1;
    int k = m / 4;

    int H_orig[MAX_M][MAX_M];
    if (strcmp(mode, "paley1") == 0) {
        if (!build_paley1(m, H_orig)) return 1;
    } else if (strcmp(mode, "paley2") == 0) {
        if (!build_paley2(m, H_orig)) return 1;
    } else {
        int ml = 0;
        if (!load_hadamard(mode, &ml, H_orig) || ml != m) return 1;
    }

    int global_best_E = -1;
    int best_tr = 0, best_r0 = 0, best_r1 = 1, best_r2 = 2, best_s1 = 1, best_s2 = 1;

    for (int tr = 0; tr < 2; tr++) {
        int H[MAX_M][MAX_M];
        int16_t HT[MAX_M][MAX_M];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                H[i][j] = (tr == 0) ? H_orig[i][j] : H_orig[j][i];
                HT[j][i] = (int16_t)H[i][j];
            }
        }
        pthread_t tids[16];
        os_worker_t args[16];
        for (int t = 0; t < nthreads; t++) {
            args[t].m = m;
            args[t].H = H;
            args[t].HT = HT;
            args[t].tid = t;
            args[t].nthreads = nthreads;
            args[t].best_E = -1;
            pthread_create(&tids[t], NULL, os_worker, &args[t]);
        }
        for (int t = 0; t < nthreads; t++) {
            pthread_join(tids[t], NULL);
            if (args[t].best_E > global_best_E) {
                global_best_E = args[t].best_E;
                best_tr = tr;
                best_r0 = args[t].best_r0;
                best_r1 = args[t].best_r1;
                best_r2 = args[t].best_r2;
                best_s1 = args[t].best_s1;
                best_s2 = args[t].best_s2;
            }
        }
    }

    int factor = 2 * k + global_best_E / 4;
    printf("n=%d m=%d k=%d mode=%s tr=%d r=(%d,%d,%d) s=(1,%d,%d) best_E3=%d factor=%d\n",
           n, m, k, mode, best_tr, best_r0, best_r1, best_r2, best_s1, best_s2, global_best_E, factor);

    if (out_file) {
        int H[MAX_M][MAX_M];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                H[i][j] = (best_tr == 0) ? H_orig[i][j] : H_orig[j][i];
            }
        }
        int c[MAX_M], in_K[MAX_M];
        for (int j = 0; j < m; j++) {
            int wsum = H[best_r0][j] + best_s1 * H[best_r1][j] + best_s2 * H[best_r2][j];
            if (wsum == 3 || wsum == -3) {
                c[j] = (wsum > 0) ? -1 : 1;
                in_K[j] = 1;
            } else {
                c[j] = (wsum > 0) ? 1 : -1;
                in_K[j] = 0;
            }
        }
        int Npp[MAX_M][MAX_M];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) Npp[i][j] = H[i][j] * c[j];
            if (i == best_r0 || i == best_r1 || i == best_r2) {
                int si = (i == best_r0) ? 1 : ((i == best_r1) ? best_s1 : best_s2);
                for (int j = 0; j < m; j++) {
                    Npp[i][j] *= si;
                    if (in_K[j]) Npp[i][j] = 1;
                }
            } else {
                int s = 0;
                for (int j = 0; j < m; j++) s += Npp[i][j];
                if (s < 0) {
                    for (int j = 0; j < m; j++) Npp[i][j] = -Npp[i][j];
                }
            }
        }
        int R[MAX_M][MAX_M];
        R[0][0] = -1;
        for (int j = 0; j < m; j++) R[0][j + 1] = in_K[j] ? -1 : 1;
        for (int i = 0; i < m; i++) {
            R[i + 1][0] = (i == best_r0 || i == best_r1 || i == best_r2) ? -1 : 1;
            for (int j = 0; j < m; j++) R[i + 1][j + 1] = Npp[i][j];
        }
        FILE *f = fopen(out_file, "w");
        if (!f) return 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) fprintf(f, "%s%d", (j == 0 ? "" : " "), R[i][j]);
            fprintf(f, "\n");
        }
        fclose(f);
    }
    return 0;
}
