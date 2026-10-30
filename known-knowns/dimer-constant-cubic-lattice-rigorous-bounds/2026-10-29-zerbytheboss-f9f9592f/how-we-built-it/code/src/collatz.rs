//! Collatz-Wielandt bound sequence evaluation and exact integer verification.

use crate::transfer::CsrMatrix;
use num_bigint::BigUint;
use num_rational::BigRational;
use num_traits::{One, ToPrimitive, Zero};

#[derive(Clone, Debug)]
pub struct CollatzStepResult {
    pub p: usize,
    pub max_ratio_num: BigUint,
    pub max_ratio_den: BigUint,
    pub bound_f64: f64,
    pub bound_ceil_6dec: f64,
}

/// Compute iterated Collatz-Wielandt bounds using exact BigUint vector multiplication.
pub fn run_collatz_biguint(
    x_mat: &CsrMatrix,
    y_mat: &CsrMatrix,
    m: usize,
    n: usize,
    p_iterations: usize,
) -> Vec<CollatzStepResult> {
    let num_orbits = x_mat.num_rows;
    let mut even = vec![BigUint::one(); num_orbits];
    let mut odd = vec![BigUint::zero(); y_mat.num_rows];
    let mut results = Vec::new();

    for p in 0..p_iterations {
        // odd = Y * even
        y_mat.mul_vec_biguint(&even, &mut odd);

        // even_next = X * odd
        let mut even_next = vec![BigUint::zero(); num_orbits];
        x_mat.mul_vec_biguint(&odd, &mut even_next);

        // Find max ratio even_next[r] / even[r] using cross multiplication
        let mut max_num = BigUint::zero();
        let mut max_den = BigUint::one();

        for r in 0..num_orbits {
            let num = &even_next[r];
            let den = &even[r];
            // Compare num / den > max_num / max_den <=> num * max_den > max_num * den
            if num * &max_den > &max_num * den {
                max_num = num.clone();
                max_den = den.clone();
            }
        }

        even = even_next;

        // Compute floating-point value and outward ceiling to 6 decimals
        let rat = BigRational::new(max_num.clone().into(), max_den.clone().into());
        let float_val = rat.to_f64().unwrap_or(f64::NAN);
        let log_val = float_val.ln();
        let bound = (1.0 / (2.0 * m as f64 * n as f64)) * log_val;
        let bound_ceil_6dec = (bound * 1e6).ceil() / 1e6;

        results.push(CollatzStepResult {
            p: p + 1,
            max_ratio_num: max_num,
            max_ratio_den: max_den,
            bound_f64: bound,
            bound_ceil_6dec,
        });
    }

    results
}

/// Verify a test vector v in exact integer arithmetic:
/// checks that (X * (Y * v))_r <= C * v_r for all r.
pub fn verify_integer_certificate(
    x_mat: &CsrMatrix,
    y_mat: &CsrMatrix,
    v: &[BigUint],
    c_num: &BigUint,
    c_den: &BigUint,
) -> Result<(), (usize, BigUint, BigUint)> {
    assert_eq!(v.len(), x_mat.num_rows);
    let mut odd = vec![BigUint::zero(); y_mat.num_rows];
    y_mat.mul_vec_biguint(v, &mut odd);

    let mut xy_v = vec![BigUint::zero(); x_mat.num_rows];
    x_mat.mul_vec_biguint(&odd, &mut xy_v);

    for r in 0..v.len() {
        assert!(!v[r].is_zero(), "Certificate vector entry {} is zero", r);
        // Check (XY v)_r / v_r <= c_num / c_den <=> (XY v)_r * c_den <= c_num * v_r
        let lhs = &xy_v[r] * c_den;
        let rhs = c_num * &v[r];
        if lhs > rhs {
            return Err((r, lhs, rhs));
        }
    }

    Ok(())
}
