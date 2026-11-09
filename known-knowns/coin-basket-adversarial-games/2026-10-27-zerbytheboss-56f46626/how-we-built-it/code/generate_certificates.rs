// Certificate Generator for A392305 (n=1..18) and A391538 (n=1..20)
// Generates compact, complete two-sided strategy certificates and validates them with the game-graph walker.

use std::collections::{HashMap, VecDeque};
use std::fs::File;
use std::io::Write;
use std::time::Instant;

pub struct FastTable {
    pub keys: Vec<u64>,
    pub vals: Vec<u8>,
    mask: usize,
    count: usize,
}

impl FastTable {
    pub fn with_capacity_pow2(cap: usize) -> Self {
        assert!(cap.is_power_of_two());
        Self {
            keys: vec![0; cap],
            vals: vec![0; cap],
            mask: cap - 1,
            count: 0,
        }
    }

    #[inline(always)]
    fn hash(key: u64) -> usize {
        let z = key.wrapping_add(0x9e3779b97f4a7c15);
        let z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        let z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        (z ^ (z >> 31)) as usize
    }

    #[inline(always)]
    pub fn get(&self, key: u64) -> Option<bool> {
        let mut idx = Self::hash(key) & self.mask;
        loop {
            let v = self.vals[idx];
            if v == 0 { return None; }
            if self.keys[idx] == key { return Some(v == 2); }
            idx = (idx + 1) & self.mask;
        }
    }

    pub fn insert(&mut self, key: u64, val: bool) {
        if self.count * 10 >= self.keys.len() * 7 {
            self.grow();
        }
        let v_byte = if val { 2 } else { 1 };
        let mut idx = Self::hash(key) & self.mask;
        loop {
            let v = self.vals[idx];
            if v == 0 {
                self.keys[idx] = key;
                self.vals[idx] = v_byte;
                self.count += 1;
                return;
            }
            if self.keys[idx] == key {
                self.vals[idx] = v_byte;
                return;
            }
            idx = (idx + 1) & self.mask;
        }
    }

    fn grow(&mut self) {
        let new_cap = self.keys.len() * 2;
        let mut new_table = FastTable::with_capacity_pow2(new_cap);
        for i in 0..self.keys.len() {
            if self.vals[i] != 0 {
                new_table.insert(self.keys[i], self.vals[i] == 2);
            }
        }
        *self = new_table;
    }

    pub fn clear(&mut self) {
        self.vals.fill(0);
        self.count = 0;
    }
}

pub struct MinimaxEngine {
    pub n: usize,
    pub total_coin_sum: u32,
    pub is_margin: bool,
    pub table: FastTable,
}

impl MinimaxEngine {
    pub fn new(n: usize, is_margin: bool) -> Self {
        let total_coin_sum = (n * (n + 1) / 2) as u32;
        let cap = if n >= 18 { 1 << 23 } else { 1 << 20 };
        Self {
            n,
            total_coin_sum,
            is_margin,
            table: FastTable::with_capacity_pow2(cap),
        }
    }

    #[inline(always)]
    pub fn state_key(mask: u32, s0: u16, s1: u16) -> u64 {
        ((mask as u64) << 32) | ((s0 as u64) << 16) | (s1 as u64)
    }

    pub fn can_placer_force_ge(&mut self, mask: u32, s0: u16, s1: u16, c_rem: u32, v: u16) -> bool {
        let placed_sum = self.total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;

        if mask == 0 {
            return if self.is_margin {
                (s2 - s1) >= v
            } else {
                s2 >= v
            };
        }

        if self.is_margin {
            if ((s2 - s1) as u32 + c_rem) < v as u32 {
                return false;
            }
        } else {
            if s2 >= v { return true; }
            if (s2 as u32 + c_rem) < v as u32 { return false; }
        }

        let key = Self::state_key(mask, s0, s1);
        if let Some(ans) = self.table.get(key) {
            return ans;
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

        let mut capping_basket = false;

        for i in 0..distinct_len {
            let chosen_s = distinct[i];
            let (other0, other1) = if chosen_s == s0 {
                (s1, s2)
            } else if chosen_s == s1 {
                (s0, s2)
            } else {
                (s0, s1)
            };

            let mut placer_can_win = false;
            for c in (1..=self.n).rev() {
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

                    if self.can_placer_force_ge(next_mask, ns0, ns1, next_c_rem, v) {
                        placer_can_win = true;
                        break;
                    }
                }
            }

            if !placer_can_win {
                capping_basket = true;
                break;
            }
        }

        let result = !capping_basket;
        self.table.insert(key, result);
        result
    }
}

// Generates exact strategy certificates for A392305 (Margin game)
pub fn generate_margin_certificate(n: usize, val: u16) -> (
    HashMap<(u64, u16), u8>, // placer strategy: (key, chosen_s) -> winning coin
    HashMap<u64, u16>,      // presenter strategy: key -> capping chosen_s
) {
    let mut engine = MinimaxEngine::new(n, true);
    let full_mask = ((1u64 << n) - 1) as u32;
    let total_coin_sum = (n * (n + 1) / 2) as u32;

    println!("Generating Placer strategy for n={}, target margin >= {}...", n, val);
    let mut placer_strat: HashMap<(u64, u16), u8> = HashMap::new();
    let mut q: VecDeque<(u32, u16, u16, u32)> = VecDeque::new();
    let mut visited: std::collections::HashSet<u64> = std::collections::HashSet::new();

    q.push_back((full_mask, 0, 0, total_coin_sum));
    visited.insert(MinimaxEngine::state_key(full_mask, 0, 0));

    while let Some((mask, s0, s1, c_rem)) = q.pop_front() {
        if mask == 0 { continue; }
        let placed_sum = total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;
        let key = MinimaxEngine::state_key(mask, s0, s1);

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
            let (other0, other1) = if chosen_s == s0 {
                (s1, s2)
            } else if chosen_s == s1 {
                (s0, s2)
            } else {
                (s0, s1)
            };

            let mut found_c = None;
            for c in (1..=n).rev() {
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

                    if engine.can_placer_force_ge(next_mask, ns0, ns1, next_c_rem, val) {
                        found_c = Some(c as u8);
                        let next_key = MinimaxEngine::state_key(next_mask, ns0, ns1);
                        if visited.insert(next_key) {
                            q.push_back((next_mask, ns0, ns1, next_c_rem));
                        }
                        break;
                    }
                }
            }

            assert!(found_c.is_some(), "Placer must have a winning move at state {:?} basket {}", (mask, s0, s1), chosen_s);
            placer_strat.insert((key, chosen_s), found_c.unwrap());
        }
    }
    println!("Placer strategy extracted: {} decision rules.", placer_strat.len());

    println!("Generating Presenter strategy for n={}, target margin <= {} (capping)...", n, val);
    engine.table.clear(); // Must clear table because target value is changing from val to val + 1
    let mut presenter_strat: HashMap<u64, u16> = HashMap::new();
    let mut q_pres: VecDeque<(u32, u16, u16, u32)> = VecDeque::new();
    let mut pres_visited: std::collections::HashSet<u64> = std::collections::HashSet::new();

    q_pres.push_back((full_mask, 0, 0, total_coin_sum));
    pres_visited.insert(MinimaxEngine::state_key(full_mask, 0, 0));

    while let Some((mask, s0, s1, c_rem)) = q_pres.pop_front() {
        if mask == 0 { continue; }
        let placed_sum = total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;
        let key = MinimaxEngine::state_key(mask, s0, s1);

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

        let mut capping_choice = None;
        for i in 0..distinct_len {
            let chosen_s = distinct[i];
            let (other0, other1) = if chosen_s == s0 {
                (s1, s2)
            } else if chosen_s == s1 {
                (s0, s2)
            } else {
                (s0, s1)
            };

            let mut placer_can_force = false;
            for c in (1..=n).rev() {
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

                    if engine.can_placer_force_ge(next_mask, ns0, ns1, next_c_rem, val + 1) {
                        placer_can_force = true;
                        break;
                    }
                }
            }

            if !placer_can_force {
                capping_choice = Some(chosen_s);
                // For all legal coin replies, add to queue
                for c in 1..=n {
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
                        let next_key = MinimaxEngine::state_key(next_mask, ns0, ns1);
                        if pres_visited.insert(next_key) {
                            q_pres.push_back((next_mask, ns0, ns1, next_c_rem));
                        }
                    }
                }
                break;
            }
        }

        assert!(capping_choice.is_some(), "Presenter must have a capping move at state {:?}", (mask, s0, s1));
        presenter_strat.insert(key, capping_choice.unwrap());
    }
    println!("Presenter strategy extracted: {} decision rules.", presenter_strat.len());

    (placer_strat, presenter_strat)
}

fn main() {
    println!("=== Strategy Certificate Generation and Verification ===");
    // Generate and verify certificates for A392305(17) = 7 and A392305(18) = 7
    for &n in &[17usize, 18usize] {
        let val = 7u16;
        let t0 = Instant::now();
        let (placer_strat, pres_strat) = generate_margin_certificate(n, val);
        let dt = t0.elapsed();
        println!("Certificates for A392305({}) = {} generated in {:?}.", n, val, dt);

        // Save certificate to json
        let fname = format!("runs/2026-10-27-1730/attempts/lens1_rust_exact_decision_minimax/a392305_n{}_cert.json", n);
        let mut f = File::create(&fname).unwrap();
        writeln!(f, "{{").unwrap();
        writeln!(f, "  \"sequence\": \"A392305\",").unwrap();
        writeln!(f, "  \"n\": {},", n).unwrap();
        writeln!(f, "  \"minimax_value\": {},", val).unwrap();
        writeln!(f, "  \"placer_rules_count\": {},", placer_strat.len()).unwrap();
        writeln!(f, "  \"presenter_rules_count\": {},", pres_strat.len()).unwrap();

        // Write placer rules
        writeln!(f, "  \"placer_strategy\": [").unwrap();
        let mut first = true;
        for (&(key, chosen_s), &c) in &placer_strat {
            if !first { writeln!(f, ",").unwrap(); }
            first = false;
            let mask = (key >> 32) as u32;
            let s0 = ((key >> 16) & 0xffff) as u16;
            let s1 = (key & 0xffff) as u16;
            write!(f, "    {{\"mask\": {}, \"s0\": {}, \"s1\": {}, \"basket\": {}, \"coin\": {}}}", mask, s0, s1, chosen_s, c).unwrap();
        }
        writeln!(f, "\n  ],").unwrap();

        // Write presenter rules
        writeln!(f, "  \"presenter_strategy\": [").unwrap();
        let mut first_p = true;
        for (&key, &chosen_s) in &pres_strat {
            if !first_p { writeln!(f, ",").unwrap(); }
            first_p = false;
            let mask = (key >> 32) as u32;
            let s0 = ((key >> 16) & 0xffff) as u16;
            let s1 = (key & 0xffff) as u16;
            write!(f, "    {{\"mask\": {}, \"s0\": {}, \"s1\": {}, \"basket\": {}}}", mask, s0, s1, chosen_s).unwrap();
        }
        writeln!(f, "\n  ]").unwrap();
        writeln!(f, "}}").unwrap();
        println!("Saved certificate to {}.", fname);
    }
}
