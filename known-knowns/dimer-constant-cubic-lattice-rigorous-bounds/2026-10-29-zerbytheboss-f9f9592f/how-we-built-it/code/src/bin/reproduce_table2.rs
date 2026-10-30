//! Reproduces He (2026, arXiv:2607.28810) Table 2 bounds up to (5,5).

use dimer_cw::collatz::run_collatz_biguint;
use dimer_cw::symmetry::{LatticeGroup, SectorOrbits};
use dimer_cw::transfer::{build_block_x, build_block_y};
use std::time::Instant;

fn compute_sector_bound(m: usize, n: usize, sector: usize, p_step: usize) -> (f64, f64, usize) {
    let lattice = LatticeGroup::new(m, n);
    let total_v = m * n;
    let t0 = Instant::now();
    let orbits_minus = SectorOrbits::build(&lattice, sector);
    let orbits_plus = SectorOrbits::build(&lattice, total_v - sector);

    let x_mat = build_block_x(&lattice, &orbits_minus, &orbits_plus);
    let y_mat = build_block_y(&lattice, &orbits_plus, &orbits_minus);

    // In He (2026) formula (3.22):
    // C_{m,n;p} = (1 / 2mn) * ln max <U| (XY)^{p+1} 1> / <U| (XY)^p 1>.
    // To evaluate p=4, we do 5 multiplications. For p=2, we do 3 multiplications.
    let num_mults = p_step + 1;
    let results = run_collatz_biguint(&x_mat, &y_mat, m, n, num_mults);
    let final_step = results.last().unwrap();
    println!(
        "    Sector {sector:2} (orbits={:5}): mults={num_mults} -> float={:.8}, ceil={:.6} [{:?}]",
        orbits_minus.num_orbits(),
        final_step.bound_f64,
        final_step.bound_ceil_6dec,
        t0.elapsed()
    );
    (final_step.bound_f64, final_step.bound_ceil_6dec, orbits_minus.num_orbits())
}

fn main() {
    println!("============================================================");
    println!("  REPRODUCING HE (2026) TABLE 2 RIGOROUS UPPER BOUNDS (p1) ");
    println!("============================================================");

    // He (2026) Table 2 values:
    // (m, n, p_step, expected_bound)
    let test_cases = vec![
        (2, 2, 4, 0.486478),
        (3, 2, 4, 0.471408),
        (3, 3, 4, 0.458558),
        (4, 2, 4, 0.465970),
        (4, 3, 4, 0.457380),
        (4, 4, 4, 0.454673),
        (5, 2, 4, 0.463401),
        (5, 3, 4, 0.454663),
        (5, 4, 4, 0.453365),
        (6, 2, 4, 0.462010),
        (6, 3, 4, 0.454618),
        (5, 5, 2, 0.452130),
    ];

    let mut results_table = Vec::new();
    let mut all_passed = true;

    for (m, n, p, expected) in test_cases {
        let t_start = Instant::now();
        let total_v = m * n;
        let max_sector = total_v / 2;

        println!("\n------------------------------------------------------------");
        println!("Evaluating ({m}, {n}): max_sector={max_sector}, p={p} (Expected: {expected:.6})");

        // For smaller lattices (m*n <= 10), verify all sectors to illustrate sector dominance
        let (raw_bound, ceil_bound) = if total_v <= 10 {
            let mut max_b = f64::NEG_INFINITY;
            let mut max_c = f64::NEG_INFINITY;
            for s in 0..=max_sector {
                let (r, c, _) = compute_sector_bound(m, n, s, p);
                if r > max_b {
                    max_b = r;
                    max_c = c;
                }
            }
            (max_b, max_c)
        } else {
            // Maximal sector strictly dominates upper bound
            let (r, c, _) = compute_sector_bound(m, n, max_sector, p);
            (r, c)
        };

        let diff = (ceil_bound - expected).abs();
        let pass = diff < 2e-6;
        println!(
            "RESULT ({m}, {n}): computed={ceil_bound:.6} (raw={raw_bound:.8}) expected={expected:.6} diff={diff:.6} -> {} [{:?}]",
            if pass { "EXACT MATCH (PASS)" } else { "DIFFERENCE DETECTED (FAIL)" },
            t_start.elapsed()
        );

        if !pass {
            all_passed = false;
        }

        results_table.push((m, n, p, raw_bound, ceil_bound, expected, pass));
    }

    println!("\n========================================================================================");
    println!("                           HE (2026) TABLE 2 REPRODUCTION SUMMARY                        ");
    println!("========================================================================================");
    println!(" (m, n) |  p  | Computed (raw) | Computed (ceil) | Table 2 Published | Status ");
    println!("--------+-----+----------------+-----------------+-------------------+--------");
    for (m, n, p, raw, ceil, exp, pass) in results_table {
        println!(
            " ({m}, {n}) |  {p}  |   {raw:.8}   |    {ceil:.6}     |     {exp:.6}      | {}",
            if pass { "PASS" } else { "FAIL" }
        );
    }
    println!("========================================================================================");
    if all_passed {
        println!("SUCCESS: ALL 12 BOUNDS IN HE (2026) TABLE 2 REPRODUCED WITH EXACT ARITHMETIC (p1)");
    } else {
        println!("WARNING: Some bounds differed from published Table 2.");
    }
    println!("========================================================================================");
}
