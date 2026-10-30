use crate::cards::{CardTables, NUM_HAND_CLASSES};
use crate::eval::Evaluator;
use rayon::prelude::*;
use std::sync::Mutex;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy, Default)]
pub struct Equity2 {
    pub win: f64,
    pub loss: f64,
    pub tie: f64,
}

pub struct EquityEngine {
    pub eq2: Vec<Vec<Equity2>>, // 169 x 169
    pub eq3_cache: Mutex<HashMap<u32, [f64; 13]>>,
}

// Key for 3-way class triple (c1, c2, c3 in 0..168)
#[inline(always)]
pub fn key3(c1: usize, c2: usize, c3: usize) -> u32 {
    ((c1 as u32) << 16) | ((c2 as u32) << 8) | (c3 as u32)
}

impl EquityEngine {
    pub fn load_from_file(path: &str) -> std::io::Result<Self> {
        let bytes = std::fs::read(path)?;
        let mut eq2 = vec![vec![Equity2::default(); NUM_HAND_CLASSES]; NUM_HAND_CLASSES];
        let mut offset = 0;
        for c1 in 0..NUM_HAND_CLASSES {
            for c2 in 0..NUM_HAND_CLASSES {
                let win = f64::from_le_bytes(bytes[offset..offset+8].try_into().unwrap());
                offset += 8;
                let loss = f64::from_le_bytes(bytes[offset..offset+8].try_into().unwrap());
                offset += 8;
                let tie = f64::from_le_bytes(bytes[offset..offset+8].try_into().unwrap());
                offset += 8;
                eq2[c1][c2] = Equity2 { win, loss, tie };
            }
        }
        Ok(EquityEngine {
            eq2,
            eq3_cache: Mutex::new(HashMap::new()),
        })
    }

    pub fn new(cards: &CardTables, eval: &Evaluator) -> Self {
        println!("Computing exact 2-way preflop equity table (169x169)...");
        let mut eq2 = vec![vec![Equity2::default(); NUM_HAND_CLASSES]; NUM_HAND_CLASSES];

        // All pairs (c1, c2) with c1 <= c2
        let mut pairs = Vec::with_capacity(169 * 170 / 2);
        for c1 in 0..NUM_HAND_CLASSES {
            for c2 in c1..NUM_HAND_CLASSES {
                pairs.push((c1, c2));
            }
        }

        let deck: [u8; 52] = core::array::from_fn(|i| i as u8);

        let results: Vec<((usize, usize), Equity2)> = pairs.par_iter().map(|&(c1, c2)| {
            let combos1 = &cards.class_combos[c1];
            let combos2 = &cards.class_combos[c2];

            let mut total_w1 = 0u64;
            let mut total_w2 = 0u64;
            let mut total_tie = 0u64;
            let mut valid_combos = 0u64;

            for &h1 in combos1 {
                for &h2 in combos2 {
                    if h1[0] == h2[0] || h1[0] == h2[1] || h1[1] == h2[0] || h1[1] == h2[1] {
                        continue;
                    }
                    valid_combos += 1;

                    let mut rem = [0u8; 48];
                    let mut k = 0;
                    for &c in &deck {
                        if c != h1[0] && c != h1[1] && c != h2[0] && c != h2[1] {
                            rem[k] = c;
                            k += 1;
                        }
                    }

                    let mut b1_cards = [0u8; 7];
                    let mut b2_cards = [0u8; 7];
                    b1_cards[0] = h1[0]; b1_cards[1] = h1[1];
                    b2_cards[0] = h2[0]; b2_cards[1] = h2[1];

                    let mut w1 = 0u64;
                    let mut w2 = 0u64;
                    let mut tie = 0u64;

                    for i0 in 0..44 {
                        b1_cards[2] = rem[i0]; b2_cards[2] = rem[i0];
                        for i1 in (i0+1)..45 {
                            b1_cards[3] = rem[i1]; b2_cards[3] = rem[i1];
                            for i2 in (i1+1)..46 {
                                b1_cards[4] = rem[i2]; b2_cards[4] = rem[i2];
                                for i3 in (i2+1)..47 {
                                    b1_cards[5] = rem[i3]; b2_cards[5] = rem[i3];
                                    for i4 in (i3+1)..48 {
                                        b1_cards[6] = rem[i4]; b2_cards[6] = rem[i4];

                                        let s1 = eval.eval_7(&b1_cards);
                                        let s2 = eval.eval_7(&b2_cards);
                                        if s1 > s2 { w1 += 1; }
                                        else if s2 > s1 { w2 += 1; }
                                        else { tie += 1; }
                                    }
                                }
                            }
                        }
                    }
                    total_w1 += w1;
                    total_w2 += w2;
                    total_tie += tie;
                }
            }

            let denom = (valid_combos as f64) * 1712304.0;
            let eq = Equity2 {
                win: (total_w1 as f64) / denom,
                loss: (total_w2 as f64) / denom,
                tie: (total_tie as f64) / denom,
            };
            ((c1, c2), eq)
        }).collect();

        for ((c1, c2), eq) in results {
            eq2[c1][c2] = eq;
            eq2[c2][c1] = Equity2 {
                win: eq.loss,
                loss: eq.win,
                tie: eq.tie,
            };
        }

        println!("2-way equity table computed successfully.");

        EquityEngine {
            eq2,
            eq3_cache: Mutex::new(HashMap::new()),
        }
    }

    // Evaluate exact 3-way equity distribution over the 13 outcomes
    pub fn get_3way(&self, c1: usize, c2: usize, c3: usize, cards: &CardTables, eval: &Evaluator) -> [f64; 13] {
        let k = key3(c1, c2, c3);
        {
            let cache = self.eq3_cache.lock().unwrap();
            if let Some(&dist) = cache.get(&k) {
                return dist;
            }
        }

        let combos1 = &cards.class_combos[c1];
        let combos2 = &cards.class_combos[c2];
        let combos3 = &cards.class_combos[c3];

        let mut outcome_counts = [0u64; 13];
        let mut valid_triples = 0u64;

        let deck: [u8; 52] = core::array::from_fn(|i| i as u8);

        for &h1 in combos1 {
            for &h2 in combos2 {
                if h1[0] == h2[0] || h1[0] == h2[1] || h1[1] == h2[0] || h1[1] == h2[1] {
                    continue;
                }
                for &h3 in combos3 {
                    if h3[0] == h1[0] || h3[0] == h1[1] || h3[1] == h1[0] || h3[1] == h1[1]
                        || h3[0] == h2[0] || h3[0] == h2[1] || h3[1] == h2[0] || h3[1] == h2[1] {
                        continue;
                    }
                    valid_triples += 1;

                    let mut rem = [0u8; 46];
                    let mut ki = 0;
                    for &c in &deck {
                        if c != h1[0] && c != h1[1] && c != h2[0] && c != h2[1] && c != h3[0] && c != h3[1] {
                            rem[ki] = c;
                            ki += 1;
                        }
                    }

                    let mut b1_cards = [0u8; 7];
                    let mut b2_cards = [0u8; 7];
                    let mut b3_cards = [0u8; 7];
                    b1_cards[0] = h1[0]; b1_cards[1] = h1[1];
                    b2_cards[0] = h2[0]; b2_cards[1] = h2[1];
                    b3_cards[0] = h3[0]; b3_cards[1] = h3[1];

                    for i0 in 0..42 {
                        b1_cards[2] = rem[i0]; b2_cards[2] = rem[i0]; b3_cards[2] = rem[i0];
                        for i1 in (i0+1)..43 {
                            b1_cards[3] = rem[i1]; b2_cards[3] = rem[i1]; b3_cards[3] = rem[i1];
                            for i2 in (i1+1)..44 {
                                b1_cards[4] = rem[i2]; b2_cards[4] = rem[i2]; b3_cards[4] = rem[i2];
                                for i3 in (i2+1)..45 {
                                    b1_cards[5] = rem[i3]; b2_cards[5] = rem[i3]; b3_cards[5] = rem[i3];
                                    for i4 in (i3+1)..46 {
                                        b1_cards[6] = rem[i4]; b2_cards[6] = rem[i4]; b3_cards[6] = rem[i4];

                                        let s1 = eval.eval_7(&b1_cards);
                                        let s2 = eval.eval_7(&b2_cards);
                                        let s3 = eval.eval_7(&b3_cards);

                                        let outcome = if s1 > s2 && s2 > s3 { 0 }
                                        else if s1 > s3 && s3 > s2 { 1 }
                                        else if s2 > s1 && s1 > s3 { 2 }
                                        else if s2 > s3 && s3 > s1 { 3 }
                                        else if s3 > s1 && s1 > s2 { 4 }
                                        else if s3 > s2 && s2 > s1 { 5 }
                                        else if s1 == s2 && s1 > s3 { 6 }
                                        else if s1 == s3 && s1 > s2 { 7 }
                                        else if s2 == s3 && s2 > s1 { 8 }
                                        else if s1 > s2 && s2 == s3 { 9 }
                                        else if s2 > s1 && s1 == s3 { 10 }
                                        else if s3 > s1 && s1 == s2 { 11 }
                                        else { 12 };

                                        outcome_counts[outcome] += 1;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        let denom = (valid_triples as f64) * 1370754.0;
        let mut dist = [0.0f64; 13];
        for i in 0..13 {
            dist[i] = (outcome_counts[i] as f64) / denom;
        }

        let mut cache = self.eq3_cache.lock().unwrap();
        cache.insert(k, dist);
        dist
    }
}
