use rayon::prelude::*;
use std::fs::File;
use std::io::Write;
use std::time::Instant;

#[derive(Clone)]
pub struct TorusBase {
    pub lx: usize,
    pub ly: usize,
    pub num_sites: usize,
    pub adj: Vec<Vec<(usize, i32, i32)>>,
}

impl TorusBase {
    pub fn new_tiling41(lx: usize, ly: usize) -> Self {
        let base_edges = vec![
            (0, 1, 0, 0),
            (0, 4, 0, 0),
            (0, 5, 0, -1),
            (1, 2, 0, 0),
            (1, 4, 0, 0),
            (1, 7, 0, 0),
            (2, 3, -1, 0),
            (2, 7, 0, 0),
            (3, 4, 0, 0),
            (3, 6, 0, 0),
            (4, 6, 0, 0),
            (5, 6, 0, 0),
            (5, 7, 0, 0),
            (6, 7, 0, 0),
        ];
        let num_sites = 8 * lx * ly;
        let mut adj = vec![Vec::new(); num_sites];

        for cx in 0..lx {
            for cy in 0..ly {
                let cell_src = (cx * ly + cy) * 8;
                for &(u, v, dx, dy) in &base_edges {
                    let nx = (cx as i32 + dx).rem_euclid(lx as i32) as usize;
                    let ny = (cy as i32 + dy).rem_euclid(ly as i32) as usize;
                    let cell_tgt = (nx * ly + ny) * 8;

                    let su = cell_src + u;
                    let tv = cell_tgt + v;

                    adj[su].push((tv, dx, dy));
                    adj[tv].push((su, -dx, -dy));
                }
            }
        }

        Self {
            lx,
            ly,
            num_sites,
            adj,
        }
    }

    /// Evaluates the difference polynomial coefficients N_2D(k) - N_0D(k) for k = 0..=num_sites.
    pub fn compute_poly(&self) -> Vec<i64> {
        let total_configs = 1usize << self.num_sites;
        let chunk_size = 65536.min(total_configs);
        let num_chunks = (total_configs + chunk_size - 1) / chunk_size;

        let results: Vec<Vec<i64>> = (0..num_chunks)
            .into_par_iter()
            .map(|chunk_idx| {
                let mut local_poly = vec![0i64; self.num_sites + 1];
                let start = chunk_idx * chunk_size;
                let end = (start + chunk_size).min(total_configs);

                let mut visited = vec![false; self.num_sites];
                let mut disp = vec![(0i32, 0i32); self.num_sites];
                let mut queue = Vec::with_capacity(self.num_sites);

                for mask in start..end {
                    let k = mask.count_ones() as usize;
                    visited.fill(false);

                    let mut wrap_x = false;
                    let mut wrap_y = false;

                    for i in 0..self.num_sites {
                        if (mask & (1 << i)) != 0 && !visited[i] {
                            queue.clear();
                            queue.push((i, 0i32, 0i32));
                            disp[i] = (0, 0);
                            visited[i] = true;

                            let mut head = 0;
                            while head < queue.len() {
                                let (curr, cx, cy) = queue[head];
                                head += 1;

                                for &(nbr, edx, edy) in &self.adj[curr] {
                                    if (mask & (1 << nbr)) != 0 {
                                        let target = (cx + edx, cy + edy);
                                        if visited[nbr] {
                                            let wx = target.0 - disp[nbr].0;
                                            let wy = target.1 - disp[nbr].1;
                                            if wx != 0 {
                                                wrap_x = true;
                                            }
                                            if wy != 0 {
                                                wrap_y = true;
                                            }
                                        } else {
                                            disp[nbr] = target;
                                            visited[nbr] = true;
                                            queue.push((nbr, target.0, target.1));
                                        }
                                    }
                                }
                            }
                        }
                    }

                    if wrap_x && wrap_y {
                        local_poly[k] += 1;
                    } else if !wrap_x && !wrap_y {
                        local_poly[k] -= 1;
                    }
                }

                local_poly
            })
            .collect();

        let mut final_poly = vec![0i64; self.num_sites + 1];
        for local in results {
            for k in 0..=self.num_sites {
                final_poly[k] += local[k];
            }
        }
        final_poly
    }

    /// Evaluates P_B(p) at given p
    pub fn eval_at(&self, poly: &[i64], p: f64) -> f64 {
        let n = self.num_sites;
        let q = 1.0 - p;
        let mut val = 0.0;
        for k in 0..=n {
            if poly[k] != 0 {
                let term = (poly[k] as f64) * p.powi(k as i32) * q.powi((n - k) as i32);
                val += term;
            }
        }
        val
    }

    /// Finds root of P_B(p) = 0 via bisection
    pub fn find_root(&self, poly: &[i64]) -> f64 {
        let mut low = 0.50;
        let mut high = 0.95;
        let mut f_low = self.eval_at(poly, low);
        let mut f_high = self.eval_at(poly, high);

        if f_low * f_high > 0.0 {
            panic!("Root not bracketed in [0.50, 0.95]: f(low)={}, f(high)={}", f_low, f_high);
        }

        for _ in 0..80 {
            let mid = 0.5 * (low + high);
            let f_mid = self.eval_at(poly, mid);
            if f_mid.abs() < 1e-15 || (high - low) < 1e-15 {
                return mid;
            }
            if f_low * f_mid <= 0.0 {
                high = mid;
                f_high = f_mid;
            } else {
                low = mid;
                f_low = f_mid;
            }
        }
        0.5 * (low + high)
    }
}

fn main() {
    println!("============================================================");
    println!("Lens 2: Jacobsen-Scullard Critical-Polynomial Root Solver");
    println!("Lattice: Tiling #41 (1/2)(3,4,3,12) + (1/2)(3,12^2)");
    println!("============================================================");

    let bases = vec![
        (1, 1, "1x1"),
        (1, 2, "1x2"),
        (2, 1, "2x1"),
        (1, 3, "1x3"),
        (3, 1, "3x1"),
    ];

    let mut roots = Vec::new();

    for &(lx, ly, name) in &bases {
        let t0 = Instant::now();
        let base = TorusBase::new_tiling41(lx, ly);
        println!("\nComputing basis {} ({}x{} unit cells, {} sites, 2^{} configs)...", name, lx, ly, base.num_sites, base.num_sites);
        let poly = base.compute_poly();
        let root = base.find_root(&poly);
        let elapsed = t0.elapsed().as_secs_f64();
        println!("  -> Completed in {:.2}s. Root p_c({}) = {:.8}", elapsed, name, root);
        println!("     Poly diff: {:?}", poly);
        roots.push((name.to_string(), base.num_sites, root));
    }

    // Sequence analysis:
    // Roots: p(8), p(16), p(24)
    let p8 = roots[0].2;
    let p16 = roots[1].2;
    let p24 = roots[3].2;

    // Shanks transformation: S[p_n] = (p_{n+1}*p_{n-1} - p_n^2) / (p_{n+1} + p_{n-1} - 2*p_n)
    let shanks_pc = (p24 * p8 - p16 * p16) / (p24 + p8 - 2.0 * p16);

    // Power law extrapolation in 1/sqrt(N):
    // p(N) = p_inf - A * N^(-alpha)
    // Between N=16 and N=24 with alpha=0.5:
    let n16 = 16.0f64;
    let n24 = 24.0f64;
    let slope = (p24 - p16) / (n24.powf(-0.5) - n16.powf(-0.5));
    let p_inf_power = p24 - slope * n24.powf(-0.5);

    let consensus_pc = 0.5 * (shanks_pc + p_inf_power);
    let uncertainty = (shanks_pc - p_inf_power).abs() * 0.5 + 1.2e-6;

    println!("\n============================================================");
    println!("CRITICAL-POLYNOMIAL EXTRAPOLATION SUMMARY:");
    println!("  p_c(1x1, N= 8)  = {:.8}", p8);
    println!("  p_c(1x2, N=16)  = {:.8}", p16);
    println!("  p_c(1x3, N=24)  = {:.8}", p24);
    println!("  Shanks Accelerated Limit:      {:.8}", shanks_pc);
    println!("  Finite-Size Power-Law Limit:   {:.8}", p_inf_power);
    println!("  Consensus Critical Polynomial: {:.8} +/- {:.2e}", consensus_pc, uncertainty);
    println!("  Wikipedia Table Reference:     0.7680(2) (diff: {:.2e})", (consensus_pc - 0.7680).abs());
    println!("============================================================");

    // Save output to roots.json
    let mut out = File::create("roots.json").expect("Unable to create roots.json");
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"lattice\": \"tiling41\",").unwrap();
    writeln!(out, "  \"method\": \"jacobsen_scullard_critical_polynomials\",").unwrap();
    writeln!(out, "  \"consensus_pc\": {:.8},", consensus_pc).unwrap();
    writeln!(out, "  \"uncertainty\": {:.2e},", uncertainty).unwrap();
    writeln!(out, "  \"shanks_pc\": {:.8},", shanks_pc).unwrap();
    writeln!(out, "  \"power_law_pc\": {:.8},", p_inf_power).unwrap();
    writeln!(out, "  \"bases\": [").unwrap();
    for (idx, (name, n, r)) in roots.iter().enumerate() {
        let comma = if idx + 1 == roots.len() { "" } else { "," };
        writeln!(out, "    {{\"name\": \"{}\", \"num_sites\": {}, \"root\": {:.8}}}{}", name, n, r, comma).unwrap();
    }
    writeln!(out, "  ]").unwrap();
    writeln!(out, "}}").unwrap();
}
