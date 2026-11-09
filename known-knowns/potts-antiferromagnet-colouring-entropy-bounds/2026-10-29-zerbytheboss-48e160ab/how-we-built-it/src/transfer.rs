use rayon::prelude::*;
use crate::partition::Partition;

// Precomputed lookup table for q = 4 and q = 5
const OFFSETS_Q5: [usize; 6] = [0, 0, 32, 560, 6544, 58904];

pub struct TransitionTable {
    table: Vec<u16>,    // flattened [m][l][mask] for m, l <= 4 (used for q <= 4)
    q5_table: Vec<u8>,  // flattened combinadic multiset table (435,896 bytes for q = 5)
    binom: [[usize; 7]; 42],
    pub q: usize,
}

impl TransitionTable {
    pub fn new(q: usize) -> Self {
        let mut binom = [[0usize; 7]; 42];
        for n in 0..42 {
            binom[n][0] = 1;
            for k in 1..=6.min(n) {
                binom[n][k] = binom[n - 1][k - 1] + binom[n - 1][k];
            }
        }

        let mut table = Vec::new();
        let mut q5_table = Vec::new();

        let size = 5 * 5 * 65536;
        table = vec![0u16; size];
        for m in 1..=4 {
            for l in 1..=4 {
                let max_mask = 1usize << (m * l);
                for mask in 0..max_mask {
                    let val = count_tau_slow(m, l, mask as u32, q);
                    let idx = (m * 5 + l) * 65536 + mask;
                    table[idx] = val as u16;
                }
            }
        }

        if q == 5 {
            q5_table = vec![0u8; 435896];
            // l = 1
            for a in 0..32 {
                let idx = OFFSETS_Q5[1] + binom[a][1];
                q5_table[idx] = count_tau_dfs(0, 0, &[a as u8], 1, 5) as u8;
            }
            // l = 2
            for a in 0..32 {
                for b in a..32 {
                    let idx = OFFSETS_Q5[2] + binom[a][1] + binom[b + 1][2];
                    q5_table[idx] = count_tau_dfs(0, 0, &[a as u8, b as u8], 2, 5) as u8;
                }
            }
            // l = 3
            for a in 0..32 {
                for b in a..32 {
                    for c in b..32 {
                        let idx = OFFSETS_Q5[3] + binom[a][1] + binom[b + 1][2] + binom[c + 2][3];
                        q5_table[idx] = count_tau_dfs(0, 0, &[a as u8, b as u8, c as u8], 3, 5) as u8;
                    }
                }
            }
            // l = 4
            for a in 0..32 {
                for b in a..32 {
                    for c in b..32 {
                        for d in c..32 {
                            let idx = OFFSETS_Q5[4] + binom[a][1] + binom[b + 1][2] + binom[c + 2][3] + binom[d + 3][4];
                            q5_table[idx] = count_tau_dfs(0, 0, &[a as u8, b as u8, c as u8, d as u8], 4, 5) as u8;
                        }
                    }
                }
            }
            // l = 5
            for a in 0..32 {
                for b in a..32 {
                    for c in b..32 {
                        for d in c..32 {
                            for e in d..32 {
                                let idx = OFFSETS_Q5[5] + binom[a][1] + binom[b + 1][2] + binom[c + 2][3] + binom[d + 3][4] + binom[e + 4][5];
                                q5_table[idx] = count_tau_dfs(0, 0, &[a as u8, b as u8, c as u8, d as u8, e as u8], 5, 5) as u8;
                            }
                        }
                    }
                }
            }
        }

        TransitionTable { table, q5_table, binom, q }
    }

    #[inline(always)]
    pub fn lookup(&self, m: usize, l: usize, mask: u32) -> u32 {
        if m <= 4 && l <= 4 {
            let idx = (m * 5 + l) * 65536 + (mask as usize);
            self.table[idx] as u32
        } else if self.q == 5 {
            let mut forbidden = [0u8; 5];
            for b in 0..l {
                let mut forb = 0u8;
                for a in 0..m {
                    if (mask & (1 << (a * l + b))) != 0 {
                        forb |= 1 << a;
                    }
                }
                forbidden[b] = forb;
            }
            self.lookup_q5(l, forbidden)
        } else {
            count_tau_slow(m, l, mask, self.q)
        }
    }

    #[inline(always)]
    pub fn lookup_q5(&self, l: usize, mut forbidden: [u8; 5]) -> u32 {
        forbidden[0..l].sort_unstable();
        let mut idx = OFFSETS_Q5[l];
        for k in 0..l {
            idx += self.binom[forbidden[k] as usize + k][k + 1];
        }
        self.q5_table[idx] as u32
    }
}

pub fn count_tau_dfs(b: usize, used: u8, forbidden: &[u8], l: usize, q: usize) -> u32 {
    let mut count = 0u32;
    fn dfs(b: usize, used: u8, forbidden: &[u8], l: usize, q: usize, count: &mut u32) {
        if b == l {
            *count += 1;
            return;
        }
        let forb = forbidden[b];
        for col in 0..q {
            let col_bit = 1 << col;
            if (used & col_bit) == 0 && (forb & col_bit) == 0 {
                dfs(b + 1, used | col_bit, forbidden, l, q, count);
            }
        }
    }
    dfs(b, used, forbidden, l, q, &mut count);
    count
}

pub fn count_tau_slow(m: usize, l: usize, mask: u32, q: usize) -> u32 {
    let mut forbidden = [0u8; 8];
    for b in 0..l {
        let mut forb = 0u8;
        for a in 0..m {
            if (mask & (1 << (a * l + b))) != 0 {
                forb |= 1 << a;
            }
        }
        forbidden[b] = forb;
    }

    let mut count = 0u32;
    fn dfs(b: usize, used: u8, l: usize, q: usize, forbidden: &[u8; 8], count: &mut u32) {
        if b == l {
            *count += 1;
            return;
        }
        let forb = forbidden[b];
        for col in 0..q {
            let col_bit = 1 << col;
            if (used & col_bit) == 0 && (forb & col_bit) == 0 {
                dfs(b + 1, used | col_bit, l, q, forbidden, count);
            }
        }
    }

    dfs(0, 0, l, q, &forbidden, &mut count);
    count
}

pub struct MatrixFreeOperator {
    pub partitions: Vec<Partition>,
    pub orbit_reps: Vec<Partition>,
    pub lut: TransitionTable,
    pub n: usize,
    pub num_orbits: usize,
}

impl MatrixFreeOperator {
    pub fn new(partitions: Vec<Partition>, orbits: Vec<Vec<Partition>>, q: usize, n: usize) -> Self {
        let num_orbits = orbits.len();
        let mut orbit_reps = Vec::with_capacity(num_orbits);
        for orb in &orbits {
            orbit_reps.push(orb[0].clone());
        }

        let lut = TransitionTable::new(q);
        MatrixFreeOperator {
            partitions,
            orbit_reps,
            lut,
            n,
            num_orbits,
        }
    }

    pub fn mult_vec(&self, v: &[f64], w: &mut [f64]) {
        let n = self.n;
        let partitions = &self.partitions;
        let lut = &self.lut;
        let q = self.lut.q;

        if q <= 4 {
            w.par_iter_mut().enumerate().for_each(|(i, w_i)| {
                let rep = &self.orbit_reps[i];
                let m = rep.num_blocks;
                let rep_blocks = &rep.blocks;

                let mut sum = 0.0f64;
                for q_part in partitions {
                    let l = q_part.num_blocks;
                    let q_blocks = &q_part.blocks;

                    let mut mask = 0u32;
                    for v_idx in 0..n {
                        let a = rep_blocks[v_idx] as usize;
                        let b = q_blocks[v_idx] as usize;
                        mask |= 1 << (a * l + b);
                    }

                    let count = lut.lookup(m, l, mask);
                    if count > 0 {
                        sum += (count as f64) * v[q_part.orbit_id];
                    }
                }
                *w_i = sum;
            });
        } else {
            // High-throughput q=5 path using 436 KB combinadic multiset lookup
            w.par_iter_mut().enumerate().for_each(|(i, w_i)| {
                let rep = &self.orbit_reps[i];
                let rep_blocks = &rep.blocks;

                let mut sum = 0.0f64;
                for q_part in partitions {
                    let l = q_part.num_blocks;
                    let q_blocks = &q_part.blocks;

                    let mut forbidden = [0u8; 5];
                    for v_idx in 0..n {
                        let a = rep_blocks[v_idx];
                        let b = q_blocks[v_idx] as usize;
                        forbidden[b] |= 1 << a;
                    }

                    let count = lut.lookup_q5(l, forbidden);
                    if count > 0 {
                        sum += (count as f64) * v[q_part.orbit_id];
                    }
                }
                *w_i = sum;
            });
        }
    }
}


#[derive(Clone, Debug)]
pub struct SparseMatrix {
    pub rows: usize,
    pub cols: usize,
    pub row_ptr: Vec<usize>,
    pub col_indices: Vec<usize>,
    pub values: Vec<f64>,
}

impl SparseMatrix {
    pub fn mult_vec(&self, x: &[f64], y: &mut [f64]) {
        y.par_iter_mut().enumerate().for_each(|(i, y_i)| {
            let start = self.row_ptr[i];
            let end = self.row_ptr[i + 1];
            let mut sum = 0.0;
            for idx in start..end {
                let j = self.col_indices[idx];
                let val = self.values[idx];
                sum += val * x[j];
            }
            *y_i = sum;
        });
    }
}

pub fn power_iteration(
    mat: &SparseMatrix,
    max_iter: usize,
    tol: f64,
) -> (f64, Vec<f64>, usize) {
    let r = mat.rows;
    let mut v = vec![1.0; r];
    let mut w = vec![0.0; r];
    let mut lambda = 1.0;

    for it in 0..max_iter {
        mat.mult_vec(&v, &mut w);
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

        if diff < tol && it >= 15 {
            return (lambda, v, it + 1);
        }
    }

    (lambda, v, max_iter)
}

pub fn build_compressed_matrix(
    orbits: &[Vec<Partition>],
    q: usize,
) -> SparseMatrix {
    let r = orbits.len();
    let lut = TransitionTable::new(q);
    let n = orbits[0][0].blocks.len();

    let rows_data: Vec<Vec<(usize, f64)>> = (0..r)
        .into_par_iter()
        .map(|i| {
            let rep = &orbits[i][0];
            let m = rep.num_blocks;
            let rep_blocks = &rep.blocks;
            let mut row = Vec::with_capacity(r);

            for j in 0..r {
                let mut total = 0u32;
                for q_part in &orbits[j] {
                    let l = q_part.num_blocks;
                    let q_blocks = &q_part.blocks;

                    let mut mask = 0u32;
                    for v in 0..n {
                        let a = rep_blocks[v] as usize;
                        let b = q_blocks[v] as usize;
                        mask |= 1 << (a * l + b);
                    }
                    total += lut.lookup(m, l, mask);
                }
                if total > 0 {
                    row.push((j, total as f64));
                }
            }
            row
        })
        .collect();

    let mut row_ptr = Vec::with_capacity(r + 1);
    let mut col_indices = Vec::new();
    let mut values = Vec::new();

    row_ptr.push(0);
    for row in rows_data {
        for (col, val) in row {
            col_indices.push(col);
            values.push(val);
        }
        row_ptr.push(col_indices.len());
    }

    SparseMatrix {
        rows: r,
        cols: r,
        row_ptr,
        col_indices,
        values,
    }
}
