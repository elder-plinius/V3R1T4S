// Lens 2: Independent Game-Graph Walker and Strategy Verifier
// Loads two-sided strategy certificates, executes complete adversarial game tree traversal,
// and verifies that all terminal outcomes satisfy two-sided minimax bounds.

use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::time::Instant;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum GameType {
    Margin, // A392305: s2 - s1
    MaxSum, // A391538: s2
}

pub struct StrategyVerifier {
    pub n: usize,
    pub val: u16,
    pub game_type: GameType,
    pub total_coin_sum: u32,
    pub placer_strategy: HashMap<(u32, u16, u16, u16), u8>, // (mask, s0, s1, basket) -> coin
    pub presenter_strategy: HashMap<(u32, u16, u16), u16>,   // (mask, s0, s1) -> basket
    pub placer_leaves: u64,
    pub presenter_leaves: u64,
}

impl StrategyVerifier {
    pub fn new(n: usize, val: u16, game_type: GameType) -> Self {
        let total_coin_sum = (n * (n + 1) / 2) as u32;
        Self {
            n,
            val,
            game_type,
            total_coin_sum,
            placer_strategy: HashMap::new(),
            presenter_strategy: HashMap::new(),
            placer_leaves: 0,
            presenter_leaves: 0,
        }
    }

    pub fn load_certificate(&mut self, json_path: &str) -> Result<(), String> {
        let file = File::open(json_path).map_err(|e| format!("Cannot open {}: {}", json_path, e))?;
        let reader = BufReader::new(file);

        let mut in_placer = false;
        let mut in_presenter = false;

        for line in reader.lines() {
            let line = line.map_err(|e| e.to_string())?;
            let trimmed = line.trim();

            if trimmed.contains("\"placer_strategy\": [") {
                in_placer = true;
                in_presenter = false;
                continue;
            }
            if trimmed.contains("\"presenter_strategy\": [") {
                in_placer = false;
                in_presenter = true;
                continue;
            }
            if trimmed.starts_with(']') {
                in_placer = false;
                in_presenter = false;
                continue;
            }

            if in_placer && trimmed.contains("\"mask\":") {
                // Parse {"mask": 131071, "s0": 0, "s1": 0, "basket": 0, "coin": 17}
                if let Some(rule) = parse_placer_rule(trimmed) {
                    self.placer_strategy.insert((rule.0, rule.1, rule.2, rule.3), rule.4);
                }
            } else if in_presenter && trimmed.contains("\"mask\":") {
                // Parse {"mask": 131071, "s0": 0, "s1": 0, "basket": 0}
                if let Some(rule) = parse_presenter_rule(trimmed) {
                    self.presenter_strategy.insert((rule.0, rule.1, rule.2), rule.3);
                }
            }
        }

        println!("Loaded certificate from {}: {} placer rules, {} presenter rules.",
                 json_path, self.placer_strategy.len(), self.presenter_strategy.len());
        Ok(())
    }

    // Walk game graph under Placer strategy against ALL Presenter basket choices
    pub fn walk_placer(&mut self, mask: u32, s0: u16, s1: u16, c_rem: u32) -> Result<(), String> {
        let placed_sum = self.total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;

        if mask == 0 {
            self.placer_leaves += 1;
            let payoff = match self.game_type {
                GameType::Margin => s2 - s1,
                GameType::MaxSum => s2,
            };
            if payoff < self.val {
                return Err(format!("Placer strategy failed at terminal state: sums=({}, {}, {}), payoff={}, expected >={}",
                                   s0, s1, s2, payoff, self.val));
            }
            return Ok(());
        }

        let mut distinct = [0u16; 3];
        let distinct_len = if s0 == s1 && s1 == s2 {
            distinct[0] = s0; 1
        } else if s0 == s1 {
            distinct[0] = s0; distinct[1] = s2; 2
        } else if s1 == s2 {
            distinct[0] = s0; distinct[1] = s1; 2
        } else {
            distinct[0] = s0; distinct[1] = s1; distinct[2] = s2; 3
        };

        for i in 0..distinct_len {
            let chosen_s = distinct[i];
            let c = match self.placer_strategy.get(&(mask, s0, s1, chosen_s)) {
                Some(&coin) => coin,
                None => return Err(format!("Placer strategy missing for state (mask={}, s0={}, s1={}, basket={})",
                                           mask, s0, s1, chosen_s)),
            };

            let bit = 1 << (c - 1);
            if (mask & bit) == 0 {
                return Err(format!("Illegal placer move: coin {} is not in mask {}", c, mask));
            }

            let next_mask = mask ^ bit;
            let next_c_rem = c_rem - c as u32;
            let new_sum = chosen_s + c as u16;

            let (other0, other1) = if chosen_s == s0 {
                (s1, s2)
            } else if chosen_s == s1 {
                (s0, s2)
            } else {
                (s0, s1)
            };

            let (ns0, ns1) = if new_sum <= other0 {
                (new_sum, other0)
            } else if new_sum <= other1 {
                (other0, new_sum)
            } else {
                (other0, other1)
            };

            self.walk_placer(next_mask, ns0, ns1, next_c_rem)?;
        }

        Ok(())
    }

    // Walk game graph under Presenter strategy against ALL Placer coin choices
    pub fn walk_presenter(&mut self, mask: u32, s0: u16, s1: u16, c_rem: u32) -> Result<(), String> {
        let placed_sum = self.total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;

        if mask == 0 {
            self.presenter_leaves += 1;
            let payoff = match self.game_type {
                GameType::Margin => s2 - s1,
                GameType::MaxSum => s2,
            };
            if payoff > self.val {
                return Err(format!("Presenter strategy failed to cap at terminal state: sums=({}, {}, {}), payoff={}, expected <={}",
                                   s0, s1, s2, payoff, self.val));
            }
            return Ok(());
        }

        let chosen_s = match self.presenter_strategy.get(&(mask, s0, s1)) {
            Some(&basket) => basket,
            None => return Err(format!("Presenter strategy missing for state (mask={}, s0={}, s1={})", mask, s0, s1)),
        };

        if chosen_s != s0 && chosen_s != s1 && chosen_s != s2 {
            return Err(format!("Invalid presenter choice {} not among current sums ({}, {}, {})",
                               chosen_s, s0, s1, s2));
        }

        let (other0, other1) = if chosen_s == s0 {
            (s1, s2)
        } else if chosen_s == s1 {
            (s0, s2)
        } else {
            (s0, s1)
        };

        for c in 1..=self.n {
            let bit = 1 << (c - 1);
            if (mask & bit) != 0 {
                let next_mask = mask ^ bit;
                let next_c_rem = c_rem - c as u32;
                let new_sum = chosen_s + c as u16;

                let (ns0, ns1) = if new_sum <= other0 {
                    (new_sum, other0)
                } else if new_sum <= other1 {
                    (other0, new_sum)
                } else {
                    (other0, other1)
                };

                self.walk_presenter(next_mask, ns0, ns1, next_c_rem)?;
            }
        }

        Ok(())
    }

    pub fn verify_complete_certificate(&mut self) -> Result<(), String> {
        let full_mask = ((1u64 << self.n) - 1) as u32;

        println!("--- Verifying Placer Strategy (guaranteeing payoff >= {}) ---", self.val);
        let t0 = Instant::now();
        self.placer_leaves = 0;
        self.walk_placer(full_mask, 0, 0, self.total_coin_sum)?;
        println!("Placer strategy verified across {} game paths in {:?}", self.placer_leaves, t0.elapsed());

        println!("--- Verifying Presenter Strategy (capping payoff <= {}) ---", self.val);
        let t1 = Instant::now();
        self.presenter_leaves = 0;
        self.walk_presenter(full_mask, 0, 0, self.total_coin_sum)?;
        println!("Presenter strategy verified across {} game paths in {:?}", self.presenter_leaves, t1.elapsed());

        println!("SUCCESS: Both strategy tables unconditionally verify minimax value = {} for n = {}.", self.val, self.n);
        Ok(())
    }
}

fn parse_placer_rule(line: &str) -> Option<(u32, u16, u16, u16, u8)> {
    // {"mask": 131071, "s0": 0, "s1": 0, "basket": 0, "coin": 17}
    let extract = |key: &str| -> Option<u64> {
        let pos = line.find(key)?;
        let rest = &line[pos + key.len()..];
        let val_str: String = rest.chars().take_while(|c| c.is_digit(10)).collect();
        val_str.parse().ok()
    };

    let mask = extract("\"mask\": ")? as u32;
    let s0 = extract("\"s0\": ")? as u16;
    let s1 = extract("\"s1\": ")? as u16;
    let basket = extract("\"basket\": ")? as u16;
    let coin = extract("\"coin\": ")? as u8;
    Some((mask, s0, s1, basket, coin))
}

fn parse_presenter_rule(line: &str) -> Option<(u32, u16, u16, u16)> {
    // {"mask": 131071, "s0": 0, "s1": 0, "basket": 0}
    let extract = |key: &str| -> Option<u64> {
        let pos = line.find(key)?;
        let rest = &line[pos + key.len()..];
        let val_str: String = rest.chars().take_while(|c| c.is_digit(10)).collect();
        val_str.parse().ok()
    };

    let mask = extract("\"mask\": ")? as u32;
    let s0 = extract("\"s0\": ")? as u16;
    let s1 = extract("\"s1\": ")? as u16;
    let basket = extract("\"basket\": ")? as u16;
    Some((mask, s0, s1, basket))
}

fn main() {
    println!("=== Lens 2: Independent Game-Graph Walker & Strategy Verifier ===");

    let mut report = Vec::new();
    report.push("=== Lens 2 Independent Strategy Walker Verification Report ===".to_string());

    for &(n, val) in &[(17usize, 7u16), (18usize, 7u16)] {
        let path = format!("runs/2026-10-27-1730/attempts/lens1_rust_exact_decision_minimax/a392305_n{}_cert.json", n);
        if std::path::Path::new(&path).exists() {
            println!("\nValidating certificate for A392305({}) = {} from {}...", n, val, path);
            let mut verifier = StrategyVerifier::new(n, val, GameType::Margin);
            match verifier.load_certificate(&path) {
                Ok(_) => {
                    match verifier.verify_complete_certificate() {
                        Ok(_) => {
                            let msg = format!("A392305({}): Verified two-sided minimax certificate for value {} (Placer leaves: {}, Presenter leaves: {}) — PASS",
                                              n, val, verifier.placer_leaves, verifier.presenter_leaves);
                            println!("{}", msg);
                            report.push(msg);
                        }
                        Err(e) => {
                            let msg = format!("A392305({}): Verification FAILED: {}", n, e);
                            eprintln!("{}", msg);
                            report.push(msg);
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Failed to load certificate: {}", e);
                }
            }
        } else {
            println!("Certificate file {} does not exist yet.", path);
        }
    }

    let out_path = "runs/2026-10-27-1730/attempts/lens2_rust_alpha_beta_game_graph_walker/verification_output.txt";
    let mut f = File::create(out_path).unwrap();
    for line in report {
        writeln!(f, "{}", line).unwrap();
    }
    println!("\nWrote verification output to {}.", out_path);
}
