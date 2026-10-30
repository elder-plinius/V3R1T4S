use jamfold_solver::cards::CardTables;
use jamfold_solver::eval::Evaluator;
use rayon::prelude::*;
use std::time::Instant;

fn main() {
    let t0 = Instant::now();
    let eval = Evaluator::new();
    let cards = CardTables::new();
    println!("Init in {:?}", t0.elapsed());

    let deck: [u8; 52] = core::array::from_fn(|i| i as u8);

    // Test 200 pairs in parallel
    let mut pairs = Vec::new();
    for c1 in 0..20 {
        for c2 in c1..20 {
            pairs.push((c1, c2));
        }
    }
    println!("Testing {} pairs in parallel...", pairs.len());

    let t1 = Instant::now();
    let results: Vec<_> = pairs.par_iter().map(|&(c1, c2)| {
        let combos1 = &cards.class_combos[c1];
        let combos2 = &cards.class_combos[c2];

        let mut total_w1 = 0u64;
        let mut total_w2 = 0u64;
        let mut total_tie = 0u64;
        let mut valid_combos = 0u64;

        // Take canonical combos (e.g. up to 3)
        for &h1 in combos1.iter().take(2) {
            for &h2 in combos2.iter().take(2) {
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
                                    if s1 > s2 { total_w1 += 1; }
                                    else if s2 > s1 { total_w2 += 1; }
                                    else { total_tie += 1; }
                                }
                            }
                        }
                    }
                }
            }
        }
        (total_w1, total_w2, total_tie, valid_combos)
    }).collect();

    let elapsed = t1.elapsed();
    println!("Computed {} pairs in {:?} ({:.2} s per pair on 4 cores)",
        results.len(), elapsed, elapsed.as_secs_f64() / (results.len() as f64));
}
