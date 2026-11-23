#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

#define MAX_STATES 22
#define MAX_LETTERS 16

typedef struct {
    int n, k;
    int T[MAX_LETTERS][MAX_STATES];
} Automaton;

static int check_eulerian_and_floyd(const Automaton *A) {
    if (A->n < 3 || A->n > MAX_STATES || A->k < 1 || A->k > MAX_LETTERS) return 0;
    int indeg[MAX_STATES] = {0};
    int reach[MAX_STATES][MAX_STATES];
    memset(reach, 0, sizeof(reach));
    for (int q = 0; q < A->n; q++) reach[q][q] = 1;

    for (int a = 0; a < A->k; a++) {
        for (int q = 0; q < A->n; q++) {
            int v = A->T[a][q];
            if (v < 0 || v >= A->n) return 0;
            indeg[v]++;
            reach[q][v] = 1;
        }
    }
    for (int q = 0; q < A->n; q++) {
        if (indeg[q] != A->k) return 0;
    }
    for (int m = 0; m < A->n; m++)
        for (int i = 0; i < A->n; i++)
            if (reach[i][m])
                for (int j = 0; j < A->n; j++)
                    if (reach[m][j]) reach[i][j] = 1;

    for (int i = 0; i < A->n; i++)
        for (int j = 0; j < A->n; j++)
            if (!reach[i][j]) return 0;
    return 1;
}

static int check_pair_sync(const Automaton *A) {
    int n = A->n, k = A->k;
    int merged[MAX_STATES][MAX_STATES];
    memset(merged, 0, sizeof(merged));
    int tail = 0;
    for (int i = 0; i < n; i++) merged[i][i] = 1;

    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (merged[i][j]) continue;
                for (int a = 0; a < k; a++) {
                    int u = A->T[a][i], v = A->T[a][j];
                    int p1 = u < v ? u : v, p2 = u < v ? v : u;
                    if (merged[p1][p2]) {
                        merged[i][j] = merged[j][i] = 1;
                        tail++;
                        changed = 1;
                        break;
                    }
                }
            }
        }
    }
    return tail == n * (n - 1) / 2;
}

static int exact_bitmask_bfs(const Automaton *A) {
    int n = A->n, k = A->k;
    uint32_t total_masks = 1U << n;
    int32_t *dist = (int32_t *)malloc(total_masks * sizeof(int32_t));
    uint32_t *queue = (uint32_t *)malloc(total_masks * sizeof(uint32_t));
    if (!dist || !queue) { free(dist); free(queue); return -2; }
    for (uint32_t i = 0; i < total_masks; i++) dist[i] = -1;

    uint32_t full = total_masks - 1U;
    dist[full] = 0;
    queue[0] = full;
    uint32_t head = 0, tail = 1;
    int ans = -1;

    while (head < tail) {
        uint32_t m = queue[head++];
        if (m != 0 && (m & (m - 1U)) == 0) {
            ans = dist[m];
            break;
        }
        for (int a = 0; a < k; a++) {
            uint32_t nm = 0;
            for (int q = 0; q < n; q++) {
                if (m & (1U << q)) nm |= (1U << A->T[a][q]);
            }
            if (dist[nm] == -1) {
                dist[nm] = dist[m] + 1;
                queue[tail++] = nm;
            }
        }
    }
    free(dist);
    free(queue);
    return ans;
}

static int parse_int_after_key(const char *buf, const char *key, int *out) {
    const char *p = strstr(buf, key);
    if (!p) return 0;
    p += strlen(key);
    while (*p && (isspace((unsigned char)*p) || *p == ':')) p++;
    if (!*p || (!isdigit((unsigned char)*p) && *p != '-')) return 0;
    char *endp = NULL;
    long v = strtol(p, &endp, 10);
    if (endp == p) return 0;
    *out = (int)v;
    return 1;
}

static int parse_transitions(const char *buf, Automaton *A) {
    const char *p = strstr(buf, "\"transitions\"");
    if (!p) return 0;
    p = strchr(p, '[');
    if (!p) return 0;
    p++;
    for (int a = 0; a < A->k; a++) {
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p != '[') return 0;
        p++;
        for (int q = 0; q < A->n; q++) {
            while (*p && isspace((unsigned char)*p)) p++;
            if (!isdigit((unsigned char)*p) && *p != '-') return 0;
            char *endp = NULL;
            long v = strtol(p, &endp, 10);
            if (endp == p) return 0;
            A->T[a][q] = (int)v;
            p = endp;
            while (*p && isspace((unsigned char)*p)) p++;
            if (q + 1 < A->n) {
                if (*p != ',') return 0;
                p++;
            }
        }
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p != ']') return 0;
        p++;
        while (*p && isspace((unsigned char)*p)) p++;
        if (a + 1 < A->k) {
            if (*p != ',') return 0;
            p++;
        }
    }
    while (*p && isspace((unsigned char)*p)) p++;
    if (*p != ']') return 0;
    return 1;
}

static int run_c_calibrations(void) {
    int ms[3] = {1, 2, 3}, exp_rts[3] = {11, 39, 83};
    for (int i = 0; i < 3; i++) {
        Automaton SV;
        SV.n = 4 * ms[i] + 1;
        SV.k = 4;
        for (int q = 0; q < SV.n; q++) {
            SV.T[0][q] = (SV.n - 1 - q) % SV.n;
            SV.T[1][q] = (SV.n + 1 - q) % SV.n;
            SV.T[2][q] = (q == 1) ? 0 : q;
            SV.T[3][q] = (q == 0) ? 1 : q;
        }
        int eul = check_eulerian_and_floyd(&SV);
        int ps = check_pair_sync(&SV);
        int rt = exact_bitmask_bfs(&SV);
        if (!eul || !ps || rt != exp_rts[i]) return 0;
        printf("[C-CALIB] Szykula-Vorel A_%d (n=%d, k=4): eulerian=%d, rt=%d == %d\n",
               ms[i], SV.n, eul, rt, exp_rts[i]);
    }
    Automaton C5;
    C5.n = 5; C5.k = 2;
    for (int q = 0; q < 5; q++) {
        C5.T[0][q] = (q == 0) ? 1 : q;
        C5.T[1][q] = (q + 1) % 5;
    }
    int eul5 = check_eulerian_and_floyd(&C5);
    int rt5 = exact_bitmask_bfs(&C5);
    if (eul5 != 0 || rt5 != 16) return 0;
    printf("[C-CALIB] Cerny C_5 (n=5, k=2): eulerian=%d (expected 0), rt=%d == 16\n", eul5, rt5);
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Usage: verify_c_bitmask <object.json>\nFAIL\n");
        return 1;
    }
    if (!run_c_calibrations()) {
        printf("[C-ERROR] Calibration failed\nFAIL\n");
        return 1;
    }
    FILE *fp = fopen(argv[1], "rb");
    if (!fp) {
        printf("[C-ERROR] Could not open file\nFAIL\n");
        return 1;
    }
    fseek(fp, 0, SEEK_END);
    long fsz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (fsz <= 0 || fsz > 1000000) {
        fclose(fp);
        printf("[C-ERROR] Invalid file size\nFAIL\n");
        return 1;
    }
    char *buf = (char *)malloc((size_t)fsz + 1);
    if (!buf || fread(buf, 1, (size_t)fsz, fp) != (size_t)fsz) {
        fclose(fp); free(buf);
        printf("[C-ERROR] Read error\nFAIL\n");
        return 1;
    }
    buf[fsz] = '\0';
    fclose(fp);

    if (!strstr(buf, "\"eulerian-synchronizing-szykula-vorel-bound\"")) {
        free(buf);
        printf("[C-ERROR] Missing or wrong target_id\nFAIL\n");
        return 1;
    }
    Automaton A;
    memset(&A, 0, sizeof(A));
    int claimed_bound = -1, claimed_rt = -1;
    if (!parse_int_after_key(buf, "\"n\"", &A.n) ||
        !parse_int_after_key(buf, "\"k\"", &A.k) ||
        !parse_int_after_key(buf, "\"szykula_vorel_bound\"", &claimed_bound) ||
        !parse_int_after_key(buf, "\"claimed_reset_threshold\"", &claimed_rt) ||
        !parse_transitions(buf, &A)) {
        free(buf);
        printf("[C-ERROR] JSON parse or dimension mismatch\nFAIL\n");
        return 1;
    }
    free(buf);

    int true_bound = (A.n * A.n - 3) / 2;
    if (claimed_bound != true_bound) {
        printf("[C-ERROR] Bound mismatch %d != %d\nFAIL\n", claimed_bound, true_bound);
        return 1;
    }
    if (!check_eulerian_and_floyd(&A)) {
        printf("[C-ERROR] Automaton failed Eulerian or strong-connectivity check\nFAIL\n");
        return 1;
    }
    if (!check_pair_sync(&A)) {
        printf("[C-ERROR] Automaton failed pair-synchronization check\nFAIL\n");
        return 1;
    }
    int rt = exact_bitmask_bfs(&A);
    if (rt != claimed_rt || rt <= true_bound) {
        printf("[C-ERROR] Exact BFS reset threshold %d (claimed %d, bound %d) failed\nFAIL\n",
               rt, claimed_rt, true_bound);
        return 1;
    }
    printf("[C-CHECK] Verified complete Eulerian synchronizing DFA: n=%d, k=%d, rt=%d > floor((%d^2-3)/2)=%d\n",
           A.n, A.k, rt, A.n, true_bound);
    printf("C_VERIFY_OK\n");
    return 0;
}
