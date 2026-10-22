/* lsearch.c -- local search on never-condition assignments with an exact subset-DP objective
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
        double t0 = now();
        int lab[MAXN]; for (int y = 0; y < n; y++) lab[y] = y <= x ? y : y + 1;
        int xp = x + 1;
        memset(cond, 9, NT);
        for (int c = 2; c < n; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) {
            int code = old[tidx(a, b, c)]; int tri[3] = {a, b, c}; int s = code / 3, p = code % 3;
            for (int rep = 0; rep < 2; rep++) {
                if (rep == 1 && a != x && b != x && c != x) break;
                int nl[3]; for (int r = 0; r < 3; r++) nl[r] = (rep == 1 && tri[r] == x) ? xp : lab[tri[r]];
                int subj = nl[s];
                /* sort nl */
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
        if (bbcap > 0) { /* exact B&B on the mixed triples (node-capped), started from the greedy value */
            NFREE = nm; for (int i = 0; i < nm; i++) { FREE[i] = mixed[i]; BBSOL[i] = cond[mixed[i]]; }
            BBBEST = vmix; NODES = 0; NODECAP = bbcap;
            for (int i = 0; i < nm; i++) setc(FREE[i], 9);
            bb(0);
            for (int i = 0; i < nm; i++) setc(FREE[i], BBSOL[i]);
            vmix = count();
        }
        greedy_sweeps(all, NT, secs);
        u64 vall = count();
        char path[1024]; snprintf(path, sizeof path, "%s_x%d.npy", outp, x); save(path);
        printf("extend n %d->%d x %d threshold %llu mixed-greedy %llu full-greedy %llu t %.1fs\n", n, N, x, (unsigned long long)vth, vmix, vall, now() - t0);
        fflush(stdout);
    }
    return 0;
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

int main(int argc, char **argv) {
    if (argc > 1 && !strcmp(argv[1], "extend")) return do_extend(argc, argv);
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

    if (!strcmp(mode, "lnsk")) {
        /* lnsk N in.npy out SECONDS SEED OPTS NODECAP K : K = 1 star (all triples through x), K >= 2: all triples
           meeting a K-set in >= 2 points; K-sets enumerated (K <= 4) in random order, passes repeated */
        const char *outp = argv[4]; double secs = atof(argv[5]); rs ^= (u64)atoll(argv[6]) * 0x2545F4914F6CDD1DULL; rnd();
        set_opts(argv[7]); NODECAP = atol(argv[8]); int K = atoi(argv[9]);
        char path[1024]; snprintf(path, sizeof path, "%s.npy", outp);
        u64 cur = count(); double t0 = now(); long rounds = 0, full = 0;
        printf("lnsk start n %d count %llu opts %s nodecap %ld K %d\n", n, cur, argv[7], NODECAP, K); fflush(stdout);
        static int SETS[20000][4]; int ns = 0, si = 0, passimp = 0, passes = 0;
        unsigned char keep[512];
        while (now() - t0 < secs) {
            if (si >= ns) {
                if (ns > 0) { passes++; printf("pass %d done t %.0fs improved %d full-B&B %ld/%d cur %llu\n", passes, now() - t0, passimp, full, ns, cur); fflush(stdout); }
                ns = 0; full = 0;
                if (K == 1) for (int a = 0; a < N; a++) { SETS[ns][0] = a; ns++; }
                else if (K == 2) for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) { SETS[ns][0] = a; SETS[ns][1] = b; ns++; }
                else if (K == 3) for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) { SETS[ns][0] = a; SETS[ns][1] = b; SETS[ns][2] = c; ns++; }
                else for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) for (int d = c + 1; d < N && ns < 20000; d++) { SETS[ns][0] = a; SETS[ns][1] = b; SETS[ns][2] = c; SETS[ns][3] = d; ns++; }
                for (int i = ns - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); for (int q = 0; q < 4; q++) { int z = SETS[i][q]; SETS[i][q] = SETS[j][q]; SETS[j][q] = z; } }
                si = 0; passimp = 0;
            }
            int in[MAXN]; memset(in, 0, sizeof in); for (int q = 0; q < K; q++) in[SETS[si][q]] = 1; si++;
            NFREE = 0;
            for (int t = 0; t < NT; t++) { int h = in[TM[t][0]] + in[TM[t][1]] + in[TM[t][2]]; if ((K == 1 && h >= 1) || (K >= 2 && h >= 2)) FREE[NFREE++] = t; }
            for (int i = NFREE - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = FREE[i]; FREE[i] = FREE[j]; FREE[j] = z; }
            for (int i = 0; i < NFREE; i++) keep[i] = cond[FREE[i]];
            for (int i = 0; i < NFREE; i++) setc(FREE[i], 9);
            BBBEST = cur; for (int i = 0; i < NFREE; i++) BBSOL[i] = keep[i]; NODES = 0;
            bb(0); if (NODES <= NODECAP) full++;
            for (int i = 0; i < NFREE; i++) setc(FREE[i], BBSOL[i]);
            u64 v = count(); rounds++;
            if (v != BBBEST) { printf("ERROR lnsk recount %llu vs %llu\n", v, BBBEST); }
            if (v > cur) { printf("round %ld set %d %d %d %d t %.0fs nodes %ld improve %llu -> %llu\n", rounds, SETS[si-1][0], K>1?SETS[si-1][1]:-1, K>2?SETS[si-1][2]:-1, K>3?SETS[si-1][3]:-1, now() - t0, NODES, cur, v); cur = v; save(path); fflush(stdout); passimp = 1;
                int *all = malloc(sizeof(int) * NT); for (int i = 0; i < NT; i++) all[i] = i;
                long mv = greedy_sweeps(all, NT, 60); free(all); u64 v2 = count();
                if (v2 > cur) { printf("  greedy after LNS: %ld moves %llu -> %llu\n", mv, cur, v2); cur = v2; save(path); fflush(stdout); } }
        }
        printf("final lnsk %llu rounds %ld passes %d time %.0fs\n", cur, rounds, passes, now() - t0); save(path); return 0;
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
