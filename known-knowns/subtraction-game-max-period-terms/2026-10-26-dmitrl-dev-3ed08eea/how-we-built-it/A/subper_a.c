/* Implementation A: exhaustive maximum eventual period of subtraction games, all S subset of {1..n} with n in S.
   mode wl: window = last n outcomes as bits (bit k = outcome at p-k); next = ((~w) & maskS) != 0.
   mode sg: window = last n Sprague-Grundy values, 5 bits each in an unsigned __int128 (n <= 25).
   Cycle length by Brent's algorithm on the window sequence started at p = n-1 (first full window).
   Usage: subper_a wl|sg n [lo hi]   (mask range over the n-1 optional moves; default all)
   Output: max, first maximising mask, histogram lines "period count". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int n;
static uint64_t full;
/* --- win/lose --- */
static inline uint64_t step_wl(uint64_t w, uint64_t maskS) {
    return ((w << 1) | (((~w) & maskS) != 0)) & full;
}
static uint64_t start_wl(uint64_t maskS) {
    /* positions 0..n-1 computed directly (moves s <= p only); bit k of w = outcome(p-k) */
    int v[64];
    for (int p = 0; p < n; p++) {
        int win = 0;
        for (int s = 1; s <= p; s++) if ((maskS >> (s - 1) & 1) && v[p - s] == 0) { win = 1; break; }
        v[p] = win;
    }
    uint64_t w = 0;
    for (int k = 0; k < n; k++) w |= (uint64_t)v[n - 1 - k] << k;
    return w;
}
static uint64_t period_wl(uint64_t maskS) {
    uint64_t x0 = start_wl(maskS);
    uint64_t power = 1, lam = 1, tort = x0, hare = step_wl(x0, maskS);
    while (tort != hare) {
        if (power == lam) { tort = hare; power <<= 1; lam = 0; }
        hare = step_wl(hare, maskS); lam++;
    }
    return lam;
}
/* --- Sprague-Grundy --- */
static int moves[64], nm;
static inline unsigned field(u128 w, int k) { return (unsigned)(w >> (5 * k)) & 31u; }
static inline u128 step_sg(u128 w) {
    uint32_t seen = 0;
    for (int t = 0; t < nm; t++) seen |= 1u << field(w, moves[t] - 1);
    unsigned v = __builtin_ctz(~seen);
    u128 mask = (((u128)1) << (5 * n)) - 1;
    return ((w << 5) | v) & mask;
}
static u128 start_sg(void) {
    int v[64];
    for (int p = 0; p < n; p++) {
        uint32_t seen = 0;
        for (int t = 0; t < nm; t++) if (moves[t] <= p) seen |= 1u << v[p - moves[t]];
        v[p] = __builtin_ctz(~seen);
    }
    u128 w = 0;
    for (int k = 0; k < n; k++) w |= ((u128)v[n - 1 - k]) << (5 * k);
    return w;
}
static uint64_t period_sg(uint64_t maskS) {
    nm = 0;
    for (int s = 1; s <= n; s++) if (maskS >> (s - 1) & 1) moves[nm++] = s;
    u128 x0 = start_sg();
    uint64_t power = 1, lam = 1;
    u128 tort = x0, hare = step_sg(x0);
    while (tort != hare) {
        if (power == lam) { tort = hare; power <<= 1; lam = 0; }
        hare = step_sg(hare); lam++;
    }
    return lam;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 2; }
    int sg = strcmp(argv[1], "sg") == 0;
    n = atoi(argv[2]);
    if (n < 1 || n > (sg ? 25 : 63)) { fprintf(stderr, "n out of range\n"); return 2; }
    full = (n == 64) ? ~0ULL : ((1ULL << n) - 1);
    uint64_t lo = 0, hi = 1ULL << (n - 1);
    if (argc >= 5) { lo = strtoull(argv[3], 0, 10); hi = strtoull(argv[4], 0, 10); }
    const uint64_t HMAX = 1u << 22;
    uint64_t *hist = calloc(HMAX, sizeof(uint64_t));
    uint64_t best = 0, arg = 0, over = 0;
    for (uint64_t m = lo; m < hi; m++) {
        uint64_t maskS = m | (1ULL << (n - 1));
        uint64_t per = sg ? period_sg(maskS) : period_wl(maskS);
        if (per < HMAX) hist[per]++; else over++;
        if (per > best) { best = per; arg = maskS; }
    }
    printf("mode %s n %d range %llu %llu max %llu argmask %llu set", sg ? "sg" : "wl", n,
           (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)best, (unsigned long long)arg);
    for (int s = 1; s <= n; s++) if (arg >> (s - 1) & 1) printf(" %d", s);
    printf("\noverflow %llu\n", (unsigned long long)over);
    for (uint64_t p = 0; p < HMAX; p++) if (hist[p]) printf("%llu %llu\n", (unsigned long long)p, (unsigned long long)hist[p]);
    return over ? 3 : 0;
}
