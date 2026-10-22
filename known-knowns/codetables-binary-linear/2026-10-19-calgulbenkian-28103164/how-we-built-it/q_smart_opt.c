/*
 * q_smart_opt.c
 *
 * Fast Smart Puncturing, Full-Space Hitting-Set Column Extension, and Column
 * Replacement over GF(q) (q in {2, 3, 4, 5}).
 */

#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"

#define MAX_K 24
#define MAX_N 260

static int D_LO[10][260][40];
static int D_LO_ORIG[10][260][40];
static int D_UP[10][260][40];

static uint8_t GF_ADD[10][10];
static uint8_t GF_SUB[10][10];
static uint8_t GF_MUL[10][10];
static uint8_t GF_INV[10];

static void init_gf(int q) {
    memset(GF_ADD, 0, sizeof(GF_ADD));
    memset(GF_SUB, 0, sizeof(GF_SUB));
    memset(GF_MUL, 0, sizeof(GF_MUL));
    memset(GF_INV, 0, sizeof(GF_INV));
    if (q == 2 || q == 3 || q == 5) {
        for (int a = 0; a < q; a++) {
            for (int b = 0; b < q; b++) {
                GF_ADD[a][b] = (a + b) % q;
                GF_SUB[a][b] = (a - b + q) % q;
                GF_MUL[a][b] = (a * b) % q;
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    } else if (q == 4) {
        const uint8_t mul4[4][4] = {{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
        for (int a = 0; a < 4; a++) {
            for (int b = 0; b < 4; b++) {
                GF_ADD[a][b] = a ^ b;
                GF_SUB[a][b] = a ^ b;
                GF_MUL[a][b] = mul4[a][b];
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    }
}

static void load_bounds_tsv(const char *path) {
    memset(D_LO, 0, sizeof(D_LO));
    memset(D_LO_ORIG, 0, sizeof(D_LO_ORIG));
    memset(D_UP, 0, sizeof(D_UP));
    FILE *f = fopen(path, "r");
    if (!f) return;
    int q, n, k, dlo, dup;
    while (fscanf(f, "%d %d %d %d %d", &q, &n, &k, &dlo, &dup) == 5) {
        if (q >= 2 && q <= 9 && n >= 1 && n < 260 && k >= 1 && k < 40) {
            D_LO[q][n][k] = dlo;
            D_LO_ORIG[q][n][k] = dlo;
            D_UP[q][n][k] = dup;
        }
    }
    fclose(f);
}

static int is_excluded_cell(int q, int n, int k) {
    if (q == 2 && k >= 19 && k <= 22 && n >= 170 && n <= 240) return 1;
    if (q == 2 && k == 22 && (n == 95 || n == 96)) return 1;
    if (q == 2 && k == 25 && n == 175) return 1;
    if (q == 2 && k == 26 && n == 213) return 1;
    if (q == 2 && k == 17 && n >= 170 && n <= 174) return 1;
    if (q == 4 && k == 10 && n == 156) return 1;
    if (q == 4 && k == 11 && (n == 154 || n == 155 || n == 157 || n == 158 || n == 162 || n == 163)) return 1;
    return 0;
}

static uint64_t rng_state = 0x123456789abcdef1ULL;
static uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return (rng_state = x);
}

static int compute_rank(int q, int k, int n, const uint8_t G[MAX_K][MAX_N]) {
    init_gf(q);
    uint8_t M[MAX_K][MAX_N];
    memcpy(M, G, sizeof(M));
    int r = 0;
    for (int col = 0; col < n && r < k; col++) {
        int piv = -1;
        for (int i = r; i < k; i++) if (M[i][col]) { piv = i; break; }
        if (piv < 0) continue;
        for (int j = 0; j < n; j++) { uint8_t t = M[r][j]; M[r][j] = M[piv][j]; M[piv][j] = t; }
        uint8_t iv = GF_INV[M[r][col]];
        for (int j = 0; j < n; j++) M[r][j] = GF_MUL[iv][M[r][j]];
        for (int i = 0; i < k; i++) {
            if (i != r && M[i][col]) {
                uint8_t fac = M[i][col];
                for (int j = 0; j < n; j++) M[i][j] = GF_SUB[M[i][j]][GF_MUL[fac][M[r][j]]];
            }
        }
        r++;
    }
    return r;
}

static void eval_exact(int q, int k, int n, const uint8_t G[MAX_K][MAX_N], int *d_out, uint64_t *Ad_out) {
    init_gf(q);
    int min_d = n + 1;
    uint64_t count_d = 0;
    uint8_t cw[MAX_N];
    int coeff[MAX_K];

    for (int lead = 0; lead < k; lead++) {
        int rem = k - 1 - lead;
        for (int j = 0; j < n; j++) cw[j] = G[lead][j];
        for (int i = 0; i < rem; i++) coeff[i] = 0;

        while (1) {
            int w = 0;
            for (int j = 0; j < n; j++) w += (cw[j] != 0);
            if (w < min_d) { min_d = w; count_d = (q - 1); }
            else if (w == min_d) { count_d += (q - 1); }

            int pos = 0;
            while (pos < rem) {
                int row = lead + 1 + pos;
                int old_c = coeff[pos];
                int new_c = (old_c + 1) % q;
                for (int j = 0; j < n; j++) {
                    uint8_t old_v = GF_MUL[old_c][G[row][j]];
                    uint8_t new_v = GF_MUL[new_c][G[row][j]];
                    uint8_t tmp = GF_SUB[cw[j]][old_v];
                    cw[j] = GF_ADD[tmp][new_v];
                }
                coeff[pos] = new_c;
                if (new_c != 0) break;
                pos++;
            }
            if (pos == rem) break;
        }
    }
    *d_out = min_d;
    *Ad_out = count_d;
}

static int save_win(int q, int n, int k, const uint8_t G[MAX_K][MAX_N], const char *desc) {
    if (is_excluded_cell(q, n, k)) return 0;
    if (compute_rank(q, k, n, G) < k) return 0;
    int d = 0;
    uint64_t A_d = 0;
    eval_exact(q, k, n, G, &d, &A_d);
    int d_lo = D_LO[q][n][k];
    int d_lo_orig = D_LO_ORIG[q][n][k];
    int d_up = D_UP[q][n][k];
    if (d_lo <= 0 || d <= d_lo) return 0;

    D_LO[q][n][k] = d;
    printf("\n*** SMART-OPT NEW BREAKTHROUGH WIN: [%d, %d, %d]_%d (beats codetables.de d_lo=%d, d_up=%d, A_d=%llu) [%s] ***\n",
           n, k, d, q, d_lo_orig, d_up, (unsigned long long)A_d, desc);
    fflush(stdout);

    char fname[256];
    snprintf(fname, sizeof(fname), "results/new_win_q%d_n%d_k%d_d%d.json", q, n, k, d);
    FILE *fp = fopen(fname, "w");
    if (fp) {
        fprintf(fp, "{\n  \"type\": \"classical\",\n  \"q\": %d,\n  \"n\": %d,\n  \"k\": %d,\n  \"d\": %d,\n", q, n, k, d);
        fprintf(fp, "  \"d_lo_codetables\": %d,\n  \"d_up_codetables\": %d,\n  \"A_d\": %llu,\n", d_lo_orig, d_up, (unsigned long long)A_d);
        fprintf(fp, "  \"construction\": \"%s\",\n  \"G\": [\n", desc);
        for (int r = 0; r < k; r++) {
            fprintf(fp, "    [");
            for (int c = 0; c < n; c++) fprintf(fp, "%d%s", G[r][c], (c + 1 < n) ? "," : "");
            fprintf(fp, "]%s\n", (r + 1 < k) ? "," : "");
        }
        fprintf(fp, "  ]\n}\n");
        fclose(fp);
    }
    return 1;
}

typedef struct {
    uint8_t u[MAX_K];
    uint8_t nz[MAX_N]; /* 1 if cw[c] != 0 */
    int wt;
} CritWord;

static void optimize_code(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp) return;
    fseek(fp, 0, SEEK_END);
    long sz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *buf = (char *)malloc(sz + 1);
    fread(buf, 1, sz, fp);
    buf[sz] = '\0';
    fclose(fp);

    char *pq = strstr(buf, "\"q\":");
    int q = pq ? atoi(pq + 4) : 2;
    char *g = strstr(buf, "\"G\"");
    if (!g) { free(buf); return; }
    g = strchr(g, '[');
    uint8_t G[MAX_K][MAX_N];
    memset(G, 0, sizeof(G));
    int depth = 0, row = 0, col = 0, N = 0;
    for (char *c = g; *c; c++) {
        if (*c == '[') { depth++; if (depth == 2) col = 0; }
        else if (*c == ']') { if (depth == 2) { N = col; row++; } depth--; if (depth == 0) break; }
        else if (depth == 2 && (*c >= '0' && *c <= '9')) G[row][col++] = (uint8_t)(*c - '0');
    }
    int k = row;
    free(buf);

    init_gf(q);
    int D = 0;
    uint64_t A_D = 0;
    eval_exact(q, k, N, G, &D, &A_D);
    printf("[SmartOpt] Loaded %s -> [%d, %d, %d]_%d (A_%d = %llu)\n", path, N, k, D, q, D, (unsigned long long)A_D);

    /* Collect projective codewords with weight <= D + 3 */
    int max_cap = 80000;
    CritWord *shell = (CritWord *)malloc(max_cap * sizeof(CritWord));
    int n_shell = 0;
    int wt_cap = D + 3;

    uint8_t cw[MAX_N];
    int coeff[MAX_K];
    for (int lead = 0; lead < k; lead++) {
        int rem = k - 1 - lead;
        for (int j = 0; j < N; j++) cw[j] = G[lead][j];
        for (int i = 0; i < rem; i++) coeff[i] = 0;

        while (1) {
            int w = 0;
            for (int j = 0; j < N; j++) w += (cw[j] != 0);
            if (w <= wt_cap && n_shell < max_cap) {
                memset(shell[n_shell].u, 0, MAX_K);
                shell[n_shell].u[lead] = 1;
                for (int i = 0; i < rem; i++) shell[n_shell].u[lead + 1 + i] = (uint8_t)coeff[i];
                for (int j = 0; j < N; j++) shell[n_shell].nz[j] = (cw[j] != 0) ? 1 : 0;
                shell[n_shell].wt = w;
                n_shell++;
            }
            int pos = 0;
            while (pos < rem) {
                int r_idx = lead + 1 + pos;
                int old_c = coeff[pos];
                int new_c = (old_c + 1) % q;
                for (int j = 0; j < N; j++) {
                    uint8_t old_v = GF_MUL[old_c][G[r_idx][j]];
                    uint8_t new_v = GF_MUL[new_c][G[r_idx][j]];
                    uint8_t tmp = GF_SUB[cw[j]][old_v];
                    cw[j] = GF_ADD[tmp][new_v];
                }
                coeff[pos] = new_c;
                if (new_c != 0) break;
                pos++;
            }
            if (pos == rem) break;
        }
    }
    printf("  Shell (wt <= %d): %d projective codewords\n", wt_cap, n_shell);

    /* 1. Smart Puncturing p = 1..5 */
    for (int p = 1; p <= 5; p++) {
        int n_target = N - p;
        if (n_target < 20 || is_excluded_cell(q, n_target, k)) continue;
        int d_lo = D_LO[q][n_target][k];
        if (d_lo <= 0) continue;
        int d_target = d_lo + 1;
        if (D < d_target) continue;

        int del_cols[16];
        uint8_t is_del[MAX_N];
        int *loss = (int *)malloc(n_shell * sizeof(int));
        int *crit_idx = (int *)malloc(n_shell * sizeof(int));

        for (int restart = 0; restart < 40; restart++) {
            memset(is_del, 0, sizeof(is_del));
            memset(loss, 0, n_shell * sizeof(int));
            for (int s_i = 0; s_i < p; s_i++) {
                int c = xorshift64() % N;
                while (is_del[c]) c = (c + 1) % N;
                del_cols[s_i] = c;
                is_del[c] = 1;
                for (int s = 0; s < n_shell; s++) loss[s] += shell[s].nz[c];
            }
            for (int iter = 0; iter < 250; iter++) {
                int min_rem = 9999, n_crit = 0, first_viol = -1;
                for (int s = 0; s < n_shell; s++) {
                    int rw = shell[s].wt - loss[s];
                    if (rw < min_rem) min_rem = rw;
                    if (rw < d_target && (first_viol < 0 || (xorshift64() & 7) == 0)) first_viol = s;
                    if (rw <= d_target + 1) crit_idx[n_crit++] = s;
                }
                if (min_rem >= d_target) break;
                int pick = iter % p;
                if (first_viol >= 0) {
                    for (int j = 0; j < p; j++) {
                        int jj = (iter + j) % p;
                        if (shell[first_viol].nz[del_cols[jj]]) { pick = jj; break; }
                    }
                }
                int old_c = del_cols[pick];
                is_del[old_c] = 0;
                for (int s = 0; s < n_shell; s++) loss[s] -= shell[s].nz[old_c];

                int best_c = old_c;
                int64_t best_pen = 0x7fffffffffffffffLL;
                for (int c = 0; c < N; c++) {
                    if (is_del[c] || c == old_c) continue;
                    int64_t pen = 0;
                    for (int ci = 0; ci < n_crit; ci++) {
                        int s = crit_idx[ci];
                        int rw = shell[s].wt - (loss[s] + shell[s].nz[c]);
                        if (rw < d_target) {
                            int v = d_target - rw;
                            pen += (int64_t)v * v * 10000LL;
                        } else if (rw == d_target) pen += 5;
                    }
                    pen = pen * 8 + (xorshift64() & 7);
                    if (pen < best_pen) { best_pen = pen; best_c = c; }
                }
                del_cols[pick] = best_c;
                is_del[best_c] = 1;
                for (int s = 0; s < n_shell; s++) loss[s] += shell[s].nz[best_c];
            }
            int min_rem = 9999;
            for (int s = 0; s < n_shell; s++) {
                int rw = shell[s].wt - loss[s];
                if (rw < min_rem) min_rem = rw;
            }
            if (min_rem >= d_target) {
                uint8_t G_p[MAX_K][MAX_N];
                memset(G_p, 0, sizeof(G_p));
                int dc = 0;
                for (int c = 0; c < N; c++) {
                    if (!is_del[c]) {
                        for (int r = 0; r < k; r++) G_p[r][dc] = G[r][c];
                        dc++;
                    }
                }
                char desc[160];
                snprintf(desc, sizeof(desc), "Smart-punctured %d cols from [%d,%d,%d]_%d", p, N, k, D, q);
                if (save_win(q, n_target, k, G_p, desc)) break;
            }
        }
        free(loss);
        free(crit_idx);
    }

    /* 2. Full-Space Hitting-Set Column Extension t = 1..2 */
    int *cur_w = (int *)malloc(n_shell * sizeof(int));
    for (int t = 1; t <= 2; t++) {
        int n_new = N + t;
        if (n_new >= 256 || is_excluded_cell(q, n_new, k)) continue;
        int d_lo = D_LO[q][n_new][k];
        if (d_lo <= 0) continue;
        int d_target = d_lo + 1;
        if (D + t < d_target) continue;

        uint8_t ext_cols[10][MAX_K];
        for (int restart = 0; restart < 25; restart++) {
            for (int s = 0; s < n_shell; s++) cur_w[s] = shell[s].wt;
            for (int step = 0; step < t; step++) {
                uint8_t best_v[MAX_K];
                int64_t best_sc = -1;
                for (int samp = 0; samp < 2500; samp++) {
                    uint8_t v[MAX_K];
                    int nz = 0;
                    for (int r = 0; r < k; r++) { v[r] = xorshift64() % q; if (v[r]) nz = 1; }
                    if (!nz) v[0] = 1;
                    int64_t sc = 0;
                    for (int s = 0; s < n_shell; s++) {
                        int def = d_target - cur_w[s];
                        if (def > 0) {
                            uint8_t dot = 0;
                            for (int r = 0; r < k; r++) {
                                if (shell[s].u[r] && v[r]) dot = GF_ADD[dot][GF_MUL[shell[s].u[r]][v[r]]];
                            }
                            if (dot != 0) sc += (int64_t)def * def * 32 + 1;
                        }
                    }
                    if (sc > best_sc) { best_sc = sc; memcpy(best_v, v, MAX_K); }
                }
                /* Local coordinate polish on best_v */
                for (int r = 0; r < k; r++) {
                    uint8_t orig_vr = best_v[r];
                    for (int val = 0; val < q; val++) {
                        if (val == orig_vr) continue;
                        best_v[r] = val;
                        int64_t sc = 0;
                        for (int s = 0; s < n_shell; s++) {
                            int def = d_target - cur_w[s];
                            if (def > 0) {
                                uint8_t dot = 0;
                                for (int rr = 0; rr < k; rr++) {
                                    if (shell[s].u[rr] && best_v[rr]) dot = GF_ADD[dot][GF_MUL[shell[s].u[rr]][best_v[rr]]];
                                }
                                if (dot != 0) sc += (int64_t)def * def * 32 + 1;
                            }
                        }
                        if (sc > best_sc) { best_sc = sc; orig_vr = val; }
                        else { best_v[r] = orig_vr; }
                    }
                }
                memcpy(ext_cols[step], best_v, MAX_K);
                for (int s = 0; s < n_shell; s++) {
                    uint8_t dot = 0;
                    for (int r = 0; r < k; r++) {
                        if (shell[s].u[r] && best_v[r]) dot = GF_ADD[dot][GF_MUL[shell[s].u[r]][best_v[r]]];
                    }
                    if (dot != 0) cur_w[s]++;
                }
            }
            int min_cw = 9999;
            for (int s = 0; s < n_shell; s++) if (cur_w[s] < min_cw) min_cw = cur_w[s];
            if (min_cw >= d_target) {
                uint8_t G_ext[MAX_K][MAX_N];
                memcpy(G_ext, G, sizeof(G));
                for (int step = 0; step < t; step++) {
                    for (int r = 0; r < k; r++) G_ext[r][N + step] = ext_cols[step][r];
                }
                char desc[160];
                snprintf(desc, sizeof(desc), "Full-space hitting-set extension (+%d cols) from [%d,%d,%d]_%d", t, N, k, D, q);
                if (save_win(q, n_new, k, G_ext, desc)) break;
            }
        }
    }
    free(cur_w);
    free(shell);
}

int main(int argc, char **argv) {
    load_bounds_tsv("data/bounds.tsv");
    for (int i = 1; i < argc; i++) {
        optimize_code(argv[i]);
    }
    return 0;
}
