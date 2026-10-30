use std::time::Instant;

// Fast 7-card evaluator test
// Ranks: 0..12 (2..A). Suits: 0..3 (c, d, h, s). Card = rank * 4 + suit.
struct Evaluator {
    flush_table: Vec<u16>,
    non_flush_table: Vec<u16>,
}

fn comb(n: usize, k: usize) -> usize {
    if k > n { return 0; }
    let mut res = 1;
    for i in 0..k {
        res = res * (n - i) / (i + 1);
    }
    res
}

fn multiset_index(sorted_ranks: &[u8; 7]) -> usize {
    let mut idx = 0;
    for (i, &r) in sorted_ranks.iter().enumerate() {
        idx += comb((r as usize) + i, i + 1);
    }
    idx
}

// 5-card evaluation for table generation
fn eval_5card_ranks(r: &[u8; 5], is_flush: bool) -> u16 {
    let mut counts = [0u8; 13];
    for &rank in r {
        counts[rank as usize] += 1;
    }
    let mut sorted_counts: Vec<(u8, u8)> = counts.iter().enumerate()
        .filter(|&(_, &c)| c > 0)
        .map(|(rank, &c)| (c, rank as u8))
        .collect();
    sorted_counts.sort_by(|a, b| b.0.cmp(&a.0).then_with(|| b.1.cmp(&a.1)));

    let mut r_sorted = *r;
    r_sorted.sort_unstable_by(|a, b| b.cmp(a));

    let mut is_straight = false;
    let mut straight_high = 0u8;
    if sorted_counts.len() == 5 {
        if r_sorted[0] - r_sorted[4] == 4 {
            is_straight = true;
            straight_high = r_sorted[0];
        } else if r_sorted == [12, 3, 2, 1, 0] {
            is_straight = true;
            straight_high = 3;
        }
    }

    if is_flush && is_straight {
        return 7000 + (straight_high as u16);
    }
    if sorted_counts[0].0 == 4 {
        return 6000 + (sorted_counts[0].1 as u16) * 15 + (sorted_counts[1].1 as u16);
    }
    if sorted_counts[0].0 == 3 && sorted_counts[1].0 == 2 {
        return 5000 + (sorted_counts[0].1 as u16) * 15 + (sorted_counts[1].1 as u16);
    }
    if is_flush {
        return 4000 + (r_sorted[0] as u16) * 200 + (r_sorted[1] as u16) * 15 + (r_sorted[2] as u16);
    }
    if is_straight {
        return 3000 + (straight_high as u16);
    }
    if sorted_counts[0].0 == 3 {
        return 2000 + (sorted_counts[0].1 as u16) * 200 + (sorted_counts[1].1 as u16) * 15 + (sorted_counts[2].1 as u16);
    }
    if sorted_counts[0].0 == 2 && sorted_counts[1].0 == 2 {
        return 1000 + (sorted_counts[0].1 as u16) * 200 + (sorted_counts[1].1 as u16) * 15 + (sorted_counts[2].1 as u16);
    }
    if sorted_counts[0].0 == 2 {
        return 500 + (sorted_counts[0].1 as u16) * 200 + (sorted_counts[1].1 as u16) * 15 + (sorted_counts[2].1 as u16);
    }
    // High card
    (r_sorted[0] as u16) * 200 + (r_sorted[1] as u16) * 15 + (r_sorted[2] as u16)
}

fn best_5_of_7_ranks(ranks: &[u8; 7], is_flush: bool) -> u16 {
    let mut best = 0;
    // Choose 5 of 7
    for i in 0..7 {
        for j in (i+1)..7 {
            let mut sub = [0u8; 5];
            let mut k = 0;
            for idx in 0..7 {
                if idx != i && idx != j {
                    sub[k] = ranks[idx];
                    k += 1;
                }
            }
            let score = eval_5card_ranks(&sub, is_flush);
            if score > best {
                best = score;
            }
        }
    }
    best
}

impl Evaluator {
    fn new() -> Self {
        // 1. Generate flush table (13-bit masks)
        let mut flush_table = vec![0u16; 8192];
        for mask in 0..8192usize {
            let mut ranks = Vec::new();
            for r in 0..13 {
                if (mask & (1 << r)) != 0 {
                    ranks.push(r as u8);
                }
            }
            if ranks.len() >= 5 {
                // best 5 cards
                let mut best = 0;
                let n = ranks.len();
                // iterate all 5-combinations
                for c in 0..(1 << n) {
                    if (c as u32).count_ones() == 5 {
                        let mut sub = [0u8; 5];
                        let mut ki = 0;
                        for b in 0..n {
                            if (c & (1 << b)) != 0 {
                                sub[ki] = ranks[b];
                                ki += 1;
                            }
                        }
                        let score = eval_5card_ranks(&sub, true);
                        if score > best { best = score; }
                    }
                }
                flush_table[mask] = best;
            }
        }

        // 2. Generate non-flush table (50,388 entries)
        let mut non_flush_table = vec![0u16; 50388];
        let mut sorted = [0u8; 7];
        fn fill(pos: usize, min_r: u8, sorted: &mut [u8; 7], table: &mut [u16]) {
            if pos == 7 {
                let idx = multiset_index(sorted);
                table[idx] = best_5_of_7_ranks(sorted, false);
                return;
            }
            for r in min_r..13 {
                sorted[pos] = r;
                fill(pos + 1, r, sorted, table);
            }
        }
        fill(0, 0, &mut sorted, &mut non_flush_table);

        Evaluator { flush_table, non_flush_table }
    }

    #[inline(always)]
    fn eval_7(&self, cards: &[u8; 7]) -> u16 {
        let mut suit_counts = [0u8; 4];
        let mut suit_masks = [0u16; 4];
        let mut ranks = [0u8; 7];

        for i in 0..7 {
            let c = cards[i];
            let r = c >> 2;
            let s = (c & 3) as usize;
            suit_counts[s] += 1;
            suit_masks[s] |= 1 << r;
            ranks[i] = r;
        }

        // Check flush
        for s in 0..4 {
            if suit_counts[s] >= 5 {
                return self.flush_table[suit_masks[s] as usize];
            }
        }

        // Sort ranks for multiset lookup
        ranks.sort_unstable();
        let idx = multiset_index(&ranks);
        self.non_flush_table[idx]
    }
}

fn main() {
    let t0 = Instant::now();
    let eval = Evaluator::new();
    println!("Evaluator initialized in {:?}", t0.elapsed());

    // Benchmark speed
    let test_hand = [0, 4, 8, 12, 16, 20, 24]; // 2c, 3c, 4c, 5c, 6c, 7c, 8c (straight flush)
    let score = eval.eval_7(&test_hand);
    println!("Test hand score: {}", score);

    let n = 10_000_000;
    let t1 = Instant::now();
    let mut sum = 0u64;
    for i in 0..n {
        let h = [
            (i % 52) as u8,
            ((i + 1) % 52) as u8,
            ((i + 5) % 52) as u8,
            ((i + 9) % 52) as u8,
            ((i + 13) % 52) as u8,
            ((i + 17) % 52) as u8,
            ((i + 21) % 52) as u8,
        ];
        sum = sum.wrapping_add(eval.eval_7(&h) as u64);
    }
    let elapsed = t1.elapsed();
    println!("Evaluated {} hands in {:?} ({:.1} million hands/sec)",
        n, elapsed, (n as f64) / elapsed.as_secs_f64() / 1e6);
}
