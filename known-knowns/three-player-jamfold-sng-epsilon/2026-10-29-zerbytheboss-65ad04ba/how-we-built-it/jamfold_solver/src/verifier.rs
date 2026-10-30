// Independent best response verifier for absorbing Markov game
use crate::cards::CardTables;
use crate::equity::EquityEngine;
use crate::eval::Evaluator;
use crate::stage::{EliminationConvention, StateStrategy};
use crate::state::{StateTable, NUM_POSITION_STATES};
use rayon::prelude::*;

pub struct Verifier<'a> {
    pub state_table: StateTable,
    pub cards: &'a CardTables,
    pub equity: &'a EquityEngine,
    pub eval: &'a Evaluator,
}

#[derive(Debug, Clone)]
pub struct VerificationReport {
    pub epsilon: f64,
    pub epsilon_i: f64,
    pub epsilon_ii: f64,
    pub max_residual: f64,
    pub values: Vec<f64>,
}

#[inline(always)]
fn route_outcome(
    adj: &mut [Vec<(usize, f64)>],
    b: &mut [f64],
    row_btn: usize,
    row_sb: usize,
    row_bb: usize,
    s: [u8; 3],
    c: [u8; 3],
    weight: f64,
    conv: EliminationConvention,
) {
    if weight <= 0.0 {
        return;
    }
    let num_busted = (c[0] == 0) as u8 + (c[1] == 0) as u8 + (c[2] == 0) as u8;
    if num_busted == 0 {
        let next_v = crate::state::stack_to_index(c[1], c[2], c[0]);
        adj[row_btn].push((next_v * 3 + 2, weight));
        adj[row_sb].push((next_v * 3 + 0, weight));
        adj[row_bb].push((next_v * 3 + 1, weight));
    } else {
        let u_term = crate::stage::eval_leaf(s[0], s[1], s[2], c[0], c[1], c[2], &[], conv);
        b[row_btn] += weight * u_term[0];
        b[row_sb] += weight * u_term[1];
        b[row_bb] += weight * u_term[2];
    }
}

#[inline(always)]
fn route_2way_showdown(
    adj: &mut [Vec<(usize, f64)>],
    b: &mut [f64],
    row_btn: usize,
    row_sb: usize,
    row_bb: usize,
    s: [u8; 3],
    p_a: usize,
    p_b: usize,
    k_a: u8,
    k_b: u8,
    dead_c: u8,
    p_win_a: f64,
    p_win_b: f64,
    p_tie: f64,
    conv: EliminationConvention,
) {
    let m = k_a.min(k_b);
    let mut c_base = s;
    c_base[p_a] = s[p_a] - k_a + (k_a - m);
    c_base[p_b] = s[p_b] - k_b + (k_b - m);
    c_base[3 - p_a - p_b] = s[3 - p_a - p_b] - dead_c;
    let main_pot = 2 * m + dead_c;

    // A wins
    if p_win_a > 0.0 {
        let mut c_a = c_base;
        c_a[p_a] += main_pot;
        route_outcome(adj, b, row_btn, row_sb, row_bb, s, c_a, p_win_a, conv);
    }

    // B wins
    if p_win_b > 0.0 {
        let mut c_b = c_base;
        c_b[p_b] += main_pot;
        route_outcome(adj, b, row_btn, row_sb, row_bb, s, c_b, p_win_b, conv);
    }

    // Tie
    if p_tie > 0.0 {
        if main_pot % 2 == 0 {
            let mut c_t = c_base;
            c_t[p_a] += main_pot / 2;
            c_t[p_b] += main_pot / 2;
            route_outcome(adj, b, row_btn, row_sb, row_bb, s, c_t, p_tie, conv);
        } else {
            let half = main_pot / 2;
            let mut c_t1 = c_base;
            c_t1[p_a] += half + 1;
            c_t1[p_b] += half;
            route_outcome(adj, b, row_btn, row_sb, row_bb, s, c_t1, p_tie * 0.5, conv);

            let mut c_t2 = c_base;
            c_t2[p_a] += half;
            c_t2[p_b] += half + 1;
            route_outcome(adj, b, row_btn, row_sb, row_bb, s, c_t2, p_tie * 0.5, conv);
        }
    }
}



impl<'a> Verifier<'a> {
    pub fn new(
        cards: &'a CardTables,
        equity: &'a EquityEngine,
        eval: &'a Evaluator,
    ) -> Self {
        Verifier {
            state_table: StateTable::new(),
            cards,
            equity,
            eval,
        }
    }

    // Build the sparse transition system for a given strategy profile and convention
    pub fn build_system(
        &self,
        profile: &[StateStrategy],
        _v_current: &[f64],
        conv: EliminationConvention,
    ) -> (Vec<Vec<(usize, f64)>>, Vec<f64>) {
        let mut adj = vec![Vec::new(); NUM_POSITION_STATES];
        let mut b = vec![0.0f64; NUM_POSITION_STATES];

        // Precompute p_c1 unconditional distribution
        let mut p_c1 = [0.0f64; 169];
        for c1 in 0..169 {
            p_c1[c1] = (self.cards.class_combos[c1].len() as f64) / 1326.0;
        }

        // For each of the 946 non-terminal states
        for (v_idx, &(s1, s2, s3)) in self.state_table.index_to_stack.iter().enumerate() {
            let strat = &profile[v_idx];
            let row_btn = v_idx * 3 + 0;
            let row_sb = v_idx * 3 + 1;
            let row_bb = v_idx * 3 + 2;

            let s = [s1, s2, s3];
            let bb_is_allin = s3 == 1;
            let bb_can_fold_fj = !bb_is_allin && s2 > 2;
            let bb_can_fold_jf = !bb_is_allin && s1 > 2;
            let bb_can_fold_jc = !bb_is_allin && (s1 > 2 || s2 > 2);

            // ---------------------------------------------------------------
            // Branch 1: BTN Folds
            // ---------------------------------------------------------------
            let mut w_sb_given_btn_f = [0.0f64; 169];
            for c1 in 0..169 {
                let w1 = p_c1[c1] * (1.0 - strat.btn_jam[c1]);
                if w1 > 0.0 {
                    let cond_row = &self.cards.cond_prob_2[c1];
                    for c2 in 0..169 {
                        w_sb_given_btn_f[c2] += w1 * cond_row[c2];
                    }
                }
            }

            // Sub-branch 1.1: SB Folds (both fold -> BB wins blinds)
            let mut w_both_fold = 0.0f64;
            if s2 > 1 {
                for c2 in 0..169 {
                    let p_sb_fold = 1.0 - strat.sb_jam_vs_fold[c2];
                    if p_sb_fold > 0.0 {
                        w_both_fold += w_sb_given_btn_f[c2] * p_sb_fold;
                    }
                }
            }
            if w_both_fold > 0.0 {
                let c_end = [s1, s2.saturating_sub(1), s3 + 1];
                route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c_end, w_both_fold, conv);
            }

            // Sub-branch 1.2: SB Jams
            // (a) BB Folds -> SB wins blinds
            if bb_can_fold_fj {
                let mut w_btn_f_sb_j_bb_f = 0.0f64;
                for c2 in 0..169 {
                    let w_sb_j = if s2 == 1 { w_sb_given_btn_f[c2] } else { w_sb_given_btn_f[c2] * strat.sb_jam_vs_fold[c2] };
                    if w_sb_j > 0.0 {
                        let cond_row = &self.cards.cond_prob_2[c2];
                        for c3 in 0..169 {
                            let p_bb_fold = 1.0 - strat.bb_call_vs_fold_jam[c3];
                            if p_bb_fold > 0.0 {
                                w_btn_f_sb_j_bb_f += w_sb_j * cond_row[c3] * p_bb_fold;
                            }
                        }
                    }
                }
                if w_btn_f_sb_j_bb_f > 0.0 {
                    let c_end = [s1, s2 + 2.min(s3), s3 - 2.min(s3)];
                    route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c_end, w_btn_f_sb_j_bb_f, conv);
                }
            }

            // (b) BB Calls -> Showdown SB vs BB
            let mut p_win_sb = 0.0f64;
            let mut p_win_bb = 0.0f64;
            let mut p_tie_sb_bb = 0.0f64;
            for c2 in 0..169 {
                let w_sb_j = if s2 == 1 { w_sb_given_btn_f[c2] } else { w_sb_given_btn_f[c2] * strat.sb_jam_vs_fold[c2] };
                if w_sb_j > 0.0 {
                    let cond_row = &self.cards.cond_prob_2[c2];
                    for c3 in 0..169 {
                        let p_bb_call = if !bb_can_fold_fj { 1.0 } else { strat.bb_call_vs_fold_jam[c3] };
                        if p_bb_call > 0.0 {
                            let w = w_sb_j * cond_row[c3] * p_bb_call;
                            let eq = &self.equity.eq2[c2][c3];
                            p_win_sb += w * eq.win;
                            p_win_bb += w * eq.loss;
                            p_tie_sb_bb += w * eq.tie;
                        }
                    }
                }
            }
            route_2way_showdown(&mut adj, &mut b, row_btn, row_sb, row_bb, s, 1, 2, s2, s3, 0, p_win_sb, p_win_bb, p_tie_sb_bb, conv);

            // ---------------------------------------------------------------
            // Branch 2: BTN Jams
            // ---------------------------------------------------------------
            let k = s;
            let mut order = [0usize, 1, 2];
            order.sort_unstable_by_key(|&i| k[i]);
            let p_min = order[0];
            let p_mid = order[1];
            let p_max = order[2];

            let m_min = k[p_min];
            let m_mid = k[p_mid];
            let m_max = k[p_max];

            let refund = m_max - m_mid;
            let side_pot = 2 * (m_mid - m_min);
            let main_pot = 3 * m_min;

            let mut c1_mid = [0u8; 3];
            c1_mid[p_max] += refund;
            if side_pot > 0 { c1_mid[p_mid] += side_pot; }
            c1_mid[0] += main_pot;

            let mut c1_max = [0u8; 3];
            c1_max[p_max] += refund;
            if side_pot > 0 { c1_max[p_max] += side_pot; }
            c1_max[0] += main_pot;

            let mut c2_mid = [0u8; 3];
            c2_mid[p_max] += refund;
            if side_pot > 0 { c2_mid[p_mid] += side_pot; }
            c2_mid[1] += main_pot;

            let mut c2_max = [0u8; 3];
            c2_max[p_max] += refund;
            if side_pot > 0 { c2_max[p_max] += side_pot; }
            c2_max[1] += main_pot;

            let mut c3_mid = [0u8; 3];
            c3_mid[p_max] += refund;
            if side_pot > 0 { c3_mid[p_mid] += side_pot; }
            c3_mid[2] += main_pot;

            let mut c3_max = [0u8; 3];
            c3_max[p_max] += refund;
            if side_pot > 0 { c3_max[p_max] += side_pot; }
            c3_max[2] += main_pot;

            let mut w_1_mid = 0.0f64;
            let mut w_1_max = 0.0f64;
            let mut w_2_mid = 0.0f64;
            let mut w_2_max = 0.0f64;
            let mut w_3_mid = 0.0f64;
            let mut w_3_max = 0.0f64;

            for c1 in 0..169 {
                let w_btn_j = p_c1[c1] * strat.btn_jam[c1];
                if w_btn_j <= 0.0 {
                    continue;
                }

                let cond_c1 = &self.cards.cond_prob_2[c1];

                let mut p_sb_fold_given_c1 = 0.0f64;
                if s2 > 1 {
                    for c2 in 0..169 {
                        p_sb_fold_given_c1 += cond_c1[c2] * (1.0 - strat.sb_call_vs_jam[c2]);
                    }
                }

                // Sub-branch 2.1: SB Folds
                if p_sb_fold_given_c1 > 0.0 {
                    let w_sb_f = w_btn_j * p_sb_fold_given_c1;

                    // (a) BB Folds -> BTN wins blinds
                    if bb_can_fold_jf {
                        let mut p_bb_fold_jf = 0.0f64;
                        for c3 in 0..169 {
                            p_bb_fold_jf += cond_c1[c3] * (1.0 - strat.bb_call_vs_jam_fold[c3]);
                        }
                        if p_bb_fold_jf > 0.0 {
                            let w = w_sb_f * p_bb_fold_jf;
                            let c_end = [s1 + 1 + 2.min(s3), s2 - 1, s3 - 2.min(s3)];
                            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c_end, w, conv);
                        }
                    }

                    // (b) BB Calls -> Showdown BTN vs BB with dead 1 from SB
                    let mut p_win_btn = 0.0f64;
                    let mut p_win_bb = 0.0f64;
                    let mut p_tie_btn_bb = 0.0f64;
                    for c3 in 0..169 {
                        let p_bb_call = if !bb_can_fold_jf { 1.0 } else { strat.bb_call_vs_jam_fold[c3] };
                        if p_bb_call > 0.0 {
                            let w = w_sb_f * cond_c1[c3] * p_bb_call;
                            let eq = &self.equity.eq2[c1][c3];
                            p_win_btn += w * eq.win;
                            p_win_bb += w * eq.loss;
                            p_tie_btn_bb += w * eq.tie;
                        }
                    }
                    route_2way_showdown(&mut adj, &mut b, row_btn, row_sb, row_bb, s, 0, 2, s1, s3, 1, p_win_btn, p_win_bb, p_tie_btn_bb, conv);
                }

                // Sub-branch 2.2: SB Calls
                for c2 in 0..169 {
                    let p_sb_call = if s2 == 1 { 1.0 } else { strat.sb_call_vs_jam[c2] };
                    if p_sb_call > 0.0 {
                        let w_sb_c = w_btn_j * cond_c1[c2] * p_sb_call;

                        // (a) BB Folds -> Showdown BTN vs SB with dead min(2, s3) from BB
                        if bb_can_fold_jc {
                            let mut p_bb_fold_overcall = 0.0f64;
                            for c3 in 0..169 {
                                p_bb_fold_overcall += cond_c1[c3] * (1.0 - strat.bb_overcall[c3]);
                            }
                            if p_bb_fold_overcall > 0.0 {
                                let w = w_sb_c * p_bb_fold_overcall;
                                let eq = &self.equity.eq2[c1][c2];
                                route_2way_showdown(
                                    &mut adj, &mut b, row_btn, row_sb, row_bb, s, 0, 1, s1, s2, 2.min(s3),
                                    w * eq.win, w * eq.loss, w * eq.tie, conv,
                                );
                            }
                        }

                        // (b) BB Overcalls -> 3-way showdown
                        for c3 in 0..169 {
                            let p_bb_overcall = if !bb_can_fold_jc { 1.0 } else { strat.bb_overcall[c3] };
                            if p_bb_overcall > 0.0 {
                                let w = w_sb_c * cond_c1[c3] * p_bb_overcall;
                                let w12 = self.equity.eq2[c1][c2].win;
                                let w13 = self.equity.eq2[c1][c3].win;
                                let w21 = self.equity.eq2[c2][c1].win;
                                let w23 = self.equity.eq2[c2][c3].win;
                                let w31 = self.equity.eq2[c3][c1].win;
                                let w32 = self.equity.eq2[c3][c2].win;

                                let mut p1 = w12 * w13;
                                let mut p2 = w21 * w23;
                                let mut p3 = w31 * w32;
                                let tot = p1 + p2 + p3;
                                if tot > 0.0 {
                                    let inv = 1.0 / tot;
                                    p1 *= inv; p2 *= inv; p3 *= inv;
                                } else {
                                    p1 = 1.0 / 3.0; p2 = 1.0 / 3.0; p3 = 1.0 / 3.0;
                                }

                                if side_pot == 0 || (p_mid == 1 && p_max == 2 && w23 >= w32) || (p_mid == 2 && p_max == 1 && w32 >= w23) {
                                    w_1_mid += w * p1;
                                } else {
                                    w_1_max += w * p1;
                                }

                                if side_pot == 0 || (p_mid == 0 && p_max == 2 && w13 >= w31) || (p_mid == 2 && p_max == 0 && w31 >= w13) {
                                    w_2_mid += w * p2;
                                } else {
                                    w_2_max += w * p2;
                                }

                                if side_pot == 0 || (p_mid == 0 && p_max == 1 && w12 >= w21) || (p_mid == 1 && p_max == 0 && w21 >= w12) {
                                    w_3_mid += w * p3;
                                } else {
                                    w_3_max += w * p3;
                                }
                            }
                        }
                    }
                }
            }

            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c1_mid, w_1_mid, conv);
            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c1_max, w_1_max, conv);
            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c2_mid, w_2_mid, conv);
            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c2_max, w_2_max, conv);
            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c3_mid, w_3_mid, conv);
            route_outcome(&mut adj, &mut b, row_btn, row_sb, row_bb, s, c3_max, w_3_max, conv);
        }

        // Compress adj to unique targets
        let mut compressed_adj = vec![Vec::new(); NUM_POSITION_STATES];
        for i in 0..NUM_POSITION_STATES {
            let mut map = std::collections::HashMap::new();
            for &(target, p) in &adj[i] {
                *map.entry(target).or_insert(0.0) += p;
            }
            compressed_adj[i] = map.into_iter().collect();
        }

        (compressed_adj, b)
    }

    // Solve (I - P) V = b using BiCGSTAB (Biconjugate Gradient Stabilized method)
    // Converges in 20-40 iterations (< 5 ms) to exact residual < 1e-11
    pub fn evaluate_policy(
        &self,
        adj: &[Vec<(usize, f64)>],
        b: &[f64],
        v_init: &[f64],
        max_iters: usize,
        tol: f64,
    ) -> (Vec<f64>, f64) {
        let n = NUM_POSITION_STATES;
        let mat_vec = |x: &[f64], y: &mut [f64]| {
            for i in 0..n {
                let mut p_sum = 0.0;
                for &(j, p) in &adj[i] {
                    p_sum += p * x[j];
                }
                y[i] = x[i] - p_sum;
            }
        };

        let dot = |x: &[f64], y: &[f64]| -> f64 {
            let mut sum = 0.0;
            for i in 0..n {
                sum += x[i] * y[i];
            }
            sum
        };

        let mut x = v_init.to_vec();
        let mut ax = vec![0.0; n];
        mat_vec(&x, &mut ax);

        let mut r = vec![0.0; n];
        for i in 0..n {
            r[i] = b[i] - ax[i];
        }

        let r_hat = r.clone();
        let mut rho_prev = 1.0;
        let mut alpha = 1.0;
        let mut omega = 1.0;

        let mut v = vec![0.0; n];
        let mut p = vec![0.0; n];
        let mut s = vec![0.0; n];
        let mut t = vec![0.0; n];

        for _iter in 0..max_iters {
            let rho = dot(&r_hat, &r);
            if rho.abs() < 1e-35 {
                break;
            }

            if _iter == 0 {
                p.copy_from_slice(&r);
            } else {
                let beta = (rho / rho_prev) * (alpha / omega);
                for i in 0..n {
                    p[i] = r[i] + beta * (p[i] - omega * v[i]);
                }
            }

            mat_vec(&p, &mut v);
            let denom = dot(&r_hat, &v);
            if denom.abs() < 1e-35 {
                break;
            }
            alpha = rho / denom;

            for i in 0..n {
                s[i] = r[i] - alpha * v[i];
            }

            let s_norm = dot(&s, &s).sqrt();
            if s_norm < tol {
                for i in 0..n {
                    x[i] += alpha * p[i];
                }
                break;
            }

            mat_vec(&s, &mut t);
            let t_dot_t = dot(&t, &t);
            if t_dot_t.abs() < 1e-35 {
                omega = 0.0;
            } else {
                omega = dot(&t, &s) / t_dot_t;
            }

            for i in 0..n {
                x[i] += alpha * p[i] + omega * s[i];
                r[i] = s[i] - omega * t[i];
            }

            rho_prev = rho;

            let mut max_diff = 0.0f64;
            for i in 0..n {
                let diff = r[i].abs();
                if diff > max_diff {
                    max_diff = diff;
                }
            }
            if max_diff < tol {
                break;
            }
        }

        // Exact maximum absolute residual ||b - (I - P) x||_inf
        mat_vec(&x, &mut ax);
        let mut max_res = 0.0f64;
        for i in 0..n {
            let diff = (b[i] - ax[i]).abs();
            if diff > max_res {
                max_res = diff;
            }
        }

        (x, max_res)
    }

    pub fn compute_all_state_exploitabilities(
        &self,
        profile: &[StateStrategy],
        conv: EliminationConvention,
        v_base: &[f64],
    ) -> Vec<(f64, usize, [u8; 3], &'static str)> {
        let mut p_c1 = [0.0f64; 169];
        for c1 in 0..169 {
            p_c1[c1] = (self.cards.class_combos[c1].len() as f64) / 1326.0;
        }

        let results: Vec<(f64, usize, [u8; 3], &'static str)> = (0..self.state_table.index_to_stack.len())
            .into_par_iter()
            .map(|v_idx| {
                let (s1, s2, s3) = self.state_table.index_to_stack[v_idx];
                let s = [s1, s2, s3];
                let strat = &profile[v_idx];

                let row_btn = v_idx * 3 + 0;
                let row_sb = v_idx * 3 + 1;
                let row_bb = v_idx * 3 + 2;

                let bb_is_allin = s3 == 1;
                let bb_can_fold_fj = !bb_is_allin && s2 > 2;
                let bb_can_fold_jf = !bb_is_allin && s1 > 2;
                let bb_can_fold_jc = !bb_is_allin && (s1 > 2 || s2 > 2);

                let mut state_max_exploit = 0.0f64;
                let mut state_max_pos = "BTN";

                let leaves_sb_bb = crate::stage::precompute_2way_leaves(1, 2, 0, s, s2, s3, 0, v_base, conv);
                let leaves_btn_bb = crate::stage::precompute_2way_leaves(0, 2, 1, s, s1, s3, 1, v_base, conv);
                let leaves_btn_sb = crate::stage::precompute_2way_leaves(0, 1, 2, s, s1, s2, 2.min(s3), v_base, conv);
                let leaves_3way = crate::stage::precompute_3way_leaves(s, v_base, conv);

                let u_bb_fold_sb_bb = crate::stage::eval_leaf(s1, s2, s3, s1, s2 + 2.min(s3), s3 - 2.min(s3), v_base, conv);
                let u_bb_fold_btn_bb = crate::stage::eval_leaf(s1, s2, s3, s1 + 1 + 2.min(s3), s2 - 1, s3 - 2.min(s3), v_base, conv);
                let u_both_fold = crate::stage::eval_leaf(s1, s2, s3, s1, s2.saturating_sub(1), s3 + 1, v_base, conv);

                // 1. Hero as BTN
                let mut u_btn_f_given_c2 = [0.0f64; 169];
                for c2 in 0..169 {
                    let p_sb_jam = if s2 == 1 { 1.0 } else { strat.sb_jam_vs_fold[c2] };
                    let mut u_sb_jam = 0.0;
                    if p_sb_jam > 0.001 {
                        let cond_c2 = &self.cards.cond_prob_2[c2];
                        for c3 in 0..169 {
                            let p_bb_call = if !bb_can_fold_fj { 1.0 } else { strat.bb_call_vs_fold_jam[c3] };
                            let eq_sb_bb = &self.equity.eq2[c2][c3];
                            let u_sb_bb_sd = eq_sb_bb.win * leaves_sb_bb.0[0] + eq_sb_bb.loss * leaves_sb_bb.1[0] + eq_sb_bb.tie * leaves_sb_bb.2[0];
                            u_sb_jam += cond_c2[c3] * ((1.0 - p_bb_call) * u_bb_fold_sb_bb[0] + p_bb_call * u_sb_bb_sd);
                        }
                    }
                    u_btn_f_given_c2[c2] = (1.0 - p_sb_jam) * u_both_fold[0] + p_sb_jam * u_sb_jam;
                }

                let active_sb_call: Vec<(usize, f64)> = (0..169)
                    .filter_map(|c2| {
                        let p = if s2 == 1 { 1.0 } else { strat.sb_call_vs_jam[c2] };
                        if p > 0.001 { Some((c2, p)) } else { None }
                    })
                    .collect();
                let active_overcall_bb: Vec<(usize, f64)> = (0..169)
                    .filter_map(|c3| {
                        let p = if !bb_can_fold_jc { 1.0 } else { strat.bb_overcall[c3] };
                        if p > 0.001 { Some((c3, p)) } else { None }
                    })
                    .collect();

                let mut v_btn_br = 0.0f64;
                for c1 in 0..169 {
                    let cond_c1 = &self.cards.cond_prob_2[c1];
                    let mut u_fold = 0.0;
                    for c2 in 0..169 {
                        u_fold += cond_c1[c2] * u_btn_f_given_c2[c2];
                    }

                    let mut p_sb_fold_given_c1 = 0.0f64;
                    if s2 > 1 {
                        for c2 in 0..169 {
                            p_sb_fold_given_c1 += cond_c1[c2] * (1.0 - strat.sb_call_vs_jam[c2]);
                        }
                    }

                    let mut u_sb_fold_c1 = 0.0f64;
                    if p_sb_fold_given_c1 > 0.0 {
                        for c3 in 0..169 {
                            let p_bb_call_jf = if !bb_can_fold_jf { 1.0 } else { strat.bb_call_vs_jam_fold[c3] };
                            let eq_btn_bb = &self.equity.eq2[c1][c3];
                            let u_btn_bb = eq_btn_bb.win * leaves_btn_bb.0[0] + eq_btn_bb.loss * leaves_btn_bb.1[0] + eq_btn_bb.tie * leaves_btn_bb.2[0];
                            u_sb_fold_c1 += cond_c1[c3] * ((1.0 - p_bb_call_jf) * u_bb_fold_btn_bb[0] + p_bb_call_jf * u_btn_bb);
                        }
                    }

                    let mut u_sb_call_sum = 0.0f64;
                    for &(c2, p_sb_call) in &active_sb_call {
                        let w_c2 = cond_c1[c2] * p_sb_call;
                        let eq_btn_sb = &self.equity.eq2[c1][c2];
                        let u_btn_sb = eq_btn_sb.win * leaves_btn_sb.0[0] + eq_btn_sb.loss * leaves_btn_sb.1[0] + eq_btn_sb.tie * leaves_btn_sb.2[0];

                        let mut p_overcall_sum = 0.0f64;
                        let mut u_3way_sum = 0.0f64;
                        for &(c3, p_over) in &active_overcall_bb {
                            let p_c3 = cond_c1[c3];
                            let w_over = p_c3 * p_over;
                            p_overcall_sum += w_over;
                            let u_3way = crate::stage::eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[0];
                            u_3way_sum += w_over * u_3way;
                        }
                        let u_call_res = (1.0 - p_overcall_sum).max(0.0) * u_btn_sb + u_3way_sum;
                        u_sb_call_sum += w_c2 * u_call_res;
                    }

                    let u_jam = p_sb_fold_given_c1 * u_sb_fold_c1 + u_sb_call_sum;
                    let u_best = u_jam.max(u_fold);
                    v_btn_br += p_c1[c1] * u_best;
                }

                let exploit_btn = (v_btn_br - v_base[row_btn]).max(0.0);
                if exploit_btn > state_max_exploit {
                    state_max_exploit = exploit_btn;
                    state_max_pos = "BTN";
                }

                // 2. Hero as SB
                let mut v_sb_br = 0.0f64;
                let mut u_sb_jam_vs_fold = [0.0f64; 169];
                for c2 in 0..169 {
                    let cond_c2 = &self.cards.cond_prob_2[c2];
                    for c3 in 0..169 {
                        let p_call = if !bb_can_fold_fj { 1.0 } else { strat.bb_call_vs_fold_jam[c3] };
                        let eq = &self.equity.eq2[c2][c3];
                        let u_bb_call = eq.win * leaves_sb_bb.0[1] + eq.loss * leaves_sb_bb.1[1] + eq.tie * leaves_sb_bb.2[1];
                        u_sb_jam_vs_fold[c2] += cond_c2[c3] * ((1.0 - p_call) * u_bb_fold_sb_bb[1] + p_call * u_bb_call);
                    }
                }

                let mut sb_fold_payoff_given_c1 = [0.0f64; 169];
                for c1 in 0..169 {
                    if strat.btn_jam[c1] > 0.001 {
                        let cond_c1 = &self.cards.cond_prob_2[c1];
                        let mut exp_p = 0.0;
                        for c3 in 0..169 {
                            let p_bb_call_jf = if !bb_can_fold_jf { 1.0 } else { strat.bb_call_vs_jam_fold[c3] };
                            let eq_btn_bb = &self.equity.eq2[c1][c3];
                            let u_btn_bb = eq_btn_bb.win * leaves_btn_bb.0[1] + eq_btn_bb.loss * leaves_btn_bb.1[1] + eq_btn_bb.tie * leaves_btn_bb.2[1];
                            exp_p += cond_c1[c3] * ((1.0 - p_bb_call_jf) * u_bb_fold_btn_bb[1] + p_bb_call_jf * u_btn_bb);
                        }
                        sb_fold_payoff_given_c1[c1] = exp_p;
                    }
                }

                let active_btn_jam: Vec<(usize, f64)> = (0..169)
                    .filter(|&c1| strat.btn_jam[c1] > 0.001)
                    .map(|c1| (c1, strat.btn_jam[c1]))
                    .collect();

                for c2 in 0..169 {
                    let cond_c2 = &self.cards.cond_prob_2[c2];
                    let mut p_btn_fold_given_c2 = 0.0;
                    for c1 in 0..169 {
                        p_btn_fold_given_c2 += cond_c2[c1] * (1.0 - strat.btn_jam[c1]);
                    }

                    let u_best_vs_fold = if s2 == 1 {
                        u_sb_jam_vs_fold[c2]
                    } else {
                        u_sb_jam_vs_fold[c2].max(u_both_fold[1])
                    };

                    let mut u_fold_vs_jam = 0.0;
                    let mut u_call_vs_jam = 0.0;
                    let mut w_jam_sum = 0.0;
                    for &(c1, p_btn_jam) in &active_btn_jam {
                        let w = cond_c2[c1] * p_btn_jam;
                        w_jam_sum += w;
                        u_fold_vs_jam += w * sb_fold_payoff_given_c1[c1];

                        let eq_btn_sb = &self.equity.eq2[c1][c2];
                        let u_btn_sb = eq_btn_sb.win * leaves_btn_sb.0[1] + eq_btn_sb.loss * leaves_btn_sb.1[1] + eq_btn_sb.tie * leaves_btn_sb.2[1];

                        let cond_c1 = &self.cards.cond_prob_2[c1];
                        let mut p_overcall_sum = 0.0;
                        let mut u_3way_sum = 0.0;
                        for &(c3, p_over) in &active_overcall_bb {
                            let p_c3 = cond_c1[c3];
                            let w_over = p_c3 * p_over;
                            p_overcall_sum += w_over;
                            let u_3way = crate::stage::eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[1];
                            u_3way_sum += w_over * u_3way;
                        }
                        let u_call_c1 = (1.0 - p_overcall_sum).max(0.0) * u_btn_sb + u_3way_sum;
                        u_call_vs_jam += w * u_call_c1;
                    }

                    let u_best_vs_jam = if s2 == 1 {
                        if w_jam_sum > 0.0 { u_call_vs_jam / w_jam_sum } else { 0.0 }
                    } else if w_jam_sum > 0.0 {
                        (u_call_vs_jam / w_jam_sum).max(u_fold_vs_jam / w_jam_sum)
                    } else {
                        0.0
                    };

                    v_sb_br += p_c1[c2] * (p_btn_fold_given_c2 * u_best_vs_fold + w_jam_sum * u_best_vs_jam);
                }

                let exploit_sb = (v_sb_br - v_base[row_sb]).max(0.0);
                if exploit_sb > state_max_exploit {
                    state_max_exploit = exploit_sb;
                    state_max_pos = "SB";
                }

                // 3. Hero as BB
                if !bb_is_allin {
                    let mut v_bb_br = 0.0f64;

                    for c3 in 0..169 {
                        let cond_c3 = &self.cards.cond_prob_2[c3];

                        // Situation 1: BTN folds
                        let mut p_btn_fold = 0.0f64;
                        for c1 in 0..169 {
                            p_btn_fold += cond_c3[c1] * (1.0 - strat.btn_jam[c1]);
                        }

                        let mut w_sb_jam = 0.0f64;
                        let mut w_sb_fold = 0.0f64;
                        let mut u_call_vs_sb_jam = 0.0f64;
                        for c2 in 0..169 {
                            let p = cond_c3[c2];
                            let jam = if s2 == 1 { 1.0 } else { strat.sb_jam_vs_fold[c2] };
                            w_sb_jam += p * jam;
                            w_sb_fold += p * (1.0 - jam);

                            if jam > 0.0 {
                                let eq = &self.equity.eq2[c2][c3];
                                let u_sd = eq.win * leaves_sb_bb.0[2] + eq.loss * leaves_sb_bb.1[2] + eq.tie * leaves_sb_bb.2[2];
                                u_call_vs_sb_jam += p * jam * u_sd;
                            }
                        }

                        let u_best_vs_sb_jam = if w_sb_jam > 0.0 {
                            let u_c = u_call_vs_sb_jam / w_sb_jam;
                            if bb_can_fold_fj { u_c.max(u_bb_fold_sb_bb[2]) } else { u_c }
                        } else {
                            u_bb_fold_sb_bb[2]
                        };

                        let val_if_btn_folds = w_sb_fold * u_both_fold[2] + w_sb_jam * u_best_vs_sb_jam;

                        // Situation 2: BTN jams
                        let mut w_btn_jam_sb_fold = 0.0f64;
                        let mut u_call_vs_btn_jam_sb_fold = 0.0f64;

                        let mut w_btn_jam_sb_call = 0.0f64;
                        let mut u_fold_vs_btn_jam_sb_call = 0.0f64;
                        let mut u_call_vs_btn_jam_sb_call = 0.0f64;

                        for c1 in 0..169 {
                            let p1 = strat.btn_jam[c1];
                            if p1 > 0.0001 {
                                let w1 = cond_c3[c1] * p1;
                                let eq_btn_bb = &self.equity.eq2[c1][c3];
                                let u_btn_bb_sd = eq_btn_bb.win * leaves_btn_bb.0[2] + eq_btn_bb.loss * leaves_btn_bb.1[2] + eq_btn_bb.tie * leaves_btn_bb.2[2];

                                for c2 in 0..169 {
                                    let p2_call = if s2 == 1 { 1.0 } else { strat.sb_call_vs_jam[c2] };
                                    let w12 = w1 * cond_c3[c2];

                                    // Subcase 2a: SB folds
                                    let w_f = w12 * (1.0 - p2_call);
                                    w_btn_jam_sb_fold += w_f;
                                    u_call_vs_btn_jam_sb_fold += w_f * u_btn_bb_sd;

                                    // Subcase 2b: SB calls
                                    if p2_call > 0.0001 {
                                        let w_c = w12 * p2_call;
                                        w_btn_jam_sb_call += w_c;

                                        let eq_btn_sb = &self.equity.eq2[c1][c2];
                                        let u_f = eq_btn_sb.win * leaves_btn_sb.0[2] + eq_btn_sb.loss * leaves_btn_sb.1[2] + eq_btn_sb.tie * leaves_btn_sb.2[2];
                                        u_fold_vs_btn_jam_sb_call += w_c * u_f;

                                        let u_3w = crate::stage::eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[2];
                                        u_call_vs_btn_jam_sb_call += w_c * u_3w;
                                    }
                                }
                            }
                        }

                        let u_best_vs_btn_jam_sb_fold = if w_btn_jam_sb_fold > 0.0 {
                            let u_c = u_call_vs_btn_jam_sb_fold / w_btn_jam_sb_fold;
                            if bb_can_fold_jf { u_c.max(u_bb_fold_btn_bb[2]) } else { u_c }
                        } else {
                            u_bb_fold_btn_bb[2]
                        };

                        let u_best_vs_btn_jam_sb_call = if w_btn_jam_sb_call > 0.0 {
                            let u_c = u_call_vs_btn_jam_sb_call / w_btn_jam_sb_call;
                            let u_f = u_fold_vs_btn_jam_sb_call / w_btn_jam_sb_call;
                            if bb_can_fold_jc { u_c.max(u_f) } else { u_c }
                        } else {
                            0.0
                        };

                        let val_if_btn_jams = w_btn_jam_sb_fold * u_best_vs_btn_jam_sb_fold + w_btn_jam_sb_call * u_best_vs_btn_jam_sb_call;

                        let u_best_c3 = p_btn_fold * val_if_btn_folds + val_if_btn_jams;
                        v_bb_br += p_c1[c3] * u_best_c3;
                    }

                    let exploit_bb = (v_bb_br - v_base[row_bb]).max(0.0);
                    if exploit_bb > state_max_exploit {
                        state_max_exploit = exploit_bb;
                        state_max_pos = "BB";
                    }
                }

                (state_max_exploit, v_idx, s, state_max_pos)
            })
            .collect();
        results
    }

    pub fn compute_exploitability_with_v(
        &self,
        profile: &[StateStrategy],
        conv: EliminationConvention,
        v_base: &[f64],
    ) -> (f64, usize, [u8; 3], &'static str) {
        let results = self.compute_all_state_exploitabilities(profile, conv, v_base);

        let mut max_exploit = 0.0f64;
        let mut max_state_idx = 0;
        let mut max_stack = [0u8; 3];
        let mut max_pos = "BTN";

        for (exp, idx, stk, pos) in results {
            if exp > max_exploit {
                max_exploit = exp;
                max_state_idx = idx;
                max_stack = stk;
                max_pos = pos;
            }
        }

        (max_exploit, max_state_idx, max_stack, max_pos)
    }

    pub fn compute_exploitability(
        &self,
        profile: &[StateStrategy],
        conv: EliminationConvention,
    ) -> (f64, Vec<f64>, usize, [u8; 3], &'static str) {
        let (adj, b) = self.build_system(profile, &vec![0.0; NUM_POSITION_STATES], conv);
        let (v_base, _) = self.evaluate_policy(&adj, &b, &b, 5000, 1e-9);
        let (max_exploit, max_state_idx, max_stack, max_pos) = self.compute_exploitability_with_v(profile, conv, &v_base);
        (max_exploit, v_base, max_state_idx, max_stack, max_pos)
    }
}
