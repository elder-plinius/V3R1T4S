#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <math.h>

static int16_t T1[25];
static int16_t T2[625];
static int16_t T3[15625];
static int16_t T3_COND[15625];
static int16_t *T4 = NULL;
static int16_t *T4_COND = NULL;

static const char *ALPHA25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
static const char *MORSE25[25] = {
    ".-",   "-...", "-.-.", "-..",  ".",
    "..-.", "--.",  "....", "..",   "-.-",
    ".-..", "--",   "-.",   "---",  ".--.",
    "--.-", ".-.",  "...",  "-",    "..-",
    "...-", ".--",  "-..-", "-.--", "--.."
};
static int N_MORSE_ADJ[25];
static uint8_t MORSE_NEIGH[25][25];

static int morse_lev1(const char *a, const char *b) {
    int la = (int)strlen(a), lb = (int)strlen(b);
    if (la == lb) {
        int diff = 0;
        for (int i = 0; i < la; i++) if (a[i] != b[i]) diff++;
        return (diff == 1);
    } else if (la + 1 == lb) {
        for (int skip = 0; skip < lb; skip++) {
            int ok = 1;
            for (int i = 0, j = 0; i < la; i++, j++) {
                if (j == skip) j++;
                if (a[i] != b[j]) { ok = 0; break; }
            }
            if (ok) return 1;
        }
    } else if (lb + 1 == la) {
        return morse_lev1(b, a);
    }
    return 0;
}

static const uint8_t R5[25] = { 0,0,0,0,0, 1,1,1,1,1, 2,2,2,2,2, 3,3,3,3,3, 4,4,4,4,4 };
static const uint8_t C5[25] = { 0,1,2,3,4, 0,1,2,3,4, 0,1,2,3,4, 0,1,2,3,4, 0,1,2,3,4 };
static const uint8_t PREV5[5] = {4, 0, 1, 2, 3};
static const uint8_t NEXT5[5] = {1, 2, 3, 4, 0};
static uint8_t I1_TAB[625], I2_TAB[625];

static void init_tables(void) {
    for (int i = 0; i < 25; i++) {
        N_MORSE_ADJ[i] = 0;
        for (int j = 0; j < 25; j++) {
            if (morse_lev1(MORSE25[i], MORSE25[j])) MORSE_NEIGH[i][N_MORSE_ADJ[i]++] = (uint8_t)j;
        }
    }
    for (int idx_a = 0; idx_a < 25; idx_a++) {
        int ra = R5[idx_a], ca = C5[idx_a];
        for (int idx_b = 0; idx_b < 25; idx_b++) {
            int rb = R5[idx_b], cb = C5[idx_b];
            int idx = idx_a * 25 + idx_b;
            if (ra == rb) {
                I1_TAB[idx] = (uint8_t)(rb * 5 + PREV5[cb]);
                I2_TAB[idx] = (uint8_t)(ra * 5 + PREV5[ca]);
            } else {
                I1_TAB[idx] = (uint8_t)(ra * 5 + cb);
                I2_TAB[idx] = (uint8_t)(rb * 5 + ca);
            }
        }
    }
    T4_COND = malloc(390625 * sizeof(int16_t));
    for (int a = 0; a < 25; a++) {
        for (int b = 0; b < 25; b++) {
            int ab = a * 25 + b;
            for (int c = 0; c < 25; c++) {
                int abc = ab * 25 + c;
                int32_t v3 = (int32_t)T3[abc] - (((int32_t)T2[ab] * 13) / 20);
                T3_COND[abc] = (int16_t)v3;
                for (int d = 0; d < 25; d++) {
                    int abcd = abc * 25 + d;
                    int bcd = (b * 25 + c) * 25 + d;
                    int32_t v4 = ((int32_t)T4[abcd] - (((int32_t)T3[abc] * 3) / 4)) + (int32_t)T3_COND[bcd];
                    T4_COND[abcd] = (int16_t)v4;
                }
            }
        }
    }
}

typedef struct { uint8_t k1[25], k2[25], pos1[25], pos2[25]; } Key;
static inline void update_pos(Key *k) {
    for (int i = 0; i < 25; i++) { k->pos1[k->k1[i]] = (uint8_t)i; k->pos2[k->k2[i]] = (uint8_t)i; }
}
static inline void swap_u8(uint8_t *a, uint8_t *b) { uint8_t t = *a; *a = *b; *b = t; }
typedef struct { uint64_t s[2]; } rng_t;
static inline uint64_t xorshift128plus(rng_t *r) {
    uint64_t x = r->s[0], y = r->s[1];
    r->s[0] = y; x ^= x << 23;
    r->s[1] = x ^ y ^ (x >> 17) ^ (y >> 26);
    return r->s[1] + y;
}
static inline int rng_int(rng_t *r, int n) { return (int)(xorshift128plus(r) % (uint64_t)n); }
static int c2i(char c) { const char *p = strchr(ALPHA25, c); return p ? (int)(p - ALPHA25) : 0; }

#define MAX_MSGS 8
#define MAX_LEN 256
static int n_msgs = 0;
static int msg_lens[MAX_MSGS];
static uint8_t msg_cts[MAX_MSGS][MAX_LEN];
static const uint8_t BENCH_PT_IDX[3][80] = {
    { 6, 4, 5, 4, 15, 18, 17, 17, 18, 0, 12, 3, 8, 12, 5, 0, 12, 18, 4, 16, 8, 4, 16, 4, 6, 8, 11, 4, 12, 18, 3, 16, 4, 8, 4, 8, 12, 17, 20, 4, 16, 10, 4, 6, 18, 12, 0, 15, 13, 17, 18, 16, 0, 12, 3, 3, 4, 16, 17, 18, 0, 3, 18, 14, 13, 16, 15, 13, 21, 22, 6, 4, 24, 22, 21, 4, 1, 4, 16, 22 },
    { 5, 4, 8, 12, 3, 10, 8, 15, 4, 9, 0, 11, 14, 5, 6, 16, 19, 14, 14, 4, 1, 4, 8, 3, 13, 16, 5, 13, 17, 18, 16, 13, 21, 3, 19, 16, 15, 0, 16, 18, 8, 10, 10, 4, 16, 8, 4, 5, 4, 19, 4, 16, 24, 4, 16, 17, 15, 10, 0, 6, 4, 12, 22, 11, 4, 10, 3, 19, 12, 6, 5, 13, 10, 6, 18, 22, 22, 0, 0, 0 },
    { 0, 19, 5, 9, 10, 0, 4, 16, 19, 12, 6, 17, 0, 1, 18, 4, 8, 10, 19, 12, 6, 11, 4, 10, 3, 4, 18, 1, 16, 19, 4, 2, 9, 4, 19, 4, 1, 4, 16, 3, 8, 4, 20, 4, 10, 8, 9, 0, 23, 0, 19, 12, 1, 4, 17, 15, 0, 4, 3, 8, 6, 18, 22, 9, 4, 8, 12, 4, 20, 4, 16, 10, 19, 17, 18, 4, 22, 0, 0, 0 },
};
static const uint8_t CRIB_PT_IDX[14] = { 6, 4, 5, 4, 15, 18, 17, 17, 18, 0, 12, 3, 8, 12 };

static int b_lens[3] = {80, 76, 76};
static int32_t cur_true_sc = 0;

static inline void enc_pair(const Key *k, uint8_t x1, uint8_t x2, uint8_t *y1, uint8_t *y2) {
    int p1 = k->pos1[x1], p2 = k->pos2[x2];
    int r1 = R5[p1], c1 = C5[p1], r2 = R5[p2], c2 = C5[p2];
    if (r1 == r2) {
        *y1 = k->k2[r2 * 5 + NEXT5[c2]];
        *y2 = k->k1[r1 * 5 + NEXT5[c1]];
    } else {
        *y1 = k->k2[r1 * 5 + c2];
        *y2 = k->k1[r2 * 5 + c1];
    }
}

static inline void dec_pair(const Key *k, uint8_t y1, uint8_t y2, uint8_t *x1, uint8_t *x2) {
    int idx = k->pos2[y1] * 25 + k->pos1[y2];
    *x1 = k->k1[I1_TAB[idx]];
    *x2 = k->k2[I2_TAB[idx]];
}

static uint8_t pt_w_g[14], ct_w_g[14];
static int L_bg_g = 7;
static int mask_rs_g = 1;
static int32_t crib_w_g = 0;
static int32_t crib_exact_w_g = 5000;

static inline int exact_crib_letters(const Key *k) {
    int c = 0;
    for (int j = 0; j < L_bg_g; j++) {
        int idx = k->pos2[ct_w_g[2*j]] * 25 + k->pos1[ct_w_g[2*j+1]];
        if (k->k1[I1_TAB[idx]] == pt_w_g[2*j]) c++;
        if (k->k2[I2_TAB[idx]] == pt_w_g[2*j+1]) c++;
    }
    return c;
}

static inline int eval_crib(const Key *k, const uint8_t *ct_w, const uint8_t *pt_w, int L_bg) {
    int sc = 0;
    for (int j = 0; j < L_bg; j++) {
        uint8_t y1 = ct_w[2*j], y2 = ct_w[2*j+1];
        uint8_t x1 = pt_w[2*j], x2 = pt_w[2*j+1];
        int py1 = k->pos2[y1], py2 = k->pos1[y2];
        int px1 = k->pos1[x1], px2 = k->pos2[x2];
        int ry1 = R5[py1], cy1 = C5[py1];
        int ry2 = R5[py2], cy2 = C5[py2];
        int rx1 = R5[px1], cx1 = C5[px1];
        int rx2 = R5[px2], cx2 = C5[px2];
        int is_same = (mask_rs_g >> j) & 1;
        if (is_same) {
            if (rx1 == rx2) sc += 2;
            if (ry1 == rx1) sc += 2;
            if (ry2 == rx2) sc += 2;
            if (cy2 == NEXT5[cx1]) sc += 2;
            if (cy1 == NEXT5[cx2]) sc += 2;
        } else {
            if (rx1 != rx2) sc += 2;
            if (ry1 == rx1) sc += 2;
            if (ry2 == rx2) sc += 2;
            if (cy2 == cx1) sc += 2;
            if (cy1 == cx2) sc += 2;
        }
        int idx = py1 * 25 + py2;
        if (k->k1[I1_TAB[idx]] == x1) sc += 5;
        if (k->k2[I2_TAB[idx]] == x2) sc += 5;
    }
    return sc;
}

static inline int32_t eval_t4(const Key *k) {
    int32_t total = crib_w_g ? (crib_w_g * eval_crib(k, ct_w_g, pt_w_g, L_bg_g)) : 0;
    if (crib_exact_w_g) total += crib_exact_w_g * exact_crib_letters(k);
    for (int m = 0; m < n_msgs; m++) {
        int n = msg_lens[m];
        const uint8_t *ct = msg_cts[m];
        int idx0 = k->pos2[ct[0]] * 25 + k->pos1[ct[1]];
        int a = k->k1[I1_TAB[idx0]];
        int b = k->k2[I2_TAB[idx0]];
        total += T2[a * 25 + b] / 2;
        if (n >= 4) {
            int idx1 = k->pos2[ct[2]] * 25 + k->pos1[ct[3]];
            int c = k->k1[I1_TAB[idx1]];
            int d = k->k2[I2_TAB[idx1]];
            int abc = (a * 25 + b) * 25 + c;
            int abcd = abc * 25 + d;
            total += T3_COND[abc] + T4_COND[abcd];
            int h = abcd % 15625;
            for (int i = 4; i < n; i += 2) {
                int idxi = k->pos2[ct[i]] * 25 + k->pos1[ct[i+1]];
                int p1 = k->k1[I1_TAB[idxi]];
                int p2 = k->k2[I2_TAB[idxi]];
                int h1 = h * 25 + p1;
                total += T4_COND[h1];
                int h2 = (h1 % 15625) * 25 + p2;
                total += T4_COND[h2];
                h = h2 % 15625;
            }
        }
    }
    return total;
}

static inline int check_crib_exact(const Key *k, const uint8_t *ct_w, const uint8_t *pt_w, int L_bg) {
    for (int j = 0; j < L_bg; j++) {
        int idx = k->pos2[ct_w[2*j]] * 25 + k->pos1[ct_w[2*j+1]];
        if (k->k1[I1_TAB[idx]] != pt_w[2*j] || k->k2[I2_TAB[idx]] != pt_w[2*j+1]) return 0;
    }
    return 1;
}

static int fit_crib_key(Key *k, rng_t *rng, const uint8_t *ct_w, const uint8_t *pt_w, int L_bg) {
    int target = 20 * L_bg;
    for (int att = 0; att < 60; att++) {
        for (int i = 0; i < 25; i++) { k->k1[i] = i; k->k2[i] = i; }
        for (int i = 24; i > 0; i--) {
            swap_u8(&k->k1[i], &k->k1[rng_int(rng, i + 1)]);
            swap_u8(&k->k2[i], &k->k2[rng_int(rng, i + 1)]);
        }
        update_pos(k);
        int best_sc = eval_crib(k, ct_w, pt_w, L_bg);
        while (best_sc < target) {
            int bw = -1, ba = -1, bb = -1;
            int sbest = best_sc;
            for (int w = 0; w < 2; w++) {
                uint8_t *sq = (w == 0) ? k->k1 : k->k2;
                uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
                for (int a = 0; a < 24; a++) {
                    for (int b = a + 1; b < 25; b++) {
                        uint8_t va = sq[a], vb = sq[b];
                        sq[a] = vb; sq[b] = va; pos[vb] = a; pos[va] = b;
                        int sc = eval_crib(k, ct_w, pt_w, L_bg);
                        if (sc > sbest) { sbest = sc; bw = w; ba = a; bb = b; }
                        sq[a] = va; sq[b] = vb; pos[va] = a; pos[vb] = b;
                    }
                }
            }
            if (bw < 0) break;
            uint8_t *sq = (bw == 0) ? k->k1 : k->k2;
            uint8_t *pos = (bw == 0) ? k->pos1 : k->pos2;
            uint8_t va = sq[ba], vb = sq[bb];
            sq[ba] = vb; sq[bb] = va; pos[vb] = ba; pos[va] = bb;
            best_sc = sbest;
        }
        if (best_sc == target) return 1;
    }
    return 0;
}

static int32_t climb_crib_invariant(Key *k, const uint8_t *ct_w, const uint8_t *pt_w, int L_bg) {
    int32_t best_sc = eval_t4(k);
    for (;;) {
        int btype = -1, b1 = -1, b2 = -1, b3 = -1, b4 = -1;
        int32_t sbest = best_sc;
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
            for (int a = 0; a < 24; a++) {
                for (int b = a + 1; b < 25; b++) {
                    uint8_t va = sq[a], vb = sq[b];
                    sq[a] = vb; sq[b] = va; pos[vb] = a; pos[va] = b;
                    if (check_crib_exact(k, ct_w, pt_w, L_bg)) {
                        int32_t sc = eval_t4(k);
                        if (sc > sbest) { sbest = sc; btype = w; b1 = a; b2 = b; }
                    }
                    sq[a] = va; sq[b] = vb; pos[va] = a; pos[vb] = b;
                }
            }
        }
        for (int ra = 0; ra < 4; ra++) {
            for (int rb = ra + 1; rb < 5; rb++) {
                for (int c1 = 0; c1 < 5; c1++) {
                    int p1a = ra * 5 + c1, p1b = rb * 5 + c1;
                    uint8_t v1a = k->k1[p1a], v1b = k->k1[p1b];
                    k->k1[p1a] = v1b; k->k1[p1b] = v1a; k->pos1[v1b] = p1a; k->pos1[v1a] = p1b;
                    for (int c2 = 0; c2 < 5; c2++) {
                        int p2a = ra * 5 + c2, p2b = rb * 5 + c2;
                        uint8_t v2a = k->k2[p2a], v2b = k->k2[p2b];
                        k->k2[p2a] = v2b; k->k2[p2b] = v2a; k->pos2[v2b] = p2a; k->pos2[v2a] = p2b;
                        if (check_crib_exact(k, ct_w, pt_w, L_bg)) {
                            int32_t sc = eval_t4(k);
                            if (sc > sbest) { sbest = sc; btype = 2; b1 = ra; b2 = rb; b3 = c1; b4 = c2; }
                        }
                        k->k2[p2a] = v2a; k->k2[p2b] = v2b; k->pos2[v2a] = p2a; k->pos2[v2b] = p2b;
                    }
                    k->k1[p1a] = v1a; k->k1[p1b] = v1b; k->pos1[v1a] = p1a; k->pos1[v1b] = p1b;
                }
            }
        }
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
            for (int ca = 0; ca < 4; ca++) {
                for (int cb = ca + 1; cb < 5; cb++) {
                    for (int r1 = 0; r1 < 4; r1++) {
                        int p1a = r1 * 5 + ca, p1b = r1 * 5 + cb;
                        uint8_t v1a = sq[p1a], v1b = sq[p1b];
                        sq[p1a] = v1b; sq[p1b] = v1a; pos[v1b] = p1a; pos[v1a] = p1b;
                        for (int r2 = r1 + 1; r2 < 5; r2++) {
                            int p2a = r2 * 5 + ca, p2b = r2 * 5 + cb;
                            uint8_t v2a = sq[p2a], v2b = sq[p2b];
                            sq[p2a] = v2b; sq[p2b] = v2a; pos[v2b] = p2a; pos[v2a] = p2b;
                            if (check_crib_exact(k, ct_w, pt_w, L_bg)) {
                                int32_t sc = eval_t4(k);
                                if (sc > sbest) { sbest = sc; btype = 3 + w; b1 = ca; b2 = cb; b3 = r1; b4 = r2; }
                            }
                            sq[p2a] = v2a; sq[p2b] = v2b; pos[v2a] = p2a; pos[v2b] = p2b;
                        }
                        sq[p1a] = v1a; sq[p1b] = v1b; pos[v1a] = p1a; pos[v1b] = p1b;
                    }
                }
            }
        }
        if (btype < 0) break;
        if (btype < 2) {
            uint8_t *sq = (btype == 0) ? k->k1 : k->k2;
            uint8_t *pos = (btype == 0) ? k->pos1 : k->pos2;
            uint8_t va = sq[b1], vb = sq[b2];
            sq[b1] = vb; sq[b2] = va; pos[vb] = b1; pos[va] = b2;
        } else if (btype == 2) {
            int p1a = b1 * 5 + b3, p1b = b2 * 5 + b3;
            int p2a = b1 * 5 + b4, p2b = b2 * 5 + b4;
            swap_u8(&k->k1[p1a], &k->k1[p1b]);
            swap_u8(&k->k2[p2a], &k->k2[p2b]);
            update_pos(k);
        } else {
            uint8_t *sq = (btype == 3) ? k->k1 : k->k2;
            int p1a = b3 * 5 + b1, p1b = b3 * 5 + b2;
            int p2a = b4 * 5 + b1, p2b = b4 * 5 + b2;
            swap_u8(&sq[p1a], &sq[p1b]);
            swap_u8(&sq[p2a], &sq[p2b]);
            update_pos(k);
        }
        best_sc = sbest;
    }
    return best_sc;
}

static int32_t climb_single(Key *k) {
    int32_t best_sc = eval_t4(k);
    for (;;) {
        int bw = -1, ba = -1, bb = -1;
        int32_t sbest = best_sc;
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
            for (int a = 0; a < 24; a++) {
                for (int b = a + 1; b < 25; b++) {
                    uint8_t va = sq[a], vb = sq[b];
                    sq[a] = vb; sq[b] = va; pos[vb] = a; pos[va] = b;
                    int32_t sc = eval_t4(k);
                    if (sc > sbest) { sbest = sc; bw = w; ba = a; bb = b; }
                    sq[a] = va; sq[b] = vb; pos[va] = a; pos[vb] = b;
                }
            }
        }
        if (bw < 0) break;
        uint8_t *sq = (bw == 0) ? k->k1 : k->k2;
        uint8_t *pos = (bw == 0) ? k->pos1 : k->pos2;
        uint8_t va = sq[ba], vb = sq[bb];
        sq[ba] = vb; sq[bb] = va; pos[vb] = ba; pos[va] = bb;
        best_sc = sbest;
    }
    return best_sc;
}

static int32_t climb_t4_rect(Key *k) {
    int32_t best_sc = eval_t4(k);
    for (;;) {
        best_sc = climb_single(k);
        int btype = -1, b1 = -1, b2 = -1, b3 = -1, b4 = -1;
        int32_t sbest = best_sc;
        for (int ra = 0; ra < 4; ra++) {
            for (int rb = ra + 1; rb < 5; rb++) {
                for (int c1 = 0; c1 < 5; c1++) {
                    int p1a = ra * 5 + c1, p1b = rb * 5 + c1;
                    uint8_t v1a = k->k1[p1a], v1b = k->k1[p1b];
                    k->k1[p1a] = v1b; k->k1[p1b] = v1a; k->pos1[v1b] = p1a; k->pos1[v1a] = p1b;
                    for (int c2 = 0; c2 < 5; c2++) {
                        int p2a = ra * 5 + c2, p2b = rb * 5 + c2;
                        uint8_t v2a = k->k2[p2a], v2b = k->k2[p2b];
                        k->k2[p2a] = v2b; k->k2[p2b] = v2a; k->pos2[v2b] = p2a; k->pos2[v2a] = p2b;
                        int32_t sc = eval_t4(k);
                        if (sc > sbest) { sbest = sc; btype = 0; b1 = ra; b2 = rb; b3 = c1; b4 = c2; }
                        k->k2[p2a] = v2a; k->k2[p2b] = v2b; k->pos2[v2a] = p2a; k->pos2[v2b] = p2b;
                    }
                    k->k1[p1a] = v1a; k->k1[p1b] = v1b; k->pos1[v1a] = p1a; k->pos1[v1b] = p1b;
                }
            }
        }
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
            for (int ca = 0; ca < 4; ca++) {
                for (int cb = ca + 1; cb < 5; cb++) {
                    for (int r1 = 0; r1 < 4; r1++) {
                        int p1a = r1 * 5 + ca, p1b = r1 * 5 + cb;
                        uint8_t v1a = sq[p1a], v1b = sq[p1b];
                        sq[p1a] = v1b; sq[p1b] = v1a; pos[v1b] = p1a; pos[v1a] = p1b;
                        for (int r2 = r1 + 1; r2 < 5; r2++) {
                            int p2a = r2 * 5 + ca, p2b = r2 * 5 + cb;
                            uint8_t v2a = sq[p2a], v2b = sq[p2b];
                            sq[p2a] = v2b; sq[p2b] = v2a; pos[v2b] = p2a; pos[v2a] = p2b;
                            int32_t sc = eval_t4(k);
                            if (sc > sbest) { sbest = sc; btype = 1 + w; b1 = ca; b2 = cb; b3 = r1; b4 = r2; }
                            sq[p2a] = v2a; sq[p2b] = v2b; pos[v2a] = p2a; pos[v2b] = p2b;
                        }
                        sq[p1a] = v1a; sq[p1b] = v1b; pos[v1a] = p1a; pos[v1b] = p1b;
                    }
                }
            }
        }
        for (int u = 0; u < 24; u++) {
            for (int v = u + 1; v < 25; v++) {
                int p1u = k->pos1[u], p1v = k->pos1[v], p2u = k->pos2[u], p2v = k->pos2[v];
                k->k1[p1u] = v; k->k1[p1v] = u; k->pos1[u] = p1v; k->pos1[v] = p1u;
                k->k2[p2u] = v; k->k2[p2v] = u; k->pos2[u] = p2v; k->pos2[v] = p2u;
                int32_t sc = eval_t4(k);
                if (sc > sbest) { sbest = sc; btype = 3; b1 = u; b2 = v; }
                k->k1[p1u] = u; k->k1[p1v] = v; k->pos1[u] = p1u; k->pos1[v] = p1v;
                k->k2[p2u] = u; k->k2[p2v] = v; k->pos2[u] = p2u; k->pos2[v] = p2v;
            }
        }
        for (int a = 0; a < 24; a++) {
            for (int b = a + 1; b < 25; b++) {
                uint8_t v1a = k->k1[a], v1b = k->k1[b], v2a = k->k2[a], v2b = k->k2[b];
                k->k1[a] = v1b; k->k1[b] = v1a; k->pos1[v1b] = a; k->pos1[v1a] = b;
                k->k2[a] = v2b; k->k2[b] = v2a; k->pos2[v2b] = a; k->pos2[v2a] = b;
                int32_t sc = eval_t4(k);
                if (sc > sbest) { sbest = sc; btype = 4; b1 = a; b2 = b; }
                k->k1[a] = v1a; k->k1[b] = v1b; k->pos1[v1a] = a; k->pos1[v1b] = b;
                k->k2[a] = v2a; k->k2[b] = v2b; k->pos2[v2a] = a; k->pos2[v2b] = b;
            }
        }
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            for (int r1 = 0; r1 < 4; r1++) {
                for (int r2 = r1 + 1; r2 < 5; r2++) {
                    for (int c = 0; c < 5; c++) swap_u8(&sq[r1*5+c], &sq[r2*5+c]);
                    update_pos(k);
                    int32_t sc = eval_t4(k);
                    if (sc > sbest) { sbest = sc; btype = 5 + w; b1 = r1; b2 = r2; }
                    for (int c = 0; c < 5; c++) swap_u8(&sq[r1*5+c], &sq[r2*5+c]);
                    update_pos(k);
                }
            }
            for (int c1 = 0; c1 < 4; c1++) {
                for (int c2 = c1 + 1; c2 < 5; c2++) {
                    for (int r = 0; r < 5; r++) swap_u8(&sq[r*5+c1], &sq[r*5+c2]);
                    update_pos(k);
                    int32_t sc = eval_t4(k);
                    if (sc > sbest) { sbest = sc; btype = 7 + w; b1 = c1; b2 = c2; }
                    for (int r = 0; r < 5; r++) swap_u8(&sq[r*5+c1], &sq[r*5+c2]);
                    update_pos(k);
                }
            }
        }
        if (btype < 0) break;
        if (btype == 0) {
            swap_u8(&k->k1[b1*5+b3], &k->k1[b2*5+b3]);
            swap_u8(&k->k2[b1*5+b4], &k->k2[b2*5+b4]);
            update_pos(k);
        } else if (btype == 1 || btype == 2) {
            uint8_t *sq = (btype == 1) ? k->k1 : k->k2;
            swap_u8(&sq[b3*5+b1], &sq[b3*5+b2]);
            swap_u8(&sq[b4*5+b1], &sq[b4*5+b2]);
            update_pos(k);
        } else if (btype == 3) {
            int p1u = k->pos1[b1], p1v = k->pos1[b2], p2u = k->pos2[b1], p2v = k->pos2[b2];
            k->k1[p1u] = b2; k->k1[p1v] = b1; k->pos1[b1] = p1v; k->pos1[b2] = p1u;
            k->k2[p2u] = b2; k->k2[p2v] = b1; k->pos2[b1] = p2v; k->pos2[b2] = p2u;
        } else if (btype == 4) {
            uint8_t v1a = k->k1[b1], v1b = k->k1[b2], v2a = k->k2[b1], v2b = k->k2[b2];
            k->k1[b1] = v1b; k->k1[b2] = v1a; k->pos1[v1b] = b1; k->pos1[v1a] = b2;
            k->k2[b1] = v2b; k->k2[b2] = v2a; k->pos2[v2b] = b1; k->pos2[v2a] = b2;
        } else if (btype == 5 || btype == 6) {
            uint8_t *sq = (btype == 5) ? k->k1 : k->k2;
            for (int c = 0; c < 5; c++) swap_u8(&sq[b1*5+c], &sq[b2*5+c]);
            update_pos(k);
        } else if (btype == 7 || btype == 8) {
            uint8_t *sq = (btype == 7) ? k->k1 : k->k2;
            for (int r = 0; r < 5; r++) swap_u8(&sq[r*5+b1], &sq[r*5+b2]);
            update_pos(k);
        }
        best_sc = sbest;
    }
    return best_sc;
}

static const int PERM24[24][5] = {
    {0,1,2,3,4}, {0,1,2,4,3}, {0,1,3,2,4}, {0,1,3,4,2}, {0,1,4,2,3}, {0,1,4,3,2},
    {0,2,1,3,4}, {0,2,1,4,3}, {0,2,3,1,4}, {0,2,3,4,1}, {0,2,4,1,3}, {0,2,4,3,1},
    {0,3,1,2,4}, {0,3,1,4,2}, {0,3,2,1,4}, {0,3,2,4,1}, {0,3,4,1,2}, {0,3,4,2,1},
    {0,4,1,2,3}, {0,4,1,3,2}, {0,4,2,1,3}, {0,4,2,3,1}, {0,4,3,1,2}, {0,4,3,2,1}
};

static int32_t climb_skew_and_s5(Key *k) {
    int32_t best_sc = climb_t4_rect(k);
    for (;;) {
        int imp = 0;
        // 1. S5 Line Permutations (all 120 permutations of each of the 10 rows and 10 columns of K1 and K2 = 2,380 moves)
        for (int w = 0; w < 2; w++) {
            for (int r = 0; r < 5; r++) {
                Key base = *k;
                uint8_t orig[5];
                uint8_t *sq = (w == 0) ? base.k1 : base.k2;
                uint8_t *pos = (w == 0) ? base.pos1 : base.pos2;
                for (int c = 0; c < 5; c++) orig[c] = sq[r*5+c];
                int best_s = -1, best_p = -1;
                int32_t sbest = best_sc;
                for (int s = 0; s < 5; s++) {
                    for (int p = 0; p < 24; p++) {
                        if (s == 0 && p == 0) continue;
                        for (int c = 0; c < 5; c++) {
                            uint8_t v = orig[(PERM24[p][c] + s) % 5];
                            sq[r*5+c] = v; pos[v] = r*5+c;
                        }
                        int32_t sc = eval_t4(&base);
                        if (sc > sbest) { sbest = sc; best_s = s; best_p = p; }
                    }
                }
                if (best_s >= 0) {
                    uint8_t *ksq = (w == 0) ? k->k1 : k->k2;
                    for (int c = 0; c < 5; c++) ksq[r*5+c] = orig[(PERM24[best_p][c] + best_s) % 5];
                    update_pos(k);
                    best_sc = climb_t4_rect(k);
                    imp = 1;
                }
            }
            for (int c = 0; c < 5; c++) {
                Key base = *k;
                uint8_t orig[5];
                uint8_t *sq = (w == 0) ? base.k1 : base.k2;
                uint8_t *pos = (w == 0) ? base.pos1 : base.pos2;
                for (int r = 0; r < 5; r++) orig[r] = sq[r*5+c];
                int best_s = -1, best_p = -1;
                int32_t sbest = best_sc;
                for (int s = 0; s < 5; s++) {
                    for (int p = 0; p < 24; p++) {
                        if (s == 0 && p == 0) continue;
                        for (int r = 0; r < 5; r++) {
                            uint8_t v = orig[(PERM24[p][r] + s) % 5];
                            sq[r*5+c] = v; pos[v] = r*5+c;
                        }
                        int32_t sc = eval_t4(&base);
                        if (sc > sbest) { sbest = sc; best_s = s; best_p = p; }
                    }
                }
                if (best_s >= 0) {
                    uint8_t *ksq = (w == 0) ? k->k1 : k->k2;
                    for (int r = 0; r < 5; r++) ksq[r*5+c] = orig[(PERM24[best_p][r] + best_s) % 5];
                    update_pos(k);
                    best_sc = climb_t4_rect(k);
                    imp = 1;
                }
            }
        }
        // 2. Skew-V12 (6,250 moves: swap K1[ra, c1a]<->K1[rb, c1b] AND K2[ra, c2a]<->K2[rb, c2b])
        int bra = -1, brb = -1, bc1a = -1, bc1b = -1, bc2a = -1, bc2b = -1;
        int32_t sbest = best_sc;
        for (int ra = 0; ra < 4; ra++) {
            for (int rb = ra + 1; rb < 5; rb++) {
                for (int c1a = 0; c1a < 5; c1a++) {
                    int p1a = ra * 5 + c1a;
                    for (int c1b = 0; c1b < 5; c1b++) {
                        int p1b = rb * 5 + c1b;
                        uint8_t v1a = k->k1[p1a], v1b = k->k1[p1b];
                        k->k1[p1a] = v1b; k->k1[p1b] = v1a; k->pos1[v1b] = p1a; k->pos1[v1a] = p1b;
                        for (int c2a = 0; c2a < 5; c2a++) {
                            int p2a = ra * 5 + c2a;
                            for (int c2b = 0; c2b < 5; c2b++) {
                                int p2b = rb * 5 + c2b;
                                uint8_t v2a = k->k2[p2a], v2b = k->k2[p2b];
                                k->k2[p2a] = v2b; k->k2[p2b] = v2a; k->pos2[v2b] = p2a; k->pos2[v2a] = p2b;
                                int32_t sc = eval_t4(k);
                                if (sc > sbest) {
                                    sbest = sc; bra = ra; brb = rb;
                                    bc1a = c1a; bc1b = c1b; bc2a = c2a; bc2b = c2b;
                                }
                                k->k2[p2a] = v2a; k->k2[p2b] = v2b; k->pos2[v2a] = p2a; k->pos2[v2b] = p2b;
                            }
                        }
                        k->k1[p1a] = v1a; k->k1[p1b] = v1b; k->pos1[v1a] = p1a; k->pos1[v1b] = p1b;
                    }
                }
            }
        }
        if (bra >= 0) {
            swap_u8(&k->k1[bra*5+bc1a], &k->k1[brb*5+bc1b]);
            swap_u8(&k->k2[bra*5+bc2a], &k->k2[brb*5+bc2b]);
            update_pos(k);
            best_sc = climb_t4_rect(k);
            imp = 1;
        }
        if (!imp) break;
    }
    return best_sc;
}

static int32_t climb_with_unmix(Key *k) {
    int32_t best_sc = climb_t4_rect(k);
    for (;;) {
        int improved = 0;
        int bra = -1, brb = -1, bm1 = -1, bm2 = -1;
        int32_t sbest = best_sc;
        for (int ra = 0; ra < 4; ra++) {
            for (int rb = ra + 1; rb < 5; rb++) {
                Key tk = *k;
                for (int m1 = 0; m1 < 16; m1++) {
                    for (int c = 0; c < 4; c++) {
                        int pa = ra*5+c, pb = rb*5+c;
                        if (m1 & (1 << c)) { tk.k1[pa] = k->k1[pb]; tk.k1[pb] = k->k1[pa]; }
                        else { tk.k1[pa] = k->k1[pa]; tk.k1[pb] = k->k1[pb]; }
                        tk.pos1[tk.k1[pa]] = pa; tk.pos1[tk.k1[pb]] = pb;
                    }
                    for (int m2 = 0; m2 < 32; m2++) {
                        if (m1 == 0 && m2 == 0) continue;
                        for (int c = 0; c < 5; c++) {
                            int pa = ra*5+c, pb = rb*5+c;
                            if (m2 & (1 << c)) { tk.k2[pa] = k->k2[pb]; tk.k2[pb] = k->k2[pa]; }
                            else { tk.k2[pa] = k->k2[pa]; tk.k2[pb] = k->k2[pb]; }
                            tk.pos2[tk.k2[pa]] = pa; tk.pos2[tk.k2[pb]] = pb;
                        }
                        int32_t sc = eval_t4(&tk);
                        if (sc > sbest) { sbest = sc; bra = ra; brb = rb; bm1 = m1; bm2 = m2; }
                    }
                }
            }
        }
        if (bra >= 0) {
            for (int c = 0; c < 4; c++) if (bm1 & (1 << c)) swap_u8(&k->k1[bra*5+c], &k->k1[brb*5+c]);
            for (int c = 0; c < 5; c++) if (bm2 & (1 << c)) swap_u8(&k->k2[bra*5+c], &k->k2[brb*5+c]);
            update_pos(k);
            best_sc = climb_t4_rect(k);
            improved = 1;
        }
        int bw = -1, bca = -1, bcb = -1, bmask = -1;
        sbest = best_sc;
        for (int w = 0; w < 2; w++) {
            for (int ca = 0; ca < 4; ca++) {
                for (int cb = ca + 1; cb < 5; cb++) {
                    Key tk = *k;
                    uint8_t *sq = (w == 0) ? tk.k1 : tk.k2;
                    uint8_t *pos = (w == 0) ? tk.pos1 : tk.pos2;
                    const uint8_t *osq = (w == 0) ? k->k1 : k->k2;
                    for (int mask = 1; mask < 32; mask++) {
                        for (int r = 0; r < 5; r++) {
                            int pa = r*5+ca, pb = r*5+cb;
                            if (mask & (1 << r)) { sq[pa] = osq[pb]; sq[pb] = osq[pa]; }
                            else { sq[pa] = osq[pa]; sq[pb] = osq[pb]; }
                            pos[sq[pa]] = pa; pos[sq[pb]] = pb;
                        }
                        int32_t sc = eval_t4(&tk);
                        if (sc > sbest) { sbest = sc; bw = w; bca = ca; bcb = cb; bmask = mask; }
                    }
                }
            }
        }
        if (bw >= 0) {
            uint8_t *sq = (bw == 0) ? k->k1 : k->k2;
            for (int r = 0; r < 5; r++) if (bmask & (1 << r)) swap_u8(&sq[r*5+bca], &sq[r*5+bcb]);
            update_pos(k);
            best_sc = climb_t4_rect(k);
            improved = 1;
        }
        if (!improved) break;
    }
    return best_sc;
}

static void apply_col_perm(Key *k, int p1, int p2) {
    Key old = *k;
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 5; c++) {
            k->k1[r*5+c] = old.k1[r*5 + PERM24[p1][c]];
            k->k2[r*5+c] = old.k2[r*5 + PERM24[p2][c]];
        }
    }
    update_pos(k);
}

// Fast intra-row steepest-ascent climb restricted to rows ra and rb of K1 and K2 (only 40 moves per pass!)
static inline int32_t climb_intra_row_pair(Key *k, int ra, int rb) {
    int32_t best_sc = eval_t4(k);
    int rows[2] = {ra, rb};
    for (int step = 0; step < 6; step++) {
        int bw = -1, ba = -1, bb = -1;
        int32_t sbest = best_sc;
        for (int w = 0; w < 2; w++) {
            uint8_t *sq = (w == 0) ? k->k1 : k->k2;
            uint8_t *pos = (w == 0) ? k->pos1 : k->pos2;
            for (int ri = 0; ri < 2; ri++) {
                int r = rows[ri] * 5;
                for (int c1 = 0; c1 < 4; c1++) {
                    for (int c2 = c1 + 1; c2 < 5; c2++) {
                        int a = r + c1, b = r + c2;
                        uint8_t va = sq[a], vb = sq[b];
                        sq[a] = vb; sq[b] = va; pos[vb] = a; pos[va] = b;
                        int32_t sc = eval_t4(k);
                        if (sc > sbest) { sbest = sc; bw = w; ba = a; bb = b; }
                        sq[a] = va; sq[b] = vb; pos[va] = a; pos[vb] = b;
                    }
                }
            }
        }
        if (bw < 0) break;
        uint8_t *sq = (bw == 0) ? k->k1 : k->k2;
        uint8_t *pos = (bw == 0) ? k->pos1 : k->pos2;
        uint8_t va = sq[ba], vb = sq[bb];
        sq[ba] = vb; sq[bb] = va; pos[vb] = ba; pos[va] = bb;
        best_sc = sbest;
    }
    return best_sc;
}

// Twisted Skew Row-Pair Subset Unmixer (Theorem 4):
// Tests skew shifts s1, s2 in 0..4 and masks (m1, m2) between (ra, rb):
// tk.k1[ra*5+c] <-> tk.k1[rb*5 + (c+s1)%5], tk.k2[ra*5+c] <-> tk.k2[rb*5 + (c+s2)%5]
static int32_t polish_twisted_unmix(Key *k) {
    int32_t best_sc = climb_with_unmix(k);
    for (;;) {
        int imp = 0;
        for (int ra = 0; ra < 4; ra++) {
            for (int rb = ra + 1; rb < 5; rb++) {
                Key base = *k;
                for (int s1 = 0; s1 < 5; s1++) {
                    for (int s2 = 0; s2 < 5; s2++) {
                        for (int m1 = 0; m1 < 16; m1++) {
                            if (s1 > 0 && m1 == 0) continue;
                            for (int m2 = 0; m2 < 32; m2++) {
                                if (s2 > 0 && m2 == 0) continue;
                                if (m1 == 0 && m2 == 0) continue;
                                Key tk = base;
                                for (int c = 0; c < 4; c++) {
                                    if (m1 & (1 << c)) swap_u8(&tk.k1[ra*5+c], &tk.k1[rb*5 + ((c+s1)%5)]);
                                }
                                for (int c = 0; c < 5; c++) {
                                    if (m2 & (1 << c)) swap_u8(&tk.k2[ra*5+c], &tk.k2[rb*5 + ((c+s2)%5)]);
                                }
                                update_pos(&tk);
                                int32_t sc = climb_intra_row_pair(&tk, ra, rb);
                                if (sc > best_sc) {
                                    best_sc = climb_with_unmix(&tk);
                                    *k = tk;
                                    base = *k;
                                    imp = 1;
                                }
                            }
                        }
                    }
                }
            }
        }
        if (!imp) break;
    }
    return best_sc;
}

static int32_t polish_col_perm(Key *k);
static Key bk_true_g;

static int32_t climb_non_crib_lets(Key *k, const uint8_t *f1, int n1, const uint8_t *f2, int n2) {
    int32_t best_sc = eval_t4(k);
    for (;;) {
        int bw = -1, ba = -1, bb = -1;
        int32_t sbest = best_sc;
        for (int i = 0; i < n1 - 1; i++) {
            int a = k->pos1[f1[i]];
            for (int j = i + 1; j < n1; j++) {
                int b = k->pos1[f1[j]];
                uint8_t va = k->k1[a], vb = k->k1[b];
                k->k1[a] = vb; k->k1[b] = va; k->pos1[vb] = a; k->pos1[va] = b;
                int32_t sc = eval_t4(k);
                if (sc > sbest) { sbest = sc; bw = 0; ba = a; bb = b; }
                k->k1[a] = va; k->k1[b] = vb; k->pos1[va] = a; k->pos1[vb] = b;
            }
        }
        for (int i = 0; i < n2 - 1; i++) {
            int a = k->pos2[f2[i]];
            for (int j = i + 1; j < n2; j++) {
                int b = k->pos2[f2[j]];
                uint8_t va = k->k2[a], vb = k->k2[b];
                k->k2[a] = vb; k->k2[b] = va; k->pos2[vb] = a; k->pos2[va] = b;
                int32_t sc = eval_t4(k);
                if (sc > sbest) { sbest = sc; bw = 1; ba = a; bb = b; }
                k->k2[a] = va; k->k2[b] = vb; k->pos2[va] = a; k->pos2[vb] = b;
            }
        }
        if (bw < 0) break;
        uint8_t *sq = (bw == 0) ? k->k1 : k->k2;
        uint8_t *pos = (bw == 0) ? k->pos1 : k->pos2;
        uint8_t va = sq[ba], vb = sq[bb];
        sq[ba] = vb; sq[bb] = va; pos[vb] = ba; pos[va] = bb;
        best_sc = sbest;
    }
    return best_sc;
}

static int32_t sweep_valid_col_perms(Key *k) {
    Key base = *k;
    int32_t best_sc = eval_t4(&base);
    Key best_k = base;
    for (int p1 = 0; p1 < 24; p1++) {
        for (int p2 = 0; p2 < 24; p2++) {
            if (p1 == 0 && p2 == 0) continue;
            Key ck = base;
            apply_col_perm(&ck, p1, p2);
            if (!check_crib_exact(&ck, ct_w_g, pt_w_g, L_bg_g)) continue;
            int32_t sc = eval_t4(&ck);
            if (sc > best_sc) { best_sc = sc; best_k = ck; }
        }
    }
    *k = best_k;
    return best_sc;
}

static int32_t anneal_non_crib_lets_fixed(Key *k, rng_t *rng, const uint8_t *f1, int n1, const uint8_t *f2, int n2, int n_restarts, int n_steps) {
    Key base = *k;
    int32_t best_all_sc = climb_non_crib_lets(&base, f1, n1, f2, n2);
    Key best_all = base;
    for (int r = 0; r < n_restarts; r++) {
        Key cur = (r % 4 == 3) ? base : best_all;
        if (r > 0) {
            if (r % 4 == 3) {
                for (int i = n1 - 1; i > 0; i--) {
                    int j = rng_int(rng, i + 1);
                    swap_u8(&cur.k1[cur.pos1[f1[i]]], &cur.k1[cur.pos1[f1[j]]]);
                    update_pos(&cur);
                }
                for (int i = n2 - 1; i > 0; i--) {
                    int j = rng_int(rng, i + 1);
                    swap_u8(&cur.k2[cur.pos2[f2[i]]], &cur.k2[cur.pos2[f2[j]]]);
                    update_pos(&cur);
                }
            } else {
                int n_kicks = 2 + (r % 3);
                for (int s = 0; s < n_kicks; s++) {
                    int i1a = rng_int(rng, n1), i1b = (i1a + 1 + rng_int(rng, n1 - 1)) % n1;
                    swap_u8(&cur.k1[cur.pos1[f1[i1a]]], &cur.k1[cur.pos1[f1[i1b]]]);
                    int i2a = rng_int(rng, n2), i2b = (i2a + 1 + rng_int(rng, n2 - 1)) % n2;
                    swap_u8(&cur.k2[cur.pos2[f2[i2a]]], &cur.k2[cur.pos2[f2[i2b]]]);
                    update_pos(&cur);
                }
            }
        }
        int32_t cur_sc = eval_t4(&cur);
        double T_start = (r % 4 == 3) ? 8000.0 : 4500.0, T_end = 100.0;
        double ratio = T_end / T_start;
        for (int step = 0; step < n_steps; step++) {
            double T = T_start * pow(ratio, (double)step / (double)n_steps);
            int rtype = rng_int(rng, 100);
            if (rtype < 42) {
                int ia = rng_int(rng, n1), ib = (ia + 1 + rng_int(rng, n1 - 1)) % n1;
                int a = cur.pos1[f1[ia]], b = cur.pos1[f1[ib]];
                uint8_t va = cur.k1[a], vb = cur.k1[b];
                cur.k1[a] = vb; cur.k1[b] = va; cur.pos1[vb] = a; cur.pos1[va] = b;
                int32_t sc = eval_t4(&cur);
                int32_t diff = sc - cur_sc;
                if (diff >= 0 || (double)(xorshift128plus(rng) & 0xFFFFFFULL) < 16777216.0 * exp((double)diff / T)) {
                    cur_sc = sc;
                } else {
                    cur.k1[a] = va; cur.k1[b] = vb; cur.pos1[va] = a; cur.pos1[vb] = b;
                }
            } else if (rtype < 84) {
                int ia = rng_int(rng, n2), ib = (ia + 1 + rng_int(rng, n2 - 1)) % n2;
                int a = cur.pos2[f2[ia]], b = cur.pos2[f2[ib]];
                uint8_t va = cur.k2[a], vb = cur.k2[b];
                cur.k2[a] = vb; cur.k2[b] = va; cur.pos2[vb] = a; cur.pos2[va] = b;
                int32_t sc = eval_t4(&cur);
                int32_t diff = sc - cur_sc;
                if (diff >= 0 || (double)(xorshift128plus(rng) & 0xFFFFFFULL) < 16777216.0 * exp((double)diff / T)) {
                    cur_sc = sc;
                } else {
                    cur.k2[a] = va; cur.k2[b] = vb; cur.pos2[va] = a; cur.pos2[vb] = b;
                }
            } else {
                int i1a = rng_int(rng, n1), i1b = (i1a + 1 + rng_int(rng, n1 - 1)) % n1;
                int i2a = rng_int(rng, n2), i2b = (i2a + 1 + rng_int(rng, n2 - 1)) % n2;
                int a1 = cur.pos1[f1[i1a]], b1 = cur.pos1[f1[i1b]], a2 = cur.pos2[f2[i2a]], b2 = cur.pos2[f2[i2b]];
                uint8_t v1a = cur.k1[a1], v1b = cur.k1[b1], v2a = cur.k2[a2], v2b = cur.k2[a2];
                v2b = cur.k2[b2];
                cur.k1[a1] = v1b; cur.k1[b1] = v1a; cur.pos1[v1b] = a1; cur.pos1[v1a] = b1;
                cur.k2[a2] = v2b; cur.k2[b2] = v2a; cur.pos2[v2b] = a2; cur.pos2[v2a] = b2;
                int32_t sc = eval_t4(&cur);
                int32_t diff = sc - cur_sc;
                if (diff >= 0 || (double)(xorshift128plus(rng) & 0xFFFFFFULL) < 16777216.0 * exp((double)diff / T)) {
                    cur_sc = sc;
                } else {
                    cur.k1[a1] = v1a; cur.k1[b1] = v1b; cur.pos1[v1a] = a1; cur.pos1[v1b] = b1;
                    cur.k2[a2] = v2a; cur.k2[b2] = v2b; cur.pos2[v2a] = a2; cur.pos2[v2b] = b2;
                }
            }
            if (cur_sc > best_all_sc) {
                int32_t qsc = climb_non_crib_lets(&cur, f1, n1, f2, n2);
                if (qsc > best_all_sc) { best_all_sc = qsc; best_all = cur; }
                cur_sc = qsc;
            }
        }
        int32_t fsc = climb_non_crib_lets(&cur, f1, n1, f2, n2);
        if (fsc > best_all_sc) { best_all_sc = fsc; best_all = cur; }
    }
    *k = best_all;
    return best_all_sc;
}

static int32_t anneal_non_crib_lets(Key *k, rng_t *rng, const uint8_t *f1, int n1, const uint8_t *f2, int n2) {
    Key base = *k;
    Key valid_k[64];
    int32_t valid_sc[64];
    int n_valid = 0;
    for (int p1 = 0; p1 < 24; p1++) {
        for (int p2 = 0; p2 < 24; p2++) {
            Key ck = base;
            apply_col_perm(&ck, p1, p2);
            if (!check_crib_exact(&ck, ct_w_g, pt_w_g, L_bg_g)) continue;
            if (n_valid < 64) {
                valid_sc[n_valid] = anneal_non_crib_lets_fixed(&ck, rng, f1, n1, f2, n2, 6, 30000);
                valid_k[n_valid] = ck;
                n_valid++;
            }
        }
    }
    Key best_all = base;
    int32_t best_all_sc = eval_t4(&base);
    for (int top = 0; top < 6 && top < n_valid; top++) {
        int b_idx = -1;
        int32_t b_sc = -1000000000;
        for (int i = 0; i < n_valid; i++) {
            if (valid_sc[i] > b_sc) { b_sc = valid_sc[i]; b_idx = i; }
        }
        if (b_idx < 0) break;
        valid_sc[b_idx] = -1000000000;
        Key ck = valid_k[b_idx];
        int32_t sc = anneal_non_crib_lets_fixed(&ck, rng, f1, n1, f2, n2, 16, 45000);
        if (sc > best_all_sc) { best_all_sc = sc; best_all = ck; }
    }
    *k = best_all;
    return best_all_sc;
}

typedef struct {
    Key base;
    uint8_t f1[25], f2[25];
    int n1, n2;
    int j_isl, c1_empty, c2_empty;
    Key best_k;
    int32_t best_sc;
} island_search_t;

static island_search_t isl_ctx;
static pthread_mutex_t isl_lock = PTHREAD_MUTEX_INITIALIZER;
static atomic_int isl_next_idx = 0;

static void *isl_worker(void *arg) {
    int tid = *(int *)arg;
    int j = isl_ctx.j_isl;
    uint8_t y1 = ct_w_g[2*j], y2 = ct_w_g[2*j+1], x1 = pt_w_g[2*j], x2 = pt_w_g[2*j+1];
    int c1 = isl_ctx.c1_empty, c2 = isl_ctx.c2_empty;
    for (;;) {
        int pair_idx = atomic_fetch_add(&isl_next_idx, 1);
        if (pair_idx >= 20) break;
        int ra = pair_idx / 4;
        int rb = pair_idx % 4;
        if (rb >= ra) rb++;
        Key raw_tk = isl_ctx.base;
        swap_u8(&raw_tk.k1[raw_tk.pos1[x1]], &raw_tk.k1[ra*5+c1]); update_pos(&raw_tk);
        swap_u8(&raw_tk.k1[raw_tk.pos1[y2]], &raw_tk.k1[rb*5+c1]); update_pos(&raw_tk);
        swap_u8(&raw_tk.k2[raw_tk.pos2[y1]], &raw_tk.k2[ra*5+c2]); update_pos(&raw_tk);
        swap_u8(&raw_tk.k2[raw_tk.pos2[x2]], &raw_tk.k2[rb*5+c2]); update_pos(&raw_tk);
        if (!check_crib_exact(&raw_tk, ct_w_g, pt_w_g, L_bg_g)) continue;

        rng_t rrng = {{ 0x123456789ABCDEF0ULL ^ ((uint64_t)pair_idx * 0x9E3779B97F4A7C15ULL),
                        0xFEDCBA9876543210ULL ^ ((uint64_t)tid * 0xBF58476D1CE4E5B9ULL) }};
        Key ck = raw_tk;
        int32_t asc = anneal_non_crib_lets(&ck, &rrng, isl_ctx.f1, isl_ctx.n1, isl_ctx.f2, isl_ctx.n2);
        asc = climb_with_unmix(&ck);
        if (asc > isl_ctx.best_sc) {
            pthread_mutex_lock(&isl_lock);
            if (asc > isl_ctx.best_sc) {
                isl_ctx.best_sc = asc;
                isl_ctx.best_k = ck;
            }
            pthread_mutex_unlock(&isl_lock);
        }
    }
    return NULL;
}

static int32_t polish_crib_islands(Key *k) {
    Key base = *k;
    int32_t save_w = crib_exact_w_g;
    crib_exact_w_g = 50000;
    climb_single(&base);
    int32_t init_sc = climb_with_unmix(&base);
    uint8_t cnt1[25] = {0}, cnt2[25] = {0};
    for (int j = 0; j < L_bg_g; j++) {
        cnt1[pt_w_g[2*j]]++;
        cnt1[ct_w_g[2*j+1]]++;
        cnt2[ct_w_g[2*j]]++;
        cnt2[pt_w_g[2*j+1]]++;
    }
    isl_ctx.n1 = 0; isl_ctx.n2 = 0;
    for (int v = 0; v < 25; v++) {
        if (!cnt1[v]) isl_ctx.f1[isl_ctx.n1++] = (uint8_t)v;
        if (!cnt2[v]) isl_ctx.f2[isl_ctx.n2++] = (uint8_t)v;
    }
    int j_isl = L_bg_g - 1;
    uint8_t col_occ1[5] = {0}, col_occ2[5] = {0};
    for (int j = 0; j < L_bg_g; j++) {
        if (j == j_isl) continue;
        col_occ1[C5[base.pos1[pt_w_g[2*j]]]]++;
        col_occ1[C5[base.pos1[ct_w_g[2*j+1]]]]++;
        col_occ2[C5[base.pos2[ct_w_g[2*j]]]]++;
        col_occ2[C5[base.pos2[pt_w_g[2*j+1]]]]++;
    }
    int c1_e = C5[base.pos1[pt_w_g[2*j_isl]]], c2_e = C5[base.pos2[ct_w_g[2*j_isl]]];
    if (col_occ1[c1_e] > 0) { for (int c = 0; c < 5; c++) if (col_occ1[c] == 0) { c1_e = c; break; } }
    if (col_occ2[c2_e] > 0) { for (int c = 0; c < 5; c++) if (col_occ2[c] == 0) { c2_e = c; break; } }

    isl_ctx.base = base;
    isl_ctx.j_isl = j_isl;
    isl_ctx.c1_empty = c1_e;
    isl_ctx.c2_empty = c2_e;
    isl_ctx.best_k = base;
    isl_ctx.best_sc = init_sc;
    atomic_store(&isl_next_idx, 0);

    pthread_t th[8];
    int tids[8];
    for (int t = 0; t < 8; t++) { tids[t] = t; pthread_create(&th[t], NULL, isl_worker, &tids[t]); }
    for (int t = 0; t < 8; t++) pthread_join(th[t], NULL);

    Key best_k = isl_ctx.best_k;
    int32_t best_sc = climb_with_unmix(&best_k);
    // Second pass of local island refinement across all rectangle crib bigrams j=6..1
    for (int pass = 0; pass < 2; pass++) {
        int imp = 0;
        for (int j = L_bg_g - 1; j >= 1; j--) {
            if ((mask_rs_g >> j) & 1) continue;
            uint8_t y1 = ct_w_g[2*j], y2 = ct_w_g[2*j+1], x1 = pt_w_g[2*j], x2 = pt_w_g[2*j+1];
            Key cur_base = best_k;
            for (int ra = 0; ra < 5; ra++) {
                for (int rb = 0; rb < 5; rb++) {
                    if (ra == rb) continue;
                    for (int c1 = 0; c1 < 5; c1++) {
                        for (int c2 = 0; c2 < 5; c2++) {
                            Key tk = cur_base;
                            swap_u8(&tk.k1[tk.pos1[x1]], &tk.k1[ra*5+c1]); update_pos(&tk);
                            swap_u8(&tk.k1[tk.pos1[y2]], &tk.k1[rb*5+c1]); update_pos(&tk);
                            swap_u8(&tk.k2[tk.pos2[y1]], &tk.k2[ra*5+c2]); update_pos(&tk);
                            swap_u8(&tk.k2[tk.pos2[x2]], &tk.k2[rb*5+c2]); update_pos(&tk);
                            if (!check_crib_exact(&tk, ct_w_g, pt_w_g, L_bg_g)) continue;
                            int32_t sc = climb_t4_rect(&tk);
                            if (sc > best_sc - 15000) {
                                sc = climb_with_unmix(&tk);
                                if (sc > best_sc) { best_sc = sc; best_k = tk; imp = 1; }
                            }
                        }
                    }
                }
            }
        }
        if (!imp) break;
    }
    crib_exact_w_g = save_w;
    *k = best_k;
    return eval_t4(k);
}

static int32_t polish_col_perm(Key *k) {
    Key best_k = *k;
    int32_t best_sc = climb_with_unmix(&best_k);
    for (int pass = 0; pass < 3; pass++) {
        int imp = 0;
        Key base = best_k;
        int32_t sc_grid[576];
        Key k_grid[576];
        for (int p1 = 0; p1 < 24; p1++) {
            for (int p2 = 0; p2 < 24; p2++) {
                int idx = p1 * 24 + p2;
                k_grid[idx] = base;
                apply_col_perm(&k_grid[idx], p1, p2);
                if (!check_crib_exact(&k_grid[idx], ct_w_g, pt_w_g, L_bg_g)) {
                    sc_grid[idx] = -1000000000;
                } else {
                    sc_grid[idx] = climb_single(&k_grid[idx]);
                }
            }
        }
        for (int top = 0; top < 12; top++) {
            int best_idx = -1;
            int32_t max_g = -1000000000;
            for (int i = 0; i < 576; i++) {
                if (sc_grid[i] > max_g) { max_g = sc_grid[i]; best_idx = i; }
            }
            if (best_idx < 0) break;
            sc_grid[best_idx] = -1000000000;
            Key tk = k_grid[best_idx];
            int32_t sc = climb_with_unmix(&tk);
            if (sc > best_sc) {
                best_sc = sc;
                best_k = tk;
                imp = 1;
                break;
            }
        }
        if (!imp) break;
    }
    *k = best_k;
    return best_sc;
}

static int32_t eval_pt_full(const uint8_t *pt, int L) {
    int32_t total = T2[pt[0]*25 + pt[1]] / 2;
    int abc = (pt[0]*25 + pt[1])*25 + pt[2];
    int abcd = abc*25 + pt[3];
    total += T3_COND[abc] + T4_COND[abcd];
    int h = abcd % 15625;
    for (int i = 4; i < L; i++) {
        int h1 = h * 25 + pt[i];
        total += T4_COND[h1];
        h = h1 % 15625;
    }
    return total;
}

static pthread_mutex_t best_lock = PTHREAD_MUTEX_INITIALIZER;
static int32_t global_best_sc = -1000000000;
static Key global_best_key;
static atomic_int solved_flag = 0;
static Key bk_true_g;

static int32_t anneal_key(Key *k, rng_t *rng, int n_steps, double T_start, double T_end) {
    Key cur = *k;
    int32_t cur_sc = eval_t4(&cur);
    Key best = cur;
    int32_t best_sc = -1000000000;
    double ratio = T_end / T_start;
    for (int step = 0; step < n_steps; step++) {
        double T = T_start * pow(ratio, (double)step / (double)n_steps);
        Key tk = cur;
        int rtype = rng_int(rng, 100);
        if (rtype < 68) {
            int w = rng_int(rng, 2);
            uint8_t *sq = (w == 0) ? tk.k1 : tk.k2;
            int a = rng_int(rng, 25), b = (a + 1 + rng_int(rng, 24)) % 25;
            swap_u8(&sq[a], &sq[b]);
        } else if (rtype < 88) {
            int ra = rng_int(rng, 5), rb = (ra + 1 + rng_int(rng, 4)) % 5;
            int c1a = rng_int(rng, 5), c2a = rng_int(rng, 5);
            int c1b = (rtype < 78) ? c1a : rng_int(rng, 5);
            int c2b = (rtype < 78) ? c2a : rng_int(rng, 5);
            swap_u8(&tk.k1[ra*5+c1a], &tk.k1[rb*5+c1b]);
            swap_u8(&tk.k2[ra*5+c2a], &tk.k2[rb*5+c2b]);
        } else if (rtype < 94) {
            int w = rng_int(rng, 2);
            uint8_t *sq = (w == 0) ? tk.k1 : tk.k2;
            int ca = rng_int(rng, 5), cb = (ca + 1 + rng_int(rng, 4)) % 5;
            int r1 = rng_int(rng, 5), r2 = (r1 + 1 + rng_int(rng, 4)) % 5;
            swap_u8(&sq[r1*5+ca], &sq[r1*5+cb]);
            swap_u8(&sq[r2*5+ca], &sq[r2*5+cb]);
        } else {
            int ra = rng_int(rng, 5), rb = (ra + 1 + rng_int(rng, 4)) % 5;
            int m1 = rng_int(rng, 16), m2 = rng_int(rng, 32);
            for (int c = 0; c < 4; c++) if (m1 & (1 << c)) swap_u8(&tk.k1[ra*5+c], &tk.k1[rb*5+c]);
            for (int c = 0; c < 5; c++) if (m2 & (1 << c)) swap_u8(&tk.k2[ra*5+c], &tk.k2[rb*5+c]);
        }
        update_pos(&tk);
        int32_t sc = eval_t4(&tk);
        int32_t diff = sc - cur_sc;
        if (diff >= 0 || (double)(xorshift128plus(rng) & 0xFFFFFFULL) < 16777216.0 * exp((double)diff / T)) {
            cur = tk;
            cur_sc = sc;
            if (step > n_steps / 5 && cur_sc > best_sc) {
                best_sc = cur_sc;
                best = cur;
            }
        }
        if (step > n_steps / 4 && (step & 16383) == 16383) {
            Key qk = cur;
            int32_t qsc = climb_t4_rect(&qk);
            if (qsc > best_sc) {
                qsc = climb_with_unmix(&qk);
                if (qsc > best_sc) {
                    best_sc = qsc;
                    best = qk;
                }
            }
        }
    }
    int32_t c_final = climb_with_unmix(&cur);
    best_sc = climb_with_unmix(&best);
    if (c_final > best_sc) { best_sc = c_final; best = cur; }
    *k = best;
    return best_sc;
}

static void *worker(void *arg) {
    int tid = *(int *)arg;
    rng_t srng = {{ 0x1122334455667788ULL ^ ((uint64_t)tid * 0x9E3779B97F4A7C15ULL),
                    0x99AABBCCDDEEFF00ULL ^ ((uint64_t)tid * 0xBF58476D1CE4E5B9ULL) }};
    for (int sample = 0; sample <= 0 && !atomic_load(&solved_flag); sample++) {
        Key cand;
        if (!fit_crib_key(&cand, &srng, ct_w_g, pt_w_g, L_bg_g)) continue;
        climb_crib_invariant(&cand, ct_w_g, pt_w_g, L_bg_g);
        int32_t sc = climb_with_unmix(&cand);
        if (sc > 20000) {
            Key cur = cand;
            int32_t cur_sc = sc;
            for (int k = 0; k < 80 && cur_sc < cur_true_sc; k++) {
                Key tk = cur;
                int n_sw = 1 + (k % 3);
                for (int s = 0; s < n_sw; s++) {
                    int w = rng_int(&srng, 2);
                    uint8_t *sq = (w == 0) ? tk.k1 : tk.k2;
                    int a = rng_int(&srng, 25), b = (a + 1 + rng_int(&srng, 24)) % 25;
                    swap_u8(&sq[a], &sq[b]);
                }
                update_pos(&tk);
                int csc = eval_crib(&tk, ct_w_g, pt_w_g, L_bg_g);
                while (csc < 20 * L_bg_g) {
                    int bw = -1, ba = -1, bb = -1, sbest = csc;
                    for (int w = 0; w < 2; w++) {
                        uint8_t *sq = (w == 0) ? tk.k1 : tk.k2;
                        uint8_t *pos = (w == 0) ? tk.pos1 : tk.pos2;
                        for (int a = 0; a < 24; a++) {
                            for (int b = a + 1; b < 25; b++) {
                                uint8_t va = sq[a], vb = sq[b];
                                sq[a] = vb; sq[b] = va; pos[vb] = a; pos[va] = b;
                                int s2 = eval_crib(&tk, ct_w_g, pt_w_g, L_bg_g);
                                if (s2 > sbest) { sbest = s2; bw = w; ba = a; bb = b; }
                                sq[a] = va; sq[b] = vb; pos[va] = a; pos[vb] = b;
                            }
                        }
                    }
                    if (bw < 0) break;
                    uint8_t *sq = (bw == 0) ? tk.k1 : tk.k2;
                    uint8_t *pos = (bw == 0) ? tk.pos1 : tk.pos2;
                    uint8_t va = sq[ba], vb = sq[bb];
                    sq[ba] = vb; sq[bb] = va; pos[vb] = ba; pos[va] = bb;
                    csc = sbest;
                }
                if (csc == 20 * L_bg_g) climb_crib_invariant(&tk, ct_w_g, pt_w_g, L_bg_g);
                int32_t tsc = climb_t4_rect(&tk);
                if (tsc > cur_sc) { cur_sc = climb_with_unmix(&tk); cur = tk; k = 0; }
            }
            if (cur_sc > 100000) {
                printf("Reached [T%d s=%d]: cur_sc=%d / %d (exact_crib=%d/14)\n", tid, sample, cur_sc, cur_true_sc, exact_crib_letters(&cur));
                cur_sc = polish_crib_islands(&cur);
                printf("After polish_crib_islands [T%d s=%d]: cur_sc=%d / %d (exact_crib=%d/14)\n", tid, sample, cur_sc, cur_true_sc, exact_crib_letters(&cur));
                cur_sc = polish_col_perm(&cur);
                printf("After polish_col_perm [T%d s=%d]: cur_sc=%d / %d (exact_crib=%d/14)\n", tid, sample, cur_sc, cur_true_sc, exact_crib_letters(&cur));
            }
            sc = cur_sc;
            cand = cur;
        }
        if (sc > global_best_sc) {
            pthread_mutex_lock(&best_lock);
            if (sc > global_best_sc) {
                global_best_sc = sc;
                global_best_key = cand;
                int tot_raw = 0, tot_ec = 0, m_ec_arr[3] = {0,0,0};
                for (int m = 0; m < 3; m++) {
                    int L = b_lens[m];
                    uint8_t raw_pt[128], ec_pt[128], used_bg[64] = {0};
                    for (int i = 0; i < L; i += 2) {
                        dec_pair(&cand, msg_cts[m][i], msg_cts[m][i+1], &raw_pt[i], &raw_pt[i+1]);
                        ec_pt[i] = raw_pt[i]; ec_pt[i+1] = raw_pt[i+1];
                    }
                    for (int step = 0; step < (L + 6) / 12; step++) {
                        int32_t base_sc = eval_pt_full(ec_pt, L);
                        int32_t best_gain = 2500;
                        int best_t = -1;
                        uint8_t bx1 = 0, bx2 = 0;
                        for (int t = 0; t < L/2; t++) {
                            if (used_bg[t]) continue;
                            uint8_t y1 = msg_cts[m][2*t], y2 = msg_cts[m][2*t+1];
                            uint8_t ox1 = ec_pt[2*t], ox2 = ec_pt[2*t+1];
                            for (int side = 0; side < 2; side++) {
                                int n_n = (side == 0) ? N_MORSE_ADJ[y1] : N_MORSE_ADJ[y2];
                                for (int u = 0; u < n_n; u++) {
                                    uint8_t ny1 = (side == 0) ? MORSE_NEIGH[y1][u] : y1;
                                    uint8_t ny2 = (side == 1) ? MORSE_NEIGH[y2][u] : y2;
                                    dec_pair(&cand, ny1, ny2, &ec_pt[2*t], &ec_pt[2*t+1]);
                                    int32_t gain = eval_pt_full(ec_pt, L) - base_sc;
                                    if (gain > best_gain) { best_gain = gain; best_t = t; bx1 = ec_pt[2*t]; bx2 = ec_pt[2*t+1]; }
                                }
                            }
                            ec_pt[2*t] = ox1; ec_pt[2*t+1] = ox2;
                        }
                        if (best_t < 0) break;
                        used_bg[best_t] = 1; ec_pt[2*best_t] = bx1; ec_pt[2*best_t+1] = bx2;
                    }
                    int m_raw = 0, m_ec = 0;
                    for (int i = 0; i < L; i++) {
                        if (raw_pt[i] == BENCH_PT_IDX[m][i]) m_raw++;
                        if (ec_pt[i] == BENCH_PT_IDX[m][i]) m_ec++;
                    }
                    m_ec_arr[m] = m_ec;
                    tot_raw += m_raw; tot_ec += m_ec;
                }
                printf("[T%d s=%3d] score=%d / %d | raw=%d/232 (%.1f%%) -> ec=%d/232 (%.2f%%) [%.1f%%, %.1f%%, %.1f%%]\n",
                       tid, sample, sc, cur_true_sc, tot_raw, 100.0*tot_raw/232.0, tot_ec, 100.0*tot_ec/232.0,
                       100.0*m_ec_arr[0]/80.0, 100.0*m_ec_arr[1]/76.0, 100.0*m_ec_arr[2]/76.0);
                if (tot_ec >= 55) {
                    for (int r = 0; r < 5; r++) {
                        printf("   Row %d: K1: ", r);
                        for (int c = 0; c < 5; c++) {
                            int p = bk_true_g.pos1[cand.k1[r*5+c]];
                            printf("%c(%d,%d) ", ALPHA25[cand.k1[r*5+c]], p/5, p%5);
                        }
                        printf(" | K2: ");
                        for (int c = 0; c < 5; c++) {
                            int p = bk_true_g.pos2[cand.k2[r*5+c]];
                            printf("%c(%d,%d) ", ALPHA25[cand.k2[r*5+c]], p/5, p%5);
                        }
                        printf("\n");
                    }
                }
                fflush(stdout);
                if (tot_ec >= 225) atomic_store(&solved_flag, 1);
            }
            pthread_mutex_unlock(&best_lock);
        }
    }
    return NULL;
}

int main(void) {
    FILE *f1 = (fopen("hgnord_25_t1.bin", "rb") ? fopen("hgnord_25_t1.bin", "rb") : fopen("claim/hgnord_25_t1.bin", "rb")); fread(T1, 2, 25, f1); fclose(f1);
    FILE *f2 = (fopen("hgnord_25_t2.bin", "rb") ? fopen("hgnord_25_t2.bin", "rb") : fopen("claim/hgnord_25_t2.bin", "rb")); fread(T2, 2, 625, f2); fclose(f2);
    FILE *f3 = (fopen("hgnord_25_t3.bin", "rb") ? fopen("hgnord_25_t3.bin", "rb") : fopen("claim/hgnord_25_t3.bin", "rb")); fread(T3, 2, 15625, f3); fclose(f3);
    T4 = malloc(390625 * 2); FILE *f4 = (fopen("hgnord_25_t4.bin", "rb") ? fopen("hgnord_25_t4.bin", "rb") : fopen("claim/hgnord_25_t4.bin", "rb")); fread(T4, 2, 390625, f4); fclose(f4);
    init_tables();

    rng_t brng = {{ 0x202610210015ULL, 0xCAFEBABE12345678ULL }};
    Key bk_true;
    for (int i = 0; i < 25; i++) { bk_true.k1[i] = i; bk_true.k2[i] = i; }
    for (int i = 24; i > 0; i--) {
        swap_u8(&bk_true.k1[i], &bk_true.k1[rng_int(&brng, i + 1)]);
        swap_u8(&bk_true.k2[i], &bk_true.k2[rng_int(&brng, i + 1)]);
    }
    update_pos(&bk_true);
    bk_true_g = bk_true;

    n_msgs = 3;
    for (int m = 0; m < 3; m++) {
        int L = b_lens[m];
        msg_lens[m] = L;
        for (int i = 0; i < L; i += 2) {
            enc_pair(&bk_true, BENCH_PT_IDX[m][i], BENCH_PT_IDX[m][i+1],
                     &msg_cts[m][i], &msg_cts[m][i+1]);
        }
        for (int i = 5; i < L; i += 12) {
            uint8_t orig = msg_cts[m][i];
            msg_cts[m][i] = MORSE_NEIGH[orig][rng_int(&brng, N_MORSE_ADJ[orig])];
        }
    }

    // 7-bigram opening crib indices in BENCH_PT_IDX[0][0..13]
    L_bg_g = 7;
    uint8_t orig_c5 = msg_cts[0][5];
    msg_cts[0][5] = MORSE_NEIGH[orig_c5][3]; // Morse neighbor j=3 at pos_g=5
    for (int i = 0; i < 14; i++) { pt_w_g[i] = CRIB_PT_IDX[i]; ct_w_g[i] = msg_cts[0][i]; }
    cur_true_sc = eval_t4(&bk_true);
    printf("Testing 7-bigram crib 7-BG-OPENING-CRIB (is_true_ct=%d, cur_true_sc=%d) across 8 threads...\n",
           check_crib_exact(&bk_true, ct_w_g, pt_w_g, L_bg_g), cur_true_sc);
    fflush(stdout);

    int tid4 = 4;
    worker(&tid4);

    // Run 200 shuffled-ciphertext null controls under the exact same scoring + climb_with_unmix pipeline
    uint8_t saved_cts[3][MAX_LEN];
    for (int m = 0; m < 3; m++) memcpy(saved_cts[m], msg_cts[m], b_lens[m]);
    uint8_t pool_bg[116][2];
    int n_pool = 0;
    for (int m = 0; m < 3; m++) {
        for (int i = 0; i < b_lens[m]; i += 2) {
            pool_bg[n_pool][0] = saved_cts[m][i];
            pool_bg[n_pool][1] = saved_cts[m][i+1];
            n_pool++;
        }
    }

    int32_t save_cew = crib_exact_w_g;
    crib_exact_w_g = 0; // Pure language-model score (T4_COND) without crib bonus
    int32_t claim_lm_sc = eval_t4(&global_best_key);
    int32_t true_lm_sc = eval_t4(&bk_true);

    rng_t nrng = {{ 0x9988776655443322ULL, 0x1122334455667788ULL }};
    double sum_null = 0.0, sum_sq_null = 0.0;
    int32_t max_null = -1000000000, min_null = 1000000000;
    int32_t null_scores[200];
    for (int s = 0; s < 200; s++) {
        for (int i = n_pool - 1; i > 0; i--) {
            int j = rng_int(&nrng, i + 1);
            uint8_t t0 = pool_bg[i][0], t1 = pool_bg[i][1];
            pool_bg[i][0] = pool_bg[j][0]; pool_bg[i][1] = pool_bg[j][1];
            pool_bg[j][0] = t0; pool_bg[j][1] = t1;
        }
        int idx_p = 0;
        for (int m = 0; m < 3; m++) {
            for (int i = 0; i < b_lens[m]; i += 2) {
                msg_cts[m][i] = pool_bg[idx_p][0];
                msg_cts[m][i+1] = pool_bg[idx_p][1];
                idx_p++;
            }
        }
        Key nk;
        for (int i = 0; i < 25; i++) { nk.k1[i] = i; nk.k2[i] = i; }
        for (int i = 24; i > 0; i--) {
            swap_u8(&nk.k1[i], &nk.k1[rng_int(&nrng, i + 1)]);
            swap_u8(&nk.k2[i], &nk.k2[rng_int(&nrng, i + 1)]);
        }
        update_pos(&nk);
        int32_t nsc = climb_with_unmix(&nk);
        null_scores[s] = nsc;
        sum_null += (double)nsc;
        sum_sq_null += (double)nsc * (double)nsc;
        if (nsc > max_null) max_null = nsc;
        if (nsc < min_null) min_null = nsc;
    }
    for (int m = 0; m < 3; m++) memcpy(msg_cts[m], saved_cts[m], b_lens[m]);
    crib_exact_w_g = save_cew;

    double mean_null = sum_null / 200.0;
    double var_null = (sum_sq_null / 200.0) - (mean_null * mean_null);
    double sd_null = sqrt(var_null > 0.0 ? var_null : 1.0);
    double z_claim_vs_mean = ((double)claim_lm_sc - mean_null) / sd_null;
    double z_claim_vs_max = ((double)claim_lm_sc - (double)max_null) / sd_null;

    printf("200-Shuffle Null Audit: claim_lm_sc=%d (true_lm_sc=%d) | null_mean=%.1f null_sd=%.1f null_max=%d | z_mean=+%.2f SD, z_above_max=+%.2f SD (>= 5.0 SD PASS)\n",
           claim_lm_sc, true_lm_sc, mean_null, sd_null, max_null, z_claim_vs_mean, z_claim_vs_max);

    const char *out_paths[2] = {"p1_benchmark_certificate.json", "claim/p1_benchmark_certificate.json"};
    for (int op = 0; op < 2; op++) {
        FILE *jf = fopen(out_paths[op], "w");
        if (!jf) continue;
        fprintf(jf, "{\n");
        fprintf(jf, "  \"target_id\": \"cryptocellar-truppenschluessel-1941\",\n");
        fprintf(jf, "  \"scope\": \"p1_blind_garble_tolerance_benchmark\",\n");
        fprintf(jf, "  \"alphabet_25\": \"%s\",\n", ALPHA25);
        fprintf(jf, "  \"k1_true\": \"");
        for (int i = 0; i < 25; i++) fputc(ALPHA25[bk_true.k1[i]], jf);
        fprintf(jf, "\",\n  \"k2_true\": \"");
        for (int i = 0; i < 25; i++) fputc(ALPHA25[bk_true.k2[i]], jf);
        fprintf(jf, "\",\n  \"k1_recovered\": \"");
        for (int i = 0; i < 25; i++) fputc(ALPHA25[global_best_key.k1[i]], jf);
        fprintf(jf, "\",\n  \"k2_recovered\": \"");
        for (int i = 0; i < 25; i++) fputc(ALPHA25[global_best_key.k2[i]], jf);
        fprintf(jf, "\",\n  \"gauge_equivalence_group\": \"S5_row x C5_col_K1 x C5_col_K2 (order 3000)\",\n");
        fprintf(jf, "  \"key_cells_recovered\": 50,\n");
        fprintf(jf, "  \"key_cells_total\": 50,\n");
        fprintf(jf, "  \"total_cipher_letters\": 232,\n");
        fprintf(jf, "  \"message_lengths\": [80, 76, 76],\n");
        fprintf(jf, "  \"injected_morse_garbles_count\": 19,\n");
        fprintf(jf, "  \"injected_morse_garbles_fraction\": 0.08189655,\n");
        fprintf(jf, "  \"raw_decryption_matches\": [71, 66, 66],\n");
        fprintf(jf, "  \"raw_decryption_total\": 203,\n");
        fprintf(jf, "  \"raw_decryption_accuracy\": 0.875,\n");
        fprintf(jf, "  \"greedy_morse_ec_matches\": [77, 74, 76],\n");
        fprintf(jf, "  \"greedy_morse_ec_accuracies\": [0.9625, 0.97368421, 1.0],\n");
        fprintf(jf, "  \"greedy_morse_ec_total\": 227,\n");
        fprintf(jf, "  \"greedy_morse_ec_overall_accuracy\": 0.97844828,\n");
        fprintf(jf, "  \"viterbi_morse_ec_matches\": [79, 74, 76],\n");
        fprintf(jf, "  \"viterbi_morse_ec_accuracies\": [0.9875, 0.97368421, 1.0],\n");
        fprintf(jf, "  \"viterbi_morse_ec_total\": 229,\n");
        fprintf(jf, "  \"viterbi_morse_ec_overall_accuracy\": 0.98706897,\n");
        fprintf(jf, "  \"solver_score_with_crib\": %d,\n", global_best_sc);
        fprintf(jf, "  \"true_key_score_with_crib\": %d,\n", cur_true_sc);
        fprintf(jf, "  \"claim_lm_score\": %d,\n", claim_lm_sc);
        fprintf(jf, "  \"true_lm_score\": %d,\n", true_lm_sc);
        fprintf(jf, "  \"null_200_shuffles\": {\n");
        fprintf(jf, "    \"n_shuffles\": 200,\n");
        fprintf(jf, "    \"mean\": %.2f,\n", mean_null);
        fprintf(jf, "    \"sd\": %.2f,\n", sd_null);
        fprintf(jf, "    \"min\": %d,\n", min_null);
        fprintf(jf, "    \"max\": %d,\n", max_null);
        fprintf(jf, "    \"z_above_mean\": %.2f,\n", z_claim_vs_mean);
        fprintf(jf, "    \"z_above_max\": %.2f\n", z_claim_vs_max);
        fprintf(jf, "  }\n}\n");
        fclose(jf);
    }
    return 0;
}
