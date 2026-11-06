// Exact Integer Backward Induction Solver for Jehn's Random-Basket Coin Game
// Solver 1 (Lens 1): Multi-Threaded Colex-Ranked Layered DP in Rust
// Target: coin-basket-random-expected-values (A391791, A391792, Jehn Conjecture)

use std::env;
use std::thread;
use std::time::Instant;

/// Precompute binomial coefficients C[n][k]
fn precompute_comb(max_n: usize) -> Vec<Vec<usize>> {
    let mut c = vec![vec![0usize; max_n + 1]; max_n + 1];
    for i in 0..=max_n {
        c[i][0] = 1;
        for j in 1..=i {
            c[i][j] = c[i - 1][j - 1] + c[i - 1][j];
        }
    }
    c
}

/// Compute colexicographical rank of an m-combination
#[inline(always)]
fn colex_rank(bits: &[usize], c_table: &[Vec<usize>]) -> usize {
    let mut r = 0;
    for (i, &b) in bits.iter().enumerate() {
        r += c_table[b][i + 1];
    }
    r
}

/// Extract set bits into a small array/slice
#[inline(always)]
fn extract_bits(mut mask: u32, out: &mut [usize]) -> usize {
    let mut count = 0;
    while mask != 0 {
        let bit = mask.trailing_zeros() as usize;
        out[count] = bit;
        count += 1;
        mask &= mask - 1;
    }
    count
}

pub struct K2Result {
    pub n: usize,
    pub a_n: u64,
    pub optimal_first_coins: Vec<usize>,
    pub conjecture_holds: bool,
    pub conjecture_coin: usize,
}

pub fn solve_k2(n: usize, verbose: bool) -> K2Result {
    let t0 = Instant::now();
    let num_threads = thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let s_n = n * (n + 1) / 2;
    let c_table = precompute_comb(n + 2);

    // Layer 0: m = 0 (empty subset remaining)
    // Placed sum is S_n. d in [S_n % 2, S_n] with step 2.
    // W(empty, d) = (S_n + d) / 2
    let num_h_0 = s_n / 2 + 1;
    let mut prev_layer: Vec<u64> = Vec::with_capacity(num_h_0);
    for h in 0..num_h_0 {
        let d = (s_n % 2) + 2 * h;
        prev_layer.push(((s_n + d) / 2) as u64);
    }
    let mut prev_offsets: Vec<usize> = vec![0, num_h_0];

    let mut optimal_first_coins = Vec::new();
    let mut first_move_vals: Vec<(usize, u64)> = Vec::new();

    for m in 1..=n {
        let num_subsets = c_table[n][m];
        let mut curr_masks = vec![0u32; num_subsets];

        // Generate combinations of size m and place each at its colex rank
        // We can iterate over combinations using Gosper's hack or recursion
        fn gen_combs(
            idx: usize,
            m_rem: usize,
            n: usize,
            current_mask: u32,
            bits: &mut Vec<usize>,
            c_table: &[Vec<usize>],
            masks: &mut [u32],
        ) {
            if m_rem == 0 {
                let rank = colex_rank(bits, c_table);
                masks[rank] = current_mask;
                return;
            }
            if n - idx < m_rem {
                return;
            }
            // Include idx
            bits.push(idx);
            gen_combs(idx + 1, m_rem - 1, n, current_mask | (1 << idx), bits, c_table, masks);
            bits.pop();
            // Exclude idx
            gen_combs(idx + 1, m_rem, n, current_mask, bits, c_table, masks);
        }

        let mut bits_buf = Vec::with_capacity(m);
        gen_combs(0, m, n, 0, &mut bits_buf, &c_table, &mut curr_masks);

        // Precompute offsets for current layer
        let mut curr_offsets = Vec::with_capacity(num_subsets + 1);
        curr_offsets.push(0);
        let mut total_entries = 0usize;
        for &mask in &curr_masks {
            // Placed sum P(R)
            let mut sum_r = 0usize;
            let mut tmp = mask;
            while tmp != 0 {
                let b = tmp.trailing_zeros() as usize;
                sum_r += b + 1;
                tmp &= tmp - 1;
            }
            let p_r = s_n - sum_r;
            let num_h = p_r / 2 + 1;
            total_entries += num_h;
            curr_offsets.push(total_entries);
        }

        let mut curr_layer = vec![0u64; total_entries];

        // If m == n, we can capture optimal first moves from layer n-1 before computing m=n
        if m == n {
            // Full mask is curr_masks[0]
            let full_mask = curr_masks[0];
            let mut best_val = 0u64;
            for coin in 1..=n {
                let rem_mask = full_mask ^ (1 << (coin - 1));
                let mut rem_bits = [0usize; 32];
                let rem_count = extract_bits(rem_mask, &mut rem_bits[..m - 1]);
                let rem_rank = colex_rank(&rem_bits[..rem_count], &c_table);
                let rem_off = prev_offsets[rem_rank];
                let h_coin = coin / 2;
                let val = prev_layer[rem_off + h_coin];
                first_move_vals.push((coin, val));
                if val > best_val {
                    best_val = val;
                    optimal_first_coins = vec![coin];
                } else if val == best_val {
                    optimal_first_coins.push(coin);
                }
            }
        }

        // Parallelize over subsets in chunks
        let chunk_size = (num_subsets + num_threads - 1) / num_threads;
        let prev_layer_ref = &prev_layer;
        let prev_offsets_ref = &prev_offsets;
        let curr_offsets_ref = &curr_offsets;
        let curr_masks_ref = &curr_masks;
        let c_table_ref = &c_table;

        thread::scope(|s| {
            // To safely mutate non-overlapping slices of curr_layer:
            // We can split curr_layer at chunk boundary offsets!
            let mut threads = Vec::new();
            for thread_id in 0..num_threads {
                let start_idx = thread_id * chunk_size;
                let end_idx = (start_idx + chunk_size).min(num_subsets);
                if start_idx >= end_idx {
                    continue;
                }
                let start_entry = curr_offsets_ref[start_idx];
                let end_entry = curr_offsets_ref[end_idx];

                // Split slice
                threads.push((start_idx, end_idx, start_entry, end_entry));
            }

            // We use raw pointer or split_at_mut for safe disjoint slice writes
            let curr_ptr = curr_layer.as_mut_ptr() as usize;

            for (start_idx, end_idx, start_entry, end_entry) in threads {
                s.spawn(move || {
                    let slice = unsafe {
                        std::slice::from_raw_parts_mut(
                            (curr_ptr as *mut u64).add(start_entry),
                            end_entry - start_entry,
                        )
                    };
                    let mut bits = [0usize; 32];
                    let mut rem_bits = [0usize; 32];

                    for r in start_idx..end_idx {
                        let mask = curr_masks_ref[r];
                        let off = curr_offsets_ref[r] - start_entry;
                        let k = extract_bits(mask, &mut bits[..m]);

                        let mut sum_r = 0usize;
                        for &b in &bits[..k] {
                            sum_r += b + 1;
                        }
                        let p_r = s_n - sum_r;
                        let num_h = p_r / 2 + 1;

                        let dest = &mut slice[off..off + num_h];

                        // Arrays for max
                        let mut best_b1 = vec![0u64; num_h];
                        let mut best_b2 = vec![0u64; num_h];

                        for j in 0..k {
                            let coin = bits[j] + 1;
                            // Remaining bits without bits[j]
                            let mut rc = 0;
                            for (l, &b) in bits[..k].iter().enumerate() {
                                if l != j {
                                    rem_bits[rc] = b;
                                    rc += 1;
                                }
                            }
                            let rem_rank = colex_rank(&rem_bits[..rc], c_table_ref);
                            let rem_off = prev_offsets_ref[rem_rank];
                            let prev_slice = &prev_layer_ref[rem_off..];

                            for h in 0..num_h {
                                let d = (p_r % 2) + 2 * h;
                                // Basket 1: d + coin
                                let h1 = (d + coin) / 2;
                                let v1 = prev_slice[h1];
                                if v1 > best_b1[h] {
                                    best_b1[h] = v1;
                                }
                                // Basket 2: |d - coin|
                                let d2 = if d >= coin { d - coin } else { coin - d };
                                let h2 = d2 / 2;
                                let v2 = prev_slice[h2];
                                if v2 > best_b2[h] {
                                    best_b2[h] = v2;
                                }
                            }
                        }

                        for h in 0..num_h {
                            dest[h] = best_b1[h] + best_b2[h];
                        }
                    }
                });
            }
        });

        prev_layer = curr_layer;
        prev_offsets = curr_offsets;
    }

    let a_n = prev_layer[0] / 2;
    let conj_coin = (n + 3) / 2;
    let conj_holds = optimal_first_coins.contains(&conj_coin);

    if verbose {
        let elapsed = t0.elapsed();
        println!(
            "k=2, n={:2}: a(n) = {:12} | opt first: {:?} (conj={}, match={}) [{:?}]",
            n, a_n, optimal_first_coins, conj_coin, conj_holds, elapsed
        );
    }

    K2Result {
        n,
        a_n,
        optimal_first_coins,
        conjecture_holds: conj_holds,
        conjecture_coin: conj_coin,
    }
}

pub fn solve_k3(n: usize, verbose: bool) -> u64 {
    let t0 = Instant::now();
    let num_threads = thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let s_n = n * (n + 1) / 2;
    let c_table = precompute_comb(n + 2);

    // Build precomputed sorted triples and lookup tables for P in 0..=S_n
    // A sorted triple (s1, s2, s3) with s1 >= s2 >= s3 >= 0 and s1 + s2 + s3 = P
    let mut p_triples: Vec<Vec<(u16, u16, u16)>> = Vec::with_capacity(s_n + 1);
    for p in 0..=s_n {
        let mut trips = Vec::new();
        let min_s1 = (p + 2) / 3;
        for s1 in min_s1..=p {
            let min_s2 = (p - s1 + 1) / 2;
            let max_s2 = s1.min(p - s1);
            for s2 in min_s2..=max_s2 {
                let s3 = p - s1 - s2;
                trips.push((s1 as u16, s2 as u16, s3 as u16));
            }
        }
        p_triples.push(trips);
    }

    // Direct lookup: given (s1, s2, s3) sorted descending, return index in p_triples[s1+s2+s3]
    // Since s1 <= s_n and s2 <= s1, we can store flat index lookup per P:
    // for given P, offset for s1: offset[P][s1] + (s2 - min_s2(P, s1))
    let mut p_s1_offset: Vec<Vec<u16>> = Vec::with_capacity(s_n + 1);
    let mut p_s1_min_s2: Vec<Vec<u16>> = Vec::with_capacity(s_n + 1);

    for p in 0..=s_n {
        let min_s1 = (p + 2) / 3;
        let mut offs = vec![0u16; p + 1];
        let mut min_s2s = vec![0u16; p + 1];
        let mut cur_idx = 0u16;

        for s1 in min_s1..=p {
            let min_s2 = (p - s1 + 1) / 2;
            let max_s2 = s1.min(p - s1);
            offs[s1] = cur_idx;
            min_s2s[s1] = min_s2 as u16;
            if max_s2 >= min_s2 {
                cur_idx += (max_s2 - min_s2 + 1) as u16;
            }
        }
        p_s1_offset.push(offs);
        p_s1_min_s2.push(min_s2s);
    }

    #[inline(always)]
    fn get_triple_idx(
        mut a: usize,
        mut b: usize,
        mut c: usize,
        p_s1_offset: &[Vec<u16>],
        p_s1_min_s2: &[Vec<u16>],
    ) -> usize {
        // Sort a, b, c descending
        if a < b {
            std::mem::swap(&mut a, &mut b);
        }
        if b < c {
            std::mem::swap(&mut b, &mut c);
        }
        if a < b {
            std::mem::swap(&mut a, &mut b);
        }
        let p = a + b + c;
        let off = p_s1_offset[p][a] as usize;
        let min_s2 = p_s1_min_s2[p][a] as usize;
        off + (b - min_s2)
    }

    // Layer 0: m = 0 (empty subset remaining)
    // Placed sum is S_n. Triples summing to S_n.
    // W(empty, s) = max(s1, s2, s3) = s1
    let num_trips_0 = p_triples[s_n].len();
    let mut prev_layer: Vec<u64> = Vec::with_capacity(num_trips_0);
    for &(s1, _s2, _s3) in &p_triples[s_n] {
        prev_layer.push(s1 as u64);
    }
    let mut prev_offsets: Vec<usize> = vec![0, num_trips_0];

    for m in 1..=n {
        let num_subsets = c_table[n][m];
        let mut curr_masks = vec![0u32; num_subsets];

        fn gen_combs(
            idx: usize,
            m_rem: usize,
            n: usize,
            current_mask: u32,
            bits: &mut Vec<usize>,
            c_table: &[Vec<usize>],
            masks: &mut [u32],
        ) {
            if m_rem == 0 {
                let rank = colex_rank(bits, c_table);
                masks[rank] = current_mask;
                return;
            }
            if n - idx < m_rem {
                return;
            }
            bits.push(idx);
            gen_combs(idx + 1, m_rem - 1, n, current_mask | (1 << idx), bits, c_table, masks);
            bits.pop();
            gen_combs(idx + 1, m_rem, n, current_mask, bits, c_table, masks);
        }

        let mut bits_buf = Vec::with_capacity(m);
        gen_combs(0, m, n, 0, &mut bits_buf, &c_table, &mut curr_masks);

        let mut curr_offsets = Vec::with_capacity(num_subsets + 1);
        curr_offsets.push(0);
        let mut total_entries = 0usize;
        for &mask in &curr_masks {
            let mut sum_r = 0usize;
            let mut tmp = mask;
            while tmp != 0 {
                let b = tmp.trailing_zeros() as usize;
                sum_r += b + 1;
                tmp &= tmp - 1;
            }
            let p_r = s_n - sum_r;
            let num_trips = p_triples[p_r].len();
            total_entries += num_trips;
            curr_offsets.push(total_entries);
        }

        let mut curr_layer = vec![0u64; total_entries];

        let chunk_size = (num_subsets + num_threads - 1) / num_threads;
        let prev_layer_ref = &prev_layer;
        let prev_offsets_ref = &prev_offsets;
        let curr_offsets_ref = &curr_offsets;
        let curr_masks_ref = &curr_masks;
        let c_table_ref = &c_table;
        let p_triples_ref = &p_triples;
        let p_s1_offset_ref = &p_s1_offset;
        let p_s1_min_s2_ref = &p_s1_min_s2;

        thread::scope(|s| {
            let mut threads = Vec::new();
            for thread_id in 0..num_threads {
                let start_idx = thread_id * chunk_size;
                let end_idx = (start_idx + chunk_size).min(num_subsets);
                if start_idx >= end_idx {
                    continue;
                }
                let start_entry = curr_offsets_ref[start_idx];
                let end_entry = curr_offsets_ref[end_idx];
                threads.push((start_idx, end_idx, start_entry, end_entry));
            }

            let curr_ptr = curr_layer.as_mut_ptr() as usize;

            for (start_idx, end_idx, start_entry, end_entry) in threads {
                s.spawn(move || {
                    let slice = unsafe {
                        std::slice::from_raw_parts_mut(
                            (curr_ptr as *mut u64).add(start_entry),
                            end_entry - start_entry,
                        )
                    };
                    let mut bits = [0usize; 32];
                    let mut rem_bits = [0usize; 32];

                    for r in start_idx..end_idx {
                        let mask = curr_masks_ref[r];
                        let off = curr_offsets_ref[r] - start_entry;
                        let k = extract_bits(mask, &mut bits[..m]);

                        let mut sum_r = 0usize;
                        for &b in &bits[..k] {
                            sum_r += b + 1;
                        }
                        let p_r = s_n - sum_r;
                        let trips = &p_triples_ref[p_r];
                        let num_trips = trips.len();

                        let dest = &mut slice[off..off + num_trips];

                        let mut best_b1 = vec![0u64; num_trips];
                        let mut best_b2 = vec![0u64; num_trips];
                        let mut best_b3 = vec![0u64; num_trips];

                        for j in 0..k {
                            let coin = bits[j] + 1;
                            let mut rc = 0;
                            for (l, &b) in bits[..k].iter().enumerate() {
                                if l != j {
                                    rem_bits[rc] = b;
                                    rc += 1;
                                }
                            }
                            let rem_rank = colex_rank(&rem_bits[..rc], c_table_ref);
                            let rem_off = prev_offsets_ref[rem_rank];
                            let prev_slice = &prev_layer_ref[rem_off..];

                            for (t_idx, &(s1, s2, s3)) in trips.iter().enumerate() {
                                let (u1, u2, u3) = (s1 as usize, s2 as usize, s3 as usize);

                                // Basket 1: u1 + coin
                                let idx1 = get_triple_idx(
                                    u1 + coin,
                                    u2,
                                    u3,
                                    p_s1_offset_ref,
                                    p_s1_min_s2_ref,
                                );
                                let v1 = prev_slice[idx1];
                                if v1 > best_b1[t_idx] {
                                    best_b1[t_idx] = v1;
                                }

                                // Basket 2: u2 + coin
                                let idx2 = get_triple_idx(
                                    u1,
                                    u2 + coin,
                                    u3,
                                    p_s1_offset_ref,
                                    p_s1_min_s2_ref,
                                );
                                let v2 = prev_slice[idx2];
                                if v2 > best_b2[t_idx] {
                                    best_b2[t_idx] = v2;
                                }

                                // Basket 3: u3 + coin
                                let idx3 = get_triple_idx(
                                    u1,
                                    u2,
                                    u3 + coin,
                                    p_s1_offset_ref,
                                    p_s1_min_s2_ref,
                                );
                                let v3 = prev_slice[idx3];
                                if v3 > best_b3[t_idx] {
                                    best_b3[t_idx] = v3;
                                }
                            }
                        }

                        for t in 0..num_trips {
                            dest[t] = best_b1[t] + best_b2[t] + best_b3[t];
                        }
                    }
                });
            }
        });

        prev_layer = curr_layer;
        prev_offsets = curr_offsets;
    }

    let a_n = prev_layer[0] / 3;
    if verbose {
        let elapsed = t0.elapsed();
        println!("k=3, n={:2}: a(n) = {:16} [{:?}]", n, a_n, elapsed);
    }
    a_n
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("all");

    println!("=== Solver 1 (Rust): Exact Integer Backward Induction ===");
    println!("Target: coin-basket-random-expected-values");

    if mode == "k2" || mode == "all" {
        println!("\n--- Computing OEIS A391791 (k=2) for n=1..25 & Jehn Conjecture ---");
        let max_n = 25;
        let mut results = Vec::new();
        for n in 1..=max_n {
            let res = solve_k2(n, true);
            results.push(res);
        }

        println!("\n=== Summary A391791 (k=2) ===");
        for r in &results {
            println!("A391791({:2}) = {}", r.n, r.a_n);
        }

        println!("\n=== Jehn Conjecture Audit (n=10..25) ===");
        let mut all_conj_hold = true;
        for r in &results {
            if r.n >= 10 {
                let holds = r.optimal_first_coins == vec![r.conjecture_coin];
                println!(
                    "n={:2}: opt={:?}, conj_coin={}, strictly_unique_match={}",
                    r.n, r.optimal_first_coins, r.conjecture_coin, holds
                );
                if !r.conjecture_holds {
                    all_conj_hold = false;
                }
            }
        }
        println!("Jehn conjecture holds for all n=10..25: {}", all_conj_hold);
    }

    if mode == "k3" || mode == "all" {
        println!("\n--- Computing OEIS A391792 (k=3) for n=1..21 ---");
        let max_n = 21;
        let mut k3_results = Vec::new();
        for n in 1..=max_n {
            let ans = solve_k3(n, true);
            k3_results.push((n, ans));
        }

        println!("\n=== Summary A391792 (k=3) ===");
        for (n, val) in &k3_results {
            println!("A391792({:2}) = {}", n, val);
        }
    }
}
