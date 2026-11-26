/*
 * impl1 — exhaustive max eventual period for ECA Rule 30 / 110 on a ring.
 *
 * Algorithm: walk every trajectory in the functional graph. When a state is
 * first seen, mark ALL of its rotations visited (rotation commutes with both
 * rules; reflection does NOT). Cycle length uses the rotation-offset formula:
 * if f^k(s) = rot_r(s), period = k * n / gcd(r, n).
 *
 * Wolfram convention: neighborhood (left,center,right) = cells (i-1, i, i+1)
 * with cell index increasing to the right; rule bit index
 *   idx = (L<<2)|(C<<1)|R ; next = (rule>>idx)&1.
 * Cell 0 = least-significant bit of the state word.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>
#include <time.h>

static int nbits;
static uint64_t mask;
static int rule_num;
static uint8_t *seen; /* 1 bit per state */
static uint64_t nstates;

static inline int bit_get(const uint8_t *b, uint64_t i) {
    return (b[i >> 3] >> (i & 7)) & 1;
}
static inline void bit_set(uint8_t *b, uint64_t i) {
    b[i >> 3] |= (uint8_t)(1u << (i & 7));
}

static inline uint64_t rot_left(uint64_t s, int k) {
    k %= nbits;
    if (!k) return s;
    return ((s << k) | (s >> (nbits - k))) & mask;
}

static inline void mark_orbit(uint64_t s) {
    uint64_t r = s;
    for (int k = 0; k < nbits; k++) {
        bit_set(seen, r);
        r = rot_left(r, 1);
    }
}

static inline int orbit_seen(uint64_t s) {
    return bit_get(seen, s); /* any rotate shares the mark once marked */
}

static inline uint64_t eca_step(uint64_t s) {
    uint64_t out = 0;
    for (int i = 0; i < nbits; i++) {
        int L = (int)((s >> ((i + nbits - 1) % nbits)) & 1ULL);
        int C = (int)((s >> i) & 1ULL);
        int R = (int)((s >> ((i + 1) % nbits)) & 1ULL);
        int idx = (L << 2) | (C << 1) | R;
        if ((rule_num >> idx) & 1) out |= (1ULL << i);
    }
    return out;
}

static int igcd(int a, int b) {
    while (b) { int t = a % b; a = b; b = t; }
    return a < 0 ? -a : a;
}

/* Direct period of s (first return), capped. */
static uint64_t direct_period(uint64_t s, uint64_t cap) {
    uint64_t cur = s;
    for (uint64_t i = 1; i <= cap; i++) {
        cur = eca_step(cur);
        if (cur == s) return i;
    }
    return 0;
}

int main(int argc, char **argv) {
    int selftest = 0;
    const char *wout = NULL;
    rule_num = -1; nbits = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--rule") && i + 1 < argc) rule_num = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--n") && i + 1 < argc) nbits = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--witness-out") && i + 1 < argc) wout = argv[++i];
        else if (!strcmp(argv[i], "--selftest")) selftest = 1;
        else {
            fprintf(stderr, "Usage: %s --rule 30|110 --n N [--witness-out F]\n", argv[0]);
            return 2;
        }
    }
    if ((rule_num != 30 && rule_num != 110) || nbits < 1 || nbits > 63) {
        fprintf(stderr, "need --rule 30|110 and --n in 1..63\n");
        return 2;
    }
    mask = (nbits == 64) ? ~0ULL : ((1ULL << nbits) - 1ULL);
    nstates = 1ULL << nbits;
    size_t nbytes = (size_t)((nstates + 7) >> 3);
    fprintf(stderr, "impl1 rule=%d n=%d bitset=%zuB\n", rule_num, nbits, nbytes);

    seen = calloc(1, nbytes);
    if (!seen) { perror("calloc"); return 1; }

    uint64_t *path = NULL;
    size_t pcap = 4096, plen;
    path = malloc(pcap * sizeof(uint64_t));
    if (!path) { perror("malloc"); return 1; }

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    uint64_t maxper = 0, witness = 0;

    for (uint64_t s0 = 0; s0 < nstates; s0++) {
        if (bit_get(seen, s0)) continue;

        plen = 0;
        uint64_t cur = s0;
        for (;;) {
            if (bit_get(seen, cur)) {
                /* Does cur equal a rotation of some path[i]? */
                int hit = -1, rot_off = -1;
                for (size_t i = 0; i < plen; i++) {
                    uint64_t base = path[i];
                    uint64_t r = base;
                    for (int k = 0; k < nbits; k++) {
                        if (r == cur) { hit = (int)i; rot_off = k; goto found; }
                        r = rot_left(r, 1);
                    }
                }
            found:
                if (hit >= 0) {
                    int ksteps = (int)(plen - (size_t)hit);
                    /* f^{ksteps}(path[hit]) = rot_{rot_off}(path[hit])
                       But cur was reached by stepping from path[plen-1],
                       and cur = rot_off(path[hit]). Verify by evolving. */
                    uint64_t st = path[hit];
                    uint64_t after = st;
                    for (int j = 0; j < ksteps; j++) after = eca_step(after);
                    int r = -1;
                    for (int off = 0; off < nbits; off++) {
                        if (rot_left(st, off) == after) { r = off; break; }
                    }
                    uint64_t period;
                    if (r < 0) {
                        period = direct_period(st, nstates);
                    } else if (r == 0) {
                        period = (uint64_t)ksteps;
                    } else {
                        int g = igcd(r, nbits);
                        period = (uint64_t)ksteps * (uint64_t)(nbits / g);
                    }
                    if (period > maxper) { maxper = period; witness = st; }
                }
                break;
            }
            /* first visit of this orbit */
            mark_orbit(cur);
            if (plen + 1 > pcap) {
                pcap *= 2;
                uint64_t *np = realloc(path, pcap * sizeof(uint64_t));
                if (!np) { perror("realloc"); return 1; }
                path = np;
            }
            path[plen++] = cur;
            cur = eca_step(cur);
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double sec = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

    if (maxper > 0) {
        uint64_t p = direct_period(witness, maxper + nbits);
        if (p != maxper) {
            fprintf(stderr, "impl1: adjusting witness period %" PRIu64 " -> %" PRIu64 "\n", maxper, p);
            /* search a bit more carefully */
            p = direct_period(witness, nstates < 100000000ULL ? nstates : maxper * (uint64_t)nbits + 10);
            if (p) maxper = p;
        }
    }

    printf("rule=%d n=%d max_period=%" PRIu64 " witness=0x%" PRIx64 " time_sec=%.4f impl=1\n",
           rule_num, nbits, maxper, witness, sec);
    fflush(stdout);

    if (wout) {
        FILE *f = fopen(wout, "w");
        if (f) {
            fprintf(f, "rule=%d\nn=%d\nmax_period=%" PRIu64 "\nwitness=0x%" PRIx64 "\nimpl=1\n",
                    rule_num, nbits, maxper, witness);
            fclose(f);
        }
    }
    (void)selftest;
    free(path);
    free(seen);
    return 0;
}
