/*
 * fast_cut_and_minor_verifier.c
 *
 * Standalone Zero-Trust Exhaustive C Verifier (8-thread POSIX pthreads) for:
 *   Mode 1 ("graph_cuts <n> <k> <field_id> <n*n entries...>"):
 *     Exhaustively checks rank == k of all C(n, k) bipartite k x (n-k) submatrices M_{S, S^c}
 *     over GF(q) for q in {2, 3, 5, 7, 8, 9, 11, 13, 16, 17, 19}.
 *   Mode 2 ("minors_10x10 <field_id> <100 entries...>"):
 *     Exhaustively checks non-vanishing of all sum_{r=1..10} C(10,r)^2 = 184,755 square minors
 *     of a 10x10 matrix U over GF(Q) for Q in {81, 121, 169, 256, 289}.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

#define MAXQ 512

static uint16_t ADD_TAB[MAXQ][MAXQ];
static uint16_t SUB_TAB[MAXQ][MAXQ];
static uint16_t MUL_TAB[MAXQ][MAXQ];
static uint16_t INV_TAB[MAXQ];
static int Q_SIZE = 0;

static void init_field(int fid) {
    Q_SIZE = fid;
    memset(ADD_TAB, 0, sizeof(ADD_TAB));
    memset(SUB_TAB, 0, sizeof(SUB_TAB));
    memset(MUL_TAB, 0, sizeof(MUL_TAB));
    memset(INV_TAB, 0, sizeof(INV_TAB));

    if (fid == 2 || fid == 3 || fid == 5 || fid == 7 || fid == 11 || fid == 13 || fid == 17 || fid == 19) {
        int p = fid;
        for (int a = 0; a < p; a++) {
            for (int b = 0; b < p; b++) {
                ADD_TAB[a][b] = (uint16_t)((a + b) % p);
                SUB_TAB[a][b] = (uint16_t)((a - b + p) % p);
                MUL_TAB[a][b] = (uint16_t)((a * b) % p);
            }
        }
    } else if (fid == 8) {
        /* GF(8) = GF(2)[w]/(w^3 + w + 1), modulus 0xB */
        for (int a = 0; a < 8; a++) {
            for (int b = 0; b < 8; b++) {
                ADD_TAB[a][b] = (uint16_t)(a ^ b);
                SUB_TAB[a][b] = (uint16_t)(a ^ b);
                int p = 0, x = a, y = b;
                for (int i = 0; i < 3; i++) {
                    if (y & 1) p ^= x;
                    x <<= 1;
                    if (x & 8) x ^= 0xB;
                    y >>= 1;
                }
                MUL_TAB[a][b] = (uint16_t)p;
            }
        }
    } else if (fid == 16) {
        /* GF(16) = GF(2)[x]/(x^4 + x + 1), modulus 0x13 */
        for (int a = 0; a < 16; a++) {
            for (int b = 0; b < 16; b++) {
                ADD_TAB[a][b] = (uint16_t)(a ^ b);
                SUB_TAB[a][b] = (uint16_t)(a ^ b);
                int p = 0, x = a, y = b;
                for (int i = 0; i < 4; i++) {
                    if (y & 1) p ^= x;
                    x <<= 1;
                    if (x & 16) x ^= 0x13;
                    y >>= 1;
                }
                MUL_TAB[a][b] = (uint16_t)p;
            }
        }
    } else if (fid == 9) {
        /* GF(9) = GF(3)[w]/(w^2 + 1), w^2 = 2 mod 3, encoding a0 + 3*a1 */
        for (int a = 0; a < 9; a++) {
            int a0 = a % 3, a1 = a / 3;
            for (int b = 0; b < 9; b++) {
                int b0 = b % 3, b1 = b / 3;
                ADD_TAB[a][b] = (uint16_t)(((a0 + b0) % 3) + 3 * ((a1 + b1) % 3));
                SUB_TAB[a][b] = (uint16_t)(((a0 - b0 + 3) % 3) + 3 * ((a1 - b1 + 3) % 3));
                int c0 = (a0 * b0 + 2 * a1 * b1) % 3;
                int c1 = (a0 * b1 + a1 * b0) % 3;
                MUL_TAB[a][b] = (uint16_t)(c0 + 3 * c1);
            }
        }
    } else if (fid == 81) {
        /* GF(81) = GF(3)[x]/(x^4 - x - 1), x^4 = x + 1 mod 3 */
        for (int a = 0; a < 81; a++) {
            int va[4] = {a % 3, (a / 3) % 3, (a / 9) % 3, (a / 27) % 3};
            for (int b = 0; b < 81; b++) {
                int vb[4] = {b % 3, (b / 3) % 3, (b / 9) % 3, (b / 27) % 3};
                ADD_TAB[a][b] = (uint16_t)(((va[0]+vb[0])%3) + 3*((va[1]+vb[1])%3) + 9*((va[2]+vb[2])%3) + 27*((va[3]+vb[3])%3));
                SUB_TAB[a][b] = (uint16_t)(((va[0]-vb[0]+3)%3) + 3*((va[1]-vb[1]+3)%3) + 9*((va[2]-vb[2]+3)%3) + 27*((va[3]-vb[3]+3)%3));
                int p[7] = {0};
                for (int i = 0; i < 4; i++)
                    for (int j = 0; j < 4; j++)
                        p[i + j] = (p[i + j] + va[i] * vb[j]) % 3;
                for (int d = 6; d >= 4; d--) {
                    int c = p[d];
                    p[d] = 0;
                    p[d - 3] = (p[d - 3] + c) % 3;
                    p[d - 4] = (p[d - 4] + c) % 3;
                }
                MUL_TAB[a][b] = (uint16_t)(p[0] + 3 * p[1] + 9 * p[2] + 27 * p[3]);
            }
        }
    } else if (fid == 121 || fid == 169 || fid == 289) {
        int p = (fid == 121) ? 11 : ((fid == 169) ? 13 : 17);
        int nr = (fid == 121) ? 7 : ((fid == 169) ? 2 : 3);
        for (int a = 0; a < fid; a++) {
            int a0 = a % p, a1 = a / p;
            for (int b = 0; b < fid; b++) {
                int b0 = b % p, b1 = b / p;
                ADD_TAB[a][b] = (uint16_t)(((a0 + b0) % p) + p * ((a1 + b1) % p));
                SUB_TAB[a][b] = (uint16_t)(((a0 - b0 + p) % p) + p * ((a1 - b1 + p) % p));
                int c0 = (a0 * b0 + nr * a1 * b1) % p;
                int c1 = (a0 * b1 + a1 * b0) % p;
                MUL_TAB[a][b] = (uint16_t)(c0 + p * c1);
            }
        }
    } else if (fid == 256) {
        /* GF(256) = GF(2)[x]/(x^8 + x^4 + x^3 + x^2 + 1), modulus 0x11D */
        for (int a = 0; a < 256; a++) {
            for (int b = 0; b < 256; b++) {
                ADD_TAB[a][b] = (uint16_t)(a ^ b);
                SUB_TAB[a][b] = (uint16_t)(a ^ b);
                int p = 0, x = a, y = b;
                for (int i = 0; i < 8; i++) {
                    if (y & 1) p ^= x;
                    x <<= 1;
                    if (x & 256) x ^= 0x11D;
                    y >>= 1;
                }
                MUL_TAB[a][b] = (uint16_t)p;
            }
        }
    } else {
        fprintf(stderr, "Unsupported field_id=%d\n", fid);
        exit(2);
    }

    for (int a = 1; a < fid; a++) {
        for (int b = 1; b < fid; b++) {
            if (MUL_TAB[a][b] == 1) {
                INV_TAB[a] = (uint16_t)b;
                break;
            }
        }
    }
}

/* Mode 1: Exhaustive Graph Cut Rank Check */
static int G_N = 0, G_K = 0;
static uint16_t G_MAT[20][20];
static uint32_t CUT_MASKS[200000];
static int N_CUTS = 0;
static int NEXT_CUT_CHUNK = 0;
static long long TOTAL_BAD_CUTS = 0;
static pthread_mutex_t MTX = PTHREAD_MUTEX_INITIALIZER;

static void *worker_graph_cuts(void *arg) {
    (void)arg;
    long long local_bad = 0;
    int R = G_K;
    int C = G_N - G_K;
    uint16_t sub[12][12];

    while (1) {
        int start = __sync_fetch_and_add(&NEXT_CUT_CHUNK, 512);
        if (start >= N_CUTS) break;
        int end = start + 512;
        if (end > N_CUTS) end = N_CUTS;

        for (int idx = start; idx < end; idx++) {
            uint32_t mask = CUT_MASKS[idx];
            int rows[12], cols[12], nr = 0, nc = 0;
            for (int v = 0; v < G_N; v++) {
                if ((mask >> v) & 1U) rows[nr++] = v;
                else                  cols[nc++] = v;
            }
            for (int i = 0; i < R; i++)
                for (int j = 0; j < C; j++)
                    sub[i][j] = G_MAT[rows[i]][cols[j]];

            int rk = 0;
            for (int col = 0; col < C && rk < R; col++) {
                int piv = -1;
                for (int r = rk; r < R; r++) {
                    if (sub[r][col] != 0) { piv = r; break; }
                }
                if (piv < 0) continue;
                if (piv != rk) {
                    for (int j = col; j < C; j++) {
                        uint16_t tmp = sub[rk][j];
                        sub[rk][j] = sub[piv][j];
                        sub[piv][j] = tmp;
                    }
                }
                uint16_t iv = INV_TAB[sub[rk][col]];
                for (int r = rk + 1; r < R; r++) {
                    uint16_t v = sub[r][col];
                    if (v != 0) {
                        uint16_t f = MUL_TAB[v][iv];
                        for (int j = col + 1; j < C; j++) {
                            sub[r][j] = SUB_TAB[sub[r][j]][MUL_TAB[f][sub[rk][j]]];
                        }
                    }
                }
                rk++;
            }
            if (rk < R) local_bad++;
        }
    }
    pthread_mutex_lock(&MTX);
    TOTAL_BAD_CUTS += local_bad;
    pthread_mutex_unlock(&MTX);
    return NULL;
}

/* Mode 2: Exhaustive 184,755 Minors Check of 10x10 Matrix U */
static uint16_t U_MAT[10][10];
static uint16_t SUB10_MASKS[1024];
static int SUB10_LEN[1024];
static uint8_t SUB10_IDX[1024][10];
static int NEXT_ROW_MASK = 1;
static long long TOTAL_BAD_MINORS = 0;

static uint16_t det_square(uint16_t M[10][10], int r) {
    uint16_t det = 1;
    for (int col = 0; col < r; col++) {
        int piv = -1;
        for (int rw = col; rw < r; rw++) {
            if (M[rw][col] != 0) { piv = rw; break; }
        }
        if (piv < 0) return 0;
        if (piv != col) {
            for (int c = col; c < r; c++) {
                uint16_t t = M[col][c];
                M[col][c] = M[piv][c];
                M[piv][c] = t;
            }
            det = SUB_TAB[0][det];
        }
        det = MUL_TAB[det][M[col][col]];
        uint16_t iv = INV_TAB[M[col][col]];
        for (int rw = col + 1; rw < r; rw++) {
            uint16_t v = M[rw][col];
            if (v != 0) {
                uint16_t f = MUL_TAB[v][iv];
                for (int c = col + 1; c < r; c++) {
                    M[rw][c] = SUB_TAB[M[rw][c]][MUL_TAB[f][M[col][c]]];
                }
            }
        }
    }
    return det;
}

static void *worker_minors_10x10(void *arg) {
    (void)arg;
    long long local_bad = 0;
    uint16_t M[10][10];

    while (1) {
        int rmask = __sync_fetch_and_add(&NEXT_ROW_MASK, 1);
        if (rmask >= 1024) break;
        int r = SUB10_LEN[rmask];
        const uint8_t *r_idx = SUB10_IDX[rmask];

        for (int cmask = 1; cmask < 1024; cmask++) {
            if (SUB10_LEN[cmask] != r) continue;
            const uint8_t *c_idx = SUB10_IDX[cmask];
            for (int i = 0; i < r; i++)
                for (int j = 0; j < r; j++)
                    M[i][j] = U_MAT[r_idx[i]][c_idx[j]];
            if (det_square(M, r) == 0) local_bad++;
        }
    }
    pthread_mutex_lock(&MTX);
    TOTAL_BAD_MINORS += local_bad;
    pthread_mutex_unlock(&MTX);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s [graph_cuts|minors_10x10] ...\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "graph_cuts") == 0) {
        if (argc < 5) return 1;
        G_N = atoi(argv[2]);
        G_K = atoi(argv[3]);
        int fid = atoi(argv[4]);
        if (argc < 5 + G_N * G_N) return 1;
        init_field(fid);
        int p = 5;
        for (int i = 0; i < G_N; i++)
            for (int j = 0; j < G_N; j++)
                G_MAT[i][j] = (uint16_t)atoi(argv[p++]);

        N_CUTS = 0;
        uint32_t lim = 1U << G_N;
        for (uint32_t m = 0; m < lim; m++) {
            if (__builtin_popcount(m) == G_K) {
                CUT_MASKS[N_CUTS++] = m;
            }
        }
        NEXT_CUT_CHUNK = 0;
        TOTAL_BAD_CUTS = 0;
        pthread_t th[8];
        for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker_graph_cuts, NULL);
        for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
        printf("TOTAL_CUTS=%d BAD_CUTS=%lld\n", N_CUTS, TOTAL_BAD_CUTS);
        return 0;
    } else if (strcmp(argv[1], "minors_10x10") == 0) {
        if (argc < 103) return 1;
        int fid = atoi(argv[2]);
        init_field(fid);
        int p = 3;
        for (int i = 0; i < 10; i++)
            for (int j = 0; j < 10; j++)
                U_MAT[i][j] = (uint16_t)atoi(argv[p++]);

        for (int m = 1; m < 1024; m++) {
            SUB10_MASKS[m] = (uint16_t)m;
            int c = 0;
            for (int b = 0; b < 10; b++) {
                if ((m >> b) & 1) SUB10_IDX[m][c++] = (uint8_t)b;
            }
            SUB10_LEN[m] = c;
        }
        NEXT_ROW_MASK = 1;
        TOTAL_BAD_MINORS = 0;
        pthread_t th[8];
        for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker_minors_10x10, NULL);
        for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);

        uint16_t M10[10][10];
        memcpy(M10, U_MAT, sizeof(U_MAT));
        uint16_t det10 = det_square(M10, 10);
        printf("TOTAL_MINORS=184755 BAD_MINORS=%lld DET10=%u\n", TOTAL_BAD_MINORS, (unsigned)det10);
        return 0;
    }
    return 1;
}
