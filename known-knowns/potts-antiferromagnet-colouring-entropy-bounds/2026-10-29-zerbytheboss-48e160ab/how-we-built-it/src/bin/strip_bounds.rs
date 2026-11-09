use std::time::Instant;
use potts_entropy_engine::partition::{get_proper_partitions, group_into_orbits};
use potts_entropy_engine::transfer::{build_compressed_matrix, power_iteration};

fn solve_pk(k: usize, q: usize) -> (usize, f64, f64) {
    let t0 = Instant::now();
    let edges: Vec<(usize, usize)> = (0..k - 1).map(|i| (i, i + 1)).collect();
    let aut = vec![
        (0..k).collect(),
        (0..k).rev().collect(),
    ];
    let mut parts = get_proper_partitions(&edges, k, q);
    let orbits = group_into_orbits(&mut parts, &aut, k);
    let dim = orbits.len();
    let mat = build_compressed_matrix(&orbits, q);
    let (lambda, _, _) = power_iteration(&mat, 1000, 1e-14);
    let dt = t0.elapsed().as_secs_f64();
    (dim, lambda, dt)
}

fn main() {
    println!("Computing strip bounds for q = 5:");
    let mut prev_eig = 0.0f64;
    for k in 2..=11 {
        let (dim, eig, dt) = solve_pk(k, 5);
        if prev_eig > 0.0 {
            let ratio = eig / prev_eig;
            println!("P_{:2}/P_{:2}: dim = {:5}, eig = {:22.12}, ratio = {:.16} (t={:.2}s)",
                k, k-1, dim, eig, ratio, dt
            );
        } else {
            println!("P_{:2}:       dim = {:5}, eig = {:22.12} (t={:.2}s)",
                k, dim, eig, dt
            );
        }
        prev_eig = eig;
    }
}
