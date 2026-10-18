// Eulerian orientations of the n x n torus (OEIS A054759) = trace(T^n) of the six-vertex row transfer matrix,
// computed modulo several primes with a cell-by-cell (broken-profile) sweep.
// Edge bits: v[r][c] = 1 means the arrow goes (r,c) -> (r+1,c); h[r][c] = 1 means (r,c) -> (r,c+1).
// Ice rule at (r,c): out-degree 2  <=>  v[r][c] + h[r][c] = v[r-1][c] + h[r][c-1].
// Mode A sweeps each row left-to-right and uses the symmetry group (shifts x reflection x global reversal).
// Mode B sweeps right-to-left with the other recursion and uses only cyclic shifts.
// Usage: ice <A|B> <n> <threads> <p1> [p2 ...]   prints one residue per prime.
use std::env;
use std::sync::{Arc, Mutex};
use std::thread;

fn rot(s: u32, k: u32, n: u32) -> u32 {
    let m = (1u32 << n) - 1;
    if k == 0 { s } else { ((s << k) | (s >> (n - k))) & m }
}
fn refl(s: u32, n: u32) -> u32 {
    let mut r = 0;
    for i in 0..n { if s >> i & 1 == 1 { r |= 1 << (n - 1 - i); } }
    r
}

fn images(s: u32, n: u32, full: bool) -> Vec<u32> {
    let m = (1u32 << n) - 1;
    let mut v = Vec::new();
    for k in 0..n {
        let a = rot(s, k, n);
        v.push(a);
        if full { v.push(refl(a, n)); v.push(!a & m); v.push(refl(!a & m, n)); }
    }
    v.sort(); v.dedup();
    v
}

fn diag_count(s: u32, n: u32, mode_a: bool, ps: &[u64], cur: &mut Vec<u64>, nxt: &mut Vec<u64>) -> Vec<u64> {
    let k = ps.len();
    let nb = 1usize << n;
    let ns = nb << 2; // bits | hb<<n | x0<<(n+1)
    // row vector over vertical bits
    let mut row = vec![0u64; nb * k];
    for j in 0..k { row[s as usize * k + j] = 1; }
    for _r in 0..n {
        for x in cur.iter_mut() { *x = 0; }
        for b in 0..nb {
            if row[b * k..b * k + k].iter().all(|&x| x == 0) { continue; }
            for x in 0..2usize {
                let idx = b | (x << n) | (x << (n + 1));
                for j in 0..k { cur[idx * k + j] = row[b * k + j]; }
            }
        }
        for step in 0..n {
            let c = if mode_a { step } else { n - 1 - step };
            for x in nxt.iter_mut() { *x = 0; }
            for idx in 0..ns {
                let base = idx * k;
                if cur[base..base + k].iter().all(|&x| x == 0) { continue; }
                let bits = idx & (nb - 1);
                let hb = (idx >> n) & 1;
                let x0 = idx >> (n + 1);
                let in_v = (bits >> c) & 1;
                for nv in 0..2usize {
                    // A: h[r][c] = in_v + h[r][c-1] - nv ;  B: h[r][c-1] = nv + h[r][c] - in_v
                    let t = if mode_a { (in_v + hb) as isize - nv as isize } else { (nv + hb) as isize - in_v as isize };
                    if t < 0 || t > 1 { continue; }
                    let nidx = ((bits & !(1 << c)) | (nv << c)) | ((t as usize) << n) | (x0 << (n + 1));
                    let nb2 = nidx * k;
                    for j in 0..k {
                        let mut y = nxt[nb2 + j] + cur[base + j];
                        if y >= ps[j] { y -= ps[j]; }
                        nxt[nb2 + j] = y;
                    }
                }
            }
            std::mem::swap(cur, nxt);
        }
        for x in row.iter_mut() { *x = 0; }
        for idx in 0..ns {
            let hb = (idx >> n) & 1;
            let x0 = idx >> (n + 1);
            if hb != x0 { continue; }
            let b = idx & (nb - 1);
            for j in 0..k {
                let mut y = row[b * k + j] + cur[idx * k + j];
                if y >= ps[j] { y -= ps[j]; }
                row[b * k + j] = y;
            }
        }
    }
    (0..k).map(|j| row[s as usize * k + j]).collect()
}

fn main() {
    let a: Vec<String> = env::args().collect();
    let mode_a = a[1] == "A";
    let n: u32 = a[2].parse().unwrap();
    let threads: usize = a[3].parse().unwrap();
    let ps: Vec<u64> = a[4..].iter().map(|x| x.parse().unwrap()).collect();
    for &p in &ps { assert!(p < (1u64 << 62)); }
    let mut reps: Vec<(u32, u64)> = Vec::new();
    for s in 0..(1u32 << n) {
        let im = images(s, n, mode_a);
        if im[0] == s { reps.push((s, im.len() as u64)); }
    }
    eprintln!("mode {} n {} reps {}", a[1], n, reps.len());
    let reps = Arc::new(reps);
    let next = Arc::new(Mutex::new(0usize));
    let total = Arc::new(Mutex::new(vec![0u64; ps.len()]));
    let mut hs = Vec::new();
    for _ in 0..threads {
        let (reps, next, total, ps) = (reps.clone(), next.clone(), total.clone(), ps.clone());
        hs.push(thread::spawn(move || {
            let k = ps.len();
            let ns = (1usize << n) << 2;
            let mut cur = vec![0u64; ns * k];
            let mut nxt = vec![0u64; ns * k];
            let mut local = vec![0u64; k];
            loop {
                let i = { let mut g = next.lock().unwrap(); let i = *g; *g += 1; i };
                if i >= reps.len() { break; }
                let (s, w) = reps[i];
                let d = diag_count(s, n, mode_a, &ps, &mut cur, &mut nxt);
                for j in 0..k {
                    local[j] = ((local[j] as u128 + d[j] as u128 * w as u128) % ps[j] as u128) as u64;
                }
            }
            let mut t = total.lock().unwrap();
            for j in 0..k { t[j] = ((t[j] as u128 + local[j] as u128) % ps[j] as u128) as u64; }
        }));
    }
    for h in hs { h.join().unwrap(); }
    let t = total.lock().unwrap();
    for j in 0..ps.len() { println!("{} {}", ps[j], t[j]); }
}
