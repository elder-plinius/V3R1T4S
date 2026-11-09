use std::time::Instant;
use serde::{Deserialize, Serialize};
use potts_entropy_engine::partition::{get_proper_partitions, group_into_orbits};
use potts_entropy_engine::transfer::MatrixFreeOperator;
use potts_entropy_engine::collatz::{power_iteration_matrix_free, certify_collatz_matrix_free};

#[derive(Serialize, Deserialize, Debug)]
pub struct CubicCollatzCertificate {
    pub target: String,
    pub model: String,
    pub width_x: usize,
    pub width_y: usize,
    pub q: usize,
    pub orbit_dimension: usize,
    pub power_iterations: usize,
    pub lambda_min: f64,
    pub lambda_max: f64,
    pub spectral_radius_estimate: f64,
    pub rigorous_upper_bound_per_site: f64,
    pub published_upper_bound: f64,
    pub bound_improvement: f64,
    pub meets_confirmed_solution_gate: bool,
    pub test_vector_sample: Vec<f64>,
    pub test_vector_min_entry: f64,
    pub test_vector_max_entry: f64,
    pub test_vector_len: usize,
}

fn build_torus_grid(nx: usize, ny: usize) -> (Vec<(usize, usize)>, Vec<Vec<usize>>) {
    let mut edges = Vec::new();
    for y in 0..ny {
        for x in 0..nx {
            let v = y * nx + x;
            // horizontal periodic edge
            edges.push((v, y * nx + (x + 1) % nx));
            // vertical periodic edge
            edges.push((v, ((y + 1) % ny) * nx + x));
        }
    }

    let mut aut = Vec::new();
    for sy in 0..ny {
        for flip_y in [false, true] {
            for sx in 0..nx {
                for flip_x in [false, true] {
                    let mut perm = Vec::new();
                    for v in 0..ny * nx {
                        let x = v % nx;
                        let y = v / nx;
                        let nx_new = if flip_x { (nx + sx - (x % nx)) % nx } else { (x + sx) % nx };
                        let ny_new = if flip_y { (ny + sy - (y % ny)) % ny } else { (y + sy) % ny };
                        perm.push(ny_new * nx + nx_new);
                    }
                    aut.push(perm);
                }
            }
        }
    }
    (edges, aut)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let nx: usize = if args.len() > 1 { args[1].parse().unwrap_or(6) } else { 6 };
    let ny: usize = if args.len() > 2 { args[2].parse().unwrap_or(4) } else { 4 };
    let q: usize = if args.len() > 3 { args[3].parse().unwrap_or(3) } else { 3 };

    let n = nx * ny;
    println!("==========================================================================");
    println!("RIGOROUS CUBIC LATTICE BOUND CERTIFICATION");
    println!("Cross-section: C_{} x C_{} ({} vertices) for q = {} Potts Antiferromagnet", nx, ny, n, q);
    println!("==========================================================================");

    let t0 = Instant::now();
    let (edges, aut) = build_torus_grid(nx, ny);

    println!("Step 1: Generating proper set partitions with <= {} blocks on C_{} x C_{}...", q, nx, ny);
    let mut parts = get_proper_partitions(&edges, n, q);
    println!("Total proper partitions: {} (elapsed: {:.2}s)", parts.len(), t0.elapsed().as_secs_f64());

    println!("Step 2: Grouping into orbits under D_{} x D_{} symmetry...", nx, ny);
    let orbits = group_into_orbits(&mut parts, &aut, n);
    let dim = orbits.len();
    println!("Compressed orbit dimension r = {} (elapsed: {:.2}s)", dim, t0.elapsed().as_secs_f64());

    println!("Step 3: Initializing MatrixFreeOperator...");
    let op = MatrixFreeOperator::new(parts, orbits, q, n);
    println!("Operator initialized (elapsed: {:.2}s)", t0.elapsed().as_secs_f64());

    println!("Step 4: Running power iteration...");
    let (lambda_est, v, iters) = power_iteration_matrix_free(&op, 40, 1e-12);
    println!("Power iteration finished in {} iters: lambda = {:.12} (elapsed: {:.2}s)",
        iters, lambda_est, t0.elapsed().as_secs_f64()
    );

    println!("Step 5: Rigorous Collatz-Wielandt certification...");
    let cert_res = certify_collatz_matrix_free(&op, &v, n as f64);

    let pub_ub = if q == 3 {
        1.4470681274660 // LM (2008) from C_6 x C_4
    } else if q == 4 {
        2.0652128520667 // LM (2008) from C_4 x C_4
    } else {
        0.0
    };
    let improvement = pub_ub - cert_res.upper_bound_per_site;
    let gate_pass = improvement >= 1e-6;

    println!("\n---------------- CERTIFICATE RESULTS ----------------");
    println!("Model:                       C_{} x C_{} (q={})", nx, ny, q);
    println!("Vertices per cross-section:  {}", n);
    println!("Orbit Dimension:             {}", dim);
    println!("Collatz-Wielandt lambda_min: {:.14}", cert_res.lambda_min);
    println!("Collatz-Wielandt lambda_max: {:.14}", cert_res.lambda_max);
    println!("Spectral radius:             {:.14}", cert_res.spectral_radius_estimate);
    println!("Rigorous upper bound W_c({}): {:.15}", q, cert_res.upper_bound_per_site);
    println!("Published LM (2008) bound:   {:.15}", pub_ub);
    println!("Strict Improvement:          {:+.10e}", improvement);
    println!("Meets >= 1e-6 Gate:          {}", if gate_pass { "PASS (CONFIRMED_SOLUTION)" } else { "NOT YET" });
    println!("-----------------------------------------------------");

    let min_v = v.iter().cloned().fold(f64::INFINITY, f64::min);
    let max_v = v.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let cert = CubicCollatzCertificate {
        target: "potts-antiferromagnet-colouring-entropy-bounds".into(),
        model: format!("C_{} x C_{} (q={})", nx, ny, q),
        width_x: nx,
        width_y: ny,
        q,
        orbit_dimension: dim,
        power_iterations: iters,
        lambda_min: cert_res.lambda_min,
        lambda_max: cert_res.lambda_max,
        spectral_radius_estimate: cert_res.spectral_radius_estimate,
        rigorous_upper_bound_per_site: cert_res.upper_bound_per_site,
        published_upper_bound: pub_ub,
        bound_improvement: improvement,
        meets_confirmed_solution_gate: gate_pass,
        test_vector_sample: v.iter().take(20).cloned().collect(),
        test_vector_min_entry: min_v,
        test_vector_max_entry: max_v,
        test_vector_len: v.len(),
    };

    let filename = format!("collatz_c{}_c{}_q{}.json", nx, ny, q);
    let json_str = serde_json::to_string_pretty(&cert).unwrap();
    std::fs::write(&filename, &json_str).unwrap();
    println!("Saved certificate to {}", filename);

    let vec_filename = format!("test_vector_c{}_c{}_q{}.bin", nx, ny, q);
    let bytes: Vec<u8> = v.iter().flat_map(|&f| f.to_le_bytes()).collect();
    std::fs::write(&vec_filename, &bytes).unwrap();
    println!("Saved binary test vector ({} bytes) to {}", bytes.len(), vec_filename);
}
