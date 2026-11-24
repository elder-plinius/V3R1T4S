/*
 * impl2 — exhaustive max eventual period for ECA Rule 30 / 110 on a ring.
 *
 * Algorithm (different from impl1): classic 3-colour walk on the functional
 * graph with NO rotation folding during search.
 *   colour 0 = white (unseen), 1 = grey (on stack), 2 = black (done)
 * When a step lands on grey, the grey-segment length is the cycle period.
 * (No rotation-offset formula here — every state is walked explicitly.)
 *
 * Same Wolfram bit-order as impl1 (cell 0 = LSB; L=i-1, R=i+1).
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
static uint8_t *colour; /* 2 bits per state packed: 4 states/byte */
static uint64_t nstates;

static inline int col_get(uint64_t i) {
    unsigned shift = (unsigned)((i & 3ULL) << 1);
    return (colour[i >> 2] >> shift) & 3;
}
static inline void col_set(uint64_t i, int c) {
    unsigned shift = (unsigned)((i & 3ULL) << 1);
    uint8_t *p = &colour[i >> 2];
    *p = (uint8_t)((*p & ~(3u << shift)) | ((unsigned)c << shift));
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

static uint64_t direct_period(uint64_t s, uint64_t cap) {
    uint64_t cur = s;
    for (uint64_t i = 1; i <= cap; i++) {
        cur = eca_step(cur);
        if (cur == s) return i;
    }
    return 0;
}

int main(int argc, char **argv) {
    const char *wout = NULL;
    rule_num = -1; nbits = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--rule") && i + 1 < argc) rule_num = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--n") && i + 1 < argc) nbits = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--witness-out") && i + 1 < argc) wout = argv[++i];
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
    size_t nbytes = (size_t)((nstates + 3) >> 2); /* 2 bits each */
    fprintf(stderr, "impl2 rule=%d n=%d colour=%zuB\n", rule_num, nbits, nbytes);

    colour = calloc(1, nbytes);
    if (!colour) { perror("calloc"); return 1; }

    uint64_t *stack = NULL;
    size_t scap = 4096, slen;
    stack = malloc(scap * sizeof(uint64_t));
    if (!stack) { perror("malloc"); return 1; }

    /* Also store index-in-stack for grey states via parallel array of positions.
       For large n we can't afford a 2^n index array. Instead, on grey-hit,
       scan the stack (cycle lengths are << 2^n for these rules in practice,
       and we only scan when we close a cycle). */
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    uint64_t maxper = 0, witness = 0;

    for (uint64_t s0 = 0; s0 < nstates; s0++) {
        if (col_get(s0) != 0) continue;
        slen = 0;
        uint64_t cur = s0;
        for (;;) {
            int c = col_get(cur);
            if (c == 2) { /* black: transient into done region */
                /* paint stack black */
                for (size_t i = 0; i < slen; i++) col_set(stack[i], 2);
                break;
            }
            if (c == 1) { /* grey: cycle */
                size_t idx = 0;
                for (; idx < slen; idx++) if (stack[idx] == cur) break;
                uint64_t period = (uint64_t)(slen - idx);
                if (period > maxper) { maxper = period; witness = cur; }
                for (size_t i = 0; i < slen; i++) col_set(stack[i], 2);
                break;
            }
            /* white -> grey, push */
            col_set(cur, 1);
            if (slen + 1 > scap) {
                scap *= 2;
                uint64_t *ns = realloc(stack, scap * sizeof(uint64_t));
                if (!ns) { perror("realloc"); return 1; }
                stack = ns;
            }
            stack[slen++] = cur;
            cur = eca_step(cur);
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double sec = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

    if (maxper > 0) {
        uint64_t p = direct_period(witness, maxper);
        if (p != maxper) {
            fprintf(stderr, "impl2: period mismatch claim=%" PRIu64 " got=%" PRIu64 "\n", maxper, p);
            maxper = p;
        }
    }

    printf("rule=%d n=%d max_period=%" PRIu64 " witness=0x%" PRIx64 " time_sec=%.4f impl=2\n",
           rule_num, nbits, maxper, witness, sec);
    fflush(stdout);

    if (wout) {
        FILE *f = fopen(wout, "w");
        if (f) {
            fprintf(f, "rule=%d\nn=%d\nmax_period=%" PRIu64 "\nwitness=0x%" PRIx64 "\nimpl=2\n",
                    rule_num, nbits, maxper, witness);
            fclose(f);
        }
    }
    free(stack);
    free(colour);
    return 0;
}
