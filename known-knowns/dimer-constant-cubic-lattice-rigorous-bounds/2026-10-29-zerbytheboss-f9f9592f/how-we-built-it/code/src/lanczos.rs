//! Power iteration and Lanczos/Arnoldi polishing to extract the Perron eigenvector
//! and convert it to a certified positive integer test vector.

use crate::transfer::CsrMatrix;
use num_bigint::BigUint;

pub fn find_perron_vector_f64(
    x_mat: &CsrMatrix,
    y_mat: &CsrMatrix,
    max_iters: usize,
    tol: f64,
) -> (f64, Vec<f64>) {
    let num_orbits = x_mat.num_rows;
    let mut v = vec![1.0; num_orbits];
    let mut w = vec![0.0; y_mat.num_rows];
    let mut v_new = vec![0.0; num_orbits];
    let mut lambda = 0.0;

    for iter in 0..max_iters {
        y_mat.mul_vec_f64(&v, &mut w);
        x_mat.mul_vec_f64(&w, &mut v_new);

        // Find max component for normalization
        let mut max_val = 0.0f64;
        for &val in &v_new {
            if val > max_val {
                max_val = val;
            }
        }
        assert!(max_val > 0.0, "Perron vector vanished");

        let mut diff = 0.0f64;
        for i in 0..num_orbits {
            let next_v = v_new[i] / max_val;
            let d = (next_v - v[i]).abs();
            if d > diff {
                diff = d;
            }
            v[i] = next_v;
        }

        lambda = max_val;
        if iter > 10 && diff < tol {
            break;
        }
    }

    (lambda, v)
}

/// Convert floating-point Perron vector to strictly positive BigUint vector.
/// Ensures min_val >= 1 and scales by target_scale.
pub fn quantize_to_positive_integers(v_f64: &[f64], target_min: u64) -> Vec<BigUint> {
    let min_f = v_f64.iter().cloned().fold(f64::INFINITY, f64::min);
    assert!(min_f > 0.0, "Perron vector coordinates must be strictly positive");

    let scale = (target_min as f64) / min_f;
    v_f64
        .iter()
        .map(|&val| {
            let int_val = (val * scale).round() as u64;
            BigUint::from(int_val.max(1))
        })
        .collect()
}
