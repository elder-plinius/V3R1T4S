/*
 * domino_mitm_a.c — Engine 1 (Attempt 1)
 * Exact 3D Grid Perfect Matching (Domino Tiling) Counter via:
 *   1. Fermionic Particle-Hole Constant-Weight Combinadic Indexing (O(1) 2-table rank + Gosper unrank)
 *   2. 3-Piece Meet-in-the-Middle across middle diagonal plane s_mid = (Lx+Ly+Lz-3)/2
 *      with 2-vertex outer pinning on V_mid to cap frontier width W <= 30 (< 1.9 GiB RAM)
 *   3. Lock-free Pull-DP parallelized across <= 4 pthreads
 *   4. Multi-prime CRT over Prime Set A (10 distinct 31-bit primes near 2^31 - 1)
 *
 * Vertex Order A within each diagonal plane s = x + y + z:
 *   (z - x, z, x, y) on V_L and V_mid; mirrored (-z + x, -z, -x, -y) from opposite corner on V_R.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#define MAX_V 512
#define MAX_W 33
#define MAX_THREADS 4

static const uint32_t PRIMES_A[10] = {
    2147483647U, /* 2^31 - 1 */
    2147483629U,
    2147483587U,
    2147483579U,
    2147483563U,
    2147483549U,
    2147483543U,
    2147483497U,
    2147483489U,
    2147483477U
};

static uint64_t binom_tbl[MAX_W + 1][MAX_W + 1];
static uint8_t  popcnt16[65536];
static uint32_t rank_lo[65536];
static uint32_t rank_hi[18][65536];

static void init_combinadics(void) {
    memset(binom_tbl, 0, sizeof(binom_tbl));
    for (int n = 0; n <= MAX_W; n++) {
        binom_tbl[n][0] = 1;
        for (int k = 1; k <= n; k++) {
            binom_tbl[n][k] = binom_tbl[n - 1][k - 1] + binom_tbl[n - 1][k];
        }
    }
    for (uint32_t m = 0; m < 65536; m++) {
        popcnt16[m] = (uint8_t)__builtin_popcount(m);
        uint32_t r = 0;
        int idx = 1;
        uint32_t tmp = m;
        while (tmp) {
            int b = __builtin_ctz(tmp);
            r += (uint32_t)binom_tbl[b][idx++];
            tmp &= tmp - 1;
        }
        rank_lo[m] = r;
    }
    for (int clo = 0; clo <= 17; clo++) {
        for (uint32_t m = 0; m < 65536; m++) {
            uint32_t r = 0;
            int idx = clo + 1;
            uint32_t tmp = m;
            while (tmp) {
                int b = __builtin_ctz(tmp);
                if (16 + b <= MAX_W && idx <= MAX_W) {
                    r += (uint32_t)binom_tbl[16 + b][idx];
                }
                idx++;
                tmp &= tmp - 1;
            }
            rank_hi[clo][m] = r;
        }
    }
}

static inline size_t comb_rank32(uint32_t B) {
    uint32_t lo = B & 0xFFFFU;
    uint32_t hi = B >> 16;
    return (size_t)rank_lo[lo] + (size_t)rank_hi[popcnt16[lo]][hi];
}

static uint64_t comb_unrank(int W, int K, size_t idx) {
    if (K == 0) return 0ULL;
    uint64_t mask = 0ULL;
    int k = K;
    for (int b = W - 1; b >= 0 && k > 0; b--) {
        uint64_t c = binom_tbl[b][k];
        if (idx >= c) {
            idx -= c;
            mask |= (1ULL << b);
            k--;
        }
    }
    return mask;
}

typedef struct {
    int W_old, K_old;
    int W_new, K_new;
    uint64_t even_old;
    uint64_t even_new;
    int enters;          /* 1 if v enters F_new (at bit W_new - 1), else 0 */
    int force_mode;      /* 0 = normal, 1 = force v NOT matched to F_old (and not entering), 2 = force v MATCHED to F_old (and not entering) */
    int n_leave;         /* leaving vertices in F_old (all are neighbors of v in grid/bridge) */
    int leave_pos[6];    /* sorted ascending positions in F_old */
    int leave_is_nb[6];  /* 1 if leaving vertex is adjacent to v */
    int n_surv_nb;       /* surviving past neighbors of v */
    int surv_nb_newpos[6]; /* their bit positions in F_new */
    int surv_nb_oldpos[6]; /* their bit positions in F_old */
} StepSpec;

/* Expand a (W_old - n_leave)-bit mask on surviving vertices back into W_old-bit mask by inserting 0s at leave_pos[0..n_leave-1] */
static inline uint64_t expand_surviving(uint64_t surv_mask, int n_leave, const int *leave_pos) {
    uint64_t x = surv_mask;
    for (int i = 0; i < n_leave; i++) {
        int d = leave_pos[i];
        uint64_t lo_mask = (d == 0) ? 0ULL : ((1ULL << d) - 1ULL);
        x = (x & lo_mask) | ((x & ~lo_mask) << 1);
    }
    return x;
}

typedef struct {
    const uint32_t *cur;
    uint32_t *nxt;
    const StepSpec *sp;
    uint32_t mod;
    size_t idx_start;
    size_t idx_end;
} WorkerArgs;

static void *pull_step_worker(void *arg) {
    WorkerArgs *wa = (WorkerArgs *)arg;
    const uint32_t *cur = wa->cur;
    uint32_t *nxt = wa->nxt;
    const StepSpec *sp = wa->sp;
    const uint32_t mod = wa->mod;
    size_t idx = wa->idx_start;
    const size_t idx_end = wa->idx_end;
    if (idx >= idx_end) return NULL;

    const int W_new = sp->W_new;
    const int K_new = sp->K_new;
    const uint64_t even_old = sp->even_old;
    const uint64_t even_new = sp->even_new;
    const int enters = sp->enters;
    const int force_mode = sp->force_mode;
    const int n_leave = sp->n_leave;
    const int n_surv_nb = sp->n_surv_nb;
    const uint64_t surv_mask_new = enters ? ((W_new == 1) ? 0ULL : ((1ULL << (W_new - 1)) - 1ULL))
                                          : ((W_new == 0) ? 0ULL : ((1ULL << W_new) - 1ULL));

    /* Check if any non-neighbor leaves F_old: in a valid graph step, every leaving vertex had v as its last neighbor,
        EXCEPT in force_mode or isolated vertices; if a non-neighbor leaves, its unmatched bit in F_old MUST be 0,
       which expand_surviving already sets to 0! */
    uint64_t leave_nb_bits[6];
    int n_leave_nb = 0;
    for (int i = 0; i < n_leave; i++) {
        if (sp->leave_is_nb[i]) {
            leave_nb_bits[n_leave_nb++] = (1ULL << sp->leave_pos[i]);
        }
    }
    uint64_t surv_nb_new_bits[6], surv_nb_old_bits[6];
    for (int i = 0; i < n_surv_nb; i++) {
        surv_nb_new_bits[i] = (1ULL << sp->surv_nb_newpos[i]);
        surv_nb_old_bits[i] = (1ULL << sp->surv_nb_oldpos[i]);
    }

    uint64_t B_new = comb_unrank(W_new, K_new, idx);
    for (; idx < idx_end; idx++) {
        uint64_t U_new = B_new ^ even_new;
        uint64_t U_surv = U_new & surv_mask_new;
        uint64_t U_old_base = expand_surviving(U_surv, n_leave, sp->leave_pos);
        uint64_t acc = 0;

        if (force_mode == 1) {
            /* v forced NOT to match F_old, and does not enter F_new */
            uint32_t B_old = (uint32_t)(U_old_base ^ even_old);
            acc = cur[comb_rank32(B_old)];
        } else if (force_mode == 2) {
            /* v forced to match one unmatched neighbor in F_old, and does not enter F_new */
            for (int i = 0; i < n_leave_nb; i++) {
                uint32_t B_old = (uint32_t)((U_old_base | leave_nb_bits[i]) ^ even_old);
                acc += cur[comb_rank32(B_old)];
            }
            for (int i = 0; i < n_surv_nb; i++) {
                if ((U_new & surv_nb_new_bits[i]) == 0) {
                    uint32_t B_old = (uint32_t)((U_old_base | surv_nb_old_bits[i]) ^ even_old);
                    acc += cur[comb_rank32(B_old)];
                }
            }
            if (acc >= mod) { acc -= mod; if (acc >= mod) { acc -= mod; if (acc >= mod) acc %= mod; } }
        } else {
            /* Normal transition */
            if (enters && ((U_new >> (W_new - 1)) & 1ULL)) {
                /* v was left unmatched at this step */
                uint32_t B_old = (uint32_t)(U_old_base ^ even_old);
                acc = cur[comb_rank32(B_old)];
            } else {
                /* v was matched to a past neighbor in F_old */
                for (int i = 0; i < n_leave_nb; i++) {
                    uint32_t B_old = (uint32_t)((U_old_base | leave_nb_bits[i]) ^ even_old);
                    acc += cur[comb_rank32(B_old)];
                }
                for (int i = 0; i < n_surv_nb; i++) {
                    if ((U_new & surv_nb_new_bits[i]) == 0) {
                        uint32_t B_old = (uint32_t)((U_old_base | surv_nb_old_bits[i]) ^ even_old);
                        acc += cur[comb_rank32(B_old)];
                    }
                }
                if (acc >= mod) { acc -= mod; if (acc >= mod) { acc -= mod; if (acc >= mod) acc %= mod; } }
            }
        }
        nxt[idx] = (uint32_t)acc;

        /* Advance B_new via Gosper's hack */
        if (K_new > 0 && idx + 1 < idx_end) {
            int tz = __builtin_ctzll(B_new);
            uint64_t r = B_new + (1ULL << tz);
            B_new = (((r ^ B_new) >> (tz + 2))) | r;
        }
    }
    return NULL;
}

static uint32_t *run_step_parallel(const uint32_t *cur, const StepSpec *sp, uint32_t mod, int n_threads) {
    if (sp->K_new < 0 || sp->K_new > sp->W_new || sp->K_old < 0 || sp->K_old > sp->W_old) {
        return NULL;
    }
    size_t sz_new = (size_t)binom_tbl[sp->W_new][sp->K_new];
    uint32_t *nxt = (uint32_t *)malloc(sz_new * sizeof(uint32_t));
    if (!nxt) {
        fprintf(stderr, "FATAL: malloc failed for %zu uint32_t\n", sz_new);
        exit(1);
    }
    if (sz_new < 65536 || n_threads <= 1) {
        WorkerArgs wa = { cur, nxt, sp, mod, 0, sz_new };
        pull_step_worker(&wa);
    } else {
        pthread_t th[MAX_THREADS];
        WorkerArgs wa[MAX_THREADS];
        int T = (n_threads > MAX_THREADS) ? MAX_THREADS : n_threads;
        size_t chunk = (sz_new + T - 1) / T;
        int active = 0;
        for (int t = 0; t < T; t++) {
            size_t s = (size_t)t * chunk;
            size_t e = s + chunk;
            if (e > sz_new) e = sz_new;
            if (s >= e) break;
            wa[t].cur = cur;
            wa[t].nxt = nxt;
            wa[t].sp = sp;
            wa[t].mod = mod;
            wa[t].idx_start = s;
            wa[t].idx_end = e;
            pthread_create(&th[t], NULL, pull_step_worker, &wa[t]);
            active++;
        }
        for (int t = 0; t < active; t++) {
            pthread_join(th[t], NULL);
        }
    }
    return nxt;
}

typedef struct {
    int x, y, z;
    int parity; /* (x+y+z) & 1 */
    int deg;
    int nbs[6];
} Vertex;

typedef struct {
    int Lx, Ly, Lz, N;
    Vertex V[MAX_V];
} Grid;

static int grid_idx(int Lx, int Ly, int Lz, int x, int y, int z) {
    (void)Lx;
    return (x * Ly + y) * Lz + z;
}

static void build_grid(Grid *g, int Lx, int Ly, int Lz) {
    g->Lx = Lx; g->Ly = Ly; g->Lz = Lz;
    g->N = Lx * Ly * Lz;
    const int dx[6] = {-1, 1, 0, 0, 0, 0};
    const int dy[6] = {0, 0, -1, 1, 0, 0};
    const int dz[6] = {0, 0, 0, 0, -1, 1};
    for (int x = 0; x < Lx; x++) {
        for (int y = 0; y < Ly; y++) {
            for (int z = 0; z < Lz; z++) {
                int id = grid_idx(Lx, Ly, Lz, x, y, z);
                g->V[id].x = x; g->V[id].y = y; g->V[id].z = z;
                g->V[id].parity = (x + y + z) & 1;
                int d = 0;
                for (int k = 0; k < 6; k++) {
                    int nx = x + dx[k], ny = y + dy[k], nz = z + dz[k];
                    if (nx >= 0 && nx < Lx && ny >= 0 && ny < Ly && nz >= 0 && nz < Lz) {
                        g->V[id].nbs[d++] = grid_idx(Lx, Ly, Lz, nx, ny, nz);
                    }
                }
                g->V[id].deg = d;
            }
        }
    }
}

static int is_adj(const Grid *g, int u, int v) {
    for (int i = 0; i < g->V[u].deg; i++) {
        if (g->V[u].nbs[i] == v) return 1;
    }
    return 0;
}

/* Sweep a sequence seq[0..len-1] inside induced subgraph on (seq union external_future_set) */
static uint32_t *sweep_half(
    const Grid *g,
    const int *seq, int len,
    const uint8_t *in_ext_future,
    uint32_t mod, int n_threads,
    int *out_F, int *out_W, int *out_K
) {
    uint8_t processed[MAX_V];
    memset(processed, 0, sizeof(processed));
    uint8_t in_seq[MAX_V];
    memset(in_seq, 0, sizeof(in_seq));
    for (int i = 0; i < len; i++) in_seq[seq[i]] = 1;

    int F_cur[MAX_W], W_cur = 0, K_cur = 0;
    uint64_t even_cur = 0ULL;
    int odd_pref = 0, even_pref = 0;

    uint32_t *cur = (uint32_t *)malloc(sizeof(uint32_t));
    cur[0] = 1U % mod;

    for (int t = 0; t < len; t++) {
        int v = seq[t];
        processed[v] = 1;
        if (g->V[v].parity) odd_pref++; else even_pref++;

        /* Determine F_new */
        int F_new[MAX_W], W_new = 0;
        StepSpec sp;
        memset(&sp, 0, sizeof(sp));
        sp.W_old = W_cur;
        sp.K_old = K_cur;
        sp.even_old = even_cur;
        sp.force_mode = 0;

        for (int j = 0; j < W_cur; j++) {
            int u = F_cur[j];
            int has_fut = 0;
            for (int k = 0; k < g->V[u].deg; k++) {
                int w = g->V[u].nbs[k];
                if ((in_seq[w] && !processed[w]) || in_ext_future[w]) {
                    has_fut = 1;
                    break;
                }
            }
            if (has_fut) {
                int new_pos = W_new;
                F_new[W_new++] = u;
                if (is_adj(g, u, v)) {
                    sp.surv_nb_oldpos[sp.n_surv_nb] = j;
                    sp.surv_nb_newpos[sp.n_surv_nb] = new_pos;
                    sp.n_surv_nb++;
                }
            } else {
                sp.leave_pos[sp.n_leave] = j;
                sp.leave_is_nb[sp.n_leave] = is_adj(g, u, v);
                sp.n_leave++;
            }
        }

        int v_has_fut = 0;
        for (int k = 0; k < g->V[v].deg; k++) {
            int w = g->V[v].nbs[k];
            if ((in_seq[w] && !processed[w]) || in_ext_future[w]) {
                v_has_fut = 1;
                break;
            }
        }
        sp.enters = v_has_fut;
        if (v_has_fut) {
            F_new[W_new++] = v;
        }
        if (W_new > MAX_W) {
            fprintf(stderr, "FATAL: W_new=%d exceeds MAX_W=%d\n", W_new, MAX_W);
            exit(1);
        }

        int w_even = 0;
        uint64_t even_new = 0ULL;
        for (int j = 0; j < W_new; j++) {
            if (g->V[F_new[j]].parity == 0) {
                w_even++;
                even_new |= (1ULL << j);
            }
        }
        int K_new = (odd_pref - even_pref) + w_even;
        sp.W_new = W_new;
        sp.K_new = K_new;
        sp.even_new = even_new;

        uint32_t *nxt = run_step_parallel(cur, &sp, mod, n_threads);
        free(cur);
        if (!nxt) {
            *out_W = -1;
            return NULL;
        }
        cur = nxt;
        memcpy(F_cur, F_new, W_new * sizeof(int));
        W_cur = W_new;
        K_cur = K_new;
        even_cur = even_new;
    }

    memcpy(out_F, F_cur, W_cur * sizeof(int));
    *out_W = W_cur;
    *out_K = K_cur;
    return cur;
}

/* Bridge vec_B (on frontier F_B[0..W_B-1] with K_B) across middle independent set M_seq[0..M_len-1],
   with first n_pin vertices pinned according to pin_mask (bit i = 1 => w_i matches into B; bit i = 0 => w_i does not match into B). */
static uint32_t *bridge_middle(
    const Grid *g,
    const uint32_t *vec_B, const int *F_B, int W_B, int K_B,
    const int *M_seq, int M_len,
    int n_pin, int pin_mask,
    uint32_t mod, int n_threads,
    int *out_W, int *out_K
) {
    int F_cur[MAX_W];
    memcpy(F_cur, F_B, W_B * sizeof(int));
    int W_cur = W_B, K_cur = K_B;
    uint64_t even_cur = 0ULL;
    for (int j = 0; j < W_cur; j++) {
        if (g->V[F_cur[j]].parity == 0) even_cur |= (1ULL << j);
    }

    /* Reconstruct delta = K_cur - w_even_cur */
    int w_even_init = __builtin_popcountll(even_cur);
    int delta = K_cur - w_even_init; /* (#odd - #even) in processed set */

    size_t init_sz = (size_t)binom_tbl[W_cur][K_cur];
    uint32_t *cur = (uint32_t *)malloc(init_sz * sizeof(uint32_t));
    memcpy(cur, vec_B, init_sz * sizeof(uint32_t));

    uint8_t in_B[MAX_V];
    memset(in_B, 0, sizeof(in_B));
    for (int j = 0; j < W_B; j++) in_B[F_B[j]] = 1;

    uint8_t m_done[MAX_V];
    memset(m_done, 0, sizeof(m_done));

    for (int i = 0; i < M_len; i++) {
        int v = M_seq[i];
        m_done[v] = 1;
        int is_pinned = (i < n_pin);
        int pin_match = is_pinned ? ((pin_mask >> i) & 1) : 0;

        /* Update delta:
           - If unpinned: v enters processed set (parity p_v), so delta += (p_v ? +1 : -1).
           - If pinned and pin_match == 1: v is matched with a vertex of opposite parity in B, AND v does NOT enter F_new!
             Including v in processed set changes (#odd - #even) by (p_v ? +1 : -1).
           - If pinned and pin_match == 0: v is DELETED (matched to the other half, never touches B), so processed set does NOT include v! */
        if (!is_pinned || pin_match == 1) {
            delta += (g->V[v].parity ? 1 : -1);
        }

        int F_new[MAX_W], W_new = 0;
        StepSpec sp;
        memset(&sp, 0, sizeof(sp));
        sp.W_old = W_cur;
        sp.K_old = K_cur;
        sp.even_old = even_cur;

        for (int j = 0; j < W_cur; j++) {
            int u = F_cur[j];
            int keep = 0;
            if (!in_B[u]) {
                /* u is an already-added unpinned vertex of M_seq: keep until end of M_seq! */
                keep = 1;
            } else {
                /* u in B: keep iff u has an unprocessed neighbor in M_seq[i+1 .. M_len-1] */
                for (int k = 0; k < g->V[u].deg; k++) {
                    int w = g->V[u].nbs[k];
                    /* Check if w is in M_seq and not yet m_done */
                    for (int r = i + 1; r < M_len; r++) {
                        if (M_seq[r] == w) { keep = 1; break; }
                    }
                    if (keep) break;
                }
            }
            if (keep) {
                int new_pos = W_new;
                F_new[W_new++] = u;
                if (in_B[u] && is_adj(g, u, v)) {
                    sp.surv_nb_oldpos[sp.n_surv_nb] = j;
                    sp.surv_nb_newpos[sp.n_surv_nb] = new_pos;
                    sp.n_surv_nb++;
                }
            } else {
                sp.leave_pos[sp.n_leave] = j;
                sp.leave_is_nb[sp.n_leave] = (in_B[u] && is_adj(g, u, v)) ? 1 : 0;
                sp.n_leave++;
            }
        }

        if (is_pinned) {
            sp.enters = 0;
            sp.force_mode = pin_match ? 2 : 1;
        } else {
            sp.enters = 1;
            sp.force_mode = 0;
            F_new[W_new++] = v;
        }

        if (W_new > MAX_W) {
            fprintf(stderr, "FATAL bridge: W_new=%d > MAX_W\n", W_new);
            exit(1);
        }

        int w_even = 0;
        uint64_t even_new = 0ULL;
        for (int j = 0; j < W_new; j++) {
            if (g->V[F_new[j]].parity == 0) {
                w_even++;
                even_new |= (1ULL << j);
            }
        }
        int K_new = delta + w_even;
        sp.W_new = W_new;
        sp.K_new = K_new;
        sp.even_new = even_new;

        uint32_t *nxt = run_step_parallel(cur, &sp, mod, n_threads);
        free(cur);
        if (!nxt) {
            *out_W = -1;
            return NULL;
        }
        cur = nxt;
        memcpy(F_cur, F_new, W_new * sizeof(int));
        W_cur = W_new;
        K_cur = K_new;
        even_cur = even_new;
    }

    *out_W = W_cur;
    *out_K = K_cur;
    return cur;
}

static Grid *g_sort_ctx = NULL;
static int cmp_order_a_fwd(const void *pa, const void *pb) {
    const Vertex *a = &g_sort_ctx->V[*(const int *)pa];
    const Vertex *b = &g_sort_ctx->V[*(const int *)pb];
    int sa = a->x + a->y + a->z, sb = b->x + b->y + b->z;
    if (sa != sb) return sa - sb;
    int da = a->z - a->x, db = b->z - b->x;
    if (da != db) return da - db;
    if (a->z != b->z) return a->z - b->z;
    if (a->x != b->x) return a->x - b->x;
    return a->y - b->y;
}

static int cmp_order_a_bwd(const void *pa, const void *pb) {
    const Vertex *a = &g_sort_ctx->V[*(const int *)pa];
    const Vertex *b = &g_sort_ctx->V[*(const int *)pb];
    int sa = a->x + a->y + a->z, sb = b->x + b->y + b->z;
    if (sa != sb) return sb - sa;
    int da = (g_sort_ctx->Lz - 1 - a->z) - (g_sort_ctx->Lx - 1 - a->x);
    int db = (g_sort_ctx->Lz - 1 - b->z) - (g_sort_ctx->Lx - 1 - b->x);
    if (da != db) return da - db;
    if (a->z != b->z) return b->z - a->z;
    if (a->x != b->x) return b->x - a->x;
    return b->y - a->y;
}

static uint32_t solve_grid_mod_mitm(int Lx, int Ly, int Lz, uint32_t mod, int n_threads) {
    long long N = (long long)Lx * Ly * Lz;
    if (N == 0) return 1U % mod;
    if (N & 1LL) return 0U;

    Grid g;
    build_grid(&g, Lx, Ly, Lz);
    g_sort_ctx = &g;

    int S_max = (Lx - 1) + (Ly - 1) + (Lz - 1);
    int s_mid = S_max / 2;

    int seq_L[MAX_V], len_L = 0;
    int seq_M[MAX_V], len_M = 0;
    int seq_R[MAX_V], len_R = 0;
    uint8_t ext_for_L[MAX_V], ext_for_R[MAX_V];
    memset(ext_for_L, 0, sizeof(ext_for_L));
    memset(ext_for_R, 0, sizeof(ext_for_R));

    for (int v = 0; v < g.N; v++) {
        int s = g.V[v].x + g.V[v].y + g.V[v].z;
        if (s < s_mid) {
            seq_L[len_L++] = v;
        } else if (s == s_mid) {
            seq_M[len_M++] = v;
            ext_for_L[v] = 1;
            ext_for_R[v] = 1;
        } else {
            seq_R[len_R++] = v;
        }
    }

    qsort(seq_L, len_L, sizeof(int), cmp_order_a_fwd);
    qsort(seq_M, len_M, sizeof(int), cmp_order_a_fwd);
    qsort(seq_R, len_R, sizeof(int), cmp_order_a_bwd);

    int F_L[MAX_W], W_L = 0, K_L = 0;
    uint32_t *vec_L = sweep_half(&g, seq_L, len_L, ext_for_L, mod, n_threads, F_L, &W_L, &K_L);
    if (!vec_L) return 0U;

    int F_R[MAX_W], W_R = 0, K_R = 0;
    uint32_t *vec_R = sweep_half(&g, seq_R, len_R, ext_for_R, mod, n_threads, F_R, &W_R, &K_R);
    if (!vec_R) { free(vec_L); return 0U; }

    int n_pin = (len_M >= 27) ? 2 : 0;
    int n_cases = 1 << n_pin;
    uint64_t total = 0ULL;

    for (int pm = 0; pm < n_cases; pm++) {
        int comp_pm = ((1 << n_pin) - 1) ^ pm;
        int outW_L = 0, outK_L = 0;
        uint32_t *out_L = bridge_middle(&g, vec_L, F_L, W_L, K_L, seq_M, len_M, n_pin, pm, mod, n_threads, &outW_L, &outK_L);
        if (!out_L) continue;

        int outW_R = 0, outK_R = 0;
        uint32_t *out_R = bridge_middle(&g, vec_R, F_R, W_R, K_R, seq_M, len_M, n_pin, comp_pm, mod, n_threads, &outW_R, &outK_R);
        if (!out_R) { free(out_L); continue; }

        if (outW_L == outW_R && outK_L + outK_R == outW_L) {
            size_t sz = (size_t)binom_tbl[outW_L][outK_L];
            uint64_t sub = 0ULL;
            for (size_t i = 0; i < sz; i++) {
                sub = (sub + (uint64_t)out_L[i] * (uint64_t)out_R[sz - 1 - i]) % mod;
            }
            total = (total + sub) % mod;
        }
        free(out_L);
        free(out_R);
    }

    free(vec_L);
    free(vec_R);
    return (uint32_t)total;
}

/* Big-integer CRT reconstruction in decimal for up to 10 31-bit primes (product < 10^100) */
typedef struct {
    uint32_t d[40]; /* base 10^9 little-endian */
    int len;
} BigUInt;

static void big_zero(BigUInt *a) { memset(a, 0, sizeof(*a)); a->len = 1; }
static void big_from_u64(BigUInt *a, uint64_t v) {
    big_zero(a);
    int i = 0;
    while (v > 0) { a->d[i++] = (uint32_t)(v % 1000000000ULL); v /= 1000000000ULL; }
    a->len = (i == 0) ? 1 : i;
}
static uint32_t big_mod_u32(const BigUInt *a, uint32_t m) {
    uint64_t r = 0;
    for (int i = a->len - 1; i >= 0; i--) {
        r = (r * 1000000000ULL + a->d[i]) % m;
    }
    return (uint32_t)r;
}
static void big_mul_add_u32(BigUInt *a, uint32_t mul, uint32_t add) {
    uint64_t carry = add;
    for (int i = 0; i < a->len; i++) {
        uint64_t cur = (uint64_t)a->d[i] * mul + carry;
        a->d[i] = (uint32_t)(cur % 1000000000ULL);
        carry = cur / 1000000000ULL;
    }
    while (carry > 0) {
        a->d[a->len++] = (uint32_t)(carry % 1000000000ULL);
        carry /= 1000000000ULL;
    }
}
static void big_to_str(const BigUInt *a, char *buf) {
    int pos = sprintf(buf, "%u", a->d[a->len - 1]);
    for (int i = a->len - 2; i >= 0; i--) {
        pos += sprintf(buf + pos, "%09u", a->d[i]);
    }
}

static uint32_t mod_pow(uint64_t a, uint64_t e, uint32_t m) {
    uint64_t r = 1; a %= m;
    while (e > 0) {
        if (e & 1) r = (r * a) % m;
        a = (a * a) % m;
        e >>= 1;
    }
    return (uint32_t)r;
}

static void crt_reconstruct(int k, const uint32_t *primes, const uint32_t *rem, BigUInt *out) {
    /* Garner's algorithm */
    BigUInt X, M;
    big_from_u64(&X, rem[0]);
    big_from_u64(&M, primes[0]);
    for (int i = 1; i < k; i++) {
        uint32_t p = primes[i];
        uint32_t x_mod_p = big_mod_u32(&X, p);
        uint32_t m_mod_p = big_mod_u32(&M, p);
        uint32_t diff = (rem[i] >= x_mod_p) ? (rem[i] - x_mod_p) : (rem[i] + p - x_mod_p);
        uint32_t inv = mod_pow(m_mod_p, p - 2, p);
        uint32_t t = (uint32_t)(((uint64_t)diff * inv) % p);
        /* X = X + M * t */
        uint64_t carry = 0;
        int max_l = (X.len > M.len + 2) ? X.len : (M.len + 2);
        for (int j = 0; j < max_l; j++) {
            uint64_t xv = (j < X.len) ? X.d[j] : 0;
            uint64_t mv = (j < M.len) ? M.d[j] : 0;
            uint64_t cur = xv + mv * (uint64_t)t + carry;
            X.d[j] = (uint32_t)(cur % 1000000000ULL);
            carry = cur / 1000000000ULL;
        }
        X.len = max_l;
        while (X.len > 1 && X.d[X.len - 1] == 0) X.len--;
        big_mul_add_u32(&M, p, 0);
    }
    *out = X;
}

static void solve_exact_str(int Lx, int Ly, int Lz, int n_primes, int n_threads, char *out_dec, uint32_t *out_rems) {
    uint32_t rems[10];
    for (int i = 0; i < n_primes; i++) {
        rems[i] = solve_grid_mod_mitm(Lx, Ly, Lz, PRIMES_A[i], n_threads);
        if (out_rems) out_rems[i] = rems[i];
    }
    BigUInt ans;
    crt_reconstruct(n_primes, PRIMES_A, rems, &ans);
    big_to_str(&ans, out_dec);
}

static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(int argc, char **argv) {
    init_combinadics();
    int mode_7 = (argc > 1 && strcmp(argv[1], "--solve-667") == 0);
    int n_threads = 4;

    printf("=== Engine 1 (Meet-in-the-Middle Diagonal Combinadic DP, Order A) ===\n");
    double t0 = now_sec();

    struct { int x, y, z, np; const char *name, *expected; } tests[] = {
        {2, 2, 2, 2, "A028446(1) = P_2xP_2xP_2", "9"},
        {4, 4, 4, 2, "A028446(2) = P_4xP_4xP_4", "5051532105"},
        {4, 4, 1, 2, "A028454(1) = P_4xP_4xP_1", "36"},
        {4, 4, 2, 2, "A028454(2) = P_4xP_4xP_2", "32000"},
        {4, 4, 3, 2, "A028454(3) = P_4xP_4xP_3", "10885344"},
        {4, 4, 5, 2, "A028454(5) = P_4xP_4xP_5", "2132137503232"},
        {4, 4, 6, 2, "A028454(6) = P_4xP_4xP_6", "932814464901633"},
        {6, 4, 4, 2, "A028454(6) = P_6xP_4xP_4", "932814464901633"},
        {4, 4, 7, 3, "A028454(7) = P_4xP_4xP_7", "403325499406267520"},
        {6, 6, 0, 1, "A049507(0) = P_6xP_6xP_0", "1"},
        {6, 6, 1, 1, "A049507(1) = P_6xP_6xP_1", "6728"},
        {6, 6, 2, 2, "A049507(2) = P_6xP_6xP_2", "53786626921"},
        {6, 6, 3, 2, "A049507(3) = P_6xP_6xP_3", "57248060375968384"},
        {6, 6, 4, 3, "A049507(4) = P_6xP_6xP_4", "123115692449982216049513"},
        {6, 6, 5, 4, "A049507(5) = P_6xP_6xP_5", "216388579168758145017797108072"},
        {6, 6, 6, 5, "A028446(3) = A049507(6) = P_6xP_6xP_6", "417898687046465734392674187695263185"},
    };
    int n_tests = (int)(sizeof(tests) / sizeof(tests[0]));
    char buf[256];
    for (int i = 0; i < n_tests; i++) {
        double ts = now_sec();
        solve_exact_str(tests[i].x, tests[i].y, tests[i].z, tests[i].np, n_threads, buf, NULL);
        double te = now_sec();
        int ok = (strcmp(buf, tests[i].expected) == 0);
        printf("[%s] %-38s = %s (%.3fs)\n", ok ? "OK" : "FAIL", tests[i].name, buf, te - ts);
        if (!ok) {
            fprintf(stderr, "MISMATCH: expected %s, got %s\n", tests[i].expected, buf);
            return 1;
        }
    }
    printf("All %d calibration checks PASSED in %.3fs.\n", n_tests, now_sec() - t0);

    if (mode_7) {
        printf("\n--- Computing A049507(7) = M(P_6 x P_6 x P_7) across 10 primes in Prime Set A ---\n");
        uint32_t rems[10];
        for (int i = 0; i < 10; i++) {
            double ts = now_sec();
            rems[i] = solve_grid_mod_mitm(6, 6, 7, PRIMES_A[i], n_threads);
            double te = now_sec();
            printf("  Prime A[%d] = %u -> residue = %u (%.3fs)\n", i, PRIMES_A[i], rems[i], te - ts);
            fflush(stdout);
        }
        /* Reconstruct from first 6 primes (already > Bregman bound 2^168), then verify primes 6..9 AND full 10-prime CRT! */
        BigUInt ans6, ans10;
        char s6[256], s10[256];
        crt_reconstruct(6, PRIMES_A, rems, &ans6);
        crt_reconstruct(10, PRIMES_A, rems, &ans10);
        big_to_str(&ans6, s6);
        big_to_str(&ans10, s10);
        printf("CRT(6 primes)  = %s\n", s6);
        printf("CRT(10 primes) = %s\n", s10);
        if (strcmp(s6, s10) != 0) {
            fprintf(stderr, "FATAL: 6-prime and 10-prime CRT disagree!\n");
            return 1;
        }
        for (int i = 0; i < 10; i++) {
            uint32_t chk = big_mod_u32(&ans10, PRIMES_A[i]);
            if (chk != rems[i]) {
                fprintf(stderr, "FATAL: residue check failed at i=%d\n", i);
                return 1;
            }
        }
        printf("OVERDETERMINED 4-PRIME CHECK: PASS (primes 7..10 match 6-prime CRT identically!)\n");
        printf("RESULT A049507(7) = %s\n", s10);
    }
    return 0;
}
