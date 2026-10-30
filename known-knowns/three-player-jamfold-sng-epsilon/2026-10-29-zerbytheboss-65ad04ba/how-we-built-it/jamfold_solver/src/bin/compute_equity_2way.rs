use jamfold_solver::cards::{CardTables, NUM_HAND_CLASSES};
use jamfold_solver::eval::Evaluator;
use rayon::prelude::*;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

// All 24 permutations of suits 0..3
const S4: [[u8; 4]; 24] = [
    [0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], [0, 3, 1, 2], [0, 3, 2, 1],
    [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], [1, 2, 3, 0], [1, 3, 0, 2], [1, 3, 2, 0],
    [2, 0, 1, 3], [2, 0, 3, 1], [2, 1, 0, 3], [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0],
    [3, 0, 1, 2], [3, 0, 2, 1], [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0],
];

#[inline(always)]
fn canonical_pair(h1: [u8; 2], h2: [u8; 2]) -> ([u8; 2], [u8; 2]) {
    let mut best_h1 = [0u8; 2];
    let mut best_h2 = [0u8; 2];
    let mut first = true;

    let r1_0 = h1[0] >> 2; let s1_0 = (h1[0] & 3) as usize;
    let r1_1 = h1[1] >> 2; let s1_1 = (h1[1] & 3) as usize;
    let r2_0 = h2[0] >> 2; let s2_0 = (h2[0] & 3) as usize;
    let r2_1 = h2[1] >> 2; let s2_1 = (h2[1] & 3) as usize;

    for p in &S4 {
        let mut p_h1 = [(r1_0 << 2) | p[s1_0], (r1_1 << 2) | p[s1_1]];
        if p_h1[0] > p_h1[1] { p_h1.swap(0, 1); }

        let mut p_h2 = [(r2_0 << 2) | p[s2_0], (r2_1 << 2) | p[s2_1]];
        if p_h2[0] > p_h2[1] { p_h2.swap(0, 1); }

        if first || (p_h1, p_h2) < (best_h1, best_h2) {
            best_h1 = p_h1;
            best_h2 = p_h2;
            first = false;
        }
    }
    (best_h1, best_h2)
}

fn main() {
    let t0 = Instant::now();
    println!("Initializing evaluator and card tables...");
    let eval = Evaluator::new();
    let cards = CardTables::new();
    println!("Tables initialized in {:?}", t0.elapsed());

    let deck: [u8; 52] = core::array::from_fn(|i| i as u8);

    // All pairs (c1, c2) with c1 <= c2
    let mut pairs = Vec::with_capacity(NUM_HAND_CLASSES * (NUM_HAND_CLASSES + 1) / 2);
    for c1 in 0..NUM_HAND_CLASSES {
        for c2 in c1..NUM_HAND_CLASSES {
            pairs.push((c1, c2));
        }
    }
    let total_pairs = pairs.len();
    println!("Computing exact 2-way equity via canonical S4 suit orbits for {} pairs...", total_pairs);

    let counter = AtomicUsize::new(0);
    let start_comp = Instant::now();

    let pair_results: Vec<((usize, usize), (f64, f64, f64))> = pairs.par_iter().map(|&(c1, c2)| {
        let combos1 = &cards.class_combos[c1];
        let combos2 = &cards.class_combos[c2];

        // Find canonical orbits for this matchup
        // Map from canonical (h1, h2) -> orbit count
        let mut orbits: Vec<([u8; 2], [u8; 2], u64)> = Vec::with_capacity(6);

        for &h1 in combos1 {
            for &h2 in combos2 {
                if h1[0] == h2[0] || h1[0] == h2[1] || h1[1] == h2[0] || h1[1] == h2[1] {
                    continue;
                }
                let can = canonical_pair(h1, h2);
                let mut found = false;
                for o in &mut orbits {
                    if o.0 == can.0 && o.1 == can.1 {
                        o.2 += 1;
                        found = true;
                        break;
                    }
                }
                if !found {
                    orbits.push((can.0, can.1, 1));
                }
            }
        }

        let mut total_w1 = 0u64;
        let mut total_w2 = 0u64;
        let mut total_tie = 0u64;
        let mut total_combos = 0u64;

        for &(h1, h2, orbit_size) in &orbits {
            total_combos += orbit_size;

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
            total_w1 += w1 * orbit_size;
            total_w2 += w2 * orbit_size;
            total_tie += tie * orbit_size;
        }

        let denom = (total_combos as f64) * 1712304.0;
        let eq = (
            (total_w1 as f64) / denom,
            (total_w2 as f64) / denom,
            (total_tie as f64) / denom,
        );

        let done = counter.fetch_add(1, Ordering::Relaxed) + 1;
        if done % 1000 == 0 || done == total_pairs {
            let elapsed = start_comp.elapsed();
            let rate = (done as f64) / elapsed.as_secs_f64();
            let remaining = ((total_pairs - done) as f64) / rate;
            println!("Progress: {}/{} pairs ({:.1}%) - {:.1} pairs/s - ETA: {:.0}s",
                done, total_pairs, (done as f64) / (total_pairs as f64) * 100.0, rate, remaining);
        }

        ((c1, c2), eq)
    }).collect();

    let mut matrix = vec![vec![[0.0f64; 3]; NUM_HAND_CLASSES]; NUM_HAND_CLASSES];
    for ((c1, c2), (w1, w2, tie)) in pair_results {
        matrix[c1][c2] = [w1, w2, tie];
        matrix[c2][c1] = [w2, w1, tie];
    }

    let out_path = std::env::args().nth(1).unwrap_or_else(|| "equity_2way.bin".to_string());
    println!("Saving binary equity table to {}...", out_path);
    let file = File::create(&out_path).expect("failed to create file");
    let mut writer = BufWriter::new(file);

    for c1 in 0..NUM_HAND_CLASSES {
        for c2 in 0..NUM_HAND_CLASSES {
            for k in 0..3 {
                writer.write_all(&matrix[c1][c2][k].to_le_bytes()).unwrap();
            }
        }
    }
    writer.flush().unwrap();
    println!("2-way equity computation complete in {:?}", start_comp.elapsed());
}
