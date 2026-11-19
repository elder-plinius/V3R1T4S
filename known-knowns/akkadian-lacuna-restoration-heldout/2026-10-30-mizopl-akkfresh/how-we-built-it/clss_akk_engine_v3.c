#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <pthread.h>

#define MAX_V 2048
#define NUM_TEMPLATES 83
#define NUM_THREADS 8
#define TOP_K_PER_CTX 25

typedef struct {
    int len;
    int is_unique;
    uint16_t *toks;
} TrainSeq;

typedef struct {
    int len;
    uint16_t *in_toks;
    int16_t *lbl_toks;
    uint16_t *raw_pos;
} TestSeq;

typedef struct {
    char name[32];
    int n_off;
    int offsets[10];
    double weight;
    uint32_t sub_mask;   // bitmask in {-3,-2,-1,+1,+2,+3} (0 for long-range templates)
    uint32_t gap_mask;   // interior gap bitmask in {-3,-2,-1,+1,+2,+3}
    int in_v2;           // whether this template was one of the 32 in CLSS-C-v2
} TemplateSpec;

static TemplateSpec TEMPLATES[NUM_TEMPLATES];

static void init_templates(void) {
    static const int OFF6[6] = {-3, -2, -1, 1, 2, 3};
    int idx = 0;
    for (uint32_t m = 1; m < 64; m++) {
        TemplateSpec *sp = &TEMPLATES[idx++];
        sp->sub_mask = m;
        int n_off = 0;
        int l_span = 0, r_span = 0;
        int l_cnt = 0, r_cnt = 0;
        for (int b = 0; b < 6; b++) {
            if ((m >> b) & 1) {
                sp->offsets[n_off++] = OFF6[b];
                if (b < 3) {
                    l_cnt++;
                    int dist = 3 - b;
                    if (dist > l_span) l_span = dist;
                } else {
                    r_cnt++;
                    int dist = b - 2;
                    if (dist > r_span) r_span = dist;
                }
            }
        }
        sp->n_off = n_off;
        uint32_t gmask = 0;
        if (l_span >= 2 && !((m >> 2) & 1)) gmask |= (1u << 2);
        if (l_span >= 3 && !((m >> 1) & 1)) gmask |= (1u << 1);
        if (r_span >= 2 && !((m >> 3) & 1)) gmask |= (1u << 3);
        if (r_span >= 3 && !((m >> 4) & 1)) gmask |= (1u << 4);
        sp->gap_mask = gmask;

        snprintf(sp->name, sizeof(sp->name), "S_%02x", m);
        sp->in_v2 = 0;

        double w = 0.0;
        if (gmask == 0) {
            sp->in_v2 = 1;
            if (l_cnt == 3 && r_cnt == 3) w = 26.0;
            else if ((l_cnt == 3 && r_cnt == 2) || (l_cnt == 2 && r_cnt == 3)) w = 20.0;
            else if (l_cnt == 2 && r_cnt == 2) w = 15.0;
            else if ((l_cnt == 3 && r_cnt == 1) || (l_cnt == 1 && r_cnt == 3)) w = 13.0;
            else if ((l_cnt == 2 && r_cnt == 1) || (l_cnt == 1 && r_cnt == 2)) w = 10.0;
            else if (l_cnt == 1 && r_cnt == 1) w = 6.5;
            else if (l_cnt == 3 || r_cnt == 3) w = 7.5;
            else if (l_cnt == 2 || r_cnt == 2) w = 4.2;
            else if (l_cnt == 1 || r_cnt == 1) w = 1.6;
        } else {
            if (m == ((1<<0)|(1<<1)|(1<<3)|(1<<4))) { w = 11.0; sp->in_v2 = 1; }
            else if (m == ((1<<1)|(1<<3)|(1<<4)))   { w = 7.5;  sp->in_v2 = 1; }
            else if (m == ((1<<0)|(1<<1)|(1<<3)))   { w = 7.5;  sp->in_v2 = 1; }
            else if (m == ((1<<1)|(1<<3)))          { w = 4.0;  sp->in_v2 = 1; }
            else if (m == ((1<<0)|(1<<1)))          { w = 2.5;  sp->in_v2 = 1; }
            else if (m == (1<<1))                   { w = 0.8;  sp->in_v2 = 1; }
            else if (m == ((1<<1)|(1<<2)|(1<<4)|(1<<5))) { w = 11.0; sp->in_v2 = 1; }
            else if (m == ((1<<1)|(1<<2)|(1<<4)))   { w = 7.5;  sp->in_v2 = 1; }
            else if (m == ((1<<2)|(1<<4)|(1<<5)))   { w = 7.5;  sp->in_v2 = 1; }
            else if (m == ((1<<2)|(1<<4)))          { w = 4.0;  sp->in_v2 = 1; }
            else if (m == ((1<<4)|(1<<5)))          { w = 2.5;  sp->in_v2 = 1; }
            else if (m == (1<<4))                   { w = 0.8;  sp->in_v2 = 1; }
            else if (m == ((1<<1)|(1<<4)))          { w = 2.0;  sp->in_v2 = 1; }
            else {
                double base = 1.8 * n_off * (l_cnt > 0 && r_cnt > 0 ? 1.45 : 1.0);
                sp->weight = base;
                continue;
            }
        }
        sp->weight = w;
    }
    // Add 20 long-range contiguous templates inside [-5, +5]
    TemplateSpec extra[20] = {
        {"L5",  5,  {-5, -4, -3, -2, -1},                 14.0, 0, 0, 1},
        {"R5",  5,  {1, 2, 3, 4, 5},                      14.0, 0, 0, 1},
        {"L4",  4,  {-4, -3, -2, -1},                     11.0, 0, 0, 1},
        {"R4",  4,  {1, 2, 3, 4},                         11.0, 0, 0, 1},
        {"B44", 8,  {-4, -3, -2, -1, 1, 2, 3, 4},         28.0, 0, 0, 0},
        {"B43", 7,  {-4, -3, -2, -1, 1, 2, 3},            24.0, 0, 0, 0},
        {"B34", 7,  {-3, -2, -1, 1, 2, 3, 4},             24.0, 0, 0, 0},
        {"B42", 6,  {-4, -3, -2, -1, 1, 2},               18.0, 0, 0, 0},
        {"B24", 6,  {-2, -1, 1, 2, 3, 4},                 18.0, 0, 0, 0},
        {"B41", 5,  {-4, -3, -2, -1, 1},                  15.0, 0, 0, 0},
        {"B14", 5,  {-1, 1, 2, 3, 4},                     15.0, 0, 0, 0},
        {"B55", 10, {-5, -4, -3, -2, -1, 1, 2, 3, 4, 5},  30.0, 0, 0, 0},
        {"B54", 9,  {-5, -4, -3, -2, -1, 1, 2, 3, 4},     26.0, 0, 0, 0},
        {"B45", 9,  {-4, -3, -2, -1, 1, 2, 3, 4, 5},     26.0, 0, 0, 0},
        {"B53", 8,  {-5, -4, -3, -2, -1, 1, 2, 3},        22.0, 0, 0, 0},
        {"B35", 8,  {-3, -2, -1, 1, 2, 3, 4, 5},          22.0, 0, 0, 0},
        {"B52", 7,  {-5, -4, -3, -2, -1, 1, 2},           19.0, 0, 0, 0},
        {"B25", 7,  {-2, -1, 1, 2, 3, 4, 5},              19.0, 0, 0, 0},
        {"B51", 6,  {-5, -4, -3, -2, -1, 1},              16.0, 0, 0, 0},
        {"B15", 6,  {-1, 1, 2, 3, 4, 5},                  16.0, 0, 0, 0}
    };
    for (int k = 0; k < 20; k++) {
        TEMPLATES[idx++] = extra[k];
    }
}

static inline uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static inline uint64_t hash_ctx(const uint16_t *padded, int pi, int n_off, const int *offsets) {
    uint64_t h = 0x123456789abcdef0ULL ^ (uint64_t)n_off;
    for (int k = 0; k < n_off; k++) {
        uint64_t v = padded[pi + offsets[k]];
        h = splitmix64(h ^ (v + ((uint64_t)k << 16)));
    }
    return h;
}

typedef struct {
    uint64_t ctx_hash;
    uint32_t target_and_w;
} RawEntry;

typedef struct {
    uint64_t ctx_hash;
    uint32_t start_idx;
    uint32_t count_entries;
    uint32_t total_weight;
} CtxHeader;

typedef struct {
    uint16_t target;
    uint32_t weight;
} TargetCount;

typedef struct {
    CtxHeader *headers;
    size_t n_headers;
    TargetCount *targets;
    size_t n_targets;
} CompressedTable;

static uint32_t V_glob, N_train, N_test;
static uint16_t BOS_C, EOS_C, MISS_C, UNK_C, MASK_C;
static int32_t *active_vocab_ids;
static TrainSeq *train_seqs;
static TestSeq *test_seqs;
static CompressedTable comp_tables[NUM_TEMPLATES];
static double uni_logprob[MAX_V];
static size_t glob_total_valid_tokens = 0;
static float *ext_prior = NULL;
static double ext_alpha = 0.0;

#define ANCHOR_HASH_SIZE (1 << 21)
typedef struct {
    uint64_t key;
    int count;
    uint32_t *doc_pos; // (doc_id << 12) | pos
} AnchorBucket;
static AnchorBucket *anchor_table = NULL;

static inline uint32_t find_anchor_slot(uint64_t key) {
    uint32_t h = (uint32_t)splitmix64(key) & (ANCHOR_HASH_SIZE - 1);
    while (anchor_table[h].key != 0 && anchor_table[h].key != key) {
        h = (h + 1) & (ANCHOR_HASH_SIZE - 1);
    }
    return h;
}

static int cmp_raw_entry(const void *a, const void *b) {
    const RawEntry *ra = (const RawEntry *)a;
    const RawEntry *rb = (const RawEntry *)b;
    if (ra->ctx_hash < rb->ctx_hash) return -1;
    if (ra->ctx_hash > rb->ctx_hash) return 1;
    uint16_t ta = (uint16_t)(ra->target_and_w >> 8);
    uint16_t tb = (uint16_t)(rb->target_and_w >> 8);
    if (ta < tb) return -1;
    if (ta > tb) return 1;
    return 0;
}

static int cmp_target_desc(const void *a, const void *b) {
    const TargetCount *ta = (const TargetCount *)a;
    const TargetCount *tb = (const TargetCount *)b;
    if (ta->weight > tb->weight) return -1;
    if (ta->weight < tb->weight) return 1;
    return (int)ta->target - (int)tb->target;
}

static void build_template_table(int t_idx, size_t total_valid_tokens) {
    const TemplateSpec *spec = &TEMPLATES[t_idx];
    RawEntry *raw = (RawEntry *)malloc(total_valid_tokens * sizeof(RawEntry));
    size_t pos = 0;

    uint16_t pad_buf[4200];
    for (uint32_t d = 0; d < N_train; d++) {
        int L = train_seqs[d].len;
        if (L > 4096) L = 4096;
        for (int k = 0; k < 5; k++) pad_buf[k] = BOS_C;
        memcpy(pad_buf + 5, train_seqs[d].toks, L * sizeof(uint16_t));
        for (int k = 0; k < 5; k++) pad_buf[5 + L + k] = EOS_C;

        for (int i = 0; i < L; i++) {
            uint16_t targ = train_seqs[d].toks[i];
            if (targ >= V_glob) continue;
            uint32_t w = (i < 128) ? 2 : 1;
            uint64_t h = hash_ctx(pad_buf, i + 5, spec->n_off, spec->offsets);
            raw[pos].ctx_hash = h;
            raw[pos].target_and_w = ((uint32_t)targ << 8) | (w & 0xFF);
            pos++;
        }
    }

    qsort(raw, pos, sizeof(RawEntry), cmp_raw_entry);

    size_t n_ctx = 0, n_targ_max = 0;
    for (size_t i = 0; i < pos; ) {
        n_ctx++;
        uint64_t ch = raw[i].ctx_hash;
        size_t c_u = 0;
        while (i < pos && raw[i].ctx_hash == ch) {
            c_u++;
            uint16_t t = (uint16_t)(raw[i].target_and_w >> 8);
            while (i < pos && raw[i].ctx_hash == ch && (uint16_t)(raw[i].target_and_w >> 8) == t) {
                i++;
            }
        }
        n_targ_max += (c_u > TOP_K_PER_CTX ? TOP_K_PER_CTX : c_u);
    }

    CtxHeader *headers = (CtxHeader *)malloc(n_ctx * sizeof(CtxHeader));
    TargetCount *targets = (TargetCount *)malloc(n_targ_max * sizeof(TargetCount));
    TargetCount temp_tgs[MAX_V];

    size_t c_idx = 0, tg_idx = 0;
    for (size_t i = 0; i < pos; ) {
        uint64_t ch = raw[i].ctx_hash;
        uint32_t tot_w = 0;
        int n_u = 0;
        while (i < pos && raw[i].ctx_hash == ch) {
            uint16_t t = (uint16_t)(raw[i].target_and_w >> 8);
            uint32_t w_sum = 0;
            while (i < pos && raw[i].ctx_hash == ch && (uint16_t)(raw[i].target_and_w >> 8) == t) {
                w_sum += (raw[i].target_and_w & 0xFF);
                i++;
            }
            temp_tgs[n_u].target = t;
            temp_tgs[n_u].weight = w_sum;
            n_u++;
            tot_w += w_sum;
        }
        if (n_u > 1) {
            qsort(temp_tgs, n_u, sizeof(TargetCount), cmp_target_desc);
        }
        int keep = (n_u > TOP_K_PER_CTX) ? TOP_K_PER_CTX : n_u;
        headers[c_idx].ctx_hash = ch;
        headers[c_idx].start_idx = (uint32_t)tg_idx;
        headers[c_idx].count_entries = (uint32_t)keep;
        headers[c_idx].total_weight = tot_w;
        memcpy(&targets[tg_idx], temp_tgs, keep * sizeof(TargetCount));
        tg_idx += keep;
        c_idx++;
    }

    free(raw);
    comp_tables[t_idx].headers = headers;
    comp_tables[t_idx].n_headers = n_ctx;
    comp_tables[t_idx].targets = targets;
    comp_tables[t_idx].n_targets = tg_idx;
}

static void* build_worker(void *arg) {
    int tid = *(int *)arg;
    for (int t_idx = tid; t_idx < NUM_TEMPLATES; t_idx += NUM_THREADS) {
        build_template_table(t_idx, glob_total_valid_tokens);
    }
    return NULL;
}

static inline const CtxHeader* lookup_ctx(int t_idx, uint64_t h) {
    const CtxHeader *arr = comp_tables[t_idx].headers;
    size_t lo = 0, hi = comp_tables[t_idx].n_headers;
    while (lo < hi) {
        size_t mid = (lo + hi) >> 1;
        uint64_t mh = arr[mid].ctx_hash;
        if (mh == h) return &arr[mid];
        if (mh < h) lo = mid + 1;
        else hi = mid;
    }
    return NULL;
}

typedef struct {
    uint32_t doc_id;
    int offset;
    int count;
} PassageHit;

static int cmp_passage_hit(const void *a, const void *b) {
    const PassageHit *pa = (const PassageHit *)a;
    const PassageHit *pb = (const PassageHit *)b;
    if (pa->count != pb->count) return pb->count - pa->count;
    if (pa->doc_id != pb->doc_id) return (int)pa->doc_id - (int)pb->doc_id;
    return pa->offset - pb->offset;
}

typedef struct {
    int t_id;
    int mode_100_mask;
    double mrr_sum;
    int hit1;
    int hit5;
    int hit10;
    int total;
    float *out_scores;
    int *doc_mask_offset;
} WorkerArgs;

static void* eval_worker(void *arg) {
    WorkerArgs *wa = (WorkerArgs *)arg;
    int t_id = wa->t_id;
    int mode_100 = wa->mode_100_mask;

    double scores[MAX_V];
    double pass_probs[140][3];
    uint16_t pass_cands[140][3];
    int has_pass[140];
    int pos_to_m_idx[140];
    PassageHit phits[16000];

    static const int OFF6[6] = {-3, -2, -1, 1, 2, 3};

    for (uint32_t doc_idx = t_id; doc_idx < N_test; doc_idx += NUM_THREADS) {
        TestSeq *ts = &test_seqs[doc_idx];
        int L = ts->len;
        uint16_t seq[140];
        int m_cnt = 0;
        for (int i = 0; i < L; i++) {
            if (ts->lbl_toks[i] != -1) {
                pos_to_m_idx[i] = wa->doc_mask_offset[doc_idx] + m_cnt;
                m_cnt++;
            } else {
                pos_to_m_idx[i] = -1;
            }
            if (mode_100 && ts->lbl_toks[i] != -1) {
                seq[i] = MASK_C;
            } else {
                seq[i] = ts->in_toks[i];
                if (seq[i] == UNK_C) {
                    seq[i] = MASK_C;
                }
            }
        }
        uint16_t pad_buf[160];
        for (int k = 0; k < 5; k++) pad_buf[k] = BOS_C;
        memcpy(pad_buf + 5, seq, L * sizeof(uint16_t));
        for (int k = 0; k < 5; k++) pad_buf[5 + L + k] = EOS_C;

        int n_ph = 0;
        for (int i = 0; i < L - 2; i++) {
            uint16_t a = seq[i], b = seq[i+1], c = seq[i+2];
            if (a < V_glob && b < V_glob && c < V_glob) {
                uint64_t akey = ((uint64_t)1 << 40) | ((uint64_t)a << 24) | ((uint64_t)b << 12) | c;
                uint32_t slot = find_anchor_slot(akey);
                if (anchor_table[slot].key == akey) {
                    int cnt = anchor_table[slot].count;
                    const uint32_t *dp = anchor_table[slot].doc_pos;
                    for (int k = 0; k < cnt; k++) {
                        uint32_t d_id = dp[k] >> 12;
                        int t_pos = (int)(dp[k] & 0xFFF);
                        int off = t_pos - i;
                        int found = 0;
                        for (int z = 0; z < n_ph; z++) {
                            if (phits[z].doc_id == d_id && phits[z].offset == off) {
                                phits[z].count++;
                                found = 1;
                                break;
                            }
                        }
                        if (!found && n_ph < 16000) {
                            phits[n_ph].doc_id = d_id;
                            phits[n_ph].offset = off;
                            phits[n_ph].count = 1;
                            n_ph++;
                        }
                    }
                }
            }
        }
        if (n_ph > 1) {
            qsort(phits, n_ph, sizeof(PassageHit), cmp_passage_hit);
        }
        int top_ph = (n_ph > 60) ? 60 : n_ph;

        memset(has_pass, 0, sizeof(has_pass));

        for (int pass = 1; pass <= 2; pass++) {
            for (int i = 0; i < L; i++) {
                if (pass == 1 && seq[i] != MASK_C) continue;
                if (pass == 2 && ts->lbl_toks[i] == -1) continue;

                int pi = i + 5;
                int g_midx = pos_to_m_idx[i];
                const float *prior_row = (ext_prior && g_midx >= 0) ? (ext_prior + (size_t)g_midx * V_glob) : NULL;

                for (uint32_t v = 0; v < V_glob; v++) {
                    scores[v] = 0.25 * uni_logprob[v];
                    if (prior_row) {
                        scores[v] += ext_alpha * (double)prior_row[v];
                    }
                }

                uint32_t avail_mask = 0;
                for (int b = 0; b < 6; b++) {
                    if (pad_buf[pi + OFF6[b]] != MASK_C) {
                        avail_mask |= (1u << b);
                    }
                }

                // A. Global 83 templates
                for (int t_idx = 0; t_idx < NUM_TEMPLATES; t_idx++) {
                    const TemplateSpec *spec = &TEMPLATES[t_idx];
                    if (i + spec->offsets[0] < 0 || i + spec->offsets[spec->n_off - 1] >= L) continue;
                    if (spec->sub_mask != 0) {
                        if ((spec->sub_mask & avail_mask) != spec->sub_mask) continue;
                        if (!spec->in_v2 && (spec->gap_mask & avail_mask) != 0) continue;
                    } else {
                        int has_mask = 0;
                        for (int k = 0; k < spec->n_off; k++) {
                            if (pad_buf[pi + spec->offsets[k]] == MASK_C) {
                                has_mask = 1;
                                break;
                            }
                        }
                        if (has_mask) continue;
                    }
                    uint64_t h = hash_ctx(pad_buf, pi, spec->n_off, spec->offsets);
                    const CtxHeader *hdr = lookup_ctx(t_idx, h);
                    if (hdr) {
                        double tot = (double)hdr->total_weight;
                        double w_mult = 1.0;
                        if (spec->gap_mask != 0 && (spec->gap_mask & avail_mask) == 0) {
                            w_mult = 1.25;
                        }
                        double d0 = (spec->n_off >= 4) ? 0.35 : ((spec->n_off == 3) ? 0.85 : 1.5);
                        double eff_tot = (spec->n_off >= 4) ? (tot + 3.5) : ((spec->n_off == 3) ? (tot + 1.5) : tot);
                        double scale = w_mult * spec->weight * log1p(eff_tot) / (tot + d0);
                        const TargetCount *tgs = &comp_tables[t_idx].targets[hdr->start_idx];
                        uint32_t ne = hdr->count_entries;
                        for (uint32_t e = 0; e < ne; e++) {
                            scores[tgs[e].target] += scale * (double)tgs[e].weight;
                        }
                    }
                }

                // B1. Intra-Tablet Self-Parallel & Local N-gram Cache over same test document
                for (int j = 0; j < L; j++) {
                    if (j == i || (j > i - 2 && j < i + 2)) continue;
                    uint16_t cand = seq[j];
                    if (cand >= V_glob) continue;
                    int pj = j + 5;
                    int m_m1 = (pad_buf[pi - 1] < V_glob && pad_buf[pi - 1] == pad_buf[pj - 1]);
                    int m_p1 = (pad_buf[pi + 1] < V_glob && pad_buf[pi + 1] == pad_buf[pj + 1]);
                    int m_m2 = (pad_buf[pi - 2] < V_glob && pad_buf[pi - 2] == pad_buf[pj - 2]);
                    int m_p2 = (pad_buf[pi + 2] < V_glob && pad_buf[pi + 2] == pad_buf[pj + 2]);
                    int m_m3 = (pad_buf[pi - 3] < V_glob && pad_buf[pi - 3] == pad_buf[pj - 3]);
                    int m_p3 = (pad_buf[pi + 3] < V_glob && pad_buf[pi + 3] == pad_buf[pj + 3]);

                    int near_m = m_m1 + m_p1 + m_m2 + m_p2 + m_m3 + m_p3;
                    if (m_m1 && m_p1) {
                        scores[cand] += 5.5 + 3.5 * (m_m2 + m_p2 + m_m3 + m_p3);
                    } else if ((m_m1 && m_m2 && m_m3) || (m_p1 && m_p2 && m_p3)) {
                        scores[cand] += 6.5 + 3.0 * (m_m1 + m_p1 - 1);
                    } else if ((m_m1 && m_m2) || (m_p1 && m_p2)) {
                        scores[cand] += 3.0 + 1.8 * (m_m3 + m_p3 + m_m1 + m_p1 - 1);
                    } else if (near_m >= 3) {
                        scores[cand] += 1.5 * near_m;
                    } else if (m_m1 || m_p1) {
                        scores[cand] += 0.45;
                    }
                }

                // B2. Parallel Passage Alignment Vote across Training Corpus
                for (int p = 0; p < top_ph; p++) {
                    uint32_t d_id = phits[p].doc_id;
                    int t_pos = i + phits[p].offset;
                    int Lt = train_seqs[d_id].len;
                    if (t_pos >= 0 && t_pos < Lt) {
                        uint16_t cand = train_seqs[d_id].toks[t_pos];
                        if (cand < V_glob) {
                            int matches = 0, near_matches = 0;
                            const uint16_t *t_toks = train_seqs[d_id].toks;
                            for (int d = -8; d <= 8; d++) {
                                if (d == 0) continue;
                                int qi = i + d, ti = t_pos + d;
                                if (qi >= 0 && qi < L && ti >= 0 && ti < Lt) {
                                    uint16_t sv = seq[qi];
                                    if (sv < V_glob && sv == t_toks[ti]) {
                                        matches++;
                                        if (d >= -3 && d <= 3) near_matches++;
                                    }
                                }
                            }
                            if (matches >= 3) {
                                scores[cand] += 0.65 * matches + 1.05 * near_matches;
                                if (matches >= 6) {
                                    scores[cand] += 2.2 * (matches - 5);
                                }
                                if (near_matches >= 4) {
                                    scores[cand] += 3.5 * (near_matches - 3);
                                }
                            }
                        }
                    }
                }

                // C. Pass-2 Belief Propagation over Pass-1 top-3 at masked neighbor i-1 or i+1
                if (pass == 2) {
                    if (pad_buf[pi - 1] == MASK_C && i > 0 && has_pass[i - 1]) {
                        for (int c = 0; c < 3; c++) {
                            uint16_t cm1 = pass_cands[i - 1][c];
                            double pm1 = pass_probs[i - 1][c];
                            pad_buf[pi - 1] = cm1;
                            uint32_t av2 = avail_mask | (1u << 2);
                            for (int t_idx = 0; t_idx < 63; t_idx++) {
                                const TemplateSpec *spec = &TEMPLATES[t_idx];
                                if (i + spec->offsets[0] < 0 || i + spec->offsets[spec->n_off - 1] >= L) continue;
                                if (!((spec->sub_mask >> 2) & 1)) continue;
                                if (spec->gap_mask != 0) continue;
                                if ((spec->sub_mask & av2) != spec->sub_mask) continue;
                                uint64_t h = hash_ctx(pad_buf, pi, spec->n_off, spec->offsets);
                                const CtxHeader *hdr = lookup_ctx(t_idx, h);
                                if (hdr) {
                                    double tot = (double)hdr->total_weight;
                                    double scale = 0.65 * pm1 * spec->weight * log1p(tot) / (tot + 1.5);
                                    const TargetCount *tgs = &comp_tables[t_idx].targets[hdr->start_idx];
                                    for (uint32_t e = 0; e < hdr->count_entries; e++) {
                                        scores[tgs[e].target] += scale * (double)tgs[e].weight;
                                    }
                                }
                            }
                        }
                        pad_buf[pi - 1] = MASK_C;
                    }
                    if (pad_buf[pi + 1] == MASK_C && i + 1 < L && has_pass[i + 1]) {
                        for (int c = 0; c < 3; c++) {
                            uint16_t cp1 = pass_cands[i + 1][c];
                            double pp1 = pass_probs[i + 1][c];
                            pad_buf[pi + 1] = cp1;
                            uint32_t av2 = avail_mask | (1u << 3);
                            for (int t_idx = 0; t_idx < 63; t_idx++) {
                                const TemplateSpec *spec = &TEMPLATES[t_idx];
                                if (i + spec->offsets[0] < 0 || i + spec->offsets[spec->n_off - 1] >= L) continue;
                                if (!((spec->sub_mask >> 3) & 1)) continue;
                                if (spec->gap_mask != 0) continue;
                                if ((spec->sub_mask & av2) != spec->sub_mask) continue;
                                uint64_t h = hash_ctx(pad_buf, pi, spec->n_off, spec->offsets);
                                const CtxHeader *hdr = lookup_ctx(t_idx, h);
                                if (hdr) {
                                    double tot = (double)hdr->total_weight;
                                    double scale = 0.65 * pp1 * spec->weight * log1p(tot) / (tot + 1.5);
                                    const TargetCount *tgs = &comp_tables[t_idx].targets[hdr->start_idx];
                                    for (uint32_t e = 0; e < hdr->count_entries; e++) {
                                        scores[tgs[e].target] += scale * (double)tgs[e].weight;
                                    }
                                }
                            }
                        }
                        pad_buf[pi + 1] = MASK_C;
                    }

                    // D. Exact Bayesian self-token preservation in COLLATOR_80_10_10 when seq[i] < V_glob
                    if (!mode_100 && seq[i] < V_glob) {
                        uint16_t obs_c = seq[i];
                        double max_sc = -1e9;
                        for (uint32_t v = 0; v < V_glob; v++) {
                            if (scores[v] > max_sc) max_sc = scores[v];
                        }
                        double init_obs = 0.25 * uni_logprob[obs_c] + (prior_row ? ext_alpha * (double)prior_row[obs_c] : 0.0);
                        double obs_ngram_gain = scores[obs_c] - init_obs;
                        if (obs_ngram_gain > 0.05 || uni_logprob[obs_c] > -8.5) {
                            scores[obs_c] = max_sc + 500.0;
                        } else {
                            scores[obs_c] = max_sc - 0.001;
                        }
                    }

                    if (wa->out_scores && g_midx >= 0) {
                        float *dst = wa->out_scores + (size_t)g_midx * V_glob;
                        for (uint32_t v = 0; v < V_glob; v++) dst[v] = (float)scores[v];
                    }

                    int16_t true_c = ts->lbl_toks[i];
                    if (true_c >= 0 && true_c < (int16_t)V_glob) {
                        double true_sc = scores[true_c];
                        int rk = 1;
                        for (uint32_t v = 0; v < V_glob; v++) {
                            if (scores[v] > true_sc) rk++;
                        }
                        if (rk <= 100) wa->mrr_sum += 1.0 / (double)rk;
                        if (rk == 1) wa->hit1++;
                        if (rk <= 5) wa->hit5++;
                        if (rk <= 10) wa->hit10++;
                    }
                    wa->total++;
                } else {
                    int b0 = 0, b1 = 1, b2 = 2;
                    double s0 = -1e18, s1 = -1e18, s2 = -1e18;
                    for (uint32_t v = 0; v < V_glob; v++) {
                        double sc = scores[v];
                        if (sc > s0) { s2 = s1; b2 = b1; s1 = s0; b1 = b0; s0 = sc; b0 = v; }
                        else if (sc > s1) { s2 = s1; b2 = b1; s1 = sc; b1 = v; }
                        else if (sc > s2) { s2 = sc; b2 = v; }
                    }
                    pass_cands[i][0] = (uint16_t)b0;
                    pass_cands[i][1] = (uint16_t)b1;
                    pass_cands[i][2] = (uint16_t)b2;
                    double p0 = 1.0;
                    double p1 = exp((s1 - s0) * 0.25);
                    double p2 = exp((s2 - s0) * 0.25);
                    double psum = p0 + p1 + p2;
                    pass_probs[i][0] = p0 / psum;
                    pass_probs[i][1] = p1 / psum;
                    pass_probs[i][2] = p2 / psum;
                    has_pass[i] = 1;
                }
            }
        }
    }

    return NULL;
}

int main(int argc, char **argv) {
    const char *bin_path = (argc >= 4) ? argv[3] : "clss_akk_corpus_clean.bin";
    const char *out_scores_path = (argc >= 5) ? argv[4] : "clss_c_v3_scores.bin";

    init_templates();

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    FILE *f = fopen(bin_path, "rb");
    if (!f) { perror("fopen"); return 1; }
    fread(&V_glob, sizeof(uint32_t), 1, f);
    fread(&N_train, sizeof(uint32_t), 1, f);
    fread(&N_test, sizeof(uint32_t), 1, f);

    BOS_C = (uint16_t)V_glob;
    EOS_C = (uint16_t)(V_glob + 1);
    MISS_C = (uint16_t)(V_glob + 2);
    UNK_C = (uint16_t)(V_glob + 3);
    MASK_C = (uint16_t)(V_glob + 4);

    active_vocab_ids = (int32_t *)malloc(V_glob * sizeof(int32_t));
    fread(active_vocab_ids, sizeof(int32_t), V_glob, f);

    train_seqs = (TrainSeq *)malloc(N_train * sizeof(TrainSeq));
    size_t total_valid_tokens = 0;
    uint64_t uni_counts[MAX_V] = {0};
    uint64_t uni_total = 0;

    for (uint32_t i = 0; i < N_train; i++) {
        uint16_t len, is_u;
        fread(&len, sizeof(uint16_t), 1, f);
        fread(&is_u, sizeof(uint16_t), 1, f);
        train_seqs[i].len = len;
        train_seqs[i].is_unique = is_u;
        train_seqs[i].toks = (uint16_t *)malloc(len * sizeof(uint16_t));
        fread(train_seqs[i].toks, sizeof(uint16_t), len, f);
        for (int k = 0; k < len; k++) {
            uint16_t t = train_seqs[i].toks[k];
            if (t < V_glob) {
                total_valid_tokens++;
                uni_counts[t]++;
                uni_total++;
            }
        }
    }
    glob_total_valid_tokens = total_valid_tokens;

    for (uint32_t v = 0; v < V_glob; v++) {
        uni_logprob[v] = log(((double)uni_counts[v] + 0.5) / ((double)uni_total + 0.5 * V_glob));
    }

    test_seqs = (TestSeq *)malloc(N_test * sizeof(TestSeq));
    int *doc_mask_offset = (int *)malloc((N_test + 1) * sizeof(int));
    int total_masked = 0;
    for (uint32_t i = 0; i < N_test; i++) {
        doc_mask_offset[i] = total_masked;
        uint16_t len;
        fread(&len, sizeof(uint16_t), 1, f);
        test_seqs[i].len = len;
        test_seqs[i].in_toks = (uint16_t *)malloc(len * sizeof(uint16_t));
        test_seqs[i].lbl_toks = (int16_t *)malloc(len * sizeof(int16_t));
        test_seqs[i].raw_pos = (uint16_t *)malloc(len * sizeof(uint16_t));
        fread(test_seqs[i].in_toks, sizeof(uint16_t), len, f);
        fread(test_seqs[i].lbl_toks, sizeof(int16_t), len, f);
        fread(test_seqs[i].raw_pos, sizeof(uint16_t), len, f);
        for (int k = 0; k < len; k++) {
            if (test_seqs[i].lbl_toks[k] != -1) total_masked++;
        }
    }
    doc_mask_offset[N_test] = total_masked;
    fclose(f);

    if (argc >= 3) {
        const char *prior_path = argv[1];
        ext_alpha = atof(argv[2]);
        FILE *fp = fopen(prior_path, "rb");
        if (fp) {
            ext_prior = (float *)malloc((size_t)total_masked * V_glob * sizeof(float));
            fread(ext_prior, sizeof(float), (size_t)total_masked * V_glob, fp);
            fclose(fp);
            printf("Loaded external neural prior %s (alpha=%.2f)\n", prior_path, ext_alpha);
        }
    }

    pthread_t bth[NUM_THREADS];
    int btids[NUM_THREADS];
    for (int t = 0; t < NUM_THREADS; t++) {
        btids[t] = t;
        pthread_create(&bth[t], NULL, build_worker, &btids[t]);
    }
    for (int t = 0; t < NUM_THREADS; t++) {
        pthread_join(bth[t], NULL);
    }

    anchor_table = (AnchorBucket *)calloc(ANCHOR_HASH_SIZE, sizeof(AnchorBucket));
    for (int pass = 0; pass < 2; pass++) {
        for (uint32_t d = 0; d < N_train; d++) {
            int L = train_seqs[d].len;
            int lim = (L - 2 < 2048) ? (L - 2) : 2048;
            const uint16_t *wt = train_seqs[d].toks;
            for (int i = 0; i < lim; i++) {
                uint16_t a = wt[i], b = wt[i+1], c = wt[i+2];
                if (a < V_glob && b < V_glob && c < V_glob) {
                    uint64_t akey = ((uint64_t)1 << 40) | ((uint64_t)a << 24) | ((uint64_t)b << 12) | c;
                    uint32_t slot = find_anchor_slot(akey);
                    if (pass == 0) {
                        anchor_table[slot].key = akey;
                        if (anchor_table[slot].count < 80) anchor_table[slot].count++;
                    } else {
                        if (anchor_table[slot].count < 80) {
                            anchor_table[slot].doc_pos[anchor_table[slot].count++] = (d << 12) | (uint32_t)i;
                        }
                    }
                }
            }
        }
        if (pass == 0) {
            for (int s = 0; s < ANCHOR_HASH_SIZE; s++) {
                if (anchor_table[s].key != 0) {
                    anchor_table[s].doc_pos = (uint32_t *)malloc(anchor_table[s].count * sizeof(uint32_t));
                    anchor_table[s].count = 0;
                }
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt_idx = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("Indexed %d templates (%zu valid tokens, V=%u) + 3-gram anchors in %.2fs\n",
           NUM_TEMPLATES, total_valid_tokens, V_glob, dt_idx);

    float *out_scores = (float *)malloc((size_t)total_masked * V_glob * sizeof(float));
    float *out_scores_100 = (float *)malloc((size_t)total_masked * V_glob * sizeof(float));

    for (int mode_100 = 1; mode_100 >= 0; mode_100--) {
        struct timespec ts0, ts1;
        clock_gettime(CLOCK_MONOTONIC, &ts0);
        pthread_t th[NUM_THREADS];
        WorkerArgs wargs[NUM_THREADS];
        for (int t = 0; t < NUM_THREADS; t++) {
            wargs[t].t_id = t;
            wargs[t].mode_100_mask = mode_100;
            wargs[t].mrr_sum = 0.0;
            wargs[t].hit1 = 0;
            wargs[t].hit5 = 0;
            wargs[t].hit10 = 0;
            wargs[t].total = 0;
            wargs[t].out_scores = (mode_100 == 0) ? out_scores : out_scores_100;
            wargs[t].doc_mask_offset = doc_mask_offset;
            pthread_create(&th[t], NULL, eval_worker, &wargs[t]);
        }
        double mrr_sum = 0.0;
        int hit1 = 0, hit5 = 0, hit10 = 0, total = 0;
        for (int t = 0; t < NUM_THREADS; t++) {
            pthread_join(th[t], NULL);
            mrr_sum += wargs[t].mrr_sum;
            hit1 += wargs[t].hit1;
            hit5 += wargs[t].hit5;
            hit10 += wargs[t].hit10;
            total += wargs[t].total;
        }
        clock_gettime(CLOCK_MONOTONIC, &ts1);
        double dt_ev = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);
        printf("CLSS-C-v3 (%s, %.2fs): MRR=%.5f, Hit@1=%.5f, Hit@5=%.5f, Hit@10=%.5f (N=%d)\n",
               mode_100 ? "100%_MASK" : "COLLATOR_80_10_10", dt_ev,
               mrr_sum / total, (double)hit1 / total, (double)hit5 / total, (double)hit10 / total, total);
    }

    FILE *fo = fopen(out_scores_path, "wb");
    if (fo) {
        fwrite(&total_masked, sizeof(int), 1, fo);
        fwrite(&V_glob, sizeof(uint32_t), 1, fo);
        fwrite(active_vocab_ids, sizeof(int32_t), V_glob, fo);
        fwrite(out_scores, sizeof(float), (size_t)total_masked * V_glob, fo);
        fclose(fo);
        printf("Saved %s (%d x %u float32 + vocab IDs)\n", out_scores_path, total_masked, V_glob);
    }
    const char *out_100_env = getenv("CLSS_OUT_100MASK");
    if (out_100_env && out_100_env[0]) {
        FILE *fo100 = fopen(out_100_env, "wb");
        if (fo100) {
            fwrite(&total_masked, sizeof(int), 1, fo100);
            fwrite(&V_glob, sizeof(uint32_t), 1, fo100);
            fwrite(active_vocab_ids, sizeof(int32_t), V_glob, fo100);
            fwrite(out_scores_100, sizeof(float), (size_t)total_masked * V_glob, fo100);
            fclose(fo100);
        }
    }
    return 0;
}
