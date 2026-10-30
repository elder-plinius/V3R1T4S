//! Symmetry group G_{m,n} = V_{m,n} \rtimes K_{m,n}
//! and orbit partitioning for diagonal transfer matrices.

use std::collections::HashSet;

#[derive(Clone, Debug)]
pub struct LatticeGroup {
    pub m: usize,
    pub n: usize,
    pub num_vertices: usize,
    /// Permutations of vertices for all g \in G_{m,n}.
    /// Each element is a Vec<usize> of length num_vertices.
    pub group_perms: Vec<Vec<usize>>,
    /// D displacements in vertex indices: for each d in D, map from vertex v to v + d.
    pub d_maps: Vec<Vec<usize>>,
    pub d_vectors: Vec<(i32, i32)>,
}

impl LatticeGroup {
    pub fn new(m: usize, n: usize) -> Self {
        let num_vertices = m * n;
        assert!(num_vertices <= 32, "Bitmask requires <= 32 vertices");

        let v_idx = |x: usize, y: usize| -> usize { x * n + y };
        let idx_to_v = |idx: usize| -> (usize, usize) { (idx / n, idx % n) };

        // Automorphisms of V_{m,n} preserving D up to translation (He 2026, Table 1):
        // 1. (x, y) (always)
        // 2. (y, x) (if m == n)
        // 3. (-x - y, y) (if n % m == 0)
        // 4. (-x - y, x) (if m == n)
        // 5. (x, -x - y) (if m % n == 0)
        // 6. (y, -x - y) (if m == n)
        let mut automorphisms: Vec<Box<dyn Fn(i32, i32) -> (i32, i32)>> = Vec::new();

        // 1.
        automorphisms.push(Box::new(|x, y| (x, y)));
        // 2.
        if m == n {
            automorphisms.push(Box::new(|x, y| (y, x)));
        }
        // 3.
        if n % m == 0 {
            automorphisms.push(Box::new(|x, y| (-x - y, y)));
        }
        // 4.
        if m == n {
            automorphisms.push(Box::new(|x, y| (-x - y, x)));
        }
        // 5.
        if m % n == 0 {
            automorphisms.push(Box::new(|x, y| (x, -x - y)));
        }
        // 6.
        if m == n {
            automorphisms.push(Box::new(|x, y| (y, -x - y)));
        }

        let m_i = m as i32;
        let n_i = n as i32;

        let mut group_perms = Vec::new();
        for a in 0..m {
            for b in 0..n {
                let a_i = a as i32;
                let b_i = b as i32;
                for phi in &automorphisms {
                    let mut perm = vec![0; num_vertices];
                    for idx in 0..num_vertices {
                        let (vx, vy) = idx_to_v(idx);
                        let (px, py) = phi(vx as i32, vy as i32);
                        let im_x = (px + a_i).rem_euclid(m_i) as usize;
                        let im_y = (py + b_i).rem_euclid(n_i) as usize;
                        perm[idx] = v_idx(im_x, im_y);
                    }
                    group_perms.push(perm);
                }
            }
        }

        // D = {(0,0), (1,0), (0,1)}
        let d_vectors = vec![(0, 0), (1, 0), (0, 1)];
        let mut d_maps = Vec::new();
        for &(dx, dy) in &d_vectors {
            let mut map = vec![0; num_vertices];
            for idx in 0..num_vertices {
                let (vx, vy) = idx_to_v(idx);
                let tx = ((vx as i32 + dx).rem_euclid(m_i)) as usize;
                let ty = ((vy as i32 + dy).rem_euclid(n_i)) as usize;
                map[idx] = v_idx(tx, ty);
            }
            d_maps.push(map);
        }

        Self {
            m,
            n,
            num_vertices,
            group_perms,
            d_maps,
            d_vectors,
        }
    }

    /// Map a bitmask under group element g.
    #[inline(always)]
    pub fn apply_g(&self, mask: u32, perm: &[usize]) -> u32 {
        let mut res = 0u32;
        let mut m = mask;
        while m > 0 {
            let v = m.trailing_zeros() as usize;
            m &= m - 1;
            res |= 1 << perm[v];
        }
        res
    }

    /// Compute canonical minimum representative of a bitmask.
    #[inline(always)]
    pub fn canonical(&self, mask: u32) -> u32 {
        let mut min_mask = mask;
        for perm in &self.group_perms {
            let im = self.apply_g(mask, perm);
            if im < min_mask {
                min_mask = im;
            }
        }
        min_mask
    }

    /// Compute full orbit of a bitmask.
    pub fn orbit_of(&self, mask: u32) -> Vec<u32> {
        let mut set = HashSet::new();
        for perm in &self.group_perms {
            set.insert(self.apply_g(mask, perm));
        }
        let mut list: Vec<u32> = set.into_iter().collect();
        list.sort_unstable();
        list
    }
}

/// Combinadic ranking/unranking for fast O(1) table indexing of subsets of size k.
#[derive(Clone, Debug)]
pub struct Combinadic {
    pub n: usize,
    pub k: usize,
    c: Vec<Vec<usize>>,
    pub total_combinations: usize,
}

impl Combinadic {
    pub fn new(n: usize, k: usize) -> Self {
        let mut c = vec![vec![0; k + 2]; n + 2];
        for i in 0..=n {
            c[i][0] = 1;
            for j in 1..=k.min(i) {
                c[i][j] = c[i - 1][j - 1] + c[i - 1][j];
            }
        }
        let total = c[n][k];
        Self {
            n,
            k,
            c,
            total_combinations: total,
        }
    }

    #[inline(always)]
    pub fn rank(&self, mask: u32) -> usize {
        let mut r = 0;
        let mut m = mask;
        let mut ones_seen = 0;
        while m > 0 {
            let tz = m.trailing_zeros() as usize;
            m &= m - 1;
            ones_seen += 1;
            r += self.c[tz][ones_seen];
        }
        r
    }
}

/// Orbit table for a given sector size k.
pub struct SectorOrbits {
    pub size_k: usize,
    pub canonical_reps: Vec<u32>,
    pub orbit_sizes: Vec<usize>,
    pub combinadic: Combinadic,
    /// Maps combinadic rank -> orbit ID in 0..canonical_reps.len().
    pub rank_to_orbit: Vec<u32>,
}

impl SectorOrbits {
    pub fn build(lattice: &LatticeGroup, k: usize) -> Self {
        let n = lattice.num_vertices;
        let comb = Combinadic::new(n, k);
        let mut rank_to_orbit = vec![u32::MAX; comb.total_combinations];
        let mut canonical_reps = Vec::new();
        let mut orbit_sizes = Vec::new();

        // Enumerate all subsets of size k using Gosper's hack
        if k == 0 {
            canonical_reps.push(0);
            orbit_sizes.push(1);
            rank_to_orbit[0] = 0;
            return Self {
                size_k: k,
                canonical_reps,
                orbit_sizes,
                combinadic: comb,
                rank_to_orbit,
            };
        }

        let mut mask = (1u32 << k) - 1;
        let limit = 1u32 << n;
        while mask < limit {
            let r = comb.rank(mask);
            if rank_to_orbit[r] == u32::MAX {
                let orbit = lattice.orbit_of(mask);
                let oid = canonical_reps.len() as u32;
                canonical_reps.push(orbit[0]);
                orbit_sizes.push(orbit.len());
                for &m in &orbit {
                    let r_m = comb.rank(m);
                    rank_to_orbit[r_m] = oid;
                }
            }
            // Gosper's hack
            let c = mask & (!mask + 1);
            let r_bits = mask + c;
            mask = (((r_bits ^ mask) >> 2) / c) | r_bits;
        }

        Self {
            size_k: k,
            canonical_reps,
            orbit_sizes,
            combinadic: comb,
            rank_to_orbit,
        }
    }

    #[inline(always)]
    pub fn get_orbit(&self, mask: u32) -> usize {
        let r = self.combinadic.rank(mask);
        self.rank_to_orbit[r] as usize
    }

    pub fn num_orbits(&self) -> usize {
        self.canonical_reps.len()
    }
}
