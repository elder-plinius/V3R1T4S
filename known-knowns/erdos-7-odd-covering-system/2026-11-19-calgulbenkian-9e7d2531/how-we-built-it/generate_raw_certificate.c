#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

__extension__ typedef __int128 i128;
static const int PRIMES[] = {3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59};
static const int NP = 16;
static const int DEN = 32; // C_i = m_i / 32 !

static double ipow_d(int p, int e) {
    double r = 1.0;
    for (int i = 0; i < e; i++) r *= (double)p;
    return r;
}

static i128 ipow_128(int p, int e) {
    i128 r = 1;
    for (int i = 0; i < e; i++) r *= p;
    return r;
}

static i128 gcd128(i128 a, i128 b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) { i128 t = a % b; a = b; b = t; }
    return a;
}

// Exact rational check using reduced (num, den) in i128 with overflow assert!
typedef struct { i128 n, d; } Rat;

static Rat rat_make(i128 n, i128 d) {
    if (n == 0) return (Rat){0, 1};
    i128 g = gcd128(n, d);
    return (Rat){n / g, d / g};
}

static Rat rat_add(Rat a, Rat b, int *ovf) {
    if (a.n == 0) return b;
    if (b.n == 0) return a;
    i128 g = gcd128(a.d, b.d);
    i128 bd = b.d / g;
    // Check overflow roughly via double:
    if (fabs((double)a.d * (double)bd) > 1e36 ||
        fabs((double)a.n * (double)bd) + fabs((double)b.n * (double)(a.d / g)) > 1e36) {
        *ovf = 1;
        return (Rat){2, 1};
    }
    i128 den = a.d * bd;
    i128 num = a.n * bd + b.n * (a.d / g);
    return rat_make(num, den);
}

static int bff_exact_128(const int *exps, int r) {
    int ovf = 0;
    Rat prod = {1, 1}, s = {0, 1};
    for (int i = 0; i < r; i++) {
        i128 pe = ipow_128(PRIMES[i], exps[i]);
        Rat th = rat_make(pe - 1, (PRIMES[i] - 2) * pe + 1);
        Rat one_plus = rat_make(th.d + th.n, th.d);
        // prod *= one_plus:
        i128 g1 = gcd128(prod.n, one_plus.d);
        i128 g2 = gcd128(one_plus.n, prod.d);
        prod.n = (prod.n / g1) * (one_plus.n / g2);
        prod.d = (prod.d / g2) * (one_plus.d / g1);
        s = rat_add(s, th, &ovf);
    }
    // Check prod - 1 - s < 1 <=> prod < 2 + s:
    Rat rhs = rat_add((Rat){2, 1}, s, &ovf);
    if (ovf) return 0;
    // Compare prod.n / prod.d < rhs.n / rhs.d:
    // Use i128 if < 1e37:
    if ((double)prod.n * (double)rhs.d < 1e36 && (double)rhs.n * (double)prod.d < 1e36) {
        return (prod.n * rhs.d) < (rhs.n * prod.d);
    }
    return 0;
}

#define MAX_M 16384
static double cur_p[MAX_M], nxt_p[MAX_M];
static int cur_vals[4096], nxt_vals[4096];

static double eval_float_m(const int *exps, int r, int k0, const int *ms) {
    double prod_base = 1.0, sum_base = 0.0;
    int n_cur = 1;
    cur_vals[0] = 1;
    cur_p[1] = 1.0;
    for (int m = 0; m < k0; m++) {
        int p = PRIMES[m], e = exps[m];
        double pe = ipow_d(p, e);
        double s_m = ((p - 2.0) * pe + 1.0) / (p - 1.0);
        double th = ((pe - 1.0) / (p - 1.0)) / s_m;
        prod_base *= (1.0 + th);
        sum_base += th;
        double tails[64]; tails[0] = 1.0;
        for (int t = 1; t <= e; t++) tails[t] = ipow_d(p, e - t) / s_m;
        tails[e + 1] = 0.0;
        int n_nxt = 0;
        for (int idx = 0; idx < n_cur; idx++) {
            int mv = cur_vals[idx];
            double pv = cur_p[mv]; cur_p[mv] = 0.0;
            for (int t = 0; t <= e; t++) {
                double pr = tails[t] - tails[t + 1];
                if (pr <= 0.0) continue;
                int nmv = mv * (1 + t);
                if (nxt_p[nmv] == 0.0) nxt_vals[n_nxt++] = nmv;
                nxt_p[nmv] += pv * pr;
            }
        }
        n_cur = n_nxt;
        for (int idx = 0; idx < n_nxt; idx++) {
            int nmv = nxt_vals[idx]; cur_vals[idx] = nmv; cur_p[nmv] = nxt_p[nmv]; nxt_p[nmv] = 0.0;
        }
    }
    double tot = prod_base - 1.0 - sum_base;
    if (tot >= 1.0) {
        for (int idx = 0; idx < n_cur; idx++) cur_p[cur_vals[idx]] = 0.0;
        return tot;
    }
    for (int i = k0; i < r; i++) {
        int p = PRIMES[i], e = exps[i];
        double pe = ipow_d(p, e);
        double rho = (pe - 1.0) / ((p - 1.0) * pe);
        double C_i = (double)ms[i - k0] / (double)DEN;
        double delta = 1.0 - 1.0 / C_i;
        if (delta < rho || C_i > (double)p) {
            for (int idx = 0; idx < n_cur; idx++) cur_p[cur_vals[idx]] = 0.0;
            return 2.0;
        }
        double loss_i = 0.0;
        for (int idx = 0; idx < n_cur; idx++) {
            int mv = cur_vals[idx];
            double alpha = rho * mv;
            if (alpha > delta) loss_i += cur_p[mv] * C_i * (alpha - delta);
        }
        tot += loss_i;
        if (tot >= 1.15 || i == r - 1) {
            for (int idx = 0; idx < n_cur; idx++) cur_p[cur_vals[idx]] = 0.0;
            return tot;
        }
        double tails[64]; tails[0] = 1.0;
        for (int t = 1; t <= e; t++) {
            double v = C_i / ipow_d(p, t);
            tails[t] = (v < 1.0) ? v : 1.0;
        }
        tails[e + 1] = 0.0;
        int n_nxt = 0;
        for (int idx = 0; idx < n_cur; idx++) {
            int mv = cur_vals[idx];
            double pv = cur_p[mv]; cur_p[mv] = 0.0;
            for (int t = 0; t <= e; t++) {
                double pr = tails[t] - tails[t + 1];
                if (pr <= 0.0) continue;
                int nmv = mv * (1 + t);
                if (nxt_p[nmv] == 0.0) nxt_vals[n_nxt++] = nmv;
                nxt_p[nmv] += pv * pr;
            }
        }
        n_cur = n_nxt;
        for (int idx = 0; idx < n_nxt; idx++) {
            int nmv = nxt_vals[idx]; cur_vals[idx] = nmv; cur_p[nmv] = nxt_p[nmv]; nxt_p[nmv] = 0.0;
        }
    }
    return tot;
}

static int find_cert(const int *exps, int r, int *out_k0, int *out_ms, double *out_val) {
    int k0_cands[] = {2, 3, 1, 4};
    double best_all = 2.0;
    for (int ki = 0; ki < 4; ki++) {
        int k0 = k0_cands[ki];
        if (k0 >= r) continue;
        int ms[16];
        for (int i = k0; i < r; i++) {
            int p = PRIMES[i], e = exps[i];
            double pe = ipow_d(p, e);
            double rho = (pe - 1.0) / ((p - 1.0) * pe);
            int m_min = (int)ceil((double)DEN / (1.0 - rho));
            int m_max = p * DEN;
            ms[i - k0] = m_min + (m_max - m_min) / 4;
            if (ms[i - k0] > 3 * DEN) ms[i - k0] = 2 * DEN;
            if (ms[i - k0] < m_min) ms[i - k0] = m_min;
        }
        double cur = eval_float_m(exps, r, k0, ms);
        for (int pass = 0; pass < 3; pass++) {
            for (int idx = 0; idx < r - k0; idx++) {
                int i = k0 + idx;
                int p = PRIMES[i], e = exps[i];
                double pe = ipow_d(p, e);
                double rho = (pe - 1.0) / ((p - 1.0) * pe);
                int m_min = (int)ceil((double)DEN / (1.0 - rho));
                int m_max = p * DEN;
                if (m_max > 8 * DEN) m_max = 8 * DEN;
                int best_m = ms[idx];
                for (int cand = m_min; cand <= m_max; cand++) {
                    ms[idx] = cand;
                    double v = eval_float_m(exps, r, k0, ms);
                    if (v < cur) { cur = v; best_m = cand; }
                }
                ms[idx] = best_m;
                if (cur < 0.990) break;
            }
            if (cur < 0.990) break;
        }
        if (cur < best_all) {
            best_all = cur;
            *out_k0 = k0;
            memcpy(out_ms, ms, (r - k0) * sizeof(int));
            *out_val = cur;
            if (cur < 0.995) return 1;
        }
    }
    return (best_all < 0.999999);
}

static i128 B0;
static int cur_exps[16];
static int n_band = 0, n_bff = 0, n_cert = 0, n_fail = 0;
static double max_cert_val = 0.0;
static FILE *fp_out;

static void dfs(int idx, i128 cur_L, i128 sig_n, i128 sig_d) {
    if (idx > 0 && sig_n >= 2 * sig_d && cur_L * 3 > B0) {
        n_band++;
        if (bff_exact_128(cur_exps, idx)) {
            n_bff++;
        } else {
            int k0 = 2, ms[16] = {0};
            double val = 2.0;
            if (find_cert(cur_exps, idx, &k0, ms, &val)) {
                n_cert++;
                if (val > max_cert_val) max_cert_val = val;
                // Write row to TSV: exps_csv \t k0 \t ms_csv
                for (int i = 0; i < idx; i++) fprintf(fp_out, "%s%d", i?",":"", cur_exps[i]);
                fprintf(fp_out, "\t%d\t", k0);
                for (int i = 0; i < idx - k0; i++) fprintf(fp_out, "%s%d", i?",":"", ms[i]);
                fprintf(fp_out, "\n");
            } else {
                n_fail++;
                printf("FAIL on L=%llu, r=%d, val=%.6f\n", (unsigned long long)cur_L, idx, val);
            }
        }
    }
    if (idx >= NP) return;
    int p = PRIMES[idx];
    if (cur_L > B0 / p) return;
    i128 pe = p, psum = 1 + p;
    int e = 1;
    while (cur_L <= B0 / pe) {
        cur_exps[idx] = e;
        dfs(idx + 1, cur_L * pe, sig_n * psum, sig_d * pe);
        if (pe > (B0 / cur_L) / p) break;
        pe *= p;
        psum += pe;
        e++;
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s out.tsv\n", argv[0]);
        return 1;
    }
    B0 = (i128)168131152814624ULL;
    fp_out = fopen(argv[1], "w");
    if (!fp_out) return 1;
    fprintf(fp_out, "exponents\tk0\tm_num_over_32\n");
    dfs(0, 1, 1, 1);
    fclose(fp_out);
    printf("n_band=%d, n_bff=%d, n_cert=%d, n_fail=%d, max_cert_val=%.6f\n",
           n_band, n_bff, n_cert, n_fail, max_cert_val);
    return 0;
}
