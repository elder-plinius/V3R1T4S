#include <stdint.h>
#include <stddef.h>

/*
 * Standalone exact int64 Mod-135 geometric maximum (16-state subset DP
 * across mod-9 rows).
 *
 * Computes exact:
 *   max_{r3, r9, r27, r5, r15, r45, h} sum_{i=0}^{n-1} a_w[i] * max(0,
 *       shift + off[i] + c3*[x_i=r3(3)] + c9*[x_i=r9(9)] + c27*[x_i=r27(27)]
 *       + c5*[x_i=r5(5)] + c15*[x_i=r15(15)] + c45*[x_i=r45(45)] + c135*[i=h])
 * where each r_g ranges over residues occurring in xs[0..n-1].
 */

static inline int64_t pos64(int64_t v) { return v > 0 ? v : 0; }

typedef struct {
    int nr3, nr5, nr15, nr9;
    int r3_vals[3], r5_vals[5], r15_vals[15];
    int row_nc[9], row_n27[9], row_n45[9];
    int row_idx[9][15];
    int row_x3[9][15], row_x5[9][15], row_x15[9][15];
    int row_i27[9][15], row_i45[9][15];
} CoreStruct;

static void build_core(int n, const int *xs, CoreStruct *cs) {
    int seen3[3] = {0}, seen5[5] = {0}, seen15[15] = {0}, seen9[9] = {0};
    int r9_vals[9];
    cs->nr3 = cs->nr5 = cs->nr15 = cs->nr9 = 0;

    for (int i = 0; i < n; i++) {
        int x = xs[i];
        int v3 = x % 3, v5 = x % 5, v15 = x % 15, v9 = x % 9;
        if (!seen3[v3]) { seen3[v3] = 1; cs->r3_vals[cs->nr3++] = v3; }
        if (!seen5[v5]) { seen5[v5] = 1; cs->r5_vals[cs->nr5++] = v5; }
        if (!seen15[v15]) { seen15[v15] = 1; cs->r15_vals[cs->nr15++] = v15; }
        if (!seen9[v9]) { seen9[v9] = 1; r9_vals[cs->nr9++] = v9; }
    }

    for (int ri = 0; ri < cs->nr9; ri++) {
        int r9 = r9_vals[ri];
        int map27[27], map45[45];
        for (int k = 0; k < 27; k++) map27[k] = -1;
        for (int k = 0; k < 45; k++) map45[k] = -1;
        int nc = 0, n27 = 0, n45 = 0;
        for (int i = 0; i < n; i++) {
            int x = xs[i];
            if (x % 9 != r9) continue;
            int v27 = x % 27, v45 = x % 45;
            if (map27[v27] < 0) map27[v27] = n27++;
            if (map45[v45] < 0) map45[v45] = n45++;
            cs->row_idx[ri][nc] = i;
            cs->row_x3[ri][nc] = x % 3;
            cs->row_x5[ri][nc] = x % 5;
            cs->row_x15[ri][nc] = x % 15;
            cs->row_i27[ri][nc] = map27[v27];
            cs->row_i45[ri][nc] = map45[v45];
            nc++;
        }
        cs->row_nc[ri] = nc;
        cs->row_n27[ri] = n27;
        cs->row_n45[ri] = n45;
    }
}

static int64_t geom135_core(
    const CoreStruct *cs,
    const int64_t *a_w,
    const int64_t *off,
    int64_t shift,
    int64_t c3, int64_t c9, int64_t c27,
    int64_t c5, int64_t c15, int64_t c45, int64_t c135
) {
    int64_t best_total = 0;
    for (int i3 = 0; i3 < cs->nr3; i3++) {
        int r3 = cs->r3_vals[i3];
        for (int i5 = 0; i5 < cs->nr5; i5++) {
            int r5 = cs->r5_vals[i5];
            for (int i15 = 0; i15 < cs->nr15; i15++) {
                int r15 = cs->r15_vals[i15];
                int64_t dp[16];
                for (int ri = 0; ri < cs->nr9; ri++) {
                    int nc = cs->row_nc[ri];
                    int n27 = cs->row_n27[ri];
                    int n45 = cs->row_n45[ri];
                    int64_t ys[15], aws[15];
                    for (int ci = 0; ci < nc; ci++) {
                        int orig = cs->row_idx[ri][ci];
                        int64_t y = shift + off[orig];
                        if (cs->row_x3[ri][ci] == r3) y += c3;
                        if (cs->row_x5[ri][ci] == r5) y += c5;
                        if (cs->row_x15[ri][ci] == r15) y += c15;
                        ys[ci] = y;
                        aws[ci] = a_w[orig];
                    }

                    int64_t row_best[16];
                    for (int b9 = 0; b9 < 2; b9++) {
                        int64_t add9 = b9 ? c9 : 0;
                        int64_t base = 0;
                        int64_t d27[3] = {0, 0, 0};
                        int64_t d45[5] = {0, 0, 0, 0, 0};
                        int64_t p27_45[15];
                        int64_t g_s0[15], g_s27[15], g_s45[15], g_s2745[15];
                        int64_t max_gs0 = 0;

                        for (int ci = 0; ci < nc; ci++) {
                            int64_t a = aws[ci];
                            int64_t y = ys[ci] + add9;
                            int64_t v0 = pos64(y);
                            int64_t v27 = pos64(y + c27);
                            int64_t v45 = pos64(y + c45);
                            int64_t v2745 = pos64(y + c27 + c45);

                            int64_t vs0 = pos64(y + c135);
                            int64_t vs27 = pos64(y + c27 + c135);
                            int64_t vs45 = pos64(y + c45 + c135);
                            int64_t vs2745 = pos64(y + c27 + c45 + c135);

                            base += a * v0;
                            d27[cs->row_i27[ri][ci]] += a * (v27 - v0);
                            d45[cs->row_i45[ri][ci]] += a * (v45 - v0);
                            p27_45[ci] = a * (v2745 - v27 - v45 + v0);

                            g_s0[ci] = a * (vs0 - v0);
                            g_s27[ci] = a * (vs27 - v27);
                            g_s45[ci] = a * (vs45 - v45);
                            g_s2745[ci] = a * (vs2745 - v2745);
                            if (g_s0[ci] > max_gs0) max_gs0 = g_s0[ci];
                        }

                        row_best[b9] = base;
                        row_best[b9 | 8] = base + max_gs0;

                        int64_t b27 = 0, b27s = 0;
                        for (int k27 = 0; k27 < n27; k27++) {
                            int64_t cur = base + d27[k27];
                            if (cur > b27) b27 = cur;
                            int64_t bsg = 0;
                            for (int ci = 0; ci < nc; ci++) {
                                int64_t sg = (cs->row_i27[ri][ci] == k27) ? g_s27[ci] : g_s0[ci];
                                if (sg > bsg) bsg = sg;
                            }
                            if (cur + bsg > b27s) b27s = cur + bsg;
                        }
                        row_best[b9 | 2] = b27;
                        row_best[b9 | 10] = b27s;

                        int64_t b45 = 0, b45s = 0;
                        for (int k45 = 0; k45 < n45; k45++) {
                            int64_t cur = base + d45[k45];
                            if (cur > b45) b45 = cur;
                            int64_t bsg = 0;
                            for (int ci = 0; ci < nc; ci++) {
                                int64_t sg = (cs->row_i45[ri][ci] == k45) ? g_s45[ci] : g_s0[ci];
                                if (sg > bsg) bsg = sg;
                            }
                            if (cur + bsg > b45s) b45s = cur + bsg;
                        }
                        row_best[b9 | 4] = b45;
                        row_best[b9 | 12] = b45s;

                        int64_t b6 = 0, b14 = 0;
                        for (int k27 = 0; k27 < n27; k27++) {
                            for (int k45 = 0; k45 < n45; k45++) {
                                int64_t cur = base + d27[k27] + d45[k45];
                                int64_t bsg = 0;
                                for (int ci = 0; ci < nc; ci++) {
                                    int m27 = (cs->row_i27[ri][ci] == k27);
                                    int m45 = (cs->row_i45[ri][ci] == k45);
                                    int64_t sg;
                                    if (m27 && m45) {
                                        cur += p27_45[ci];
                                        sg = g_s2745[ci];
                                    } else if (m27) {
                                        sg = g_s27[ci];
                                    } else if (m45) {
                                        sg = g_s45[ci];
                                    } else {
                                        sg = g_s0[ci];
                                    }
                                    if (sg > bsg) bsg = sg;
                                }
                                if (cur > b6) b6 = cur;
                                if (cur + bsg > b14) b14 = cur + bsg;
                            }
                        }
                        row_best[b9 | 6] = b6;
                        row_best[b9 | 14] = b14;
                    }

                    if (ri == 0) {
                        for (int m = 0; m < 16; m++) dp[m] = row_best[m];
                    } else {
                        int64_t ndp[16];
                        for (int m = 0; m < 16; m++) {
                            int64_t bm = 0;
                            for (int s = m; ; s = (s - 1) & m) {
                                int64_t v = dp[s] + row_best[m ^ s];
                                if (v > bm) bm = v;
                                if (s == 0) break;
                            }
                            ndp[m] = bm;
                        }
                        for (int m = 0; m < 16; m++) dp[m] = ndp[m];
                    }
                }
                if (dp[15] > best_total) best_total = dp[15];
            }
        }
    }
    return best_total;
}

int64_t geom135_single(
    int n, const int *xs, const int64_t *a_w, const int64_t *off,
    int64_t shift,
    int64_t c3, int64_t c9, int64_t c27,
    int64_t c5, int64_t c15, int64_t c45, int64_t c135
) {
    CoreStruct cs;
    build_core(n, xs, &cs);
    return geom135_core(&cs, a_w, off, shift, c3, c9, c27, c5, c15, c45, c135);
}

/*
 * Batch evaluator for a list of n_q queries sharing (xs, a_w, off):
 * Each query k has 8 int64s: [shift, c3, c9, c27, c5, c15, c45, c135].
 */
void geom135_batch(
    int n, const int *xs, const int64_t *a_w, const int64_t *off,
    int n_q, const int64_t *queries, int64_t *out
) {
    CoreStruct cs;
    build_core(n, xs, &cs);
    for (int k = 0; k < n_q; k++) {
        const int64_t *q = queries + 8 * k;
        out[k] = geom135_core(&cs, a_w, off, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]);
    }
}

/*
 * Fast multi-offset batch evaluator: builds CoreStruct ONCE and evaluates
 * all n_off offset arrays across all n_q queries, storing out[oi * n_q + k].
 */
void geom135_multi_off_batch(
    int n, const int *xs, const int64_t *a_w,
    int n_off, const int64_t *offs,
    int n_q, const int64_t *queries,
    int64_t *out
) {
    CoreStruct cs;
    build_core(n, xs, &cs);
    for (int oi = 0; oi < n_off; oi++) {
        const int64_t *off = offs + (size_t)oi * (size_t)n;
        int64_t *row_out = out + (size_t)oi * (size_t)n_q;
        for (int k = 0; k < n_q; k++) {
            const int64_t *q = queries + 8 * k;
            row_out[k] = geom135_core(&cs, a_w, off, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]);
        }
    }
}
