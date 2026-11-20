#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXN 32

typedef struct {
    int n;
    uint32_t adj[MAXN];
    uint8_t oppA[MAXN][MAXN];
    uint8_t oppB[MAXN][MAXN];
    int edge_u[3 * MAXN];
    int edge_v[3 * MAXN];
    int edge_pos[MAXN][MAXN];
    int num_edges;
} Tri;

static inline uint64_t splitmix64(uint64_t *state) {
    uint64_t z = (*state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

static inline double rand_u01(uint64_t *rng) {
    return (splitmix64(rng) >> 11) * (1.0 / 9007199254740992.0);
}

static void tri_set_opp(Tri *T, int a, int b, uint8_t x, uint8_t y) {
    T->oppA[a][b] = x; T->oppB[a][b] = y;
    T->oppA[b][a] = x; T->oppB[b][a] = y;
}

static void tri_replace_opp(Tri *T, int a, int b, uint8_t old_w, uint8_t new_w) {
    if (T->oppA[a][b] == old_w) T->oppA[a][b] = new_w;
    else T->oppB[a][b] = new_w;
    if (T->oppA[b][a] == old_w) T->oppA[b][a] = new_w;
    else T->oppB[b][a] = new_w;
}

static void tri_add_edge(Tri *T, int u, int v) {
    if (u > v) { int t = u; u = v; v = t; }
    T->adj[u] |= (1u << v);
    T->adj[v] |= (1u << u);
    int idx = T->num_edges++;
    T->edge_u[idx] = u;
    T->edge_v[idx] = v;
    T->edge_pos[u][v] = idx;
    T->edge_pos[v][u] = idx;
}

/* Initialize double-wheel / stacked triangulation and mix with 5000 random Wagner flips */
static void tri_init_random(Tri *T, int n, uint64_t *rng) {
    memset(T, 0, sizeof(*T));
    T->n = n;
    /* Start with K4 on {0,1,2,3} */
    int faces[2 * MAXN][3];
    int nf = 4;
    faces[0][0]=0; faces[0][1]=1; faces[0][2]=2;
    faces[1][0]=0; faces[1][1]=1; faces[1][2]=3;
    faces[2][0]=0; faces[2][1]=2; faces[2][2]=3;
    faces[3][0]=1; faces[3][1]=2; faces[3][2]=3;
    for (int w = 4; w < n; w++) {
        int f = (int)(splitmix64(rng) % (uint64_t)nf);
        int a = faces[f][0], b = faces[f][1], c = faces[f][2];
        faces[f][0] = a; faces[f][1] = b; faces[f][2] = w;
        faces[nf][0] = b; faces[nf][1] = c; faces[nf][2] = w; nf++;
        faces[nf][0] = c; faces[nf][1] = a; faces[nf][2] = w; nf++;
    }
    /* Build adj and oppA/oppB from face list */
    uint8_t cnt[MAXN][MAXN];
    memset(cnt, 0, sizeof(cnt));
    for (int f = 0; f < nf; f++) {
        int vs[3] = {faces[f][0], faces[f][1], faces[f][2]};
        for (int i = 0; i < 3; i++) {
            int a = vs[i], b = vs[(i+1)%3], c = vs[(i+2)%3];
            if (!(T->adj[a] & (1u << b))) {
                tri_add_edge(T, a, b);
            }
            int lo = a < b ? a : b, hi = a < b ? b : a;
            if (cnt[lo][hi] == 0) { T->oppA[lo][hi] = T->oppA[hi][lo] = (uint8_t)c; cnt[lo][hi] = 1; }
            else { T->oppB[lo][hi] = T->oppB[hi][lo] = (uint8_t)c; cnt[lo][hi] = 2; }
        }
    }
    /* Mix thoroughly with 5000 Wagner flips */
    for (int step = 0; step < 5000; step++) {
        int eidx = (int)(splitmix64(rng) % (uint64_t)T->num_edges);
        int u = T->edge_u[eidx], v = T->edge_v[eidx];
        int x = T->oppA[u][v], y = T->oppB[u][v];
        if (x == y || (T->adj[x] & (1u << y))) continue;
        /* Perform flip (u,v) -> (x,y) */
        T->adj[u] &= ~(1u << v); T->adj[v] &= ~(1u << u);
        T->adj[x] |= (1u << y);  T->adj[y] |= (1u << x);
        int rx = x < y ? x : y, ry = x < y ? y : x;
        T->edge_u[eidx] = rx; T->edge_v[eidx] = ry;
        T->edge_pos[rx][ry] = T->edge_pos[ry][rx] = eidx;
        tri_set_opp(T, rx, ry, (uint8_t)u, (uint8_t)v);
        tri_replace_opp(T, u, x, (uint8_t)v, (uint8_t)y);
        tri_replace_opp(T, v, x, (uint8_t)u, (uint8_t)y);
        tri_replace_opp(T, u, y, (uint8_t)v, (uint8_t)x);
        tri_replace_opp(T, v, y, (uint8_t)u, (uint8_t)x);
    }
}

static bool tri_verify_sphere(const Tri *T) {
    int n = T->n;
    if (T->num_edges != 3 * n - 6) return false;
    for (int i = 0; i < T->num_edges; i++) {
        int u = T->edge_u[i], v = T->edge_v[i];
        if (!(T->adj[u] & (1u << v))) return false;
        int x = T->oppA[u][v], y = T->oppB[u][v];
        if (x == y) return false;
        if (!(T->adj[u] & (1u << x)) || !(T->adj[v] & (1u << x))) return false;
        if (!(T->adj[u] & (1u << y)) || !(T->adj[v] & (1u << y))) return false;
    }
    /* Check every vertex link is a single cycle! */
    for (int v = 0; v < n; v++) {
        uint32_t nb = T->adj[v];
        int deg = __builtin_popcount(nb);
        if (deg < 3) return false;
        int start = __builtin_ctz(nb);
        int prev = -1, cur = start, steps = 0;
        do {
            int a = T->oppA[v][cur], b = T->oppB[v][cur];
            int nxt = (a == prev) ? b : a;
            if (prev == -1) nxt = a;
            prev = cur;
            cur = nxt;
            steps++;
            if (steps > deg + 1) return false;
        } while (cur != start);
        if (steps != deg) return false;
    }
    return true;
}

static inline void tri_do_flip(Tri *T, int eidx, int u, int v, int x, int y) {
    T->adj[u] &= ~(1u << v); T->adj[v] &= ~(1u << u);
    T->adj[x] |= (1u << y);  T->adj[y] |= (1u << x);
    int rx = x < y ? x : y, ry = x < y ? y : x;
    T->edge_u[eidx] = rx; T->edge_v[eidx] = ry;
    T->edge_pos[rx][ry] = T->edge_pos[ry][rx] = eidx;
    tri_set_opp(T, rx, ry, (uint8_t)u, (uint8_t)v);
    tri_replace_opp(T, u, x, (uint8_t)v, (uint8_t)y);
    tri_replace_opp(T, v, x, (uint8_t)u, (uint8_t)y);
    tri_replace_opp(T, u, y, (uint8_t)v, (uint8_t)x);
    tri_replace_opp(T, v, y, (uint8_t)u, (uint8_t)x);
}

/* Fast exact max clique bitmask Bron-Kerbosch (finds one max clique & size) */
typedef struct {
    int best_sz;
    uint32_t best_mask;
    const uint32_t *adj;
} CliqueCtx;

static void bk_max_clique(CliqueCtx *ctx, uint32_t R, uint32_t P) {
    int rsz = __builtin_popcount(R);
    int psz = __builtin_popcount(P);
    if (rsz + psz <= ctx->best_sz) return;
    if (P == 0) {
        ctx->best_sz = rsz;
        ctx->best_mask = R;
        return;
    }
    int pivot = __builtin_ctz(P);
    uint32_t cand = P & ~ctx->adj[pivot];
    while (cand) {
        int v = __builtin_ctz(cand);
        uint32_t vb = 1u << v;
        bk_max_clique(ctx, R | vb, P & ctx->adj[v]);
        P &= ~vb;
        if (rsz + __builtin_popcount(P) <= ctx->best_sz) return;
        cand &= cand - 1;
    }
}

/* Fast exact k-colorability on induced subgraph 'active_mask' using DSATUR + bitmask backtracking */
typedef struct {
    int n, k;
    const uint32_t *adj;
    uint32_t active_mask;
    uint8_t forbidden_cnt[MAXN][12];
    uint16_t avail_mask[MAXN];
    int colored_cnt;
    int target_cnt;
} ColCtx;

static bool color_dfs(ColCtx *C) {
    if (C->colored_cnt == C->target_cnt) return true;
    /* Pick uncolored vertex with minimum available colors (MRV / DSATUR) */
    uint32_t rem = C->active_mask;
    int best_v = -1, best_avail = 99;
    while (rem) {
        int v = __builtin_ctz(rem);
        int av = __builtin_popcount(C->avail_mask[v]);
        if (av == 0) return false;
        if (av < best_avail) {
            best_avail = av;
            best_v = v;
            if (av == 1) break;
        }
        rem &= rem - 1;
    }
    uint32_t vb = 1u << best_v;
    C->active_mask &= ~vb;
    C->colored_cnt++;
    uint16_t mask = C->avail_mask[best_v];
    uint32_t nb = C->adj[best_v] & C->active_mask;
    while (mask) {
        int c = __builtin_ctz(mask);
        uint16_t cb = (uint16_t)(1u << c);
        /* Propagate to uncolored neighbors */
        uint32_t m = nb;
        bool dead = false;
        while (m) {
            int u = __builtin_ctz(m);
            if (C->forbidden_cnt[u][c]++ == 0) {
                C->avail_mask[u] &= ~cb;
                if (C->avail_mask[u] == 0) dead = true;
            }
            m &= m - 1;
        }
        if (!dead && color_dfs(C)) return true;
        /* Undo */
        m = nb;
        while (m) {
            int u = __builtin_ctz(m);
            if (--C->forbidden_cnt[u][c] == 0) {
                C->avail_mask[u] |= cb;
            }
            m &= m - 1;
        }
        mask &= (uint16_t)(mask - 1);
    }
    C->colored_cnt--;
    C->active_mask |= vb;
    return false;
}

static bool is_k_colorable(int n, const uint32_t *adj, uint32_t sub_mask, int k) {
    /* Build induced adj on sub_mask */
    uint32_t sadj[MAXN];
    uint32_t m = sub_mask;
    while (m) {
        int v = __builtin_ctz(m);
        sadj[v] = adj[v] & sub_mask;
        m &= m - 1;
    }
    /* Iteratively peel vertices of degree < k! Huge speedup! */
    bool changed = true;
    while (changed) {
        changed = false;
        uint32_t cur = sub_mask;
        while (cur) {
            int v = __builtin_ctz(cur);
            if (__builtin_popcount(sadj[v]) < k) {
                uint32_t vb = 1u << v;
                sub_mask &= ~vb;
                uint32_t nb = sadj[v];
                while (nb) {
                    int u = __builtin_ctz(nb);
                    sadj[u] &= ~vb;
                    nb &= nb - 1;
                }
                changed = true;
            }
            cur &= cur - 1;
        }
    }
    int rem_n = __builtin_popcount(sub_mask);
    if (rem_n <= k) return true;

    /* Find max clique on remaining graph for instant lower bound + symmetry breaking */
    CliqueCtx cc = {0, 0, sadj};
    bk_max_clique(&cc, 0, sub_mask);
    if (cc.best_sz > k) return false;

    ColCtx ctx;
    memset(&ctx, 0, sizeof(ctx));
    ctx.n = n;
    ctx.k = k;
    ctx.adj = sadj;
    ctx.active_mask = sub_mask;
    ctx.target_cnt = rem_n;
    uint16_t all_c = (uint16_t)((1u << k) - 1);
    uint32_t cur = sub_mask;
    while (cur) {
        int v = __builtin_ctz(cur);
        ctx.avail_mask[v] = all_c;
        cur &= cur - 1;
    }
    /* Fix colors 0..best_sz-1 on cc.best_mask */
    uint32_t cm = cc.best_mask;
    int ci = 0;
    while (cm) {
        int v = __builtin_ctz(cm);
        uint32_t vb = 1u << v;
        ctx.active_mask &= ~vb;
        ctx.colored_cnt++;
        uint16_t cb = (uint16_t)(1u << ci);
        uint32_t nb = sadj[v] & ctx.active_mask;
        while (nb) {
            int u = __builtin_ctz(nb);
            if (ctx.forbidden_cnt[u][ci]++ == 0) {
                ctx.avail_mask[u] &= ~cb;
                if (ctx.avail_mask[u] == 0) return false;
            }
            nb &= nb - 1;
        }
        ci++;
        cm &= cm - 1;
    }
    return color_dfs(&ctx);
}

static bool complement_connected(int n, const uint32_t *G_adj, uint32_t mask_n) {
    uint32_t H_adj[MAXN];
    for (int v = 0; v < n; v++) H_adj[v] = (~G_adj[v]) & mask_n & ~(1u << v);
    uint32_t vis = 1u, q = 1u;
    while (q) {
        int v = __builtin_ctz(q);
        q &= q - 1;
        uint32_t add = H_adj[v] & ~vis;
        vis |= add;
        q |= add;
    }
    return vis == mask_n;
}

static void dump_candidate(const char *tag, int n, const Tri *T0, const Tri *T1, int chi_lb, int bad_v, int i3, int omega, FILE *out) {
    fprintf(out, "{\"tag\":\"%s\",\"n\":%d,\"chi_lb\":%d,\"bad_v\":%d,\"i3\":%d,\"omega\":%d,\"T0\":[",
            tag, n, chi_lb, bad_v, i3, omega);
    for (int i = 0; i < T0->num_edges; i++) {
        fprintf(out, "%s[%d,%d]", i ? "," : "", T0->edge_u[i], T0->edge_v[i]);
    }
    fprintf(out, "],\"T1\":[");
    for (int i = 0; i < T1->num_edges; i++) {
        fprintf(out, "%s[%d,%d]", i ? "," : "", T1->edge_u[i], T1->edge_v[i]);
    }
    fprintf(out, "]}\n");
    fflush(out);
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 19;
    uint64_t seed = (argc > 2) ? strtoull(argv[2], NULL, 10) : 12345ULL;
    double max_secs = (argc > 3) ? atof(argv[3]) : 5.0;
    const char *out_path = (argc > 4) ? argv[4] : "candidates.jsonl";
    int forbid_k8 = (argc > 5) ? atoi(argv[5]) : 0;

    FILE *out = fopen(out_path, "a");
    if (!out) { perror("fopen"); return 1; }

    uint32_t mask_n = (n == 32) ? 0xFFFFFFFFu : ((1u << n) - 1u);
    uint64_t rng = seed;
    struct timespec ts0, ts1;
    clock_gettime(CLOCK_MONOTONIC, &ts0);

    long long total_flips = 0, accepted = 0, chi9_hits = 0, span_crit_hits = 0;
    int global_min_i3 = 999999, global_min_badv = 999;

    while (1) {
        clock_gettime(CLOCK_MONOTONIC, &ts1);
        double el = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);
        if (el >= max_secs) break;

        Tri T0, T1;
        tri_init_random(&T0, n, &rng);
        tri_init_random(&T1, n, &rng);

        uint32_t G_adj[MAXN], H_adj[MAXN];
        int overlap = 0;
        for (int v = 0; v < n; v++) {
            G_adj[v] = T0.adj[v] | T1.adj[v];
            H_adj[v] = (~G_adj[v]) & mask_n & ~(1u << v);
            overlap += __builtin_popcount(T0.adj[v] & T1.adj[v]);
        }
        overlap /= 2;
        int i3 = 0;
        for (int u = 0; u < n; u++) {
            uint32_t m = H_adj[u] & (~((1u << (u + 1)) - 1u));
            while (m) {
                int v = __builtin_ctz(m);
                i3 += __builtin_popcount(H_adj[u] & H_adj[v] & (~((1u << (v + 1)) - 1u)));
                m &= m - 1;
            }
        }
        /* Also track universal vertices (isolated in H) to discourage joins! */
        int univ_cnt = 0; (void)univ_cnt;
        for (int v = 0; v < n; v++) if (H_adj[v] == 0) univ_cnt++;

        /* Phase 1: Fast SA on surrogate E = 4*i3 + 3*overlap + 12*univ_cnt */
        int max_steps = 400000;
        for (int step = 0; step < max_steps; step++) {
            if ((step & 16383) == 0) {
                clock_gettime(CLOCK_MONOTONIC, &ts1);
                if ((ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec) >= max_secs) break;
            }
            double temp = 4.5 * pow(0.08 / 4.5, (double)step / (double)max_steps);
            int which = (int)(splitmix64(&rng) & 1ULL);
            Tri *T = which ? &T1 : &T0;
            const Tri *Other = which ? &T0 : &T1;
            int eidx = (int)(splitmix64(&rng) % (uint64_t)T->num_edges);
            int u = T->edge_u[eidx], v = T->edge_v[eidx];
            int x = T->oppA[u][v], y = T->oppB[u][v];
            if (x == y || (T->adj[x] & (1u << y))) continue;
            total_flips++;

            /* Incremental delta of overlap, i3, univ_cnt */
            int d_ov = 0, d_i3 = 0, d_univ = 0;
            bool uv_in_other = (Other->adj[u] & (1u << v)) != 0;
            bool xy_in_other = (Other->adj[x] & (1u << y)) != 0;
            if (uv_in_other) d_ov--;
            if (xy_in_other) d_ov++;

            /* If !uv_in_other, (u,v) enters H! If !xy_in_other, (x,y) leaves H! */
            if (!uv_in_other && !xy_in_other) {
                /* First remove (x,y) from H, then add (u,v) to H */
                d_i3 -= __builtin_popcount(H_adj[x] & H_adj[y]);
                uint32_t hu = H_adj[u], hv = H_adj[v];
                if (u == x) hu &= ~(1u << y); else if (u == y) hu &= ~(1u << x);
                if (v == x) hv &= ~(1u << y); else if (v == y) hv &= ~(1u << x);
                d_i3 += __builtin_popcount(hu & hv);
            } else if (!uv_in_other) {
                d_i3 += __builtin_popcount(H_adj[u] & H_adj[v]);
            } else if (!xy_in_other) {
                d_i3 -= __builtin_popcount(H_adj[x] & H_adj[y]);
            }

            /* Check univ_cnt delta quickly */
            uint32_t new_hu = H_adj[u], new_hv = H_adj[v], new_hx = H_adj[x], new_hy = H_adj[y];
            if (!xy_in_other) {
                new_hx &= ~(1u << y); new_hy &= ~(1u << x);
                if (u == x) new_hu = new_hx; else if (u == y) new_hu = new_hy;
                if (v == x) new_hv = new_hx; else if (v == y) new_hv = new_hy;
            }
            if (!uv_in_other) {
                new_hu |= (1u << v); new_hv |= (1u << u);
                if (x == u) new_hx = new_hu; else if (x == v) new_hx = new_hv;
                if (y == u) new_hy = new_hu; else if (y == v) new_hy = new_hv;
            }
            int touched[4] = {u, v, x, y};
            uint32_t new_h[4] = {new_hu, new_hv, new_hx, new_hy};
            for (int ti = 0; ti < 4; ti++) {
                bool dup = false;
                for (int tj = 0; tj < ti; tj++) if (touched[ti] == touched[tj]) dup = true;
                if (dup) continue;
                int w = touched[ti];
                int old_z = (H_adj[w] == 0) ? 1 : 0;
                int new_z = (new_h[ti] == 0) ? 1 : 0;
                d_univ += (new_z - old_z);
            }

            int dE = 4 * d_i3 + 3 * d_ov + (forbid_k8 ? 18 : 8) * d_univ;
            if (dE <= 0 || rand_u01(&rng) < exp(-(double)dE / temp)) {
                tri_do_flip(T, eidx, u, v, x, y);
                overlap += d_ov;
                i3 += d_i3;
                univ_cnt += d_univ;
                if (!xy_in_other) {
                    G_adj[x] |= (1u << y); G_adj[y] |= (1u << x);
                    H_adj[x] &= ~(1u << y); H_adj[y] &= ~(1u << x);
                }
                if (!uv_in_other) {
                    G_adj[u] &= ~(1u << v); G_adj[v] &= ~(1u << u);
                    H_adj[u] |= (1u << v);  H_adj[v] |= (1u << u);
                }
                accepted++;

                if (i3 < global_min_i3) {
                    global_min_i3 = i3;
                    if (n == 18 && i3 == 0) {
                        dump_candidate("alpha2_n18", n, &T0, &T1, 9, -1, i3, 0, out);
                    }
                }

                /* Whenever dense & low-i3, check exact 8-colorability! */
                if (overlap <= 8 && i3 <= (n == 18 ? 16 : (n == 19 ? 24 : 34)) && ((step & 63) == 0 || dE < 0)) {
                    if (!is_k_colorable(n, G_adj, mask_n, 8)) {
                        chi9_hits++;
                        /* FIRST: Check if NOT 9-colorable (FULL MOONSHOT!) */
                        if (!is_k_colorable(n, G_adj, mask_n, 9)) {
                            printf("!!! MOONSHOT CHI>=10 FOUND ON n=%d !!!\n", n);
                            dump_candidate("MOONSHOT_CHI10", n, &T0, &T1, 10, 0, i3, 8, out);
                            fclose(out);
                            return 0;
                        }
                        /* SECOND: Enter Phase 2 (bad_v descent while preserving chi>=9!) */
                        int bad_v = 0;
                        for (int w = 0; w < n; w++) {
                            if (!is_k_colorable(n, G_adj, mask_n & ~(1u << w), 8)) bad_v++;
                        }
                        CliqueCtx cc0 = {0, 0, G_adj};
                        bk_max_clique(&cc0, 0, mask_n);
                        if (bad_v < global_min_badv) global_min_badv = bad_v;
                        if (bad_v == 0 && complement_connected(n, G_adj, mask_n)) {
                            span_crit_hits++;
                            dump_candidate("SPAN_CRIT9", n, &T0, &T1, 9, 0, i3, cc0.best_sz, out);
                        } else if (bad_v > 0) {
                            /* Dedicated 8000-step bad_v + omega descent inside the chi>=9 manifold! */
                            for (int bstep = 0; bstep < 8000 && bad_v > 0; bstep++) {
                                int bw = (int)(splitmix64(&rng) & 1ULL);
                                Tri *BT = bw ? &T1 : &T0;
                                const Tri *BO = bw ? &T0 : &T1;
                                int be = (int)(splitmix64(&rng) % (uint64_t)BT->num_edges);
                                int bu = BT->edge_u[be], bv = BT->edge_v[be];
                                int bx = BT->oppA[bu][bv], by = BT->oppB[bu][bv];
                                if (bx == by || (BT->adj[bx] & (1u << by))) continue;
                                bool buv_o = (BO->adj[bu] & (1u << bv)) != 0;
                                bool bxy_o = (BO->adj[bx] & (1u << by)) != 0;
                                if (buv_o && bxy_o) {
                                    /* Pure internal layer swap without changing G! */
                                    tri_do_flip(BT, be, bu, bv, bx, by);
                                    continue;
                                }
                                /* Apply tentatively to G_adj */
                                uint32_t old_gu = G_adj[bu], old_gv = G_adj[bv], old_gx = G_adj[bx], old_gy = G_adj[by];
                                if (!bxy_o) { G_adj[bx] |= (1u << by); G_adj[by] |= (1u << bx); }
                                if (!buv_o) { G_adj[bu] &= ~(1u << bv); G_adj[bv] &= ~(1u << bu); }

                                if (!is_k_colorable(n, G_adj, mask_n, 8)) {
                                    if (!is_k_colorable(n, G_adj, mask_n, 9)) {
                                        tri_do_flip(BT, be, bu, bv, bx, by);
                                        printf("!!! MOONSHOT CHI>=10 FOUND IN PHASE 2 ON n=%d !!!\n", n);
                                        dump_candidate("MOONSHOT_CHI10", n, &T0, &T1, 10, 0, -1, 8, out);
                                        fclose(out);
                                        return 0;
                                    }
                                    int nbad = 0;
                                    for (int w = 0; w < n; w++) {
                                        if (!is_k_colorable(n, G_adj, mask_n & ~(1u << w), 8)) nbad++;
                                    }
                                    CliqueCtx cc1 = {0, 0, G_adj};
                                    bk_max_clique(&cc1, 0, mask_n);
                                    int score_old = 10 * bad_v + (forbid_k8 && cc0.best_sz >= 8 ? 15 : 0);
                                    int score_new = 10 * nbad  + (forbid_k8 && cc1.best_sz >= 8 ? 15 : 0);
                                    if (score_new <= score_old || rand_u01(&rng) < 0.08) {
                                        tri_do_flip(BT, be, bu, bv, bx, by);
                                        bad_v = nbad;
                                        cc0 = cc1;
                                        if (bad_v < global_min_badv) global_min_badv = bad_v;
                                        if (bad_v == 0 && complement_connected(n, G_adj, mask_n)) {
                                            span_crit_hits++;
                                            dump_candidate("SPAN_CRIT9_P2", n, &T0, &T1, 9, 0, -1, cc1.best_sz, out);
                                        }
                                        continue;
                                    }
                                }
                                /* Revert G_adj */
                                G_adj[bu] = old_gu; G_adj[bv] = old_gv; G_adj[bx] = old_gx; G_adj[by] = old_gy;
                            }
                            /* Recompute H_adj, overlap, i3, univ_cnt cleanly after Phase 2 */
                            overlap = 0; univ_cnt = 0;
                            for (int v0 = 0; v0 < n; v0++) {
                                G_adj[v0] = T0.adj[v0] | T1.adj[v0];
                                H_adj[v0] = (~G_adj[v0]) & mask_n & ~(1u << v0);
                                overlap += __builtin_popcount(T0.adj[v0] & T1.adj[v0]);
                                if (H_adj[v0] == 0) univ_cnt++;
                            }
                            overlap /= 2;
                            i3 = 0;
                            for (int u0 = 0; u0 < n; u0++) {
                                uint32_t m0 = H_adj[u0] & (~((1u << (u0 + 1)) - 1u));
                                while (m0) {
                                    int v0 = __builtin_ctz(m0);
                                    i3 += __builtin_popcount(H_adj[u0] & H_adj[v0] & (~((1u << (v0 + 1)) - 1u)));
                                    m0 &= m0 - 1;
                                }
                            }
                        }
                    }
                }
            }
        }
        if (!tri_verify_sphere(&T0) || !tri_verify_sphere(&T1)) {
            fprintf(stderr, "FATAL: sphere invariant failed!\n");
            return 2;
        }
    }
    fclose(out);
    printf("DONE n=%d seed=%llu flips=%lld acc=%lld min_i3=%d chi9_hits=%lld min_badv=%d span_crit_hits=%lld\n",
           n, (unsigned long long)seed, total_flips, accepted, global_min_i3, chi9_hits, global_min_badv, span_crit_hits);
    return 0;
}
