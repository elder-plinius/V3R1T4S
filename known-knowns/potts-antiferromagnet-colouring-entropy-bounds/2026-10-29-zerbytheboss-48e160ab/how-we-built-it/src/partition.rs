use std::collections::HashMap;

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct Partition {
    pub blocks: Vec<u8>,        // blocks[v] in 0..num_blocks-1
    pub block_masks: Vec<u64>,  // block_masks[b] has bit v set
    pub num_blocks: usize,
    pub orbit_id: usize,
}

impl Partition {
    pub fn new(blocks: Vec<u8>) -> Self {
        let num_blocks = (blocks.iter().cloned().max().unwrap_or(0) as usize) + 1;
        let mut block_masks = vec![0u64; num_blocks];
        for (v, &b) in blocks.iter().enumerate() {
            block_masks[b as usize] |= 1u64 << v;
        }
        Partition {
            blocks,
            block_masks,
            num_blocks,
            orbit_id: 0,
        }
    }
}

pub fn get_proper_partitions(edges: &[(usize, usize)], n: usize, q: usize) -> Vec<Partition> {
    let mut results = Vec::new();
    let mut curr = vec![0u8; n];

    fn dfs(
        idx: usize,
        max_b: i32,
        curr: &mut Vec<u8>,
        edges: &[(usize, usize)],
        n: usize,
        q: usize,
        results: &mut Vec<Partition>,
    ) {
        if idx == n {
            results.push(Partition::new(curr.clone()));
            return;
        }
        let limit = ((max_b + 2) as usize).min(q);
        for b in 0..limit {
            let mut conflict = false;
            for &(u, v) in edges {
                if u == idx && v < idx && curr[v] == b as u8 {
                    conflict = true;
                    break;
                }
                if v == idx && u < idx && curr[u] == b as u8 {
                    conflict = true;
                    break;
                }
            }
            if !conflict {
                curr[idx] = b as u8;
                let next_max = max_b.max(b as i32);
                dfs(idx + 1, next_max, curr, edges, n, q, results);
            }
        }
    }

    dfs(0, -1, &mut curr, edges, n, q, &mut results);
    results
}

pub fn group_into_orbits(
    partitions: &mut [Partition],
    aut_group: &[Vec<usize>],
    n: usize,
) -> Vec<Vec<Partition>> {
    let mut orbit_map: HashMap<Vec<u8>, usize> = HashMap::new();
    let mut orbits: Vec<Vec<Partition>> = Vec::new();
    let mut mapping = vec![255u8; 16];

    for part in partitions.iter_mut() {
        let mut min_canon: Option<Vec<u8>> = None;

        for pi in aut_group {
            mapping.fill(255);
            let mut next_lbl = 0u8;
            let mut canon = Vec::with_capacity(n);

            for v in 0..n {
                let orig_b = part.blocks[pi[v]];
                let mapped = mapping[orig_b as usize];
                if mapped == 255 {
                    mapping[orig_b as usize] = next_lbl;
                    canon.push(next_lbl);
                    next_lbl += 1;
                } else {
                    canon.push(mapped);
                }
            }

            match &min_canon {
                None => min_canon = Some(canon),
                Some(best) => {
                    if &canon < best {
                        min_canon = Some(canon);
                    }
                }
            }
        }

        let key = min_canon.unwrap();
        let orbit_idx = match orbit_map.get(&key) {
            Some(&idx) => idx,
            None => {
                let idx = orbits.len();
                orbit_map.insert(key, idx);
                orbits.push(Vec::new());
                idx
            }
        };
        part.orbit_id = orbit_idx;
        orbits[orbit_idx].push(part.clone());
    }

    orbits
}
