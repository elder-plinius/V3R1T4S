// Dedicated solver for A392305 (Margin Game, n=17..20) with certificate export.
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

pub struct MarginSolver {
    pub n: usize,
    pub total_coin_sum: u32,
    pub table: FastTable,
    pub record_strategy: bool,
    pub placer_strategy: std::collections::HashMap<(u64, u16), u8>,
    pub presenter_strategy: std::collections::HashMap<u64, u16>,
}

impl MarginSolver {
    pub fn new(n: usize) -> Self {
        let total_coin_sum = (n * (n + 1) / 2) as u32;
        let cap = if n >= 19 { 1 << 25 } else if n >= 17 { 1 << 23 } else { 1 << 20 };
        Self {
            n,
            total_coin_sum,
            table: FastTable::with_capacity_pow2(cap),
            record_strategy: false,
            placer_strategy: std::collections::HashMap::new(),
            presenter_strategy: std::collections::HashMap::new(),
        }
    }

    #[inline(always)]
    fn state_key(mask: u32, s0: u16, s1: u16) -> u64 {
        ((mask as u64) << 32) | ((s0 as u64) << 16) | (s1 as u64)
    }

    pub fn can_placer_force_ge(&mut self, mask: u32, s0: u16, s1: u16, c_rem: u32, v: u16) -> bool {
        let placed_sum = self.total_coin_sum - c_rem;
        let s2 = (placed_sum - s0 as u32 - s1 as u32) as u16;

        if mask == 0 {
            return (s2 - s1) >= v;
        }

        if ((s2 - s1) as u32 + c_rem) < v as u32 {
            return false;
        }

        let key = Self::state_key(mask, s0, s1);
        if !self.record_strategy {
            if let Some(ans) = self.table.get(key) {
                return ans;
            }
        }

        let mut distinct = [0u16; 3];
        let distinct_len;
        if s0 == s1 && s1 == s2 {
            distinct[0] = s0;
            distinct_len = 1;
        } else if s0 == s1 {
            distinct[0] = s0;
            distinct[1] = s2;
            distinct_len = 2;
        } else if s1 == s2 {
            distinct[0] = s0;
            distinct[1] = s1;
            distinct_len = 2;
        } else {
            distinct[0] = s0;
            distinct[1] = s1;
            distinct[2] = s2;
            distinct_len = 3;
        }

        let mut capping_basket = None;

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
            let mut winning_coin = None;

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
                        winning_coin = Some(c as u8);
                        break;
                    }
                }
            }

            if self.record_strategy && placer_can_win {
                if let Some(c) = winning_coin {
                    self.placer_strategy.insert((key, chosen_s), c);
                }
            }

            if !placer_can_win {
                capping_basket = Some(chosen_s);
                break;
            }
        }

        let result = capping_basket.is_none();
        if self.record_strategy && !result {
            if let Some(b) = capping_basket {
                self.presenter_strategy.insert(key, b);
            }
        }

        if !self.record_strategy {
            self.table.insert(key, result);
        }
        result
    }

    pub fn solve_exact_value(&mut self, min_guess: u16) -> u16 {
        let full_mask = ((1u64 << self.n) - 1) as u32;
        let mut v = min_guess;
        loop {
            self.table.clear();
            self.record_strategy = false;
            if self.can_placer_force_ge(full_mask, 0, 0, self.total_coin_sum, v) {
                v += 1;
            } else {
                return v - 1;
            }
        }
    }
}

fn main() {
    println!("=== A392305 Dedicated Solver (n=17..20) ===");
    let mut prev = 6; // A392305(16) = 6
    for n in 17..=20 {
        let t0 = Instant::now();
        let mut solver = MarginSolver::new(n);
        let val = solver.solve_exact_value(prev);
        let dt = t0.elapsed();
        println!("A392305({:2}) = {} in {:?}", n, val, dt);
        prev = val;
    }
}
