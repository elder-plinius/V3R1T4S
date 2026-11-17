/* solver lens: exact counter of inequivalent anomaly-free U(1) charge assignments
 * (BRIEF convention: 1 + #primitive nonzero solutions / (S3 per species x overall sign)).
 *
 * Method (own design):
 *  - S3^6 orbits of ordered solutions == tuples of 6 multisets (sorted triples), since every ACC is
 *    symmetric in the 3 families of a species. So we count multiset tuples directly.
 *  - Linear ACCs: with species sums s_X, the 4 linear equations give
 *        s_d = -2 sQ - su, s_L = -3 sQ, s_e = 2 sQ - su, s_nu = 4 sQ + su     (SMnuR)
 *    For SM (no nu) additionally s_nu = 0 i.e. su = -4 sQ, and nu is the fixed multiset {0,0,0}.
 *  - For each (sQ, su): meet in the middle on key (quadratic part, cubic part) with the split
 *        A = (Q, L, nu)   |   B = (u, d, e)
 *    (not the (Q,u,d)|(L,e,nu) split). The smaller half goes into a hash table.
 *  - F -> -F maps (sQ,su) -> (-sQ,-su) bijectively: N = cnt(0,0) + 2 * sum_{(sQ,su) > 0} cnt.
 *  - N(q) = # all multiset tuples with entries in [-q,q] (incl. zero). Moebius over gcd:
 *        P(q) = sum_d mu(d) (N(q/d) - 1)   (primitive nonzero)
 *  - Sign quotient by Burnside: tuples fixed by F -> -F have every species = {-a,0,a}, a>=0; they satisfy
 *    linear and cubic ACCs automatically; quadratic: aQ^2 - 2 au^2 + ad^2 - aL^2 + ae^2 = 0, a_nu free
 *    (SM: a_nu = 0). Fx(q) = sum_d mu(d) (Fix(q/d) - 1).  Answer = 1 + (P + Fx)/2.
 * Usage: mitm SM|SMnuR Qmax
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/resource.h>

typedef struct { int32_t q, c; } QC;

static int nuR;          /* 1 = SMnuR, 0 = SM */
static int B;            /* current bound */
static QC **lst;         /* lst[s+3B] = list of (sum sq, sum cubes) of multisets with sum s */
static int *len;

static void build_lists(int b) {
    B = b;
    int ns = 6 * b + 1;
    lst = calloc(ns, sizeof(QC *));
    len = calloc(ns, sizeof(int));
    int *cap = calloc(ns, sizeof(int));
    for (int x = -b; x <= b; x++)
        for (int y = x; y <= b; y++)
            for (int z = y; z <= b; z++) {
                int s = x + y + z + 3 * b;
                if (len[s] == cap[s]) { cap[s] = cap[s] ? 2 * cap[s] : 16; lst[s] = realloc(lst[s], cap[s] * sizeof(QC)); }
                lst[s][len[s]].q = x * x + y * y + z * z;
                lst[s][len[s]].c = x * x * x + y * y * y + z * z * z;
                len[s]++;
            }
    free(cap);
}
static void free_lists(void) {
    for (int s = 0; s < 6 * B + 1; s++) free(lst[s]);
    free(lst); free(len);
}

static QC zero_nu = {0, 0};
/* fetch species list for sum s (returns length, 0 if out of range) */
static int get(int s, QC **out) {
    if (s < -3 * B || s > 3 * B) return 0;
    *out = lst[s + 3 * B];
    return len[s + 3 * B];
}

/* hash table: open addressing, linear probing */
static uint64_t *hk; static uint32_t *hv; static size_t hcap = 0, hmask;
#define EMPTY UINT64_MAX
static inline uint64_t mk(int64_t q, int64_t c) { return ((uint64_t)(q + (1LL << 30)) << 32) | (uint64_t)(uint32_t)(c + (1LL << 31)); }
static inline size_t hh(uint64_t k) { k *= 0x9E3779B97F4A7C15ULL; return (size_t)(k >> 20); }
static void hprep(size_t n) {
    size_t need = 16; while (need < 2 * n) need <<= 1;
    if (need > hcap) {
        free(hk); free(hv);
        hcap = need; hk = malloc(hcap * 8); hv = malloc(hcap * 4);
        if (!hk || !hv) { fprintf(stderr, "oom\n"); exit(1); }
    }
    hmask = need - 1;
    memset(hk, 0xff, need * 8);
}
static inline void hins(uint64_t k) {
    size_t i = hh(k) & hmask;
    while (hk[i] != EMPTY) { if (hk[i] == k) { hv[i]++; return; } i = (i + 1) & hmask; }
    hk[i] = k; hv[i] = 1;
}
static inline uint32_t hget(uint64_t k) {
    size_t i = hh(k) & hmask;
    while (hk[i] != EMPTY) { if (hk[i] == k) return hv[i]; i = (i + 1) & hmask; }
    return 0;
}

/* weights: quadratic (Q,u,d,L,e,nu) = (1,-2,1,-1,1,0), cubic = (6,3,3,2,1,1) */
static uint64_t count_pair(int sQ, int su) {
    QC *lQ, *lL, *lN, *lu, *ld, *le;
    int nQ = get(sQ, &lQ), nL = get(-3 * sQ, &lL);
    int nN;
    if (nuR) nN = get(4 * sQ + su, &lN);
    else { if (4 * sQ + su != 0) return 0; lN = &zero_nu; nN = 1; }
    int nu_ = get(su, &lu), nd = get(-2 * sQ - su, &ld), ne = get(2 * sQ - su, &le);
    uint64_t nA = (uint64_t)nQ * nL * nN, nB = (uint64_t)nu_ * nd * ne;
    if (!nA || !nB) return 0;
    uint64_t tot = 0;
    if (nA <= nB) {
        hprep(nA);
        for (int i = 0; i < nQ; i++) for (int j = 0; j < nL; j++) {
            int64_t q0 = (int64_t)lQ[i].q - lL[j].q, c0 = 6LL * lQ[i].c + 2LL * lL[j].c;
            for (int k = 0; k < nN; k++) hins(mk(q0, c0 + lN[k].c));
        }
        for (int i = 0; i < nu_; i++) for (int j = 0; j < nd; j++) {
            int64_t q0 = -2LL * lu[i].q + ld[j].q, c0 = 3LL * lu[i].c + 3LL * ld[j].c;
            for (int k = 0; k < ne; k++) tot += hget(mk(-(q0 + le[k].q), -(c0 + le[k].c)));
        }
    } else {
        hprep(nB);
        for (int i = 0; i < nu_; i++) for (int j = 0; j < nd; j++) {
            int64_t q0 = -2LL * lu[i].q + ld[j].q, c0 = 3LL * lu[i].c + 3LL * ld[j].c;
            for (int k = 0; k < ne; k++) hins(mk(q0 + le[k].q, c0 + le[k].c));
        }
        for (int i = 0; i < nQ; i++) for (int j = 0; j < nL; j++) {
            int64_t q0 = (int64_t)lQ[i].q - lL[j].q, c0 = 6LL * lQ[i].c + 2LL * lL[j].c;
            for (int k = 0; k < nN; k++) tot += hget(mk(-q0, -(c0 + lN[k].c)));
        }
    }
    return tot;
}

/* N(b): all multiset tuples (incl. zero) with entries in [-b,b] satisfying the 6 ACCs */
static uint64_t countN(int b) {
    build_lists(b);
    uint64_t tot = count_pair(0, 0);
    for (int sQ = 0; sQ <= b; sQ++)            /* |s_L| = 3|sQ| <= 3b */
        for (int su = (sQ == 0 ? 1 : -3 * b); su <= 3 * b; su++)
            tot += 2 * count_pair(sQ, su);
    free_lists();
    return tot;
}

/* Fix(b): tuples of a_X in [0,b] with aQ^2 - 2au^2 + ad^2 - aL^2 + ae^2 = 0, a_nu in [0,b] (SM: a_nu=0) */
static uint64_t countFix(int b) {
    uint64_t t = 0;
    for (int aQ = 0; aQ <= b; aQ++) for (int au = 0; au <= b; au++) for (int ad = 0; ad <= b; ad++)
        for (int aL = 0; aL <= b; aL++) for (int ae = 0; ae <= b; ae++)
            if (aQ * aQ - 2 * au * au + ad * ad - aL * aL + ae * ae == 0) t++;
    return t * (nuR ? (uint64_t)(b + 1) : 1);
}

static int mobius(int n) {
    int m = 1;
    for (int p = 2; p * p <= n; p++) if (n % p == 0) { n /= p; if (n % p == 0) return 0; m = -m; }
    if (n > 1) m = -m;
    return m;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s SM|SMnuR Qmax\n", argv[0]); return 1; }
    nuR = strcmp(argv[1], "SMnuR") == 0;
    if (!nuR && strcmp(argv[1], "SM")) { fprintf(stderr, "model must be SM or SMnuR\n"); return 1; }
    int Q = atoi(argv[2]);
    uint64_t *N = calloc(Q + 1, 8), *Fx = calloc(Q + 1, 8);
    char *done = calloc(Q + 1, 1);
    __int128 P = 0, F = 0;
    for (int d = 1; d <= Q; d++) {
        int m = mobius(d); if (!m) continue;
        int b = Q / d;
        if (!done[b]) {
            struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
            N[b] = countN(b); Fx[b] = countFix(b); done[b] = 1;
            clock_gettime(CLOCK_MONOTONIC, &t1);
            printf("bound %d: N(all multiset tuples incl zero) = %llu  Fix = %llu  (%.1f s)\n", b,
                   (unsigned long long)N[b], (unsigned long long)Fx[b],
                   (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec));
            fflush(stdout);
        }
        P += (__int128)m * (__int128)(N[b] - 1);
        F += (__int128)m * (__int128)(Fx[b] - 1);
    }
    if ((P + F) % 2 != 0) { printf("PARITY ERROR\n"); return 2; }
    __int128 ans = 1 + (P + F) / 2;
    printf("%s Qmax %d: primitive nonzero multiset tuples P = %llu, sign-fixed primitive = %llu\n", argv[1], Q,
           (unsigned long long)P, (unsigned long long)F);
    printf("RESULT %s Qmax %d: inequivalent = %llu\n", argv[1], Q, (unsigned long long)ans);
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    printf("maxrss %ld KB\n", ru.ru_maxrss);
    return 0;
}
