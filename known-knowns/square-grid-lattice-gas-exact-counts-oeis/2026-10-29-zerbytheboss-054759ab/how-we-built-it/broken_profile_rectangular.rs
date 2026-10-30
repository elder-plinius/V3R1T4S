use num_bigint::BigUint;
use num_traits::{One, Zero};
use std::time::Instant;

/// Fast broken-profile DP for Hard Squares (A089980) on an M x N grid
pub fn hard_squares_rect_fast(m: usize, n: usize) -> BigUint {
    if m == 0 || n == 0 {
        return BigUint::one();
    }
    let (w, len) = if m <= n { (m, n) } else { (n, m) };
    let size = 1usize << w;
    let mut dp0 = vec![BigUint::zero(); size];
    let mut dp1 = vec![BigUint::zero(); size];
    dp0[0] = BigUint::one();

    for _r in 0..len {
        for c in 0..w {
            let mut next_dp0 = vec![BigUint::zero(); size];
            let mut next_dp1 = vec![BigUint::zero(); size];
            let mask_low = (1usize << c) - 1;
            let mask_high = !mask_low;
            let half = 1usize << (w - 1);

            for u in 0..half {
                let low = u & mask_low;
                let high = (u & mask_high) << 1;
                let u0 = high | low;
                let u1 = u0 | (1usize << c);

                let val0 = &dp0[u0];
                let val1 = &dp0[u1];
                let carry0 = &dp1[u0];
                let carry1 = &dp1[u1];

                let mut s0 = val0 + val1;
                s0 += carry0;
                s0 += carry1;

                next_dp0[u0] = s0;
                next_dp1[u1] = val0.clone();
            }
            dp0 = next_dp0;
            dp1 = next_dp1;
        }
        for i in 0..size {
            if !dp1[i].is_zero() {
                dp0[i] += std::mem::take(&mut dp1[i]);
            }
        }
    }
    dp0.iter().cloned().sum()
}

/// Fast broken-profile DP for Monomer-Dimer (A210662) on an M x N grid
pub fn monomer_dimer_rect_fast(m: usize, n: usize) -> BigUint {
    if m == 0 || n == 0 {
        return BigUint::one();
    }
    let (w, len) = if m <= n { (m, n) } else { (n, m) };
    let size = 1usize << w;
    let mut dp0 = vec![BigUint::zero(); size];
    let mut dp1 = vec![BigUint::zero(); size];
    dp0[0] = BigUint::one();

    for r in 0..len {
        for c in 0..w {
            let mut next_dp0 = vec![BigUint::zero(); size];
            let mut next_dp1 = vec![BigUint::zero(); size];
            let mask_low = (1usize << c) - 1;
            let mask_high = !mask_low;
            let half = 1usize << (w - 1);

            for u in 0..half {
                let low = u & mask_low;
                let high = (u & mask_high) << 1;
                let u0 = high | low;
                let u1 = u0 | (1usize << c);

                let val0 = &dp0[u0];
                let val1 = &dp0[u1];
                let carry = &dp1[u0];

                let s0 = val0 + val1 + carry;
                next_dp0[u0] = s0;

                if r + 1 < len {
                    next_dp0[u1] = val0.clone();
                }

                if c + 1 < w {
                    next_dp1[u0] = val0.clone();
                }
            }
            dp0 = next_dp0;
            dp1 = next_dp1;
        }
        for x in dp1.iter_mut() {
            *x = BigUint::zero();
        }
    }
    dp0[0].clone()
}

fn main() {
    println!("=================================================================");
    println!(" RECTANGULAR STRIP SOLVER: ROW 28 OF A210662 & A089980 (p2)     ");
    println!("=================================================================");

    let row = 28;

    // 1. Compute Row 28 of A089980 (Hard Squares on 28 x k)
    println!("\n--- Computing A089980 (Hard Squares) Row 28 for k = 1..20 ---");
    let mut hs_results = Vec::new();
    for k in 1..=20 {
        let t0 = Instant::now();
        let val = hard_squares_rect_fast(row, k);
        let elapsed = t0.elapsed().as_secs_f64();
        println!("A089980(28, {:2}) = {} (time: {:6.3}s, digits: {})", k, val, elapsed, val.to_string().len());
        hs_results.push(serde_json::json!({
            "m": row,
            "n": k,
            "val": val.to_string(),
            "digits": val.to_string().len(),
            "time_sec": elapsed
        }));
    }

    let out_hs = std::env::var("OUT_HS").unwrap_or_else(|_| "data/a089980_row28.json".to_string());
    if let Some(parent) = std::path::Path::new(&out_hs).parent() {
        if !parent.as_os_str().is_empty() {
            let _ = std::fs::create_dir_all(parent);
        }
    }
    std::fs::write(&out_hs, serde_json::to_string_pretty(&hs_results).unwrap()).unwrap();
    println!("Saved A089980 Row 28 to {}", out_hs);

    // 2. Compute Row 28 of A210662 (Monomer-Dimer on 28 x k for k = 1..18)
    println!("\n--- Computing A210662 (Monomer-Dimer) Row 28 for k = 1..18 ---");
    let mut md_results = Vec::new();
    for k in 1..=18 {
        let t0 = Instant::now();
        let val = monomer_dimer_rect_fast(row, k);
        let elapsed = t0.elapsed().as_secs_f64();
        println!("A210662(28, {:2}) = {} (time: {:6.3}s, digits: {})", k, val, elapsed, val.to_string().len());
        md_results.push(serde_json::json!({
            "m": row,
            "n": k,
            "val": val.to_string(),
            "digits": val.to_string().len(),
            "time_sec": elapsed
        }));
    }

    let out_md = std::env::var("OUT_MD").unwrap_or_else(|_| "data/a210662_row28.json".to_string());
    if let Some(parent) = std::path::Path::new(&out_md).parent() {
        if !parent.as_os_str().is_empty() {
            let _ = std::fs::create_dir_all(parent);
        }
    }
    std::fs::write(&out_md, serde_json::to_string_pretty(&md_results).unwrap()).unwrap();
    println!("Saved A210662 Row 28 to {}", out_md);
}
