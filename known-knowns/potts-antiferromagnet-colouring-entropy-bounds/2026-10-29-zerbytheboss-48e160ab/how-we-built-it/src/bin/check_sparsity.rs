use potts_entropy_engine::partition::{get_proper_partitions, group_into_orbits};
use potts_entropy_engine::transfer::build_compressed_matrix;

fn main() {
    for k in [6, 8, 10] {
        let edges: Vec<(usize, usize)> = (0..k).map(|i| (i, (i + 1) % k)).collect();
        let mut aut = Vec::new();
        for s in 0..k {
            aut.push((0..k).map(|i| (i + s) % k).collect());
            aut.push((0..k).map(|i| (k + s - (i % k)) % k).collect());
        }
        let mut parts = get_proper_partitions(&edges, k, 5);
        let orbits = group_into_orbits(&mut parts, &aut, k);
        let dim = orbits.len();
        let mat = build_compressed_matrix(&orbits, 5);
        let nnz = mat.values.len();
        let density = (nnz as f64) / ((dim * dim) as f64);
        let avg_deg = (nnz as f64) / (dim as f64);
        println!("C_{:2} (q=5): dim = {:5}, nnz = {:8}, avg_degree = {:6.1}, density = {:.4}",
            k, dim, nnz, avg_deg, density
        );
    }
}
