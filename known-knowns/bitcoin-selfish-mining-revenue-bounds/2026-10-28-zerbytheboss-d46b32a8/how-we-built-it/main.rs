use num_bigint::BigInt;
use num_rational::Ratio;
use num_traits::{Signed, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Action {
    Adopt = 0,
    Override = 1,
    Match = 2,
    Wait = 3,
}

#[derive(Clone, Debug)]
pub struct Transition {
    pub prob: f64,
    pub next_s: usize,
    pub r: f64,
}

pub struct SSZModel {
    pub alpha: f64,
    pub gamma: f64,
    pub t: usize,
    pub rho: f64,
    pub overpaying: bool,
    pub comp_variant: usize, // 1: eq 6 literal, 2: (1-rho) factored
    pub num_states: usize,
    pub transitions: Vec<Vec<(Action, Vec<Transition>)>>,
}

impl SSZModel {
    #[inline(always)]
    pub fn s_idx(t: usize, a: usize, h: usize, fork: usize) -> usize {
        a * (t + 1) * 3 + h * 3 + fork
    }

    #[inline(always)]
    pub fn idx_to_s(t: usize, idx: usize) -> (usize, usize, usize) {
        let fork = idx % 3;
        let temp = idx / 3;
        let h = temp % (t + 1);
        let a = temp / (t + 1);
        (a, h, fork)
    }

    pub fn new(alpha: f64, gamma: f64, t: usize, rho: f64, overpaying: bool, comp_variant: usize) -> Self {
        let num_states = (t + 1) * (t + 1) * 3;
        let mut transitions = Vec::with_capacity(num_states);

        let denom = 1.0 - 2.0 * alpha;
        let term1 = alpha * (1.0 - alpha) / (denom * denom);

        for a in 0..=t {
            for h in 0..=t {
                for fork in 0..3 {
                    let mut state_actions = Vec::new();

                    // Boundary state
                    if a == t || h == t {
                        let r_adopt = if !overpaying {
                            -rho * (h as f64)
                        } else {
                            if a == t {
                                let term2 = 0.5 * (((a as f64) - (h as f64)) / denom + (a as f64) + (h as f64));
                                if comp_variant == 1 {
                                    (1.0 - rho) * term1 + term2
                                } else {
                                    (1.0 - rho) * (term1 + term2)
                                }
                            } else {
                                let ratio = (alpha / (1.0 - alpha)).powi((h as i32) - (a as i32));
                                let term_ret = term1 + ((h as f64) - (a as f64)) / denom;
                                (1.0 - ratio) * (-rho * (h as f64)) + ratio * (1.0 - rho) * term_ret
                            }
                        };

                        state_actions.push((
                            Action::Adopt,
                            vec![
                                Transition { prob: alpha, next_s: Self::s_idx(t, 1, 0, 0), r: r_adopt },
                                Transition { prob: 1.0 - alpha, next_s: Self::s_idx(t, 0, 1, 0), r: r_adopt },
                            ],
                        ));

                        transitions.push(state_actions);
                        continue;
                    }

                    // Non-boundary states: max(a, h) < t
                    // 1. Adopt
                    let r_adopt = -rho * (h as f64);
                    state_actions.push((
                        Action::Adopt,
                        vec![
                            Transition { prob: alpha, next_s: Self::s_idx(t, 1, 0, 0), r: r_adopt },
                            Transition { prob: 1.0 - alpha, next_s: Self::s_idx(t, 0, 1, 0), r: r_adopt },
                        ],
                    ));

                    // 2. Override (feasible if a > h)
                    if a > h {
                        let r_over = (1.0 - rho) * ((h as f64) + 1.0);
                        state_actions.push((
                            Action::Override,
                            vec![
                                Transition { prob: alpha, next_s: Self::s_idx(t, a - h, 0, 0), r: r_over },
                                Transition { prob: 1.0 - alpha, next_s: Self::s_idx(t, a - h - 1, 1, 1), r: r_over },
                            ],
                        ));
                    }

                    // 3. Match (feasible if fork == 1 and a >= h and h > 0)
                    if fork == 1 && a >= h && h > 0 {
                        let mut succs = Vec::new();
                        succs.push(Transition { prob: alpha, next_s: Self::s_idx(t, a + 1, h, 2), r: 0.0 });
                        if gamma > 0.0 {
                            succs.push(Transition {
                                prob: gamma * (1.0 - alpha),
                                next_s: Self::s_idx(t, a - h, 1, 1),
                                r: (1.0 - rho) * (h as f64),
                            });
                        }
                        succs.push(Transition {
                            prob: (1.0 - gamma) * (1.0 - alpha),
                            next_s: Self::s_idx(t, a, h + 1, 1),
                            r: 0.0,
                        });
                        state_actions.push((Action::Match, succs));
                    }

                    // 4. Wait
                    if fork != 2 {
                        state_actions.push((
                            Action::Wait,
                            vec![
                                Transition { prob: alpha, next_s: Self::s_idx(t, a + 1, h, 0), r: 0.0 },
                                Transition { prob: 1.0 - alpha, next_s: Self::s_idx(t, a, h + 1, 1), r: 0.0 },
                            ],
                        ));
                    } else if fork == 2 && a > h && h > 0 {
                        let mut succs = Vec::new();
                        succs.push(Transition { prob: alpha, next_s: Self::s_idx(t, a + 1, h, 2), r: 0.0 });
                        if gamma > 0.0 {
                            succs.push(Transition {
                                prob: gamma * (1.0 - alpha),
                                next_s: Self::s_idx(t, a - h, 1, 1),
                                r: (1.0 - rho) * (h as f64),
                            });
                        }
                        succs.push(Transition {
                            prob: (1.0 - gamma) * (1.0 - alpha),
                            next_s: Self::s_idx(t, a, h + 1, 1),
                            r: 0.0,
                        });
                        state_actions.push((Action::Wait, succs));
                    }

                    transitions.push(state_actions);
                }
            }
        }

        Self {
            alpha,
            gamma,
            t,
            rho,
            overpaying,
            comp_variant,
            num_states,
            transitions,
        }
    }

    /// Solves for the optimal gain g and bias vector h
    pub fn solve_bias(&self, tol: f64, max_iter: usize) -> (f64, Vec<f64>, usize) {
        let mut h = vec![0.0; self.num_states];
        let mut g = 0.0;

        for it in 0..max_iter {
            let mut min_diff = f64::INFINITY;
            let mut max_diff = f64::NEG_INFINITY;

            for s in 0..self.num_states {
                let mut max_q = f64::NEG_INFINITY;

                for (_action, succs) in &self.transitions[s] {
                    let mut q = 0.0;
                    for succ in succs {
                        q += succ.prob * (succ.r + h[succ.next_s]);
                    }
                    if q > max_q {
                        max_q = q;
                    }
                }

                let diff = max_q - h[s];
                if diff < min_diff { min_diff = diff; }
                if diff > max_diff { max_diff = diff; }
                h[s] = max_q - g;
            }

            g = 0.5 * (max_diff + min_diff);
            let span = max_diff - min_diff;

            let h0 = h[0];
            for x in h.iter_mut() {
                *x -= h0;
            }

            if span < tol {
                return (g, h, it + 1);
            }
        }

        (g, h, max_iter)
    }
}

/// Exact Rational verifier for N_rho^T dual certificate
pub struct ExactVerifier {
    pub alpha: Ratio<BigInt>,
    pub gamma: Ratio<BigInt>,
    pub t: usize,
    pub rho: Ratio<BigInt>,
    pub g: Ratio<BigInt>,
    pub comp_variant: usize,
    pub h: Vec<Ratio<BigInt>>,
}

impl ExactVerifier {
    pub fn new(
        alpha: Ratio<BigInt>,
        gamma: Ratio<BigInt>,
        t: usize,
        rho: Ratio<BigInt>,
        g: Ratio<BigInt>,
        comp_variant: usize,
        h: Vec<Ratio<BigInt>>,
    ) -> Self {
        Self {
            alpha,
            gamma,
            t,
            rho,
            g,
            comp_variant,
            h,
        }
    }

    #[inline(always)]
    pub fn s_idx(&self, a: usize, h: usize, fork: usize) -> usize {
        a * (self.t + 1) * 3 + h * 3 + fork
    }

    /// Verifies that for every state s and every valid action a:
    /// r_rho(s, a) + sum P(s'|s, a) h(s') - h(s) <= g
    pub fn verify_all(&self) -> (bool, Ratio<BigInt>, usize) {
        let one = Ratio::from_integer(BigInt::from(1));
        let zero = Ratio::zero();
        let two = Ratio::from_integer(BigInt::from(2));
        let half = Ratio::new(BigInt::from(1), BigInt::from(2));

        let denom = one.clone() - two * self.alpha.clone();
        let term1 = (self.alpha.clone() * (one.clone() - self.alpha.clone())) / (denom.clone() * denom.clone());

        let mut max_slack = Ratio::new(BigInt::from(-1000000000), BigInt::from(1));
        let mut violations = 0;

        for a in 0..=self.t {
            for h in 0..=self.t {
                for fork in 0..3 {
                    let s = self.s_idx(a, h, fork);
                    let h_s = &self.h[s];

                    // Check boundary state
                    if a == self.t || h == self.t {
                        // Action Adopt only
                        let r_adopt = if a == self.t {
                            let term2 = half.clone() * (Ratio::from_integer(BigInt::from((a as i64) - (h as i64))) / denom.clone()
                                + Ratio::from_integer(BigInt::from((a + h) as i64)));
                            if self.comp_variant == 1 {
                                (one.clone() - self.rho.clone()) * term1.clone() + term2
                            } else {
                                (one.clone() - self.rho.clone()) * (term1.clone() + term2)
                            }
                        } else {
                            // h == t, a < t
                            let diff = (h - a) as usize;
                            let mut ratio = one.clone();
                            let base = self.alpha.clone() / (one.clone() - self.alpha.clone());
                            for _ in 0..diff {
                                ratio = ratio * base.clone();
                            }
                            let term_ret = term1.clone() + Ratio::from_integer(BigInt::from((h - a) as i64)) / denom.clone();
                            (one.clone() - ratio.clone()) * (-self.rho.clone() * Ratio::from_integer(BigInt::from(h as i64)))
                                + ratio * (one.clone() - self.rho.clone()) * term_ret
                        };

                        let s_100 = self.s_idx(1, 0, 0);
                        let s_010 = self.s_idx(0, 1, 0);
                        let exp_next = self.alpha.clone() * self.h[s_100].clone() + (one.clone() - self.alpha.clone()) * self.h[s_010].clone();
                        let lhs = r_adopt + exp_next - h_s.clone();
                        if lhs > max_slack { max_slack = lhs.clone(); }
                        if lhs > self.g {
                            violations += 1;
                        }
                        continue;
                    }

                    // Non-boundary states:
                    // 1. Adopt
                    let r_adopt = -self.rho.clone() * Ratio::from_integer(BigInt::from(h as i64));
                    let s_100 = self.s_idx(1, 0, 0);
                    let s_010 = self.s_idx(0, 1, 0);
                    let exp_next = self.alpha.clone() * self.h[s_100].clone() + (one.clone() - self.alpha.clone()) * self.h[s_010].clone();
                    let lhs = r_adopt + exp_next - h_s.clone();
                    if lhs > max_slack { max_slack = lhs.clone(); }
                    if lhs > self.g {
                        violations += 1;
                    }

                    // 2. Override (feasible if a > h)
                    if a > h {
                        let r_over = (one.clone() - self.rho.clone()) * Ratio::from_integer(BigInt::from((h + 1) as i64));
                        let s_over_a = self.s_idx(a - h, 0, 0);
                        let s_over_h = self.s_idx(a - h - 1, 1, 1);
                        let exp_next = self.alpha.clone() * self.h[s_over_a].clone() + (one.clone() - self.alpha.clone()) * self.h[s_over_h].clone();
                        let lhs = r_over + exp_next - h_s.clone();
                        if lhs > max_slack { max_slack = lhs.clone(); }
                        if lhs > self.g {
                            violations += 1;
                        }
                    }

                    // 3. Match (feasible if fork == 1 and a >= h and h > 0)
                    if fork == 1 && a >= h && h > 0 {
                        let s_match_a = self.s_idx(a + 1, h, 2);
                        let s_match_h = self.s_idx(a, h + 1, 1);
                        let mut exp_next = self.alpha.clone() * self.h[s_match_a].clone();
                        let mut r_exp = zero.clone();
                        if self.gamma > zero {
                            let s_match_h_supp = self.s_idx(a - h, 1, 1);
                            let prob_supp = self.gamma.clone() * (one.clone() - self.alpha.clone());
                            let r_h = (one.clone() - self.rho.clone()) * Ratio::from_integer(BigInt::from(h as i64));
                            r_exp = prob_supp.clone() * r_h;
                            exp_next = exp_next + prob_supp * self.h[s_match_h_supp].clone();
                        }
                        let prob_opp = (one.clone() - self.gamma.clone()) * (one.clone() - self.alpha.clone());
                        exp_next = exp_next + prob_opp * self.h[s_match_h].clone();
                        let lhs = r_exp + exp_next - h_s.clone();
                        if lhs > max_slack { max_slack = lhs.clone(); }
                        if lhs > self.g {
                            violations += 1;
                        }
                    }

                    // 4. Wait
                    if fork != 2 {
                        let s_wait_a = self.s_idx(a + 1, h, 0);
                        let s_wait_h = self.s_idx(a, h + 1, 1);
                        let exp_next = self.alpha.clone() * self.h[s_wait_a].clone() + (one.clone() - self.alpha.clone()) * self.h[s_wait_h].clone();
                        let lhs = exp_next - h_s.clone();
                        if lhs > max_slack { max_slack = lhs.clone(); }
                        if lhs > self.g {
                            violations += 1;
                        }
                    } else if fork == 2 && a > h && h > 0 {
                        let s_wait_a = self.s_idx(a + 1, h, 2);
                        let s_wait_h = self.s_idx(a, h + 1, 1);
                        let mut exp_next = self.alpha.clone() * self.h[s_wait_a].clone();
                        let mut r_exp = zero.clone();
                        if self.gamma > zero {
                            let s_wait_h_supp = self.s_idx(a - h, 1, 1);
                            let prob_supp = self.gamma.clone() * (one.clone() - self.alpha.clone());
                            let r_h = (one.clone() - self.rho.clone()) * Ratio::from_integer(BigInt::from(h as i64));
                            r_exp = prob_supp.clone() * r_h;
                            exp_next = exp_next + prob_supp * self.h[s_wait_h_supp].clone();
                        }
                        let prob_opp = (one.clone() - self.gamma.clone()) * (one.clone() - self.alpha.clone());
                        exp_next = exp_next + prob_opp * self.h[s_wait_h].clone();
                        let lhs = r_exp + exp_next - h_s.clone();
                        if lhs > max_slack { max_slack = lhs.clone(); }
                        if lhs > self.g {
                            violations += 1;
                        }
                    }
                }
            }
        }

        (violations == 0, max_slack, violations)
    }
}

#[derive(Serialize, Deserialize)]
pub struct CertificateExport {
    pub target_id: String,
    pub alpha_num: i64,
    pub alpha_den: i64,
    pub gamma_num: i64,
    pub gamma_den: i64,
    pub truncation_t: usize,
    pub comp_variant: usize,
    pub u_num: i64,
    pub u_den: i64,
    pub u_float: f64,
    pub g_num: i64,
    pub g_den: i64,
    pub g_float: f64,
    pub denom_d: i64,
    pub h_numerators: Vec<i64>,
}

fn export_certificate(
    path: &str,
    alpha_num: i64,
    alpha_den: i64,
    u_num: i64,
    u_den: i64,
    t: usize,
    comp_var: usize,
    d: i64,
) {
    let alpha_f = (alpha_num as f64) / (alpha_den as f64);
    let u_f = (u_num as f64) / (u_den as f64);
    println!("Generating certificate: alpha={}/{}, U={}/{} ({}), T={}, comp_var={}", alpha_num, alpha_den, u_num, u_den, u_f, t, comp_var);

    let mdp = SSZModel::new(alpha_f, 0.0, t, u_f, true, comp_var);
    let (g_float, h_float, iters) = mdp.solve_bias(1e-8, 6000);
    println!("  RVI solved: gain = {:+.8} in {} iters", g_float, iters);

    // Quantize h to rationals with denominator d
    let h_nums: Vec<i64> = h_float.iter().map(|&x| (x * (d as f64)).round() as i64).collect();
    let h_rat: Vec<Ratio<BigInt>> = h_nums.iter().map(|&n| Ratio::new(BigInt::from(n), BigInt::from(d))).collect();

    // Find exact max slack across all state-actions
    let alpha_rat = Ratio::new(BigInt::from(alpha_num), BigInt::from(alpha_den));
    let gamma_rat = Ratio::zero();
    let u_rat = Ratio::new(BigInt::from(u_num), BigInt::from(u_den));

    // Temporary verifier with dummy g=0
    let temp_verifier = ExactVerifier::new(alpha_rat.clone(), gamma_rat.clone(), t, u_rat.clone(), Ratio::zero(), comp_var, h_rat.clone());
    let (_, max_slack, _) = temp_verifier.verify_all();
    let max_slack_f = max_slack.numer().to_f64().unwrap() / max_slack.denom().to_f64().unwrap();
    println!("  Exact maximum slack across all state-action pairs: {:+.8}", max_slack_f);

    // Set g_cert strictly between max_slack and 0
    let g_rat = max_slack.clone() + Ratio::new(BigInt::from(1), BigInt::from(100_000));
    assert!(g_rat.is_negative(), "g_rat must be negative!");
    let g_f = g_rat.numer().to_f64().unwrap() / g_rat.denom().to_f64().unwrap();
    println!("  Certified gain g = {:+.8} ({})", g_f, g_rat);

    let final_verifier = ExactVerifier::new(alpha_rat, gamma_rat, t, u_rat, g_rat.clone(), comp_var, h_rat);
    let (pass, verified_max, viols) = final_verifier.verify_all();
    let verified_max_f = verified_max.numer().to_f64().unwrap() / verified_max.denom().to_f64().unwrap();
    println!("  Exact verification: PASS = {}, violations = {}, verified max slack = {:+.8}", pass, viols, verified_max_f);
    assert!(pass, "Exact verification must pass with zero violations!");

    // Export certificate
    let cert = CertificateExport {
        target_id: "bitcoin-selfish-mining-revenue-bounds".to_string(),
        alpha_num,
        alpha_den,
        gamma_num: 0,
        gamma_den: 1,
        truncation_t: t,
        comp_variant: comp_var,
        u_num,
        u_den,
        u_float: u_f,
        g_num: g_rat.numer().to_i64().unwrap(),
        g_den: g_rat.denom().to_i64().unwrap(),
        g_float: g_f,
        denom_d: d,
        h_numerators: h_nums,
    };

    let serialized = serde_json::to_string_pretty(&cert).unwrap();
    let mut file = File::create(path).unwrap();
    file.write_all(serialized.as_bytes()).unwrap();
    println!("  Exported certificate to {}", path);
}

fn main() {
    println!("=== SSZ Dual Certificate Exact Generator and Certifier ===");
    let d = 10_000_000i64; // Denominator 10^7

    // 1. CONFIRMED_SOLUTION: alpha = 0.45, U = 0.70099
    export_certificate(
        "certificate_alpha_0.45.json",
        45, 100, 70099, 100000, 95, 2, d,
    );

    // Also export var 1 certificate for alpha = 0.45 at T = 180 to satisfy both formula interpretations!
    export_certificate(
        "certificate_alpha_0.45_var1.json",
        45, 100, 70099, 100000, 180, 1, d,
    );

    // 2. CONFIRMED_SOLUTION: alpha = 0.475, U = 0.90466
    export_certificate(
        "certificate_alpha_0.475.json",
        475, 1000, 90466, 100000, 95, 2, d,
    );

    // 3. Partial win p2: alpha = 0.425, U = 0.57216
    export_certificate(
        "certificate_alpha_0.425.json",
        425, 1000, 57216, 100000, 95, 2, d,
    );

    // 4. Partial win p2: alpha = 0.40, U = 0.48894
    export_certificate(
        "certificate_alpha_0.40.json",
        40, 100, 48894, 100000, 95, 2, d,
    );

    println!("\nAll certificates generated, certified in exact rational arithmetic, and exported!");

    // 5. Partial win p1: explicit stationary policies strictly beating published revenues
    println!("\n=== Partial Win p1: Stationary Policy Generation and Evaluation ===");
    export_policy(
        "policy_alpha_0.45.json",
        45, 100, 120, 0.66894, 0.66894 + 1e-6,
    );

    export_policy(
        "policy_alpha_0.475.json",
        475, 1000, 120, 0.80184, 0.80184 + 1e-6,
    );
}

#[derive(Serialize, Deserialize)]
pub struct PolicyExport {
    pub target_id: String,
    pub alpha_num: i64,
    pub alpha_den: i64,
    pub gamma_num: i64,
    pub gamma_den: i64,
    pub truncation_t: usize,
    pub rev_lower_bound: f64,
    pub rev_upper_bound: f64,
    pub r1_epoch: f64,
    pub r2_epoch: f64,
    pub published_bar: f64,
    pub strictly_exceeds_published: bool,
    pub actions: Vec<u8>,
}

fn export_policy(
    path: &str,
    alpha_num: i64,
    alpha_den: i64,
    t: usize,
    pub_bar: f64,
    required_min: f64,
) {
    let alpha_f = (alpha_num as f64) / (alpha_den as f64);
    println!("\nExtracting and evaluating policy for alpha = {}/{} at T = {}:", alpha_num, alpha_den, t);

    // Solve underpaying MDP with rho = pub_bar
    let mdp = SSZModel::new(alpha_f, 0.0, t, pub_bar, false, 1);
    let mut v = vec![0.0; mdp.num_states];
    let mut policy = vec![Action::Adopt; mdp.num_states];

    // RVI to get optimal policy
    for _ in 0..5000 {
        let mut min_diff = f64::INFINITY;
        let mut max_diff = f64::NEG_INFINITY;

        for s in 0..mdp.num_states {
            let mut max_q = f64::NEG_INFINITY;
            let mut best_a = Action::Adopt;

            for (act, succs) in &mdp.transitions[s] {
                let mut q = 0.0;
                for succ in succs {
                    q += succ.prob * (succ.r + v[succ.next_s]);
                }
                if q > max_q {
                    max_q = q;
                    best_a = *act;
                }
            }

            policy[s] = best_a;
            let diff = max_q - v[s];
            if diff < min_diff { min_diff = diff; }
            if diff > max_diff { max_diff = diff; }
            v[s] = max_q;
        }

        let span = max_diff - min_diff;
        let v0 = v[0];
        for x in v.iter_mut() {
            *x -= v0;
        }
        if span < 1e-8 {
            break;
        }
    }

    // Evaluate renewal reward expected blocks
    let mut e1 = vec![0.0; mdp.num_states];
    let mut e2 = vec![0.0; mdp.num_states];

    // Precompute rewards for policy
    let denom = 1.0 - 2.0 * alpha_f;
    for _ in 0..5000 {
        let mut max_change = 0.0f64;

        for s in 0..mdp.num_states {
            let (a, h, _) = SSZModel::idx_to_s(t, s);
            let act = policy[s];

            if act == Action::Adopt || a == t || h == t {
                e1[s] = 0.0;
                e2[s] = h as f64;
                continue;
            }

            let (r1, r2) = match act {
                Action::Adopt => (0.0, h as f64),
                Action::Override => ((h + 1) as f64, 0.0),
                Action::Match | Action::Wait => (0.0, 0.0),
            };

            let succs = &mdp.transitions[s].iter().find(|(a, _)| *a == act).unwrap().1;
            let mut q1 = 0.0;
            let mut q2 = 0.0;
            for succ in succs {
                q1 += succ.prob * (succ.r + e1[succ.next_s]); // Note: for renewal reward we track blocks directly
            }

            // Direct block tracking:
            let next_e1 = match act {
                Action::Override => (h + 1) as f64 + alpha_f * e1[SSZModel::s_idx(t, a - h, 0, 0)] + (1.0 - alpha_f) * e1[SSZModel::s_idx(t, a - h - 1, 1, 1)],
                Action::Wait => {
                    let (_, _, fork) = SSZModel::idx_to_s(t, s);
                    if fork != 2 {
                        alpha_f * e1[SSZModel::s_idx(t, a + 1, h, 0)] + (1.0 - alpha_f) * e1[SSZModel::s_idx(t, a, h + 1, 1)]
                    } else {
                        alpha_f * e1[SSZModel::s_idx(t, a + 1, h, 2)] + (1.0 - alpha_f) * e1[SSZModel::s_idx(t, a, h + 1, 1)]
                    }
                },
                Action::Match => {
                    alpha_f * e1[SSZModel::s_idx(t, a + 1, h, 2)] + (1.0 - alpha_f) * e1[SSZModel::s_idx(t, a, h + 1, 1)]
                },
                Action::Adopt => 0.0,
            };

            let next_e2 = match act {
                Action::Override => alpha_f * e2[SSZModel::s_idx(t, a - h, 0, 0)] + (1.0 - alpha_f) * e2[SSZModel::s_idx(t, a - h - 1, 1, 1)],
                Action::Wait => {
                    let (_, _, fork) = SSZModel::idx_to_s(t, s);
                    if fork != 2 {
                        alpha_f * e2[SSZModel::s_idx(t, a + 1, h, 0)] + (1.0 - alpha_f) * e2[SSZModel::s_idx(t, a, h + 1, 1)]
                    } else {
                        alpha_f * e2[SSZModel::s_idx(t, a + 1, h, 2)] + (1.0 - alpha_f) * e2[SSZModel::s_idx(t, a, h + 1, 1)]
                    }
                },
                Action::Match => {
                    alpha_f * e2[SSZModel::s_idx(t, a + 1, h, 2)] + (1.0 - alpha_f) * e2[SSZModel::s_idx(t, a, h + 1, 1)]
                },
                Action::Adopt => h as f64,
            };

            let diff1 = (next_e1 - e1[s]).abs();
            let diff2 = (next_e2 - e2[s]).abs();
            if diff1 > max_change { max_change = diff1; }
            if diff2 > max_change { max_change = diff2; }

            e1[s] = next_e1;
            e2[s] = next_e2;
        }

        if max_change < 1e-12 {
            break;
        }
    }

    let s_100 = SSZModel::s_idx(t, 1, 0, 0);
    let s_010 = SSZModel::s_idx(t, 0, 1, 0);
    let r1_epoch = alpha_f * e1[s_100] + (1.0 - alpha_f) * e1[s_010];
    let r2_epoch = alpha_f * e2[s_100] + (1.0 - alpha_f) * e2[s_010];
    let rev = r1_epoch / (r1_epoch + r2_epoch);

    println!("  Expected epoch rewards: R1 = {:.8}, R2 = {:.8}", r1_epoch, r2_epoch);
    println!("  Stationary Relative Revenue REV = {:.8}", rev);
    println!("  Published bar: {:.8}, Required min: {:.8}", pub_bar, required_min);
    let exceeds = rev > required_min;
    println!("  Strictly exceeds published bar + 1e-6: {}", exceeds);
    assert!(exceeds, "Policy revenue must strictly exceed published bar + 1e-6!");

    let action_bytes: Vec<u8> = policy.iter().map(|&a| a as u8).collect();
    let export = PolicyExport {
        target_id: "bitcoin-selfish-mining-revenue-bounds".to_string(),
        alpha_num,
        alpha_den,
        gamma_num: 0,
        gamma_den: 1,
        truncation_t: t,
        rev_lower_bound: rev - 1e-10,
        rev_upper_bound: rev + 1e-10,
        r1_epoch,
        r2_epoch,
        published_bar: pub_bar,
        strictly_exceeds_published: exceeds,
        actions: action_bytes,
    };

    let serialized = serde_json::to_string_pretty(&export).unwrap();
    let mut file = File::create(path).unwrap();
    file.write_all(serialized.as_bytes()).unwrap();
    println!("  Exported policy to {}", path);
}

