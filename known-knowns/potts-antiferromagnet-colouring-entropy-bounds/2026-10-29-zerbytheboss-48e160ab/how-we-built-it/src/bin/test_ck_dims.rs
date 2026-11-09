use potts_entropy_engine::partition::{get_proper_partitions, group_into_orbits};

fn main() {
    println!("--- C_k for q = 4 ---");
    for k in (4..=18).step_by(2) {
        let edges: Vec<(usize, usize)> = (0..k).map(|i| (i, (i + 1) % k)).collect();
        let mut aut = Vec::new();
        for s in 0..k {
            aut.push((0..k).map(|i| (i + s) % k).collect());
            aut.push((0..k).map(|i| (k + s - (i % k)) % k).collect());
        }
        let t0 = std::time::Instant::now();
        let mut parts = get_proper_partitions(&edges, k, 4);
        let orbits = group_into_orbits(&mut parts, &aut, k);
        println!("C_{:2} (q=4): partitions = {:8}, orbits = {:6} (elapsed: {:.2}s)",
            k, parts.len(), orbits.len(), t0.elapsed().as_secs_f64()
        );
    }
}
