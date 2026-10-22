#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAX_R 2500
#define MAX_D 256

static int n_dim[3];
static int d_dim[3];
static int R;
static int max_coeff = 2;
static int16_t mat[3][MAX_R][MAX_D];
static uint64_t hval[3][MAX_R];
static int bad_vec[3][MAX_R];
static int l1_vec[3][MAX_R];
static uint64_t zobrist[3][MAX_D];

static int best_R;
static int best_bad_triads;
static int best_bad_entries;
static int16_t best_mat[3][MAX_R][MAX_D];

static uint64_t rng_state = 0x853c49e6748fea9bULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static void init_zobrist(uint64_t seed) {
    rng_state = seed ? seed : 0x853c49e6748fea9bULL;
    for (int f = 0; f < 3; f++) {
        for (int c = 0; c < MAX_D; c++) {
            zobrist[f][c] = xorshift64() | 1ULL;
        }
    }
}

static void recompute_vec_stats(int f, int r) {
    uint64_t h = 0;
    int bad = 0;
    int l1 = 0;
    int D = d_dim[f];
    const int16_t *v = mat[f][r];
    const uint64_t *z = zobrist[f];
    for (int c = 0; c < D; c++) {
        int val = v[c];
        if (val != 0) {
            h += (uint64_t)(int64_t)val * z[c];
            int av = val < 0 ? -val : val;
            l1 += av;
            if (av > 1) bad += (av - 1);
        }
    }
    hval[f][r] = h;
    bad_vec[f][r] = bad;
    l1_vec[f][r] = l1;
}

static inline int vec_equal_sign(int f, int r1, int r2) {
    uint64_t h1 = hval[f][r1];
    uint64_t h2 = hval[f][r2];
    if (h1 == 0 || h2 == 0) return 0;
    int D = d_dim[f];
    if (h1 == h2) {
        if (memcmp(mat[f][r1], mat[f][r2], D * sizeof(int16_t)) == 0) return 1;
    }
    if (h1 == (uint64_t)(-(int64_t)h2)) {
        const int16_t *v1 = mat[f][r1];
        const int16_t *v2 = mat[f][r2];
        for (int c = 0; c < D; c++) {
            if (v1[c] != -v2[c]) return 0;
        }
        return -1;
    }
    return 0;
}

static void delete_triad(int r) {
    if (r < R - 1) {
        for (int f = 0; f < 3; f++) {
            memcpy(mat[f][r], mat[f][R - 1], d_dim[f] * sizeof(int16_t));
            hval[f][r] = hval[f][R - 1];
            bad_vec[f][r] = bad_vec[f][R - 1];
            l1_vec[f][r] = l1_vec[f][R - 1];
        }
    }
    R--;
}

static int try_reduce_triad(int r1) {
    if (r1 >= R) return 0;
    if (l1_vec[0][r1] == 0 || l1_vec[1][r1] == 0 || l1_vec[2][r1] == 0) {
        delete_triad(r1);
        return 1;
    }
    for (int r2 = 0; r2 < R; r2++) {
        if (r1 == r2) continue;
        int s0 = vec_equal_sign(0, r1, r2);
        int s1 = vec_equal_sign(1, r1, r2);
        int s2 = vec_equal_sign(2, r1, r2);
        int f_diff = -1, sign_prod = 0;
        if (s0 != 0 && s1 != 0) { f_diff = 2; sign_prod = s0 * s1; }
        else if (s0 != 0 && s2 != 0) { f_diff = 1; sign_prod = s0 * s2; }
        else if (s1 != 0 && s2 != 0) { f_diff = 0; sign_prod = s1 * s2; }
        if (f_diff >= 0) {
            int D = d_dim[f_diff];
            int ok = 1;
            for (int c = 0; c < D; c++) {
                int v = mat[f_diff][r1][c] + sign_prod * mat[f_diff][r2][c];
                int av = v < 0 ? -v : v;
                if (av > 1) { ok = 0; break; }
            }
            if (!ok) continue;
            for (int c = 0; c < D; c++) {
                mat[f_diff][r1][c] += sign_prod * mat[f_diff][r2][c];
            }
            recompute_vec_stats(f_diff, r1);
            int low = r1 < r2 ? r1 : r2;
            delete_triad(r2);
            if (l1_vec[f_diff][low] == 0) delete_triad(low);
            return 1;
        }
    }
    return 0;
}

static void reduce_scheme_full(void) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int r = 0; r < R; r++) {
            if (try_reduce_triad(r)) {
                changed = 1;
                break;
            }
        }
    }
}

static void compute_global_totals(int *out_bad_triads, int *out_bad_entries) {
    int bt = 0, be = 0;
    for (int r = 0; r < R; r++) {
        int b = bad_vec[0][r] + bad_vec[1][r] + bad_vec[2][r];
        if (b > 0) {
            bt++;
            be += b;
        }
    }
    *out_bad_triads = bt;
    *out_bad_entries = be;
}

static void save_best(void) {
    int bt, be;
    compute_global_totals(&bt, &be);
    if (R < best_R || (R == best_R && bt < best_bad_triads) ||
        (R == best_R && bt == best_bad_triads && be < best_bad_entries)) {
        best_R = R;
        best_bad_triads = bt;
        best_bad_entries = be;
        for (int f = 0; f < 3; f++) {
            for (int r = 0; r < R; r++) {
                memcpy(best_mat[f][r], mat[f][r], d_dim[f] * sizeof(int16_t));
            }
        }
    }
}

static int attempt_pair_flip(int r1, int r2, int require_strict) {
    int s0 = vec_equal_sign(0, r1, r2);
    int s1 = vec_equal_sign(1, r1, r2);
    int s2 = vec_equal_sign(2, r1, r2);
    int n_shared = (s0 != 0) + (s1 != 0) + (s2 != 0);
    if (n_shared != 1) return 0;

    int f_same = (s0 != 0) ? 0 : ((s1 != 0) ? 1 : 2);
    int s = (s0 != 0) ? s0 : ((s1 != 0) ? s1 : s2);
    int f1 = (f_same + 1) % 3;
    int f2 = (f_same + 2) % 3;
    int pairs[2][2] = {{f1, f2}, {f2, f1}};

    int old_b1 = bad_vec[0][r1] + bad_vec[1][r1] + bad_vec[2][r1];
    int old_b2 = bad_vec[0][r2] + bad_vec[1][r2] + bad_vec[2][r2];
    int old_bt = (old_b1 > 0) + (old_b2 > 0);

    int p_start = (int)(xorshift64() & 1ULL);
    for (int pi = 0; pi < 2; pi++) {
        int p = (p_start + pi) & 1;
        int fb = pairs[p][0];
        int fc = pairs[p][1];
        int Db = d_dim[fb];
        int Dc = d_dim[fc];
        int old_be = bad_vec[fb][r1] + bad_vec[fc][r2];

        int a_start = (xorshift64() & 1ULL) ? 1 : -1;
        for (int ai = 0; ai < 2; ai++) {
            int alpha = (ai == 0) ? a_start : -a_start;
            int new_bad_b = 0, max_b = 0, nz_b = 0;
            const int16_t *vb1 = mat[fb][r1];
            const int16_t *vb2 = mat[fb][r2];
            for (int c = 0; c < Db; c++) {
                int v = vb1[c] + alpha * vb2[c];
                int av = v < 0 ? -v : v;
                if (av > 0) nz_b = 1;
                if (av > max_b) max_b = av;
                if (av > 1) new_bad_b += (av - 1);
            }
            if (max_b > max_coeff) continue;

            int as = alpha * s;
            int new_bad_c = 0, max_c = 0, nz_c = 0;
            const int16_t *vc2 = mat[fc][r2];
            const int16_t *vc1 = mat[fc][r1];
            for (int c = 0; c < Dc; c++) {
                int v = vc2[c] - as * vc1[c];
                int av = v < 0 ? -v : v;
                if (av > 0) nz_c = 1;
                if (av > max_c) max_c = av;
                if (av > 1) new_bad_c += (av - 1);
            }
            if (max_c > max_coeff) continue;

            int new_b1 = old_b1 - bad_vec[fb][r1] + new_bad_b;
            int new_b2 = old_b2 - bad_vec[fc][r2] + new_bad_c;
            int new_bt = (new_b1 > 0) + (old_b2 > 0 ? (new_b2 > 0) : (new_b2 > 0));
            int new_be = new_bad_b + new_bad_c;
            int dbt = new_bt - old_bt;
            int dbe = new_be - old_be;

            int is_strict = (!nz_b || !nz_c || dbt < 0 || (dbt == 0 && dbe < 0));
            int is_neutral = (dbt <= 0 && dbe <= 0);

            if (is_strict || (!require_strict && is_neutral)) {
                for (int c = 0; c < Db; c++) mat[fb][r1][c] += alpha * mat[fb][r2][c];
                for (int c = 0; c < Dc; c++) mat[fc][r2][c] -= as * mat[fc][r1][c];
                recompute_vec_stats(fb, r1);
                recompute_vec_stats(fc, r2);
                int red = 0;
                if (try_reduce_triad(r1)) red = 1;
                if (r2 < R && try_reduce_triad(r2)) red = 1;
                if (is_strict || red) save_best();
                return 1;
            }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    int max_steps = 50000;
    uint64_t seed = 1337ULL;
    if (argc > 1) max_steps = atoi(argv[1]);
    if (argc > 2) seed = strtoull(argv[2], NULL, 10);
    if (argc > 3) max_coeff = atoi(argv[3]);

    if (scanf("%d %d %d %d", &n_dim[0], &n_dim[1], &n_dim[2], &R) != 4) {
        return 1;
    }
    d_dim[0] = n_dim[0] * n_dim[1];
    d_dim[1] = n_dim[1] * n_dim[2];
    d_dim[2] = n_dim[2] * n_dim[0];

    init_zobrist(seed);

    for (int f = 0; f < 3; f++) {
        int D = d_dim[f];
        for (int r = 0; r < R; r++) {
            for (int c = 0; c < D; c++) {
                int v;
                if (scanf("%d", &v) != 1) return 1;
                mat[f][r][c] = (int16_t)v;
            }
            recompute_vec_stats(f, r);
        }
    }

    reduce_scheme_full();
    best_R = 999999;
    best_bad_triads = 999999;
    best_bad_entries = 999999;
    save_best();

    int init_R = best_R, init_bt = best_bad_triads, init_be = best_bad_entries;

    // Initial full strict sweep on bad triads
    int improved = 1;
    while (improved) {
        improved = 0;
        for (int r1 = 0; r1 < R; r1++) {
            if (bad_vec[0][r1] + bad_vec[1][r1] + bad_vec[2][r1] == 0) continue;
            for (int r2 = 0; r2 < R; r2++) {
                if (r1 == r2) continue;
                if (attempt_pair_flip(r1, r2, 1) || attempt_pair_flip(r2, r1, 1)) {
                    improved = 1;
                    break;
                }
            }
            if (improved) break;
        }
    }

    for (int step = 0; step < max_steps; step++) {
        if (R <= 1) break;
        int r1 = (int)(xorshift64() % (uint64_t)R);
        int r2_start = (int)(xorshift64() % (uint64_t)R);
        int flipped = 0;
        for (int i = 0; i < R; i++) {
            int r2 = (r2_start + i) % R;
            if (r1 == r2) continue;
            if (attempt_pair_flip(r1, r2, 0)) {
                flipped = 1;
                break;
            }
        }
        // Periodically check if any bad triad can now be strictly absorbed
        if (flipped && (step & 15) == 0 && best_bad_triads > 0) {
            for (int b1 = 0; b1 < R; b1++) {
                if (bad_vec[0][b1] + bad_vec[1][b1] + bad_vec[2][b1] == 0) continue;
                for (int b2 = 0; b2 < R; b2++) {
                    if (b1 == b2) continue;
                    if (attempt_pair_flip(b1, b2, 1) || attempt_pair_flip(b2, b1, 1)) break;
                }
            }
        }
    }

    fprintf(stderr, "C_OPT(max=%d): R %d -> %d | bad_triads %d -> %d | bad_entries %d -> %d\n",
            max_coeff, init_R, best_R, init_bt, best_bad_triads, init_be, best_bad_entries);

    printf("%d %d %d %d\n", n_dim[0], n_dim[1], n_dim[2], best_R);
    for (int f = 0; f < 3; f++) {
        int D = d_dim[f];
        for (int r = 0; r < best_R; r++) {
            for (int c = 0; c < D; c++) {
                printf("%d%c", (int)best_mat[f][r][c], (c == D - 1) ? '\n' : ' ');
            }
        }
    }
    return 0;
}
