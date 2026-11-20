#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

/*
 * Fast exact 0-1 cluster-merging verifier & redundancy detector for sorting networks (n <= 64).
 */

typedef struct {
    int u, v;
} Pair;

typedef struct {
    uint64_t *data;
    size_t len;
} Cluster;

static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a;
    uint64_t y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}

static int greedy_depth(int n, const Pair *ces, int m) {
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

/*
 * Verify network `ces[0..m-1]` on `n` wires.
 * Returns 1 if valid sorting network, 0 if invalid, -1 if max_patterns exceeded.
 * Also records any comparator index `k` that was a no-op upon application in `noop_flag[k]`.
 */
static int verify_network(int n, const Pair *ces, int m, size_t max_patterns, int *out_noop_count, int *first_noop_orig_idx, int *is_noop_arr) {
    Cluster clusters[64];
    int listidx[64];
    for (int k = 0; k < n; k++) {
        clusters[k].data = (uint64_t *)malloc(2 * sizeof(uint64_t));
        clusters[k].data[0] = 0ULL;
        clusters[k].data[1] = 1ULL << k;
        clusters[k].len = 2;
        listidx[k] = k;
    }

    typedef struct {
        int u, v, orig_idx;
    } WorkItem;

    WorkItem *work = (WorkItem *)malloc(m * sizeof(WorkItem));
    WorkItem *tmp_work = (WorkItem *)malloc(m * sizeof(WorkItem));
    for (int k = 0; k < m; k++) {
        work[k].u = ces[k].u;
        work[k].v = ces[k].v;
        work[k].orig_idx = k;
        if (is_noop_arr) is_noop_arr[k] = 0;
    }
    int wlen = m;
    int noop_cnt = 0;
    if (first_noop_orig_idx) *first_noop_orig_idx = -1;

    while (wlen > 0) {
        int i = work[0].u;
        int j = work[0].v;
        int orig_idx = work[0].orig_idx;

        if (listidx[i] != listidx[j]) {
            int ci = listidx[i];
            int cj = listidx[j];
            size_t li = clusters[ci].len;
            size_t lj = clusters[cj].len;
            if (li > max_patterns / lj) {
                for (int k = 0; k < n; k++) if (clusters[k].data) free(clusters[k].data);
                free(work);
                free(tmp_work);
                return -1;
            }
            size_t lz_len = li * lj;
            uint64_t *lz = (uint64_t *)malloc(lz_len * sizeof(uint64_t));
            const uint64_t *di = clusters[ci].data;
            const uint64_t *dj = clusters[cj].data;
            size_t idx = 0;
            for (size_t a = 0; a < li; a++) {
                uint64_t pa = di[a];
                for (size_t b = 0; b < lj; b++) {
                    lz[idx++] = pa | dj[b];
                }
            }
            qsort(lz, lz_len, sizeof(uint64_t), cmp_u64);
            free(clusters[ci].data);
            free(clusters[cj].data);
            clusters[ci].data = lz;
            clusters[ci].len = lz_len;
            clusters[cj].data = NULL;
            clusters[cj].len = 0;
            for (int k = 0; k < n; k++) {
                if (listidx[k] == cj) listidx[k] = ci;
            }

            /* Reorder remaining worklist to fire accessible intra-cluster CEs first */
            uint64_t visited = 0ULL;
            int n1 = 0, n2 = 0;
            WorkItem *l2 = tmp_work;
            for (int k = 0; k < wlen; k++) {
                int p = work[k].u, q = work[k].v;
                uint64_t mp = (1ULL << p) | (1ULL << q);
                if ((visited & mp) == 0 && listidx[p] == listidx[q]) {
                    work[n1++] = work[k];
                } else {
                    l2[n2++] = work[k];
                }
                visited |= mp;
            }
            memcpy(work + n1, l2, n2 * sizeof(WorkItem));
            i = work[0].u;
            j = work[0].v;
            orig_idx = work[0].orig_idx;
        }

        /* Apply CE (i, j) on clusters[listidx[i]] */
        int ci = listidx[i];
        uint64_t *pat = clusters[ci].data;
        size_t l = clusters[ci].len;
        uint64_t p = 1ULL << i;
        uint64_t q = 1ULL << j;
        uint64_t mask = p | q;

        size_t idxp = 0, idxnp = 0;
        while (idxp < l && (pat[idxp] & mask) != p) idxp++;
        if (idxp == l) {
            /* Zero patterns had bit i == 1 and bit j == 0! This CE is a no-op! */
            noop_cnt++;
            if (is_noop_arr) is_noop_arr[orig_idx] = 1;
            if (first_noop_orig_idx && *first_noop_orig_idx == -1) {
                *first_noop_orig_idx = orig_idx;
            }
        } else {
            while (idxnp < l && (pat[idxnp] & mask) == p) idxnp++;
            uint64_t *res = (uint64_t *)malloc(l * sizeof(uint64_t));
            size_t out = 0;
            uint64_t last = UINT64_MAX;
            int has_last = 0;

            while (idxnp < l && idxp < l) {
                uint64_t a = pat[idxp] ^ mask;
                uint64_t b = pat[idxnp];
                if (a < b) {
                    if (!has_last || a != last) {
                        res[out++] = a;
                        last = a;
                        has_last = 1;
                    }
                    idxp++;
                    while (idxp < l && (pat[idxp] & mask) != p) idxp++;
                } else if (b < a) {
                    if (!has_last || b != last) {
                        res[out++] = b;
                        last = b;
                        has_last = 1;
                    }
                    idxnp++;
                    while (idxnp < l && (pat[idxnp] & mask) == p) idxnp++;
                } else {
                    /* a == b: advance both! */
                    if (!has_last || a != last) {
                        res[out++] = a;
                        last = a;
                        has_last = 1;
                    }
                    idxp++;
                    while (idxp < l && (pat[idxp] & mask) != p) idxp++;
                    idxnp++;
                    while (idxnp < l && (pat[idxnp] & mask) == p) idxnp++;
                }
            }
            while (idxnp < l) {
                uint64_t b = pat[idxnp];
                if (!has_last || b != last) {
                    res[out++] = b;
                    last = b;
                    has_last = 1;
                }
                idxnp++;
                while (idxnp < l && (pat[idxnp] & mask) == p) idxnp++;
            }
            while (idxp < l) {
                uint64_t a = pat[idxp] ^ mask;
                if (!has_last || a != last) {
                    res[out++] = a;
                    last = a;
                    has_last = 1;
                }
                idxp++;
                while (idxp < l && (pat[idxp] & mask) != p) idxp++;
            }
            free(pat);
            clusters[ci].data = res;
            clusters[ci].len = out;
        }

        memmove(work, work + 1, (wlen - 1) * sizeof(WorkItem));
        wlen--;
    }

    if (out_noop_count) *out_noop_count = noop_cnt;

    /* Check total output patterns == n + 1 and single cluster */
    int c0 = listidx[0];
    int single_cluster = 1;
    for (int k = 1; k < n; k++) {
        if (listidx[k] != c0) single_cluster = 0;
    }
    int valid = 0;
    if (single_cluster && clusters[c0].len == (size_t)(n + 1)) {
        valid = 1;
        for (int k = 0; k <= n; k++) {
            uint64_t expected = (k == 0) ? 0ULL : ((k == 64) ? UINT64_MAX : (((1ULL << k) - 1ULL) << (n - k)));
            if (clusters[c0].data[k] != expected) {
                valid = 0;
                break;
            }
        }
    }

    for (int k = 0; k < n; k++) {
        if (clusters[k].data) free(clusters[k].data);
    }
    free(work);
    free(tmp_work);
    return valid;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <network_txt_file> [check_leave_one_out] [out_pruned_file]\n", argv[0]);
        return 1;
    }
    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }
    int n, m;
    if (fscanf(fp, "%d %d", &n, &m) != 2) {
        fprintf(stderr, "Invalid header\n");
        fclose(fp);
        return 1;
    }
    Pair *ces = (Pair *)malloc(m * sizeof(Pair));
    for (int k = 0; k < m; k++) {
        if (fscanf(fp, "%d %d", &ces[k].u, &ces[k].v) != 2) {
            fprintf(stderr, "Error reading pair %d\n", k);
            fclose(fp);
            return 1;
        }
    }
    fclose(fp);

    int noop_cnt = 0, first_noop = -1;
    int *is_noop = (int *)calloc(m, sizeof(int));
    size_t max_pat = 200000000ULL;
    int v = verify_network(n, ces, m, max_pat, &noop_cnt, &first_noop, is_noop);
    int d = greedy_depth(n, ces, m);

    Pair *pruned = (Pair *)malloc(m * sizeof(Pair));
    int pm = 0;
    for (int k = 0; k < m; k++) {
        if (!is_noop[k]) pruned[pm++] = ces[k];
    }
    int pd = greedy_depth(n, pruned, pm);

    printf("VERIFY n=%d size=%d depth=%d valid=%d noops=%d pruned_size=%d pruned_depth=%d\n",
           n, m, d, v, noop_cnt, pm, pd);

    if (v == 1 && argc >= 4) {
        FILE *out_fp = fopen(argv[3], "w");
        if (out_fp) {
            fprintf(out_fp, "%d %d\n", n, pm);
            for (int k = 0; k < pm; k++) {
                fprintf(out_fp, "%d %d\n", pruned[k].u, pruned[k].v);
            }
            fclose(out_fp);
        }
    }

    if (v == 1 && argc >= 3 && atoi(argv[2]) == 1) {
        Pair *sub = (Pair *)malloc(pm * sizeof(Pair));
        for (int skip = pm - 1; skip >= 0; skip--) {
            int idx = 0;
            for (int k = 0; k < pm; k++) {
                if (k != skip) sub[idx++] = pruned[k];
            }
            int v2 = verify_network(n, sub, pm - 1, max_pat, NULL, NULL, NULL);
            if (v2 == 1) {
                printf("REDUNDANT_CE index=%d pair=(%d,%d) new_size=%d new_depth=%d\n",
                       skip, pruned[skip].u, pruned[skip].v, pm - 1, greedy_depth(n, sub, pm - 1));
            }
        }
        free(sub);
    }

    free(is_noop);
    free(pruned);
    free(ces);
    return (v == 1) ? 0 : 1;
}
