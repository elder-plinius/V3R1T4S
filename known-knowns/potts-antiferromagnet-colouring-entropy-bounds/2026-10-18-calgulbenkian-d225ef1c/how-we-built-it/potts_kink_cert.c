#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef unsigned __int128 u128;

typedef struct {
    uint64_t w[4];
} u256;

typedef struct {
    uint64_t w[8];
} u512;

static inline u256 u256_zero(void) {
    u256 r = {{0, 0, 0, 0}};
    return r;
}

static inline void u256_add_into(u256 *r, const u256 *a) {
    u128 carry = 0;
    for (int k = 0; k < 4; ++k) {
        u128 s = (u128)r->w[k] + (u128)a->w[k] + carry;
        r->w[k] = (uint64_t)s;
        carry = s >> 64;
    }
}

static inline void u256_add_mul32(u256 *r, const u256 *a, uint32_t m) {
    u128 carry = 0;
    for (int k = 0; k < 4; ++k) {
        u128 prod = (u128)a->w[k] * (u128)m + (u128)r->w[k] + carry;
        r->w[k] = (uint64_t)prod;
        carry = prod >> 64;
    }
}

static inline u256 u256_shr(const u256 *a, int sh) {
    u256 r;
    if (sh == 0) return *a;
    r.w[0] = (a->w[0] >> sh) | (a->w[1] << (64 - sh));
    r.w[1] = (a->w[1] >> sh) | (a->w[2] << (64 - sh));
    r.w[2] = (a->w[2] >> sh) | (a->w[3] << (64 - sh));
    r.w[3] = (a->w[3] >> sh);
    return r;
}

static inline int u256_top_bit_in_w3(uint64_t w3) {
    if (w3 == 0) return 0;
    return 64 - __builtin_clzll(w3);
}

static inline u512 u256_mul(const u256 *a, const u256 *b) {
    u512 r;
    memset(&r, 0, sizeof(r));
    for (int i = 0; i < 4; ++i) {
        u128 carry = 0;
        for (int j = 0; j < 4; ++j) {
            u128 prod = (u128)a->w[i] * (u128)b->w[j] + (u128)r.w[i + j] + carry;
            r.w[i + j] = (uint64_t)prod;
            carry = prod >> 64;
        }
        r.w[i + 4] = (uint64_t)carry;
    }
    return r;
}

static inline int u512_cmp(const u512 *a, const u512 *b) {
    for (int k = 7; k >= 0; --k) {
        if (a->w[k] < b->w[k]) return -1;
        if (a->w[k] > b->w[k]) return 1;
    }
    return 0;
}

static inline int ratio_cmp(const u256 *y1, const u256 *v1, const u256 *y2, const u256 *v2) {
    u512 lhs = u256_mul(y1, v2);
    u512 rhs = u256_mul(y2, v1);
    return u512_cmp(&lhs, &rhs);
}

static void print_u256_hex(const u256 *a) {
    printf("0x%016llx%016llx%016llx%016llx",
           (unsigned long long)a->w[3],
           (unsigned long long)a->w[2],
           (unsigned long long)a->w[1],
           (unsigned long long)a->w[0]);
}

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

static inline uint64_t encode_y_seq(const uint8_t *y, int m, int q) {
    uint64_t B = (uint64_t)(q - 1);
    uint64_t pref = 0;
    for (int r = 2; r <= m - 2; ++r) {
        uint8_t yr = y[r];
        uint8_t yn = y[r + 1];
        uint8_t d = (yr > yn) ? (uint8_t)(yr - 1) : yr;
        pref = pref * B + (uint64_t)d;
    }
    return pref * (uint64_t)q + (uint64_t)y[m - 1];
}

static inline void canonicalize_s_q(const uint8_t *in, uint8_t *out, int m) {
    int8_t mp[8] = {-1, -1, -1, -1, -1, -1, -1, -1};
    uint8_t nxt = 0;
    for (int i = 0; i < m; ++i) {
        uint8_t c = in[i];
        if (mp[c] == -1) mp[c] = (int8_t)(nxt++);
        out[i] = (uint8_t)mp[c];
    }
}

typedef struct {
    int q;
    int m;
    int mode;
    uint64_t B;
    uint64_t n_codes;
    uint64_t n_mid;
    uint64_t n_final;
    uint64_t n_valid_norm;
    uint32_t n_orb;
    int n_pairs;
    int32_t *state_to_orb;
    uint64_t *rep_codes;
    uint32_t *orb_sizes;
    uint32_t *orb_gather; // size n_orb * n_pairs
} KinkContext;

static void build_kink_context(KinkContext *ctx, int q, int m, int mode) {
    ctx->q = q;
    ctx->m = m;
    ctx->mode = mode;
    uint64_t B = (uint64_t)(q - 1);
    ctx->B = B;

    uint64_t n_codes = 1;
    for (int p = 2; p < m; ++p) n_codes *= B;
    ctx->n_codes = n_codes;

    uint64_t bm4 = 1;
    for (int p = 0; p < m - 4; ++p) bm4 *= B;
    ctx->n_mid = (uint64_t)q * (uint64_t)q * bm4;
    ctx->n_final = (uint64_t)q * bm4 * B;

    int32_t *state_to_orb = (int32_t *)malloc(n_codes * sizeof(int32_t));
    for (uint64_t c = 0; c < n_codes; ++c) state_to_orb[c] = -1;

    uint32_t cap_orbs = (uint32_t)(n_codes / 2ULL + 1024ULL);
    uint64_t *rep_codes = (uint64_t *)malloc(cap_orbs * sizeof(uint64_t));
    uint32_t *orb_sizes = (uint32_t *)malloc(cap_orbs * sizeof(uint32_t));
    uint32_t n_orb = 0;
    uint64_t n_valid_norm = 0;

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

    ctx->n_valid_norm = n_valid_norm;
    ctx->n_orb = n_orb;
    ctx->state_to_orb = state_to_orb;
    ctx->rep_codes = rep_codes;
    ctx->orb_sizes = orb_sizes;

    int n_pairs = q * q - 3 * q + 3;
    ctx->n_pairs = n_pairs;
    uint32_t *orb_gather = (uint32_t *)malloc((uint64_t)n_orb * (uint64_t)n_pairs * sizeof(uint32_t));

    uint8_t u_col[32], y_seq[32];
    for (uint32_t i = 0; i < n_orb; ++i) {
        decode_norm(rep_codes[i], u_col, m, q);
        int pidx = 0;
        for (uint8_t v0 = 0; v0 < (uint8_t)q; ++v0) {
            if (v0 == 0) continue;
            for (uint8_t v1 = 0; v1 < (uint8_t)q; ++v1) {
                if (v1 == 1 || v1 == v0) continue;
                uint8_t tau[8];
                tau[v0] = 0;
                tau[v1] = 1;
                uint8_t nxt = 2;
                for (uint8_t c = 0; c < (uint8_t)q; ++c) {
                    if (c != v0 && c != v1) tau[c] = nxt++;
                }
                for (int p = 2; p < m; ++p) y_seq[p] = tau[u_col[p]];
                orb_gather[(uint64_t)i * (uint64_t)n_pairs + (uint64_t)pidx] = (uint32_t)encode_y_seq(y_seq, m, q);
                pidx++;
            }
        }
    }
    ctx->orb_gather = orb_gather;
}

static void kink_matvec_double(const KinkContext *ctx, const double *v, double *out, double *bufA, double *bufB) {
    int q = ctx->q;
    int m = ctx->m;
    uint64_t B = ctx->B;
    uint64_t n_mid = ctx->n_mid;
    uint64_t n_final = ctx->n_final;

    // Step s = 2: accumulate from state_to_orb into bufA (size n_mid = q^2 * B^(m-4))
    memset(bufA, 0, n_mid * sizeof(double));
    uint64_t R2 = 1;
    for (int p = 0; p < m - 4; ++p) R2 *= B;

    for (uint64_t d2 = 0; d2 < B; ++d2) {
        uint8_t w2 = (d2 >= 1) ? (uint8_t)(d2 + 1) : (uint8_t)d2;
        for (uint64_t d3 = 0; d3 < B; ++d3) {
            uint8_t w3 = (d3 >= w2) ? (uint8_t)(d3 + 1) : (uint8_t)d3;
            uint64_t code_base = (d2 * B + d3) * R2;
            for (uint64_t rem = 0; rem < R2; ++rem) {
                int32_t orb = ctx->state_to_orb[code_base + rem];
                if (orb < 0) continue;
                double val = v[orb];
                for (int y2 = 0; y2 < q; ++y2) {
                    if (y2 == (int)w2) continue;
                    uint64_t dst_idx = ((uint64_t)y2 * (uint64_t)q + (uint64_t)w3) * R2 + rem;
                    bufA[dst_idx] += val;
                }
            }
        }
    }

    double *cur = bufA;
    double *nxt = bufB;

    // Steps s = 3 .. m - 2
    uint64_t Ps = 1;
    uint64_t Rs = R2;
    for (int s = 3; s <= m - 2; ++s) {
        Rs /= B;
        memset(nxt, 0, n_mid * sizeof(double));
        for (uint64_t pref = 0; pref < Ps; ++pref) {
            for (int ys1 = 0; ys1 < q; ++ys1) {
                for (int ws = 0; ws < q; ++ws) {
                    for (uint64_t ds1 = 0; ds1 < B; ++ds1) {
                        int ws1 = (ds1 >= (uint64_t)ws) ? (int)(ds1 + 1) : (int)ds1;
                        uint64_t src_base = ((((pref * (uint64_t)q + (uint64_t)ys1) * (uint64_t)q + (uint64_t)ws) * B) + ds1) * Rs;
                        for (int ys = 0; ys < q; ++ys) {
                            if (ys == ys1 || ys == ws) continue;
                            uint64_t dy = (ys1 > ys) ? (uint64_t)(ys1 - 1) : (uint64_t)ys1;
                            uint64_t pref_new = pref * B + dy;
                            uint64_t dst_base = ((pref_new * (uint64_t)q + (uint64_t)ys) * (uint64_t)q + (uint64_t)ws1) * Rs;
                            const double *src_ptr = cur + src_base;
                            double *dst_ptr = nxt + dst_base;
                            for (uint64_t rem = 0; rem < Rs; ++rem) {
                                dst_ptr[rem] += src_ptr[rem];
                            }
                        }
                    }
                }
            }
        }
        Ps *= B;
        double *tmp = cur; cur = nxt; nxt = tmp;
    }

    // Step s = m - 1: cur has size Ps * q * q = n_mid, nxt has size n_final = Ps * B * q
    memset(nxt, 0, n_final * sizeof(double));
    for (uint64_t pref = 0; pref < Ps; ++pref) {
        for (int ym2 = 0; ym2 < q; ++ym2) {
            for (int wm1 = 0; wm1 < q; ++wm1) {
                double val = cur[(pref * (uint64_t)q + (uint64_t)ym2) * (uint64_t)q + (uint64_t)wm1];
                if (val == 0.0) continue;
                for (int ym1 = 0; ym1 < q; ++ym1) {
                    if (ym1 == ym2 || ym1 == wm1) continue;
                    uint64_t dy = (ym2 > ym1) ? (uint64_t)(ym2 - 1) : (uint64_t)ym2;
                    uint64_t pref_new = pref * B + dy;
                    nxt[pref_new * (uint64_t)q + (uint64_t)ym1] += val;
                }
            }
        }
    }

    int n_pairs = ctx->n_pairs;
    for (uint32_t i = 0; i < ctx->n_orb; ++i) {
        double sum = 0.0;
        const uint32_t *g = ctx->orb_gather + (uint64_t)i * (uint64_t)n_pairs;
        for (int p = 0; p < n_pairs; ++p) {
            sum += nxt[g[p]];
        }
        out[i] = sum;
    }
}

static void kink_matvec_u256(const KinkContext *ctx, const u256 *v, u256 *out, u256 *bufA, u256 *bufB) {
    int q = ctx->q;
    int m = ctx->m;
    uint64_t B = ctx->B;
    uint64_t n_mid = ctx->n_mid;
    uint64_t n_final = ctx->n_final;

    memset(bufA, 0, n_mid * sizeof(u256));
    uint64_t R2 = 1;
    for (int p = 0; p < m - 4; ++p) R2 *= B;

    for (uint64_t d2 = 0; d2 < B; ++d2) {
        uint8_t w2 = (d2 >= 1) ? (uint8_t)(d2 + 1) : (uint8_t)d2;
        for (uint64_t d3 = 0; d3 < B; ++d3) {
            uint8_t w3 = (d3 >= w2) ? (uint8_t)(d3 + 1) : (uint8_t)d3;
            uint64_t code_base = (d2 * B + d3) * R2;
            for (uint64_t rem = 0; rem < R2; ++rem) {
                int32_t orb = ctx->state_to_orb[code_base + rem];
                if (orb < 0) continue;
                u256 val = v[orb];
                for (int y2 = 0; y2 < q; ++y2) {
                    if (y2 == (int)w2) continue;
                    uint64_t dst_idx = ((uint64_t)y2 * (uint64_t)q + (uint64_t)w3) * R2 + rem;
                    u256_add_into(&bufA[dst_idx], &val);
                }
            }
        }
    }

    u256 *cur = bufA;
    u256 *nxt = bufB;

    uint64_t Ps = 1;
    uint64_t Rs = R2;
    for (int s = 3; s <= m - 2; ++s) {
        Rs /= B;
        memset(nxt, 0, n_mid * sizeof(u256));
        for (uint64_t pref = 0; pref < Ps; ++pref) {
            for (int ys1 = 0; ys1 < q; ++ys1) {
                for (int ws = 0; ws < q; ++ws) {
                    for (uint64_t ds1 = 0; ds1 < B; ++ds1) {
                        int ws1 = (ds1 >= (uint64_t)ws) ? (int)(ds1 + 1) : (int)ds1;
                        uint64_t src_base = ((((pref * (uint64_t)q + (uint64_t)ys1) * (uint64_t)q + (uint64_t)ws) * B) + ds1) * Rs;
                        for (int ys = 0; ys < q; ++ys) {
                            if (ys == ys1 || ys == ws) continue;
                            uint64_t dy = (ys1 > ys) ? (uint64_t)(ys1 - 1) : (uint64_t)ys1;
                            uint64_t pref_new = pref * B + dy;
                            uint64_t dst_base = ((pref_new * (uint64_t)q + (uint64_t)ys) * (uint64_t)q + (uint64_t)ws1) * Rs;
                            const u256 *src_ptr = cur + src_base;
                            u256 *dst_ptr = nxt + dst_base;
                            for (uint64_t rem = 0; rem < Rs; ++rem) {
                                u256_add_into(&dst_ptr[rem], &src_ptr[rem]);
                            }
                        }
                    }
                }
            }
        }
        Ps *= B;
        u256 *tmp = cur; cur = nxt; nxt = tmp;
    }

    memset(nxt, 0, n_final * sizeof(u256));
    for (uint64_t pref = 0; pref < Ps; ++pref) {
        for (int ym2 = 0; ym2 < q; ++ym2) {
            for (int wm1 = 0; wm1 < q; ++wm1) {
                u256 val = cur[(pref * (uint64_t)q + (uint64_t)ym2) * (uint64_t)q + (uint64_t)wm1];
                if (val.w[0] == 0 && val.w[1] == 0 && val.w[2] == 0 && val.w[3] == 0) continue;
                for (int ym1 = 0; ym1 < q; ++ym1) {
                    if (ym1 == ym2 || ym1 == wm1) continue;
                    uint64_t dy = (ym2 > ym1) ? (uint64_t)(ym2 - 1) : (uint64_t)ym2;
                    uint64_t pref_new = pref * B + dy;
                    u256_add_into(&nxt[pref_new * (uint64_t)q + (uint64_t)ym1], &val);
                }
            }
        }
    }

    int n_pairs = ctx->n_pairs;
    for (uint32_t i = 0; i < ctx->n_orb; ++i) {
        u256 sum = u256_zero();
        const uint32_t *g = ctx->orb_gather + (uint64_t)i * (uint64_t)n_pairs;
        for (int p = 0; p < n_pairs; ++p) {
            u256_add_into(&sum, &nxt[g[p]]);
        }
        out[i] = sum;
    }
}

static void kink_matvec_u128(const KinkContext *ctx, const u128 *v, u128 *out, u128 *bufA, u128 *bufB) {
    int q = ctx->q;
    int m = ctx->m;
    uint64_t B = ctx->B;
    uint64_t n_mid = ctx->n_mid;
    uint64_t n_final = ctx->n_final;

    memset(bufA, 0, n_mid * sizeof(u128));
    uint64_t R2 = 1;
    for (int p = 0; p < m - 4; ++p) R2 *= B;

    for (uint64_t d2 = 0; d2 < B; ++d2) {
        uint8_t w2 = (d2 >= 1) ? (uint8_t)(d2 + 1) : (uint8_t)d2;
        for (uint64_t d3 = 0; d3 < B; ++d3) {
            uint8_t w3 = (d3 >= w2) ? (uint8_t)(d3 + 1) : (uint8_t)d3;
            uint64_t code_base = (d2 * B + d3) * R2;
            for (uint64_t rem = 0; rem < R2; ++rem) {
                int32_t orb = ctx->state_to_orb[code_base + rem];
                if (orb < 0) continue;
                u128 val = v[orb];
                for (int y2 = 0; y2 < q; ++y2) {
                    if (y2 == (int)w2) continue;
                    uint64_t dst_idx = ((uint64_t)y2 * (uint64_t)q + (uint64_t)w3) * R2 + rem;
                    bufA[dst_idx] += val;
                }
            }
        }
    }

    u128 *cur = bufA;
    u128 *nxt = bufB;

    uint64_t Ps = 1;
    uint64_t Rs = R2;
    for (int s = 3; s <= m - 2; ++s) {
        Rs /= B;
        memset(nxt, 0, n_mid * sizeof(u128));
        for (uint64_t pref = 0; pref < Ps; ++pref) {
            for (int ys1 = 0; ys1 < q; ++ys1) {
                for (int ws = 0; ws < q; ++ws) {
                    for (uint64_t ds1 = 0; ds1 < B; ++ds1) {
                        int ws1 = (ds1 >= (uint64_t)ws) ? (int)(ds1 + 1) : (int)ds1;
                        uint64_t src_base = ((((pref * (uint64_t)q + (uint64_t)ys1) * (uint64_t)q + (uint64_t)ws) * B) + ds1) * Rs;
                        for (int ys = 0; ys < q; ++ys) {
                            if (ys == ys1 || ys == ws) continue;
                            uint64_t dy = (ys1 > ys) ? (uint64_t)(ys1 - 1) : (uint64_t)ys1;
                            uint64_t pref_new = pref * B + dy;
                            uint64_t dst_base = ((pref_new * (uint64_t)q + (uint64_t)ys) * (uint64_t)q + (uint64_t)ws1) * Rs;
                            const u128 *src_ptr = cur + src_base;
                            u128 *dst_ptr = nxt + dst_base;
                            for (uint64_t rem = 0; rem < Rs; ++rem) {
                                dst_ptr[rem] += src_ptr[rem];
                            }
                        }
                    }
                }
            }
        }
        Ps *= B;
        u128 *tmp = cur; cur = nxt; nxt = tmp;
    }

    memset(nxt, 0, n_final * sizeof(u128));
    for (uint64_t pref = 0; pref < Ps; ++pref) {
        for (int ym2 = 0; ym2 < q; ++ym2) {
            for (int wm1 = 0; wm1 < q; ++wm1) {
                u128 val = cur[(pref * (uint64_t)q + (uint64_t)ym2) * (uint64_t)q + (uint64_t)wm1];
                if (val == 0) continue;
                for (int ym1 = 0; ym1 < q; ++ym1) {
                    if (ym1 == ym2 || ym1 == wm1) continue;
                    uint64_t dy = (ym2 > ym1) ? (uint64_t)(ym2 - 1) : (uint64_t)ym2;
                    uint64_t pref_new = pref * B + dy;
                    nxt[pref_new * (uint64_t)q + (uint64_t)ym1] += val;
                }
            }
        }
    }

    int n_pairs = ctx->n_pairs;
    for (uint32_t i = 0; i < ctx->n_orb; ++i) {
        u128 sum = 0;
        const uint32_t *g = ctx->orb_gather + (uint64_t)i * (uint64_t)n_pairs;
        for (int p = 0; p < n_pairs; ++p) {
            sum += nxt[g[p]];
        }
        out[i] = sum;
    }
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <q> <mode:0=cyl,1=open> <m> [n_iters_u256] [save_cert_path]\n", argv[0]);
        return 1;
    }
    int q = atoi(argv[1]);
    int mode = atoi(argv[2]);
    int m = atoi(argv[3]);
    int n_iters = (argc >= 5) ? atoi(argv[4]) : 80;
    const char *save_cert = (argc >= 6) ? argv[5] : NULL;

    if (m < 4) {
        fprintf(stderr, "potts_kink_cert requires m >= 4\n");
        return 1;
    }

    KinkContext ctx;
    build_kink_context(&ctx, q, m, mode);

    uint32_t n_orb = ctx.n_orb;
    uint64_t buf_sz = (ctx.n_mid > ctx.n_final) ? ctx.n_mid : ctx.n_final;

    double *vf = (double *)malloc(n_orb * sizeof(double));
    double *nf = (double *)malloc(n_orb * sizeof(double));
    double *bufA_f = (double *)malloc(buf_sz * sizeof(double));
    double *bufB_f = (double *)malloc(buf_sz * sizeof(double));

    for (uint32_t i = 0; i < n_orb; ++i) vf[i] = 1.0;
    double est_lam = 1.0;
    for (int it = 0; it < 35; ++it) {
        kink_matvec_double(&ctx, vf, nf, bufA_f, bufB_f);
        est_lam = nf[0] / vf[0];
        double inv = 1.0 / nf[0];
        for (uint32_t i = 0; i < n_orb; ++i) vf[i] = nf[i] * inv;
    }
    free(bufA_f); free(bufB_f);

    uint32_t shift_s = (uint32_t)(0.20 * est_lam) + 1U;

    // Stage 2: 50 native u128 iterations (converges from 53 bits to ~104 bits)
    u128 *v128 = (u128 *)malloc(n_orb * sizeof(u128));
    u128 *nv128 = (u128 *)malloc(n_orb * sizeof(u128));
    u128 *bufA_128 = (u128 *)malloc(buf_sz * sizeof(u128));
    u128 *bufB_128 = (u128 *)malloc(buf_sz * sizeof(u128));

    for (uint32_t i = 0; i < n_orb; ++i) {
        uint64_t init_w = (uint64_t)(vf[i] * (double)(1ULL << 52));
        if (init_w == 0) init_w = 1;
        v128[i] = ((u128)init_w) << 44;
    }
    free(vf); free(nf);

    for (int it = 0; it < 50; ++it) {
        kink_matvec_u128(&ctx, v128, nv128, bufA_128, bufB_128);
        uint64_t max_hi = 0;
        for (uint32_t i = 0; i < n_orb; ++i) {
            nv128[i] += v128[i] * (u128)shift_s;
            uint64_t hi = (uint64_t)(nv128[i] >> 64);
            if (hi > max_hi) max_hi = hi;
        }
        int top_bits = u256_top_bit_in_w3(max_hi);
        int sh = (top_bits > 32) ? (top_bits - 32) : 0;
        for (uint32_t i = 0; i < n_orb; ++i) {
            v128[i] = (sh > 0) ? (nv128[i] >> sh) : nv128[i];
            if (v128[i] == 0) v128[i] = 1;
        }
    }
    free(bufA_128); free(bufB_128); free(nv128);

    // Stage 3: n_iters u256 iterations (converges from ~104 bits to ~212 bits)
    u256 *v = (u256 *)malloc(n_orb * sizeof(u256));
    u256 *nv = (u256 *)malloc(n_orb * sizeof(u256));
    for (uint32_t i = 0; i < n_orb; ++i) {
        v[i].w[0] = 0;
        v[i].w[1] = 0;
        v[i].w[2] = (uint64_t)v128[i];
        v[i].w[3] = (uint64_t)(v128[i] >> 64);
        if (v[i].w[2] == 0 && v[i].w[3] == 0) v[i].w[2] = 1;
    }
    free(v128);

    u256 *bufA = (u256 *)malloc(buf_sz * sizeof(u256));
    u256 *bufB = (u256 *)malloc(buf_sz * sizeof(u256));

    for (int it = 0; it < n_iters; ++it) {
        kink_matvec_u256(&ctx, v, nv, bufA, bufB);
        uint64_t max_w3 = 0;
        for (uint32_t i = 0; i < n_orb; ++i) {
            u256_add_mul32(&nv[i], &v[i], shift_s);
            if (nv[i].w[3] > max_w3) max_w3 = nv[i].w[3];
        }
        int top_bits = u256_top_bit_in_w3(max_w3);
        int sh = (top_bits > 32) ? (top_bits - 32) : 0;
        for (uint32_t i = 0; i < n_orb; ++i) {
            v[i] = (sh > 0) ? u256_shr(&nv[i], sh) : nv[i];
            if (v[i].w[0] == 0 && v[i].w[1] == 0 && v[i].w[2] == 0 && v[i].w[3] == 0) {
                v[i].w[0] = 1;
            }
        }
    }

    // Final unshifted y = M * v in exact 256-bit arithmetic
    kink_matvec_u256(&ctx, v, nv, bufA, bufB);

    if (save_cert) {
        FILE *fc = fopen(save_cert, "wb");
        if (fc) {
            fwrite(&n_orb, sizeof(uint32_t), 1, fc);
            fwrite(v, sizeof(u256), n_orb, fc);
            fwrite(nv, sizeof(u256), n_orb, fc);
            fclose(fc);
        }
    }

    uint32_t min_idx = 0, max_idx = 0;
    u256 min_y = nv[0], min_v = v[0];
    u256 max_y = nv[0], max_v = v[0];

    for (uint32_t i = 1; i < n_orb; ++i) {
        if (ratio_cmp(&nv[i], &v[i], &min_y, &min_v) < 0) {
            min_y = nv[i];
            min_v = v[i];
            min_idx = i;
        }
        if (ratio_cmp(&nv[i], &v[i], &max_y, &max_v) > 0) {
            max_y = nv[i];
            max_v = v[i];
            max_idx = i;
        }
    }

    uint64_t n1 = ctx.n_valid_norm * (uint64_t)q * (uint64_t)(q - 1);
    printf("%d %d %d %llu %u %u ", q, mode, m, (unsigned long long)n1, n_orb, min_idx);
    print_u256_hex(&min_y); printf(" ");
    print_u256_hex(&min_v); printf(" %u ", max_idx);
    print_u256_hex(&max_y); printf(" ");
    print_u256_hex(&max_v); printf("\n");

    free(bufA); free(bufB); free(v); free(nv);
    free(ctx.state_to_orb); free(ctx.rep_codes); free(ctx.orb_sizes); free(ctx.orb_gather);
    return 0;
}
