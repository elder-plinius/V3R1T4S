/* lsx.c (lens lns-high, wave 2: adds mode dlns = sequenced pair-LNS + triple-of-alternatives LNS + kicks; based on) lsearch.c -- local search on never-condition assignments with an exact subset-DP objective
 * (lens local-search, run 2026-10-17-2220).
 *
 * Encoding (same as the prior run's cdcount.c / cdlib.py): alternatives 0..n-1, triple a<b<c has colex index
 * C(c,3)+C(b,2)+a, cond = 3*s+p, s = subject (0 a, 1 b, 2 c), p = forbidden position of the subject within the
 * triple (0 top, 1 middle, 2 bottom); paper notation iNj <=> s = i-1, p = j-1.  9 = unconstrained.
 *
 * Objective: |full domain| = number of linear orders obeying every condition, by a DP over prefix sets
 * (placing e after the set S is allowed iff no condition with subject e forbids it; this depends only on (S,e)).
 *
 * Pattern DP (the move evaluator): relax one triple t = {m0<m1<m2}, run the DP over states (S, first, second)
 * where first/second record which members of t were placed first and second.  At the full set this gives
 * C[pi] = number of orders obeying all OTHER conditions whose restriction to t is pi (6 values).  The count with
 * condition (s, p) on t is the sum of C[pi] over the pi in which member s is not at position p.  So all 9 options
 * of a triple are scored exactly by one DP.
 *
 * Search = heat-bath (Gibbs) annealing: pick a triple, score its options, sample an option with probability
 * proportional to (count/current)^(1/T); T = 0 means greedy with uniform choice among ties (neutral drift).
 * Temperature cycles geometrically T0 -> T1 over CYC moves, then the next cycle restarts from the best found
 * (with probability RESTART) or continues.
 *
 * Usage:
 *   lsearch count N in.npy
 *   lsearch enum N in.npy > orders.txt               (all orders of the full domain; count on stderr)
 *   lsearch selftest N in.npy                     (pattern DP vs plain DP on 50 random triples/options)
 *   lsearch anneal N in.npy out_prefix SECONDS SEED T0 T1 CYC OPTS [RESTART]
 *        OPTS: pp6 (xN1/xN3 for every member), pp4 (1N3,3N1,2N1,2N3), all9
 *   lsearch lns N in.npy out_prefix SECONDS SEED OPTS NODECAP [HINTS]  (pair-LNS: all n-2 triples through a pair {x,y}
 *        re-optimised by node-capped exact B&B; systematic passes over all pairs; HINTS "x,y;x,y" tried first)
 *   lsearch extend n in_n.npy out_prefix SECS_PER_X [OPTS] [XLO XHI] [BBCAP]  (clone x -> (x,x+1): thresholds, greedy on the
 *        n-1 mixed triples, then greedy on all triples for SECS_PER_X; writes out_prefix_x<x>.npy on n+1)
 * Writes out_prefix.npy (best assignment, uint8 colex) whenever the best improves, and logs to stdout.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#define MAXN 28
typedef uint32_t mask_t;
typedef unsigned long long u64;

static int N, NT;
static unsigned char *cond;
static int TM[4000][3];
static mask_t M[3][MAXN][MAXN];
static mask_t HAS[3][MAXN];
static mask_t FULL;

static long long binom(int n, int k) {
    if (k < 0 || n < k) return 0;
    long long r = 1;
    for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
    return r;
}
static int tidx(int a, int b, int c) { return (int)(binom(c, 3) + binom(b, 2) + a); }

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static u64 rs = 88172645463325252ULL;
static inline u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

/* add (sign=1) or remove (sign=0) the condition code of triple t to the masks */
static void put(int t, int code, int sign) {
    if (code >= 9) return;
    int s = code / 3, p = code % 3;
    int e = TM[t][s], x = TM[t][(s + 1) % 3], y = TM[t][(s + 2) % 3];
    if (sign) {
        M[p][e][x] |= (mask_t)1 << y; M[p][e][y] |= (mask_t)1 << x;
        HAS[p][e] |= ((mask_t)1 << x) | ((mask_t)1 << y);
    } else {
        M[p][e][x] &= ~((mask_t)1 << y); M[p][e][y] &= ~((mask_t)1 << x);
        if (!M[p][e][x]) HAS[p][e] &= ~((mask_t)1 << x);
        if (!M[p][e][y]) HAS[p][e] &= ~((mask_t)1 << y);
    }
}
static void setc(int t, int code) { put(t, cond[t], 0); cond[t] = (unsigned char)code; put(t, code, 1); }

static void build(void) {
    memset(M, 0, sizeof M); memset(HAS, 0, sizeof HAS);
    for (int t = 0; t < NT; t++) put(t, cond[t], 1);
}

static inline int valid(mask_t S, int e) {
    mask_t notS = FULL & ~S, xs;
    xs = HAS[0][e] & notS;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M[0][e][x] & notS) return 0; }
    xs = HAS[2][e] & S;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M[2][e][x] & S) return 0; }
    xs = HAS[1][e] & S;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M[1][e][x] & notS) return 0; }
    return 1;
}

/* hash table with 64-bit keys */
#define EMPTY 0xFFFFFFFFFFFFFFFFULL
typedef struct { u64 *key, *val; int *used; int cap, cnt; } HT;
static void ht_init(HT *h, int cap) {
    h->cap = cap; h->cnt = 0;
    h->key = malloc(sizeof(u64) * cap); h->val = malloc(sizeof(u64) * cap); h->used = malloc(sizeof(int) * cap);
    memset(h->key, 0xFF, sizeof(u64) * cap);
}
static void ht_clear(HT *h) { for (int i = 0; i < h->cnt; i++) h->key[h->used[i]] = EMPTY; h->cnt = 0; }
static inline unsigned hh(u64 k) { k *= 0x9E3779B97F4A7C15ULL; return (unsigned)(k >> 32); }
static void ht_add(HT *h, u64 k, u64 v);
static void ht_grow(HT *h) {
    HT g; ht_init(&g, h->cap * 2);
    for (int i = 0; i < h->cnt; i++) { int j = h->used[i]; ht_add(&g, h->key[j], h->val[j]); }
    free(h->key); free(h->val); free(h->used); *h = g;
}
static void ht_add(HT *h, u64 k, u64 v) {
    if (2 * (h->cnt + 1) > h->cap) ht_grow(h);
    unsigned m = h->cap - 1, i = hh(k) & m;
    while (h->key[i] != EMPTY && h->key[i] != k) i = (i + 1) & m;
    if (h->key[i] == EMPTY) { h->key[i] = k; h->val[i] = v; h->used[h->cnt++] = (int)i; }
    else h->val[i] += v;
}
static HT HA, HB;

static u64 count(void) {
    HT *cur = &HA, *nxt = &HB; ht_clear(cur); ht_clear(nxt);
    ht_add(cur, 0, 1);
    for (int k = 0; k < N; k++) {
        ht_clear(nxt);
        for (int i = 0; i < cur->cnt; i++) {
            int j = cur->used[i]; mask_t S = (mask_t)cur->key[j]; u64 v = cur->val[j];
            mask_t rest = FULL & ~S;
            while (rest) { int e = __builtin_ctz(rest); rest &= rest - 1; if (valid(S, e)) ht_add(nxt, S | ((mask_t)1 << e), v); }
        }
        HT *tmp = cur; cur = nxt; nxt = tmp;
    }
    u64 tot = 0;
    for (int i = 0; i < cur->cnt; i++) tot += cur->val[cur->used[i]];
    return tot;
}

/* pattern DP for triple t: C[f][s] (f,s in 0..2 member indices, f != s) */
static void pattern(int t, u64 C[3][3]) {
    int old = cond[t];
    put(t, old, 0);
    int mem[MAXN]; for (int i = 0; i < N; i++) mem[i] = -1;
    for (int r = 0; r < 3; r++) mem[TM[t][r]] = r;
    HT *cur = &HA, *nxt = &HB; ht_clear(cur); ht_clear(nxt);
    ht_add(cur, 0, 1);
    for (int k = 0; k < N; k++) {
        ht_clear(nxt);
        for (int i = 0; i < cur->cnt; i++) {
            int j = cur->used[i]; u64 key = cur->key[j]; mask_t S = (mask_t)key; u64 v = cur->val[j];
            int f = (int)((key >> 32) & 3), s = (int)((key >> 34) & 3);
            mask_t rest = FULL & ~S;
            while (rest) {
                int e = __builtin_ctz(rest); rest &= rest - 1;
                if (!valid(S, e)) continue;
                u64 nk = (u64)(S | ((mask_t)1 << e));
                int nf = f, ns = s;
                if (mem[e] >= 0) { if (!f) nf = mem[e] + 1; else if (!s) ns = mem[e] + 1; }
                nk |= ((u64)nf << 32) | ((u64)ns << 34);
                ht_add(nxt, nk, v);
            }
        }
        HT *tmp = cur; cur = nxt; nxt = tmp;
    }
    memset(C, 0, sizeof(u64) * 9);
    for (int i = 0; i < cur->cnt; i++) {
        u64 key = cur->key[cur->used[i]];
        int f = (int)((key >> 32) & 3), s = (int)((key >> 34) & 3);
        C[f - 1][s - 1] += cur->val[cur->used[i]];
    }
    put(t, old, 1);
}
/* count with option code on t, from the pattern counts */
static u64 optcount(u64 C[3][3], int code) {
    if (code >= 9) { u64 s = 0; for (int f = 0; f < 3; f++) for (int g = 0; g < 3; g++) if (f != g) s += C[f][g]; return s; }
    int sub = code / 3, p = code % 3; u64 s = 0;
    for (int f = 0; f < 3; f++) for (int g = 0; g < 3; g++) {
        if (f == g) continue;
        int th = 3 - f - g; int pos = (sub == f) ? 0 : (sub == g ? 1 : 2);
        (void)th;
        if (pos != p) s += C[f][g];
    }
    return s;
}

static int OPTS[9], NOPT;
static void set_opts(const char *s) {
    if (!strcmp(s, "pp6")) { int o[] = {0, 2, 3, 5, 6, 8}; NOPT = 6; memcpy(OPTS, o, sizeof o); }
    else if (!strcmp(s, "pp4")) { int o[] = {2, 3, 5, 6}; NOPT = 4; memcpy(OPTS, o, sizeof o); }
    else { NOPT = 9; for (int i = 0; i < 9; i++) OPTS[i] = i; }
}

static void load(const char *path) {
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    unsigned char hdr[10]; if (fread(hdr, 1, 10, f) != 10) exit(2);
    int hl = hdr[8] | (hdr[9] << 8); fseek(f, 10 + hl, SEEK_SET);
    cond = malloc(NT); if ((int)fread(cond, 1, NT, f) != NT) { fprintf(stderr, "short file\n"); exit(3); }
    fclose(f);
}
static void save(const char *path) {
    char tmp[1024]; snprintf(tmp, sizeof tmp, "%s.tmp", path);
    FILE *f = fopen(tmp, "wb");
    char h[128]; int l = snprintf(h, sizeof h, "{'descr': '|u1', 'fortran_order': False, 'shape': (%d,), }", NT);
    int tot = 10 + l + 1; int pad = (64 - tot % 64) % 64;
    fwrite("\x93NUMPY\x01\x00", 1, 8, f);
    int hl = l + pad + 1; unsigned char b[2] = {(unsigned char)(hl & 255), (unsigned char)(hl >> 8)}; fwrite(b, 1, 2, f);
    fwrite(h, 1, l, f); for (int i = 0; i < pad; i++) fputc(' ', f); fputc('\n', f);
    fwrite(cond, 1, NT, f); fclose(f); rename(tmp, path);
}

static void init(int n) {
    N = n; NT = (int)binom(n, 3); FULL = (n == 32) ? 0xFFFFFFFFu : (((mask_t)1 << n) - 1);
    for (int c = 2; c < n; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) {
        int t = tidx(a, b, c); TM[t][0] = a; TM[t][1] = b; TM[t][2] = c;
    }
    ht_init(&HA, 1 << 12); ht_init(&HB, 1 << 12);
}

/* ---------- pair LNS: re-optimise all triples through a pair {x,y} by exact DFS B&B ---------- */
static int FREE[512], NFREE; static u64 BBBEST; static unsigned char BBSOL[512]; static long NODES, NODECAP;
static void bb(int i) {
    if (NODES++ > NODECAP) return;
    if (i == NFREE) { u64 v = count(); if (v > BBBEST) { BBBEST = v; for (int k = 0; k < NFREE; k++) BBSOL[k] = cond[FREE[k]]; } return; }
    int t = FREE[i];
    /* children bounds: triples i+1.. are relaxed (9), so the pattern DP on t gives exact upper bounds */
    u64 C[3][3]; pattern(t, C);
    u64 ub[9]; int ord[9];
    for (int o = 0; o < NOPT; o++) { ub[o] = optcount(C, OPTS[o]); ord[o] = o; }
    for (int a = 0; a < NOPT; a++) for (int b = a + 1; b < NOPT; b++) if (ub[ord[b]] > ub[ord[a]]) { int z = ord[a]; ord[a] = ord[b]; ord[b] = z; }
    for (int a = 0; a < NOPT; a++) {
        int o = ord[a]; if (ub[o] <= BBBEST) break;
        setc(t, OPTS[o]);
        if (i + 1 == NFREE) { if (ub[o] > BBBEST) { BBBEST = ub[o]; for (int k = 0; k < NFREE; k++) BBSOL[k] = cond[FREE[k]]; } }
        else bb(i + 1);
        if (NODES > NODECAP) break;
    }
    setc(t, 9);
}


/* ---------- extend: clone x into (x, x+1), complete mixed triples, polish ---------- */
static long greedy_sweeps(int *tl, int nt, double tmax) {
    /* sweeps over the listed triples, strict improvements only, until none or time */
    double t0 = now(); long moves = 0; int imp = 1;
    while (imp && now() - t0 < tmax) {
        imp = 0;
        for (int i = 0; i < nt; i++) {
            int t = tl[i]; u64 C[3][3]; pattern(t, C);
            u64 cv = optcount(C, cond[t]); int bo = -1;
            for (int o = 0; o < NOPT; o++) { u64 v = optcount(C, OPTS[o]); if (v > cv) { cv = v; bo = o; } }
            if (bo >= 0) { setc(t, OPTS[bo]); imp = 1; moves++; }
        }
    }
    return moves;
}
/* clone x of the n-assignment old (colex on n) into (x, x+1) on N = n+1 (init(n+1) must be done; cond has NT bytes):
   thresholds, greedy on the n-1 mixed triples, node-capped exact B&B on them, greedy on all triples for secs */
static void extend_one(int n, const unsigned char *old, int x, long bbcap, double secs, int *all, u64 *vth_, u64 *vmix_, u64 *vall_) {
        int lab[MAXN]; for (int y = 0; y < n; y++) lab[y] = y <= x ? y : y + 1;
        int xp = x + 1;
        memset(cond, 9, NT);
        for (int c = 2; c < n; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) {
            int code = old[tidx(a, b, c)]; int tri[3] = {a, b, c}; int s = code / 3, p = code % 3;
            for (int rep = 0; rep < 2; rep++) {
                if (rep == 1 && a != x && b != x && c != x) break;
                int nl[3]; for (int r = 0; r < 3; r++) nl[r] = (rep == 1 && tri[r] == x) ? xp : lab[tri[r]];
                int subj = nl[s];
                int u[3] = {nl[0], nl[1], nl[2]}, z;
                if (u[0] > u[1]) { z = u[0]; u[0] = u[1]; u[1] = z; } if (u[1] > u[2]) { z = u[1]; u[1] = u[2]; u[2] = z; } if (u[0] > u[1]) { z = u[0]; u[0] = u[1]; u[1] = z; }
                int si = (u[0] == subj) ? 0 : (u[1] == subj ? 1 : 2);
                cond[tidx(u[0], u[1], u[2])] = (unsigned char)(3 * si + p);
            }
        }
        int mixed[MAXN], cyT[MAXN], cxB[MAXN], nm = 0;
        for (int k = 0; k < N; k++) if (k != x && k != xp) {
            int u0, u1, u2;
            if (k < x) { u0 = k; u1 = x; u2 = xp; } else { u0 = x; u1 = xp; u2 = k; }
            int t = tidx(u0, u1, u2); mixed[nm] = t;
            int iy = (u0 == xp) ? 0 : (u1 == xp ? 1 : 2), ix = (u0 == x) ? 0 : (u1 == x ? 1 : 2);
            cyT[nm] = 3 * iy + 0; cxB[nm] = 3 * ix + 2; nm++;
        }
        build();
        u64 best = 0; int bt = 0;
        for (int th = 0; th <= nm; th++) {
            for (int i = 0; i < nm; i++) setc(mixed[i], i < th ? cyT[i] : cxB[i]);
            u64 v = count(); if (v > best) { best = v; bt = th; }
        }
        for (int i = 0; i < nm; i++) setc(mixed[i], i < bt ? cyT[i] : cxB[i]);
        u64 vth = count();
        greedy_sweeps(mixed, nm, 1e9);
        u64 vmix = count();
        if (bbcap > 0) {
            NFREE = nm; for (int i = 0; i < nm; i++) { FREE[i] = mixed[i]; BBSOL[i] = cond[mixed[i]]; }
            BBBEST = vmix; NODES = 0; NODECAP = bbcap;
            for (int i = 0; i < nm; i++) setc(FREE[i], 9);
            bb(0);
            for (int i = 0; i < nm; i++) setc(FREE[i], BBSOL[i]);
            vmix = count();
        }
        greedy_sweeps(all, NT, secs);
        *vth_ = vth; *vmix_ = vmix; *vall_ = count();
}
static int do_extend(int argc, char **argv) {
    int n = atoi(argv[2]); const char *outp = argv[4]; double secs = atof(argv[5]); set_opts(argc > 6 ? argv[6] : "pp6");
    int xlo = argc > 7 ? atoi(argv[7]) : 0, xhi = argc > 8 ? atoi(argv[8]) : n - 1; long bbcap = argc > 9 ? atol(argv[9]) : 0;
    int NTo = (int)binom(n, 3);
    unsigned char *old = malloc(NTo);
    { FILE *f = fopen(argv[3], "rb"); unsigned char hdr[10]; if (fread(hdr, 1, 10, f) != 10) return 2; int hl = hdr[8] | (hdr[9] << 8);
      fseek(f, 10 + hl, SEEK_SET); if ((int)fread(old, 1, NTo, f) != NTo) return 3; fclose(f); }
    init(n + 1); cond = malloc(NT);
    int *all = malloc(sizeof(int) * NT); for (int i = 0; i < NT; i++) all[i] = i;
    for (int x = xlo; x <= xhi; x++) {
        double t0 = now(); u64 vth, vmix, vall;
        extend_one(n, old, x, bbcap, secs, all, &vth, &vmix, &vall);
        char path[1024]; snprintf(path, sizeof path, "%s_x%d.npy", outp, x); save(path);
        printf("extend n %d->%d x %d threshold %llu mixed-greedy %llu full-greedy %llu t %.1fs\n", n, N, x, (unsigned long long)vth, vmix, vall, now() - t0);
        fflush(stdout);
    }
    return 0;
}

/* restrict the n-assignment src to [n] \ {v} (colex on n-1) */
static void restrict_to(int n, const unsigned char *src, int v, unsigned char *dst) {
    for (int c = 2; c < n - 1; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) {
        int A = a < v ? a : a + 1, B = b < v ? b : b + 1, C = c < v ? c : c + 1;
        dst[tidx(a, b, c)] = src[tidx(A, B, C)];
    }
}
/* restrict N in.npy out_prefix : count the full domain of every one-alternative deletion; save the best (n-1) */
static int do_restrict(int argc, char **argv) {
    int n = atoi(argv[2]); init(n); load(argv[3]); unsigned char *orig = malloc(NT); memcpy(orig, cond, NT);
    build(); u64 c0 = count();
    init(n - 1); unsigned char *r = malloc(NT), *best = malloc(NT); u64 bv = 0; int bvv = -1;
    for (int v = 0; v < n; v++) {
        restrict_to(n, orig, v, r); memcpy(cond, r, NT); build(); u64 c = count();
        printf("restrict n %d (count %llu) delete %d -> n %d count %llu\n", n, c0, v, n - 1, c); fflush(stdout);
        if (c > bv) { bv = c; bvv = v; memcpy(best, r, NT); }
        if (argc > 5) { char pth[1024]; snprintf(pth, sizeof pth, "%s_v%d.npy", argv[4], v); save(pth); } /* keep every deletion */
    }
    memcpy(cond, best, NT); char path[1024]; snprintf(path, sizeof path, "%s.npy", argv[4]); save(path);
    printf("best restrict delete %d count %llu saved %s\n", bvv, bv, path); return 0;
}
/* restrict2 N in.npy out_prefix K : all ordered pairs of deletions (n -> n-2); save the K best distinct counts as
   out_prefix_k<i>.npy and print them */
static int do_restrict2(int argc, char **argv) {
    int n = atoi(argv[2]); int K = argc > 5 ? atoi(argv[5]) : 3; if (K > 16) K = 16;
    init(n); load(argv[3]); unsigned char *orig = malloc(NT); memcpy(orig, cond, NT);
    int NT1 = (int)binom(n - 1, 3); unsigned char *r1 = malloc(NT1);
    init(n - 2); unsigned char *r2 = malloc(NT); unsigned char *keep[16]; u64 kv[16]; int ka[16], kb[16], nk = 0;
    for (int i = 0; i < K; i++) keep[i] = malloc(NT);
    for (int v1 = 0; v1 < n; v1++) {
        restrict_to(n, orig, v1, r1);
        for (int v2 = 0; v2 < n - 1; v2++) {
            restrict_to(n - 1, r1, v2, r2); memcpy(cond, r2, NT); build(); u64 c = count();
            int dup = 0; for (int i = 0; i < nk; i++) if (kv[i] == c) dup = 1;
            if (dup) continue;
            if (nk < K || c > kv[nk - 1]) {
                int pos = nk < K ? nk++ : nk - 1;
                while (pos > 0 && kv[pos - 1] < c) { kv[pos] = kv[pos - 1]; ka[pos] = ka[pos - 1]; kb[pos] = kb[pos - 1]; memcpy(keep[pos], keep[pos - 1], NT); pos--; }
                kv[pos] = c; ka[pos] = v1; kb[pos] = v2; memcpy(keep[pos], r2, NT);
            }
        }
    }
    for (int i = 0; i < nk; i++) {
        memcpy(cond, keep[i], NT); char pth[1024]; snprintf(pth, sizeof pth, "%s_k%d.npy", argv[4], i); save(pth);
        printf("restrict2 n %d -> n %d rank %d delete %d then %d count %llu file %s\n", n, n - 2, i, ka[i], kb[i], kv[i], pth);
    }
    return 0;
}
/* rr N in.npy out_prefix SECS SEED BBCAP GSECS XW : ruin and recreate.  For deleted v (random order) and clone x in
   [(n-1)/2 - XW, (n-1)/2 + XW]: restrict to [n]\{v}, clone x back to n alternatives (extend_one), compare with the
   start; save the best n-assignment found as out_prefix.npy (and print every value). */
static int do_rr(int argc, char **argv) {
    int n = atoi(argv[2]); init(n); load(argv[3]); build(); set_opts("pp6");
    const char *outp = argv[4]; double secs = atof(argv[5]); rs ^= (u64)atoll(argv[6]) * 0x2545F4914F6CDD1DULL; rnd();
    long bbcap = atol(argv[7]); double gsecs = atof(argv[8]); int xw = atoi(argv[9]);
    unsigned char *orig = malloc(NT); memcpy(orig, cond, NT); u64 c0 = count(), bv = c0;
    unsigned char *best = malloc(NT); memcpy(best, orig, NT);
    int NTm = (int)binom(n - 1, 3); unsigned char *r = malloc(NTm);
    int *all = malloc(sizeof(int) * NT); for (int i = 0; i < NT; i++) all[i] = i;
    int vs[MAXN]; for (int i = 0; i < n; i++) vs[i] = i;
    for (int i = n - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = vs[i]; vs[i] = vs[j]; vs[j] = z; }
    double t0 = now(); char path[1024]; snprintf(path, sizeof path, "%s.npy", outp);
    printf("rr start n %d count %llu\n", n, c0); fflush(stdout);
    for (int vi = 0; vi < n && now() - t0 < secs; vi++) {
        int v = vs[vi]; restrict_to(n, orig, v, r);
        int m = n - 1, xlo = m / 2 - xw, xhi = m / 2 + xw; if (xlo < 0) xlo = 0; if (xhi > m - 1) xhi = m - 1;
        for (int x = xlo; x <= xhi && now() - t0 < secs; x++) {
            u64 vth, vmix, vall; extend_one(m, r, x, bbcap, gsecs, all, &vth, &vmix, &vall);
            printf("rr delete %d clone %d mixed %llu full-greedy %llu%s t %.0fs\n", v, x, vmix, vall, vall > bv ? " BEST" : "", now() - t0); fflush(stdout);
            if (vall > bv) { bv = vall; memcpy(best, cond, NT); memcpy(cond, best, NT); save(path); }
        }
    }
    memcpy(cond, best, NT); build(); u64 chk = count(); save(path);
    printf("final rr %llu (start %llu) recount %llu time %.0fs\n", bv, c0, chk, now() - t0); return 0;
}

/* ---------- enum: write every order of the full domain to stdout (1-based, best first) ---------- */
static int ORDV[MAXN]; static u64 NOUT; static char *OBUF; static size_t OPOS;
static void edfs(mask_t S, int k) {
    if (k == N) {
        for (int i = 0; i < N; i++) { int v = ORDV[i] + 1; if (i) OBUF[OPOS++] = ' '; if (v >= 10) OBUF[OPOS++] = (char)('0' + v / 10); OBUF[OPOS++] = (char)('0' + v % 10); }
        OBUF[OPOS++] = '\n'; NOUT++;
        if (OPOS > (1 << 22)) { fwrite(OBUF, 1, OPOS, stdout); OPOS = 0; }
        return;
    }
    mask_t rest = FULL & ~S;
    while (rest) { int e = __builtin_ctz(rest); rest &= rest - 1; if (valid(S, e)) { ORDV[k] = e; edfs(S | ((mask_t)1 << e), k + 1); } }
}


/* ---------- dlns (lens lns-high): sequenced pair-LNS to a pair local optimum, then triple-of-alternatives LNS ---------- */
static void sort3(int *a, int *b, int *c) { int z; if (*a > *b) { z = *a; *a = *b; *b = z; } if (*b > *c) { z = *b; *b = *c; *c = z; } if (*a > *b) { z = *a; *a = *b; *b = z; } }
static void free_pair(int x, int y) {
    NFREE = 0;
    for (int k = 0; k < N; k++) if (k != x && k != y) { int a = x, b = y, c = k; sort3(&a, &b, &c); FREE[NFREE++] = tidx(a, b, c); }
}
static void free_tri(int x, int y, int z) {
    /* all triples with >= 2 members in {x,y,z}: 3(n-3)+1 */
    NFREE = 0; int P[3][2] = {{x, y}, {x, z}, {y, z}};
    for (int q = 0; q < 3; q++) for (int k = 0; k < N; k++) if (k != x && k != y && k != z) { int a = P[q][0], b = P[q][1], c = k; sort3(&a, &b, &c); FREE[NFREE++] = tidx(a, b, c); }
    { int a = x, b = y, c = z; sort3(&a, &b, &c); FREE[NFREE++] = tidx(a, b, c); }
}
static u64 run_free(u64 cur, long cap) {
    unsigned char keep[512];
    for (int i = NFREE - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = FREE[i]; FREE[i] = FREE[j]; FREE[j] = z; }
    for (int i = 0; i < NFREE; i++) keep[i] = cond[FREE[i]];
    for (int i = 0; i < NFREE; i++) setc(FREE[i], 9);
    BBBEST = cur; for (int i = 0; i < NFREE; i++) BBSOL[i] = keep[i]; NODES = 0; NODECAP = cap;
    bb(0);
    for (int i = 0; i < NFREE; i++) setc(FREE[i], BBSOL[i]);
    u64 v = count();
    if (v != BBBEST) printf("ERROR recount %llu vs %llu\n", v, BBBEST);
    return v;
}
static int do_dlns(int argc, char **argv) {
    /* dlns N in.npy out_prefix SECONDS SEED OPTS PAIRCAP TRICAP */
    int n = atoi(argv[2]); init(n); load(argv[3]); build();
    const char *outp = argv[4]; double secs = atof(argv[5]); rs ^= (u64)atoll(argv[6]) * 0x2545F4914F6CDD1DULL; rnd();
    set_opts(argv[7]); long pcap = atol(argv[8]), tcap = atol(argv[9]);
    char path[1024]; snprintf(path, sizeof path, "%s.npy", outp);
    int *all = malloc(sizeof(int) * NT); for (int i = 0; i < NT; i++) all[i] = i;
    u64 cur = count(); double t0 = now(), tlog = t0;
    printf("dlns start n %d count %llu opts %s paircap %ld tricap %ld\n", n, cur, argv[7], pcap, tcap); fflush(stdout);
    int NP = N * (N - 1) / 2; int PA[400], PB[400], perm[400], stk[400], nst = 0; long stamp[400], capd[400], escd[400]; long impc = 0;
    long ncapped = 0, nesc = 0; long ecap = pcap * 8;
    static int pid[MAXN][MAXN];
    int k = 0; for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) { PA[k] = a; PB[k] = b; pid[a][b] = pid[b][a] = k; stamp[k] = -1; capd[k] = -1; escd[k] = -1; perm[k] = k; k++; }
    for (int i = NP - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = perm[i]; perm[i] = perm[j]; perm[j] = z; }
    int pos = 0; long prounds = 0, trounds = 0, tnodes = 0; int atopt = 0;
    save(path);
    while (now() - t0 < secs) {
        int c = -1;
        while (nst > 0) { int q = stk[--nst]; if (stamp[q] != impc) { c = q; break; } }
        if (c < 0) for (int s = 0; s < NP; s++) { int q = perm[(pos + s) % NP]; if (stamp[q] != impc) { c = q; pos = (pos + s + 1) % NP; break; } }
        int changed[3], nch = 0, esc = 0;
        if (c < 0) { /* escalation: re-try the pairs whose B&B hit the cap in this epoch, with 8x the cap */
            for (int q = 0; q < NP; q++) if (capd[q] == impc && escd[q] != impc) { c = q; esc = 1; break; }
        }
        if (c >= 0) {
            long cp = esc ? ecap : pcap;
            if (esc) { escd[c] = impc; nesc++; } else stamp[c] = impc;
            int x = PA[c], y = PB[c]; free_pair(x, y); u64 v = run_free(cur, cp); prounds++;
            if (!esc && NODES > cp) { capd[c] = impc; ncapped++; }
            if (v > cur) { printf("pair %d %d%s t %.0fs nodes %ld improve %llu -> %llu\n", x, y, esc ? " (escalated cap)" : "", now() - t0, NODES, cur, v); cur = v; changed[0] = x; changed[1] = y; nch = 2; }
        } else {
            if (!atopt) { printf("pair-LNS local optimum %llu (cap %ld, capped pairs re-tried with cap %ld) t %.0fs pair rounds %ld capped %ld escalated %ld\n", cur, pcap, ecap, now() - t0, prounds, ncapped, nesc); fflush(stdout); atopt = 1; }
            int x = (int)(rnd() % N), y, z; do y = (int)(rnd() % N); while (y == x); do z = (int)(rnd() % N); while (z == x || z == y);
            free_tri(x, y, z); u64 v = run_free(cur, tcap); trounds++; tnodes += NODES;
            if (v > cur) { printf("triple %d %d %d t %.0fs nodes %ld improve %llu -> %llu\n", x, y, z, now() - t0, NODES, cur, v); cur = v; changed[0] = x; changed[1] = y; changed[2] = z; nch = 3; }
        }
        if (nch) {
            save(path);
            long mv = greedy_sweeps(all, NT, 60); u64 v2 = count();
            if (v2 > cur) { printf("  greedy %ld moves %llu -> %llu\n", mv, cur, v2); cur = v2; save(path); }
            fflush(stdout); impc++; atopt = 0; nst = 0;
            for (int q = nch - 1; q >= 0; q--) for (int kk = N - 1; kk >= 0; kk--) if (kk != changed[q]) stk[nst++ % 400] = pid[changed[q]][kk];
            if (nst > 400) nst = 400;
        }
        if (now() - tlog > 30) { tlog = now(); printf("t %.0fs pair rounds %ld triple rounds %ld (nodes %ld) cur %llu\n", now() - t0, prounds, trounds, tnodes, cur); fflush(stdout); }
    }
    printf("final dlns %llu pair rounds %ld triple rounds %ld time %.0fs\n", cur, prounds, trounds, now() - t0); save(path); return 0;
}

int main(int argc, char **argv) {
    if (argc > 1 && !strcmp(argv[1], "extend")) return do_extend(argc, argv);
    if (argc > 1 && !strcmp(argv[1], "dlns")) return do_dlns(argc, argv);
    if (argc > 1 && !strcmp(argv[1], "restrict")) return do_restrict(argc, argv);
    if (argc > 1 && !strcmp(argv[1], "rr")) return do_rr(argc, argv);
    if (argc > 1 && !strcmp(argv[1], "restrict2")) return do_restrict2(argc, argv);
    if (argc < 4) { fprintf(stderr, "usage: see header\n"); return 1; }
    const char *mode = argv[1]; int n = atoi(argv[2]); init(n); load(argv[3]); build();
    if (!strcmp(mode, "enum")) { OBUF = malloc((1 << 22) + 4096); OPOS = 0; edfs(0, 0); fwrite(OBUF, 1, OPOS, stdout); fflush(stdout);
        fprintf(stderr, "enum n %d orders %llu (DP count %llu)\n", n, NOUT, count()); return 0; }
    if (!strcmp(mode, "count")) { double t0 = now(); u64 v = count(); printf("n %d count %llu time %.4fs\n", n, v, now() - t0); return 0; }
    if (!strcmp(mode, "selftest")) {
        u64 base = count(); int bad = 0;
        for (int r = 0; r < 50; r++) {
            int t = (int)(rnd() % NT); u64 C[3][3]; pattern(t, C);
            if (optcount(C, cond[t]) != base) { bad++; printf("mismatch current t %d\n", t); }
            int o = (int)(rnd() % 10); int old = cond[t]; setc(t, o); u64 v = count(); setc(t, old);
            if (v != optcount(C, o)) { bad++; printf("mismatch t %d opt %d plain %llu pattern %llu\n", t, o, v, optcount(C, o)); }
        }
        printf("selftest n %d base %llu mismatches %d\n", n, base, bad); return bad != 0;
    }
    if (!strcmp(mode, "anneal")) {
        const char *outp = argv[4]; double secs = atof(argv[5]); rs ^= (u64)atoll(argv[6]) * 0x2545F4914F6CDD1DULL; rnd();
        double T0 = atof(argv[7]), T1 = atof(argv[8]); long CYC = atol(argv[9]); set_opts(argv[10]);
        double prest = argc > 11 ? atof(argv[11]) : 1.0;
        char path[1024]; snprintf(path, sizeof path, "%s.npy", outp);
        unsigned char *best = malloc(NT); memcpy(best, cond, NT);
        u64 cur = count(), bestv = cur; double t0 = now(), tlog = t0;
        printf("start n %d count %llu opts %s T0 %g T1 %g cyc %ld\n", n, cur, argv[10], T0, T1, CYC); fflush(stdout);
        long it = 0; int cyc = 0;
        while (now() - t0 < secs) {
            double frac = (double)(it % CYC) / CYC;
            double T = (T0 > 0) ? T0 * pow(T1 / T0, frac) : 0;
            if (it % CYC == 0 && it > 0) {
                cyc++;
                if (urand() < prest) { memcpy(cond, best, NT); build(); cur = bestv; }
                printf("cycle %d t %.0fs cur %llu best %llu\n", cyc, now() - t0, cur, bestv); fflush(stdout);
            }
            it++;
            int t = (int)(rnd() % NT); u64 C[3][3]; pattern(t, C);
            u64 cv[9]; double w[9], ws = 0; u64 mx = 0;
            for (int o = 0; o < NOPT; o++) { cv[o] = optcount(C, OPTS[o]); if (cv[o] > mx) mx = cv[o]; }
            int pick = -1;
            if (T <= 0) {
                int nt = 0; for (int o = 0; o < NOPT; o++) if (cv[o] == mx) nt++;
                int r = (int)(rnd() % nt); for (int o = 0; o < NOPT; o++) if (cv[o] == mx && r-- == 0) { pick = o; break; }
            } else {
                for (int o = 0; o < NOPT; o++) { w[o] = cv[o] ? exp(log((double)cv[o] / (double)mx) / T) : 0; ws += w[o]; }
                double r = urand() * ws; for (int o = 0; o < NOPT; o++) { r -= w[o]; if (r <= 0) { pick = o; break; } }
                if (pick < 0) pick = NOPT - 1;
            }
            if (OPTS[pick] != cond[t]) { setc(t, OPTS[pick]); }
            cur = cv[pick];
            if (cur > bestv) { bestv = cur; memcpy(best, cond, NT); save(path); }
            if (now() - tlog > 30) { tlog = now(); printf("it %ld t %.0fs T %.2e cur %llu best %llu\n", it, now() - t0, T, cur, bestv); fflush(stdout); }
        }
        memcpy(cond, best, NT); build(); u64 chk = count();
        printf("final best %llu recount %llu iters %ld time %.0fs\n", bestv, chk, it, now() - t0);
        save(path); return 0;
    }
    if (!strcmp(mode, "lns")) {
        const char *outp = argv[4]; double secs = atof(argv[5]); rs ^= (u64)atoll(argv[6]) * 0x2545F4914F6CDD1DULL; rnd();
        set_opts(argv[7]); NODECAP = atol(argv[8]);
        char path[1024]; snprintf(path, sizeof path, "%s.npy", outp);
        u64 cur = count(); double t0 = now(); long rounds = 0;
        printf("lns start n %d count %llu opts %s nodecap %ld\n", n, cur, argv[7], NODECAP); fflush(stdout);
        /* systematic passes over all pairs in random order; optional hint pairs first (argv[9] = "x,y;x,y") */
        int PX[1000], PY[1000], np_ = 0, pi = 0, nh = 0, passimp = 0;
        if (argc > 9) { const char *h = argv[9]; while (*h) { int a, b; if (sscanf(h, "%d,%d", &a, &b) == 2) { PX[nh] = a; PY[nh] = b; nh++; } while (*h && *h != ';') h++; if (*h) h++; } }
        np_ = nh;
        while (now() - t0 < secs) {
            if (pi >= np_) {
                if (np_ > nh && !passimp && rounds > 0) { printf("pass without improvement: pair-LNS local optimum (within node cap)\n"); fflush(stdout); }
                np_ = 0; for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) { PX[np_] = a; PY[np_] = b; np_++; }
                for (int i = np_ - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = PX[i]; PX[i] = PX[j]; PX[j] = z; z = PY[i]; PY[i] = PY[j]; PY[j] = z; }
                pi = 0; passimp = 0;
            }
            int x = PX[pi], y = PY[pi]; pi++; if (x == y || x >= N || y >= N) continue;
            NFREE = 0; unsigned char keep[512];
            for (int k = 0; k < N; k++) if (k != x && k != y) {
                int a = x, b = y, c = k, z;
                if (a > b) { z = a; a = b; b = z; } if (b > c) { z = b; b = c; c = z; } if (a > b) { z = a; a = b; b = z; }
                FREE[NFREE++] = tidx(a, b, c);
            }
            /* random order of the free triples */
            for (int i = NFREE - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = FREE[i]; FREE[i] = FREE[j]; FREE[j] = z; }
            for (int i = 0; i < NFREE; i++) keep[i] = cond[FREE[i]];
            for (int i = 0; i < NFREE; i++) setc(FREE[i], 9);
            BBBEST = cur; for (int i = 0; i < NFREE; i++) BBSOL[i] = keep[i]; NODES = 0;
            bb(0);
            for (int i = 0; i < NFREE; i++) setc(FREE[i], BBSOL[i]);
            u64 v = count(); rounds++;
            if (v != BBBEST) { printf("ERROR lns recount %llu vs %llu\n", v, BBBEST); }
            if (v > cur) { printf("round %ld pair %d %d t %.0fs nodes %ld improve %llu -> %llu\n", rounds, x, y, now() - t0, NODES, cur, v); cur = v; save(path); fflush(stdout); passimp = 1;
                /* after an improvement: greedy single-triple sweeps on all triples */
                int *all = malloc(sizeof(int) * NT); for (int i = 0; i < NT; i++) all[i] = i;
                long mv = greedy_sweeps(all, NT, 60); free(all); u64 v2 = count();
                if (v2 > cur) { printf("  greedy after LNS: %ld moves %llu -> %llu\n", mv, cur, v2); cur = v2; save(path); fflush(stdout); } }
            else if (rounds % 20 == 0) { printf("round %ld t %.0fs nodes %ld cur %llu\n", rounds, now() - t0, NODES, cur); fflush(stdout); }
        }
        printf("final lns %llu rounds %ld time %.0fs\n", cur, rounds, now() - t0); save(path); return 0;
    }
    return 1;
}
