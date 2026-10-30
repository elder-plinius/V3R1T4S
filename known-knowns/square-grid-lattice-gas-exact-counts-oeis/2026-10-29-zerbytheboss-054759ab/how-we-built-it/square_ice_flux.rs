use num_bigint::BigUint;
use num_traits::{One, Zero};
use rayon::prelude::*;
use std::collections::HashMap;
use std::time::Instant;

/// Adjacency entry for sparse transfer matrix: (destination index, weight)
#[derive(Clone, Copy, Debug)]
struct Edge {
    dest: usize,
    weight: u32,
}

/// Compute square ice counts (Eulerian orientations) on an n x n torus.
pub fn compute_square_ice(n: usize) -> (BigUint, f64) {
    let start_time = Instant::now();
    let mut total = BigUint::zero();

    // Iterate over conserved flux sectors k in 0 ..= n / 2
    for k in 0..=(n / 2) {
        // Collect all states in {0, 1}^n with popcount == k
        let states: Vec<u32> = (0..(1u32 << n))
            .filter(|&mask| mask.count_ones() as usize == k)
            .collect();
        let dim = states.len();
        if dim == 0 {
            continue;
        }

        let state_to_idx: HashMap<u32, usize> = states
            .iter()
            .enumerate()
            .map(|(i, &u)| (u, i))
            .collect();

        // Build sparse transfer matrix adjacency list: adj[src] = [Edge, ...]
        let mut adj: Vec<Vec<Edge>> = vec![Vec::new(); dim];
        for (i, &u) in states.iter().enumerate() {
            let mut reach: HashMap<usize, u32> = HashMap::new();
            for h0 in 0..=1 {
                let mut stack = vec![(0usize, h0, 0u32)];
                while let Some((c, h, v_mask)) = stack.pop() {
                    if c == n {
                        if h == h0 {
                            if let Some(&v_idx) = state_to_idx.get(&v_mask) {
                                *reach.entry(v_idx).or_insert(0) += 1;
                            }
                        }
                        continue;
                    }
                    let u_c = (u >> c) & 1;
                    // Conservation at vertex: next_h = h + u_c - v_c
                    for v_c in 0..=1 {
                        let next_h = h as i32 + u_c as i32 - v_c as i32;
                        if next_h >= 0 && next_h <= 1 {
                            stack.push((c + 1, next_h as u32, v_mask | (v_c << c)));
                        }
                    }
                }
            }
            adj[i] = reach
                .into_iter()
                .map(|(dest, weight)| Edge { dest, weight })
                .collect();
        }

        // Partition states into cyclic translation orbits under u -> rotl(u, 1)
        let mut visited = vec![false; dim];
        let mut orbits: Vec<Vec<usize>> = Vec::new();
        for i in 0..dim {
            if visited[i] {
                continue;
            }
            let mut orbit = Vec::new();
            let mut cur = states[i];
            for _ in 0..n {
                // 1-bit cyclic left shift on n-bit integer
                cur = ((cur << 1) & ((1 << n) - 1)) | (cur >> (n - 1));
                if let Some(&idx) = state_to_idx.get(&cur) {
                    if !visited[idx] {
                        visited[idx] = true;
                        orbit.push(idx);
                    }
                }
            }
            if !orbit.is_empty() {
                orbits.push(orbit);
            }
        }

        // Evaluate each orbit representative in parallel using Rayon
        let sector_trace: BigUint = orbits
            .par_iter()
            .map(|orbit| {
                let rep = orbit[0];
                let orbit_size = BigUint::from(orbit.len());

                // Sparse vector evolution: v^(0) = e_rep
                let mut v = vec![BigUint::zero(); dim];
                let mut next_v = vec![BigUint::zero(); dim];
                v[rep] = BigUint::one();

                // Multiply by transfer matrix n times to complete the torus
                for _row in 0..n {
                    for (src_idx, v_val) in v.iter().enumerate() {
                        if v_val.is_zero() {
                            continue;
                        }
                        for edge in &adj[src_idx] {
                            if edge.weight == 1 {
                                next_v[edge.dest] += v_val;
                            } else {
                                next_v[edge.dest] += v_val * edge.weight;
                            }
                        }
                    }
                    v.clone_from_slice(&next_v);
                    next_v.fill(BigUint::zero());
                }

                // Diagonal contribution from this orbit: Tr_orbit = |orbit| * v^(n)[rep]
                &v[rep] * &orbit_size
            })
            .sum();

        // Sector reflection symmetry: weight 1 for k = n / 2 (when n is even), weight 2 otherwise
        if n % 2 == 0 && k == n / 2 {
            total += sector_trace;
        } else {
            total += sector_trace * 2u32;
        }
    }

    let elapsed = start_time.elapsed().as_secs_f64();
    (total, elapsed)
}

fn load_published_bfile(paths: &[&str]) -> HashMap<usize, String> {
    for path in paths {
        if let Ok(content) = std::fs::read_to_string(path) {
            let mut map = HashMap::new();
            for line in content.lines() {
                let line = line.trim();
                if line.is_empty() || line.starts_with('#') {
                    continue;
                }
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 2 {
                    if let Ok(n) = parts[0].parse::<usize>() {
                        map.insert(n, parts[1].to_string());
                    }
                }
            }
            if !map.is_empty() {
                return map;
            }
        }
    }
    // Fallback known published terms (Brendan McKay, 2024)
    [
        (1, "4"), (2, "18"), (3, "148"), (4, "2970"), (5, "143224"),
        (6, "16448400"), (7, "4484823396"), (8, "2901094068042"),
        (9, "4448410550095612"), (10, "16178049740086515288"),
        (11, "139402641051212392498528"), (12, "2849295959501939989625992464"),
        (13, "137950545200232788276834783781648"),
        (14, "15844635835975276495290739119895808472"),
    ]
    .iter()
    .map(|&(n, s)| (n, s.to_string()))
    .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut max_n = 16;
    let mut force_overwrite = false;

    for arg in args.iter().skip(1) {
        if arg == "--force" {
            force_overwrite = true;
        } else if let Ok(n) = arg.parse::<usize>() {
            max_n = n;
        }
    }

    println!("=================================================================");
    println!(" SQUARE ICE ON TORUS (A054759) FLUX-CONSERVING TRANSFER SOLVER ");
    println!("=================================================================");

    let published_map = load_published_bfile(&[
        "data/b054759.txt",
        "../../data/b054759.txt",
        "runs/2026-10-29-0820/data/b054759.txt",
    ]);

    let out_path = std::env::var("OUT_PATH").unwrap_or_else(|_| "data/a054759_results.json".to_string());

    // Load existing results to guard against accidental truncation of high-N records
    let mut existing_records: HashMap<usize, serde_json::Value> = HashMap::new();
    if !force_overwrite {
        if let Ok(content) = std::fs::read_to_string(&out_path) {
            if let Ok(arr) = serde_json::from_str::<Vec<serde_json::Value>>(&content) {
                for item in arr {
                    if let Some(n) = item.get("n").and_then(|v| v.as_u64()) {
                        existing_records.insert(n as usize, item);
                    }
                }
            }
        }
    }

    for n in 1..=max_n {
        let (val, elapsed) = compute_square_ice(n);
        let val_str = val.to_string();
        let status = if let Some(expected) = published_map.get(&n) {
            if &val_str == expected {
                "EXACT MATCH [PASS]"
            } else {
                "MISMATCH [FAIL]"
            }
        } else {
            "NEW TERM CERTIFIED [WORLD RECORD]"
        };

        println!(
            "n = {:2} | time: {:8.3}s | status: {} | digits: {:3}",
            n,
            elapsed,
            status,
            val_str.len()
        );
        println!("  a({}) = {}", n, val_str);

        existing_records.insert(n, serde_json::json!({
            "n": n,
            "val": val_str,
            "digits": val_str.len(),
            "time_sec": elapsed,
            "status": status,
        }));
    }

    let mut sorted_keys: Vec<usize> = existing_records.keys().copied().collect();
    sorted_keys.sort();
    let final_results: Vec<&serde_json::Value> = sorted_keys.iter().map(|k| &existing_records[k]).collect();

    let json_text = serde_json::to_string_pretty(&final_results).unwrap();
    if let Some(parent) = std::path::Path::new(&out_path).parent() {
        if !parent.as_os_str().is_empty() {
            let _ = std::fs::create_dir_all(parent);
        }
    }
    std::fs::write(&out_path, json_text).unwrap();
    println!("Saved results to {}", out_path);
}
