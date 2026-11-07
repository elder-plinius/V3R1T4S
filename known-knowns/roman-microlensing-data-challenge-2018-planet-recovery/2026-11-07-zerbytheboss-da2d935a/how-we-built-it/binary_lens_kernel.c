#include <math.h>
#include <stdlib.h>

typedef struct {
    double re;
    double im;
} cpx;

static inline cpx c_add(cpx a, cpx b) { return (cpx){a.re + b.re, a.im + b.im}; }
static inline cpx c_sub(cpx a, cpx b) { return (cpx){a.re - b.re, a.im - b.im}; }
static inline cpx c_mul(cpx a, cpx b) { return (cpx){a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re}; }
static inline cpx c_scale(cpx a, double s) { return (cpx){a.re * s, a.im * s}; }
static inline cpx c_conj(cpx a) { return (cpx){a.re, -a.im}; }
static inline double c_abs2(cpx a) { return a.re * a.re + a.im * a.im; }
static inline double c_abs(cpx a) { return sqrt(a.re * a.re + a.im * a.im); }
static inline cpx c_div(cpx a, cpx b) {
    double d = b.re * b.re + b.im * b.im;
    if (d < 1e-300) d = 1e-300;
    return (cpx){(a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d};
}
static inline cpx c_inv(cpx b) {
    double d = b.re * b.re + b.im * b.im;
    if (d < 1e-300) d = 1e-300;
    return (cpx){b.re / d, -b.im / d};
}

static inline double solve_point_mag(cpx zeta, double s, double q, int *n_img_out, double *min_detJ_out) {
    double m1 = 1.0 / (1.0 + q);
    double m2 = q / (1.0 + q);
    double z1 = -m2 * s;
    double z2 = m1 * s;
    cpx zb = c_conj(zeta);

    double u = c_abs(zeta);
    if (u < 1e-5) u = 1e-5;
    double r_plus = 0.5 * (sqrt(u * u + 4.0) + u);
    double r_minus = 0.5 * (sqrt(u * u + 4.0) - u);
    double ux = zeta.re / u;
    double uy = zeta.im / u;

    cpx roots[5];
    roots[0] = (cpx){r_plus * ux + 0.001, r_plus * uy - 0.001};
    roots[1] = (cpx){-r_minus * ux - 0.001, -r_minus * uy + 0.001};
    roots[2] = (cpx){z1 + 0.015, 0.021};
    roots[3] = (cpx){z2 - 0.015, -0.019};
    roots[4] = (cpx){0.5 * (z1 + z2) + 0.007, 0.025};

    double sum_z12 = z1 + z2;

    for (int iter = 0; iter < 16; iter++) {
        cpx step[5];
        double max_step2 = 0.0;
        for (int k = 0; k < 5; k++) {
            cpx z = roots[k];
            cpx zm1 = (cpx){z.re - z1, z.im};
            cpx zm2 = (cpx){z.re - z2, z.im};
            cpx P = c_mul(zm1, zm2);
            cpx dP = (cpx){2.0 * z.re - sum_z12, 2.0 * z.im};
            cpx lin = (cpx){m1 * zm2.re + m2 * zm1.re, z.im};

            cpx zbm1 = (cpx){zb.re - z1, zb.im};
            cpx zbm2 = (cpx){zb.re - z2, zb.im};
            cpx A = c_add(c_mul(zbm1, P), lin);
            cpx B = c_add(c_mul(zbm2, P), lin);
            cpx dA = c_add(c_mul(zbm1, dP), (cpx){1.0, 0.0});
            cpx dB = c_add(c_mul(zbm2, dP), (cpx){1.0, 0.0});

            cpx mB_mA = (cpx){m1 * B.re + m2 * A.re, m1 * B.im + m2 * A.im};
            cpx dmB_mA = (cpx){m1 * dB.re + m2 * dA.re, m1 * dB.im + m2 * dA.im};

            cpx zmzeta = c_sub(z, zeta);
            cpx AB = c_mul(A, B);
            cpx F = c_sub(c_mul(zmzeta, AB), c_mul(P, mB_mA));

            cpx dAB = c_add(c_mul(dA, B), c_mul(A, dB));
            cpx dF = c_sub(c_add(AB, c_mul(zmzeta, dAB)), c_add(c_mul(dP, mB_mA), c_mul(P, dmB_mA)));

            cpx w = c_div(F, dF);
            cpx s_inv = (cpx){0.0, 0.0};
            for (int j = 0; j < 5; j++) {
                if (j != k) {
                    s_inv = c_add(s_inv, c_inv(c_sub(z, roots[j])));
                }
            }
            cpx denom = c_sub((cpx){1.0, 0.0}, c_mul(w, s_inv));
            step[k] = c_div(w, denom);
            double st2 = c_abs2(step[k]);
            if (st2 > max_step2) max_step2 = st2;
        }
        for (int k = 0; k < 5; k++) {
            roots[k] = c_sub(roots[k], step[k]);
        }
        if (max_step2 < 1e-24) break;
    }

    double total_mag = 0.0;
    int n_valid = 0;
    double min_det = 1e30;

    for (int k = 0; k < 5; k++) {
        cpx z = roots[k];
        cpx rb = c_conj(z);
        cpx rbm1 = (cpx){rb.re - z1, rb.im};
        cpx rbm2 = (cpx){rb.re - z2, rb.im};
        cpx defl = c_add(c_scale(c_inv(rbm1), m1), c_scale(c_inv(rbm2), m2));
        cpx res = c_add(c_sub(zeta, z), defl);
        if (c_abs2(res) < 1e-7) {
            // Check duplicate roots
            int dup = 0;
            for (int j = 0; j < k; j++) {
                if (c_abs2(c_sub(z, roots[j])) < 1e-10) {
                    dup = 1;
                    break;
                }
            }
            if (!dup) {
                cpx zm1 = (cpx){z.re - z1, z.im};
                cpx zm2 = (cpx){z.re - z2, z.im};
                cpx sh1 = c_scale(c_inv(c_mul(zm1, zm1)), m1);
                cpx sh2 = c_scale(c_inv(c_mul(zm2, zm2)), m2);
                cpx shear = c_add(sh1, sh2);
                double detJ = fabs(1.0 - c_abs2(shear));
                if (detJ < min_det) min_det = detJ;
                if (detJ < 1e-9) detJ = 1e-9;
                total_mag += 1.0 / detJ;
                n_valid++;
            }
        }
    }
    if (n_valid < 3) {
        // Fallback to Paczynski if numerical root missed
        double uc = (u > 1e-6) ? u : 1e-6;
        total_mag = (uc * uc + 2.0) / (uc * sqrt(uc * uc + 4.0));
    }
    if (n_img_out) *n_img_out = n_valid;
    if (min_detJ_out) *min_detJ_out = min_det;
    return total_mag;
}

void bl_magnification_fs(
    int n_pts,
    const double *u1,
    const double *u2,
    double s,
    double q,
    double rho,
    double gamma_ld,
    double *mag_out
) {
    // Precompute ring quadrature nodes & weights for Tier 1 (8 pts + center) and Tier 2 (36 pts + center)
    static const double r1_frac[2] = {0.52, 0.88};
    static const double r1_area[2] = {0.42, 0.46}; // center gets 0.12
    static const double c4[4] = {1.0, 0.0, -1.0, 0.0};
    static const double s4[4] = {0.0, 1.0, 0.0, -1.0};

    static const double r2_frac[4] = {0.25, 0.52, 0.76, 0.94};
    static const double r2_area[4] = {0.14, 0.24, 0.30, 0.28}; // center gets 0.04
    double c12[12], s12[12];
    for (int j = 0; j < 12; j++) {
        double ang = j * (3.14159265358979323846 / 6.0);
        c12[j] = cos(ang);
        s12[j] = sin(ang);
    }

    for (int i = 0; i < n_pts; i++) {
        cpx z0 = (cpx){u1[i], u2[i]};
        int n0 = 3;
        double min_det0 = 1.0;
        double m0 = solve_point_mag(z0, s, q, &n0, &min_det0);

        if (rho <= 1e-5 || (min_det0 > 0.25 && m0 < 5.0 && rho < 0.02)) {
            mag_out[i] = m0;
            continue;
        }

        // Tier 1 probe: 8 points on 2 rings
        int caustic_cross = (n0 == 5);
        double m_min = m0, m_max = m0;
        double w_sum1 = 0.12 * (1.0 + 0.5 * gamma_ld);
        double mag_sum1 = w_sum1 * m0;

        for (int ir = 0; ir < 2; ir++) {
            double rf = r1_frac[ir];
            double rp = rho * rf;
            double mu = sqrt(1.0 - rf * rf);
            double w_ring = (r1_area[ir] / 4.0) * (1.0 - gamma_ld * (1.0 - 1.5 * mu));
            for (int ia = 0; ia < 4; ia++) {
                cpx zp = (cpx){z0.re + rp * c4[ia], z0.im + rp * s4[ia]};
                int np_img = 3;
                double md = 1.0;
                double mp = solve_point_mag(zp, s, q, &np_img, &md);
                if (np_img != n0 || md < 0.03) caustic_cross = 1;
                if (mp < m_min) m_min = mp;
                if (mp > m_max) m_max = mp;
                mag_sum1 += w_ring * mp;
                w_sum1 += w_ring;
            }
        }

        if (!caustic_cross && (m_max - m_min) < 0.15 * m0) {
            mag_out[i] = mag_sum1 / w_sum1;
            continue;
        }

        // Tier 2 full 4-ring x 12-angle + center limb-darkened quadrature (49 points)
        double w_sum2 = 0.04 * (1.0 + 0.5 * gamma_ld);
        double mag_sum2 = w_sum2 * m0;
        for (int ir = 0; ir < 4; ir++) {
            double rf = r2_frac[ir];
            double rp = rho * rf;
            double mu = sqrt(1.0 - rf * rf);
            double w_ring = (r2_area[ir] / 12.0) * (1.0 - gamma_ld * (1.0 - 1.5 * mu));
            for (int ia = 0; ia < 12; ia++) {
                cpx zp = (cpx){z0.re + rp * c12[ia], z0.im + rp * s12[ia]};
                int np_img = 3;
                double md = 1.0;
                double mp = solve_point_mag(zp, s, q, &np_img, &md);
                mag_sum2 += w_ring * mp;
                w_sum2 += w_ring;
            }
        }
        mag_out[i] = mag_sum2 / w_sum2;
    }
}

double bl_eval_trajectory_chi2(
    int n_pts,
    const double *t,
    const double *f,
    const double *ferr,
    double t0,
    double u0,
    double tE,
    double s,
    double q,
    double alpha_rad,
    double rho,
    double gamma_ld,
    double *fs_out,
    double *fb_out,
    double *mag_buf
) {
    double ca = cos(alpha_rad);
    double sa = sin(alpha_rad);
    double inv_tE = 1.0 / (tE > 1e-4 ? tE : 1e-4);

    // Compute source trajectory in CoM frame:
    // At t = t0, closest approach to CoM has offset u0;
    // Following Penny/MulensModel convention: u1 = -tau * cos(alpha) + u0 * sin(alpha), u2 = -tau * sin(alpha) - u0 * cos(alpha)
    // Wait: since binary lens magnification is symmetric under (u2 -> -u2, alpha -> -alpha), scanning alpha in [0, 2*pi) covers all trajectories!
    double *u1 = (double *)malloc(sizeof(double) * n_pts * 2);
    double *u2 = u1 + n_pts;
    for (int i = 0; i < n_pts; i++) {
        double tau = (t[i] - t0) * inv_tE;
        u1[i] = tau * ca - u0 * sa;
        u2[i] = tau * sa + u0 * ca;
    }

    bl_magnification_fs(n_pts, u1, u2, s, q, rho, gamma_ld, mag_buf);
    free(u1);

    // Linear weighted least squares for F(t) = Fs * (A(t) - 1) + Fb with Fs >= 0
    double sw = 0.0, sx = 0.0, sxx = 0.0, sy = 0.0, sxy = 0.0;
    for (int i = 0; i < n_pts; i++) {
        double w = 1.0 / (ferr[i] * ferr[i]);
        double x = mag_buf[i] - 1.0;
        double y = f[i];
        sw += w;
        sx += w * x;
        sxx += w * x * x;
        sy += w * y;
        sxy += w * x * y;
    }
    double det = sw * sxx - sx * sx;
    double Fs = 0.0, Fb = sy / (sw > 1e-20 ? sw : 1e-20);
    if (det > 1e-20) {
        Fs = (sw * sxy - sx * sy) / det;
        Fb = (sxx * sy - sx * sxy) / det;
        if (Fs < 0.0) {
            Fs = 0.0;
            Fb = sy / sw;
        }
    }
    if (fs_out) *fs_out = Fs;
    if (fb_out) *fb_out = Fb;

    double chi2 = 0.0;
    for (int i = 0; i < n_pts; i++) {
        double pred = Fs * (mag_buf[i] - 1.0) + Fb;
        double r = (f[i] - pred) / ferr[i];
        chi2 += r * r;
    }
    return chi2;
}

double bl_fit_event_logq(
    int n_pts,
    const double *dtau_sub,
    const double *df_obs,
    const double *es,
    double u0,
    double tau_a,
    double Fs,
    double sp,
    int is_cent,
    double *best_chi2_out
) {
    double ua = sqrt(u0 * u0 + tau_a * tau_a);
    if (ua < 1e-4) ua = 1e-4;
    double A_host_ua = (ua * ua + 2.0) / (ua * sqrt(ua * ua + 4.0));
    double sp_exact = 0.5 * (sqrt(ua * ua + 4.0) + ua);
    double dtheta = atan2(u0, tau_a);

    const int n_phi = 72;
    double c_phi[72], s_phi[72], phi_grid[72];
    for (int j = 0; j < n_phi; j++) {
        phi_grid[j] = j * (3.14159265358979323846 / (double)(n_phi - 1));
        c_phi[j] = cos(phi_grid[j]);
        s_phi[j] = sin(phi_grid[j]);
    }

    double *u1 = (double *)malloc(sizeof(double) * n_pts * 3);
    double *u2 = u1 + n_pts;
    double *mag_buf = u2 + n_pts;

    double best_chi2 = 1e30;
    double best_lq = -3.0;
    const double b_mults[5] = {-1.8, -0.65, 0.0, 0.65, 1.8};
    const double sh_mults[3] = {-0.35, 0.0, 0.35};
    const double rhos[3] = {0.0008, 0.004, 0.015};

    int n_s = is_cent ? 1 : 2;
    double s_cands[2];
    s_cands[0] = is_cent ? sp : sp_exact;
    s_cands[1] = 1.0 / sp_exact;

    for (int iq = 0; iq < 18; iq++) {
        double lq = -5.6 + iq * ((-1.5 - (-5.6)) / 17.0);
        double q = pow(10.0, lq);
        double m2 = q / (1.0 + q);

        for (int is_c = 0; is_c < n_s; is_c++) {
            double s_cand = s_cands[is_c];
            double z_host = (s_cand >= 1.0) ? (-m2 * (s_cand - 1.0 / s_cand)) : 0.0;

            double max_pos = -1e30, min_neg = 1e30;
            int ipk_pos = 0, ipk_neg = 0;
            for (int j = 0; j < n_phi; j++) {
                cpx zc = (cpx){z_host + ua * c_phi[j], ua * s_phi[j]};
                double m0 = solve_point_mag(zc, s_cand, q, NULL, NULL);
                double dA = m0 - A_host_ua;
                if (dA > max_pos) { max_pos = dA; ipk_pos = j; }
                if (dA < min_neg) { min_neg = dA; ipk_neg = j; }
            }

            int n_phi_c = (ipk_pos == ipk_neg) ? 1 : 2;
            double phi_cands[2] = {phi_grid[ipk_pos], phi_grid[ipk_neg]};

            double denom_s = fabs(s_cand - 1.0 / s_cand);
            double caustic_scale;
            if (is_cent) {
                double d2 = denom_s * denom_s;
                if (d2 < 0.15) d2 = 0.15;
                caustic_scale = 4.0 * q / d2;
            } else {
                double ds = s_cand * sqrt(fabs(s_cand * s_cand - 1.0) + 0.05);
                if (ds < 0.2) ds = 0.2;
                caustic_scale = sqrt(q) / ds;
            }
            if (caustic_scale < 0.0005) caustic_scale = 0.0005;

            for (int ip = 0; ip < n_phi_c; ip++) {
                double phi_star = phi_cands[ip];
                double zc_re = z_host + ua * cos(phi_star);
                double zc_im = ua * sin(phi_star);
                double ths[2] = {phi_star + dtheta, phi_star - dtheta};

                static const double r1_frac[2] = {0.52, 0.88};
                static const double w_c = 0.12 * (1.0 + 0.5 * 0.45);
                static const double w_r0 = (0.42 / 4.0) * (1.0 - 0.45 * (1.0 - 1.5 * 0.854166));
                static const double w_r1 = (0.46 / 4.0) * (1.0 - 0.45 * (1.0 - 1.5 * 0.474974));
                static const double w_tot = 0.12 * (1.0 + 0.5 * 0.45) + 4.0 * ((0.42 / 4.0) * (1.0 - 0.45 * (1.0 - 1.5 * 0.854166)) + (0.46 / 4.0) * (1.0 - 0.45 * (1.0 - 1.5 * 0.474974)));
                static const double c4[4] = {1.0, 0.0, -1.0, 0.0};
                static const double s4[4] = {0.0, 1.0, 0.0, -1.0};

                for (int ith = 0; ith < 2; ith++) {
                    double ct = cos(ths[ith]);
                    double st_ang = sin(ths[ith]);
                    for (int ib = 0; ib < 5; ib++) {
                        double b_perp = b_mults[ib] * caustic_scale;
                        for (int ish = 0; ish < 3; ish++) {
                            double dtau_sh = sh_mults[ish] * caustic_scale;
                            double s_yy[3] = {0.0, 0.0, 0.0};
                            double s_yg[3] = {0.0, 0.0, 0.0};
                            double s_gg[3] = {0.0, 0.0, 0.0};
                            for (int i = 0; i < n_pts; i++) {
                                double tl = dtau_sub[i] - dtau_sh;
                                double x0 = zc_re + tl * ct - b_perp * st_ang;
                                double y0 = zc_im + tl * st_ang + b_perp * ct;
                                double dx = x0 - z_host;
                                double dy = y0;
                                double du = sqrt(dx * dx + dy * dy);
                                if (du < 1e-5) du = 1e-5;
                                double A_pspl = (du * du + 2.0) / (du * sqrt(du * du + 4.0));

                                int n0 = 3;
                                double md0 = 1.0;
                                double m0 = solve_point_mag((cpx){x0, y0}, s_cand, q, &n0, &md0);
                                double inv_e = 1.0 / es[i];
                                double yn = df_obs[i] * inv_e;

                                for (int ir = 0; ir < 3; ir++) {
                                    double rho = rhos[ir];
                                    double m_fs;
                                    if (md0 > 0.30 && m0 < 5.0 && rho < 0.01) {
                                        m_fs = m0;
                                    } else {
                                        double m_sum = w_c * m0;
                                        double rp0 = rho * r1_frac[0];
                                        double rp1 = rho * r1_frac[1];
                                        for (int ia = 0; ia < 4; ia++) {
                                            m_sum += w_r0 * solve_point_mag((cpx){x0 + rp0 * c4[ia], y0 + rp0 * s4[ia]}, s_cand, q, NULL, NULL);
                                            m_sum += w_r1 * solve_point_mag((cpx){x0 + rp1 * c4[ia], y0 + rp1 * s4[ia]}, s_cand, q, NULL, NULL);
                                        }
                                        m_fs = m_sum / w_tot;
                                    }
                                    double gn = Fs * (m_fs - A_pspl) * inv_e;
                                    s_yy[ir] += yn * yn;
                                    s_yg[ir] += yn * gn;
                                    s_gg[ir] += gn * gn;
                                }
                            }
                            for (int ir = 0; ir < 3; ir++) {
                                if (s_gg[ir] <= 1e-12 || s_yg[ir] <= 0.0) continue;
                                double beta = s_yg[ir] / s_gg[ir];
                                if (beta < 0.45) beta = 0.45;
                                if (beta > 2.20) beta = 2.20;
                                double c2 = s_yy[ir] - 2.0 * beta * s_yg[ir] + beta * beta * s_gg[ir];
                                if (c2 < best_chi2) {
                                    best_chi2 = c2;
                                    best_lq = lq;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    free(u1);
    if (best_chi2_out) *best_chi2_out = best_chi2;
    return best_lq;
}

