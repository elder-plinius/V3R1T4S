#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define NOPTS 6561
#define NWORDS 103
#define NITEMS 351
#define IWORDS 6

static int pts[1066][8];
static int vec_to_pt[6561];
static int planes[22960][13];
static uint8_t adj[1066][1066];

static int vec_code(const int v[8]) {
    int c = 0;
    for (int i = 0; i < 8; i++) c = c * 3 + v[i];
    return c;
}
static int q8(const int v[8]) {
    return (v[0]*v[1] + v[2]*v[3] + v[4]*v[5] + v[6]*v[6] + v[7]*v[7]) % 3;
}
static int b8(const int u[8], const int v[8]) {
    return (u[0]*v[1] + u[1]*v[0] + u[2]*v[3] + u[3]*v[2] +
            u[4]*v[5] + u[5]*v[4] + 2*u[6]*v[6] + 2*u[7]*v[7]) % 3;
}
static int cmp_plane(const void *a, const void *b) {
    return memcmp(a, b, 13 * sizeof(int));
}
static int find_plane(const int p[13]) {
    int lo = 0, hi = 22959;
    while (lo <= hi) {
        int mid = (lo + hi) >> 1;
        int c = memcmp(planes[mid], p, 13 * sizeof(int));
        if (c == 0) return mid;
        if (c < 0) lo = mid + 1; else hi = mid - 1;
    }
    exit(1);
}

static void build_q7_3(void) {
    memset(vec_to_pt, -1, sizeof(vec_to_pt));
    int npts = 0;
    for (int code = 1; code < 6561; code++) {
        int v[8], tmp = code, first_nz = 0;
        for (int i = 7; i >= 0; i--) { v[i] = tmp % 3; tmp /= 3; }
        for (int i = 0; i < 8; i++) { if (v[i] != 0) { first_nz = v[i]; break; } }
        if (first_nz != 1) continue;
        if (q8(v) == 0) {
            memcpy(pts[npts], v, sizeof(v));
            vec_to_pt[code] = npts;
            int v2[8];
            for (int i = 0; i < 8; i++) v2[i] = (2 * v[i]) % 3;
            vec_to_pt[vec_code(v2)] = npts;
            npts++;
        }
    }
    memset(adj, 0, sizeof(adj));
    for (int i = 0; i < 1066; i++)
        for (int j = i + 1; j < 1066; j++)
            if (b8(pts[i], pts[j]) == 0)
                adj[i][j] = adj[j][i] = 1;
    int nplanes = 0;
    for (int p0 = 0; p0 < 1066; p0++) {
        for (int p1 = p0 + 1; p1 < 1066; p1++) {
            if (!adj[p0][p1]) continue;
            int lpts[4], nl = 0;
            for (int a = 0; a < 3; a++)
                for (int b = 0; b < 3; b++) {
                    if (a == 0 && b == 0) continue;
                    int w[8];
                    for (int k = 0; k < 8; k++) w[k] = (a*pts[p0][k] + b*pts[p1][k]) % 3;
                    int id = vec_to_pt[vec_code(w)], dup = 0;
                    for (int t = 0; t < nl; t++) if (lpts[t] == id) dup = 1;
                    if (!dup) lpts[nl++] = id;
                }
            for (int a = 0; a < 4; a++)
                for (int b = a + 1; b < 4; b++)
                    if (lpts[a] > lpts[b]) { int t = lpts[a]; lpts[a] = lpts[b]; lpts[b] = t; }
            if (lpts[0] != p0 || lpts[1] != p1) continue;
            for (int p2 = p1 + 1; p2 < 1066; p2++) {
                if (!adj[p0][p2] || !adj[p1][p2]) continue;
                if (p2 == lpts[2] || p2 == lpts[3]) continue;
                int ppts[13], np = 0;
                for (int a = 0; a < 3; a++)
                    for (int b = 0; b < 3; b++)
                        for (int c = 0; c < 3; c++) {
                            if (a == 0 && b == 0 && c == 0) continue;
                            int w[8];
                            for (int k = 0; k < 8; k++)
                                w[k] = (a*pts[p0][k] + b*pts[p1][k] + c*pts[p2][k]) % 3;
                            int id = vec_to_pt[vec_code(w)], dup = 0;
                            for (int t = 0; t < np; t++) if (ppts[t] == id) dup = 1;
                            if (!dup) ppts[np++] = id;
                        }
                for (int a = 0; a < 13; a++)
                    for (int b = a + 1; b < 13; b++)
                        if (ppts[a] > ppts[b]) { int t = ppts[a]; ppts[a] = ppts[b]; ppts[b] = t; }
                int smallest_out = -1;
                for (int a = 0; a < 13; a++) {
                    int x = ppts[a];
                    if (x != lpts[0] && x != lpts[1] && x != lpts[2] && x != lpts[3]) {
                        smallest_out = x; break;
                    }
                }
                if (ppts[0] == p0 && ppts[1] == p1 && smallest_out == p2)
                    memcpy(planes[nplanes++], ppts, sizeof(ppts));
            }
        }
    }
    qsort(planes, 22960, sizeof(planes[0]), cmp_plane);
}

static int A_mat[8][8] = {
    {1, 2, 0, 0, 0, 0, 1, 0},
    {0, 1, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 2, 0, 0},
    {0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 1, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 1, 0, 0},
    {0, 1, 0, 0, 0, 0, 1, 0},
    {0, 0, 0, 0, 0, 0, 0, 1}
};

static void mat_mul8(const int X[8][8], const int Y[8][8], int Z[8][8]) {
    int T[8][8];
    for (int i = 0; i < 8; i++)
        for (int j = 0; j < 8; j++) {
            int s = 0;
            for (int k = 0; k < 8; k++) s += X[i][k] * Y[k][j];
            T[i][j] = s % 3;
        }
    memcpy(Z, T, sizeof(T));
}
static void mat_vec8(const int M[8][8], const int v[8], int out[8]) {
    for (int i = 0; i < 8; i++) {
        int s = 0;
        for (int j = 0; j < 8; j++) s += M[i][j] * v[j];
        out[i] = s % 3;
    }
}

#define MAX_NORM 1900000
static uint8_t (*norm_mats)[8][8];
static int n_norm = 0;

static void enumerate_normalizer(void) {
    norm_mats = malloc(MAX_NORM * sizeof(*norm_mats));
    int A2[8][8]; mat_mul8(A_mat, A_mat, A2);
    int N0[8][8], N0_2[8][8];
    for (int i = 0; i < 8; i++)
        for (int j = 0; j < 8; j++)
            N0[i][j] = (A_mat[i][j] - (i==j ? 1 : 0) + 3) % 3;
    mat_mul8(N0, N0, N0_2);
    int u[8][8] = {0};
    u[0][1] = 1; mat_vec8(N0, u[0], u[1]); mat_vec8(N0_2, u[0], u[2]);
    u[3][3] = 1; mat_vec8(N0, u[3], u[4]);
    u[5][5] = 1; mat_vec8(N0, u[5], u[6]);
    u[7][7] = 1;

    int aug[8][16] = {0};
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) aug[r][c] = u[c][r];
        aug[r][8 + r] = 1;
    }
    for (int c = 0; c < 8; c++) {
        int piv = -1;
        for (int r = c; r < 8; r++) if (aug[r][c] != 0) { piv = r; break; }
        if (piv != c) for (int j = 0; j < 16; j++) { int t = aug[c][j]; aug[c][j] = aug[piv][j]; aug[piv][j] = t; }
        int inv = (aug[c][c] == 1) ? 1 : 2;
        for (int j = 0; j < 16; j++) aug[c][j] = (aug[c][j] * inv) % 3;
        for (int r = 0; r < 8; r++) if (r != c && aug[r][c] != 0) {
            int f = aug[r][c];
            for (int j = 0; j < 16; j++) aug[r][j] = (aug[r][j] - f * aug[c][j] + 9) % 3;
        }
    }
    int Uinv[8][8];
    for (int r = 0; r < 8; r++) for (int c = 0; c < 8; c++) Uinv[r][c] = aug[r][8 + c];
    int bu[8][8], qu[8];
    for (int a = 0; a < 8; a++) {
        qu[a] = q8(u[a]);
        for (int b = 0; b < 8; b++) bu[a][b] = b8(u[a], u[b]);
    }
    int all_v[6561][8];
    for (int code = 0; code < 6561; code++) {
        int tmp = code;
        for (int i = 7; i >= 0; i--) { all_v[code][i] = tmp % 3; tmp /= 3; }
    }
    for (int eps = 1; eps <= 2; eps++) {
        int (*Ae)[8] = (eps == 1) ? A_mat : A2;
        int Ne[8][8], Ne2[8][8];
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                Ne[i][j] = (Ae[i][j] - (i==j ? 1 : 0) + 3) % 3;
        mat_mul8(Ne, Ne, Ne2);
        int ker2[2187][8], nker2 = 0, ker1[81][8], nker1 = 0;
        for (int code = 0; code < 6561; code++) {
            int w1[8], w2[8];
            mat_vec8(Ne, all_v[code], w1); mat_vec8(Ne2, all_v[code], w2);
            int z1 = 1, z2 = 1;
            for (int i = 0; i < 8; i++) { if (w1[i]) z1 = 0; if (w2[i]) z2 = 0; }
            if (z2) memcpy(ker2[nker2++], all_v[code], sizeof(int)*8);
            if (z1) memcpy(ker1[nker1++], all_v[code], sizeof(int)*8);
        }
        for (int lam = 1; lam <= 2; lam++) {
            for (int c0 = 1; c0 < 6561; c0++) {
                int y[8][8];
                memcpy(y[0], all_v[c0], sizeof(int)*8);
                if (q8(y[0]) != (lam * qu[0]) % 3) continue;
                mat_vec8(Ne, y[0], y[1]); mat_vec8(Ne2, y[0], y[2]);
                int fnz = 0;
                for (int i = 0; i < 8; i++) if (y[2][i] != 0) { fnz = y[2][i]; break; }
                if (fnz != 1) continue;
                int ok0 = 1;
                for (int a = 0; a <= 2 && ok0; a++) {
                    if (q8(y[a]) != (lam * qu[a]) % 3) ok0 = 0;
                    for (int b = a + 1; b <= 2 && ok0; b++)
                        if (b8(y[a], y[b]) != (lam * bu[a][b]) % 3) ok0 = 0;
                }
                if (!ok0) continue;
                int cand3[2187], nc3 = 0, cand5[2187], nc5 = 0, cand7[81], nc7 = 0;
                for (int idx = 0; idx < nker2; idx++) {
                    const int *v = ker2[idx]; int nv[8]; mat_vec8(Ne, v, nv);
                    if (q8(v) == (lam * qu[3]) % 3 && q8(nv) == (lam * qu[4]) % 3 && b8(v, nv) == (lam * bu[3][4]) % 3) {
                        int ok = 1;
                        for (int a = 0; a <= 2; a++)
                            if (b8(y[a], v) != (lam * bu[a][3]) % 3 || b8(y[a], nv) != (lam * bu[a][4]) % 3) { ok = 0; break; }
                        if (ok) cand3[nc3++] = idx;
                    }
                    if (q8(v) == (lam * qu[5]) % 3 && q8(nv) == (lam * qu[6]) % 3 && b8(v, nv) == (lam * bu[5][6]) % 3) {
                        int ok = 1;
                        for (int a = 0; a <= 2; a++)
                            if (b8(y[a], v) != (lam * bu[a][5]) % 3 || b8(y[a], nv) != (lam * bu[a][6]) % 3) { ok = 0; break; }
                        if (ok) cand5[nc5++] = idx;
                    }
                }
                for (int idx = 0; idx < nker1; idx++) {
                    const int *v = ker1[idx];
                    if (q8(v) != (lam * qu[7]) % 3) continue;
                    int ok = 1;
                    for (int a = 0; a <= 2; a++) if (b8(y[a], v) != (lam * bu[a][7]) % 3) { ok = 0; break; }
                    if (ok) cand7[nc7++] = idx;
                }
                for (int i3 = 0; i3 < nc3; i3++) {
                    memcpy(y[3], ker2[cand3[i3]], sizeof(int)*8); mat_vec8(Ne, y[3], y[4]);
                    for (int i5 = 0; i5 < nc5; i5++) {
                        const int *v5 = ker2[cand5[i5]]; int nv5[8]; mat_vec8(Ne, v5, nv5);
                        if (b8(y[3], v5) != (lam * bu[3][5]) % 3 || b8(y[3], nv5) != (lam * bu[3][6]) % 3 ||
                            b8(y[4], v5) != (lam * bu[4][5]) % 3 || b8(y[4], nv5) != (lam * bu[4][6]) % 3) continue;
                        memcpy(y[5], v5, sizeof(int)*8); memcpy(y[6], nv5, sizeof(int)*8);
                        for (int i7 = 0; i7 < nc7; i7++) {
                            const int *v7 = ker1[cand7[i7]];
                            if (b8(y[3], v7) != (lam * bu[3][7]) % 3 || b8(y[4], v7) != (lam * bu[4][7]) % 3 ||
                                b8(y[5], v7) != (lam * bu[5][7]) % 3 || b8(y[6], v7) != (lam * bu[6][7]) % 3) continue;
                            memcpy(y[7], v7, sizeof(int)*8);
                            int Ymat[8][8], M[8][8];
                            for (int r = 0; r < 8; r++) for (int c = 0; c < 8; c++) Ymat[r][c] = y[c][r];
                            mat_mul8(Ymat, Uinv, M);
                            for (int r = 0; r < 8; r++) for (int c = 0; c < 8; c++) norm_mats[n_norm][r][c] = (uint8_t)M[r][c];
                            n_norm++;
                        }
                    }
                }
            }
        }
    }
}

static int apply_norm_to_orb3(int m_idx, int o3_idx, const int *orb3_rep_pl, const int *pl_to_orb3) {
    int pl = orb3_rep_pl[o3_idx], img_pl[13];
    for (int k = 0; k < 13; k++) {
        int p = planes[pl][k], w[8];
        for (int r = 0; r < 8; r++) {
            int s = 0;
            for (int c = 0; c < 8; c++) s += norm_mats[m_idx][r][c] * pts[p][c];
            w[r] = s % 3;
        }
        img_pl[k] = vec_to_pt[vec_code(w)];
    }
    for (int a = 0; a < 13; a++)
        for (int b = a + 1; b < 13; b++)
            if (img_pl[a] > img_pl[b]) { int t = img_pl[a]; img_pl[a] = img_pl[b]; img_pl[b] = t; }
    return pl_to_orb3[find_plane(img_pl)];
}

static uint16_t opt_items[NOPTS][13];
static uint64_t opt_item_mask[NOPTS][IWORDS];
static uint64_t compat_mask[NOPTS][NWORDS];
static uint64_t item_opts[NITEMS][NWORDS];

typedef struct {
    int branch_id;
    int j1;
    int j2;
} Task;

static Task tasks[300];
static int ntasks = 0;
static int next_task_idx = 0;
static pthread_mutex_t task_mu = PTHREAD_MUTEX_INITIALIZER;
static volatile int global_found_sat = 0;
static int sat_sol[27];
static uint64_t task_nodes[300];
static int task_res[300];

typedef struct {
    uint64_t nodes;
    int sol[30];
} SearchCtx;

static int swar_dfs(SearchCtx *ctx, int depth, uint64_t active[NWORDS], uint64_t uncov[IWORDS]) {
    for (;;) {
        if ((uncov[0] | uncov[1] | uncov[2] | uncov[3] | uncov[4] | uncov[5]) == 0)
            return 1;
        if (global_found_sat) return 0;

        int n_act = 0;
        int nz_w[NWORDS], nnz = 0;
        for (int w = 0; w < NWORDS; w++) {
            uint64_t aw = active[w];
            if (aw) {
                nz_w[nnz++] = w;
                n_act += __builtin_popcountll(aw);
            }
        }
        if (n_act < 27 - depth) return 0;

        int best_item = -1, best_deg = 1000000;
        int forced_opts[20], n_forced = 0;

        if (n_act < 750) {
            uint16_t deg[NITEMS] = {0};
            uint16_t last_opt[NITEMS];
            for (int idx = 0; idx < nnz; idx++) {
                int w = nz_w[idx];
                uint64_t aw = active[w];
                while (aw) {
                    int bit = __builtin_ctzll(aw);
                    aw &= aw - 1;
                    int opt = (w << 6) + bit;
                    const uint16_t *it = opt_items[opt];
                    for (int k = 0; k < 13; k++) {
                        uint16_t r = it[k];
                        deg[r]++;
                        last_opt[r] = (uint16_t)opt;
                    }
                }
            }
            for (int iw = 0; iw < IWORDS; iw++) {
                uint64_t u = uncov[iw];
                while (u) {
                    int bit = __builtin_ctzll(u);
                    u &= u - 1;
                    int item = (iw << 6) + bit;
                    int d = deg[item];
                    if (d == 0) return 0;
                    if (d == 1) {
                        if (n_forced < 20) forced_opts[n_forced++] = last_opt[item];
                    } else if (d < best_deg) {
                        best_deg = d; best_item = item;
                    }
                }
            }
        } else {
            for (int iw = 0; iw < IWORDS; iw++) {
                uint64_t u = uncov[iw];
                while (u) {
                    int bit = __builtin_ctzll(u);
                    u &= u - 1;
                    int item = (iw << 6) + bit;
                    const uint64_t *io = item_opts[item];
                    int d = 0;
                    for (int idx = 0; idx < nnz; idx++) {
                        int w = nz_w[idx];
                        d += __builtin_popcountll(active[w] & io[w]);
                    }
                    if (d == 0) return 0;
                    if (d == 1) {
                        for (int idx = 0; idx < nnz; idx++) {
                            int w = nz_w[idx];
                            uint64_t m = active[w] & io[w];
                            if (m) { forced_opts[n_forced++] = (w << 6) + __builtin_ctzll(m); break; }
                        }
                        break;
                    }
                    if (d < best_deg) { best_deg = d; best_item = item; }
                }
                if (n_forced > 0) break;
            }
        }

        if (n_forced > 0) {
            for (int f = 0; f < n_forced; f++) {
                int chosen = forced_opts[f];
                /* Verify chosen is still active and disjoint from earlier forced opts in this batch! */
                if (!(active[chosen >> 6] & (1ULL << (chosen & 63)))) {
                    /* If an item covered by chosen was STILL uncovered, contradiction -> UNSAT!
                     * Otherwise another forced opt already covered that item? No: two distinct options covering the same item
                     * cannot both have deg==1; if chosen became inactive, it conflicted with an earlier forced opt on ANOTHER item,
                     * leaving its own deg==1 item with 0 active options -> UNSAT!! */
                    return 0;
                }
                /* Skip duplicate if two deg==1 items pointed to the SAME chosen option!
                 * Wait: if chosen was already picked in this loop, active[chosen] IS 0! Let's check duplicate first! */
                ctx->sol[depth++] = chosen;
                const uint64_t *cm = compat_mask[chosen];
                for (int idx = 0; idx < nnz; idx++) {
                    int w = nz_w[idx];
                    active[w] &= cm[w];
                }
                const uint64_t *im = opt_item_mask[chosen];
                for (int iw = 0; iw < IWORDS; iw++) uncov[iw] &= ~im[iw];
                /* Only apply ONE forced option per iteration if duplicates could occur, or deduplicate! */
                break;
            }
            continue;
        }

        ctx->nodes++;
        int cand[300], ncand = 0;
        const uint64_t *io = item_opts[best_item];
        for (int idx = 0; idx < nnz; idx++) {
            int w = nz_w[idx];
            uint64_t m = active[w] & io[w];
            while (m) {
                int bit = __builtin_ctzll(m);
                m &= m - 1;
                cand[ncand++] = (w << 6) + bit;
            }
        }
        for (int i = 0; i < ncand; i++) {
            int opt = cand[i];
            ctx->sol[depth] = opt;
            uint64_t next_act[NWORDS];
            memset(next_act, 0, sizeof(next_act));
            const uint64_t *cm = compat_mask[opt];
            for (int idx = 0; idx < nnz; idx++) {
                int w = nz_w[idx];
                next_act[w] = active[w] & cm[w];
            }
            uint64_t next_uncov[IWORDS];
            const uint64_t *im = opt_item_mask[opt];
            for (int iw = 0; iw < IWORDS; iw++) next_uncov[iw] = uncov[iw] & ~im[iw];

            int res = swar_dfs(ctx, depth + 1, next_act, next_uncov);
            if (res == 1) return 1;
            active[opt >> 6] &= ~(1ULL << (opt & 63));
        }
        return 0;
    }
}

static void *worker_loop(void *arg) {
    (void)arg;
    for (;;) {
        int tidx;
        pthread_mutex_lock(&task_mu);
        if (global_found_sat || next_task_idx >= ntasks) {
            pthread_mutex_unlock(&task_mu);
            return NULL;
        }
        tidx = next_task_idx++;
        pthread_mutex_unlock(&task_mu);

        int j1 = tasks[tidx].j1;
        int j2 = tasks[tidx].j2;
        uint64_t active[NWORDS], uncov[IWORDS];
        for (int iw = 0; iw < IWORDS; iw++) uncov[iw] = ~0ULL;
        uncov[IWORDS - 1] &= ((1ULL << (NITEMS & 63)) - 1);
        for (int w = 0; w < NWORDS; w++)
            active[w] = compat_mask[0][w] & compat_mask[j1][w] & compat_mask[j2][w];
        for (int iw = 0; iw < IWORDS; iw++)
            uncov[iw] &= ~(opt_item_mask[0][iw] | opt_item_mask[j1][iw] | opt_item_mask[j2][iw]);

        SearchCtx ctx;
        ctx.nodes = 0;
        ctx.sol[0] = 0; ctx.sol[1] = j1; ctx.sol[2] = j2;
        int res = swar_dfs(&ctx, 3, active, uncov);
        task_nodes[tidx] = ctx.nodes;
        task_res[tidx] = res;

        if (res == 1) {
            pthread_mutex_lock(&task_mu);
            if (!global_found_sat) {
                global_found_sat = 1;
                memcpy(sat_sol, ctx.sol, 27 * sizeof(int));
            }
            pthread_mutex_unlock(&task_mu);
            printf("  *** SAT FOUND ON TASK %d (j1=%d, j2=%d)!! ***\n", tidx, j1, j2);
            return NULL;
        }
        if ((tidx + 1) % 25 == 0 || tidx + 1 == ntasks) {
            printf("  Progress: completed task %3d / %3d (branch=%d, j1=%4d, j2=%4d, nodes=%llu)\n",
                   tidx + 1, ntasks, tasks[tidx].branch_id, j1, j2, (unsigned long long)ctx.nodes);
        }
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    struct timespec ts0, ts1;
    clock_gettime(CLOCK_MONOTONIC, &ts0);

    build_q7_3();
    enumerate_normalizer();

    int pt_img[1066], pt_orb[1066], orb_rep_pt[NITEMS];
    memset(pt_orb, -1, sizeof(pt_orb));
    int norb = 0;
    for (int p = 0; p < 1066; p++) {
        int w[8]; mat_vec8(A_mat, pts[p], w);
        pt_img[p] = vec_to_pt[vec_code(w)];
    }
    for (int p = 0; p < 1066; p++) {
        if (pt_img[p] == p) continue;
        if (pt_orb[p] == -1) {
            orb_rep_pt[norb] = p;
            int c = p;
            while (pt_orb[c] == -1) { pt_orb[c] = norb; c = pt_img[c]; }
            norb++;
        }
    }
    uint8_t vis[22960] = {0};
    int pl_to_orb3[22960]; memset(pl_to_orb3, -1, sizeof(pl_to_orb3));
    int orb3_rep_pl[NOPTS], norb3 = 0;
    for (int j = 0; j < 22960; j++) {
        if (vis[j]) continue;
        int orb[3], olen = 0, cur = j;
        while (!vis[cur]) {
            vis[cur] = 1; orb[olen++] = cur;
            int img_pl[13];
            for (int k = 0; k < 13; k++) img_pl[k] = pt_img[planes[cur][k]];
            for (int a = 0; a < 13; a++)
                for (int b = a + 1; b < 13; b++)
                    if (img_pl[a] > img_pl[b]) { int t = img_pl[a]; img_pl[a] = img_pl[b]; img_pl[b] = t; }
            cur = find_plane(img_pl);
        }
        if (olen != 3) continue;
        uint8_t seen_pt[1066] = {0}; int disj = 1;
        for (int a = 0; a < 3 && disj; a++)
            for (int k = 0; k < 13; k++) {
                int x = planes[orb[a]][k];
                if (seen_pt[x]) { disj = 0; break; }
                seen_pt[x] = 1;
            }
        if (!disj) continue;
        orb3_rep_pl[norb3] = orb[0];
        for (int a = 0; a < 3; a++) pl_to_orb3[orb[a]] = norb3;
        for (int k = 0; k < 13; k++) {
            int it = pt_orb[planes[orb[0]][k]];
            opt_items[norb3][k] = (uint16_t)it;
            opt_item_mask[norb3][it >> 6] |= (1ULL << (it & 63));
            item_opts[it][norb3 >> 6] |= (1ULL << (norb3 & 63));
        }
        norb3++;
    }
    for (int i = 0; i < NOPTS; i++)
        for (int j = 0; j < NOPTS; j++) {
            if (i == j) continue;
            uint64_t ov = 0;
            for (int iw = 0; iw < IWORDS; iw++) ov |= (opt_item_mask[i][iw] & opt_item_mask[j][iw]);
            if (ov == 0) compat_mask[i][j >> 6] |= (1ULL << (j & 63));
        }

    /* Generate all 4 Depth-1 branches on r1 = 342, sorted by largest |Stab_N({0,j1})| first,
     * and eliminate Orb_N({0, j1}) from compat_mask after each UNSAT stage! */
    int r1 = 342;
    int stab0_r1[300], nstab0_r1 = 0;
    int *m_of_0 = malloc(n_norm * sizeof(int));
    for (int m = 0; m < n_norm; m++) m_of_0[m] = apply_norm_to_orb3(m, 0, orb3_rep_pl, pl_to_orb3);

    for (int m = 0; m < n_norm; m++) {
        if (m_of_0[m] != 0) continue;
        int p = orb_rep_pt[r1], w[8];
        for (int a = 0; a < 8; a++) {
            int sum = 0;
            for (int b = 0; b < 8; b++) sum += norm_mats[m][a][b] * pts[p][b];
            w[a] = sum % 3;
        }
        if (pt_orb[vec_to_pt[vec_code(w)]] == r1) stab0_r1[nstab0_r1++] = m;
    }

    int j1_reps[10], j1_stabs[10], nj1 = 0;
    uint8_t vis_j1[NOPTS] = {0};
    for (int j = 0; j < NOPTS; j++) {
        if (!(compat_mask[0][j >> 6] & (1ULL << (j & 63)))) continue;
        if (!(item_opts[r1][j >> 6] & (1ULL << (j & 63)))) continue;
        if (vis_j1[j]) continue;
        j1_reps[nj1] = j;
        int cnt = 0;
        for (int m = 0; m < n_norm; m++) {
            int a0 = m_of_0[m];
            if (a0 != 0 && a0 != j) continue;
            int a1 = apply_norm_to_orb3(m, j, orb3_rep_pl, pl_to_orb3);
            if ((a0 == 0 && a1 == j) || (a0 == j && a1 == 0)) cnt++;
        }
        j1_stabs[nj1++] = cnt;
        for (int s = 0; s < nstab0_r1; s++)
            vis_j1[apply_norm_to_orb3(stab0_r1[s], j, orb3_rep_pl, pl_to_orb3)] = 1;
    }
    for (int a = 0; a < nj1; a++)
        for (int b = a + 1; b < nj1; b++)
            if (j1_stabs[b] > j1_stabs[a]) {
                int t = j1_reps[a]; j1_reps[a] = j1_reps[b]; j1_reps[b] = t;
                int ts = j1_stabs[a]; j1_stabs[a] = j1_stabs[b]; j1_stabs[b] = ts;
            }

    uint64_t grand_nodes = 0;
    int grand_tasks = 0;
    for (int b = 0; b < nj1; b++) {
        int j1 = j1_reps[b];
        if (!(compat_mask[0][j1 >> 6] & (1ULL << (j1 & 63)))) continue;
        int stab_pair[300], nsp = 0;
        for (int m = 0; m < n_norm; m++) {
            int a0 = m_of_0[m];
            if (a0 != 0 && a0 != j1) continue;
            int a1 = apply_norm_to_orb3(m, j1, orb3_rep_pl, pl_to_orb3);
            if ((a0 == 0 && a1 == j1) || (a0 == j1 && a1 == 0)) stab_pair[nsp++] = m;
        }
        uint8_t cov01[NITEMS] = {0};
        for (int k = 0; k < 13; k++) { cov01[opt_items[0][k]] = 1; cov01[opt_items[j1][k]] = 1; }

        int best_r2 = -1, best_norb2 = 1000000, best_reps[300];
        for (int r2 = 0; r2 < NITEMS; r2++) {
            if (cov01[r2]) continue;
            int stab_r2[300], nsr2 = 0;
            for (int s = 0; s < nsp; s++) {
                int m = stab_pair[s], p = orb_rep_pt[r2], w[8];
                for (int a = 0; a < 8; a++) {
                    int sum = 0;
                    for (int c = 0; c < 8; c++) sum += norm_mats[m][a][c] * pts[p][c];
                    w[a] = sum % 3;
                }
                if (pt_orb[vec_to_pt[vec_code(w)]] == r2) stab_r2[nsr2++] = m;
            }
            uint8_t vis2[NOPTS] = {0};
            int reps2[300], nr2 = 0;
            for (int j2 = 0; j2 < NOPTS; j2++) {
                if (!(compat_mask[0][j2 >> 6] & (1ULL << (j2 & 63)))) continue;
                if (!(compat_mask[j1][j2 >> 6] & (1ULL << (j2 & 63)))) continue;
                if (!(item_opts[r2][j2 >> 6] & (1ULL << (j2 & 63)))) continue;
                if (vis2[j2]) continue;
                reps2[nr2++] = j2;
                for (int s = 0; s < nsr2; s++)
                    vis2[apply_norm_to_orb3(stab_r2[s], j2, orb3_rep_pl, pl_to_orb3)] = 1;
            }
            if (nr2 < best_norb2) {
                best_norb2 = nr2; best_r2 = r2;
                memcpy(best_reps, reps2, nr2 * sizeof(int));
            }
        }
        ntasks = 0; next_task_idx = 0;
        for (int t = 0; t < best_norb2; t++) {
            tasks[ntasks].branch_id = b;
            tasks[ntasks].j1 = j1;
            tasks[ntasks].j2 = best_reps[t];
            ntasks++;
        }
        struct timespec s0, s1;
        clock_gettime(CLOCK_MONOTONIC, &s0);
        pthread_t tids[4];
        for (int t = 0; t < 4; t++) pthread_create(&tids[t], NULL, worker_loop, NULL);
        for (int t = 0; t < 4; t++) pthread_join(tids[t], NULL);
        clock_gettime(CLOCK_MONOTONIC, &s1);
        uint64_t snodes = 0;
        for (int i = 0; i < ntasks; i++) snodes += task_nodes[i];
        grand_nodes += snodes;
        grand_tasks += ntasks;
        printf("Stage %d (j1=%4d, |Stab|=%2d, r2=%3d, %2d tasks): sat=%d, nodes=%9llu, time=%.3fs\n",
               b, j1, nsp, best_r2, ntasks, global_found_sat, (unsigned long long)snodes,
               (s1.tv_sec - s0.tv_sec) + 1e-9*(s1.tv_nsec - s0.tv_nsec));
        if (global_found_sat) break;

        if (b + 1 < nj1) {
            for (int m = 0; m < n_norm; m++) {
                int u = m_of_0[m];
                int v = apply_norm_to_orb3(m, j1, orb3_rep_pl, pl_to_orb3);
                compat_mask[u][v >> 6] &= ~(1ULL << (v & 63));
                compat_mask[v][u >> 6] &= ~(1ULL << (u & 63));
            }
        }
    }
    free(m_of_0);
    free(norm_mats);
    clock_gettime(CLOCK_MONOTONIC, &ts1);
    printf("=== STAGED SWAR COMPLETE: sat=%d, total_tasks=%d, total_nodes=%llu, wall_time=%.3fs ===\n",
           global_found_sat, grand_tasks, (unsigned long long)grand_nodes,
           (ts1.tv_sec - ts0.tv_sec) + 1e-9*(ts1.tv_nsec - ts0.tv_nsec));
    return 0;
}
