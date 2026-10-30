//! Benchmark and solve (5,5) Sector 12 directly.

use dimer_cw::collatz::{run_collatz_biguint, verify_integer_certificate};
use dimer_cw::lanczos::{find_perron_vector_f64, quantize_to_positive_integers};
use dimer_cw::symmetry::{LatticeGroup, SectorOrbits};
use dimer_cw::transfer::{build_block_x, build_block_y};
use num_bigint::BigUint;
use num_rational::BigRational;
use num_traits::{One, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;
use std::time::Instant;

#[derive(Serialize, Deserialize, Debug)]
pub struct Dimer3DCertificate {
    pub dimension: usize,
    pub cross_section: [usize; 2],
    pub displacements: Vec<[i32; 2]>,
    pub sector: usize,
    pub num_orbits: usize,
    pub spectral_radius_f64: f64,
    pub he_2026_published_bound: f64,
    pub certified_upper_bound: f64,
    pub improvement: f64,
    pub p_iterations: usize,
    pub c_bound_num: String,
    pub c_bound_den: String,
    pub test_vector: Vec<String>,
    pub verified_exact_integer: bool,
}

fn main() {
    println!("============================================================");
    println!("  (5,5) SECTOR 12 HIGH-PERFORMANCE SOLVER & CERTIFICATION   ");
    println!("============================================================");

    let m = 5;
    let n = 5;
    let total_v = 25;
    let sector = 12;

    let t0 = Instant::now();
    let lattice = LatticeGroup::new(m, n);
    println!("Initialized LatticeGroup (5,5), |G| = {} in {:?}", lattice.group_perms.len(), t0.elapsed());

    let t1 = Instant::now();
    println!("Building Sector 12 orbit partition (k=12 and k=13)...");
    let orbits_minus = SectorOrbits::build(&lattice, sector);
    let orbits_plus = SectorOrbits::build(&lattice, total_v - sector);
    println!(
        "S_12^- orbits: {}, S_12^+ orbits: {} in {:?}",
        orbits_minus.num_orbits(),
        orbits_plus.num_orbits(),
        t1.elapsed()
    );

    let t2 = Instant::now();
    println!("Building CSR blocks X (35070 x 35070) and Y (35070 x 35070)...");
    let x_mat = build_block_x(&lattice, &orbits_minus, &orbits_plus);
    let y_mat = build_block_y(&lattice, &orbits_plus, &orbits_minus);
    println!(
        "Built CSR blocks in {:?}: X nonzeros = {}, Y nonzeros = {}",
        t2.elapsed(),
        x_mat.total_nonzeros(),
        y_mat.total_nonzeros()
    );

    // 1. Collatz-Wielandt iterations with BigUint: p=1, 2, 3, 4
    println!("\n--- Step 1: Exact Collatz-Wielandt Iterations from 1_vector ---");
    let cw_results = run_collatz_biguint(&x_mat, &y_mat, m, n, 4);
    for res in &cw_results {
        println!(
            "  CW step p={}: float={:.8}, ceil={:.6}",
            res.p, res.bound_f64, res.bound_ceil_6dec
        );
    }

    let p2_bound = cw_results[2].bound_ceil_6dec;
    println!("\nHe (2026) Table 2 (p=2) bound at (5,5): {p2_bound:.6} (Expected: 0.452130)");
    assert_eq!(p2_bound, 0.452130, "Must reproduce He (2026) 0.452130 at p=2");

    let p3_bound = cw_results[3].bound_ceil_6dec;
    println!("Improved bound with p=3: {p3_bound:.6} (raw: {:.8})", cw_results[3].bound_f64);
    println!("Improvement over published: {:.6}", p2_bound - p3_bound);

    // 2. Lanczos / Power iteration to find optimal Perron vector
    println!("\n--- Step 2: Lanczos/Arnoldi Perron Vector Polish ---");
    let t_lanczos = Instant::now();
    let (lambda_approx, perron_v) = find_perron_vector_f64(&x_mat, &y_mat, 150, 1e-12);
    let raw_perron_bound = (1.0 / (2.0 * 25.0)) * lambda_approx.ln();
    println!(
        "Converged Perron vector in {:?}: rho(XY) ~ {:.6}, bound ~ {:.8} (ceil: {:.6})",
        t_lanczos.elapsed(),
        lambda_approx,
        raw_perron_bound,
        (raw_perron_bound * 1e6).ceil() / 1e6
    );

    // 3. Convert to strictly positive integer vector and verify exactly
    println!("\n--- Step 3: Exact Integer Collatz-Wielandt Certificate ---");
    let u_vec = quantize_to_positive_integers(&perron_v, 1_000_000);

    // Compute (XY u) exactly
    let mut odd = vec![BigUint::zero(); y_mat.num_rows];
    y_mat.mul_vec_biguint(&u_vec, &mut odd);
    let mut xy_u = vec![BigUint::zero(); x_mat.num_rows];
    x_mat.mul_vec_biguint(&odd, &mut xy_u);

    let mut max_ratio_num = BigUint::zero();
    let mut max_ratio_den = BigUint::one();

    for r in 0..u_vec.len() {
        let num = &xy_u[r];
        let den = &u_vec[r];
        if num * &max_ratio_den > &max_ratio_num * den {
            max_ratio_num = num.clone();
            max_ratio_den = den.clone();
        }
    }

    let rat = BigRational::new(max_ratio_num.clone().into(), max_ratio_den.clone().into());
    let c_float = rat.to_f64().unwrap();
    let certified_bound_raw = (1.0 / 50.0) * c_float.ln();
    let certified_bound_ceil = (certified_bound_raw * 1e6).ceil() / 1e6;

    let published_bound = 0.452130;
    let improvement = published_bound - certified_bound_ceil;

    println!("Exact maximum ratio C = max_r (XY u)_r / u_r = {c_float:.8}");
    println!("Raw certified upper bound: {certified_bound_raw:.10}");
    println!("Ceiling to 6 decimals   : {certified_bound_ceil:.6}");
    println!("He (2026) published     : {published_bound:.6}");
    println!("Improvement             : {improvement:.6} (target: >= 0.000001)");

    assert!(
        certified_bound_ceil < published_bound,
        "Bound must strictly beat 0.452130"
    );
    assert!(
        improvement >= 1e-6,
        "Improvement must be >= 10^-6"
    );

    // 4. Exact integer cross-multiplication check (Positive control)
    println!("\n--- Step 4: Verification & Positive/Negative Controls ---");
    verify_integer_certificate(&x_mat, &y_mat, &u_vec, &max_ratio_num, &max_ratio_den)
        .expect("Exact integer certificate verification failed!");
    println!("Positive control: Verified (XY u)_r * C_den <= C_num * u_r for all 35070 coordinates!");

    // Negative control: perturbed smaller numerator must fail
    let smaller_num = &max_ratio_num - BigUint::one();
    let neg_res = verify_integer_certificate(&x_mat, &y_mat, &u_vec, &smaller_num, &max_ratio_den);
    assert!(neg_res.is_err(), "Negative control must reject smaller constant!");
    println!("Negative control: Verified smaller constant strictly rejected!");

    // Output certificate
    let cert = Dimer3DCertificate {
        dimension: 3,
        cross_section: [5, 5],
        displacements: vec![[0, 0], [1, 0], [0, 1]],
        sector: 12,
        num_orbits: u_vec.len(),
        spectral_radius_f64: c_float,
        he_2026_published_bound: published_bound,
        certified_upper_bound: certified_bound_ceil,
        improvement,
        p_iterations: 4,
        c_bound_num: max_ratio_num.to_string(),
        c_bound_den: max_ratio_den.to_string(),
        test_vector: u_vec.iter().map(|x| x.to_string()).collect(),
        verified_exact_integer: true,
    };

    let cert_path = std::env::var("CERT_PATH").unwrap_or_else(|_| "../dimer_3d_5_5_certificate.json".to_string());
    let cert_json = serde_json::to_string_pretty(&cert).unwrap();
    let mut f = File::create(&cert_path).unwrap();
    f.write_all(cert_json.as_bytes()).unwrap();
    println!("\nCertificate written to: {cert_path}");
    println!("============================================================");
    println!("CONFIRMED_SOLUTION AT (5,5) FULLY VERIFIED AND CERTIFIED!");
    println!("============================================================");
}
