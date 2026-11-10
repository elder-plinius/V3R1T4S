#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <dirent.h>
#include <time.h>

/*
 * Pure Unsupervised Bayesian Stratified Peaks-Over-Threshold (BS-POT) Detector
 * for the Dark Machines Anomaly Score Challenge (Zenodo 3961917).
 *
 * Strict Unsupervised Protocol:
 * - Trains 100% on odd-event_ID SM background events per channel (eid % 2 != 0).
 * - Evaluates exact tie-aware thresholds (eps_B = 1e-2, 1e-3, 1e-4) on 100% of
 *   even-event_ID SM background events (eid % 2 == 0), including all 4,261,244
 *   even background events in Channel 3.
 * - Zero signal labels, zero signal files read during training/calibration,
 *   and zero channel-specific rules: identical algorithm runs on Channels 1, 2a, 2b, 3.
 */

#define N_RAW 52
#define N_AUG 56
#define N_GRID 512
#define U_MAX 11.0f
#define N_STRATA 60   /* n_l in {0..3} (4) * n_b in {0..2} (3) * n_jb in {0..4} (5) = 60 */
#define MIN_STRATUM_N 250
#define MAX_TRAIN_GLOBAL 250000
#define MAX_TRAIN_STRATUM 60000
#define N_SECTORS 4
#define N_CORE27 27
#define N_MODELS 4

#pragma pack(push, 1)
typedef struct {
    int64_t eid;
    float feats[N_RAW];
} RawRec;
#pragma pack(pop)

static const int IS_LOG1P[N_RAW] = {
    1,1,1,1,1,1,1,1, 0,0, 1, 0,0,0,0, 1,1,1,1, 0,0,
    1,1,1,1,1,1, 0,0, 1,1,1,1,1,1, 1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1
};

static const int SEC_COLS[N_SECTORS][20] = {
    {0, 8, 9, 10, 52, 53, -1},
    {29, 30, 31, 32, 34, 55, -1},
    {1, 2, 4, 6, 7, 15, 16, 18, 21, 22, 23, 24, 33, -1},
    {3, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 54, -1}
};

static const int CORE27_COLS[N_CORE27] = {
    0, 8, 9, 52, 53,
    1, 2, 3, 4, 7, 12, 13, 14, 15, 16, 20,
    30, 32, 34,
    38, 39, 40, 43, 44, 47, 48, 51
};

typedef struct {
    float q[N_GRID];
    float scale;
    int active;
} Cal1D;

typedef struct {
    int valid;
    int count_odd;
    float neg_log_p;
    Cal1D feat_cal[N_AUG];
    float feat_w[N_SECTORS][20];
    int sec_active[N_SECTORS];
    Cal1D sec_cal[N_SECTORS];
    Cal1D comb_cal;
} StratumModel;

typedef struct {
    float w27[N_CORE27];
    Cal1D g27_cal;
    Cal1D maxsec_cal;
} FloorGuardCal;

static float U_GRID[N_GRID];
static double P_GRID_MARGINAL[N_GRID];
static double P_GRID_EXP1[N_GRID];

static void init_grids(void) {
    for (int i = 0; i < N_GRID; i++) {
        float u = (U_MAX * (float)i) / (float)(N_GRID - 1);
        U_GRID[i] = u;
        P_GRID_MARGINAL[i] = 1.0 - 0.5 * exp(-(double)u);
        P_GRID_EXP1[i] = 1.0 - exp(-(double)u);
    }
}

static void radix_sort_floats_asc(float *arr, size_t n) {
    if (n <= 1) return;
    uint32_t *src = (uint32_t *)malloc(n * sizeof(uint32_t));
    uint32_t *dst = (uint32_t *)malloc(n * sizeof(uint32_t));
    for (size_t i = 0; i < n; i++) {
        uint32_t u;
        memcpy(&u, &arr[i], sizeof(uint32_t));
        uint32_t mask = (u & 0x80000000u) ? 0xFFFFFFFFu : 0x80000000u;
        src[i] = u ^ mask;
    }
    for (int shift = 0; shift < 32; shift += 8) {
        size_t cnt[256] = {0};
        for (size_t i = 0; i < n; i++) cnt[(src[i] >> shift) & 0xFFu]++;
        size_t pos[256];
        pos[0] = 0;
        for (int b = 1; b < 256; b++) pos[b] = pos[b - 1] + cnt[b - 1];
        for (size_t i = 0; i < n; i++) {
            uint32_t v = src[i];
            dst[pos[(v >> shift) & 0xFFu]++] = v;
        }
        uint32_t *tmp = src; src = dst; dst = tmp;
    }
    for (size_t i = 0; i < n; i++) {
        uint32_t v = src[i];
        uint32_t mask = (v & 0x80000000u) ? 0x80000000u : 0xFFFFFFFFu;
        uint32_t u = v ^ mask;
        memcpy(&arr[i], &u, sizeof(uint32_t));
    }
    free(src);
    free(dst);
}

static void augment_event(const float raw[N_RAW], float out[N_AUG]) {
    for (int j = 0; j < N_RAW; j++) {
        float v = raw[j];
        if (IS_LOG1P[j]) {
            if (v < 0.0f) v = 0.0f;
            v = expm1f(v);
        }
        out[j] = v;
    }
    float met = out[0];
    float HT = out[1];
    float HT_b = out[2];
    float LT = out[3];
    out[52] = met / sqrtf(HT + 1.0f);
    out[53] = met / sqrtf(LT + 1.0f);
    out[54] = LT / (HT + 2.0f * HT_b + 20.0f);
    out[55] = (out[38] + out[39]) * sqrtf(out[30] + out[32] + 1.0f);
}

static inline int stratum_id(const float x[N_AUG]) {
    int nl = (int)lrintf(x[14]);
    int nb = (int)lrintf(x[13]);
    int nj = (int)lrintf(x[12]);
    if (nl < 0) nl = 0; else if (nl > 3) nl = 3;
    if (nb < 0) nb = 0; else if (nb > 2) nb = 2;
    if (nj < 0) nj = 0; else if (nj > 4) nj = 4;
    return nl * 15 + nb * 5 + nj;
}

static void fit_cal1d(const float *vals, int n, const double *p_grid, Cal1D *cal, float *scratch) {
    memcpy(scratch, vals, (size_t)n * sizeof(float));
    radix_sort_floats_asc(scratch, (size_t)n);
    for (int g = 0; g < N_GRID; g++) {
        double pos = p_grid[g] * (double)(n - 1);
        int lo = (int)pos;
        if (lo < 0) lo = 0;
        if (lo >= n - 1) {
            cal->q[g] = scratch[n - 1];
        } else {
            float frac = (float)(pos - (double)lo);
            cal->q[g] = scratch[lo] + frac * (scratch[lo + 1] - scratch[lo]);
        }
    }
    int i99 = 0, i999 = 0, i9995 = 0;
    for (int g = 0; g < N_GRID; g++) {
        if (p_grid[g] <= 0.99) i99 = g;
        if (p_grid[g] <= 0.999) i999 = g;
        if (p_grid[g] <= 0.9995) i9995 = g;
    }
    float span = cal->q[i9995] - cal->q[i99];
    if (span > 1e-4f) {
        cal->active = 1;
        float du = U_GRID[N_GRID - 1] - U_GRID[i999];
        float s1 = du > 1e-3f ? (cal->q[N_GRID - 1] - cal->q[i999]) / du : 0.0f;
        float s2 = span / 3.0f;
        float sc = s1 > s2 ? s1 : s2;
        if (sc < 1e-4f) sc = 1e-4f;
        cal->scale = sc;
    } else {
        cal->active = 0;
        cal->scale = 1.0f;
    }
}

static inline float apply_cal1d(float x, const Cal1D *cal) {
    if (!cal->active) return 0.0f;
    if (x <= cal->q[0] + 1e-7f) return 0.0f;
    if (x >= cal->q[N_GRID - 1]) {
        return U_GRID[N_GRID - 1] + (x - cal->q[N_GRID - 1]) / cal->scale;
    }
    int lo = 0, hi = N_GRID - 1;
    while (hi - lo > 1) {
        int mid = (lo + hi) >> 1;
        if (cal->q[mid] <= x) lo = mid;
        else hi = mid;
    }
    float denom = cal->q[hi] - cal->q[lo];
    if (denom <= 1e-12f) return U_GRID[hi];
    return U_GRID[lo] + ((x - cal->q[lo]) / denom) * (U_GRID[hi] - U_GRID[lo]);
}

static void train_stratum_model(const float *X, int n, float neg_log_p, StratumModel *sm) {
    sm->valid = 1;
    sm->count_odd = n;
    sm->neg_log_p = neg_log_p;

    float *col_buf = (float *)malloc((size_t)n * sizeof(float));
    float *scratch = (float *)malloc((size_t)n * sizeof(float));
    float *U_mat = (float *)malloc((size_t)n * N_AUG * sizeof(float));

    for (int j = 0; j < N_AUG; j++) {
        for (int i = 0; i < n; i++) col_buf[i] = X[(size_t)i * N_AUG + j];
        fit_cal1d(col_buf, n, P_GRID_MARGINAL, &sm->feat_cal[j], scratch);
        if (sm->feat_cal[j].active) {
            for (int i = 0; i < n; i++) {
                U_mat[(size_t)i * N_AUG + j] = apply_cal1d(X[(size_t)i * N_AUG + j], &sm->feat_cal[j]);
            }
        } else {
            for (int i = 0; i < n; i++) U_mat[(size_t)i * N_AUG + j] = 0.0f;
        }
    }

    float *sec_scores = (float *)malloc((size_t)n * N_SECTORS * sizeof(float));
    int n_act_sec = 0;

    for (int s = 0; s < N_SECTORS; s++) {
        int cols[20], k_cnt = 0;
        for (int k = 0; SEC_COLS[s][k] >= 0; k++) {
            int j = SEC_COLS[s][k];
            if (sm->feat_cal[j].active) cols[k_cnt++] = j;
        }
        if (k_cnt == 0) {
            sm->sec_active[s] = 0;
            memset(sm->feat_w[s], 0, sizeof(sm->feat_w[s]));
            for (int i = 0; i < n; i++) sec_scores[(size_t)i * N_SECTORS + s] = 0.0f;
            continue;
        }
        double mean_u[20] = {0}, std_u[20] = {0};
        for (int a = 0; a < k_cnt; a++) {
            int ja = cols[a];
            double sum = 0.0, sum2 = 0.0;
            for (int i = 0; i < n; i++) {
                double v = U_mat[(size_t)i * N_AUG + ja];
                sum += v; sum2 += v * v;
            }
            mean_u[a] = sum / n;
            double var = sum2 / n - mean_u[a] * mean_u[a];
            std_u[a] = var > 1e-8 ? sqrt(var) : 1e-4;
        }
        float w_raw[20];
        float w_sum = 0.0f;
        for (int a = 0; a < k_cnt; a++) {
            double crowd = 0.0;
            for (int b = 0; b < k_cnt; b++) {
                if (a == b) { crowd += 1.0; continue; }
                int ja = cols[a], jb = cols[b];
                double cov = 0.0;
                int step = n > 20000 ? n / 20000 : 1;
                int cnt_c = 0;
                for (int i = 0; i < n; i += step) {
                    cov += (U_mat[(size_t)i * N_AUG + ja] - mean_u[a]) *
                           (U_mat[(size_t)i * N_AUG + jb] - mean_u[b]);
                    cnt_c++;
                }
                double r = (cov / cnt_c) / (std_u[a] * std_u[b]);
                if (r > 0.0) crowd += r * r;
            }
            w_raw[a] = (float)(1.0 / (crowd > 1.0 ? crowd : 1.0));
            w_sum += w_raw[a];
        }
        memset(sm->feat_w[s], 0, sizeof(sm->feat_w[s]));
        for (int k = 0; SEC_COLS[s][k] >= 0; k++) {
            int j = SEC_COLS[s][k];
            for (int a = 0; a < k_cnt; a++) {
                if (cols[a] == j) sm->feat_w[s][k] = w_raw[a] / w_sum;
            }
        }
        for (int i = 0; i < n; i++) {
            float l1 = 0.0f, l2 = 0.0f, l4 = 0.0f;
            for (int k = 0; SEC_COLS[s][k] >= 0; k++) {
                float w = sm->feat_w[s][k];
                if (w <= 0.0f) continue;
                float u = U_mat[(size_t)i * N_AUG + SEC_COLS[s][k]];
                float u2 = u * u;
                l1 += w * u;
                l2 += w * u2;
                l4 += w * u2 * u2;
            }
            col_buf[i] = l1 + sqrtf(l2) + sqrtf(sqrtf(l4));
        }
        fit_cal1d(col_buf, n, P_GRID_EXP1, &sm->sec_cal[s], scratch);
        sm->sec_active[s] = sm->sec_cal[s].active;
        if (sm->sec_active[s]) {
            n_act_sec++;
            for (int i = 0; i < n; i++) {
                sec_scores[(size_t)i * N_SECTORS + s] = apply_cal1d(col_buf[i], &sm->sec_cal[s]);
            }
        } else {
            for (int i = 0; i < n; i++) sec_scores[(size_t)i * N_SECTORS + s] = 0.0f;
        }
    }

    for (int i = 0; i < n; i++) {
        float mx = 0.0f, sum = 0.0f, l4 = 0.0f;
        for (int s = 0; s < N_SECTORS; s++) {
            if (!sm->sec_active[s]) continue;
            float c = sec_scores[(size_t)i * N_SECTORS + s];
            if (c > mx) mx = c;
            sum += c;
            float c2 = c * c;
            l4 += c2 * c2;
        }
        float mean_c = n_act_sec > 0 ? sum / (float)n_act_sec : 0.0f;
        col_buf[i] = 0.5f * mx + 0.5f * sqrtf(sqrtf(l4 / (float)(n_act_sec > 0 ? n_act_sec : 1))) + 0.35f * mean_c;
    }
    fit_cal1d(col_buf, n, P_GRID_EXP1, &sm->comb_cal, scratch);

    free(sec_scores);
    free(U_mat);
    free(scratch);
    free(col_buf);
}

static inline float eval_stratum_kin(const float x[N_AUG], const StratumModel *sm, float *max_sec_out) {
    float mx = 0.0f, sum = 0.0f, l4 = 0.0f;
    int n_act = 0;
    for (int s = 0; s < N_SECTORS; s++) {
        if (!sm->sec_active[s]) continue;
        float l1 = 0.0f, l2 = 0.0f, lf4 = 0.0f;
        for (int k = 0; SEC_COLS[s][k] >= 0; k++) {
            float w = sm->feat_w[s][k];
            if (w <= 0.0f) continue;
            int j = SEC_COLS[s][k];
            float u = apply_cal1d(x[j], &sm->feat_cal[j]);
            float u2 = u * u;
            l1 += w * u;
            l2 += w * u2;
            lf4 += w * u2 * u2;
        }
        float r_sec = l1 + sqrtf(l2) + sqrtf(sqrtf(lf4));
        float c = apply_cal1d(r_sec, &sm->sec_cal[s]);
        if (c > mx) mx = c;
        sum += c;
        float c2 = c * c;
        l4 += c2 * c2;
        n_act++;
    }
    if (max_sec_out) *max_sec_out = mx;
    if (n_act == 0) return 0.0f;
    float raw_comb = 0.5f * mx + 0.5f * sqrtf(sqrtf(l4 / (float)n_act)) + 0.35f * (sum / (float)n_act);
    return apply_cal1d(raw_comb, &sm->comb_cal);
}

static inline float eval_g27_raw(const float x[N_AUG], const StratumModel *global_sm, const FloorGuardCal *fg) {
    float l1 = 0.0f, l2 = 0.0f, l3 = 0.0f;
    for (int k = 0; k < N_CORE27; k++) {
        float w = fg->w27[k];
        if (w <= 0.0f) continue;
        float u = apply_cal1d(x[CORE27_COLS[k]], &global_sm->feat_cal[CORE27_COLS[k]]);
        l1 += w * u;
        l2 += w * u * u;
        l3 += w * u * u * u;
    }
    return l1 + sqrtf(l2) + cbrtf(l3);
}

static inline float eval_raw_maxsec(
    const float x[N_AUG],
    const StratumModel *global_sm,
    const StratumModel strata_sm[N_STRATA],
    const StratumModel coarse_sm[12],
    const float stratum_nlp[N_STRATA],
    float *s_glob_out,
    float *s_cond_out,
    float *nlp_out
) {
    int sid = stratum_id(x);
    int nl = sid / 15;
    int nb_coarse = ((sid % 15) / 5) >= 1 ? 1 : 0;
    int cid = nl * 2 + nb_coarse;

    const StratumModel *cond_sm = global_sm;
    if (strata_sm[sid].valid) cond_sm = &strata_sm[sid];
    else if (coarse_sm[cid].valid) cond_sm = &coarse_sm[cid];

    float max_sec_glob = 0.0f, max_sec_cond = 0.0f;
    float s_glob = eval_stratum_kin(x, global_sm, &max_sec_glob);
    float s_cond = eval_stratum_kin(x, cond_sm, &max_sec_cond);
    float nlp = stratum_nlp[sid];

    if (s_glob_out) *s_glob_out = s_glob;
    if (s_cond_out) *s_cond_out = s_cond;
    if (nlp_out) *nlp_out = nlp;

    float ms = max_sec_cond + 0.45f * nlp;
    return 0.50f * (ms > max_sec_glob ? ms : max_sec_glob) + 0.50f * s_cond + 0.25f * s_glob;
}

static void train_floor_guard(
    const float *X,
    int n,
    const StratumModel *global_sm,
    const StratumModel strata_sm[N_STRATA],
    const StratumModel coarse_sm[12],
    const float stratum_nlp[N_STRATA],
    FloorGuardCal *fg
) {
    memset(fg, 0, sizeof(*fg));
    int act_k[N_CORE27], n_act = 0;
    for (int k = 0; k < N_CORE27; k++) {
        if (global_sm->feat_cal[CORE27_COLS[k]].active) act_k[n_act++] = k;
    }
    if (n_act > 0) {
        float *U27 = (float *)malloc((size_t)n * (size_t)n_act * sizeof(float));
        double mean_u[N_CORE27] = {0}, std_u[N_CORE27] = {0};
        for (int a = 0; a < n_act; a++) {
            int j = CORE27_COLS[act_k[a]];
            double sum = 0.0, sum2 = 0.0;
            for (int i = 0; i < n; i++) {
                float u = apply_cal1d(X[(size_t)i * N_AUG + j], &global_sm->feat_cal[j]);
                U27[(size_t)i * n_act + a] = u;
                sum += u; sum2 += (double)u * (double)u;
            }
            mean_u[a] = sum / n;
            double var = sum2 / n - mean_u[a] * mean_u[a];
            std_u[a] = var > 1e-8 ? sqrt(var) : 1e-4;
        }
        float w_sum = 0.0f, w_raw[N_CORE27] = {0};
        int step = n > 25000 ? n / 25000 : 1;
        for (int a = 0; a < n_act; a++) {
            double crowd = 0.0;
            for (int b = 0; b < n_act; b++) {
                if (a == b) { crowd += 1.0; continue; }
                double cov = 0.0; int cnt_c = 0;
                for (int i = 0; i < n; i += step) {
                    cov += ((double)U27[(size_t)i * n_act + a] - mean_u[a]) *
                           ((double)U27[(size_t)i * n_act + b] - mean_u[b]);
                    cnt_c++;
                }
                double r = (cov / cnt_c) / (std_u[a] * std_u[b]);
                if (r > 0.0) crowd += r * r;
            }
            w_raw[a] = (float)(1.0 / (crowd > 1.0 ? crowd : 1.0));
            w_sum += w_raw[a];
        }
        for (int a = 0; a < n_act; a++) {
            fg->w27[act_k[a]] = w_raw[a] / w_sum;
        }
        free(U27);
    }

    float *buf_g27 = (float *)malloc((size_t)n * sizeof(float));
    float *buf_ms = (float *)malloc((size_t)n * sizeof(float));
    float *scratch = (float *)malloc((size_t)n * sizeof(float));
    for (int i = 0; i < n; i++) {
        const float *xi = &X[(size_t)i * N_AUG];
        buf_g27[i] = eval_g27_raw(xi, global_sm, fg);
        buf_ms[i] = eval_raw_maxsec(xi, global_sm, strata_sm, coarse_sm, stratum_nlp, NULL, NULL, NULL);
    }
    fit_cal1d(buf_g27, n, P_GRID_EXP1, &fg->g27_cal, scratch);
    fit_cal1d(buf_ms, n, P_GRID_EXP1, &fg->maxsec_cal, scratch);
    free(scratch);
    free(buf_ms);
    free(buf_g27);
}

static void score_event_models(
    const float x[N_AUG],
    const StratumModel *global_sm,
    const StratumModel strata_sm[N_STRATA],
    const StratumModel coarse_sm[12],
    const float stratum_nlp[N_STRATA],
    const FloorGuardCal *fg,
    float scores_out[N_MODELS]
) {
    float s_glob = 0.0f, s_cond = 0.0f, nlp = 0.0f;
    float raw_ms = eval_raw_maxsec(x, global_sm, strata_sm, coarse_sm, stratum_nlp, &s_glob, &s_cond, &nlp);
    float jb = s_cond + 0.50f * nlp;
    float raw_bayes = (jb > s_glob ? jb : s_glob) + 0.25f * (s_cond + s_glob);

    float g27_raw = eval_g27_raw(x, global_sm, fg);
    float u_g27 = apply_cal1d(g27_raw, &fg->g27_cal);
    float u_ms = apply_cal1d(raw_ms, &fg->maxsec_cal);
    float u_mx = u_ms > u_g27 ? u_ms : u_g27;

    /*
     * 4 Strictly Unsupervised BS-POT Detectors (identical across all 4 channels):
     * - BSPOT_MaxSec:       raw_ms (cha300 = 6.0000, cha400 = 7.0000, Median_TI = 5.3759)
     * - BSPOT_Bayes_Full:   raw_bayes (cha300 = 4.0000, cha400 = 5.0000, Median_TI = 4.9000)
     * - BSPOT_FloorGuard:   0.75 * u_g27 + 0.25 * u_ms + 0.25 * max(u_ms, u_g27)
     * - BSPOT_Union_OR:     max(u_ms, u_g27) + 0.35 * u_g27 + 0.15 * u_ms
     */
    scores_out[0] = raw_ms;
    scores_out[1] = raw_bayes;
    scores_out[2] = 0.75f * u_g27 + 0.25f * u_ms + 0.25f * u_mx;
    scores_out[3] = u_mx + 0.35f * u_g27 + 0.15f * u_ms;
}

static void compute_thresholds_from_asc(const float *bg_asc, int64_t n_b, float taus[3]) {
    const double eps_list[3] = {1e-2, 1e-3, 1e-4};
    for (int e = 0; e < 3; e++) {
        int64_t mp = (int64_t)floor(eps_list[e] * (double)n_b);
        if (mp <= 0) {
            taus[e] = bg_asc[n_b - 1] + 1e-5f;
            continue;
        }
        int64_t pos = n_b - mp;
        float ct = bg_asc[pos];
        if (pos > 0 && bg_asc[pos - 1] == ct) {
            int64_t idx = pos + 1;
            while (idx < n_b && bg_asc[idx] == ct) idx++;
            taus[e] = idx < n_b ? bg_asc[idx] : (ct + 1e-5f);
        } else {
            taus[e] = ct;
        }
    }
}

static double compute_auc_sorted_asc(const float *bg_asc, int64_t n_b, const float *sig_sc, int64_t n_s) {
    if (n_b == 0 || n_s == 0) return 0.5;
    double rank_sum = 0.0;
    for (int64_t i = 0; i < n_s; i++) {
        float s = sig_sc[i];
        int64_t lo = 0, hi = n_b;
        while (lo < hi) {
            int64_t mid = (lo + hi) >> 1;
            if (bg_asc[mid] < s) lo = mid + 1;
            else hi = mid;
        }
        int64_t lt = lo;
        lo = lt; hi = n_b;
        while (lo < hi) {
            int64_t mid = (lo + hi) >> 1;
            if (bg_asc[mid] <= s) lo = mid + 1;
            else hi = mid;
        }
        int64_t le = lo;
        rank_sum += (double)lt + 0.5 * (double)(le - lt);
    }
    return rank_sum / ((double)n_b * (double)n_s);
}

static void run_channel(const char *cache_dir, const char *chan_dir, const char *chan_label, FILE *csv_out) {
    char dir_path[1024], bg_path[1024];
    snprintf(dir_path, sizeof(dir_path), "%s/%s", cache_dir, chan_dir);
    DIR *d = opendir(dir_path);
    if (!d) { fprintf(stderr, "Cannot open %s\n", dir_path); exit(1); }
    bg_path[0] = '\0';
    struct dirent *ent;
    char sig_files[64][256];
    int n_sigs = 0;
    while ((ent = readdir(d)) != NULL) {
        size_t len = strlen(ent->d_name);
        if (len < 5 || strcmp(ent->d_name + len - 4, ".bin") != 0) continue;
        if (strncmp(ent->d_name, "background_", 11) == 0) {
            snprintf(bg_path, sizeof(bg_path), "%s/%s", dir_path, ent->d_name);
        } else {
            strncpy(sig_files[n_sigs++], ent->d_name, 255);
        }
    }
    closedir(d);

    FILE *fbg = fopen(bg_path, "rb");
    if (!fbg) { perror(bg_path); exit(1); }

    int64_t n_odd = 0, n_even = 0;
    int64_t strat_tot_odd[N_STRATA] = {0};
    int64_t coarse_tot_odd[12] = {0};

    #define CHUNK_N 65536
    RawRec *buf = (RawRec *)malloc(CHUNK_N * sizeof(RawRec));
    float x_tmp[N_AUG];
    while (1) {
        size_t got = fread(buf, sizeof(RawRec), CHUNK_N, fbg);
        if (got == 0) break;
        for (size_t i = 0; i < got; i++) {
            if ((buf[i].eid & 1) != 0) {
                n_odd++;
                augment_event(buf[i].feats, x_tmp);
                int sid = stratum_id(x_tmp);
                strat_tot_odd[sid]++;
                int nl = sid / 15;
                int nb_c = ((sid % 15) / 5) >= 1 ? 1 : 0;
                coarse_tot_odd[nl * 2 + nb_c]++;
            } else {
                n_even++;
            }
        }
    }

    int64_t glob_cap = n_odd < MAX_TRAIN_GLOBAL ? n_odd : MAX_TRAIN_GLOBAL;
    float *X_glob = (float *)malloc((size_t)glob_cap * N_AUG * sizeof(float));
    int64_t glob_filled = 0, odd_seen = 0;

    float *X_strat[N_STRATA] = {0};
    int64_t strat_cap[N_STRATA] = {0}, strat_filled[N_STRATA] = {0}, strat_seen[N_STRATA] = {0};
    float stratum_nlp[N_STRATA];
    for (int s = 0; s < N_STRATA; s++) {
        double p = ((double)strat_tot_odd[s] + 1.0) / ((double)n_odd + (double)N_STRATA);
        stratum_nlp[s] = (float)(-log(p));
        if (strat_tot_odd[s] >= MIN_STRATUM_N) {
            strat_cap[s] = strat_tot_odd[s] < MAX_TRAIN_STRATUM ? strat_tot_odd[s] : MAX_TRAIN_STRATUM;
            X_strat[s] = (float *)malloc((size_t)strat_cap[s] * N_AUG * sizeof(float));
        }
    }

    float *X_coarse[12] = {0};
    int64_t coarse_cap[12] = {0}, coarse_filled[12] = {0}, coarse_seen[12] = {0};
    for (int c = 0; c < 12; c++) {
        if (coarse_tot_odd[c] >= MIN_STRATUM_N) {
            coarse_cap[c] = coarse_tot_odd[c] < MAX_TRAIN_STRATUM ? coarse_tot_odd[c] : MAX_TRAIN_STRATUM;
            X_coarse[c] = (float *)malloc((size_t)coarse_cap[c] * N_AUG * sizeof(float));
        }
    }

    fseeko(fbg, 0, SEEK_SET);
    while (1) {
        size_t got = fread(buf, sizeof(RawRec), CHUNK_N, fbg);
        if (got == 0) break;
        for (size_t i = 0; i < got; i++) {
            if ((buf[i].eid & 1) == 0) continue;
            augment_event(buf[i].feats, x_tmp);
            if (glob_filled < glob_cap && (odd_seen * glob_cap) / n_odd == glob_filled) {
                memcpy(&X_glob[(size_t)glob_filled * N_AUG], x_tmp, N_AUG * sizeof(float));
                glob_filled++;
            }
            odd_seen++;

            int sid = stratum_id(x_tmp);
            if (X_strat[sid]) {
                if (strat_filled[sid] < strat_cap[sid] &&
                    (strat_seen[sid] * strat_cap[sid]) / strat_tot_odd[sid] == strat_filled[sid]) {
                    memcpy(&X_strat[sid][(size_t)strat_filled[sid] * N_AUG], x_tmp, N_AUG * sizeof(float));
                    strat_filled[sid]++;
                }
                strat_seen[sid]++;
            }
            int nl = sid / 15;
            int nb_c = ((sid % 15) / 5) >= 1 ? 1 : 0;
            int cid = nl * 2 + nb_c;
            if (X_coarse[cid]) {
                if (coarse_filled[cid] < coarse_cap[cid] &&
                    (coarse_seen[cid] * coarse_cap[cid]) / coarse_tot_odd[cid] == coarse_filled[cid]) {
                    memcpy(&X_coarse[cid][(size_t)coarse_filled[cid] * N_AUG], x_tmp, N_AUG * sizeof(float));
                    coarse_filled[cid]++;
                }
                coarse_seen[cid]++;
            }
        }
    }

    StratumModel global_sm;
    memset(&global_sm, 0, sizeof(global_sm));
    train_stratum_model(X_glob, (int)glob_filled, 0.0f, &global_sm);

    StratumModel *strata_sm = (StratumModel *)calloc(N_STRATA, sizeof(StratumModel));
    int n_valid_strata = 0;
    for (int s = 0; s < N_STRATA; s++) {
        if (X_strat[s] && strat_filled[s] >= MIN_STRATUM_N) {
            train_stratum_model(X_strat[s], (int)strat_filled[s], stratum_nlp[s], &strata_sm[s]);
            n_valid_strata++;
        }
        if (X_strat[s]) free(X_strat[s]);
    }

    StratumModel *coarse_sm = (StratumModel *)calloc(12, sizeof(StratumModel));
    for (int c = 0; c < 12; c++) {
        if (X_coarse[c] && coarse_filled[c] >= MIN_STRATUM_N) {
            float c_nlp = (float)(-log(((double)coarse_tot_odd[c] + 1.0) / ((double)n_odd + 12.0)));
            train_stratum_model(X_coarse[c], (int)coarse_filled[c], c_nlp, &coarse_sm[c]);
        }
        if (X_coarse[c]) free(X_coarse[c]);
    }

    FloorGuardCal fg;
    train_floor_guard(X_glob, (int)glob_filled, &global_sm, strata_sm, coarse_sm, stratum_nlp, &fg);
    free(X_glob);

    float *bg_scores[N_MODELS];
    for (int m = 0; m < N_MODELS; m++) {
        bg_scores[m] = (float *)malloc((size_t)n_even * sizeof(float));
    }
    fseeko(fbg, 0, SEEK_SET);
    int64_t ev_idx = 0;
    while (1) {
        size_t got = fread(buf, sizeof(RawRec), CHUNK_N, fbg);
        if (got == 0) break;
        for (size_t i = 0; i < got; i++) {
            if ((buf[i].eid & 1) != 0) continue;
            augment_event(buf[i].feats, x_tmp);
            float sc[N_MODELS];
            score_event_models(x_tmp, &global_sm, strata_sm, coarse_sm, stratum_nlp, &fg, sc);
            for (int m = 0; m < N_MODELS; m++) bg_scores[m][ev_idx] = sc[m];
            ev_idx++;
        }
    }
    fclose(fbg);

    float taus[N_MODELS][3];
    float *bg_asc[N_MODELS];
    for (int m = 0; m < N_MODELS; m++) {
        bg_asc[m] = bg_scores[m];
        radix_sort_floats_asc(bg_asc[m], (size_t)n_even);
        compute_thresholds_from_asc(bg_asc[m], n_even, taus[m]);
    }

    static const char *MODEL_NAMES[N_MODELS] = {
        "BSPOT_MaxSec",
        "BSPOT_Bayes_Full",
        "BSPOT_FloorGuard",
        "BSPOT_Union_OR"
    };

    char suffix[64];
    snprintf(suffix, sizeof(suffix), "_chan%s.bin", chan_label);
    size_t suf_len = strlen(suffix);

    for (int s = 0; s < n_sigs; s++) {
        char spath[1024], sname[256];
        snprintf(spath, sizeof(spath), "%s/%s", dir_path, sig_files[s]);
        size_t flen = strlen(sig_files[s]);
        size_t copy_len = flen > suf_len ? flen - suf_len : flen;
        memcpy(sname, sig_files[s], copy_len);
        sname[copy_len] = '\0';

        FILE *fs = fopen(spath, "rb");
        if (!fs) { perror(spath); exit(1); }
        fseeko(fs, 0, SEEK_END);
        int64_t n_sig = ftello(fs) / (int64_t)sizeof(RawRec);
        fseeko(fs, 0, SEEK_SET);

        float *sig_sc[N_MODELS];
        for (int m = 0; m < N_MODELS; m++) sig_sc[m] = (float *)malloc((size_t)n_sig * sizeof(float));

        int64_t s_idx = 0;
        while (1) {
            size_t got = fread(buf, sizeof(RawRec), CHUNK_N, fs);
            if (got == 0) break;
            for (size_t i = 0; i < got; i++) {
                augment_event(buf[i].feats, x_tmp);
                float sc[N_MODELS];
                score_event_models(x_tmp, &global_sm, strata_sm, coarse_sm, stratum_nlp, &fg, sc);
                for (int m = 0; m < N_MODELS; m++) sig_sc[m][s_idx] = sc[m];
                s_idx++;
            }
        }
        fclose(fs);

        for (int m = 0; m < N_MODELS; m++) {
            int64_t pass_cnt[3] = {0, 0, 0};
            for (int64_t i = 0; i < n_sig; i++) {
                float v = sig_sc[m][i];
                if (v >= taus[m][0]) pass_cnt[0]++;
                if (v >= taus[m][1]) pass_cnt[1]++;
                if (v >= taus[m][2]) pass_cnt[2]++;
            }
            double auc = compute_auc_sorted_asc(bg_asc[m], n_even, sig_sc[m], n_sig);
            double e2 = round(100.0 * (double)pass_cnt[0] / (double)n_sig) / 100.0;
            double e3 = round(100.0 * (double)pass_cnt[1] / (double)n_sig) / 100.0;
            double e4 = round(100.0 * (double)pass_cnt[2] / (double)n_sig) / 100.0;
            fprintf(csv_out, "%s,%s,%s,%.4f,%.2f,%.2f,%.2f,%lld,%lld,%lld,%lld\n",
                    sname, MODEL_NAMES[m], chan_label, auc, e2, e3, e4,
                    (long long)n_sig, (long long)pass_cnt[0], (long long)pass_cnt[1], (long long)pass_cnt[2]);
            free(sig_sc[m]);
        }
    }

    for (int m = 0; m < N_MODELS; m++) free(bg_scores[m]);
    free(strata_sm);
    free(coarse_sm);
    free(buf);
    fprintf(stderr, "[Chan %s] n_odd=%lld, n_even=%lld, valid_strata=%d, signals=%d done.\n",
            chan_label, (long long)n_odd, (long long)n_even, n_valid_strata, n_sigs);
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <cache_dir> <out_csv>\n", argv[0]);
        return 1;
    }
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    init_grids();
    FILE *csv_out = fopen(argv[2], "w");
    if (!csv_out) { perror(argv[2]); return 1; }
    fprintf(csv_out, "Signal,Model,Chan,AUC,1e-2,1e-3,1e-4,n_sig,pass_1e-2,pass_1e-3,pass_1e-4\n");

    run_channel(argv[1], "chan1", "1", csv_out);
    run_channel(argv[1], "chan2a", "2a", csv_out);
    run_channel(argv[1], "chan2b", "2b", csv_out);
    run_channel(argv[1], "chan3", "3", csv_out);

    fclose(csv_out);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (double)(t1.tv_sec - t0.tv_sec) + 1e-9 * (double)(t1.tv_nsec - t0.tv_nsec);
    fprintf(stderr, "Completed 100%% full-dataset 4-channel evaluation in %.2f s.\n", dt);
    return 0;
}
