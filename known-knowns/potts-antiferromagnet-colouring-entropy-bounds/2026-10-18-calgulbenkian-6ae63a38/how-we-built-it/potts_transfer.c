#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// Encode a proper q-colouring w[0..m-1] with w[0]=0, w[1]=1 as a base-(q-1) integer in [0, (q-1)^(m-2))
static inline uint64_t encode_norm(const uint8_t *w, int m, int q) {
    uint64_t code = 0;
    uint64_t base = (uint64_t)(q - 1);
    for (int p = 2; p < m; ++p) {
        uint8_t c = w[p];
        uint8_t prev = w[p - 1];
        uint8_t d = (c > prev) ? (uint8_t)(c - 1) : c;
        code = code * base + (uint64_t)d;
    }
    return code;
}

static inline void decode_norm(uint64_t code, uint8_t *w, int m, int q) {
    w[0] = 0;
    w[1] = 1;
    uint64_t base = (uint64_t)(q - 1);
    for (int p = m - 1; p >= 2; --p) {
        uint8_t d = (uint8_t)(code % base);
        code /= base;
        w[p] = d;
    }
    for (int p = 2; p < m; ++p) {
        if (w[p] >= w[p - 1]) w[p]++;
    }
}

// Canonicalize w[0..m-1] to Restricted Growth String (RGS) under S_q
static inline void canonicalize_s_q(const uint8_t *in, uint8_t *out, int m) {
    int8_t mp[8] = {-1, -1, -1, -1, -1, -1, -1, -1};
    uint8_t nxt = 0;
    for (int i = 0; i < m; ++i) {
        uint8_t c = in[i];
        if (mp[c] == -1) mp[c] = (int8_t)(nxt++);
        out[i] = (uint8_t)mp[c];
    }
}

// Mode 0: Cycle C_m (periodic, group S_q x D_m)
// Mode 1: Path P_m (open, group S_q x Z_2)
int build_potts_2d(int q, int m, int mode, const char *out_path) {
    uint64_t n_codes = 1;
    for (int p = 2; p < m; ++p) n_codes *= (uint64_t)(q - 1);

    int32_t *state_to_orb = (int32_t *)malloc(n_codes * sizeof(int32_t));
    for (uint64_t c = 0; c < n_codes; ++c) state_to_orb[c] = -1;

    uint32_t cap_orbs = (uint32_t)(n_codes / 2ULL + 1024ULL);
    uint64_t *rep_codes = (uint64_t *)malloc(cap_orbs * sizeof(uint64_t));
    uint32_t *orb_sizes = (uint32_t *)malloc(cap_orbs * sizeof(uint32_t));
    uint32_t n_orb = 0;
    uint64_t n_valid_norm = 0;

    // Generate all 24 or 120 permutations of {2, ..., q-1} fixing 0 and 1
    uint8_t perms[6][8];
    int n_sub_perms = 1;
    if (q == 3) {
        n_sub_perms = 1;
        perms[0][0] = 0; perms[0][1] = 1; perms[0][2] = 2;
    } else if (q == 4) {
        n_sub_perms = 2;
        perms[0][0] = 0; perms[0][1] = 1; perms[0][2] = 2; perms[0][3] = 3;
        perms[1][0] = 0; perms[1][1] = 1; perms[1][2] = 3; perms[1][3] = 2;
    } else if (q == 5) {
        n_sub_perms = 6;
        const uint8_t p3[6][3] = {
            {2,3,4}, {2,4,3}, {3,2,4}, {3,4,2}, {4,2,3}, {4,3,2}
        };
        for (int s = 0; s < 6; ++s) {
            perms[s][0] = 0; perms[s][1] = 1;
            perms[s][2] = p3[s][0]; perms[s][3] = p3[s][1]; perms[s][4] = p3[s][2];
        }
    }

    uint8_t w[32], rot[32], rev[32], rgs[32], permed[32];

    for (uint64_t code = 0; code < n_codes; ++code) {
        decode_norm(code, w, m, q);
        if (mode == 0 && w[m - 1] == w[0]) continue;
        n_valid_norm++;
        if (state_to_orb[code] != -1) continue;

        uint32_t orbit_id = n_orb++;
        rep_codes[orbit_id] = code;
        uint32_t sz = 0;

        int n_rot = (mode == 0) ? m : 1;
        for (int r = 0; r < n_rot; ++r) {
            for (int i = 0; i < m; ++i) rot[i] = w[(i + r) % m];
            canonicalize_s_q(rot, rgs, m);
            for (int s = 0; s < n_sub_perms; ++s) {
                for (int i = 0; i < m; ++i) permed[i] = perms[s][rgs[i]];
                uint64_t c_id = encode_norm(permed, m, q);
                if (state_to_orb[c_id] == -1) { state_to_orb[c_id] = (int32_t)orbit_id; sz++; }
            }
            for (int i = 0; i < m; ++i) rev[i] = rot[m - 1 - i];
            canonicalize_s_q(rev, rgs, m);
            for (int s = 0; s < n_sub_perms; ++s) {
                for (int i = 0; i < m; ++i) permed[i] = perms[s][rgs[i]];
                uint64_t c_id = encode_norm(permed, m, q);
                if (state_to_orb[c_id] == -1) { state_to_orb[c_id] = (int32_t)orbit_id; sz++; }
            }
        }
        orb_sizes[orbit_id] = sz;
    }

    uint32_t *row_ptr = (uint32_t *)calloc(n_orb + 1, sizeof(uint32_t));
    uint64_t cap = (uint64_t)n_orb * 64ULL + 1024ULL;
    uint32_t *col_idx = (uint32_t *)malloc(cap * sizeof(uint32_t));
    uint32_t *val = (uint32_t *)malloc(cap * sizeof(uint32_t));
    uint64_t nnz = 0;

    uint32_t *row_acc = (uint32_t *)calloc(n_orb, sizeof(uint32_t));
    uint32_t *touched = (uint32_t *)malloc(n_orb * sizeof(uint32_t));

    uint8_t u_col[32], u_hat[32];
    uint64_t base = (uint64_t)(q - 1);

    for (uint32_t i = 0; i < n_orb; ++i) {
        decode_norm(rep_codes[i], u_col, m, q);
        uint32_t n_touched = 0;

        // Loop over all valid pairs (v0, v1) with v0 != u_col[0], v1 != u_col[1], v0 != v1
        for (uint8_t v0 = 0; v0 < (uint8_t)q; ++v0) {
            if (v0 == u_col[0]) continue;
            for (uint8_t v1 = 0; v1 < (uint8_t)q; ++v1) {
                if (v1 == u_col[1] || v1 == v0) continue;

                // Build bijection tau mapping v0 -> 0, v1 -> 1, and remaining colours in order to 2..q-1
                uint8_t tau[8];
                tau[v0] = 0;
                tau[v1] = 1;
                uint8_t nxt = 2;
                for (uint8_t c = 0; c < (uint8_t)q; ++c) {
                    if (c != v0 && c != v1) tau[c] = nxt++;
                }
                for (int p = 0; p < m; ++p) u_hat[p] = tau[u_col[p]];

                // Iterative DFS over p = 2 .. m-1 in normalized coordinates (v_hat[0]=0, v_hat[1]=1)
                uint32_t stack_pos[128];
                uint8_t stack_prev[128];
                uint64_t stack_code[128];
                int sp = 0;
                stack_pos[sp] = 2;
                stack_prev[sp] = 1;
                stack_code[sp] = 0;
                sp++;

                while (sp > 0) {
                    sp--;
                    uint32_t pos = stack_pos[sp];
                    uint8_t prev = stack_prev[sp];
                    uint64_t code = stack_code[sp];

                    if (pos == (uint32_t)m) {
                        uint32_t j = (uint32_t)state_to_orb[code];
                        if (row_acc[j] == 0) {
                            touched[n_touched++] = j;
                        }
                        row_acc[j]++;
                        continue;
                    }

                    uint8_t forbid_u = u_hat[pos];
                    for (uint8_t c = 0; c < (uint8_t)q; ++c) {
                        if (c == prev || c == forbid_u) continue;
                        if (mode == 0 && pos == (uint32_t)(m - 1) && c == 0) continue; // c != v_hat[0] == 0
                        uint8_t d = (c > prev) ? (uint8_t)(c - 1) : c;
                        stack_pos[sp] = pos + 1;
                        stack_prev[sp] = c;
                        stack_code[sp] = code * base + (uint64_t)d;
                        sp++;
                    }
                }
            }
        }

        if (nnz + n_touched > cap) {
            cap = (nnz + n_touched) * 2ULL;
            col_idx = (uint32_t *)realloc(col_idx, cap * sizeof(uint32_t));
            val = (uint32_t *)realloc(val, cap * sizeof(uint32_t));
        }
        for (uint32_t t = 0; t < n_touched; ++t) {
            uint32_t j = touched[t];
            col_idx[nnz] = j;
            val[nnz] = row_acc[j];
            row_acc[j] = 0;
            nnz++;
        }
        row_ptr[i + 1] = (uint32_t)nnz;
    }

    uint32_t nnz32 = (uint32_t)nnz;
    FILE *f = fopen(out_path, "wb");
    if (!f) return -1;
    fwrite(&n_orb, sizeof(uint32_t), 1, f);
    fwrite(&nnz32, sizeof(uint32_t), 1, f);
    fwrite(orb_sizes, sizeof(uint32_t), n_orb, f);
    fwrite(row_ptr, sizeof(uint32_t), n_orb + 1, f);
    fwrite(col_idx, sizeof(uint32_t), nnz32, f);
    fwrite(val, sizeof(uint32_t), nnz32, f);
    fclose(f);

    printf("Built Potts q=%d mode=%d m=%2d: N1=%9llu, N3(orbits)=%6u, nnz=%9u -> %s\n",
           q, mode, m, (unsigned long long)(n_valid_norm * (uint64_t)q * (uint64_t)(q - 1)),
           n_orb, nnz32, out_path);

    free(state_to_orb); free(rep_codes); free(orb_sizes);
    free(row_ptr); free(col_idx); free(val); free(row_acc); free(touched);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s <q> <mode:0=cyl,1=open> <m> <out_path>\n", argv[0]);
        return 1;
    }
    int q = atoi(argv[1]);
    int mode = atoi(argv[2]);
    int m = atoi(argv[3]);
    return build_potts_2d(q, m, mode, argv[4]);
}
