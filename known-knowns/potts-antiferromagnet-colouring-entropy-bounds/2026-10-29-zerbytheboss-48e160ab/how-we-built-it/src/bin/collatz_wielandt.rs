use std::time::Instant;
use serde::{Deserialize, Serialize};
use potts_entropy_engine::partition::{get_proper_partitions, group_into_orbits};
use potts_entropy_engine::transfer::MatrixFreeOperator;
use potts_entropy_engine::collatz::{power_iteration_matrix_free, certify_collatz_matrix_free};

#[derive(Serialize, Deserialize, Debug)]
pub struct CollatzCertificate {
    pub target: String,
    pub model: String,
    pub width: usize,
    pub q: usize,
    pub orbit_dimension: usize,
    pub power_iterations: usize,
    pub lambda_min: f64,
    pub lambda_max: f64,
    pub spectral_radius_estimate: f64,
    pub rigorous_upper_bound: f64,
    pub rigorous_lower_bound: f64,
    pub published_upper_bound: f64,
    pub bound_improvement: f64,
    pub meets_confirmed_solution_gate: bool,
    pub test_vector_sample: Vec<f64>,
    pub test_vector_min_entry: f64,
    pub test_vector_max_entry: f64,
    pub test_vector_len: usize,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let k: usize = if args.len() > 1 {
        args[1].parse().unwrap_or(14)
    } else {
        14
    };
    let q: usize = if args.len() > 2 {
        args[2].parse().unwrap_or(4)
    } else {
        4
    };

    println!("==========================================================================");
    println!("MATRIX-FREE COLLATZ-WIELANDDT RIGOROUS BOUND CERTIFICATION");
    println!("Model: C_{} cylinder for q = {} Potts Antiferromagnet", k, q);
    println!("==========================================================================");

    let t0 = Instant::now();
    let edges: Vec<(usize, usize)> = (0..k).map(|i| (i, (i + 1) % k)).collect();
    let mut aut = Vec::new();
    for s in 0..k {
        aut.push((0..k).map(|i| (i + s) % k).collect());
        aut.push((0..k).map(|i| (k + s - (i % k)) % k).collect());
    }

    println!("Step 1: Generating proper set partitions with <= {} blocks on C_{}...", q, k);
    let mut parts = get_proper_partitions(&edges, k, q);
    println!("Total proper partitions: {} (elapsed: {:.2}s)", parts.len(), t0.elapsed().as_secs_f64());

    println!("Step 2: Grouping into orbits under D_{} symmetry...", k);
    let orbits = group_into_orbits(&mut parts, &aut, k);
    let dim = orbits.len();
    println!("Compressed orbit dimension r = {} (elapsed: {:.2}s)", dim, t0.elapsed().as_secs_f64());

    println!("Step 3: Initializing zero-allocation MatrixFreeOperator (dim {}x{})...", dim, dim);
    let op = MatrixFreeOperator::new(parts, orbits, q, k);
    println!("Operator initialized (elapsed: {:.2}s)", t0.elapsed().as_secs_f64());

    println!("Step 4: Running matrix-free power iteration to find positive eigenvector...");
    let (lambda_est, v, iters) = power_iteration_matrix_free(&op, 30, 1e-10);
    println!("Power iteration finished in {} iterations: spectral radius approx = {:.12} (elapsed: {:.2}s)",
        iters, lambda_est, t0.elapsed().as_secs_f64()
    );

    println!("Step 5: Rigorous Collatz-Wielandt certification...");
    let cert_res = certify_collatz_matrix_free(&op, &v, k as f64);

    let pub_ub = if q == 4 {
        2.33606820555777 // LM (2008) from C_16
    } else if q == 5 {
        3.250407145038276 // LM (2008) from C_12
    } else {
        0.0
    };

    let improvement = pub_ub - cert_res.upper_bound_per_site;
    let gate_pass = improvement >= 1e-9;

    println!("\n---------------- CERTIFICATE RESULTS ----------------");
    println!("Model:                       C_{} (q={})", k, q);
    println!("Orbit Dimension:             {}", dim);
    println!("Collatz-Wielandt lambda_min: {:.14}", cert_res.lambda_min);
    println!("Collatz-Wielandt lambda_max: {:.14}", cert_res.lambda_max);
    println!("Spectral radius:             {:.14}", cert_res.spectral_radius_estimate);
    println!("Upper bound W_sq({}) <=       {:.15}", q, cert_res.upper_bound_per_site);
    println!("Published LM (2008) bound:   {:.15}", pub_ub);
    println!("Strict Improvement:          {:+.10e}", improvement);
    println!("Meets >= 1e-9 Gate:          {}", if gate_pass { "PASS (CONFIRMED_SOLUTION)" } else { "NOT YET" });
    println!("-----------------------------------------------------");

    let min_v = v.iter().cloned().fold(f64::INFINITY, f64::min);
    let max_v = v.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let cert = CollatzCertificate {
        target: "potts-antiferromagnet-colouring-entropy-bounds".into(),
        model: format!("C_{} (q={})", k, q),
        width: k,
        q,
        orbit_dimension: dim,
        power_iterations: iters,
        lambda_min: cert_res.lambda_min,
        lambda_max: cert_res.lambda_max,
        spectral_radius_estimate: cert_res.spectral_radius_estimate,
        rigorous_upper_bound: cert_res.upper_bound_per_site,
        rigorous_lower_bound: cert_res.lower_bound_per_site,
        published_upper_bound: pub_ub,
        bound_improvement: improvement,
        meets_confirmed_solution_gate: gate_pass,
        test_vector_sample: v.iter().take(20).cloned().collect(),
        test_vector_min_entry: min_v,
        test_vector_max_entry: max_v,
        test_vector_len: v.len(),
    };

    let filename = format!("collatz_c{}_q{}.json", k, q);
    let json_str = serde_json::to_string_pretty(&cert).unwrap();
    std::fs::write(&filename, &json_str).unwrap();
    println!("Saved certificate to {}", filename);

    let vec_filename = format!("test_vector_c{}_q{}.bin", k, q);
    let bytes: Vec<u8> = v.iter().flat_map(|&f| f.to_le_bytes()).collect();
    std::fs::write(&vec_filename, &bytes).unwrap();
    println!("Saved binary test vector ({} bytes) to {}", bytes.len(), vec_filename);
}
