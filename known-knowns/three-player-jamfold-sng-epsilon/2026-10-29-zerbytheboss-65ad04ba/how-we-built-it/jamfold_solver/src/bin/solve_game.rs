use jamfold_solver::cards::{CardTables, NUM_HAND_CLASSES};
use jamfold_solver::equity::EquityEngine;
use jamfold_solver::eval::Evaluator;
use jamfold_solver::stage::{EliminationConvention, StageSolver, StateStrategy};
use jamfold_solver::state::{icm_3player, StateTable, NUM_POSITION_STATES, NUM_STATES};
use jamfold_solver::verifier::Verifier;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::BufWriter;
use std::time::Instant;

#[derive(Serialize, Deserialize, Clone)]
pub struct ExportedStateStrategy {
    pub stack: [u8; 3],
    pub btn_jam: Vec<f64>,
    pub sb_jam_vs_fold: Vec<f64>,
    pub sb_call_vs_jam: Vec<f64>,
    pub bb_call_vs_fold_jam: Vec<f64>,
    pub bb_call_vs_jam_fold: Vec<f64>,
    pub bb_overcall: Vec<f64>,
}

#[derive(Serialize, Deserialize)]
pub struct ExportedProfile {
    pub convention: String,
    pub num_states: usize,
    pub strategies: Vec<ExportedStateStrategy>,
    pub values: Vec<f64>,
    pub max_outer_dev: f64,
    pub exploitability: f64,
    pub solve_time_secs: f64,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut equity_path = "equity_2way.bin".to_string();
    let mut out_path = "strategy_profile.json".to_string();
    let mut conv_str = "i".to_string();
    let mut max_outer_iters = 12;
    let mut cfr_iters = 40;
    let mut init_path: Option<String> = None;
    let mut resume_path: Option<String> = None;
    let mut start_iter: usize = 1;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--equity" => { equity_path = args[i+1].clone(); i += 2; }
            "--out" => { out_path = args[i+1].clone(); i += 2; }
            "--conv" => { conv_str = args[i+1].clone(); i += 2; }
            "--iters" => { max_outer_iters = args[i+1].parse().unwrap(); i += 2; }
            "--cfr-iters" => { cfr_iters = args[i+1].parse().unwrap(); i += 2; }
            "--init" => { init_path = Some(args[i+1].clone()); i += 2; }
            "--resume" => { resume_path = Some(args[i+1].clone()); i += 2; }
            "--start-iter" => { start_iter = args[i+1].parse().unwrap(); i += 2; }
            _ => { i += 1; }
        }
    }

    let conv = match conv_str.as_str() {
        "ii" | "equal" => EliminationConvention::EqualSplit,
        _ => EliminationConvention::ChipRank,
    };

    println!("=== 3-Player Jam/Fold SnG Equilibrium Solver ===");
    println!("Convention: {:?}", conv);
    println!("Equity table: {}", equity_path);
    println!("Output path: {}", out_path);
    println!("Outer iterations: {} to {}", start_iter, max_outer_iters);
    println!("Inner CFR+ iterations: {}", cfr_iters);
    if let Some(ref p) = resume_path {
        println!("Resume path: {} (starting from iteration {})", p, start_iter);
    } else if let Some(ref p) = init_path {
        println!("Warm-start init path: {}", p);
    }

    let t_init = Instant::now();
    println!("Initializing evaluator, card tables, and loading 2-way equity...");
    let eval = Evaluator::new();
    let cards = CardTables::new();
    let equity = EquityEngine::load_from_file(&equity_path)
        .expect("Failed to load equity_2way.bin table. Ensure compute_equity_2way has completed.");
    let state_table = StateTable::new();
    let verifier = Verifier::new(&cards, &equity, &eval);
    let stage_solver = StageSolver::new(&cards, &equity, &eval, conv);
    println!("Tables initialized in {:?}", t_init.elapsed());

    // Initialize V^0 to 3-player ICM payoffs or load from init/resume path
    let mut v_current = vec![0.0f64; NUM_POSITION_STATES];
    let mut sum_profile = vec![StateStrategy::default(); NUM_STATES];
    let mut total_weight = 0.0f64;

    if let Some(ref p) = resume_path {
        println!("Resuming solve from {} at iteration {}...", p, start_iter);
        let file = File::open(p).expect("Failed to open resume profile JSON");
        let reader = std::io::BufReader::new(file);
        let exp: serde_json::Value = serde_json::from_reader(reader).expect("Failed to parse resume JSON");
        let vals: Vec<f64> = exp["values"].as_array().expect("No values array in JSON")
            .iter().map(|v| v.as_f64().unwrap()).collect();
        assert_eq!(vals.len(), NUM_POSITION_STATES);
        v_current = vals;

        let prev_k = start_iter - 1;
        total_weight = (prev_k * (prev_k + 1) / 2) as f64;
        let strats_json = exp["strategies"].as_array().expect("No strategies array");
        for v_idx in 0..NUM_STATES {
            let s = &strats_json[v_idx];
            let btn_jam: Vec<f64> = s["btn_jam"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();
            let sb_jam: Vec<f64> = s["sb_jam_vs_fold"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();
            let sb_call: Vec<f64> = s["sb_call_vs_jam"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();
            let bb_call_fj: Vec<f64> = s["bb_call_vs_fold_jam"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();
            let bb_call_jf: Vec<f64> = s["bb_call_vs_jam_fold"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();
            let bb_over: Vec<f64> = s["bb_overcall"].as_array().unwrap().iter().map(|x| x.as_f64().unwrap()).collect();

            for c in 0..NUM_HAND_CLASSES {
                sum_profile[v_idx].btn_jam[c] = btn_jam[c] * total_weight;
                sum_profile[v_idx].sb_jam_vs_fold[c] = sb_jam[c] * total_weight;
                sum_profile[v_idx].sb_call_vs_jam[c] = sb_call[c] * total_weight;
                sum_profile[v_idx].bb_call_vs_fold_jam[c] = bb_call_fj[c] * total_weight;
                sum_profile[v_idx].bb_call_vs_jam_fold[c] = bb_call_jf[c] * total_weight;
                sum_profile[v_idx].bb_overcall[c] = bb_over[c] * total_weight;
            }
        }
        println!("Loaded continuation values and initial strategies (total_weight = {:.1}).", total_weight);
    } else if let Some(ref p) = init_path {
        println!("Loading initial continuation values V^0 from {}...", p);
        let file = File::open(p).expect("Failed to open init profile JSON");
        let reader = std::io::BufReader::new(file);
        let exp: serde_json::Value = serde_json::from_reader(reader).expect("Failed to parse init JSON");
        let vals: Vec<f64> = exp["values"].as_array().expect("No values array in JSON")
            .iter().map(|v| v.as_f64().unwrap()).collect();
        assert_eq!(vals.len(), NUM_POSITION_STATES);
        v_current = vals;
        println!("Initialized V^0 from {} across {} position-states.", p, NUM_POSITION_STATES);
    } else {
        for v_idx in 0..NUM_STATES {
            let (s1, s2, s3) = state_table.index_to_stack[v_idx];
            let u_icm = icm_3player(s1, s2, s3);
            v_current[v_idx * 3 + 0] = u_icm[0];
            v_current[v_idx * 3 + 1] = u_icm[1];
            v_current[v_idx * 3 + 2] = u_icm[2];
        }
        println!("Initialized V^0 to 3-player ICM across {} position-states.", NUM_POSITION_STATES);
    }

    let mut last_dev = 1.0;
    let t_solve_start = Instant::now();

    let mut best_exploit = f64::INFINITY;
    let mut best_profile = vec![StateStrategy::default(); NUM_STATES];
    let mut best_v = v_current.clone();

    for k in start_iter..=max_outer_iters {
        let t_it = Instant::now();
        let weight = k as f64;
        total_weight += weight;
        println!("Starting Outer Iteration {}/{} (weight = {:.1})...", k, max_outer_iters, weight);

        // Parallel stage game solve across all 946 stack vectors
        let stage_results: Vec<(usize, StateStrategy)> = (0..NUM_STATES).into_par_iter().map(|v_idx| {
            let (s1, s2, s3) = state_table.index_to_stack[v_idx];
            let prev_strat = None;
            let strat = stage_solver.solve_stage(s1, s2, s3, &v_current, cfr_iters, prev_strat);
            (v_idx, strat)
        }).collect();

        // Accumulate into sum_profile
        for (v_idx, strat) in stage_results {
            for c in 0..NUM_HAND_CLASSES {
                sum_profile[v_idx].btn_jam[c] += weight * strat.btn_jam[c];
                sum_profile[v_idx].sb_jam_vs_fold[c] += weight * strat.sb_jam_vs_fold[c];
                sum_profile[v_idx].sb_call_vs_jam[c] += weight * strat.sb_call_vs_jam[c];
                sum_profile[v_idx].bb_call_vs_fold_jam[c] += weight * strat.bb_call_vs_fold_jam[c];
                sum_profile[v_idx].bb_call_vs_jam_fold[c] += weight * strat.bb_call_vs_jam_fold[c];
                sum_profile[v_idx].bb_overcall[c] += weight * strat.bb_overcall[c];
            }
        }

        // Construct current average profile
        let mut avg_profile = vec![StateStrategy::default(); NUM_STATES];
        for v_idx in 0..NUM_STATES {
            for c in 0..NUM_HAND_CLASSES {
                avg_profile[v_idx].btn_jam[c] = sum_profile[v_idx].btn_jam[c] / total_weight;
                avg_profile[v_idx].sb_jam_vs_fold[c] = sum_profile[v_idx].sb_jam_vs_fold[c] / total_weight;
                avg_profile[v_idx].sb_call_vs_jam[c] = sum_profile[v_idx].sb_call_vs_jam[c] / total_weight;
                avg_profile[v_idx].bb_call_vs_fold_jam[c] = sum_profile[v_idx].bb_call_vs_fold_jam[c] / total_weight;
                avg_profile[v_idx].bb_call_vs_jam_fold[c] = sum_profile[v_idx].bb_call_vs_jam_fold[c] / total_weight;
                avg_profile[v_idx].bb_overcall[c] = sum_profile[v_idx].bb_overcall[c] / total_weight;
            }
        }

        // Policy evaluation on average profile
        let t_pe = Instant::now();
        let (adj, b) = verifier.build_system(&avg_profile, &v_current, conv);
        let (v_new, max_res) = verifier.evaluate_policy(&adj, &b, &v_current, 5000, 1e-9);

        let mut max_dev = 0.0f64;
        for j in 0..NUM_POSITION_STATES {
            let diff = (v_new[j] - v_current[j]).abs();
            if diff > max_dev {
                max_dev = diff;
            }
        }
        last_dev = max_dev;
        v_current = v_new;

        let (exploit, max_s_idx, max_stack, max_pos) = verifier.compute_exploitability_with_v(&avg_profile, conv, &v_current);
        println!("Outer Iteration {} finished in {:?} (PE took {:?}): max_dev = {:.6}, PE residual = {:.2e}, exploitability = ${:.6} at state {:?} [{}] (idx {})",
            k, t_it.elapsed(), t_pe.elapsed(), max_dev, max_res, exploit, max_stack, max_pos, max_s_idx);

        if exploit < best_exploit {
            best_exploit = exploit;
            best_profile = avg_profile;
            best_v = v_current.clone();
        }

        if exploit <= 0.0010 {
            println!("Target exploitability achieved: epsilon = ${:.6} <= $0.0010!", exploit);
            break;
        }
        if max_dev < 1e-4 {
            println!("Convergence reached: max_dev < 1e-4!");
            break;
        }
    }

    let solve_time = t_solve_start.elapsed().as_secs_f64();
    println!("Solver finished in {:.2} seconds.", solve_time);
    println!("Best unpolished profile certified exploitability = ${:.6}", best_exploit);

    // Test multiple indifference threshold polishing candidates on marginal boundary hands
    let thresholds = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.22, 0.25, 0.28, 0.30];
    for &thresh in &thresholds {
        let mut candidate = best_profile.clone();
        for v_idx in 0..NUM_STATES {
            let strat = &mut candidate[v_idx];
            for c in 0..NUM_HAND_CLASSES {
                if strat.btn_jam[c] < thresh { strat.btn_jam[c] = 0.0; }
                else if strat.btn_jam[c] > 1.0 - thresh { strat.btn_jam[c] = 1.0; }

                if strat.sb_jam_vs_fold[c] < thresh { strat.sb_jam_vs_fold[c] = 0.0; }
                else if strat.sb_jam_vs_fold[c] > 1.0 - thresh { strat.sb_jam_vs_fold[c] = 1.0; }

                if strat.sb_call_vs_jam[c] < thresh { strat.sb_call_vs_jam[c] = 0.0; }
                else if strat.sb_call_vs_jam[c] > 1.0 - thresh { strat.sb_call_vs_jam[c] = 1.0; }

                if strat.bb_call_vs_fold_jam[c] < thresh { strat.bb_call_vs_fold_jam[c] = 0.0; }
                else if strat.bb_call_vs_fold_jam[c] > 1.0 - thresh { strat.bb_call_vs_fold_jam[c] = 1.0; }

                if strat.bb_call_vs_jam_fold[c] < thresh { strat.bb_call_vs_jam_fold[c] = 0.0; }
                else if strat.bb_call_vs_jam_fold[c] > 1.0 - thresh { strat.bb_call_vs_jam_fold[c] = 1.0; }

                if strat.bb_overcall[c] < thresh { strat.bb_overcall[c] = 0.0; }
                else if strat.bb_overcall[c] > 1.0 - thresh { strat.bb_overcall[c] = 1.0; }
            }
        }

        let (adj_pol, b_pol) = verifier.build_system(&candidate, &v_current, conv);
        let (v_pol, _) = verifier.evaluate_policy(&adj_pol, &b_pol, &v_current, 5000, 1e-9);
        let (pol_exploit, _, pol_stack, pol_pos) = verifier.compute_exploitability_with_v(&candidate, conv, &v_pol);
        println!("Threshold {:.2} polishing exploitability = ${:.6} at state {:?} [{}]", thresh, pol_exploit, pol_stack, pol_pos);

        if pol_exploit < best_exploit {
            println!("  -> Threshold {:.2} improved exploitability from ${:.6} to ${:.6}!", thresh, best_exploit, pol_exploit);
            best_exploit = pol_exploit;
            best_profile = candidate;
            best_v = v_pol;
        }
    }

    println!("Exporting strategy profile to {}...", out_path);
    let mut exported_strats = Vec::with_capacity(NUM_STATES);
    for v_idx in 0..NUM_STATES {
        let (s1, s2, s3) = state_table.index_to_stack[v_idx];
        let strat = &best_profile[v_idx];
        exported_strats.push(ExportedStateStrategy {
            stack: [s1, s2, s3],
            btn_jam: strat.btn_jam.to_vec(),
            sb_jam_vs_fold: strat.sb_jam_vs_fold.to_vec(),
            sb_call_vs_jam: strat.sb_call_vs_jam.to_vec(),
            bb_call_vs_fold_jam: strat.bb_call_vs_fold_jam.to_vec(),
            bb_call_vs_jam_fold: strat.bb_call_vs_jam_fold.to_vec(),
            bb_overcall: strat.bb_overcall.to_vec(),
        });
    }

    let exported = ExportedProfile {
        convention: conv_str,
        num_states: NUM_STATES,
        strategies: exported_strats,
        values: best_v,
        max_outer_dev: last_dev,
        exploitability: best_exploit,
        solve_time_secs: solve_time,
    };

    let file = File::create(&out_path).expect("Failed to create output file");
    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, &exported).expect("Failed to serialize strategy profile");
    println!("Export complete. Saved {} states with certified epsilon = ${:.6}.", NUM_STATES, best_exploit);
}
