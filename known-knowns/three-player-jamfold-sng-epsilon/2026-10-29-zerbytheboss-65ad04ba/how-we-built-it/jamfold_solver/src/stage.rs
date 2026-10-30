// Stage game logic and CFR+ solver for 3-player Jam/Fold SnG
use crate::cards::{CardTables, NUM_HAND_CLASSES};
use crate::equity::EquityEngine;
use crate::eval::Evaluator;
use crate::state::{icm_2player, stack_to_index, TOTAL_CHIPS};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EliminationConvention {
    ChipRank,   // Convention (i): starting chip priority (30/20, or 25/25 on tie)
    EqualSplit, // Convention (ii): equal split (25/25)
}

#[derive(Debug, Clone)]
pub struct StateStrategy {
    pub btn_jam: [f64; NUM_HAND_CLASSES],
    pub sb_jam_vs_fold: [f64; NUM_HAND_CLASSES],
    pub sb_call_vs_jam: [f64; NUM_HAND_CLASSES],
    pub bb_call_vs_fold_jam: [f64; NUM_HAND_CLASSES],
    pub bb_call_vs_jam_fold: [f64; NUM_HAND_CLASSES],
    pub bb_overcall: [f64; NUM_HAND_CLASSES],
}

impl Default for StateStrategy {
    fn default() -> Self {
        StateStrategy {
            btn_jam: [0.0; NUM_HAND_CLASSES],
            sb_jam_vs_fold: [0.0; NUM_HAND_CLASSES],
            sb_call_vs_jam: [0.0; NUM_HAND_CLASSES],
            bb_call_vs_fold_jam: [0.0; NUM_HAND_CLASSES],
            bb_call_vs_jam_fold: [0.0; NUM_HAND_CLASSES],
            bb_overcall: [0.0; NUM_HAND_CLASSES],
        }
    }
}

// Leaf payoff evaluation:
// Given starting stacks (s1, s2, s3), end-of-hand chip counts (c1, c2, c3),
// continuation values V (size 2838), and elimination convention.
// Returns (u_btn, u_sb, u_bb).
#[inline(always)]
pub fn eval_leaf(
    s1: u8, s2: u8, s3: u8,
    c1: u8, c2: u8, c3: u8,
    v: &[f64],
    conv: EliminationConvention,
) -> [f64; 3] {
    let mut u = [0.0; 3];
    let num_busted = (c1 == 0) as u8 + (c2 == 0) as u8 + (c3 == 0) as u8;

    match num_busted {
        0 => {
            // Non-terminal transition: rotate clockwise
            // Previous SB (c2) is now BTN
            // Previous BB (c3) is now SB
            // Previous BTN (c1) is now BB
            let s_prime_idx = stack_to_index(c2, c3, c1);
            let base = s_prime_idx * 3;
            u[0] = v[base + 2]; // BTN is now BB
            u[1] = v[base + 0]; // SB is now BTN
            u[2] = v[base + 1]; // BB is now SB
        }
        1 => {
            // Exactly 1 player eliminated
            if c1 == 0 {
                u[0] = 20.0;
                u[1] = icm_2player(c2, c3);
                u[2] = icm_2player(c3, c2);
            } else if c2 == 0 {
                u[1] = 20.0;
                u[0] = icm_2player(c1, c3);
                u[2] = icm_2player(c3, c1);
            } else {
                u[2] = 20.0;
                u[0] = icm_2player(c1, c2);
                u[1] = icm_2player(c2, c1);
            }
        }
        2 => {
            // 2 players eliminated in the same hand!
            // Winner gets $50
            if c1 == TOTAL_CHIPS {
                u[0] = 50.0;
                match conv {
                    EliminationConvention::ChipRank => {
                        if s2 > s3 { u[1] = 30.0; u[2] = 20.0; }
                        else if s3 > s2 { u[1] = 20.0; u[2] = 30.0; }
                        else { u[1] = 25.0; u[2] = 25.0; }
                    }
                    EliminationConvention::EqualSplit => {
                        u[1] = 25.0; u[2] = 25.0;
                    }
                }
            } else if c2 == TOTAL_CHIPS {
                u[1] = 50.0;
                match conv {
                    EliminationConvention::ChipRank => {
                        if s1 > s3 { u[0] = 30.0; u[2] = 20.0; }
                        else if s3 > s1 { u[0] = 20.0; u[2] = 30.0; }
                        else { u[0] = 25.0; u[2] = 25.0; }
                    }
                    EliminationConvention::EqualSplit => {
                        u[0] = 25.0; u[2] = 25.0;
                    }
                }
            } else {
                u[2] = 50.0;
                match conv {
                    EliminationConvention::ChipRank => {
                        if s1 > s2 { u[0] = 30.0; u[1] = 20.0; }
                        else if s2 > s1 { u[0] = 20.0; u[1] = 30.0; }
                        else { u[0] = 25.0; u[1] = 25.0; }
                    }
                    EliminationConvention::EqualSplit => {
                        u[0] = 25.0; u[1] = 25.0;
                    }
                }
            }
        }
        _ => unreachable!(),
    }
    u
}

// 2-way showdown leaf evaluation between Player A and Player B, with dead money from Player C.
// Player A has committed k_a, Player B has committed k_b.
// Dead money from C is dead_c.
// Total pot = 2 * min(k_a, k_b) + dead_c.
// Excess chips |k_a - k_b| refunded.
// If pot has an odd 1-chip unit, split 50/50.
#[inline(always)]
pub fn precompute_2way_leaves(
    p_a: usize, p_b: usize, p_c: usize,
    s: [u8; 3],
    k_a: u8, k_b: u8, dead_c: u8,
    v: &[f64],
    conv: EliminationConvention,
) -> ([f64; 3], [f64; 3], [f64; 3]) {
    let m = k_a.min(k_b);
    let mut c_win_a = s;
    c_win_a[p_a] = s[p_a] - k_a + 2 * m + dead_c;
    c_win_a[p_b] = s[p_b] - k_b + (k_b - m);
    c_win_a[p_c] = s[p_c] - dead_c;
    let u_a = eval_leaf(s[0], s[1], s[2], c_win_a[0], c_win_a[1], c_win_a[2], v, conv);

    let mut c_win_b = s;
    c_win_b[p_a] = s[p_a] - k_a + (k_a - m);
    c_win_b[p_b] = s[p_b] - k_b + 2 * m + dead_c;
    c_win_b[p_c] = s[p_c] - dead_c;
    let u_b = eval_leaf(s[0], s[1], s[2], c_win_b[0], c_win_b[1], c_win_b[2], v, conv);

    let pot = 2 * m + dead_c;
    let u_tie = if pot % 2 == 0 {
        let half = pot / 2;
        let mut c_tie = s;
        c_tie[p_a] = s[p_a] - k_a + half + (k_a - m);
        c_tie[p_b] = s[p_b] - k_b + half + (k_b - m);
        c_tie[p_c] = s[p_c] - dead_c;
        eval_leaf(s[0], s[1], s[2], c_tie[0], c_tie[1], c_tie[2], v, conv)
    } else {
        let half_low = pot / 2;
        let half_high = half_low + 1;
        let mut c_a_odd = s;
        c_a_odd[p_a] = s[p_a] - k_a + half_high + (k_a - m);
        c_a_odd[p_b] = s[p_b] - k_b + half_low + (k_b - m);
        c_a_odd[p_c] = s[p_c] - dead_c;
        let u3a = eval_leaf(s[0], s[1], s[2], c_a_odd[0], c_a_odd[1], c_a_odd[2], v, conv);

        let mut c_b_odd = s;
        c_b_odd[p_a] = s[p_a] - k_a + half_low + (k_a - m);
        c_b_odd[p_b] = s[p_b] - k_b + half_high + (k_b - m);
        c_b_odd[p_c] = s[p_c] - dead_c;
        let u3b = eval_leaf(s[0], s[1], s[2], c_b_odd[0], c_b_odd[1], c_b_odd[2], v, conv);

        [
            0.5 * (u3a[0] + u3b[0]),
            0.5 * (u3a[1] + u3b[1]),
            0.5 * (u3a[2] + u3b[2]),
        ]
    };

    (u_a, u_b, u_tie)
}

pub fn eval_showdown_2way(
    p_a: usize, p_b: usize, p_c: usize,
    s: [u8; 3],
    k_a: u8, k_b: u8, dead_c: u8,
    p_win_a: f64, p_win_b: f64, p_tie: f64,
    v: &[f64],
    conv: EliminationConvention,
) -> [f64; 3] {
    let (u_a, u_b, u_tie) = precompute_2way_leaves(p_a, p_b, p_c, s, k_a, k_b, dead_c, v, conv);
    [
        p_win_a * u_a[0] + p_win_b * u_b[0] + p_tie * u_tie[0],
        p_win_a * u_a[1] + p_win_b * u_b[1] + p_tie * u_tie[1],
        p_win_a * u_a[2] + p_win_b * u_b[2] + p_tie * u_tie[2],
    ]
}
// 3-way showdown leaf evaluation among BTN, SB, BB
pub fn eval_showdown_3way(
    s: [u8; 3], // starting stacks
    dist13: &[f64; 13], // 13 outcome probabilities
    v: &[f64],
    conv: EliminationConvention,
) -> [f64; 3] {
    // Commitments are equal to starting stacks
    let k = s;
    // Determine stack order: sort indices by commitment
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

    let mut expected_u = [0.0; 3];

    // For each of the 13 outcomes, determine winner(s) of main pot and side pot
    // Outcome indices:
    // 0: 0>1>2, 1: 0>2>1, 2: 1>0>2, 3: 1>2>0, 4: 2>0>1, 5: 2>1>0
    // 6: 0=1>2, 7: 0=2>1, 8: 1=2>0
    // 9: 0>1=2, 10: 1>0=2, 11: 2>0=1
    // 12: 0=1=2
    for outcome in 0..13 {
        let prob = dist13[outcome];
        if prob == 0.0 { continue; }

        let mut c_base = [0u8; 3];
        c_base[p_max] += refund;

        // Relative ranks r[0], r[1], r[2]
        let r = match outcome {
            0 => [2, 1, 0],
            1 => [2, 0, 1],
            2 => [1, 2, 0],
            3 => [0, 2, 1],
            4 => [1, 0, 2],
            5 => [0, 1, 2],
            6 => [2, 2, 0],
            7 => [2, 0, 2],
            8 => [0, 2, 2],
            9 => [2, 1, 1],
            10 => [1, 2, 1],
            11 => [1, 1, 2],
            12 => [2, 2, 2],
            _ => unreachable!(),
        };

        // Resolve Side Pot (between p_mid and p_max):
        let mut side_award = [0u8; 3];
        if side_pot > 0 {
            if r[p_mid] > r[p_max] {
                side_award[p_mid] = side_pot;
            } else if r[p_max] > r[p_mid] {
                side_award[p_max] = side_pot;
            } else {
                // Split side pot equally (side_pot is 2*(m_mid - m_min), always even!)
                side_award[p_mid] = side_pot / 2;
                side_award[p_max] = side_pot / 2;
            }
        }

        // Resolve Main Pot (among all 3):
        let max_r = r[0].max(r[1]).max(r[2]);
        let winners: Vec<usize> = (0..3).filter(|&i| r[i] == max_r).collect();

        if winners.len() == 1 {
            let mut c = c_base;
            for i in 0..3 { c[i] += side_award[i]; }
            c[winners[0]] += main_pot;
            let u_leaf = eval_leaf(s[0], s[1], s[2], c[0], c[1], c[2], v, conv);
            for i in 0..3 { expected_u[i] += prob * u_leaf[i]; }
        } else if winners.len() == 2 {
            let w1 = winners[0];
            let w2 = winners[1];
            if main_pot % 2 == 0 {
                let mut c = c_base;
                for i in 0..3 { c[i] += side_award[i]; }
                c[w1] += main_pot / 2;
                c[w2] += main_pot / 2;
                let u_leaf = eval_leaf(s[0], s[1], s[2], c[0], c[1], c[2], v, conv);
                for i in 0..3 { expected_u[i] += prob * u_leaf[i]; }
            } else {
                // Odd pot: split 50/50
                let h_low = main_pot / 2;
                let h_high = h_low + 1;

                let mut c1 = c_base;
                for i in 0..3 { c1[i] += side_award[i]; }
                c1[w1] += h_high; c1[w2] += h_low;
                let u1 = eval_leaf(s[0], s[1], s[2], c1[0], c1[1], c1[2], v, conv);

                let mut c2 = c_base;
                for i in 0..3 { c2[i] += side_award[i]; }
                c2[w1] += h_low; c2[w2] += h_high;
                let u2 = eval_leaf(s[0], s[1], s[2], c2[0], c2[1], c2[2], v, conv);

                for i in 0..3 {
                    expected_u[i] += prob * 0.5 * (u1[i] + u2[i]);
                }
            }
        } else {
            // All 3 tie: main_pot is 3 * m_min, divisible by 3!
            let mut c = c_base;
            for i in 0..3 { c[i] += side_award[i]; }
            c[0] += m_min;
            c[1] += m_min;
            c[2] += m_min;
            let u_leaf = eval_leaf(s[0], s[1], s[2], c[0], c[1], c[2], v, conv);
            for i in 0..3 { expected_u[i] += prob * u_leaf[i]; }
        }
    }

    expected_u
}

#[derive(Debug, Clone, Copy)]
pub struct Showdown3WayLeaves {
    pub p_mid: usize,
    pub p_max: usize,
    pub side_pot: u8,
    pub u1_mid: [f64; 3],
    pub u1_max: [f64; 3],
    pub u2_mid: [f64; 3],
    pub u2_max: [f64; 3],
    pub u3_mid: [f64; 3],
    pub u3_max: [f64; 3],
}

pub fn precompute_3way_leaves(
    s: [u8; 3],
    v: &[f64],
    conv: EliminationConvention,
) -> Showdown3WayLeaves {
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

    // Outcome 1: BTN (0) wins main pot
    let mut c1_mid = [0u8; 3];
    c1_mid[p_max] += refund;
    if side_pot > 0 { c1_mid[p_mid] += side_pot; }
    c1_mid[0] += main_pot;
    let u1_mid = eval_leaf(s[0], s[1], s[2], c1_mid[0], c1_mid[1], c1_mid[2], v, conv);

    let mut c1_max = [0u8; 3];
    c1_max[p_max] += refund;
    if side_pot > 0 { c1_max[p_max] += side_pot; }
    c1_max[0] += main_pot;
    let u1_max = eval_leaf(s[0], s[1], s[2], c1_max[0], c1_max[1], c1_max[2], v, conv);

    // Outcome 2: SB (1) wins main pot
    let mut c2_mid = [0u8; 3];
    c2_mid[p_max] += refund;
    if side_pot > 0 { c2_mid[p_mid] += side_pot; }
    c2_mid[1] += main_pot;
    let u2_mid = eval_leaf(s[0], s[1], s[2], c2_mid[0], c2_mid[1], c2_mid[2], v, conv);

    let mut c2_max = [0u8; 3];
    c2_max[p_max] += refund;
    if side_pot > 0 { c2_max[p_max] += side_pot; }
    c2_max[1] += main_pot;
    let u2_max = eval_leaf(s[0], s[1], s[2], c2_max[0], c2_max[1], c2_max[2], v, conv);

    // Outcome 3: BB (2) wins main pot
    let mut c3_mid = [0u8; 3];
    c3_mid[p_max] += refund;
    if side_pot > 0 { c3_mid[p_mid] += side_pot; }
    c3_mid[2] += main_pot;
    let u3_mid = eval_leaf(s[0], s[1], s[2], c3_mid[0], c3_mid[1], c3_mid[2], v, conv);

    let mut c3_max = [0u8; 3];
    c3_max[p_max] += refund;
    if side_pot > 0 { c3_max[p_max] += side_pot; }
    c3_max[2] += main_pot;
    let u3_max = eval_leaf(s[0], s[1], s[2], c3_max[0], c3_max[1], c3_max[2], v, conv);

    Showdown3WayLeaves {
        p_mid,
        p_max,
        side_pot,
        u1_mid,
        u1_max,
        u2_mid,
        u2_max,
        u3_mid,
        u3_max,
    }
}

#[inline(always)]
pub fn eval_showdown_3way_with_leaves(
    leaves: &Showdown3WayLeaves,
    c1: usize, c2: usize, c3: usize,
    equity: &crate::equity::EquityEngine,
) -> [f64; 3] {
    let w12 = equity.eq2[c1][c2].win;
    let w13 = equity.eq2[c1][c3].win;
    let w21 = equity.eq2[c2][c1].win;
    let w23 = equity.eq2[c2][c3].win;
    let w31 = equity.eq2[c3][c1].win;
    let w32 = equity.eq2[c3][c2].win;

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

    let u1 = if leaves.side_pot == 0 || (leaves.p_mid == 1 && leaves.p_max == 2 && w23 >= w32) || (leaves.p_mid == 2 && leaves.p_max == 1 && w32 >= w23) {
        &leaves.u1_mid
    } else {
        &leaves.u1_max
    };

    let u2 = if leaves.side_pot == 0 || (leaves.p_mid == 0 && leaves.p_max == 2 && w13 >= w31) || (leaves.p_mid == 2 && leaves.p_max == 0 && w31 >= w13) {
        &leaves.u2_mid
    } else {
        &leaves.u2_max
    };

    let u3 = if leaves.side_pot == 0 || (leaves.p_mid == 0 && leaves.p_max == 1 && w12 >= w21) || (leaves.p_mid == 1 && leaves.p_max == 0 && w21 >= w12) {
        &leaves.u3_mid
    } else {
        &leaves.u3_max
    };

    [
        p1 * u1[0] + p2 * u2[0] + p3 * u3[0],
        p1 * u1[1] + p2 * u2[1] + p3 * u3[1],
        p1 * u1[2] + p2 * u2[2] + p3 * u3[2],
    ]
}

pub fn eval_showdown_3way_fast(
    s: [u8; 3],
    c1: usize, c2: usize, c3: usize,
    equity: &crate::equity::EquityEngine,
    v: &[f64],
    conv: EliminationConvention,
) -> [f64; 3] {
    let leaves = precompute_3way_leaves(s, v, conv);
    eval_showdown_3way_with_leaves(&leaves, c1, c2, c3, equity)
}

// Stage game counterfactual value and best response computation

pub struct StageSolver<'a> {
    pub cards: &'a CardTables,
    pub equity: &'a EquityEngine,
    pub eval: &'a Evaluator,
    pub conv: EliminationConvention,
}

impl<'a> StageSolver<'a> {
    pub fn new(
        cards: &'a CardTables,
        equity: &'a EquityEngine,
        eval: &'a Evaluator,
        conv: EliminationConvention,
    ) -> Self {
        StageSolver { cards, equity, eval, conv }
    }

    // Solve stage game at state s = (s1, s2, s3) using CFR+
    pub fn solve_stage(
        &self,
        s1: u8, s2: u8, s3: u8,
        v: &[f64],
        num_iters: usize,
        init_strat: Option<&StateStrategy>,
    ) -> StateStrategy {
        let mut strat = StateStrategy::default();
        let s = [s1, s2, s3];

        // Regret matching+ accumulators
        let mut r_btn_jam = [0.0f64; NUM_HAND_CLASSES];
        let mut r_btn_fold = [0.0f64; NUM_HAND_CLASSES];

        let mut r_sb_j_jam = [0.0f64; NUM_HAND_CLASSES];
        let mut r_sb_j_fold = [0.0f64; NUM_HAND_CLASSES];
        let mut r_sb_c_call = [0.0f64; NUM_HAND_CLASSES];
        let mut r_sb_c_fold = [0.0f64; NUM_HAND_CLASSES];

        let mut r_bb_fj_call = [0.0f64; NUM_HAND_CLASSES];
        let mut r_bb_fj_fold = [0.0f64; NUM_HAND_CLASSES];
        let mut r_bb_jf_call = [0.0f64; NUM_HAND_CLASSES];
        let mut r_bb_jf_fold = [0.0f64; NUM_HAND_CLASSES];
        let mut r_bb_jc_call = [0.0f64; NUM_HAND_CLASSES];
        let mut r_bb_jc_fold = [0.0f64; NUM_HAND_CLASSES];

        // Strategy sum for averaging
        let mut sum_btn_jam = [0.0f64; NUM_HAND_CLASSES];
        let mut sum_sb_j = [0.0f64; NUM_HAND_CLASSES];
        let mut sum_sb_c = [0.0f64; NUM_HAND_CLASSES];
        let mut sum_bb_fj = [0.0f64; NUM_HAND_CLASSES];
        let mut sum_bb_jf = [0.0f64; NUM_HAND_CLASSES];
        let mut sum_bb_jc = [0.0f64; NUM_HAND_CLASSES];

        let bb_is_allin = s3 == 1;
        let bb_can_fold_fj = !bb_is_allin && s2 > 2;
        let bb_can_fold_jf = !bb_is_allin && s1 > 2;
        let bb_can_fold_jc = !bb_is_allin && (s1 > 2 || s2 > 2);

        if let Some(init) = init_strat {
            strat = init.clone();
        } else {
            // Initial default strategy: top 20% hands jam/call
            for c in 0..NUM_HAND_CLASSES {
                let hc = &self.cards.classes[c];
                let is_top = hc.r1 >= 9 || (hc.r1 >= 7 && hc.r2 >= 7);
                strat.btn_jam[c] = if is_top { 1.0 } else { 0.0 };
                strat.sb_jam_vs_fold[c] = if s2 == 1 { 1.0 } else if is_top { 1.0 } else { 0.0 };
                strat.sb_call_vs_jam[c] = if s2 == 1 { 1.0 } else if hc.r1 >= 10 { 1.0 } else { 0.0 };
                strat.bb_call_vs_fold_jam[c] = if !bb_can_fold_fj { 1.0 } else if is_top { 1.0 } else { 0.0 };
                strat.bb_call_vs_jam_fold[c] = if !bb_can_fold_jf { 1.0 } else if hc.r1 >= 10 { 1.0 } else { 0.0 };
                strat.bb_overcall[c] = if !bb_can_fold_jc { 1.0 } else if hc.r1 >= 11 && hc.r2 >= 11 { 1.0 } else { 0.0 };
            }
        }

        // Precompute 2-way showdown outcome leaves for this state:
        let leaves_sb_bb = precompute_2way_leaves(1, 2, 0, s, s2, s3, 0, v, self.conv);
        let leaves_btn_bb = precompute_2way_leaves(0, 2, 1, s, s1, s3, 1, v, self.conv);
        let leaves_btn_sb = precompute_2way_leaves(0, 1, 2, s, s1, s2, 2.min(s3), v, self.conv);
        let leaves_3way = precompute_3way_leaves(s, v, self.conv);

        let u_bb_fold_sb_bb = eval_leaf(s1, s2, s3, s1, s2 + 2.min(s3), s3 - 2.min(s3), v, self.conv);
        let u_bb_fold_btn_bb = eval_leaf(s1, s2, s3, s1 + 1 + 2.min(s3), s2 - 1, s3 - 2.min(s3), v, self.conv);
        let u_both_fold = eval_leaf(s1, s2, s3, s1, s2.saturating_sub(1), s3 + 1, v, self.conv);
        let mut active_btn_sb: Vec<(usize, usize, f64, f64)> = Vec::with_capacity(300);
        let mut active_overcall_bb: Vec<(usize, f64)> = Vec::with_capacity(169);
        let mut active_btn_jam: Vec<(usize, f64)> = Vec::with_capacity(169);
        let mut active_sb_call: Vec<(usize, f64)> = Vec::with_capacity(169);

        for t in 1..=num_iters {
            let weight = t as f64;

            // 1. BB updates
            // Situation A: BTN Fold, SB Jam
            if !bb_can_fold_fj {
                for c3 in 0..NUM_HAND_CLASSES {
                    strat.bb_call_vs_fold_jam[c3] = 1.0;
                    sum_bb_fj[c3] += weight;
                }
            } else {
                let u_fold_a = u_bb_fold_sb_bb[2];
                for c3 in 0..NUM_HAND_CLASSES {
                    let mut u_call_sum = 0.0;
                    let mut w_sum = 0.0;
                    let cond_c3 = &self.cards.cond_prob_2[c3];
                    for c2 in 0..NUM_HAND_CLASSES {
                        let p_sb_jam = strat.sb_jam_vs_fold[c2];
                        if p_sb_jam > 0.0 {
                            let p_c2 = cond_c3[c2];
                            let w = p_c2 * p_sb_jam;
                            w_sum += w;
                            let eq = &self.equity.eq2[c2][c3];
                            let u_sd = eq.win * leaves_sb_bb.0[2] + eq.loss * leaves_sb_bb.1[2] + eq.tie * leaves_sb_bb.2[2];
                            u_call_sum += w * u_sd;
                        }
                    }
                    let u_call = if w_sum > 0.0 { u_call_sum / w_sum } else { u_fold_a };
                    let diff = u_call - u_fold_a;
                    r_bb_fj_call[c3] = (r_bb_fj_call[c3] + diff).max(0.0);
                    r_bb_fj_fold[c3] = (r_bb_fj_fold[c3] - diff).max(0.0);

                    let sum_r = r_bb_fj_call[c3] + r_bb_fj_fold[c3];
                    strat.bb_call_vs_fold_jam[c3] = if sum_r > 0.0 { r_bb_fj_call[c3] / sum_r } else { 0.0 };
                    sum_bb_fj[c3] += weight * strat.bb_call_vs_fold_jam[c3];
                }
            }

            // Situation B: BTN Jam, SB Fold
            if !bb_can_fold_jf {
                for c3 in 0..NUM_HAND_CLASSES {
                    strat.bb_call_vs_jam_fold[c3] = 1.0;
                    sum_bb_jf[c3] += weight;
                }
            } else {
                let u_fold_b = u_bb_fold_btn_bb[2];
                for c3 in 0..NUM_HAND_CLASSES {
                    let mut u_call_sum = 0.0;
                    let mut w_sum = 0.0;
                    let cond_c3 = &self.cards.cond_prob_2[c3];
                    for c1 in 0..NUM_HAND_CLASSES {
                        let p_btn_jam = strat.btn_jam[c1];
                        if p_btn_jam > 0.0 {
                            let p_c1 = cond_c3[c1];
                            let w = p_c1 * p_btn_jam;
                            w_sum += w;
                            let eq = &self.equity.eq2[c1][c3];
                            let u_sd = eq.win * leaves_btn_bb.0[2] + eq.loss * leaves_btn_bb.1[2] + eq.tie * leaves_btn_bb.2[2];
                            u_call_sum += w * u_sd;
                        }
                    }
                    let u_call = if w_sum > 0.0 { u_call_sum / w_sum } else { u_fold_b };
                    let diff = u_call - u_fold_b;
                    r_bb_jf_call[c3] = (r_bb_jf_call[c3] + diff).max(0.0);
                    r_bb_jf_fold[c3] = (r_bb_jf_fold[c3] - diff).max(0.0);

                    let sum_r = r_bb_jf_call[c3] + r_bb_jf_fold[c3];
                    strat.bb_call_vs_jam_fold[c3] = if sum_r > 0.0 { r_bb_jf_call[c3] / sum_r } else { 0.0 };
                    sum_bb_jf[c3] += weight * strat.bb_call_vs_jam_fold[c3];
                }
            }

            // Situation C: BTN Jam, SB Call
            if !bb_can_fold_jc {
                for c3 in 0..NUM_HAND_CLASSES {
                    strat.bb_overcall[c3] = 1.0;
                    sum_bb_jc[c3] += weight;
                }
            } else {
                active_btn_sb.clear();
                for c1 in 0..NUM_HAND_CLASSES {
                    let p1 = strat.btn_jam[c1];
                    if p1 > 0.001 {
                        for c2 in 0..NUM_HAND_CLASSES {
                            let p2 = strat.sb_call_vs_jam[c2];
                            if p2 > 0.001 {
                                let eq_btn_sb = &self.equity.eq2[c1][c2];
                                let u_f = eq_btn_sb.win * leaves_btn_sb.0[2] + eq_btn_sb.loss * leaves_btn_sb.1[2] + eq_btn_sb.tie * leaves_btn_sb.2[2];
                                active_btn_sb.push((c1, c2, p1 * p2, u_f));
                            }
                        }
                    }
                }

                for c3 in 0..NUM_HAND_CLASSES {
                    let mut u_fold_sum = 0.0;
                    let mut u_call_sum = 0.0;
                    let mut w_sum = 0.0;
                    let cond_c3 = &self.cards.cond_prob_2[c3];

                    for &(c1, c2, prod_p, u_f) in &active_btn_sb {
                        let w = cond_c3[c1] * cond_c3[c2] * prod_p;
                        w_sum += w;
                        u_fold_sum += w * u_f;

                        let u_c = eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[2];
                        u_call_sum += w * u_c;
                    }

                    let (u_fold, u_call) = if w_sum > 0.0 {
                        (u_fold_sum / w_sum, u_call_sum / w_sum)
                    } else {
                        (0.0, 0.0)
                    };
                    let diff = u_call - u_fold;
                    r_bb_jc_call[c3] = (r_bb_jc_call[c3] + diff).max(0.0);
                    r_bb_jc_fold[c3] = (r_bb_jc_fold[c3] - diff).max(0.0);

                    let sum_r = r_bb_jc_call[c3] + r_bb_jc_fold[c3];
                    strat.bb_overcall[c3] = if sum_r > 0.0 { r_bb_jc_call[c3] / sum_r } else { 0.0 };
                    sum_bb_jc[c3] += weight * strat.bb_overcall[c3];
                }
            }

            // 2. SB updates
            // Situation 1: BTN Fold
            if s2 == 1 {
                for c2 in 0..NUM_HAND_CLASSES {
                    strat.sb_jam_vs_fold[c2] = 1.0;
                    sum_sb_j[c2] += weight;
                }
            } else {
                let u_both_fold_sb = u_both_fold[1];
                let u_bb_fold_sb = u_bb_fold_sb_bb[1];
                for c2 in 0..NUM_HAND_CLASSES {
                    let u_fold = u_both_fold_sb;
                    let mut u_jam_sum = 0.0;
                    let cond_c2 = &self.cards.cond_prob_2[c2];
                    for c3 in 0..NUM_HAND_CLASSES {
                        let p_c3 = cond_c2[c3];
                        let p_call = strat.bb_call_vs_fold_jam[c3];
                        let eq = &self.equity.eq2[c2][c3];
                        let u_bb_call = eq.win * leaves_sb_bb.0[1] + eq.loss * leaves_sb_bb.1[1] + eq.tie * leaves_sb_bb.2[1];
                        u_jam_sum += p_c3 * ((1.0 - p_call) * u_bb_fold_sb + p_call * u_bb_call);
                    }
                    let diff = u_jam_sum - u_fold;
                    r_sb_j_jam[c2] = (r_sb_j_jam[c2] + diff).max(0.0);
                    r_sb_j_fold[c2] = (r_sb_j_fold[c2] - diff).max(0.0);

                    let sum_r = r_sb_j_jam[c2] + r_sb_j_fold[c2];
                    strat.sb_jam_vs_fold[c2] = if sum_r > 0.0 { r_sb_j_jam[c2] / sum_r } else { 0.0 };
                    sum_sb_j[c2] += weight * strat.sb_jam_vs_fold[c2];
                }
            }

            // Situation 2: BTN Jam
            if s2 == 1 {
                for c2 in 0..NUM_HAND_CLASSES {
                    strat.sb_call_vs_jam[c2] = 1.0;
                    sum_sb_c[c2] += weight;
                }
            } else {
                let u_btn_wins_sb = u_bb_fold_btn_bb[1];
                let mut sb_fold_payoff_given_c1 = [0.0f64; NUM_HAND_CLASSES];
                for c1 in 0..NUM_HAND_CLASSES {
                    if strat.btn_jam[c1] > 0.001 {
                        let cond_c1 = &self.cards.cond_prob_2[c1];
                        let mut exp_p = 0.0;
                        for c3 in 0..NUM_HAND_CLASSES {
                            let p_bb_call_jf = strat.bb_call_vs_jam_fold[c3];
                            let eq_btn_bb = &self.equity.eq2[c1][c3];
                            let u_btn_bb = eq_btn_bb.win * leaves_btn_bb.0[1] + eq_btn_bb.loss * leaves_btn_bb.1[1] + eq_btn_bb.tie * leaves_btn_bb.2[1];
                            exp_p += cond_c1[c3] * ((1.0 - p_bb_call_jf) * u_btn_wins_sb + p_bb_call_jf * u_btn_bb);
                        }
                        sb_fold_payoff_given_c1[c1] = exp_p;
                    }
                }

                active_overcall_bb.clear();
                for c3 in 0..NUM_HAND_CLASSES {
                    if strat.bb_overcall[c3] > 0.001 {
                        active_overcall_bb.push((c3, strat.bb_overcall[c3]));
                    }
                }

                active_btn_jam.clear();
                for c1 in 0..NUM_HAND_CLASSES {
                    if strat.btn_jam[c1] > 0.001 {
                        active_btn_jam.push((c1, strat.btn_jam[c1]));
                    }
                }

                for c2 in 0..NUM_HAND_CLASSES {
                    let mut u_fold_sum = 0.0;
                    let mut u_call_sum = 0.0;
                    let mut w_sum = 0.0;
                    let cond_c2 = &self.cards.cond_prob_2[c2];

                    for &(c1, p_btn_jam) in &active_btn_jam {
                        let p_c1 = cond_c2[c1];
                        let w = p_c1 * p_btn_jam;
                        w_sum += w;
                        u_fold_sum += w * sb_fold_payoff_given_c1[c1];

                        let eq_btn_sb = &self.equity.eq2[c1][c2];
                        let u_btn_sb = eq_btn_sb.win * leaves_btn_sb.0[1] + eq_btn_sb.loss * leaves_btn_sb.1[1] + eq_btn_sb.tie * leaves_btn_sb.2[1];

                        let cond_c1 = &self.cards.cond_prob_2[c1];
                        let mut p_overcall_sum = 0.0;
                        let mut u_3way_sum = 0.0;
                        for &(c3, p_over) in &active_overcall_bb {
                            let p_c3 = cond_c1[c3];
                            let w_over = p_c3 * p_over;
                            p_overcall_sum += w_over;
                            let u_3way = eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[1];
                            u_3way_sum += w_over * u_3way;
                        }
                        let u_call_c1 = (1.0 - p_overcall_sum).max(0.0) * u_btn_sb + u_3way_sum;
                        u_call_sum += w * u_call_c1;
                    }

                    let (u_fold, u_call) = if w_sum > 0.0 {
                        (u_fold_sum / w_sum, u_call_sum / w_sum)
                    } else {
                        (0.0, 0.0)
                    };
                    let diff = u_call - u_fold;
                    r_sb_c_call[c2] = (r_sb_c_call[c2] + diff).max(0.0);
                    r_sb_c_fold[c2] = (r_sb_c_fold[c2] - diff).max(0.0);

                    let sum_r = r_sb_c_call[c2] + r_sb_c_fold[c2];
                    strat.sb_call_vs_jam[c2] = if sum_r > 0.0 { r_sb_c_call[c2] / sum_r } else { 0.0 };
                    sum_sb_c[c2] += weight * strat.sb_call_vs_jam[c2];
                }
            }

            // 3. BTN updates
            let mut u_btn_f_given_c2 = [0.0f64; NUM_HAND_CLASSES];
            let u_both_fold_btn = u_both_fold[0];
            let u_bb_folds_to_sb_btn = u_bb_fold_sb_bb[0];
            for c2 in 0..NUM_HAND_CLASSES {
                let p_sb_jam = strat.sb_jam_vs_fold[c2];
                let mut u_sb_jam = 0.0;
                if p_sb_jam > 0.001 {
                    let cond_c2 = &self.cards.cond_prob_2[c2];
                    for c3 in 0..NUM_HAND_CLASSES {
                        let p_bb_call = strat.bb_call_vs_fold_jam[c3];
                        let eq_sb_bb = &self.equity.eq2[c2][c3];
                        let u_sb_bb_sd = eq_sb_bb.win * leaves_sb_bb.0[0] + eq_sb_bb.loss * leaves_sb_bb.1[0] + eq_sb_bb.tie * leaves_sb_bb.2[0];
                        u_sb_jam += cond_c2[c3] * ((1.0 - p_bb_call) * u_bb_folds_to_sb_btn + p_bb_call * u_sb_bb_sd);
                    }
                }
                u_btn_f_given_c2[c2] = (1.0 - p_sb_jam) * u_both_fold_btn + p_sb_jam * u_sb_jam;
            }

            let u_btn_wins_btn = u_bb_fold_btn_bb[0];
            active_sb_call.clear();
            for c2 in 0..NUM_HAND_CLASSES {
                if strat.sb_call_vs_jam[c2] > 0.001 {
                    active_sb_call.push((c2, strat.sb_call_vs_jam[c2]));
                }
            }

            active_overcall_bb.clear();
            for c3 in 0..NUM_HAND_CLASSES {
                if strat.bb_overcall[c3] > 0.001 {
                    active_overcall_bb.push((c3, strat.bb_overcall[c3]));
                }
            }

            for c1 in 0..NUM_HAND_CLASSES {
                let cond_c1 = &self.cards.cond_prob_2[c1];

                // BTN folds:
                let mut u_fold_sum = 0.0;
                for c2 in 0..NUM_HAND_CLASSES {
                    u_fold_sum += cond_c1[c2] * u_btn_f_given_c2[c2];
                }

                // BTN jams:
                // Sub-case A: SB folds
                let mut p_sb_fold_given_c1 = 0.0f64;
                for c2 in 0..NUM_HAND_CLASSES {
                    p_sb_fold_given_c1 += cond_c1[c2] * (1.0 - strat.sb_call_vs_jam[c2]);
                }

                let mut u_sb_fold_c1 = 0.0f64;
                if p_sb_fold_given_c1 > 0.0 {
                    for c3 in 0..NUM_HAND_CLASSES {
                        let p_bb_call_jf = strat.bb_call_vs_jam_fold[c3];
                        let eq_btn_bb = &self.equity.eq2[c1][c3];
                        let u_btn_bb = eq_btn_bb.win * leaves_btn_bb.0[0] + eq_btn_bb.loss * leaves_btn_bb.1[0] + eq_btn_bb.tie * leaves_btn_bb.2[0];
                        u_sb_fold_c1 += cond_c1[c3] * ((1.0 - p_bb_call_jf) * u_btn_wins_btn + p_bb_call_jf * u_btn_bb);
                    }
                }

                // Sub-case B: SB calls
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
                        let u_3way = eval_showdown_3way_with_leaves(&leaves_3way, c1, c2, c3, self.equity)[0];
                        u_3way_sum += w_over * u_3way;
                    }
                    let u_call_res = (1.0 - p_overcall_sum).max(0.0) * u_btn_sb + u_3way_sum;
                    u_sb_call_sum += w_c2 * u_call_res;
                }

                let u_jam_sum = p_sb_fold_given_c1 * u_sb_fold_c1 + u_sb_call_sum;

                let diff = u_jam_sum - u_fold_sum;
                r_btn_jam[c1] = (r_btn_jam[c1] + diff).max(0.0);
                r_btn_fold[c1] = (r_btn_fold[c1] - diff).max(0.0);

                let sum_r = r_btn_jam[c1] + r_btn_fold[c1];
                strat.btn_jam[c1] = if sum_r > 0.0 { r_btn_jam[c1] / sum_r } else { 0.0 };
                sum_btn_jam[c1] += weight * strat.btn_jam[c1];
            }
        }

        // Return time-averaged strategy
        let total_w = (num_iters * (num_iters + 1) / 2) as f64;
        let mut final_strat = StateStrategy::default();
        for c in 0..NUM_HAND_CLASSES {
            final_strat.btn_jam[c] = (sum_btn_jam[c] / total_w).clamp(0.0, 1.0);
            final_strat.sb_jam_vs_fold[c] = (sum_sb_j[c] / total_w).clamp(0.0, 1.0);
            final_strat.sb_call_vs_jam[c] = (sum_sb_c[c] / total_w).clamp(0.0, 1.0);
            final_strat.bb_call_vs_fold_jam[c] = (sum_bb_fj[c] / total_w).clamp(0.0, 1.0);
            final_strat.bb_call_vs_jam_fold[c] = (sum_bb_jf[c] / total_w).clamp(0.0, 1.0);
            final_strat.bb_overcall[c] = (sum_bb_jc[c] / total_w).clamp(0.0, 1.0);
        }
        final_strat
    }
}
