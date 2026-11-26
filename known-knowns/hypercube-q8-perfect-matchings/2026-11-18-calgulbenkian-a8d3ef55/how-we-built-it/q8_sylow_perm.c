/*
 * Engine A1: Exact & Modular Bipartite Permanent for Hypercube Q_n (n=1..8),
 * Folded n-Cube FQ_n (n=2..6), and Stabilizer-Stratified Abelian Subgroup
 * Orbit-Quotient Fixed-Point Counts |Fix_{M(Q_n)}(P)|.
 *
 * Uses Glynn's Gray-code permanent formula in exact 128-bit arithmetic (__int128)
 * plus modular arithmetic mod M for overflow-proof verification on 32x32 matrices.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef __int128 i128;
typedef unsigned __int128 u128;

static void print_u128(u128 x) {
    if (x == 0) { putchar('0'); return; }
    char buf[64];
    int pos = 0;
    while (x > 0) {
        buf[pos++] = (char)('0' + (int)(x % 10));
        x /= 10;
    }
    while (pos > 0) putchar(buf[--pos]);
}

/* Exact Glynn permanent for m x m non-negative integer matrix A (m <= 32).
 * Glynn's formula:
 *   perm(A) = (1 / 2^(m-1)) * sum_{delta in {-1,+1}^m, delta_0 = +1}
 *             (prod_{j=0}^{m-1} delta_j) * prod_{i=0}^{m-1} sum_{j=0}^{m-1} delta_j A_{i,j}
 * Using Gray code on bits 1..m-1: each step flips one delta_k (+1 <-> -1),
 * updating row_sum[i] += 2 * delta_k_new * A[i][k].
 * If mod > 0, computes perm(A) mod mod (mod must be odd so 2^(m-1) is invertible!).
 * If mod == 0, computes exact u128 permanent (valid when sum of |prod| < 2^127).
 */
static uint64_t mod_pow(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1 % m;
    a %= m;
    while (e > 0) {
        if (e & 1) r = (uint64_t)(((u128)r * a) % m);
        a = (uint64_t)(((u128)a * a) % m);
        e >>= 1;
    }
    return r;
}

static u128 perm_glynn_exact(int m, const int A[36][36]) {
    if (m == 0) return 1;
    int64_t row[36];
    for (int i = 0; i < m; i++) {
        int64_t s = 0;
        for (int j = 0; j < m; j++) s += A[i][j];
        row[i] = s;
    }
    int delta[36];
    for (int j = 0; j < m; j++) delta[j] = 1;
    int sign = 1;

    i128 acc = 0;
    {
        i128 p = 1;
        for (int i = 0; i < m; i++) p *= row[i];
        acc += p;
    }

    uint64_t limit = (m == 1) ? 1ULL : (1ULL << (m - 1));
    uint64_t prev_gray = 0;
    for (uint64_t step = 1; step < limit; step++) {
        uint64_t gray = step ^ (step >> 1);
        uint64_t diff = gray ^ prev_gray;
        int k = __builtin_ctzll(diff) + 1; /* bit in 1..m-1 */
        prev_gray = gray;

        delta[k] = -delta[k];
        sign = -sign;
        int64_t d2 = 2LL * delta[k];
        i128 p = 1;
        for (int i = 0; i < m; i++) {
            row[i] += d2 * A[i][k];
            p *= row[i];
        }
        acc += (sign > 0) ? p : -p;
    }
    /* Divide by 2^(m-1) */
    if (acc < 0) {
        fprintf(stderr, "ERROR: negative permanent accumulator!\n");
        exit(2);
    }
    return ((u128)acc) >> (m - 1);
}

static uint64_t perm_glynn_mod(int m, const int A[36][36], uint64_t mod) {
    if (m == 0) return 1 % mod;
    int64_t row[36];
    for (int i = 0; i < m; i++) {
        int64_t s = 0;
        for (int j = 0; j < m; j++) s += A[i][j];
        row[i] = s;
    }
    int delta[36];
    for (int j = 0; j < m; j++) delta[j] = 1;
    int sign = 1;

    uint64_t acc = 0;
    {
        uint64_t p = 1;
        for (int i = 0; i < m; i++) {
            int64_t r = row[i] % (int64_t)mod;
            if (r < 0) r += (int64_t)mod;
            p = (uint64_t)(((u128)p * (uint64_t)r) % mod);
        }
        acc = p;
    }

    uint64_t limit = (m == 1) ? 1ULL : (1ULL << (m - 1));
    uint64_t prev_gray = 0;
    for (uint64_t step = 1; step < limit; step++) {
        uint64_t gray = step ^ (step >> 1);
        uint64_t diff = gray ^ prev_gray;
        int k = __builtin_ctzll(diff) + 1;
        prev_gray = gray;

        delta[k] = -delta[k];
        sign = -sign;
        int64_t d2 = 2LL * delta[k];
        uint64_t p = 1;
        for (int i = 0; i < m; i++) {
            row[i] += d2 * A[i][k];
            int64_t r = row[i] % (int64_t)mod;
            if (r < 0) r += (int64_t)mod;
            p = (uint64_t)(((u128)p * (uint64_t)r) % mod);
        }
        if (sign > 0) {
            acc += p;
            if (acc >= mod) acc -= mod;
        } else {
            acc = (acc >= p) ? (acc - p) : (acc + mod - p);
        }
    }
    /* Multiply by (2^(m-1))^(-1) mod mod (requires odd mod; use Fermat/Euler or extended GCD) */
    int64_t a = (int64_t)(1ULL << (m - 1)), b = (int64_t)mod;
    /* Compute inverse of 2 mod mod repeated m-1 times since mod is odd: inv2 = (mod + 1)/2 */
    uint64_t inv2 = (mod + 1) / 2;
    uint64_t inv = mod_pow(inv2, (uint64_t)(m - 1), mod);
    (void)a; (void)b;
    return (uint64_t)(((u128)acc * inv) % mod);
}

/* Represent a finite abelian coordinate-permutation group P <= S_8 (|P| <= 16) */
typedef struct {
    int order;
    int perms[16][8]; /* perms[g][coord] */
} Group;

static int apply_perm_vertex(const int perm[8], int n, int v) {
    int out = 0;
    for (int c = 0; c < n; c++) {
        if ((v >> c) & 1) {
            out |= (1 << perm[c]);
        }
    }
    return out;
}

static u128 count_fixed_matchings(int n, const Group *G, uint64_t mod_only) {
    int N = 1 << n;
    uint16_t stab_mask[256];
    int orbit_id[256];
    memset(orbit_id, -1, sizeof(orbit_id));

    for (int v = 0; v < N; v++) {
        uint16_t sm = 0;
        for (int g = 0; g < G->order; g++) {
            if (apply_perm_vertex(G->perms[g], n, v) == v) {
                sm |= (uint16_t)(1u << g);
            }
        }
        stab_mask[v] = sm;
    }

    /* Enumerate distinct stabilizer masks */
    uint16_t distinct_stabs[32];
    int num_stabs = 0;
    for (int v = 0; v < N; v++) {
        int found = 0;
        for (int s = 0; s < num_stabs; s++) {
            if (distinct_stabs[s] == stab_mask[v]) { found = 1; break; }
        }
        if (!found) distinct_stabs[num_stabs++] = stab_mask[v];
    }

    u128 total_exact = 1;
    uint64_t total_mod = 1 % (mod_only ? mod_only : 1);

    for (int s = 0; s < num_stabs; s++) {
        uint16_t sm = distinct_stabs[s];
        int even_reps[36], odd_reps[36];
        int even_orb_of_v[256], odd_orb_of_v[256];
        memset(even_orb_of_v, -1, sizeof(even_orb_of_v));
        memset(odd_orb_of_v, -1, sizeof(odd_orb_of_v));
        int ne = 0, no = 0;

        for (int v = 0; v < N; v++) {
            if (stab_mask[v] != sm) continue;
            int parity = __builtin_popcount((unsigned)v) & 1;
            if (!parity && even_orb_of_v[v] == -1) {
                int id = ne++;
                even_reps[id] = v;
                for (int g = 0; g < G->order; g++) {
                    int u = apply_perm_vertex(G->perms[g], n, v);
                    even_orb_of_v[u] = id;
                }
            } else if (parity && odd_orb_of_v[v] == -1) {
                int id = no++;
                odd_reps[id] = v;
                for (int g = 0; g < G->order; g++) {
                    int u = apply_perm_vertex(G->perms[g], n, v);
                    odd_orb_of_v[u] = id;
                }
            }
        }
        if (ne != no) return 0;
        if (ne > 35) {
            fprintf(stderr, "Stratum too large (%d > 35) for Glynn!\n", ne);
            exit(3);
        }
        int W[36][36];
        memset(W, 0, sizeof(W));
        for (int i = 0; i < ne; i++) {
            int u = even_reps[i];
            for (int bit = 0; bit < n; bit++) {
                int v = u ^ (1 << bit);
                if (stab_mask[v] == sm) {
                    int j = odd_orb_of_v[v];
                    W[i][j]++;
                }
            }
        }
        if (mod_only) {
            uint64_t pm = perm_glynn_mod(ne, W, mod_only);
            total_mod = (uint64_t)(((u128)total_mod * pm) % mod_only);
        } else {
            u128 pe = perm_glynn_exact(ne, W);
            total_exact *= pe;
        }
    }
    return mod_only ? (u128)total_mod : total_exact;
}

static Group make_cyclic_cycle(int len) {
    Group G;
    G.order = len;
    for (int g = 0; g < len; g++) {
        for (int c = 0; c < 8; c++) {
            G.perms[g][c] = (c < len) ? ((c + g) % len) : c;
        }
    }
    return G;
}

static Group make_sylow3_c3xc3(void) {
    Group G;
    G.order = 9;
    int idx = 0;
    for (int a = 0; a < 3; a++) {
        for (int b = 0; b < 3; b++) {
            for (int c = 0; c < 8; c++) {
                if (c < 3) G.perms[idx][c] = (c + a) % 3;
                else if (c < 6) G.perms[idx][c] = 3 + ((c - 3 + b) % 3);
                else G.perms[idx][c] = c;
            }
            idx++;
        }
    }
    return G;
}

static Group make_diag3(void) {
    Group G;
    G.order = 3;
    for (int a = 0; a < 3; a++) {
        for (int c = 0; c < 8; c++) {
            if (c < 3) G.perms[a][c] = (c + a) % 3;
            else if (c < 6) G.perms[a][c] = 3 + ((c - 3 + a) % 3);
            else G.perms[a][c] = c;
        }
    }
    return G;
}

int main(void) {
    printf("=== 1. Full Hypercube Q_n Exact Permanent (n = 1..6) ===\n");
    Group G_id = make_cyclic_cycle(1);
    for (int n = 1; n <= 6; n++) {
        u128 val = count_fixed_matchings(n, &G_id, 0);
        printf("Q_%d exact A005271(%d) = ", n, n);
        print_u128(val);
        printf(" (mod 3 = %llu, mod 5 = %llu, mod 7 = %llu)\n",
               (unsigned long long)(val % 3),
               (unsigned long long)(val % 5),
               (unsigned long long)(val % 7));
        fflush(stdout);
    }

    printf("\n=== 2. Folded Cube FQ_n Exact Permanent (even n = 2, 4, 6; bipartite) ===\n");
    for (int n = 2; n <= 6; n += 2) {
        /* FQ_n is Q_{n-1} plus antipodal edges {x, ~x}; bipartite since n-1 is odd! */
        int N = 1 << (n - 1);
        int mask_all = N - 1;
        int ev[36], od[36], id_of[128];
        int ne = 0, no = 0;
        for (int v = 0; v < N; v++) {
            if ((__builtin_popcount((unsigned)v) & 1) == 0) { id_of[v] = ne; ev[ne++] = v; }
            else { id_of[v] = no; od[no++] = v; }
        }
        int A[36][36];
        memset(A, 0, sizeof(A));
        for (int i = 0; i < ne; i++) {
            int u = ev[i];
            for (int bit = 0; bit < n - 1; bit++) {
                A[i][id_of[u ^ (1 << bit)]]++;
            }
            A[i][id_of[u ^ mask_all]]++; /* antipodal edge */
        }
        u128 val = perm_glynn_exact(ne, A);
        printf("FQ_%d (bipartite %dx%d) exact matchings = ", n, ne, ne);
        print_u128(val);
        printf("\n");
        fflush(stdout);
    }

    printf("\n=== 3. Sylow 5-Subgroup P_5 = <(0 1 2 3 4)> on Q_5..Q_8 ===\n");
    Group G5 = make_cyclic_cycle(5);
    for (int n = 5; n <= 8; n++) {
        u128 val = count_fixed_matchings(n, &G5, 0);
        uint64_t m1 = (uint64_t)count_fixed_matchings(n, &G5, 1000000007ULL);
        uint64_t m2 = (uint64_t)count_fixed_matchings(n, &G5, 1000000009ULL);
        printf("Q_%d |Fix(P_5)| = ", n);
        print_u128(val);
        printf(" | mod 5 = %llu | check_1e9+7=%llu (==%llu), check_1e9+9=%llu (==%llu)\n",
               (unsigned long long)(val % 5),
               (unsigned long long)(val % 1000000007ULL), (unsigned long long)m1,
               (unsigned long long)(val % 1000000009ULL), (unsigned long long)m2);
        fflush(stdout);
    }

    printf("\n=== 4. Sylow 7-Subgroup P_7 = <(0 1 2 3 4 5 6)> on Q_7..Q_8 ===\n");
    Group G7 = make_cyclic_cycle(7);
    for (int n = 7; n <= 8; n++) {
        u128 val = count_fixed_matchings(n, &G7, 0);
        printf("Q_%d |Fix(P_7)| = ", n);
        print_u128(val);
        printf(" | mod 7 = %llu\n", (unsigned long long)(val % 7));
        fflush(stdout);
    }

    printf("\n=== 5. Sylow 3-Subgroup P_3 = <(0 1 2),(3 4 5)> (C_3 x C_3) & Subgroups on Q_6..Q_8 ===\n");
    Group G3_syl = make_sylow3_c3xc3();
    Group G3_cyc = make_cyclic_cycle(3);
    Group G3_diag = make_diag3();
    for (int n = 6; n <= 8; n++) {
        u128 v_syl = count_fixed_matchings(n, &G3_syl, 0);
        printf("Q_%d |Fix(P_3 [C3xC3])| = ", n);
        print_u128(v_syl);
        printf(" | mod 3 = %llu, mod 9 = %llu\n",
               (unsigned long long)(v_syl % 3), (unsigned long long)(v_syl % 9));
        /* Also H_1 = <(0 1 2)>: for n <= 7 exact u128 fits easily; for n = 8, 32x32 weighted permanent
         * could exceed u128? Let's check with CRT mod 3 large odd primes + mod 9! */
        if (n <= 7) {
            u128 v_h1 = count_fixed_matchings(n, &G3_cyc, 0);
            u128 v_h3 = count_fixed_matchings(n, &G3_diag, 0);
            u128 mod9_comb = (2 * (v_h1 % 9) + 2 * (v_h3 % 9) + 9 - (3 * (v_syl % 9)) % 9) % 9;
            printf("Q_%d |Fix(H_1 <(012)>)| = ", n); print_u128(v_h1);
            printf(" (mod 3 = %llu, mod 9 = %llu)\n", (unsigned long long)(v_h1 % 3), (unsigned long long)(v_h1 % 9));
            printf("Q_%d |Fix(H_3 <(012)(345)>)| = ", n); print_u128(v_h3);
            printf(" (mod 3 = %llu, mod 9 = %llu)\n", (unsigned long long)(v_h3 % 3), (unsigned long long)(v_h3 % 9));
            printf("Q_%d Burnside-mod-9 formula (2|Fix(H_1)| + 2|Fix(H_3)| - 3|Fix(P_3)|) mod 9 = %llu\n",
                   n, (unsigned long long)mod9_comb);
        } else {
            /* P_3 [C3xC3] already printed above in <1ms! Also verify P_3 mod 1e9+7 and 1e9+9 */
            uint64_t m1 = (uint64_t)count_fixed_matchings(n, &G3_syl, 1000000007ULL);
            uint64_t m2 = (uint64_t)count_fixed_matchings(n, &G3_syl, 1000000009ULL);
            printf("Q_8 |Fix(P_3 [C3xC3])| modular cross-check: 1e9+7=%llu (==%llu), 1e9+9=%llu (==%llu)\n",
                   (unsigned long long)(v_syl % 1000000007ULL), (unsigned long long)m1,
                   (unsigned long long)(v_syl % 1000000009ULL), (unsigned long long)m2);
        }
        fflush(stdout);
    }
    return 0;
}
