/* cdcount.c -- exact size of the full domain of a never-condition assignment (glue-constructor lens, run 2026-10-17-2113).
 *
 * Assignment encoding: alternatives 0..n-1 (label = index+1). Triple a<b<c has colex index
 *   C(c,3) + C(b,2) + a.  cond[idx] = 3*s + p, s in {0,1,2} = subject (a, b or c), p in {0,1,2} = forbidden
 *   position of the subject inside the triple (0 = top/first, 1 = middle, 2 = bottom/last).
 *   (paper notation iNj  <=>  s = i-1, p = j-1.)
 *
 * Counting (PROVED-HERE in NOTES.md): build an order top-down. Whether the next alternative e may follow the set S
 * of already placed alternatives depends only on (S, e): every condition of a triple {e,x,y} with subject e is
 * violated iff |{x,y} n S| == p; conditions with another subject are decided when that subject is placed.
 * So |D| = number of monotone paths from 0 to full set in the subset lattice using valid steps: a level-by-level
 * DP over reachable subsets (hash table per level).
 *
 * Library functions (ctypes):
 *   long long cd_count(int n, const unsigned char *cond, long long *nstates_out)
 *   long long cd_enum(int n, const unsigned char *cond, const char *outpath)   (writes orders, 1-based, best first)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 32
typedef uint32_t mask_t;

static long long binom(int n, int k) {
    if (k < 0 || n < k) return 0;
    long long r = 1;
    for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
    return r;
}

static mask_t M0[MAXN][MAXN], M1[MAXN][MAXN], M2[MAXN][MAXN];
static mask_t HAS0[MAXN], HAS1[MAXN], HAS2[MAXN]; /* which x have nonempty mask (speed) */

static void build_masks(int n, const unsigned char *cond) {
    memset(M0, 0, sizeof M0); memset(M1, 0, sizeof M1); memset(M2, 0, sizeof M2);
    memset(HAS0, 0, sizeof HAS0); memset(HAS1, 0, sizeof HAS1); memset(HAS2, 0, sizeof HAS2);
    for (int c = 2; c < n; c++)
        for (int b = 1; b < c; b++)
            for (int a = 0; a < b; a++) {
                long long idx = binom(c, 3) + binom(b, 2) + a;
                int code = cond[idx];
                if (code >= 9) continue; /* 9 = unconstrained (relaxation) */
                int s = code / 3, p = code % 3;
                int t[3] = {a, b, c};
                int e = t[s], x = t[(s + 1) % 3], y = t[(s + 2) % 3];
                mask_t (*M)[MAXN] = p == 0 ? M0 : (p == 1 ? M1 : M2);
                mask_t *H = p == 0 ? HAS0 : (p == 1 ? HAS1 : HAS2);
                M[e][x] |= (mask_t)1 << y;
                M[e][y] |= (mask_t)1 << x;
                H[e] |= ((mask_t)1 << x) | ((mask_t)1 << y);
            }
}

static inline int valid(mask_t S, int e, mask_t full) {
    mask_t notS = full & ~S;
    mask_t xs;
    /* p=0 (never top): violated iff some pair x,y both not in S */
    xs = HAS0[e] & notS;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M0[e][x] & notS) return 0; }
    /* p=2 (never bottom): violated iff some pair both in S */
    xs = HAS2[e] & S;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M2[e][x] & S) return 0; }
    /* p=1 (never middle): violated iff exactly one in S */
    xs = HAS1[e] & S;
    while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; if (M1[e][x] & notS) return 0; }
    return 1;
}

/* simple open-addressing hash: key mask (0 never used as key at level>=1; level 0 handled separately) */
typedef struct { mask_t *key; unsigned long long *val; size_t cap, cnt; } table_t;

static void tinit(table_t *t, size_t cap) {
    t->cap = cap; t->cnt = 0;
    t->key = (mask_t *)calloc(cap, sizeof(mask_t));
    t->val = (unsigned long long *)calloc(cap, sizeof(unsigned long long));
}
static void tfree(table_t *t) { free(t->key); free(t->val); t->key = NULL; t->val = NULL; }
static inline size_t hsh(mask_t k, size_t cap) { uint64_t h = (uint64_t)k * 0x9E3779B97F4A7C15ULL; return (size_t)(h >> 20) & (cap - 1); }
static void tadd(table_t *t, mask_t k, unsigned long long v);
static void tgrow(table_t *t) {
    table_t nt; tinit(&nt, t->cap * 2);
    for (size_t i = 0; i < t->cap; i++) if (t->key[i]) tadd(&nt, t->key[i], t->val[i]);
    tfree(t); *t = nt;
}
static void tadd(table_t *t, mask_t k, unsigned long long v) {
    if (2 * (t->cnt + 1) > t->cap) tgrow(t);
    size_t i = hsh(k, t->cap);
    while (t->key[i] && t->key[i] != k) i = (i + 1) & (t->cap - 1);
    if (!t->key[i]) { t->key[i] = k; t->val[i] = v; t->cnt++; }
    else t->val[i] += v;
}

long long cd_count(int n, const unsigned char *cond, long long *nstates_out) {
    if (n < 1 || n > 31) return -1;
    build_masks(n, cond);
    mask_t full = (n == 32) ? 0xFFFFFFFFu : (((mask_t)1 << n) - 1);
    long long nstates = 1;
    table_t cur; tinit(&cur, 1024);
    /* level 1 */
    for (int e = 0; e < n; e++) if (valid(0, e, full)) tadd(&cur, (mask_t)1 << e, 1);
    for (int k = 1; k < n; k++) {
        nstates += (long long)cur.cnt;
        table_t nxt; tinit(&nxt, 1024);
        for (size_t i = 0; i < cur.cap; i++) {
            mask_t S = cur.key[i];
            if (!S) continue;
            unsigned long long v = cur.val[i];
            mask_t rest = full & ~S;
            while (rest) {
                int e = __builtin_ctz(rest); rest &= rest - 1;
                if (valid(S, e, full)) tadd(&nxt, S | ((mask_t)1 << e), v);
            }
        }
        tfree(&cur); cur = nxt;
    }
    unsigned long long total = 0;
    for (size_t i = 0; i < cur.cap; i++) if (cur.key[i] == full) total = cur.val[i];
    tfree(&cur);
    if (nstates_out) *nstates_out = nstates;
    return (long long)total;
}

/* enumeration by DFS (writes one order per line, labels 1..n, most preferred first) */
static FILE *OUT; static int ORD[MAXN]; static long long NOUT; static int NN; static mask_t FULL;
static void dfs(mask_t S, int k) {
    if (k == NN) {
        char buf[200]; int p = 0;
        for (int i = 0; i < NN; i++) p += sprintf(buf + p, i ? " %d" : "%d", ORD[i] + 1);
        buf[p++] = '\n'; fwrite(buf, 1, p, OUT); NOUT++; return;
    }
    mask_t rest = FULL & ~S;
    while (rest) {
        int e = __builtin_ctz(rest); rest &= rest - 1;
        if (valid(S, e, FULL)) { ORD[k] = e; dfs(S | ((mask_t)1 << e), k + 1); }
    }
}
long long cd_enum(int n, const unsigned char *cond, const char *outpath) {
    if (n < 1 || n > 31) return -1;
    build_masks(n, cond);
    NN = n; FULL = ((mask_t)1 << n) - 1; NOUT = 0;
    OUT = fopen(outpath, "w"); if (!OUT) return -2;
    dfs(0, 0);
    fclose(OUT);
    return NOUT;
}
