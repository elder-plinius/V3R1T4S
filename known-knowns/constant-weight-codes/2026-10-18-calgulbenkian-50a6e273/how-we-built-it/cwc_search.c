#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define KMAX 512
#define WMAX 8
#define SENT 30000
#define MAX_KB 6
#define MAX_RMAX 16
#define CH_MAX 64

static int64_t B[65][65];
static int64_t T_rank[8][256][65];
static int POP8[256];

static void init_tables(int n) {
    memset(B, 0, sizeof(B));
    for (int a = 0; a <= 64; a++) {
        B[a][0] = 1;
        for (int b = 1; b <= a; b++) {
            B[a][b] = B[a - 1][b - 1] + B[a - 1][b];
        }
    }
    for (int i = 0; i < 256; i++) {
        POP8[i] = __builtin_popcount(i);
    }
    int nbytes = (n + 7) / 8;
    memset(T_rank, 0, sizeof(T_rank));
    for (int i = 0; i < nbytes; i++) {
        for (int b = 0; b < 256; b++) {
            for (int k = 0; k < 65; k++) {
                int64_t s = 0;
                int j = 0;
                int ok = 1;
                for (int p = 0; p < 8; p++) {
                    if ((b >> p) & 1) {
                        int pos = 8 * i + p;
                        int kk = k + 1 + j;
                        if (pos > 63 || kk > 63) {
                            ok = 0;
                            break;
                        }
                        s += B[pos][kk];
                        j++;
                    }
                }
                T_rank[i][b][k] = ok ? s : 0;
            }
        }
    }
}

static inline int64_t rank_t(uint64_t x, int nbytes) {
    int64_t r = 0;
    int k = 0;
    for (int i = 0; i < nbytes; i++) {
        int b = (int)((x >> (8 * i)) & 255u);
        r += T_rank[i][b][k];
        k += POP8[b];
    }
    return r;
}

static inline uint64_t unrank_colex(int64_t r, int w, int n) {
    uint64_t x = 0;
    int top = n;
    for (int k = w; k >= 1; k--) {
        int lo = k - 1, hi = top - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >> 1;
            if (B[mid][k] <= r) lo = mid;
            else hi = mid - 1;
        }
        x |= (1ULL << lo);
        r -= B[lo][k];
        top = lo;
    }
    return x;
}

static inline int sub_ranks_g(uint64_t x, int n, int w, int r, int64_t *out) {
    int e[64];
    int k = 0;
    uint64_t tmp = x;
    while (tmp) {
        e[k++] = __builtin_ctzll(tmp);
        tmp &= tmp - 1;
    }
    int64_t S[6][65];
    for (int c = 0; c <= r; c++) {
        S[c][0] = 0;
        for (int j = 0; j < w; j++) {
            int idx = j + 1 - c;
            S[c][j + 1] = S[c][j] + (idx >= 0 ? B[e[j]][idx] : 0);
        }
    }
    int pos[6];
    for (int i = 0; i < r; i++) pos[i] = i;
    int out_idx = 0;
    while (1) {
        int64_t rk = S[0][pos[0]];
        for (int c = 1; c < r; c++) {
            rk += S[c][pos[c]] - S[c][pos[c - 1] + 1];
        }
        rk += S[r][w] - S[r][pos[r - 1] + 1];
        out[out_idx++] = rk;

        int i = r - 1;
        while (i >= 0 && pos[i] == w - r + i) i--;
        if (i < 0) break;
        pos[i]++;
        for (int j = i + 1; j < r; j++) pos[j] = pos[j - 1] + 1;
    }
    return out_idx;
}

static inline uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *s = x;
    return x;
}

static int gen_submasks(const int *pos, int m, int jmax, uint64_t *out, int *off) {
    int k = 0;
    off[0] = 0;
    for (int i1 = 0; i1 < m; i1++) {
        out[k++] = 1ULL << pos[i1];
    }
    off[1] = k;
    if (jmax >= 2) {
        for (int i1 = 0; i1 < m; i1++) {
            for (int i2 = i1 + 1; i2 < m; i2++) {
                out[k++] = (1ULL << pos[i1]) | (1ULL << pos[i2]);
            }
        }
    }
    off[2] = k;
    if (jmax >= 3) {
        for (int i1 = 0; i1 < m; i1++) {
            for (int i2 = i1 + 1; i2 < m; i2++) {
                for (int i3 = i2 + 1; i3 < m; i3++) {
                    out[k++] = (1ULL << pos[i1]) | (1ULL << pos[i2]) | (1ULL << pos[i3]);
                }
            }
        }
    }
    off[3] = k;
    if (jmax >= 4) {
        for (int i1 = 0; i1 < m; i1++) {
            for (int i2 = i1 + 1; i2 < m; i2++) {
                for (int i3 = i2 + 1; i3 < m; i3++) {
                    for (int i4 = i3 + 1; i4 < m; i4++) {
                        out[k++] = (1ULL << pos[i1]) | (1ULL << pos[i2]) | (1ULL << pos[i3]) | (1ULL << pos[i4]);
                    }
                }
            }
        }
    }
    off[4] = k;
    return k;
}

typedef struct {
    const uint64_t *words;
    int count;
    int n, w, r, nbytes;
    int16_t delta;
    int16_t *cnt;
    int tid, nthreads;
} NeighborJob;

static void *update_neighbors_worker(void *arg) {
    NeighborJob *job = (NeighborJob *)arg;
    int n = job->n, r = job->r, nbytes = job->nbytes;
    int16_t delta = job->delta;
    int16_t *cnt = job->cnt;

    uint64_t *S = (uint64_t *)malloc(16384 * sizeof(uint64_t));
    uint64_t *C = (uint64_t *)malloc(262144 * sizeof(uint64_t));
    int oS[6], oC[6];

    for (int idx = job->tid; idx < job->count; idx += job->nthreads) {
        uint64_t c = job->words[idx];
        int supp[64], comp[64], a = 0, b = 0;
        for (int p = 0; p < n; p++) {
            if ((c >> p) & 1ULL) supp[a++] = p;
            else comp[b++] = p;
        }
        gen_submasks(supp, a, r, S, oS);
        gen_submasks(comp, b, r, C, oC);
        for (int j = 1; j <= r; j++) {
            int s0 = oS[j - 1], s1 = oS[j];
            int c0 = oC[j - 1], c1 = oC[j];
            for (int u = s0; u < s1; u++) {
                uint64_t cu = c ^ S[u];
                for (int v = c0; v < c1; v++) {
                    uint64_t y = cu | C[v];
                    int64_t rk = rank_t(y, nbytes);
                    __atomic_fetch_add(&cnt[rk], delta, __ATOMIC_RELAXED);
                }
            }
        }
    }
    free(S);
    free(C);
    return NULL;
}

static void parallel_update_neighbors(const uint64_t *words, int count, int n, int w, int r, int16_t *cnt, int16_t delta, int nthreads) {
    if (count == 0) return;
    int nt = (count < nthreads) ? count : nthreads;
    pthread_t th[16];
    NeighborJob jobs[16];
    int nbytes = (n + 7) / 8;
    for (int t = 0; t < nt; t++) {
        jobs[t].words = words;
        jobs[t].count = count;
        jobs[t].n = n;
        jobs[t].w = w;
        jobs[t].r = r;
        jobs[t].nbytes = nbytes;
        jobs[t].delta = delta;
        jobs[t].cnt = cnt;
        jobs[t].tid = t;
        jobs[t].nthreads = nt;
        pthread_create(&th[t], NULL, update_neighbors_worker, &jobs[t]);
    }
    for (int t = 0; t < nt; t++) {
        pthread_join(th[t], NULL);
    }
}

// Exact bitset branch-and-bound Maximum Independent Set solver (port of mis_exact_g)
static int mis_exact_g(const uint64_t *cand, int K, int tthr, int node_cap, uint64_t bestC[WMAX]) {
    int W = (K + 63) / 64;
    uint64_t adj[KMAX][WMAX];
    for (int i = 0; i < K; i++) {
        memset(adj[i], 0, W * sizeof(uint64_t));
    }
    for (int i = 0; i < K; i++) {
        uint64_t ci = cand[i];
        for (int j = i + 1; j < K; j++) {
            if (__builtin_popcountll(ci & cand[j]) >= tthr) {
                adj[i][j >> 6] |= (1ULL << (j & 63));
                adj[j][i >> 6] |= (1ULL << (i & 63));
            }
        }
    }

    uint64_t stP[KMAX + 2][WMAX];
    uint64_t stC[KMAX + 2][WMAX];
    int stS[KMAX + 2];

    memset(stP[0], 0, WMAX * sizeof(uint64_t));
    memset(stC[0], 0, WMAX * sizeof(uint64_t));
    for (int i = 0; i < K; i++) {
        stP[0][i >> 6] |= (1ULL << (i & 63));
    }
    stS[0] = 0;
    int sp = 1;
    int best = 0;
    memset(bestC, 0, WMAX * sizeof(uint64_t));

    uint64_t P[WMAX], C[WMAX], tmp[WMAX], cand2[WMAX];
    int nodes = 0;

    while (sp > 0) {
        sp--;
        nodes++;
        if (nodes > node_cap) break;

        memcpy(P, stP[sp], W * sizeof(uint64_t));
        memcpy(C, stC[sp], W * sizeof(uint64_t));
        int size = stS[sp];

        int cntP = 0;
        for (int k = 0; k < W; k++) cntP += __builtin_popcountll(P[k]);
        if (cntP == 0) {
            if (size > best) {
                best = size;
                memcpy(bestC, C, W * sizeof(uint64_t));
            }
            continue;
        }
        if (size + cntP <= best) continue;

        // Greedy sequential clique-cover upper bound on P
        memcpy(tmp, P, W * sizeof(uint64_t));
        int cover = 0;
        while (1) {
            int v = -1;
            for (int k = 0; k < W; k++) {
                if (tmp[k] != 0) {
                    v = k * 64 + __builtin_ctzll(tmp[k]);
                    break;
                }
            }
            if (v < 0) break;
            cover++;
            tmp[v >> 6] &= ~(1ULL << (v & 63));
            for (int k = 0; k < W; k++) cand2[k] = tmp[k] & adj[v][k];
            while (1) {
                int u = -1;
                for (int k = 0; k < W; k++) {
                    if (cand2[k] != 0) {
                        u = k * 64 + __builtin_ctzll(cand2[k]);
                        break;
                    }
                }
                if (u < 0) break;
                tmp[u >> 6] &= ~(1ULL << (u & 63));
                for (int k = 0; k < W; k++) cand2[k] &= adj[u][k];
                cand2[u >> 6] &= ~(1ULL << (u & 63));
            }
        }
        if (size + cover <= best) continue;

        // Branch on vertex bv of maximum degree inside P
        int bv = -1, bd = -1;
        for (int k = 0; k < W; k++) {
            uint64_t t = P[k];
            while (t != 0) {
                int b = __builtin_ctzll(t);
                int v = k * 64 + b;
                int dg = 0;
                for (int kk = 0; kk < W; kk++) {
                    dg += __builtin_popcountll(adj[v][kk] & P[kk]);
                }
                if (dg > bd) {
                    bd = dg;
                    bv = v;
                }
                t &= t - 1;
            }
        }
        if (bd == 0) {
            if (size + cntP > best) {
                best = size + cntP;
                for (int k = 0; k < W; k++) bestC[k] = C[k] | P[k];
            }
            continue;
        }

        // Child 1: exclude bv
        memcpy(stP[sp], P, W * sizeof(uint64_t));
        stP[sp][bv >> 6] &= ~(1ULL << (bv & 63));
        memcpy(stC[sp], C, W * sizeof(uint64_t));
        stS[sp] = size;
        sp++;

        // Child 2: include bv (explored first)
        for (int k = 0; k < W; k++) stP[sp][k] = P[k] & ~adj[bv][k];
        stP[sp][bv >> 6] &= ~(1ULL << (bv & 63));
        memcpy(stC[sp], C, W * sizeof(uint64_t));
        stC[sp][bv >> 6] |= (1ULL << (bv & 63));
        stS[sp] = size + 1;
        sp++;
    }
    return best;
}

typedef struct {
    uint64_t w;
    int8_t k;
    int32_t b[MAX_KB];
} LowWord;

typedef struct {
    int8_t len;
    int32_t c[MAX_RMAX];
} RemSet;

static int cmp_int32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a;
    int32_t y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a;
    uint64_t y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}

static int cmp_remset(const void *a, const void *b) {
    const RemSet *ra = (const RemSet *)a;
    const RemSet *rb = (const RemSet *)b;
    if (ra->len != rb->len) return (ra->len > rb->len) - (ra->len < rb->len);
    for (int i = 0; i < ra->len; i++) {
        if (ra->c[i] != rb->c[i]) return (ra->c[i] > rb->c[i]) - (ra->c[i] < rb->c[i]);
    }
    return 0;
}

typedef struct {
    const int16_t *cnt;
    int64_t r0, r1;
    int n, w, r, KB;
    const int32_t *owner;
    LowWord *out;
    int64_t count;
    int64_t cap;
    int64_t mism;
} ScanJob;

static void *scan_low_worker(void *arg) {
    ScanJob *job = (ScanJob *)arg;
    const int16_t *cnt = job->cnt;
    int n = job->n, w = job->w, r = job->r, KB = job->KB;
    const int32_t *owner = job->owner;
    int64_t rk_buf[256];

    for (int64_t rk = job->r0; rk < job->r1; rk++) {
        int16_t cval = cnt[rk];
        if (cval <= KB) {
            if (job->count >= job->cap) {
                job->cap = job->cap ? job->cap * 2 : 65536;
                job->out = (LowWord *)realloc(job->out, job->cap * sizeof(LowWord));
            }
            uint64_t x = unrank_colex(rk, w, n);
            int m = sub_ranks_g(x, n, w, r, rk_buf);
            int nbk = 0;
            int32_t bl[MAX_KB + 4];
            for (int k = 0; k < m; k++) {
                int32_t o = owner[rk_buf[k]];
                if (o != -1) {
                    int dup = 0;
                    for (int j = 0; j < nbk; j++) {
                        if (bl[j] == o) { dup = 1; break; }
                    }
                    if (!dup) {
                        if (nbk < MAX_KB) bl[nbk] = o;
                        nbk++;
                    }
                }
            }
            if (nbk != cval) job->mism++;
            // Sort blockers ascending
            for (int a = 1; a < nbk && a < MAX_KB; a++) {
                int32_t v = bl[a];
                int b = a - 1;
                while (b >= 0 && bl[b] > v) {
                    bl[b + 1] = bl[b];
                    b--;
                }
                bl[b + 1] = v;
            }
            LowWord *lw = &job->out[job->count++];
            lw->w = x;
            lw->k = (int8_t)nbk;
            for (int j = 0; j < nbk && j < MAX_KB; j++) lw->b[j] = bl[j];
        }
    }
    return NULL;
}

typedef struct {
    const RemSet *R;
    int NR;
    const int64_t *bptr;
    const int64_t *bidx;
    const LowWord *lw;
    const uint64_t *words;
    int tthr;
    int node_cap;
    int8_t *status;
    int32_t *nch;
    uint64_t *chosen; // NR * CH_MAX
    int next_q;
    pthread_mutex_t *mtx;
} SolveJob;

static void *solve_all_worker(void *arg) {
    SolveJob *job = (SolveJob *)arg;
    uint64_t cand[KMAX + 1];
    uint64_t bestC[WMAX];

    while (1) {
        int q0;
        pthread_mutex_lock(job->mtx);
        q0 = job->next_q;
        job->next_q += 64;
        pthread_mutex_unlock(job->mtx);
        if (q0 >= job->NR) break;
        int q1 = q0 + 64;
        if (q1 > job->NR) q1 = job->NR;

        for (int q = q0; q < q1; q++) {
            const RemSet *rq = &job->R[q];
            int nr = rq->len;
            int K = 0;
            int over = 0;
            for (int a = 0; a < nr; a++) {
                int32_t c = rq->c[a];
                for (int64_t z = job->bptr[c]; z < job->bptr[c + 1]; z++) {
                    int64_t i = job->bidx[z];
                    const LowWord *w_i = &job->lw[i];
                    int k = w_i->k;
                    // Since w_i->b is sorted ascending, minimum blocker is w_i->b[0]
                    if (w_i->b[0] != c) continue;
                    int ok = 1;
                    for (int j = 0; j < k; j++) {
                        int32_t b = w_i->b[j];
                        int inR = 0;
                        for (int e = 0; e < nr; e++) {
                            if (rq->c[e] == b) { inR = 1; break; }
                        }
                        if (!inR) { ok = 0; break; }
                    }
                    if (ok) {
                        if (K + nr >= KMAX) { over = 1; break; }
                        cand[K++] = w_i->w;
                    }
                }
                if (over) break;
            }
            if (over || K == 0) continue;
            int K_cand = K;
            for (int a = 0; a < nr; a++) {
                cand[K++] = job->words[rq->c[a]];
            }
            int best = mis_exact_g(cand, K, job->tthr, job->node_cap, bestC);
            if (best < nr) continue;
            int m = 0, newcount = 0;
            uint64_t *ch_q = &job->chosen[(int64_t)q * CH_MAX];
            for (int i = 0; i < K; i++) {
                if ((bestC[i >> 6] >> (i & 63)) & 1ULL) {
                    if (m < CH_MAX) ch_q[m] = cand[i];
                    m++;
                    if (i < K_cand) newcount++;
                }
            }
            if (m > CH_MAX) continue;
            job->nch[q] = m;
            if (best > nr) job->status[q] = 2;
            else if (newcount > 0) job->status[q] = 1;
        }
    }
    return NULL;
}

static void save_code_file(const char *outdir, int n, int d, int w, int M, const uint64_t *words) {
    char path[512];
    snprintf(path, sizeof(path), "%s/A%d_%d_%d_%d.txt", outdir, n, d, w, M);
    FILE *f = fopen(path, "w");
    if (!f) return;
    char line[72];
    line[n] = '\n';
    line[n + 1] = '\0';
    for (int i = 0; i < M; i++) {
        uint64_t x = words[i];
        for (int b = 0; b < n; b++) {
            line[n - 1 - b] = ((x >> b) & 1ULL) ? '1' : '0';
        }
        fputs(line, f);
    }
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "Usage: %s seed_txt n d w out_results_dir [rounds] [kb] [rmax] [clusters] [max4] [plateau_frac] [seed]\n", argv[0]);
        return 2;
    }
    const char *seed_path = argv[1];
    int n = atoi(argv[2]);
    int d = atoi(argv[3]);
    int w = atoi(argv[4]);
    const char *outdir = argv[5];
    int max_rounds = (argc > 6) ? atoi(argv[6]) : 80;
    int KB = (argc > 7) ? atoi(argv[7]) : 3;
    int rmax = (argc > 8) ? atoi(argv[8]) : 8;
    int ncluster = (argc > 9) ? atoi(argv[9]) : 4000;
    int max4 = (argc > 10) ? atoi(argv[10]) : 15000;
    double plateau_frac = (argc > 11) ? atof(argv[11]) : 0.5;
    uint64_t rng = (argc > 12) ? (uint64_t)atoll(argv[12]) : 77777ULL;
    double max_seconds = (argc > 13) ? atof(argv[13]) : 25.0;
    int switch_kb4_round = (argc > 14) ? atoi(argv[14]) : -1;
    if (rng == 0) rng = 1ULL;

    struct timespec ts_start, ts_now;
    clock_gettime(CLOCK_MONOTONIC, &ts_start);

    init_tables(n);
    int r = d / 2 - 1;
    int t_sub = w - r;
    int tthr = t_sub;
    int nbytes = (n + 7) / 8;

    // Load seed codewords from .txt file
    FILE *fp = fopen(seed_path, "r");
    if (!fp) {
        fprintf(stderr, "Cannot open %s\n", seed_path);
        return 1;
    }
    int cap_w = 65536;
    uint64_t *words = (uint64_t *)malloc(cap_w * sizeof(uint64_t));
    int M = 0;
    char buf[256];
    while (fgets(buf, sizeof(buf), fp)) {
        int len = 0;
        uint64_t x = 0;
        for (int i = 0; buf[i]; i++) {
            if (buf[i] == '0' || buf[i] == '1') {
                x = (x << 1) | (uint64_t)(buf[i] - '0');
                len++;
            }
        }
        if (len == n) {
            if (M >= cap_w) {
                cap_w *= 2;
                words = (uint64_t *)realloc(words, cap_w * sizeof(uint64_t));
            }
            words[M++] = x;
        }
    }
    fclose(fp);
    // Optional degree-sorted coordinate relabeling (enabled when env CWC_RELABEL=1 or by default on --relabel)
    if (getenv("CWC_RELABEL") && atoi(getenv("CWC_RELABEL")) == 1) {
        int freq[64] = {0};
        int perm[64];
        for (int b = 0; b < n; b++) perm[b] = b;
        for (int i = 0; i < M; i++) {
            uint64_t x = words[i];
            for (int b = 0; b < n; b++) {
                if ((x >> (n - 1 - b)) & 1ULL) freq[b]++;
            }
        }
        for (int a = 1; a < n; a++) {
            int p = perm[a];
            int c = a - 1;
            while (c >= 0 && freq[perm[c]] < freq[p]) {
                perm[c + 1] = perm[c];
                c--;
            }
            perm[c + 1] = p;
        }
        for (int i = 0; i < M; i++) {
            uint64_t old_x = words[i], new_x = 0;
            for (int b = 0; b < n; b++) {
                uint64_t bit = (old_x >> (n - 1 - perm[b])) & 1ULL;
                new_x = (new_x << 1) | bit;
            }
            words[i] = new_x;
        }
    }
    qsort(words, M, sizeof(uint64_t), cmp_u64);

    int64_t total_words = B[n][w];
    int64_t total_subs = B[n][t_sub];
    printf("START cell=A(%d,%d,%d) M0=%d C(n,w)=%lld C(n,t)=%lld KB=%d rmax=%d clusters=%d max4=%d pf=%.2f seed=%llu max_s=%.0f\n",
           n, d, w, M, (long long)total_words, (long long)total_subs, KB, rmax, ncluster, max4, plateau_frac, (unsigned long long)rng, max_seconds);
    fflush(stdout);

    int16_t *cnt = (int16_t *)calloc((size_t)total_words, sizeof(int16_t));
    int32_t *owner = (int32_t *)malloc((size_t)total_subs * sizeof(int32_t));
    if (!cnt || !owner) {
        fprintf(stderr, "Allocation failed\n");
        return 1;
    }

    int nthreads = 8;
    for (int i = 0; i < M; i++) {
        cnt[rank_t(words[i], nbytes)] = SENT;
    }
    parallel_update_neighbors(words, M, n, w, r, cnt, 1, nthreads);
    for (int i = 0; i < M; i++) {
        if (cnt[rank_t(words[i], nbytes)] != SENT) {
            fprintf(stderr, "INVALID seed: codeword %d conflicted with another codeword!\n", i);
            return 1;
        }
    }

    int best_M = M;
    int node_cap = 100000;

    for (int rnd = 0; rnd < max_rounds; rnd++) {
        clock_gettime(CLOCK_MONOTONIC, &ts_now);
        double elapsed = (ts_now.tv_sec - ts_start.tv_sec) + 1e-9 * (ts_now.tv_nsec - ts_start.tv_nsec);
        if (elapsed >= max_seconds) {
            printf("  [TIME CAP] Reached %.1fs at round %d.\n", elapsed, rnd);
            break;
        }
        if (switch_kb4_round >= 0 && rnd == switch_kb4_round) {
            KB = 4;
            if (rmax < 12) rmax = 12;
            plateau_frac = 0.30;
            printf("  [PHASE SWITCH] round %d: switching to deep neighborhood KB=%d rmax=%d pf=%.2f\n", rnd, KB, rmax, plateau_frac);
            fflush(stdout);
        }
        // 1. Rebuild owner table
        memset(owner, -1, (size_t)total_subs * sizeof(int32_t));
        int64_t rk_buf[256];
        int bad_owner = 0;
        for (int i = 0; i < M; i++) {
            int m = sub_ranks_g(words[i], n, w, r, rk_buf);
            for (int j = 0; j < m; j++) {
                if (owner[rk_buf[j]] != -1) bad_owner++;
                owner[rk_buf[j]] = i;
            }
        }
        if (bad_owner > 0) {
            fprintf(stderr, "ERROR: owner table collision (%d) at round %d!\n", bad_owner, rnd);
            return 1;
        }

        // 2. Parallel scan for low-blocked words
        pthread_t th[16];
        ScanJob sjobs[16];
        int64_t step = (total_words + nthreads - 1) / nthreads;
        for (int t = 0; t < nthreads; t++) {
            sjobs[t].cnt = cnt;
            sjobs[t].r0 = t * step;
            sjobs[t].r1 = (t + 1) * step < total_words ? (t + 1) * step : total_words;
            sjobs[t].n = n; sjobs[t].w = w; sjobs[t].r = r; sjobs[t].KB = KB;
            sjobs[t].owner = owner;
            sjobs[t].out = NULL; sjobs[t].count = 0; sjobs[t].cap = 0; sjobs[t].mism = 0;
            pthread_create(&th[t], NULL, scan_low_worker, &sjobs[t]);
        }
        int64_t L = 0, total_mism = 0;
        for (int t = 0; t < nthreads; t++) {
            pthread_join(th[t], NULL);
            L += sjobs[t].count;
            total_mism += sjobs[t].mism;
        }
        if (total_mism > 0) {
            fprintf(stderr, "ERROR: incremental count mismatch (%lld) at round %d!\n", (long long)total_mism, rnd);
            return 1;
        }

        LowWord *lw = (LowWord *)malloc((L + 1) * sizeof(LowWord));
        int64_t pos = 0;
        for (int t = 0; t < nthreads; t++) {
            if (sjobs[t].count > 0) {
                memcpy(&lw[pos], sjobs[t].out, sjobs[t].count * sizeof(LowWord));
                pos += sjobs[t].count;
            }
            free(sjobs[t].out);
        }

        // Random permutation of lw for tie-breaking
        for (int64_t i = L - 1; i > 0; i--) {
            int64_t j = xorshift64(&rng) % (i + 1);
            LowWord tmp = lw[i]; lw[i] = lw[j]; lw[j] = tmp;
        }
        if (L > 45000) {
            int64_t keep = 0;
            for (int64_t i = 0; i < L; i++) {
                if (lw[i].k <= 1) {
                    LowWord tmp = lw[keep]; lw[keep] = lw[i]; lw[i] = tmp;
                    keep++;
                }
            }
            if (keep < 45000) L = 45000;
            else L = (keep < 90000) ? keep : 90000;
        }

        int64_t hist[MAX_KB + 1] = {0};
        uint64_t *free0 = NULL;
        int n_free0 = 0, cap_free0 = 0;

        // Build CSR codeword -> low words it blocks, and collect blocker tuples
        int64_t *cw_deg = (int64_t *)calloc(M + 1, sizeof(int64_t));
        for (int64_t i = 0; i < L; i++) {
            int k = lw[i].k;
            hist[k]++;
            if (k == 0) {
                if (n_free0 >= cap_free0) {
                    cap_free0 = cap_free0 ? cap_free0 * 2 : 256;
                    free0 = (uint64_t *)realloc(free0, cap_free0 * sizeof(uint64_t));
                }
                free0[n_free0++] = lw[i].w;
            }
            for (int j = 0; j < k; j++) {
                cw_deg[lw[i].b[j] + 1]++;
            }
        }
        int64_t *bptr = (int64_t *)malloc((M + 1) * sizeof(int64_t));
        bptr[0] = 0;
        for (int c = 0; c < M; c++) bptr[c + 1] = bptr[c] + cw_deg[c + 1];
        int64_t *bidx = (int64_t *)malloc((bptr[M] + 1) * sizeof(int64_t));
        int64_t *bfill = (int64_t *)malloc(M * sizeof(int64_t));
        memcpy(bfill, bptr, M * sizeof(int64_t));
        for (int64_t i = 0; i < L; i++) {
            int k = lw[i].k;
            for (int j = 0; j < k; j++) {
                int32_t c = lw[i].b[j];
                bidx[bfill[c]++] = i;
            }
        }
        free(bfill);
        free(cw_deg);

        // Extract unique blocker sets of size 1..KB
        RemSet *raw_sets = (RemSet *)malloc((L + 1) * sizeof(RemSet));
        int64_t n_raw = 0;
        for (int64_t i = 0; i < L; i++) {
            if (lw[i].k >= 1) {
                raw_sets[n_raw].len = lw[i].k;
                for (int j = 0; j < lw[i].k; j++) raw_sets[n_raw].c[j] = lw[i].b[j];
                n_raw++;
            }
        }
        qsort(raw_sets, n_raw, sizeof(RemSet), cmp_remset);
        int64_t n_uniq = 0;
        for (int64_t i = 0; i < n_raw; i++) {
            if (i == 0 || cmp_remset(&raw_sets[i], &raw_sets[n_uniq - 1]) != 0) {
                raw_sets[n_uniq++] = raw_sets[i];
            }
        }

        // Build co-blocking graph CSR on codewords 0..M-1 from uniq blocker sets of size >= 2
        int64_t *adj_cnt = (int64_t *)calloc(M + 1, sizeof(int64_t));
        for (int64_t u = 0; u < n_uniq; u++) {
            int k = raw_sets[u].len;
            if (k >= 2) {
                for (int a = 0; a < k; a++) adj_cnt[raw_sets[u].c[a] + 1] += k - 1;
            }
        }
        int64_t *aptr = (int64_t *)malloc((M + 1) * sizeof(int64_t));
        aptr[0] = 0;
        for (int c = 0; c < M; c++) aptr[c + 1] = aptr[c] + adj_cnt[c + 1];
        int32_t *anbr = (int32_t *)malloc((aptr[M] + 1) * sizeof(int32_t));
        int64_t *afill = (int64_t *)malloc(M * sizeof(int64_t));
        memcpy(afill, aptr, M * sizeof(int64_t));
        for (int64_t u = 0; u < n_uniq; u++) {
            int k = raw_sets[u].len;
            if (k >= 2) {
                for (int a = 0; a < k; a++) {
                    int32_t ca = raw_sets[u].c[a];
                    for (int b = 0; b < k; b++) {
                        if (b != a) anbr[afill[ca]++] = raw_sets[u].c[b];
                    }
                }
            }
        }
        free(afill);
        free(adj_cnt);

        // Deduplicate adjacency segments and collect active nodes
        int32_t *active_nodes = (int32_t *)malloc(M * sizeof(int32_t));
        int n_active = 0;
        int64_t *aptr2 = (int64_t *)calloc(M + 1, sizeof(int64_t));
        int64_t k2 = 0;
        for (int c = 0; c < M; c++) {
            int64_t s0 = aptr[c], s1 = aptr[c + 1];
            if (s1 > s0) {
                qsort(&anbr[s0], s1 - s0, sizeof(int32_t), cmp_int32);
                int32_t last = -1;
                for (int64_t z = s0; z < s1; z++) {
                    if (anbr[z] != last) {
                        anbr[k2++] = anbr[z];
                        last = anbr[z];
                    }
                }
            }
            aptr2[c + 1] = k2;
            if (aptr2[c + 1] > aptr2[c]) active_nodes[n_active++] = c;
        }
        free(aptr);
        aptr = aptr2;

        // Assemble removal sets: all 1..3-blocker sets, up to max4 4-blocker sets, and ncluster connected clusters
        int64_t n_small = 0, n_big = 0;
        for (int64_t u = 0; u < n_uniq; u++) {
            if (raw_sets[u].len <= 3) n_small++;
            else n_big++;
        }
        int64_t cap_R = n_small + (n_big < max4 ? n_big : max4) + ncluster + 16;
        RemSet *allR = (RemSet *)malloc(cap_R * sizeof(RemSet));
        int64_t NR = 0;
        for (int64_t u = 0; u < n_uniq; u++) {
            if (raw_sets[u].len <= 3) allR[NR++] = raw_sets[u];
        }
        if (n_big > 0) {
            RemSet *big_ptr = &raw_sets[n_small];
            if (n_big > max4) {
                for (int i = 0; i < max4; i++) {
                    int64_t j = i + (xorshift64(&rng) % (n_big - i));
                    RemSet tmp = big_ptr[i]; big_ptr[i] = big_ptr[j]; big_ptr[j] = tmp;
                    allR[NR++] = big_ptr[i];
                }
            } else {
                for (int64_t i = 0; i < n_big; i++) allR[NR++] = big_ptr[i];
            }
        }
        free(raw_sets);

        // Generate random connected clusters on co-blocking graph
        int32_t front[16384];
        if (n_active > 0 && rmax >= 3) {
            for (int q = 0; q < ncluster; q++) {
                int32_t c = active_nodes[xorshift64(&rng) % n_active];
                RemSet cl;
                cl.c[0] = c;
                int nr = 1;
                int target = 3 + (int)(xorshift64(&rng) % (rmax - 2));
                int nf = 0;
                for (int64_t z = aptr[c]; z < aptr[c + 1] && nf < 16384; z++) {
                    front[nf++] = anbr[z];
                }
                while (nr < target && nf > 0) {
                    int idx = (int)(xorshift64(&rng) % nf);
                    int32_t v = front[idx];
                    front[idx] = front[--nf];
                    int inR = 0;
                    for (int e = 0; e < nr; e++) {
                        if (cl.c[e] == v) { inR = 1; break; }
                    }
                    if (inR) continue;
                    cl.c[nr++] = v;
                    for (int64_t z = aptr[v]; z < aptr[v + 1] && nf < 16384; z++) {
                        int32_t u = anbr[z];
                        int inR2 = 0;
                        for (int e = 0; e < nr; e++) {
                            if (cl.c[e] == u) { inR2 = 1; break; }
                        }
                        if (!inR2) front[nf++] = u;
                    }
                }
                cl.len = (int8_t)nr;
                for (int a = 1; a < nr; a++) {
                    int32_t x = cl.c[a];
                    int b = a - 1;
                    while (b >= 0 && cl.c[b] > x) { cl.c[b + 1] = cl.c[b]; b--; }
                    cl.c[b + 1] = x;
                }
                allR[NR++] = cl;
            }
        }
        free(active_nodes);
        free(aptr);
        free(anbr);

        // Deduplicate allR and shuffle
        qsort(allR, NR, sizeof(RemSet), cmp_remset);
        int64_t NR_u = 0;
        for (int64_t i = 0; i < NR; i++) {
            if (i == 0 || cmp_remset(&allR[i], &allR[NR_u - 1]) != 0) {
                allR[NR_u++] = allR[i];
            }
        }
        NR = NR_u;
        for (int64_t i = NR - 1; i > 0; i--) {
            int64_t j = xorshift64(&rng) % (i + 1);
            RemSet tmp = allR[i]; allR[i] = allR[j]; allR[j] = tmp;
        }

        // 4. Solve MIS for all removal sets in parallel
        int8_t *status = (int8_t *)calloc(NR + 1, sizeof(int8_t));
        int32_t *nch = (int32_t *)calloc(NR + 1, sizeof(int32_t));
        uint64_t *chosen = (uint64_t *)calloc((NR + 1) * CH_MAX, sizeof(uint64_t));
        pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
        SolveJob sjob;
        sjob.R = allR; sjob.NR = (int)NR;
        sjob.bptr = bptr; sjob.bidx = bidx; sjob.lw = lw;
        sjob.words = words; sjob.tthr = tthr; sjob.node_cap = node_cap;
        sjob.status = status; sjob.nch = nch; sjob.chosen = chosen;
        sjob.next_q = 0; sjob.mtx = &mtx;

        for (int t = 0; t < nthreads; t++) {
            pthread_create(&th[t], NULL, solve_all_worker, &sjob);
        }
        for (int t = 0; t < nthreads; t++) {
            pthread_join(th[t], NULL);
        }

        int n_imp = 0, n_pla = 0;
        int32_t *imp_idx = (int32_t *)malloc((NR + 1) * sizeof(int32_t));
        int32_t *pla_idx = (int32_t *)malloc((NR + 1) * sizeof(int32_t));
        for (int q = 0; q < NR; q++) {
            if (status[q] == 2) imp_idx[n_imp++] = q;
            else if (status[q] == 1) pla_idx[n_pla++] = q;
        }

        // 5. Apply free words, then disjoint improving moves (sorted by gain desc), else plateau moves
        uint8_t *used_cw = (uint8_t *)calloc(M, sizeof(uint8_t));
        uint64_t *ins_words = (uint64_t *)malloc((M + 4096) * sizeof(uint64_t));
        uint64_t *rem_words = (uint64_t *)malloc((M + 4096) * sizeof(uint64_t));
        int n_ins = 0, n_rem = 0, n_applied = 0;

        for (int i = 0; i < n_free0; i++) {
            uint64_t x = free0[i];
            int compat = 1;
            for (int j = 0; j < n_ins; j++) {
                if (__builtin_popcountll(x & ins_words[j]) >= tthr) { compat = 0; break; }
            }
            if (compat) {
                ins_words[n_ins++] = x;
                n_applied++;
            }
        }

        // Sort imp_idx by gain descending
        for (int a = 1; a < n_imp; a++) {
            int q = imp_idx[a];
            int gain_q = nch[q] - allR[q].len;
            int b = a - 1;
            while (b >= 0 && (nch[imp_idx[b]] - allR[imp_idx[b]].len) < gain_q) {
                imp_idx[b + 1] = imp_idx[b];
                b--;
            }
            imp_idx[b + 1] = q;
        }

        for (int a = 0; a < n_imp; a++) {
            int q = imp_idx[a];
            const RemSet *rq = &allR[q];
            int overlap = 0;
            for (int e = 0; e < rq->len; e++) {
                if (used_cw[rq->c[e]]) { overlap = 1; break; }
            }
            if (overlap) continue;
            const uint64_t *ch_q = &chosen[(int64_t)q * CH_MAX];
            int m = nch[q];
            int compat = 1;
            for (int i = 0; i < m && compat; i++) {
                for (int j = 0; j < n_ins; j++) {
                    if (__builtin_popcountll(ch_q[i] & ins_words[j]) >= tthr) { compat = 0; break; }
                }
            }
            if (!compat) continue;
            for (int e = 0; e < rq->len; e++) {
                used_cw[rq->c[e]] = 1;
                rem_words[n_rem++] = words[rq->c[e]];
            }
            for (int i = 0; i < m; i++) ins_words[n_ins++] = ch_q[i];
            n_applied++;
        }

        int net_gain = n_ins - n_rem;
        if (net_gain == 0 && n_pla > 0) {
            for (int i = n_pla - 1; i > 0; i--) {
                int j = (int)(xorshift64(&rng) % (i + 1));
                int32_t tmp = pla_idx[i]; pla_idx[i] = pla_idx[j]; pla_idx[j] = tmp;
            }
            int lim = (int)(n_pla * plateau_frac);
            if (lim < 1) lim = 1;
            for (int a = 0; a < lim; a++) {
                int q = pla_idx[a];
                const RemSet *rq = &allR[q];
                int overlap = 0;
                for (int e = 0; e < rq->len; e++) {
                    if (used_cw[rq->c[e]]) { overlap = 1; break; }
                }
                if (overlap) continue;
                const uint64_t *ch_q = &chosen[(int64_t)q * CH_MAX];
                int m = nch[q];
                int compat = 1;
                for (int i = 0; i < m && compat; i++) {
                    for (int j = 0; j < n_ins; j++) {
                        if (__builtin_popcountll(ch_q[i] & ins_words[j]) >= tthr) { compat = 0; break; }
                    }
                }
                if (!compat) continue;
                for (int e = 0; e < rq->len; e++) {
                    used_cw[rq->c[e]] = 1;
                    rem_words[n_rem++] = words[rq->c[e]];
                }
                for (int i = 0; i < m; i++) ins_words[n_ins++] = ch_q[i];
                n_applied++;
            }
        }

        // Update codewords and incremental counts
        if (n_applied > 0) {
            // Strip unchanged words present in both rem_words and ins_words
            qsort(rem_words, n_rem, sizeof(uint64_t), cmp_u64);
            qsort(ins_words, n_ins, sizeof(uint64_t), cmp_u64);
            int r_i = 0, i_i = 0, out_r = 0, out_i = 0;
            while (r_i < n_rem && i_i < n_ins) {
                if (rem_words[r_i] == ins_words[i_i]) {
                    r_i++;
                    i_i++;
                } else if (rem_words[r_i] < ins_words[i_i]) {
                    rem_words[out_r++] = rem_words[r_i++];
                } else {
                    ins_words[out_i++] = ins_words[i_i++];
                }
            }
            while (r_i < n_rem) rem_words[out_r++] = rem_words[r_i++];
            while (i_i < n_ins) ins_words[out_i++] = ins_words[i_i++];
            n_rem = out_r;
            n_ins = out_i;

            for (int i = 0; i < n_rem; i++) {
                cnt[rank_t(rem_words[i], nbytes)] = 0;
            }
            parallel_update_neighbors(rem_words, n_rem, n, w, r, cnt, -1, nthreads);
            for (int i = 0; i < n_ins; i++) {
                int64_t rk = rank_t(ins_words[i], nbytes);
                if (cnt[rk] != 0) {
                    fprintf(stderr, "ERROR: inserted word still blocked (cnt=%d)!\n", cnt[rk]);
                    return 1;
                }
                cnt[rk] = SENT;
            }
            parallel_update_neighbors(ins_words, n_ins, n, w, r, cnt, 1, nthreads);

            int new_M = 0;
            for (int i = 0; i < M; i++) {
                if (bsearch(&words[i], rem_words, n_rem, sizeof(uint64_t), cmp_u64) == NULL) {
                    words[new_M++] = words[i];
                }
            }
            for (int i = 0; i < n_ins; i++) {
                if (new_M >= cap_w) {
                    cap_w *= 2;
                    words = (uint64_t *)realloc(words, cap_w * sizeof(uint64_t));
                }
                words[new_M++] = ins_words[i];
            }
            qsort(words, new_M, sizeof(uint64_t), cmp_u64);
            // Deduplicate if any overlap between retained and inserted
            int dedup_M = 0;
            for (int i = 0; i < new_M; i++) {
                if (i == 0 || words[i] != words[dedup_M - 1]) words[dedup_M++] = words[i];
            }
            M = dedup_M;
        }

        if (M > best_M) {
            best_M = M;
            save_code_file(outdir, n, d, w, M, words);
            printf("  [NEW RECORD!] round %d: A(%d,%d,%d) >= %d (gain=+%d, low=%lld, R=%lld, imp=%d, pla=%d)\n",
                   rnd, n, d, w, M, net_gain, (long long)L, (long long)NR, n_imp, n_pla);
            fflush(stdout);
        } else if (rnd % 5 == 0 || net_gain > 0 || rnd == max_rounds - 1) {
            printf("  round %3d: M=%d best=%d gain=%d applied=%d low=%lld [0:%lld,1:%lld,2:%lld,3:%lld] R=%lld imp=%d pla=%d\n",
                   rnd, M, best_M, net_gain, n_applied, (long long)L,
                   (long long)hist[0], (long long)hist[1], (long long)hist[2], (long long)hist[3],
                   (long long)NR, n_imp, n_pla);
            fflush(stdout);
        }

        free(used_cw);
        free(ins_words);
        free(rem_words);
        free(imp_idx);
        free(pla_idx);
        free(status);
        free(nch);
        free(chosen);
        free(allR);
        free(bptr);
        free(bidx);
        free(free0);
        free(lw);

        if (n_imp == 0 && n_pla == 0 && net_gain == 0) {
            printf("  [FROZEN] No improving or plateau moves at round %d.\n", rnd);
            break;
        }
    }

    printf("DONE cell=A(%d,%d,%d) best_M=%d\n", n, d, w, best_M);
    free(owner);
    free(cnt);
    free(words);
    return 0;
}
