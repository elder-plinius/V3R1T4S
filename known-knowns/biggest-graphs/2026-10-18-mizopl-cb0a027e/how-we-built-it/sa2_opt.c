/* sa2_opt.c -- Native C bit-parallel BFS evaluator & Simulated Annealing optimizer
 * for degree-diameter vertex insertion and rewiring.
 *
 * Build:  cc -O3 -o sa2_opt sa2_opt.c -lm
 * Usage:  ./sa2_opt SEED_GRAPH DELTA D K_INSERT OUT_PREFIX [ITERS] [RESTARTS] [SEED]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXN 4096
#define MAXW 64
#define MAXDEG 32
#define MAXP 250000

static uint64_t rng_state = 88172645463325252ULL;
static inline uint64_t xrand() {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return rng_state = x;
}
static inline int rand_int(int n) {
    return (int)(xrand() % (uint64_t)n);
}
static inline double urand() {
    return (xrand() >> 11) * (1.0 / 9007199254740992.0);
}

static int N0, N, Delta, D, W;
static int orig_adj[MAXN][MAXDEG], orig_deg[MAXN];
static int adj[MAXN][MAXDEG], deg[MAXN];
static int best_adj[MAXN][MAXDEG], best_deg[MAXN];

static uint64_t R[MAXN][MAXW], Rn[MAXN][MAXW];
static uint64_t BAD[MAXN][MAXW], BAD2[MAXN][MAXW];
static int defic[MAXN], defic2[MAXN];
static int Pp[MAXP], Pq[MAXP], nP;

static inline int has_edge(int a, int b) {
    for (int i = 0; i < deg[a]; i++) {
        if (adj[a][i] == b) return 1;
    }
    return 0;
}

static inline void add_edge(int a, int b) {
    adj[a][deg[a]++] = b;
    adj[b][deg[b]++] = a;
}

static inline void rm_edge(int a, int b) {
    for (int i = 0; i < deg[a]; i++) {
        if (adj[a][i] == b) {
            adj[a][i] = adj[a][--deg[a]];
            break;
        }
    }
    for (int i = 0; i < deg[b]; i++) {
        if (adj[b][i] == a) {
            adj[b][i] = adj[b][--deg[b]];
            break;
        }
    }
}

static void bfs_dist(int src, int *dist, int *queue) {
    for (int i = 0; i < N; i++) dist[i] = -1;
    dist[src] = 0;
    queue[0] = src;
    int head = 0, tail = 1;
    while (head < tail) {
        int u = queue[head++];
        int du = dist[u] + 1;
        for (int i = 0; i < deg[u]; i++) {
            int v = adj[u][i];
            if (dist[v] < 0) {
                dist[v] = du;
                queue[tail++] = v;
            }
        }
    }
}

static long long full_eval_store(uint64_t out_BAD[MAXN][MAXW], int out_defic[MAXN]) {
    for (int v = 0; v < N; v++) {
        for (int w = 0; w < W; w++) R[v][w] = 0;
        R[v][v >> 6] |= 1ULL << (v & 63);
    }
    for (int step = 0; step < D - 1; step++) {
        for (int v = 0; v < N; v++) {
            uint64_t *rnv = Rn[v];
            const uint64_t *rv = R[v];
            for (int w = 0; w < W; w++) rnv[w] = rv[w];
            int dv = deg[v];
            for (int j = 0; j < dv; j++) {
                const uint64_t *ru = R[adj[v][j]];
                for (int w = 0; w < W; w++) rnv[w] |= ru[w];
            }
        }
        for (int v = 0; v < N; v++) {
            for (int w = 0; w < W; w++) R[v][w] = Rn[v][w];
        }
    }
    uint64_t lastmask = ~0ULL;
    int rem = N & 63;
    if (rem != 0) lastmask = (1ULL << rem) - 1ULL;
    long long total = 0;
    for (int v = 0; v < N; v++) {
        int c = 0;
        int dv = deg[v];
        for (int w = 0; w < W; w++) {
            uint64_t x = R[v][w];
            for (int j = 0; j < dv; j++) {
                x |= R[adj[v][j]][w];
            }
            uint64_t nb = ~x;
            if (w == W - 1) nb &= lastmask;
            out_BAD[v][w] = nb;
            c += __builtin_popcountll(nb);
        }
        out_defic[v] = c;
        total += c;
    }
    return total / 2;
}

static inline int isbad(uint64_t B[MAXN][MAXW], int p, int q) {
    return (int)((B[p][q >> 6] >> (q & 63)) & 1ULL);
}

static void load_seed_graph(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) { perror("fopen seed"); exit(1); }
    memset(orig_deg, 0, sizeof(orig_deg));
    char line[4096];
    int maxv = -1;
    while (fgets(line, sizeof(line), f)) {
        char *p = line;
        while (*p == ' ' || *p == '\t') p++;
        if (*p == '#' || *p == '\n' || *p == '\r' || *p == 0) continue;
        int vals[128], nvals = 0;
        while (*p && nvals < 128) {
            while (*p == ' ' || *p == '\t' || *p == ':' || *p == ',') p++;
            if (*p == '#' || *p == '\n' || *p == '\r' || *p == 0) break;
            char *q;
            long v = strtol(p, &q, 10);
            if (q == p) break;
            vals[nvals++] = (int)v;
            if ((int)v > maxv) maxv = (int)v;
            p = q;
        }
        if (nvals < 2) continue;
        int u = vals[0];
        for (int i = 1; i < nvals; i++) {
            int v = vals[i];
            if (u == v) continue;
            int found = 0;
            for (int j = 0; j < orig_deg[u]; j++) if (orig_adj[u][j] == v) { found = 1; break; }
            if (!found) {
                orig_adj[u][orig_deg[u]++] = v;
                orig_adj[v][orig_deg[v]++] = u;
            }
        }
    }
    fclose(f);
    N0 = maxv + 1;
}

static void prune_redundant_seed_edges() {
    N = N0;
    W = (N + 63) / 64;
    for (int v = 0; v < N0; v++) {
        deg[v] = orig_deg[v];
        for (int j = 0; j < deg[v]; j++) adj[v][j] = orig_adj[v][j];
    }
    if (full_eval_store(BAD, defic) != 0) return;
    int pruned = 0;
    for (int u = N0 - 1; u >= 0; u--) {
        for (int idx = deg[u] - 1; idx >= 0; idx--) {
            int v = adj[u][idx];
            if (u < v) continue;
            rm_edge(u, v);
            if (full_eval_store(BAD, defic) == 0) {
                pruned++;
            } else {
                add_edge(u, v);
            }
        }
    }
    for (int v = 0; v < N0; v++) {
        orig_deg[v] = deg[v];
        for (int j = 0; j < deg[v]; j++) orig_adj[v][j] = adj[v][j];
    }
    int slack_slots = 0;
    for (int v = 0; v < N0; v++) slack_slots += (Delta - orig_deg[v]);
    printf("Pruned %d redundant seed edges -> %d free degree slots in N0=%d\n", pruned, slack_slots, N0);
    fflush(stdout);
}

static void warm_start_insert(int k) {
    N = N0 + k;
    W = (N + 63) / 64;
    for (int v = 0; v < N0; v++) {
        deg[v] = orig_deg[v];
        for (int j = 0; j < deg[v]; j++) adj[v][j] = orig_adj[v][j];
    }
    for (int v = N0; v < N; v++) deg[v] = 0;

    // Precompute (D-1)-balls in original graph
    static uint64_t Rb[MAXN][MAXW];
    for (int v = 0; v < N; v++) {
        for (int w = 0; w < W; w++) R[v][w] = 0;
        R[v][v >> 6] |= 1ULL << (v & 63);
    }
    for (int step = 0; step < D - 1; step++) {
        for (int v = 0; v < N; v++) {
            for (int w = 0; w < W; w++) Rn[v][w] = R[v][w];
            for (int j = 0; j < deg[v]; j++) {
                int u = adj[v][j];
                for (int w = 0; w < W; w++) Rn[v][w] |= R[u][w];
            }
        }
        for (int v = 0; v < N; v++) for (int w = 0; w < W; w++) R[v][w] = Rn[v][w];
    }
    for (int v = 0; v < N; v++) for (int w = 0; w < W; w++) Rb[v][w] = R[v][w];

    int used[MAXN] = {0};
    static uint64_t cov[16][MAXW];
    int slots[16];
    for (int r = 0; r < k && r < 16; r++) {
        memset(cov[r], 0, sizeof(cov[r]));
        slots[r] = Delta;
    }
    for (int step = 0; step < Delta; step++) {
        for (int r = 0; r < k && r < 16; r++) {
            int z = N0 + r;
            if (slots[r] <= 0) continue;
            int best_v = -1, best_gain = -1;
            int start = rand_int(N0);
            for (int off = 0; off < N0; off++) {
                int v = (start + off) % N0;
                if (deg[v] < Delta && !has_edge(z, v) && !used[v]) {
                    int g = 0;
                    for (int w = 0; w < W; w++) g += __builtin_popcountll(Rb[v][w] & ~cov[r][w]);
                    if (g > best_gain) {
                        best_gain = g;
                        best_v = v;
                    }
                }
            }
            if (best_v < 0) continue;
            add_edge(z, best_v);
            for (int w = 0; w < W; w++) cov[r][w] |= Rb[best_v][w];
            slots[r]--;
        }
    }
    for (int r = 0; r < k && r < 16; r++) {
        int z = N0 + r;
        while (slots[r] >= 2) {
            int best_a = -1, best_b = -1, best_g = -1;
            for (int t = 0; t < 600; t++) {
                int a = rand_int(N0);
                if (deg[a] == 0 || used[a]) continue;
                int b = adj[a][rand_int(deg[a])];
                if (b >= N0 || used[b] || has_edge(z, a) || has_edge(z, b)) continue;
                int g = 0;
                for (int w = 0; w < W; w++) g += __builtin_popcountll((Rb[a][w] | Rb[b][w]) & ~cov[r][w]);
                if (g > best_g) {
                    best_g = g; best_a = a; best_b = b;
                }
            }
            if (best_a < 0) break;
            used[best_a] = 1; used[best_b] = 1;
            rm_edge(best_a, best_b);
            add_edge(z, best_a);
            add_edge(z, best_b);
            for (int w = 0; w < W; w++) cov[r][w] |= Rb[best_a][w] | Rb[best_b][w];
            slots[r] -= 2;
        }
    }
    // Pair up any leftover free slots on new vertices ONLY (preserve free slots on 0..N0-1 for Move 1!)
    int free_v[MAXN];
    for (int pass = 0; pass < 4; pass++) {
        int nf = 0;
        for (int v = 0; v < N; v++) if (deg[v] < Delta) free_v[nf++] = v;
        for (int i = nf - 1; i > 0; i--) {
            int j = rand_int(i + 1);
            int tmp = free_v[i]; free_v[i] = free_v[j]; free_v[j] = tmp;
        }
        for (int i = 0; i < nf; i++) {
            for (int j = i + 1; j < nf; j++) {
                int p = free_v[i], q = free_v[j];
                if (deg[p] < Delta && deg[q] < Delta && !has_edge(p, q) && (p >= N0 || q >= N0)) {
                    add_edge(p, q);
                }
            }
        }
    }
}

static void write_edges(const char *path) {
    FILE *f = fopen(path, "w");
    if (!f) { perror("fopen out"); return; }
    for (int u = 0; u < N; u++) {
        for (int i = 0; i < best_deg[u]; i++) {
            int v = best_adj[u][i];
            if (u < v) fprintf(f, "%d %d\n", u, v);
        }
    }
    fclose(f);
}

static int distx[MAXN], disty[MAXN], queue[MAXN];
static int lst[MAXN], lst2[MAXN], free_pool[MAXN];
static int dA[16][MAXN], dR[16][MAXN];

static long long sa2_run(long long iters, double T0, double T1, long long patience,
                         double p_free, double p_target,
                         long long *out_init, long long *out_acc, long long *out_full, long long *out_screen) {
    long long cost = full_eval_store(BAD, defic);
    *out_init = cost;
    long long best = cost;
    memcpy(best_adj, adj, sizeof(adj));
    memcpy(best_deg, deg, sizeof(deg));

    nP = 0;
    for (int p = 0; p < N; p++) {
        if (defic[p] > 0) {
            for (int q = p + 1; q < N; q++) {
                if (isbad(BAD, p, q) && nP < MAXP) {
                    Pp[nP] = p; Pq[nP] = q; nP++;
                }
            }
        }
    }

    long long acc = 0, nfull = 0, nscreen = 0, last_imp = 0;
    int ops[16][3];
    int addA[8][2], remR[8][2];

    for (long long it = 0; it < iters; it++) {
        if (cost == 0) break;
        if (it - last_imp > patience) break;
        double T = T0 * pow(T1 / T0, (double)it / (double)iters);
        int nops = 0, ok = 0;
        double r = urand();

        if (r < p_free) {
            // Move 1: pure addition between deficient vertices near a bad pair
            if (nP > 0) {
                int k = rand_int(nP);
                int x = Pp[k], y = Pq[k];
                if (xrand() & 1) { int t = x; x = y; y = t; }
                bfs_dist(x, distx, queue);
                bfs_dist(y, disty, queue);
                int na = 0, nb2 = 0;
                for (int v = 0; v < N; v++) {
                    if (deg[v] < Delta && distx[v] >= 0 && distx[v] <= D - 1) lst[na++] = v;
                    if (deg[v] < Delta && disty[v] >= 0 && disty[v] <= D - 1) lst2[nb2++] = v;
                }
                if (na > 0 && nb2 > 0) {
                    for (int tr = 0; tr < 200; tr++) {
                        int a = lst[rand_int(na)];
                        int b = lst2[rand_int(nb2)];
                        if (a != b && distx[a] + disty[b] <= D - 1 && !has_edge(a, b)) {
                            add_edge(a, b);
                            ops[nops][0] = 1; ops[nops][1] = a; ops[nops][2] = b; nops++;
                            ok = 1; break;
                        }
                    }
                }
            }
        } else if (r < p_free + p_target) {
            // Move 2: targeted shortcut rewire for a bad pair
            if (nP > 0) {
                int k = rand_int(nP);
                int x = Pp[k], y = Pq[k];
                if (xrand() & 1) { int t = x; x = y; y = t; }
                bfs_dist(x, distx, queue);
                bfs_dist(y, disty, queue);
                int i = rand_int(D);
                int j = D - 1 - i;
                int ma = 0, mb = 0;
                for (int v = 0; v < N; v++) {
                    if (distx[v] == i) lst[ma++] = v;
                    if (disty[v] == j) lst2[mb++] = v;
                }
                int a = ma > 0 ? lst[rand_int(ma)] : -1;
                int b = mb > 0 ? lst2[rand_int(mb)] : -1;
                if (a >= 0 && b >= 0 && a != b && !has_edge(a, b)) {
                    int c = -1, d = -1;
                    if (deg[a] >= Delta) {
                        for (int tr = 0; tr < 6; tr++) {
                            c = adj[a][rand_int(deg[a])];
                            if (distx[c] >= i) break;
                        }
                    }
                    if (deg[b] >= Delta) {
                        for (int tr = 0; tr < 6; tr++) {
                            d = adj[b][rand_int(deg[b])];
                            if (disty[d] >= j) break;
                        }
                    }
                    if (c == b || d == a) {
                        ok = 0;
                    } else {
                        if (c >= 0) {
                            rm_edge(a, c);
                            ops[nops][0] = 2; ops[nops][1] = a; ops[nops][2] = c; nops++;
                        }
                        if (d >= 0 && !(d == a && c == b)) {
                            rm_edge(b, d);
                            ops[nops][0] = 2; ops[nops][1] = b; ops[nops][2] = d; nops++;
                        }
                        add_edge(a, b);
                        ops[nops][0] = 1; ops[nops][1] = a; ops[nops][2] = b; nops++;
                        if (c >= 0 && d >= 0 && c != d && !has_edge(c, d)) {
                            add_edge(c, d);
                            ops[nops][0] = 1; ops[nops][1] = c; ops[nops][2] = d; nops++;
                        }
                        ok = 1;
                    }
                }
            }
        } else {
            // Move 3: random 2-switch
            for (int tr = 0; tr < 20; tr++) {
                int a = rand_int(N);
                if (deg[a] == 0) continue;
                int b = adj[a][rand_int(deg[a])];
                int c = rand_int(N);
                if (deg[c] == 0) continue;
                int d = adj[c][rand_int(deg[c])];
                if (a == c || a == d || b == c || b == d) continue;
                if (has_edge(a, d) || has_edge(c, b)) continue;
                rm_edge(a, b); rm_edge(c, d);
                add_edge(a, d); add_edge(c, b);
                ops[0][0] = 2; ops[0][1] = a; ops[0][2] = b;
                ops[1][0] = 2; ops[1][1] = c; ops[1][2] = d;
                ops[2][0] = 1; ops[2][1] = a; ops[2][2] = d;
                ops[3][0] = 1; ops[3][1] = c; ops[3][2] = b;
                nops = 4; ok = 1; break;
            }
        }
        if (!ok) continue;

        double thr = -T * log(urand() + 1e-300);
        int nA = 0, nR = 0;
        for (int t = 0; t < nops; t++) {
            if (ops[t][0] == 1) { addA[nA][0] = ops[t][1]; addA[nA][1] = ops[t][2]; nA++; }
            else { remR[nR][0] = ops[t][1]; remR[nR][1] = ops[t][2]; nR++; }
        }
        int ne = 0;
        for (int e = 0; e < nA; e++) {
            bfs_dist(addA[e][0], dA[ne++], queue);
            bfs_dist(addA[e][1], dA[ne++], queue);
        }
        long long gain = 0;
        for (int k = 0; k < nP; k++) {
            int p = Pp[k], q = Pq[k];
            int fixed = 0;
            for (int e = 0; e < nA; e++) {
                int du_p = dA[2*e][p], dv_q = dA[2*e+1][q];
                int dv_p = dA[2*e+1][p], du_q = dA[2*e][q];
                if (du_p >= 0 && dv_q >= 0 && du_p + 1 + dv_q <= D) fixed = 1;
                if (dv_p >= 0 && du_q >= 0 && dv_p + 1 + du_q <= D) fixed = 1;
                if (du_p >= 0 && du_q >= 0 && du_p + du_q <= D) fixed = 1;
                if (dv_p >= 0 && dv_q >= 0 && dv_p + dv_q <= D) fixed = 1;
            }
            if (fixed) gain++;
        }

        if (nR == 0) {
            if (gain > 0) {
                cost -= gain;
                acc++;
                int nP2 = 0;
                for (int k = 0; k < nP; k++) {
                    int p = Pp[k], q = Pq[k];
                    int still = 1;
                    for (int e = 0; e < nA; e++) {
                        int du_p = dA[2*e][p], dv_q = dA[2*e+1][q];
                        int dv_p = dA[2*e+1][p], du_q = dA[2*e][q];
                        if (du_p >= 0 && dv_q >= 0 && du_p + 1 + dv_q <= D) still = 0;
                        if (dv_p >= 0 && du_q >= 0 && dv_p + 1 + du_q <= D) still = 0;
                        if (du_p >= 0 && du_q >= 0 && du_p + du_q <= D) still = 0;
                        if (dv_p >= 0 && dv_q >= 0 && dv_p + dv_q <= D) still = 0;
                    }
                    if (still) {
                        Pp[nP2] = p; Pq[nP2] = q; nP2++;
                    } else {
                        BAD[p][q >> 6] &= ~(1ULL << (q & 63));
                        BAD[q][p >> 6] &= ~(1ULL << (p & 63));
                        defic[p]--; defic[q]--;
                    }
                }
                nP = nP2;
                if (cost < best) {
                    best = cost;
                    memcpy(best_adj, adj, sizeof(adj));
                    memcpy(best_deg, deg, sizeof(deg));
                    last_imp = it;
                }
            } else {
                for (int t = nops - 1; t >= 0; t--) {
                    if (ops[t][0] == 1) rm_edge(ops[t][1], ops[t][2]);
                    else add_edge(ops[t][1], ops[t][2]);
                }
            }
            continue;
        }

        nscreen++;
        int ends[12], cnt = 0;
        for (int e = 0; e < nR; e++) {
            for (int s = 0; s < 2; s++) {
                int v = remR[e][s], dup = 0;
                for (int t = 0; t < cnt; t++) if (ends[t] == v) dup = 1;
                if (!dup) ends[cnt++] = v;
            }
        }
        for (int z = N0; z < N && cnt < 12; z++) {
            int dup = 0;
            for (int t = 0; t < cnt; t++) if (ends[t] == z) dup = 1;
            if (!dup) ends[cnt++] = z;
        }
        long long Lp = 0;
        for (int t = 0; t < cnt; t++) {
            int v = ends[t];
            bfs_dist(v, dR[t], queue);
            for (int q = 0; q < N; q++) {
                int dq = dR[t][q];
                if ((dq < 0 || dq > D) && !isbad(BAD, v, q)) Lp++;
            }
        }
        long long dbl = 0;
        for (int t1 = 0; t1 < cnt; t1++) {
            for (int t2 = t1 + 1; t2 < cnt; t2++) {
                int dd = dR[t1][ends[t2]];
                if ((dd < 0 || dd > D) && !isbad(BAD, ends[t1], ends[t2])) dbl++;
            }
        }
        Lp -= dbl;
        if ((double)(Lp - gain) > thr) {
            for (int t = nops - 1; t >= 0; t--) {
                if (ops[t][0] == 1) rm_edge(ops[t][1], ops[t][2]);
                else add_edge(ops[t][1], ops[t][2]);
            }
            continue;
        }

        nfull++;
        long long newcost = full_eval_store(BAD2, defic2);
        long long dc = newcost - cost;
        if ((double)dc <= thr) {
            cost = newcost;
            memcpy(BAD, BAD2, sizeof(BAD));
            memcpy(defic, defic2, sizeof(defic));
            acc++;
            nP = 0;
            for (int p = 0; p < N; p++) {
                if (defic[p] > 0) {
                    for (int q = p + 1; q < N; q++) {
                        if (isbad(BAD, p, q) && nP < MAXP) {
                            Pp[nP] = p; Pq[nP] = q; nP++;
                        }
                    }
                }
            }
            if (cost < best) {
                best = cost;
                memcpy(best_adj, adj, sizeof(adj));
                memcpy(best_deg, deg, sizeof(deg));
                last_imp = it;
                if (best == 0) break;
            }
        } else {
            for (int t = nops - 1; t >= 0; t--) {
                if (ops[t][0] == 1) rm_edge(ops[t][1], ops[t][2]);
                else add_edge(ops[t][1], ops[t][2]);
            }
        }
    }
    *out_acc = acc;
    *out_full = nfull;
    *out_screen = nscreen;
    return best;
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "Usage: %s SEED_GRAPH DELTA D K_INSERT OUT_PREFIX [ITERS] [RESTARTS] [SEED]\n", argv[0]);
        return 2;
    }
    const char *seed_path = argv[1];
    Delta = atoi(argv[2]);
    D = atoi(argv[3]);
    int k_ins = atoi(argv[4]);
    const char *out_prefix = argv[5];
    long long iters = argc > 6 ? atoll(argv[6]) : 300000LL;
    int restarts = argc > 7 ? atoi(argv[7]) : 20;
    uint64_t base_seed = argc > 8 ? (uint64_t)atoll(argv[8]) : 1ULL;

    load_seed_graph(seed_path);
    printf("Loaded %s: N0=%d, target=(%d,%d), inserting k=%d -> N=%d\n", seed_path, N0, Delta, D, k_ins, N0 + k_ins);
    fflush(stdout);
    prune_redundant_seed_edges();

    for (int rs = 0; rs < restarts; rs++) {
        rng_state = base_seed * 1000003ULL + (uint64_t)(rs + 1) * 918273645ULL;
        for (int i = 0; i < 20; i++) xrand();
        warm_start_insert(k_ins);

        long long init_cost = 0, acc = 0, nfull = 0, nscreen = 0;
        clock_t t0 = clock();
        long long best = sa2_run(iters, 0.6, 0.02, 150000LL, 0.20, 0.60, &init_cost, &acc, &nfull, &nscreen);
        double elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("rs=%d: init=%lld best=%lld acc=%lld full=%lld screen=%lld (%.2fs)\n",
               rs, init_cost, best, acc, nfull, nscreen, elapsed);
        fflush(stdout);

        // If near-miss (0 < best <= 30), run polish rounds starting from best_adj
        if (best > 0 && best <= 30) {
            static int saved_adj[MAXN][MAXDEG], saved_deg[MAXN];
            memcpy(saved_adj, best_adj, sizeof(best_adj));
            memcpy(saved_deg, best_deg, sizeof(best_deg));
            for (int pr = 0; pr < 12 && best > 0; pr++) {
                memcpy(adj, saved_adj, sizeof(saved_adj));
                memcpy(deg, saved_deg, sizeof(saved_deg));
                rng_state = base_seed * 7777771ULL + (uint64_t)(rs * 31 + pr + 1) * 123456789ULL;
                for (int i = 0; i < 20; i++) xrand();
                long long p_init = 0, p_acc = 0, p_full = 0, p_scr = 0;
                clock_t tp = clock();
                double T_start = (pr % 3 == 0) ? 0.35 : ((pr % 3 == 1) ? 0.18 : 0.08);
                long long p_best = sa2_run(150000LL, T_start, 0.015, 80000LL, 0.20, 0.65, &p_init, &p_acc, &p_full, &p_scr);
                double pel = (double)(clock() - tp) / CLOCKS_PER_SEC;
                printf("  [polish %d] init=%lld best=%lld acc=%lld full=%lld (%.2fs)\n",
                       pr, p_init, p_best, p_acc, p_full, pel);
                fflush(stdout);
                if (p_best < best) {
                    best = p_best;
                    memcpy(saved_adj, best_adj, sizeof(best_adj));
                    memcpy(saved_deg, best_deg, sizeof(best_deg));
                }
            }
            memcpy(best_adj, saved_adj, sizeof(saved_adj));
            memcpy(best_deg, saved_deg, sizeof(best_deg));
        }

        if (best == 0) {
            char out_file[512];
            snprintf(out_file, sizeof(out_file), "%s_N%d.edges", out_prefix, N);
            write_edges(out_file);
            printf("SUCCESS! Wrote %s\n", out_file);
            return 0;
        }
    }
    return 1;
}
