// Lens 2: Fast 64-bit bitmask WalkSAT + Dynamic Constraint Weighting (DCW) + Best-State Intensification
// Compile: clang -O3 -pthread covering_sa.c -o covering_sa
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

static int V, K, T, M, B;
static int NUM_SUBS;
static int V_SUB_LEN;
static uint64_t *sub_masks = NULL;
static int **v_subs = NULL;
static uint64_t *init_blocks_global = NULL;
static int n_init_blocks_global = 0;

static void gen_subsets_rec(int idx, int left, uint64_t cur, int *pos) {
    if (left == 0) {
        sub_masks[(*pos)++] = cur;
        return;
    }
    for (int i = idx; i <= V - left; i++) {
        gen_subsets_rec(i + 1, left - 1, cur | (1ULL << i), pos);
    }
}

static uint64_t xorshift64(uint64_t *s) {
    uint64_t x = *s;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return *s = x;
}

typedef struct {
    int thread_id;
    long long max_iters;
    char out_path[512];
} thread_arg_t;

static volatile int found_flag = 0;
static pthread_mutex_t out_mutex = PTHREAD_MUTEX_INITIALIZER;

static inline void add_uncov(int s, int *uncov_list, int *uncov_pos, int *n_uncov) {
    if (uncov_pos[s] < 0) {
        int idx = (*n_uncov)++;
        uncov_list[idx] = s;
        uncov_pos[s] = idx;
    }
}

static inline void rem_uncov(int s, int *uncov_list, int *uncov_pos, int *n_uncov) {
    int idx = uncov_pos[s];
    if (idx >= 0) {
        int last = uncov_list[--(*n_uncov)];
        uncov_list[idx] = last;
        uncov_pos[last] = idx;
        uncov_pos[s] = -1;
    }
}

static void rebuild_cov(uint64_t *blocks, uint16_t *cov, int *uncov_list, int *uncov_pos, int *n_uncov) {
    *n_uncov = 0;
    for (int s = 0; s < NUM_SUBS; s++) {
        uncov_pos[s] = -1;
        int c = 0;
        uint64_t sm = sub_masks[s];
        for (int i = 0; i < B; i++) {
            if (__builtin_popcountll(blocks[i] & sm) >= T) c++;
        }
        cov[s] = (uint16_t)c;
        if (c == 0) add_uncov(s, uncov_list, uncov_pos, n_uncov);
    }
}

static void apply_block_change(int bi, uint64_t old_bm, uint64_t new_bm,
                               uint64_t *blocks, uint16_t *cov,
                               int *uncov_list, int *uncov_pos, int *n_uncov) {
    uint64_t diff = old_bm ^ new_bm;
    uint64_t rem_mask = old_bm & diff;
    uint64_t add_mask = new_bm & diff;
    if (!diff) return;

    uint64_t cur_bm = old_bm;
    while (rem_mask && add_mask) {
        int u_out = __builtin_ctzll(rem_mask);
        int u_in = __builtin_ctzll(add_mask);
        rem_mask &= rem_mask - 1;
        add_mask &= add_mask - 1;
        uint64_t b_prime = cur_bm ^ (1ULL << u_out);
        const int *vs_out = v_subs[u_out];
        for (int idx = 0; idx < V_SUB_LEN; idx++) {
            int s = vs_out[idx];
            if (__builtin_popcountll(b_prime & sub_masks[s]) == T - 1) {
                if (--cov[s] == 0) add_uncov(s, uncov_list, uncov_pos, n_uncov);
            }
        }
        const int *vs_in = v_subs[u_in];
        for (int idx = 0; idx < V_SUB_LEN; idx++) {
            int s = vs_in[idx];
            if (__builtin_popcountll(b_prime & sub_masks[s]) == T - 1) {
                if (cov[s]++ == 0) rem_uncov(s, uncov_list, uncov_pos, n_uncov);
            }
        }
        cur_bm = b_prime | (1ULL << u_in);
    }
    blocks[bi] = cur_bm;
}

static void *worker(void *arg_ptr) {
    thread_arg_t *arg = (thread_arg_t *)arg_ptr;
    uint64_t rng = 0xD1B54A32D192ED03ULL ^ ((uint64_t)(arg->thread_id + 1) * 0x94D049BB133111EBULL) ^ (uint64_t)time(NULL);

    uint64_t *blocks = calloc(B, sizeof(uint64_t));
    uint64_t *best_blocks = calloc(B, sizeof(uint64_t));
    uint16_t *cov = calloc(NUM_SUBS, sizeof(uint16_t));
    uint32_t *weights = calloc(NUM_SUBS, sizeof(uint32_t));
    int *uncov_list = calloc(NUM_SUBS, sizeof(int));
    int *uncov_pos = malloc(NUM_SUBS * sizeof(int));
    long long *tabu = calloc((size_t)B * 64, sizeof(long long));

    if (n_init_blocks_global >= B) {
        int skip = (n_init_blocks_global > B) ? (arg->thread_id % n_init_blocks_global) : -1;
        int dst = 0;
        for (int i = 0; i < n_init_blocks_global && dst < B; i++) {
            if (i == skip) continue;
            uint64_t bm = init_blocks_global[i] & ((1ULL << V) - 1ULL);
            while (__builtin_popcountll(bm) < K) bm |= (1ULL << (xorshift64(&rng) % V));
            while (__builtin_popcountll(bm) > K) {
                int bit = xorshift64(&rng) % V;
                if (bm & (1ULL << bit)) bm ^= (1ULL << bit);
            }
            blocks[dst++] = bm;
        }
    } else {
        int v0 = (arg->thread_id % 2 == 0) ? V : (V - 1);
        if (v0 < 1) v0 = 1;
        uint64_t base_mask = 0;
        for (int i = 0; i < B; i++) {
            if (i % v0 == 0) {
                base_mask = 0;
                while (__builtin_popcountll(base_mask) < K) {
                    base_mask |= (1ULL << (xorshift64(&rng) % V));
                }
            }
            int sh = i % v0;
            uint64_t cyc = base_mask & ((1ULL << v0) - 1ULL);
            uint64_t fix = base_mask & ~((1ULL << v0) - 1ULL);
            uint64_t bm = (((cyc << sh) | (cyc >> (v0 - sh))) & ((1ULL << v0) - 1ULL)) | fix;
            while (1) {
                int dup = 0;
                for (int j = 0; j < i; j++) if (blocks[j] == bm) dup = 1;
                if (!dup && __builtin_popcountll(bm) == K) break;
                bm = 0;
                while (__builtin_popcountll(bm) < K) bm |= (1ULL << (xorshift64(&rng) % V));
            }
            blocks[i] = bm;
        }
    }

    for (int s = 0; s < NUM_SUBS; s++) weights[s] = 1;
    int n_uncov = 0;
    rebuild_cov(blocks, cov, uncov_list, uncov_pos, &n_uncov);

    int best_uncov = n_uncov;
    memcpy(best_blocks, blocks, B * sizeof(uint64_t));
    long long last_imp_iter = 0;

    for (long long iter = 1; iter <= arg->max_iters && !found_flag; iter++) {
        if (n_uncov < best_uncov) {
            best_uncov = n_uncov;
            memcpy(best_blocks, blocks, B * sizeof(uint64_t));
            last_imp_iter = iter;
            if (arg->thread_id == 0 && (best_uncov <= 15 || iter % 10000 == 0)) {
                printf("[SA T%d] iter=%lld best_uncov=%d/%d\n", arg->thread_id, iter, best_uncov, NUM_SUBS);
                fflush(stdout);
            }
        }
        if (n_uncov == 0) {
            int dup = 0;
            for (int i = 0; i < B; i++) {
                for (int j = i + 1; j < B; j++) if (blocks[i] == blocks[j]) dup = 1;
            }
            if (!dup) {
                pthread_mutex_lock(&out_mutex);
                if (!found_flag) {
                    found_flag = 1;
                    FILE *fp = fopen(arg->out_path, "w");
                    if (fp) {
                        fprintf(fp, "{\n  \"v\": %d, \"k\": %d, \"t\": %d, \"m\": %d, \"b\": %d,\n  \"method\": \"c-evaluator-optimizer (64-bit DCW + WalkSAT/Tabu)\",\n  \"blocks\": [\n",
                                V, K, T, M, B);
                        for (int i = 0; i < B; i++) {
                            fprintf(fp, "    [");
                            int first = 1;
                            for (int bit = 0; bit < V; bit++) {
                                if (blocks[i] & (1ULL << bit)) {
                                    fprintf(fp, "%s%d", first ? "" : ",", bit + 1);
                                    first = 0;
                                }
                            }
                            fprintf(fp, "]%s\n", (i + 1 < B) ? "," : "");
                        }
                        fprintf(fp, "  ]\n}\n");
                        fclose(fp);
                    }
                    printf("SUCCESS [SA T%d]: found (%d,%d,%d,%d) in %d blocks at iter %lld -> %s\n",
                           arg->thread_id, V, K, T, M, B, iter, arg->out_path);
                    fflush(stdout);
                }
                pthread_mutex_unlock(&out_mutex);
                break;
            }
        }

        // Periodic intensification around best_blocks when stalled
        if (iter - last_imp_iter > 2500) {
            memcpy(blocks, best_blocks, B * sizeof(uint64_t));
            rebuild_cov(blocks, cov, uncov_list, uncov_pos, &n_uncov);
            for (int s = 0; s < NUM_SUBS; s++) weights[s] = (weights[s] >> 1) + 1;
            for (int idx = 0; idx < n_uncov; idx++) weights[uncov_list[idx]] += 5 + (xorshift64(&rng) % 7);
            memset(tabu, 0, (size_t)B * 64 * sizeof(long long));
            last_imp_iter = iter;
        }

        int s0 = uncov_list[xorshift64(&rng) % n_uncov];
        if ((xorshift64(&rng) % 10 < 7) && n_uncov > 1) {
            for (int q = 0; q < 3; q++) {
                int cand_s = uncov_list[xorshift64(&rng) % n_uncov];
                if (weights[cand_s] > weights[s0]) s0 = cand_s;
            }
        }
        uint64_t s0_mask = sub_masks[s0];

        int max_inter = -1;
        int cand_blocks[160];
        int n_cand_blocks = 0;
        for (int i = 0; i < B; i++) {
            int inter = __builtin_popcountll(blocks[i] & s0_mask);
            if (inter > max_inter) {
                max_inter = inter;
                n_cand_blocks = 0;
                cand_blocks[n_cand_blocks++] = i;
            } else if (inter == max_inter && n_cand_blocks < 160) {
                cand_blocks[n_cand_blocks++] = i;
            }
        }

        int best_blk = -1;
        uint64_t best_new_bm = 0;
        int64_t best_delta = 0x7FFFFFFFFFFFFFFFLL;
        int n_ties = 0;

        int blk_samples = (n_cand_blocks <= 24) ? n_cand_blocks : 24;
        for (int bs = 0; bs < blk_samples; bs++) {
            int bi = (n_cand_blocks <= 24) ? cand_blocks[bs] : cand_blocks[xorshift64(&rng) % n_cand_blocks];
            uint64_t bm = blocks[bi];
            int r = __builtin_popcountll(bm & s0_mask);
            int d = T - r;
            if (d <= 0) continue;

            uint64_t in_mask = s0_mask & ~bm;
            uint64_t out_mask = bm & ~s0_mask;
            int ins[32], n_ins = 0;
            int outs[32], n_outs = 0;
            int64_t out_loss[32];

            for (int u = 0; u < V; u++) {
                if (in_mask & (1ULL << u)) ins[n_ins++] = u;
                if (out_mask & (1ULL << u)) {
                    int64_t l = 0;
                    uint64_t b_prime = bm ^ (1ULL << u);
                    const int *vs_out = v_subs[u];
                    for (int idx = 0; idx < V_SUB_LEN; idx++) {
                        int s = vs_out[idx];
                        if (cov[s] == 1 && __builtin_popcountll(b_prime & sub_masks[s]) == T - 1) {
                            l += weights[s];
                        }
                    }
                    out_loss[n_outs] = l;
                    outs[n_outs++] = u;
                }
            }
            if (n_ins < d || n_outs < d) continue;

            for (int a = 0; a < n_outs - 1; a++) {
                for (int b = a + 1; b < n_outs; b++) {
                    if (out_loss[b] < out_loss[a]) {
                        int64_t tl = out_loss[a]; out_loss[a] = out_loss[b]; out_loss[b] = tl;
                        int tu = outs[a]; outs[a] = outs[b]; outs[b] = tu;
                    }
                }
            }

            if (d == 1) {
                int out_try = (n_outs <= 8) ? n_outs : 8;
                for (int oo = 0; oo < out_try; oo++) {
                    int u_out = outs[oo];
                    if (tabu[bi * 64 + u_out] > iter && best_blk >= 0) continue;
                    uint64_t b_prime = bm ^ (1ULL << u_out);
                    int64_t base_loss = out_loss[oo];

                    for (int ii = 0; ii < n_ins; ii++) {
                        int u_in = ins[ii];
                        uint64_t new_bm = b_prime | (1ULL << u_in);
                        int is_dup = 0;
                        for (int j = 0; j < B; j++) if (j != bi && blocks[j] == new_bm) { is_dup = 1; break; }
                        if (is_dup) continue;

                        int64_t gain = 0;
                        uint64_t u_in_bit = 1ULL << u_in;
                        for (int idx = 0; idx < n_uncov; idx++) {
                            int s = uncov_list[idx];
                            uint64_t sm = sub_masks[s];
                            if ((sm & u_in_bit) && __builtin_popcountll(b_prime & sm) == T - 1) {
                                gain += weights[s];
                            }
                        }
                        int64_t delta = base_loss - gain;
                        if (delta < best_delta) {
                            best_delta = delta;
                            best_blk = bi;
                            best_new_bm = new_bm;
                            n_ties = 1;
                        } else if (delta == best_delta) {
                            n_ties++;
                            if ((xorshift64(&rng) % n_ties) == 0) {
                                best_blk = bi;
                                best_new_bm = new_bm;
                            }
                        }
                    }
                }
            } else {
                uint64_t new_bm = bm;
                int64_t approx_loss = 0;
                for (int q = 0; q < d; q++) {
                    new_bm ^= (1ULL << outs[q]);
                    approx_loss += out_loss[q];
                }
                for (int q = 0; q < d; q++) {
                    int pick = q + (xorshift64(&rng) % (n_ins - q));
                    int tmp = ins[q]; ins[q] = ins[pick]; ins[pick] = tmp;
                    new_bm |= (1ULL << ins[q]);
                }
                int64_t gain = 0;
                for (int idx = 0; idx < n_uncov; idx++) {
                    int s = uncov_list[idx];
                    if (__builtin_popcountll(new_bm & sub_masks[s]) >= T) {
                        gain += weights[s];
                    }
                }
                int64_t delta = approx_loss - gain;
                if (delta < best_delta) {
                    best_delta = delta;
                    best_blk = bi;
                    best_new_bm = new_bm;
                    n_ties = 1;
                }
            }
        }

        if (best_blk >= 0) {
            int old_n_uncov = n_uncov;
            uint64_t old_bm = blocks[best_blk];
            uint64_t added = best_new_bm & ~old_bm;
            while (added) {
                int u_in = __builtin_ctzll(added);
                added &= added - 1;
                tabu[best_blk * 64 + u_in] = iter + 5 + (xorshift64(&rng) % 8);
            }
            apply_block_change(best_blk, old_bm, best_new_bm, blocks, cov, uncov_list, uncov_pos, &n_uncov);

            if (n_uncov >= old_n_uncov) {
                for (int idx = 0; idx < n_uncov; idx++) {
                    weights[uncov_list[idx]]++;
                }
                if (weights[s0] > 5000) {
                    for (int s = 0; s < NUM_SUBS; s++) weights[s] = (weights[s] >> 1) + 1;
                }
            }
        }
    }

    free(blocks);
    free(best_blocks);
    free(cov);
    free(weights);
    free(uncov_list);
    free(uncov_pos);
    free(tabu);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 7) {
        fprintf(stderr, "Usage: %s v k t m b out.json [max_iters] [threads] [init_blocks.txt]\n", argv[0]);
        return 1;
    }
    V = atoi(argv[1]);
    K = atoi(argv[2]);
    T = atoi(argv[3]);
    M = atoi(argv[4]);
    B = atoi(argv[5]);
    const char *out_path = argv[6];
    long long max_iters = (argc > 7) ? atoll(argv[7]) : 200000;
    int n_threads = (argc > 8) ? atoi(argv[8]) : 8;

    if (argc > 9) {
        FILE *fp = fopen(argv[9], "r");
        if (fp) {
            init_blocks_global = calloc(1000, sizeof(uint64_t));
            char line[2048];
            while (fgets(line, sizeof(line), fp) && n_init_blocks_global < 1000) {
                uint64_t bm = 0;
                char *p = line;
                while (*p) {
                    while (*p && (*p < '0' || *p > '9')) p++;
                    if (!*p) break;
                    int val = (int)strtol(p, &p, 10);
                    if (val >= 1 && val <= 64) bm |= (1ULL << (val - 1));
                }
                if (__builtin_popcountll(bm) >= T) {
                    init_blocks_global[n_init_blocks_global++] = bm;
                }
            }
            fclose(fp);
            printf("Loaded %d initial blocks from %s\n", n_init_blocks_global, argv[9]);
        }
    }

    long long cvm = 1;
    for (int i = 1; i <= M; i++) cvm = cvm * (V - i + 1) / i;
    NUM_SUBS = (int)cvm;
    V_SUB_LEN = (int)(cvm * M / V);

    sub_masks = malloc(NUM_SUBS * sizeof(uint64_t));
    int pos = 0;
    gen_subsets_rec(0, M, 0ULL, &pos);

    v_subs = malloc(V * sizeof(int *));
    int *v_cnt = calloc(V, sizeof(int));
    for (int u = 0; u < V; u++) v_subs[u] = malloc(V_SUB_LEN * sizeof(int));
    for (int s = 0; s < NUM_SUBS; s++) {
        uint64_t sm = sub_masks[s];
        for (int u = 0; u < V; u++) {
            if (sm & (1ULL << u)) v_subs[u][v_cnt[u]++] = s;
        }
    }
    free(v_cnt);

    pthread_t th[32];
    thread_arg_t args[32];
    for (int i = 0; i < n_threads; i++) {
        args[i].thread_id = i;
        args[i].max_iters = max_iters;
        strncpy(args[i].out_path, out_path, sizeof(args[i].out_path) - 1);
        pthread_create(&th[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < n_threads; i++) pthread_join(th[i], NULL);

    for (int u = 0; u < V; u++) free(v_subs[u]);
    free(v_subs);
    free(sub_masks);
    if (init_blocks_global) free(init_blocks_global);
    return found_flag ? 0 : 1;
}
