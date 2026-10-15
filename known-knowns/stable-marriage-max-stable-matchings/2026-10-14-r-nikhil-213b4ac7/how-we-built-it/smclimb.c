/* smclimb.c: exact counter of stable matchings (rotation-lattice walk from the man-optimal matching,
   Gusfield & Irving 1989 ch. 2-3: the cycles of next_M are the rotations exposed in M; eliminating one gives a
   stable matching; every stable matching is reached from M0; a hash set deduplicates) plus an iterated local search
   over preference profiles.  Written for V3R1T4S lane A, 2026-10-14.  n <= 16.
   Usage: smclimb count FILE [verify]      (verify=1 re-checks every visited matching against the definition)
          smclimb climb N SEEDFILE|random RNGSEED SECONDS OUTPREFIX [KICKEVALS] [KMAX]
   v2 (15:29 UTC): kick = restart from the best with 1..KMAX forced random moves (v1 used 2..6; too destructive).
   Prefs file: 2n lines, men's lists (women 1..n best first) then women's lists (men 1..n); '#' lines are comments. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#define MAXN 16
typedef struct { int n; int mpref[MAXN][MAXN], wpref[MAXN][MAXN], mrank[MAXN][MAXN], wrank[MAXN][MAXN]; } Inst;

static void build_ranks(Inst *I) {
    for (int m = 0; m < I->n; m++) for (int p = 0; p < I->n; p++) I->mrank[m][I->mpref[m][p]] = p;
    for (int w = 0; w < I->n; w++) for (int p = 0; p < I->n; p++) I->wrank[w][I->wpref[w][p]] = p;
}
static int check_perms(const Inst *I) {
    for (int s = 0; s < 2; s++) for (int i = 0; i < I->n; i++) {
        int seen[MAXN] = {0};
        for (int p = 0; p < I->n; p++) { int x = s ? I->wpref[i][p] : I->mpref[i][p]; if (x < 0 || x >= I->n || seen[x]) return 0; seen[x] = 1; }
    }
    return 1;
}
static int read_prefs(const char *path, Inst *I) {
    FILE *f = fopen(path, "r"); if (!f) { perror(path); return 0; }
    char line[4096]; int rows = 0, n = -1; int grid[2 * MAXN][MAXN];
    while (fgets(line, sizeof line, f)) {
        char *s = line; while (*s == ' ' || *s == '\t') s++;
        if (*s == '#' || *s == '\n' || *s == '\r' || *s == 0) continue;
        int cnt = 0; char *tok = strtok(s, " \t\r\n");
        while (tok) { if (cnt >= MAXN) { fprintf(stderr, "too many entries\n"); fclose(f); return 0; } grid[rows][cnt++] = atoi(tok) - 1; tok = strtok(NULL, " \t\r\n"); }
        if (n < 0) n = cnt; else if (cnt != n) { fprintf(stderr, "ragged row %d\n", rows + 1); fclose(f); return 0; }
        rows++; if (rows > 2 * MAXN) { fprintf(stderr, "too many rows\n"); fclose(f); return 0; }
    }
    fclose(f);
    if (n <= 0 || n > MAXN || rows != 2 * n) { fprintf(stderr, "need 2n rows of n entries, n<=%d (got rows=%d n=%d)\n", MAXN, rows, n); return 0; }
    I->n = n;
    for (int i = 0; i < n; i++) for (int p = 0; p < n; p++) { I->mpref[i][p] = grid[i][p]; I->wpref[i][p] = grid[n + i][p]; }
    if (!check_perms(I)) { fprintf(stderr, "lists must be complete strict permutations\n"); return 0; }
    build_ranks(I); return 1;
}
static void write_prefs(const char *path, const Inst *I, const char *comment) {
    FILE *f = fopen(path, "w"); if (!f) { perror(path); return; }
    if (comment) fprintf(f, "# %s\n", comment);
    for (int i = 0; i < I->n; i++) { for (int p = 0; p < I->n; p++) fprintf(f, "%d%c", I->mpref[i][p] + 1, p + 1 < I->n ? ' ' : '\n'); }
    for (int i = 0; i < I->n; i++) { for (int p = 0; p < I->n; p++) fprintf(f, "%d%c", I->wpref[i][p] + 1, p + 1 < I->n ? ' ' : '\n'); }
    fclose(f);
}
/* Gale-Shapley, proposers use pref[][], receivers use rrank[][]; returns match[p] = r (proposer-optimal). */
static void gale_shapley(int n, const int pref[MAXN][MAXN], const int rrank[MAXN][MAXN], int *match) {
    int nxt[MAXN] = {0}, held[MAXN], freeq[MAXN], nf = 0;
    for (int i = 0; i < n; i++) { held[i] = -1; match[i] = -1; freeq[nf++] = i; }
    while (nf) {
        int p = freeq[--nf]; int r = pref[p][nxt[p]++]; int h = held[r];
        if (h == -1) { held[r] = p; match[p] = r; }
        else if (rrank[r][p] < rrank[r][h]) { held[r] = p; match[p] = r; match[h] = -1; freeq[nf++] = h; }
        else freeq[nf++] = p;
    }
}
static int is_stable(const Inst *I, const int *M) {
    int n = I->n, Mw[MAXN];
    for (int m = 0; m < n; m++) Mw[M[m]] = m;
    for (int m = 0; m < n; m++) for (int w = 0; w < n; w++)
        if (I->mrank[m][w] < I->mrank[m][M[m]] && I->wrank[w][m] < I->wrank[w][Mw[w]]) return 0;
    return 1;
}
/* open-addressing hash set of uint64 keys (EMPTY = all ones is never a valid encoded bijection for n <= 16) */
typedef struct { uint64_t *k; size_t cap, cnt; } HSet;
static const uint64_t EMPTY = ~(uint64_t)0;
static uint64_t mix(uint64_t x) { x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL; x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL; return x ^ (x >> 31); }
static void hs_init(HSet *h, size_t cap) { h->cap = cap; h->cnt = 0; h->k = malloc(cap * 8); for (size_t i = 0; i < cap; i++) h->k[i] = EMPTY; }
static int hs_insert(HSet *h, uint64_t key);
static void hs_grow(HSet *h) { HSet g; hs_init(&g, h->cap * 2); for (size_t i = 0; i < h->cap; i++) if (h->k[i] != EMPTY) hs_insert(&g, h->k[i]); free(h->k); *h = g; }
static int hs_insert(HSet *h, uint64_t key) {   /* returns 1 if newly inserted */
    if (h->cnt * 2 >= h->cap) hs_grow(h);
    size_t i = mix(key) & (h->cap - 1);
    while (h->k[i] != EMPTY) { if (h->k[i] == key) return 0; i = (i + 1) & (h->cap - 1); }
    h->k[i] = key; h->cnt++; return 1;
}
static inline uint64_t encode(int n, const int *M) { uint64_t k = 0; for (int m = 0; m < n; m++) k |= (uint64_t)M[m] << (4 * m); return k; }
static inline void decode(int n, uint64_t k, int *M) { for (int m = 0; m < n; m++) M[m] = (int)((k >> (4 * m)) & 15); }

static long count_sm(const Inst *I, int verify) {
    int n = I->n, M0[MAXN], Mzw[MAXN], Mz[MAXN];
    gale_shapley(n, I->mpref, I->wrank, M0);
    gale_shapley(n, I->wpref, I->mrank, Mzw);
    for (int w = 0; w < n; w++) Mz[Mzw[w]] = w;
    if (verify && !(is_stable(I, M0) && is_stable(I, Mz))) { fprintf(stderr, "GS output unstable?!\n"); exit(3); }
    HSet hs; hs_init(&hs, 1 << 12);
    size_t scap = 1 << 12, sn = 0; uint64_t *stack = malloc(scap * 8);
    uint64_t k0 = encode(n, M0); hs_insert(&hs, k0); stack[sn++] = k0;
    int M[MAXN], Mw[MAXN], nxt[MAXN], state[MAXN], path[MAXN], M2[MAXN];
    while (sn) {
        uint64_t key = stack[--sn]; decode(n, key, M);
        if (verify && !is_stable(I, M)) { fprintf(stderr, "lattice walk produced an unstable matching\n"); exit(3); }
        for (int m = 0; m < n; m++) Mw[M[m]] = m;
        for (int m = 0; m < n; m++) {
            nxt[m] = -1;
            int lo = I->mrank[m][M[m]] + 1, hi = I->mrank[m][Mz[m]];
            for (int p = lo; p <= hi; p++) { int w = I->mpref[m][p]; if (I->wrank[w][m] < I->wrank[w][Mw[w]]) { nxt[m] = Mw[w]; break; } }
        }
        for (int m = 0; m < n; m++) state[m] = 0;
        for (int s = 0; s < n; s++) {
            if (state[s] || nxt[s] == -1) continue;
            int pl = 0, u = s;
            while (u != -1 && state[u] == 0) { state[u] = 1; path[pl++] = u; u = nxt[u]; }
            if (u != -1 && state[u] == 1) {
                int st = 0; while (path[st] != u) st++;
                int len = pl - st; memcpy(M2, M, sizeof(int) * n);
                for (int i = 0; i < len; i++) M2[path[st + i]] = M[path[st + (i + 1) % len]];
                uint64_t k2 = encode(n, M2);
                if (hs_insert(&hs, k2)) { if (sn == scap) { scap *= 2; stack = realloc(stack, scap * 8); } stack[sn++] = k2; }
            }
            for (int i = 0; i < pl; i++) state[path[i]] = 2;
        }
    }
    if (verify) { uint64_t kz = encode(n, Mz); size_t i = mix(kz) & (hs.cap - 1); int found = 0; while (hs.k[i] != EMPTY) { if (hs.k[i] == kz) { found = 1; break; } i = (i + 1) & (hs.cap - 1); } if (!found) { fprintf(stderr, "woman-optimal matching not reached\n"); exit(3); } }
    long c = (long)hs.cnt; free(hs.k); free(stack); return c;
}
/* xorshift64* rng */
static uint64_t rs;
static uint64_t rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 0x2545F4914F6CDD1DULL; }
static int rndint(int k) { return (int)(rnd() % (uint64_t)k); }
static void random_inst(Inst *I, int n) {
    I->n = n;
    for (int s = 0; s < 2; s++) for (int i = 0; i < n; i++) {
        int *L = s ? I->wpref[i] : I->mpref[i];
        for (int p = 0; p < n; p++) L[p] = p;
        for (int p = n - 1; p > 0; p--) { int j = rndint(p + 1); int t = L[p]; L[p] = L[j]; L[j] = t; }
    }
    build_ranks(I);
}
static double now_s(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
/* one random move on a copy: adjacent swap (70%) or arbitrary swap (30%) in one list */
static void random_move(Inst *I) {
    int n = I->n, side = rndint(2), i = rndint(n);
    int *L = side ? I->wpref[i] : I->mpref[i];
    int a, b;
    if (rndint(10) < 7) { a = rndint(n - 1); b = a + 1; } else { a = rndint(n); do { b = rndint(n); } while (b == a); }
    int t = L[a]; L[a] = L[b]; L[b] = t;
    build_ranks(I);
}
int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "count")) {
        Inst I; if (!read_prefs(argv[2], &I)) return 2;
        int verify = argc >= 4 ? atoi(argv[3]) : 0;
        double t0 = now_s(); long c = count_sm(&I, verify); double t1 = now_s();
        printf("file: %s\nn: %d\ncount: %ld\nverify: %d\nseconds: %.4f\n", argv[2], I.n, c, verify, t1 - t0);
        return 0;
    }
    if (argc >= 7 && !strcmp(argv[1], "climb")) {
        int n = atoi(argv[2]); const char *seedfile = argv[3]; uint64_t seed = strtoull(argv[4], 0, 10);
        double secs = atof(argv[5]); const char *out = argv[6]; long kick = argc >= 8 ? atol(argv[7]) : 3000; int kmax = argc >= 9 ? atoi(argv[8]) : 1;
        rs = seed * 0x9E3779B97F4A7C15ULL + 12345; for (int i = 0; i < 10; i++) rnd();
        Inst cur, best, cand;
        if (!strcmp(seedfile, "random")) random_inst(&cur, n); else { if (!read_prefs(seedfile, &cur)) return 2; if (cur.n != n) { fprintf(stderr, "seed file order %d != %d\n", cur.n, n); return 2; } }
        long curc = count_sm(&cur, 0), bestc = curc; best = cur;
        char bpath[1024], lpath[1024]; snprintf(bpath, sizeof bpath, "%s.best.prefs", out); snprintf(lpath, sizeof lpath, "%s.log", out);
        FILE *lf = fopen(lpath, "a"); if (!lf) { perror(lpath); return 2; }
        char cm[256]; snprintf(cm, sizeof cm, "best so far: n=%d count=%ld seed=%llu start=%s", n, bestc, (unsigned long long)seed, seedfile);
        write_prefs(bpath, &best, cm);
        double t0 = now_s(), tlast = t0; long evals = 0, since_best = 0, kicks = 0, accepted = 0;
        fprintf(lf, "start n=%d seed=%llu start=%s secs=%.0f initial_count=%ld kick=%ld kmax=%d\n", n, (unsigned long long)seed, seedfile, secs, curc, kick, kmax); fflush(lf);
        printf("start n=%d seed=%llu start=%s initial_count=%ld\n", n, (unsigned long long)seed, seedfile, curc); fflush(stdout);
        while (1) {
            double t = now_s(); if (t - t0 >= secs) break;
            if (t - tlast >= 10.0) { tlast = t; fprintf(lf, "t=%.0f evals=%ld accepted=%ld kicks=%ld cur=%ld best=%ld rate=%.1f/s\n", t - t0, evals, accepted, kicks, curc, bestc, evals / (t - t0)); fflush(lf); }
            cand = cur; random_move(&cand); long c = count_sm(&cand, 0); evals++;
            if (c >= curc) {
                if (c > curc) since_best = 0; else since_best++;
                cur = cand; curc = c; accepted++;
                if (c > bestc) { bestc = c; best = cur; snprintf(cm, sizeof cm, "best so far: n=%d count=%ld seed=%llu start=%s evals=%ld t=%.0f", n, bestc, (unsigned long long)seed, seedfile, evals, now_s() - t0); write_prefs(bpath, &best, cm); fprintf(lf, "NEWBEST t=%.0f evals=%ld best=%ld\n", now_s() - t0, evals, bestc); fflush(lf); }
            } else since_best++;
            if (since_best >= kick) { cur = best; int k = 1 + rndint(kmax); for (int i = 0; i < k; i++) random_move(&cur); curc = count_sm(&cur, 0); evals++; since_best = 0; kicks++; }
        }
        double el = now_s() - t0;
        fprintf(lf, "end t=%.0f evals=%ld accepted=%ld kicks=%ld cur=%ld best=%ld rate=%.1f/s\n", el, evals, accepted, kicks, curc, bestc, evals / el); fclose(lf);
        printf("end n=%d seed=%llu evals=%ld best=%ld rate=%.1f/s best_file=%s\n", n, (unsigned long long)seed, evals, bestc, evals / el, bpath);
        return 0;
    }
    fprintf(stderr, "usage: smclimb count FILE [verify] | smclimb climb N SEEDFILE|random RNGSEED SECONDS OUTPREFIX [KICKEVALS] [KMAX]\n");
    return 1;
}
