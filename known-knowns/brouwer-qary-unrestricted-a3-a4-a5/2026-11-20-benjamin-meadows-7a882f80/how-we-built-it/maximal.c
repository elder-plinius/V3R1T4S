/* Maximality check: counts the words of {0,...,q-1}^n (q <= 4, n <= 16) at Hamming distance >= d from every
   codeword, i.e. the words that could be added to the code. 0 means the code is maximal (no word can be added).
   usage: cc -O2 -o maximal maximal.c && ./maximal CODE_FILE q n d
   CODE_FILE: one word per line as n digits; lines starting with '#' are skipped. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: maximal CODE_FILE q n d\n"); return 2; }
    int q = atoi(argv[2]), n = atoi(argv[3]), d = atoi(argv[4]);
    if (q < 2 || q > 4 || n < 1 || n > 16) return 2;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 2;
    static uint32_t C[65536];
    int M = 0;
    char *line = NULL;
    size_t cap = 0;
    while (getline(&line, &cap, f) != -1) {
        if (line[0] == '#' || (int)strlen(line) < n) continue;
        if (M == 65536) return 2;
        uint32_t w = 0;
        for (int i = 0; i < n; i++) w |= (uint32_t)(line[i] - '0') << (2 * i);
        C[M++] = w;
    }
    fclose(f);
    free(line);
    uint32_t lo = 0;
    for (int i = 0; i < n; i++) lo |= 1u << (2 * i);
    long long total = 1, found = 0;
    for (int i = 0; i < n; i++) total *= q;
    int digit[16] = {0};
    uint32_t x = 0;
    for (long long t = 0; t < total; t++) {
        int ok = 1;
        for (int k = 0; k < M && ok; k++) {
            uint32_t z = x ^ C[k];
            if (__builtin_popcount((z | (z >> 1)) & lo) < d) ok = 0;
        }
        if (ok) {
            if (found < 5) { printf("addable word: "); for (int i = 0; i < n; i++) putchar('0' + ((x >> (2 * i)) & 3)); putchar('\n'); }
            found++;
        }
        for (int i = 0; i < n; i++) { /* next word in base q */
            if (++digit[i] < q) { x += 1u << (2 * i); break; }
            digit[i] = 0; x &= ~(3u << (2 * i));
        }
    }
    printf("q=%d n=%d d=%d codewords=%d words scanned=%lld addable words=%lld\n", q, n, d, M, total, found);
    return 0;
}
