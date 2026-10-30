use jamfold_solver::cards::CardTables;
use jamfold_solver::equity::EquityEngine;
use jamfold_solver::eval::Evaluator;
use jamfold_solver::stage::{EliminationConvention, StateStrategy};
use jamfold_solver::verifier::Verifier;
use std::fs::File;
use std::io::BufReader;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let conv_str = if args.len() > 1 { &args[1] } else { "i" };
    let prof = if args.len() > 2 { &args[2] } else { "attempts/lens1_solver/strategy_profile_conv_i.json" };
    let eq = if args.len() > 3 { &args[3] } else { "data/equity_2way.bin" };

    let eval = Evaluator::new();
    let cards = CardTables::new();
    let equity = EquityEngine::load_from_file(eq).unwrap();
    let verifier = Verifier::new(&cards, &equity, &eval);
    let conv = match conv_str {
        "ii" => EliminationConvention::EqualSplit,
        _ => EliminationConvention::ChipRank,
    };

    let file = File::open(prof).unwrap();
    let reader = BufReader::new(file);
    let exported: serde_json::Value = serde_json::from_reader(reader).unwrap();
    let values: Vec<f64> = exported["values"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();

    let mut profile = vec![StateStrategy::default(); jamfold_solver::state::NUM_STATES];
    for (v_idx, exp_s) in exported["strategies"].as_array().unwrap().iter().enumerate() {
        let strat = &mut profile[v_idx];
        let btn_jam: Vec<f64> = exp_s["btn_jam"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let sb_jam: Vec<f64> = exp_s["sb_jam_vs_fold"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let sb_call: Vec<f64> = exp_s["sb_call_vs_jam"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let bb_call_fj: Vec<f64> = exp_s["bb_call_vs_fold_jam"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let bb_call_jf: Vec<f64> = exp_s["bb_call_vs_jam_fold"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let bb_over: Vec<f64> = exp_s["bb_overcall"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();

        for c in 0..169 {
            strat.btn_jam[c] = btn_jam[c];
            strat.sb_jam_vs_fold[c] = sb_jam[c];
            strat.sb_call_vs_jam[c] = sb_call[c];
            strat.bb_call_vs_fold_jam[c] = bb_call_fj[c];
            strat.bb_call_vs_jam_fold[c] = bb_call_jf[c];
            strat.bb_overcall[c] = bb_over[c];
        }
    }

    let (adj, b) = verifier.build_system(&profile, &values, conv);
    let (v_eval, max_res) = verifier.evaluate_policy(&adj, &b, &values, 5000, 1e-9);

    println!("=== Exploitability Breakdown for Conv {} ({}) ===", conv_str, prof);
    println!("Policy evaluation max residual: {:.2e}", max_res);

    let mut results = verifier.compute_all_state_exploitabilities(&profile, conv, &v_eval);
    results.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

    println!("\nTop 25 highest-exploitability states:");
    for (i, (exp, idx, stk, pos)) in results.iter().take(25).enumerate() {
        println!("{:2}. State {:?} [{:3}] (idx {:3}): exploitability = ${:.6}", i + 1, stk, pos, idx, exp);
    }

    let count_above_0488 = results.iter().filter(|r| r.0 >= 0.0488).count();
    let count_above_0300 = results.iter().filter(|r| r.0 >= 0.0300).count();
    let count_above_0100 = results.iter().filter(|r| r.0 >= 0.0100).count();
    let count_above_0010 = results.iter().filter(|r| r.0 >= 0.0010).count();

    println!("\nDistribution of exploitabilities across all 946 states:");
    println!("  States with epsilon >= $0.0488: {}", count_above_0488);
    println!("  States with epsilon >= $0.0300: {}", count_above_0300);
    println!("  States with epsilon >= $0.0100: {}", count_above_0100);
    println!("  States with epsilon >= $0.0010: {}", count_above_0010);
    println!("  States with epsilon <  $0.0010: {}", 946 - count_above_0010);
}
