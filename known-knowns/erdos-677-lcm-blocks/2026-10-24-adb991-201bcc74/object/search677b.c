/* search677b.c -- chunked, lower-memory version of search677.c (same mathematics; see header there and NOTES.md).

   Complete search for Erdos 677 counterexamples (n, m, k) with n + k <= N0 and ANY m:
     * k = 1, 2 impossible (trivial / strictly increasing);
     * Lemma A: m + k <= (n+k) * rho_k, rho_k = (lcm(1..k)/k)^(1/k) < 3, and G_k(m) = G_k(n)
       (G_k = product of the block with all prime factors < k removed);
     * the m-block contains no prime, so k <= K = (max gap between consecutive primes p < 3*N0) - 1.
   For each 3 <= k <= K: additive 64-bit hash of G_k over sliding windows; every (n, m) with n <= N0 - k,
   n + k <= m <= (n_chunk_max + k) * rho_k + 2 - k, prime-free m-block and equal hash is written out for exact
   verification. Equal G_k => equal hash, so no true solution can be missed (hash collisions only add candidates).

   usage: search677b N0 seed outfile [kmin kmax]
          search677b TEST XT KT seed outfile   (self-test: all n, m <= XT with m > n, k <= KT, no prime filter)
   env:   FORCE=m|n   force the insertion side;  CHUNK=size of n-chunks (default 1<<24);
          SHIFT=s     validation only: remove primes < k+s instead of < k (coarser G, more collisions)
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

static inline uint64_t splitmix64(uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}
static uint64_t SEED;
static inline uint64_t hp(uint64_t p) { return splitmix64(p * 0x2545F4914F6CDD1DULL ^ SEED) | 1ULL; }

static uint64_t *cbits;   /* composite bitset */
static inline int isprime_(uint64_t x) { return !((cbits[x >> 6] >> (x & 63)) & 1ULL); }
static inline void setcomp(uint64_t x) { cbits[x >> 6] |= 1ULL << (x & 63); }

static uint64_t *tkey; static uint32_t *tval; static uint64_t tmask, tcap = 0;
static void table_reset(uint64_t nentries) {
    uint64_t sz = 1024;
    while (sz < 2 * nentries) sz <<= 1;
    if (sz > tcap) {
        free(tkey); free(tval);
        tkey = (uint64_t *)malloc(sz * sizeof(uint64_t));
        tval = (uint32_t *)malloc(sz * sizeof(uint32_t));
        if (!tkey || !tval) { fprintf(stderr, "alloc fail table %llu\n", (unsigned long long)sz); exit(2); }
        tcap = sz;
    }
    memset(tval, 0, sz * sizeof(uint32_t));
    tmask = sz - 1;
}
static inline void table_insert(uint64_t key, uint32_t v) {   /* v = x + 1 ; 0 = empty */
    uint64_t i = splitmix64(key) & tmask;
    while (tval[i]) i = (i + 1) & tmask;
    tkey[i] = key; tval[i] = v;
}

static uint64_t *A; static uint64_t Y;
static void remove_prime(uint64_t p) {
    uint64_t h = hp(p);
    for (uint64_t q = p; q <= Y; ) {
        for (uint64_t y = q; y <= Y; y += q) A[y] -= h;
        if (q > Y / p) break; q *= p;
    }
}
static double lnpp(uint64_t x) {  /* ln p if x = p^a (a >= 1), else 0 */
    if (x < 2) return 0.0;
    uint64_t p = 0, t = x;
    for (uint64_t d = 2; d * d <= t; d++) if (t % d == 0) { p = d; break; }
    if (!p) p = t;
    while (t % p == 0) t /= p;
    return t == 1 ? log((double)p) : 0.0;
}

int main(int argc, char **argv) {
    int test = (argc > 1 && strcmp(argv[1], "TEST") == 0);
    uint64_t N0, XT = 0, KT = 0, kmin = 3, kmax = 0; const char *outfile;
    if (test) {
        if (argc < 6) return 1;
        XT = strtoull(argv[2], 0, 10); KT = strtoull(argv[3], 0, 10); SEED = strtoull(argv[4], 0, 10);
        outfile = argv[5]; N0 = XT + KT; kmin = 1; kmax = KT;
    } else {
        if (argc < 4) return 1;
        N0 = strtoull(argv[1], 0, 10); SEED = strtoull(argv[2], 0, 10); outfile = argv[3];
        if (argc >= 6) { kmin = strtoull(argv[4], 0, 10); kmax = strtoull(argv[5], 0, 10); }
    }
    const char *force = getenv("FORCE");
    uint64_t CHUNK = getenv("CHUNK") ? strtoull(getenv("CHUNK"), 0, 10) : (1ULL << 24);
    uint64_t SHIFT = getenv("SHIFT") ? strtoull(getenv("SHIFT"), 0, 10) : 0;
    Y = 3 * N0 + 100000;
    time_t t0 = time(0);
    cbits = (uint64_t *)calloc((Y >> 6) + 2, sizeof(uint64_t));
    setcomp(0); setcomp(1);
    for (uint64_t i = 2; i * i <= Y; i++) if (isprime_(i)) for (uint64_t j = i * i; j <= Y; j += i) setcomp(j);
    uint64_t lastp = 2, maxgap = 1, gapat = 2;
    for (uint64_t x = 3; x <= Y; x++) if (isprime_(x)) {
        if (lastp < 3 * N0) { if (x - lastp > maxgap) { maxgap = x - lastp; gapat = lastp; } }
        else break;
        lastp = x;
    }
    if (lastp < 3 * N0) { fprintf(stderr, "sieve too short\n"); return 3; }
    uint64_t K = maxgap - 1;
    if (!test && (kmax == 0 || kmax > K)) kmax = K;
    FILE *fo = fopen(outfile, "w");
    fprintf(fo, "# search677b N0=%llu seed=%llu Y=%llu maxgap(primes<3N0)=%llu at %llu => K=%llu ; kmin=%llu kmax=%llu test=%d SHIFT=%llu FORCE=%s CHUNK=%llu\n",
            (unsigned long long)N0, (unsigned long long)SEED, (unsigned long long)Y, (unsigned long long)maxgap,
            (unsigned long long)gapat, (unsigned long long)K, (unsigned long long)kmin, (unsigned long long)kmax,
            test, (unsigned long long)SHIFT, force ? force : "auto", (unsigned long long)CHUNK);
    fflush(fo);
    A = (uint64_t *)calloc(Y + 1, sizeof(uint64_t));
    if (!A) { fprintf(stderr, "alloc A fail\n"); return 2; }
    for (uint64_t p = 2; p <= Y; p++) if (isprime_(p)) {
        uint64_t h = hp(p);
        for (uint64_t q = p; q <= Y; ) {
            for (uint64_t y = q; y <= Y; y += q) A[y] += h;
            if (q > Y / p) break; q *= p;
        }
    }
    for (uint64_t p = 2; p < kmin + SHIFT; p++) if (isprime_(p)) remove_prime(p);
    double psi = 0.0;
    for (uint64_t x = 2; x < kmin; x++) psi += lnpp(x);
    fprintf(stderr, "setup done in %ld s, K=%llu\n", (long)(time(0) - t0), (unsigned long long)K);
    unsigned long long total_cand = 0;
    for (uint64_t k = kmin; k <= kmax; k++) {
        if (k > kmin && k - 1 + SHIFT >= 2 && isprime_(k - 1 + SHIFT)) remove_prime(k - 1 + SHIFT);
        psi += lnpp(k);
        uint64_t nmax, X; double rho = 3.0;
        if (test) { nmax = XT; X = XT; }
        else {
            rho = exp((psi - log((double)k)) / (double)k);     /* R(k) = lcm(1..k)/k */
            if (!(rho < 3.0)) { fprintf(stderr, "rho >= 3 at k=%llu\n", (unsigned long long)k); return 4; }
            nmax = N0 - k;
            X = (uint64_t)(floor((double)N0 * rho) + 2.0 - (double)k);
            if (X + k > Y) { fprintf(stderr, "X too big\n"); return 5; }
        }
        uint64_t mlo = test ? 1 : k;
        uint64_t cntM = 0;
        { uint64_t pc = 0;
          for (uint64_t y = mlo + 1; y <= mlo + k; y++) pc += isprime_(y);
          for (uint64_t m = mlo; m <= X; m++) { if (test || pc == 0) cntM++; pc += isprime_(m + k + 1); pc -= isprime_(m + 1); } }
        int insert_m = force ? (force[0] == 'm') : (cntM < (nmax + 1) / 4);
        unsigned long long cand = 0, probes = 0;
        if (insert_m) {
            table_reset(cntM);
            uint64_t pc = 0, H = 0;
            for (uint64_t y = mlo + 1; y <= mlo + k; y++) { pc += isprime_(y); H += A[y]; }
            for (uint64_t m = mlo; m <= X; m++) {
                if (test || pc == 0) table_insert(H, (uint32_t)(m + 1));
                pc += isprime_(m + k + 1); pc -= isprime_(m + 1);
                H += A[m + k + 1]; H -= A[m + 1];
            }
            H = 0;
            for (uint64_t y = 1; y <= k; y++) H += A[y];
            for (uint64_t n = 0; n <= nmax; n++) {
                uint64_t i = splitmix64(H) & tmask; probes++;
                while (tval[i]) {
                    if (tkey[i] == H) {
                        uint64_t m = tval[i] - 1;
                        if ((test && m > n) || (!test && m >= n + k)) {
                            fprintf(fo, "%llu %llu %llu\n", (unsigned long long)k, (unsigned long long)n, (unsigned long long)m); cand++; }
                    }
                    i = (i + 1) & tmask;
                }
                H += A[n + k + 1]; H -= A[n + 1];
            }
        } else {
            for (uint64_t a = 0; a <= nmax; a += CHUNK) {
                uint64_t b = a + CHUNK; if (b > nmax + 1) b = nmax + 1;      /* n in [a, b) */
                table_reset(b - a);
                uint64_t H = 0;
                for (uint64_t y = a + 1; y <= a + k; y++) H += A[y];
                for (uint64_t n = a; n < b; n++) { table_insert(H, (uint32_t)(n + 1)); H += A[n + k + 1]; H -= A[n + 1]; }
                uint64_t m0 = test ? mlo : a + k, m1 = X;
                if (!test) { double mh = floor((double)(b - 1 + k) * rho) + 2.0 - (double)k; if ((double)m1 > mh) m1 = (uint64_t)mh; }
                if (m0 < mlo) m0 = mlo;
                uint64_t pc = 0; H = 0;
                for (uint64_t y = m0 + 1; y <= m0 + k; y++) { pc += isprime_(y); H += A[y]; }
                for (uint64_t m = m0; m <= m1; m++) {
                    if (test || pc == 0) {
                        uint64_t i = splitmix64(H) & tmask; probes++;
                        while (tval[i]) {
                            if (tkey[i] == H) {
                                uint64_t n = tval[i] - 1;
                                if ((test && m > n) || (!test && m >= n + k)) {
                                    fprintf(fo, "%llu %llu %llu\n", (unsigned long long)k, (unsigned long long)n, (unsigned long long)m); cand++; }
                            }
                            i = (i + 1) & tmask;
                        }
                    }
                    pc += isprime_(m + k + 1); pc -= isprime_(m + 1);
                    H += A[m + k + 1]; H -= A[m + 1];
                }
            }
        }
        total_cand += cand;
        fprintf(fo, "# done k=%llu nmax=%llu X=%llu rho=%.6f primefree_m_windows=%llu insert_m=%d probes=%llu cand=%llu t=%lds\n",
                (unsigned long long)k, (unsigned long long)nmax, (unsigned long long)X, rho, (unsigned long long)cntM,
                insert_m, probes, cand, (long)(time(0) - t0));
        fflush(fo);
    }
    fprintf(fo, "# COMPLETE kmin=%llu kmax=%llu total_candidates=%llu elapsed=%lds\n", (unsigned long long)kmin,
            (unsigned long long)kmax, total_cand, (long)(time(0) - t0));
    fclose(fo);
    return 0;
}
