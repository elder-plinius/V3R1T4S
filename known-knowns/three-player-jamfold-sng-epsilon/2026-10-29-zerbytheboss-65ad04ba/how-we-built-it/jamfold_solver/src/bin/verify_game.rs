use jamfold_solver::cards::{CardTables, NUM_HAND_CLASSES};
use jamfold_solver::equity::EquityEngine;
use jamfold_solver::eval::Evaluator;
use jamfold_solver::stage::{EliminationConvention, StateStrategy};
use jamfold_solver::state::NUM_STATES;
use jamfold_solver::verifier::Verifier;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::BufReader;
use std::time::Instant;

#[derive(Serialize, Deserialize, Clone)]
pub struct ExportedStateStrategy {
    #[serde(default)]
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
    #[serde(default)]
    pub num_states: usize,
    pub strategies: Vec<ExportedStateStrategy>,
    pub values: Vec<f64>,
    #[serde(default)]
    pub max_outer_dev: f64,
    #[serde(default)]
    pub exploitability: f64,
    pub solve_time_secs: f64,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut equity_path = "equity_2way.bin".to_string();
    let mut strategy_path = "strategy_profile.json".to_string();
    let mut conv_mode = "both".to_string();

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--equity" => { equity_path = args[i+1].clone(); i += 2; }
            "--strategy" => { strategy_path = args[i+1].clone(); i += 2; }
            "--conv" => { conv_mode = args[i+1].clone(); i += 2; }
            _ => { i += 1; }
        }
    }

    println!("=== Lens 1: Compiled Rust Independent Best-Response Verifier ===");
    println!("Strategy profile: {}", strategy_path);
    println!("Equity table: {}", equity_path);
    println!("Convention mode: {}", conv_mode);

    let t_init = Instant::now();
    let eval = Evaluator::new();
    let cards = CardTables::new();
    let equity = EquityEngine::load_from_file(&equity_path)
        .expect("Failed to load equity_2way.bin table.");
    let verifier = Verifier::new(&cards, &equity, &eval);
    println!("Tables initialized in {:?}", t_init.elapsed());

    let file = File::open(&strategy_path).expect("Failed to open strategy profile JSON");
    let reader = BufReader::new(file);
    let exported: ExportedProfile = serde_json::from_reader(reader)
        .expect("Failed to deserialize strategy profile JSON");

    assert_eq!(exported.strategies.len(), NUM_STATES);
    let mut profile = vec![StateStrategy::default(); NUM_STATES];
    for (v_idx, exp_s) in exported.strategies.iter().enumerate() {
        let strat = &mut profile[v_idx];
        for c in 0..NUM_HAND_CLASSES {
            strat.btn_jam[c] = exp_s.btn_jam[c];
            strat.sb_jam_vs_fold[c] = exp_s.sb_jam_vs_fold[c];
            strat.sb_call_vs_jam[c] = exp_s.sb_call_vs_jam[c];
            strat.bb_call_vs_fold_jam[c] = exp_s.bb_call_vs_fold_jam[c];
            strat.bb_call_vs_jam_fold[c] = exp_s.bb_call_vs_jam_fold[c];
            strat.bb_overcall[c] = exp_s.bb_overcall[c];
        }
    }
    println!("Loaded {} states from strategy profile.", NUM_STATES);

    let convs = match conv_mode.as_str() {
        "i" => vec![EliminationConvention::ChipRank],
        "ii" => vec![EliminationConvention::EqualSplit],
        _ => vec![EliminationConvention::ChipRank, EliminationConvention::EqualSplit],
    };

    println!("\n{}", "=".repeat(60));
    println!("=== VERIFICATION RESULTS ===");

    for conv in convs {
        let conv_name = match conv {
            EliminationConvention::ChipRank => "Convention (i) [Chip-Rank Priority]",
            EliminationConvention::EqualSplit => "Convention (ii) [Equal Split]",
        };
        println!("\n--- Verifying under {} ---", conv_name);
        let t_ver = Instant::now();
        let (exploit, v_base, max_idx, max_stack, max_pos) = verifier.compute_exploitability(&profile, conv);
        let elapsed = t_ver.elapsed();

        let idx_15 = jamfold_solver::state::stack_to_index(15, 15, 15);
        let v_btn_15 = v_base[idx_15 * 3 + 0];
        let v_sb_15 = v_base[idx_15 * 3 + 1];
        let v_bb_15 = v_base[idx_15 * 3 + 2];
        let sum_15 = v_btn_15 + v_sb_15 + v_bb_15;

        println!("Equal stack state (15, 15, 15) values:");
        println!("  BTN = ${:.4}, SB = ${:.4}, BB = ${:.4} (Sum = ${:.4})", v_btn_15, v_sb_15, v_bb_15, sum_15);
        println!("Certified ex-post exploitability epsilon = ${:.6}", exploit);
        println!("  Max exploit location: state {:?} (idx {}), Position {}", max_stack, max_idx, max_pos);
        println!("Verification computed in {:?}", elapsed);

        let pass_p1 = exploit < 0.0488;
        let pass_conf = exploit <= 0.0010;
        println!("  Status: p1 (< $0.0488): {}", if pass_p1 { "PASS" } else { "FAIL" });
        println!("  Status: Full solution (<= $0.0010): {}", if pass_conf { "PASS" } else { "FAIL" });
    }
    println!("\n{}", "=".repeat(60));
}
