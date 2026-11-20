#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct {
    int u, v;
} Pair;

static int greedy_depth(int n, const Pair *ces, int m) {
    (void)n;
    int d[64];
    memset(d, 0, sizeof(d));
    int max_d = 0;
    for (int k = 0; k < m; k++) {
        int u = ces[k].u, v = ces[k].v;
        int nd = (d[u] > d[v] ? d[u] : d[v]) + 1;
        d[u] = d[v] = nd;
        if (nd > max_d) max_d = nd;
    }
    return max_d;
}

static int forward_wire_reduce(int N, const Pair *in_ces, int m, int w0, int val, Pair *out_ces) {
    int pi[64];
    for (int u = 0; u < N; u++) {
        if (u == w0) pi[u] = -1;
        else pi[u] = (u < w0) ? u : (u - 1);
    }
    int p = w0;
    int out_m = 0;
    for (int k = 0; k < m; k++) {
        int i = in_ces[k].u;
        int j = in_ces[k].v;
        if (i == p || j == p) {
            int other = (i == p) ? j : i;
            int real_wire = pi[other];
            pi[other] = -1;
            if (val == 0) {
                p = i;
                pi[j] = real_wire;
            } else {
                p = j;
                pi[i] = real_wire;
            }
        } else {
            int u = pi[i], v = pi[j];
            int lo = (u < v) ? u : v;
            int hi = (u < v) ? v : u;
            pi[i] = lo;
            pi[j] = hi;
            out_ces[out_m].u = lo;
            out_ces[out_m].v = hi;
            out_m++;
        }
    }
    return out_m;
}

static uint64_t rng_state = 0x123456789abcdef0ULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

#define NGROUPS 256
static uint64_t test_bpl[65][NGROUPS][64];
static int bpl_inited[65];

static void add_vec(int n, int *vec_idx, uint64_t mask) {
    if (*vec_idx >= NGROUPS * 64) return;
    int g = (*vec_idx) / 64;
    int b = (*vec_idx) % 64;
    for (int w = 0; w < n; w++) {
        if ((mask >> w) & 1ULL) {
            test_bpl[n][g][w] |= (1ULL << b);
        }
    }
    (*vec_idx)++;
}

static void ensure_test_bpl(int n) {
    if (bpl_inited[n]) return;
    rng_state = 0x9e3779b97f4a7c15ULL ^ ((uint64_t)n * 0x517cc1b727220a95ULL);
    memset(test_bpl[n], 0, sizeof(test_bpl[n]));
    uint64_t full = (n == 64) ? ~0ULL : ((1ULL << n) - 1ULL);

    int vec_idx = 0;
    /* All weight-1 and weight-(n-1) */
    for (int i = 0; i < n; i++) {
        add_vec(n, &vec_idx, 1ULL << i);
        add_vec(n, &vec_idx, full ^ (1ULL << i));
    }
    /* All weight-2 and weight-(n-2) */
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            uint64_t m2 = (1ULL << i) | (1ULL << j);
            add_vec(n, &vec_idx, m2);
            add_vec(n, &vec_idx, full ^ m2);
        }
    }
    /* Local weight-3 and weight-(n-3) */
    for (int i = 0; i < n && vec_idx < (NGROUPS - 64) * 64; i++) {
        for (int j = i + 1; j < i + 12 && j < n && vec_idx < (NGROUPS - 64) * 64; j++) {
            for (int k = j + 1; k < i + 16 && k < n && vec_idx < (NGROUPS - 64) * 64; k++) {
                uint64_t m3 = (1ULL << i) | (1ULL << j) | (1ULL << k);
                add_vec(n, &vec_idx, m3);
                add_vec(n, &vec_idx, full ^ m3);
            }
        }
    }
    int start_g = (vec_idx + 63) / 64;
    for (int g = start_g; g < NGROUPS; g++) {
        for (int w = 0; w < n; w++) {
            uint64_t word = xorshift64();
            int mode = g % 8;
            if (mode == 1) word &= xorshift64();
            else if (mode == 2) word |= xorshift64();
            else if (mode == 3) word &= xorshift64() & xorshift64();
            else if (mode == 4) word |= xorshift64() | xorshift64();
            else if (mode == 5) word &= xorshift64() & xorshift64() & xorshift64();
            else if (mode == 6) word |= xorshift64() | xorshift64() | xorshift64();
            test_bpl[n][g][w] = word;
        }
    }
    bpl_inited[n] = 1;
}

/* Step-wise no-op pruning (safe: never alters wire trajectories) + counts single-Deletion LOO candidates without compounding */
static int eval_noops_and_loo1(int n, const Pair *in_ces, int m, Pair *out_ces, int *out_loo_est) {
    ensure_test_bpl(n);
    int active[600];
    memset(active, 0, m * sizeof(int));

    for (int g = 0; g < NGROUPS; g++) {
        uint64_t data[64];
        for (int w = 0; w < n; w++) data[w] = test_bpl[n][g][w];
        for (int k = 0; k < m; k++) {
            int u = in_ces[k].u, v = in_ces[k].v;
            uint64_t a = data[u], b = data[v];
            if ((a & ~b) != 0ULL) active[k] = 1;
            data[u] = a & b;
            data[v] = a | b;
        }
    }
    int m1 = 0;
    for (int k = 0; k < m; k++) {
        if (active[k]) out_ces[m1++] = in_ces[k];
    }
    *out_loo_est = m1;
    return m1;
}

typedef struct {
    int n, m, est_m, depth;
    Pair ces[600];
    Pair p_ces[600];
} CandNet;

static void save_cand(const char *dir, const char *tag, int idx, const CandNet *c) {
    char path[512];
    snprintf(path, sizeof(path), "%s/cand_%s_n%d_s%d_d%d_i%d.txt", dir, tag, c->n, c->est_m, c->depth, idx);
    FILE *fp = fopen(path, "w");
    if (!fp) return;
    fprintf(fp, "%d %d\n", c->n, c->m);
    for (int k = 0; k < c->m; k++) {
        fprintf(fp, "%d %d\n", c->ces[k].u, c->ces[k].v);
    }
    fclose(fp);
}

/* Permute wire order so interior wires are explored first when ties occur */
static void step_beam(const CandNet *in_beam, int in_cnt, CandNet *out_beam, int *out_cnt, int max_beam) {
    *out_cnt = 0;
    Pair r[600], p[600];
    for (int b = 0; b < in_cnt; b++) {
        int N = in_beam[b].n;
        int M = in_beam[b].m;
        const Pair *orig = in_beam[b].ces;
        for (int step_w = 0; step_w < N; step_w++) {
            /* Alternate from center outward: N/2, N/2-1, N/2+1, ... */
            int w0 = (step_w % 2 == 0) ? (N / 2 + step_w / 2) : (N / 2 - (step_w + 1) / 2);
            if (w0 < 0 || w0 >= N) w0 = step_w;
            for (int val = 1; val >= 0; val--) {
                int m1 = forward_wire_reduce(N, orig, M, w0, val, r);
                int loo_est = 0;
                int mp = eval_noops_and_loo1(N - 1, r, m1, p, &loo_est);
                int dp = greedy_depth(N - 1, p, mp);

                int dup = 0;
                for (int j = 0; j < *out_cnt; j++) {
                    if (out_beam[j].est_m == mp && out_beam[j].depth == dp &&
                        memcmp(out_beam[j].p_ces, p, mp * sizeof(Pair)) == 0) {
                        dup = 1;
                        break;
                    }
                }
                if (dup) continue;

                int pos = *out_cnt;
                while (pos > 0 && (mp < out_beam[pos - 1].est_m || (mp == out_beam[pos - 1].est_m && dp < out_beam[pos - 1].depth))) {
                    pos--;
                }
                if (pos < max_beam) {
                    int move_cnt = (*out_cnt < max_beam) ? (*out_cnt - pos) : (max_beam - 1 - pos);
                    if (move_cnt > 0) {
                        memmove(&out_beam[pos + 1], &out_beam[pos], move_cnt * sizeof(CandNet));
                    }
                    out_beam[pos].n = N - 1;
                    out_beam[pos].m = m1;
                    out_beam[pos].est_m = mp;
                    out_beam[pos].depth = dp;
                    memcpy(out_beam[pos].ces, r, m1 * sizeof(Pair));
                    memcpy(out_beam[pos].p_ces, p, mp * sizeof(Pair));
                    if (*out_cnt < max_beam) (*out_cnt)++;
                }
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s <net_txt> <max_k> <out_dir> <tag>\n", argv[0]);
        return 1;
    }
    FILE *fp = fopen(argv[1], "r");
    if (!fp) return 1;
    static CandNet init_net;
    if (fscanf(fp, "%d %d", &init_net.n, &init_net.m) != 2) { fclose(fp); return 1; }
    for (int k = 0; k < init_net.m; k++) {
        fscanf(fp, "%d %d", &init_net.ces[k].u, &init_net.ces[k].v);
    }
    fclose(fp);
    init_net.est_m = init_net.m;
    init_net.depth = greedy_depth(init_net.n, init_net.ces, init_net.m);

    int max_k = atoi(argv[2]);
    const char *out_dir = argv[3];
    const char *tag = argv[4];

    #define BEAM_W 96
    static CandNet beam_a[BEAM_W], beam_b[BEAM_W];
    beam_a[0] = init_net;
    int cnt_a = 1, cnt_b = 0;

    for (int step = 1; step <= max_k && beam_a[0].n > 13; step++) {
        step_beam(beam_a, cnt_a, beam_b, &cnt_b, BEAM_W);
        if (cnt_b == 0) break;
        int best_for_d[64];
        int saved_for_d[64];
        for (int d = 0; d < 64; d++) { best_for_d[d] = 999999; saved_for_d[d] = 0; }
        for (int j = 0; j < cnt_b; j++) {
            int d = beam_b[j].depth;
            if (beam_b[j].est_m < best_for_d[d]) best_for_d[d] = beam_b[j].est_m;
        }
        for (int j = 0; j < cnt_b; j++) {
            int d = beam_b[j].depth;
            if (beam_b[j].est_m <= best_for_d[d] + 2 && saved_for_d[d] < 16) {
                saved_for_d[d]++;
                if (saved_for_d[d] == 1) {
                    printf("STEP k=%d n=%d raw=%d est=%d depth=%d\n",
                           step, beam_b[j].n, beam_b[j].m, beam_b[j].est_m, d);
                }
                save_cand(out_dir, tag, saved_for_d[d], &beam_b[j]);
            }
        }
        memcpy(beam_a, beam_b, cnt_b * sizeof(CandNet));
        cnt_a = cnt_b;
    }
    return 0;
}
