/*
 * saw_bounds_2d.c
 *
 * Rigorous upper bounds and exact Collatz-Wielandt certificates for the
 * connective constant mu of 2D lattices:
 *   1. (4.8^2) (bathroom-tile) lattice  [best published upper bound: 1.82926, Jensen/Alm 2004]
 *   2. Kagome lattice                   [best published upper bound: 2.590301, Jensen/GPR 2004]
 *   3. Triangular lattice               [best published upper bound: 4.25152, Jensen/Alm 2004]
 *   4. Square lattice                   [Pönitz-Tittmann & Couronné 2022]
 *
 * Uses the finite-memory loop-avoiding walk automaton (Pönitz-Tittmann 2000)
 * with exact graph shortest-path distances, full lattice dihedral + translation
 * symmetry reduction, and small-bridge 4-cycle/3-cycle subset pruning where applicable.
 *
 * Certifies the upper bound via the Collatz-Wielandt theorem using an explicit
 * strictly positive integer vector V in Z_{>0}^t:
 *   mu <= max_{1 <= i <= t} ( (M V)_i / V_i )
 * evaluated in exact 128-bit integer arithmetic, and exports a standalone
 * certificate file for independent verification by verify_saw.py.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX_K 44
#define MAX_DEG 6
#define GRID_R 96
#define GRID_W (2 * GRID_R + 1)
#define GRID_N (GRID_W * GRID_W)

typedef enum {
    LAT_482 = 0,
    LAT_KAGOME = 1,
    LAT_TRIANGULAR = 2,
    LAT_SQUARE = 3
} lattice_t;

static lattice_t G_lat = LAT_482;
static int G_k = 20;
static int G_deg = 3;

/* Precomputed local graph on [-GRID_R..GRID_R]^2 */
static int G_valid_pt[GRID_N];
static int G_nbr_dx[GRID_N][MAX_DEG];
static int G_nbr_dy[GRID_N][MAX_DEG];
static int G_nbr_deg[GRID_N];
static int16_t *G_dist = NULL; /* G_dist[u * GRID_N + v] = exact graph distance */

static inline int pt_id(int x, int y) {
    if (x < -GRID_R || x > GRID_R || y < -GRID_R || y > GRID_R) return -1;
    return (x + GRID_R) * GRID_W + (y + GRID_R);
}

static int is_valid_vertex(lattice_t lat, int x, int y) {
    if (lat == LAT_482) {
        int xm = ((x % 3) + 3) % 3;
        int ym = ((y % 3) + 3) % 3;
        return ((xm == 0 && (ym == 1 || ym == 2)) || (ym == 0 && (xm == 1 || xm == 2)));
    } else if (lat == LAT_KAGOME) {
        return ((x & 1) | (y & 1)) != 0;
    } else {
        return 1;
    }
}

static void init_lattice_graph(lattice_t lat) {
    G_lat = lat;
    memset(G_valid_pt, 0, sizeof(G_valid_pt));
    memset(G_nbr_deg, 0, sizeof(G_nbr_deg));

    for (int x = -GRID_R; x <= GRID_R; x++) {
        for (int y = -GRID_R; y <= GRID_R; y++) {
            int u = pt_id(x, y);
            if (!is_valid_vertex(lat, x, y)) continue;
            G_valid_pt[u] = 1;
            int d = 0;
            if (lat == LAT_482) {
                int xm = ((x % 3) + 3) % 3;
                int ym = ((y % 3) + 3) % 3;
                if (xm == 1 && ym == 0) {
                    /* East vertex of cell: neighbors (-1, 1), (-1, -1), (+1, 0) */
                    G_nbr_dx[u][0] = -1; G_nbr_dy[u][0] = 1;
                    G_nbr_dx[u][1] = -1; G_nbr_dy[u][1] = -1;
                    G_nbr_dx[u][2] = 1;  G_nbr_dy[u][2] = 0;
                    d = 3;
                } else if (xm == 0 && ym == 1) {
                    /* North vertex: (1, -1), (-1, -1), (0, 1) */
                    G_nbr_dx[u][0] = 1;  G_nbr_dy[u][0] = -1;
                    G_nbr_dx[u][1] = -1; G_nbr_dy[u][1] = -1;
                    G_nbr_dx[u][2] = 0;  G_nbr_dy[u][2] = 1;
                    d = 3;
                } else if (xm == 2 && ym == 0) {
                    /* West vertex: (1, 1), (1, -1), (-1, 0) */
                    G_nbr_dx[u][0] = 1;  G_nbr_dy[u][0] = 1;
                    G_nbr_dx[u][1] = 1;  G_nbr_dy[u][1] = -1;
                    G_nbr_dx[u][2] = -1; G_nbr_dy[u][2] = 0;
                    d = 3;
                } else if (xm == 0 && ym == 2) {
                    /* South vertex: (1, 1), (-1, 1), (0, -1) */
                    G_nbr_dx[u][0] = 1;  G_nbr_dy[u][0] = 1;
                    G_nbr_dx[u][1] = -1; G_nbr_dy[u][1] = 1;
                    G_nbr_dx[u][2] = 0;  G_nbr_dy[u][2] = -1;
                    d = 3;
                }
            } else if (lat == LAT_KAGOME) {
                if (y & 1) {
                    G_nbr_dx[u][d] = 1;  G_nbr_dy[u][d++] = 0;
                    G_nbr_dx[u][d] = -1; G_nbr_dy[u][d++] = 0;
                }
                if (x & 1) {
                    G_nbr_dx[u][d] = 0;  G_nbr_dy[u][d++] = 1;
                    G_nbr_dx[u][d] = 0;  G_nbr_dy[u][d++] = -1;
                }
                if ((x + y) & 1) {
                    G_nbr_dx[u][d] = 1;  G_nbr_dy[u][d++] = -1;
                    G_nbr_dx[u][d] = -1; G_nbr_dy[u][d++] = 1;
                }
            } else if (lat == LAT_TRIANGULAR) {
                int dx[6] = {1, -1, 0, 0, 1, -1};
                int dy[6] = {0, 0, 1, -1, -1, 1};
                for (int i = 0; i < 6; i++) {
                    G_nbr_dx[u][i] = dx[i];
                    G_nbr_dy[u][i] = dy[i];
                }
                d = 6;
            } else if (lat == LAT_SQUARE) {
                int dx[4] = {1, -1, 0, 0};
                int dy[4] = {0, 0, 1, -1};
                for (int i = 0; i < 4; i++) {
                    G_nbr_dx[u][i] = dx[i];
                    G_nbr_dy[u][i] = dy[i];
                }
                d = 4;
            }
            G_nbr_deg[u] = d;
            G_deg = d;
        }
    }

    /* Compute exact shortest paths from all vertices in [-48..48]^2 via BFS */
    if (!G_dist) {
        G_dist = malloc((size_t)GRID_N * (size_t)GRID_N * sizeof(int16_t));
    }
    for (size_t i = 0; i < (size_t)GRID_N * GRID_N; i++) G_dist[i] = 9999;

    int *q = malloc(GRID_N * sizeof(int));
    for (int sx = -52; sx <= 52; sx++) {
        for (int sy = -52; sy <= 52; sy++) {
            int s = pt_id(sx, sy);
            if (s < 0 || !G_valid_pt[s]) continue;
            int16_t *drow = &G_dist[(size_t)s * GRID_N];
            drow[s] = 0;
            int head = 0, tail = 0;
            q[tail++] = s;
            while (head < tail) {
                int u = q[head++];
                int ux = (u / GRID_W) - GRID_R;
                int uy = (u % GRID_W) - GRID_R;
                int du = drow[u];
                if (du >= MAX_K + 4) continue;
                int deg = G_nbr_deg[u];
                for (int j = 0; j < deg; j++) {
                    int v = pt_id(ux + G_nbr_dx[u][j], uy + G_nbr_dy[u][j]);
                    if (v >= 0 && G_valid_pt[v] && drow[v] > du + 1) {
                        drow[v] = du + 1;
                        q[tail++] = v;
                    }
                }
            }
        }
    }
    free(q);
}

static inline int graph_dist(int x1, int y1, int x2, int y2) {
    if (G_lat == LAT_SQUARE) {
        return abs(x1 - x2) + abs(y1 - y2);
    } else if (G_lat == LAT_TRIANGULAR) {
        int dx = x2 - x1;
        int dy = y2 - y1;
        if ((dx >= 0 && dy >= 0) || (dx <= 0 && dy <= 0)) {
            return abs(dx + dy);
        } else {
            return (abs(dx) > abs(dy)) ? abs(dx) : abs(dy);
        }
    }
    int u = pt_id(x1, y1);
    int v = pt_id(x2, y2);
    return G_dist[(size_t)u * GRID_N + v];
}

/* Apply dihedral symmetry sym in 0..num_sym-1 to point (x, y) */
static inline void apply_sym(lattice_t lat, int sym, int x, int y, int *ox, int *oy) {
    if (lat == LAT_482 || lat == LAT_SQUARE) {
        /* D_4: 8 symmetries */
        int sx = (sym & 1) ? -x : x;
        int sy = (sym & 2) ? -y : y;
        if (sym & 4) { *ox = sy; *oy = sx; }
        else         { *ox = sx; *oy = sy; }
    } else {
        /* D_6: 12 symmetries preserving x^2 + xy + y^2 */
        int r = sym % 6;
        int f = sym / 6;
        if (f) { int tmp = x; x = y; y = tmp; }
        switch (r) {
            case 0: *ox = x;      *oy = y;      break;
            case 1: *ox = x + y;  *oy = -x;     break;
            case 2: *ox = y;      *oy = -x - y; break;
            case 3: *ox = -x;     *oy = -y;     break;
            case 4: *ox = -x - y; *oy = x;      break;
            case 5: *ox = -y;     *oy = x + y;  break;
        }
    }
}

/*
 * State representation:
 * A walk state is a sequence of L vertices (x[0], y[0]), ..., (x[L-1], y[L-1])
 * where B = (x[0], y[0]) is the oldest vertex and A = (x[L-1], y[L-1]) is the head.
 * Number of edges in the state is L - 1, and size_loop = (L - 1) + dist(A, B).
 *
 * Canonicalization under Aut(G):
 * We translate so the unit cell of A = (x[L-1], y[L-1]) is at the origin cell,
 * and apply every valid symmetry in D_4 (or D_6) that fixes the lattice,
 * picking the lexicographically smallest coordinate sequence from the head A
 * backwards to B: (x'[L-1], y'[L-1], x'[L-2], y'[L-2], ..., x'[0], y'[0]).
 * Because we compare from A backwards, two walks with the same last step are
 * always placed in the exact same orientation!
 */
struct walk_state {
    uint8_t L;
    int8_t x[MAX_K];
    int8_t y[MAX_K];
};

static void canonicalize_state(const struct walk_state *in, struct walk_state *out) {
    int L = in->L;
    int ax = in->x[L - 1];
    int ay = in->y[L - 1];

    /* Translate unit cell of A to (0, 0) */
    int tx = 0, ty = 0;
    if (G_lat == LAT_482) {
        /* Cell center of A is the nearest multiple of 3 */
        int rx = ((ax % 3) + 3) % 3;
        int ry = ((ay % 3) + 3) % 3;
        tx = ax - ((rx == 2) ? -1 : rx);
        ty = ay - ((ry == 2) ? -1 : ry);
    } else if (G_lat == LAT_KAGOME) {
        /* Translate by even integers so A lands in {(1,0), (0,1), (1,1)} */
        tx = ax - (ax & 1);
        ty = ay - (ay & 1);
    } else {
        tx = ax;
        ty = ay;
    }

    int nsym = (G_lat == LAT_482 || G_lat == LAT_SQUARE) ? 8 : 12;
    int best_set = 0;
    out->L = L;

    for (int s = 0; s < nsym; s++) {
        int8_t cx[MAX_K], cy[MAX_K];
        for (int i = 0; i < L; i++) {
            int px, py;
            apply_sym(G_lat, s, in->x[i] - tx, in->y[i] - ty, &px, &py);
            cx[i] = (int8_t)px;
            cy[i] = (int8_t)py;
        }
        /* For Kagome, translating by (0,0), (2,0), (0,2), or (2,2) if needed so A is in {(1,0),(0,1),(1,1)} */
        if (G_lat == LAT_KAGOME) {
            int ktx = cx[L - 1] - (cx[L - 1] & 1);
            int kty = cy[L - 1] - (cy[L - 1] & 1);
            for (int i = 0; i < L; i++) {
                cx[i] -= ktx;
                cy[i] -= kty;
            }
        }
        if (!best_set) {
            memcpy(out->x, cx, L);
            memcpy(out->y, cy, L);
            best_set = 1;
        } else {
            int better = 0;
            for (int i = L - 1; i >= 0; i--) {
                if (cx[i] != out->x[i]) { better = (cx[i] < out->x[i]); break; }
                if (cy[i] != out->y[i]) { better = (cy[i] < out->y[i]); break; }
            }
            if (better) {
                memcpy(out->x, cx, L);
                memcpy(out->y, cy, L);
            }
        }
    }
}

/* Hash table for canonical states */
static uint64_t hash_state(const struct walk_state *s) {
    uint64_t h = 1469598103934665603ULL;
    h ^= s->L;
    h *= 1099511628211ULL;
    for (int i = 0; i < s->L; i++) {
        h ^= (uint8_t)s->x[i];
        h *= 1099511628211ULL;
        h ^= (uint8_t)s->y[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static struct walk_state *G_states = NULL;
static int G_num_states = 0;
static int G_cap_states = 0;
static int *G_ht = NULL;
static int *G_ht_next = NULL;
static int G_ht_mask = 0;
static int (*G_trans)[MAX_DEG] = NULL;
static int *G_trans_cnt = NULL;

/* Candidate pool for multi-choice small-bridge subset reductions */
static int (*G_cand_off)[MAX_DEG] = NULL;
static uint8_t (*G_cand_cnt)[MAX_DEG] = NULL;
static int *G_cand_pool = NULL;
static size_t G_cand_pool_len = 0;
static size_t G_cand_pool_cap = 0;
static int G_use_bridges = 1;

static void init_state_table(int cap_pow2) {
    int ht_size = 1 << cap_pow2;
    G_ht_mask = ht_size - 1;
    G_ht = malloc(ht_size * sizeof(int));
    memset(G_ht, -1, ht_size * sizeof(int));
    G_cap_states = 2000000;
    G_states = malloc(G_cap_states * sizeof(struct walk_state));
    G_ht_next = malloc(G_cap_states * sizeof(int));
    G_trans = malloc(G_cap_states * sizeof(*G_trans));
    G_trans_cnt = malloc(G_cap_states * sizeof(int));
    G_cand_off = malloc(G_cap_states * sizeof(*G_cand_off));
    G_cand_cnt = malloc(G_cap_states * sizeof(*G_cand_cnt));
    G_cand_pool_cap = 8000000;
    G_cand_pool = malloc(G_cand_pool_cap * sizeof(int));
    G_cand_pool_len = 0;
    G_num_states = 0;
}

static void push_cand(int state_idx) {
    if (G_cand_pool_len >= G_cand_pool_cap) {
        G_cand_pool_cap *= 2;
        G_cand_pool = realloc(G_cand_pool, G_cand_pool_cap * sizeof(int));
    }
    G_cand_pool[G_cand_pool_len++] = state_idx;
}

static int lookup_state_only(const struct walk_state *s) {
    uint64_t h = hash_state(s);
    int bucket = (int)(h & (uint64_t)G_ht_mask);
    for (int idx = G_ht[bucket]; idx != -1; idx = G_ht_next[idx]) {
        if (G_states[idx].L == s->L &&
            memcmp(G_states[idx].x, s->x, s->L) == 0 &&
            memcmp(G_states[idx].y, s->y, s->L) == 0) {
            return idx;
        }
    }
    return -1;
}

static int find_or_insert_state(const struct walk_state *s) {
    int existing = lookup_state_only(s);
    if (existing != -1) return existing;
    if (G_num_states >= G_cap_states) {
        G_cap_states *= 2;
        G_states = realloc(G_states, G_cap_states * sizeof(struct walk_state));
        G_ht_next = realloc(G_ht_next, G_cap_states * sizeof(int));
        G_trans = realloc(G_trans, G_cap_states * sizeof(*G_trans));
        G_trans_cnt = realloc(G_trans_cnt, G_cap_states * sizeof(int));
        G_cand_off = realloc(G_cand_off, G_cap_states * sizeof(*G_cand_off));
        G_cand_cnt = realloc(G_cand_cnt, G_cap_states * sizeof(*G_cand_cnt));
    }
    uint64_t h = hash_state(s);
    int bucket = (int)(h & (uint64_t)G_ht_mask);
    int idx = G_num_states++;
    G_states[idx] = *s;
    G_ht_next[idx] = G_ht[bucket];
    G_ht[bucket] = idx;
    return idx;
}

/* Helper: suffix-prune a walk w of length wL until size_loop <= max_loop_k, then canonicalize */
static int suffix_prune_and_insert(const int8_t *wx, const int8_t *wy, int wL, int max_loop_k) {
    int nx = wx[wL - 1], ny = wy[wL - 1];
    int start = 0;
    while (start < wL - 2) {
        int edges = (wL - 1) - start;
        int dist_ab = graph_dist(wx[start], wy[start], nx, ny);
        if (edges + dist_ab <= max_loop_k) break;
        start++;
    }
    struct walk_state trimmed, can;
    trimmed.L = (uint8_t)(wL - start);
    for (int i = 0; i < trimmed.L; i++) {
        trimmed.x[i] = wx[start + i];
        trimmed.y[i] = wy[start + i];
    }
    canonicalize_state(&trimmed, &can);
    return find_or_insert_state(&can);
}

/* Recursively shortcut chords (a, b) with graph_dist == 1 while walk is still too big */
static void find_chord_candidates(const int8_t *wx, const int8_t *wy, int wL,
                                  int max_loop_k, int depth, int min_a,
                                  int *local_cands, int *n_cands) {
    for (int a = min_a; a <= wL - 4; a++) {
        for (int b = a + 2; b <= wL - 2; b++) {
            if (graph_dist(wx[a], wy[a], wx[b], wy[b]) == 1) {
                int8_t sx[MAX_K], sy[MAX_K];
                int sL = 0;
                for (int i = 0; i <= a; i++) { sx[sL] = wx[i]; sy[sL++] = wy[i]; }
                for (int i = b; i < wL; i++) { sx[sL] = wx[i]; sy[sL++] = wy[i]; }
                int cid = suffix_prune_and_insert(sx, sy, sL, max_loop_k);
                int dup = 0;
                for (int q = 0; q < *n_cands; q++) {
                    if (local_cands[q] == cid) { dup = 1; break; }
                }
                if (!dup && *n_cands < 64) {
                    local_cands[(*n_cands)++] = cid;
                }
                int rem_loop = (sL - 1) + graph_dist(sx[0], sy[0], sx[sL - 1], sy[sL - 1]);
                if (depth < 3 && rem_loop > max_loop_k) {
                    find_chord_candidates(sx, sy, sL, max_loop_k, depth + 1, a, local_cands, n_cands);
                }
            }
        }
    }
}

/*
 * Check if (sx, sy) is in the infinite component of G \ {(bx[0],by[0]), ..., (bx[bL-1],by[bL-1])}.
 * If the BFS queue empties before leaving [min_x-2, max_x+2] x [min_y-2, max_y+2],
 * then (sx, sy) is in a strictly FINITE connected component of G \ B!
 */
static int G_bfs_vis[GRID_N];
static int G_bfs_tag = 1;

static int can_reach_exterior(int sx, int sy, const int8_t *bx, const int8_t *by, int bL) {
    int min_x = sx, max_x = sx, min_y = sy, max_y = sy;
    G_bfs_tag++;
    if (G_bfs_tag > 1000000000) {
        memset(G_bfs_vis, 0, sizeof(G_bfs_vis));
        G_bfs_tag = 1;
    }
    int tag = G_bfs_tag;
    for (int i = 0; i < bL; i++) {
        int x = bx[i], y = by[i];
        if (x < min_x) min_x = x;
        if (x > max_x) max_x = x;
        if (y < min_y) min_y = y;
        if (y > max_y) max_y = y;
        int id = pt_id(x, y);
        if (id >= 0) G_bfs_vis[id] = tag;
    }
    min_x -= 2; max_x += 2;
    min_y -= 2; max_y += 2;

    int start_id = pt_id(sx, sy);
    if (start_id < 0) return 1;
    G_bfs_vis[start_id] = tag;

    int q[4096];
    int head = 0, tail = 0;
    q[tail++] = start_id;
    while (head < tail) {
        int u = q[head++];
        int ux = (u / GRID_W) - GRID_R;
        int uy = (u % GRID_W) - GRID_R;
        if (ux < min_x || ux > max_x || uy < min_y || uy > max_y) {
            return 1;
        }
        int deg = G_nbr_deg[u];
        for (int d = 0; d < deg; d++) {
            int vx = ux + G_nbr_dx[u][d];
            int vy = uy + G_nbr_dy[u][d];
            int v = pt_id(vx, vy);
            if (v >= 0 && G_valid_pt[v] && G_bfs_vis[v] != tag) {
                G_bfs_vis[v] = tag;
                if (tail < 4096) q[tail++] = v;
                else return 1;
            }
        }
    }
    return 0; /* Queue emptied: (sx, sy) is trapped in a finite component of G \ B! */
}

static void build_automaton(int max_loop_k) {
    G_k = max_loop_k;
    /* Seed with initial 1-edge state(s) */
    struct walk_state init_raw, init_can;
    init_raw.L = 2;
    if (G_lat == LAT_482) {
        /* Seed 1: square edge (1,0) -> (0,1) */
        init_raw.x[0] = 1; init_raw.y[0] = 0;
        init_raw.x[1] = 0; init_raw.y[1] = 1;
        canonicalize_state(&init_raw, &init_can);
        find_or_insert_state(&init_can);
        /* Seed 2: octagon edge (1,0) -> (2,0) */
        init_raw.x[0] = 1; init_raw.y[0] = 0;
        init_raw.x[1] = 2; init_raw.y[1] = 0;
        canonicalize_state(&init_raw, &init_can);
        find_or_insert_state(&init_can);
    } else if (G_lat == LAT_KAGOME) {
        init_raw.x[0] = 0; init_raw.y[0] = 1;
        init_raw.x[1] = 1; init_raw.y[1] = 1;
        canonicalize_state(&init_raw, &init_can);
        find_or_insert_state(&init_can);
    } else {
        init_raw.x[0] = -1; init_raw.y[0] = 0;
        init_raw.x[1] = 0;  init_raw.y[1] = 0;
        canonicalize_state(&init_raw, &init_can);
        find_or_insert_state(&init_can);
    }

    for (int cur = 0; cur < G_num_states; cur++) {
        struct walk_state st = G_states[cur];
        int L = st.L;
        int ax = st.x[L - 1];
        int ay = st.y[L - 1];
        int u = pt_id(ax, ay);
        int deg = G_nbr_deg[u];
        int nchild = 0;

        for (int d = 0; d < deg; d++) {
            int nx = ax + G_nbr_dx[u][d];
            int ny = ay + G_nbr_dy[u][d];

            /* Check if (nx, ny) is already visited in st (including immediate backtrack L-2) */
            int visited = 0;
            for (int i = 0; i < L; i++) {
                if (st.x[i] == nx && st.y[i] == ny) { visited = 1; break; }
            }
            if (visited) continue;

            int8_t ex[MAX_K], ey[MAX_K];
            for (int i = 0; i < L; i++) {
                ex[i] = st.x[i];
                ey[i] = st.y[i];
            }
            ex[L] = (int8_t)nx;
            ey[L] = (int8_t)ny;
            int newL = L + 1;

            /* Finite-component pocket check for A'=(nx,ny) and B=(ex[0],ey[0]) when G_use_bridges >= 2 */
            if (G_use_bridges >= 2) {
                /* 1. Can A'=(nx,ny) reach the exterior avoiding st[0..L-1]? */
                if (!can_reach_exterior(nx, ny, st.x, st.y, L)) continue;
                /* 2. Can B=(ex[0],ey[0]) reach the exterior avoiding ex[1..newL-1]? */
                if (!can_reach_exterior(ex[0], ey[0], ex + 1, ey + 1, newL - 1)) continue;
            }

            int local_cands[64];
            int n_cands = 0;

            /* Candidate 0: standard suffix pruning */
            int c0 = suffix_prune_and_insert(ex, ey, newL, max_loop_k);
            local_cands[n_cands++] = c0;

            /* If ext was too big and bridge shortcutting is enabled, find chord shortcuts */
            int full_loop = (newL - 1) + graph_dist(ex[0], ey[0], nx, ny);
            if (G_use_bridges && full_loop > max_loop_k) {
                find_chord_candidates(ex, ey, newL, max_loop_k, 1, 0, local_cands, &n_cands);
            }

            G_cand_off[cur][nchild] = (int)G_cand_pool_len;
            G_cand_cnt[cur][nchild] = (uint8_t)n_cands;
            for (int q = 0; q < n_cands; q++) push_cand(local_cands[q]);
            G_trans[cur][nchild] = local_cands[0];
            nchild++;
        }
        G_trans_cnt[cur] = nchild;
    }

    /* Second pass: check if intermediate suffixes while erasing old vertices are already states */
    if (G_use_bridges) {
        for (int cur = 0; cur < G_num_states; cur++) {
            struct walk_state st = G_states[cur];
            int L = st.L;
            int ax = st.x[L - 1];
            int ay = st.y[L - 1];
            int u = pt_id(ax, ay);
            int deg = G_nbr_deg[u];
            int dir_idx = 0;
            for (int d = 0; d < deg; d++) {
                int nx = ax + G_nbr_dx[u][d];
                int ny = ay + G_nbr_dy[u][d];
                int visited = 0;
                for (int i = 0; i < L; i++) {
                    if (st.x[i] == nx && st.y[i] == ny) { visited = 1; break; }
                }
                if (visited) continue;

                int8_t ex[MAX_K], ey[MAX_K];
                for (int i = 0; i < L; i++) { ex[i] = st.x[i]; ey[i] = st.y[i]; }
                ex[L] = (int8_t)nx; ey[L] = (int8_t)ny;
                int newL = L + 1;
                int full_loop = (newL - 1) + graph_dist(ex[0], ey[0], nx, ny);
                if (full_loop > max_loop_k) {
                    /* Check if any intermediate suffix start=0..newL-3 is already in G_states */
                    for (int start = 0; start < newL - 2; start++) {
                        int edges = (newL - 1) - start;
                        int dist_ab = graph_dist(ex[start], ey[start], nx, ny);
                        if (edges + dist_ab <= max_loop_k) break;
                        struct walk_state trimmed, can;
                        trimmed.L = (uint8_t)(newL - start);
                        for (int i = 0; i < trimmed.L; i++) {
                            trimmed.x[i] = ex[start + i];
                            trimmed.y[i] = ey[start + i];
                        }
                        canonicalize_state(&trimmed, &can);
                        int existing = lookup_state_only(&can);
                        if (existing != -1) {
                            /* Append to candidate list if not already present */
                            int off = G_cand_off[cur][dir_idx];
                            int cnt = G_cand_cnt[cur][dir_idx];
                            int dup = 0;
                            for (int q = 0; q < cnt; q++) {
                                if (G_cand_pool[off + q] == existing) { dup = 1; break; }
                            }
                            if (!dup && cnt < 32) {
                                int new_off = (int)G_cand_pool_len;
                                for (int q = 0; q < cnt; q++) push_cand(G_cand_pool[off + q]);
                                push_cand(existing);
                                G_cand_off[cur][dir_idx] = new_off;
                                G_cand_cnt[cur][dir_idx] = (uint8_t)(cnt + 1);
                            }
                        }
                    }
                }
                dir_idx++;
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s {482|kagome|triangular|square} {k} [cert_out_file] [use_bridges=1]\n", argv[0]);
        return 0;
    }
    lattice_t lat = LAT_482;
    if (strcmp(argv[1], "482") == 0) lat = LAT_482;
    else if (strcmp(argv[1], "kagome") == 0) lat = LAT_KAGOME;
    else if (strcmp(argv[1], "triangular") == 0) lat = LAT_TRIANGULAR;
    else if (strcmp(argv[1], "square") == 0) lat = LAT_SQUARE;
    else {
        fprintf(stderr, "Unknown lattice: %s\n", argv[1]);
        return 1;
    }
    int k = atoi(argv[2]);
    const char *cert_file = (argc >= 4 && strcmp(argv[3], "-") != 0) ? argv[3] : NULL;
    if (argc >= 5) G_use_bridges = atoi(argv[4]);

    struct timespec ts0, ts1;
    clock_gettime(CLOCK_MONOTONIC, &ts0);

    init_lattice_graph(lat);
    init_state_table(22);
    build_automaton(k);

    clock_gettime(CLOCK_MONOTONIC, &ts1);
    double t_build = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);

    int N = G_num_states;
    double *v = malloc(N * sizeof(double));
    double *w = malloc(N * sizeof(double));
    for (int i = 0; i < N; i++) v[i] = 1.0;

    double ub = 10.0, lb = 0.0, prev_ub = 20.0;
    int iter = 0;
    for (iter = 1; iter <= 2000; iter++) {
        double max_w = 0.0;
        double max_ratio = 0.0;
        double min_ratio = 1e9;
        for (int i = 0; i < N; i++) {
            double sum = 0.0;
            int cnt = G_trans_cnt[i];
            for (int j = 0; j < cnt; j++) {
                int ccnt = G_cand_cnt[i][j];
                int coff = G_cand_off[i][j];
                int best_child = G_cand_pool[coff];
                double best_val = v[best_child];
                for (int c = 1; c < ccnt; c++) {
                    int ch = G_cand_pool[coff + c];
                    if (v[ch] < best_val) {
                        best_val = v[ch];
                        best_child = ch;
                    }
                }
                G_trans[i][j] = best_child;
                sum += best_val;
            }
            w[i] = sum;
            if (sum > max_w) max_w = sum;
            if (v[i] > 1e-5) {
                double r = sum / v[i];
                if (r > max_ratio) max_ratio = r;
                if (cnt > 0 && r < min_ratio) min_ratio = r;
            }
        }
        prev_ub = ub;
        ub = max_ratio;
        lb = min_ratio;
        /* Resolvent floor 1e-7 ensures transient/dead-end states also satisfy (Mv)_i <= ub * v_i */
        for (int i = 0; i < N; i++) {
            double target = w[i] / max_w;
            if (target < 1e-7) target = 1e-7;
            v[i] = 0.85 * target + 0.15 * v[i];
        }
        if ((ub - lb < 1e-12 || fabs(ub - prev_ub) < 1e-13) && iter >= 120) break;
    }

    /* Final resolvent polish on the locked optimal policy G_trans[i][j] */
    double lambda_target = ub * (1.0 + 1e-11);
    for (int sweep = 0; sweep < 80; sweep++) {
        int changed = 0;
        for (int i = 0; i < N; i++) {
            double sum = 0.0;
            int cnt = G_trans_cnt[i];
            for (int j = 0; j < cnt; j++) {
                int ccnt = G_cand_cnt[i][j];
                int coff = G_cand_off[i][j];
                int best_child = G_cand_pool[coff];
                double best_val = v[best_child];
                for (int c = 1; c < ccnt; c++) {
                    int ch = G_cand_pool[coff + c];
                    if (v[ch] < best_val) {
                        best_val = v[ch];
                        best_child = ch;
                    }
                }
                G_trans[i][j] = best_child;
                sum += best_val;
            }
            double req = sum / lambda_target;
            if (req > v[i]) {
                v[i] = req * (1.0 + 1e-13);
                changed = 1;
            }
        }
        if (!changed) break;
    }

    /* Quantize v[i] to strictly positive 64-bit integers V[i] in [1000, 10^13] */
    uint64_t *V = malloc(N * sizeof(uint64_t));
    const double SCALE = 1e13;
    for (int i = 0; i < N; i++) {
        double val = v[i] * SCALE;
        if (val < 1000.0) V[i] = 1000;
        else V[i] = (uint64_t)llround(val);
    }

    /* Integer Collatz-Wielandt relaxation for target rational bound target_num / target_den */
    uint64_t target_den = 1000000000000ULL;
    uint64_t target_num = (uint64_t)llround(ub * (double)target_den) + 100ULL;
    for (int sweep = 0; sweep < 100; sweep++) {
        int changed = 0;
        for (int i = 0; i < N; i++) {
            uint64_t num = 0;
            int cnt = G_trans_cnt[i];
            for (int j = 0; j < cnt; j++) {
                int ccnt = G_cand_cnt[i][j];
                int coff = G_cand_off[i][j];
                int best_child = G_cand_pool[coff];
                uint64_t best_val = V[best_child];
                for (int c = 1; c < ccnt; c++) {
                    int ch = G_cand_pool[coff + c];
                    if (V[ch] < best_val) {
                        best_val = V[ch];
                        best_child = ch;
                    }
                }
                G_trans[i][j] = best_child;
                num += best_val;
            }
            if ((__int128)num * (__int128)target_den > (__int128)target_num * (__int128)V[i]) {
                V[i] = (uint64_t)(((__int128)num * (__int128)target_den) / (__int128)target_num) + 1ULL;
                changed = 1;
            }
        }
        if (!changed) break;
    }

    uint64_t best_num = 0, best_den = 1;
    int worst_state = 0;
    for (int i = 0; i < N; i++) {
        uint64_t num = 0;
        int cnt = G_trans_cnt[i];
        for (int j = 0; j < cnt; j++) {
            num += V[G_trans[i][j]];
        }
        uint64_t den = V[i];
        /* Compare num / den > best_num / best_den in 128-bit integer arithmetic */
        if ((__int128)num * (__int128)best_den > (__int128)best_num * (__int128)den) {
            best_num = num;
            best_den = den;
            worst_state = i;
        }
    }

    double exact_cw_ub = (double)best_num / (double)best_den;
    clock_gettime(CLOCK_MONOTONIC, &ts1);
    double t_total = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);

    printf("Lattice=%s k=%d states=%d build=%.3fs total=%.3fs iters=%d\n",
           argv[1], k, N, t_build, t_total, iter);
    printf("Float Collatz-Wielandt interval: [%.12f, %.12f]\n", lb, ub);
    printf("EXACT Integer CW Certificate: max_i (MV)_i / V_i = %llu / %llu = %.12f (at state %d)\n",
           (unsigned long long)best_num, (unsigned long long)best_den, exact_cw_ub, worst_state);

    if (cert_file) {
        FILE *fp = fopen(cert_file, "w");
        if (fp) {
            fprintf(fp, "# Rigorous Collatz-Wielandt Upper Bound Certificate\n");
            fprintf(fp, "lattice %s\n", argv[1]);
            fprintf(fp, "max_loop_k %d\n", k);
            fprintf(fp, "num_states %d\n", N);
            fprintf(fp, "cw_num %llu\n", (unsigned long long)best_num);
            fprintf(fp, "cw_den %llu\n", (unsigned long long)best_den);
            fprintf(fp, "cw_upper_bound %.15f\n", exact_cw_ub);
            for (int i = 0; i < N; i++) {
                fprintf(fp, "S %d %llu %d", i, (unsigned long long)V[i], (int)G_states[i].L);
                for (int j = 0; j < G_states[i].L; j++) {
                    fprintf(fp, " %d,%d", (int)G_states[i].x[j], (int)G_states[i].y[j]);
                }
                fprintf(fp, " | %d", G_trans_cnt[i]);
                for (int j = 0; j < G_trans_cnt[i]; j++) {
                    fprintf(fp, " %d", G_trans[i][j]);
                }
                fprintf(fp, "\n");
            }
            fclose(fp);
            printf("Saved certificate to %s\n", cert_file);
        }
    }

    free(V);
    free(v);
    free(w);
    return 0;
}
