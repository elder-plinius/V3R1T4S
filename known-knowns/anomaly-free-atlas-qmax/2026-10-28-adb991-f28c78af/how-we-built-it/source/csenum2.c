/* csenum.c -- construct-space lister for anomaly-free U(1)_F charge assignments (SM / SMnuR).
 *
 * Organisation (NOT "iterate Q,u,d and match L,e,nu"):
 *   The four linear ACCs leave two free linear sums a = sum F_Q, b = sum F_u; all six species sums are
 *   then fixed:  sd = -2a-b, sL = -3a, se = 2a-b, snu = 4a+b  (SM: the gravity ACC forces b = -4a).
 *   Outer loop: over the (a,b) lattice points of the half plane {a>0} u {a=0,b>=0} (the other half is the
 *   F -> -F mirror).  Each (a,b) block is an independent hash join:
 *     build side: all (L,e,nu) sorted triples with sums (-3a, 2a-b, 4a+b), keyed on
 *                 (q2, c3) = (-sum L^2 + sum e^2, 2 sum L^3 + sum e^3 + sum nu^3)
 *     probe side: all (Q,u,d) sorted triples with sums (a, b, -2a-b), probing key
 *                 (-(sum Q^2 - 2 sum u^2 + sum d^2), -(6 sum Q^3 + 3 sum u^3 + 3 sum d^3)).
 *   Every match is a solution with each species sorted (= one permutation orbit); it is replaced by
 *   max(F, -F) (lexicographic, after re-sorting -F), encoded as a 6-bit-per-charge 128-bit integer whose
 *   numeric order is the lexicographic order, filtered (nonzero, gcd 1), and stored.
 *   Blocks run on NTHR threads (dynamic schedule); each thread sorts its own bucket; the buckets are then
 *   k-way merged into the output stream (strict increase is asserted during the merge).
 *   To bound memory the canonical first charge q1 range is split into NPASS contiguous passes; a pass only
 *   probes with Q triples whose canonical q1 (= max(x0, -x2)) lies in its range, so passes are emitted in
 *   order and simply concatenated.
 * Usage: csenum QMAX NU(0|1) NPASS NTHR  > list   (stats on stderr)
 *
 * csenum2 (run 2026-10-19-0818): passes split on the pair (q1, q2) of the first two canonical charges instead of q1
 * alone, so one q1 value can span several passes. q2 is fixed by the Q triple too: x1 if x0 > -x2, -x1 if
 * x0 < -x2, |x1| on a tie (the tie is broken by comparing x1 with -x1). Output bytes are unchanged.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

typedef unsigned __int128 u128;
typedef struct { int x[3]; int s1; int64_t s2, s3; } Tri;

static int QM, NU, NS;           /* NS = number of species (5 or 6) */
static Tri *tri; static int ntri;
static int *bysum, *gst, *gcn;   /* triples grouped by sum: index s+3QM */

static int nsum(int s) { return (s < -3*QM || s > 3*QM) ? 0 : gcn[s + 3*QM]; }
static int *grp(int s) { return bysum + gst[s + 3*QM]; }
static int cq1(const Tri *t) { int a = t->x[0], b = -t->x[2]; return a > b ? a : b; }
static int cq2(const Tri *t) { int a = t->x[0], b = -t->x[2], y = t->x[1]; return a > b ? y : (a < b ? -y : (y < 0 ? -y : y)); }
static int W;                     /* 2*QM+1 */
static int cqi(const Tri *t) { return (cq1(t) + QM) * W + (cq2(t) + QM); }

typedef struct { u128 *v; size_t n, cap; } Vec;
static void vpush(Vec *V, u128 x) {
    if (V->n == V->cap) {
        V->cap = V->cap ? V->cap + V->cap / 2 : (1u << 20);
        V->v = realloc(V->v, V->cap * sizeof(u128));
        if (!V->v) { fprintf(stderr, "out of memory\n"); exit(2); }
    }
    V->v[V->n++] = x;
}

/* quicksort for u128 (median of three, insertion sort below 24) */
static void isort(u128 *a, long n) {
    for (long i = 1; i < n; i++) { u128 x = a[i]; long j = i; while (j > 0 && a[j-1] > x) { a[j] = a[j-1]; j--; } a[j] = x; }
}
static void qsort128(u128 *a, long n) {
    while (n > 24) {
        u128 x = a[0], y = a[n/2], z = a[n-1], p;
        if (x < y) { p = y < z ? y : (x < z ? z : x); } else { p = x < z ? x : (y < z ? z : y); }
        long i = 0, j = n - 1;
        for (;;) {
            while (a[i] < p) i++;
            while (a[j] > p) j--;
            if (i >= j) break;
            u128 t = a[i]; a[i] = a[j]; a[j] = t; i++; j--;
        }
        /* [0, j] <= p <= [j+1, n) */
        long nl = j + 1, nr = n - nl;
        if (nl < nr) { qsort128(a, nl); a += nl; n = nr; } else { qsort128(a + nl, nr); n = nl; }
    }
    isort(a, n);
}

static inline int64_t gcd64(int64_t a, int64_t b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { int64_t t = a % b; a = b; b = t; } return a; }

/* per-thread scratch for the build side */
typedef struct { int64_t *key, *skey; uint64_t *pay, *spay; uint32_t *head; size_t cap, hcap; } Scratch;

static void ensure(Scratch *S, size_t n, size_t nb) {
    if (n > S->cap) {
        S->cap = n + n / 4;
        S->key = realloc(S->key, S->cap * 8); S->skey = realloc(S->skey, S->cap * 8);
        S->pay = realloc(S->pay, S->cap * 8); S->spay = realloc(S->spay, S->cap * 8);
    }
    if (nb + 1 > S->hcap) { S->hcap = nb + 1; S->head = realloc(S->head, S->hcap * 4); }
}

#define KEY(k3, k2) ((int64_t)(k3) * 16777216LL + ((int64_t)(k2) + 8388608LL))
static inline uint32_t hsh(int64_t K, int bits) { return (uint32_t)(((uint64_t)K * 0x9E3779B97F4A7C15ULL) >> (64 - bits)); }

static int lo_pass, hi_pass;
static int **plist, *pcnt;   /* per pass: Q triples with sum s (index s+3QM) and cq1 in [lo,hi] */

static void emit(Vec *V, const int *F, int selfmirror) {
    u128 e = 0, m = 0;
    int nz = 0; int64_t g = 0;
    for (int s = 0; s < NS; s++) {
        for (int i = 0; i < 3; i++) { e = (e << 6) | (u128)(F[3*s+i] + 32); if (F[3*s+i]) nz = 1; }
        for (int i = 2; i >= 0; i--) m = (m << 6) | (u128)(-F[3*s+i] + 32);
    }
    if (!nz) return;
    if (selfmirror && e < m) return;   /* block (0,0) contains both F and -F: keep the larger only */
    u128 c = e > m ? e : m;
    int q1 = (int)((c >> (6 * (3*NS - 1))) & 63) - 32;
    int q2 = (int)((c >> (6 * (3*NS - 2))) & 63) - 32;
    int qi = (q1 + QM) * W + (q2 + QM);
    if (qi < lo_pass || qi > hi_pass) return;
    for (int i = 0; i < 3*NS && g != 1; i++) g = gcd64(g, F[i]);
    if (g != 1) return;
    vpush(V, c);
}

static uint64_t nprobe_tot, nbuild_tot, nmatch_tot;

static void do_block(int a, int b, Scratch *S, Vec *V) {
    int sQ = a, su = b, sd = -2*a - b, sL = -3*a, se = 2*a - b, sn = 4*a + b;
    int nQ = (sQ >= -3*QM && sQ <= 3*QM) ? pcnt[sQ + 3*QM] : 0;
    int nu_ = nsum(su), nd = nsum(sd), nL = nsum(sL), ne = nsum(se), nn = NU ? nsum(sn) : 1;
    if (!nQ || !nu_ || !nd || !nL || !ne || !nn) return;
    size_t nR = (size_t)nL * ne * nn;
    int bits = 1; while (((size_t)1 << bits) < 2 * nR) bits++;
    size_t nb = (size_t)1 << bits;
    ensure(S, nR, nb);
    int *gL = grp(sL), *ge = grp(se), *gn = NU ? grp(sn) : NULL;
    size_t r = 0;
    int k2min = 1 << 30, k2max = -(1 << 30);
    for (int i = 0; i < nL; i++) {
        const Tri *L = &tri[gL[i]];
        for (int j = 0; j < ne; j++) {
            const Tri *E = &tri[ge[j]];
            int k2 = (int)(-L->s2 + E->s2);
            if (k2 < k2min) k2min = k2;
            if (k2 > k2max) k2max = k2;
            int64_t c = 2 * L->s3 + E->s3;
            for (int k = 0; k < nn; k++) {
                int64_t k3 = c + (NU ? tri[gn[k]].s3 : 0);
                S->key[r] = KEY(k3, k2);
                S->pay[r] = ((uint64_t)gL[i] << 42) | ((uint64_t)ge[j] << 21) | (uint64_t)(NU ? gn[k] : 0);
                r++;
            }
        }
    }
    memset(S->head, 0, (nb + 1) * 4);
    for (size_t t = 0; t < nR; t++) S->head[hsh(S->key[t], bits) + 1]++;
    for (size_t h = 0; h < nb; h++) S->head[h + 1] += S->head[h];
    /* scatter (use head as cursor, then restore) */
    for (size_t t = 0; t < nR; t++) { uint32_t h = hsh(S->key[t], bits); uint32_t p = S->head[h]++; S->skey[p] = S->key[t]; S->spay[p] = S->pay[t]; }
    for (size_t h = nb; h > 0; h--) S->head[h] = S->head[h - 1];
    S->head[0] = 0;

    int *gQ = plist[sQ + 3*QM], *gu = grp(su), *gd = grp(sd);
    uint64_t np = 0, nm = 0;
    int F[18];
    for (int i = 0; i < nQ; i++) {
        const Tri *Qt = &tri[gQ[i]];
        for (int j = 0; j < nu_; j++) {
            const Tri *U = &tri[gu[j]];
            int64_t b2 = Qt->s2 - 2 * U->s2, b3 = 6 * Qt->s3 + 3 * U->s3;
            for (int k = 0; k < nd; k++) {
                const Tri *D = &tri[gd[k]];
                int k2 = (int)-(b2 + D->s2);
                np++;
                if (k2 < k2min || k2 > k2max) continue;
                int64_t K = KEY(-(b3 + 3 * D->s3), k2);
                uint32_t h = hsh(K, bits);
                for (uint32_t p = S->head[h], pe = S->head[h + 1]; p < pe; p++) {
                    if (S->skey[p] != K) continue;
                    nm++;
                    uint64_t y = S->spay[p];
                    const Tri *L = &tri[y >> 42], *E = &tri[(y >> 21) & 0x1FFFFF], *N = &tri[y & 0x1FFFFF];
                    for (int z = 0; z < 3; z++) {
                        F[z] = Qt->x[z]; F[3+z] = U->x[z]; F[6+z] = D->x[z];
                        F[9+z] = L->x[z]; F[12+z] = E->x[z]; if (NU) F[15+z] = N->x[z];
                    }
                    emit(V, F, a == 0 && b == 0);
                }
            }
        }
    }
    #pragma omp atomic
    nprobe_tot += np;
    #pragma omp atomic
    nmatch_tot += nm;
    #pragma omp atomic
    nbuild_tot += nR;
}

/* output */
static char obuf[1 << 20]; static size_t opos;
static void oflush(void) { fwrite(obuf, 1, opos, stdout); opos = 0; }
static void put(u128 c) {
    if (opos > sizeof(obuf) - 256) oflush();
    int n = 3 * NS;
    for (int i = 0; i < n; i++) {
        int v = (int)((c >> (6 * (n - 1 - i))) & 63) - 32;
        if (i) obuf[opos++] = ' ';
        if (v < 0) { obuf[opos++] = '-'; v = -v; }
        if (v >= 10) obuf[opos++] = (char)('0' + v / 10);
        obuf[opos++] = (char)('0' + v % 10);
    }
    obuf[opos++] = '\n';
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s QMAX NU NPASS NTHR\n", argv[0]); return 1; }
    QM = atoi(argv[1]); NU = atoi(argv[2]); int NPASS = atoi(argv[3]); int NTHR = atoi(argv[4]);
    NS = NU ? 6 : 5;
    if (QM < 1 || QM > 31) { fprintf(stderr, "QMAX out of range\n"); return 1; }
    omp_set_num_threads(NTHR);
    W = 2 * QM + 1;
    double t0 = omp_get_wtime();
    /* sorted triples */
    ntri = 0; int w = 2 * QM + 1;
    tri = malloc(sizeof(Tri) * (size_t)w * w * w);
    for (int x = -QM; x <= QM; x++) for (int y = x; y <= QM; y++) for (int z = y; z <= QM; z++) {
        Tri *t = &tri[ntri++]; t->x[0] = x; t->x[1] = y; t->x[2] = z; t->s1 = x + y + z;
        t->s2 = (int64_t)x*x + (int64_t)y*y + (int64_t)z*z; t->s3 = (int64_t)x*x*x + (int64_t)y*y*y + (int64_t)z*z*z;
    }
    if (ntri >= (1 << 21)) { fprintf(stderr, "too many triples\n"); return 1; }
    int ng = 6 * QM + 1;
    gcn = calloc(ng, sizeof(int)); gst = calloc(ng + 1, sizeof(int)); bysum = malloc(sizeof(int) * ntri);
    for (int i = 0; i < ntri; i++) gcn[tri[i].s1 + 3*QM]++;
    for (int s = 0; s < ng; s++) gst[s + 1] = gst[s] + gcn[s];
    { int *cur = malloc(sizeof(int) * ng); memcpy(cur, gst, sizeof(int) * ng);
      for (int i = 0; i < ntri; i++) bysum[cur[tri[i].s1 + 3*QM]++] = i; free(cur); }
    /* half-plane block list */
    int nblk = 0; int (*blk)[2] = malloc(sizeof(int[2]) * (size_t)ng * ng);
    for (int a = 0; a <= QM; a++) for (int b = -3*QM; b <= 3*QM; b++) {
        if (a == 0 && b < 0) continue;
        if (!NU && b != -4*a) continue;
        blk[nblk][0] = a; blk[nblk][1] = b; nblk++;
    }
    /* pass split of canonical q1 in [-QM, QM] by probe-volume weight */
    int NI = W * W;
    double *wt = calloc(NI, sizeof(double)); double wtot = 0;
    for (int i = 0; i < ntri; i++) {
        const Tri *t = &tri[i]; int a = t->s1; if (a < 0) continue;
        double s = 0;
        for (int k = 0; k < nblk; k++) if (blk[k][0] == a) s += (double)nsum(blk[k][1]) * nsum(-2*a - blk[k][1]);
        wt[cqi(t)] += s; wtot += s;
    }
    int *plo = malloc(sizeof(int) * (NPASS + 1)), *phi = malloc(sizeof(int) * (NPASS + 1)); int np = 0;
    { double acc = 0; int start = 0;
      for (int v = 0; v < NI; v++) {
          acc += wt[v];
          if ((acc >= wtot * (np + 1) / NPASS && np < NPASS - 1) || v == NI - 1) { plo[np] = start; phi[np] = v; np++; start = v + 1; }
      } }
    Scratch *SC = calloc(NTHR, sizeof(Scratch)); Vec *VV = calloc(NTHR, sizeof(Vec));
    plist = malloc(sizeof(int*) * ng); pcnt = calloc(ng, sizeof(int));
    for (int s = 0; s < ng; s++) plist[s] = malloc(sizeof(int) * (gcn[s] + 1));
    uint64_t nout = 0; int bad = 0;
    for (int p = 0; p < np; p++) {
        double tp = omp_get_wtime();
        lo_pass = plo[p]; hi_pass = phi[p];
        for (int s = 0; s < ng; s++) { pcnt[s] = 0; int *g = bysum + gst[s];
            for (int k = 0; k < gcn[s]; k++) { int c = cqi(&tri[g[k]]); if (c >= lo_pass && c <= hi_pass) plist[s][pcnt[s]++] = g[k]; } }
        for (int t = 0; t < NTHR; t++) VV[t].n = 0;
        #pragma omp parallel for schedule(dynamic, 1)
        for (int k = 0; k < nblk; k++) { int t = omp_get_thread_num(); do_block(blk[k][0], blk[k][1], &SC[t], &VV[t]); }
        double tj = omp_get_wtime();
        #pragma omp parallel for schedule(static, 1)
        for (int t = 0; t < NTHR; t++) qsort128(VV[t].v, (long)VV[t].n);
        double ts = omp_get_wtime();
        /* k-way merge of the thread buckets */
        size_t *pos = calloc(NTHR, sizeof(size_t)); int first = 1; u128 prev = 0; size_t pn = 0;
        for (;;) {
            int bt = -1; u128 best = 0;
            for (int t = 0; t < NTHR; t++) if (pos[t] < VV[t].n && (bt < 0 || VV[t].v[pos[t]] < best)) { bt = t; best = VV[t].v[pos[t]]; }
            if (bt < 0) break;
            pos[bt]++;
            if (!first && best <= prev) { bad = 1; fprintf(stderr, "ERROR: duplicate/unsorted in pass %d\n", p); }
            first = 0; prev = best; put(best); pn++;
        }
        free(pos);
        nout += pn;
        size_t mem = 0; for (int t = 0; t < NTHR; t++) mem += VV[t].cap * sizeof(u128);
        fprintf(stderr, "pass %d qidx [%d,%d]: %zu lines, join %.1fs sort %.1fs merge %.1fs, bucket mem %.2f GB\n",
                p, lo_pass, hi_pass, pn, tj - tp, ts - tj, omp_get_wtime() - ts, mem / 1e9);
    }
    oflush();
    fprintf(stderr, "QMAX %d NU %d: blocks %d, build %llu, probes %llu, matches %llu, lines %llu, count(+1) %llu, %.1fs%s\n",
            QM, NU, nblk, (unsigned long long)nbuild_tot, (unsigned long long)nprobe_tot, (unsigned long long)nmatch_tot,
            (unsigned long long)nout, (unsigned long long)nout + 1, omp_get_wtime() - t0, bad ? " ERRORS" : "");
    return bad ? 3 : 0;
}
