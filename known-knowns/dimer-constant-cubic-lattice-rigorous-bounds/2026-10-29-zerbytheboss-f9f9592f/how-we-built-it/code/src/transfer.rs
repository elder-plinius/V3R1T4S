//! Construction of compressed transfer blocks X_{m,n}^{(i)} and Y_{m,n}^{(i)}
//! via injective displacement matchings, stored as Compressed Sparse Row (CSR) matrices.

use crate::symmetry::{LatticeGroup, SectorOrbits};
use num_bigint::BigUint;
use num_traits::Zero;
use rayon::prelude::*;
use std::collections::HashMap;

/// Compressed Sparse Row (CSR) matrix with integer entries.
#[derive(Clone, Debug)]
pub struct CsrMatrix {
    pub num_rows: usize,
    pub num_cols: usize,
    pub row_offsets: Vec<usize>,
    pub col_indices: Vec<u32>,
    pub values: Vec<u32>,
}

impl CsrMatrix {
    pub fn mul_vec_f64(&self, x: &[f64], out: &mut [f64]) {
        assert_eq!(x.len(), self.num_cols);
        assert_eq!(out.len(), self.num_rows);
        out.par_iter_mut().enumerate().for_each(|(r, out_val)| {
            let start = self.row_offsets[r];
            let end = self.row_offsets[r + 1];
            let mut sum = 0.0;
            for idx in start..end {
                let c = self.col_indices[idx] as usize;
                let v = self.values[idx] as f64;
                sum += v * x[c];
            }
            *out_val = sum;
        });
    }

    pub fn mul_vec_biguint(&self, x: &[BigUint], out: &mut [BigUint]) {
        assert_eq!(x.len(), self.num_cols);
        assert_eq!(out.len(), self.num_rows);
        out.par_iter_mut().enumerate().for_each(|(r, out_val)| {
            let start = self.row_offsets[r];
            let end = self.row_offsets[r + 1];
            let mut sum = BigUint::zero();
            for idx in start..end {
                let c = self.col_indices[idx] as usize;
                let v = self.values[idx];
                sum += BigUint::from(v) * &x[c];
            }
            *out_val = sum;
        });
    }

    pub fn total_nonzeros(&self) -> usize {
        self.col_indices.len()
    }
}

/// Helper function to enumerate all injective displacement maps alpha: verts -> D.
/// For each valid alpha, computes the target complement mask: ((1 << N) - 1) ^ image_mask.
pub fn enumerate_matchings(
    verts: &[usize],
    d_maps: &[Vec<usize>],
    full_mask: u32,
    results: &mut Vec<u32>,
) {
    fn backtrack(
        idx: usize,
        cur_img: u32,
        verts: &[usize],
        d_maps: &[Vec<usize>],
        full_mask: u32,
        results: &mut Vec<u32>,
    ) {
        if idx == verts.len() {
            results.push(full_mask ^ cur_img);
            return;
        }
        let v = verts[idx];
        for d_map in d_maps {
            let target_v = d_map[v];
            if (cur_img & (1 << target_v)) == 0 {
                backtrack(idx + 1, cur_img | (1 << target_v), verts, d_maps, full_mask, results);
            }
        }
    }
    backtrack(0, 0, verts, d_maps, full_mask, results);
}

/// Build the X block for sector i: maps from S_i^+ to S_i^-.
/// Row r corresponds to orbit r in S_i^-. Its representative has size i.
/// Target complement masks have size N - i, belonging to orbits in S_i^+.
pub fn build_block_x(
    lattice: &LatticeGroup,
    orbits_minus: &SectorOrbits,
    orbits_plus: &SectorOrbits,
) -> CsrMatrix {
    let num_rows = orbits_minus.num_orbits();
    let num_cols = orbits_plus.num_orbits();
    let n = lattice.num_vertices;
    let full_mask = if n == 32 { u32::MAX } else { (1u32 << n) - 1 };

    // Parallel extraction of row transitions
    let rows: Vec<Vec<(u32, u32)>> = (0..num_rows)
        .into_par_iter()
        .map(|r| {
            let rep = orbits_minus.canonical_reps[r];
            let mut verts = Vec::with_capacity(orbits_minus.size_k);
            let mut m = rep;
            while m > 0 {
                let v = m.trailing_zeros() as usize;
                m &= m - 1;
                verts.push(v);
            }
            let mut matchings = Vec::new();
            enumerate_matchings(&verts, &lattice.d_maps, full_mask, &mut matchings);

            // Tally counts per target orbit in orbits_plus
            let mut counts: HashMap<u32, u32> = HashMap::new();
            for tgt_mask in matchings {
                let target_oid = orbits_plus.get_orbit(tgt_mask) as u32;
                *counts.entry(target_oid).or_insert(0) += 1;
            }
            let mut row_entries: Vec<(u32, u32)> = counts.into_iter().collect();
            row_entries.sort_unstable_by_key(|&(col, _)| col);
            row_entries
        })
        .collect();

    // Assemble CSR
    let mut row_offsets = Vec::with_capacity(num_rows + 1);
    let mut col_indices = Vec::new();
    let mut values = Vec::new();
    row_offsets.push(0);

    for row in rows {
        for (col, val) in row {
            col_indices.push(col);
            values.push(val);
        }
        row_offsets.push(col_indices.len());
    }

    CsrMatrix {
        num_rows,
        num_cols,
        row_offsets,
        col_indices,
        values,
    }
}

/// Build the Y block for sector i: maps from S_i^- to S_i^+.
/// Row r corresponds to orbit r in S_i^+. Its representative has size N - i.
/// Target complement masks have size i, belonging to orbits in S_i^-.
pub fn build_block_y(
    lattice: &LatticeGroup,
    orbits_plus: &SectorOrbits,
    orbits_minus: &SectorOrbits,
) -> CsrMatrix {
    let num_rows = orbits_plus.num_orbits();
    let num_cols = orbits_minus.num_orbits();
    let n = lattice.num_vertices;
    let full_mask = if n == 32 { u32::MAX } else { (1u32 << n) - 1 };

    let rows: Vec<Vec<(u32, u32)>> = (0..num_rows)
        .into_par_iter()
        .map(|r| {
            let rep = orbits_plus.canonical_reps[r];
            let mut verts = Vec::with_capacity(orbits_plus.size_k);
            let mut m = rep;
            while m > 0 {
                let v = m.trailing_zeros() as usize;
                m &= m - 1;
                verts.push(v);
            }
            let mut matchings = Vec::new();
            enumerate_matchings(&verts, &lattice.d_maps, full_mask, &mut matchings);

            let mut counts: HashMap<u32, u32> = HashMap::new();
            for tgt_mask in matchings {
                let target_oid = orbits_minus.get_orbit(tgt_mask) as u32;
                *counts.entry(target_oid).or_insert(0) += 1;
            }
            let mut row_entries: Vec<(u32, u32)> = counts.into_iter().collect();
            row_entries.sort_unstable_by_key(|&(col, _)| col);
            row_entries
        })
        .collect();

    let mut row_offsets = Vec::with_capacity(num_rows + 1);
    let mut col_indices = Vec::new();
    let mut values = Vec::new();
    row_offsets.push(0);

    for row in rows {
        for (col, val) in row {
            col_indices.push(col);
            values.push(val);
        }
        row_offsets.push(col_indices.len());
    }

    CsrMatrix {
        num_rows,
        num_cols,
        row_offsets,
        col_indices,
        values,
    }
}
