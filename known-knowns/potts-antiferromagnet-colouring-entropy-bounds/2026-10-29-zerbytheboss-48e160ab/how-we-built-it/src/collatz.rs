use crate::transfer::MatrixFreeOperator;

#[derive(Clone, Debug)]
pub struct CollatzResult {
    pub lambda_min: f64,
    pub lambda_max: f64,
    pub spectral_radius_estimate: f64,
    pub upper_bound_per_site: f64,
    pub lower_bound_per_site: f64,
    pub iterations: usize,
    pub test_vector: Vec<f64>,
}

pub fn power_iteration_matrix_free(
    op: &MatrixFreeOperator,
    max_iter: usize,
    tol: f64,
) -> (f64, Vec<f64>, usize) {
    let r = op.num_orbits;
    let mut v = vec![1.0; r];
    let mut w = vec![0.0; r];
    let mut lambda = 1.0;

    for it in 0..max_iter {
        let t_it = std::time::Instant::now();
        op.mult_vec(&v, &mut w);

        let mut max_val = 0.0f64;
        for &val in &w {
            if val.abs() > max_val {
                max_val = val.abs();
            }
        }
        if max_val == 0.0 {
            break;
        }

        lambda = max_val;
        let mut diff = 0.0f64;
        for i in 0..r {
            let next_v = w[i] / lambda;
            let d = (next_v - v[i]).abs();
            if d > diff {
                diff = d;
            }
            v[i] = next_v;
        }

        println!("  iter {:3}: lambda = {:18.10}, diff = {:9.2e} (t={:.2}s)", it + 1, lambda, diff, t_it.elapsed().as_secs_f64());

        if diff < tol && it >= 8 {
            return (lambda, v, it + 1);
        }
    }

    (lambda, v, max_iter)
}

pub fn certify_collatz_matrix_free(
    op: &MatrixFreeOperator,
    v: &[f64],
    per_site_root: f64,
) -> CollatzResult {
    let r = op.num_orbits;
    let mut w = vec![0.0; r];
    op.mult_vec(v, &mut w);

    let mut min_ratio = f64::INFINITY;
    let mut max_ratio = f64::NEG_INFINITY;

    for i in 0..r {
        assert!(v[i] > 0.0, "Test vector must be strictly positive!");
        let ratio = w[i] / v[i];
        if ratio < min_ratio {
            min_ratio = ratio;
        }
        if ratio > max_ratio {
            max_ratio = ratio;
        }
    }

    let upper_bound = max_ratio.powf(1.0 / per_site_root);
    let lower_bound = min_ratio.powf(1.0 / per_site_root);
    let est = (min_ratio + max_ratio) / 2.0;

    CollatzResult {
        lambda_min: min_ratio,
        lambda_max: max_ratio,
        spectral_radius_estimate: est,
        upper_bound_per_site: upper_bound,
        lower_bound_per_site: lower_bound,
        iterations: 0,
        test_vector: v.to_vec(),
    }
}
