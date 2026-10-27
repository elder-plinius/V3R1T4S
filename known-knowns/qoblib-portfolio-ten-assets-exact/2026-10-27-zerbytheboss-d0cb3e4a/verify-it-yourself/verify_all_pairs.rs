// SPDX-License-Identifier: AGPL-3.0-or-later
// Exact Bellman Dynamic Programming on QOBLIB Portfolio Instance po_a010_t10_orig_b004_l1e-03

use flate2::read::GzDecoder;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::time::Instant;

fn parse_decimal(s: &str) -> Option<BigRational> {
    let s = s.trim();
    if s.is_empty() {
        return None;
    }
    let (mant, exp10) = match s.find(['e', 'E']) {
        Some(i) => (&s[..i], s[i + 1..].parse::<i64>().ok()?),
        None => (s, 0i64),
    };
    let (mant, neg) = match mant.strip_prefix('-') {
        Some(r) => (r, true),
        None => (mant.strip_prefix('+').unwrap_or(mant), false),
    };
    let (ipart, fpart) = match mant.find('.') {
        Some(i) => (&mant[..i], &mant[i + 1..]),
        None => (mant, ""),
    };
    if ipart.is_empty() && fpart.is_empty() {
        return None;
    }
    if !ipart.chars().all(|c| c.is_ascii_digit()) || !fpart.chars().all(|c| c.is_ascii_digit()) {
        return None;
    }
    let digits = format!("{ipart}{fpart}");
    if digits.is_empty() {
        return None;
    }
    let num: BigInt = digits.parse().ok()?;
    let scale = fpart.len() as i64 - exp10;
    let (num, den) = if scale >= 0 {
        (num, BigInt::from(10).pow(scale as u32))
    } else {
        (num * BigInt::from(10).pow((-scale) as u32), BigInt::one())
    };
    let num = if neg { -num } else { num };
    Some(BigRational::new(num, den))
}

fn zround(x: &BigRational) -> i64 {
    let half = BigRational::new(BigInt::one(), BigInt::from(2));
    let shifted = if x.is_negative() { x - &half } else { x + &half };
    let bi = shifted.trunc().to_integer();
    bi.to_string().parse::<i64>().unwrap()
}

#[derive(Clone)]
struct Instance {
    symbols: Vec<String>,
    index: HashMap<String, usize>,
    periods: usize,
    unit_prices: Vec<Vec<BigRational>>,
}

fn open_maybe_gz(path: &Path) -> std::io::Result<Box<dyn BufRead>> {
    let f = File::open(path)?;
    if path.extension().map(|e| e == "gz").unwrap_or(false) {
        Ok(Box::new(BufReader::new(GzDecoder::new(f))))
    } else {
        Ok(Box::new(BufReader::new(f)))
    }
}

fn read_instance(dir: &Path, unit_cash: &BigRational) -> Instance {
    let price_path = dir.join("stock_prices.txt.gz");
    let reader = open_maybe_gz(&price_path).expect("cannot open stock_prices");
    let mut symbols: Vec<String> = Vec::new();
    let mut index: HashMap<String, usize> = HashMap::new();
    let mut entries: Vec<(usize, usize, BigRational)> = Vec::new();
    let mut max_day = 0usize;

    for line in reader.lines() {
        let line = line.expect("read error");
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut it = line.split_whitespace();
        let (d, s, v) = (it.next().unwrap(), it.next().unwrap(), it.next().unwrap());
        let day: usize = d.parse().unwrap();
        let val = parse_decimal(v).unwrap();
        let id = *index.entry(s.to_string()).or_insert_with(|| {
            symbols.push(s.to_string());
            symbols.len() - 1
        });
        max_day = max_day.max(day);
        entries.push((id, day, val));
    }
    let periods = max_day + 1;
    let mut raw: Vec<Vec<Option<BigRational>>> = vec![vec![None; periods]; symbols.len()];
    for (id, day, val) in entries {
        raw[id][day] = Some(val);
    }
    let mut raw_prices = Vec::with_capacity(symbols.len());
    for row in raw {
        let mut out = Vec::with_capacity(periods);
        for v in row {
            out.push(v.unwrap());
        }
        raw_prices.push(out);
    }
    let mut unit_prices = Vec::with_capacity(symbols.len());
    for row in &raw_prices {
        let base = &row[0];
        unit_prices.push(row.iter().map(|v| v * unit_cash / base).collect());
    }
    Instance { symbols, index, periods, unit_prices }
}

fn read_covariance(dir: &Path, inst: &Instance) -> HashMap<(usize, usize, usize), BigRational> {
    let cov_path = dir.join("covariance_matrices.txt.gz");
    let reader = open_maybe_gz(&cov_path).expect("cannot open covariance");
    let mut cov = HashMap::new();
    for line in reader.lines() {
        let line = line.expect("read error");
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut it = line.split_whitespace();
        let (d, s1, s2, v) = (it.next().unwrap(), it.next().unwrap(), it.next().unwrap(), it.next().unwrap());
        let day: usize = d.parse().unwrap();
        let val = parse_decimal(v).unwrap();
        let i = *inst.index.get(s1).unwrap();
        let j = *inst.index.get(s2).unwrap();
        cov.insert((i, j, day), val);
    }
    cov
}

// State: 20 counts (lo, sh for 10 assets), each in 0..3, total <= 4.
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
struct State {
    counts: [u8; 20],
}

impl State {
    fn total(&self) -> u8 {
        self.counts.iter().sum()
    }
    fn net(&self) -> i32 {
        let mut n = 0i32;
        for i in 0..10 {
            n += self.counts[2 * i] as i32 - self.counts[2 * i + 1] as i32;
        }
        n
    }
}

fn generate_states() -> Vec<State> {
    let mut states = Vec::new();
    let mut cur = [0u8; 20];

    fn backtrack(pos: usize, rem: u8, cur: &mut [u8; 20], states: &mut Vec<State>) {
        if pos == 20 {
            states.push(State { counts: *cur });
            return;
        }
        for v in 0..=rem.min(3) {
            cur[pos] = v;
            backtrack(pos + 1, rem - v, cur, states);
        }
    }

    backtrack(0, 4, &mut cur, &mut states);
    states
}

fn parse_solution_path(path: &Path, inst: &Instance, states: &[State]) -> Vec<usize> {
    let file = File::open(path).expect("cannot open sol");
    let reader = BufReader::new(file);
    let mut pos: HashMap<(usize, usize), (u8, u8)> = HashMap::new();
    for line in reader.lines() {
        let line = line.unwrap();
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut it = line.split_whitespace();
        let k = it.next().unwrap();
        if k == "instance" || k == "budget" || k == "lambda" || k == "objective" {
            continue;
        }
        let t: usize = k.parse().unwrap();
        let sym = it.next().unwrap();
        let lo: u8 = it.next().unwrap().parse().unwrap();
        let sh: u8 = it.next().unwrap().parse().unwrap();
        let asset = *inst.index.get(sym).unwrap();
        pos.insert((t, asset), (lo, sh));
    }

    let mut state_indices = Vec::with_capacity(inst.periods);
    for t in 0..inst.periods {
        let mut counts = [0u8; 20];
        for i in 0..10 {
            if let Some(&(lo, sh)) = pos.get(&(t, i)) {
                counts[2 * i] = lo;
                counts[2 * i + 1] = sh;
            }
        }
        let st = State { counts };
        let idx = states.iter().position(|s| s == &st).expect("incumbent state not found");
        state_indices.push(idx);
    }
    state_indices
}

fn main() {
    let t_start = Instant::now();
    let data_dir = Path::new("runs/2026-10-27-1610/data");
    let unit_cash = BigRational::from_integer(BigInt::from(100000));
    let lambda = BigRational::new(BigInt::one(), BigInt::from(1000)); // 0.001
    let delta = BigRational::new(BigInt::one(), BigInt::from(1000));  // 0.001
    let nu = BigRational::new(BigInt::one(), BigInt::from(10000));     // 0.0001
    let rho = BigRational::new(BigInt::from(25), BigInt::from(1000000)); // 0.000025

    println!("Loading QOBLIB portfolio instance po_a010_t10_orig...");
    let inst = read_instance(data_dir, &unit_cash);
    let cov = read_covariance(data_dir, &inst);
    let periods = inst.periods; // 10
    println!("Loaded: {} assets, {} periods", inst.symbols.len(), periods);

    println!("Generating discrete count state space (20 counts in 0..3, total <= 4)...");
    let states = generate_states();
    let n_states = states.len();
    println!("Exact number of count states: {}", n_states);
    assert_eq!(n_states, 10606, "State count must be exactly 10606");

    // Precompute coefficients
    println!("Precomputing exact rounded model coefficients...");
    // 1. Transaction flip cost per asset and period: w_trans[t][i] = zround(delta * p[i, t])
    let mut w_trans = vec![vec![0i64; 10]; periods];
    for t in 0..periods {
        for i in 0..10 {
            w_trans[t][i] = zround(&(&delta * &inst.unit_prices[i][t]));
        }
    }

    // 2. Short selling cost per asset and period: w_short[t][i] = zround(rho * p[i, t])
    let mut w_short = vec![vec![0i64; 10]; periods];
    for t in 0..periods {
        for i in 0..10 {
            w_short[t][i] = zround(&(&rho * &inst.unit_prices[i][t]));
        }
    }

    // 3. Return coef per asset and period: w_ret[t][i] = zround(p[i, t+1] - p[i, t]) for t < periods - 1
    let mut w_ret = vec![vec![0i64; 10]; periods];
    for t in 0..(periods - 1) {
        for i in 0..10 {
            let dp = &inst.unit_prices[i][t + 1] - &inst.unit_prices[i][t];
            w_ret[t][i] = zround(&dp);
        }
    }

    // 4. Cash interest digits: coef_cash[k] = zround(nu * unit * 2^k) for k in 0..4
    let mut coef_cash = [0i64; 4];
    for k in 0..4 {
        let pow2 = BigRational::from_integer(BigInt::one() << k);
        coef_cash[k] = zround(&(&nu * &unit_cash * pow2));
    }

    // 5. Risk matrix per period: Q[t][(i, tau_i)][(j, tau_j)]
    // Indices 0..20: group g = 2*i + (if tau==1 {0} else {1})
    let mut Q_risk = vec![vec![vec![0i64; 20]; 20]; periods];
    for t in 0..periods {
        for i in 0..10 {
            for tau_i_idx in 0..2 {
                let tau_i = if tau_i_idx == 0 { 1i32 } else { -1i32 };
                let gi = 2 * i + tau_i_idx;
                for j in 0..10 {
                    for tau_j_idx in 0..2 {
                        let tau_j = if tau_j_idx == 0 { 1i32 } else { -1i32 };
                        let gj = 2 * j + tau_j_idx;
                        let c = cov.get(&(i, j, t)).expect("missing cov entry");
                        let sign = BigRational::from_integer(BigInt::from(tau_i * tau_j));
                        let base = &lambda * &sign * c * &inst.unit_prices[i][t] * &inst.unit_prices[j][t];
                        Q_risk[t][gi][gj] = zround(&base);
                    }
                }
            }
        }
    }

    // Precompute Stage Costs: stage_cost[t][s]
    println!("Precomputing stage costs for all 10 periods x 10,606 states...");
    let mut stage_cost = vec![vec![0i64; n_states]; periods];
    for t in 0..periods {
        for (s_idx, s) in states.iter().enumerate() {
            let mut cost = 0i64;

            // Risk
            let mut r = 0i64;
            for gi in 0..20 {
                let ui = s.counts[gi] as i64;
                if ui == 0 { continue; }
                for gj in 0..20 {
                    let uj = s.counts[gj] as i64;
                    if uj == 0 { continue; }
                    r += Q_risk[t][gi][gj] * ui * uj;
                }
            }
            cost += r;

            // Cash interest
            let net = s.net();
            let slack1 = 10 - net;
            if slack1 >= 0 {
                let s_val = slack1 as u32;
                for k in 0..4 {
                    if (s_val >> k) & 1 == 1 {
                        cost -= coef_cash[k];
                    }
                }
            }

            // Short selling cost
            for i in 0..10 {
                let sh = s.counts[2 * i + 1] as i64;
                if sh > 0 {
                    cost += w_short[t][i] * sh;
                }
            }

            // Expected return (t < 9)
            if t < periods - 1 {
                for i in 0..10 {
                    let lo = s.counts[2 * i] as i64;
                    let sh = s.counts[2 * i + 1] as i64;
                    if lo > 0 {
                        cost -= w_ret[t][i] * lo;
                    }
                    if sh > 0 {
                        // signed return = -1 * dp => - zround(-dp) * sh = + zround(dp) * sh
                        cost += w_ret[t][i] * sh;
                    }
                }
            }

            // Initial buy-in at t = 0
            if t == 0 {
                for i in 0..10 {
                    let total_u = (s.counts[2 * i] + s.counts[2 * i + 1]) as i64;
                    if total_u > 0 {
                        cost += w_trans[0][i] * total_u;
                    }
                }
            }

            // Liquidation at t = 9
            if t == periods - 1 {
                for i in 0..10 {
                    let total_u = (s.counts[2 * i] + s.counts[2 * i + 1]) as i64;
                    if total_u > 0 {
                        cost += w_trans[periods - 1][i] * total_u;
                    }
                }
            }

            stage_cost[t][s_idx] = cost;
        }
    }

    // Positive Control: Verify incumbent solution against our stage & transition costs
    let sol_file = data_dir.join("po_a010_t10_orig_b004_l1e-3.bst.sol");
    let inc_path = parse_solution_path(&sol_file, &inst, &states);
    println!("Evaluating incumbent trajectory through discrete count states...");
    let mut inc_obj = 0i64;
    for t in 0..periods {
        let s_cur = inc_path[t];
        let sc = stage_cost[t][s_cur];
        inc_obj += sc;
        if t > 0 && t < periods - 1 {
            let s_prev = inc_path[t - 1];
            let mut tc = 0i64;
            for i in 0..10 {
                let d_lo = (states[s_prev].counts[2 * i] as i64 - states[s_cur].counts[2 * i] as i64).abs();
                let d_sh = (states[s_prev].counts[2 * i + 1] as i64 - states[s_cur].counts[2 * i + 1] as i64).abs();
                tc += w_trans[t][i] * (d_lo + d_sh);
            }
            inc_obj += tc;
        }
    }
    println!("Incumbent trajectory recomputed objective: {}", inc_obj);
    assert_eq!(inc_obj, -8397, "Incumbent objective must be exactly -8397");
    println!("POSITIVE CONTROL: PASS (Exact match to incumbent -8397)");

    // Exact Bellman Dynamic Programming
    println!("\nExecuting Exact Bellman Backward/Forward Dynamic Programming...");
    let mut V = vec![vec![i64::MAX; n_states]; periods];
    let mut parent = vec![vec![0usize; n_states]; periods];

    // t = 0
    for s in 0..n_states {
        V[0][s] = stage_cost[0][s];
    }

    // t = 1..8
    for t in 1..(periods - 1) {
        let t_step = Instant::now();
        let wt = &w_trans[t];
        for s in 0..n_states {
            let sc = stage_cost[t][s];
            let cur_s = &states[s];
            let mut best_val = i64::MAX;
            let mut best_p = 0usize;

            for p in 0..n_states {
                let prev_v = V[t - 1][p];
                if prev_v == i64::MAX { continue; }
                let prev_s = &states[p];
                let mut tc = 0i64;
                for i in 0..10 {
                    let d_lo = (prev_s.counts[2 * i] as i64 - cur_s.counts[2 * i] as i64).abs();
                    let d_sh = (prev_s.counts[2 * i + 1] as i64 - cur_s.counts[2 * i + 1] as i64).abs();
                    tc += wt[i] * (d_lo + d_sh);
                }
                let cand = prev_v + tc;
                if cand < best_val {
                    best_val = cand;
                    best_p = p;
                }
            }
            V[t][s] = best_val + sc;
            parent[t][s] = best_p;
        }
        println!("  Period t={} Bellman step completed in {:.2?} (min V[{}] = {})",
                 t, t_step.elapsed(), t, V[t].iter().min().unwrap());
    }

    // t = 9: No rebalancing transition cost between t=8 and t=9
    let t_step = Instant::now();
    let min_v8 = *V[periods - 2].iter().min().unwrap();
    let best_v8_state = V[periods - 2].iter().position(|&v| v == min_v8).unwrap();
    for s in 0..n_states {
        V[periods - 1][s] = stage_cost[periods - 1][s] + min_v8;
        parent[periods - 1][s] = best_v8_state;
    }
    println!("  Period t=9 terminal liquidation completed in {:.2?} (min V[9] = {})",
             t_step.elapsed(), V[periods - 1].iter().min().unwrap());

    // Find Global Optimum
    let opt_val = *V[periods - 1].iter().min().unwrap();
    let opt_final_state = V[periods - 1].iter().position(|&v| v == opt_val).unwrap();

    println!("\n=======================================================");
    println!("EXACT BELLMAN GLOBAL OPTIMUM: {}", opt_val);
    println!("INCUMBENT PUBLISHED VALUE:   -8397");
    println!("=======================================================");

    // Reconstruct optimal path
    let mut opt_path = vec![0usize; periods];
    opt_path[periods - 1] = opt_final_state;
    for t in (1..periods).rev() {
        opt_path[t - 1] = parent[t][opt_path[t]];
    }

    println!("\nAttaining Optimal Trajectory:");
    for t in 0..periods {
        let st = &states[opt_path[t]];
        print!("  t={}: ", t);
        for i in 0..10 {
            if st.counts[2 * i] > 0 || st.counts[2 * i + 1] > 0 {
                print!("{}:(lo={},sh={}) ", inst.symbols[i], st.counts[2 * i], st.counts[2 * i + 1]);
            }
        }
        if st.total() == 0 {
            print!("[empty portfolio]");
        }
        println!();
    }

    println!("\nMatching Incumbent Trajectory vs Optimal Trajectory:");
    let mut identical = true;
    for t in 0..periods {
        let is_same = opt_path[t] == inc_path[t];
        println!("  t={}: opt_state={} inc_state={} (match: {})", t, opt_path[t], inc_path[t], is_same);
        if !is_same { identical = false; }
    }

    if opt_val == -8397 {
        println!("\nCONCLUSION: -8397 IS THE MATHEMATICALLY PROVED GLOBAL OPTIMUM!");
        println!("No schedule in the entire space of 10,606^10 possible trajectories can achieve < -8397.");
        println!("The Bellman optimality certificate proves global optimality unconditionally.");
    } else if opt_val < -8397 {
        println!("\nCONCLUSION: STRICT IMPROVEMENT FOUND! New record: {}", opt_val);
    } else {
        panic!("Bellman optimum ({}) exceeds incumbent (-8397), which is impossible!", opt_val);
    }

    println!("Total execution time: {:.2?}", t_start.elapsed());
}
