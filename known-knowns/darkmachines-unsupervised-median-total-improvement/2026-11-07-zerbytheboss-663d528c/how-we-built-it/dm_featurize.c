#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define MAX_OBJS 64
#define N_FEATS 52
#define MZ 91.1876
#define MW 80.3790

typedef struct {
    int type; // 0: j, 1: b, 2: e-, 3: e+, 4: m-, 5: m+, 6: g
    double E, pt, eta, phi;
    double px, py, pz, p, m;
} Obj;

static inline double wrap_dphi(double dphi) {
    while (dphi > M_PI) dphi -= 2.0 * M_PI;
    while (dphi < -M_PI) dphi += 2.0 * M_PI;
    return fabs(dphi);
}

static inline double calc_mt(double pt, double phi, double met, double met_phi) {
    double dphi = phi - met_phi;
    double val = 2.0 * pt * met * (1.0 - cos(dphi));
    return val > 0.0 ? sqrt(val) : 0.0;
}

static inline double calc_inv_mass2(const Obj *a, const Obj *b) {
    double E = a->E + b->E;
    double px = a->px + b->px;
    double py = a->py + b->py;
    double pz = a->pz + b->pz;
    double m2 = E*E - (px*px + py*py + pz*pz);
    return m2 > 0.0 ? sqrt(m2) : 0.0;
}

static double calc_mt2(double px1, double py1, double px2, double py2, double mpx, double mpy) {
    double p1 = hypot(px1, py1);
    double p2 = hypot(px2, py2);
    double met = hypot(mpx, mpy);
    if (p1 < 1e-6 || p2 < 1e-6 || met < 1e-6) return 0.0;
    double det = px1 * py2 - py1 * px2;
    if (fabs(det) > 1e-9) {
        double alpha = (mpx * py2 - mpy * px2) / det;
        double beta  = (px1 * mpy - py1 * mpx) / det;
        if (alpha >= 0.0 && beta >= 0.0) return 0.0;
    }
    double best_mt2_sq = 1e30;
    for (int i = 0; i <= 16; i++) {
        double frac = (double)i / 16.0;
        double q1x = frac * mpx, q1y = frac * mpy;
        double q2x = mpx - q1x, q2y = mpy - q1y;
        double q1 = hypot(q1x, q1y), q2 = hypot(q2x, q2y);
        double mt1_sq = 2.0 * (p1 * q1 - (px1 * q1x + py1 * q1y));
        double mt2_sq = 2.0 * (p2 * q2 - (px2 * q2x + py2 * q2y));
        double mx = mt1_sq > mt2_sq ? mt1_sq : mt2_sq;
        if (mx < best_mt2_sq) best_mt2_sq = mx;
    }
    double ux = -mpy / met, uy = mpx / met;
    double f_opt = p2 / (p1 + p2);
    for (int i = -8; i <= 8; i++) {
        double s = (double)i * 0.15 * met;
        double q1x = f_opt * mpx + s * ux;
        double q1y = f_opt * mpy + s * uy;
        double q2x = mpx - q1x, q2y = mpy - q1y;
        double q1 = hypot(q1x, q1y), q2 = hypot(q2x, q2y);
        double mt1_sq = 2.0 * (p1 * q1 - (px1 * q1x + py1 * q1y));
        double mt2_sq = 2.0 * (p2 * q2 - (px2 * q2x + py2 * q2y));
        double mx = mt1_sq > mt2_sq ? mt1_sq : mt2_sq;
        if (mx < best_mt2_sq) best_mt2_sq = mx;
    }
    return best_mt2_sq > 0.0 ? sqrt(best_mt2_sq) : 0.0;
}

static int cmp_pt_desc(const void *a, const void *b) {
    double pa = ((const Obj *)a)->pt;
    double pb = ((const Obj *)b)->pt;
    return (pb > pa) - (pb < pa);
}

static void extract_line(char *line, int64_t *eid_out, float *feats) {
    char *saveptr = NULL;
    char *tok = strtok_r(line, ";\r\n", &saveptr);
    if (!tok) { *eid_out = -1; return; }
    *eid_out = strtoll(tok, NULL, 10);

    tok = strtok_r(NULL, ";\r\n", &saveptr); // process_id (ignored)
    tok = strtok_r(NULL, ";\r\n", &saveptr); // weight (ignored)
    tok = strtok_r(NULL, ";\r\n", &saveptr);
    double met = tok ? strtod(tok, NULL) / 1000.0 : 0.0;
    tok = strtok_r(NULL, ";\r\n", &saveptr);
    double met_phi = tok ? strtod(tok, NULL) : 0.0;
    double mpx = met * cos(met_phi);
    double mpy = met * sin(met_phi);

    Obj all_objs[MAX_OBJS];
    Obj jb_objs[MAX_OBJS];
    Obj b_objs[MAX_OBJS];
    Obj l_objs[MAX_OBJS];
    int n_all = 0, n_jb = 0, n_b = 0, n_l = 0, n_g = 0;

    while ((tok = strtok_r(NULL, ";\r\n", &saveptr)) != NULL) {
        if (*tok == '\0' || n_all >= MAX_OBJS) continue;
        char *p1 = strchr(tok, ',');
        if (!p1) continue;
        int t = -1;
        size_t tlen = (size_t)(p1 - tok);
        if (tlen == 1 && tok[0] == 'j') t = 0;
        else if (tlen == 1 && tok[0] == 'b') t = 1;
        else if (tlen == 2 && tok[0] == 'e' && tok[1] == '-') t = 2;
        else if (tlen == 2 && tok[0] == 'e' && tok[1] == '+') t = 3;
        else if (tlen == 2 && tok[0] == 'm' && tok[1] == '-') t = 4;
        else if (tlen == 2 && tok[0] == 'm' && tok[1] == '+') t = 5;
        else if (tlen == 1 && tok[0] == 'g') t = 6;
        if (t < 0) continue;

        char *endp;
        double E = strtod(p1 + 1, &endp) / 1000.0;
        if (*endp == ',') endp++;
        double pt = strtod(endp, &endp) / 1000.0;
        if (*endp == ',') endp++;
        double eta = strtod(endp, &endp);
        if (*endp == ',') endp++;
        double phi = strtod(endp, &endp);

        Obj o;
        o.type = t;
        o.E = E; o.pt = pt; o.eta = eta; o.phi = phi;
        o.px = pt * cos(phi);
        o.py = pt * sin(phi);
        o.pz = pt * sinh(eta);
        o.p  = pt * cosh(eta);
        double m2 = E*E - o.p*o.p;
        o.m  = m2 > 0.0 ? sqrt(m2) : 0.0;

        all_objs[n_all++] = o;
        if (t == 0 || t == 1) {
            jb_objs[n_jb++] = o;
            if (t == 1) b_objs[n_b++] = o;
        } else if (t >= 2 && t <= 5) {
            l_objs[n_l++] = o;
        } else if (t == 6) {
            n_g++;
        }
    }

    qsort(all_objs, n_all, sizeof(Obj), cmp_pt_desc);
    qsort(jb_objs, n_jb, sizeof(Obj), cmp_pt_desc);
    qsort(b_objs, n_b, sizeof(Obj), cmp_pt_desc);
    qsort(l_objs, n_l, sizeof(Obj), cmp_pt_desc);

    double HT = 0.0, HT_b = 0.0, LT = 0.0, GT = 0.0;
    double E_vis = 0.0, px_vis = 0.0, py_vis = 0.0, pz_vis = 0.0;
    double E_jb = 0.0, px_jb = 0.0, py_jb = 0.0, pz_jb = 0.0;
    double max_m_all = 0.0, sum_m_all = 0.0, max_m_lep = 0.0, max_m_jb = 0.0;
    double max_gam_inv_all = 0.0, max_gam_inv_lep = 0.0;

    for (int i = 0; i < n_all; i++) {
        Obj *o = &all_objs[i];
        E_vis += o->E; px_vis += o->px; py_vis += o->py; pz_vis += o->pz;
        sum_m_all += o->m;
        if (o->m > max_m_all) max_m_all = o->m;
        double ginv = o->m / (o->E > 1.0 ? o->E : 1.0);
        if (ginv > max_gam_inv_all) max_gam_inv_all = ginv;

        if (o->type == 0 || o->type == 1) {
            HT += o->pt;
            E_jb += o->E; px_jb += o->px; py_jb += o->py; pz_jb += o->pz;
            if (o->m > max_m_jb) max_m_jb = o->m;
            if (o->type == 1) HT_b += o->pt;
        } else if (o->type >= 2 && o->type <= 5) {
            LT += o->pt;
            if (o->m > max_m_lep) max_m_lep = o->m;
            if (ginv > max_gam_inv_lep) max_gam_inv_lep = ginv;
        } else if (o->type == 6) {
            GT += o->pt;
        }
    }

    double ST = met + HT + LT + GT;
    double vis_T = HT + LT + GT;
    double m2_vis = E_vis*E_vis - (px_vis*px_vis + py_vis*py_vis + pz_vis*pz_vis);
    double M_vis = m2_vis > 0.0 ? sqrt(m2_vis) : 0.0;
    double m2_jb = E_jb*E_jb - (px_jb*px_jb + py_jb*py_jb + pz_jb*pz_jb);
    double M_jb = m2_jb > 0.0 ? sqrt(m2_jb) : 0.0;
    double met_sig = met / sqrt(vis_T > 1.0 ? vis_T : 1.0);
    double met_frac = met / (ST > 1.0 ? ST : 1.0);
    double soft_px = -(mpx + px_vis);
    double soft_py = -(mpy + py_vis);
    double pt_soft = hypot(soft_px, soft_py);

    double pt_j1 = n_jb >= 1 ? jb_objs[0].pt : 0.0;
    double pt_j2 = n_jb >= 2 ? jb_objs[1].pt : 0.0;
    double pt_j3 = n_jb >= 3 ? jb_objs[2].pt : 0.0;
    double pt_j4 = n_jb >= 4 ? jb_objs[3].pt : 0.0;
    double pt_b1 = n_b >= 1 ? b_objs[0].pt : 0.0;
    double pt_b2 = n_b >= 2 ? b_objs[1].pt : 0.0;

    double dphi_j1 = n_jb >= 1 ? wrap_dphi(jb_objs[0].phi - met_phi) : 0.0;
    double min_dphi_j4 = n_jb >= 1 ? 4.0 : 0.0;
    double min_mt_j3 = n_jb >= 1 ? 1e9 : 0.0;
    for (int i = 0; i < n_jb && i < 4; i++) {
        double dp = wrap_dphi(jb_objs[i].phi - met_phi);
        if (dp < min_dphi_j4) min_dphi_j4 = dp;
        if (i < 3) {
            double mtj = calc_mt(jb_objs[i].pt, jb_objs[i].phi, met, met_phi);
            if (mtj < min_mt_j3) min_mt_j3 = mtj;
        }
    }
    double mt_j1 = n_jb >= 1 ? calc_mt(jb_objs[0].pt, jb_objs[0].phi, met, met_phi) : 0.0;
    double mt_b1 = n_b >= 1 ? calc_mt(b_objs[0].pt, b_objs[0].phi, met, met_phi) : 0.0;
    double mt2_j12 = n_jb >= 2 ? calc_mt2(jb_objs[0].px, jb_objs[0].py, jb_objs[1].px, jb_objs[1].py, mpx, mpy) : 0.0;
    double m_jj = n_jb >= 2 ? calc_inv_mass2(&jb_objs[0], &jb_objs[1]) : 0.0;
    double mct_j12 = 0.0;
    if (n_jb >= 2) {
        double v = 2.0 * (jb_objs[0].pt * jb_objs[1].pt + jb_objs[0].px * jb_objs[1].px + jb_objs[0].py * jb_objs[1].py);
        if (v > 0.0) mct_j12 = sqrt(v);
    }

    double pt_l1 = n_l >= 1 ? l_objs[0].pt : 0.0;
    double pt_l2 = n_l >= 2 ? l_objs[1].pt : 0.0;
    double pt_l3 = n_l >= 3 ? l_objs[2].pt : 0.0;
    double mt_l1 = n_l >= 1 ? calc_mt(l_objs[0].pt, l_objs[0].phi, met, met_phi) : 0.0;
    double mt_l2 = n_l >= 2 ? calc_mt(l_objs[1].pt, l_objs[1].phi, met, met_phi) : 0.0;
    double mt_l3 = n_l >= 3 ? calc_mt(l_objs[2].pt, l_objs[2].phi, met, met_phi) : 0.0;

    double min_mt_l = n_l >= 1 ? 1e9 : 0.0;
    double max_mt_l = 0.0;
    for (int i = 0; i < n_l; i++) {
        double mt = calc_mt(l_objs[i].pt, l_objs[i].phi, met, met_phi);
        if (mt < min_mt_l) min_mt_l = mt;
        if (mt > max_mt_l) max_mt_l = mt;
    }

    double m_ll12 = n_l >= 2 ? calc_inv_mass2(&l_objs[0], &l_objs[1]) : 0.0;
    double mt2_ll12 = n_l >= 2 ? calc_mt2(l_objs[0].px, l_objs[0].py, l_objs[1].px, l_objs[1].py, mpx, mpy) : 0.0;
    double mct_ll12 = 0.0;
    double pt_ll12 = 0.0, mt_ll12 = 0.0;
    if (n_l >= 2) {
        double v = 2.0 * (l_objs[0].pt * l_objs[1].pt + l_objs[0].px * l_objs[1].px + l_objs[0].py * l_objs[1].py);
        if (v > 0.0) mct_ll12 = sqrt(v);
        double lpx = l_objs[0].px + l_objs[1].px;
        double lpy = l_objs[0].py + l_objs[1].py;
        pt_ll12 = hypot(lpx, lpy);
        mt_ll12 = calc_mt(pt_ll12, atan2(lpy, lpx), met, met_phi);
    }

    double best_z_diff = 0.0, pt_z = 0.0, mt_lw = 0.0, pt_lw = 0.0, mt2_z_lw = 0.0, m_3l = 0.0, mt_3l = 0.0, mt_lw_wz = 0.0;
    if (n_l >= 2) {
        int best_a = -1, best_b = -1;
        double min_diff = 1e9;
        double best_wz_score = 1e18;
        for (int i = 0; i < n_l; i++) {
            for (int j = i + 1; j < n_l; j++) {
                int ti = l_objs[i].type, tj = l_objs[j].type;
                if ((ti == 2 && tj == 3) || (ti == 3 && tj == 2) || (ti == 4 && tj == 5) || (ti == 5 && tj == 4)) {
                    double m = calc_inv_mass2(&l_objs[i], &l_objs[j]);
                    double d = fabs(m - MZ);
                    if (d < min_diff) {
                        min_diff = d;
                        best_a = i; best_b = j;
                    }
                    if (n_l >= 3) {
                        int w_idx = -1;
                        for (int k = 0; k < n_l; k++) {
                            if (k != i && k != j) { w_idx = k; break; }
                        }
                        if (w_idx >= 0) {
                            double mt_cand = calc_mt(l_objs[w_idx].pt, l_objs[w_idx].phi, met, met_phi);
                            double ex_w = mt_cand > MW ? (mt_cand - MW) / 15.0 : 0.0;
                            double wz_sc = (d / 6.0)*(d / 6.0) + ex_w*ex_w;
                            if (wz_sc < best_wz_score) {
                                best_wz_score = wz_sc;
                                mt_lw_wz = mt_cand;
                            }
                        }
                    }
                }
            }
        }
        if (best_a >= 0) {
            best_z_diff = min_diff;
            double zpx = l_objs[best_a].px + l_objs[best_b].px;
            double zpy = l_objs[best_a].py + l_objs[best_b].py;
            pt_z = hypot(zpx, zpy);
            if (n_l >= 3) {
                int w_idx = -1;
                for (int k = 0; k < n_l; k++) {
                    if (k != best_a && k != best_b) { w_idx = k; break; }
                }
                if (w_idx >= 0) {
                    pt_lw = l_objs[w_idx].pt;
                    mt_lw = calc_mt(l_objs[w_idx].pt, l_objs[w_idx].phi, met, met_phi);
                    mt2_z_lw = calc_mt2(zpx, zpy, l_objs[w_idx].px, l_objs[w_idx].py, mpx, mpy);
                }
            }
        } else {
            best_z_diff = fabs(m_ll12 - MZ);
            if (n_l >= 3) {
                pt_lw = l_objs[0].pt;
                mt_lw = mt_l1;
                mt_lw_wz = mt_l1;
            }
        }
    }
    if (n_l >= 3) {
        double E3 = l_objs[0].E + l_objs[1].E + l_objs[2].E;
        double px3 = l_objs[0].px + l_objs[1].px + l_objs[2].px;
        double py3 = l_objs[0].py + l_objs[1].py + l_objs[2].py;
        double pz3 = l_objs[0].pz + l_objs[1].pz + l_objs[2].pz;
        double m2 = E3*E3 - (px3*px3 + py3*py3 + pz3*pz3);
        m_3l = m2 > 0.0 ? sqrt(m2) : 0.0;
        double pt3 = hypot(px3, py3);
        mt_3l = calc_mt(pt3, atan2(py3, px3), met, met_phi);
    }

    int idx = 0;
    feats[idx++] = (float)log1p(met);          // 0
    feats[idx++] = (float)log1p(HT);           // 1
    feats[idx++] = (float)log1p(HT_b);         // 2
    feats[idx++] = (float)log1p(LT);           // 3
    feats[idx++] = (float)log1p(ST);           // 4
    feats[idx++] = (float)log1p(E_vis);        // 5
    feats[idx++] = (float)log1p(M_vis);        // 6
    feats[idx++] = (float)log1p(M_jb);         // 7
    feats[idx++] = (float)met_sig;             // 8
    feats[idx++] = (float)met_frac;            // 9
    feats[idx++] = (float)log1p(pt_soft);      // 10
    feats[idx++] = (float)(HT_b / (HT > 1.0 ? HT : 1.0)); // 11
    feats[idx++] = (float)n_jb;                // 12
    feats[idx++] = (float)n_b;                 // 13
    feats[idx++] = (float)n_l;                 // 14
    feats[idx++] = (float)log1p(max_m_all);    // 15
    feats[idx++] = (float)log1p(sum_m_all);    // 16
    feats[idx++] = (float)log1p(max_m_lep);    // 17
    feats[idx++] = (float)log1p(max_m_jb);     // 18
    feats[idx++] = (float)max_gam_inv_all;     // 19
    feats[idx++] = (float)max_gam_inv_lep;     // 20
    feats[idx++] = (float)log1p(pt_j1);        // 21
    feats[idx++] = (float)log1p(pt_j2);        // 22
    feats[idx++] = (float)log1p(pt_j3);        // 23
    feats[idx++] = (float)log1p(pt_j4);        // 24
    feats[idx++] = (float)log1p(pt_b1);        // 25
    feats[idx++] = (float)log1p(pt_b2);        // 26
    feats[idx++] = (float)dphi_j1;             // 27
    feats[idx++] = (float)min_dphi_j4;         // 28
    feats[idx++] = (float)log1p(mt_j1);        // 29
    feats[idx++] = (float)log1p(min_mt_j3);    // 30
    feats[idx++] = (float)log1p(mt_b1);        // 31
    feats[idx++] = (float)log1p(mt2_j12);      // 32
    feats[idx++] = (float)log1p(m_jj);         // 33
    feats[idx++] = (float)log1p(mct_j12);      // 34
    feats[idx++] = (float)log1p(pt_l1);        // 35
    feats[idx++] = (float)log1p(pt_l2);        // 36
    feats[idx++] = (float)log1p(pt_l3);        // 37
    feats[idx++] = (float)log1p(min_mt_l);     // 38
    feats[idx++] = (float)log1p(max_mt_l);     // 39
    feats[idx++] = (float)log1p(mt2_ll12);     // 40
    feats[idx++] = (float)log1p(best_z_diff);  // 41
    feats[idx++] = (float)log1p(mt_lw);        // 42
    feats[idx++] = (float)log1p(mt2_z_lw);     // 43
    feats[idx++] = (float)log1p(mt_lw_wz);     // 44
    feats[idx++] = (float)log1p(pt_z);         // 45
    feats[idx++] = (float)log1p(pt_lw);        // 46
    feats[idx++] = (float)log1p(m_3l);         // 47
    feats[idx++] = (float)log1p(mt_3l);        // 48
    feats[idx++] = (float)log1p(mct_ll12);     // 49
    feats[idx++] = (float)log1p(m_ll12);       // 50
    feats[idx++] = (float)log1p(mt_ll12);      // 51
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <input.csv> <output.bin>\n", argv[0]);
        return 1;
    }
    FILE *fin = fopen(argv[1], "r");
    if (!fin) { perror("fopen in"); return 1; }
    FILE *fout = fopen(argv[2], "wb");
    if (!fout) { perror("fopen out"); return 1; }

    char buf[65536];
    float feats[N_FEATS];
    int64_t eid;
    int64_t count = 0;
    while (fgets(buf, sizeof(buf), fin)) {
        extract_line(buf, &eid, feats);
        if (eid < 0) continue;
        fwrite(&eid, sizeof(int64_t), 1, fout);
        fwrite(feats, sizeof(float), N_FEATS, fout);
        count++;
    }
    fclose(fin);
    fclose(fout);
    printf("Processed %lld events from %s -> %s\n", (long long)count, argv[1], argv[2]);
    return 0;
}
