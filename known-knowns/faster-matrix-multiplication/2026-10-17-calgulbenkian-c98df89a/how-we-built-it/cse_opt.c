/*
 * cse_opt.c — Native C Multi-Threaded CSE + O(f * row_len) Exact Lookahead (gp)
 *             + Warm-Started LNS + Exact Sub-Row Re-Covering & Pruning Optimizer
 *             for Fast Matrix Multiplication Ternary Linear Maps over Z.
 *
 * Compile: clang -O3 -pthread -o cse_opt cse_opt.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#define MAX_ROWS 256
#define MAX_BASE 256
#define MAX_VARS 640
#define MAX_ROW_LEN 64

typedef struct {
    int idx;
    int val; /* -1 or +1 */
} Term;

typedef struct {
    int len;
    Term t[MAX_ROW_LEN];
} Row;

typedef struct {
    int a;
    int b;
    int s; /* +1 or -1: v_new = v_a + s * v_b */
} FreshDef;

typedef struct {
    int n_fresh;
    FreshDef fresh[MAX_VARS];
    Row out[MAX_ROWS];
    int total_adds;
} Solution;

/* Global problem definition (read-only during search) */
static int G_R = 0;
static int G_C = 0;
static int G_target[MAX_ROWS][MAX_BASE];
static uint64_t G_zobrist[MAX_BASE];
static Solution G_init_sol;
static int G_has_init = 0;

/* Shared best solution protected by mutex */
static pthread_mutex_t G_lock = PTHREAD_MUTEX_INITIALIZER;
static Solution G_best_sol;
static volatile int G_stop = 0;
static int G_time_limit_ms = 5000;
static struct timespec G_start_time;

static inline uint64_t xorshift64(uint64_t *state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    return x;
}

static long elapsed_ms(void) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (now.tv_sec - G_start_time.tv_sec) * 1000L +
           (now.tv_nsec - G_start_time.tv_nsec) / 1000000L;
}

static int compute_sol_adds(const Solution *sol) {
    int adds = sol->n_fresh; /* each fresh var is a binary op (len 2 -> 1 add) */
    for (int r = 0; r < G_R; r++) {
        if (sol->out[r].len > 1) {
            adds += sol->out[r].len - 1;
        }
    }
    return adds;
}

/* Verify that a Solution expands exactly to G_target over Z */
static int verify_solution(const Solution *sol) {
    int total_vars = G_C + sol->n_fresh;
    if (total_vars > MAX_VARS) return 0;
    int vec[MAX_VARS][MAX_BASE];
    memset(vec, 0, sizeof(int) * total_vars * G_C);
    for (int i = 0; i < G_C; i++) vec[i][i] = 1;

    for (int f = 0; f < sol->n_fresh; f++) {
        int a = sol->fresh[f].a;
        int b = sol->fresh[f].b;
        int s = sol->fresh[f].s;
        int v_idx = G_C + f;
        if (a < 0 || a >= v_idx || b < 0 || b >= v_idx || a == b) return 0;
        if (s != 1 && s != -1) return 0;
        for (int c = 0; c < G_C; c++) {
            vec[v_idx][c] = vec[a][c] + s * vec[b][c];
        }
    }

    for (int r = 0; r < G_R; r++) {
        if (sol->out[r].len < 1 || sol->out[r].len > MAX_ROW_LEN) return 0;
        int acc[MAX_BASE];
        memset(acc, 0, sizeof(int) * G_C);
        for (int i = 0; i < sol->out[r].len; i++) {
            int idx = sol->out[r].t[i].idx;
            int val = sol->out[r].t[i].val;
            if (idx < 0 || idx >= total_vars) return 0;
            if (val != 1 && val != -1) return 0;
            for (int j = 0; j < i; j++) {
                if (sol->out[r].t[j].idx == idx) return 0; /* duplicate */
            }
            for (int c = 0; c < G_C; c++) {
                acc[c] += val * vec[idx][c];
            }
        }
        for (int c = 0; c < G_C; c++) {
            if (acc[c] != G_target[r][c]) return 0;
        }
    }
    return 1;
}

/*
 * Post-processing:
 * 1. Exact sub-row re-covering (replace k-subsets of output rows with 1-term or 2-term
 *    combinations of existing variables).
 * 2. Semantic 2-subset collision CSE across output rows.
 * 3. Dead (0-use) and single-use (1-use canceling) fresh variable elimination.
 */
static void post_optimize(Solution *sol) {
    int improved = 1;
    while (improved) {
        improved = 0;
        int n_vars = G_C + sol->n_fresh;
        int vec[MAX_VARS][MAX_BASE];
        uint64_t h[MAX_VARS];
        memset(vec, 0, sizeof(int) * n_vars * G_C);
        for (int i = 0; i < G_C; i++) {
            vec[i][i] = 1;
            h[i] = G_zobrist[i];
        }
        for (int f = 0; f < sol->n_fresh; f++) {
            int a = sol->fresh[f].a;
            int b = sol->fresh[f].b;
            int s = sol->fresh[f].s;
            int v = G_C + f;
            for (int c = 0; c < G_C; c++) {
                vec[v][c] = vec[a][c] + s * vec[b][c];
            }
            h[v] = h[a] + (uint64_t)((int64_t)s) * h[b];
        }

        /* Step A: Sub-row re-covering on each output row */
        for (int r = 0; r < G_R; r++) {
            int L = sol->out[r].len;
            if (L < 2) continue;

            /* First check if the ENTIRE row equals 1-term or 2-term (when L >= 3) */
            uint64_t row_h = 0;
            for (int i = 0; i < L; i++) {
                int idx = sol->out[r].t[i].idx;
                int val = sol->out[r].t[i].val;
                row_h += (val == 1) ? h[idx] : -h[idx];
            }

            /* Check 1-term match for whole row */
            int matched_whole = 0;
            for (int v = 0; v < n_vars && !matched_whole; v++) {
                for (int s = 1; s >= -1; s -= 2) {
                    uint64_t vh = (s == 1) ? h[v] : -h[v];
                    if (vh == row_h) {
                        int ok = 1;
                        for (int c = 0; c < G_C; c++) {
                            if (s * vec[v][c] != G_target[r][c]) { ok = 0; break; }
                        }
                        if (ok) {
                            sol->out[r].len = 1;
                            sol->out[r].t[0].idx = v;
                            sol->out[r].t[0].val = s;
                            matched_whole = 1;
                            improved = 1;
                            break;
                        }
                    }
                }
            }
            if (matched_whole) continue;

            /* If L >= 3, check 2-term match for whole row */
            if (L >= 3) {
                for (int v1 = 0; v1 < n_vars && !matched_whole; v1++) {
                    for (int s1 = 1; s1 >= -1 && !matched_whole; s1 -= 2) {
                        uint64_t rem_h = row_h - ((s1 == 1) ? h[v1] : -h[v1]);
                        for (int v2 = v1 + 1; v2 < n_vars && !matched_whole; v2++) {
                            for (int s2 = 1; s2 >= -1; s2 -= 2) {
                                uint64_t v2h = (s2 == 1) ? h[v2] : -h[v2];
                                if (v2h == rem_h) {
                                    int ok = 1;
                                    for (int c = 0; c < G_C; c++) {
                                        if (s1 * vec[v1][c] + s2 * vec[v2][c] != G_target[r][c]) {
                                            ok = 0; break;
                                        }
                                    }
                                    if (ok) {
                                        sol->out[r].len = 2;
                                        sol->out[r].t[0].idx = v1;
                                        sol->out[r].t[0].val = s1;
                                        sol->out[r].t[1].idx = v2;
                                        sol->out[r].t[1].val = s2;
                                        matched_whole = 1;
                                        improved = 1;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
                if (matched_whole) continue;
            }

            /* Check 2-subsets and 3-subsets inside row r */
            int row_changed = 0;
            /* Check if any 2-subset in row r equals a single variable v */
            for (int i1 = 0; i1 < L && !row_changed; i1++) {
                for (int i2 = i1 + 1; i2 < L && !row_changed; i2++) {
                    int u1 = sol->out[r].t[i1].idx, c1 = sol->out[r].t[i1].val;
                    int u2 = sol->out[r].t[i2].idx, c2 = sol->out[r].t[i2].val;
                    uint64_t sub_h = ((c1 == 1) ? h[u1] : -h[u1]) + ((c2 == 1) ? h[u2] : -h[u2]);
                    for (int v = 0; v < n_vars && !row_changed; v++) {
                        /* Ensure v is not already in the remaining terms of row r */
                        int conflict = 0;
                        for (int k = 0; k < L; k++) {
                            if (k != i1 && k != i2 && sol->out[r].t[k].idx == v) { conflict = 1; break; }
                        }
                        if (conflict) continue;
                        for (int s = 1; s >= -1; s -= 2) {
                            if (((s == 1) ? h[v] : -h[v]) == sub_h) {
                                int ok = 1;
                                for (int c = 0; c < G_C; c++) {
                                    if (s * vec[v][c] != c1 * vec[u1][c] + c2 * vec[u2][c]) { ok = 0; break; }
                                }
                                if (ok) {
                                    sol->out[r].t[i1].idx = v;
                                    sol->out[r].t[i1].val = s;
                                    sol->out[r].t[i2] = sol->out[r].t[L - 1];
                                    sol->out[r].len = L - 1;
                                    row_changed = 1;
                                    improved = 1;
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            if (row_changed) continue;

            /* Check if any 3-subset in row r equals a 1-term or 2-term combination */
            if (L >= 4) {
                for (int i1 = 0; i1 < L && !row_changed; i1++) {
                    for (int i2 = i1 + 1; i2 < L && !row_changed; i2++) {
                        for (int i3 = i2 + 1; i3 < L && !row_changed; i3++) {
                            int u1 = sol->out[r].t[i1].idx, c1 = sol->out[r].t[i1].val;
                            int u2 = sol->out[r].t[i2].idx, c2 = sol->out[r].t[i2].val;
                            int u3 = sol->out[r].t[i3].idx, c3 = sol->out[r].t[i3].val;
                            uint64_t sub_h = ((c1 == 1) ? h[u1] : -h[u1]) +
                                             ((c2 == 1) ? h[u2] : -h[u2]) +
                                             ((c3 == 1) ? h[u3] : -h[u3]);
                            int sub_vec[MAX_BASE];
                            for (int c = 0; c < G_C; c++) {
                                sub_vec[c] = c1 * vec[u1][c] + c2 * vec[u2][c] + c3 * vec[u3][c];
                            }
                            /* Check 2-term replacement for this 3-subset */
                            for (int v1 = 0; v1 < n_vars && !row_changed; v1++) {
                                int conf1 = 0;
                                for (int k = 0; k < L; k++) {
                                    if (k != i1 && k != i2 && k != i3 && sol->out[r].t[k].idx == v1) { conf1 = 1; break; }
                                }
                                if (conf1) continue;
                                for (int s1 = 1; s1 >= -1 && !row_changed; s1 -= 2) {
                                    uint64_t rem_h = sub_h - ((s1 == 1) ? h[v1] : -h[v1]);
                                    for (int v2 = v1 + 1; v2 < n_vars && !row_changed; v2++) {
                                        int conf2 = 0;
                                        for (int k = 0; k < L; k++) {
                                            if (k != i1 && k != i2 && k != i3 && sol->out[r].t[k].idx == v2) { conf2 = 1; break; }
                                        }
                                        if (conf2) continue;
                                        for (int s2 = 1; s2 >= -1; s2 -= 2) {
                                            if (((s2 == 1) ? h[v2] : -h[v2]) == rem_h) {
                                                int ok = 1;
                                                for (int c = 0; c < G_C; c++) {
                                                    if (s1 * vec[v1][c] + s2 * vec[v2][c] != sub_vec[c]) { ok = 0; break; }
                                                }
                                                if (ok) {
                                                    sol->out[r].t[i1].idx = v1;
                                                    sol->out[r].t[i1].val = s1;
                                                    sol->out[r].t[i2].idx = v2;
                                                    sol->out[r].t[i2].val = s2;
                                                    sol->out[r].t[i3] = sol->out[r].t[L - 1];
                                                    sol->out[r].len = L - 1;
                                                    row_changed = 1;
                                                    improved = 1;
                                                    break;
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

        /* Step B: Prune 0-use fresh variables and inline 1-use fresh variables */
        int use_cnt[MAX_VARS];
        memset(use_cnt, 0, sizeof(int) * n_vars);
        for (int f = 0; f < sol->n_fresh; f++) {
            use_cnt[sol->fresh[f].a]++;
            use_cnt[sol->fresh[f].b]++;
        }
        for (int r = 0; r < G_R; r++) {
            for (int i = 0; i < sol->out[r].len; i++) {
                use_cnt[sol->out[r].t[i].idx]++;
            }
        }
        int pruned = 0;
        for (int f = sol->n_fresh - 1; f >= 0; f--) {
            int v = G_C + f;
            if (use_cnt[v] == 0) {
                for (int f2 = f; f2 < sol->n_fresh - 1; f2++) {
                    sol->fresh[f2] = sol->fresh[f2 + 1];
                    if (sol->fresh[f2].a > v) sol->fresh[f2].a--;
                    if (sol->fresh[f2].b > v) sol->fresh[f2].b--;
                }
                sol->n_fresh--;
                for (int r = 0; r < G_R; r++) {
                    for (int i = 0; i < sol->out[r].len; i++) {
                        if (sol->out[r].t[i].idx > v) sol->out[r].t[i].idx--;
                    }
                }
                improved = 1;
                pruned = 1;
                break;
            } else if (use_cnt[v] == 1) {
                /* Check if used in an output row r where inlining cancels a term */
                int a = sol->fresh[f].a;
                int b = sol->fresh[f].b;
                int s = sol->fresh[f].s;
                for (int r = 0; r < G_R; r++) {
                    int pos_v = -1, pos_a = -1, pos_b = -1;
                    for (int i = 0; i < sol->out[r].len; i++) {
                        if (sol->out[r].t[i].idx == v) pos_v = i;
                        else if (sol->out[r].t[i].idx == a) pos_a = i;
                        else if (sol->out[r].t[i].idx == b) pos_b = i;
                    }
                    if (pos_v != -1) {
                        int cv = sol->out[r].t[pos_v].val;
                        int ca = cv;
                        int cb = cv * s;
                        if (pos_a != -1 && pos_b == -1 && sol->out[r].t[pos_a].val + ca == 0) {
                            /* v_a cancels! Replace v with cb*v_b and remove v_a */
                            sol->out[r].t[pos_v].idx = b;
                            sol->out[r].t[pos_v].val = cb;
                            sol->out[r].t[pos_a] = sol->out[r].t[sol->out[r].len - 1];
                            sol->out[r].len--;
                            improved = 1;
                            pruned = 1;
                        } else if (pos_b != -1 && pos_a == -1 && sol->out[r].t[pos_b].val + cb == 0) {
                            /* v_b cancels! Replace v with ca*v_a and remove v_b */
                            sol->out[r].t[pos_v].idx = a;
                            sol->out[r].t[pos_v].val = ca;
                            sol->out[r].t[pos_b] = sol->out[r].t[sol->out[r].len - 1];
                            sol->out[r].len--;
                            improved = 1;
                            pruned = 1;
                        }
                        break;
                    }
                }
                if (pruned) break;
            }
        }
        if (pruned) continue;

        /* Step C: Semantic 2-subset collision across distinct output rows */
        if (n_vars < MAX_VARS - 1) {
            int found_sem = 0;
            for (int r1 = 0; r1 < G_R && !found_sem; r1++) {
                int L1 = sol->out[r1].len;
                if (L1 < 2) continue;
                for (int i1 = 0; i1 < L1 && !found_sem; i1++) {
                    for (int j1 = i1 + 1; j1 < L1 && !found_sem; j1++) {
                        int u1 = sol->out[r1].t[i1].idx, c1 = sol->out[r1].t[i1].val;
                        int u2 = sol->out[r1].t[j1].idx, c2 = sol->out[r1].t[j1].val;
                        uint64_t h1 = ((c1 == 1) ? h[u1] : -h[u1]) + ((c2 == 1) ? h[u2] : -h[u2]);
                        for (int r2 = r1 + 1; r2 < G_R && !found_sem; r2++) {
                            int L2 = sol->out[r2].len;
                            if (L2 < 2) continue;
                            for (int i2 = 0; i2 < L2 && !found_sem; i2++) {
                                for (int j2 = i2 + 1; j2 < L2 && !found_sem; j2++) {
                                    int v1 = sol->out[r2].t[i2].idx, d1 = sol->out[r2].t[i2].val;
                                    int v2 = sol->out[r2].t[j2].idx, d2 = sol->out[r2].t[j2].val;
                                    uint64_t h2 = ((d1 == 1) ? h[v1] : -h[v1]) + ((d2 == 1) ? h[v2] : -h[v2]);
                                    int s_match = 0;
                                    if (h1 == h2) s_match = 1;
                                    else if (h1 == -h2) s_match = -1;
                                    if (s_match != 0) {
                                        int ok = 1;
                                        for (int c = 0; c < G_C; c++) {
                                            int w1 = c1 * vec[u1][c] + c2 * vec[u2][c];
                                            int w2 = d1 * vec[v1][c] + d2 * vec[v2][c];
                                            if (w1 != s_match * w2) { ok = 0; break; }
                                        }
                                        if (ok) {
                                            /* Create fresh variable v_new = u1 + (c1*c2)*u2 */
                                            int v_new = G_C + sol->n_fresh;
                                            int a = (u1 < u2) ? u1 : u2;
                                            int b = (u1 < u2) ? u2 : u1;
                                            int sa = (u1 < u2) ? c1 : c2;
                                            int sb = (u1 < u2) ? c2 : c1;
                                            sol->fresh[sol->n_fresh].a = a;
                                            sol->fresh[sol->n_fresh].b = b;
                                            sol->fresh[sol->n_fresh].s = sa * sb;
                                            sol->n_fresh++;

                                            sol->out[r1].t[i1].idx = v_new;
                                            sol->out[r1].t[i1].val = sa;
                                            sol->out[r1].t[j1] = sol->out[r1].t[L1 - 1];
                                            sol->out[r1].len = L1 - 1;

                                            sol->out[r2].t[i2].idx = v_new;
                                            sol->out[r2].t[i2].val = sa * s_match;
                                            sol->out[r2].t[j2] = sol->out[r2].t[L2 - 1];
                                            sol->out[r2].len = L2 - 1;

                                            found_sem = 1;
                                            improved = 1;
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
    sol->total_adds = compute_sol_adds(sol);
}

/*
 * Forward CSE rollout from a given prefix of fresh variables.
 * strategy:
 *   0 = ga (greedy alternative: random among max freq)
 *   1 = gp (exact 1-step lookahead potential on top-24 pairs!)
 *   2 = gi (intersection lookahead with randomized tie-break)
 *   3 = gr (hybrid 70% gp/ga, 30% weighted random)
 */
static void run_rollout(Solution *sol, int prefix_len, int strategy, uint64_t *rng) {
    int n_vars = G_C;
    Row rows[MAX_ROWS];
    for (int r = 0; r < G_R; r++) {
        rows[r].len = 0;
        for (int c = 0; c < G_C; c++) {
            if (G_target[r][c] != 0) {
                rows[r].t[rows[r].len].idx = c;
                rows[r].t[rows[r].len].val = G_target[r][c];
                rows[r].len++;
            }
        }
    }

    /* Replay prefix */
    int actual_fresh = 0;
    for (int f = 0; f < prefix_len && n_vars < MAX_VARS - 1; f++) {
        int a = sol->fresh[f].a;
        int b = sol->fresh[f].b;
        int s = sol->fresh[f].s;
        if (a >= n_vars || b >= n_vars || a == b) continue;
        /* Count occurrences in rows */
        int occ = 0;
        for (int r = 0; r < G_R; r++) {
            int pa = -1, pb = -1;
            for (int i = 0; i < rows[r].len; i++) {
                if (rows[r].t[i].idx == a) pa = i;
                else if (rows[r].t[i].idx == b) pb = i;
            }
            if (pa != -1 && pb != -1 && rows[r].t[pa].val * s == rows[r].t[pb].val) {
                occ++;
            }
        }
        if (occ < 2) continue;
        int v_new = n_vars++;
        sol->fresh[actual_fresh].a = a;
        sol->fresh[actual_fresh].b = b;
        sol->fresh[actual_fresh].s = s;
        actual_fresh++;
        for (int r = 0; r < G_R; r++) {
            int pa = -1, pb = -1;
            for (int i = 0; i < rows[r].len; i++) {
                if (rows[r].t[i].idx == a) pa = i;
                else if (rows[r].t[i].idx == b) pb = i;
            }
            if (pa != -1 && pb != -1 && rows[r].t[pa].val * s == rows[r].t[pb].val) {
                int sign_new = rows[r].t[pa].val;
                rows[r].t[pa].idx = v_new;
                rows[r].t[pa].val = sign_new;
                rows[r].t[pb] = rows[r].t[rows[r].len - 1];
                rows[r].len--;
            }
        }
    }

    /* Continue CSE until no pair has frequency >= 2 */
    int16_t *freq_plus = (int16_t *)calloc(MAX_VARS * MAX_VARS, sizeof(int16_t));
    int16_t *freq_minus = (int16_t *)calloc(MAX_VARS * MAX_VARS, sizeof(int16_t));

    /* Build initial pair frequencies */
    for (int r = 0; r < G_R; r++) {
        int L = rows[r].len;
        for (int i = 0; i < L; i++) {
            int u = rows[r].t[i].idx, su = rows[r].t[i].val;
            for (int j = i + 1; j < L; j++) {
                int v = rows[r].t[j].idx, sv = rows[r].t[j].val;
                int a = (u < v) ? u : v;
                int b = (u < v) ? v : u;
                if (su == sv) freq_plus[a * MAX_VARS + b]++;
                else freq_minus[a * MAX_VARS + b]++;
            }
        }
    }

    while (n_vars < MAX_VARS - 1) {
        int max_f = 1;
        for (int a = 0; a < n_vars; a++) {
            int base_idx = a * MAX_VARS;
            for (int b = a + 1; b < n_vars; b++) {
                if (freq_plus[base_idx + b] > max_f) max_f = freq_plus[base_idx + b];
                if (freq_minus[base_idx + b] > max_f) max_f = freq_minus[base_idx + b];
            }
        }
        if (max_f < 2) break;

        /* Collect candidates */
        FreshDef cands[256];
        int cand_freq[256];
        int n_cands = 0;
        int min_f_collect = (strategy == 1 || strategy == 2) ? ((max_f > 2) ? max_f - 1 : 2) : max_f;
        if (strategy == 3 && (xorshift64(rng) % 100) < 25) {
            min_f_collect = 2;
        }

        for (int a = 0; a < n_vars; a++) {
            int base_idx = a * MAX_VARS;
            for (int b = a + 1; b < n_vars; b++) {
                for (int s = 1; s >= -1; s -= 2) {
                    int f = (s == 1) ? freq_plus[base_idx + b] : freq_minus[base_idx + b];
                    if (f >= min_f_collect) {
                        if (n_cands < 256) {
                            cands[n_cands].a = a;
                            cands[n_cands].b = b;
                            cands[n_cands].s = s;
                            cand_freq[n_cands] = f;
                            n_cands++;
                        } else {
                            /* reservoir replace if f == max_f */
                            int rep = xorshift64(rng) % 256;
                            if (f >= cand_freq[rep]) {
                                cands[rep].a = a;
                                cands[rep].b = b;
                                cands[rep].s = s;
                                cand_freq[rep] = f;
                            }
                        }
                    }
                }
            }
        }

        int chosen = 0;
        if (strategy == 0 || n_cands == 1) {
            chosen = xorshift64(rng) % n_cands;
        } else if (strategy == 1 || strategy == 2) {
            /* Exact O(f * row_len) 1-step lookahead potential (gp) */
            double best_score = -1e18;
            int best_list[256];
            int n_best = 0;
            int16_t c_plus[MAX_VARS], c_minus[MAX_VARS];
            int touched[MAX_VARS];
            memset(c_plus, 0, sizeof(c_plus));
            memset(c_minus, 0, sizeof(c_minus));

            for (int ci = 0; ci < n_cands; ci++) {
                int a = cands[ci].a;
                int b = cands[ci].b;
                int s = cands[ci].s;
                int f = cand_freq[ci];
                int n_touched = 0;
                int lost_profit = 0;

                for (int r = 0; r < G_R; r++) {
                    int pa = -1, pb = -1;
                    for (int i = 0; i < rows[r].len; i++) {
                        if (rows[r].t[i].idx == a) pa = i;
                        else if (rows[r].t[i].idx == b) pb = i;
                    }
                    if (pa != -1 && pb != -1 && rows[r].t[pa].val * s == rows[r].t[pb].val) {
                        int sa = rows[r].t[pa].val;
                        for (int i = 0; i < rows[r].len; i++) {
                            if (i == pa || i == pb) continue;
                            int c = rows[r].t[i].idx;
                            int sc = rows[r].t[i].val;
                            if (c_plus[c] == 0 && c_minus[c] == 0) {
                                touched[n_touched++] = c;
                            }
                            if (sc == sa) c_plus[c]++;
                            else c_minus[c]++;
                        }
                    }
                }

                int new_profit = 0;
                int max_new_pair = 0;
                for (int ti = 0; ti < n_touched; ti++) {
                    int c = touched[ti];
                    int cp = c_plus[c];
                    int cm = c_minus[c];
                    if (cp >= 2) new_profit += cp - 1;
                    if (cm >= 2) new_profit += cm - 1;
                    if (cp > max_new_pair) max_new_pair = cp;
                    if (cm > max_new_pair) max_new_pair = cm;

                    /* Compute lost profit on (a, c) and (b, c) */
                    int u1 = (a < c) ? a : c, v1 = (a < c) ? c : a;
                    int f_ac_p = freq_plus[u1 * MAX_VARS + v1];
                    int f_ac_m = freq_minus[u1 * MAX_VARS + v1];
                    if (f_ac_p >= 2) {
                        int rem = f_ac_p - cp;
                        lost_profit += (f_ac_p - 1) - (rem >= 2 ? rem - 1 : 0);
                    }
                    if (f_ac_m >= 2) {
                        int rem = f_ac_m - cm;
                        lost_profit += (f_ac_m - 1) - (rem >= 2 ? rem - 1 : 0);
                    }

                    int u2 = (b < c) ? b : c, v2 = (b < c) ? c : b;
                    int f_bc_p = freq_plus[u2 * MAX_VARS + v2];
                    int f_bc_m = freq_minus[u2 * MAX_VARS + v2];
                    int bp = (s == 1) ? cp : cm;
                    int bm = (s == 1) ? cm : cp;
                    if (f_bc_p >= 2) {
                        int rem = f_bc_p - bp;
                        lost_profit += (f_bc_p - 1) - (rem >= 2 ? rem - 1 : 0);
                    }
                    if (f_bc_m >= 2) {
                        int rem = f_bc_m - bm;
                        lost_profit += (f_bc_m - 1) - (rem >= 2 ? rem - 1 : 0);
                    }

                    c_plus[c] = 0;
                    c_minus[c] = 0;
                }

                double alpha = (strategy == 1) ? 0.35 : 0.20;
                double beta  = (strategy == 1) ? 0.08 : 0.15;
                double score = (double)(f - 1) + alpha * (double)(new_profit + max_new_pair) - beta * (double)lost_profit;
                if (score > best_score + 1e-9) {
                    best_score = score;
                    best_list[0] = ci;
                    n_best = 1;
                } else if (score >= best_score - 1e-9) {
                    best_list[n_best++] = ci;
                }
            }
            chosen = best_list[xorshift64(rng) % n_best];
        } else {
            /* Weighted random by (f - 1)^2 */
            int total_w = 0;
            for (int ci = 0; ci < n_cands; ci++) {
                int w = (cand_freq[ci] - 1) * (cand_freq[ci] - 1);
                total_w += w;
            }
            int pick = xorshift64(rng) % (total_w > 0 ? total_w : 1);
            for (int ci = 0; ci < n_cands; ci++) {
                int w = (cand_freq[ci] - 1) * (cand_freq[ci] - 1);
                if (pick < w) { chosen = ci; break; }
                pick -= w;
            }
        }

        int a = cands[chosen].a;
        int b = cands[chosen].b;
        int s = cands[chosen].s;
        int v_new = n_vars++;
        sol->fresh[actual_fresh].a = a;
        sol->fresh[actual_fresh].b = b;
        sol->fresh[actual_fresh].s = s;
        actual_fresh++;

        /* Apply replacement and incrementally update pair frequencies */
        for (int r = 0; r < G_R; r++) {
            int pa = -1, pb = -1;
            int L = rows[r].len;
            for (int i = 0; i < L; i++) {
                if (rows[r].t[i].idx == a) pa = i;
                else if (rows[r].t[i].idx == b) pb = i;
            }
            if (pa != -1 && pb != -1 && rows[r].t[pa].val * s == rows[r].t[pb].val) {
                int sa = rows[r].t[pa].val;
                int sb = rows[r].t[pb].val;
                /* Remove old pairs involving a and b in row r */
                if (sa == sb) freq_plus[a * MAX_VARS + b]--;
                else freq_minus[a * MAX_VARS + b]--;

                for (int i = 0; i < L; i++) {
                    if (i == pa || i == pb) continue;
                    int c = rows[r].t[i].idx;
                    int sc = rows[r].t[i].val;
                    int u1 = (a < c) ? a : c, v1 = (a < c) ? c : a;
                    if (sa == sc) freq_plus[u1 * MAX_VARS + v1]--;
                    else freq_minus[u1 * MAX_VARS + v1]--;

                    int u2 = (b < c) ? b : c, v2 = (b < c) ? c : b;
                    if (sb == sc) freq_plus[u2 * MAX_VARS + v2]--;
                    else freq_minus[u2 * MAX_VARS + v2]--;

                    /* Add new pair (c, v_new) */
                    if (sa == sc) freq_plus[c * MAX_VARS + v_new]++;
                    else freq_minus[c * MAX_VARS + v_new]++;
                }

                rows[r].t[pa].idx = v_new;
                rows[r].t[pa].val = sa;
                rows[r].t[pb] = rows[r].t[L - 1];
                rows[r].len = L - 1;
            }
        }
    }

    free(freq_plus);
    free(freq_minus);

    sol->n_fresh = actual_fresh;
    for (int r = 0; r < G_R; r++) {
        sol->out[r] = rows[r];
    }
    post_optimize(sol);
}

static void *worker_thread(void *arg) {
    uint64_t rng = (uint64_t)(uintptr_t)arg;
    Solution local;

    while (!G_stop) {
        if (elapsed_ms() >= G_time_limit_ms) {
            G_stop = 1;
            break;
        }

        pthread_mutex_lock(&G_lock);
        local = G_best_sol;
        pthread_mutex_unlock(&G_lock);

        int prefix_len = 0;
        uint64_t mode = xorshift64(&rng) % 100;
        if (local.n_fresh > 0 && mode < 70) {
            if (mode < 35) {
                /* Prefix LNS: keep random prefix of best solution */
                prefix_len = (int)(xorshift64(&rng) % (uint64_t)local.n_fresh);
            } else {
                /* Destroy-and-repair LNS: delete 1 to 3 random fresh vars from best solution */
                int del_pos = (int)(xorshift64(&rng) % (uint64_t)local.n_fresh);
                int del_cnt = 1 + (int)(xorshift64(&rng) % 3);
                int new_f = 0;
                for (int i = 0; i < local.n_fresh; i++) {
                    if (i >= del_pos && i < del_pos + del_cnt) continue;
                    local.fresh[new_f++] = local.fresh[i];
                }
                prefix_len = new_f;
            }
        } else {
            prefix_len = 0;
        }

        int strat = (int)(xorshift64(&rng) % 4);
        run_rollout(&local, prefix_len, strat, &rng);

        if (local.total_adds < G_best_sol.total_adds) {
            pthread_mutex_lock(&G_lock);
            if (local.total_adds < G_best_sol.total_adds && verify_solution(&local)) {
                G_best_sol = local;
            }
            pthread_mutex_unlock(&G_lock);
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "Usage: %s input_file output_file threads time_ms seed\n", argv[0]);
        return 2;
    }
    const char *in_path = argv[1];
    const char *out_path = argv[2];
    int n_threads = atoi(argv[3]);
    G_time_limit_ms = atoi(argv[4]);
    uint64_t seed = strtoull(argv[5], NULL, 10);
    if (seed == 0) seed = 0x9E3779B97F4A7C15ULL;

    FILE *fin = fopen(in_path, "r");
    if (!fin) { perror("fopen input"); return 1; }

    int f_init = 0;
    if (fscanf(fin, "%d %d %d", &G_R, &G_C, &f_init) != 3) {
        fprintf(stderr, "Invalid header\n");
        fclose(fin);
        return 1;
    }

    for (int c = 0; c < G_C; c++) {
        G_zobrist[c] = xorshift64(&seed);
    }

    for (int r = 0; r < G_R; r++) {
        for (int c = 0; c < G_C; c++) {
            if (fscanf(fin, "%d", &G_target[r][c]) != 1) {
                fprintf(stderr, "Invalid target entry\n");
                fclose(fin);
                return 1;
            }
        }
    }

    /* Initialize baseline trivial solution (0 fresh vars) */
    memset(&G_best_sol, 0, sizeof(Solution));
    for (int r = 0; r < G_R; r++) {
        G_best_sol.out[r].len = 0;
        for (int c = 0; c < G_C; c++) {
            if (G_target[r][c] != 0) {
                int k = G_best_sol.out[r].len++;
                G_best_sol.out[r].t[k].idx = c;
                G_best_sol.out[r].t[k].val = G_target[r][c];
            }
        }
    }
    G_best_sol.total_adds = compute_sol_adds(&G_best_sol);

    /* If warm-start fresh sequence + out rows provided, read and post-optimize it first! */
    if (f_init > 0) {
        memset(&G_init_sol, 0, sizeof(Solution));
        G_init_sol.n_fresh = f_init;
        for (int f = 0; f < f_init; f++) {
            if (fscanf(fin, "%d %d %d", &G_init_sol.fresh[f].a, &G_init_sol.fresh[f].b, &G_init_sol.fresh[f].s) != 3) {
                f_init = 0;
                break;
            }
        }
        if (f_init > 0) {
            int ok_out = 1;
            for (int r = 0; r < G_R; r++) {
                int len = 0;
                if (fscanf(fin, "%d", &len) != 1 || len < 1 || len > MAX_ROW_LEN) { ok_out = 0; break; }
                G_init_sol.out[r].len = len;
                for (int i = 0; i < len; i++) {
                    if (fscanf(fin, "%d %d", &G_init_sol.out[r].t[i].idx, &G_init_sol.out[r].t[i].val) != 2) {
                        ok_out = 0; break;
                    }
                }
                if (!ok_out) break;
            }
            if (ok_out && verify_solution(&G_init_sol)) {
                post_optimize(&G_init_sol);
                if (verify_solution(&G_init_sol) && G_init_sol.total_adds < G_best_sol.total_adds) {
                    G_best_sol = G_init_sol;
                    G_has_init = 1;
                }
            } else if (f_init > 0) {
                run_rollout(&G_init_sol, f_init, 1, &seed);
                if (verify_solution(&G_init_sol) && G_init_sol.total_adds < G_best_sol.total_adds) {
                    G_best_sol = G_init_sol;
                    G_has_init = 1;
                }
            }
        }
    }
    fclose(fin);

    clock_gettime(CLOCK_MONOTONIC, &G_start_time);

    if (G_time_limit_ms > 0) {
        if (n_threads < 1) n_threads = 1;
        if (n_threads > 16) n_threads = 16;
        pthread_t tids[16];
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setstacksize(&attr, 8 * 1024 * 1024);
        for (int t = 0; t < n_threads; t++) {
            uint64_t tseed = xorshift64(&seed) ^ ((uint64_t)(t + 1) * 0x517CC1B727220A95ULL);
            pthread_create(&tids[t], &attr, worker_thread, (void *)(uintptr_t)tseed);
        }
        for (int t = 0; t < n_threads; t++) {
            pthread_join(tids[t], NULL);
        }
        pthread_attr_destroy(&attr);
    }

    FILE *fout = fopen(out_path, "w");
    if (!fout) { perror("fopen output"); return 1; }
    fprintf(fout, "%d %d\n", G_best_sol.total_adds, G_best_sol.n_fresh);
    for (int f = 0; f < G_best_sol.n_fresh; f++) {
        fprintf(fout, "%d %d %d\n", G_best_sol.fresh[f].a, G_best_sol.fresh[f].b, G_best_sol.fresh[f].s);
    }
    for (int r = 0; r < G_R; r++) {
        fprintf(fout, "%d", G_best_sol.out[r].len);
        for (int i = 0; i < G_best_sol.out[r].len; i++) {
            fprintf(fout, " %d %d", G_best_sol.out[r].t[i].idx, G_best_sol.out[r].t[i].val);
        }
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;
}
